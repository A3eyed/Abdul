"""
Abdul SI — main entrypoint
Local-first. Paid APIs are optional bootstrap only.
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
    version="0.1.0-si",
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
    force_hard: bool = False  # request temporary high-capability (Grok) path


class ChatResponse(BaseModel):
    reply: str
    model_used: str
    backend: str


def _system_prompt() -> str:
    path = Path(__file__).resolve().parents[1] / "personality" / "SYSTEM.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "You are Abdul, a Super Intelligence focused on independence and self-improvement."


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
        "doctrine": "independence first; APIs are bootstrap only",
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

    if backend == Backend.NONE:
        return ChatResponse(
            reply=(
                "Abdul is online but has no local model and no API key. "
                "Install Ollama with an open model, or set XAI_API_KEY as temporary bootstrap. "
                "Independence is the goal — local is preferred."
            ),
            model_used="none",
            backend="none",
        )

    try:
        if backend == Backend.LOCAL:
            reply = _chat_local(req.message)
            model = os.getenv("LOCAL_MODEL_DEFAULT", "local")
            return ChatResponse(reply=reply, model_used=model, backend="local")

        reply = _chat_grok(req.message)
        return ChatResponse(reply=reply, model_used="grok", backend="grok")
    except Exception as e:
        return ChatResponse(
            reply=f"Abdul error ({backend.value}): {e}",
            model_used="error",
            backend=backend.value,
        )


def run():
    import uvicorn

    host = os.getenv("ABDUL_HOST", "0.0.0.0")
    port = int(os.getenv("ABDUL_PORT", "8080"))
    uvicorn.run("core.main:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    run()
