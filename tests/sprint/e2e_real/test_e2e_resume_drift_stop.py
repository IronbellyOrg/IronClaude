"""E2E (real ``claude`` subprocess) — auto-resume material-drift STOP.

Validates AC-5 end-to-end through the real CLI: after an interrupted sprint,
a material operator edit that removes a completed task id from the boundary
tasklist must stop before dispatching any rerun task.
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
    initial_result = _phase1_result(config.results_dir)
    initial = _status_by_id(initial_result)
    assert initial["T01.02"] == "fail_recoverable"
    assert initial["T01.01"] == "pass"
    assert initial["T01.03"] == "pass"
    assert initial_result.get("tasklist_sha256")


@pytest.mark.integration
class TestE2EResumeDriftStop:
    def test_e2e_run_stops_on_material_tasklist_drift(self, claude_shim, real_release):
        """AC-5: material drift stops auto-resume before any task dispatch."""
        config, index = real_release
        _run_until_interrupted(config, claude_shim)
        before_resume_result = _phase1_result(config.results_dir)

        tasklist_path = config.release_dir / "phase-1-tasklist.md"
        original_tasklist = tasklist_path.read_text(encoding="utf-8")
        tasklist_path.write_text(
            original_tasklist.replace(
                "### T01.01 -- First task", "### T01.09 -- Renamed task"
            ),
            encoding="utf-8",
        )

        claude_shim.set_failures()
        with (
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.summarizer.invoke_sonnet", return_value=""),
        ):
            result = CliRunner().invoke(
                sprint_group, ["run", str(index), "--yes", "--no-tmux"]
            )

        assert result.exit_code != 0, result.output
        output = result.output.lower()
        assert "drift" in output
        assert "confidence" in output
        assert "--start" in output or "--fresh" in output
        assert claude_shim.run_log() == []
        assert _phase1_result(config.results_dir) == before_resume_result
