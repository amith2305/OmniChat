"""Structured data processor for CSV/TSV/JSON/XLSX files."""
import csv
import io
import json
import os
from pathlib import Path

from app.rag.chunker import make_chunk
from app.utils.logging import get_logger

log = get_logger("[DATA]")


def _read_json(path: str) -> str:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return json.dumps(data, ensure_ascii=False, indent=2, default=str)
    except Exception as exc:  # noqa: BLE001
        log.warning("JSON read failed: %s", exc)
        return Path(path).read_text(encoding="utf-8", errors="ignore")


def _read_csv(path: str) -> str:
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    rows = []
    for row in csv.reader(io.StringIO(text)):
        rows.append(", ".join(row))
    return "\n".join(rows[:200])


def _read_xlsx(path: str) -> str:
    try:
        import openpyxl

        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        sheets = []
        for ws in wb.worksheets:
            rows = []
            for row in ws.iter_rows(values_only=True):
                values = ["" if v is None else str(v) for v in row]
                if any(v.strip() for v in values):
                    rows.append(" | ".join(values))
            if rows:
                sheets.append(f"Sheet: {ws.title}\n" + "\n".join(rows[:80]))
        return "\n\n".join(sheets) if sheets else ""
    except Exception as exc:  # noqa: BLE001
        log.warning("XLSX read failed: %s", exc)
        return ""


def process_data(path: str, progress=None) -> list[dict]:
    def report(msg: str, pct: int | None = None):
        if progress:
            progress(msg, pct)

    source_name = os.path.basename(path)
    ext = Path(path).suffix.lower()
    report(f"Reading {source_name}...", 10)

    text = ""
    if ext == ".json":
        text = _read_json(path)
    elif ext in {".csv", ".tsv"}:
        text = _read_csv(path)
    elif ext in {".xlsx", ".xls"}:
        text = _read_xlsx(path)
    else:
        text = Path(path).read_text(encoding="utf-8", errors="ignore")

    if not text.strip():
        text = "Structured data uploaded successfully but no parseable rows were found."

    report("Chunking structured data...", 70)
    chunks = [make_chunk(text[:4000], "data", source_name, metadata={"chars": len(text)})]
    report("Done", 100)
    return chunks
