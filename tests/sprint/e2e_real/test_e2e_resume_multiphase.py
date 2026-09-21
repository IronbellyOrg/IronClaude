"""E2E (real ``claude`` subprocess) — multi-phase auto-resume default.

This test builds its own two-phase release to prove that bare ``sprint run``
resumes at TASK granularity across a phase boundary: completed phase-1 tasks and
the already-passed phase-2 task are not re-executed; only the failed boundary
task is rerun and merged back into canonical result JSON.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.sprint.config import load_sprint_config

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
