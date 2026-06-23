"""Drift guards for the /sc:research command doc (Cluster C3).

Verifies the command POINTS to the research engine rather than duplicating Tavily
params (X6), and that its Adaptive-Depth tiers match RESEARCH_CONFIG.md's Depth
Profiles in name and order. CI-safe (pure file-content assertions).
"""

import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_RESEARCH_MD = _REPO / "src" / "superclaude" / "commands" / "research.md"
_CONFIG_MD = _REPO / "src" / "superclaude" / "core" / "RESEARCH_CONFIG.md"

_TIERS = ["quick", "standard", "deep", "exhaustive"]


def _adaptive_depth_section() -> str:
    text = _RESEARCH_MD.read_text(encoding="utf-8")
    after = text.split("### Adaptive Depth", 1)
    assert len(after) == 2, "research.md missing the '### Adaptive Depth' section"
    return after[1].split("\n## ", 1)[0]


def test_research_command_no_param_duplication():
    """research.md must not duplicate concrete Tavily param assignments (X6)."""
    text = _RESEARCH_MD.read_text(encoding="utf-8")
    for tok in ("search_depth:", "extract_depth:", "max_results:"):
        assert tok not in text, (
            f"research.md duplicates Tavily param '{tok}' (X6 violation)"
        )


def test_research_tiers_match_config():
    """The four Adaptive-Depth tiers match RESEARCH_CONFIG.md profiles; quick/standard != advanced."""
    section = _adaptive_depth_section()
    found = [m.group(1).lower() for m in re.finditer(r"\*\*([A-Za-z]+)\*\*", section)]
    assert found[:4] == _TIERS, (
        f"research.md Adaptive-Depth tiers {found[:4]} != {_TIERS} (name/order mismatch)"
    )

    config = _CONFIG_MD.read_text(encoding="utf-8")
    for t in _TIERS:
        assert re.search(rf"\|\s*{t}\s*\|", config), (
            f"RESEARCH_CONFIG.md missing Depth Profile row for '{t}'"
        )

    # quick/standard tiers must never claim `advanced` depth.
    for line in section.splitlines():
        low = line.lower().strip()
        if low.startswith("- **quick**") or low.startswith("- **standard**"):
            assert "advanced" not in low, f"tier line must not claim advanced: {line!r}"
