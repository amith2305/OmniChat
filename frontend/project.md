# OmniChat Frontend - Project Documentation

> **Scope: frontend only.** OmniChat is a multimodal RAG application (upload PDFs, audio, and videos and chat with them). The **backend** (FastAPI + LangChain + FAISS + Whisper + TTS) is being built separately by a teammate — see the root `README.md` for the full-stack architecture, backend structure, and API contract.
>
> This document only tracks the **React frontend** in this repo.

---

## Repo Layout

```
omnichat/
├── README.md            # Full-stack overview + backend API contract (friend's side)
├── project.md           # This file — frontend docs
├── todo.md              # Frontend task tracker
├── index.html           # Vite entry (fonts, root div)
├── vite.config.js
├── package.json
├── src/                 # React frontend (everything below)
│   ├── main.jsx
│   ├── App.jsx
│   ├── index.css        # Glassmorphism design tokens
│   ├── constants/
│   ├── utils/
│   ├── services/        # storage, documentParser, llm, libraryLoader
│   ├── hooks/           # useChat, useDocuments, useToast, useModel, ...
│   └── components/      # Sidebar, DocumentPane, ChatPane, SettingsModal, Toast
```

The original vanilla version (`omnichat.html/js/css`) was removed during cleanup (Session 4, see `history.md`).

---

## Quick Start

```bash
npm install
npm run dev        # start dev server
npm run build      # production build
npm run preview    # preview production build
```

---

## Tech Stack (Frontend)

| Layer       | Choice                                    |
| ----------- | ----------------------------------------- |
| Framework   | React 18 (`react`, `react-dom`)           |
| Build       | Vite 6 (`@vitejs/plugin-react`)           |
| Icons       | `lucide-react`                            |
| PDF parsing | pdf.js 3.4.120 (CDN, loaded at runtime)   |
| DOCX parsing| Mammoth 1.6.0 (CDN, loaded at runtime)    |
| Styling     | Plain CSS, CSS variables (no framework)   |

