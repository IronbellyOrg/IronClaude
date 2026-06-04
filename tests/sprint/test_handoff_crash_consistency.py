"""Stage-2 L3 — crash-consistency asymmetry: handoff file is authoritative.

The handoff file is written atomically (temp+replace); the JSONL journal event
is a separate, lock-free append. A crash BETWEEN the two leaves a completed task
with a handoff record but NO `task_complete` journal event. Resume must treat the
atomically-written handoff file — not the JSONL — as the authoritative completion
source, and therefore skip the task.
"""

from __future__ import annotations

import json
from pathlib import Path

from superclaude.cli.sprint.executor import execute_phase_tasks
from superclaude.cli.sprint.handoff import FileHandoffStore
from superclaude.cli.sprint.models import (
    GateOutcome,
    HandoffRecord,
    Phase,
    SprintConfig,
    TaskEntry,
    TaskStatus,
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


def test_resume_honors_handoff_file_without_journal_event(tmp_path: Path) -> None:
    config = _config(tmp_path, resume_task_id="T01.01")
    phase = config.phases[0]
    store = FileHandoffStore(config)
    task = TaskEntry("T01.01", "First")

    # Crash-between state: write the validated-success handoff record atomically,
    # but DO NOT emit the corresponding task_complete journal event (the crash
    # window between the handoff write and the JSONL append).
    store.write(
        HandoffRecord(
            task_id="T01.01",
            phase=1,
            status=TaskStatus.PASS.value,
            gate_outcome=GateOutcome.PASS.value,
            turns_consumed=4,
            exit_code=0,
            output_path="/r/T01.01.txt",
        ),
        phase=phase,
        task=task,
    )

    # Assert the asymmetry: handoff file present, journal has no task_complete.
    assert config.handoff_file(phase, task).exists()
    jsonl = config.execution_log_jsonl
    if jsonl.exists():
        events = [
            json.loads(line) for line in jsonl.read_text().splitlines() if line.strip()
        ]
        assert not any(e.get("event") == "task_complete" for e in events), (
            "precondition violated: a task_complete event exists (not the crash window)"
        )

    # Resume must trust the atomically-written handoff file → skip the task.
    ran: list[str] = []

    def _factory(task, config, phase):
        ran.append(task.task_id)
        return (0, 1, 0)

    results, _remaining, _gates = execute_phase_tasks(
        [task], config, phase, _subprocess_factory=_factory, handoff_store=store
    )

    assert ran == [], (
        "resume re-ran a task whose handoff file marks it validated-success"
    )
    assert results[0].status == TaskStatus.PASS
