"""Video processor: extract audio (ffmpeg) -> Whisper transcript; OpenCV frames -> vision.

Produces both video_transcript and video_frame chunks with timestamps.
"""
import os
import subprocess
import time
from pathlib import Path

import cv2

from app import config
from app.rag.chunker import chunk_audio_transcript, chunk_frame
from app.services.vision import vision_service
from app.services.whisper import whisper_service
from app.utils.logging import get_logger

log = get_logger("[VIDEO]")


class VideoProcessingError(RuntimeError):
    pass


def _ffmpeg_path() -> str:
    return "ffmpeg"


def extract_audio(video_path: str, out_path: str) -> bool:
    """Extract audio track with ffmpeg. Returns True if audio was extracted."""
    try:
        result = subprocess.run(
            [_ffmpeg_path(), "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", out_path],
            capture_output=True, text=True, timeout=1800,
        )
        if result.returncode != 0:
            log.warning("[VIDEO] ffmpeg audio extraction failed: %s", result.stderr[-300:])
            return False
        return os.path.getsize(out_path) > 1000
    except FileNotFoundError:
        log.error("[VIDEO] ffmpeg not found on PATH; audio extraction disabled")
        return False
    except Exception as exc:  # noqa: BLE001
        log.warning("[VIDEO] ffmpeg error: %s", exc)
        return False


def process_video(path: str, progress=None) -> list[dict]:
    """Full video pipeline -> transcript chunks + frame description chunks."""
    def report(msg: str, pct: int | None = None):
        if progress:
            progress(msg, pct)

    source_name = os.path.basename(path)
    chunks: list[dict] = []

    # ----------------------------------------------------------- validate
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        cap.release()
        raise VideoProcessingError("Could not open the video file (corrupted or unsupported codec).")
    fps = cap.get(cv2.CAP_PROP_FPS) or 1.0
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps else 0
    cap.release()
    log.info("[VIDEO] %s: %.1fs, %.1f fps, %d frames", source_name, duration, fps, frame_count)

    # ------------------------------------------------------------ audio part
    config.ensure_dirs()
    audio_out = str(config.PROCESSED_DIR / f"{Path(path).stem}_audio.wav")
    report("Extracting audio...", 5)
    if extract_audio(path, audio_out):
        report("Transcribing audio...", 20)
        try:
            result = whisper_service.transcribe(audio_out)
            if result.get("text"):
                chunks.extend(chunk_audio_transcript(result["segments"], source_name, ctype="video_transcript"))
        except Exception as exc:  # noqa: BLE001
            log.warning("[VIDEO] transcription failed: %s", exc)
    else:
        log.warning("[VIDEO] no audio track extracted for %s", source_name)

    # ------------------------------------------------------------ frames part
    report("Sampling frames...", 35)
    interval = max(0.5, config.VIDEO_FRAME_INTERVAL)
    frame_ts = 0.0
    n = 0
    cap = cv2.VideoCapture(path)
    frame_step = max(1, int(round(interval * fps)))

    frame_dir = config.FRAMES_DIR
    frame_dir.mkdir(parents=True, exist_ok=True)

    frames_for_vision: list[tuple[float, str]] = []
    while True:
        ok = cap.grab()
        if not ok:
            break
        if n % frame_step == 0:
            ok2, frame = cap.retrieve()
            if ok2:
                ts = n / fps
                fpath = str(frame_dir / f"{Path(path).stem}_f{n:06d}.jpg")
                if cv2.imwrite(fpath, frame):
                    frames_for_vision.append((ts, fpath))
        n += 1
    cap.release()
    log.info("[VIDEO] sampled %d frames", len(frames_for_vision))

    total_frames = len(frames_for_vision)
    for i, (ts, fpath) in enumerate(frames_for_vision):
        pct = 35 + int((i / max(1, total_frames)) * 60)
        if i % max(1, total_frames // 10) == 0 or i == total_frames - 1:
            report(f"Analyzing frame {i + 1}/{total_frames} ({ts:.0f}s)...", pct)
        try:
            description = vision_service.describe(fpath)
        except Exception as exc:  # noqa: BLE001
            log.warning("[VISION] frame %s failed: %s", fpath, exc)
            description = "(frame could not be analyzed)"
        chunks.append(chunk_frame(description, source_name, ts, duration=interval))
        time.sleep(0.05)

    report("Done", 100)
    if not chunks:
        raise VideoProcessingError("No content could be extracted from this video.")
    log.info("[VIDEO] %s -> %d chunks", source_name, len(chunks))
    return chunks
