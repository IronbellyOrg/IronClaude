"""Tests for PRD supplementary blocks in tasklist prompt builders.

Parametrized across 4 scenarios:
  A: tdd_file=None, prd_file=None (baseline)
  B: tdd_file=set, prd_file=None (TDD only)
  C: tdd_file=None, prd_file=set (PRD only)
  D: tdd_file=set, prd_file=set (both)
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.prompt_policy import BASH_INSPECTION_POLICY
from superclaude.cli.tasklist.prompts import (
    build_tasklist_fidelity_prompt,
    build_tasklist_generate_prompt,
)

ROADMAP = Path("roadmap.md")
TASKLIST_DIR = Path("tasklists/")
TDD = Path("tdd.md")
PRD = Path("prd.md")
PRD_MARKER = "Supplementary PRD"
TDD_MARKER = "Supplementary TDD"


# ── build_tasklist_fidelity_prompt ────────────────────────────────────


class TestTasklistFidelityPrd:
    """PRD supplementary block in build_tasklist_fidelity_prompt."""

    def test_scenario_a_no_blocks(self):
        output = build_tasklist_fidelity_prompt(ROADMAP, TASKLIST_DIR)
        assert PRD_MARKER not in output
        assert TDD_MARKER not in output

    def test_scenario_b_tdd_only(self):
        output = build_tasklist_fidelity_prompt(ROADMAP, TASKLIST_DIR, tdd_file=TDD)
        assert TDD_MARKER in output
        assert PRD_MARKER not in output

    def test_scenario_c_prd_only(self):
        output = build_tasklist_fidelity_prompt(ROADMAP, TASKLIST_DIR, prd_file=PRD)
        assert PRD_MARKER in output
        assert TDD_MARKER not in output

    def test_scenario_d_both(self):
        output = build_tasklist_fidelity_prompt(
            ROADMAP, TASKLIST_DIR, tdd_file=TDD, prd_file=PRD
        )
        assert TDD_MARKER in output
        assert PRD_MARKER in output
        # TDD block appears before PRD block
        tdd_pos = output.index(TDD_MARKER)
        prd_pos = output.index(PRD_MARKER)
        assert tdd_pos < prd_pos

    def test_framework_policy_block_is_excluded_from_drift(self):
        output = build_tasklist_fidelity_prompt(ROADMAP, TASKLIST_DIR)

        assert "## Required Framework Guidance Exclusion" in output
        assert "Do NOT report its heading" in output
        assert "do not recommend removing or weakening it" in output


# ── build_tasklist_generate_prompt ────────────────────────────────────


class TestTasklistGeneratePrd:
    """PRD/TDD enrichment blocks in build_tasklist_generate_prompt."""

    def test_scenario_a_no_blocks(self):
        output = build_tasklist_generate_prompt(ROADMAP)
        assert PRD_MARKER not in output
        assert TDD_MARKER not in output

    def test_scenario_b_tdd_only(self):
        output = build_tasklist_generate_prompt(ROADMAP, tdd_file=TDD)
        assert TDD_MARKER in output
        assert PRD_MARKER not in output

    def test_scenario_c_prd_only(self):
        output = build_tasklist_generate_prompt(ROADMAP, prd_file=PRD)
        assert PRD_MARKER in output
        assert TDD_MARKER not in output
        # PRD suppression guard was removed to allow PRD-driven task generation
        assert "does NOT generate standalone implementation tasks" not in output

    def test_scenario_d_both(self):
        output = build_tasklist_generate_prompt(ROADMAP, tdd_file=TDD, prd_file=PRD)
        assert TDD_MARKER in output
        assert PRD_MARKER in output
        assert "TDD + PRD Interaction" in output

    def test_scenario_d_interaction_note_only_when_both(self):
        """Interaction note only appears when BOTH are provided."""
        output_c = build_tasklist_generate_prompt(ROADMAP, prd_file=PRD)
        output_b = build_tasklist_generate_prompt(ROADMAP, tdd_file=TDD)
        assert "TDD + PRD Interaction" not in output_c
        assert "TDD + PRD Interaction" not in output_b

    def test_baseline_identical_without_supplements(self):
        baseline = build_tasklist_generate_prompt(ROADMAP)
        explicit_none = build_tasklist_generate_prompt(
            ROADMAP, tdd_file=None, prd_file=None
        )
        assert baseline == explicit_none

    def test_policy_is_present_for_all_enrichment_shapes(self):
        outputs = [
            build_tasklist_generate_prompt(ROADMAP),
            build_tasklist_generate_prompt(ROADMAP, tdd_file=TDD),
            build_tasklist_generate_prompt(ROADMAP, prd_file=PRD),
            build_tasklist_generate_prompt(ROADMAP, tdd_file=TDD, prd_file=PRD),
        ]

        for output in outputs:
            assert BASH_INSPECTION_POLICY in output
            assert "## Framework Bash Inspection Policy" in output
            assert "Collapse each eligible five-plus serial inspection wave" in output

        both = outputs[-1]
        assert (
            both.index(TDD_MARKER)
            < both.index(PRD_MARKER)
            < both.index("## Framework Bash Inspection Policy")
            < both.index("<output_format>")
        )
