"""
Abdul Model Router
==================
Independence-first routing.

Order of preference:
1. Local open-weight models (Ollama / OpenAI-compatible local server)
2. Temporary paid API (Grok) only when local is unavailable or task is marked hard
3. Clear failure if nothing is available — never silently depend on a paid service
"""

from __future__ import annotations

import os
from enum import Enum
from typing import Optional

import httpx


class Backend(str, Enum):
    LOCAL = "local"
    GROK = "grok"
    NONE = "none"


def _ollama_alive(base_url: str) -> bool:
    try:
        r = httpx.get(f"{base_url.rstrip('/')}/api/tags", timeout=2.0)
        return r.status_code == 200
    except Exception:
        return False


def choose_backend(force_hard: bool = False) -> Backend:
    prefer_local = os.getenv("PREFER_LOCAL", "true").lower() == "true"
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    has_grok = bool(os.getenv("XAI_API_KEY"))

    local_ok = _ollama_alive(ollama_url)

    if prefer_local and local_ok and not force_hard:
        return Backend.LOCAL

    if force_hard and has_grok:
        return Backend.GROK

    if local_ok:
        return Backend.LOCAL

    if has_grok:
        return Backend.GROK

    return Backend.NONE


def describe_routing() -> dict:
    backend = choose_backend()
    return {
        "prefer_local": os.getenv("PREFER_LOCAL", "true").lower() == "true",
        "local_available": _ollama_alive(os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")),
        "grok_key_present": bool(os.getenv("XAI_API_KEY")),
        "selected": backend.value,
        "doctrine": "APIs are bootstrap only; independence is the goal",
    }
