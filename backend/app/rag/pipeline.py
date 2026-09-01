"""RAG pipeline: ingest chunks -> embed -> store; question -> retrieve -> LLM -> answer."""
from app import config
from app.llm import prompts
from app.llm.ollama import OllamaClient, OllamaError
from app.rag.embeddings import embedding_service
from app.rag.vector_store import vector_store
from app.utils.logging import get_logger

log = get_logger("[RAG]")

llm = OllamaClient()


def _resolve_identifier(source: str | None) -> str | None:
    """Map a user-facing identifier (stored source / file_id / filename) to the
    stored 'source' value used by ChromaDB, so every caller filters consistently."""
    if not source:
        return None
    resolved = vector_store.resolve_source(source)
    if resolved is None:
        log.warning("[RAG] no indexed document matches identifier '%s'", source)
    return resolved


# ---------------------------------------------------------------- ingestion
def index_chunks(chunks: list[dict]) -> int:
    """Embed and store chunks in the shared vector database."""
    if not chunks:
        return 0
    texts = [c["content"] for c in chunks]
    embeddings = embedding_service.embed_documents(texts)
    vector_store.add_chunks(chunks, embeddings)
    return len(chunks)


def index_source(chunks: list[dict]) -> int:
    return index_chunks(chunks)


# ------------------------------------------------------------------- answer
def _format_context(results: list[dict]) -> str:
    blocks = []
    for i, r in enumerate(results, 1):
        source_label = r.get("source", "unknown")
        # Strip file ID prefix if present for cleaner context
        if "_" in source_label and len(source_label.split("_")[0]) == 32:
            source_label = "_".join(source_label.split("_")[1:])

        ctype = r.get("type", "content")
        details = []
        if r.get("page") is not None:
            details.append(f"Page {r['page']}")
        if r.get("start_time") is not None:
            from app.utils.files import format_time
            st = format_time(r['start_time'])
            et = format_time(r.get('end_time', r['start_time']))
            details.append(f"Time: {st} - {et}")

        meta_str = f" ({', '.join(details)})" if details else ""
        blocks.append(f"[Source {i}: {ctype} from '{source_label}'{meta_str}]\n{r['content']}")
    return "\n\n".join(blocks)


def answer_question(question: str, history: list[dict] | None = None,
                    source_filter: str | None = None, top_k: int = None) -> dict:
    """Run the full RAG pipeline and return {'answer', 'sources'}."""
    top_k = top_k or config.TOP_K
    query_embedding = embedding_service.embed_query(question)
    where = None
    if source_filter:
        resolved = _resolve_identifier(source_filter)
        if resolved:
            where = {"source": resolved}
    results = vector_store.query(query_embedding, top_k=top_k, where=where)
    log.info("[RAG] Query: %s", question[:80])
    log.info("[RAG] Retrieved relevant chunks: %d%s",
             len(results), f" (source: {resolved})" if where else "")

    context = _format_context(results)
    history_text = None
    if history:
        history_text = "\n".join(
            f"{turn['role'].upper()}: {turn['content']}" for turn in history[-config.HISTORY_WINDOW:]
        )

    if not results:
        prompt = prompts.build_rag_prompt(question, "(no relevant content retrieved)", history_text)
        try:
            answer = llm.generate(prompt, system=prompts.SYSTEM_INSTRUCTION)
        except OllamaError as exc:
            raise OllamaError(str(exc)) from exc
        if not answer:
            answer = "I could not retrieve any relevant content to answer that question."
        return {"answer": answer, "sources": []}

    answer = llm.generate(
        prompts.build_rag_prompt(question, context, history_text),
        system=prompts.SYSTEM_INSTRUCTION,
    )
    if not answer:
        answer = "I could not generate an answer from the retrieved content."

    sources = []
    for r in results:
        sources.append({
            "id": r["id"],
            "type": r["type"],
            "source": r["source"],
            "page": r.get("page"),
            "start_time": r.get("start_time"),
            "end_time": r.get("end_time"),
            "content": r["content"][:300],
        })
    return {"answer": answer, "sources": sources}


