"""COMP-011 PtyStream tests (Task T02.17 / D-0037).

The PtyStream class wraps an arbitrary chunk source (typically
:class:`superclaude.cli.eval.PtyDriver.read_stdout`) and yields ANSI-stripped,
line-buffered text. These tests pin each T02.17 acceptance bullet as an
executable assertion using a lightweight callable source (no pexpect
dependency) plus one end-to-end smoke against a real ``PtyDriver`` over a
deterministic Python stub.

Acceptance bullets covered here:

1. ``PtyStream`` strips ANSI escape sequences from byte chunks and yields
   line-buffered output. (see :func:`test_strips_ansi_csi_sgr`,
   :func:`test_strips_osc_title_set`, :func:`test_buffers_partial_lines`).
2. ``PtyTimeout`` is raised when no new line arrives within the configured
   timeout. (see :func:`test_raises_pty_timeout_when_no_line_arrives`,
   :func:`test_per_call_timeout_overrides_default`).
3. ANSI test fixture is normalized to identical plain-text output across
   runs. (see :func:`test_identical_plain_text_across_runs`,
   :func:`test_iteration_yields_all_clean_lines`).
"""

from __future__ import annotations

import sys
import textwrap
import time
from collections import deque
from typing import Callable, Iterable

import pytest

from superclaude.cli.eval import (
    ANSI_ESCAPE_RE,
    PtyDriver,
    PtyStream,
    PtyStreamError,
    PtyTimeout,
)

# ---------------------------------------------------------------------------
# Test helpers -- scripted chunk readers
# ---------------------------------------------------------------------------


def scripted_reader(chunks: Iterable[str], *, idle: str = "") -> Callable[[float], str]:
    """Build a ``(timeout) -> str`` callable that yields ``chunks`` then ``idle``.

    Each call pops the next entry from the queue; once exhausted, every
    subsequent call returns ``idle`` (default empty string) so the consumer
    can exhaust its timeout budget naturally.
    """

    pending: deque[str] = deque(chunks)

    def _reader(_timeout: float) -> str:
        if pending:
            return pending.popleft()
        return idle

    return _reader


def delayed_reader(
    chunks: Iterable[tuple[float, str]],
) -> Callable[[float], str]:
    """Yield ``(min_wait_seconds, chunk)`` pairs gated by monotonic time.

    The first call returns the chunk immediately; subsequent calls return
    ``""`` until at least ``min_wait_seconds`` have elapsed since the previous
    chunk, then emit the next one. This lets a test simulate "a slow PTY
    that eventually produces a line" without sleeping the test process.
    """

    pending: deque[tuple[float, str]] = deque(chunks)
    next_at: list[float] = [time.monotonic()]

    def _reader(timeout: float) -> str:
        now = time.monotonic()
        if not pending:
            return ""
        if now < next_at[0]:
            # Sleep at most the caller's timeout, never past the next chunk.
            time.sleep(min(timeout, max(0.0, next_at[0] - now)))
            now = time.monotonic()
            if now < next_at[0]:
                return ""
        delay, chunk = pending.popleft()
        next_at[0] = now + delay
        return chunk

    return _reader


# ---------------------------------------------------------------------------
# 1. ANSI stripping
# ---------------------------------------------------------------------------


def test_ansi_regex_strips_csi_sgr_color_codes() -> None:
    """SGR colour codes (CSI ... m) must be removed verbatim."""

    coloured = "\x1B[31mERROR\x1B[0m: boom\n"
    assert ANSI_ESCAPE_RE.sub("", coloured) == "ERROR: boom\n"


def test_ansi_regex_strips_cursor_moves() -> None:
    cursor = "before\x1B[2J\x1B[1;1Hafter\n"
    assert ANSI_ESCAPE_RE.sub("", cursor) == "beforeafter\n"


def test_ansi_regex_strips_osc_title_set_bel_terminated() -> None:
    osc = "x\x1B]0;hello world\x07y\n"
    assert ANSI_ESCAPE_RE.sub("", osc) == "xy\n"


def test_ansi_regex_strips_osc_title_set_st_terminated() -> None:
    osc = "x\x1B]0;hello world\x1B\\y\n"
    assert ANSI_ESCAPE_RE.sub("", osc) == "xy\n"


def test_ansi_regex_strips_c1_singleton() -> None:
    # ESC '=' is a single-character Fe (DECPAM).
    raw = "x\x1B=y\n"
    assert ANSI_ESCAPE_RE.sub("", raw) == "xy\n"


def test_strips_ansi_csi_sgr() -> None:
    """T02.17 AC bullet 1 — colour codes are absent from the yielded line."""

    reader = scripted_reader(["\x1B[31mERROR\x1B[0m: boom\r\n"])
    stream = PtyStream(reader, timeout=1.0, poll_interval=0.05)
    assert stream.read_line() == "ERROR: boom"


def test_strips_osc_title_set() -> None:
    reader = scripted_reader(["\x1B]0;ttl\x07hello\n"])
    stream = PtyStream(reader, timeout=1.0, poll_interval=0.05)
    assert stream.read_line() == "hello"


