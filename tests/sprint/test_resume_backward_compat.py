"""Stage-2 M5 — resume against a pre-Stage-1 release dir (no handoff/) degrades.

Resuming against a `results_dir` with NO `handoff/` subdirectory must: (a) raise
no error, (b) perform no per-task skipping (run every task), and (c) behave
identically to today's phase-granular resume. Reads must NOT lazily create the
`handoff/` dir — only writes do.
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.sprint.executor import execute_phase_tasks
from superclaude.cli.sprint.handoff import FileHandoffStore
from superclaude.cli.sprint.models import (
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


def test_resume_without_handoff_dir_runs_all_tasks_no_error(tmp_path: Path) -> None:
    # Resume is requested, but the release dir predates Stage 1 → no handoff/ dir.
    config = _config(tmp_path, resume_task_id="T01.01")
    phase = config.phases[0]
    store = FileHandoffStore(config)
    assert not (config.results_dir / "handoff").exists()

    tasks = [TaskEntry("T01.01", "First"), TaskEntry("T01.02", "Second")]
    ran: list[str] = []

    def _factory(task, config, phase):
        ran.append(task.task_id)
        return (0, 1, 0)

    # (a) no error raised even though resume is active and handoff/ is absent
    results, _remaining, _gates = execute_phase_tasks(
        tasks, config, phase, _subprocess_factory=_factory, handoff_store=store
    )

    # (b) no per-task skipping — every task ran (phase-granular behavior); and
    # (c) the results are exactly what a non-resume run would produce.
    assert ran == ["T01.01", "T01.02"]
    assert len(results) == 2
    assert all(r.status == TaskStatus.PASS for r in results)


def test_store_read_on_missing_handoff_dir_does_not_create_it(tmp_path: Path) -> None:
    # Lazy-creation guarantee (Step 4.5): a READ against a missing handoff/ dir
    # returns None and must NOT create the directory — only writes do.
    config = _config(tmp_path)
    phase = config.phases[0]
    store = FileHandoffStore(config)
    task = TaskEntry("T01.01", "First")

    assert not (config.results_dir / "handoff").exists()
    assert store.read(phase=phase, task=task) is None
    assert not (config.results_dir / "handoff").exists(), (
        "FileHandoffStore.read created handoff/ — lazy creation must be write-only"
    )