**Backend stack (friend's side, not maintained here):** FastAPI, LangChain, OpenAI GPT-4o / Gemini, Sentence Transformers, FAISS, Whisper, Kitten TTS, PyMuPDF, MoviePy, PostgreSQL, Redis, Celery, JWT — see `README.md`.

> The frontend currently calls LLM providers **directly** from the browser (`services/llm.js`) as a temporary standalone bridge. Once the backend is live, these calls move to the backend API (see Integration Plan below). The UI stays identical.

---

## File Structure

```
src/
├── main.jsx                    # ReactDOM entry
├── App.jsx                     # Root layout + global state wiring
├── index.css                   # Glassmorphism design tokens + globals
├── constants/
│   └── models.js               # Model options + API key label maps
├── utils/
│   └── formatting.js           # formatTime / formatNumber
├── services/
│   ├── storage.js              # localStorage: API keys, active model
│   ├── llm.js                  # Direct Gemini/OpenAI clients (temporary bridge)
│   ├── documentParser.js       # TXT/PDF/DOCX -> text
│   └── libraryLoader.js        # CDN loader for pdf.js / Mammoth
├── hooks/
│   ├── useToast.js
│   ├── useDocuments.js         # Files + upload/delete/clear + mock docs
│   ├── useChat.js              # Messages + send flow
│   ├── useModel.js             # Active AI provider
│   ├── useVoiceInput.js        # Web Speech API (mic)
│   └── useDocumentZoom.js      # Sheet zoom
└── components/
    ├── Sidebar/                # Model select, API key, upload, file list, nav
    ├── DocumentPane/           # DocumentHeader, DocumentSheet, DocumentStats,
    │                           # SummaryPanel, WelcomeScreen, LoadingOverlay
    ├── ChatPane/               # ChatBubble, ChatInput, TypingIndicator
    ├── SettingsModal/
    └── Toast/
```

Each feature/function lives in its own file so it is easy to track and swap out (important when wiring the backend).

---

## Feature Map (Current Frontend)

| Feature                 | File(s)                                                 |
| ----------------------- | ------------------------------------------------------- |
| Model switching         | `Sidebar.jsx` + `useModel.js` + `constants/models.js`   |
| API key entry + validate| `Sidebar.jsx` (live) + `SettingsModal.jsx` + `storage.js`|
| Upload PDF / TXT / DOCX | `Sidebar.jsx` + `useDocuments.js` + `documentParser.js` |
| PDF/DOCX library load   | `libraryLoader.js` (once in `App.jsx`)                  |
| AI summary (3 bullets)  | `useDocuments.js` + `llm.js` (`fetchSummaryFromLLM`)    |
| Chat with document      | `useChat.js` + `llm.js` (`fetchChatResponseFromLLM`)    |
| Voice input (mic -> text)| `useVoiceInput.js` + `ChatInput.jsx`                   |
| Document zoom           | `useDocumentZoom.js` + `DocumentHeader.jsx`             |
| Share insights          | `DocumentHeader.jsx` (clipboard)                        |
| Collapsible AI summary  | `SummaryPanel.jsx`                                      |
| Reset workspace         | `App.jsx` (`handleClearAll` -> `storage.clearAll`)      |
| Toast notifications     | `useToast.js` + `Toast.jsx`                             |

---

## Backend Integration Plan (Friend's FastAPI)

The frontend will consume the endpoints defined in `README.md`. Currently on hold until the backend is ready; UI components are already designed to slot in.

| Backend endpoint          | Frontend integration                                    | Status        |
| ------------------------- | ------------------------------------------------------- | ------------- |
| `POST /upload/pdf`        | Replaces client-side `documentParser` for PDFs          | Waiting backend|
| `POST /upload/audio`      | New audio upload UI (needs design)                      | Waiting backend|
| `POST /upload/video`      | New video upload UI (needs design)                      | Waiting backend|
| `POST /chat`              | Replaces `llm.js` chat call in `useChat.js`             | Waiting backend|
| `POST /summarize`         | Replaces `fetchSummaryFromLLM`                          | Waiting backend|
| `POST /stt`               | Optionally replace browser mic STT with Whisper          | Waiting backend|
| `POST /tts`               | New audio playback of AI answers                        | Waiting backend|
| `GET /history/{session_id}`| Session history panel (needs design)                   | Waiting backend|
| `GET /topics/{session_id}`| Topics extract panel (needs design)                     | Waiting backend|
| `WS /ws/{session_id}`     | Real-time streaming chat (replaces typing-wait pattern) | Waiting backend|
| `GET /health`             | Backend status indicator in the UI                      | Waiting backend|
| Auth (JWT)                | Login/session screens (needs design)                    | Waiting backend|

Until the backend is ready, the frontend keeps working standalone via `services/llm.js` and mock documents, so UI development is never blocked.

---

## Data Flow (current, direct-LLM mode)

```
App.jsx
 ├─ useModel() ──────────────── modelProvider ──► Sidebar / ChatPane
 ├─ useDocuments() ──────────── documents, activeDocument, uploadFile(...)
 │                                └─ parseFile() -> summary via llm.js
 ├─ useChat(activeDocument) ─── messages, sendMessage(text, provider)
 │                                └─ llm.js fetchChatResponseFromLLM()
 ├─ useToast() ──────────────── showToast(message, type)
 └─ SettingsModal / Toast

Sidebar -> onUpload(file)      -> uploadFile(file, modelProvider)
Sidebar -> onSelectDoc(name)   -> setActiveDoc(name)
Sidebar -> onDeleteDoc(name)   -> deleteDocument(name)
Sidebar -> onClearAll()        -> clear localStorage + docs + chat
ChatPane -> onSend(text)       -> sendMessage(text, modelProvider)
```

When the backend lands, the services layer is swapped (`llm.js` -> `api.js` wrapper) and nothing in the components changes.

---

## Design System (Liquid Glass)

Apple-style "Liquid Glass" in a **light / white** theme built on a custom 5-color palette. Translucent, ultra-transparent white panels show the pre-blurred backdrop orbs straight through. Design tokens live in `src/index.css` under `:root`.

**Palette:**

| Role       | Value        |
| ---------- | ------------ |
| Text / ink | `#000000`    |
| Secondary  | `#666666`    |
| Muted      | `#979797`    |
| Background | `#eeeeee`    |
| Accent     | `#0088cc`    |

```css
--lg-fill:        linear-gradient(165deg, rgba(255,255,255,0.38), ...); /* very transparent glass */
--lg-ring:        rgba(0, 0, 0, 0.05);   /* hairline ring for definition */
--lg-highlight:   rgba(255, 255, 255, 0.7); /* specular top edge */
--lg-shadow:      0 24px 70px rgba(0, 0, 0, 0.14);
--bg-primary:     #eeeeee;
--text-primary:   #000000;
--accent:         #0088cc;
--accent-gradient: linear-gradient(135deg, #0088cc, #33a8e0 60%, #66c2ee 130%);
```

1. Panels use very low-alpha gradient fills (`rgba(255,255,255,0.05–0.38)`) so the pre-blurred blue orbs and backdrop show through — the "liquid" transparency. `backdrop-filter` is used only where cheap and static (modal, toast, input pill); the scrolling document pane relies on the pre-blurred orbs for frost, keeping scroll compositor-smooth.
2. Depth comes from 3 **static, pre-blurred** `#0088cc`/`#66c2ee` orbs + radial gradients on `.app-container`. Orbs are intentionally not animated — motion behind glass forces per-frame backdrop re-blur and janky scrolling.
3. Specular highlights via `inset 0 1px 0 rgba(255,255,255,0.7)` top edges; buttons use `#0088cc` gradient fills with a lighter inset rim.
4. Concentric radii: panels `--radius-lg` (22px), inner cards `--radius-md` (14px), controls `--radius-sm`/pill.
5. Light theme only for now (dark variant can be re-added via a `.dark` class / tokens swap later).

---

## Services API (Current Frontend)

### `storage.js`
`getApiKey(provider)` / `setApiKey(provider, key)` / `getStoredModel()` / `storeModel(provider)` / `clearAll()`

### `llm.js` (temporary direct bridge)
`callGemini` / `callOpenAI` / `fetchSummaryFromLLM` / `fetchChatResponseFromLLM`

### `documentParser.js`
`parseFile(file)` dispatches to `parseTxtFile` / `parsePdfFile` / `parseDocxFile`, returns `{ name, title, sector, text, wordCount, charCount }`.

### `libraryLoader.js`
`loadDocumentLibraries()` injects pdf.js + Mammoth CDN scripts and sets the pdf.js worker.

---

## Mock Data

`useDocuments.js` ships two offline mock documents (Market Analysis 2024, Q3 Tech Report) so the full UI can be demoed without API keys. Exposed via `loadMock(name)`.

---

## Environment / Notes

- Node 18+ required (Vite 6).
- API keys stay in the browser (localStorage) until backend auth arrives.
- Gemini endpoint uses `v1beta` (newer models 404 on `v1`).
- Mic input requires Web Speech API support (Chrome/Edge).
- pdf.js / Mammoth come from CDN at runtime — internet needed for PDF/DOCX parsing.
