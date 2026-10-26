"""Generic webhook POST for custom automations (Zapier, Make, n8n, CRM)."""

from __future__ import annotations

from typing import Any

import httpx


def post(url: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    if not url:
        return {"ok": False, "error": "missing webhook url"}
    try:
        r = httpx.post(url, json=body or {}, timeout=30.0)
        return {"ok": r.is_success, "status_code": r.status_code, "body": r.text[:1000]}
    except Exception as e:
        return {"ok": False, "error": str(e)}
