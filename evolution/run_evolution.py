#!/usr/bin/env python3
"""
Abdul Self-Evolution Cycle
=========================
Runs via GitHub Actions. Goal: increase independence and local capability.

Priority order for improvements:
1. Better local tools, memory, routing, and agent scaffolding
2. Reductions in paid API dependence
3. Local model adapters / fine-tune recipes
4. Only then: prompt tweaks that assume external APIs

APIs may assist the evolution process while bootstrap is needed, but every
cycle should bias toward work that makes future API use less necessary.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


EVOLUTION_GOALS = [
    "Improve local-first routing and fallbacks",
    "Strengthen tools that run without external APIs",
    "Improve memory so less re-querying of large models is needed",
    "Generate or refine synthetic data / fine-tune recipes for open models",
    "Reduce surface area that requires paid endpoints",
    "Improve computer and messaging channels reliability",
]


def main() -> None:
    now = datetime.now(timezone.utc)
    print(f"[{now.isoformat()}] Abdul evolution cycle started")
    print("Doctrine: independence first; APIs are bootstrap only")
    print("Auto-merge enabled:", os.getenv("AUTO_MERGE_EVOLUTIONS", "true"))

    log_dir = Path("evolution/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"cycle_{now.strftime('%Y%m%d_%H%M%S')}.json"

    log_data = {
        "timestamp": now.isoformat(),
        "status": "independence_focused_scaffold",
        "goals": EVOLUTION_GOALS,
        "message": (
            "Evolution cycle prioritizes local capability and reduced API dependence. "
            "Full automated code mutation + test loop comes next."
        ),
        "prefer_local": os.getenv("PREFER_LOCAL", "true"),
        "has_xai_key": bool(os.getenv("XAI_API_KEY")),
    }

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2)

    print(f"Evolution log written to {log_file}")
    print("Cycle complete.")


if __name__ == "__main__":
    main()
