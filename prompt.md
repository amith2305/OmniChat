# OMNICHAT AI — COMPLETE MULTIMODAL RAG SYSTEM

You are the lead developer responsible for implementing the complete **OmniChat AI** application.

You are working on an existing repository.

The goal is to transform it into a simple but fully functional **multimodal RAG + LLM media intelligence application** that can read documents, understand images, listen to audio, analyze video, and allow the user to chat with all of them.

---

# 1. FIRST: INSPECT THE EXISTING PROJECT

DO NOT start coding immediately.

First inspect the entire repository.

You MUST:

1. Inspect the complete project structure.
2. Read the existing `README.md`.
3. Read existing backend code.
4. Read existing frontend code.
5. Identify existing dependencies.
6. Identify existing APIs.
7. Identify already implemented features.
8. Identify features that are missing.
9. Preserve useful existing functionality.
10. Avoid rewriting working code unnecessarily.

The uploaded OmniChat AI specification is the functional reference for the required features.

Do not remove a feature simply because the new architecture is different.

After understanding the repository, create a short implementation plan and then implement it.

---

# 2. CORE REQUIREMENT

Build OmniChat AI as a:

> **Multimodal RAG-powered media intelligence chatbot**

The system must support:

```text
📄 PDF
🖼️ Image
🎵 Audio
🎬 Video
```

The user should be able to upload media and chat with it naturally.

The system should understand:

```text
PDF text
PDF scanned text
Images
Image text
Audio speech
Video speech
Video visual content
```

All of this should eventually participate in a **shared searchable RAG system**.

The specification describes the application as a media intelligence hub that can read, listen and watch rather than being limited to PDFs.

---

# 3. TECHNOLOGY REQUIREMENTS

Use:

```text
Python 3.14
FastAPI
HTML
CSS
Vanilla JavaScript
Ollama
Llama 3B
Sentence Transformers
ChromaDB
PyMuPDF
Tesseract
Whisper
OpenCV
Pillow
pyttsx3 / gTTS
spaCy / NLTK where useful
```

The exact dependencies should remain minimal.

---

# 4. VERY IMPORTANT — NO OVER-ENGINEERING

Use **pure/classic Python architecture**.

Do NOT use:

```text
LangChain
LlamaIndex
Haystack
CrewAI
AutoGen
LangGraph
React
Next.js
Vue
Angular
Streamlit
Tailwind
Bootstrap
Celery
Redis
Docker
```

unless an existing project dependency absolutely requires something.

Do not introduce a framework simply because it is popular.

Implement the RAG pipeline using normal Python classes and functions.

The code should be understandable to a Python developer.

---

# 5. PYTHON ENVIRONMENT

Use the existing:

```text
.venv
```

Do NOT create another virtual environment.

The backend must run using Python 3.14.

Verify:

```bash
python --version
```

and ensure it is Python 3.14.x.

Dependencies must be installable with:

```bash
pip install -r requirements.txt
```

Do not use a different Python environment.

---

# 6. FRONTEND

Do NOT use Streamlit.

Create the frontend using only:

```text
HTML
CSS
Vanilla JavaScript
```

Structure:

```text
frontend/
├── index.html
├── style.css
└── script.js
```

FastAPI should serve this frontend directly.

The user should be able to open:

```text
http://localhost:8000
```

and use the application.

No Node.js development server should be required.

---

# 7. MAIN FRONTEND EXPERIENCE

Create a clean responsive interface.

Layout:

```text
┌─────────────────────────────────────────────────────┐
│                    OmniChat AI                      │
│              Multimodal RAG Assistant               │
├──────────────────────┬──────────────────────────────┤
│                      │                              │
│    MEDIA PREVIEW     │            CHAT              │
│                      │                              │
│    PDF               │ User: Explain this          │
│    Image             │                              │
│    Audio             │ AI: ...                     │
│    Video             │                              │
│                      │ Source: Page 4               │
│    ▶ Player          │ Source: 02:14–02:45         │
│                      │                              │
│                      │ [Ask something...] [🎤]     │
│                      │                         Send │
└──────────────────────┴──────────────────────────────┘
```

