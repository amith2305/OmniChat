# 🤖 OmniChat AI

**Multimodal RAG-Powered Media Intelligence Chatbot**

OmniChat AI is a powerful local-first AI assistant that lets you chat with your documents, images, audio, and video files using advanced Retrieval-Augmented Generation (RAG) technology. Built with Python 3.14, FastAPI, and Llama 3.2 via Ollama.

---

## ✨ Features

### 📄 Document Intelligence
- **PDF Chat**: Upload and chat with PDF documents (including scanned PDFs with OCR)
- **Multi-page Support**: Automatic page-by-page processing with source references
- **OCR Integration**: Tesseract-powered text extraction from scanned documents

### 🖼️ Image Analysis
- **Vision Understanding**: Analyze images, diagrams, charts, and screenshots
- **Text Extraction**: Combined OCR and vision model descriptions
- **Visual Q&A**: Ask questions about image content

### 🎵 Audio Intelligence
- **Audio Transcription**: Faster-Whisper powered speech-to-text with timestamps
- **Timestamp Preservation**: Clickable timestamps linking to specific audio moments
- **Multi-format Support**: MP3, WAV, M4A, and more

### 🎬 Video Analysis
- **Dual Pipeline**: Analyzes both spoken content (audio) and visual content (frames)
- **Frame Sampling**: Configurable frame extraction and vision analysis
- **Timestamped References**: Link answers to specific video moments
- **Cross-modal Search**: Ask "What did they say about the diagram shown on screen?"

### 🔍 Advanced RAG System
- **Multimodal Vector Search**: Single search across all media types
- **Smart Chunking**: Context-aware segmentation (paragraphs, time intervals, scenes)
- **Source Attribution**: Every answer includes page numbers, timestamps, and file references
- **Conversation Memory**: Follow-up questions with context retention

### 🛠️ Additional Features
- **Document Summarization**: AI-generated summaries using map-reduce approach
- **Topic Extraction**: Automatic keyword and topic identification
- **Voice Input**: Speech-to-text for hands-free querying
- **Text-to-Speech**: Listen to AI responses
- **Export**: Save chat history and summaries as TXT or PDF

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                  HTML/CSS/JS or React               │
│                     FRONTEND                        │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│                    FastAPI                          │
│                    BACKEND                          │
└──────────────────────┬──────────────────────────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
       ▼               ▼               ▼
     PDF            IMAGE            AUDIO
       │               │               │
  PyMuPDF/OCR    Vision/OCR        Whisper
       │               │               │
       └───────────────┼───────────────┘
                       │
                     VIDEO
                       │
              ┌────────┴────────┐
              ▼                 ▼
           Whisper           OpenCV
              │                 │
           Audio             Frames
              │                 │
              │             Vision
              │                 │
              └────────┬────────┘
                       ▼
              COMMON CHUNKS
                       │
                       ▼
          Sentence Transformers
                       │
                       ▼
                   ChromaDB
                       │
                       ▼
                TOP-K RETRIEVAL
                       │
                       ▼
              Llama 3.2 / Ollama
                       │
                       ▼
                   RESPONSE
```

---

## 📋 Prerequisites

### Required Software

1. **Python 3.14+**
   ```bash
   python --version  # Should show Python 3.14.x
   ```

2. **Ollama** - Local LLM server
   - Download: https://ollama.ai
   - Install and start the Ollama service
   ```bash
   # Pull required models
   ollama pull llama3.2:3b
   ollama pull llava:latest  # or another vision model
   ```

3. **Tesseract OCR** - For scanned PDFs and images
   - **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

4. **FFmpeg** - For video audio extraction
   - **Windows**: Download from https://ffmpeg.org/download.html
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg`

---

## 🚀 Installation

### 1. Clone the Repository

```bash
cd OmniChat_AI
```

### 2. Backend Setup

```bash
cd backend

# Activate virtual environment (already created)
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create and configure environment file
cp .env.example .env
# Edit .env with your preferred settings
```

### 3. Frontend Setup (if using React)

```bash
cd ../frontend

# Install dependencies
npm install

# Build for production
npm run build

# Or run development server
npm run dev
```

### 4. Verify Ollama Models

```bash
# Ensure required models are available
ollama list

# Should show:
# llama3.2:3b
# llava:latest (or your chosen vision model)
```

---

## ⚙️ Configuration

Edit `backend/.env` to configure:

### Core Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `LLM_MODEL` | `llama3.2:3b` | Primary text generation model |
| `VISION_MODEL` | `llava:latest` | Vision-capable model for images/video |
| `WHISPER_MODEL` | `base` | Whisper model size (tiny/base/small/medium/large) |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Text embedding model |

### RAG Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `TOP_K` | `5` | Number of chunks to retrieve per query |
| `CHUNK_SIZE` | `800` | Characters per chunk |
| `CHUNK_OVERLAP` | `100` | Overlap between chunks |
| `HISTORY_WINDOW` | `8` | Recent conversation turns to include |

