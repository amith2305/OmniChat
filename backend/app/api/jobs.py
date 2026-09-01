"""In-memory upload/job registry with progress tracking."""
import threading
import time

from app.utils.logging import get_logger

log = get_logger("[JOB]")

STATUSES = ("queued", "validating", "processing", "done", "error")


class JobRegistry:
    def __init__(self):
        self._jobs: dict[str, dict] = {}
        self._lock = threading.Lock()

    def create(self, file_id: str, filename: str, media_type: str) -> dict:
        job = {
            "file_id": file_id,
            "filename": filename,
            "type": media_type,
            "status": "queued",
            "message": "Uploaded",
            "progress": 0,
            "chunks": 0,
            "error": None,
            "updated": time.time(),
        }
        with self._lock:
            self._jobs[file_id] = job
        return job

    def update(self, file_id: str, status: str = None, message: str = None,
               progress: int = None, chunks: int = None, error: str = None) -> None:
        with self._lock:
            job = self._jobs.get(file_id)
            if job is None:
                return
            if status is not None:
                job["status"] = status
            if message is not None:
                job["message"] = message
            if progress is not None:
                job["progress"] = max(0, min(100, progress))
            if chunks is not None:
                job["chunks"] = chunks
            if error is not None:
                job["error"] = error
            job["updated"] = time.time()

    def progress_fn(self, file_id: str):
        def report(message: str, pct: int | None = None):
            self.update(file_id, message=message, progress=pct)
        return report

    def get(self, file_id: str) -> dict | None:
        with self._lock:
            job = self._jobs.get(file_id)
            return dict(job) if job else None

    def all(self) -> list[dict]:
        with self._lock:
            return [dict(j) for j in self._jobs.values()]


jobs = JobRegistry()
