"""The always-loaded core/CLAUDE.md carries a copy of the guide's level table.

The copy must stay byte-equal to the guide's level-table block (between the
same markers), so editing one without the other fails here. The block must also
carry the /sc:<name> must-invoke-skill rule and a plain-path pointer to the
guide, never an @ import (an import would load the whole guide every session).
"""

from __future__ import annotations

import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_CORE = _REPO / "src/superclaude/core"
_CLAUDE = _CORE / "CLAUDE.md"
_GUIDE = _CORE / "HOW-WE-WORK.md"
_BEGIN, _END = "<!-- level-table:v1 -->", "<!-- /level-table -->"


def _block(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    assert text.count(_BEGIN) == 1 and text.count(_END) == 1, path
    start = text.index(_BEGIN) + len(_BEGIN)
    return text[start : text.index(_END, start)]


def test_level_table_copy_matches_guide():
    assert _block(_CLAUDE) == _block(_GUIDE), (
        "core/CLAUDE.md level table differs from HOW-WE-WORK.md; "
        "re-copy the block between the level-table markers from the guide"
    )


def test_routing_block_rule_and_pointer():
    text = _CLAUDE.read_text(encoding="utf-8")
    assert "## How to choose a workflow" in text
    assert "`/sc:` commands must load their skill" in text
    assert (
        "invoke the matching skill with the Skill tool before any other output" in text
    )
    assert "`~/.claude/HOW-WE-WORK.md`" in text
    assert "/sc:recommend" in text
    # The pointer and the context-pressure warning must sit in the routing block
    # itself (after the level table, before the next heading), not only in Key Docs.
    after = text[text.index(_END) + len(_END) :]
    tail = after.split("\n## ", 1)[0]
    assert "`~/.claude/HOW-WE-WORK.md`" in tail
    assert "/sc:recommend" in tail
    assert "warn the user" in tail
    assert not re.search(r"^\s*@\S*HOW-WE-WORK", text, re.M)


def test_imports_resolve_to_shipped_core_files():
    text = _CLAUDE.read_text(encoding="utf-8")
    imports = re.findall(r"^\s*@(\S+)\s*$", text, re.M)
    assert imports == ["BASH_INSPECTION_POLICY.md"]
    assert all((_CORE / name).is_file() for name in imports)


def test_removed_sections_stay_removed():
    text = _CLAUDE.read_text(encoding="utf-8")
    for gone in (
        "## Personas",
        "## Skills & Commands",
        "## Project Structure",
        "## Dev Commands",
        "## Component Sync",
        "wave strategies",
        "PLANNING.md",
        "`TASK.md`",
        "KNOWLEDGE.md",
        "make dev",
        "make sync-dev",
    ):
        assert gone not in text, gone


def test_mcp_flag_column_is_advisory():
    text = _CLAUDE.read_text(encoding="utf-8")
    assert "| Flag (advisory) |" in text
