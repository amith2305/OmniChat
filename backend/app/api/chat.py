"""Chat endpoint: RAG question answering with conversation memory + history."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.llm.ollama import OllamaError
from app.memory.conversation import memory
from app.rag.pipeline import answer_question
from app.utils.logging import get_logger

log = get_logger("[API]")

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    question: str
    session_id: str | None = None
    source: str | None = None


@router.post("/chat")
def chat(req: ChatRequest):
    if not req.question or not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    session_id = req.session_id or memory.new_session()
    conv = memory.get(session_id)

    try:
        result = answer_question(req.question.strip(), history=conv.recent(), source_filter=req.source)
    except OllamaError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    conv.add("user", req.question.strip())
    conv.add("assistant", result["answer"], sources=result["sources"])

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "session_id": session_id,
    }


@router.get("/history")
def get_history(session_id: str):
    conv = memory.get(session_id)
    return {"session_id": session_id, "turns": conv.to_list()}


class ResetHistoryRequest(BaseModel):
    session_id: str | None = None


@router.post("/history/reset")
def reset_history(req: ResetHistoryRequest | None = None, session_id: str | None = None):
    target = (req.session_id if req else None) or session_id
    if not target:
        raise HTTPException(status_code=400, detail="session_id is required.")
    memory.reset(target)
    return {"reset": True, "session_id": target}
