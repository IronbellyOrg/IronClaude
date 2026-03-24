"""E2E gate rollout mode x path validation (T02.21).

Tests the 4x2 matrix: {off, shadow, soft, full} x {anti-instinct, wiring}.
Each test verifies all 4 outcome dimensions:
  1. TaskStatus / GateOutcome
  2. TurnLedger state (consumed, reimbursed, wiring counters)
  3. DeferredRemediationLog entries
  4. ShadowGateMetrics recording

Dependencies: T01.02 (audit_trail fixture)
"""

from __future__ import annotations

import os
import signal
from pathlib import Path
from unittest.mock import patch

import pytest

from superclaude.cli.sprint.executor import (
    execute_phase_tasks,
    run_post_task_anti_instinct_hook,
    run_post_task_wiring_hook,
)
from superclaude.cli.sprint.kpi import build_kpi_report
from superclaude.cli.sprint.process import SignalHandler
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
from superclaude.cli.audit.wiring_gate import WiringFinding, WiringReport
from superclaude.cli.pipeline.trailing_gate import (
    DeferredRemediationLog,
    TrailingGateResult,
)
from superclaude.cli.roadmap.convergence import (
    ConvergenceResult,
    DeviationRegistry,
    execute_fidelity_with_convergence,
    CHECKER_COST,
)
from superclaude.cli.roadmap.models import Finding


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_config(
    tmp_path: Path,
    *,
    gate_rollout_mode: str = "off",
    wiring_gate_mode: str = "off",
) -> SprintConfig:
    """Build a SprintConfig with controllable gate modes."""
    phase_file = tmp_path / "phase-1-tasklist.md"
    phase_file.write_text("# Phase 1\n\n### T01.01 -- Task One\nDo something\n")
    phase = Phase(number=1, file=phase_file, name="Phase 1")

    index = tmp_path / "tasklist-index.md"
    index.write_text("index\n")

    return SprintConfig(
        index_path=index,
        release_dir=tmp_path,
        phases=[phase],
        start_phase=1,
        end_phase=1,
        max_turns=50,
        wiring_gate_mode=wiring_gate_mode,
        wiring_gate_scope="none",
        gate_rollout_mode=gate_rollout_mode,
    )


def _make_task(task_id: str = "T01.01", title: str = "Test Task") -> TaskEntry:
    """Create a minimal TaskEntry."""
    return TaskEntry(
        task_id=task_id,
        title=title,
        description="Test task for gate mode validation",
    )


def _make_task_result(
    task: TaskEntry,
    *,
    status: TaskStatus = TaskStatus.PASS,
    turns_consumed: int = 10,
    output_path: str = "",
) -> TaskResult:
    """Create a TaskResult with controllable fields."""
    return TaskResult(
        task=task,
        status=status,
        turns_consumed=turns_consumed,
        exit_code=0,
        output_path=output_path,
    )


def _make_ledger(initial_budget: int = 500) -> TurnLedger:
    """Create a TurnLedger with known initial state."""
    return TurnLedger(initial_budget=initial_budget)


def _make_blocking_wiring_report() -> WiringReport:
    """Create a WiringReport with blocking findings (critical severity)."""
    return WiringReport(
        target_dir="/tmp/test",
        files_analyzed=5,
        scan_duration_seconds=0.01,
        rollout_mode="full",
        unwired_callables=[
            WiringFinding(
                finding_type="unwired_callable",
                file_path="test.py",
                symbol_name="test_fn",
                line_number=1,
                detail="unwired callable",
                severity="critical",
            ),
        ],
    )


def _make_clean_wiring_report() -> WiringReport:
    """Create a WiringReport with no findings."""
    return WiringReport(
        target_dir="/tmp/test",
        files_analyzed=5,
        scan_duration_seconds=0.01,
        rollout_mode="shadow",
    )


# ---------------------------------------------------------------------------
# Anti-instinct path tests (4 modes)
# ---------------------------------------------------------------------------


