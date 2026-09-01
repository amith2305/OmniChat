"""Health endpoint: reports backend + AI stack availability."""
from fastapi import APIRouter

from app import config
from app.llm.ollama import OllamaClient
from app.rag.embeddings import embedding_service
from app.rag.vector_store import vector_store
from app.services.ocr import ocr_service
from app.services.vision import vision_service
from app.services.whisper import whisper_service

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def health():
    ollama_client = OllamaClient()
    ollama_ok = ollama_client.is_available()
    models = []
    try:
        models = ollama_client.list_models()
    except Exception:  # noqa: BLE001
        pass

    whisper_ok = True
    try:
        whisper_service._ensure_model()
    except Exception:  # noqa: BLE001
        whisper_ok = False

    try:
        embed_backend = embedding_service.backend
    except Exception:  # noqa: BLE001
        embed_backend = "unavailable"

    return {
        "status": "ok",
        "ollama": {
            "available": ollama_ok,
            "base_url": config.OLLAMA_BASE_URL,
            "models": models,
            "llm_model": config.LLM_MODEL,
            "vision_model": config.VISION_MODEL,
            "llm_ready": config.LLM_MODEL in models or any(m.split(":")[0] == config.LLM_MODEL.split(":")[0] for m in models),
            "vision_ready": any(m.split(":")[0] == config.VISION_MODEL.split(":")[0] for m in models),
        },
        "embeddings": {
            "backend": embed_backend,
            "model": config.EMBEDDING_MODEL,
            "fallback": config.EMBEDDING_FALLBACK_OLLAMA,
        },
        "whisper": {"model": config.WHISPER_MODEL, "ready": whisper_ok},
        "tesseract": {"available": ocr_service.is_available()},
        "chroma": {"chunks": vector_store.count()},
        "python": {"model": config.EMBEDDING_MODEL},
    }
