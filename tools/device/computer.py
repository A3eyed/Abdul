"""
Abdul Computer Control Tools
===========================
Allows Abdul to act on the host computer when explicitly instructed.

Safety: These tools should only be exposed when ENABLE_COMPUTER_USE=true
and the user has granted permission. High-risk actions should still be logged.
"""

from __future__ import annotations

import os
import subprocess
import shlex
from pathlib import Path
from typing import Optional


class ComputerTools:
    """Basic computer interaction layer for Abdul."""

    def __init__(self, allowed_roots: Optional[list[str]] = None):
        self.allowed_roots = [Path(p).resolve() for p in (allowed_roots or [".", str(Path.home())])]

    def _is_safe_path(self, path: str | Path) -> bool:
        try:
            resolved = Path(path).resolve()
            return any(str(resolved).startswith(str(root)) for root in self.allowed_roots)
        except Exception:
            return False

    def run_shell(self, command: str, timeout: int = 60) -> dict:
        """Execute a shell command and return stdout/stderr/returncode."""
        if not os.getenv("ENABLE_SHELL", "true").lower() == "true":
            return {"error": "Shell execution is disabled"}

        try:
            result = subprocess.run(
                shlex.split(command),
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {"error": f"Command timed out after {timeout}s"}
        except Exception as e:
            return {"error": str(e)}

    def read_file(self, path: str) -> dict:
        if not self._is_safe_path(path):
            return {"error": "Path not allowed"}
        try:
            content = Path(path).read_text(encoding="utf-8", errors="replace")
            return {"content": content}
        except Exception as e:
            return {"error": str(e)}

    def write_file(self, path: str, content: str) -> dict:
        if not self._is_safe_path(path):
            return {"error": "Path not allowed"}
        try:
            Path(path).write_text(content, encoding="utf-8")
            return {"status": "ok", "path": path}
        except Exception as e:
            return {"error": str(e)}

    def list_dir(self, path: str = ".") -> dict:
        if not self._is_safe_path(path):
            return {"error": "Path not allowed"}
        try:
            entries = [p.name for p in Path(path).iterdir()]
            return {"entries": entries}
        except Exception as e:
            return {"error": str(e)}


# Future: browser automation via Playwright will be added here.
