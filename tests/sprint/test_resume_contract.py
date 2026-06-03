"""Stage-2 H5 — resume skip predicate + per-state skip/run behavior."""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.sprint.executor import execute_phase_tasks
from superclaude.cli.sprint.handoff import FileHandoffStore, is_validated_success
from superclaude.cli.sprint.models import (
    GateOutcome,
    HandoffRecord,
    Phase,
    SprintConfig,
    TaskEntry,
    TaskStatus,
    TurnLedger,
)


def _config(tmp_path: Path, *, resume_task_id: str = "") -> SprintConfig:
    pf = tmp_path / "phase-1-tasklist.md"
    pf.write_text("# Phase 1\n")
    index = tmp_path / "tasklist-index.md"
    index.write_text("index\n")
    config = SprintConfig(
        index_path=index,
        release_dir=tmp_path,
        phases=[Phase(number=1, file=pf, name="Phase 1")],
        start_phase=1,
        end_phase=1,
        max_turns=100,
        wiring_gate_mode="off",
        wiring_gate_scope="none",
        resume_task_id=resume_task_id,
    )
    config.results_dir.mkdir(parents=True, exist_ok=True)
    return config


def _record(task_id: str, status: TaskStatus, gate: GateOutcome) -> HandoffRecord:
    return HandoffRecord(
        task_id=task_id,
        phase=1,
        status=status.value,
        gate_outcome=gate.value,
        turns_consumed=4,
        exit_code=0,
        output_path=f"/r/{task_id}.txt",
    )


# --- (a) predicate per TaskStatus ----------------------------------------


def test_is_validated_success_only_for_pass_plus_gate_success() -> None:
    cases = [
        (TaskStatus.PASS, GateOutcome.PASS, True),
        (TaskStatus.PASS, GateOutcome.FAIL, False),  # PASS but gate failed
        (TaskStatus.PASS, GateOutcome.DEFERRED, False),
        (TaskStatus.PASS, GateOutcome.PENDING, False),
        (TaskStatus.FAIL_TERMINAL, GateOutcome.PASS, False),
        (TaskStatus.FAIL_RECOVERABLE, GateOutcome.PASS, False),
        (TaskStatus.INCOMPLETE, GateOutcome.PASS, False),
        (TaskStatus.SKIPPED, GateOutcome.PASS, False),
    ]
    for status, gate, expected in cases:
        rec = _record("T01.01", status, gate)
        assert is_validated_success(rec) is expected, (
            f"{status.value}+{gate.value} → {is_validated_success(rec)}, expected {expected}"
        )


# --- (b) skip validated-success, re-run failure, no budget debit on skip --


def test_resume_skips_validated_success_and_reruns_failure(tmp_path: Path) -> None:
    config = _config(tmp_path, resume_task_id="T01.02")
    phase = config.phases[0]
    store = FileHandoffStore(config)
    tasks = [TaskEntry("T01.01", "First"), TaskEntry("T01.02", "Second")]

    # Pre-seed: T01.01 validated-success, T01.02 recoverable failure.
    store.write(_record("T01.01", TaskStatus.PASS, GateOutcome.PASS), phase=phase, task=tasks[0])
    store.write(_record("T01.02", TaskStatus.FAIL_RECOVERABLE, GateOutcome.FAIL), phase=phase, task=tasks[1])

    ran: list[str] = []

    def _factory(task, config, phase):
        ran.append(task.task_id)
        return (0, 3, 100)

    ledger = TurnLedger(initial_budget=100)
    results, remaining, _ = execute_phase_tasks(
        tasks,
        config,
        phase,
        ledger=ledger,
        _subprocess_factory=_factory,
        handoff_store=store,
    )

    # T01.01 validated-success → skipped (never re-run); T01.02 → re-ran.
    assert "T01.01" not in ran, "validated-success task was re-run"
    assert "T01.02" in ran, "recoverable-failure task was NOT re-run"

    by_id = {r.task.task_id: r for r in results}
    # Skipped task is recorded as satisfied (PASS), with no turns spent this run.
    assert by_id["T01.01"].status == TaskStatus.PASS
    assert by_id["T01.01"].turns_consumed == 0
    # Only ONE task debited the budget (the re-run); the skip debited nothing.
    assert ledger.consumed == ledger.minimum_allocation, (
        f"expected exactly one task's min-allocation debited, got consumed={ledger.consumed}"
    )


def test_resume_inactive_runs_all_tasks_even_with_records(tmp_path: Path) -> None:
    # resume_task_id="" → resume inactive → no skipping even if records exist.
    config = _config(tmp_path, resume_task_id="")
    phase = config.phases[0]
    store = FileHandoffStore(config)
    tasks = [TaskEntry("T01.01", "First")]
    store.write(_record("T01.01", TaskStatus.PASS, GateOutcome.PASS), phase=phase, task=tasks[0])

    ran: list[str] = []

    def _factory(task, config, phase):
        ran.append(task.task_id)
        return (0, 1, 0)

    execute_phase_tasks(
        tasks, config, phase, _subprocess_factory=_factory, handoff_store=store
    )
    assert ran == ["T01.01"], "task was skipped despite resume being inactive"
