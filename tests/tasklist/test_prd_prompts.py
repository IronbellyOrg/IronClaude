"""Tests for PRD supplementary blocks in tasklist prompt builders.

Parametrized across 4 scenarios:
  A: tdd_file=None, prd_file=None (baseline)
  B: tdd_file=set, prd_file=None (TDD only)
  C: tdd_file=None, prd_file=set (PRD only)
  D: tdd_file=set, prd_file=set (both)
"""

from __future__ import annotations

from pathlib import Path

import pytest

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
        output = build_tasklist_fidelity_prompt(
            ROADMAP, TASKLIST_DIR, tdd_file=TDD
        )
        assert TDD_MARKER in output
        assert PRD_MARKER not in output

    def test_scenario_c_prd_only(self):
        output = build_tasklist_fidelity_prompt(
            ROADMAP, TASKLIST_DIR, prd_file=PRD
        )
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
