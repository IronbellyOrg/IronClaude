"""T07.08 / FR-005 -- ``superclaude swarm kill`` subcommand.

Covers roadmap row R-124 (FR-005). Pins the operator-visible contract
of ``cli/swarm/commands.py::kill_cmd``:

1. Registered with ``swarm_group`` under the ``kill`` name (replaces
   the T01.08 placeholder).
2. Accepts a positional ``JOB_ID`` and an optional ``--output DIR``.
3. Behaviour:

       * Terminates the live ``swarm-<JOB_ID>`` tmux session via
         :func:`tmux.kill`.
       * When ``--output`` is supplied, writes a terminal-state
         ``.swarm-state.json`` AND emits ``done.json`` carrying
         ``terminal_status: killed``. Both writes are atomic
         (tmp + ``os.replace``).
       * Idempotent: a second invocation against the same job_id is a
         clean no-op (tmux session already gone, done.json already on
         disk) and still exits 0.

4. Exit codes:

       * 0  -- session terminated cleanly OR no session was present
               (the AC "Idempotent (kill twice no-op)" branch).
       * 2  -- usage error: tmux missing on PATH, JOB_ID carries
               tmux-illegal characters, or ``--output`` references a
               non-directory.

5. The tmux integration is monkeypatched in the live tests so the
   suite never spawns a real session; the live-tmux branch is gated
   on ``shutil.which('tmux')``.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.swarm import swarm_group
from superclaude.cli.swarm import tmux as swarm_tmux
from superclaude.cli.swarm.commands import (
    DONE_SENTINEL_FILENAME,
    EXIT_OK,
    EXIT_USAGE,
    KILLED_TERMINAL_STATUS,
    SWARM_STATE_FILENAME,
    kill_cmd,
)
from superclaude.cli.swarm.models import SwarmState
from superclaude.cli.swarm.state import read_state, write_state

TMUX_PRESENT = shutil.which("tmux") is not None
requires_tmux = pytest.mark.skipif(
    not TMUX_PRESENT,
    reason="tmux binary not installed; detached swarm mode unavailable",
)


# ---------------------------------------------------------------------------
# Registration -- AC-002 / T01.08 placeholder replacement.
# ---------------------------------------------------------------------------


def test_kill_cmd_registered_with_swarm_group() -> None:
    """``kill`` is bound on swarm_group to the concrete command."""
    assert "kill" in swarm_group.commands
    assert swarm_group.commands["kill"] is kill_cmd


def test_kill_help_advertises_job_id_argument() -> None:
    """``--help`` documents the positional JOB_ID and ``--output``."""
    runner = CliRunner()
    result = runner.invoke(swarm_group, ["kill", "--help"])
    assert result.exit_code == 0, result.output
    assert "JOB_ID" in result.output
    assert "--output" in result.output


# ---------------------------------------------------------------------------
# Usage-error paths -- EXIT_USAGE.
# ---------------------------------------------------------------------------


def test_kill_rejects_missing_argument() -> None:
    """Missing JOB_ID is a Click usage error (exit 2)."""
    runner = CliRunner()
    result = runner.invoke(swarm_group, ["kill"])
    # Click's own usage-error exit code is also 2.
    assert result.exit_code == 2, result.output


def test_kill_rejects_tmux_illegal_job_id() -> None:
    """A JOB_ID containing tmux-illegal chars exits EXIT_USAGE."""
    runner = CliRunner()
    result = runner.invoke(swarm_group, ["kill", "bad:job"])
    assert result.exit_code == EXIT_USAGE, result.output
    assert "invalid job_id" in result.stderr


def test_kill_tmux_unavailable_exits_usage(monkeypatch) -> None:
    """tmux missing on PATH yields EXIT_USAGE with a clear stderr line."""
    monkeypatch.setattr(swarm_tmux, "is_tmux_available", lambda: False)
    runner = CliRunner()
    result = runner.invoke(swarm_group, ["kill", "job-x"])
    assert result.exit_code == EXIT_USAGE, result.output
    assert "tmux is not available" in result.stderr


# ---------------------------------------------------------------------------
# Happy path -- live session terminated, exit 0.
# ---------------------------------------------------------------------------


def test_kill_present_session_calls_tmux_kill(monkeypatch) -> None:
    """When session exists, kill delegates to tmux.kill and exits 0."""
    calls: list[str] = []
    monkeypatch.setattr(swarm_tmux, "is_tmux_available", lambda: True)

    def _fake_kill(job_id: str) -> bool:
        calls.append(job_id)
        return True

    monkeypatch.setattr(swarm_tmux, "kill", _fake_kill)

    runner = CliRunner()
    result = runner.invoke(swarm_group, ["kill", "job-present"])
    assert result.exit_code == EXIT_OK, result.output
    assert calls == ["job-present"]
    assert "terminated tmux session" in result.stderr
    assert "job-present" in result.stderr


def test_kill_missing_session_is_graceful_no_op(monkeypatch) -> None:
    """No live session => exit 0 with a diagnostic on stderr (idempotent)."""
    monkeypatch.setattr(swarm_tmux, "is_tmux_available", lambda: True)
    monkeypatch.setattr(swarm_tmux, "kill", lambda _job_id: False)

    runner = CliRunner()
    result = runner.invoke(swarm_group, ["kill", "job-missing"])
    assert result.exit_code == EXIT_OK, result.output
    assert "no live tmux session" in result.stderr
    assert "job-missing" in result.stderr


# ---------------------------------------------------------------------------
# Terminal-state writes -- --output supplied.
# ---------------------------------------------------------------------------


def _patch_tmux_killed(monkeypatch, killed: bool = True) -> None:
    monkeypatch.setattr(swarm_tmux, "is_tmux_available", lambda: True)
    monkeypatch.setattr(swarm_tmux, "kill", lambda _job_id: killed)


def test_kill_writes_terminal_state_and_done_sentinel(
    tmp_path: Path, monkeypatch
) -> None:
    """With ``--output``, write .swarm-state.json terminal + done.json killed."""
    _patch_tmux_killed(monkeypatch, killed=True)

    # Seed a mid-flight state so the kill flips it to terminal.
    write_state(
        tmp_path / SWARM_STATE_FILENAME,
        SwarmState(state="dispatching", job_id="job-k"),
    )

    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        ["kill", "job-k", "--output", str(tmp_path)],
    )
    assert result.exit_code == EXIT_OK, result.output

    # State flipped to terminal, job_id preserved.
    state = read_state(tmp_path / SWARM_STATE_FILENAME)
    assert state is not None
    assert state.state == "terminal"
    assert state.job_id == "job-k"

    # done.json carries terminal_status="killed".
    done_path = tmp_path / DONE_SENTINEL_FILENAME
    assert done_path.is_file()
    payload = json.loads(done_path.read_text(encoding="utf-8"))
    assert payload["terminal_status"] == KILLED_TERMINAL_STATUS == "killed"
    assert payload["atomic_write"] is True
    # contract_path is "" for killed runs (no return contract to point at).
    assert payload["contract_path"] == ""


def test_kill_creates_state_when_absent(tmp_path: Path, monkeypatch) -> None:
    """If state file is missing, kill writes a terminal-state stub."""
    _patch_tmux_killed(monkeypatch, killed=True)

    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        ["kill", "job-fresh", "--output", str(tmp_path)],
    )
    assert result.exit_code == EXIT_OK, result.output

    state = read_state(tmp_path / SWARM_STATE_FILENAME)
    assert state is not None
    assert state.state == "terminal"
    assert state.job_id == "job-fresh"


def test_kill_writes_done_sentinel_when_no_session(tmp_path: Path, monkeypatch) -> None:
    """Even with no tmux session, ``--output`` still gets the killed sentinel.

    This pins the AC "Idempotent (kill twice no-op)" branch: a re-invocation
    after the session is gone must still leave the four-artifact
    observability set in a consistent killed-terminal shape.
    """
    _patch_tmux_killed(monkeypatch, killed=False)

    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        ["kill", "job-gone", "--output", str(tmp_path)],
    )
    assert result.exit_code == EXIT_OK, result.output

    done_path = tmp_path / DONE_SENTINEL_FILENAME
    assert done_path.is_file()
    payload = json.loads(done_path.read_text(encoding="utf-8"))
    assert payload["terminal_status"] == "killed"


def test_kill_is_idempotent_second_invocation_no_op(
    tmp_path: Path, monkeypatch
) -> None:
    """Calling kill twice must not corrupt state or change the sentinel."""
    _patch_tmux_killed(monkeypatch, killed=True)

    runner = CliRunner()
    first = runner.invoke(
        swarm_group,
        ["kill", "job-twice", "--output", str(tmp_path)],
    )
    assert first.exit_code == EXIT_OK, first.output

    done_path = tmp_path / DONE_SENTINEL_FILENAME
    first_payload = done_path.read_bytes()

    # Second call: tmux session is now gone.
    _patch_tmux_killed(monkeypatch, killed=False)
    second = runner.invoke(
        swarm_group,
        ["kill", "job-twice", "--output", str(tmp_path)],
    )
    assert second.exit_code == EXIT_OK, second.output

    # done.json content unchanged (writer is idempotent when target exists).
    assert done_path.read_bytes() == first_payload

    state = read_state(tmp_path / SWARM_STATE_FILENAME)
    assert state is not None
    assert state.state == "terminal"
    assert state.job_id == "job-twice"


def test_kill_rejects_output_that_is_a_file(tmp_path: Path, monkeypatch) -> None:
    """``--output`` pointing at a regular file is a usage error."""
    _patch_tmux_killed(monkeypatch, killed=True)
    not_a_dir = tmp_path / "regular.txt"
    not_a_dir.write_text("x", encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        ["kill", "job-x", "--output", str(not_a_dir)],
    )
    # Click's path-type guard raises a usage error (exit 2) before kill_cmd
    # runs; either Click's own 2 or our EXIT_USAGE is acceptable.
    assert result.exit_code == 2, result.output


def test_kill_creates_output_dir_when_missing(tmp_path: Path, monkeypatch) -> None:
    """``--output`` path that does not yet exist is materialised."""
    _patch_tmux_killed(monkeypatch, killed=True)
    target = tmp_path / "nested" / "out"
    assert not target.exists()

    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        ["kill", "job-mkdir", "--output", str(target)],
    )
    assert result.exit_code == EXIT_OK, result.output
    assert (target / SWARM_STATE_FILENAME).is_file()
    assert (target / DONE_SENTINEL_FILENAME).is_file()


# ---------------------------------------------------------------------------
# Race-condition paths -- tmux state shifts between probes.
# ---------------------------------------------------------------------------


def test_kill_handles_tmux_unavailable_race(monkeypatch) -> None:
    """If tmux disappears between availability check and kill, EXIT_USAGE."""
    monkeypatch.setattr(swarm_tmux, "is_tmux_available", lambda: True)

    def _raise_unavailable(_job_id: str) -> bool:
        raise swarm_tmux.TmuxUnavailableError("tmux vanished")

    monkeypatch.setattr(swarm_tmux, "kill", _raise_unavailable)

    runner = CliRunner()
    result = runner.invoke(swarm_group, ["kill", "job-x"])
    assert result.exit_code == EXIT_USAGE, result.output
    assert "tmux vanished" in result.stderr


# ---------------------------------------------------------------------------
# Atomic-write contract -- IMM-6.
# ---------------------------------------------------------------------------


def test_kill_done_sentinel_uses_os_replace(tmp_path: Path, monkeypatch) -> None:
    """The done.json writer must leave no .tmp residue after success."""
    _patch_tmux_killed(monkeypatch, killed=True)

    runner = CliRunner()
    result = runner.invoke(
        swarm_group,
        ["kill", "job-atomic", "--output", str(tmp_path)],
    )
    assert result.exit_code == EXIT_OK, result.output

    # No leftover tmp file from the atomic-replace sequence.
    leftovers = list(tmp_path.glob(f"{DONE_SENTINEL_FILENAME}.tmp*"))
    assert leftovers == [], f"unexpected tmp residue: {leftovers}"


# ---------------------------------------------------------------------------
# Live tmux gate -- exercises the real availability probe.
# ---------------------------------------------------------------------------


@requires_tmux
def test_kill_live_tmux_missing_session_is_graceful() -> None:
    """With tmux installed but no matching session, exit 0 gracefully.

    Does NOT monkeypatch ``is_tmux_available`` / ``kill`` -- the real probes
    run against the live tmux binary. The job_id is unique so no prior test
    run could have left a stray session behind.
    """
    import uuid

    job_id = f"kill-live-{uuid.uuid4().hex[:10]}"
    runner = CliRunner()
    result = runner.invoke(swarm_group, ["kill", job_id])
    assert result.exit_code == EXIT_OK, result.output
    assert "no live tmux session" in result.stderr
