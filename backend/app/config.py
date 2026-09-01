"""Application configuration loaded from environment variables / .env file."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATA_DIR = Path(os.getenv("DATA_DIR", str(BASE_DIR / "data")))

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", str(DATA_DIR / "uploads")))
PROCESSED_DIR = Path(os.getenv("PROCESSED_DIR", str(DATA_DIR / "processed")))
AUDIO_DIR = Path(os.getenv("AUDIO_DIR", str(DATA_DIR / "audio")))
FRAMES_DIR = Path(os.getenv("FRAMES_DIR", str(DATA_DIR / "frames")))
EXPORTS_DIR = Path(os.getenv("EXPORTS_DIR", str(DATA_DIR / "exports")))
CHROMA_DIR = Path(os.getenv("CHROMA_DIR", str(DATA_DIR / "chroma")))

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2:3b")
VISION_MODEL = os.getenv("VISION_MODEL", "gemma3:4b").strip() or "gemma3:4b"
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2").strip()
EMBEDDING_FALLBACK_OLLAMA = os.getenv("EMBEDDING_FALLBACK_OLLAMA", "nomic-embed-text").strip() or "nomic-embed-text"
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
WHISPER_COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")

TOP_K = int(os.getenv("TOP_K", "5"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))
VIDEO_FRAME_INTERVAL = float(os.getenv("VIDEO_FRAME_INTERVAL", "1"))
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "500"))
HISTORY_WINDOW = int(os.getenv("HISTORY_WINDOW", "8"))
OCR_MIN_TEXT_LENGTH = int(os.getenv("OCR_MIN_TEXT_LENGTH", "40"))
TESSERACT_CMD = os.getenv("TESSERACT_CMD", "tesseract")

SUPPORTED_EXTENSIONS = {
    "pdf": {"extensions": {".pdf"}, "type": "pdf"},
    "document": {"extensions": {".txt", ".md", ".rtf", ".doc", ".docx"}, "type": "document"},
    "data": {"extensions": {".csv", ".tsv", ".json", ".xlsx", ".xls"}, "type": "data"},
    "image": {"extensions": {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}, "type": "image"},
    "audio": {"extensions": {".mp3", ".wav", ".m4a", ".ogg", ".aac", ".flac"}, "type": "audio"},
    "video": {"extensions": {".mp4", ".mkv", ".avi", ".mov", ".webm", ".wmv"}, "type": "video"},
}


def ensure_dirs() -> None:
    for d in (UPLOAD_DIR, PROCESSED_DIR, AUDIO_DIR, FRAMES_DIR, EXPORTS_DIR, CHROMA_DIR):
        d.mkdir(parents=True, exist_ok=True)


def classify_file(filename: str) -> str | None:
    """Return the media type ('pdf' | 'image' | 'audio' | 'video') or None."""
    ext = Path(filename).suffix.lower()
    for kind, info in SUPPORTED_EXTENSIONS.items():
        if ext in info["extensions"]:
            return kind
    return None
