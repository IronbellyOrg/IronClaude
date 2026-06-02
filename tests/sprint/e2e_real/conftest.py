"""Fixtures for the real-``claude``-subprocess sprint rerun e2e harness.

These fixtures stand up the two things the harness needs to exercise the
*unmocked* spawn → stdin-prompt → stdout-capture → on-disk-merge chain:

1. ``claude_shim`` — installs ``fake_claude.py`` as a real executable named
   ``claude`` on ``$PATH`` (NO ``shutil.which`` / ``subprocess.Popen`` mock),
   and hands back a small handle for driving its JSON control file (which task
   ids fail this run, and the per-task run counter).

2. ``real_release`` — seeds a minimal but *real* sprint release layout under
   ``tmp_path`` (a ``tasklist-index.md`` + a per-task ``phase-1-tasklist.md``
   with three ``### T01.NN`` task blocks) and returns the loaded
   ``SprintConfig``. The phase file uses per-task headings so the executor
   takes the ``execute_phase_tasks`` per-task path that rerun-tasks targets.
"""

from __future__ import annotations

import json
import os
import shutil
import stat
from dataclasses import dataclass
from pathlib import Path

import pytest

_SHIM_SOURCE = Path(__file__).parent / "fake_claude.py"

# Three real per-task headings; T01.02 is the one the harness fails on run #1.
_PHASE_1_TASKLIST = """# Phase 1: Real Subprocess Harness

| Field | Value |
|---|---|

## Tasks

### T01.01 -- First task

**Dependencies:** none

Body for T01.01.

### T01.02 -- Second task (transient fail on first run)

**Dependencies:** none

Body for T01.02.

### T01.03 -- Third task

**Dependencies:** none

Body for T01.03.
"""

_INDEX = (
    "# TASKLIST INDEX\n"
    "\n"
    "## Phase Files\n"
    "\n"
    "| Phase | File | Phase Name |\n"
    "|---|---|---|\n"
    "| 1 | phase-1-tasklist.md | Real Subprocess Harness |\n"
)


@dataclass
class ShimHandle:
    """Drive the deterministic ``claude`` shim's JSON control file."""

    bin_dir: Path
    control_path: Path

    def set_failures(self, *task_ids: str) -> None:
        """Configure which task ids fail (transiently) on the next run(s).

        Resets the per-task run counter / run-log so a fresh phase of the
        scenario can assert cleanly on what executed.
        """
        self.control_path.write_text(
            json.dumps(
                {"fail_tasks": list(task_ids), "runs": {}, "run_log": []}, indent=2
            ),
            encoding="utf-8",
        )

    def control(self) -> dict:
        try:
            return json.loads(self.control_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}

    def runs(self) -> dict:
        return self.control().get("runs", {})

    def run_log(self) -> list[str]:
        return self.control().get("run_log", [])


@pytest.fixture
def claude_shim(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> ShimHandle:
    """Install ``fake_claude.py`` as an executable ``claude`` on ``$PATH``.

    The executor's ``shutil.which("claude")`` then resolves THIS file and
    ``subprocess.Popen`` spawns it for real — no mock involved.
    """
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    shim_dst = bin_dir / "claude"
    shutil.copy2(_SHIM_SOURCE, shim_dst)
    mode = shim_dst.stat().st_mode
    shim_dst.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    control_path = tmp_path / "fake_claude_control.json"
    control_path.write_text(
        json.dumps({"fail_tasks": [], "runs": {}, "run_log": []}, indent=2),
        encoding="utf-8",
    )

    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    monkeypatch.setenv("FAKE_CLAUDE_CONTROL", str(control_path))

    handle = ShimHandle(bin_dir=bin_dir, control_path=control_path)
    # Sanity: confirm the real PATH resolution lands on our shim before any
    # test relies on it (this is the property the harness exists to prove).
    assert shutil.which("claude") == str(shim_dst)
    return handle


@pytest.fixture
def real_release(tmp_path: Path):
    """Seed a real per-task sprint release and return its loaded SprintConfig."""
    from superclaude.cli.sprint.config import load_sprint_config

    release = tmp_path / "release"
    release.mkdir(parents=True, exist_ok=True)
    (release / "phase-1-tasklist.md").write_text(_PHASE_1_TASKLIST, encoding="utf-8")
    index = release / "tasklist-index.md"
    index.write_text(_INDEX, encoding="utf-8")

    config = load_sprint_config(index)
    return config, index
