"""E2E-3 — real-CLI proof for the rerun-tasks safety defenses.

Companion to ``test_e2e_rerun_happy_path.py``. Where the happy-path test proves
the unmocked spawn → capture → merge round-trip, this test proves the two
*abort* defenses that protect that round-trip, driven through a REAL
``rerun-tasks`` CLI invocation against the ``real_release`` fixture (no
``Popen`` / ``shutil.which`` mock):

  * AC4 — concurrent-recovery lock. A second invocation aborts when a live PID
    already holds ``<results_dir>/.recovery-locks/phase-1.lock`` (step 1 of
    ``run_rerun_tasks`` calls ``acquire_recovery_lock``). The abort names the
    holding PID.
  * AC6 — retry-cap-3. When the canonical ``phase-1-result.json`` records 3
    prior reruns of a task (``recovery_history`` entries whose
    ``affected_tasks`` contains the task id — exactly what
    ``recovery.retry_count_for_task`` counts), the step-8 guard aborts the 4th
    attempt with the byte-exact cap message. ``--allow-loop`` bypasses it.

The lock guard (step 1) and the cap guard (step 8) both fire BEFORE the
executor spawns the shim, so the shim need not run for tests #1 and #2 — they
are still real CLI invocations hitting the real production guards. Test #3
(``--allow-loop``) seeds the same capped state, lets the rerun proceed past the
guard, and relies on the real shim passing the task.

Only environmental noise is patched: ``notify._notify`` (desktop toast) and
``rerun_tasks.subprocess.run`` (the post-merge ``verify-checkpoints --recover``
auto-invoke). ``subprocess.Popen`` / ``os.setpgrp`` are NOT patched.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from superclaude.cli.sprint.commands import sprint_group

_TARGET = "T01.02"
_PHASE = 1


def _task_result_entry(task_id: str, status: str) -> dict:
    """A TaskResult.to_dict-shaped entry the result-json readers round-trip."""
    return {
        "task": {
            "task_id": task_id,
            "title": f"Task {task_id}",
            "description": "",
            "dependencies": [],
            "command": "",
            "classifier": "",
        },
        "status": status,
        "turns_consumed": 5,
        "exit_code": 0 if status == "pass" else 1,
        "started_at": "2026-06-01T00:00:00+00:00",
        "finished_at": "2026-06-01T00:01:00+00:00",
        "output_bytes": 100,
        "gate_outcome": "pass" if status == "pass" else "fail",
        "reimbursement_amount": 0,
        "output_path": "",
    }


def _seed_phase_result_with_retries(
    results_dir: Path,
    *,
    target: str,
    attempts: int,
    target_status: str = "fail_recoverable",
) -> Path:
    """Write the canonical ``phase-1-result.json`` so ``retry_count_for_task``
    returns ``attempts`` for ``target``.

    ``recovery.retry_count_for_task`` counts ``recovery_history`` entries whose
    ``affected_tasks`` list contains the task id — so we seed exactly
    ``attempts`` such entries. The three real per-task headings from the
    ``real_release`` fixture (T01.01/T01.02/T01.03) are recorded so the result
    view is coherent with the on-disk tasklist.
    """
    results_dir.mkdir(parents=True, exist_ok=True)
    history = [
        {
            "bundle_id": f"rerun-prior-{i}",
            "affected_tasks": [target],
            "status": "success",
            "timestamp": f"2026-06-01T0{i}:00:00+00:00",
        }
        for i in range(attempts)
    ]
    statuses = {"T01.01": "pass", target: target_status, "T01.03": "pass"}
    payload = {
        "phase": _PHASE,
        "task_results": [
            _task_result_entry(tid, status) for tid, status in statuses.items()
        ],
        "recovery_history": history,
    }
    result_path = results_dir / f"phase-{_PHASE}-result.json"
    result_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return result_path


@pytest.mark.integration
class TestE2ELockAndRetryCap:
    def test_concurrent_lock_aborts_with_pid(self, claude_shim, real_release):
        """AC4: a held lock (THIS live PID) aborts a real rerun, naming the PID.

        Pre-create ``<results_dir>/.recovery-locks/phase-1.lock`` with the
        running process's PID (guaranteed alive) in the exact production JSON
        body shape (``{"pid": ..., "timestamp": ...}``), then invoke
        ``rerun-tasks`` for real. ``acquire_recovery_lock`` (step 1) sees the
        live PID and raises the abort before any task spawns.
        """
        config, index = real_release
        results_dir = config.results_dir
        results_dir.mkdir(parents=True, exist_ok=True)

        my_pid = os.getpid()
        held_ts = "2026-06-02T12:00:00+00:00"
        locks_dir = results_dir / ".recovery-locks"
        locks_dir.mkdir(parents=True, exist_ok=True)
        lock_path = locks_dir / f"phase-{_PHASE}.lock"
        # Match the production body shape written by acquire_recovery_lock:
        # json.dumps({"pid": os.getpid(), "timestamp": <iso>}) (no indent).
        lock_path.write_text(
            json.dumps({"pid": my_pid, "timestamp": held_ts}), encoding="utf-8"
        )

        runner = CliRunner()
        with (
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.rerun_tasks.subprocess.run"),
        ):
            result = runner.invoke(
                sprint_group,
                ["rerun-tasks", str(index), "--phase", str(_PHASE), "--tasks", _TARGET],
            )

        assert result.exit_code != 0, result.output
        # Byte-exact abort surface from acquire_recovery_lock's raise site.
        assert f"Recovery lock held by PID {my_pid} since {held_ts}." in result.output
        assert str(my_pid) in result.output
        assert f"Remove `{lock_path}` if the prior process crashed." in result.output

        # The lock guard fired before the executor — the shim never spawned.
        assert claude_shim.run_log() == [], (
            f"lock abort should pre-empt execution; run_log={claude_shim.run_log()}"
        )

    def test_fourth_attempt_aborts_with_cap_message(self, claude_shim, real_release):
        """AC6: a task already rerun 3 times aborts the 4th with the cap message.

        Seed ``phase-1-result.json`` with 3 ``recovery_history`` entries for
        T01.02 so ``retry_count_for_task(view, "T01.02") == 3``; the step-8
        guard (``>= 3``) fires before execution.
        """
        config, index = real_release
        results_dir = config.results_dir
        result_path = _seed_phase_result_with_retries(
            results_dir, target=_TARGET, attempts=3
        )

        # Confirm the seed produces a count of exactly 3 against the real
        # production counter (re-read the source, do not assume the shape).
        from superclaude.cli.sprint.recovery import retry_count_for_task
        from superclaude.cli.sprint.rerun_tasks import _load_phase_result_view

        view = _load_phase_result_view(result_path)
        assert retry_count_for_task(view, _TARGET) == 3, (
            "seed did not yield retry_count == 3; "
            f"got {retry_count_for_task(view, _TARGET)}"
        )

        runner = CliRunner()
        with (
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.rerun_tasks.subprocess.run"),
        ):
            result = runner.invoke(
                sprint_group,
                ["rerun-tasks", str(index), "--phase", str(_PHASE), "--tasks", _TARGET],
            )

        assert result.exit_code != 0, result.output
        # Byte-exact prefix from the step-8 guard raise site (the trailing
        # `Inspect bundles: [...]` list is environment-dependent).
        assert (
            f"Task {_TARGET} has been rerun 3 times. Manual intervention "
            f"required. Inspect bundles: " in result.output
        ), result.output

        # The cap guard fired before the executor — the shim never spawned.
        assert claude_shim.run_log() == [], (
            f"cap abort should pre-empt execution; run_log={claude_shim.run_log()}"
        )

    def test_allow_loop_bypasses_cap(self, claude_shim, real_release):
        """AC6 inverse: ``--allow-loop`` skips the cap guard for the same state.

        Same seeded count-3 state as the cap test, but ``--allow-loop`` makes
        ``run_rerun_tasks`` skip the step-8 ``>= 3`` check entirely. With the
        shim configured to PASS T01.02 on rerun, the run proceeds past the guard
        and must NOT emit the cap message.
        """
        config, index = real_release
        results_dir = config.results_dir
        _seed_phase_result_with_retries(results_dir, target=_TARGET, attempts=3)

        # Shim passes everything this run (no failures) so the bypassed run can
        # actually proceed through execution/merge rather than re-abort.
        claude_shim.set_failures()

        runner = CliRunner()
        with (
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.rerun_tasks.subprocess.run"),
        ):
            result = runner.invoke(
                sprint_group,
                [
                    "rerun-tasks",
                    str(index),
                    "--phase",
                    str(_PHASE),
                    "--tasks",
                    _TARGET,
                    "--allow-loop",
                ],
            )

        # The defining assertion: the cap message must NOT appear — the guard
        # was bypassed. (Exit code may still vary on downstream steps, but the
        # cap abort specifically must not be what fired.)
        assert "has been rerun 3 times" not in result.output, result.output

        # Positive proof the guard was actually bypassed: the run reached the
        # executor and re-ran ONLY the target via the real shim.
        assert claude_shim.run_log() == [_TARGET], (
            f"--allow-loop run should reach execution and run {_TARGET}; "
            f"run_log={claude_shim.run_log()}, output={result.output}"
        )
        # And it succeeded end-to-end (merge-back happy path) — proving the
        # bypass led to a normal rerun, not a different abort.
        assert result.exit_code == 0, result.output
        assert "Rerun merged" in result.output
