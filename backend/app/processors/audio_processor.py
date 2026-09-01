"""Audio processor: Whisper transcription with timestamps -> time-based chunks."""
import os

from app.rag.chunker import chunk_audio_transcript
from app.services.whisper import whisper_service
from app.utils.logging import get_logger

log = get_logger("[AUDIO]")


class AudioProcessingError(RuntimeError):
    pass


def process_audio(path: str, progress=None, ctype: str = "audio") -> list[dict]:
    """Transcribe audio/video-derived audio into timestamped chunks."""
    def report(msg: str, pct: int | None = None):
        if progress:
            progress(msg, pct)

    report("Transcribing with Whisper...", 20)
    try:
        result = whisper_service.transcribe(path)
    except Exception as exc:  # noqa: BLE001
        raise AudioProcessingError(f"Transcription failed: {exc}") from exc

    if not result.get("text"):
        raise AudioProcessingError("No speech detected in the audio file.")

    source_name = os.path.basename(path)
    chunks = chunk_audio_transcript(result["segments"], source_name, ctype=ctype)
    report("Done", 100)
    log.info("[AUDIO] %s -> %d chunks", source_name, len(chunks))
    return chunks
