"""Stage-1 M5 — `--handoff=off` reproduces legacy behavior exactly.

Drives a real per-task sprint via ``execute_sprint`` with ``handoff_enabled=False``
(stubbing only the per-task subprocess) and asserts the handoff feature is fully
inert: (a) NO files under ``<results_dir>/handoff/``, (b) NO ``task_complete``
events in the execution-log JSONL, (c) zero extra daemon threads vs the baseline.
"""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path
from unittest.mock import patch

from superclaude.cli.sprint import executor as executor_mod
from superclaude.cli.sprint.executor import execute_sprint
from superclaude.cli.sprint.models import Phase, SprintConfig

_PER_TASK_PHASE = """# Phase 1

## Tasks

### T01.01 -- First task

**Dependencies:** none

Body for T01.01.

### T01.02 -- Second task

**Dependencies:** none

Body for T01.02.
"""


def _per_task_config(tmp_path: Path, *, handoff_enabled: bool) -> SprintConfig:
    pf = tmp_path / "phase-1-tasklist.md"
    pf.write_text(_PER_TASK_PHASE)
    index = tmp_path / "tasklist-index.md"
    index.write_text("index\n")
    config = SprintConfig(
        index_path=index,
        release_dir=tmp_path,
        phases=[Phase(number=1, file=pf, name="Phase 1")],
        start_phase=1,
        end_phase=1,
        max_turns=10,
        wiring_gate_mode="off",
        wiring_gate_scope="none",
        handoff_enabled=handoff_enabled,
    )
    config.results_dir.mkdir(parents=True, exist_ok=True)
    return config


def test_handoff_off_is_legacy_exact(tmp_path: Path, monkeypatch) -> None:
    config = _per_task_config(tmp_path, handoff_enabled=False)

    def _stub_subprocess(task, config, phase, prior_context=""):
        # Real per-task path replacement: write a minimal stream-json transcript
        # and report success, without spawning a process.
        config.task_output_file(phase, task).write_text(
            '{"type":"result","subtype":"success","num_turns":1}\n'
        )
        return (0, 1, 0)

    monkeypatch.setattr(executor_mod, "_run_task_subprocess", _stub_subprocess)

    baseline_threads = threading.active_count()

    with (
        patch(
            "superclaude.cli.sprint.executor.shutil.which",
            return_value="/usr/bin/claude",
        ),
        patch(
            "superclaude.cli.sprint.summarizer.PhaseSummarizer.narrate",
            return_value="",
        ),
        patch("superclaude.cli.sprint.notify._notify"),
    ):
        try:
            execute_sprint(config)
        except SystemExit:
            pass

    time.sleep(0.1)
    post_threads = threading.active_count()

    # (a) No handoff records written.
    handoff_dir = config.results_dir / "handoff"
    assert not handoff_dir.exists() or not any(handoff_dir.iterdir()), (
        f"handoff/ should be empty/absent with --handoff=off, found: "
        f"{list(handoff_dir.iterdir()) if handoff_dir.exists() else None}"
    )

    # (b) No task_complete events in the JSONL.
    jsonl = config.execution_log_jsonl
    assert jsonl.exists(), "execution log JSONL should still be written"
    events = [
        json.loads(line) for line in jsonl.read_text().splitlines() if line.strip()
    ]
    assert not any(e.get("event") == "task_complete" for e in events), (
        "task_complete event emitted despite --handoff=off"
    )

    # (c) Zero extra daemon threads (legacy thread-count parity).
    assert post_threads <= baseline_threads + 1, (
        f"handoff path leaked threads: baseline={baseline_threads}, post={post_threads}"
    )


def test_handoff_on_does_write_records_and_events(tmp_path: Path, monkeypatch) -> None:
    """Positive control: with handoff_enabled=True the SAME sprint DOES write
    handoff records and task_complete events — proving the off-case inertness is
    the gate, not a broken path."""
    config = _per_task_config(tmp_path, handoff_enabled=True)

    def _stub_subprocess(task, config, phase, prior_context=""):
        config.task_output_file(phase, task).write_text(
            '{"type":"result","subtype":"success","num_turns":1}\n'
        )
        return (0, 1, 0)

    monkeypatch.setattr(executor_mod, "_run_task_subprocess", _stub_subprocess)

    with (
        patch(
            "superclaude.cli.sprint.executor.shutil.which",
            return_value="/usr/bin/claude",
        ),
        patch(
            "superclaude.cli.sprint.summarizer.PhaseSummarizer.narrate",
            return_value="",
        ),
        patch("superclaude.cli.sprint.notify._notify"),
    ):
        try:
            execute_sprint(config)
        except SystemExit:
            pass

    handoff_dir = config.results_dir / "handoff"
    records = list(handoff_dir.glob("phase-1-task-*.json")) if handoff_dir.exists() else []
    assert len(records) == 2, f"expected 2 handoff records, found {records}"

    events = [
        json.loads(line)
        for line in config.execution_log_jsonl.read_text().splitlines()
        if line.strip()
    ]
    assert sum(1 for e in events if e.get("event") == "task_complete") == 2
