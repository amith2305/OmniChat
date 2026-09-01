"""Prompt templates for the Llama 3B / Ollama generation model."""

SYSTEM_INSTRUCTION = (
    "You are OmniChat AI, an expert multimodal media intelligence assistant. "
    "You answer user questions accurately and comprehensively based on the RELEVANT CONTEXT provided below.\n\n"
    "Guidelines:\n"
    "- Carefully review the provided source blocks (which may include document text, OCR text, image descriptions, audio transcripts, or video frame descriptions).\n"
    "- Answer the user's question directly using the information in the context.\n"
    "- Reference specific sources naturally (e.g., mention page numbers for PDFs, timestamps like 00:15 or MM:SS for audio/video, and file names).\n"
    "- If visual frame or image descriptions are provided, use them to describe what appears on screen.\n"
    "- If the context genuinely contains no relevant information to answer the question, state politely that the context does not have that information.\n"
    "- Use conversation history to understand follow-up questions.\n"
    "- Be clear, helpful, and concise."
)


def build_rag_prompt(question: str, context: str, history: str | None = None) -> str:
    parts = []
    if history:
        parts.append(f"CONVERSATION HISTORY:\n{history}\n")
    parts.append(f"RELEVANT CONTEXT:\n{context}\n")
    parts.append(f"USER QUESTION:\n{question}")
    return "\n\n".join(parts)


def build_summarize_prompt(text: str, title: str) -> str:
    return (
        f"Summarize the following content from '{title}' in a clear, structured way. "
        "Capture the main points, key numbers and conclusions. "
        "Write the summary in plain paragraphs with short bullet lists where useful.\n\n"
        f"CONTENT:\n{text}"
    )


def build_combine_summaries_prompt(summaries: list[str], title: str) -> str:
    joined = "\n\n---\n\n".join(f"Part summary:\n{s}" for s in summaries)
    return (
        f"You are given section summaries of '{title}'. "
        "Combine them into one coherent overall summary. Remove repetition, "
        "keep all important facts and conclusions.\n\n"
        f"SECTION SUMMARIES:\n{joined}"
    )


def build_topics_prompt(candidate_topics: list[str], sample_text: str) -> str:
    candidates = ", ".join(candidate_topics)
    return (
        "Extract the main topics from the following document content. "
        "Return ONLY a short bullet list of 3-8 concise topic names, one per line, "
        "starting with '- '. Do not add explanations.\n\n"
        f"CANDIDATE KEYWORDS: {candidates}\n\n"
        f"DOCUMENT SAMPLE:\n{sample_text[:3000]}"
    )
