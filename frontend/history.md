# OmniChat - Change History

> Running log of every session's changes. Add a new entry at the top after each session using the template below. Keep entries short and factual — one bullet per change.

## Template

```md
## Session <n> — YYYY-MM-DD

**Focus:** <one line on the goal>

**Changed:**
- <file> — what changed / why

**Added:**
- <file> — what was added

**Removed:**
- <file> — what was removed

**Next up:** <pointer to todo.md>
```

---

## Session 7 — 2026-08-06

**Focus:** Apply the user's custom palette and make the glass much more transparent ("more liquid glass").

**Changed:**
- `src/index.css` — new palette: `--bg-primary: #eeeeee`, `--text-primary: #000000`, `--text-secondary: #666666`, `--text-muted: #979797`, accent `#0088cc` (with `#33a8e0` / `#66c2ee` gradient stops). Glass fills dropped to very low alpha (`rgba(255,255,255,0.05–0.38)` gradients over `rgba(255,255,255,0.14)`), so the pre-blurred blue orbs and backdrop show straight through the panels. Background orbs recolored to `#0088cc` / `#66c2ee` tints; backdrop is now a cool gray `#eeeeee`-family wash.
- `src/components/DocumentPane/DocumentPane.css` — transparent fills on pane/sheet/cards/step-cards (alpha 0.16–0.35), blue accent icons, gradient title black→`#0088cc`. Summary panel kept more opaque for legibility over scrolling content. No `backdrop-filter` on the scrolling pane (Session 5 fix intact).
- `src/components/Sidebar/Sidebar.css` — transparent glass sidebar, `#0088cc` accent treatments, lighter inputs/file items.
- `src/components/ChatPane/ChatPane.css` — transparent chat panes and AI bubbles, user bubbles now `#0088cc→#33a8e0`, blue send/avatar.
- `src/components/SettingsModal/SettingsModal.css` / `Toast.css` — transparent modal glass with real blur (small/static), black toast pill using palette black.
- `todo.md` — added "Custom Palette + Ultra-Transparent Glass — DONE (Session 7)" section + changelog entry.
- `project.md` — Design System section rewritten around the 5-color palette table + ultra-transparent glass notes.
- `history.md` — this entry (Session 7).

**Verified:**
- `npm run build` passes (vite build, ~179 kB JS / ~25 kB CSS).

**Next up:** see `todo.md`.

---

## Session 6 — 2026-08-06

**Focus:** Switch the Liquid Glass theme from dark to a light "white" look matching the Apple website.

**Changed:**
- `src/index.css` — light-mode design tokens: `--bg-primary: #f5f5f7`, Apple text scale (`#1d1d1f` / `#6e6e73` / `#86868b`), Apple blue accent (`#0071e3` / `#2997ff` / `#5ac8fa`), Apple status colors. Glass fills are now white translucent (`rgba(255,255,255,…)`), borders/hairlines use `rgba(0,0,0,…)` rings for definition, shadows are soft blue-greys. Backdrop changed to a light Tahoe-style wash with pastel lavender / sky / peach orbs.
- `src/components/DocumentPane/DocumentPane.css` — light glass for pane, header, sheet, highlight cards, step cards, summary panel, loading overlay; gradient text switched to dark→blue; scroll smoothness fixes from Session 5 kept intact.
- `src/components/Sidebar/Sidebar.css` — light glass sidebar, blue-gradient logo/buttons, light inputs and file list.
- `src/components/ChatPane/ChatPane.css` — white glass chat pane, Apple-blue user bubbles, light frosted AI bubbles, white input pill.
- `src/components/SettingsModal/SettingsModal.css` — white glass modal + pill buttons.
- `src/components/Toast/Toast.css` — dark Apple-style toast pill (light text) with red error variant.

**Verified:**
- `npm run build` passes (vite build, ~179 kB JS / ~25 kB CSS).

**Next up:** see `todo.md`.

---

## Session 5 — 2026-08-06

**Focus:** Restyle the UI as Apple "Liquid Glass" (macOS Tahoe style) and fix jittery/laggy scrolling in the middle document window.

**Changed:**
- `src/index.css` — rebuilt design system around Liquid Glass: new `--lg-*` tokens (gradient fills, hairline borders, specular highlight, deep shadows), `--radius-*` scale, Tahoe-style luminous radial-gradient backdrop, refined indigo/violet/cyan accent palette. Background orbs are now **static pre-blurred** shapes (`filter: blur(72px)`, no `orb-float` animation) so the "frosted" look is baked in instead of re-blurring every frame.
- `src/components/DocumentPane/DocumentPane.css` — **jank fix**: removed `backdrop-filter` from the scrolling middle pane (`.document-pane`) and `.document-sheet`; the frosted effect now comes from layered translucent fills over pre-blurred orbs, so scroll is compositor-smooth. Liquid glass styling for header, zoom buttons, share pill, highlight cards, step cards, summary panel, loading overlay. Reduced `doc-viewer-body` bottom padding (200px → 140px).
- `src/components/Sidebar/Sidebar.css` — Liquid Glass fills/highlights for sidebar, logo, model select, key input, upload box, file items, nav, profile card. Removed backdrop-filter from the sidebar surface.
- `src/components/ChatPane/ChatPane.css` — Liquid Glass chat pane and bubbles (gradient user bubble with specular inset highlight, frosted AI bubble), glass input pill with real blur (static, non-scrolling), refined send/mic buttons. Removed backdrop-filter from the scrolling messages area.
- `src/components/SettingsModal/SettingsModal.css` — Liquid Glass modal (kept backdrop blur — small, static), pill buttons, input focus rings.
- `src/components/Toast/Toast.css` — Liquid Glass pill toast, gradient error variant.
- `src/components/DocumentPane/WelcomeScreen.jsx` — dropped `glass-card` class on step cards (now self-styled via `.step-card`).

