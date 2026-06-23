"""Drift-guard tests for RESEARCH_CONFIG.md Depth Profiles + Discovery Routing (Cluster C2).

Asserts against the ACTUAL file text (CI-safe, no network):
- every Depth Profile names concrete `search_depth` + `extract_depth` + tool names,
- `advanced` appears only with gating language tying it to deep/exhaustive (never quick/standard),
- the `maps`/`crawls` caps and the crawl 50-URL truncation are present.
"""

import re
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_CONFIG = _REPO_ROOT / "src" / "superclaude" / "core" / "RESEARCH_CONFIG.md"

_PROFILES = ["quick", "standard", "deep", "exhaustive"]


def _read() -> str:
    return _CONFIG.read_text(encoding="utf-8")


def _profile_rows() -> dict[str, str]:
    """Return the Depth Profiles markdown table row for each profile name."""
    rows: dict[str, str] = {}
    for line in _read().splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        first_cell = stripped.strip("|").split("|", 1)[0].strip().lower()
        if first_cell in _PROFILES:
            rows[first_cell] = stripped
    return rows


def test_each_depth_profile_names_concrete_params_and_tools():
    rows = _profile_rows()
    for p in _PROFILES:
        assert p in rows, f"missing Depth Profile row: {p}"
        cells = [c.strip() for c in rows[p].strip().strip("|").split("|")]
        depth_vals = [c for c in cells if c in ("basic", "advanced")]
        assert len(depth_vals) >= 2, (
            f"{p} row lacks concrete search_depth + extract_depth values: {rows[p]}"
        )
        assert "search" in rows[p], f"{p} row does not name any tool: {rows[p]}"


def test_advanced_only_with_gating_language():
    rows = _profile_rows()
    # quick/standard stay basic — must NOT carry `advanced`.
    for p in ["quick", "standard"]:
        assert "advanced" not in rows[p], (
            f"{p} must stay basic, found advanced: {rows[p]}"
        )
    # deep/exhaustive use advanced.
    for p in ["deep", "exhaustive"]:
        assert "advanced" in rows[p], f"{p} must use advanced: {rows[p]}"
    # Explicit gating sentence tying advanced to deep/exhaustive.
    text = _read()
    gating = re.search(
        r"advanced.*ONLY.*(deep|exhaustive)|(deep|exhaustive).*advanced",
        text,
        re.IGNORECASE | re.DOTALL,
    )
    assert gating, "no gating language tying `advanced` to the deep/exhaustive tiers"


def test_discovery_caps_and_crawl_truncation_present():
    text = _read()
    assert "maps=2" in text, "missing maps=2 cap"
    assert "crawls=1" in text, "missing crawls=1 cap"
    assert re.search(r"50[\s-]*URL", text, re.IGNORECASE), (
        "missing crawl 50-URL truncation cap"
    )


def test_map_and_crawl_tool_ids_present():
    text = _read()
    assert "mcp__tavily__tavily-map" in text
    assert "mcp__tavily__tavily-crawl" in text
