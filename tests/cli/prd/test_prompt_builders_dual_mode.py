"""Unit tests for the dual-mode prd CLI prompt builders.

Covers the new critical path introduced by PR #71 and consolidated by its
remediation (Cluster 2 + Cluster 4): the `_dual_mode_call` dispatch helper,
the three dual-mode builders (`build_investigation_prompt`,
`build_web_research_prompt`, `build_synthesis_prompt`), the
`_parse_agent_block` research-notes parser, and the `_build_prompt`
inspect-signature dispatch in the executor.

These are the executor's only Stage B prompt-construction path — review
finding H1 flagged the complete absence of coverage here.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.prd import prompts
from superclaude.cli.prd.config import resolve_config
from superclaude.cli.prd.executor import PrdExecutor
from superclaude.cli.prd.prompts import (
    _parse_agent_block,
    _render_investigation_prompt,
    build_investigation_prompt,
    build_synthesis_prompt,
    build_web_research_prompt,
)

_RESEARCH_NOTES = """# Research Notes

### Agent 1 — Foo Domain
- **Topic**: Some investigation topic about the foo subsystem
- **Agent type**: backend
- **Files**:
  - src/foo.py
  - src/foo_helpers.py

### Agent 2 — Bar Domain
- **Topic**: A different topic about bar
- **Agent type**: frontend

### Agent 7 — Foo Web
- **Topic**: External web research for the foo ecosystem
- **Agent type**: web-analyst
"""


@pytest.fixture
def config_with_notes(tmp_path: Path):
    """A PrdConfig whose task_dir holds a research-notes.md fixture."""
    config = resolve_config(
        "test product", product="dualmode-test", tier="standard", dry_run=True
    )
    task_dir = tmp_path / "prd-dualmode-test"
    (task_dir / "research").mkdir(parents=True)
    (task_dir / "synthesis").mkdir(parents=True)
    config.task_dir = task_dir
    config.work_dir = tmp_path
    (task_dir / "research-notes.md").write_text(_RESEARCH_NOTES, encoding="utf-8")
    return config


# ---------------------------------------------------------------------------
# build_investigation_prompt — config mode
# ---------------------------------------------------------------------------


def test_build_investigation_prompt_config_mode_returns_agent_1_topic(
    config_with_notes,
):
    """Config-mode dispatch resolves Agent 1 and embeds its topic."""
    prompt = build_investigation_prompt(
        config_with_notes, step_id="investigation-1"
    )
    assert prompt
    assert "Some investigation topic about the foo subsystem" in prompt


# ---------------------------------------------------------------------------
# _parse_agent_block
# ---------------------------------------------------------------------------


def test_parse_agent_block_minimal_valid():
    """A well-formed Agent block yields topic / agent_type / files."""
    agent = _parse_agent_block(_RESEARCH_NOTES, 1)
    assert agent["topic"] == "Some investigation topic about the foo subsystem"
    assert agent["agent_type"] == "backend"
    assert "src/foo.py" in agent["files"]


def test_parse_agent_block_missing_topic_falls_back_to_title():
    """A block with a title but no **Topic** line uses the title as topic."""
    notes = "### Agent 1 — Title Only Domain\n- **Agent type**: backend\n"
    agent = _parse_agent_block(notes, 1)
    assert agent["topic"] == "Title Only Domain"


def test_parse_agent_block_missing_agent_n_returns_empty():
    """Requesting an absent Agent index yields an empty dict."""
    assert _parse_agent_block(_RESEARCH_NOTES, 5) == {}


def test_parse_agent_block_no_false_match_at_agent_10():
    """`Agent 1` must not false-match a notes file containing only Agent 10."""
    notes = "### Agent 10 — Tenth Domain\n- **Topic**: tenth\n"
    assert _parse_agent_block(notes, 1) == {}


# ---------------------------------------------------------------------------
# build_web_research_prompt — config mode (agent_idx = 6 + web_idx)
# ---------------------------------------------------------------------------


def test_build_web_research_prompt_resolves_agent_idx_6_plus_web_idx(
    config_with_notes,
):
    """web-research-1 maps to Agent 7 (6 + 1) and embeds that topic."""
    prompt = build_web_research_prompt(
        config_with_notes, step_id="web-research-1"
    )
    assert "External web research for the foo ecosystem" in prompt


# ---------------------------------------------------------------------------
# build_synthesis_prompt — config mode + out-of-range fallback
# ---------------------------------------------------------------------------


def test_build_synthesis_prompt_returns_mapping_entry_synth_file(
    config_with_notes,
):
    """synthesis-1 resolves to the first synthesis-mapping entry."""
    prompt = build_synthesis_prompt(config_with_notes, step_id="synthesis-1")
    assert "synth-01-" in prompt


def test_build_synthesis_prompt_out_of_range_falls_back_to_entry_1(
    config_with_notes,
):
    """An out-of-range synthesis index falls back to mapping entry 1."""
    prompt = build_synthesis_prompt(config_with_notes, step_id="synthesis-99")
    assert "synth-01-" in prompt


# ---------------------------------------------------------------------------
# Legacy positional calling convention still works
# ---------------------------------------------------------------------------


def test_build_investigation_prompt_legacy_positional_call_still_works(
    tmp_path: Path,
):
    """The legacy positional signature still routes to the renderer."""
    out = tmp_path / "o.md"
    via_builder = build_investigation_prompt(
        topic="x", agent_type="y", files=["f"],
        product_root=".", output_path=out,
    )
    direct = _render_investigation_prompt(
        topic="x", agent_type="y", files=["f"],
        product_root=".", output_path=out,
    )
    assert via_builder == direct


# ---------------------------------------------------------------------------
# _build_prompt must NOT swallow a TypeError raised inside a builder body
# ---------------------------------------------------------------------------


def test_build_prompt_propagates_typeerror_from_buggy_builder_body(
    monkeypatch,
):
    """A TypeError from inside the builder body surfaces — not swallowed.

    The prior triple-`except TypeError` cascade would silently fall
    through to a stub string; the inspect-signature dispatch only guards
    `inspect.signature`, so a body bug propagates as the real error.
    """
    def buggy_builder(config, **kwargs):
        raise TypeError("body bug")

    monkeypatch.setattr(prompts, "buggy_builder", buggy_builder, raising=False)
    config = resolve_config(
        "test", product="bug-test", tier="standard", dry_run=True
    )
    executor = PrdExecutor(config)
    with pytest.raises(TypeError, match="body bug"):
        executor._build_prompt("buggy_builder")
