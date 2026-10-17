"""
Abdul iMessage Channel
======================
Self-hosted iMessage access.

Reality check
-------------
Apple provides no public iMessage API. All working solutions require a Mac
that is signed into Messages.app.

Recommended paths (2026):
1. BlueBubbles — open-source server that runs on a Mac and exposes a REST API +
   webhooks. Widely used by personal AI projects.
2. imsg-style CLI bridges (used by advanced agent frameworks) that talk directly
   to the local Messages database / private APIs on macOS.

Without a Mac, reliable self-hosted iMessage is currently not practical.

Status: Scaffolding. Full BlueBubbles / imsg integration will be completed next.
"""

from __future__ import annotations

import os
from typing import Callable, Optional


class iMessageChannel:
    """iMessage channel for Abdul (requires a Mac + BlueBubbles or imsg)."""

    def __init__(self):
        self.enabled = os.getenv("ENABLE_IMESSAGE", "false").lower() == "true"
        self.server_url = os.getenv("BLUEBUBBLES_URL", "http://localhost:1234")
        self.password = os.getenv("BLUEBUBBLES_PASSWORD", "")
        self.allowed_handles = [
            h.strip()
            for h in os.getenv("IMESSAGE_ALLOWED_HANDLES", "").split(",")
            if h.strip()
        ]

    def is_ready(self) -> bool:
        return self.enabled and bool(self.server_url)

    def send_message(self, to: str, text: str) -> dict:
        """Send an iMessage to a handle (phone or email)."""
        if not self.is_ready():
            return {"error": "iMessage channel not enabled or BlueBubbles not configured"}

        # Placeholder for actual BlueBubbles / imsg send call
        return {
            "status": "queued",
            "to": to,
            "text": text,
            "note": "Full BlueBubbles REST or imsg send will be wired next",
        }

    def on_message(self, handler: Callable):
        """Register handler for incoming iMessages (via webhook or polling)."""
        pass


def get_imessage_channel() -> iMessageChannel:
    return iMessageChannel()
