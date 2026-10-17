"""
Abdul Mobile Interaction Layer
=============================
Practical way for Abdul to interact with the user's phone.

Full arbitrary control of a modern smartphone is restricted by the OS for security.
The realistic high-value channels are messaging bots (Telegram, Discord, WhatsApp)
that can receive commands, return results, send notifications, and trigger phone-side
automations (Tasker, Shortcuts, etc.).

This module provides the interface for those channels.
"""

from __future__ import annotations

import os
from typing import Optional, Callable


class MobileBridge:
    """Bridge between Abdul and the user's mobile devices via messaging platforms."""

    def __init__(self):
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.allowed_users = [
            uid.strip()
            for uid in os.getenv("TELEGRAM_ALLOWED_USER_IDS", "").split(",")
            if uid.strip()
        ]
        self.discord_token = os.getenv("DISCORD_BOT_TOKEN")

    def is_telegram_ready(self) -> bool:
        return bool(self.telegram_token and self.allowed_users)

    def send_message(self, text: str, channel: str = "telegram") -> dict:
        """Send a message to the user on their phone."""
        if channel == "telegram" and self.is_telegram_ready():
            # Placeholder for actual Telegram Bot API call
            return {
                "status": "queued",
                "channel": "telegram",
                "message": text,
                "note": "Implement with python-telegram-bot or httpx to Telegram API",
            }
        return {"error": f"Channel {channel} not configured or not allowed"}

    def on_command(self, handler: Callable):
        """Register a handler for incoming commands from the phone."""
        # In the full implementation this starts the bot polling / webhook
        # and routes messages from allowed users to Abdul's agent loop.
        pass


def get_mobile_bridge() -> MobileBridge:
    return MobileBridge()
