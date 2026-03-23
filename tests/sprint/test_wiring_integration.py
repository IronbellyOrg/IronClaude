"""Integration tests for TurnLedger threading through the sprint executor.

Verifies that TurnLedger, DeferredRemediationLog, and post-phase wiring
hooks are correctly constructed and threaded through execute_sprint and
execute_phase_tasks.
"""

from __future__ import annotations

import os
import time
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch, call

import pytest

from superclaude.cli.sprint.executor import (
    execute_phase_tasks,
    execute_sprint,
    run_post_phase_wiring_hook,
)
from superclaude.cli.sprint.models import (
    Phase,
    PhaseResult,
    PhaseStatus,
    SprintConfig,
    SprintOutcome,
    TaskEntry,
    TaskResult,
    TaskStatus,
    TurnLedger,
)
from superclaude.cli.pipeline.trailing_gate import DeferredRemediationLog


def _make_config(tmp_path: Path, num_phases: int = 2) -> SprintConfig:
    """Build a SprintConfig with wiring gates off for controlled testing."""
    phases = []
    for i in range(1, num_phases + 1):
        pf = tmp_path / f"phase-{i}-tasklist.md"
        pf.write_text(f"# Phase {i}\n")
        phases.append(Phase(number=i, file=pf, name=f"Phase {i}"))

    index = tmp_path / "tasklist-index.md"
    index.write_text("index\n")

    return SprintConfig(
        index_path=index,
        release_dir=tmp_path,
        phases=phases,
        start_phase=1,
        end_phase=num_phases,
        max_turns=5,
        wiring_gate_mode="off",
        wiring_gate_scope="none",
    )


def _make_tasks(count: int = 2) -> list[TaskEntry]:
    """Build a list of TaskEntry objects for testing."""
    return [
        TaskEntry(
            task_id=f"T01.{i:02d}",
            title=f"Task {i}",
            description=f"Description for task {i}",
        )
        for i in range(1, count + 1)
    ]


class TestExecuteSprintCreatesTurnledger:
    """Verify that execute_sprint constructs a TurnLedger during startup."""

    def test_execute_sprint_creates_turnledger(self, tmp_path):
        """TurnLedger is constructed inside execute_sprint and passed to
        execute_phase_tasks. We verify this by patching execute_phase_tasks
        and inspecting the ledger argument it receives."""
        config = _make_config(tmp_path, num_phases=1)
        config.results_dir.mkdir(parents=True, exist_ok=True)

        # Write task inventory so the per-task path is taken
        phase_file = config.phases[0].file
        phase_file.write_text(
            "# Phase 1\n\n### T01.01 -- Task One\nDo something\n"
        )

        captured_ledger = []

        def _capture_phase_tasks(tasks, config, phase, ledger=None, **kwargs):
            captured_ledger.append(ledger)
            # Return minimal results: all tasks pass, no remaining, no gate results
            results = [
                TaskResult(
                    task=t,
                    status=TaskStatus.PASS,
                    exit_code=0,
                    turns_consumed=1,
                )
                for t in tasks
            ]
            return results, [], []

        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.sprint.executor.execute_phase_tasks",
                side_effect=_capture_phase_tasks,
            ),
            patch(
                "superclaude.cli.sprint.executor.run_post_phase_wiring_hook",
                side_effect=lambda phase, config, pr, **kw: pr,
            ),
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.executor.SprintLogger"),
            patch(
                "superclaude.cli.sprint.preflight.execute_preflight_phases",
                return_value=[],
            ),
        ):
            execute_sprint(config)

        assert len(captured_ledger) == 1, (
            "execute_phase_tasks should have been called once for 1 phase"
        )
        ledger = captured_ledger[0]
        assert isinstance(ledger, TurnLedger), (
            f"Expected TurnLedger, got {type(ledger).__name__}"
        )
        assert ledger.initial_budget == config.max_turns * len(config.active_phases)
        assert ledger.consumed == 0, "Ledger should start with zero consumption"


class TestPostPhaseHookCalledPerPhase:
    """Verify run_post_phase_wiring_hook is called once per phase."""

    def test_post_phase_hook_called_per_phase(self, tmp_path):
        """With 2 phases, run_post_phase_wiring_hook must be called twice."""
        config = _make_config(tmp_path, num_phases=2)
        config.results_dir.mkdir(parents=True, exist_ok=True)

        # Write task inventory for both phases so per-task path is taken
        for phase in config.phases:
            phase.file.write_text(
                f"# Phase {phase.number}\n\n"
                f"### T{phase.number:02d}.01 -- Task One\nDo something\n"
            )

        def _stub_phase_tasks(tasks, config, phase, ledger=None, **kwargs):
            results = [
                TaskResult(
                    task=t,
                    status=TaskStatus.PASS,
                    exit_code=0,
                    turns_consumed=1,
                )
                for t in tasks
            ]
            return results, [], []

        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.sprint.executor.execute_phase_tasks",
                side_effect=_stub_phase_tasks,
            ),
            patch(
                "superclaude.cli.sprint.executor.run_post_phase_wiring_hook",
            ) as mock_hook,
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.executor.SprintLogger"),
            patch(
                "superclaude.cli.sprint.preflight.execute_preflight_phases",
                return_value=[],
            ),
        ):
            # The hook must return a PhaseResult; use side_effect to pass through
            mock_hook.side_effect = lambda phase, config, pr, **kw: pr
            execute_sprint(config)

        assert mock_hook.call_count == 2, (
            f"Expected 2 calls to run_post_phase_wiring_hook, got {mock_hook.call_count}"
        )
        # Verify each call received the correct phase number
        phase_numbers = [
            c.args[0].number for c in mock_hook.call_args_list
        ]
        assert phase_numbers == [1, 2], (
            f"Expected hook called for phases [1, 2], got {phase_numbers}"
        )


