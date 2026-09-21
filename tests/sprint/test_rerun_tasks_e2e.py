"""AC1, AC2, AC3 — E2E integration tests for sprint rerun-tasks."""

from __future__ import annotations

import io
import json
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from superclaude.cli.sprint.commands import sprint_group
from superclaude.cli.sprint.models import (
    GateOutcome,
    TaskEntry,
    TaskResult,
    TaskStatus,
)

# ---------------------------------------------------------------------------
# Shared seeding helpers
# ---------------------------------------------------------------------------

_PHASE_TASKLIST = """# Phase 7: Recoverable Work

| Field | Value |
|---|---|

## Tasks

### T07.11 -- First recoverable task

**Dependencies:** none

Body for T07.11.

### T07.12 -- Second recoverable task

**Dependencies:** none

Body for T07.12.
"""


def _write_index_and_phase(tmp_path: Path) -> Path:
    """Write a minimal valid tasklist-index.md + phase-7-tasklist.md.

    Returns the index path. The index uses the canonical ``## Phase Files``
    table shape that ``discover_phases`` parses (File column), and the phase
    file carries two ``### T07.NN`` task blocks so ``_parse_phase_tasks``
    delegates to the per-task executor path.
    """
    phase_file = tmp_path / "phase-7-tasklist.md"
    phase_file.write_text(_PHASE_TASKLIST, encoding="utf-8")

    index = tmp_path / "tasklist-index.md"
    index.write_text(
        "# TASKLIST INDEX\n"
        "\n"
        "## Phase Files\n"
        "\n"
        "| Phase | File | Phase Name |\n"
        "|---|---|---|\n"
        "| 7 | phase-7-tasklist.md | Recoverable Work |\n",
        encoding="utf-8",
    )
    return index


def _task_result_dict(task_id: str, status: TaskStatus) -> dict:
    """Build a serialized TaskResult dict (TaskResult.to_dict() shape)."""
    now = datetime(2026, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
    return TaskResult(
        task=TaskEntry(task_id=task_id, title=f"{task_id} title", dependencies=[]),
        status=status,
        turns_consumed=5,
        exit_code=1 if status is not TaskStatus.PASS else 0,
        started_at=now,
        finished_at=now,
        output_bytes=10,
        gate_outcome=GateOutcome.FAIL
        if status is not TaskStatus.PASS
        else GateOutcome.PASS,
    ).to_dict()


def _seed_failed_phase(tmp_path: Path, phase: int = 7) -> Path:
    """Seed a release dir whose phase-N-result.json has 2 FAIL_RECOVERABLE tasks.

    Also writes pre-existing canonical task transcripts so the merge step has
    something to rename to ``*.failed-<ts>``. Returns the index path.
    """
    index = _write_index_and_phase(tmp_path)
    results = tmp_path / "results"
    results.mkdir(parents=True, exist_ok=True)

    payload = {
        "phase": phase,
        "status": "error",
        "exit_code": 1,
        "started_at": "2026-06-01T12:00:00+00:00",
        "finished_at": "2026-06-01T12:05:00+00:00",
        "task_results": [
            _task_result_dict("T07.11", TaskStatus.FAIL_RECOVERABLE),
            _task_result_dict("T07.12", TaskStatus.FAIL_RECOVERABLE),
        ],
        "recovery_history": [],
    }
    (results / f"phase-{phase}-result.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )

    # Pre-existing canonical transcripts (the originals that get renamed on merge).
    for tid in ("T07.11", "T07.12"):
        (results / f"phase-{phase}-task-{tid}-output.txt").write_text(
            "original failing transcript\n", encoding="utf-8"
        )
        (results / f"phase-{phase}-task-{tid}-errors.txt").write_text(
            "original error log\n", encoding="utf-8"
        )
    return index


class _FakePopenSuccess:
    """Mirrors test_e2e_success._FakePopenSuccess + a stdin stub.

    The executor's ClaudeProcess.start() writes the prompt to ``stdin`` then
    closes it; the per-task path exercises that, so the fake exposes a
    BytesIO-like stdin in addition to poll()/wait().
    """

    def __init__(self):
        self.returncode = 0
        self.pid = 20000
        self.stdin = io.BytesIO()
        self._poll_count = 0

    def poll(self):
        self._poll_count += 1
        if self._poll_count <= 1:
            return None
        return 0

    def wait(self, timeout=None):
        self.returncode = 0
        return 0


# ---------------------------------------------------------------------------
# AC1 — --dry-run prints the plan and executes nothing
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestRerunTasksDryRun:
    """AC1: `rerun-tasks --dry-run` previews the plan without spawning work."""

    def test_dry_run_prints_plan_does_not_execute(self, tmp_path):
        index = _seed_failed_phase(tmp_path, phase=7)
        runner = CliRunner()

        with patch("superclaude.cli.pipeline.process.subprocess.Popen") as mock_popen:
            result = runner.invoke(
                sprint_group,
                [
                    "rerun-tasks",
                    str(index),
                    "--phase",
                    "7",
                    "--tasks",
                    "T07.11,T07.12",
                    "--dry-run",
                ],
            )

        assert result.exit_code == 0, result.output
        # No subprocess may spawn on the dry-run path.
        mock_popen.assert_not_called()
        # The dry-run plan surface is printed.
        assert "[dry-run]" in result.output
        assert "T07.11" in result.output
        assert "T07.12" in result.output


# ---------------------------------------------------------------------------
# AC2 + AC3 — full re-execute: rename originals, flip checkboxes, emit the
# phase_rerun_complete JSONL event, run verify-checkpoints, regenerate state.
# ---------------------------------------------------------------------------


def _popen_factory_all_pass():
    """Popen factory whose every spawned process exits 0 (mirrors test_e2e_success).

    Each task subprocess that the rerun executor launches gets a fresh
    ``_FakePopenSuccess``; with exit code 0 the executor classifies every
    rerun task as PASS, which is what lets ``_rerun_targets_passed`` see the
    targets succeed and proceed to merge-back.
    """

    def factory(cmd, **kwargs):
        return _FakePopenSuccess()

    return factory