The UI should contain:

* application header
* upload area
* drag and drop
* media preview
* chat
* chat history
* source references
* timestamps
* summarize button
* topics button
* voice input
* text-to-speech
* export
* processing status
* error messages

---

# 8. SUPPORTED FILE TYPES

Support:

## PDF

```text
.pdf
```

## Images

```text
.png
.jpg
.jpeg
.webp
```

## Audio

```text
.mp3
.wav
.m4a
```

## Video

```text
.mp4
.mkv
```

Validate files before processing.

Do not silently accept arbitrary file types.

---

# 9. MULTIMODAL RAG ARCHITECTURE

The architecture should be:

```text
                         USER
                          │
                          ▼
                   HTML/CSS/JS
                          │
                       FastAPI
                          │
             ┌────────────┼────────────┐
             │            │            │
             ▼            ▼            ▼
            PDF         IMAGE        AUDIO
             │            │            │
             ▼            ▼            ▼
        Text + OCR   Vision + OCR   Whisper
             │            │            │
             └────────────┼────────────┘
                          │
                         VIDEO
                          │
                 ┌────────┴────────┐
                 ▼                 ▼
              Whisper           OpenCV
                 │                 │
                 │            Video Frames
                 │                 │
                 │            Vision Model
                 │                 │
                 └────────┬────────┘
                          ▼
                  MULTIMODAL CHUNKS
                          │
                          ▼
                Sentence Transformers
                          │
                          ▼
                       ChromaDB
                          │
                          ▼
                      Retrieval
                          │
                          ▼
                    Llama 3B
                     Ollama
                          │
                          ▼
                       ANSWER
```

---

# 10. LLM — LLAMA 3B THROUGH OLLAMA

The primary generation model MUST be:

```text
Llama 3B
```

running through:

```text
Ollama
```

Do not replace it with OpenAI GPT-4o or Gemini.

Use configuration:

```env
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=llama3:3b
```

The exact Ollama model tag can remain configurable.

Llama 3B is responsible for:

* RAG question answering
* conversational responses
* document summarization
* topic extraction
* contextual follow-up questions
* query understanding where useful

---

# 11. VISION MODEL

Do NOT assume the text-only Llama 3B model can understand images.

Use a separate configurable vision-capable Ollama model for:

* standalone images
* video frames
* image understanding
* visual descriptions

Example configuration:

```env
VISION_MODEL=
```

If the selected Llama model is vision-capable, it may be used.

Otherwise use the configured vision model.

Do not silently replace the main Llama 3B generation model.

---

# 12. PDF UPLOAD

Implement complete PDF support.

Pipeline:

```text
PDF
 ↓
file validation
 ↓
save file
 ↓
PyMuPDF text extraction
 ↓
if text is insufficient
 ↓
Tesseract OCR
 ↓
multimodal/document chunking
 ↓
embeddings
 ↓
ChromaDB
```

Support:

* normal PDFs
* scanned PDFs
* multi-page PDFs

The specification explicitly requires PDF upload and scanned-PDF OCR.

---

# 13. PDF PREVIEW

The frontend must display the uploaded PDF.

Use the browser's PDF rendering capability or a lightweight viewer.

The preview should be visible beside the chat.

Do not require a separate PDF application.

The original specification includes a PDF preview alongside the chat.

---

# 14. TEXT EXTRACTION

Use:

```text
PyMuPDF
```

and optionally:

```text
pdfplumber
```

if required for difficult layouts.

Extract:

* text
* page number
* document name

Preserve page metadata.

The source specification describes PyMuPDF/pdfplumber-based extraction and notes that complex layouts can produce imperfect ordering.

---

# 15. OCR

Use:

```text
Tesseract
pytesseract
```

for scanned PDFs and images containing text.

