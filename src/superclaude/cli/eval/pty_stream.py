"""COMP-011 PtyStream -- ANSI-stripped, line-buffered iteration over a PTY.

The cliEval harness drives the real ``claude`` binary through a pseudo-terminal
(see :mod:`superclaude.cli.eval.pty_driver`). The raw PTY output is a stream
of bytes peppered with ANSI escape sequences (colour codes, cursor moves,
title-set OSC bursts) and partial lines: ``read_stdout`` may return half a
line on one call and the rest on the next. Downstream ``Expect.stdout`` /
``Expect.stderr`` primitives (T04.07) need to assert against *plain text
lines*, not raw chunks, so this module sits between the driver and those
primitives.

Responsibilities
----------------

* **ANSI stripping.** Every chunk passes through :data:`ANSI_ESCAPE_RE`
  before reaching the line buffer. CSI sequences (colour / SGR / cursor),
  OSC sequences (title-set, hyperlinks), and 7-bit C1 singletons are all
  removed. The regex is intentionally permissive: stripping too much is
  preferable to leaking escape bytes into ``Expect`` assertions, where a
  hidden ``\\x1B[0m`` reset would silently break a substring check.
* **Line buffering.** Chunks are accumulated in an internal buffer; the
  iterator only yields when a ``\\n`` terminator arrives. Partial lines do
  not appear as empty strings -- they wait for completion or for an
  explicit :meth:`drain` flush.
* **Timeout.** Each :meth:`read_line` call carries a wall-clock budget. If
  the budget elapses with no complete line in the buffer, :class:`PtyTimeout`
  is raised. This is the stall signal the orchestrator's per-eval reaper
  watches for -- a hung child that prints a colour reset and nothing else
  must not look like progress to the harness.

API contract (T02.17 / D-0037 acceptance criteria)
--------------------------------------------------

```python
stream = PtyStream(driver, timeout=5.0)
for line in stream:
    if "ready" in line:
        break
# or, explicitly:
line = stream.read_line(timeout=2.0)        # str, ANSI-stripped, no trailing \\n
tail = stream.drain()                       # whatever sits in the buffer
```

The constructor accepts either a :class:`PtyDriver` (the standard case --
``read_stdout`` is the chunk producer) or any callable ``(timeout: float)
-> str`` returning the next available chunk. The callable form keeps the
unit tests independent of pexpect.

Failure modes
-------------

* :class:`PtyTimeout` -- raised by :meth:`read_line` (and propagated from
  :meth:`__next__`) when the per-line budget elapses with no terminator.
* :class:`PtyStreamError` -- raised when the stream is used after
  :meth:`close`. Also serves as the shared base class for
  ``except PtyStreamError:`` callers.

The iterator deliberately propagates :class:`PtyTimeout` rather than
swallowing it into :class:`StopIteration`. Downstream ``Expect`` primitives
treat a stalled stream as a deterministic failure, not as "stream
exhausted" -- collapsing both into ``StopIteration`` would silently mask a
hung child during an assertion loop.
"""

from __future__ import annotations

import re
import time
from typing import Any, Callable, Pattern

__all__ = [
    "ANSI_ESCAPE_RE",
    "PtyStream",
    "PtyStreamError",
    "PtyTimeout",
]


# Combined ANSI / VT escape stripper.
#
# Covers:
#   * CSI:  ESC '[' <params> <intermediate> <final>     -- SGR, cursor, mode
#   * OSC:  ESC ']' <text> (BEL | ST)                   -- title, hyperlinks
#   * DCS / SOS / PM / APC: ESC ('P'|'X'|'^'|'_') <text> ST
#   * Two-byte singletons:  ESC followed by any single 0x20-0x7E byte that
#     was not consumed by the multi-byte alternatives above.  Covers the
#     full ESC Fp/Fe/Fs ranges (DECPAM `\x1B=`, DECPNM `\x1B>`, IND, NEL,
#     HTS, RI, SS2, SS3, charset selectors, ...) without enumerating each.
#
# The regex is non-greedy where it scans content between an opener and its
# terminator so a stream containing several OSC bursts is not collapsed
# into one huge match. The catch-all alternative is listed LAST so the
# multi-byte sequences match in preference to a single-byte strip.
ANSI_ESCAPE_RE: Pattern[str] = re.compile(
    r"\x1B"
    r"(?:"
    r"\[[0-?]*[ -/]*[@-~]"               # CSI ... final
    r"|\][^\x07\x1B]*?(?:\x07|\x1B\\)"   # OSC ... BEL or ST
    r"|[PX^_].*?\x1B\\"                  # DCS / SOS / PM / APC ... ST
    r"|[\x20-\x7E]"                      # ESC + any single printable -- catch-all
    r")"
)


class PtyStreamError(Exception):
    """Base class for :class:`PtyStream` failures."""


class PtyTimeout(PtyStreamError):
    """Raised when no complete line arrives within the configured timeout."""


# Type alias for any object that can produce the next chunk of stream text.
ChunkReader = Callable[[float], str]


