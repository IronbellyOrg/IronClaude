"""COMP-007 PtyDriver -- pexpect.spawn wrapper for real Claude Code subprocess.

This module satisfies FR-G1 (real-subprocess discipline) by spawning the real
``claude`` binary via a pseudo-terminal. It deliberately avoids any in-process
SDK shortcut: every interaction with the child goes through the PTY's stdin /
stdout file descriptors, exactly as a human user would drive the REPL.

The class exposes the five method names enumerated in the COMP-007 roadmap row
(R-036) and the T02.16 acceptance criteria:

* :meth:`PtyDriver.expect_prompt_ready` -- block until the child emits a
  "prompt is ready for input" indicator (``>`` or ``$`` on its own line by
  default; configurable via ``prompt_ready_pattern``).
* :meth:`PtyDriver.inject_prompt` -- write a user-style prompt to the child's
  stdin, terminated by a carriage return + line-feed, and flush.
* :meth:`PtyDriver.write_stdin` -- raw write to the child's stdin without any
  newline handling. Used for control sequences, partial-line input, or
  test-stub probing.
* :meth:`PtyDriver.read_stdout` -- non-blocking read of the next chunk of bytes
  from the PTY. Returns ``b""`` immediately when no data is available.
* :meth:`PtyDriver.wait_exit` -- wait for the child to exit and return its
  exit code. Captures signal-termination as a negative exit code (POSIX
  convention) so callers can distinguish ``exit(124)`` from ``SIGTERM``.

The vendored ptytest fork (T02.01) lives at
``src/superclaude/cli/eval/pty/`` and pins ``pexpect>=4.9`` via the vendored
imports. This module first attempts to source ``pexpect`` from the vendored
location and falls back to the top-level ``pexpect`` package while the
vendored sources are still landing. Once T02.01 lands its sources, the
fall-back path becomes dead code -- this is intentional, not a long-term
escape hatch.

Test stubs:

The unit tests in ``tests/cli/eval/test_pty_driver.py`` spawn a
self-contained Python stub (a small script that prints a prompt-ready
indicator, echoes a single line, and exits with a known code) rather than
the real ``claude`` binary. This keeps the unit tests deterministic and
host-portable while still exercising the full PTY round-trip.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, Any, Pattern

if TYPE_CHECKING:  # pragma: no cover - typing only
    pass

try:  # Prefer the vendored fork once T02.01 lands.
    from superclaude.cli.eval.pty import (
        pexpect as _pexpect,  # type: ignore[attr-defined]
    )
except ImportError:  # pragma: no cover - exercised until T02.01 lands sources
    import pexpect as _pexpect

__all__ = [
    "DEFAULT_PROMPT_READY_PATTERN",
    "PtyDriver",
    "PtyDriverError",
    "PtyDriverTimeout",
    "PtyDriverNotStarted",
    "PtyDriverEOF",
]


# Default prompt-ready pattern. Matches the two indicators Claude Code emits
# at the end of a "ready for input" frame: a bare ``>`` or ``$`` followed by
# optional whitespace and a CR/LF terminator. The pattern relies on an
# explicit newline rather than the ``$`` end-of-string anchor because
# ``pexpect`` compiles patterns without MULTILINE and the incremental PTY
# buffer almost always has trailing CR/LF after the marker -- an unanchored
# match against the newline is both more permissive and more reliable.
DEFAULT_PROMPT_READY_PATTERN: str = r"[>$] *\r*\n"


class PtyDriverError(Exception):
    """Base class for ``PtyDriver`` failures."""


class PtyDriverTimeout(PtyDriverError):
    """Raised when an ``expect`` or ``wait`` exceeded its timeout budget."""


class PtyDriverNotStarted(PtyDriverError):
    """Raised when an interaction method is called before ``spawn`` completed."""


class PtyDriverEOF(PtyDriverError):
    """Raised when the child closed its PTY before the expected event."""


class PtyDriver:
    """Wraps ``pexpect.spawn`` for the IronClaude real-eval harness.

    The constructor does **not** spawn the child; it only validates arguments
    and stores them. Call :meth:`spawn` (or use the class as a context manager)
    to actually launch the subprocess. This split keeps the constructor cheap
    and matches the cliEval orchestrator's "build many drivers, spawn them in
    parallel" pattern.

    Parameters
    ----------
    command:
        Either a single executable string or a ``[command, *args]`` list.
        Mirrors the ``pexpect.spawn`` first-argument contract.
    env:
        Optional environment overlay. ``None`` inherits the parent process
        environment. To run with the per-eval HOME, pass
        ``HomeIsolation.env()`` here.
    cwd:
        Working directory for the child. ``None`` inherits the parent CWD.
    prompt_ready_pattern:
        Regex matched against the PTY output by
        :meth:`expect_prompt_ready`. Defaults to
        :data:`DEFAULT_PROMPT_READY_PATTERN`.
    default_timeout:
        Wall-clock seconds used by ``expect_prompt_ready`` and ``wait_exit``
        when the caller does not specify a per-call timeout.
    encoding:
        Text encoding used by ``pexpect.spawn``. ``"utf-8"`` is the default;
        pass ``None`` to receive raw ``bytes`` (rarely useful for Claude Code,
        whose TTY output is text-mode UTF-8).
    dimensions:
        ``(rows, cols)`` of the simulated terminal. The default
        ``(40, 120)`` matches Claude Code's recommended dev-host geometry.
    """

    def __init__(
        self,
        command: str | list[str],
        *,
        env: dict[str, str] | None = None,
        cwd: Path | str | None = None,
        prompt_ready_pattern: str | Pattern[str] = DEFAULT_PROMPT_READY_PATTERN,
        default_timeout: float = 30.0,
        encoding: str | None = "utf-8",
        dimensions: tuple[int, int] = (40, 120),
    ) -> None:
        if isinstance(command, str):
            self._argv: list[str] = [command]
        else:
            if not command:
                raise ValueError("command must be a non-empty string or list")
            self._argv = list(command)

        self._env: dict[str, str] | None = dict(env) if env is not None else None
        self._cwd: str | None = str(cwd) if cwd is not None else None

        if isinstance(prompt_ready_pattern, str):
            self._prompt_ready_pattern: Pattern[str] = re.compile(prompt_ready_pattern)
        else:
            self._prompt_ready_pattern = prompt_ready_pattern

        if default_timeout <= 0:
            raise ValueError("default_timeout must be > 0")
        self._default_timeout = float(default_timeout)
        self._encoding = encoding
        self._dimensions = dimensions

        self._child: Any | None = None  # pexpect.spawn instance once spawned
        self._exit_code: int | None = None

    # ------------------------------------------------------------------ lifecycle

    def spawn(self) -> None:
        """Launch the child subprocess via ``pexpect.spawn``.

        Idempotent: a second call after the child has exited starts a fresh
        process; a second call while the child is still alive raises
        :class:`PtyDriverError`.
        """

        if self._child is not None and self.is_alive():
            raise PtyDriverError("PtyDriver.spawn called while child is still alive")

        rows, cols = self._dimensions
        argv0, *args = self._argv
        self._child = _pexpect.spawn(
            argv0,
            args=args,
            env=self._env,
            cwd=self._cwd,
            timeout=self._default_timeout,
            encoding=self._encoding,
            dimensions=(rows, cols),
        )
        self._exit_code = None

    def __enter__(self) -> "PtyDriver":
        self.spawn()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            if self.is_alive():
                self.terminate()
        finally:
            self.close()

    # ------------------------------------------------------------------ state

    def is_alive(self) -> bool:
        """Return ``True`` while the child is running."""

        return self._child is not None and bool(self._child.isalive())

    @property
    def pid(self) -> int | None:
        """PID of the child process, or ``None`` if not yet spawned."""

        if self._child is None:
            return None
        return int(self._child.pid)

    # ------------------------------------------------------------------ I/O

    def _require_child(self) -> Any:
        if self._child is None:
            raise PtyDriverNotStarted("spawn() must be called before interaction")
        return self._child

    def expect_prompt_ready(self, timeout: float | None = None) -> str:
        """Block until the child emits the prompt-ready indicator.

        Parameters
        ----------
        timeout:
            Wall-clock seconds. ``None`` uses the driver's
            ``default_timeout``. Pass an explicit value to override on a
            per-call basis.

        Returns
        -------
        str
            The bytes captured *before* the prompt-ready match. Useful when
            the caller wants to inspect banner / version output the child
            emitted prior to becoming interactive.

        Raises
        ------
        PtyDriverTimeout
            The prompt-ready pattern did not appear within ``timeout``
            seconds.
        PtyDriverEOF
            The child closed its PTY (typically a crash) before emitting
            the prompt-ready pattern.
        """

        child = self._require_child()
        effective_timeout = self._default_timeout if timeout is None else float(timeout)
        try:
            child.expect(self._prompt_ready_pattern, timeout=effective_timeout)
        except _pexpect.TIMEOUT as exc:
            raise PtyDriverTimeout(
                f"prompt_ready_pattern not seen within {effective_timeout:.2f}s"
            ) from exc
        except _pexpect.EOF as exc:
            raise PtyDriverEOF(
                "child closed PTY before prompt-ready pattern matched"
            ) from exc
        before = child.before
        return before if isinstance(before, str) else (before or b"").decode(
            self._encoding or "utf-8", errors="replace"
        )

    def inject_prompt(self, text: str) -> None:
        """Send a user-style prompt to the child, terminated by ``\\r\\n``.

        Wraps ``pexpect.spawn.send`` with the carriage-return + line-feed
        sequence Claude Code expects from a real TTY. The send is flushed
        before returning.
        """

        child = self._require_child()
        if not isinstance(text, str):
            raise TypeError("inject_prompt requires str (use write_stdin for bytes)")
        child.send(text + "\r\n")
        # pexpect.spawn writes via os.write which is unbuffered, but be explicit
        # in case a subclass or vendored fork swaps the I/O layer.
        flush = getattr(child, "flush", None)
        if callable(flush):
            try:
                flush()
            except (OSError, ValueError):
                pass

    def write_stdin(self, data: str | bytes) -> int:
        """Raw write to the child's stdin.

        Returns the number of bytes (or characters when ``encoding`` is set)
        that pexpect reports it wrote. No newline is appended; callers that
        want a prompt-style write should use :meth:`inject_prompt`.
        """

        child = self._require_child()
        if isinstance(data, bytes) and self._encoding is not None:
            data = data.decode(self._encoding, errors="strict")
        result = child.send(data)
        return int(result) if result is not None else len(data)

    def read_stdout(self, size: int = -1, timeout: float | None = None) -> str:
        """Non-blocking read of up to ``size`` bytes from the child PTY.

        ``size`` is the maximum chunk size; negative values map to "as much
        as the PTY currently holds, capped at 65536 bytes." Returns an empty
        string when no data is currently buffered (instead of blocking).

        ``timeout`` is the maximum time pexpect will wait for the first byte.
        ``None`` uses the driver's ``default_timeout``; pass ``0`` for a true
        non-blocking poll.
        """

        child = self._require_child()
        cap = 65536 if size is None or size < 0 else int(size)
        if cap <= 0:
            return ""
        wait = self._default_timeout if timeout is None else float(timeout)
        try:
            chunk = child.read_nonblocking(size=cap, timeout=wait)
        except _pexpect.TIMEOUT:
            return ""
        except _pexpect.EOF:
            return ""
        if isinstance(chunk, bytes):
            chunk = chunk.decode(self._encoding or "utf-8", errors="replace")
        return chunk

    # ------------------------------------------------------------------ exit

    def wait_exit(self, timeout: float | None = None) -> int:
        """Wait for the child to exit and return its exit code.

        Parameters
        ----------
        timeout:
            Wall-clock seconds. ``None`` uses the driver's default timeout.

        Returns
        -------
        int
            POSIX exit code. Signal-terminated children return a negative
            value (``-SIGTERM`` = ``-15``, etc.) so callers can distinguish
            ``exit(124)`` from ``SIGTERM`` cleanly.

        Raises
        ------
        PtyDriverTimeout
            The child was still alive after ``timeout`` seconds. The child
            remains running; call :meth:`terminate` to clean it up.
        """

        child = self._require_child()
        if self._exit_code is not None and not child.isalive():
            return self._exit_code

        effective_timeout = self._default_timeout if timeout is None else float(timeout)
        # pexpect.wait() doesn't accept a timeout; emulate one by polling
        # ``expect(EOF, timeout=...)`` which blocks until the PTY closes.
        try:
            child.expect(_pexpect.EOF, timeout=effective_timeout)
        except _pexpect.TIMEOUT as exc:
            raise PtyDriverTimeout(
                f"child did not exit within {effective_timeout:.2f}s"
            ) from exc

        # Wait reaps the zombie and populates exitstatus / signalstatus.
        try:
            child.wait()
        except _pexpect.ExceptionPexpect:
            # ``wait()`` raises if pexpect believes the child is still alive;
            # in our flow EOF already arrived, so any residual race is
            # benign -- isalive() will return False and exitstatus / signalstatus
            # will be set on the next attribute read.
            pass

        if child.signalstatus is not None:
            self._exit_code = -int(child.signalstatus)
        else:
            self._exit_code = int(child.exitstatus) if child.exitstatus is not None else -1
        return self._exit_code

    # ------------------------------------------------------------------ cleanup

    def terminate(self, force: bool = False) -> None:
        """Send SIGTERM (or SIGKILL when ``force=True``) to the child.

        Safe to call when the child has already exited.
        """

        if self._child is None or not self._child.isalive():
            return
        self._child.terminate(force=force)

    def close(self) -> None:
        """Close the PTY file descriptors and release pexpect's bookkeeping."""

        if self._child is None:
            return
        try:
            self._child.close(force=False)
        except _pexpect.ExceptionPexpect:
            # close() can raise when the child is still alive; force-close to
            # avoid leaking the PTY fd. terminate() is safe to call twice.
            try:
                self._child.close(force=True)
            except _pexpect.ExceptionPexpect:
                pass
        if self._child.signalstatus is not None:
            self._exit_code = -int(self._child.signalstatus)
        elif self._child.exitstatus is not None and self._exit_code is None:
            self._exit_code = int(self._child.exitstatus)

    # ------------------------------------------------------------------ helpers

    @property
    def exit_code(self) -> int | None:
        """Last-captured exit code (``None`` until the child has exited)."""

        return self._exit_code

    def fileno(self) -> int:
        """Return the PTY's read file descriptor for ``select``-based loops."""

        return int(self._require_child().fileno())
