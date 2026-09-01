"""PDF processor: PyMuPDF text extraction with Tesseract OCR fallback for scanned pages."""
import fitz
from PIL import Image

from app import config
from app.rag.chunker import chunk_pdf_text
from app.services.ocr import ocr_service
from app.utils.logging import get_logger

log = get_logger("[PDF]")


class PDFProcessingError(RuntimeError):
    pass


def extract_text_with_layout(page) -> str:
    return page.get_text("text")


def process_pdf(path: str, progress=None) -> list[dict]:
    """Extract text/OCR per page and return multimodal chunks."""
    def report(msg: str, pct: int | None = None):
        if progress:
            progress(msg, pct)

    try:
        doc = fitz.open(path)
    except Exception as exc:  # noqa: BLE001
        raise PDFProcessingError(f"Could not open PDF: {exc}") from exc

    chunks: list[dict] = []
    ocr_pages = 0
    total = doc.page_count
    source_name = doc.name or path
    import os
    source_name = os.path.basename(source_name)

    if total == 0:
        raise PDFProcessingError("PDF has no pages.")

    for page_index, page in enumerate(doc):
        report(f"Extracting page {page_index + 1}/{total}...", int((page_index / total) * 100))
        text = extract_text_with_layout(page).strip()

        if len(text) < config.OCR_MIN_TEXT_LENGTH:
            log.info("[PDF] page %d has little text (%d chars) -> OCR", page_index + 1, len(text))
            try:
                pix = page.get_pixmap(dpi=200)
                image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                if ocr_service.is_available():
                    text = ocr_service.ocr_image(image)
                    ocr_pages += 1
                else:
                    log.warning("[PDF] OCR unavailable; page %d skipped", page_index + 1)
            except Exception as exc:  # noqa: BLE001
                log.warning("[PDF] OCR failed on page %d: %s", page_index + 1, exc)
                text = ""

        if text.strip():
            chunks.extend(chunk_pdf_text(text, source_name, page_index + 1))

    doc.close()
    log.info("[PDF] %s -> %d chunks (OCR on %d pages)", source_name, len(chunks), ocr_pages)
    if not chunks:
        raise PDFProcessingError("No text could be extracted from this PDF.")
    return chunks