def test_can_disable_ansi_stripping() -> None:
    reader = scripted_reader(["\x1B[31mERROR\x1B[0m\n"])
    stream = PtyStream(reader, timeout=1.0, strip_ansi=False, poll_interval=0.05)
    assert stream.read_line() == "\x1B[31mERROR\x1B[0m"


# ---------------------------------------------------------------------------
# 2. Line buffering
# ---------------------------------------------------------------------------


def test_buffers_partial_lines() -> None:
    """T02.17 AC bullet 1 — partial chunks must coalesce into one line."""

    reader = scripted_reader(["par", "tial-", "line\n"])
    stream = PtyStream(reader, timeout=1.0, poll_interval=0.01)
    assert stream.read_line() == "partial-line"


def test_yields_multiple_lines_in_order() -> None:
    reader = scripted_reader(["alpha\nbeta\ngamma\n"])
    stream = PtyStream(reader, timeout=1.0, poll_interval=0.01)
    assert stream.read_line() == "alpha"
    assert stream.read_line() == "beta"
    assert stream.read_line() == "gamma"


def test_keep_newline_preserves_terminator() -> None:
    reader = scripted_reader(["alpha\r\n"])
    stream = PtyStream(reader, timeout=1.0, keep_newline=True, poll_interval=0.01)
    assert stream.read_line() == "alpha\r\n"


def test_strips_crlf_by_default() -> None:
    reader = scripted_reader(["alpha\r\n"])
    stream = PtyStream(reader, timeout=1.0, poll_interval=0.01)
    assert stream.read_line() == "alpha"


def test_drain_returns_unterminated_remainder() -> None:
    reader = scripted_reader(["complete\n", "trailing-no-newline"])
    stream = PtyStream(reader, timeout=0.3, poll_interval=0.05)
    assert stream.read_line() == "complete"
    with pytest.raises(PtyTimeout):
        stream.read_line(timeout=0.2)
    assert stream.drain() == "trailing-no-newline"
    # Buffer is cleared after drain.
    assert stream.buffer == ""


# ---------------------------------------------------------------------------
# 3. Timeout semantics
# ---------------------------------------------------------------------------


def test_raises_pty_timeout_when_no_line_arrives() -> None:
    """T02.17 AC bullet 2 — stalled stream raises PtyTimeout."""

    reader = scripted_reader([])  # always returns ""
    stream = PtyStream(reader, timeout=0.2, poll_interval=0.05)
    start = time.monotonic()
    with pytest.raises(PtyTimeout):
        stream.read_line()
    elapsed = time.monotonic() - start
    assert 0.15 <= elapsed <= 1.0, f"timeout did not honour budget: {elapsed:.3f}s"


def test_pty_timeout_is_pty_stream_error() -> None:
    """``except PtyStreamError:`` must catch PtyTimeout."""

    reader = scripted_reader([])
    stream = PtyStream(reader, timeout=0.1, poll_interval=0.05)
    with pytest.raises(PtyStreamError):
        stream.read_line()


def test_per_call_timeout_overrides_default() -> None:
    reader = scripted_reader([])
    stream = PtyStream(reader, timeout=10.0, poll_interval=0.05)
    start = time.monotonic()
    with pytest.raises(PtyTimeout):
        stream.read_line(timeout=0.15)
    elapsed = time.monotonic() - start
    assert elapsed < 2.0, "per-call timeout was ignored (waited too long)"


def test_timeout_reports_pending_buffer_size() -> None:
    """The timeout exception message must include the unterminated buffer
    length so a debugger can see how much partial output is stuck."""

    reader = scripted_reader(["dangling-fragment"])
    stream = PtyStream(reader, timeout=0.2, poll_interval=0.05)
    with pytest.raises(PtyTimeout) as excinfo:
        stream.read_line()
    assert "buffer=" in str(excinfo.value)


def test_slow_stream_eventually_returns_line() -> None:
    """Chunks arriving below the per-call timeout still coalesce into a line."""

    reader = delayed_reader([(0.05, "slow "), (0.05, "but-arrives\n")])
    stream = PtyStream(reader, timeout=2.0, poll_interval=0.02)
    assert stream.read_line() == "slow but-arrives"


# ---------------------------------------------------------------------------
# 4. Iteration protocol
# ---------------------------------------------------------------------------


def test_iteration_yields_all_clean_lines() -> None:
    """T02.17 AC bullet 3 — iteration produces the canonical clean transcript."""

    reader = scripted_reader([
        "\x1B[32mone\x1B[0m\n",
        "\x1B[32mtwo\x1B[0m\n",
        "\x1B[32mthree\x1B[0m\n",
    ])
    stream = PtyStream(reader, timeout=0.5, poll_interval=0.02)
    collected: list[str] = []
    try:
        for line in stream:
            collected.append(line)
            if len(collected) == 3:
                break
    except PtyTimeout:
        pytest.fail("iteration timed out before all lines arrived")
    assert collected == ["one", "two", "three"]


