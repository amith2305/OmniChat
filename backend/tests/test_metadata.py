"""Unit tests for ChromaDB metadata sanitization.

Run with:  python tests/test_metadata.py
or:        pytest tests/test_metadata.py  (from backend/)
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import classify_file
from app.rag.metadata import sanitize_metadata
from app.rag.vector_store import VectorStore
from app.utils.validation import validate_upload


def test_pdf_metadata_none_values_removed():
    meta = sanitize_metadata({"source": "test.pdf", "page": 1, "start_time": None, "end_time": None})
    assert meta == {"source": "test.pdf", "page": 1}
    assert None not in meta.values()


def test_audio_timestamps_preserved():
    meta = sanitize_metadata({"source": "lecture.mp3", "start_time": 134.5, "end_time": 165.2})
    assert meta["start_time"] == 134.5
    assert meta["end_time"] == 165.2
    assert isinstance(meta["start_time"], float)


def test_video_list_and_path_converted():
    meta = sanitize_metadata({
        "source": "test.mp4",
        "start_time": 12.5,
        "tags": ["AI", "ML"],
        "path": Path("test.mp4"),
    })
    assert isinstance(meta["tags"], str)
    assert "AI" in meta["tags"] and "ML" in meta["tags"]
    assert isinstance(meta["path"], str)
    assert meta["path"] == "test.mp4"
    assert meta["start_time"] == 12.5


def test_dict_and_other_types_converted():
    meta = sanitize_metadata({"extra": {"foo": "bar"}, "flag": True, "ratio": 0.5, "none": None})
    assert isinstance(meta["extra"], str)
    assert meta["flag"] is True
    assert meta["ratio"] == 0.5
    assert "none" not in meta


def test_all_values_are_chromadb_primitives():
    meta = sanitize_metadata({
        "source": "a.pdf", "page": 2, "flag": True, "ratio": 0.5,
        "none": None, "tags": [1, 2], "path": Path("a.pdf"),
    })
    for value in meta.values():
        assert isinstance(value, (str, int, float, bool)), value


def test_classify_multiple_supported_upload_types():
    assert classify_file("sample.pdf") == "pdf"
    assert classify_file("notes.txt") == "document"
    assert classify_file("report.csv") == "data"
    assert classify_file("report.json") == "data"
    assert classify_file("workbook.xlsx") == "data"
    assert classify_file("letter.docx") == "document"
    assert classify_file("image.png") == "image"
    assert classify_file("voice.mp3") == "audio"
    assert classify_file("clip.mp4") == "video"


def test_validate_supports_text_and_data_files():
    validate_upload("notes.txt", b"hello world", "document")
    validate_upload("data.csv", b"name,value\nhello,1\n", "data")
    validate_upload("payload.json", b'{"hello": "world"}', "data")


def test_integration_add_chunks_with_none_metadata():
    """Real ChromaDB insert of PDF-style chunks (page set, times None)."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        vs = VectorStore(persist_dir=Path(tmp), collection="test_meta")
        chunks = [
            {
                "id": "c1", "content": "The budget was increased by twenty percent this year.",
                "type": "pdf", "source": "test.pdf", "page": 1,
                "start_time": None, "end_time": None, "metadata": {"index": "0", "chars": "60"},
            },
            {
                "id": "c2", "content": "Second page explains the roadmap for next quarter.",
                "type": "pdf", "source": "test.pdf", "page": 2,
                "start_time": None, "end_time": None, "metadata": {},
            },
        ]
        embeddings = [[0.1] * 8, [0.2] * 8]
        vs.add_chunks(chunks, embeddings)  # must not raise
        assert vs.count() == 2
        vs.delete_source("test.pdf")
        assert vs.count() == 0


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in tests:
        fn()
        print(f"PASS  {fn.__name__}")
    print(f"\n{len(tests)} tests passed.")