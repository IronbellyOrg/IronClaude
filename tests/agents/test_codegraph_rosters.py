"""Drift guards for the codegraph rosters of the four read-only review agents (issue #323, Phase 3).

Each agent may list only the exact codegraph tool names its spawn modes earned in
Phase 3 experiment E-6, never a wildcard, never a Serena name; its body points to
the shared guide `~/.claude/CODEGRAPH.md`; and reuse-auditor keeps the Phase 1 Grep
floor below its codegraph tier. CI-safe: pure file-content assertions.
"""

import re
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_AGENTS = _REPO / "src" / "superclaude" / "agents"

# Expected codegraph names per agent, from
# .dev/codegraph-migration/experiments/P3-T0/E6-agent-matrix.md (Claude Code 2.1.316):
# every agent passed both foreground and background spawns, so each keeps the exact
# roster of source section 1.2 (rows 5, 7, 8, 12). An agent that fails E-6 maps to set().
_E6_CODEGRAPH_ROSTERS = {
    "troubleshoot-analyst": {
        "mcp__codegraph__codegraph_search",
        "mcp__codegraph__codegraph_node",
        "mcp__codegraph__codegraph_callers",
        "mcp__codegraph__codegraph_impact",
    },
    "reflect-reviewer": {
        "mcp__codegraph__codegraph_search",
        "mcp__codegraph__codegraph_node",
        "mcp__codegraph__codegraph_callers",
        "mcp__codegraph__codegraph_impact",
    },
    "reuse-auditor": {
        "mcp__codegraph__codegraph_search",
        "mcp__codegraph__codegraph_node",
        "mcp__codegraph__codegraph_callers",
    },
    "auggie-reviewer": {
        "mcp__codegraph__codegraph_search",
        "mcp__codegraph__codegraph_node",
        "mcp__codegraph__codegraph_callers",
    },
}


def _split(name: str) -> tuple[list[str], str]:
    text = (_AGENTS / f"{name}.md").read_text(encoding="utf-8")
    m = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, re.S)
    assert m, f"{name}.md has no frontmatter"
    roster = re.search(r"^tools:\s*(.*)$", m.group(1), re.M)
    assert roster, f"{name}.md has no tools: line"
    tools = [t.strip() for t in roster.group(1).strip("[] ").split(",") if t.strip()]
    return tools, m.group(2)


@pytest.mark.parametrize("name", sorted(_E6_CODEGRAPH_ROSTERS))
def test_roster_has_exact_codegraph_names(name):
    tools, _ = _split(name)
    assert not [t for t in tools if t.startswith("mcp__serena")], (
        f"{name} still lists Serena"
    )
    assert "mcp__codegraph__*" not in tools, f"{name} uses the codegraph wildcard"
    codegraph = {t for t in tools if t.startswith("mcp__codegraph__")}
    assert codegraph == _E6_CODEGRAPH_ROSTERS[name], (
        f"{name} codegraph roster drifted from E-6"
    )


@pytest.mark.parametrize("name", sorted(_E6_CODEGRAPH_ROSTERS))
def test_body_points_to_shared_guide(name):
    _, body = _split(name)
    assert "~/.claude/CODEGRAPH.md" in body, f"{name} body lacks the guide lookup line"


def test_reuse_auditor_keeps_grep_floor_below_codegraph():
    _, body = _split("reuse-auditor")
    cost = body.split("### 8. Cost control", 1)[1].split("\n## ", 1)[0]
    assert "codegraph_" in cost and "Grep" in cost, (
        "section 8 must name codegraph and the Grep floor"
    )
    f4 = next(ln for ln in body.splitlines() if ln.startswith("| F4 "))
    assert "codegraph_" in f4 and "Grep" in f4, (
        "F4 must name codegraph and the Grep floor"
    )


def test_auggie_reviewer_bars_codegraph_cli():
    _, body = _split("auggie-reviewer")
    assert "Do not run the `codegraph` CLI through Bash" in body
