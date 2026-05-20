"""Round-trip integration test: research notes prompt → gate.

Closes the structural blind spot identified in the schema-divergence audit:
test_gates.py only feeds the gate hand-written input in the gate's schema,
and test_prompts.py only asserts the prompt emits its own schema. Neither
verifies that the schema instructed by the prompt is the schema accepted
by the gate. This test wires the two together.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from superclaude.cli.prd.gates import (
    _RESEARCH_REQUIRED_SECTIONS,
    _check_research_notes_sections,
    _check_suggested_phases_detail,
)
from superclaude.cli.prd.models import PrdConfig
from superclaude.cli.prd.prompts import build_research_notes_prompt


@pytest.fixture()
def minimal_config(tmp_path: Path) -> PrdConfig:
    task_dir = tmp_path / "task"
    task_dir.mkdir()
    (task_dir / "scope-discovery-raw.md").write_text("# scope\nstub\n")
    (task_dir / "parsed-request.json").write_text(
        '{"GOAL": "x", "PRODUCT_NAME": "X", "PRODUCT_SLUG": "x", '
        '"PRD_SCOPE": "feature", "SCENARIO": "B"}'
    )
    skill_refs = tmp_path / "refs"
    skill_refs.mkdir()
    return PrdConfig(
        user_message="x",
        product_name="X",
        product_slug="x",
        tier="standard",
        task_dir=task_dir,
        skill_refs_dir=skill_refs,
        output_path=tmp_path / "out.md",
    )


def _extract_h2_sections_from_prompt(prompt: str) -> list[str]:
    """Pull the '## SECTION_NAME' headings the prompt instructs the agent to emit."""
    return re.findall(r"^##\s+([A-Z_][A-Z0-9_]+)\s*$", prompt, re.MULTILINE)


def test_prompt_schema_matches_gate_schema(minimal_config: PrdConfig) -> None:
    """The 7 sections the prompt instructs MUST equal the 7 sections the gate requires."""
    prompt = build_research_notes_prompt(minimal_config)
    instructed = _extract_h2_sections_from_prompt(prompt)
    assert sorted(instructed) == sorted(_RESEARCH_REQUIRED_SECTIONS), (
        f"prompt instructs {instructed!r} but gate requires "
        f"{_RESEARCH_REQUIRED_SECTIONS!r}"
    )


def test_prompt_conforming_output_passes_gate(minimal_config: PrdConfig) -> None:
    """A research-notes.md that follows the prompt's instructions MUST pass the gate."""
    prompt = build_research_notes_prompt(minimal_config)
    instructed = _extract_h2_sections_from_prompt(prompt)
    fake_research_notes = "---\nDate: 2026-05-20\nScenario: B\nTier: standard\n---\n\n"
    for section in instructed:
        fake_research_notes += f"## {section}\n- detail\n\n"
    # Ensure SUGGESTED_PHASES has a numbered list item so _check_suggested_phases_detail
    # finds detail under the heading (the loop appends a "- detail" bullet which already
    # satisfies the list-pattern regex, but be explicit for clarity).
    fake_research_notes += "1. Phase one detail\n"

    assert _check_research_notes_sections(fake_research_notes) is True
    assert _check_suggested_phases_detail(fake_research_notes) is True
