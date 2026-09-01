"""In-memory conversation memory with a configurable recent-message window."""
import threading
import time
import uuid

from app import config
from app.utils.logging import get_logger

log = get_logger("[MEMORY]")


class Conversation:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.turns: list[dict] = []

    def add(self, role: str, content: str, sources: list | None = None) -> dict:
        turn = {
            "role": role,
            "content": content,
            "sources": sources or [],
            "timestamp": time.time(),
        }
        self.turns.append(turn)
        return turn

    def recent(self, window: int = None) -> list[dict]:
        window = window or config.HISTORY_WINDOW
        return self.turns[-window:]

    def to_list(self) -> list[dict]:
        return self.turns


class ConversationMemory:
    """Thread-safe session store (current-session history, in-memory)."""

    def __init__(self):
        self._sessions: dict[str, Conversation] = {}
        self._lock = threading.Lock()

    def new_session(self) -> str:
        session_id = uuid.uuid4().hex[:16]
        with self._lock:
            self._sessions[session_id] = Conversation(session_id)
        return session_id

    def get(self, session_id: str) -> Conversation:
        with self._lock:
            conv = self._sessions.get(session_id)
            if conv is None:
                conv = Conversation(session_id)
                self._sessions[session_id] = conv
            return conv

    def reset(self, session_id: str) -> None:
        with self._lock:
            self._sessions.pop(session_id, None)

    def list_sessions(self) -> list[str]:
        with self._lock:
            return list(self._sessions.keys())


memory = ConversationMemory()
