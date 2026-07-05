"""T07.07 / FR-004 -- ``superclaude swarm attach`` subcommand.

Covers roadmap row R-123 (FR-004). Pins the operator-visible contract
of ``cli/swarm/commands.py::attach_cmd``:

1. Registered with ``swarm_group`` under the ``attach`` name (replaces
   the T01.08 placeholder).
2. Accepts a positional ``JOB_ID`` and runs ``tmux attach-session -t
   swarm-<JOB_ID>`` after validating the session exists.
3. Exit codes:

       * 0 -- attached cleanly OR no live session present (graceful
         no-op per the AC "exits gracefully if no detached session
         present").
       * 2 -- usage error: tmux unavailable or malformed JOB_ID.
       * propagated -- the tmux subprocess return code is forwarded
         when attach itself returns non-zero.

4. The tmux integration is monkeypatched in the live tests so the
   suite never blocks on a real PTY; the real tmux binary check is
   exercised by the ``requires_tmux``-gated branch.
"""

from __future__ import annotations

import shutil

import pytest
from click.testing import CliRunner

from superclaude.cli.swarm import swarm_group
from superclaude.cli.swarm import tmux as swarm_tmux
from superclaude.cli.swarm.commands import (
    EXIT_OK,
    EXIT_USAGE,
    attach_cmd,
)

TMUX_PRESENT = shutil.which("tmux") is not None
requires_tmux = pytest.mark.skipif(
    not TMUX_PRESENT,
    reason="tmux binary not installed; detached swarm mode unavailable",
)


# ---------------------------------------------------------------------------
# Registration -- AC-002 / T01.08 placeholder replacement.
# ---------------------------------------------------------------------------


def test_attach_cmd_registered_with_swarm_group() -> None:
    """``attach`` is bound on swarm_group to the concrete command."""
    assert "attach" in swarm_group.commands
    assert swarm_group.commands["attach"] is attach_cmd


def test_attach_help_advertises_job_id_argument() -> None:
    """``--help`` documents the positional JOB_ID argument."""
    runner = CliRunner()
    result = runner.invoke(swarm_group, ["attach", "--help"])
    assert result.exit_code == 0, result.output
    assert "JOB_ID" in result.output


# ---------------------------------------------------------------------------
# Usage-error paths -- EXIT_USAGE.
# ---------------------------------------------------------------------------


def test_attach_rejects_missing_argument() -> None:
    """Missing JOB_ID is a Click usage error (exit 2)."""
    runner = CliRunner()
    result = runner.invoke(swarm_group, ["attach"])
    # Click's own usage-error exit code is also 2 -- the test pins
    # rejection without distinguishing it from EXIT_USAGE.
    assert result.exit_code == 2, result.output


def test_attach_rejects_tmux_illegal_job_id() -> None:
    """A JOB_ID containing tmux-illegal chars exits EXIT_USAGE."""
    runner = CliRunner()
    result = runner.invoke(swarm_group, ["attach", "bad:job"])
    assert result.exit_code == EXIT_USAGE, result.output
    assert "invalid job_id" in result.stderr


def test_attach_tmux_unavailable_exits_usage(monkeypatch) -> None:
    """tmux missing on PATH yields EXIT_USAGE with a clear stderr line."""
    monkeypatch.setattr(swarm_tmux, "is_tmux_available", lambda: False)
    runner = CliRunner()
    result = runner.invoke(swarm_group, ["attach", "job-x"])
    assert result.exit_code == EXIT_USAGE, result.output
    assert "tmux is not available" in result.stderr


# ---------------------------------------------------------------------------
# Graceful no-op -- missing session exits 0 with a diagnostic on stderr.
# ---------------------------------------------------------------------------


def test_attach_missing_session_exits_zero_gracefully(monkeypatch) -> None:
    """No live ``swarm-<id>`` session -> exit 0, stderr explains."""
    monkeypatch.setattr(swarm_tmux, "is_tmux_available", lambda: True)
    monkeypatch.setattr(swarm_tmux, "has_session", lambda _job_id: False)

    def _attach_should_not_run(_job_id: str) -> int:  # pragma: no cover
        raise AssertionError(
            "tmux.attach must not be invoked when has_session is False"
        )

    monkeypatch.setattr(swarm_tmux, "attach", _attach_should_not_run)

    runner = CliRunner()
    result = runner.invoke(swarm_group, ["attach", "job-missing"])
    assert result.exit_code == EXIT_OK, result.output
    assert "no live tmux session" in result.stderr
    assert "job-missing" in result.stderr