class PtyStream:
    """ANSI-stripped, line-buffered iterator over a PTY-like chunk source.

    Parameters
    ----------
    source:
        Either an object exposing ``read_stdout(timeout=<float>) -> str`` (in
        practice, a :class:`PtyDriver`) or a callable ``(timeout: float) ->
        str`` returning the next available chunk. The chunk source MUST
        return ``""`` (rather than blocking forever) when no data is
        currently available so the timeout budget can advance.
    timeout:
        Default per-line timeout in seconds. ``read_line`` raises
        :class:`PtyTimeout` when this elapses with no terminator. ``__next__``
        uses this same default. Must be ``> 0``.
    poll_interval:
        Maximum seconds passed to the chunk source on each underlying read.
        Small enough to react to new chunks promptly; large enough that an
        idle stream does not spin the CPU. Must be ``> 0``.
    strip_ansi:
        When ``True`` (default), :data:`ANSI_ESCAPE_RE` is applied to each
        chunk before buffering. Pass ``False`` for transcript-fidelity use
        cases (eg. recording for replay).
    keep_newline:
        When ``False`` (default), the trailing ``\\r``/``\\n`` is stripped
        from each yielded line. When ``True``, the terminator is preserved,
        which keeps the byte-for-byte transcript stable across re-runs.
    """

    def __init__(
        self,
        source: Any,
        *,
        timeout: float = 5.0,
        poll_interval: float = 0.1,
        strip_ansi: bool = True,
        keep_newline: bool = False,
    ) -> None:
        if timeout <= 0:
            raise ValueError("timeout must be > 0")
        if poll_interval <= 0:
            raise ValueError("poll_interval must be > 0")

        self._reader: ChunkReader = self._coerce_reader(source)
        self._timeout = float(timeout)
        self._poll_interval = float(poll_interval)
        self._strip_ansi = bool(strip_ansi)
        self._keep_newline = bool(keep_newline)

        self._buffer: str = ""
        self._closed: bool = False

    # ------------------------------------------------------------------ source

    @staticmethod
    def _coerce_reader(source: Any) -> ChunkReader:
        read_stdout = getattr(source, "read_stdout", None)
        if callable(read_stdout):
            def _from_driver(timeout: float) -> str:
                # PtyDriver.read_stdout(size=-1, timeout=None) -> str.
                chunk = read_stdout(timeout=timeout)
                return chunk if isinstance(chunk, str) else chunk.decode("utf-8", errors="replace")
            return _from_driver
        if callable(source):
            return source  # type: ignore[return-value]
        raise TypeError(
            "PtyStream source must expose read_stdout(timeout=...) -> str "
            "or be a callable(timeout) -> str"
        )

    # ------------------------------------------------------------------ public

    def read_line(self, timeout: float | None = None) -> str:
        """Return the next complete line, ANSI-stripped.

        Blocks up to ``timeout`` seconds (or the stream default) waiting for a
        ``\\n`` terminator. The terminator is stripped from the returned
        string unless the stream was constructed with ``keep_newline=True``.

        Raises
        ------
        PtyStreamError
            The stream has been :meth:`close`-d.
        PtyTimeout
            No complete line arrived within the budget.
        """

        if self._closed:
            raise PtyStreamError("read_line called on closed PtyStream")
        budget = self._timeout if timeout is None else float(timeout)
        if budget <= 0:
            raise ValueError("timeout must be > 0")

        deadline = time.monotonic() + budget
        while True:
            line = self._take_buffered_line()
            if line is not None:
                return line

            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise PtyTimeout(
                    f"no complete line within {budget:.2f}s "
                    f"(buffer={len(self._buffer)} chars unterminated)"
                )

            wait = min(self._poll_interval, remaining)
            chunk = self._reader(wait)
            if not chunk:
                continue
            if self._strip_ansi:
                chunk = ANSI_ESCAPE_RE.sub("", chunk)
            self._buffer += chunk

    def drain(self) -> str:
        """Return whatever (ANSI-stripped) bytes remain in the line buffer.

        Useful after the child exits when the final emit lacked a trailing
        newline. The buffer is cleared.
        """

        result, self._buffer = self._buffer, ""
        return result

    def close(self) -> None:
        """Mark the stream closed. Subsequent reads raise."""

        self._closed = True

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def buffer(self) -> str:
        """Read-only view of the current unterminated line fragment.

        Exposed for diagnostics and test introspection -- callers must not
        mutate the underlying buffer state.
        """

        return self._buffer

    # ------------------------------------------------------------------ protocols

    def __iter__(self) -> "PtyStream":
        return self

    def __next__(self) -> str:
        if self._closed:
            raise StopIteration
        return self.read_line()

    def __enter__(self) -> "PtyStream":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    # ------------------------------------------------------------------ helpers

    def _take_buffered_line(self) -> str | None:
        """Pop the first ``\\n``-terminated line from the buffer, or None."""

        idx = self._buffer.find("\n")
        if idx < 0:
            return None
        line = self._buffer[: idx + 1]
        self._buffer = self._buffer[idx + 1 :]
        if not self._keep_newline:
            line = line.rstrip("\r\n")
        return line
