"""Vision service: describes images and video frames via a vision-capable Ollama model."""
from app import config
from app.llm.ollama import OllamaClient, OllamaError
from app.utils.logging import get_logger

log = get_logger("[VISION]")

_PROMPT = (
    "Describe this image in detail. Mention the main subject, objects, people, "
    "text, charts, diagrams or on-screen information. Be factual and specific. "
    "If there is text, include the important parts verbatim."
)


class VisionService:
    def __init__(self):
        self._client = None
        self._last_error: str | None = None

    def _get_client(self) -> OllamaClient:
        if self._client is None:
            self._client = OllamaClient(model=config.VISION_MODEL)
        return self._client

    def describe(self, image_path: str, model: str | None = None, prompt: str | None = None) -> str:
        try:
            m = model or config.VISION_MODEL
            client = OllamaClient(model=m)
            description = client.generate_with_images(prompt or _PROMPT, [image_path], model=m)
            log.info("[VISION] described %s (%d chars)", image_path, len(description))
            return description
        except OllamaError as exc:
            self._last_error = str(exc)
            log.error("[VISION] failed: %s", exc)
            raise

    @property
    def available(self) -> bool:
        try:
            return OllamaClient(model=config.VISION_MODEL).has_model(config.VISION_MODEL)
        except Exception:  # noqa: BLE001
            return False


vision_service = VisionService()
