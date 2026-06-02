"""E2E-1 — real-``claude``-subprocess proof for ``sprint rerun-tasks``.

This is the proof-of-harness test. Unlike ``tests/sprint/test_e2e_success.py``
and ``tests/sprint/test_rerun_tasks_e2e.py`` (which patch ``subprocess.Popen``
and/or ``shutil.which``), this test spawns a REAL deterministic ``claude`` shim
installed on ``$PATH`` and exercises the whole chain unmocked:

    process-spawn  ->  stdin-prompt  ->  stdout-capture  ->  on-disk merge

Scenario:
  * A real 1-phase / 3-task sprint runs for real. The shim fails ``T01.02``
    transiently on run #1 (terminal result line ``is_error:true`` +
    ``output_tokens:0`` -> ``_is_transient_failure`` -> FAIL_RECOVERABLE);
    ``T01.01`` and ``T01.03`` pass.
  * A real ``rerun-tasks --phase 1 --tasks T01.02`` re-executes ONLY that task
    via the CLI (no Popen mock); the shim passes it on the rerun.
  * Assertions hit the REAL on-disk state produced by the merge-back.

Only environmental noise is patched: ``notify._notify`` (no desktop toast) and
``rerun_tasks.subprocess.run`` (the post-merge ``verify-checkpoints --recover``
auto-invoke, which would otherwise shell out to a second ``superclaude`` CLI
process; we assert it FIRED rather than running it for real). ``os.setpgrp``
and ``subprocess.Popen`` are NOT patched — the shim is spawned for real.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from superclaude.cli.sprint.commands import sprint_group
from superclaude.cli.sprint.executor import execute_sprint


def _load_phase1_result(results_dir: Path) -> dict:
    return json.loads(
        (results_dir / "phase-1-result.json").read_text(encoding="utf-8")
    )


def _status_by_id(result_json: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for tr in result_json.get("task_results", []):
        tid = tr.get("task", {}).get("task_id")
        if tid:
            out[tid] = tr.get("status")
    return out


@pytest.mark.integration
class TestE2ERerunHappyPath:
    def test_real_subprocess_rerun_round_trip(self, claude_shim, real_release):
        config, index = real_release
        results_dir = config.results_dir

        # --- Run 1: real sprint; shim fails T01.02 transiently -------------
        claude_shim.set_failures("T01.02")

        with patch("superclaude.cli.sprint.notify._notify"):
            # execute_sprint spawns the REAL shim per task (no Popen mock).
            # A recoverable task failure makes the phase ERROR, so the sprint
            # exits non-zero — the expected, real outcome of run #1.
            with pytest.raises(SystemExit) as exc_info:
                execute_sprint(config)
            assert exc_info.value.code == 1

        # The initial run executed all three tasks for real.
        first_runs = claude_shim.runs()
        assert first_runs.get("T01.01") == 1
        assert first_runs.get("T01.02") == 1
        assert first_runs.get("T01.03") == 1

        # Real on-disk task transcripts exist (shim stdout was captured).
        for tid in ("T01.01", "T01.02", "T01.03"):
            out = results_dir / f"phase-1-task-{tid}-output.txt"
            assert out.exists(), f"missing real transcript for {tid}"
            assert out.read_text(encoding="utf-8").strip(), f"empty transcript {tid}"

        # The executor classified the phase from the REAL exit codes.
        initial = _load_phase1_result(results_dir)
        initial_status = _status_by_id(initial)
        assert initial_status["T01.01"] == "pass"
        assert initial_status["T01.03"] == "pass"
        assert initial_status["T01.02"] == "fail_recoverable", (
            "transient-fail exit code did not classify T01.02 as FAIL_RECOVERABLE; "
            f"got {initial_status.get('T01.02')!r}"
        )

        # Capture the original T01.02 transcript content + the unchanged
        # neighbours' mtimes so we can prove the rerun touched only T01.02.
        t0102_orig = (
            results_dir / "phase-1-task-T01.02-output.txt"
        ).read_text(encoding="utf-8")
        t0101_mtime = (results_dir / "phase-1-task-T01.01-output.txt").stat().st_mtime_ns
        t0103_mtime = (results_dir / "phase-1-task-T01.03-output.txt").stat().st_mtime_ns

        # --- Run 2: real rerun via the CLI; shim now passes T01.02 ---------
        # Resetting failures also clears the run counter / run-log so the
        # rerun's run-log reflects ONLY what the rerun re-executed.
        claude_shim.set_failures()  # no failures this run
        runner = CliRunner()

        with (
            patch("superclaude.cli.sprint.notify._notify"),
            # The post-merge verify-checkpoints --recover auto-invoke shells
            # out to a second `superclaude` CLI; assert it fired, don't run it.
            patch("superclaude.cli.sprint.rerun_tasks.subprocess.run") as mock_verify,
        ):
            result = runner.invoke(
                sprint_group,
                [
                    "rerun-tasks",
                    str(index),
                    "--phase",
                    "1",
                    "--tasks",
                    "T01.02",
                ],
            )

        assert result.exit_code == 0, result.output
        assert "Rerun merged" in result.output

        # --- Proof 1: ONLY T01.02 re-executed in the rerun ----------------
        rerun_runs = claude_shim.runs()
        rerun_log = claude_shim.run_log()
        assert rerun_log == ["T01.02"], (
            f"rerun re-executed more than the target; run_log={rerun_log}"
        )
        assert rerun_runs == {"T01.02": 1}, (
            f"expected only T01.02 to run once on rerun; runs={rerun_runs}"
        )

        # Neighbours' canonical transcripts were not rewritten by the rerun.
        assert (
            results_dir / "phase-1-task-T01.01-output.txt"
        ).stat().st_mtime_ns == t0101_mtime
        assert (
            results_dir / "phase-1-task-T01.03-output.txt"
        ).stat().st_mtime_ns == t0103_mtime

        # --- Proof 2: original T01.02 transcript renamed to *.failed-<ts>* -
        failed_renames = sorted(
            results_dir.glob("phase-1-task-T01.02-output.failed-*.txt")
        )
        assert failed_renames, (
            "expected original T01.02 transcript renamed to *.failed-<ts>; "
            f"results dir held: {sorted(p.name for p in results_dir.iterdir())}"
        )
        # The preserved artifact is the ORIGINAL failing transcript.
        assert failed_renames[0].read_text(encoding="utf-8") == t0102_orig

        # --- Proof 3: a FRESH T01.02 transcript replaced the canonical one -
        fresh = (results_dir / "phase-1-task-T01.02-output.txt").read_text(
            encoding="utf-8"
        )
        assert fresh != t0102_orig, "canonical T01.02 transcript was not replaced"
        # The fresh transcript is a PASS transcript (no transient-error marker).
        assert '"is_error": false' in fresh or '"is_error":false' in fresh

        # --- Proof 4: the rerun itself recorded T01.02 PASS in its bundle --
        # Locate the rerun bundle (rerun-<ts>/) and read its isolated result.
        bundles = sorted(p for p in results_dir.glob("rerun-*") if p.is_dir())
        assert bundles, "no rerun bundle directory was created"
        bundle = bundles[-1]
        bundle_result = json.loads(
            (bundle / "results" / "phase-1-result.json").read_text(encoding="utf-8")
        )
        assert _status_by_id(bundle_result).get("T01.02") == "pass", (
            "the rerun's own (isolated) result JSON did not record T01.02 PASS"
        )

        # --- Proof 5: sidecar written + canonical status refreshed to pass --
        # F2 (AC-1): run_rerun_tasks wrote the task-results.json sidecar into the
        # bundle results dir — direct evidence, not just transitive via the merge.
        assert (bundle / "results" / "task-results.json").exists(), (
            "run_rerun_tasks did not write the task-results.json sidecar"
        )
        merged = _load_phase1_result(results_dir)
        merged_status = _status_by_id(merged)
        assert {"T01.01", "T01.02", "T01.03"} <= set(merged_status)
        # AC-2 (the gap this fix closes): the sidecar-driven merge flips the
        # CANONICAL T01.02 entry fail_recoverable -> pass, with no duplicate entry;
        # the passing neighbours are unchanged.
        assert merged_status["T01.02"] == "pass", (
            "canonical T01.02 status was not refreshed to pass after merge-back; "
            f"got {merged_status.get('T01.02')!r}"
        )
        assert merged_status["T01.01"] == "pass"
        assert merged_status["T01.03"] == "pass"
        t0102_entries = [
            tr
            for tr in merged["task_results"]
            if tr.get("task", {}).get("task_id") == "T01.02"
        ]
        assert len(t0102_entries) == 1, "T01.02 entry was duplicated, not replaced"
        assert merged.get("recovery_history"), (
            "recovery_history was not appended to the canonical result JSON"
        )

        # --- Proof 6: exactly one phase_rerun_complete event in the log ----
        execlog = config.execution_log_jsonl
        assert execlog.exists(), "execution-log.jsonl missing after rerun"
        events = [
            json.loads(line)
            for line in execlog.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        rerun_complete = [e for e in events if e.get("event") == "phase_rerun_complete"]
        assert len(rerun_complete) == 1, (
            f"expected exactly one phase_rerun_complete; got {len(rerun_complete)}"
        )
        assert rerun_complete[0]["phase"] == 1

        # --- Proof 7: T01.02 checkbox/provenance finalized on the tasklist -
        phase_text = (config.release_dir / "phase-1-tasklist.md").read_text(
            encoding="utf-8"
        )
        assert "SUPERCLAUDE-RERUN" in phase_text
        assert "rerun_history:" in phase_text
        assert "T01.02" in phase_text

        # --- Proof 8: verify-checkpoints --recover auto-invoke fired -------
        assert mock_verify.called, "verify-checkpoints --recover was not auto-invoked"
        verify_argv = mock_verify.call_args.args[0]
        assert "verify-checkpoints" in verify_argv
        assert "--recover" in verify_argv