Pipeline:

```text
page/image
 ↓
image
 ↓
Tesseract
 ↓
text
 ↓
chunk
```

Do not OCR normal PDFs unnecessarily if clean text extraction already works.

---

# 16. IMAGE SUPPORT

Standalone image upload is REQUIRED.

For an image:

```text
IMAGE
 ↓
Pillow
 ↓
OCR if useful
 ↓
VISION MODEL
 ↓
visual description
 ↓
common chunk
 ↓
embedding
 ↓
ChromaDB
```

Store both:

```text
image description
original image reference
```

Do not discard the original image.

Image metadata should include:

```text
type=image
source=<filename>
image_path=<path/reference>
```

The user should be able to ask:

```text
"What is in this image?"
"What does this diagram show?"
"Explain the text in this image."
```

---

# 17. DOCUMENT CHUNKING

Do NOT use only fixed character splitting.

Create a simple multimodal chunking system.

For PDFs:

```text
paragraph/page based
```

For audio:

```text
time interval based
```

For video:

```text
scene/time based
```

For images:

```text
one or more semantic descriptions
```

The specification specifically describes the evolution from document chunking to multimodal chunking using paragraph, time interval and scene/time blocks.

Each chunk must preserve metadata.

---

# 18. AUDIO CHAT AND TRANSCRIPTION

Support:

```text
MP3
WAV
M4A
```

Use Whisper.

Pipeline:

```text
Audio
 ↓
Whisper
 ↓
timestamped transcript
 ↓
chunk transcript
 ↓
embeddings
 ↓
ChromaDB
```

The user should be able to ask questions directly about the audio.

The specification requires direct audio chat and timestamped Whisper transcription.

---

# 19. AUDIO TIMESTAMPS

Every transcript chunk should preserve:

```text
start_time
end_time
```

Example:

```text
02:14 - 02:45
"The professor explains..."
```

When RAG retrieves that chunk, the timestamp must survive all the way to the final API response.

---

# 20. VIDEO CHAT AND ANALYSIS

Support:

```text
MP4
MKV
```

The user must be able to ask about:

```text
what was said
+
what appeared on screen
```

The specification explicitly requires both spoken and visual video analysis.

---

# 21. VIDEO AUDIO PIPELINE

Extract video audio using:

```text
MoviePy
```

or an equivalent simple implementation.

Then:

```text
Video
 ↓
Audio extraction
 ↓
Whisper
 ↓
timestamped transcript
```

---

# 22. VIDEO FRAME PIPELINE

Use:

```text
OpenCV
```

or Decord if necessary.

Sample frames at a configurable interval.

Example:

```env
VIDEO_FRAME_INTERVAL=1
```

Do not process every frame.

For each sampled frame:

```text
frame
 ↓
vision model
 ↓
visual description
 ↓
timestamp
 ↓
multimodal chunk
 ↓
embedding
 ↓
ChromaDB
```

The specification describes approximately one-second frame sampling and warns that very fast visual changes may be missed.

---

# 23. SHARED VECTOR DATABASE

Use:

```text
ChromaDB
```

with persistent local storage.

The database must contain:

```text
PDF text
OCR text
image descriptions
audio transcripts
video transcripts
video frame descriptions
```

in a common searchable system.

This is a CORE REQUIREMENT.

A query should be able to search across formats simultaneously.

For example:

```text
"What did they say about the budget?"
```

should potentially retrieve:

```text
PDF → budget information
Audio → budget discussion
Video → budget slide
```

The specification explicitly requires this cross-format search.

---

# 24. EMBEDDINGS

Use:

```text
Sentence Transformers
```

for embeddings.

Create:

```text
embedding_service.py
```

with:

```python
embed_text()
embed_documents()
embed_query()
```

Do NOT use Llama 3B as the embedding model.

---

# 25. COMMON CHUNK SCHEMA

Use a standard internal representation.

Example:

