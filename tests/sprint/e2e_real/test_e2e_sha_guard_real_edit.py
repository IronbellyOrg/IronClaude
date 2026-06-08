"""E2E-2 — real-subprocess proof of the rerun-tasks SHA mid-flight-edit guard.

This test proves the §T8.1 source-tasklist mid-flight-edit guard in
``rerun_tasks.run_rerun_tasks`` *discriminates* between two things that both
mutate the source ``phase-1-tasklist.md`` during a rerun:

  1. the ENGINE's own step-10 provenance write (the ``<!-- SUPERCLAUDE-RERUN -->``
     block) — which must NOT trip the guard, because the guard hashes the
     block-stripped content (``_content_sha256_excluding_rerun_block``); and
  2. a GENUINE operator edit to task content OUTSIDE that block — which MUST
     trip the guard, aborting the merge-back unless ``--force-merge`` is passed.

Like E2E-1 (``test_e2e_rerun_happy_path``) this runs the whole spawn → stdin →
stdout → on-disk-merge chain against a REAL ``claude`` shim installed on
``$PATH``; there is no ``subprocess.Popen`` / ``shutil.which`` mock. The only
environmental noise patched is ``notify._notify`` and the post-merge
``rerun_tasks.subprocess.run`` (the ``verify-checkpoints --recover`` auto-invoke).

The mid-flight edit is injected for real: a test-local shim
(``fake_claude_sourceedit.py``) appends a content line to the source tasklist
path (handed to it via ``$FAKE_CLAUDE_EDIT_PATH``) while it is executing the
rerun task — i.e. between the engine's step-4 SHA capture and its step-12
re-check. Test 1 reuses the shared ``conftest.claude_shim`` (no edit).
"""

from __future__ import annotations

import json
import os
import shutil
import stat
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from superclaude.cli.sprint.commands import sprint_group
from superclaude.cli.sprint.config import load_sprint_config
from superclaude.cli.sprint.executor import execute_sprint

# The byte-exact abort message run_rerun_tasks raises at step 12 (the substring
# we assert; the runtime message interpolates the bundle path into the middle).
_ABORT_HEAD = "Source tasklist modified since rerun started. Bundle "
_ABORT_TAIL = "To force, use --force-merge."

_EDIT_SHIM_SOURCE = Path(__file__).parent / "fake_claude_sourceedit.py"
_EDIT_MARKER = "<!-- operator edit -->"