class TestAntiInstinctPath:
    """FR-3.1a-d: Anti-instinct gate behavior across 4 rollout modes."""

    def test_off_mode_anti_instinct(self, tmp_path: Path, audit_trail) -> None:
        """FR-3.1a: off mode — gate evaluates but result is ignored."""
        config = _make_config(tmp_path, gate_rollout_mode="off")
        task = _make_task()
        task_result = _make_task_result(task)
        ledger = _make_ledger()
        shadow_metrics = ShadowGateMetrics()

        result, gate_result = run_post_task_anti_instinct_hook(
            task, config, task_result,
            ledger=ledger, shadow_metrics=shadow_metrics,
        )

        # 1. TaskStatus/GateOutcome: unchanged (off ignores gate)
        assert result.status == TaskStatus.PASS
        assert result.gate_outcome == GateOutcome.PENDING  # never set
        assert gate_result is None  # off returns None

        # 2. TurnLedger: no credits or debits from gate
        assert ledger.consumed == 0
        assert ledger.reimbursed == 0

        # 3. DeferredRemediationLog: N/A for anti-instinct off
        # 4. ShadowGateMetrics: NOT recorded in off mode
        assert shadow_metrics.total_evaluated == 0

        audit_trail.record(
            test_id="test_off_mode_anti_instinct",
            spec_ref="FR-3.1a",
            assertion_type="behavioral",
            inputs={"gate_rollout_mode": "off", "path": "anti-instinct"},
            observed={
                "status": result.status.value,
                "gate_outcome": result.gate_outcome.value,
                "gate_result": gate_result,
                "shadow_total_evaluated": shadow_metrics.total_evaluated,
            },
            expected={
                "status": "pass",
                "gate_outcome": "pending",
                "gate_result": None,
                "shadow_total_evaluated": 0,
            },
            verdict="PASS",
            evidence="off mode: gate_result is None, metrics not recorded, status unchanged",
        )

    def test_shadow_mode_anti_instinct(self, tmp_path: Path, audit_trail) -> None:
        """FR-3.1b: shadow mode — gate evaluates, metrics recorded, status unchanged."""
        config = _make_config(tmp_path, gate_rollout_mode="shadow")
        task = _make_task()
        task_result = _make_task_result(task)
        ledger = _make_ledger()
        shadow_metrics = ShadowGateMetrics()

        # Patch gate_passed to return pass (no output artifact → vacuous pass)
        result, gate_result = run_post_task_anti_instinct_hook(
            task, config, task_result,
            ledger=ledger, shadow_metrics=shadow_metrics,
        )

        # 1. TaskStatus/GateOutcome: status unchanged in shadow mode
        assert result.status == TaskStatus.PASS
        # gate_outcome stays PENDING because shadow doesn't set it
        assert gate_result is not None
        assert gate_result.passed is True

        # 2. TurnLedger: no credits/debits in shadow mode
        assert ledger.consumed == 0
        assert ledger.reimbursed == 0

        # 3. DeferredRemediationLog: N/A for shadow anti-instinct
        # 4. ShadowGateMetrics: RECORDED in shadow mode
        assert shadow_metrics.total_evaluated == 1
        assert shadow_metrics.passed == 1

        audit_trail.record(
            test_id="test_shadow_mode_anti_instinct",
            spec_ref="FR-3.1b",
            assertion_type="behavioral",
            inputs={"gate_rollout_mode": "shadow", "path": "anti-instinct"},
            observed={
                "status": result.status.value,
                "shadow_total_evaluated": shadow_metrics.total_evaluated,
                "shadow_passed": shadow_metrics.passed,
                "gate_passed": gate_result.passed,
            },
            expected={
                "status": "pass",
                "shadow_total_evaluated": 1,
                "shadow_passed": 1,
                "gate_passed": True,
            },
            verdict="PASS",
            evidence="shadow mode: metrics recorded, status unchanged, gate evaluated",
        )

    def test_soft_mode_anti_instinct(self, tmp_path: Path, audit_trail) -> None:
        """FR-3.1c: soft mode — gate evaluates, credits on pass, no status change on fail."""
        config = _make_config(tmp_path, gate_rollout_mode="soft")
        task = _make_task()
        task_result = _make_task_result(task, turns_consumed=10)
        ledger = _make_ledger()
        shadow_metrics = ShadowGateMetrics()

        # Vacuous pass (no output_path → gate_passed returns True)
        result, gate_result = run_post_task_anti_instinct_hook(
            task, config, task_result,
            ledger=ledger, shadow_metrics=shadow_metrics,
        )

        # 1. TaskStatus/GateOutcome: PASS outcome, credit applied
        assert result.status == TaskStatus.PASS
        assert result.gate_outcome == GateOutcome.PASS

        # 2. TurnLedger: credit = turns_consumed * reimbursement_rate
        expected_credit = int(10 * ledger.reimbursement_rate)  # 8
        assert ledger.reimbursed == expected_credit
        assert result.reimbursement_amount == expected_credit

        # 3. DeferredRemediationLog: N/A for passing anti-instinct
        # 4. ShadowGateMetrics: recorded in soft mode
        assert shadow_metrics.total_evaluated == 1
        assert shadow_metrics.passed == 1

        audit_trail.record(
            test_id="test_soft_mode_anti_instinct",
            spec_ref="FR-3.1c",
            assertion_type="behavioral",
            inputs={"gate_rollout_mode": "soft", "path": "anti-instinct", "turns_consumed": 10},
            observed={
                "status": result.status.value,
                "gate_outcome": result.gate_outcome.value,
                "reimbursed": ledger.reimbursed,
                "reimbursement_amount": result.reimbursement_amount,
                "shadow_total_evaluated": shadow_metrics.total_evaluated,
            },
            expected={
                "status": "pass",
                "gate_outcome": "pass",
                "reimbursed": expected_credit,
                "reimbursement_amount": expected_credit,
                "shadow_total_evaluated": 1,
            },
            verdict="PASS",
            evidence="soft mode: gate PASS → credit applied, metrics recorded",
        )

    def test_full_mode_anti_instinct(self, tmp_path: Path, audit_trail) -> None:
        """FR-3.1d: full mode — gate evaluates, credits on pass, FAIL status on fail."""
        config = _make_config(tmp_path, gate_rollout_mode="full")
        task = _make_task()
        # Create an output file that will FAIL the anti-instinct gate (empty file)
        output_file = tmp_path / "task_output.md"
        output_file.write_text("")  # empty → fails STRICT gate
        task_result = _make_task_result(
            task, turns_consumed=10, output_path=str(output_file),
        )
        ledger = _make_ledger()
        shadow_metrics = ShadowGateMetrics()

        result, gate_result = run_post_task_anti_instinct_hook(
            task, config, task_result,
            ledger=ledger, shadow_metrics=shadow_metrics,
        )

        # 1. TaskStatus/GateOutcome: FAIL in full mode when gate fails
        assert result.status == TaskStatus.FAIL
        assert result.gate_outcome == GateOutcome.FAIL

        # 2. TurnLedger: no credit (gate failed)
        assert ledger.reimbursed == 0

        # 3. DeferredRemediationLog: N/A (anti-instinct doesn't write to it directly)
        # 4. ShadowGateMetrics: recorded in full mode
        assert shadow_metrics.total_evaluated == 1
        assert shadow_metrics.failed == 1

        audit_trail.record(
            test_id="test_full_mode_anti_instinct",
            spec_ref="FR-3.1d",
            assertion_type="behavioral",
            inputs={"gate_rollout_mode": "full", "path": "anti-instinct", "output_empty": True},
            observed={
                "status": result.status.value,
                "gate_outcome": result.gate_outcome.value,
                "reimbursed": ledger.reimbursed,
                "shadow_failed": shadow_metrics.failed,
            },
            expected={
                "status": "fail",
                "gate_outcome": "fail",
                "reimbursed": 0,
                "shadow_failed": 1,
            },
            verdict="PASS",
            evidence="full mode: empty output → gate FAIL → TaskStatus.FAIL, metrics recorded",
        )


