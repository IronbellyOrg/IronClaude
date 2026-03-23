"""Wiring budget scenario tests -- labeled scenarios 5-8.

Tests exercise TurnLedger wiring arithmetic, the run_post_task_wiring_hook
interaction with ledger and remediation log, and edge cases around null
ledger passthrough and shadow mode logging.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from superclaude.cli.sprint.executor import run_post_task_wiring_hook
from superclaude.cli.sprint.models import (
    Phase,
    SprintConfig,
    TaskEntry,
    TaskResult,
    TaskStatus,
    TurnLedger,
    GateOutcome,
)
from superclaude.cli.pipeline.trailing_gate import (
    DeferredRemediationLog,
    TrailingGateResult,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_config(tmp_path: Path, wiring_mode: str = "off") -> SprintConfig:
    """Build a minimal SprintConfig for wiring tests."""
    pf = tmp_path / "phase-1-tasklist.md"
    pf.write_text("# Phase 1\n")
    phase = Phase(number=1, file=pf, name="Phase 1")

    index = tmp_path / "tasklist-index.md"
    index.write_text("index\n")

    return SprintConfig(
        index_path=index,
        release_dir=tmp_path,
        phases=[phase],
        start_phase=1,
        end_phase=1,
        max_turns=100,
        wiring_gate_mode=wiring_mode,
        wiring_gate_scope="none",
    )


def _make_task(task_id: str = "T01.01", title: str = "Test task") -> TaskEntry:
    return TaskEntry(task_id=task_id, title=title)


def _make_result(task: TaskEntry | None = None) -> TaskResult:
    t = task or _make_task()
    return TaskResult(task=t, status=TaskStatus.PASS)


# ---------------------------------------------------------------------------
# Stub for WiringReport used by mocked run_wiring_analysis
# ---------------------------------------------------------------------------


@dataclass
class _FakeFinding:
    finding_type: str = "unwired_callable"
    file_path: str = "src/foo.py"
    symbol_name: str = "bar"
    line_number: int = 1
    detail: str = "missing wiring"
    severity: str = "critical"
    suppressed: bool = False


@dataclass
class _FakeWiringReport:
    all_findings: list = None
    scan_duration_seconds: float = 0.001
    target_dir: str = "."
    rollout_mode: str = "shadow"

    def __post_init__(self):
        if self.all_findings is None:
            self.all_findings = []

    @property
    def unsuppressed_findings(self):
        return [f for f in self.all_findings if not f.suppressed]

    @property
    def total_findings(self):
        return len(self.unsuppressed_findings)

    def blocking_count(self, mode=None):
        effective = mode or self.rollout_mode
        unsuppressed = self.unsuppressed_findings
        if effective == "shadow":
            return 0
        if effective == "soft":
            return sum(1 for f in unsuppressed if f.severity == "critical")
        if effective == "full":
            return sum(
                1 for f in unsuppressed if f.severity in ("critical", "major")
            )
        return 0


# ---------------------------------------------------------------------------
# Scenario 5: Credit floor-to-zero arithmetic
# ---------------------------------------------------------------------------


class TestScenario5CreditFloorToZero:
    """int(1 * 0.8) = 0 -- single-turn credit floors to zero."""

    def test_scenario_5_credit_floor_to_zero(self):
        """credit_wiring(1, 0.8) returns 0 due to int() floor."""
        ledger = TurnLedger(initial_budget=100)

        credited = ledger.credit_wiring(1, 0.8)

        assert credited == 0, (
            f"Expected floor-to-zero: int(1 * 0.8) == 0, got {credited}"
        )
        assert ledger.reimbursed == 0
        assert ledger.wiring_turns_credited == 0
        assert ledger.available() == 100

    def test_credit_floor_to_zero_with_default_rate(self):
        """credit_wiring(1) with default rate 0.8 also floors to zero."""
        ledger = TurnLedger(initial_budget=50, reimbursement_rate=0.8)

        credited = ledger.credit_wiring(1)

        assert credited == 0
        assert ledger.reimbursed == 0

    def test_credit_above_floor_returns_positive(self):
        """credit_wiring(2, 0.8) = int(1.6) = 1 -- above the floor."""
        ledger = TurnLedger(initial_budget=50)

        credited = ledger.credit_wiring(2, 0.8)

        assert credited == 1
        assert ledger.reimbursed == 1
        assert ledger.wiring_turns_credited == 1


# ---------------------------------------------------------------------------
# Scenario 6: Blocking remediation lifecycle (full mode)
# ---------------------------------------------------------------------------


class TestScenario6BlockingRemediationLifecycle:
    """Full mode: finding triggers remediation, debit occurs, budget decreases."""

    @patch("superclaude.cli.audit.wiring_gate.run_wiring_analysis")
    @patch("superclaude.cli.audit.wiring_config.WiringConfig")
    @patch("superclaude.cli.sprint.executor._recheck_wiring")
    def test_scenario_6_blocking_remediation_lifecycle(
        self, mock_recheck, mock_wc_cls, mock_analysis, tmp_path,
    ):
        """Full mode wiring hook: finding -> debit -> remediation -> budget decreased."""
        config = _make_config(tmp_path, wiring_mode="full")
        task = _make_task()
        result = _make_result(task)

        ledger = TurnLedger(initial_budget=20)
        initial_available = ledger.available()

        # Stub run_wiring_analysis to return a report with a blocking finding
        blocking_finding = _FakeFinding(severity="critical")
        report = _FakeWiringReport(
            all_findings=[blocking_finding],
            rollout_mode="full",
        )
        mock_analysis.return_value = report

        # Recheck wiring returns failure (remediation did not fix it)
        mock_recheck.return_value = (False, report)

        returned = run_post_task_wiring_hook(
            task, config, result, ledger=ledger,
        )

        # Budget should have decreased: wiring_analysis_turns debit + remediation_cost debit
        assert ledger.available() < initial_available, (
            f"Budget should decrease after full-mode remediation. "
            f"Was {initial_available}, now {ledger.available()}"
        )
        # Wiring analysis debit recorded
        assert ledger.wiring_turns_used >= config.wiring_analysis_turns
        # Remediation cost was debited (consumed increased by remediation_cost)
        assert ledger.consumed >= config.wiring_analysis_turns + config.remediation_cost
        # Task marked FAIL because recheck returned False
        assert returned.status == TaskStatus.FAIL
        assert returned.gate_outcome == GateOutcome.FAIL


# ---------------------------------------------------------------------------
# Scenario 7: Null ledger passthrough
# ---------------------------------------------------------------------------


class TestScenario7NullLedgerPassthrough:
    """ledger=None must not crash; result returned unchanged."""

    @patch("superclaude.cli.audit.wiring_gate.run_wiring_analysis")
    @patch("superclaude.cli.audit.wiring_config.WiringConfig")
    def test_scenario_7_null_ledger_passthrough(
        self, mock_wc_cls, mock_analysis, tmp_path,
    ):
        """run_post_task_wiring_hook with ledger=None returns result unchanged, no crash."""
        config = _make_config(tmp_path, wiring_mode="shadow")
        task = _make_task()
        result = _make_result(task)
        original_status = result.status

        # Provide a clean report so shadow mode logs nothing
        mock_analysis.return_value = _FakeWiringReport(rollout_mode="shadow")

        returned = run_post_task_wiring_hook(
            task, config, result, ledger=None,
        )

        assert returned is result
        assert returned.status == original_status

    def test_null_ledger_off_mode_passthrough(self, tmp_path):
        """Off mode with ledger=None is a trivial passthrough (no mock needed)."""
        config = _make_config(tmp_path, wiring_mode="off")
        task = _make_task()
        result = _make_result(task)

        returned = run_post_task_wiring_hook(
            task, config, result, ledger=None,
        )

        assert returned is result
        assert returned.status == TaskStatus.PASS


# ---------------------------------------------------------------------------
# Scenario 8: Shadow mode deferred log integrity
# ---------------------------------------------------------------------------


class TestScenario8ShadowDeferredLog:
    """Shadow mode logs findings to DeferredRemediationLog without corruption."""

    @patch("superclaude.cli.audit.wiring_gate.run_wiring_analysis")
    @patch("superclaude.cli.audit.wiring_config.WiringConfig")
    def test_scenario_8_shadow_deferred_log(
        self, mock_wc_cls, mock_analysis, tmp_path,
    ):
        """Shadow mode appends findings to remediation log; log is not corrupted."""
        config = _make_config(tmp_path, wiring_mode="shadow")
        task = _make_task(task_id="T02.03", title="Shadow test")
        result = _make_result(task)

        remediation_log = DeferredRemediationLog()

        # Report with two unsuppressed findings
        findings = [
            _FakeFinding(
                finding_type="unwired_callable",
                detail="missing import A",
                severity="major",
            ),
            _FakeFinding(
                finding_type="orphan_module",
                detail="orphan B",
                severity="info",
            ),
        ]
        mock_analysis.return_value = _FakeWiringReport(
            all_findings=findings,
            rollout_mode="shadow",
        )

        returned = run_post_task_wiring_hook(
            task, config, result, ledger=TurnLedger(initial_budget=50),
            remediation_log=remediation_log,
        )

        # Task status unchanged in shadow mode
        assert returned.status == TaskStatus.PASS

        # Remediation log should have entries for each finding
        pending = remediation_log.pending_remediations()
        assert len(pending) == 2, (
            f"Expected 2 pending remediations, got {len(pending)}"
        )

        # Verify log entries reference the correct task
        for entry in pending:
            assert entry.step_id == "T02.03"
            assert "shadow" in entry.failure_reason.lower()

        # Verify serialization round-trip does not corrupt
        serialized = remediation_log.serialize()
        recovered = DeferredRemediationLog.deserialize(serialized)
        assert recovered.entry_count == 2
        recovered_pending = recovered.pending_remediations()
        assert len(recovered_pending) == 2
        for orig, recov in zip(pending, recovered_pending):
            assert orig.step_id == recov.step_id
            assert orig.failure_reason == recov.failure_reason

    @patch("superclaude.cli.audit.wiring_gate.run_wiring_analysis")
    @patch("superclaude.cli.audit.wiring_config.WiringConfig")
    def test_shadow_no_findings_log_empty(
        self, mock_wc_cls, mock_analysis, tmp_path,
    ):
        """Shadow mode with no findings leaves remediation log empty."""
        config = _make_config(tmp_path, wiring_mode="shadow")
        task = _make_task()
        result = _make_result(task)
        remediation_log = DeferredRemediationLog()

        mock_analysis.return_value = _FakeWiringReport(rollout_mode="shadow")

        run_post_task_wiring_hook(
            task, config, result,
            ledger=TurnLedger(initial_budget=50),
            remediation_log=remediation_log,
        )

        assert remediation_log.entry_count == 0
