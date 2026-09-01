"""Media endpoints: file serving, summarize, topics, export, STT, TTS."""
import json
import time
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app import config
from app.memory.conversation import memory
from app.rag.pipeline import extract_topics, summarize_source
from app.services.tts import text_to_speech
from app.services.whisper import whisper_service
from app.utils.files import format_time, save_upload
from app.utils.logging import get_logger
from app.utils.validation import validate_upload

log = get_logger("[API]")

router = APIRouter(prefix="/api", tags=["media"])

_SAFE_DIRS = ("uploads", "processed", "frames", "audio", "exports")

_MEDIA_TYPES = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".m4a": "audio/mp4",
    ".mp4": "video/mp4",
    ".mkv": "video/x-matroska",
    ".txt": "text/plain",
}


def _resolve_media(rel: str) -> Path:
    rel = rel.replace("\\", "/")
    parts = rel.split("/")
    if not parts or parts[0] not in _SAFE_DIRS:
        raise HTTPException(status_code=400, detail="Invalid media path.")
    path = (config.DATA_DIR / rel).resolve()
    if not str(path).startswith(str(config.DATA_DIR.resolve())):
        raise HTTPException(status_code=400, detail="Invalid media path.")
    if path.is_file():
        return path
    # Files are stored with a "{file_id}_" prefix; match on the requested name so
    # logical paths (e.g. "uploads/report.pdf") resolve to the stored file.
    if path.parent.is_dir():
        for candidate in path.parent.iterdir():
            if candidate.name == path.name or candidate.name.endswith(f"_{path.name}"):
                return candidate
    raise HTTPException(status_code=404, detail="File not found.")


@router.api_route("/media", methods=["GET", "HEAD"])
def media(rel: str):
    path = _resolve_media(rel)
    media_type = _MEDIA_TYPES.get(path.suffix.lower(), "application/octet-stream")
    # FileResponse handles HEAD natively: it stats the file and sends headers
    # (Content-Type, Content-Length, ...) without streaming the body.
    return FileResponse(path, media_type=media_type)


# -------------------------------------------------------------- summarize
class SummarizeRequest(BaseModel):
    source: str
    title: str | None = None


@router.post("/summarize")
def summarize(req: SummarizeRequest):
    try:
        result = summarize_source(req.source, req.title or req.source)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"source": req.source, "summary": result["summary"], "steps": result["steps"]}


# ----------------------------------------------------------------- topics
class TopicsRequest(BaseModel):
    source: str


@router.post("/topics")
def topics(req: TopicsRequest):
    try:
        result = extract_topics(req.source)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"source": req.source, "topics": result["topics"]}


# ----------------------------------------------------------------- export
class ExportRequest(BaseModel):
    kind: str = "chat"  # "chat" | "summary"
    format: str = "txt"  # "txt" | "pdf"
    session_id: str | None = None
    source: str | None = None
    summary: str | None = None


def _render_chat_txt(conv) -> str:
    lines = [f"OmniChat AI - Chat Export ({time.strftime('%Y-%m-%d %H:%M')})", "=" * 60]
    for turn in conv.to_list():
        role = "You" if turn["role"] == "user" else "OmniChat AI"
        lines.append(f"\n[{role}] ({time.strftime('%H:%M', time.localtime(turn['timestamp']))})")
        lines.append(turn["content"])
        if turn.get("sources"):
            lines.append("Sources:")
            for s in turn["sources"]:
                ref = s["source"]
                if s.get("page"):
                    ref += f" (page {s['page']})"
                if s.get("start_time") is not None:
                    ref += f" ({format_time(s['start_time'])} - {format_time(s['end_time'])})"
                lines.append(f"  - {ref}")
    return "\n".join(lines)


def _text_to_pdf(text: str, title: str, out_path: Path) -> None:
    import fitz
    doc = fitz.open()
    page = doc.new_page()
    y = 40
    page.insert_text((40, y), title, fontsize=14, fontname="helv")
    y += 24
    margin = 40
    width = page.rect.width - 80
    for para in text.split("\n"):
        if para.strip().startswith("==") or para.strip().startswith("OmniChat AI -"):
            y += 12
        fontsize = 10
        while para:
            line = ""
            for word in para.split():
                trial = line + " " + word if line else word
                if fitz.get_text_length(trial, fontname="helv", fontsize=fontsize) <= width:
                    line = trial
                else:
                    page.insert_text((margin, y), line, fontsize=fontsize, fontname="helv")
                    y += 14
                    line = word
                if y > page.rect.height - 40:
                    page = doc.new_page()
                    y = 40
            if line:
                page.insert_text((margin, y), line, fontsize=fontsize, fontname="helv")
                y += 14
            if y > page.rect.height - 40:
                page = doc.new_page()
                y = 40
    doc.save(str(out_path))
    doc.close()


@router.post("/export")
def export(req: ExportRequest):
    if req.format not in ("txt", "pdf"):
        raise HTTPException(status_code=400, detail="Format must be 'txt' or 'pdf'.")
    if req.kind not in ("chat", "summary"):
        raise HTTPException(status_code=400, detail="Kind must be 'chat' or 'summary'.")

    config.ensure_dirs()
    if req.kind == "summary":
        if not req.summary and req.source:
            try:
                req.summary = summarize_source(req.source, req.source)["summary"]
            except Exception as exc:  # noqa: BLE001
                raise HTTPException(status_code=500, detail=str(exc)) from exc
        content = f"OmniChat AI - Summary Export ({time.strftime('%Y-%m-%d %H:%M')})\n{'=' * 60}\n\n{req.summary}"
        title = "OmniChat AI Summary"
    else:
        if not req.session_id:
            raise HTTPException(status_code=400, detail="session_id required for chat export.")
        conv = memory.get(req.session_id)
        content = _render_chat_txt(conv)
        title = "OmniChat AI Chat Export"

    ext = "pdf" if req.format == "pdf" else "txt"
    out_path = config.EXPORTS_DIR / f"export_{uuid.uuid4().hex[:10]}.{ext}"
    if req.format == "pdf":
        _text_to_pdf(content, title, out_path)
    else:
        out_path.write_text(content, encoding="utf-8")

    log.info("[EXPORT] wrote %s", out_path)
    return {"url": f"exports/{out_path.name}", "filename": out_path.name, "content": content}


# --------------------------------------------------------------------- STT
@router.post("/stt")
async def stt(file: UploadFile = File(...)):
    filename = file.filename or "voice.webm"
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty recording.")
    if len(content) > 50 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Recording too large.")

    tmp = config.UPLOAD_DIR / f"stt_{uuid.uuid4().hex}.wav"
    tmp.write_bytes(content)
    try:
        result = whisper_service.transcribe(str(tmp))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Speech-to-text failed: {exc}") from exc
    finally:
        tmp.unlink(missing_ok=True)
    return {"text": result["text"]}


# --------------------------------------------------------------------- TTS
class TTSRequest(BaseModel):
    text: str


@router.post("/tts")
def tts(req: TTSRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    try:
        path = text_to_speech(req.text.strip())
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    rel = Path(path).relative_to(config.DATA_DIR)
    return {"url": f"{rel.as_posix()}"}
