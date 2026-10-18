"""
Abdul Model Router
==================
Independence-first routing.

Order of preference:
1. Local open-weight models (Ollama) — only if running and not freezing the machine
2. Temporary paid API (Grok) — optional bootstrap only
3. Built-in offline SI brain — always works, zero cost, no external dependency
"""

from __future__ import annotations

import os
from enum import Enum

import httpx


class Backend(str, Enum):
    LOCAL = "local"
    GROK = "grok"
    OFFLINE = "offline"


def _ollama_alive(base_url: str) -> bool:
    try:
        r = httpx.get(f"{base_url.rstrip('/')}/api/tags", timeout=2.0)
        return r.status_code == 200
    except Exception:
        return False


def choose_backend(force_hard: bool = False) -> Backend:
    # INDEPENDENT=true forces offline (no paid API, no Ollama)
    if os.getenv("INDEPENDENT", "true").lower() == "true" and not force_hard:
        # Still prefer Ollama only if user explicitly disabled independent-only
        # and Ollama is up — but default independent means offline brain on laptop
        allow_ollama = os.getenv("ALLOW_OLLAMA", "false").lower() == "true"
        ollama_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
        if allow_ollama and _ollama_alive(ollama_url):
            return Backend.LOCAL
        return Backend.OFFLINE

    prefer_local = os.getenv("PREFER_LOCAL", "false").lower() == "true"
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    has_grok = bool(os.getenv("XAI_API_KEY"))
    local_ok = _ollama_alive(ollama_url)

    if prefer_local and local_ok and not force_hard:
        return Backend.LOCAL
    if force_hard and has_grok:
        return Backend.GROK
    if local_ok and os.getenv("ALLOW_OLLAMA", "false").lower() == "true":
        return Backend.LOCAL
    if has_grok:
        return Backend.GROK
    return Backend.OFFLINE


def describe_routing() -> dict:
    backend = choose_backend()
    return {
        "independent": os.getenv("INDEPENDENT", "true").lower() == "true",
        "prefer_local": os.getenv("PREFER_LOCAL", "false").lower() == "true",
        "local_available": _ollama_alive(os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")),
        "grok_key_present": bool(os.getenv("XAI_API_KEY")),
        "selected": backend.value,
        "doctrine": "Independence first — offline brain always available; APIs optional",
    }