def test_iteration_after_close_stops_immediately() -> None:
    reader = scripted_reader(["never-read\n"])
    stream = PtyStream(reader, timeout=1.0, poll_interval=0.01)
    stream.close()
    assert stream.closed is True
    out = list(iter(stream))
    assert out == []


def test_iteration_propagates_pty_timeout() -> None:
    """A stalled iterator must raise PtyTimeout rather than silently halting.

    This is the load-bearing design choice for Expect primitives -- they need
    to distinguish "stream done" from "stream stalled".
    """

    reader = scripted_reader([])
    stream = PtyStream(reader, timeout=0.15, poll_interval=0.05)
    iterator = iter(stream)
    with pytest.raises(PtyTimeout):
        next(iterator)


# ---------------------------------------------------------------------------
# 5. Constructor + source coercion
# ---------------------------------------------------------------------------


def test_constructor_rejects_non_positive_timeout() -> None:
    with pytest.raises(ValueError, match="timeout"):
        PtyStream(scripted_reader([]), timeout=0)


def test_constructor_rejects_non_positive_poll_interval() -> None:
    with pytest.raises(ValueError, match="poll_interval"):
        PtyStream(scripted_reader([]), timeout=1.0, poll_interval=0)


def test_constructor_rejects_bad_source() -> None:
    with pytest.raises(TypeError, match="read_stdout"):
        PtyStream(42, timeout=1.0)


def test_accepts_object_with_read_stdout_method() -> None:
    """The standard form: pass a PtyDriver-like object."""

    class Fake:
        def __init__(self) -> None:
            self._left = deque(["hi\n"])

        def read_stdout(self, timeout: float = 0.0, size: int = -1) -> str:
            return self._left.popleft() if self._left else ""

    stream = PtyStream(Fake(), timeout=1.0, poll_interval=0.01)
    assert stream.read_line() == "hi"


def test_read_line_rejects_zero_timeout() -> None:
    stream = PtyStream(scripted_reader([]), timeout=1.0, poll_interval=0.05)
    with pytest.raises(ValueError, match="timeout"):
        stream.read_line(timeout=0)


def test_read_after_close_raises() -> None:
    stream = PtyStream(scripted_reader(["x\n"]), timeout=1.0, poll_interval=0.05)
    stream.close()
    with pytest.raises(PtyStreamError):
        stream.read_line()


def test_context_manager_closes() -> None:
    reader = scripted_reader(["x\n"])
    with PtyStream(reader, timeout=1.0, poll_interval=0.05) as stream:
        assert stream.read_line() == "x"
    assert stream.closed is True


# ---------------------------------------------------------------------------
# 6. Deterministic ANSI fixture normalization
# ---------------------------------------------------------------------------


# ANSI-laden transcript with cursor moves, SGR colour, OSC title, and
# a stray C1 escape -- chosen to cover all four ANSI_ESCAPE_RE branches.
ANSI_FIXTURE: list[str] = [
    "\x1B]0;claude\x07",                                  # OSC title
    "\x1B[2J\x1B[1;1H",                                   # CSI clear + home
    "\x1B[1;32m== welcome ==\x1B[0m\r\n",                 # SGR colour line
    "\x1B[33mprompt> \x1B[0m\r\n",                        # prompt line
    "\x1B=output\x1B[0K\r\n",                             # C1 single + EL
]

EXPECTED_LINES: list[str] = [
    "== welcome ==",
    "prompt> ",
    "output",
]


def test_identical_plain_text_across_runs() -> None:
    """T02.17 AC bullet 3 — fixture normalizes to identical text on repeat."""

    runs: list[list[str]] = []
    for _ in range(3):
        reader = scripted_reader(list(ANSI_FIXTURE))
        stream = PtyStream(reader, timeout=1.0, poll_interval=0.01)
        runs.append([stream.read_line() for _ in EXPECTED_LINES])
    assert runs[0] == runs[1] == runs[2] == EXPECTED_LINES


# ---------------------------------------------------------------------------
# 7. End-to-end smoke against a real PtyDriver
# ---------------------------------------------------------------------------


PTY_STUB_SOURCE = textwrap.dedent(
    """
    import sys, time
    sys.stdout.write("\\x1B[2J\\x1B[1;1H")
    sys.stdout.flush()
    sys.stdout.write("\\x1B[32mhello-from-stub\\x1B[0m\\r\\n")
    sys.stdout.flush()
    sys.stdout.write("\\x1B]0;ttl\\x07ready\\r\\n")
    sys.stdout.flush()
    """
).strip()


def test_end_to_end_with_real_pty_driver() -> None:
    """T02.17 AC bullet 1 — PtyDriver -> PtyStream end-to-end strips ANSI."""

    driver = PtyDriver(
        command=[sys.executable, "-u", "-c", PTY_STUB_SOURCE],
        default_timeout=5.0,
    )
    driver.spawn()
    try:
        with PtyStream(driver, timeout=5.0, poll_interval=0.05) as stream:
            first = stream.read_line()
            second = stream.read_line()
        assert first == "hello-from-stub"
        assert second == "ready"
    finally:
        driver.close()
