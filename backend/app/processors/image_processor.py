"""Image processor: OCR text (if useful) + vision model description -> chunks."""
import os

from PIL import Image

from app import config
from app.rag.chunker import chunk_image
from app.services.ocr import ocr_service
from app.services.vision import vision_service
from app.utils.files import rel_path
from app.utils.logging import get_logger

log = get_logger("[IMAGE]")


class ImageProcessingError(RuntimeError):
    pass


def process_image(path: str, progress=None) -> list[dict]:
    def report(msg: str, pct: int | None = None):
        if progress:
            progress(msg, pct)

    report("Reading image...", 10)
    try:
        image = Image.open(path)
        image.load()
    except Exception as exc:  # noqa: BLE001
        raise ImageProcessingError(f"Could not read image: {exc}") from exc

    source_name = os.path.basename(path)

    report("Running OCR...", 30)
    ocr_text = ""
    if ocr_service.is_available():
        try:
            ocr_text = ocr_service.ocr_image(image)
        except Exception as exc:  # noqa: BLE001
            log.warning("[IMAGE] OCR failed: %s", exc)
    if ocr_text:
        log.info("[IMAGE] OCR found %d chars", len(ocr_text))

    report("Describing image with vision model...", 60)
    try:
        description = vision_service.describe(path)
    except Exception as exc:  # noqa: BLE001
        log.error("[IMAGE] vision failed: %s", exc)
        description = ""

    parts = []
    if description:
        parts.append(f"Visual description: {description}")
    if ocr_text:
        parts.append(f"OCR text found in the image: {ocr_text}")
    if not parts:
        parts.append("Image could not be interpreted (vision model unavailable).")
    content = "\n".join(parts)

    chunk = chunk_image(content, source_name, rel_path(path))
    report("Done", 100)
    return [chunk]
