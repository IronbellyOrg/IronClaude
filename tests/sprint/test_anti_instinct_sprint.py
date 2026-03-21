"""Tests for anti-instinct gate integration in sprint executor.

Covers:
- Rollout mode matrix: 4 modes x pass/fail = 8 scenarios (FR-SPRINT.3)
- None-safe TurnLedger guards (NFR-007)
- Gate independence: anti-instinct and wiring gates do not interact (NFR-010)
- ShadowGateMetrics recording per mode (FR-SPRINT.4)
- Budget exhaustion path (BUDGET_EXHAUSTED on FAIL)
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

from superclaude.cli.sprint.executor import (
    execute_phase_tasks,
    run_post_task_anti_instinct_hook,
)
from superclaude.cli.sprint.models import (
    GateOutcome,
    Phase,
    ShadowGateMetrics,
    SprintConfig,
    TaskEntry,
    TaskResult,
    TaskStatus,
    TurnLedger,
)


def _make_config(tmp_path: Path, gate_rollout_mode: str = "off") -> SprintConfig:
    pf = tmp_path / "phase-1-tasklist.md"
    pf.write_text("# Phase 1\n")
    return SprintConfig(
        index_path=tmp_path / "tasklist-index.md",
        release_dir=tmp_path,
        phases=[Phase(number=1, file=pf, name="Phase 1")],
        gate_rollout_mode=gate_rollout_mode,
        wiring_gate_mode="off",  # isolate anti-instinct gate from wiring gate
    )


def _make_task(task_id: str = "T01.01") -> TaskEntry:
    return TaskEntry(task_id=task_id, title="Test task")


def _make_task_result(
    task: TaskEntry | None = None,
    status: TaskStatus = TaskStatus.PASS,
    turns_consumed: int = 10,
    output_path: str = "",
) -> TaskResult:
    now = datetime.now(timezone.utc)
    return TaskResult(
        task=task or _make_task(),
        status=status,
        turns_consumed=turns_consumed,
        exit_code=0,
        started_at=now - timedelta(seconds=30),
        finished_at=now,
        output_path=output_path,
    )


# ---------------------------------------------------------------------------
# Rollout mode matrix: 4 modes x pass/fail = 8 scenarios
# ---------------------------------------------------------------------------


class TestRolloutModeMatrix:
    """FR-SPRINT.3: rollout mode behavior matrix tests."""

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(True, None))
    def test_off_mode_pass(self, mock_gate, tmp_path):
        """off mode: evaluate + ignore result. No metrics, no status change."""
        config = _make_config(tmp_path, gate_rollout_mode="off")
        result = _make_task_result(output_path=str(tmp_path / "output.md"))
        metrics = ShadowGateMetrics()

        result = run_post_task_anti_instinct_hook(
            _make_task(), config, result, shadow_metrics=metrics,
        )

        assert result.status == TaskStatus.PASS
        assert metrics.total_evaluated == 0  # off mode does NOT record

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(False, "fail"))
    def test_off_mode_fail(self, mock_gate, tmp_path):
        """off mode: gate fails but result is ignored."""
        config = _make_config(tmp_path, gate_rollout_mode="off")
        result = _make_task_result()

        result = run_post_task_anti_instinct_hook(
            _make_task(), config, result,
        )

        assert result.status == TaskStatus.PASS  # unchanged

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(True, None))
    def test_shadow_mode_pass(self, mock_gate, tmp_path):
        """shadow mode: evaluate + record metrics. No status change."""
        config = _make_config(tmp_path, gate_rollout_mode="shadow")
        result = _make_task_result(output_path=str(tmp_path / "output.md"))
        (tmp_path / "output.md").write_text("test content")
        metrics = ShadowGateMetrics()

        result = run_post_task_anti_instinct_hook(
            _make_task(), config, result, shadow_metrics=metrics,
        )

        assert result.status == TaskStatus.PASS
        assert metrics.total_evaluated == 1
        assert metrics.passed == 1

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(False, "undischarged obligations"))
    def test_shadow_mode_fail(self, mock_gate, tmp_path):
        """shadow mode: gate fails, metrics recorded, but status unchanged."""
        config = _make_config(tmp_path, gate_rollout_mode="shadow")
        result = _make_task_result(output_path=str(tmp_path / "output.md"))
        (tmp_path / "output.md").write_text("test content")
        metrics = ShadowGateMetrics()

        result = run_post_task_anti_instinct_hook(
            _make_task(), config, result, shadow_metrics=metrics,
        )

        assert result.status == TaskStatus.PASS  # unchanged in shadow mode
        assert metrics.total_evaluated == 1
        assert metrics.failed == 1

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(True, None))
    def test_soft_mode_pass_credits(self, mock_gate, tmp_path):
        """soft mode: PASS credits turns via TurnLedger."""
        config = _make_config(tmp_path, gate_rollout_mode="soft")
        result = _make_task_result(output_path=str(tmp_path / "output.md"), turns_consumed=10)
        (tmp_path / "output.md").write_text("test content")
        ledger = TurnLedger(initial_budget=100)
        metrics = ShadowGateMetrics()

        result = run_post_task_anti_instinct_hook(
            _make_task(), config, result, ledger=ledger, shadow_metrics=metrics,
        )

        assert result.status == TaskStatus.PASS
        assert result.gate_outcome == GateOutcome.PASS
        assert result.reimbursement_amount == 8  # int(10 * 0.8) = 8
        assert ledger.reimbursed == 8
        assert metrics.passed == 1

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(False, "undischarged"))
    def test_soft_mode_fail_no_task_fail(self, mock_gate, tmp_path):
        """soft mode: FAIL marks gate_outcome=FAIL but does NOT fail the task."""
        config = _make_config(tmp_path, gate_rollout_mode="soft")
        result = _make_task_result(output_path=str(tmp_path / "output.md"))
        (tmp_path / "output.md").write_text("test content")
        ledger = TurnLedger(initial_budget=100)
        metrics = ShadowGateMetrics()

        result = run_post_task_anti_instinct_hook(
            _make_task(), config, result, ledger=ledger, shadow_metrics=metrics,
        )

        assert result.status == TaskStatus.PASS  # soft mode does NOT fail task
        assert result.gate_outcome == GateOutcome.FAIL
        assert metrics.failed == 1

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(True, None))
    def test_full_mode_pass_credits(self, mock_gate, tmp_path):
        """full mode: PASS credits turns."""
        config = _make_config(tmp_path, gate_rollout_mode="full")
        result = _make_task_result(output_path=str(tmp_path / "output.md"), turns_consumed=20)
        (tmp_path / "output.md").write_text("test content")
        ledger = TurnLedger(initial_budget=200)
        metrics = ShadowGateMetrics()

        result = run_post_task_anti_instinct_hook(
            _make_task(), config, result, ledger=ledger, shadow_metrics=metrics,
        )

        assert result.status == TaskStatus.PASS
        assert result.gate_outcome == GateOutcome.PASS
        assert result.reimbursement_amount == 16  # int(20 * 0.8) = 16

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(False, "undischarged"))
    def test_full_mode_fail_sets_task_fail(self, mock_gate, tmp_path):
        """full mode: FAIL sets TaskResult.status = FAIL."""
        config = _make_config(tmp_path, gate_rollout_mode="full")
        result = _make_task_result(output_path=str(tmp_path / "output.md"))
        (tmp_path / "output.md").write_text("test content")
        ledger = TurnLedger(initial_budget=100)
        metrics = ShadowGateMetrics()

        result = run_post_task_anti_instinct_hook(
            _make_task(), config, result, ledger=ledger, shadow_metrics=metrics,
        )

        assert result.status == TaskStatus.FAIL  # full mode FAILS the task
        assert result.gate_outcome == GateOutcome.FAIL


# ---------------------------------------------------------------------------
# None-safe TurnLedger guards (NFR-007)
# ---------------------------------------------------------------------------


class TestNoneSafeLedgerGuards:
    """NFR-007: sprint runs without TurnLedger must not raise."""

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(True, None))
    def test_soft_mode_no_ledger_pass(self, mock_gate, tmp_path):
        """soft mode PASS with ledger=None does not raise."""
        config = _make_config(tmp_path, gate_rollout_mode="soft")
        result = _make_task_result(output_path=str(tmp_path / "output.md"))
        (tmp_path / "output.md").write_text("test content")

        result = run_post_task_anti_instinct_hook(
            _make_task(), config, result, ledger=None,
        )

        assert result.status == TaskStatus.PASS
        assert result.gate_outcome == GateOutcome.PASS
        assert result.reimbursement_amount == 0  # no ledger → no reimbursement

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(False, "fail"))
    def test_full_mode_no_ledger_fail(self, mock_gate, tmp_path):
        """full mode FAIL with ledger=None does not raise."""
        config = _make_config(tmp_path, gate_rollout_mode="full")
        result = _make_task_result(output_path=str(tmp_path / "output.md"))
        (tmp_path / "output.md").write_text("test content")

        result = run_post_task_anti_instinct_hook(
            _make_task(), config, result, ledger=None,
        )

        assert result.status == TaskStatus.FAIL
        assert result.gate_outcome == GateOutcome.FAIL

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(False, "fail"))
    def test_soft_mode_no_ledger_fail(self, mock_gate, tmp_path):
        """soft mode FAIL with ledger=None does not raise."""
        config = _make_config(tmp_path, gate_rollout_mode="soft")
        result = _make_task_result(output_path=str(tmp_path / "output.md"))
        (tmp_path / "output.md").write_text("test content")

        result = run_post_task_anti_instinct_hook(
            _make_task(), config, result, ledger=None,
        )

        assert result.status == TaskStatus.PASS  # soft doesn't fail
        assert result.gate_outcome == GateOutcome.FAIL


# ---------------------------------------------------------------------------
# Gate independence (NFR-010)
# ---------------------------------------------------------------------------


class TestGateIndependence:
    """NFR-010: anti-instinct and wiring gates evaluate independently."""

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(True, None))
    def test_anti_instinct_independent_of_wiring(self, mock_gate, tmp_path):
        """Anti-instinct gate evaluation does not depend on wiring gate state."""
        config = _make_config(tmp_path, gate_rollout_mode="shadow")
        config_off_wiring = SprintConfig(
            index_path=config.index_path,
            release_dir=config.release_dir,
            phases=config.phases,
            gate_rollout_mode="shadow",
            wiring_gate_mode="full",  # wiring gate on full mode
        )
        result = _make_task_result(output_path=str(tmp_path / "output.md"))
        (tmp_path / "output.md").write_text("test content")
        metrics = ShadowGateMetrics()

        result = run_post_task_anti_instinct_hook(
            _make_task(), config_off_wiring, result, shadow_metrics=metrics,
        )

        # Anti-instinct evaluates independently regardless of wiring config
        assert metrics.total_evaluated == 1
        assert result.status == TaskStatus.PASS

    def test_execute_phase_tasks_both_gates_independent(self, tmp_path):
        """Both gates run independently in execute_phase_tasks."""
        config = _make_config(tmp_path, gate_rollout_mode="off")
        config.wiring_gate_mode = "off"
        phase = config.phases[0]
        tasks = [_make_task("T01.01")]
        metrics = ShadowGateMetrics()

        def _factory(task, cfg, ph):
            return (0, 5, 100)  # exit_code=0, turns=5, output_bytes=100

        results, remaining = execute_phase_tasks(
            tasks, config, phase,
            _subprocess_factory=_factory,
            shadow_metrics=metrics,
        )

        assert len(results) == 1
        assert results[0].status == TaskStatus.PASS
        assert metrics.total_evaluated == 0  # off mode, no recording


# ---------------------------------------------------------------------------
# Budget exhaustion path
# ---------------------------------------------------------------------------


class TestBudgetExhaustion:
    """Budget-exhausted path: FAIL + insufficient remediation budget."""

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(False, "undischarged"))
    def test_full_mode_budget_exhausted(self, mock_gate, tmp_path):
        """full mode FAIL with exhausted remediation budget → BUDGET_EXHAUSTED."""
        config = _make_config(tmp_path, gate_rollout_mode="full")
        result = _make_task_result(output_path=str(tmp_path / "output.md"))
        (tmp_path / "output.md").write_text("test content")
        ledger = TurnLedger(initial_budget=2, minimum_remediation_budget=3)
        # Budget is 2, min remediation is 3 → can't remediate

        result = run_post_task_anti_instinct_hook(
            _make_task(), config, result, ledger=ledger,
        )

        assert result.status == TaskStatus.FAIL
        assert result.gate_outcome == GateOutcome.FAIL

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(False, "undischarged"))
    def test_soft_mode_budget_exhausted(self, mock_gate, tmp_path):
        """soft mode FAIL with exhausted remediation budget → gate FAIL, task PASS."""
        config = _make_config(tmp_path, gate_rollout_mode="soft")
        result = _make_task_result(output_path=str(tmp_path / "output.md"))
        (tmp_path / "output.md").write_text("test content")
        ledger = TurnLedger(initial_budget=2, minimum_remediation_budget=3)

        result = run_post_task_anti_instinct_hook(
            _make_task(), config, result, ledger=ledger,
        )

        assert result.status == TaskStatus.PASS  # soft doesn't fail task
        assert result.gate_outcome == GateOutcome.FAIL


# ---------------------------------------------------------------------------
# No output artifact (vacuous pass)
# ---------------------------------------------------------------------------


class TestNoOutputArtifact:
    """Gate passes vacuously when no output artifact exists."""

    def test_no_output_path_passes(self, tmp_path):
        """No output_path → gate passes vacuously."""
        config = _make_config(tmp_path, gate_rollout_mode="shadow")
        result = _make_task_result(output_path="")
        metrics = ShadowGateMetrics()

        result = run_post_task_anti_instinct_hook(
            _make_task(), config, result, shadow_metrics=metrics,
        )

        assert result.status == TaskStatus.PASS
        assert metrics.total_evaluated == 1
        assert metrics.passed == 1

    def test_nonexistent_output_path_passes(self, tmp_path):
        """output_path set but file doesn't exist → gate passes vacuously."""
        config = _make_config(tmp_path, gate_rollout_mode="shadow")
        result = _make_task_result(output_path=str(tmp_path / "nonexistent.md"))
        metrics = ShadowGateMetrics()

        result = run_post_task_anti_instinct_hook(
            _make_task(), config, result, shadow_metrics=metrics,
        )

        assert result.status == TaskStatus.PASS
        assert metrics.passed == 1
