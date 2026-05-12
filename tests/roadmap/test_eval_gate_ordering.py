"""P1 Eval: Gate Ordering Invariants.

Tests that _build_steps() produces correct step ordering with correct
input dependencies, and that gate N's output is referenced by downstream steps.

NEW eval identified during adversarial debate — structural pipeline property
with zero existing coverage.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.roadmap.executor import _build_steps
from superclaude.cli.roadmap.models import AgentSpec, RoadmapConfig
from superclaude.cli.pipeline.models import Step


def _make_config(tmp_path: Path) -> RoadmapConfig:
    spec = tmp_path / "spec.md"
    spec.write_text("# Test Spec\n\nRequirements here.\n")
    # These tests verify structural step dependencies (each step references
    # prior-step outputs). Compression routing is a separate concern covered
    # by dedicated tests, so disable it here.
    return RoadmapConfig(
        spec_file=spec,
        output_dir=tmp_path / "output",
        agents=[AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")],
        compress_enabled=False,
    )


def _flatten_steps(steps: list) -> list[Step]:
    """Flatten parallel groups into sequential list."""
    flat = []
    for item in steps:
        if isinstance(item, list):
            flat.extend(item)
        else:
            flat.append(item)
    return flat


def _get_step_ids(steps: list) -> list[str]:
    """Get ordered step IDs, preserving parallel groups as sublists."""
    ids = []
    for item in steps:
        if isinstance(item, list):
            ids.extend(s.id for s in item)
        else:
            ids.append(item.id)
    return ids


class TestStepOrdering:
    """Verify pipeline step ordering invariants."""

    def test_step_count(self, tmp_path):
        """Pipeline produces exactly 13 steps (12 entries; parallel pair counts as 2).
        certify is dynamic, not in static step list; _get_all_step_ids has 14.
        """
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = _flatten_steps(steps)
        assert len(flat) == 13  # extract + 2 generate + diff + debate + score + merge + anti-instinct + test-strategy + spec-fidelity + wiring + deviation-analysis + remediate

    def test_extract_is_first(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        assert isinstance(steps[0], Step)
        assert steps[0].id == "extract"

    def test_generate_pair_is_parallel(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        assert isinstance(steps[1], list), "Generate steps should be a parallel group"
        assert len(steps[1]) == 2
        gen_ids = {s.id for s in steps[1]}
        assert "generate-opus-architect" in gen_ids
        assert "generate-haiku-architect" in gen_ids

    def test_sequential_order_after_generate(self, tmp_path):
        """Steps after generate must follow correct order including new post-fidelity steps."""
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        sequential = [s for s in steps[2:] if isinstance(s, Step)]
        seq_ids = [s.id for s in sequential]
        expected_order = ["diff", "debate", "score", "merge", "anti-instinct", "test-strategy", "spec-fidelity", "wiring-verification", "deviation-analysis", "remediate"]
        assert seq_ids == expected_order

    def test_spec_fidelity_after_test_strategy(self, tmp_path):
        """spec-fidelity must come after test-strategy (FR-008)."""
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = _flatten_steps(steps)
        ids = [s.id for s in flat]
        ts_idx = ids.index("test-strategy")
        sf_idx = ids.index("spec-fidelity")
        assert sf_idx > ts_idx

    def test_wiring_after_spec_fidelity(self, tmp_path):
        """wiring-verification must come after spec-fidelity."""
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = _flatten_steps(steps)
        ids = [s.id for s in flat]
        sf_idx = ids.index("spec-fidelity")
        wv_idx = ids.index("wiring-verification")
        assert wv_idx > sf_idx


class TestInputDependencies:
    """Verify each step's inputs reference outputs of prior steps."""

    def test_extract_inputs_spec(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        extract = steps[0]
        assert config.spec_file in extract.inputs

    def test_generate_inputs_extraction(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        extract = steps[0]
        gen_group = steps[1]
        for gen_step in gen_group:
            assert extract.output_file in gen_step.inputs

    def test_diff_inputs_both_roadmaps(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        gen_group = steps[1]
        diff = steps[2]
        for gen_step in gen_group:
            assert gen_step.output_file in diff.inputs

    def test_debate_inputs_diff_and_roadmaps(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        diff = steps[2]
        debate = steps[3]
        assert diff.output_file in debate.inputs
        gen_group = steps[1]
        for gen_step in gen_group:
            assert gen_step.output_file in debate.inputs

    def test_merge_inputs_score_and_roadmaps(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        score = steps[4]
        merge = steps[5]
        assert score.output_file in merge.inputs

    def test_spec_fidelity_inputs_spec_and_merge(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = _flatten_steps(steps)
        merge = next(s for s in flat if s.id == "merge")
        sf = next(s for s in flat if s.id == "spec-fidelity")
        assert config.spec_file in sf.inputs
        assert merge.output_file in sf.inputs

    def test_wiring_inputs_merge_and_fidelity(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = _flatten_steps(steps)
        merge = next(s for s in flat if s.id == "merge")
        sf = next(s for s in flat if s.id == "spec-fidelity")
        wv = next(s for s in flat if s.id == "wiring-verification")
        assert merge.output_file in wv.inputs
        assert sf.output_file in wv.inputs


class TestGateAssignment:
    """Verify each step has the correct gate assigned."""

    def test_all_steps_have_gates(self, tmp_path):
        """Every step should have a gate (or None for convergence-mode spec-fidelity)."""
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = _flatten_steps(steps)
        for step in flat:
            if step.id == "spec-fidelity" and config.convergence_enabled:
                assert step.gate is None
            else:
                assert step.gate is not None, f"Step '{step.id}' has no gate"

    def test_convergence_mode_disables_fidelity_gate(self, tmp_path):
        """When convergence_enabled=True, spec-fidelity gate is None."""
        config = _make_config(tmp_path)
        config.convergence_enabled = True
        steps = _build_steps(config)
        flat = _flatten_steps(steps)
        sf = next(s for s in flat if s.id == "spec-fidelity")
        assert sf.gate is None

    def test_all_strict_gates_have_semantic_checks(self, tmp_path):
        """All STRICT-tier gates should define semantic checks."""
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = _flatten_steps(steps)
        for step in flat:
            if step.gate and step.gate.enforcement_tier == "STRICT":
                assert step.gate.semantic_checks, (
                    f"STRICT gate on step '{step.id}' has no semantic checks"
                )


class TestModelRouting:
    """Generate steps use the correct model from agent specs."""

    def test_model_assigned_to_generate_steps(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        gen_group = steps[1]
        models = {s.model for s in gen_group}
        assert "opus" in models
        assert "haiku" in models

    def test_single_agent_both_generate(self, tmp_path):
        """Single agent produces both generate steps with same model."""
        config = _make_config(tmp_path)
        config.agents = [AgentSpec("opus", "architect")]
        steps = _build_steps(config)
        gen_group = steps[1]
        assert all(s.model == "opus" for s in gen_group)


class TestStepMetadata:
    """Verify step metadata (timeouts, retry limits) are reasonable."""

    def test_timeouts_positive(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = _flatten_steps(steps)
        for step in flat:
            assert step.timeout_seconds > 0, f"Step '{step.id}' has non-positive timeout"

    def test_wiring_has_trailing_gate_mode(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = _flatten_steps(steps)
        wv = next(s for s in flat if s.id == "wiring-verification")
        from superclaude.cli.pipeline.models import GateMode
        assert wv.gate_mode == GateMode.TRAILING

    def test_wiring_zero_retries(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = _flatten_steps(steps)
        wv = next(s for s in flat if s.id == "wiring-verification")
        assert wv.retry_limit == 0

    def test_output_files_unique(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = _flatten_steps(steps)
        outputs = [str(s.output_file) for s in flat]
        assert len(outputs) == len(set(outputs)), "Duplicate output files detected"

    def test_new_steps_blocking_gate_mode(self, tmp_path):
        """deviation-analysis and remediate use BLOCKING gate mode (enforcement promoted)."""
        from superclaude.cli.pipeline.models import GateMode
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = _flatten_steps(steps)
        da = next(s for s in flat if s.id == "deviation-analysis")
        rem = next(s for s in flat if s.id == "remediate")
        assert da.gate_mode == GateMode.BLOCKING
        assert rem.gate_mode == GateMode.BLOCKING


class TestNewStepOrdering:
    """Verify ordering of newly wired post-fidelity steps."""

    def test_deviation_analysis_after_wiring(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = _flatten_steps(steps)
        ids = [s.id for s in flat]
        wv_idx = ids.index("wiring-verification")
        da_idx = ids.index("deviation-analysis")
        assert da_idx > wv_idx

    def test_remediate_after_deviation_analysis(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = _flatten_steps(steps)
        ids = [s.id for s in flat]
        da_idx = ids.index("deviation-analysis")
        rem_idx = ids.index("remediate")
        assert rem_idx > da_idx


class TestNewStepInputDependencies:
    """Verify input dependencies for newly wired steps."""

    def test_deviation_analysis_inputs_fidelity_and_merge(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = _flatten_steps(steps)
        da = next(s for s in flat if s.id == "deviation-analysis")
        sf = next(s for s in flat if s.id == "spec-fidelity")
        merge = next(s for s in flat if s.id == "merge")
        assert sf.output_file in da.inputs
        assert merge.output_file in da.inputs

    def test_remediate_inputs_deviation_fidelity_merge(self, tmp_path):
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = _flatten_steps(steps)
        da = next(s for s in flat if s.id == "deviation-analysis")
        sf = next(s for s in flat if s.id == "spec-fidelity")
        merge = next(s for s in flat if s.id == "merge")
        rem = next(s for s in flat if s.id == "remediate")
        assert da.output_file in rem.inputs
        assert sf.output_file in rem.inputs
        assert merge.output_file in rem.inputs
