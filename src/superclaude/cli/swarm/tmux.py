"""Swarm tmux integration -- detachable session management.

Mirrors ``cli/sprint/tmux.py`` in role: provide tmux session lifecycle
helpers so ``superclaude swarm run --detached`` (RuntimeSpec.mode =
'detached', T07.11) can launch a background job and ``swarm attach`` /
``swarm kill`` (T07.07 / T07.08) can later reattach or terminate it.

Surface vs. sprint
==================

The sprint variant builds a 3-pane Rich/TUI layout because sprint
execution is an interactive operator surface (live phase summaries +
tail). Swarm detached mode is the opposite: the operator dispatches a
fan-out job, walks away, and reattaches only on demand. So this module
deliberately omits the pane-split / TUI machinery and ships a small set
of lifecycle primitives only:

* :func:`is_tmux_available` -- tmux installed AND we are NOT already
  inside an outer tmux session.
* :func:`session_name` -- deterministic ``swarm-<job_id>`` name derived
  from the JobSpec ``job_id`` (DM-001), validated for tmux-legal chars.
* :func:`has_session` -- live-session probe via ``tmux has-session``.
* :func:`launch_detached` -- ``tmux new-session -d -s swarm-<job_id> --
  <command...>``; survives caller exit (AC-008 / FR-014). Caller passes
  the swarm run argv (T07.11 wires this from ``run_cmd --detached``).
* :func:`attach` -- ``tmux attach-session -t swarm-<job_id>``; blocks
  until the operator detaches or the session ends.
* :func:`kill` -- ``tmux kill-session``; idempotent (kill-twice no-op
  per T07.08 AC).
* :func:`list_swarm_sessions` -- enumerate live ``swarm-*`` sessions
  for the M7 ``status`` surface (T07.04 may surface a fleet listing
  later; the helper exists now so attach/kill error messages can name
  what IS running when the target is missing).

Error contract
==============

* :class:`TmuxUnavailableError` -- tmux missing on PATH. Detached mode
  caller (T07.11) raises this to the user; inline-only fallback is
  documented in T07.17 (``docs/swarm/runbook.md``).
* :class:`TmuxSessionMissingError` -- attach/kill target has no live
  session. Distinct subclass of :class:`LookupError` so the M7
  subcommands (T07.07 / T07.08) can render a clean "no such job"
  message without confusing tmux-not-installed with job-not-running.

Both are raised eagerly; subprocess calls otherwise propagate their
return code so callers can map non-zero exits to operator-facing
errors without re-wrapping the whole subprocess module.

Atomicity
=========

This module does NOT touch ``.swarm-state.json`` / ``done.json``.
Terminal-state writes live in :mod:`superclaude.cli.swarm.reduce` and
the kill subcommand (T07.08) layers the ``done.json`` emission on top
of :func:`kill`. Keeping the tmux primitives free of state-file side
effects means the swarm reduce/state surface stays the single source
of truth for terminal status, and this module remains a thin shell
over tmux's own lifecycle.
"""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Sequence

SESSION_PREFIX = "swarm-"

__all__ = [
    "SESSION_PREFIX",
    "TmuxUnavailableError",
    "TmuxSessionMissingError",
    "is_tmux_available",
    "session_name",
    "has_session",
    "launch_detached",
    "attach",
    "kill",
    "list_swarm_sessions",
]


class TmuxUnavailableError(RuntimeError):
    """Raised when a tmux operation is attempted but tmux is unavailable."""


class TmuxSessionMissingError(LookupError):
    """Raised when attach/kill targets a job_id with no live tmux session."""


def is_tmux_available() -> bool:
    """Return True if tmux is installed and we are not nested inside tmux.

    Nested-session check mirrors the sprint variant: launching a
    detached session from inside another tmux session is technically
    legal but produces a confusing operator experience (the new session
    is hidden behind the current one) and is not part of the M7 detached
    contract. Callers wanting raw "is the binary on PATH" should test
    ``shutil.which('tmux')`` directly.
    """
    if shutil.which("tmux") is None:
        return False
    return "TMUX" not in os.environ


