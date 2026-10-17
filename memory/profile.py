"""
Abdul private user profile ("study me")
======================================
Stores preferences, routines, and work patterns the user allows.
Local / user-owned only. Inspectable and deletable.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class UserProfile:
    display_name: str = ""
    timezone: str = ""
    work_hours_hint: str = ""
    communication_style: str = ""
    preferred_tools: list[str] = field(default_factory=list)
    projects: list[dict[str, Any]] = field(default_factory=list)
    recurring_tasks: list[dict[str, Any]] = field(default_factory=list)
    corrections: list[dict[str, str]] = field(default_factory=list)
    notes: str = ""
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc).isoformat()


class ProfileStore:
    def __init__(self, path: str | Path | None = None):
        root = Path(__file__).resolve().parents[1] / "data" / "profile"
        root.mkdir(parents=True, exist_ok=True)
        self.path = Path(path) if path else root / "user_profile.json"

    def load(self) -> UserProfile:
        if not self.path.exists():
            return UserProfile()
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return UserProfile(**{k: v for k, v in data.items() if k in UserProfile.__dataclass_fields__})

    def save(self, profile: UserProfile) -> None:
        profile.touch()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(asdict(profile), indent=2), encoding="utf-8")

    def record_correction(self, what: str, correction: str) -> UserProfile:
        profile = self.load()
        profile.corrections.append(
            {
                "at": datetime.now(timezone.utc).isoformat(),
                "what": what,
                "correction": correction,
            }
        )
        self.save(profile)
        return profile
