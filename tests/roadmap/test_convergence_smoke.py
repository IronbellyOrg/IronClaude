"""Smoke tests for convergence paths.

1. _run_convergence_spec_fidelity() executor path — verifies the executor
   helper completes without runtime exceptions, producing a valid StepResult.
2. execute_fidelity_with_convergence() loop — verifies the convergence loop
   completes without crash and returns a valid ConvergenceResult (T02.26).
"""
from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

from superclaude.cli.pipeline.models import Step, StepResult, StepStatus
from superclaude.cli.roadmap.convergence import (
    ConvergenceResult,
    DeviationRegistry,
    execute_fidelity_with_convergence,
    CHECKER_COST,
    MAX_CONVERGENCE_BUDGET,
    REMEDIATION_COST,
)
from superclaude.cli.roadmap.executor import _run_convergence_spec_fidelity
from superclaude.cli.roadmap.models import RoadmapConfig
from superclaude.cli.sprint.models import TurnLedger


def _make_config(tmp_path: Path) -> RoadmapConfig:
    """Create a minimal RoadmapConfig with spec and output dir."""
    spec = tmp_path / "spec.md"
    spec.write_text("# Test Spec\nFR-1: Must have feature X\n")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    roadmap = output_dir / "roadmap.md"
    roadmap.write_text("# Roadmap\n## Feature X\nImplement FR-1\n")
    return RoadmapConfig(
        spec_file=spec,
        output_dir=output_dir,
    )


def _make_step(tmp_path: Path) -> Step:
    """Create a minimal Step for spec-fidelity."""
    return Step(
        id="step-8",
        prompt="spec fidelity",
        output_file=tmp_path / "output" / "spec-fidelity.md",
        gate=None,
        timeout_seconds=60,
    )


@pytest.mark.integration
class TestConvergenceSmoke:
    """Smoke tests for _run_convergence_spec_fidelity() executor path."""

    def test_smoke_no_runtime_exceptions(self, tmp_path):
        """_run_convergence_spec_fidelity() completes without TypeError/AttributeError."""
        config = _make_config(tmp_path)
        step = _make_step(tmp_path)
        started_at = datetime.now(timezone.utc)

        # Mock structural_checkers and semantic_layer to avoid Claude calls
        with (
            patch(
                "superclaude.cli.roadmap.structural_checkers.run_all_checkers",
                return_value=[],
            ),
            patch(
                "superclaude.cli.roadmap.semantic_layer.run_semantic_layer",
                return_value=None,
            ),
            patch(
                "superclaude.cli.roadmap.remediate_executor.execute_remediation",
            ),
        ):
            result = _run_convergence_spec_fidelity(step, config, started_at)

        assert isinstance(result, StepResult)
        assert result.step == step
        assert result.started_at == started_at
        assert result.finished_at is not None
        assert result.finished_at >= started_at

    def test_smoke_returns_valid_step_result(self, tmp_path):
        """StepResult has PASS status when checkers find 0 HIGHs."""
        config = _make_config(tmp_path)
        step = _make_step(tmp_path)
        started_at = datetime.now(timezone.utc)

        with (
            patch(
                "superclaude.cli.roadmap.structural_checkers.run_all_checkers",
                return_value=[],
            ),
            patch(
                "superclaude.cli.roadmap.semantic_layer.run_semantic_layer",
                return_value=None,
            ),
            patch(
                "superclaude.cli.roadmap.remediate_executor.execute_remediation",
            ),
        ):
            result = _run_convergence_spec_fidelity(step, config, started_at)

        assert result.status == StepStatus.PASS
        assert result.gate_failure_reason is None

    def test_smoke_output_file_written(self, tmp_path):
        """spec-fidelity output file is written to output_dir."""
        config = _make_config(tmp_path)
        step = _make_step(tmp_path)
        started_at = datetime.now(timezone.utc)

        with (
            patch(
                "superclaude.cli.roadmap.structural_checkers.run_all_checkers",
                return_value=[],
            ),
            patch(
                "superclaude.cli.roadmap.semantic_layer.run_semantic_layer",
                return_value=None,
            ),
            patch(
                "superclaude.cli.roadmap.remediate_executor.execute_remediation",
            ),
        ):
            _run_convergence_spec_fidelity(step, config, started_at)

        assert step.output_file.exists(), (
            f"Expected spec-fidelity output at {step.output_file}"
        )


