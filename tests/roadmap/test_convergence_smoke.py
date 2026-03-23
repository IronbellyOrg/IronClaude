"""Smoke test for _run_convergence_spec_fidelity() executor path.

Verifies the executor helper completes without runtime exceptions when
invoked with a real RoadmapConfig, producing a valid StepResult and
writing a registry JSON file.
"""
from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

from superclaude.cli.pipeline.models import Step, StepResult, StepStatus
from superclaude.cli.roadmap.executor import _run_convergence_spec_fidelity
from superclaude.cli.roadmap.models import RoadmapConfig


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
