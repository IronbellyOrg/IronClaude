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


def _wave_section(n: str) -> str:
    text = _BRAINSTORM.read_text(encoding="utf-8")
    parts = re.split(rf"###\s*Wave {n}\b", text, maxsplit=1)
    assert len(parts) == 2, f"brainstorm SKILL missing the 'Wave {n}' section"
    return re.split(r"\n###\s*Wave ", parts[1], maxsplit=1)[0]


def test_brainstorm_unattended_nested_directories_are_named():
    """Under --unattended the nested calls get their own directories (P1 worker contract)."""
    wave3 = _wave_section("3")
    assert "--unattended" in wave3 and "nested/adversarial-" in wave3
    wave2a = _wave2a_section()
    assert "nested/analyze-" in wave2a and "skipped" in wave2a
    assert "exactly as passed" in _wave_section("0")
    refs = _BRAINSTORM.parent / "refs" / "handoff-routing.md"
    assert "nested/adversarial-" in refs.read_text(encoding="utf-8")


def _section(text: str, start: str, end_pattern: str) -> str:
    after = text.split(start, 1)
    assert len(after) == 2, f"missing anchor {start!r}"
    return re.split(end_pattern, after[1], maxsplit=1, flags=re.M)[0]


def test_brainstorm_unattended_codebase_scan_writes_no_nested_directory():
    """Only a /sc:analyze call writes nested/analyze-<n>/; auggie and fallback_1 do not (P1 lc10)."""
    lead = "**Under `--unattended`**"
    parts = _wave2a_section().split(lead, 1)
    assert len(parts) == 2, "Wave 2A missing the Under --unattended paragraph"
    paragraph = re.split(r"\n\s*\n", parts[1], maxsplit=1)[0]
    assert "Quality-tier tracking" not in paragraph, "paragraph slice ran past its end"
    for phrase in (
        "fallback_1",
        "write no nested directory and no nested contract",
        "only by a `/sc:analyze` call",
    ):
        assert phrase in paragraph, phrase

    routing = (_BRAINSTORM.parent / "refs" / "handoff-routing.md").read_text(
        encoding="utf-8"
    )
    tier1 = _section(
        routing, "**Tier 1 (primary)**", r"^\*\*Tier 2 \(fallback_1\)\*\*: codegraph"
    )
    tier2 = _section(
        routing, "**Tier 2 (fallback_1)**: codegraph", r"^\*\*Final fallback"
    )
    for name, tier in (("Tier 1", tier1), ("Tier 2", tier2)):
        for phrase in (
            "writes no nested directory and no nested contract",
            "only by a `/sc:analyze` call",
        ):
            assert tier.count(phrase) == 1, f"{name}: {phrase}"


def test_brainstorm_unattended_research_light_runs_nested_and_deep_is_skipped():
    """Under --unattended research-light is a nested /sc:research call; research-deep is skipped (D-P2-1)."""
    lead = "**Under `--unattended`**"
    parts = _wave2a_section().split(lead, 1)
    assert len(parts) == 2, "Wave 2A missing the Under --unattended paragraph"
    paragraph = re.split(r"\n\s*\n", parts[1], maxsplit=1)[0]
    for phrase in ("/sc:research", "nested/research-", "quality_tier: skipped"):
        assert phrase in paragraph, phrase
    assert "the two research rows are skipped" not in paragraph


def test_brainstorm_omitted_model_and_explicit_rotation_are_separate():
    wave0 = _wave_section("0")
    assert "When omitted, use `default` for every persona at every depth" in wave0
    wave2 = _wave_section("2B")
    assert "Omitted `--models`: assign `default`" in wave2
    assert "preserve the validated list order" in wave2
    assert "never promote or replace" in wave2
    assert "prefer `opus`" not in wave2


def test_brainstorm_no_tavily_param_duplication():
    """Wave-2A enrichment matrix routes only — no Tavily params / map/crawl tool names."""
    section = _wave2a_section()
    for tok in _FORBIDDEN:
        assert tok not in section, (
            f"Wave-2A matrix must not contain Tavily token '{tok}' (enrichment routes only)"
        )
