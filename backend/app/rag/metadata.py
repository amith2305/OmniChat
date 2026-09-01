"""ChromaDB metadata sanitization.

ChromaDB 1.5.x (Rust core) rejects metadata values that are not plain
str/int/float/bool and rejects Python None values with
"argument 'metadatas': Cannot convert Python object to MetadataValue".

This module converts arbitrary Python values into ChromaDB-compatible
primitives before insertion:
  - None values are dropped (page/start_time/end_time may legitimately be absent)
  - Path/datetime/date objects become their string representation
  - lists/dicts/tuples/sets become lossless JSON strings
  - anything else becomes str(value)
"""
import json
from datetime import date, datetime
from pathlib import Path

from app.utils.logging import get_logger

log = get_logger("[CHROMA]")

_SCALARS = (str, int, float, bool)


def sanitize_value(key: str, value):
    """Convert one metadata value to a ChromaDB-compatible primitive (never None)."""
    if value is None:
        return None
    if isinstance(value, _SCALARS):
        return value
    if isinstance(value, (Path, datetime, date)):
        log.warning("[CHROMA] Invalid metadata value key=%s type=%s value=%r -> str()",
                    key, type(value).__name__, value)
        return str(value)
    log.warning("[CHROMA] Invalid metadata value key=%s type=%s value=%r -> JSON string",
                key, type(value).__name__, value)
    try:
        return json.dumps(value, ensure_ascii=False, default=str)
    except (TypeError, ValueError):
        return str(value)


def sanitize_metadata(metadata: dict | None) -> dict:
    """Return a copy of metadata containing only ChromaDB-compatible values."""
    if not metadata:
        return {}
    clean: dict = {}
    for key, value in metadata.items():
        key = str(key)
        converted = sanitize_value(key, value)
        if converted is None:
            continue
        clean[key] = converted
    return clean