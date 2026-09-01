"""Whisper transcription via faster-whisper (timestamps preserved)."""
import threading

from app import config
from app.utils.logging import get_logger

log = get_logger("[WHISPER]")


class WhisperService:
    def __init__(self):
        self._model = None
        self._lock = threading.Lock()
        self._load_error: Exception | None = None

    def _ensure_model(self):
        if self._model is None and self._load_error is None:
            with self._lock:
                if self._model is None and self._load_error is None:
                    try:
                        from faster_whisper import WhisperModel
                        log.info("[WHISPER] loading model '%s' (device=%s, compute=%s) from local cache",
                                 config.WHISPER_MODEL, config.WHISPER_DEVICE, config.WHISPER_COMPUTE_TYPE)
                        self._model = WhisperModel(
                            config.WHISPER_MODEL,
                            device=config.WHISPER_DEVICE,
                            compute_type=config.WHISPER_COMPUTE_TYPE,
                            local_files_only=True,
                        )
                        log.info("[WHISPER] model ready")
                    except Exception as exc:  # noqa: BLE001
                        self._load_error = exc
                        log.error("[WHISPER] failed to load model: %s", exc)
        if self._load_error is not None:
            raise RuntimeError(f"Whisper model unavailable: {self._load_error}")

    def transcribe(self, audio_path: str, language: str | None = None) -> dict:
        """Transcribe an audio file. Returns {'text', 'segments': [{'text','start','end'}]}."""
        self._ensure_model()
        segments_iter, info = self._model.transcribe(
            audio_path,
            language=language,
            vad_filter=True,
        )
        segments = []
        parts = []
        for seg in segments_iter:
            segments.append({"text": seg.text.strip(), "start": float(seg.start), "end": float(seg.end)})
            parts.append(seg.text.strip())
        text = " ".join(parts).strip()
        log.info("[WHISPER] transcribed %s -> %d segments, %d chars", audio_path, len(segments), len(text))
        return {"text": text, "segments": segments, "language": getattr(info, "language", None)}


whisper_service = WhisperService()
