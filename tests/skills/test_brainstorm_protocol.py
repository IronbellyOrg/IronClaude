"""Drift guard for the sc:brainstorm protocol (Cluster C4).

The Wave-2A enrichment matrix must ROUTE to the research engine only — it must not
duplicate Tavily params or name the map/crawl tools (X5/X6). CI-safe.
"""

import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_BRAINSTORM = (
    _REPO / "src" / "superclaude" / "skills" / "sc-brainstorm-protocol" / "SKILL.md"
)

_FORBIDDEN = [
    "search_depth:",
    "extract_depth:",
    "max_results:",
    "tavily-map",
    "tavily-crawl",
]


def _wave2a_section() -> str:
    text = _BRAINSTORM.read_text(encoding="utf-8")
    parts = re.split(r"###\s*Wave 2A", text, maxsplit=1)
    assert len(parts) == 2, "brainstorm SKILL missing the 'Wave 2A' section"
    # Up to the next '### Wave ' heading.
    return re.split(r"\n###\s*Wave ", parts[1], maxsplit=1)[0]


def test_brainstorm_no_tavily_param_duplication():
    """Wave-2A enrichment matrix routes only — no Tavily params / map/crawl tool names."""
    section = _wave2a_section()
    for tok in _FORBIDDEN:
        assert tok not in section, (
            f"Wave-2A matrix must not contain Tavily token '{tok}' (enrichment routes only)"
        )