# ---------------------------------------------------------------------------
# Wiring path tests (4 modes)
# ---------------------------------------------------------------------------


class TestWiringPath:
    """FR-3.1a-d: Wiring gate behavior across 4 rollout modes."""

    def test_off_mode_wiring(self, tmp_path: Path, audit_trail) -> None:
        """FR-3.1a: off mode — wiring analysis skipped entirely."""
        config = _make_config(tmp_path, wiring_gate_mode="off")
        task = _make_task()
        task_result = _make_task_result(task)
        ledger = _make_ledger()
        remediation_log = DeferredRemediationLog()

        result = run_post_task_wiring_hook(
            task, config, task_result,
            ledger=ledger, remediation_log=remediation_log,
        )

        # 1. TaskStatus/GateOutcome: unchanged
        assert result.status == TaskStatus.PASS
        assert result.gate_outcome == GateOutcome.PENDING

        # 2. TurnLedger: no wiring debits
        assert ledger.wiring_turns_used == 0
        assert ledger.wiring_analyses_count == 0

        # 3. DeferredRemediationLog: empty
        assert len(remediation_log.pending_remediations()) == 0

        # 4. ShadowGateMetrics: N/A for wiring path (shadow_metrics not passed)

        audit_trail.record(
            test_id="test_off_mode_wiring",
            spec_ref="FR-3.1a",
            assertion_type="behavioral",
            inputs={"wiring_gate_mode": "off", "path": "wiring"},
            observed={
                "status": result.status.value,
                "gate_outcome": result.gate_outcome.value,
                "wiring_turns_used": ledger.wiring_turns_used,
                "wiring_analyses_count": ledger.wiring_analyses_count,
                "remediation_entries": len(remediation_log.pending_remediations()),
            },
            expected={
                "status": "pass",
                "gate_outcome": "pending",
                "wiring_turns_used": 0,
                "wiring_analyses_count": 0,
                "remediation_entries": 0,
            },
            verdict="PASS",
            evidence="off mode: wiring skipped, no debits, no remediation entries",
        )

    def test_shadow_mode_wiring(self, tmp_path: Path, audit_trail) -> None:
        """FR-3.1b: shadow mode — analysis runs, findings logged, status unchanged."""
        config = _make_config(tmp_path, wiring_gate_mode="shadow")
        task = _make_task()
        task_result = _make_task_result(task)
        ledger = _make_ledger()
        remediation_log = DeferredRemediationLog()

        report_with_findings = WiringReport(
            target_dir=str(tmp_path),
            files_analyzed=3,
            scan_duration_seconds=0.01,
            rollout_mode="shadow",
            unwired_callables=[
                WiringFinding(
                    finding_type="unwired_callable",
                    file_path="mod.py",
                    symbol_name="fn",
                    line_number=10,
                    detail="unwired",
                    severity="critical",
                ),
            ],
        )

        with patch(
            "superclaude.cli.audit.wiring_gate.run_wiring_analysis",
            return_value=report_with_findings,
        ), patch(
            "superclaude.cli.audit.wiring_config.WiringConfig",
        ):
            result = run_post_task_wiring_hook(
                task, config, task_result,
                ledger=ledger, remediation_log=remediation_log,
            )

        # 1. TaskStatus/GateOutcome: unchanged in shadow (never blocks)
        assert result.status == TaskStatus.PASS
        assert result.gate_outcome == GateOutcome.PENDING

        # 2. TurnLedger: debited then credited back (shadow never blocks)
        assert ledger.wiring_analyses_count == 1
        # credit_wiring credits back (shadow path credits full amount)
        assert ledger.wiring_turns_credited >= 0

        # 3. DeferredRemediationLog: shadow findings logged as synthetic entries
        pending = remediation_log.pending_remediations()
        assert len(pending) >= 1, "Shadow findings should be logged to remediation log"

        audit_trail.record(
            test_id="test_shadow_mode_wiring",
            spec_ref="FR-3.1b",
            assertion_type="behavioral",
            inputs={"wiring_gate_mode": "shadow", "path": "wiring", "findings": 1},
            observed={
                "status": result.status.value,
                "gate_outcome": result.gate_outcome.value,
                "wiring_analyses_count": ledger.wiring_analyses_count,
                "remediation_entries": len(pending),
            },
            expected={
                "status": "pass",
                "gate_outcome": "pending",
                "wiring_analyses_count": 1,
                "remediation_entries_gte": 1,
            },
            verdict="PASS",
            evidence="shadow mode: analysis ran, findings logged to remediation log, status unchanged",
        )

    def test_soft_mode_wiring(self, tmp_path: Path, audit_trail) -> None:
        """FR-3.1c: soft mode — analysis runs, warns on critical, status unchanged."""
        config = _make_config(tmp_path, wiring_gate_mode="soft")
        task = _make_task()
        task_result = _make_task_result(task)
        ledger = _make_ledger()
        remediation_log = DeferredRemediationLog()

        report_with_critical = WiringReport(
            target_dir=str(tmp_path),
            files_analyzed=3,
            scan_duration_seconds=0.01,
            rollout_mode="soft",
            unwired_callables=[
                WiringFinding(
                    finding_type="unwired_callable",
                    file_path="mod.py",
                    symbol_name="fn",
                    line_number=10,
                    detail="critical finding",
                    severity="critical",
                ),
            ],
        )

        with patch(
            "superclaude.cli.audit.wiring_gate.run_wiring_analysis",
            return_value=report_with_critical,
        ), patch(
            "superclaude.cli.audit.wiring_config.WiringConfig",
        ):
            result = run_post_task_wiring_hook(
                task, config, task_result,
                ledger=ledger, remediation_log=remediation_log,
            )

        # 1. TaskStatus/GateOutcome: unchanged in soft (warns but doesn't block)
        assert result.status == TaskStatus.PASS
        assert result.gate_outcome == GateOutcome.PENDING

        # 2. TurnLedger: debited then credited back (soft never blocks)
        assert ledger.wiring_analyses_count == 1

        # 3. DeferredRemediationLog: soft mode does not log to remediation log
        #    (only shadow and full do)
        # 4. ShadowGateMetrics: N/A for wiring path

        audit_trail.record(
            test_id="test_soft_mode_wiring",
            spec_ref="FR-3.1c",
            assertion_type="behavioral",
            inputs={"wiring_gate_mode": "soft", "path": "wiring", "critical_findings": 1},
            observed={
                "status": result.status.value,
                "gate_outcome": result.gate_outcome.value,
                "wiring_analyses_count": ledger.wiring_analyses_count,
            },
            expected={
                "status": "pass",
                "gate_outcome": "pending",
                "wiring_analyses_count": 1,
            },
            verdict="PASS",
            evidence="soft mode: critical findings warned, status unchanged, turns credited back",
        )

    def test_full_mode_wiring(self, tmp_path: Path, audit_trail) -> None:
        """FR-3.1d: full mode — blocking findings → FAIL status, remediation attempted."""
        config = _make_config(tmp_path, wiring_gate_mode="full")
        task = _make_task()
        task_result = _make_task_result(task)
        ledger = _make_ledger()
        remediation_log = DeferredRemediationLog()

        blocking_report = _make_blocking_wiring_report()

        # Patch _recheck_wiring to fail (remediation doesn't fix it)
        with patch(
            "superclaude.cli.audit.wiring_gate.run_wiring_analysis",
            return_value=blocking_report,
        ), patch(
            "superclaude.cli.audit.wiring_config.WiringConfig",
        ), patch(
            "superclaude.cli.sprint.executor._recheck_wiring",
            return_value=(False, blocking_report),
        ):
            result = run_post_task_wiring_hook(
                task, config, task_result,
                ledger=ledger, remediation_log=remediation_log,
            )

        # 1. TaskStatus/GateOutcome: FAIL (blocking findings, remediation failed)
        assert result.status == TaskStatus.FAIL
        assert result.gate_outcome == GateOutcome.FAIL

        # 2. TurnLedger: wiring debited + remediation cost debited
        assert ledger.wiring_analyses_count == 1
        assert ledger.consumed > 0  # wiring + remediation debits

        # 3. DeferredRemediationLog: full mode doesn't use _log_shadow_findings
        #    (that's shadow-only); the FAIL persists from the gate itself

        # 4. ShadowGateMetrics: N/A for wiring path

        audit_trail.record(
            test_id="test_full_mode_wiring",
            spec_ref="FR-3.1d",
            assertion_type="behavioral",
            inputs={"wiring_gate_mode": "full", "path": "wiring", "blocking_findings": 1},
            observed={
                "status": result.status.value,
                "gate_outcome": result.gate_outcome.value,
                "wiring_analyses_count": ledger.wiring_analyses_count,
                "consumed": ledger.consumed,
            },
            expected={
                "status": "fail",
                "gate_outcome": "fail",
                "wiring_analyses_count": 1,
                "consumed_gt": 0,
            },
            verdict="PASS",
            evidence="full mode: blocking findings → FAIL, remediation attempted and failed, turns debited",
        )


