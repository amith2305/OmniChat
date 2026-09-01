"""Minimal Ollama HTTP client (generate / chat / embeddings / vision)."""
import base64
import time
from pathlib import Path

import requests

from app import config
from app.utils.logging import get_logger

log = get_logger("[LLM]")


class OllamaError(RuntimeError):
    pass


class OllamaClient:
    def __init__(self, base_url: str | None = None, model: str | None = None):
        self.base_url = (base_url or config.OLLAMA_BASE_URL).rstrip("/")
        self.model = model or config.LLM_MODEL

    # -------------------------------------------------------------- helpers
    def _post(self, path: str, payload: dict, timeout: int = 300) -> dict:
        try:
            resp = requests.post(f"{self.base_url}{path}", json=payload, timeout=timeout)
        except requests.ConnectionError as exc:
            raise OllamaError(
                f"Ollama is not reachable at {self.base_url}. Start it with 'ollama serve'."
            ) from exc
        if resp.status_code != 200:
            raise OllamaError(f"Ollama {path} failed: HTTP {resp.status_code}: {resp.text[:200]}")
        return resp.json()

    def is_available(self) -> bool:
        try:
            return requests.get(f"{self.base_url}/api/tags", timeout=5).status_code == 200
        except requests.RequestException:
            return False

    def list_models(self) -> list[str]:
        data = requests.get(f"{self.base_url}/api/tags", timeout=10).json()
        return [m["name"] for m in data.get("models", [])]

    def has_model(self, model: str | None = None) -> bool:
        name = model or self.model
        try:
            return any(m.split(":")[0] == name.split(":")[0] or m == name for m in self.list_models())
        except requests.RequestException:
            return False

    # ------------------------------------------------------------ generation
    def generate(self, prompt: str, *, model: str | None = None, system: str | None = None,
                 options: dict | None = None, stream: bool = False,
                 images: list[str] | None = None) -> str:
        """Generate a completion. images = list of base64-encoded image strings."""
        payload: dict = {"model": model or self.model, "prompt": prompt, "stream": stream}
        if system:
            payload["system"] = system
        if options:
            payload["options"] = options
        if images:
            payload["images"] = images
        data = self._post("/api/generate", payload)
        return (data.get("response") or "").strip()

    def generate_with_images(self, prompt: str, image_paths: list[str], *,
                             model: str | None = None) -> str:
        """Generate using local image file paths (multimodal vision models)."""
        encoded = []
        for p in image_paths:
            data = base64.b64encode(Path(p).read_bytes()).decode("utf-8")
            encoded.append(data)
        return self.generate(prompt, model=model or config.VISION_MODEL, images=encoded)

    # ------------------------------------------------------------ embeddings
    def embed(self, texts: str | list[str]) -> list[list[float]]:
        if isinstance(texts, str):
            texts = [texts]
        data = self._post("/api/embed", {"model": config.EMBEDDING_FALLBACK_OLLAMA, "input": texts}, timeout=120)
        return [list(map(float, v)) for v in data.get("embeddings", [])]


def wait_for_model(model: str, timeout: int = 600) -> bool:
    """Poll Ollama until a model tag is ready (loads if needed via /api/show)."""
    client = OllamaClient(model=model)
    deadline = time.time() + timeout
    while time.time() < deadline:
        if not client.is_available():
            time.sleep(2)
            continue
        try:
            requests.post(f"{client.base_url}/api/generate",
                          json={"model": model, "prompt": "", "stream": False, "keep_alive": 0},
                          timeout=20)
            return True
        except requests.RequestException:
            time.sleep(2)
    return False


ollama_client = OllamaClient()
