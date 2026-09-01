"""File validation helpers (extension + magic bytes + size)."""
import os

from app.utils.logging import get_logger

log = get_logger("[VALIDATE]")


class ValidationError(RuntimeError):
    pass


_MAGIC: dict[str, tuple[bytes, int]] = {
    ".pdf": (b"%PDF", 0),
    ".png": (b"\x89PNG\r\n\x1a\n", 0),
    ".jpg": (b"\xff\xd8\xff", 0),
    ".jpeg": (b"\xff\xd8\xff", 0),
    ".mp3": (b"ID3", 0),
    ".wav": (b"RIFF", 0),
    ".m4a": (b"\x00\x00\x00", 4),
    ".mp4": (b"ftyp", 4),
    ".mkv": (b"\x1aE\xdf\xa3", 0),
}


def validate_upload(filename: str, content: bytes, media_type: str) -> None:
    from pathlib import Path
    ext = Path(filename).suffix.lower()

    max_size = 500 * 1024 * 1024
    if len(content) > max_size:
        raise ValidationError(f"File is too large (max {max_size // (1024 * 1024)} MB).")

    if media_type == "pdf" and ext != ".pdf":
        raise ValidationError("PDF uploads must use the .pdf extension.")
    if media_type == "document" and ext not in (".txt", ".md", ".rtf", ".doc", ".docx"):
        raise ValidationError(f"Unsupported document extension '{ext}'.")
    if media_type == "data" and ext not in (".csv", ".tsv", ".json", ".xlsx", ".xls"):
        raise ValidationError(f"Unsupported data extension '{ext}'.")
    if media_type == "image" and ext not in (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"):
        raise ValidationError(f"Unsupported image extension '{ext}'.")
    if media_type == "audio" and ext not in (".mp3", ".wav", ".m4a", ".ogg", ".aac", ".flac"):
        raise ValidationError(f"Unsupported audio extension '{ext}'.")
    if media_type == "video" and ext not in (".mp4", ".mkv", ".avi", ".mov", ".webm", ".wmv"):
        raise ValidationError(f"Unsupported video extension '{ext}'.")

    if len(content) == 0:
        raise ValidationError("File is empty.")

    if ext == ".webp":
        return

    sig, off = _MAGIC.get(ext, (b"", 0))
    if sig and content[off:off + len(sig)] != sig:
        raise ValidationError(f"File content does not match the '{ext}' format (corrupted or wrong extension).")