# ------------------------------------------------------------ summarization
def summarize_source(source: str, title: str, top_k: int = 400) -> dict:
    """Chunk-level summaries combined into one summary (map-reduce)."""
    log.info("[SUMMARY] Requested file: %s", source)
    resolved = _resolve_identifier(source)
    if resolved is None:
        return {"summary": "No indexed content found for this file.", "steps": 0}
    all_chunks = vector_store.get_all(source=resolved)
    log.info("[SUMMARY] Resolved document: %s", resolved)
    log.info("[SUMMARY] Retrieved %d chunks", len(all_chunks))
    log.info("[SUMMARY] Generating summary with %s", llm.model)

    chunk_summaries = []
    for c in all_chunks:
        text = c["content"]
        if len(text) > 2500:
            text = text[:2500]
        try:
            s = llm.generate(prompts.build_summarize_prompt(text, title))
            chunk_summaries.append(s or text)
        except OllamaError as exc:
            log.warning("chunk summary failed: %s", exc)
            chunk_summaries.append(text[:800])

    if len(chunk_summaries) == 1:
        final_summary = chunk_summaries[0]
    else:
        final_summary = llm.generate(prompts.build_combine_summaries_prompt(chunk_summaries, title))

    return {"summary": final_summary, "steps": len(chunk_summaries)}


# ------------------------------------------------------------ topic extraction
_STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "of", "in", "on", "at", "to", "for", "with",
    "from", "by", "as", "is", "are", "was", "were", "be", "been", "it", "its", "this",
    "that", "these", "those", "there", "their", "they", "we", "you", "your", "he", "she",
    "his", "her", "them", "not", "no", "yes", "so", "if", "then", "than", "too", "very",
    "can", "could", "will", "would", "should", "may", "might", "must", "do", "does", "did",
    "have", "has", "had", "about", "into", "over", "under", "again", "more", "most", "some",
    "any", "each", "other", "such", "only", "own", "same", "than", "how", "when", "where",
    "which", "while", "what", "who", "why", "also", "all", "one", "two", "first", "second",
    "etc", "e.g", "i.e", "via", "per", "used", "using", "use", "using", "make", "made",
}


def extract_topics(source: str, top_n: int = 40) -> dict:
    """Frequency-based keyword extraction (pure python) refined by the LLM."""
    log.info("[TOPICS] Requested file: %s", source)
    resolved = _resolve_identifier(source)
    if resolved is None:
        return {"topics": []}
    chunks = vector_store.get_all(source=resolved)
    log.info("[TOPICS] Resolved document: %s", resolved)
    log.info("[TOPICS] Retrieved %d chunks", len(chunks))
    log.info("[TOPICS] Extracting topics with %s", llm.model)

    text = " ".join(c["content"] for c in chunks)
    words = re_find_words(text)
    counts: dict[str, int] = {}
    for w in words:
        if len(w) < 4 or w.lower() in _STOPWORDS:
            continue
        counts[w.lower()] = counts.get(w.lower(), 0) + 1

    ranked = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
    candidates = [w for w, _ in ranked if not w.isdigit()][:20]

    try:
        response = llm.generate(prompts.build_topics_prompt(candidates, text))
        topics = [
            line.lstrip("-• ").strip()
            for line in response.splitlines()
            if line.strip() and not line.lower().startswith(("here", "the main", "based", "document"))
        ]
        topics = [t for t in topics if t and len(t) < 60][:8]
        if topics:
            return {"topics": topics, "keywords": candidates}
    except OllamaError:
        pass

    return {"topics": candidates[:8], "keywords": candidates}


def re_find_words(text: str) -> list[str]:
    import re
    return re.findall(r"[A-Za-z][A-Za-z'-]{2,}", text)
