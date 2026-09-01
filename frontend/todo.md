# OmniChat Frontend - TODO / Task Tracker

> **Frontend focus only.** Backend (FastAPI + multimodal RAG) is being built separately by a teammate; the backend-facing tasks below are marked **BLOCKED** until their API is live.
> Convention: `[x]` done · `[ ]` pending · `[-]` blocked · `[!]` needs design decision

---

## Migration (vanilla -> React) — DONE

- [x] Convert vanilla `omnichat.html/js/css` to React component tree
- [x] Split every feature into its own file (see `project.md` -> File Structure)
- [x] `App.jsx` wires global state: model, documents, chat, toast, settings modal
- [x] Runtime CDN loader for pdf.js + Mammoth (`services/libraryLoader.js`)
- [x] Production build passes (`npm run build`)

## Glassmorphism UI — DONE (base)

- [x] Global design tokens in `index.css` (`--glass-*`, accent gradient)
- [x] Animated background orbs + radial gradient backdrop
- [x] Glass panels: Sidebar, DocumentPane, ChatPane, SettingsModal, Toast
- [x] Glass inputs, upload box, file items, stat cards, summary panel
- [x] Gradient text for titles / stat values / logo

## Liquid Glass UI — DONE (Session 5)

- [x] Apple Liquid Glass redesign (macOS Tahoe style): `--lg-*` tokens, specular highlights, concentric radii, luminous backdrop
- [x] Background orbs made static + pre-blurred (removes per-frame backdrop re-blur)
- [x] Fixed jittery/laggy scroll in the middle document window (dropped `backdrop-filter` on the scrolling pane + sheet)
- [x] Refreshed Sidebar, ChatPane, SettingsModal, Toast with Liquid Glass styling

## Light Theme — DONE (Session 6)

- [x] Converted the whole theme to light/white (Apple website style): `#f5f5f7` background, `#1d1d1f` text, Apple blue `#0071e3` accent
- [x] White glass fills, light hairline rings, soft blue-grey shadows, pastel background orbs
- [x] Updated gradient text (dark→blue) for titles/stat values/logo

## Custom Palette + Ultra-Transparent Glass — DONE (Session 7)

- [x] Applied user palette: `#000000` / `#666666` / `#979797` / `#eeeeee` / `#0088cc`
- [x] Glass fills made much more transparent (alpha 0.05–0.38) so the pre-blurred orbs show through — more "liquid glass"
- [x] Recolored orbs/backdrop to `#0088cc` / `#66c2ee` tints, accent gradients re-derived from `#0088cc`

---

## Current Focus: UI & Frontend (can do now)

### Polish / UX
- [ ] Add a "Try demo documents" button in the Sidebar that calls `loadMock(name)`
- [ ] Restore "Active document: <name>" system message in chat when a doc is selected
- [ ] Replace `window.confirm` reset flow with an in-app glass confirmation modal
- [ ] Responsive layout: collapse Sidebar to an icon rail < 1024px
- [ ] Keyboard shortcut: `/` focuses chat input, `Ctrl/Cmd + Enter` sends
- [ ] Skeleton loading states for document sheet and summary while parsing
- [ ] Empty-state design for deleted/last document

### Chat UX
- [ ] Markdown rendering in AI bubbles (headers, lists, code) instead of plain text
- [ ] Copy-to-clipboard button on AI messages
- [ ] Regenerate / edit message actions
- [ ] Streaming-style animated text when backend returns full responses (skeleton for WS)
- [ ] `isTyping` indicator when a document is still loading

### Sidebar
- [ ] Search/filter for uploaded files
- [ ] File size + type badge on each uploaded file
- [ ] Drag & drop file upload onto the document pane

### Misc UI
- [ ] `GET /health`-style "Backend online/offline" status pill in the header
- [ ] Theme polish: light mode toggle (design decision needed)
- [ ] Reduce re-renders with `React.memo` on `ChatBubble`, file list items

---

## Backend Integration (BLOCKED — waiting on friend's FastAPI)

Contract lives in root `README.md`. UI is already designed to slot these in with no component changes (services layer swap).

- [- ] Swap direct `llm.js` calls for `POST /chat` (chat) and `POST /summarize` (summary)
- [- ] `POST /upload/pdf` replaces client-side PDF parsing
- [- ] **Audio upload UI** (`POST /upload/audio`) — design needed [!]
- [- ] **Video upload UI** (`POST /upload/video`) — design needed [!]
- [- ] STT via `POST /stt` as alternative to browser mic
- [- ] TTS playback (`POST /tts`) — audio player UI for AI answers, design needed [!]
- [- ] Session history panel (`GET /history/{session_id}`) — design needed [!]
- [- ] Topics extraction panel (`GET /topics/{session_id}`) — design needed [!]
- [- ] Real-time chat via `WS /ws/{session_id}` (streaming responses)
- [- ] Auth / JWT login screens — design needed [!]
- [- ] `services/api.js` wrapper with error handling + auth headers, then retire `llm.js`

---

## Testing / Quality

- [ ] Add ESLint + Prettier with an npm lint script
- [ ] Unit tests: `documentParser.js`, `storage.js`, `formatting.js`
- [ ] Component tests (Vitest + React Testing Library): Sidebar, ChatPane, DocumentPane
- [ ] E2E smoke test: upload -> summary -> chat flow

## Performance

- [ ] `React.lazy` for `SettingsModal` / `SummaryPanel`
- [ ] Debounce summary generation for very large documents (> 25k chars)
- [ ] Memoize parsed document text / heavy derivations

---

## Changelog

### 2026-08-06
- React migration + glassmorphism redesign completed
- Docs split into frontend-only focus: `project.md` (frontend docs) + `todo.md` (frontend tracker); backend scope documented in root `README.md`
- Added backend integration plan table in `project.md` and BLOCKED task group in `todo.md`
- Liquid Glass redesign (Apple Tahoe style) + fixed jittery scrolling in the middle document window (Session 5)
- Light/white theme conversion (Apple website style) (Session 6)
- Custom palette (#000000/#666666/#979797/#eeeeee/#0088cc) + ultra-transparent liquid glass (Session 7)