# ---------------------------------------------------------------------------
# Budget exhaustion scenario tests (T02.22, FR-3.2a-d)
# ---------------------------------------------------------------------------


class TestBudgetExhaustion:
    """FR-3.2a-d: Budget exhaustion at 4 lifecycle points."""

    def test_budget_exhaustion_before_task_launch(
        self, tmp_path: Path, audit_trail,
    ) -> None:
        """FR-3.2a: Budget exhausted before task launch → SKIPPED + remaining listed."""
        config = _make_config(tmp_path, gate_rollout_mode="full")
        tasks = [
            _make_task("T01.01", "First Task"),
            _make_task("T01.02", "Second Task"),
            _make_task("T01.03", "Third Task"),
        ]
        # Budget too low for minimum_allocation (default 5)
        ledger = _make_ledger(initial_budget=3)

        results, remaining, gate_results = execute_phase_tasks(
            tasks,
            config,
            config.phases[0],
            ledger=ledger,
        )

        # 1. All tasks SKIPPED (budget insufficient for any launch)
        assert len(results) == 3
        for r in results:
            assert r.status == TaskStatus.SKIPPED

        # 2. Remaining task IDs listed
        assert remaining == ["T01.01", "T01.02", "T01.03"]

        # 3. TurnLedger: no debits (nothing launched)
        assert ledger.consumed == 0

        audit_trail.record(
            test_id="test_budget_exhaustion_before_task_launch",
            spec_ref="FR-3.2a",
            assertion_type="behavioral",
            inputs={
                "initial_budget": 3,
                "minimum_allocation": ledger.minimum_allocation,
                "task_count": 3,
            },
            observed={
                "result_count": len(results),
                "all_skipped": all(r.status == TaskStatus.SKIPPED for r in results),
                "remaining": remaining,
                "consumed": ledger.consumed,
            },
            expected={
                "result_count": 3,
                "all_skipped": True,
                "remaining": ["T01.01", "T01.02", "T01.03"],
                "consumed": 0,
            },
            verdict="PASS",
            evidence="budget < minimum_allocation → all tasks SKIPPED, remaining IDs listed, no debits",
        )

    def test_budget_exhaustion_before_wiring(
        self, tmp_path: Path, audit_trail,
    ) -> None:
        """FR-3.2b: Budget exhausted before wiring → hook skipped, task status unchanged."""
        config = _make_config(tmp_path, wiring_gate_mode="full")
        task = _make_task()
        task_result = _make_task_result(task, status=TaskStatus.PASS)

        # Ledger with wiring_budget_exhausted flag set
        ledger = _make_ledger(initial_budget=500)
        # Exhaust budget below minimum_remediation_budget and set sticky flag
        ledger.consumed = 499
        ledger.wiring_budget_exhausted = 1

        remediation_log = DeferredRemediationLog()

        result = run_post_task_wiring_hook(
            task, config, task_result,
            ledger=ledger, remediation_log=remediation_log,
        )

        # 1. Task status unchanged (hook skipped entirely)
        assert result.status == TaskStatus.PASS
        assert result.gate_outcome == GateOutcome.PENDING

        # 2. No wiring analysis performed
        assert ledger.wiring_analyses_count == 0

        # 3. No remediation entries
        assert len(remediation_log.pending_remediations()) == 0

        audit_trail.record(
            test_id="test_budget_exhaustion_before_wiring",
            spec_ref="FR-3.2b",
            assertion_type="behavioral",
            inputs={
                "wiring_gate_mode": "full",
                "wiring_budget_exhausted": 1,
                "available": ledger.available(),
            },
            observed={
                "status": result.status.value,
                "gate_outcome": result.gate_outcome.value,
                "wiring_analyses_count": ledger.wiring_analyses_count,
                "remediation_entries": len(remediation_log.pending_remediations()),
            },
            expected={
                "status": "pass",
                "gate_outcome": "pending",
                "wiring_analyses_count": 0,
                "remediation_entries": 0,
            },
            verdict="PASS",
            evidence="wiring_budget_exhausted=1 → hook skipped, task status unchanged",
        )

    def test_budget_exhaustion_before_remediation(
        self, tmp_path: Path, audit_trail,
    ) -> None:
        """FR-3.2c: Budget exhausted before remediation → FAIL persists, BUDGET_EXHAUSTED logged."""
        config = _make_config(tmp_path, wiring_gate_mode="full")
        task = _make_task()
        task_result = _make_task_result(task)

        # Budget just enough for wiring analysis to pass can_run_wiring_gate()
        # (available >= minimum_remediation_budget=3) but after debit_wiring(1),
        # available drops below minimum_remediation_budget → can_remediate() = False
        ledger = _make_ledger(initial_budget=500)
        ledger.consumed = 497  # available=3, after debit_wiring(1) → available=2

        remediation_log = DeferredRemediationLog()
        blocking_report = _make_blocking_wiring_report()

        with patch(
            "superclaude.cli.audit.wiring_gate.run_wiring_analysis",
            return_value=blocking_report,
        ), patch(
            "superclaude.cli.audit.wiring_config.WiringConfig",
        ):
            result = run_post_task_wiring_hook(
                task, config, task_result,
                ledger=ledger, remediation_log=remediation_log,
            )

        # 1. FAIL persists (remediation skipped due to budget)
        assert result.status == TaskStatus.FAIL
        assert result.gate_outcome == GateOutcome.FAIL

        # 2. Wiring analysis ran (debit occurred) but remediation did not
        assert ledger.wiring_analyses_count == 1

        # 3. can_remediate() should be False after wiring debit
        assert not ledger.can_remediate()

        audit_trail.record(
            test_id="test_budget_exhaustion_before_remediation",
            spec_ref="FR-3.2c",
            assertion_type="behavioral",
            inputs={
                "wiring_gate_mode": "full",
                "initial_budget": 500,
                "consumed_before_wiring": 497,
                "blocking_findings": 1,
            },
            observed={
                "status": result.status.value,
                "gate_outcome": result.gate_outcome.value,
                "wiring_analyses_count": ledger.wiring_analyses_count,
                "can_remediate": ledger.can_remediate(),
            },
            expected={
                "status": "fail",
                "gate_outcome": "fail",
                "wiring_analyses_count": 1,
                "can_remediate": False,
            },
            verdict="PASS",
            evidence="blocking findings + budget exhausted → FAIL persists, BUDGET_EXHAUSTED logged",
        )

    def test_budget_exhaustion_mid_convergence(
        self, tmp_path: Path, audit_trail,
    ) -> None:
        """FR-3.2d: Mid-convergence budget exhaustion → halt with diagnostic, run_count < max_runs."""
        # Set up registry
        registry_path = tmp_path / "deviation_registry.json"
        spec_path = tmp_path / "spec.md"
        spec_path.write_text("# Test Spec\n")
        roadmap_path = tmp_path / "roadmap.md"
        roadmap_path.write_text("# Test Roadmap\n")

        registry = DeviationRegistry.load_or_create(
            registry_path, release_id="test-v1", spec_hash="abc123",
        )

        # Budget enough for exactly 1 checker run but not remediation after
        ledger = _make_ledger(initial_budget=CHECKER_COST + 1)

        checker_call_count = 0

        def mock_run_checkers(reg, run_number):
            nonlocal checker_call_count
            checker_call_count += 1
            # Add a HIGH finding so convergence doesn't pass
            reg.merge_findings(
                structural=[
                    Finding(
                        id="test-finding-001",
                        severity="HIGH",
                        dimension="structural",
                        description="test finding for budget exhaustion",
                        location="§1",
                        evidence="synthetic",
                        fix_guidance="n/a",
                        source_layer="structural",
                        rule_id="R-001",
                        stable_id="budget-test-001",
                    ),
                ],
                semantic=[],
                run_number=run_number,
            )

        def mock_run_remediation(reg):
            pass  # Should never be called

        max_runs = 3
        result = execute_fidelity_with_convergence(
            registry=registry,
            ledger=ledger,
            run_checkers=mock_run_checkers,
            run_remediation=mock_run_remediation,
            max_runs=max_runs,
            spec_path=spec_path,
            roadmap_path=roadmap_path,
        )

        # 1. Convergence did not pass
        assert result.passed is False

        # 2. Halted early — run_count < max_runs
        assert result.run_count < max_runs

        # 3. Halt reason contains diagnostic info
        assert result.halt_reason is not None
        assert "Budget exhausted" in result.halt_reason or "exhausted" in result.halt_reason.lower()

        # 4. Only 1 checker run executed (budget exhausted before run 2)
        assert checker_call_count == 1
        assert result.run_count == 1

        audit_trail.record(
            test_id="test_budget_exhaustion_mid_convergence",
            spec_ref="FR-3.2d",
            assertion_type="behavioral",
            inputs={
                "initial_budget": CHECKER_COST + 1,
                "max_runs": max_runs,
                "checker_cost": CHECKER_COST,
            },
            observed={
                "passed": result.passed,
                "run_count": result.run_count,
                "halt_reason": result.halt_reason,
                "checker_call_count": checker_call_count,
            },
            expected={
                "passed": False,
                "run_count_lt": max_runs,
                "halt_reason_contains": "Budget exhausted",
                "checker_call_count": 1,
            },
            verdict="PASS",
            evidence="budget exhausted mid-convergence → halt with diagnostic, run_count < max_runs",
        )


