"""E2E (real ``claude`` subprocess) — auto-resume default (v4.3.5).

Reuses the ``claude_shim`` + ``real_release`` harness (commit 344a754a) to prove
auto-resume end-to-end without mocking the spawn chain:

  * AC-2 / AC-9 — after a real interrupted run leaves T01.02 fail_recoverable,
    BARE ``rerun-tasks <index>`` (no --phase/--tasks) auto-detects the boundary
    phase + failed task and re-runs ONLY it, merging the canonical status to pass.
  * AC-1 — BARE ``sprint run <index>`` auto-resumes the same interrupted release
    (last-completed double-validated first), dispatches the task-level path, and
    refreshes the canonical T01.02 status to pass.
  * AC-3 — a hard crash (result.json + transcripts gone, dangling phase_start)
    drives PHASE-granularity resume: the whole boundary phase re-runs.

Only environmental noise is patched: ``notify._notify`` (desktop toast),
``rerun_tasks.subprocess.run`` (the post-merge verify-checkpoints auto-invoke),
and ``summarizer.invoke_sonnet`` (the gate's ADVISORY coherence read — forced to
"" so it never shells the shim; it can never change the deterministic verdict).
The shim itself is spawned for real.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from superclaude.cli.sprint.commands import sprint_group
from superclaude.cli.sprint.executor import execute_sprint


def _status_by_id(result_json: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for tr in result_json.get("task_results", []):
        tid = tr.get("task", {}).get("task_id")
        if tid:
            out[tid] = tr.get("status")
    return out


def _phase1_result(results_dir: Path) -> dict:
    return json.loads((results_dir / "phase-1-result.json").read_text(encoding="utf-8"))


def _run_until_interrupted(config, claude_shim) -> None:
    """Run 1: a real sprint where the shim fails T01.02 transiently."""
    claude_shim.set_failures("T01.02")
    with patch("superclaude.cli.sprint.notify._notify"):
        with pytest.raises(SystemExit) as exc_info:
            execute_sprint(config)
        assert exc_info.value.code == 1
    initial = _status_by_id(_phase1_result(config.results_dir))
    assert initial["T01.02"] == "fail_recoverable"
    assert initial["T01.01"] == "pass"
    assert initial["T01.03"] == "pass"


@pytest.mark.integration
class TestE2EResume:
    def test_e2e_rerun_tasks_autodetect(self, claude_shim, real_release):
        """AC-2 / AC-9: bare ``rerun-tasks <index>`` auto-detects phase 1 +
        T01.02 and re-runs ONLY it, refreshing canonical status to pass."""
        config, index = real_release
        _run_until_interrupted(config, claude_shim)

        claude_shim.set_failures()  # shim passes everything on the rerun
        with (
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.rerun_tasks.subprocess.run"),
            patch("superclaude.cli.sprint.summarizer.invoke_sonnet", return_value=""),
        ):
            result = CliRunner().invoke(sprint_group, ["rerun-tasks", str(index)])

        assert result.exit_code == 0, result.output
        assert "Auto-detected rerun target: phase 1, tasks T01.02" in result.output
        # Only T01.02 re-executed.
        assert claude_shim.run_log() == ["T01.02"]
        # Canonical status refreshed to pass via merge-back.
        merged = _status_by_id(_phase1_result(config.results_dir))
        assert merged["T01.02"] == "pass"
        assert merged["T01.01"] == "pass"
        assert merged["T01.03"] == "pass"

    def test_e2e_run_autodetect_task_level(self, claude_shim, real_release):
        """AC-1: bare ``sprint run <index>`` auto-resumes the interrupted release
        (gate validates the last-completed task first), dispatches the task-level
        path, and refreshes canonical T01.02 to pass."""
        config, index = real_release
        _run_until_interrupted(config, claude_shim)

        claude_shim.set_failures()
        with (
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.rerun_tasks.subprocess.run"),
            patch("superclaude.cli.sprint.summarizer.invoke_sonnet", return_value=""),
        ):
            result = CliRunner().invoke(
                sprint_group, ["run", str(index), "--yes", "--no-tmux"]
            )

        assert result.exit_code == 0, result.output
        assert claude_shim.run_log() == ["T01.02"]
        merged = _status_by_id(_phase1_result(config.results_dir))
        assert merged["T01.02"] == "pass"
        assert merged["T01.01"] == "pass"
        assert merged["T01.03"] == "pass"

    def test_e2e_hard_crash_phase_level(self, claude_shim, real_release):
        """AC-3: a hard crash (no result.json, no transcripts, dangling
        phase_start) drives PHASE-granularity resume — the whole boundary phase
        re-runs via ``sprint run``."""
        config, index = real_release
        _run_until_interrupted(config, claude_shim)
        results_dir = config.results_dir

        # Simulate a hard crash that left NO per-task data: remove result.json and
        # every per-task transcript, and leave only a dangling phase_start.
        (results_dir / "phase-1-result.json").unlink()
        for transcript in results_dir.glob("phase-1-task-*"):
            transcript.unlink()
        config.execution_log_jsonl.write_text(
            json.dumps({"event": "phase_start", "phase": 1}) + "\n",
            encoding="utf-8",
        )

        claude_shim.set_failures()  # everything passes on the phase re-run
        with (
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.summarizer.invoke_sonnet", return_value=""),
        ):
            result = CliRunner().invoke(
                sprint_group, ["run", str(index), "--yes", "--no-tmux"]
            )

        assert result.exit_code == 0, result.output
        # PHASE-level resume re-ran the WHOLE phase (all three tasks).
        rerun_log = sorted(claude_shim.run_log())
        assert rerun_log == ["T01.01", "T01.02", "T01.03"]
        merged = _status_by_id(_phase1_result(results_dir))
        assert merged["T01.01"] == "pass"
        assert merged["T01.02"] == "pass"
        assert merged["T01.03"] == "pass"