```python
{
    "id": "...",
    "content": "...",
    "type": "pdf",
    "source": "document.pdf",
    "page": 5,
    "start_time": None,
    "end_time": None,
    "metadata": {}
}
```

Audio:

```python
{
    "id": "...",
    "content": "...",
    "type": "audio",
    "source": "lecture.mp3",
    "page": None,
    "start_time": 134.0,
    "end_time": 165.0,
    "metadata": {}
}
```

Video frame:

```python
{
    "id": "...",
    "content": "Professor showing a neural network diagram.",
    "type": "video_frame",
    "source": "lecture.mp4",
    "start_time": 142.0,
    "end_time": 143.0,
    "metadata": {}
}
```

Image:

```python
{
    "id": "...",
    "content": "A neural network diagram...",
    "type": "image",
    "source": "diagram.png",
    "metadata": {}
}
```

---

# 26. RAG RETRIEVAL

Implement simple RAG:

```text
User Query
 ↓
Query Embedding
 ↓
ChromaDB
 ↓
Top-K results
 ↓
Context construction
 ↓
Llama 3B
 ↓
Answer
```

Configuration:

```env
TOP_K=5
```

The original RAG behavior is query embedding → similarity matching → top chunks → LLM context.

---

# 27. RAG ANSWER RULES

Llama 3B should receive:

```text
SYSTEM INSTRUCTION

USER QUESTION

RELEVANT CONTEXT

CONVERSATION HISTORY
```

The prompt should tell the model:

* answer using retrieved context
* do not invent facts
* distinguish uncertainty
* use source metadata
* provide timestamps when relevant
* provide page references when relevant
* answer naturally
* handle follow-up questions

If the answer cannot be found, say so instead of hallucinating.

---

# 28. SOURCE REFERENCES

Every retrieved result should retain:

```text
source
type
page
timestamp
```

The frontend should display references such as:

```text
📄 Page 5
```

```text
🎵 02:14 – 02:45
```

```text
🎬 01:42
```

```text
🖼️ diagram.png
```

---

# 29. CLICKABLE TIMESTAMPS

Audio/video references must be clickable.

When the user clicks:

```text
02:14
```

JavaScript should set:

```javascript
media.currentTime = 134;
```

and begin playback or position the player.

This implements the timestamp referencing feature described in the specification.

---

# 30. MULTIMODAL PREVIEW PANEL

Create a split-screen preview.

For:

```text
PDF → PDF viewer
Image → image viewer
Audio → audio player
Video → video player
```

The media preview should appear next to the chat.

If a retrieved answer contains a timestamp, clicking it should seek the audio/video player.

The specification describes this media-preview-plus-chat experience.

---

# 31. PDF CHAT

Implement normal PDF conversation.

Every question should go through:

```text
question
 ↓
embedding
 ↓
retrieval
 ↓
Llama 3B
 ↓
answer
```

The specification defines PDF Chat as a normal chat thread where each question runs through the RAG pipeline.

---

# 32. DOCUMENT SUMMARIZATION

Implement:

```text
Summarize
```

for:

* PDFs
* audio
* video
* images where meaningful

For long documents:

```text
chunks
 ↓
chunk summaries
 ↓
combined summary
```

Do not send extremely large documents directly to Llama 3B.

The original document specifies chunk-level summaries followed by a combined summary.

---

# 33. TOPIC EXTRACTION

Implement topic extraction.

Use simple NLP and/or Llama 3B.

Topics should be returned in structured form.

Example:

```text
Machine Learning
Neural Networks
Deep Learning
Optimization
```

The specification describes spaCy/NLTK-based topic extraction as an existing feature.

---

# 34. CHAT HISTORY

Store current-session:

```text
user messages
assistant messages
timestamps
```

The frontend should display the complete chat thread.

The backend should retain the session history.

---

# 35. CONVERSATION MEMORY

Support follow-up questions.

Example:

```text
User:
What is the first concept?

AI:
The first concept is...

User:
What about the second one?
```

