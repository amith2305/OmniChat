"""OCR service using pytesseract / Tesseract for scanned PDFs and image text."""
import shutil

import pytesseract
from PIL import Image

from app import config
from app.utils.logging import get_logger

log = get_logger("[OCR]")


class OCRService:
    def __init__(self):
        self._configured = False
        self._available: bool | None = None

    def _configure(self):
        if self._configured:
            return
        self._configured = True
        if config.TESSERACT_CMD and shutil.which(config.TESSERACT_CMD):
            pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD
            self._available = True
        else:
            self._available = False
            log.warning("[OCR] tesseract binary not found on PATH; OCR disabled")

    def is_available(self) -> bool:
        self._configure()
        return bool(self._available)

    def ocr_image(self, image: Image.Image) -> str:
        """OCR a PIL image, returns extracted text."""
        self._configure()
        if not self._available:
            raise RuntimeError("Tesseract is not installed or not on PATH. OCR is unavailable.")
        try:
            text = pytesseract.image_to_string(image)
            log.info("[OCR] extracted %d chars", len(text.strip()))
            return text.strip()
        except pytesseract.TesseractError as exc:
            log.error("[OCR] failed: %s", exc)
            raise RuntimeError(f"OCR failed: {exc}") from exc


ocr_service = OCRService()