### Processing Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `VIDEO_FRAME_INTERVAL` | `1.0` | Seconds between sampled video frames |
| `OCR_MIN_TEXT_LENGTH` | `40` | Min text length before triggering OCR |
| `MAX_FILE_SIZE_MB` | `500` | Maximum upload file size |

See `.env.example` for all available options.

---

## 🎯 Usage

### Starting the Backend

```bash
cd backend

# Activate virtual environment
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### Accessing the Frontend

- **Production**: Open http://localhost:8000 (FastAPI serves built frontend)
- **Development**: Run `npm run dev` in `frontend/` → http://localhost:5173

### Using OmniChat AI

1. **Upload Files**: Drag & drop or browse for PDF, images, audio, or video files
2. **Wait for Processing**: Files are indexed automatically (progress shown)
3. **Ask Questions**: Type or speak your questions
4. **View Sources**: Click timestamps to jump to audio/video positions
5. **Summarize**: Generate AI summaries of uploaded files
6. **Extract Topics**: Identify key themes and keywords
7. **Export**: Save chat history or summaries as TXT/PDF

---

## 📚 API Endpoints

### Health & Status

- `GET /api/health` - System health check (Ollama, Whisper, Tesseract, ChromaDB status)

### File Management

- `POST /api/upload` - Upload and process a file
- `GET /api/upload/{file_id}/status` - Check processing status
- `GET /api/files` - List all indexed files
- `DELETE /api/files/{source}` - Delete a file from index
- `GET /api/media?rel={path}` - Serve uploaded media files

### Chat & RAG

- `POST /api/chat` - Ask a question (RAG pipeline)
  ```json
  {
    "question": "What is the main topic?",
    "session_id": "optional-session-id",
    "source": "optional-filename-filter"
  }
  ```
- `GET /api/history?session_id={id}` - Get chat history
- `POST /api/history/reset` - Clear conversation history

### Analysis

- `POST /api/summarize` - Generate document/media summary
  ```json
  {
    "source": "filename.pdf",
    "title": "Optional title"
  }
  ```
- `POST /api/topics` - Extract topics from document
  ```json
  {
    "source": "filename.pdf"
  }
  ```

### Voice & Export

- `POST /api/stt` - Speech-to-text (upload audio file)
- `POST /api/tts` - Text-to-speech (returns audio URL)
  ```json
  {
    "text": "Text to convert to speech"
  }
  ```
- `POST /api/export` - Export chat or summary
  ```json
  {
    "kind": "chat",  // or "summary"
    "format": "txt",  // or "pdf"
    "session_id": "your-session-id"
  }
  ```

---

## 📁 Project Structure

```
OmniChat_AI/
│
├── backend/
│   ├── .venv/              # Python virtual environment
│   ├── app/
│   │   ├── main.py         # FastAPI entry point
│   │   ├── config.py       # Configuration from .env
│   │   │
│   │   ├── api/            # API endpoints
│   │   │   ├── chat.py     # Chat & conversation
│   │   │   ├── upload.py   # File upload & processing
│   │   │   ├── media.py    # Summarize, topics, export, STT, TTS
│   │   │   └── health.py   # Health check
│   │   │
│   │   ├── processors/     # Media processors
│   │   │   ├── pdf_processor.py
│   │   │   ├── image_processor.py
│   │   │   ├── audio_processor.py
│   │   │   └── video_processor.py
│   │   │
│   │   ├── rag/            # RAG pipeline
│   │   │   ├── chunker.py      # Multimodal chunking
│   │   │   ├── embeddings.py   # Sentence Transformers
│   │   │   ├── vector_store.py # ChromaDB interface
│   │   │   ├── retriever.py    # Query & retrieval
│   │   │   └── pipeline.py     # End-to-end RAG
│   │   │
│   │   ├── llm/            # LLM integration
│   │   │   ├── ollama.py   # Ollama client
│   │   │   └── prompts.py  # System prompts
│   │   │
│   │   ├── services/       # AI services
│   │   │   ├── whisper.py  # Audio transcription
│   │   │   ├── vision.py   # Image/frame description
│   │   │   ├── ocr.py      # Tesseract OCR
│   │   │   └── tts.py      # Text-to-speech
│   │   │
│   │   ├── memory/         # Conversation memory
│   │   │   └── conversation.py
│   │   │
│   │   └── utils/          # Utilities
│   │       ├── files.py
│   │       ├── logging.py
│   │       └── validation.py
│   │
│   ├── data/               # Storage (created automatically)
│   │   ├── uploads/        # Uploaded files
│   │   ├── processed/      # Processed intermediates
│   │   ├── audio/          # Extracted audio
│   │   ├── frames/         # Extracted video frames
│   │   ├── exports/        # Exported files
│   │   └── chroma/         # ChromaDB persistent storage
│   │
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example        # Configuration template
│   └── README.md
│
└── frontend/               # React UI (or vanilla HTML/CSS/JS)
    ├── src/
    ├── dist/               # Production build
    ├── index.html
    ├── package.json
    └── vite.config.js