The second question should understand what "second one" refers to.

Use recent conversation turns as context.

Do NOT build infinite memory.

Keep a configurable recent-message window.

This matches the specification's conversation-memory behavior.

---

# 36. EXPORT

Implement:

```text
Export Chat
Export Summary
```

Support:

```text
TXT
PDF
```

The export should include:

* user questions
* assistant answers
* sources where available
* timestamps where available

Basic formatting is sufficient.

The specification explicitly includes export of summaries or complete chat to text/PDF.

---

# 37. TEXT-TO-SPEECH

Implement TTS.

Provide a speaker button for assistant answers.

Use:

```text
pyttsx3
```

for offline speech where practical.

Optionally support:

```text
gTTS
```

if configured.

Keep the implementation modular:

```python
text_to_speech(text)
```

The specification includes both offline pyttsx3 and gTTS approaches.

---

# 38. SPEECH-TO-TEXT

Users must be able to speak their questions.

Support browser microphone input and/or backend Whisper.

The important flow is:

```text
Voice
 ↓
Speech-to-text
 ↓
Text query
 ↓
Normal RAG pipeline
```

Do not create a separate voice RAG system.

The specification defines speech input as being converted into a normal text question.

---

# 39. FASTAPI API

Implement clean endpoints similar to:

```text
GET  /
GET  /api/health

POST /api/upload
POST /api/chat

POST /api/summarize
POST /api/topics

GET  /api/history
POST /api/export

POST /api/stt
POST /api/tts
```

Adapt to existing routes if they already exist.

Do not create unnecessary endpoints.

---

# 40. ASYNC PROCESSING

Large uploads such as video should not freeze the API.

Use FastAPI background tasks or a simple internal job mechanism.

Do NOT introduce Celery or Redis.

The backend should provide processing status.

Example:

```text
Uploading...
Processing...
Transcribing...
Analyzing frames...
Creating embeddings...
Indexing...
Ready
```

---

# 41. FILE STORAGE

Use:

```text
data/
├── uploads/
├── processed/
├── audio/
├── frames/
├── exports/
└── chroma/
```

Do not store large binary media inside ChromaDB.

ChromaDB should store embeddings, text/descriptions and metadata.

Original media remains in file storage.

---

# 42. CONFIGURATION

Create:

```text
.env.example
```

Example:

```env
OLLAMA_BASE_URL=http://localhost:11434

LLM_MODEL=llama3:3b
VISION_MODEL=

EMBEDDING_MODEL=

TOP_K=5

CHUNK_SIZE=800
CHUNK_OVERLAP=100

VIDEO_FRAME_INTERVAL=1

UPLOAD_DIR=data/uploads
CHROMA_DIR=data/chroma

MAX_FILE_SIZE_MB=500
```

Do not hard-code these values throughout the code.

---

# 43. PROJECT STRUCTURE

Use a simple structure similar to:

```text
OmniChat_AI/
│
├── backend/
│   │
│   ├── .venv/
│   │
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   ├── chat.py
│   │   │   ├── upload.py
│   │   │   ├── media.py
│   │   │   └── health.py
│   │   │
│   │   ├── processors/
│   │   │   ├── pdf_processor.py
│   │   │   ├── image_processor.py
│   │   │   ├── audio_processor.py
│   │   │   └── video_processor.py
│   │   │
│   │   ├── rag/
│   │   │   ├── chunker.py
│   │   │   ├── embeddings.py
│   │   │   ├── vector_store.py
│   │   │   ├── retriever.py
│   │   │   └── pipeline.py
│   │   │
│   │   ├── llm/
│   │   │   ├── ollama.py
│   │   │   └── prompts.py
│   │   │
│   │   ├── services/
│   │   │   ├── whisper.py
│   │   │   ├── vision.py
│   │   │   ├── ocr.py
│   │   │   └── tts.py
│   │   │
│   │   ├── memory/
│   │   │   └── conversation.py
│   │   │
│   │   └── utils/
│   │       ├── files.py
│   │       └── logging.py
│   │
│   ├── data/
│   │   ├── uploads/
│   │   ├── processed/
│   │   ├── frames/
│   │   ├── exports/
│   │   └── chroma/
│   │
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
└── frontend/
    ├── index.html
    ├── style.css
    └── script.js
```

