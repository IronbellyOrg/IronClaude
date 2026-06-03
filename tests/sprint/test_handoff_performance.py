"""Stage-3 L4 — parallel wall-clock win + in-flight-dependency resume safety.

(a) With a fixed-duration mock subprocess, ``task_parallelism=4`` completes a
    no-dependency phase in < 0.5x the serial (``task_parallelism=1``) wall-clock.
(b) A task that was in-flight at kill time has NO handoff record; on resume its
    declared dependents must NOT launch before it — the scheduler orders the
    dependent after its (unsatisfied) dependency, which still runs.
"""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from superclaude.cli.sprint.executor import execute_phase_tasks
from superclaude.cli.sprint.handoff import FileHandoffStore
from superclaude.cli.sprint.models import (
    Phase,
    SprintConfig,
    TaskEntry,
    TaskStatus,
)

_TASK_SLEEP = 0.2


def _config(tmp_path: Path, *, task_parallelism: int = 1, resume_task_id: str = "") -> SprintConfig:
    tmp_path.mkdir(parents=True, exist_ok=True)
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
        max_turns=1000,
        wiring_gate_mode="off",
        wiring_gate_scope="none",
        task_parallelism=task_parallelism,
        resume_task_id=resume_task_id,
    )
    config.results_dir.mkdir(parents=True, exist_ok=True)
    return config


def _sleep_factory(task, config, phase):
    time.sleep(_TASK_SLEEP)
    return (0, 1, 0)


@pytest.mark.slow
@pytest.mark.performance
def test_parallel_k4_under_half_serial_wallclock(tmp_path: Path) -> None:
    tasks = [TaskEntry(f"T01.{i:02d}", f"t{i}") for i in range(1, 5)]  # independent

    serial_cfg = _config(tmp_path / "serial", task_parallelism=1)
    t0 = time.monotonic()
    r1, _, _ = execute_phase_tasks(
        tasks, serial_cfg, serial_cfg.phases[0], _subprocess_factory=_sleep_factory
    )
    serial = time.monotonic() - t0

    par_cfg = _config(tmp_path / "par", task_parallelism=4)
    t0 = time.monotonic()
    r4, _, _ = execute_phase_tasks(
        tasks, par_cfg, par_cfg.phases[0], _subprocess_factory=_sleep_factory
    )
    parallel = time.monotonic() - t0

    assert len(r1) == 4 and len(r4) == 4
    assert all(r.status == TaskStatus.PASS for r in r4)
    assert parallel < 0.5 * serial, (
        f"parallel not < 0.5x serial: serial={serial:.3f}s parallel={parallel:.3f}s "
        f"(ratio {parallel / serial:.2f})"
    )


@pytest.mark.slow
def test_in_flight_dependency_dependents_wait_on_resume(tmp_path: Path) -> None:
    config = _config(tmp_path, task_parallelism=4, resume_task_id="T01.02")
    phase = config.phases[0]
    # Resume is active and handoff/ exists, but the in-flight task left NO record.
    store = FileHandoffStore(config)
    (config.results_dir / "handoff").mkdir(parents=True, exist_ok=True)

    tasks = [
        TaskEntry("T01.01", "in-flight dependency"),
        TaskEntry("T01.02", "dependent", dependencies=["T01.01"]),
    ]

    launched: list[str] = []

    def _factory(task, config, phase):
        launched.append(task.task_id)
        time.sleep(0.05)
        return (0, 1, 0)

    results, _remaining, _gates = execute_phase_tasks(
        tasks,
        config,
        phase,
        _subprocess_factory=_factory,
        handoff_store=store,
    )

    by_id = {r.task.task_id: r for r in results}
    # The in-flight dependency had no validated-success record → NOT skipped, it ran.
    assert "T01.01" in launched
    assert by_id["T01.01"].status == TaskStatus.PASS
    # The dependent did NOT launch before its (unsatisfied) dependency — the
    # scheduler ordered T01.02 strictly after T01.01.
    assert "T01.02" in launched
    assert launched.index("T01.01") < launched.index("T01.02"), (
        f"dependent launched before its dependency on resume: {launched}"
    )
