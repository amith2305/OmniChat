"""OmniChat AI - FastAPI entry point. Serves the API and the static frontend."""
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app import config
from app.api import chat, health, media, upload
from app.utils.logging import get_logger

log = get_logger("MAIN")

app = FastAPI(title="OmniChat AI", version="1.0.0", description="Multimodal RAG media intelligence assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup():
    config.ensure_dirs()
    log.info("OmniChat AI starting (Python 3.14, FastAPI)")


app.include_router(health.router)
app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(media.router)

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
DIST_DIR = FRONTEND_DIR / "dist"
STATIC_DIR = DIST_DIR if DIST_DIR.exists() else FRONTEND_DIR


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    from fastapi.responses import Response
    icon = STATIC_DIR / "favicon.ico"
    if icon.exists():
        return FileResponse(icon, media_type="image/x-icon")
    # Check frontend root
    frontend_icon = FRONTEND_DIR / "favicon.ico"
    if frontend_icon.exists():
        return FileResponse(frontend_icon, media_type="image/x-icon")
    # Return empty 204 No Content if no favicon exists
    return Response(status_code=204)


app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