# ---------------------------------------------------------------------------
# Happy path -- attach succeeds, return code propagates.
# ---------------------------------------------------------------------------


def test_attach_present_session_calls_tmux_attach(monkeypatch) -> None:
    """When session exists, attach delegates to tmux.attach and returns its rc."""
    calls: list[str] = []
    monkeypatch.setattr(swarm_tmux, "is_tmux_available", lambda: True)
    monkeypatch.setattr(swarm_tmux, "has_session", lambda _job_id: True)

    def _fake_attach(job_id: str) -> int:
        calls.append(job_id)
        return 0

    monkeypatch.setattr(swarm_tmux, "attach", _fake_attach)

    runner = CliRunner()
    result = runner.invoke(swarm_group, ["attach", "job-present"])
    assert result.exit_code == EXIT_OK, result.output
    assert calls == ["job-present"]


def test_attach_propagates_non_zero_tmux_return_code(monkeypatch) -> None:
    """A non-zero tmux attach return code is forwarded verbatim."""
    monkeypatch.setattr(swarm_tmux, "is_tmux_available", lambda: True)
    monkeypatch.setattr(swarm_tmux, "has_session", lambda _job_id: True)
    monkeypatch.setattr(swarm_tmux, "attach", lambda _job_id: 7)

    runner = CliRunner()
    result = runner.invoke(swarm_group, ["attach", "job-busted"])
    assert result.exit_code == 7, result.output


# ---------------------------------------------------------------------------
# Race-condition paths -- tmux state shifts between probe and attach.
# ---------------------------------------------------------------------------


def test_attach_handles_session_missing_race(monkeypatch) -> None:
    """If session evaporates between has_session and attach, exit 0."""
    monkeypatch.setattr(swarm_tmux, "is_tmux_available", lambda: True)
    monkeypatch.setattr(swarm_tmux, "has_session", lambda _job_id: True)

    def _raise_missing(_job_id: str) -> int:
        raise swarm_tmux.TmuxSessionMissingError(
            f"no live tmux session for job_id={_job_id!r}"
        )

    monkeypatch.setattr(swarm_tmux, "attach", _raise_missing)

    runner = CliRunner()
    result = runner.invoke(swarm_group, ["attach", "job-race"])
    assert result.exit_code == EXIT_OK, result.output
    assert "no live tmux session" in result.stderr


def test_attach_handles_tmux_unavailable_race(monkeypatch) -> None:
    """If tmux disappears between availability check and attach, EXIT_USAGE."""
    monkeypatch.setattr(swarm_tmux, "is_tmux_available", lambda: True)
    monkeypatch.setattr(swarm_tmux, "has_session", lambda _job_id: True)

    def _raise_unavailable(_job_id: str) -> int:
        raise swarm_tmux.TmuxUnavailableError("tmux vanished")

    monkeypatch.setattr(swarm_tmux, "attach", _raise_unavailable)

    runner = CliRunner()
    result = runner.invoke(swarm_group, ["attach", "job-x"])
    assert result.exit_code == EXIT_USAGE, result.output
    assert "tmux vanished" in result.stderr


# ---------------------------------------------------------------------------
# Live tmux gate -- exercises the real availability probe.
# ---------------------------------------------------------------------------


@requires_tmux
def test_attach_live_tmux_missing_session_is_graceful(monkeypatch) -> None:
    """With tmux installed but no matching session, exit 0 gracefully.

    Does NOT monkeypatch ``is_tmux_available`` / ``has_session`` -- the
    real probes run against the live tmux binary. The job_id is unique
    so no prior test run could have left a stray session behind.
    """
    import uuid

    job_id = f"attach-live-{uuid.uuid4().hex[:10]}"
    runner = CliRunner()
    result = runner.invoke(swarm_group, ["attach", job_id])
    assert result.exit_code == EXIT_OK, result.output
    assert "no live tmux session" in result.stderr
