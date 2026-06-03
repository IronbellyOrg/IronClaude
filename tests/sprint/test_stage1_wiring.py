"""Stage-1 wiring acceptance — M3 context injection, H3 task_complete event, M6 router.

(a) build_task_context output reaches the per-task prompt (and execute_phase_tasks
    threads it through);
(b) a per-task run with a logger emits a reconciled `task_complete` JSONL event
    (distinct from `task_rerun_complete`);
(c) the M6 near-miss heading corpus routes correctly, warns on near-misses, stays
    silent on legitimately freeform phases, and reclassifies nothing.
"""

from __future__ import annotations

import json
import logging
import types
from pathlib import Path

from superclaude.cli.sprint import executor as executor_mod
from superclaude.cli.sprint.executor import (
    _parse_phase_tasks,
    _run_task_subprocess,
    execute_phase_tasks,
)
from superclaude.cli.sprint.logging_ import SprintLogger
from superclaude.cli.sprint.models import (
    GateOutcome,
    Phase,
    SprintConfig,
    TaskEntry,
    TaskResult,
    TaskStatus,
)
from superclaude.cli.sprint.process import build_task_context


def _config(tmp_path: Path) -> SprintConfig:
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
        max_turns=5,
        wiring_gate_mode="off",
        wiring_gate_scope="none",
    )
    config.results_dir.mkdir(parents=True, exist_ok=True)
    return config


# --- (a) M3 context injection reaches the prompt --------------------------


def test_prior_context_reaches_per_task_prompt(tmp_path: Path, monkeypatch) -> None:
    config = _config(tmp_path)
    phase = config.phases[0]
    prior = TaskResult(
        task=TaskEntry(task_id="T01.01", title="First"),
        status=TaskStatus.PASS,
        gate_outcome=GateOutcome.PASS,
    )
    prior_context = build_task_context([prior])
    assert "## Prior Task Context" in prior_context  # sanity: non-empty block

    captured: dict = {}
    import superclaude.cli.pipeline.process as pipe
    import superclaude.cli.sprint.process as sproc

    def _spy_init(self, *, prompt, **kwargs):
        captured["prompt"] = prompt
        # Mimic a finished Popen: poll() returns the (non-None) returncode so the
        # RC.2 stall watchdog in _run_task_subprocess sees the process as already
        # exited and does not enter its poll loop.
        self._process = types.SimpleNamespace(returncode=0, poll=lambda: 0)

    monkeypatch.setattr(pipe.ClaudeProcess, "__init__", _spy_init)
    monkeypatch.setattr(sproc.ClaudeProcess, "start", lambda self: None)
    monkeypatch.setattr(sproc.ClaudeProcess, "wait", lambda self: None)

    task2 = TaskEntry(task_id="T01.02", title="Second")
    _run_task_subprocess(task2, config, phase, prior_context=prior_context)

    assert "## Prior Task Context" in captured["prompt"]
    assert "T01.01" in captured["prompt"]  # the prior task appears in context
    assert "Execute task T01.02" in captured["prompt"]  # single-task directive kept


def test_execute_phase_tasks_threads_prior_context(tmp_path: Path, monkeypatch) -> None:
    config = _config(tmp_path)
    phase = config.phases[0]
    tasks = [TaskEntry(task_id="T01.01", title="A"), TaskEntry(task_id="T01.02", title="B")]

    seen: list[tuple[str, str]] = []

    def _spy(task, config, phase, prior_context=""):
        seen.append((task.task_id, prior_context))
        return (0, 1, 0)

    monkeypatch.setattr(executor_mod, "_run_task_subprocess", _spy)
    execute_phase_tasks(tasks, config, phase)

    assert seen[0][1] == ""  # first task: no prior context
    assert "## Prior Task Context" in seen[1][1]  # second task: prior context present
    assert "T01.01" in seen[1][1]


# --- (b) H3 reconciled task_complete event --------------------------------


