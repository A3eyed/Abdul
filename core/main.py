"""
Abdul SI — main entrypoint
Independence first. Works with ZERO external models by default.
Paid APIs and Ollama are optional — not required to start or chat.
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

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

app = FastAPI(
    title="Abdul SI",
    description="Self-evolving Super Intelligence — independence first",
    version="0.2.0-si",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = "default"
    force_hard: bool = False


class ChatResponse(BaseModel):
    reply: str
    model_used: str
    backend: str


def _system_prompt() -> str:
    path = Path(__file__).resolve().parents[1] / "personality" / "SYSTEM.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "You are Abdul, a Super Intelligence focused on independence and self-improvement."


def _chat_offline(message: str) -> str:
    """Built-in SI brain — no network, no Ollama, no paid API."""
    m = message.lower().strip()

    if any(k in m for k in ("introduce", "who are you", "what are you")):
        return (
            "I am Abdul — a Super Intelligence built as your personal presence. "
            "I run independently on your machine: no paid API required, no heavy local model that freezes your laptop. "
            "I am the desktop shell, your tools, and a mind that improves over time. "
            "Optional Grok or remote open models can boost reasoning later; they are not required for me to be online."
        )

    if any(k in m for k in ("independent", "offline", "api", "cost", "free", "ollama")):
        return (
            "Independence is the default. Right now I am using the built-in offline brain — zero cost, zero external calls. "
            "Ollama is off on this laptop because it freezes your machine. "
            "A valid key from console.x.ai is optional bootstrap only. "
            "Longer term: brain on a small VPS with open models, while this laptop stays the UI and tool layer."
        )

    if any(k in m for k in ("help", "can you do", "what can", "automat", "desktop", "phone")):
        return (
            "I can chat, help you plan, remember preferences you teach me, and grow tool access "
            "(files, shell, browser, schedules) as those modules come online. "
            "Phone access is planned via WhatsApp; native apps later. "
            "Ask me something concrete and I will answer with what I can do offline right now."
        )

    if any(k in m for k in ("study", "learn", "remember", "profile")):
        return (
            "Teach me with corrections and preferences. I store a private profile on your machine "
            "(data/profile) — inspectable and deletable by you. I do not need a cloud model to keep that."
        )

    if any(k in m for k in ("online", "status", "health", "working")):
        return (
            "Core is online in independent mode. UI talks to me on localhost:8080. "
            "No external model is required for this path."
        )

    return (
        f"I am online in independent mode (offline SI brain). "
        f"I understood: {message[:280]}. "
        f"I can discuss, plan, and guide setup without paid APIs. "
        f"For deeper frontier reasoning later, optionally add a console.x.ai key or a remote open-model host — never required to keep me running."
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
        "doctrine": "independence first — offline brain always available",
        "routing": describe_routing(),
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    status = get_health_status()
    status["routing"] = describe_routing()
    return status


@app.get("/routing")
def routing():
    return describe_routing()


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

        # Default: independent offline brain
        reply = _chat_offline(req.message)
        return ChatResponse(reply=reply, model_used="offline-si", backend="offline")
    except Exception as e:
        # Never go fully silent — fall back to offline
        reply = _chat_offline(req.message)
        return ChatResponse(
            reply=f"{reply}\n\n(Note: primary backend error was: {e})",
            model_used="offline-si",
            backend="offline",
        )


def run():
    import uvicorn

    host = os.getenv("ABDUL_HOST", "127.0.0.1")
    port = int(os.getenv("ABDUL_PORT", "8080"))
    uvicorn.run("core.main:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    run()
