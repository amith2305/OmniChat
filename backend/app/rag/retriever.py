"""Retrieval: query embedding -> ChromaDB top-K -> ranked chunks with metadata."""
from app import config
from app.rag.embeddings import embedding_service
from app.rag.vector_store import vector_store
from app.utils.logging import get_logger

log = get_logger("[RETRIEVE]")


def retrieve(query: str, top_k: int = None, where: dict | None = None) -> list[dict]:
    top_k = top_k or config.TOP_K
    query_embedding = embedding_service.embed_query(query)
    results = vector_store.query(query_embedding, top_k=top_k, where=where)
    log.info("[RETRIEVE] '%s' -> %d results", query[:60], len(results))
    return results


def retrieve_by_source(query: str, source: str, top_k: int = None) -> list[dict]:
    """Retrieve only from one uploaded source (used for per-file chat)."""
    return retrieve(query, top_k=top_k, where={"source": source})