**Verified:**
- `npm run build` passes (vite build, ~179 kB JS / ~25 kB CSS).

**Next up:** see `todo.md`.

---

## Session 4 — 2026-08-06

**Focus:** Clean up the repo — remove obsolete vanilla files and leftover artifacts.

**Removed:**
- `omnichat.html`, `omnichat.js`, `omnichat.css` — original vanilla single-file version, fully superseded by the React app.
- `set_uo.txt` — leftover notes on a backend `requirements.txt`, unrelated to the frontend.
- `public/` — empty folder (no static assets).
- `dist/` — generated build output (regenerated by `npm run build`).

**Changed:**
- `history.md` — removed "safe to delete" note for the deleted files.

**Next up:** see `todo.md`.

---

## Session 3 — 2026-08-06

**Focus:** Set up a persistent change log.

**Added:**
- `history.md` — this file, with a template for future sessions.

**Next up:** see `todo.md` (UI polish backlog + backend integration blocked on friend's API).

---

## Session 2 — 2026-08-06

**Focus:** Re-scope docs to frontend-only; backend (FastAPI + multimodal RAG) is owned by a teammate (root `README.md`).

**Changed:**
- `project.md` — rewritten as "OmniChat Frontend" docs: frontend-only scope note, backend tech stack referenced from `README.md`, new "Backend Integration Plan" table (each endpoint -> frontend slot, marked "Waiting backend"), `llm.js` marked as a temporary direct-LLM bridge that will be swapped for the backend API without component changes.
- `todo.md` — restructured: "Current Focus: UI & Frontend" section, "Backend Integration (BLOCKED)" group using `[-]` convention, design-decision items flagged `[!]` (audio/video upload UI, TTS player, history/topics panels, auth screens).

**Added:**
- `history.md` (now), documenting sessions 2 and 3.

**Next up:** UI polish backlog — see `todo.md`.

---

## Session 1 — 2026-08-06

**Focus:** Migrate the vanilla `omnichat.html/js/css` app to React and redesign the UI with a glassmorphism theme.

**Changed:**
- `src/services/storage.js` — added `getStoredModel()` / `storeModel()` for persisting the active AI provider.
- `src/hooks/useChat.js` — removed `feedRef` (ChatPane now owns its scroll ref); dropped unused `showToast` param.
- `src/components/Sidebar/Sidebar.jsx` — model dropdown + API key labels now sourced from `constants/models.js`.
- `src/components/Sidebar/Sidebar.css` — glass treatment on model select, upload box, and file items (backdrop blur).
- `src/index.css` — rebuilt as the glassmorphism design system: design tokens (`--glass-*`, `--accent-gradient`), animated background orbs, radial gradient backdrop, glass primitives, gradient text helper, scrollbars.
- `package.json` — unchanged deps; `npm install` run (Vite 6.4.3 installed).

**Added:**
- `src/App.jsx` — root layout wiring global state (model, documents, chat, toast, settings modal) and loading document-parsing libraries on mount.
- `src/constants/models.js` — model options + API key label maps.
- `src/utils/formatting.js` — `formatTime` / `formatNumber`.
- `src/services/libraryLoader.js` — runtime CDN loader for pdf.js + Mammoth (replaces the static CDN script tags).
- `src/hooks/useModel.js` — active provider state with localStorage persistence.
- `src/hooks/useVoiceInput.js` — Web Speech API wrapper (mic -> text).
- `src/hooks/useDocumentZoom.js` — document sheet zoom (0.85–1.3).
- `src/components/ChatPane/` — `ChatPane.jsx`, `ChatBubble.jsx`, `ChatInput.jsx`, `TypingIndicator.jsx` + CSS (glass chat feed, gradient user bubbles, mic/send pill input).
- `src/components/DocumentPane/` — `DocumentPane.jsx`, `DocumentHeader.jsx`, `DocumentSheet.jsx`, `DocumentStats.jsx`, `SummaryPanel.jsx`, `WelcomeScreen.jsx`, `LoadingOverlay.jsx` + CSS (glass sheet, stat cards, collapsible summary, loading overlay).
- `project.md` — file structure, feature map, design tokens, data flow, service APIs.
- `todo.md` — task tracker with done items + backlog.

**Verified:**
- `npm run build` passes (vite build, ~179 kB JS / ~22 kB CSS).

**Remaining from original app (deferred):**
- "Intelligence History" nav tab, per-message system notices, `window.confirm` reset — tracked in `todo.md`.