```

---

## 🧪 Testing

### Test Each Feature

#### 1. PDF Processing

```bash
# Upload a normal PDF
curl -X POST http://localhost:8000/api/upload \
  -F "file=@document.pdf"

# Upload a scanned PDF (OCR will activate)
curl -X POST http://localhost:8000/api/upload \
  -F "file=@scanned.pdf"

# Ask a question
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic of this document?"}'
```

#### 2. Image Analysis

```bash
# Upload an image
curl -X POST http://localhost:8000/api/upload \
  -F "file=@diagram.png"

# Ask about the image
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What does this diagram show?"}'
```

#### 3. Audio Transcription

```bash
# Upload audio file
curl -X POST http://localhost:8000/api/upload \
  -F "file=@lecture.mp3"

# Query the transcript
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What was discussed about neural networks?"}'
```

#### 4. Video Analysis

```bash
# Upload video
curl -X POST http://localhost:8000/api/upload \
  -F "file=@presentation.mp4"

# Cross-modal query
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What did the speaker say about the chart shown at 2:30?"}'
```

#### 5. Summarization

```bash
curl -X POST http://localhost:8000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{"source": "document.pdf", "title": "Research Paper"}'
```

#### 6. Topic Extraction

```bash
curl -X POST http://localhost:8000/api/topics \
  -H "Content-Type: application/json" \
  -d '{"source": "document.pdf"}'
```

---

## 🐛 Troubleshooting

### Ollama Connection Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama service
# Windows: Restart from system tray
# macOS/Linux: systemctl restart ollama
```

### Model Not Found

```bash
# List available models
ollama list

# Pull missing model
ollama pull llama3.2:3b
ollama pull llava:latest
```

### Tesseract Not Found

```bash
# Verify Tesseract installation
tesseract --version

# If not found, add to PATH or set in .env:
TESSERACT_CMD=/path/to/tesseract
```

### FFmpeg Not Found

```bash
# Verify FFmpeg installation
ffmpeg -version

# If not found, install via package manager or add to PATH
```

### ChromaDB Errors

```bash
# Reset ChromaDB (WARNING: deletes all indexed data)
rm -rf backend/data/chroma/*
```

### Port Already in Use

```bash
# Kill process on port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

---

## ⚠️ Known Limitations

- **Large Videos**: High-resolution videos may take significant time to process
- **Frame Sampling**: Fast visual changes may be missed between sampled frames
- **Audio Quality**: Noisy audio or multiple speakers can reduce transcription accuracy
- **OCR Accuracy**: Poor quality scans may produce incorrect text extraction
- **Complex PDF Layouts**: Multi-column or table-heavy PDFs may have extraction issues
- **Context Window**: Llama 3.2 3B has limited context; very long documents are chunked
- **Hallucination Risk**: LLM may occasionally generate plausible but incorrect information
- **Conversation Memory**: Limited to recent turns (configurable via `HISTORY_WINDOW`)
- **Local Only**: No cloud backup; all data stored locally

---

## 🛡️ Security & Privacy

- **100% Local**: All processing happens on your machine
- **No Data Sent to Cloud**: Your files never leave your computer
- **No Authentication**: Designed for single-user local use
- **File Validation**: Basic file type and size validation
- **Path Security**: File serving includes path traversal protection

**For multi-user deployments**: Add authentication, rate limiting, and enhanced security measures.

---

## 🔧 Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend Framework** | FastAPI (Python 3.14) |
| **LLM** | Llama 3.2 3B via Ollama |
| **Vision Model** | LLaVA or compatible via Ollama |
| **Embeddings** | Sentence Transformers (all-MiniLM-L6-v2) |
| **Vector Database** | ChromaDB (persistent local storage) |
| **Speech-to-Text** | Faster-Whisper |
| **OCR** | Tesseract |
| **PDF Processing** | PyMuPDF (fitz) |
| **Image Processing** | Pillow |
| **Video Processing** | OpenCV + FFmpeg |
| **Text-to-Speech** | pyttsx3 |
| **Frontend** | React + Vite (or vanilla HTML/CSS/JS) |

---

## 📝 License

This project is provided as-is for educational and personal use.

---

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) - Local LLM infrastructure
- [Llama 3.2](https://ai.meta.com/llama/) - Meta's open LLM
- [ChromaDB](https://www.trychroma.com/) - Open-source vector database
- [Sentence Transformers](https://www.sbert.net/) - State-of-the-art embeddings
- [Faster-Whisper](https://github.com/guillaumekln/faster-whisper) - Efficient speech recognition
- [Tesseract](https://github.com/tesseract-ocr/tesseract) - OCR engine
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework

---

## 📧 Support

For issues, questions, or contributions, please refer to the project documentation or raise an issue in the repository.

---

**Built with ❤️ using Python, FastAPI, and Llama 3.2**

*OmniChat AI - Your Local Multimodal AI Assistant*
