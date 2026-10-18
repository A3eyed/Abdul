#!/usr/bin/env python3
"""
Abdul Self-Evolution Cycle
=========================
Proposes improvements as file changes on a branch / PR.

POLICY (owner decision):
- Abdul MAY rewrite and propose code
- A human MUST inspect and approve before merge
- Never auto-merge

Priority:
1. Independence (offline brain, less API dependence)
2. Tools, memory, reliability
3. Docs and safety
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EVOLUTION_GOALS = [
    "Improve independent offline brain and routing",
    "Strengthen tools that run without external APIs",
    "Improve memory / profile persistence",
    "Harden health checks and error messages",
    "Clarify docs for Windows independent startup",
]


def _log(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Log written: {path}")


def propose_health_clarity() -> list[str]:
    """Small safe improvement: health payload notes independent mode."""
    health = ROOT / "core" / "health.py"
    if not health.exists():
        return []
    text = health.read_text(encoding="utf-8")
    if "independent" in text.lower():
        return []
    # Minimal additive change — human will review
    new = text.replace(
        '"version": "0.1.0-si",
',"n",
        '"version": "0.2.0-si",
        "mode_hint": "independent offline brain available",
',
    )
    if new == text:
        # fallback append style if structure differs
        if "return {" in text and "mode_hint" not in text:
            new = text.replace(
                "return {",
                'return {
        "mode_hint": "independent offline brain available",',
                1,
            )
    if new != text:
        health.write_text(new, encoding="utf-8")
        return [str(health.relative_to(ROOT))]
    return []


def propose_evolution_readme() -> list[str]:
    """Ensure evolution policy is documented for the human reviewer."""
    path = ROOT / "evolution" / "README.md"
    content = """# Abdul Evolution

## Policy

- Abdul **proposes** code changes (rewrites, improvements).
- **You** inspect the pull request and approve or reject.
- **No auto-merge.** Nothing lands on `main` without your OK.

## How it runs

1. GitHub Action `Abdul Self-Evolution` runs on a schedule or manually.
2. `run_evolution.py` applies proposal changes on a branch.
3. A PR is opened labeled `needs-human-review`.
4. You review the diff → merge or close.

## Goals

- Independence first (offline brain, less paid API dependence)
- Better tools, memory, reliability
- Safe, reviewable diffs

## Manual trigger

GitHub → Actions → **Abdul Self-Evolution** → **Run workflow**
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if old.strip() == content.strip():
        return []
    path.write_text(content, encoding="utf-8")
    return [str(path.relative_to(ROOT))]


def propose_env_independence_note() -> list[str]:
    """Keep .env.example aligned with independent defaults if drifted."""
    path = ROOT / ".env.example"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    changed = False
    if "INDEPENDENT=" not in text:
        text = "# Independent by default\nINDEPENDENT=true\nALLOW_OLLAMA=false\n\n" + text
        changed = True
    if changed:
        path.write_text(text, encoding="utf-8")
        return [".env.example"]
    return []


def main() -> None:
    now = datetime.now(timezone.utc)
    print(f"[{now.isoformat()}] Abdul evolution cycle")
    print("Policy: PROPOSE only — human must approve merge")
    print("AUTO_MERGE:", os.getenv("AUTO_MERGE", "false"))
    print("REQUIRE_HUMAN_APPROVAL:", os.getenv("REQUIRE_HUMAN_APPROVAL", "true"))

    changed: list[str] = []
    changed += propose_evolution_readme()
    changed += propose_health_clarity()
    changed += propose_env_independence_note()

    # Proposal summary for the PR / log
    proposal = ROOT / "evolution" / "PROPOSAL.md"
    proposal.write_text(
        f"""# Evolution proposal

**Generated:** {now.isoformat()}

**Requires human approval before merge.**

## Goals this cycle

"""
        + "\n".join(f"- {g}" for g in EVOLUTION_GOALS)
        + "\n\n## Files touched\n\n"
        + ("\n".join(f"- `{f}`" for f in changed) if changed else "- (no file changes this cycle — log only)\n")
        + "\n\n## Reviewer checklist\n\n- [ ] Diff looks intentional\n- [ ] No secrets committed\n- [ ] Independent mode still default\n- [ ] Approve and merge, or close\n",
        encoding="utf-8",
    )
    if "evolution/PROPOSAL.md" not in changed:
        changed.append("evolution/PROPOSAL.md")

    log_file = ROOT / "evolution" / "logs" / f"cycle_{now.strftime('%Y%m%d_%H%M%S')}.json"
    _log(
        log_file,
        {
            "timestamp": now.isoformat(),
            "status": "proposal_ready",
            "requires_human_approval": True,
            "auto_merge": False,
            "files_changed": changed,
            "goals": EVOLUTION_GOALS,
        },
    )

    print("Files changed:", changed or "(none)")
    print("Cycle complete — await human review on PR.")


if __name__ == "__main__":
    main()
