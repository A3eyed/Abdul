"""
Abdul WhatsApp Channel
======================
Self-hosted WhatsApp access using the Baileys-style multi-device protocol
(unofficial WhatsApp Web). This is the same approach used by mature personal
AI agents such as OpenClaw.

How it works
------------
1. A Node/TypeScript (or Python bridge) process runs Baileys.
2. You scan a QR code once with the WhatsApp app on a phone (preferably a
   secondary number).
3. Incoming messages are forwarded to Abdul's agent loop.
4. Abdul's replies are sent back as WhatsApp messages.

Important
---------
- This is unofficial. Meta can restrict accounts that appear automated.
- Strongly recommended: use a dedicated secondary number for the bot.
- Keep usage personal and low-volume to stay under the radar.

Status: Scaffolding. Full Baileys integration will be completed in the next
iterations (either pure Python bridge or a small Node sidecar).
"""

from __future__ import annotations

import os
from typing import Callable, Optional


class WhatsAppChannel:
    """WhatsApp messaging channel for Abdul."""

    def __init__(self):
        self.enabled = os.getenv("ENABLE_WHATSAPP", "false").lower() == "true"
        self.allowed_numbers = [
            n.strip()
            for n in os.getenv("WHATSAPP_ALLOWED_NUMBERS", "").split(",")
            if n.strip()
        ]
        # Path where Baileys session / auth state will live
        self.session_dir = os.getenv("WHATSAPP_SESSION_DIR", "./data/whatsapp_session")

    def is_ready(self) -> bool:
        return self.enabled and bool(self.allowed_numbers)

    def send_message(self, to: str, text: str) -> dict:
        """Send a text message to a WhatsApp number (E.164 format)."""
        if not self.is_ready():
            return {"error": "WhatsApp channel not enabled or no allowed numbers configured"}
        if self.allowed_numbers and to not in self.allowed_numbers and "*" not in self.allowed_numbers:
            return {"error": "Recipient not in allow-list"}

        # Placeholder for actual Baileys send call
        return {
            "status": "queued",
            "to": to,
            "text": text,
            "note": "Full Baileys send will be wired in the Node/Python bridge",
        }

    def on_message(self, handler: Callable):
        """Register handler for incoming WhatsApp messages."""
        # In the full implementation this starts the Baileys event loop
        # and routes messages from allowed numbers into Abdul's agent.
        pass


def get_whatsapp_channel() -> WhatsAppChannel:
    return WhatsAppChannel()
