"""Multimodal chunking: PDFs by paragraph/page, audio/video by time, images by description.

Every processor returns a flat list of chunks using this common schema:

{
    "id": str,
    "content": str,
    "type": "pdf" | "image" | "audio" | "video_transcript" | "video_frame",
    "source": str,            # original file name
    "page": int | None,
    "start_time": float | None,
    "end_time": float | None,
    "metadata": dict,
}
"""
import re
import uuid

from app import config
from app.utils.logging import get_logger

log = get_logger("[CHUNK]")


def new_chunk_id() -> str:
    return uuid.uuid4().hex


def make_chunk(content: str, ctype: str, source: str, *, page: int | None = None,
               start_time: float | None = None, end_time: float | None = None,
               metadata: dict | None = None) -> dict:
    return {
        "id": new_chunk_id(),
        "content": content,
        "type": ctype,
        "source": source,
        "page": page,
        "start_time": start_time,
        "end_time": end_time,
        "metadata": metadata or {},
    }


def _clean(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _window_split(text: str, size: int = None, overlap: int = None) -> list[str]:
    """Sliding-window character split that prefers paragraph boundaries."""
    size = size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP
    text = _clean(text)
    if not text:
        return []
    if len(text) <= size:
        return [text]

    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    if not paragraphs:
        paragraphs = [text]

    chunks: list[str] = []
    buffer = ""
    for para in paragraphs:
        para = para.strip()
        if len(para) > size:
            if buffer:
                chunks.append(buffer)
                buffer = ""
            for i in range(0, len(para), size - overlap):
                piece = para[i:i + size]
                if piece:
                    chunks.append(piece)
            continue
        if len(buffer) + len(para) + 2 > size and buffer:
            chunks.append(buffer)
            tail = buffer[-overlap:] if overlap else ""
            buffer = tail + "\n\n" if tail else ""
        buffer = (buffer + "\n\n" + para).strip()
    if buffer:
        chunks.append(buffer)
    return chunks


def chunk_pdf_text(text: str, source: str, page: int) -> list[dict]:
    """Chunk one page of PDF text into paragraph-aware chunks."""
    parts = _window_split(text)
    chunks = []
    for i, part in enumerate(parts):
        chunks.append(make_chunk(part, "pdf", source, page=page,
                                 metadata={"page": page, "index": i, "chars": len(part)}))
    return chunks


def chunk_audio_transcript(segments: list[dict], source: str, ctype: str = "audio") -> list[dict]:
    """Group timestamped transcription segments into time-based chunks.

    segments: list of {"text", "start", "end"}
    """
    chunks = []
    buffer = ""
    start_t = None
    end_t = None
    size = config.CHUNK_SIZE

    def flush():
        nonlocal buffer, start_t, end_t
        if buffer.strip():
            chunks.append(make_chunk(buffer.strip(), ctype, source,
                                     start_time=start_t, end_time=end_t,
                                     metadata={"chars": len(buffer)}))
        buffer = ""
        start_t = None
        end_t = None

    for seg in segments:
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        if start_t is None:
            start_t = float(seg.get("start", 0.0))
        end_t = float(seg.get("end", start_t))
        if len(buffer) + len(text) + 1 > size and buffer:
            flush()
            start_t = float(seg.get("start", 0.0))
        buffer = (buffer + " " + text).strip()

    flush()
    if not chunks and segments:
        chunks.append(make_chunk(" ".join(s.get("text", "") for s in segments), ctype, source,
                                 start_time=float(segments[0].get("start", 0.0)),
                                 end_time=float(segments[-1].get("end", 0.0)),
                                 metadata={"chars": 0}))
    return chunks


def chunk_frame(description: str, source: str, ts: float, duration: float = 1.0) -> dict:
    """One chunk per video frame description."""
    return make_chunk(description, "video_frame", source,
                      start_time=ts, end_time=ts + duration,
                      metadata={"ts": ts, "chars": len(description)})


def chunk_image(description: str, source: str, image_rel_path: str | None = None) -> dict:
    return make_chunk(description, "image", source,
                      metadata={"image_path": image_rel_path, "chars": len(description)})