Adapt this to the existing repository instead of blindly replacing its structure.

---

# 44. KEEP PROCESSORS SEPARATE

Each media type should have a clear processor.

For example:

```python
process_pdf(path)
process_image(path)
process_audio(path)
process_video(path)
```

Each processor should return common chunks.

This makes the system easy to extend.

---

# 45. LOGGING

Use Python's built-in:

```python
logging
```

Log:

```text
[UPLOAD]
[PDF]
[OCR]
[IMAGE]
[WHISPER]
[VIDEO]
[VISION]
[CHUNK]
[EMBED]
[CHROMA]
[RETRIEVE]
[LLM]
[TTS]
[EXPORT]
```

Do not introduce a complex logging framework.

---

# 46. ERROR HANDLING

Handle:

```text
Ollama unavailable
Llama model unavailable
Vision model unavailable
Whisper unavailable
Tesseract unavailable
invalid file
unsupported format
corrupted PDF
corrupted audio
corrupted video
empty document
embedding failure
ChromaDB failure
```

Errors should produce useful messages in the frontend.

Do not crash the whole server because one media file failed.

---

# 47. README REQUIREMENTS

Read the existing README first.

Then update it.

The README must contain:

```text
1. OmniChat AI overview
2. Features
3. Complete feature list
4. Architecture
5. Multimodal RAG flow
6. Supported file types
7. Technology stack
8. Python 3.14 requirement
9. .venv setup
10. Ollama setup
11. Llama 3B setup
12. Vision model setup
13. Whisper setup
14. Tesseract installation
15. FFmpeg/MoviePy requirements
16. Installation
17. Environment variables
18. Running backend
19. Running frontend
20. API endpoints
21. Project structure
22. Troubleshooting
23. Known limitations
```

Do not document features that aren't implemented.

---

# 48. REQUIREMENTS.TXT

Only include packages actually used.

Avoid dependency bloat.

The requirements should cover the implemented backend.

System-level dependencies such as:

```text
Ollama
Tesseract
FFmpeg
```

must be documented separately in README.

---

# 49. TEST EVERYTHING

Before declaring completion, test every major feature.

## PDF

```text
normal PDF
scanned PDF
multi-page PDF
OCR
PDF preview
PDF chat
```

## Image

```text
PNG
JPG
diagram
OCR
vision understanding
image chat
```

## Audio

```text
MP3
WAV
M4A
transcription
timestamps
audio chat
```

## Video

```text
MP4
MKV
audio extraction
Whisper
frame sampling
vision analysis
timestamp retrieval
video chat
```

## RAG

Test:

```text
PDF-only question
image-only question
audio-only question
video-only question
cross-media question
follow-up question
```

Example:

```text
"What did the speaker say about the diagram shown on screen?"
```

The system should be able to retrieve both:

```text
audio transcript
+
video frame description
```

---

# 50. IMPORTANT LIMITATIONS

Do not pretend the system is perfect.

Document realistic limitations.

For example:

* large high-resolution videos can take significant processing time
* fast visual changes may be missed due to frame sampling
* noisy audio can reduce transcription quality
* multiple speakers may reduce transcription quality
* OCR can fail on poor scans
* complex PDF layouts may extract incorrectly
* retrieval quality depends on embeddings
* Llama 3B may hallucinate
* conversation memory is limited
* browser media streaming can depend on server configuration

## These limitations are explicitly discussed in the specification and should remain documented rather than hidden.

# 51. FINAL ARCHITECTURE

The final system should essentially be:

