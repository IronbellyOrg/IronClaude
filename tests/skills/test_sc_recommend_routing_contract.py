"""Regression tests for the routing contract in the sc-recommend SKILL.md.

Spec 3.2 asks /sc:recommend to read the routing guide first, let the guide's
levels override native-first answers, emit ordered workflows with every
mandatory flag, allow the two Claude Code built-ins, fall back cleanly when the
guide is missing, and keep the uv cache step optional. These tests pin the
SKILL.md text that carries each requirement, so a later edit cannot drop one
silently.
"""

from __future__ import annotations

from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_SKILL = _REPO / "src/superclaude/skills/sc-recommend/SKILL.md"
_HELP = _REPO / "src/superclaude/commands/help.md"

_NOT_FOUND = (
    "Routing guide not found. pipx/pip install: run superclaude update. "
    "Plugin install: update the SuperClaude plugin. Until then, recommendations "
    "do not use the routing guide."
)


def _text() -> str:
    return _SKILL.read_text(encoding="utf-8")


def _section(text: str, start: str, end: str) -> str:
    begin = text.index(start)
    return text[begin : text.index(end, begin + len(start))]


def test_step_0_comes_before_the_hot_path():
    text = _text()
    assert text.index("## Step 0") < text.index("## Hot-Path Cache Lookup")


def test_guide_locations_are_listed_in_order():
    step0 = _section(_text(), "## Step 0", "## Hot-Path Cache Lookup")
    paths = [
        "`~/.claude/HOW-WE-WORK.md`",
        "`${CLAUDE_SKILL_DIR}/refs/HOW-WE-WORK.md`",
        "`${CLAUDE_PLUGIN_ROOT}/skills/sc-recommend/refs/HOW-WE-WORK.md`",
        "`src/superclaude/core/HOW-WE-WORK.md`",
    ]
    positions = [step0.index(p) for p in paths]
    assert positions == sorted(positions), positions


def test_guide_not_found_line_is_shared_with_help():
    assert _NOT_FOUND in _text()
    assert _NOT_FOUND in _HELP.read_text(encoding="utf-8")


def test_hard_limit_overrides_native_first():
    text = _text()
    assert "hard limit overrides native first" in text
    assert "more than 5 edits or touches more than one source file" in text


def test_mandatory_flags_rule_is_present():
    assert "Every flag listed in the row's `mandatory_flags`" in _text()


def test_builtins_allowed_in_r2_and_r4():
    text = _text()
    r2 = _section(text, "### Rule R2", "### Rule R3")
    r4 = _section(text, "### Rule R4", "## Return Contract")
    for rule in (r2, r4):
        assert "/code-review" in rule and "/security-review" in rule


def test_uv_cache_step_is_gated():
    hot = _section(_text(), "## Hot-Path Cache Lookup", "## Phase 0")
    assert "**Availability gate" in hot
    assert "test -f src/superclaude/cli/recommend/prompts.py" in hot
    assert "uv run superclaude recommend --help" in hot
    assert "recommend CLI unavailable; cache skipped" in hot