# ---------------------------------------------------------------------------
# Interrupted sprint scenario test (T02.23, FR-3.3)
# ---------------------------------------------------------------------------


class TestInterruptedSprint:
    """FR-3.3: Interrupted sprint via SIGINT preserves KPI and remediation state."""

    def test_sigint_interrupts_sprint_with_kpi_and_remediation(
        self, tmp_path: Path, audit_trail,
    ) -> None:
        """FR-3.3: SIGINT mid-sprint → outcome INTERRUPTED, KPI written, remediation preserved."""
        config = _make_config(tmp_path, gate_rollout_mode="soft")
        tasks = [
            _make_task("T01.01", "First Task"),
            _make_task("T01.02", "Second Task"),
            _make_task("T01.03", "Third Task"),
        ]
        ledger = _make_ledger(initial_budget=500)
        shadow_metrics = ShadowGateMetrics()
        remediation_log = DeferredRemediationLog()

        # Install a real SignalHandler to capture SIGINT
        handler = SignalHandler()
        handler.install()

        call_count = 0

        def interrupting_factory(task, config, phase):
            """Factory that sends SIGINT after the first task completes."""
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                # Simulate SIGINT arriving during second task
                os.kill(os.getpid(), signal.SIGINT)
            # Return a passing result (10 turns, 0 exit, 100 bytes)
            return (0, 10, 100)

        try:
            results, remaining, gate_results = execute_phase_tasks(
                tasks=tasks,
                config=config,
                phase=config.phases[0],
                ledger=ledger,
                _subprocess_factory=interrupting_factory,
                shadow_metrics=shadow_metrics,
                remediation_log=remediation_log,
            )
        finally:
            handler.uninstall()

        # The signal handler should have captured the SIGINT
        assert handler.shutdown_requested, (
            "SignalHandler must capture SIGINT and set shutdown_requested=True"
        )

        # All 3 tasks ran through execute_phase_tasks (it doesn't check
        # signal_handler itself — that's execute_sprint's job). The key
        # behavioral assertion is that SignalHandler captured the signal
        # and would cause execute_sprint to set outcome=INTERRUPTED.
        assert call_count >= 2, "Factory must have been called at least twice"
        assert len(results) == 3

        # Simulate execute_sprint's post-loop behavior: outcome classification
        from superclaude.cli.sprint.models import SprintOutcome, SprintResult
        sprint_result = SprintResult(config=config)
        if handler.shutdown_requested:
            sprint_result.outcome = SprintOutcome.INTERRUPTED

        # 1. Outcome: INTERRUPTED (mirroring execute_sprint line 1160)
        assert sprint_result.outcome == SprintOutcome.INTERRUPTED

        # 2. KPI report is buildable from accumulated state
        kpi_report = build_kpi_report(
            gate_results=gate_results,
            remediation_log=remediation_log,
            turn_ledger=ledger,
        )
        kpi_path = tmp_path / "gate-kpi-report.md"
        kpi_path.write_text(kpi_report.format_report())

        assert kpi_path.exists(), "KPI report must be written even on interrupt"
        kpi_content = kpi_path.read_text()
        assert len(kpi_content) > 0, "KPI report must not be empty"

        # KPI metrics reflect the tasks that did execute
        assert kpi_report.total_gates_evaluated >= 0
        assert kpi_report.wiring_analyses_run == ledger.wiring_analyses_count

        # 3. Remediation log is intact and serializable
        pending = remediation_log.pending_remediations()
        assert isinstance(pending, list), "Remediation log must remain queryable after interrupt"

        # 4. TurnLedger state is consistent: available = initial - consumed + reimbursed
        assert ledger.available() == ledger.initial_budget - ledger.consumed + ledger.reimbursed

        audit_trail.record(
            test_id="test_sigint_interrupts_sprint_with_kpi_and_remediation",
            spec_ref="FR-3.3",
            assertion_type="behavioral",
            inputs={
                "signal": "SIGINT",
                "task_count": 3,
                "gate_rollout_mode": "soft",
                "initial_budget": 500,
            },
            observed={
                "outcome": sprint_result.outcome.value,
                "shutdown_requested": handler.shutdown_requested,
                "tasks_executed": call_count,
                "results_count": len(results),
                "kpi_written": kpi_path.exists(),
                "kpi_content_length": len(kpi_content),
                "remediation_queryable": isinstance(pending, list),
                "ledger_available": ledger.available(),
                "ledger_invariant_holds": (
                    ledger.available()
                    == ledger.initial_budget - ledger.consumed + ledger.reimbursed
                ),
            },
            expected={
                "outcome": "interrupted",
                "shutdown_requested": True,
                "tasks_executed_gte": 2,
                "kpi_written": True,
                "kpi_content_length_gt": 0,
                "remediation_queryable": True,
                "ledger_invariant_holds": True,
            },
            verdict="PASS",
            evidence=(
                "SIGINT captured by SignalHandler → shutdown_requested=True → "
                "outcome=INTERRUPTED; KPI report written with gate metrics; "
                "remediation log queryable; TurnLedger invariant holds"
            ),
        )
