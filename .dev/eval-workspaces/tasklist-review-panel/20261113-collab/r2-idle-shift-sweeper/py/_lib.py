"""Shared helpers: load the real findings parser read-only from REPO/src (stdlib-only module, loaded by path so
no package import side effects), and the findings-block line locator used by h2_normalize and tagger."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path

R2 = Path(__file__).resolve().parents[1]
REAL_REPO = R2.parents[4]
FINDINGS_PY = Path(os.environ.get("R2_FINDINGS_PY") or REAL_REPO / "src/superclaude/cli/review/findings.py")

_mod = None


def findings():
    global _mod
    if _mod is None:
        spec = importlib.util.spec_from_file_location("r2_findings", FINDINGS_PY)
        _mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_mod)
    return _mod


def last_block_lines(text: str) -> list[tuple[int, str]]:
    """(1-based line number, text) of the body lines of the last findings-v1 block, [] when none."""
    f = findings()
    _found, blocks = f._blocks_after(text, f._HEAD_FINDINGS, "findings-v1")
    return blocks[-1][1] if blocks else []


def replace_lines(text: str, repl: dict[int, str]) -> str:
    lines = text.split("\n")
    for n, s in repl.items():
        lines[n - 1] = s
    return "\n".join(lines)
