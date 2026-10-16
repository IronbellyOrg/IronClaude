"""Content tests for the live-listing /sc:help command."""

from __future__ import annotations

import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_HELP = _REPO / "src/superclaude/commands/help.md"


def _text() -> str:
    return _HELP.read_text(encoding="utf-8")


def test_help_has_no_static_command_table():
    assert not re.search(r"^\|\s*`?/sc:[a-z-]+`?\s*\|", _text(), re.M)


def test_help_lists_live_locations():
    text = _text()
    for p in (
        '"$HOME/.claude/commands/sc"',
        '"$HOME/.claude/skills"',
        "find -L .claude/commands .claude/skills",
    ):
        assert p in text, p


def test_help_prints_level_table_by_marker_and_points_to_recommend():
    text = _text()
    assert "<!-- level-table:v1 -->" in text
    assert "<!-- /level-table -->" in text
    assert "/sc:recommend" in text


def test_help_points_to_guide_as_plain_path():
    text = _text()
    assert "~/.claude/HOW-WE-WORK.md" in text
    assert not re.search(r"^\s*@\S*HOW-WE-WORK", text, re.M)
    assert "level-table:v1" in text


def test_help_size_and_shape():
    text = _text()
    assert len(text.splitlines()) <= 200
    assert "## Activation" not in text
    assert "allowed-tools:" in text.split("---", 2)[1]
    for name in (
        "FLAGS.md",
        "ORCHESTRATOR.md",
        "COMMANDS.md",
        "PERSONAS.md",
        "MODES.md",
        "MCP.md",
    ):
        assert name not in text


def test_help_names_builtins():
    text = _text()
    assert "/code-review" in text and "/security-review" in text