_PHASE_1_TASKLIST = """# Phase 1: SHA Guard Harness

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
    "| 1 | phase-1-tasklist.md | SHA Guard Harness |\n"
)


def _load_phase1_result(results_dir: Path) -> dict:
    return json.loads((results_dir / "phase-1-result.json").read_text(encoding="utf-8"))


def _status_by_id(result_json: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for tr in result_json.get("task_results", []):
        tid = tr.get("task", {}).get("task_id")
        if tid:
            out[tid] = tr.get("status")
    return out


@dataclass
class EditShimRig:
    """A self-contained release + edit-capable ``claude`` shim on ``$PATH``."""

    config: object
    index: Path
    control_path: Path
    source_phase: Path

    def set_failures(self, *task_ids: str) -> None:
        self.control_path.write_text(
            json.dumps(
                {"fail_tasks": list(task_ids), "runs": {}, "run_log": []}, indent=2
            ),
            encoding="utf-8",
        )

    def run_log(self) -> list[str]:
        try:
            data = json.loads(self.control_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return []
        return data.get("run_log", [])


def _install_edit_rig(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> EditShimRig:
    """Stand up an isolated release and install the edit shim as ``claude``.

    Mirrors ``conftest.claude_shim`` + ``real_release`` but uses the test-local
    ``fake_claude_sourceedit.py`` so the harness can inject a mid-flight edit.
    No ``subprocess.Popen`` / ``shutil.which`` mock — real PATH resolution only.
    """
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    shim_dst = bin_dir / "claude"
    shutil.copy2(_EDIT_SHIM_SOURCE, shim_dst)
    mode = shim_dst.stat().st_mode
    shim_dst.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    control_path = tmp_path / "fake_claude_control.json"
    control_path.write_text(
        json.dumps({"fail_tasks": [], "runs": {}, "run_log": []}, indent=2),
        encoding="utf-8",
    )

    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    monkeypatch.setenv("FAKE_CLAUDE_CONTROL", str(control_path))

    release = tmp_path / "release"
    release.mkdir(parents=True, exist_ok=True)
    source_phase = release / "phase-1-tasklist.md"
    source_phase.write_text(_PHASE_1_TASKLIST, encoding="utf-8")
    index = release / "tasklist-index.md"
    index.write_text(_INDEX, encoding="utf-8")

    config = load_sprint_config(index)
    # The property the harness exists to prove: PATH resolves to OUR shim.
    assert shutil.which("claude") == str(shim_dst)
    return EditShimRig(
        config=config,
        index=index,
        control_path=control_path,
        source_phase=source_phase,
    )


def _seed_fail_recoverable(rig: EditShimRig) -> None:
    """Run the real sprint once so T01.02 lands as FAIL_RECOVERABLE on disk.

    The edit shim has no ``$FAKE_CLAUDE_EDIT_PATH`` set yet, so it behaves like
    the plain shim here (transient-fail T01.02, pass the neighbours).
    """
    rig.set_failures("T01.02")
    with patch("superclaude.cli.sprint.notify._notify"):
        with pytest.raises(SystemExit) as exc_info:
            execute_sprint(rig.config)
        assert exc_info.value.code == 1

    initial = _load_phase1_result(rig.config.results_dir)
    assert _status_by_id(initial).get("T01.02") == "fail_recoverable", (
        "setup precondition failed: T01.02 was not FAIL_RECOVERABLE after run 1"
    )


@pytest.mark.integration
class TestE2EShaGuardRealEdit:
    def test_no_false_trip_engine_provenance_write(self, claude_shim, real_release):
        """Negative half: the engine's own step-10 provenance write must NOT trip.

        A normal ``--merge-back`` rerun (no ``--force-merge``, no operator edit)
        completes cleanly. The block-stripped hash makes the guard blind to the
        ``<!-- SUPERCLAUDE-RERUN -->`` block the engine itself writes between the
        step-4 capture and the step-12 re-check.
        """
        config, index = real_release
        results_dir = config.results_dir

        # Run 1: real sprint; shim fails T01.02 transiently -> FAIL_RECOVERABLE.
        claude_shim.set_failures("T01.02")
        with patch("superclaude.cli.sprint.notify._notify"):
            with pytest.raises(SystemExit) as exc_info:
                execute_sprint(config)
            assert exc_info.value.code == 1

        initial = _load_phase1_result(results_dir)
        assert _status_by_id(initial).get("T01.02") == "fail_recoverable"

        # Run 2: real rerun; shim now passes T01.02. The ONLY source mutation is
        # the engine's provenance block — the guard must stay quiet.
        claude_shim.set_failures()  # no failures on the rerun
        runner = CliRunner()
        with (
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.rerun_tasks.subprocess.run"),
        ):
            result = runner.invoke(
                sprint_group,
                ["rerun-tasks", str(index), "--phase", "1", "--tasks", "T01.02"],
            )

        assert result.exit_code == 0, result.output
        assert "Rerun merged" in result.output
        assert "Source tasklist modified" not in result.output, (
            "engine's own provenance write FALSE-tripped the mid-flight guard"
        )

        # The provenance block was in fact written to the source (i.e. the guard
        # really did have a source mutation to ignore, not a vacuous pass).
        phase_text = (config.release_dir / "phase-1-tasklist.md").read_text(
            encoding="utf-8"
        )
        assert "SUPERCLAUDE-RERUN" in phase_text
        # And the canonical status was refreshed by the merge-back.
        assert _status_by_id(_load_phase1_result(results_dir)).get("T01.02") == "pass"

    def test_real_operator_edit_mid_flight_aborts(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """Positive half: a genuine operator edit mid-rerun MUST trip the guard.

        The edit shim appends a real content line to the source tasklist (outside
        the provenance block) WHILE executing the rerun task — between step-4 and
        step-12. The block-stripped hash changes -> step-12 aborts with the
        byte-exact message. Then ``--force-merge`` overrides the guard and merges.
        """
        # --- Abort scenario --------------------------------------------------
        rig = _install_edit_rig(tmp_path / "abort", monkeypatch)
        _seed_fail_recoverable(rig)

        # Arm the mid-flight edit: the shim will append to the SOURCE tasklist
        # while it runs the rerun task. (No failures this run -> T01.02 passes,
        # so the rerun "succeeds" and reaches the step-12 merge-back guard.)
        rig.set_failures()
        monkeypatch.setenv("FAKE_CLAUDE_EDIT_PATH", str(rig.source_phase))

        runner = CliRunner()
        with (
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.rerun_tasks.subprocess.run") as mock_verify,
        ):
            result = runner.invoke(
                sprint_group,
                ["rerun-tasks", str(rig.index), "--phase", "1", "--tasks", "T01.02"],
            )

        # The rerun re-executed the target (proving the shim ran, hence edited).
        assert rig.run_log() == ["T01.02"], rig.run_log()
        # The operator edit really landed in the source, outside the block.
        edited_text = rig.source_phase.read_text(encoding="utf-8")
        assert _EDIT_MARKER in edited_text, (
            "edit shim did not append the operator edit to the source tasklist"
        )

        # The guard tripped: non-zero exit + byte-exact abort message.
        assert result.exit_code != 0, result.output
        assert _ABORT_HEAD in result.output, result.output
        assert _ABORT_TAIL in result.output, result.output
        # Aborted BEFORE merge: the verify-checkpoints auto-invoke never fired.
        assert not mock_verify.called, (
            "verify-checkpoints fired despite the guard aborting the merge"
        )
        # The merge did NOT run: canonical T01.02 is still fail_recoverable.
        assert (
            _status_by_id(_load_phase1_result(rig.config.results_dir)).get("T01.02")
            == "fail_recoverable"
        ), "canonical status was refreshed despite the guard aborting"

        # --- --force-merge override scenario (fresh, isolated release) -------
        forced = _install_edit_rig(tmp_path / "forced", monkeypatch)
        _seed_fail_recoverable(forced)
        forced.set_failures()
        monkeypatch.setenv("FAKE_CLAUDE_EDIT_PATH", str(forced.source_phase))

        with (
            patch("superclaude.cli.sprint.notify._notify"),
            patch("superclaude.cli.sprint.rerun_tasks.subprocess.run"),
        ):
            forced_result = runner.invoke(
                sprint_group,
                [
                    "rerun-tasks",
                    str(forced.index),
                    "--phase",
                    "1",
                    "--tasks",
                    "T01.02",
                    "--force-merge",
                ],
            )

        # Same mid-flight edit landed...
        assert _EDIT_MARKER in forced.source_phase.read_text(encoding="utf-8")
        # ...but --force-merge overrides the guard and merges anyway.
        assert forced_result.exit_code == 0, forced_result.output
        assert "Rerun merged" in forced_result.output
        assert "Source tasklist modified" not in forced_result.output, (
            "--force-merge did not override the mid-flight-edit guard"
        )
        assert (
            _status_by_id(_load_phase1_result(forced.config.results_dir)).get("T01.02")
            == "pass"
        ), "--force-merge run did not refresh the canonical T01.02 status to pass"