def session_name(job_id: str) -> str:
    """Return ``swarm-<job_id>`` after validating ``job_id`` characters.

    tmux rejects session names containing ``:`` (target separator) or
    ``.`` (window-pane separator). Whitespace is also blocked to keep
    shell command construction from getting subtly wrong.
    """
    if not job_id:
        raise ValueError("job_id must be a non-empty string")
    forbidden = {":", ".", " ", "\t", "\n", "\r"}
    bad = sorted(c for c in forbidden if c in job_id)
    if bad:
        raise ValueError(f"job_id {job_id!r} contains tmux-illegal characters: {bad!r}")
    return f"{SESSION_PREFIX}{job_id}"


def has_session(job_id: str) -> bool:
    """Return True if a live tmux session named ``swarm-<job_id>`` exists."""
    if shutil.which("tmux") is None:
        return False
    target = session_name(job_id)
    result = subprocess.run(
        ["tmux", "has-session", "-t", target],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def launch_detached(
    job_id: str,
    command: Sequence[str],
    *,
    cwd: Optional[Path] = None,
    env: Optional[dict[str, str]] = None,
) -> str:
    """Launch ``command`` inside a detached tmux session and return its name.

    The session is created with ``tmux new-session -d -s swarm-<job_id>``
    so it survives the caller's exit (AC-008 / FR-014). ``command`` is
    quoted via :mod:`shlex` and passed as a single shell string so
    argv-with-spaces survives tmux's own parsing.

    Raises:
        TmuxUnavailableError: tmux missing on PATH.
        RuntimeError: a session for this job_id is already running.
        ValueError: ``command`` is empty.
        subprocess.CalledProcessError: tmux exited non-zero.
    """
    if shutil.which("tmux") is None:
        raise TmuxUnavailableError(
            "tmux is not installed; detached swarm mode requires tmux"
        )
    if not command:
        raise ValueError("command must be a non-empty sequence")
    name = session_name(job_id)
    if has_session(job_id):
        raise RuntimeError(
            f"tmux session {name!r} already exists; refusing to overwrite"
        )
    argv: list[str] = ["tmux", "new-session", "-d", "-s", name]
    if cwd is not None:
        argv.extend(["-c", str(cwd)])
    shell_cmd = " ".join(shlex.quote(str(a)) for a in command)
    argv.append(shell_cmd)
    subprocess.run(argv, check=True, env=env)
    return name


def attach(job_id: str) -> int:
    """Interactively attach to ``swarm-<job_id>``; block until detach/exit.

    Returns the tmux subprocess return code. Raises
    :class:`TmuxUnavailableError` if tmux is missing and
    :class:`TmuxSessionMissingError` if no session exists for ``job_id``.
    """
    if shutil.which("tmux") is None:
        raise TmuxUnavailableError(
            "tmux is not installed; cannot attach to swarm session"
        )
    if not has_session(job_id):
        raise TmuxSessionMissingError(
            f"no live tmux session for job_id={job_id!r} "
            f"(looked for {session_name(job_id)!r})"
        )
    return subprocess.run(
        ["tmux", "attach-session", "-t", session_name(job_id)],
        check=False,
    ).returncode


def kill(job_id: str) -> bool:
    """Terminate the tmux session for ``job_id``; idempotent.

    Returns True if a session was killed, False if none existed.
    Raises :class:`TmuxUnavailableError` if tmux is missing -- callers
    invoking ``swarm kill`` on a host without tmux always indicates an
    operator mistake (the job could not have been launched detached).
    """
    if shutil.which("tmux") is None:
        raise TmuxUnavailableError("tmux is not installed; cannot kill swarm session")
    if not has_session(job_id):
        return False
    subprocess.run(
        ["tmux", "kill-session", "-t", session_name(job_id)],
        check=False,
    )
    return True


def list_swarm_sessions() -> list[str]:
    """Return all live tmux session names starting with ``swarm-``.

    Empty list when tmux is missing or no sessions exist (the
    ``no server running`` return code from ``tmux list-sessions`` is
    treated as empty, not an error).
    """
    if shutil.which("tmux") is None:
        return []
    result = subprocess.run(
        ["tmux", "list-sessions", "-F", "#{session_name}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [
        line
        for line in result.stdout.strip().splitlines()
        if line.startswith(SESSION_PREFIX)
    ]
