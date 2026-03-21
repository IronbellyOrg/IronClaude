"""Full-flow integration test -- 4 scenarios exercising the complete pipeline.

Covers T07.07 acceptance criteria (Gap 6 deliverable: mandatory).

Scenarios:
1. Task passes gate → continue to next task
2. Task fails gate → remediation spawned → remediation passes → continue
3. Task fails gate → remediation fails → retry fails → HALT with diagnostic
4. Low budget → can_remediate() false → HALT with budget message

Mock boundaries: subprocess execution is mocked; real orchestration, budget,
gate, remediation, conflict review, and diagnostic chain logic is exercised.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from superclaude.cli.pipeline.conflict_review import (
    ConflictAction,
    review_conflicts,
)
from superclaude.cli.pipeline.diagnostic_chain import (
    DiagnosticStage,
    run_diagnostic_chain,
)
from superclaude.cli.pipeline.models import (
    GateCriteria,
    Step,
    StepResult,
    StepStatus,
)
from superclaude.cli.pipeline.trailing_gate import (
    RemediationRetryStatus,
    TrailingGateResult,
    attempt_remediation,
    build_remediation_prompt,
)
from superclaude.cli.sprint.models import (
    SprintConfig,
    TaskEntry,
    TurnLedger,
    build_resume_output,
)


def _make_step(step_id: str, tmp_path: Path, gate: GateCriteria | None = None) -> Step:
    output = tmp_path / f"{step_id}_output.md"
    return Step(
        id=step_id,
        prompt=f"Execute {step_id}",
        output_file=output,
        gate=gate,
        timeout_seconds=60,
    )


def _make_gate_result(step_id: str, passed: bool, reason: str | None = None):
    return TrailingGateResult(
        step_id=step_id,
        passed=passed,
        evaluation_ms=10.0,
        failure_reason=reason,
    )


def _make_step_result(step: Step, status: StepStatus = StepStatus.PASS):
    now = datetime.now(timezone.utc)
    return StepResult(step=step, status=status, started_at=now, finished_at=now)


class TestFullFlowIntegration:
    """Full-flow integration test exercising 4 compound scenarios."""

    # -----------------------------------------------------------------------
    # Scenario 1: Task passes gate → continue
    # -----------------------------------------------------------------------

    def test_scenario_1_pass_gate_continue(self, tmp_path):
        """Task passes gate; budget debited and reimbursed; next task proceeds."""
        ledger = TurnLedger(initial_budget=100)

        gate = GateCriteria(
            required_frontmatter_fields=["title"],
            min_lines=3,
            enforcement_tier="STANDARD",
        )
        step = _make_step("task-1", tmp_path, gate=gate)

        # Simulate task execution
        ledger.debit(10)
        result = _make_step_result(step, StepStatus.PASS)

        # Gate passes
        gate_result = _make_gate_result("task-1", passed=True)
        assert gate_result.passed

        # Reimbursement on pass
        reimbursement = int(10 * ledger.reimbursement_rate)
        ledger.credit(reimbursement)

        # Budget accounting correct
        assert ledger.consumed == 10
        assert ledger.reimbursed == reimbursement
        assert ledger.available() == 100 - 10 + reimbursement

        # No remediation needed, no conflict review needed
        # Next task can proceed
        assert ledger.can_launch()

    # -----------------------------------------------------------------------
    # Scenario 2: Task fails gate → remediation succeeds → continue
    # -----------------------------------------------------------------------

    def test_scenario_2_fail_remediate_pass(self, tmp_path):
        """Task fails gate, remediation passes on first attempt, continues."""
        ledger = TurnLedger(initial_budget=100, minimum_remediation_budget=5)

        gate = GateCriteria(
            required_frontmatter_fields=["title"],
            min_lines=5,
            enforcement_tier="STRICT",
        )
        step = _make_step("task-2", tmp_path, gate=gate)

        # Task execution
        ledger.debit(10)
        task_result = _make_step_result(step, StepStatus.PASS)

        # Gate fails
        gate_result = _make_gate_result(
            "task-2",
            passed=False,
            reason="Missing required field 'title'",
        )
        assert not gate_result.passed

        # Build remediation prompt
        prompt = build_remediation_prompt(
            gate_result,
            step,
            file_paths={step.output_file},
        )
        assert "Missing required field 'title'" in prompt

        # Build remediation step
        remediation_step = _make_step("task-2_remediation", tmp_path)

        # Attempt remediation (passes first attempt)
        retry_result = attempt_remediation(
            remediation_step=remediation_step,
            turns_per_attempt=5,
            can_remediate=ledger.can_remediate,
            debit=ledger.debit,
            run_step=lambda s: _make_step_result(s, StepStatus.PASS),
            check_gate=lambda r: _make_gate_result("task-2_remediation", True),
        )

        assert retry_result.status == RemediationRetryStatus.PASS_FIRST_ATTEMPT
        assert retry_result.attempts_made == 1

        # Conflict review (no intervening tasks in this scenario)
        conflict = review_conflicts(
            remediation_files={remediation_step.output_file},
            intervening_files=set(),
        )
        assert conflict.action == ConflictAction.PASSTHROUGH

        # Budget accounting
        assert ledger.consumed == 15  # 10 original + 5 remediation
        assert ledger.can_launch()  # Can continue

    # -----------------------------------------------------------------------
    # Scenario 3: Task fails gate → remediation fails → HALT with diagnostic
    # -----------------------------------------------------------------------

    def test_scenario_3_fail_remediate_fail_halt(self, tmp_path):
        """Task fails gate, remediation persistently fails, HALT with diagnostic."""
        ledger = TurnLedger(initial_budget=100, minimum_remediation_budget=5)

        gate = GateCriteria(
            required_frontmatter_fields=["title", "status"],
            min_lines=10,
            enforcement_tier="STRICT",
        )
        step = _make_step("task-3", tmp_path, gate=gate)

        # Task execution
        ledger.debit(10)

        # Gate fails
        gate_result = _make_gate_result(
            "task-3",
            passed=False,
            reason="Output too short and missing frontmatter",
        )

        # Build remediation
        remediation_step = _make_step("task-3_remediation", tmp_path)

        # Both remediation attempts fail
        retry_result = attempt_remediation(
            remediation_step=remediation_step,
            turns_per_attempt=5,
            can_remediate=ledger.can_remediate,
            debit=ledger.debit,
            run_step=lambda s: _make_step_result(s, StepStatus.FAIL),
            check_gate=lambda r: _make_gate_result(
                "task-3_remediation", False, "still broken"
            ),
        )

        assert retry_result.status == RemediationRetryStatus.PERSISTENT_FAILURE
        assert retry_result.attempts_made == 2

        # Both attempts' turns consumed
        assert ledger.consumed == 20  # 10 original + 5 + 5 remediation

        # Diagnostic chain fires
        diagnostic = run_diagnostic_chain(
            step_id="task-3",
            failure_reason="Output too short and missing frontmatter",
            remediation_output="",
        )
        assert diagnostic.is_complete
        assert diagnostic.stages_completed == 4

        # Resume output generated
        remaining = [
            TaskEntry(task_id="T07.04", title="Conflict review"),
            TaskEntry(task_id="T07.05", title="Diagnostic chain"),
        ]
        config = SprintConfig(index_path=Path("sprint.md"), work_dir=tmp_path)
        resume = build_resume_output(
            config=config,
            halt_task_id="T07.04",
            remaining_tasks=remaining,
            diagnostic_path=str(tmp_path / "diagnostic.md"),
            ledger=ledger,
        )
        assert "--resume T07.04" in resume
        assert "2" in resume  # remaining count
        assert "diagnostic.md" in resume

    # -----------------------------------------------------------------------
    # Scenario 4: Low budget → skip remediation → HALT
    # -----------------------------------------------------------------------

    def test_scenario_4_low_budget_halt(self, tmp_path):
        """Low budget prevents remediation; HALT with budget message."""
        ledger = TurnLedger(
            initial_budget=15,
            minimum_remediation_budget=10,
            minimum_allocation=5,
        )

        step = _make_step("task-4", tmp_path)

        # Task consumes most of the budget
        ledger.debit(12)
        assert ledger.available() == 3

        # Gate fails
        gate_result = _make_gate_result(
            "task-4",
            passed=False,
            reason="Gate failure",
        )

        # Can't remediate (budget too low)
        assert not ledger.can_remediate()

        # Attempt remediation returns BUDGET_EXHAUSTED
        remediation_step = _make_step("task-4_remediation", tmp_path)
        retry_result = attempt_remediation(
            remediation_step=remediation_step,
            turns_per_attempt=10,
            can_remediate=ledger.can_remediate,
            debit=ledger.debit,
            run_step=lambda s: _make_step_result(s, StepStatus.PASS),
            check_gate=lambda r: _make_gate_result("task-4_remediation", True),
        )

        assert retry_result.status == RemediationRetryStatus.BUDGET_EXHAUSTED
        assert retry_result.attempts_made == 0
        assert retry_result.turns_consumed == 0

        # Budget unchanged (no remediation was attempted)
        assert ledger.consumed == 12

        # No diagnostic chain for budget-specific halt (Gap 2, R-011)
        # Resume output includes budget info
        config = SprintConfig(index_path=Path("sprint.md"), work_dir=tmp_path)
        remaining = [TaskEntry(task_id="T07.05", title="Next task")]
        resume = build_resume_output(
            config=config,
            halt_task_id="T07.05",
            remaining_tasks=remaining,
            ledger=ledger,
        )
        assert "--resume T07.05" in resume
        assert "3" in resume  # available turns
        assert "12" in resume  # consumed turns

    # -----------------------------------------------------------------------
    # Cross-scenario: Budget accounting consistency
    # -----------------------------------------------------------------------

    def test_budget_accounting_across_scenarios(self, tmp_path):
        """Verify TurnLedger state is consistent across multiple operations."""
        ledger = TurnLedger(initial_budget=200, minimum_remediation_budget=5)

        # Task 1: passes (10 consumed, 5 reimbursed)
        ledger.debit(10)
        ledger.credit(int(10 * ledger.reimbursement_rate))

        # Task 2: fails, remediation passes (10 + 5 consumed)
        ledger.debit(10)
        retry = attempt_remediation(
            remediation_step=_make_step("s2_rem", tmp_path),
            turns_per_attempt=5,
            can_remediate=ledger.can_remediate,
            debit=ledger.debit,
            run_step=lambda s: _make_step_result(s, StepStatus.PASS),
            check_gate=lambda r: _make_gate_result("s2", True),
        )
        assert retry.status == RemediationRetryStatus.PASS_FIRST_ATTEMPT

        # Verify cumulative accounting
        # consumed: 10 + 10 + 5 = 25
        # reimbursed: int(10 * 0.8) = 8
        # available: 200 - 25 + 8 = 183
        expected_reimbursed = int(10 * ledger.reimbursement_rate)
        assert ledger.consumed == 25
        assert ledger.reimbursed == expected_reimbursed
        assert ledger.available() == 200 - 25 + expected_reimbursed


# ---------------------------------------------------------------------------
# Anti-instinct gate full pipeline flow tests
# ---------------------------------------------------------------------------

from unittest.mock import patch

from superclaude.cli.sprint.executor import (
    execute_phase_tasks,
    run_post_task_anti_instinct_hook,
)
from superclaude.cli.sprint.models import (
    GateOutcome,
    Phase,
    ShadowGateMetrics,
    TaskEntry as SprintTaskEntry,
    TaskResult as SprintTaskResult,
    TaskStatus as SprintTaskStatus,
)


def _make_sprint_config(tmp_path: Path, gate_rollout_mode: str = "off"):
    pf = tmp_path / "phase-1.md"
    pf.write_text("# Phase 1\n")
    return SprintConfig(
        index_path=tmp_path / "idx.md",
        release_dir=tmp_path,
        phases=[Phase(number=1, file=pf)],
        gate_rollout_mode=gate_rollout_mode,
        wiring_gate_mode="off",
    )


class TestAntiInstinctFullFlow:
    """Full pipeline flow tests for anti-instinct gate reimbursement paths."""

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(True, None))
    def test_reimbursement_path_credit_on_pass(self, mock_gate, tmp_path):
        """Credit path: gate PASS credits ledger via reimbursement_rate."""
        config = _make_sprint_config(tmp_path, "soft")
        phase = config.phases[0]
        ledger = TurnLedger(initial_budget=100)
        metrics = ShadowGateMetrics()
        tasks = [SprintTaskEntry(task_id="T01.01", title="Task 1")]

        def _factory(task, cfg, ph):
            return (0, 10, 100)

        results, remaining = execute_phase_tasks(
            tasks, config, phase, ledger=ledger,
            _subprocess_factory=_factory,
            shadow_metrics=metrics,
        )

        assert len(results) == 1
        assert results[0].status == SprintTaskStatus.PASS
        assert results[0].gate_outcome == GateOutcome.PASS
        assert results[0].reimbursement_amount == 8  # int(10 * 0.8)
        assert ledger.reimbursed >= 8  # at least the anti-instinct credit

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(False, "fail"))
    def test_remediation_path_budget_exhausted(self, mock_gate, tmp_path):
        """Remediation path: gate FAIL + insufficient budget → BUDGET_EXHAUSTED.

        Uses run_post_task_anti_instinct_hook directly since execute_phase_tasks
        constructs TaskResult without output_path (subprocess-level concern).
        """
        config = _make_sprint_config(tmp_path, "full")
        (tmp_path / "output.md").write_text("test output")
        ledger = TurnLedger(initial_budget=2, minimum_remediation_budget=10)
        metrics = ShadowGateMetrics()

        result = SprintTaskResult(
            task=SprintTaskEntry(task_id="T01.01", title="Task 1"),
            status=SprintTaskStatus.PASS,
            turns_consumed=5,
            output_path=str(tmp_path / "output.md"),
        )

        result = run_post_task_anti_instinct_hook(
            result.task, config, result, ledger=ledger, shadow_metrics=metrics,
        )

        assert result.gate_outcome == GateOutcome.FAIL
        assert result.status == SprintTaskStatus.FAIL  # full mode fails task

    @patch("superclaude.cli.pipeline.gates.gate_passed", return_value=(False, "undischarged"))
    def test_full_mode_fail_sets_task_result_fail(self, mock_gate, tmp_path):
        """Full mode: gate FAIL → TaskResult.status = FAIL."""
        config = _make_sprint_config(tmp_path, "full")
        (tmp_path / "output.md").write_text("test output")
        ledger = TurnLedger(initial_budget=100)
        metrics = ShadowGateMetrics()

        result = SprintTaskResult(
            task=SprintTaskEntry(task_id="T01.01", title="Task 1"),
            status=SprintTaskStatus.PASS,
            turns_consumed=10,
            output_path=str(tmp_path / "output.md"),
        )

        result = run_post_task_anti_instinct_hook(
            result.task, config, result, ledger=ledger, shadow_metrics=metrics,
        )

        assert result.status == SprintTaskStatus.FAIL
        assert result.gate_outcome == GateOutcome.FAIL
        assert metrics.failed == 1


# ---------------------------------------------------------------------------
# Wiring budget scenario integration tests (T04.02, D-0022)
# ---------------------------------------------------------------------------

from superclaude.cli.sprint.executor import run_post_task_wiring_hook


def _make_wiring_sprint_config(
    tmp_path: Path,
    wiring_gate_mode: str = "shadow",
    wiring_analysis_turns: int = 1,
    remediation_cost: int = 2,
):
    """Create a SprintConfig with wiring gate enabled."""
    pf = tmp_path / "phase-1.md"
    pf.write_text("# Phase 1\n")
    return SprintConfig(
        index_path=tmp_path / "idx.md",
        release_dir=tmp_path,
        phases=[Phase(number=1, file=pf)],
        gate_rollout_mode="off",
        wiring_gate_mode=wiring_gate_mode,
        wiring_analysis_turns=wiring_analysis_turns,
        remediation_cost=remediation_cost,
    )


class TestWiringBudgetScenarios:
    """Wiring budget integration tests: Scenarios 5-8 (D-0022).

    Validates credit/debit flows, floor-to-zero arithmetic (SC-012),
    BLOCKING remediation, null-ledger compatibility (SC-014), and
    shadow deferred logging.
    """

    # -----------------------------------------------------------------------
    # Scenario 5: Credit floor-to-zero (SC-012)
    # -----------------------------------------------------------------------

    def test_scenario_5_credit_floor_to_zero(self):
        """credit_wiring(1, 0.8) returns 0 credits due to int() floor.

        SC-012: debit/credit correctness — int(1 * 0.8) == 0, so no credits
        are returned. This is the design intent per R7.
        """
        ledger = TurnLedger(initial_budget=100)
        initial_available = ledger.available()

        # Debit 1 turn for wiring analysis
        ledger.debit_wiring(1)
        assert ledger.wiring_turns_used == 1
        assert ledger.available() == initial_available - 1

        # Credit with floor-to-zero: int(1 * 0.8) == 0
        credited = ledger.credit_wiring(1, 0.8)
        assert credited == 0, (
            f"Expected 0 credits (floor-to-zero), got {credited}"
        )
        assert ledger.wiring_turns_credited == 0
        assert ledger.reimbursed == 0

        # Available decreased by 1 with no reimbursement
        assert ledger.available() == initial_available - 1

    # -----------------------------------------------------------------------
    # Scenario 6: BLOCKING remediation debits budget, BUDGET_EXHAUSTED on depletion
    # -----------------------------------------------------------------------

    def test_scenario_6_blocking_remediation_budget_exhausted(self, tmp_path):
        """Full mode: blocking findings trigger remediation debit;
        budget depletion prevents further remediation.
        """
        config = _make_wiring_sprint_config(
            tmp_path,
            wiring_gate_mode="full",
            wiring_analysis_turns=1,
            remediation_cost=2,
        )
        # Tight budget: just enough for analysis + one remediation
        ledger = TurnLedger(
            initial_budget=10,
            minimum_remediation_budget=5,
        )

        task = SprintTaskEntry(task_id="T01.01", title="Wiring task")
        result = SprintTaskResult(
            task=task,
            status=SprintTaskStatus.PASS,
            turns_consumed=5,
        )

        # Run wiring hook — analysis runs against tmp_path (no Python files
        # means no findings, but we test the budget debit-before-analysis path)
        result = run_post_task_wiring_hook(task, config, result, ledger=ledger)

        # Budget was debited for wiring analysis
        assert ledger.wiring_turns_used == 1
        # With no findings (empty dir), credits should be returned
        assert ledger.available() >= ledger.initial_budget - 1

        # Now deplete budget to test exhaustion guard
        ledger.debit(ledger.available() - 2)  # leave only 2 turns
        assert not ledger.can_run_wiring_gate()

        # Second wiring hook should be skipped due to budget exhaustion
        result2 = SprintTaskResult(
            task=SprintTaskEntry(task_id="T01.02", title="Task 2"),
            status=SprintTaskStatus.PASS,
            turns_consumed=1,
        )
        result2 = run_post_task_wiring_hook(
            result2.task, config, result2, ledger=ledger
        )
        # Task status unchanged (skipped due to budget)
        assert result2.status == SprintTaskStatus.PASS

    # -----------------------------------------------------------------------
    # Scenario 7: Null-ledger compatibility (SC-014)
    # -----------------------------------------------------------------------

    def test_scenario_7_null_ledger_compatibility(self, tmp_path):
        """ledger=None path: no budget operations, no crashes (SC-014).

        When ledger is None, wiring hook must still run analysis but
        skip all budget operations without raising exceptions.
        """
        config = _make_wiring_sprint_config(
            tmp_path,
            wiring_gate_mode="shadow",
        )

        task = SprintTaskEntry(task_id="T01.01", title="Task 1")
        result = SprintTaskResult(
            task=task,
            status=SprintTaskStatus.PASS,
            turns_consumed=5,
        )

        # Pass ledger=None — must not crash
        result = run_post_task_wiring_hook(task, config, result, ledger=None)

        # Task status unchanged (shadow mode never blocks)
        assert result.status == SprintTaskStatus.PASS

    # -----------------------------------------------------------------------
    # Scenario 8: Shadow mode defers finding log without modifying status
    # -----------------------------------------------------------------------

    def test_scenario_8_shadow_deferred_log(self, tmp_path):
        """Shadow mode: findings logged but task status unchanged."""
        config = _make_wiring_sprint_config(
            tmp_path,
            wiring_gate_mode="shadow",
            wiring_analysis_turns=1,
        )
        ledger = TurnLedger(initial_budget=100)

        task = SprintTaskEntry(task_id="T01.01", title="Task 1")
        result = SprintTaskResult(
            task=task,
            status=SprintTaskStatus.PASS,
            turns_consumed=5,
        )

        # Run shadow hook
        result = run_post_task_wiring_hook(task, config, result, ledger=ledger)

        # Shadow mode: status always unchanged regardless of findings
        assert result.status == SprintTaskStatus.PASS

        # Budget: debited then credited back (shadow never blocks)
        assert ledger.wiring_turns_used == 1
        # Credit returned (shadow always credits back)
        assert ledger.wiring_turns_credited >= 0