@pytest.mark.integration
class TestConvergenceLoopSmoke:
    """Smoke tests for execute_fidelity_with_convergence() loop (T02.26, R-035).

    Minimal invocation of the convergence loop to verify it completes
    without crash and produces a valid ConvergenceResult.
    """

    def test_loop_no_crash_clean_checkers(self, tmp_path: Path, audit_trail):
        """execute_fidelity_with_convergence() returns ConvergenceResult with 0 HIGHs."""
        reg_path = tmp_path / "registry.json"
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap\n## Feature X\nImplement FR-1\n")

        reg = DeviationRegistry(
            path=reg_path, release_id="smoke-1", spec_hash="smoke-hash",
        )
        ledger = TurnLedger(
            initial_budget=MAX_CONVERGENCE_BUDGET,
            minimum_allocation=CHECKER_COST,
            minimum_remediation_budget=REMEDIATION_COST,
        )

        def noop_checkers(registry, run_number):
            registry.merge_findings([], [], run_number=run_number)

        def noop_remediation(registry):
            pass

        result = execute_fidelity_with_convergence(
            registry=reg,
            ledger=ledger,
            run_checkers=noop_checkers,
            run_remediation=noop_remediation,
            max_runs=1,
            roadmap_path=roadmap,
        )

        assert isinstance(result, ConvergenceResult)
        assert result.passed is True
        assert result.run_count == 1
        assert result.final_high_count == 0
        assert result.regression_detected is False

        audit_trail.record(
            test_id="test_loop_no_crash_clean_checkers",
            spec_ref="R-035,FR-6.1-T12",
            assertion_type="behavioral",
            inputs={"max_runs": 1, "findings": 0},
            observed={
                "type": type(result).__name__,
                "passed": result.passed,
                "run_count": result.run_count,
                "final_high_count": result.final_high_count,
                "regression_detected": result.regression_detected,
            },
            expected={
                "type": "ConvergenceResult",
                "passed": True,
                "run_count": 1,
                "final_high_count": 0,
                "regression_detected": False,
            },
            verdict="PASS",
            evidence="Convergence loop smoke: completes without crash, returns valid ConvergenceResult (T02.26)",
        )

    def test_loop_registry_saveable(self, tmp_path: Path, audit_trail):
        """Registry is saveable after convergence loop; runs list is populated."""
        reg_path = tmp_path / "registry.json"
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap")

        reg = DeviationRegistry(
            path=reg_path, release_id="smoke-2", spec_hash="smoke-hash-2",
        )
        ledger = TurnLedger(
            initial_budget=MAX_CONVERGENCE_BUDGET,
            minimum_allocation=CHECKER_COST,
            minimum_remediation_budget=REMEDIATION_COST,
        )

        def noop_checkers(registry, run_number):
            registry.merge_findings([], [], run_number=run_number)

        def noop_remediation(registry):
            pass

        execute_fidelity_with_convergence(
            registry=reg,
            ledger=ledger,
            run_checkers=noop_checkers,
            run_remediation=noop_remediation,
            max_runs=1,
            roadmap_path=roadmap,
        )

        # Registry should have run metadata populated
        assert len(reg.runs) >= 1
        # Save should succeed without error
        reg.save()
        assert reg_path.exists(), f"Registry not persisted at {reg_path}"

        audit_trail.record(
            test_id="test_loop_registry_saveable",
            spec_ref="R-035,FR-6.1-T12",
            assertion_type="structural",
            inputs={"registry_path": str(reg_path)},
            observed={
                "runs_count": len(reg.runs),
                "registry_exists_after_save": reg_path.exists(),
            },
            expected={
                "runs_count_gte_1": True,
                "registry_exists_after_save": True,
            },
            verdict="PASS",
            evidence="Convergence loop smoke: registry saveable with run metadata after loop (T02.26)",
        )
