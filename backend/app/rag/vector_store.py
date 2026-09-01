"""Persistent ChromaDB vector store for all media chunk types."""
from pathlib import Path

import chromadb

from app import config
from app.rag.metadata import sanitize_metadata
from app.utils.logging import get_logger

log = get_logger("[CHROMA]")


class VectorStore:
    def __init__(self, persist_dir: Path | None = None, collection: str = "omnichat"):
        self.persist_dir = persist_dir or config.CHROMA_DIR
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self._client = chromadb.PersistentClient(path=str(self.persist_dir))
        self._collection = self._client.get_or_create_collection(
            name=collection, metadata={"hnsw:space": "cosine"}
        )

    # ------------------------------------------------------------- ingestion
    def add_chunks(self, chunks: list[dict], embeddings: list[list[float]]) -> None:
        if not chunks:
            return
        log.info("[CHROMA] Preparing %d chunks", len(chunks))
        ids = [c["id"] for c in chunks]
        documents = [c["content"] for c in chunks]
        metadatas = [
            sanitize_metadata({
                "type": c["type"],
                "source": c["source"],
                "page": c.get("page"),
                "start_time": c.get("start_time"),
                "end_time": c.get("end_time"),
                **{k: str(v) for k, v in (c.get("metadata") or {}).items() if k != "page"},
            })
            for c in chunks
        ]
        log.info("[CHROMA] Sanitizing metadata (%d records)", len(metadatas))
        log.info("[CHROMA] Adding %d documents", len(ids))
        try:
            self._collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)
        except Exception as exc:
            log.error("[CHROMA] Failed to index chunks: %s", exc)
            raise
        log.info("[CHROMA] Successfully indexed %d chunks (total %d)", len(chunks), self._collection.count())

    # ---------------------------------------------------------------- query
    def query(self, query_embedding: list[float], top_k: int = 5,
              where: dict | None = None) -> list[dict]:
        res = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
            include=["documents", "metadatas", "distances"],
        )
        out = []
        ids = res.get("ids", [[]])[0]
        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        dists = res.get("distances", [[]])[0]
        for i, cid in enumerate(ids):
            meta = metas[i] or {}
            page = meta.get("page")
            try:
                page = int(page) if page not in (None, "") else None
            except (TypeError, ValueError):
                page = None
            st = meta.get("start_time")
            et = meta.get("end_time")
            try:
                st = float(st) if st not in (None, "") else None
            except (TypeError, ValueError):
                st = None
            try:
                et = float(et) if et not in (None, "") else None
            except (TypeError, ValueError):
                et = None
            out.append({
                "id": cid,
                "content": docs[i],
                "type": meta.get("type", "unknown"),
                "source": meta.get("source", ""),
                "page": page,
                "start_time": st,
                "end_time": et,
                "distance": float(dists[i]) if i < len(dists) else None,
                "metadata": {k: v for k, v in meta.items() if k not in ("type", "source", "page", "start_time", "end_time")},
            })
        return out

    # ------------------------------------------------------------ management
    def resolve_source(self, requested: str | None) -> str | None:
        """Map a user-facing identifier to the stored 'source' metadata value.

        Accepts (in order of preference):
          - the exact stored source (e.g. "9652f..._Yadhu-krishna-nm.pdf")
          - the stable file_id prefix (e.g. "9652f1155fd8402bb7f4e48640cb4ab5")
          - the original filename suffix (e.g. "Yadhu-krishna-nm.pdf")
        """
        if not requested:
            return None
        stored = [s["source"] for s in self.list_sources()]
        if requested in stored:
            return requested
        prefixed = [s for s in stored if s.startswith(f"{requested}_")]
        if prefixed:
            return self._pick_newest(prefixed)
        suffixed = [s for s in stored if s.endswith(f"_{requested}")]
        if suffixed:
            return self._pick_newest(suffixed)
        return None

    @staticmethod
    def _pick_newest(sources: list[str]) -> str:
        """Of multiple matching uploads of the same file, pick the newest on disk."""
        best, best_mtime = sources[0], -1.0
        for src in sources:
            for d in (config.UPLOAD_DIR, config.PROCESSED_DIR):
                f = d / src
                if f.is_file():
                    if f.stat().st_mtime > best_mtime:
                        best, best_mtime = src, f.stat().st_mtime
                    break
        return best

    def list_sources(self) -> list[dict]:
        rows = self._collection.get(include=["metadatas"])
        seen: dict[str, dict] = {}
        for i, cid in enumerate(rows["ids"]):
            meta = rows["metadatas"][i] or {}
            src = meta.get("source", "unknown")
            entry = seen.setdefault(src, {"source": src, "chunks": 0, "types": set()})
            entry["chunks"] += 1
            entry["types"].add(meta.get("type", "unknown"))
        for e in seen.values():
            e["types"] = sorted(e["types"])
        return list(seen.values())

    def get_all(self, source: str | None = None) -> list[dict]:
        """Return all stored chunks (optionally filtered by source)."""
        where = {"source": source} if source else None
        rows = self._collection.get(where=where, include=["documents", "metadatas"])
        out = []
        for i, cid in enumerate(rows["ids"]):
            meta = rows["metadatas"][i] or {}
            page = meta.get("page")
            try:
                page = int(page) if page not in (None, "") else None
            except (TypeError, ValueError):
                page = None
            st = meta.get("start_time")
            et = meta.get("end_time")
            try:
                st = float(st) if st not in (None, "") else None
            except (TypeError, ValueError):
                st = None
            try:
                et = float(et) if et not in (None, "") else None
            except (TypeError, ValueError):
                et = None
            out.append({
                "id": cid,
                "content": rows["documents"][i],
                "type": meta.get("type", "unknown"),
                "source": meta.get("source", ""),
                "page": page,
                "start_time": st,
                "end_time": et,
                "metadata": {k: v for k, v in meta.items()
                             if k not in ("type", "source", "page", "start_time", "end_time")},
            })
        return out

    def delete_source(self, source: str) -> int:
        rows = self._collection.get(include=["metadatas"])
        ids = [rid for i, rid in enumerate(rows["ids"]) if (rows["metadatas"][i] or {}).get("source") == source]
        if ids:
            self._collection.delete(ids=ids)
            log.info("[CHROMA] deleted %d chunks of '%s'", len(ids), source)
        return len(ids)

    def count(self) -> int:
        return self._collection.count()

    def reset(self) -> None:
        self._client.delete_collection(self._collection.name)
        self._collection = self._client.get_or_create_collection(
            name=self._collection.name, metadata={"hnsw:space": "cosine"}
        )
        log.info("[CHROMA] collection reset")


vector_store = VectorStore()
