"""
web/routes.py
FastAPI routes — wraps the Orchestrator for the dashboard.
Uses SSE (Server-Sent Events) for live pipeline updates.
"""
import asyncio
import json
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel

from config       import Config
from orchestrator import Orchestrator, _load_state, _save_state

router = APIRouter(prefix="/api")

cfg  = Config()
orch = Orchestrator(cfg)

# Live event queue for SSE
_event_queue: asyncio.Queue = asyncio.Queue()


def _emit(agent: str, message: str) -> None:
    """Push pipeline events to SSE queue."""
    event = json.dumps({"agent": agent, "message": message})
    try:
        _event_queue.put_nowait(event)
    except asyncio.QueueFull:
        pass


# ── Request models ────────────────────────────────────────────────────────────

class ReviewRequest(BaseModel):
    base:         str = "main"
    commit_range: str = ""

class DraftRequest(BaseModel):
    kind:        str
    instruction: str = ""
    base:        str = "main"

class ApproveRequest(BaseModel):
    approved: bool

class ImproveRequest(BaseModel):
    kind:   str
    number: int

class ConfigUpdate(BaseModel):
    dry_run:       Optional[bool] = None
    repo_path:     Optional[str]  = None
    github_token:  Optional[str]  = None
    github_owner:  Optional[str]  = None
    github_repo:   Optional[str]  = None
    ollama_model:  Optional[str]  = None


# ── SSE stream ────────────────────────────────────────────────────────────────

@router.get("/stream")
async def stream():
    async def event_generator():
        while True:
            try:
                event = await asyncio.wait_for(_event_queue.get(), timeout=30)
                yield f"data: {event}\n\n"
            except asyncio.TimeoutError:
                yield "data: {\"agent\":\"heartbeat\",\"message\":\"ping\"}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# ── Status ────────────────────────────────────────────────────────────────────

@router.get("/status")
def status():
    import requests as req
    try:
        r = req.get(f"{cfg.OLLAMA_BASE_URL}/api/tags", timeout=3)
        ollama = "running" if r.ok else "error"
    except Exception:
        ollama = "offline"

    github = "configured" if cfg.GITHUB_TOKEN else "not_configured"

    pending = _load_state(cfg)

    return {
        "ollama":      ollama,
        "github":      github,
        "dry_run":     cfg.DRY_RUN,
        "model":       cfg.OLLAMA_MODEL,
        "repo_path":   cfg.REPO_PATH,
        "has_pending": pending is not None,
        "pending_task": pending.task if pending else None,
    }


# ── Review ────────────────────────────────────────────────────────────────────

@router.post("/review")
async def review(req: ReviewRequest):
    loop = asyncio.get_event_loop()
    try:
        report = await loop.run_in_executor(
            None, lambda: orch.review(
                base=req.base,
                commit_range=req.commit_range,
                emit=_emit,
            )
        )
        return JSONResponse(report.to_dict())
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# ── Draft ─────────────────────────────────────────────────────────────────────

@router.post("/draft")
async def draft(req: DraftRequest):
    loop = asyncio.get_event_loop()
    try:
        report = await loop.run_in_executor(
            None, lambda: orch.draft(
                kind=req.kind,
                instruction=req.instruction,
                base=req.base,
                emit=_emit,
            )
        )
        return JSONResponse(report.to_dict())
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# ── Approve ───────────────────────────────────────────────────────────────────

@router.post("/approve")
async def approve(req: ApproveRequest):
    loop = asyncio.get_event_loop()
    try:
        report = await loop.run_in_executor(
            None, lambda: orch.approve(approved=req.approved, emit=_emit)
        )
        return JSONResponse(report.to_dict())
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# ── Improve ───────────────────────────────────────────────────────────────────

@router.post("/improve")
async def improve(req: ImproveRequest):
    loop = asyncio.get_event_loop()
    try:
        report = await loop.run_in_executor(
            None, lambda: orch.improve(
                kind=req.kind,
                number=req.number,
                emit=_emit,
            )
        )
        return JSONResponse(report.to_dict())
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# ── State ─────────────────────────────────────────────────────────────────────

@router.get("/state")
def get_state():
    report = _load_state(cfg)
    if not report:
        return JSONResponse({"task": None})
    return JSONResponse(report.to_dict())


# ── Config ────────────────────────────────────────────────────────────────────

@router.get("/config")
def get_config():
    return {
        "dry_run":      cfg.DRY_RUN,
        "repo_path":    cfg.REPO_PATH,
        "ollama_model": cfg.OLLAMA_MODEL,
        "github_owner": cfg.GITHUB_OWNER,
        "github_repo":  cfg.GITHUB_REPO,
        "has_token":    bool(cfg.GITHUB_TOKEN),
    }


@router.patch("/config")
def update_config(update: ConfigUpdate):
    if update.dry_run      is not None: cfg.DRY_RUN       = update.dry_run
    if update.repo_path:               cfg.REPO_PATH      = update.repo_path
    if update.github_token:            cfg.GITHUB_TOKEN   = update.github_token
    if update.github_owner:            cfg.GITHUB_OWNER   = update.github_owner
    if update.github_repo:             cfg.GITHUB_REPO    = update.github_repo
    if update.ollama_model:            cfg.OLLAMA_MODEL   = update.ollama_model
    # Recreate orchestrator with new config
    global orch
    orch = Orchestrator(cfg)
    return {"ok": True}
