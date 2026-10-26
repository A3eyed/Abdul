"""
Social publishing connector.

Real publish requires platform credentials in env:
  META_PAGE_ACCESS_TOKEN + META_PAGE_ID  (Facebook/Instagram via Graph API)
  X_API_KEY / X_API_SECRET / X_ACCESS_TOKEN / X_ACCESS_SECRET
  LINKEDIN_ACCESS_TOKEN

Without credentials: dry-run success with staged payload (safe default).
"""

from __future__ import annotations

import os
from typing import Any


def publish(platform: str, text: str) -> dict[str, Any]:
    platform = (platform or "unknown").lower().strip()
    text = (text or "").strip()
    if not text:
        return {"ok": False, "error": "empty post text"}

    dry = os.getenv("SOCIAL_DRY_RUN", "true").lower() == "true"

    if platform in ("facebook", "instagram", "meta"):
        token = os.getenv("META_PAGE_ACCESS_TOKEN", "")
        page_id = os.getenv("META_PAGE_ID", "")
        if dry or not token or not page_id:
            return {
                "ok": True,
                "dry_run": True,
                "platform": platform,
                "text": text,
                "note": "Set META_PAGE_ACCESS_TOKEN, META_PAGE_ID and SOCIAL_DRY_RUN=false to publish",
            }
        # Graph API publish would go here with httpx
        return {"ok": False, "error": "Live Meta publish not yet wired — dry_run path works"}

    if platform in ("x", "twitter"):
        if dry or not os.getenv("X_ACCESS_TOKEN"):
            return {
                "ok": True,
                "dry_run": True,
                "platform": "x",
                "text": text,
                "note": "Set X_* tokens and SOCIAL_DRY_RUN=false to publish",
            }
        return {"ok": False, "error": "Live X publish not yet wired — dry_run path works"}

    if platform == "linkedin":
        if dry or not os.getenv("LINKEDIN_ACCESS_TOKEN"):
            return {
                "ok": True,
                "dry_run": True,
                "platform": "linkedin",
                "text": text,
                "note": "Set LINKEDIN_ACCESS_TOKEN and SOCIAL_DRY_RUN=false to publish",
            }
        return {"ok": False, "error": "Live LinkedIn publish not yet wired — dry_run path works"}

    return {
        "ok": True,
        "dry_run": True,
        "platform": platform,
        "text": text,
        "note": f"No connector for {platform}; staged as dry-run",
    }