def test_task_complete_event_emitted_and_distinct(tmp_path: Path) -> None:
    config = _config(tmp_path)
    phase = config.phases[0]
    logger = SprintLogger(config)
    tasks = [TaskEntry(task_id="T01.01", title="A")]

    def _factory(task, config, phase):
        return (0, 3, 100)

    execute_phase_tasks(
        tasks, config, phase, _subprocess_factory=_factory, logger=logger
    )

    lines = [
        json.loads(line)
        for line in config.execution_log_jsonl.read_text().splitlines()
        if line.strip()
    ]
    complete = [e for e in lines if e.get("event") == "task_complete"]
    assert len(complete) == 1, f"expected exactly one task_complete event, got {complete}"
    ev = complete[0]
    # Reconciled field set, identical shape to task_rerun_complete.
    assert ev["phase"] == 1
    assert ev["task_id"] == "T01.01"
    assert ev["status"] == "pass"
    assert ev["turns"] == 3
    assert "duration_sec" in ev
    assert "timestamp" in ev
    # Distinct from the rerun event.
    assert not any(e.get("event") == "task_rerun_complete" for e in lines)


# --- (c) M6 near-miss heading corpus --------------------------------------

# (content, expects_tasks, expects_warning)
_HEADING_CORPUS = [
    # correct strict headings -> route to per-task, NO warning
    ("### T01.01 -- Correct double-dash\n\n**Dependencies:** none\n\nBody.\n", True, False),
    ("### T01.01 — Correct em-dash\n\n**Dependencies:** none\n\nBody.\n", True, False),
    (
        "### T01.01 -- First\n\n**Dependencies:** none\n\nA.\n\n### T01.02 -- Second\n\n**Dependencies:** none\n\nB.\n",
        True,
        False,
    ),
    # near-misses -> route to Path A (None) WITH a warning
    ("#### T01.01 -- Wrong level (4 hashes)\n\nBody.\n", False, True),
    ("## T01.01 -- Wrong level (2 hashes)\n\nBody.\n", False, True),
    ("### T01.01: Colon separator\n\nBody.\n", False, True),
    ("### T1.1 -- Missing zero-pad\n\nBody.\n", False, True),
    ("   ### T01.01 -- Leading whitespace\n\nBody.\n", False, True),
    ("### T01.01-NoSeparatorSpace\n\nBody.\n", False, True),
    ("##### T01.02 -- Five hashes\n\nBody.\n", False, True),
    # legitimately freeform -> Path A (None), NO warning, NO reclassification
    ("# Phase Goal\n\nDo the thing. No task headings here.\n", False, False),
    ("## Overview\n\nSome prose about the migration. Nothing task-like.\n", False, False),
]


def test_m6_heading_router_corpus(tmp_path: Path, caplog) -> None:
    for idx, (content, expects_tasks, expects_warning) in enumerate(_HEADING_CORPUS):
        pf = tmp_path / f"phase-corpus-{idx}.md"
        pf.write_text(content)
        index = tmp_path / "tasklist-index.md"
        index.write_text("index\n")
        config = SprintConfig(
            index_path=index,
            release_dir=tmp_path,
            phases=[Phase(number=1, file=pf, name="P")],
            start_phase=1,
            end_phase=1,
            max_turns=5,
        )
        phase = config.phases[0]

        caplog.clear()
        with caplog.at_level(logging.WARNING, logger="superclaude.sprint.routing"):
            result = _parse_phase_tasks(phase, config)

        routed_to_tasks = result is not None
        assert routed_to_tasks == expects_tasks, (
            f"corpus[{idx}] route mismatch: content={content!r} "
            f"routed_to_tasks={routed_to_tasks} expected={expects_tasks}"
        )

        warned = any("near-miss" in rec.message for rec in caplog.records)
        assert warned == expects_warning, (
            f"corpus[{idx}] warning mismatch: content={content!r} "
            f"warned={warned} expected={expects_warning}"
        )