class TestTurnledgerBudgetDebitAcrossPhases:
    """Verify TurnLedger.consumed increases across execute_phase_tasks."""

    def test_turnledger_budget_debit_across_phases(self, tmp_path):
        """Run execute_phase_tasks with 2 tasks via _subprocess_factory.
        Each task consumes turns; verify ledger.consumed increased."""
        config = _make_config(tmp_path, num_phases=1)
        tasks = _make_tasks(count=2)
        phase = config.phases[0]

        ledger = TurnLedger(initial_budget=100)

        turns_per_task = 3

        def _factory(task, config, phase):
            # Return (exit_code=0, turns_consumed, output_bytes)
            return (0, turns_per_task, 256)

        results, remaining, gate_results = execute_phase_tasks(
            tasks=tasks,
            config=config,
            phase=phase,
            ledger=ledger,
            _subprocess_factory=_factory,
        )

        assert len(results) == 2, f"Expected 2 results, got {len(results)}"
        assert all(r.status == TaskStatus.PASS for r in results), (
            "All tasks should pass with exit_code=0"
        )
        assert len(remaining) == 0, "No tasks should be remaining"

        # Budget accounting: for each task, the executor pre-debits
        # minimum_allocation (5) via debit(), then reconciles.
        # Since actual(3) < pre_allocated(5), it credits back 2 per task.
        # consumed = 2 * 5 = 10 (two pre-debits of minimum_allocation)
        # reimbursed = 2 * (5-3) = 4 (two credits of the over-allocation)
        # available() = 100 - 10 + 4 = 94
        min_alloc = ledger.minimum_allocation  # 5
        num_tasks = 2
        expected_consumed = num_tasks * min_alloc  # 10
        expected_reimbursed = num_tasks * (min_alloc - turns_per_task)  # 4

        assert ledger.consumed == expected_consumed, (
            f"Expected consumed={expected_consumed}, got {ledger.consumed}"
        )
        assert ledger.reimbursed == expected_reimbursed, (
            f"Expected reimbursed={expected_reimbursed}, got {ledger.reimbursed}"
        )
        assert ledger.available() == 100 - expected_consumed + expected_reimbursed


class TestShadowFindingsLoggedToRemediationLog:
    """Verify shadow wiring mode logs findings to DeferredRemediationLog."""

    def test_shadow_findings_logged_to_remediation_log(self, tmp_path):
        """Configure shadow wiring mode, run a task through
        execute_phase_tasks, verify remediation_log receives entries."""
        config = _make_config(tmp_path, num_phases=1)
        # Override to shadow mode for this test
        object.__setattr__(config, "wiring_gate_mode", "shadow")
        object.__setattr__(config, "wiring_gate_scope", "none")

        tasks = _make_tasks(count=1)
        phase = config.phases[0]

        ledger = TurnLedger(initial_budget=100)
        remediation_log = DeferredRemediationLog(
            persist_path=tmp_path / "remediation.json",
        )

        def _factory(task, config, phase):
            return (0, 2, 128)

        # Mock the wiring analysis to return findings
        mock_report = MagicMock()
        mock_report.total_findings = 2
        mock_report.blocking_count.return_value = 0
        mock_report.scan_duration_seconds = 0.05

        # Create mock findings for shadow logging
        finding_1 = MagicMock()
        finding_1.finding_type = "missing-import"
        finding_1.detail = "Module X not imported"
        finding_1.severity = "minor"

        finding_2 = MagicMock()
        finding_2.finding_type = "unused-export"
        finding_2.detail = "Function Y exported but unused"
        finding_2.severity = "minor"

        mock_report.unsuppressed_findings = [finding_1, finding_2]

        with (
            patch(
                "superclaude.cli.audit.wiring_gate.run_wiring_analysis",
                return_value=mock_report,
            ),
            patch(
                "superclaude.cli.audit.wiring_config.WiringConfig",
            ),
        ):
            results, remaining, gate_results = execute_phase_tasks(
                tasks=tasks,
                config=config,
                phase=phase,
                ledger=ledger,
                _subprocess_factory=_factory,
                remediation_log=remediation_log,
            )

        assert len(results) == 1
        assert results[0].status == TaskStatus.PASS, (
            "Shadow mode must not change task status"
        )

        # Verify remediation_log received the shadow findings
        pending = remediation_log.pending_remediations()
        assert len(pending) == 2, (
            f"Expected 2 remediation entries from shadow findings, got {len(pending)}"
        )
        # Verify the entries contain shadow-prefixed failure reasons
        for entry in pending:
            assert "[shadow]" in entry.failure_reason, (
                f"Expected '[shadow]' prefix in failure_reason, got: {entry.failure_reason}"
            )