```text
                  ┌──────────────────────┐
                  │   HTML/CSS/JS        │
                  │      FRONTEND        │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │       FastAPI        │
                  │       BACKEND        │
                  └──────────┬───────────┘
                             │
        ┌────────────────────┼─────────────────────┐
        │                    │                     │
        ▼                    ▼                     ▼
      PDF                  IMAGE                 AUDIO
        │                    │                     │
  PyMuPDF/OCR          Vision/OCR              Whisper
        │                    │                     │
        └────────────────────┼─────────────────────┘
                             │
                            VIDEO
                             │
                    ┌────────┴────────┐
                    │                 │
                 Whisper           OpenCV
                    │                 │
                 Audio             Frames
                    │                 │
                    │             Vision
                    │                 │
                    └────────┬────────┘
                             │
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
                      CONTEXT BUILDER
                             │
                     ┌───────┴───────┐
                     │               │
              Chat History      Retrieved Media
                     │               │
                     └───────┬───────┘
                             ▼
                     Llama 3B / Ollama
                             │
                             ▼
                         RESPONSE
                             │
               ┌─────────────┼──────────────┐
               ▼             ▼              ▼
            Sources      Timestamps        TTS
               │             │              │
               └─────────────┼──────────────┘
                             ▼
                    HTML/CSS/JS FRONTEND
```

---

# 52. FINAL DEVELOPMENT RULE

Build this incrementally.

Recommended order:

```text
1. Existing repository inspection
2. FastAPI foundation
3. HTML/CSS/JS frontend
4. PDF processing
5. OCR
6. Chunking
7. Embeddings
8. ChromaDB
9. Llama 3B/Ollama
10. Basic RAG
11. Chat history
12. Summarization
13. Topic extraction
14. Image processing
15. Whisper audio processing
16. Video processing
17. Timestamp references
18. Multimodal retrieval
19. STT
20. TTS
21. Export
22. UI polishing
23. Error handling
24. Testing
25. README update
```

Do not attempt to build everything as one giant file.

---

# 53. COMPLETION REQUIREMENT

When finished, provide:

```text
1. What was implemented
2. Files created
3. Files modified
4. Dependencies added
5. Ollama models required
6. System dependencies required
7. How to activate .venv
8. How to start FastAPI
9. How to access the frontend
10. How to test PDF
11. How to test image
12. How to test audio
13. How to test video
14. Known limitations
```

Most importantly:

**Do not claim completion unless the implemented code actually supports the features listed above.**

Keep the implementation simple, local-first, modular and understandable.

The primary generation model is **Llama 3B through Ollama**.

The backend is **Python 3.14 + FastAPI**.

The frontend is **plain HTML + CSS + JavaScript**.

The RAG implementation is **custom classic Python**, not LangChain.

The vector database is **ChromaDB**.

The embedding system is **Sentence Transformers**.

All PDF, image, audio and video information must ultimately participate in the same searchable multimodal RAG pipeline.

## MODEL REQUIREMENTS — IMPORTANT

The required AI models are ALREADY DOWNLOADED locally.

DO NOT download, install, pull, fine-tune, or replace any AI model.

All model names must be configured through `.env`.

### LLM

Use the already-installed Ollama model:

LLM_MODEL=llama3.2:3b

Ollama configuration:

OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=llama3.2:3b

The backend must call this model through Ollama.

Do NOT use:
- OpenAI
- Gemini
- GPT
- Claude
- another LLM

unless explicitly required by the existing project.

---

### Speech-to-Text

Use `faster-whisper`.

Model:

WHISPER_MODEL=base

The `base` model is already available/configured as required.

Use Faster-Whisper for:

- uploaded audio transcription
- video audio transcription
- speech-to-text where backend transcription is required

The implementation must preserve timestamps.

Example:

{
    "text": "The neural network consists of...",
    "start_time": 12.4,
    "end_time": 17.8
}

Do NOT use the regular `openai-whisper` package.

Use:

```python
from faster_whisper import WhisperModel
