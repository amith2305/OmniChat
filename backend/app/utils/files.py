"""File storage helpers and common utilities."""
import re
import time
import uuid
from pathlib import Path

from app import config
from app.utils.logging import get_logger

log = get_logger("[FILE]")


def new_id() -> str:
    return uuid.uuid4().hex


def safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", name)


def save_upload(filename: str, content: bytes) -> tuple[str, str]:
    """Save an uploaded file into data/uploads. Returns (file_id, path)."""
    config.ensure_dirs()
    file_id = new_id()
    safe = safe_name(Path(filename).name)
    path = config.UPLOAD_DIR / f"{file_id}_{safe}"
    path.write_bytes(content)
    log.info("[UPLOAD] saved %s -> %s (%d bytes)", filename, path, len(content))
    return file_id, str(path)


def rel_path(path: str) -> str:
    """Turn an absolute path under data/ into a web-serveable relative path."""
    try:
        return str(Path(path).resolve().relative_to(config.DATA_DIR.resolve())).replace("\\", "/")
    except ValueError:
        return str(Path(path).resolve()).replace("\\", "/")


def format_time(seconds: float | None) -> str | None:
    """Format seconds as mm:ss (or hh:mm:ss for >= 1 hour)."""
    if seconds is None:
        return None
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def monotime() -> float:
    return time.time()
