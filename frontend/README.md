# OmniChat AI

Multimodal RAG application that allows users to upload PDFs, audio files, and videos and chat with them. Extracts text, transcribes speech, analyzes video frames, generates embeddings, stores them in FAISS, and answers questions using an LLM.

## Tech Stack

- **FastAPI** - Async Python web framework
- **LangChain / LLM** - OpenAI GPT-4o / Gemini
- **Embeddings** - Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Store** - FAISS
- **STT** - Whisper Base
- **TTS** - Kitten TTS
- **PDF** - PyMuPDF, pdfplumber, PyPDF2, Tesseract OCR
- **Video** - MoviePy, OpenCV
- **NLP** - spaCy, NLTK
- **Database** - PostgreSQL (async), Redis, Celery
- **Auth** - JWT

## Project Structure

```
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── dependencies.py
│   ├── websocket.py
│   ├── routes/        # API route handlers
│   ├── services/      # Business logic
│   ├── database/      # ORM models, session, CRUD
│   ├── utils/         # Logger, chunking, timestamps
│   └── schemas/       # Pydantic models
├── uploads/
├── generated_audio/
├── vector_store/
├── .env
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL
- Redis

### Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Copy and edit .env
cp .env.example .env
```

### Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
docker-compose up -d
```

## API Endpoints

| Method | Endpoint              | Description               |
|--------|-----------------------|---------------------------|
| POST   | /upload/pdf           | Upload PDF file           |
| POST   | /upload/audio         | Upload audio file         |
| POST   | /upload/video         | Upload video file         |
| POST   | /chat                 | Ask a question            |
| POST   | /stt                  | Speech-to-text            |
| POST   | /tts                  | Text-to-speech            |
| POST   | /summarize            | Summarize session content |
| GET    | /history/{session_id} | Get chat history          |
| GET    | /topics/{session_id}  | Extract topics            |
| WS     | /ws/{session_id}      | Real-time chat            |
| GET    | /health               | Health check              |
