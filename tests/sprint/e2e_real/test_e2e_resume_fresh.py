"""E2E (real ``claude`` subprocess) — ``sprint run --fresh`` opt-out.

Contrasts the v4.3.5 auto-resume default with the explicit ``--fresh`` escape
hatch. Both tests start from the same real interrupted sprint state where T01.02
is ``fail_recoverable`` on disk. ``--fresh`` must ignore that auto-resume target
and execute the whole phase from scratch; bare ``sprint run`` must auto-resume
only T01.02.
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
class TestE2EResumeFresh:
    def test_e2e_run_fresh_disables_autoresume(self, claude_shim, real_release):
        """``--fresh`` opts out of task-level auto-resume and re-runs phase 1."""
        config, index = real_release
        _run_until_interrupted(config, claude_shim)

        claude_shim.set_failures()  # shim passes everything on the fresh run
        with (
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.summarizer.invoke_sonnet", return_value=""),
        ):
            result = CliRunner().invoke(
                sprint_group, ["run", str(index), "--fresh", "--no-tmux"]
            )

        assert result.exit_code == 0, result.output
        assert sorted(claude_shim.run_log()) == ["T01.01", "T01.02", "T01.03"]
        merged = _status_by_id(_phase1_result(config.results_dir))
        assert merged["T01.01"] == "pass"
        assert merged["T01.02"] == "pass"
        assert merged["T01.03"] == "pass"

    def test_e2e_run_autoresume_without_fresh_reexecutes_only_failed_task(
        self, claude_shim, real_release
    ):
        """Bare ``sprint run`` auto-resumes only T01.02 from the same state."""
        config, index = real_release
        _run_until_interrupted(config, claude_shim)

        claude_shim.set_failures()  # shim passes everything on the rerun
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
        assert merged["T01.01"] == "pass"
        assert merged["T01.02"] == "pass"
        assert merged["T01.03"] == "pass"
