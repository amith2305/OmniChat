"""Text-to-speech using pyttsx3 (offline). Optionally gTTS if configured and reachable."""
import uuid
from pathlib import Path

from app import config
from app.utils.logging import get_logger

log = get_logger("[TTS]")

TTS_USE_GTTS = False  # set True via .env TTS_ENGINE=gtts


def text_to_speech(text: str) -> str:
    """Synthesize speech, save to data/audio, return the file path."""
    config.ensure_dirs()
    out_path = config.AUDIO_DIR / f"tts_{uuid.uuid4().hex}.wav"
    text = text[:4000]

    if TTS_USE_GTTS:
        try:
            from gtts import gTTS
            gTTS(text=text, lang="en").save(str(out_path))
            log.info("[TTS] gTTS -> %s", out_path)
            return str(out_path)
        except Exception as exc:  # noqa: BLE001
            log.warning("[TTS] gTTS failed (%s); falling back to pyttsx3", exc)

    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.save_to_file(text, str(out_path))
        engine.runAndWait()
        engine.stop()
        log.info("[TTS] pyttsx3 -> %s", out_path)
        return str(out_path)
    except Exception as exc:  # noqa: BLE001
        log.error("[TTS] failed: %s", exc)
        raise RuntimeError(f"Text-to-speech failed: {exc}") from exc
