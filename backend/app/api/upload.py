"""Upload endpoint: validate, save, process asynchronously, track status."""
import asyncio
import os

from fastapi import APIRouter, File, HTTPException, UploadFile

from app import config
from app.api.jobs import jobs
from app.processors.audio_processor import process_audio
from app.processors.data_processor import process_data
from app.processors.document_processor import process_document
from app.processors.image_processor import process_image
from app.processors.pdf_processor import process_pdf
from app.processors.video_processor import process_video
from app.rag.pipeline import index_chunks
from app.rag.vector_store import vector_store
from app.utils.files import save_upload
from app.utils.logging import get_logger
from app.utils.validation import validate_upload

log = get_logger("[API]")

router = APIRouter(prefix="/api", tags=["upload"])

PROCESSORS = {
    "pdf": process_pdf,
    "document": process_document,
    "data": process_data,
    "image": process_image,
    "audio": process_audio,
    "video": process_video,
}


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename or "upload"
    media_type = config.classify_file(filename)
    if media_type is None:
        raise HTTPException(status_code=400, detail=f"Unsupported file type '{filename}'. "
                                                    "Supported: .pdf .png .jpg .jpeg .webp .mp3 .wav .m4a .mp4 .mkv")

    content = await file.read()
    try:
        validate_upload(filename, content, media_type)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    file_id, path = save_upload(filename, content)
    job = jobs.create(file_id, filename, media_type)

    asyncio.get_running_loop().run_in_executor(
        None, _process_upload, file_id, path, media_type, filename
    )
    return {"file_id": file_id, "filename": filename, "type": media_type, "status": "processing"}


def _process_upload(file_id: str, path: str, media_type: str, filename: str) -> None:
    try:
        jobs.update(file_id, status="processing", message="Processing...", progress=5)
        processor = PROCESSORS[media_type]
        chunks = processor(path, progress=jobs.progress_fn(file_id))
        jobs.update(file_id, message="Creating embeddings and indexing...", progress=80)
        n = index_chunks(chunks)
        jobs.update(file_id, status="done", message="Ready", progress=100, chunks=n)
        log.info("[UPLOAD] finished %s: %d chunks indexed", filename, n)
    except Exception as exc:  # noqa: BLE001
        log.error("[UPLOAD] failed %s: %s", filename, exc)
        jobs.update(file_id, status="error", message="Failed", error=str(exc))


@router.get("/upload/{file_id}/status")
def upload_status(file_id: str):
    job = jobs.get(file_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Unknown file id.")
    return job


@router.get("/files")
def list_files():
    sources = vector_store.list_sources()
    for s in sources:
        rel = None
        src = s["source"]
        for d, name in ((config.UPLOAD_DIR, "uploads"), (config.PROCESSED_DIR, "processed")):
            for f in d.iterdir():
                if f.name.endswith(f"_{src}") or f.name == src:
                    rel = f"{name}/{f.name}"
                    break
            if rel:
                break
        s["url"] = rel
    return {"sources": sources}


@router.delete("/files/{source:path}")
def delete_file(source: str):
    n = vector_store.delete_source(source)
    if n == 0:
        raise HTTPException(status_code=404, detail="Source not found in index.")
    for d in (config.UPLOAD_DIR, config.PROCESSED_DIR):
        for f in d.iterdir():
            if f.name.endswith(f"_{source}"):
                try:
                    os.remove(f)
                except OSError:
                    pass
    return {"deleted": n, "source": source}
