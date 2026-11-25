"""Pin the research-routing rule in the always-loaded core/CLAUDE.md (issue 597).

The incident behind issue 597 showed a documentation question delegated to an
agent whose tools had no research MCP access, so the lookup ran entirely on
native fetches. The rule must keep the MCP-first routes, require a delegate
capability check (else a direct lookup), and keep native/local fallbacks —
never a blanket native-tool ban.
"""

from __future__ import annotations

from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_CLAUDE = _REPO / "src/superclaude/core/CLAUDE.md"


def _rule() -> str:
    text = _CLAUDE.read_text(encoding="utf-8")
    start = text.index("## Core Rules")
    section = text[start:].split("\n## ", 1)[0]
    return next(
        line for line in section.splitlines() if line.startswith("11. **Research routing**")
    )


def test_rule_pins_mcp_first_routes():
    rule = _rule()
    assert "`context7` first" in rule
    assert "`tavily` first" in rule
    assert "extract a likely answer's page before searching more" in rule


def test_rule_requires_delegate_capability_check_or_direct_lookup():
    rule = _rule()
    assert "check the delegate's tools include the needed server" in rule
    assert "run the lookup directly" in rule


def test_rule_keeps_native_and_local_fallback():
    rule = _rule()
    assert "fallbacks" in rule
    assert "missing, erroring or out of scope" in rule
