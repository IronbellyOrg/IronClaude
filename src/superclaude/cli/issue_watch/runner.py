"""Run one external command as an argv list and report what happened.

This is the only module of the ``issue_watch`` package that imports
``subprocess``. It never parses output and knows nothing about the program
it runs.
"""

from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from typing import Protocol

STDERR_CAP_BYTES = 500
"""Most bytes of a child's stderr kept in a ``CommandResult``."""


@dataclass(frozen=True)
class CommandResult:
    """The outcome of one command run.

    ``returncode`` is None when the command timed out or could not be started.
    ``stderr`` holds at most ``STDERR_CAP_BYTES`` bytes of UTF-8 text.
    ``spawn_error`` is the ``OSError`` or ``ValueError`` class name only, never
    its message text.
    """

    argv: tuple[str, ...]
    returncode: int | None
    stdout: str
    stderr: str
    timed_out: bool
    spawn_error: str | None
    duration_s: float


class Runner(Protocol):
    """Runs one argv list with a timeout and returns a ``CommandResult``."""

    def run(
        self, argv: list[str], timeout: float, *, cwd: str | None = None
    ) -> CommandResult:
        """Run ``argv`` for at most ``timeout`` seconds, in ``cwd`` when given."""
        ...


def _as_text(output: str | bytes | None) -> str:
    """Return partial child output as text; a timeout may give bytes or None."""
    if output is None:
        return ""
    if isinstance(output, bytes):
        return output.decode("utf-8", errors="replace")
    return output


def _cap_stderr(text: str) -> str:
    """Cut ``text`` to ``STDERR_CAP_BYTES`` UTF-8 bytes.

    A character split by the byte limit is dropped (``errors="ignore"``), so the
    result never re-encodes to more than the cap.
    """
    raw = text.encode("utf-8")[:STDERR_CAP_BYTES]
    return raw.decode("utf-8", errors="ignore")


class SubprocessRunner:
    """The real ``Runner``: one ``subprocess.run`` call per command, no shell."""

    def run(
        self, argv: list[str], timeout: float, *, cwd: str | None = None
    ) -> CommandResult:
        """Run ``argv`` with ``shell=False`` and stdin closed.

        Raises ``TypeError`` when ``argv`` is a ``str``, empty or not a list of
        ``str``. A timeout gives ``timed_out=True`` and ``returncode=None``; an
        ``OSError`` at start, or a ``ValueError`` from a NUL byte in ``argv`` or
        ``cwd``, gives ``spawn_error`` set to its class name and empty output.
        Output is decoded as UTF-8 with undecodable bytes replaced, so a child
        that prints other bytes never makes this method raise.
        """
        if (
            not isinstance(argv, list)
            or not argv
            or not all(isinstance(a, str) for a in argv)
        ):
            raise TypeError("argv must be a non-empty list of str")
        argv_t = tuple(argv)
        start = time.monotonic()
        try:
            proc = subprocess.run(
                argv,
                shell=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                stdin=subprocess.DEVNULL,
                cwd=cwd,
            )
        except subprocess.TimeoutExpired as exc:
            return CommandResult(
                argv=argv_t,
                returncode=None,
                stdout=_as_text(exc.stdout),
                stderr=_cap_stderr(_as_text(exc.stderr)),
                timed_out=True,
                spawn_error=None,
                duration_s=time.monotonic() - start,
            )
        except (OSError, ValueError) as exc:
            return CommandResult(
                argv=argv_t,
                returncode=None,
                stdout="",
                stderr="",
                timed_out=False,
                spawn_error=type(exc).__name__,
                duration_s=time.monotonic() - start,
            )
        return CommandResult(
            argv=argv_t,
            returncode=proc.returncode,
            stdout=proc.stdout,
            stderr=_cap_stderr(proc.stderr),
            timed_out=False,
            spawn_error=None,
            duration_s=time.monotonic() - start,
        )
