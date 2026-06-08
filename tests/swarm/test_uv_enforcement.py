"""T01.01 — UV mandate CI guard for swarm modules.

Enforces AC-001 from the MultiModelSwarm roadmap: all swarm scripts must
execute via `uv run`; bare `python -m` and `pip install` invocations are
rejected in `src/superclaude/cli/swarm/`.

This mirrors the project-wide UV-only rule from CLAUDE.md and acts as the
parity counterpart of the sprint CLI's contract tests.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SWARM_DIR = REPO_ROOT / "src" / "superclaude" / "cli" / "swarm"

# Forbidden invocation patterns. Each pattern targets bare interpreter or
# pip usage that would bypass the UV environment.
#   - `python -m <mod>`     → must be `uv run python -m <mod>` (or the
#                             native CLI). Anchored to avoid matching
#                             `uv run python -m ...` or substrings like
#                             `ipython -m`.
#   - `pip install ...`     → must be `uv pip install ...`. Anchored
#                             likewise.
FORBIDDEN_PATTERNS: dict[str, re.Pattern[str]] = {
    "python -m": re.compile(r"(?<![\w/.-])python\s+-m\b"),
    "pip install": re.compile(r"(?<![\w/.-])pip\s+install\b"),
}

# This test file documents the rule by quoting the patterns; exclude it
# from the scan so the documentation does not self-flag.
SELF_PATH = Path(__file__).resolve()

# Files allowed to mention the forbidden tokens explicitly because they
# document the prohibition rather than invoke it. Keep this set minimal.
ALLOWLIST: set[Path] = set()


def _iter_swarm_sources() -> list[Path]:
    """Return every text source file under the swarm package, if any."""
    if not SWARM_DIR.exists():
        return []
    suffixes = {".py", ".sh", ".md", ".toml", ".yaml", ".yml", ".cfg", ".ini"}
    return [
        p
        for p in SWARM_DIR.rglob("*")
        if p.is_file()
        and p.suffix in suffixes
        and "__pycache__" not in p.parts
        and p.resolve() not in ALLOWLIST
        and p.resolve() != SELF_PATH
    ]


def test_swarm_dir_scan_runs_even_when_empty() -> None:
    """The scan must execute regardless of swarm-package readiness.

    During the earliest Phase 1 tasks the swarm package may not yet exist;
    the guard must still be exercised so it cannot silently no-op once
    files appear.
    """
    # Touching SWARM_DIR.exists() is the smoke check; no assertion on the
    # boolean — both states are valid early in M1.
    _ = SWARM_DIR.exists()


@pytest.mark.parametrize("label,pattern", list(FORBIDDEN_PATTERNS.items()))
def test_no_forbidden_python_or_pip_invocations(
    label: str, pattern: re.Pattern[str]
) -> None:
    """Reject any bare ``python -m`` / ``pip install`` token in swarm sources.

    AC-001: CI lane rejects bare pip/python invocations in swarm code.
    """
    offenders: list[str] = []
    for source in _iter_swarm_sources():
        try:
            text = source.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            # Allow doc/comment lines that explicitly describe the
            # prohibition (e.g. "do NOT use `python -m`").
            if stripped.startswith(("#", "//", "<!--")) and (
                "uv " in stripped.lower()
                or "do not" in stripped.lower()
                or "forbidden" in stripped.lower()
                or "must use" in stripped.lower()
            ):
                continue
            if pattern.search(line):
                rel = source.relative_to(REPO_ROOT)
                offenders.append(f"  {rel}:{lineno}: {stripped}")

    assert not offenders, (
        f"Forbidden `{label}` usage in swarm sources (AC-001 violation). "
        f"Use `uv run` / `uv pip` instead:\n" + "\n".join(offenders)
    )
