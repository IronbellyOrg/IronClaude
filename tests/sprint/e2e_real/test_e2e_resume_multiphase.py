"""E2E (real ``claude`` subprocess) — multi-phase auto-resume default.

This test builds its own two-phase release to prove that bare ``sprint run``
resumes at TASK granularity across a phase boundary: completed phase-1 tasks and
the already-passed phase-2 task are not re-executed; only the failed boundary
task is rerun and merged back into canonical result JSON.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from superclaude.cli.sprint.commands import sprint_group
from superclaude.cli.sprint.config import load_sprint_config
from superclaude.cli.sprint.executor import execute_sprint

_PHASE_1_TASKLIST = """# Phase 1: Multi-phase Resume Harness

| Field | Value |
|---|---|

## Tasks

### T01.01 -- First phase first task

**Dependencies:** none

Body for T01.01.

### T01.02 -- First phase second task

**Dependencies:** none

Body for T01.02.
"""

_PHASE_2_TASKLIST = """# Phase 2: Multi-phase Resume Boundary

| Field | Value |
|---|---|

## Tasks

### T02.01 -- Second phase first task

**Dependencies:** none

Body for T02.01.

### T02.02 -- Second phase transient task

**Dependencies:** none

Body for T02.02.
"""

_INDEX = (
    "# TASKLIST INDEX\n"
    "\n"
    "## Phase Files\n"
    "\n"
    "| Phase | File | Phase Name |\n"
    "|---|---|---|\n"
    "| 1 | phase-1-tasklist.md | Multi-phase Resume Harness |\n"
    "| 2 | phase-2-tasklist.md | Multi-phase Resume Boundary |\n"
)


def _status_by_id(result_json: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for task_result in result_json.get("task_results", []):
        task_id = task_result.get("task", {}).get("task_id")
        if task_id:
            out[task_id] = task_result.get("status")
    return out


def _read_result(results_dir: Path, phase: int) -> dict:
    return json.loads(
        (results_dir / f"phase-{phase}-result.json").read_text(encoding="utf-8")
    )


@pytest.fixture
def two_phase_release(tmp_path: Path):
    release = tmp_path / "release"
    release.mkdir(parents=True, exist_ok=True)
    (release / "phase-1-tasklist.md").write_text(_PHASE_1_TASKLIST, encoding="utf-8")
    (release / "phase-2-tasklist.md").write_text(_PHASE_2_TASKLIST, encoding="utf-8")
    index = release / "tasklist-index.md"
    index.write_text(_INDEX, encoding="utf-8")

    config = load_sprint_config(index)
    return config, index


@pytest.mark.integration
def test_e2e_run_autodetect_task_level_across_phase_boundary(
    claude_shim, two_phase_release
):
    config, index = two_phase_release
    results_dir = config.results_dir

    claude_shim.set_failures("T02.02")
    with patch("superclaude.cli.sprint.notify._notify"):
        with pytest.raises(SystemExit) as exc_info:
            execute_sprint(config)
        assert exc_info.value.code == 1

    phase_1_path = results_dir / "phase-1-result.json"
    phase_2_path = results_dir / "phase-2-result.json"
    assert phase_1_path.exists()
    assert phase_2_path.exists()

    phase_1_before = phase_1_path.read_text(encoding="utf-8")
    phase_1_initial = _status_by_id(json.loads(phase_1_before))
    assert phase_1_initial["T01.01"] == "pass"
    assert phase_1_initial["T01.02"] == "pass"

    phase_2_initial = _status_by_id(_read_result(results_dir, 2))
    assert phase_2_initial["T02.01"] == "pass"
    assert phase_2_initial["T02.02"] == "fail_recoverable"

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
    assert claude_shim.run_log() == ["T02.02"]

    phase_2_merged = _status_by_id(_read_result(results_dir, 2))
    assert phase_2_merged["T02.01"] == "pass"
    assert phase_2_merged["T02.02"] == "pass"
    assert phase_1_path.read_text(encoding="utf-8") == phase_1_before
