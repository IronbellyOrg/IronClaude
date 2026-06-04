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


@pytest.mark.integration
class TestRerunTasksRoundTrip:
    """AC2 + AC3: a successful rerun renames originals, emits exactly one
    phase_rerun_complete event, and regenerates the checkpoint manifest."""

    def test_rerun_renames_originals_flips_checkboxes_emits_event_runs_verify_checkpoints(
        self, tmp_path
    ):
        index = _seed_failed_phase(tmp_path, phase=7)
        results = tmp_path / "results"
        factory = _popen_factory_all_pass()
        runner = CliRunner()

        # Every external boundary of run_rerun_tasks is mocked so no real
        # process spawns: the per-task executor subprocess (Popen factory),
        # the claude-binary preflight (shutil.which), the process-group call
        # (os.setpgrp), the sprint notify hook, and the post-merge
        # verify-checkpoints auto-invoke (subprocess.run in rerun_tasks).
        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.pipeline.process.subprocess.Popen",
                side_effect=factory,
            ),
            patch("superclaude.cli.pipeline.process.os.setpgrp", create=True),
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.rerun_tasks.subprocess.run") as mock_verify,
        ):
            result = runner.invoke(
                sprint_group,
                [
                    "rerun-tasks",
                    str(index),
                    "--phase",
                    "7",
                    "--tasks",
                    "T07.11,T07.12",
                    # --force-merge is required: flip_target_checkboxes writes a
                    # rerun-provenance block into the source tasklist before the
                    # merge-time SHA re-check, so the source SHA legitimately
                    # differs from the value captured pre-flip. Forcing the merge
                    # is the supported way to complete the round trip.
                    "--force-merge",
                ],
            )

        assert result.exit_code == 0, result.output

        # --- Invariant 1: originals renamed to *.failed-<ts> on merge-back ---
        failed_renames = sorted(results.glob("phase-7-task-*-output.failed-*.txt"))
        assert failed_renames, (
            "expected original transcripts renamed to *.failed-<ts>; "
            f"results dir held: {sorted(p.name for p in results.iterdir())}"
        )

        # --- Invariant 2: checkbox/provenance finalized on the source tasklist ---
        # finalize_checkboxes_on_success records the completed rerun in a
        # rerun_history provenance block on the canonical phase tasklist.
        phase_text = (tmp_path / "phase-7-tasklist.md").read_text(encoding="utf-8")
        assert "SUPERCLAUDE-RERUN" in phase_text
        assert "rerun_history:" in phase_text

        # --- Invariant 3: exactly one phase_rerun_complete event in the log ---
        execlog = tmp_path / "execution-log.jsonl"
        assert execlog.exists(), "execution-log.jsonl was not written"
        events = [
            json.loads(line)
            for line in execlog.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        rerun_complete = [e for e in events if e.get("event") == "phase_rerun_complete"]
        assert len(rerun_complete) == 1, (
            f"expected exactly one phase_rerun_complete; got {len(rerun_complete)}"
        )
        assert rerun_complete[0]["phase"] == 7

        # --- Invariant 4: post-run checkpoint/manifest regeneration triggered ---
        # The default path auto-invokes `verify-checkpoints --recover`. We assert
        # the invocation fired (it is the state-regeneration step) rather than
        # spawning a real second CLI process.
        assert mock_verify.called, "verify-checkpoints --recover was not auto-invoked"
        verify_argv = mock_verify.call_args.args[0]
        assert "verify-checkpoints" in verify_argv
        assert "--recover" in verify_argv

        # --- AC3 round-trip artifact equivalence (key invariant form) ---
        # The merged result JSON keeps both target tasks and records the rerun in
        # recovery_history — the canonical post-rerun state is internally
        # consistent with the rerun that produced it.
        merged = json.loads(
            (results / "phase-7-result.json").read_text(encoding="utf-8")
        )
        merged_task_ids = {
            tr.get("task", {}).get("task_id") for tr in merged.get("task_results", [])
        }
        assert {"T07.11", "T07.12"} <= merged_task_ids
        assert merged.get("recovery_history"), "recovery_history not appended on merge"


# ---------------------------------------------------------------------------
# R-F6 / §T8.1 — the engine's own provenance write must NOT self-trip the
# mid-flight-edit guard. The happy path must merge back WITHOUT --force-merge.
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestRerunTasksMergeBackNoForce:
    """Regression: --merge-back succeeds on the happy path without --force-merge.

    Before the R-F6 fix, step 10 (`flip_target_checkboxes`) wrote a
    SUPERCLAUDE-RERUN provenance block into the source tasklist, so the
    step-12 whole-file SHA re-check (`current_sha != source_sha`) always
    tripped — forcing every clean rerun to require ``--force-merge`` (which
    disables the guard entirely). With both guard hashes now computed over
    the provenance-block-stripped content, the engine's own write is
    invisible to the guard and the merge completes on the default path.
    """

    def test_merge_back_succeeds_without_force_merge(self, tmp_path):
        index = _seed_failed_phase(tmp_path, phase=7)
        results = tmp_path / "results"
        factory = _popen_factory_all_pass()
        runner = CliRunner()

        with (
            patch(
                "superclaude.cli.sprint.executor.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.pipeline.process.subprocess.Popen",
                side_effect=factory,
            ),
            patch("superclaude.cli.pipeline.process.os.setpgrp", create=True),
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.rerun_tasks.subprocess.run"),
        ):
            result = runner.invoke(
                sprint_group,
                [
                    "rerun-tasks",
                    str(index),
                    "--phase",
                    "7",
                    "--tasks",
                    "T07.11,T07.12",
                    # NOTE: deliberately NO --force-merge. The whole point of
                    # this regression test is that the happy path merges back
                    # cleanly without it, proving the engine's own provenance
                    # write no longer self-trips the §T8.1 guard.
                ],
            )

        # --- Primary assertion: clean exit, no mid-flight-edit abort ---
        assert result.exit_code == 0, result.output
        assert "Source tasklist modified since rerun started" not in result.output
        assert "Rerun merged" in result.output

        # --- The merge actually happened (originals renamed, history recorded) ---
        failed_renames = sorted(results.glob("phase-7-task-*-output.failed-*.txt"))
        assert failed_renames, (
            "expected original transcripts renamed to *.failed-<ts> on a "
            "successful merge-back without --force-merge; results dir held: "
            f"{sorted(p.name for p in results.iterdir())}"
        )

        phase_text = (tmp_path / "phase-7-tasklist.md").read_text(encoding="utf-8")
        assert "SUPERCLAUDE-RERUN" in phase_text
        assert "rerun_history:" in phase_text

        merged = json.loads(
            (results / "phase-7-result.json").read_text(encoding="utf-8")
        )
        merged_task_ids = {
            tr.get("task", {}).get("task_id") for tr in merged.get("task_results", [])
        }
        assert {"T07.11", "T07.12"} <= merged_task_ids
        assert merged.get("recovery_history"), "recovery_history not appended on merge"
