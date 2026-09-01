"""Generic document processor for TXT/MD/RTF/DOC/DOCX-like content."""
import json
import os
import re
from pathlib import Path

from app.rag.chunker import make_chunk
from app.utils.logging import get_logger

log = get_logger("[DOCUMENT]")


def _read_text_bytes(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return Path(path).read_text(encoding="utf-8-sig")
        except Exception:
            return Path(path).read_bytes().decode("latin-1", errors="ignore")


def _extract_docx_text(path: str) -> str:
    try:
        import zipfile
        from xml.etree import ElementTree as ET

        with zipfile.ZipFile(path) as zf:
            xml = zf.read("word/document.xml")
        root = ET.fromstring(xml)
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        texts = []
        for para in root.findall(".//w:p", ns):
            pieces = [node.text for node in para.findall(".//w:t", ns) if node.text]
            if pieces:
                texts.append("".join(pieces))
        return "\n".join(texts)
    except Exception as exc:  # noqa: BLE001
        log.warning("DOCX extraction failed: %s", exc)
        return ""


def process_document(path: str, progress=None) -> list[dict]:
    def report(msg: str, pct: int | None = None):
        if progress:
            progress(msg, pct)

    source_name = os.path.basename(path)
    ext = Path(path).suffix.lower()
    report(f"Reading {source_name}...", 10)

    text = ""
    if ext == ".docx":
        text = _extract_docx_text(path)
    elif ext == ".doc":
        text = ""  # existing project does not include a DOC parser; keep graceful fallback
    else:
        text = _read_text_bytes(path)

    if not text.strip():
        fallback = "Document uploaded successfully but no readable text could be extracted."
        return [make_chunk(fallback, "document", source_name, metadata={"chars": len(fallback)})]

    cleaned = re.sub(r"\r\n?", "\n", text)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    if not cleaned:
        cleaned = "Document uploaded successfully but no content was extracted."

    report("Chunking document content...", 70)
    chunks = []
    for i, paragraph in enumerate(re.split(r"\n\s*\n", cleaned)):
        para = paragraph.strip()
        if not para:
            continue
        chunks.append(make_chunk(para, "document", source_name, metadata={"index": i, "chars": len(para)}))

    if not chunks:
        chunks.append(make_chunk(cleaned[:4000], "document", source_name, metadata={"chars": len(cleaned)}))

    report("Done", 100)
    return chunks
