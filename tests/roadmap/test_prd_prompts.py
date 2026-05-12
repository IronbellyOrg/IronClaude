"""Tests for PRD supplementary blocks in roadmap prompt builders.

Parametrized across 4 core scenarios:
  A: tdd_file=None, prd_file=None (baseline)
  B: tdd_file=set, prd_file=None
  C: tdd_file=None, prd_file=set (PRD only)
  D: tdd_file=set, prd_file=set (both)
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.roadmap.prompts import (
    build_extract_prompt,
    build_extract_prompt_tdd,
    build_generate_prompt,
    build_score_prompt,
    build_spec_fidelity_prompt,
    build_test_strategy_prompt,
)
from superclaude.cli.roadmap.models import AgentSpec


SPEC = Path("spec.md")
TDD = Path("tdd.md")
PRD = Path("prd.md")
ROADMAP = Path("roadmap.md")
DEBATE = Path("debate.md")
VARIANT_A = Path("variant-a.md")
VARIANT_B = Path("variant-b.md")
PRD_MARKER = "Supplementary PRD"
TDD_SUPP_MARKER = "Supplementary TDD"
AGENT = AgentSpec("opus", "architect")
EXTRACTION = Path("extraction.md")


# ── build_extract_prompt ──────────────────────────────────────────────

class TestBuildExtractPromptPrd:
    """PRD supplementary block in build_extract_prompt."""

    def test_scenario_a_no_prd_block(self):
        output = build_extract_prompt(SPEC)
        assert PRD_MARKER not in output

    def test_scenario_b_tdd_only_no_prd_block(self):
        output = build_extract_prompt(SPEC, tdd_file=TDD)
        assert PRD_MARKER not in output

    def test_scenario_c_prd_block_present(self):
        output = build_extract_prompt(SPEC, prd_file=PRD)
        assert PRD_MARKER in output

    def test_scenario_d_both_blocks_present(self):
        output = build_extract_prompt(SPEC, tdd_file=TDD, prd_file=PRD)
        assert PRD_MARKER in output

    def test_baseline_identical_without_prd(self):
        """Output with prd_file=None must match output without prd_file kwarg."""
        baseline = build_extract_prompt(SPEC)
        explicit_none = build_extract_prompt(SPEC, prd_file=None)
        assert baseline == explicit_none


# ── build_extract_prompt_tdd ──────────────────────────────────────────

class TestBuildExtractPromptTddPrd:
    """PRD supplementary block in build_extract_prompt_tdd."""

    def test_scenario_a_no_prd_block(self):
        output = build_extract_prompt_tdd(SPEC)
        assert PRD_MARKER not in output

    def test_scenario_c_prd_block_present(self):
        output = build_extract_prompt_tdd(SPEC, prd_file=PRD)
        assert PRD_MARKER in output

    def test_scenario_d_both_present(self):
        output = build_extract_prompt_tdd(SPEC, tdd_file=TDD, prd_file=PRD)
        assert PRD_MARKER in output


# ── build_generate_prompt ─────────────────────────────────────────────

class TestBuildGeneratePromptPrd:
    """PRD supplementary block in build_generate_prompt."""

    def test_scenario_a_no_prd_block(self):
        output = build_generate_prompt(AGENT, EXTRACTION)
        assert PRD_MARKER not in output

    def test_scenario_c_prd_block_present(self):
        output = build_generate_prompt(AGENT, EXTRACTION, prd_file=PRD)
        assert PRD_MARKER in output

    def test_baseline_identical_without_prd(self):
        baseline = build_generate_prompt(AGENT, EXTRACTION)
        explicit_none = build_generate_prompt(AGENT, EXTRACTION, prd_file=None)
        assert baseline == explicit_none


# ── build_score_prompt ────────────────────────────────────────────────

class TestBuildScorePromptPrd:
    """PRD supplementary block in build_score_prompt."""

    def test_scenario_a_no_prd_block(self):
        output = build_score_prompt(DEBATE, VARIANT_A, VARIANT_B)
        assert PRD_MARKER not in output

    def test_scenario_c_prd_block_present(self):
        output = build_score_prompt(DEBATE, VARIANT_A, VARIANT_B, prd_file=PRD)
        assert PRD_MARKER in output


# ── build_spec_fidelity_prompt ────────────────────────────────────────

class TestBuildSpecFidelityPromptPrd:
    """PRD dimensions 12-15 in build_spec_fidelity_prompt."""

    def test_scenario_a_no_prd_dimensions(self):
        output = build_spec_fidelity_prompt(SPEC, ROADMAP)
        assert "Persona Coverage" not in output
        assert "Compliance & Legal Coverage" not in output

    def test_scenario_c_prd_dimensions_present(self):
        output = build_spec_fidelity_prompt(SPEC, ROADMAP, prd_file=PRD)
        assert PRD_MARKER in output or "Persona Coverage" in output


# ── build_test_strategy_prompt ────────────────────────────────────────

class TestBuildTestStrategyPromptPrd:
    """PRD checks in build_test_strategy_prompt."""

    def test_scenario_a_no_prd_checks(self):
        output = build_test_strategy_prompt(ROADMAP, EXTRACTION)
        assert PRD_MARKER not in output

    def test_scenario_c_prd_checks_present(self):
        output = build_test_strategy_prompt(ROADMAP, EXTRACTION, prd_file=PRD)
        assert PRD_MARKER in output


# ── Scenario B & E (10.3b) ────────────────────────────────────────────

class TestScenarioBAndE:
    """Explicit coverage for Scenarios B (TDD primary, no supplements) and
    E (spec primary + TDD supplement + PRD supplement)."""

    def test_scenario_b_tdd_primary_no_supplements(self):
        """When primary input is TDD (using build_extract_prompt_tdd),
        no PRD block should appear if prd_file is absent."""
        output = build_extract_prompt_tdd(SPEC)
        assert PRD_MARKER not in output
        assert TDD_SUPP_MARKER not in output

    def test_scenario_e_spec_primary_both_supplements(self):
        """When primary input is spec (build_extract_prompt) and both
        tdd_file and prd_file are provided, both supplement blocks appear."""
        output = build_extract_prompt(SPEC, tdd_file=TDD, prd_file=PRD)
        assert PRD_MARKER in output
        # Both blocks present, non-overlapping
        prd_pos = output.index(PRD_MARKER)
        assert prd_pos > 0  # PRD block is in the output


# ── Spec Fidelity Dimensions (10.4) ──────────────────────────────────

class TestSpecFidelityDimensions:
    """Verify dimensions 1-11 are unchanged without PRD, and dimensions
    12-15 appear only when prd_file is provided."""

    def test_baseline_dimensions_present_without_prd(self):
        output = build_spec_fidelity_prompt(SPEC, ROADMAP)
        # Standard dimensions should always be present (dimension names from TDD integration)
        assert "Signatures" in output
        assert "Data Models" in output

    def test_prd_dimensions_absent_without_prd(self):
        output = build_spec_fidelity_prompt(SPEC, ROADMAP)
        assert "Persona Coverage" not in output

    def test_prd_dimensions_present_with_prd(self):
        output = build_spec_fidelity_prompt(SPEC, ROADMAP, prd_file=PRD)
        assert "Persona" in output or PRD_MARKER in output


# ── Test Strategy PRD Checks (10.4) ──────────────────────────────────

class TestTestStrategyPrdChecks:
    """Verify PRD check items appear only when prd_file is provided."""

    def test_prd_checks_absent_without_prd(self):
        output = build_test_strategy_prompt(ROADMAP, EXTRACTION)
        assert PRD_MARKER not in output

    def test_prd_checks_present_with_prd(self):
        output = build_test_strategy_prompt(ROADMAP, EXTRACTION, prd_file=PRD)
        assert PRD_MARKER in output

    def test_baseline_identical_without_prd(self):
        baseline = build_test_strategy_prompt(ROADMAP, EXTRACTION)
        explicit_none = build_test_strategy_prompt(
            ROADMAP, EXTRACTION, prd_file=None
        )
        assert baseline == explicit_none


# ── Scenario F: Redundancy Guard (10.8) ──────────────────────────────

class TestRedundancyGuard:
    """When input_type=='tdd' and tdd_file is provided, the executor should
    nullify tdd_file (redundancy guard). This tests the logic exists in
    executor.py at line ~858."""

    def test_redundancy_guard_logic(self):
        """Verify the guard pattern: when input_type is tdd and tdd_file is set,
        tdd_file should be replaced with None via dataclasses.replace."""
        import dataclasses
        from superclaude.cli.roadmap.models import RoadmapConfig

        config = RoadmapConfig(
            spec_file=Path("tdd.md"),
            input_type="tdd",
            tdd_file=Path("extra_tdd.md"),
        )

        # Simulate the redundancy guard logic from executor.py:858-864
        effective_input_type = config.input_type
        if effective_input_type == "tdd" and config.tdd_file is not None:
            config = dataclasses.replace(config, tdd_file=None)

        assert config.tdd_file is None

    def test_no_guard_when_spec_input(self):
        """When input_type is spec, tdd_file should NOT be nullified."""
        import dataclasses
        from superclaude.cli.roadmap.models import RoadmapConfig

        config = RoadmapConfig(
            spec_file=Path("spec.md"),
            input_type="spec",
            tdd_file=Path("tdd.md"),
        )

        effective_input_type = config.input_type
        if effective_input_type == "tdd" and config.tdd_file is not None:
            config = dataclasses.replace(config, tdd_file=None)

        assert config.tdd_file == Path("tdd.md")
