"""Outbound messaging for customer service workflows."""

from __future__ import annotations

import os
from typing import Any


def send(channel: str, text: str) -> dict[str, Any]:
    channel = (channel or "email").lower()
    text = (text or "").strip()
    if not text:
        return {"ok": False, "error": "empty message"}

    dry = os.getenv("MESSAGING_DRY_RUN", "true").lower() == "true"

    if dry:
        return {
            "ok": True,
            "dry_run": True,
            "channel": channel,
            "text": text,
            "note": "MESSAGING_DRY_RUN=true — message staged, not sent",
        }

    if channel == "email":
        # Wire SMTP / SendGrid / etc. when SMTP_* env set
        if not os.getenv("SMTP_HOST"):
            return {"ok": False, "error": "SMTP_HOST not configured"}
        return {"ok": False, "error": "Live email send not yet wired"}

    if channel in ("whatsapp", "sms"):
        return {"ok": False, "error": f"Live {channel} send not yet wired"}

    return {"ok": False, "error": f"Unknown channel {channel}"}
