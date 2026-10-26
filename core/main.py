"""
Abdul SI — main entrypoint
Mobile-ready personal SI + workflow automation backend.
Independence first: chat works offline; automations use dry-run until API keys set.
"""

from __future__ import annotations

import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.health import get_health_status
from core.router import Backend, choose_backend, describe_routing
from core.workflows.api import router as workflows_router

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

app = FastAPI(
    title="Abdul SI",
    description="Personal Super Intelligence + automation platform",
    version="0.3.0-si",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workflows_router)


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = "default"
    force_hard: bool = False


class ChatResponse(BaseModel):
    reply: str
    model_used: str
    backend: str


def _safe_routing() -> dict:
    try:
        return describe_routing()
    except Exception as e:
        return {
            "selected": "offline",
            "error": str(e),
            "doctrine": "independence first",
        }


def _system_prompt() -> str:
    path = Path(__file__).resolve().parents[1] / "personality" / "SYSTEM.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "You are Abdul, a Super Intelligence and automation assistant."


def _chat_offline(message: str) -> str:
    m = message.lower().strip()

    if any(k in m for k in ("introduce", "who are you", "what are you")):
        return (
            "I am Abdul — your personal Super Intelligence assistant. "
            "I chat, plan, and run workflows for customer service, marketing, and social publishing. "
            "Use the mobile app or API: /workflows/customer-service, /workflows/social, /workflows/marketing-calendar. "
            "Publishing stays in dry-run until you add platform API keys and turn dry-run off."
        )

    if any(k in m for k in ("workflow", "automat", "social", "marketing", "customer")):
        return (
            "Automation is live on this core:\n"
            "• POST /workflows/customer-service — draft CS replies (approve then send)\n"
            "• POST /workflows/social — draft + optional publish (X/Meta/LinkedIn)\n"
            "• POST /workflows/marketing-calendar — multi-day content plan\n"
            "• POST /workflows/{id}/approve — approve from your phone\n"
            "• GET /workflows — list jobs\n"
            "Default is safe dry-run for outbound actions."
        )

    if any(k in m for k in ("independent", "offline", "api", "cost", "free", "ollama")):
        return (
            "Chat works independently with the offline brain. "
            "Real social/email send needs platform tokens — that is unavoidable for true publishing. "
            "Until then, workflows stage content for your approval."
        )

    if any(k in m for k in ("help", "can you do", "what can")):
        return (
            "I can: converse as your SI, draft CS replies, build marketing calendars, "
            "stage social posts, run webhook automations, and queue jobs you approve from mobile. "
            "See /docs for full API."
        )

    return (
        f"Online (independent mode). You said: {message[:280]}. "
        f"Ask about workflows, social, marketing, or customer service — or open /docs."
    )


def _chat_local(message: str) -> str:
    base = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
    model = os.getenv("LOCAL_MODEL_DEFAULT", "qwen2.5:14b")
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": _system_prompt()},
            {"role": "user", "content": message},
        ],
        "stream": False,
    }
    r = httpx.post(f"{base}/api/chat", json=payload, timeout=120.0)
    r.raise_for_status()
    data = r.json()
    return data.get("message", {}).get("content") or data.get("response") or ""


def _chat_grok(message: str) -> str:
    from openai import OpenAI

    client = OpenAI(
        api_key=os.getenv("XAI_API_KEY"),
        base_url=os.getenv("XAI_BASE_URL", "https://api.x.ai/v1"),
    )
    completion = client.chat.completions.create(
        model=os.getenv("XAI_MODEL", "grok-3"),
        messages=[
            {"role": "system", "content": _system_prompt()},
            {"role": "user", "content": message},
        ],
        temperature=0.7,
    )
    return completion.choices[0].message.content or ""


@app.get("/")
def root():
    return {
        "name": "Abdul",
        "type": "Super Intelligence (SI)",
        "status": "online",
        "product": "mobile personal SI + automation",
        "workflows": "/workflows",
        "docs": "/docs",
        "health": "/health",
        "routing": _safe_routing(),
    }


@app.get("/health")
def health():
    try:
        status = get_health_status()
    except Exception:
        status = {"status": "ok", "service": "Abdul SI"}
    status["routing"] = _safe_routing()
    status["status"] = status.get("status") or "ok"
    status["workflows"] = True
    return status


@app.get("/routing")
def routing():
    return _safe_routing()


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    backend = choose_backend(force_hard=req.force_hard)
    try:
        if backend == Backend.LOCAL:
            reply = _chat_local(req.message)
            return ChatResponse(
                reply=reply,
                model_used=os.getenv("LOCAL_MODEL_DEFAULT", "local"),
                backend="local",
            )
        if backend == Backend.GROK:
            reply = _chat_grok(req.message)
            return ChatResponse(reply=reply, model_used="grok", backend="grok")
        reply = _chat_offline(req.message)
        return ChatResponse(reply=reply, model_used="offline-si", backend="offline")
    except Exception as e:
        reply = _chat_offline(req.message)
        return ChatResponse(
            reply=f"{reply}\n\n(Note: primary backend error was: {e})",
            model_used="offline-si",
            backend="offline",
        )


def run():
    import uvicorn

    host = os.getenv("ABDUL_HOST", "0.0.0.0")
    port = int(os.getenv("ABDUL_PORT", "8080"))
    uvicorn.run("core.main:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    run()
