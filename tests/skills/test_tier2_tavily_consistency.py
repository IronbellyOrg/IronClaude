"""Cluster C5 (troubleshoot/reflect) Tavily consistency drift guards (M3b).

The Tier-2 troubleshoot path and the reflect path use ONLY `tavily-search` (no
extract/map/crawl — X5), preserve their rate cap and fail-open posture, and obey the
X3 split: troubleshoot overrides `search_depth: advanced` per-call (M3b) while reflect
inherits the basic baseline (names no per-call params). CI-safe (file-content only).
"""

import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_SC = _REPO / "src" / "superclaude"

_TROUBLESHOOT_CMD = _SC / "commands" / "troubleshoot.md"
_TROUBLESHOOT_SKILL = _SC / "skills" / "sc-troubleshoot-protocol" / "SKILL.md"
_REFLECT_CMD = _SC / "commands" / "reflect.md"
_REFLECT_SKILL = _SC / "skills" / "sc-reflect-protocol" / "SKILL.md"
_BRAINSTORM_SKILL = _SC / "skills" / "sc-brainstorm-protocol" / "SKILL.md"

_ALL_FOUR = [_TROUBLESHOOT_CMD, _TROUBLESHOOT_SKILL, _REFLECT_CMD, _REFLECT_SKILL]
_FORBIDDEN_TOOLS = ["tavily-extract", "tavily-map", "tavily-crawl"]


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def test_tier2_tool_id_parity():
    """All 4 C5 files reference mcp__tavily__tavily_search and NO extract/map/crawl (X5)."""
    for p in _ALL_FOUR:
        text = _read(p)
        assert "mcp__tavily__tavily_search" in text, (
            f"{p.name} must reference tavily-search"
        )
        for tool in _FORBIDDEN_TOOLS:
            assert tool not in text, f"{p.name} must not reference {tool} (X5)"


def test_brainstorm_no_map_crawl():
    """X5 — sc-brainstorm-protocol delegates to /sc:research and must NOT reference
    extract/map/crawl directly (L2).

    Brainstorm carries no ``mcp__tavily__*`` tool id of its own (it inherits the surface
    via the /sc:research delegation), so it is intentionally excluded from ``_ALL_FOUR``
    (which requires ``tavily-search``). This guard closes the X5 coverage gap for the
    brainstorm consumer without falsely requiring a tool id it does not declare.
    """
    text = _read(_BRAINSTORM_SKILL)
    for tool in _FORBIDDEN_TOOLS:
        assert tool not in text, (
            f"sc-brainstorm-protocol must not reference {tool} (X5 confinement)"
        )


def test_rate_cap_intact():
    """The troubleshoot SKILL retains its ≤2-query Tier-2 rate cap."""
    text = _read(_TROUBLESHOOT_SKILL)
    assert re.search(r"≤2|at most 2 quer|2 queries", text), (
        "troubleshoot SKILL lost its ≤2-query Tier-2 rate cap"
    )


def test_fail_open_intact():
    """Both skills retain fail-open / degraded posture on missing MCP."""
    for p in (_TROUBLESHOOT_SKILL, _REFLECT_SKILL):
        text = _read(p).lower()
        assert "fail-open" in text or "fail open" in text or "degrad" in text, (
            f"{p.name} lost its fail-open/degraded language"
        )


def test_troubleshoot_search_depth_advanced():
    """M3b: troubleshoot SKILL overrides search_depth: advanced; reflect names no per-call params."""
    assert "search_depth: advanced" in _read(_TROUBLESHOOT_SKILL), (
        "troubleshoot SKILL must carry the Tier-2 `search_depth: advanced` override (M3b)"
    )
    reflect = _read(_REFLECT_SKILL)
    for tok in ("search_depth:", "extract_depth:", "max_results:"):
        assert tok not in reflect, (
            f"reflect SKILL must not name per-call Tavily param '{tok}' (X3 — inherits basic)"
        )
