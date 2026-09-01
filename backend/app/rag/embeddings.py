"""Embedding service: Sentence Transformers (offline/cached) with Ollama fallback.

Implements the required interface:
    embed_text()       -> single vector
    embed_documents()  -> list of vectors
    embed_query()      -> single query vector
"""
import threading

from app import config
from app.utils.logging import get_logger

log = get_logger("[EMBED]")


class EmbeddingService:
    def __init__(self):
        self._model = None
        self._fallback_client = None
        self._lock = threading.Lock()
        self._backend = None

    # ------------------------------------------------------------------ init
    def _load_sentence_transformers(self):
        from sentence_transformers import SentenceTransformer
        try:
            model = SentenceTransformer(config.EMBEDDING_MODEL, local_files_only=True)
            self._model = model
            self._backend = "sentence-transformers"
            log.info("embedding backend: sentence-transformers (%s) [offline cache]", config.EMBEDDING_MODEL)
        except Exception as exc:  # noqa: BLE001
            log.warning("sentence-transformers failed (%s); trying Ollama fallback", exc)
            self._load_ollama()

    def _load_ollama(self):
        from app.llm.ollama import OllamaClient
        try:
            client = OllamaClient(model=config.EMBEDDING_FALLBACK_OLLAMA)
            client.embed("ping")
            self._fallback_client = client
            self._backend = "ollama"
            log.info("embedding backend: ollama (%s)", config.EMBEDDING_FALLBACK_OLLAMA)
        except Exception as exc:  # noqa: BLE001
            log.error("embedding unavailable: %s", exc)
            self._backend = "unavailable"

    def ensure_loaded(self):
        if self._backend is None:
            with self._lock:
                if self._backend is None:
                    if config.EMBEDDING_MODEL:
                        self._load_sentence_transformers()
                    if self._backend is None:
                        self._load_ollama()

    @property
    def backend(self) -> str:
        self.ensure_loaded()
        return self._backend or "unavailable"

    # ------------------------------------------------------------- embed API
    def embed_text(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        self.ensure_loaded()
        if self._backend == "unavailable":
            raise RuntimeError("No embedding backend available (sentence-transformers and Ollama both failed).")
        if self._backend == "sentence-transformers":
            vectors = self._model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
            return [v.tolist() for v in vectors]
        return self._fallback_client.embed(texts)

    def embed_query(self, text: str) -> list[float]:
        self.ensure_loaded()
        if self._backend == "sentence-transformers":
            vector = self._model.encode([text], normalize_embeddings=True, show_progress_bar=False)[0]
            return vector.tolist()
        return self._fallback_client.embed([text])[0]


embedding_service = EmbeddingService()
