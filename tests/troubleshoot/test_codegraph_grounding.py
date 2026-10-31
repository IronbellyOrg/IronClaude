"""Drift guards for codegraph grounding in /sc:troubleshoot Tier 1 (issue #323, Phase 3).

Pins the five exact codegraph tools in the protocol skill's allowlist (never explore),
the Wave 1 codegraph step sitting above the unchanged Glob + Grep floor, the TARGET
header's `mcps_available` enum, the codegraph run state passed in the analyst briefs,
and that no Serena text came back. CI-safe: pure file-content assertions.
"""

import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_SKILL_DIR = _REPO / "src" / "superclaude" / "skills" / "sc-troubleshoot-protocol"
_SKILL = _SKILL_DIR / "SKILL.md"
_COMMAND = _REPO / "src" / "superclaude" / "commands" / "troubleshoot.md"
_FILES = [
    _COMMAND,
    _SKILL,
    _SKILL_DIR / "refs" / "triage-checklist.md",
    _SKILL_DIR / "refs" / "diagnosability-audit.md",
]
_TOOLS = [f"mcp__codegraph__codegraph_{t}" for t in ("status", "search", "node", "callers", "impact")]
_STATE_FIELDS = ("index_state", "checked_at", "worktree_root", "projectPath")


def _skill() -> str:
    return _SKILL.read_text(encoding="utf-8")


def _section(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


def test_allowed_tools_name_five_codegraph_tools_and_no_explore():
    front = re.match(r"\A---\n(.*?)\n---", _skill(), re.S).group(1)
    allowed = re.search(r"^allowed-tools:\s*(.*)$", front, re.M).group(1)
    tools = {t.strip() for t in allowed.split(",")}
    for name in _TOOLS:
        assert name in tools, f"allowed-tools lacks {name}"
    assert "codegraph_explore" not in _skill()
    assert "mcp__codegraph__*" not in tools


def test_wave1_names_codegraph_node_above_glob_grep_floor():
    wave1 = _section(_skill(), "### Wave 1: Tier 1", "### Wave 1.5:")
    assert "codegraph_node" in wave1 and "codegraph_callers" in wave1
    assert "`Glob` + `Grep`" in wave1, "the Phase 1 Glob + Grep floor must stay"
    assert wave1.index("codegraph_node") < wave1.index("`Glob` + `Grep`"), "codegraph tier goes first"
    assert "tier1-callers.md" in wave1


def test_target_header_mcps_available_enum():
    assert "mcps_available: <auggie|codegraph|context7|tavily|none>" in _skill().splitlines()


def test_analyst_briefs_carry_codegraph_run_state():
    text = _skill()
    delegation = _section(text, "## Native diagnostic delegation", "| Dispatch site |")
    wave16 = _section(text, "### Wave 1.6:", "### Wave 1.7:")
    wave3 = _section(text, "### Wave 3:", "### Wave 4")
    for part, name in ((delegation, "delegation contract"), (wave16, "Wave 1.6 brief"), (wave3, "Wave 3 brief")):
        for field in _STATE_FIELDS:
            assert field in part, f"{name} does not pass {field}"


def test_no_serena_in_troubleshoot_files():
    for path in _FILES:
        assert "serena" not in path.read_text(encoding="utf-8").lower(), f"{path.relative_to(_REPO)} names serena"
