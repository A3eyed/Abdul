"""
Abdul SI — main entrypoint
Runs on localhost or any host. Provides health check and a basic chat endpoint.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.health import get_health_status

# Load .env from project root
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

app = FastAPI(
    title="Abdul SI",
    description="Self-evolving Super Intelligence",
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


class ChatResponse(BaseModel):
    reply: str
    model_used: str


@app.get("/")
def root():
    return {
        "name": "Abdul",
        "type": "Super Intelligence (SI)",
        "status": "online",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return get_health_status()


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Minimal chat endpoint. Will be replaced by the full agent loop."""
    api_key = os.getenv("XAI_API_KEY")
    prefer_local = os.getenv("PREFER_LOCAL", "true").lower() == "true"

    if not api_key and prefer_local:
        return ChatResponse(
            reply=(
                "Abdul is online on localhost. "
                "No XAI_API_KEY set and local model routing is not fully wired yet. "
                "Add your Grok key to .env or wait for the local model path."
            ),
            model_used="none",
        )

    # Temporary direct Grok call until the full agent + router is ready
    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=api_key,
            base_url=os.getenv("XAI_BASE_URL", "https://api.x.ai/v1"),
        )
        system = Path(__file__).resolve().parents[1] / "personality" / "SYSTEM.md"
        system_text = system.read_text(encoding="utf-8") if system.exists() else "You are Abdul, a Super Intelligence."

        completion = client.chat.completions.create(
            model=os.getenv("XAI_MODEL", "grok-3"),
            messages=[
                {"role": "system", "content": system_text},
                {"role": "user", "content": req.message},
            ],
            temperature=0.7,
        )
        reply = completion.choices[0].message.content or ""
        return ChatResponse(reply=reply, model_used="grok")
    except Exception as e:
        return ChatResponse(
            reply=f"Abdul encountered an error talking to the model: {e}",
            model_used="error",
        )


def run():
    import uvicorn

    host = os.getenv("ABDUL_HOST", "0.0.0.0")
    port = int(os.getenv("ABDUL_PORT", "8080"))
    uvicorn.run("core.main:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    run()
