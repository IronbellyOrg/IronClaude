"""COMP-007 PtyDriver tests (Task T02.16 / D-0036).

The PtyDriver at ``src/superclaude/cli/eval/pty_driver.py`` wraps
``pexpect.spawn`` and exposes the five-method contract enumerated in the
T02.16 acceptance criteria. These tests pin each acceptance bullet as an
executable assertion against a deterministic Python subprocess stub.

Acceptance bullets covered here:

1. The class exposes ``expect_prompt_ready``, ``inject_prompt``,
   ``write_stdin``, ``read_stdout``, and ``wait_exit`` (see
   :func:`test_method_surface_matches_comp_007_contract`).
2. A unit test spawns a real ``claude --help`` (or test-stub) subprocess
   via PTY and ``expect_prompt_ready()`` returns within the timeout
   (see :func:`test_expect_prompt_ready_returns_before_timeout_against_stub`
   and the opt-in :func:`test_real_claude_help_smoketest`).
3. ``wait_exit()`` captures and returns the subprocess exit code
   accurately (see :func:`test_wait_exit_captures_exit_code_from_stub`
   and :func:`test_wait_exit_reports_signal_termination_as_negative`).
"""

from __future__ import annotations

import inspect
import shutil
import sys
import textwrap
import time

import pytest

from superclaude.cli.eval import (
    PtyDriver,
    PtyDriverEOF,
    PtyDriverError,
    PtyDriverNotStarted,
    PtyDriverTimeout,
)

# ---------------------------------------------------------------------------
# Stub builders
# ---------------------------------------------------------------------------


def _prompt_stub_source(exit_code: int = 0) -> str:
    """Python source that prints a banner, then a prompt-ready ``> `` line,
    echoes whatever it reads from stdin, and exits with ``exit_code``.
    """

    return textwrap.dedent(
        f"""
        import sys
        sys.stdout.write("banner: stub up\\r\\n")
        sys.stdout.write("> \\r\\n")
        sys.stdout.flush()
        line = sys.stdin.readline()
        sys.stdout.write("echo: " + line)
        sys.stdout.flush()
        sys.exit({int(exit_code)})
        """
    ).strip()


def _hang_stub_source() -> str:
    """Python source that prints a banner *without* the prompt-ready marker
    and then blocks on stdin, used to exercise the timeout path of
    ``expect_prompt_ready`` and ``wait_exit``.
    """

    return textwrap.dedent(
        """
        import sys
        sys.stdout.write("banner only\\r\\n")
        sys.stdout.flush()
        sys.stdin.read()
        """
    ).strip()


def _eof_stub_source(exit_code: int = 7) -> str:
    """Python source that exits immediately without ever emitting the
    prompt-ready marker. Used to exercise the EOF path of
    ``expect_prompt_ready``.
    """

    return textwrap.dedent(
        f"""
        import sys
        sys.stdout.write("nope\\r\\n")
        sys.stdout.flush()
        sys.exit({int(exit_code)})
        """
    ).strip()


def _make_driver(stub_source: str, *, timeout: float = 5.0) -> PtyDriver:
    return PtyDriver(
        command=[sys.executable, "-u", "-c", stub_source],
        default_timeout=timeout,
    )


# ---------------------------------------------------------------------------
# 1. Surface contract — COMP-007 method set
# ---------------------------------------------------------------------------


def test_method_surface_matches_comp_007_contract() -> None:
    """T02.16 AC bullet 1 — the 5 method names from COMP-007 are present."""

    required = {
        "expect_prompt_ready",
        "inject_prompt",
        "write_stdin",
        "read_stdout",
        "wait_exit",
    }
    actual = {
        name
        for name, member in inspect.getmembers(PtyDriver, predicate=inspect.isfunction)
    }
    missing = required - actual
    assert not missing, f"PtyDriver is missing required methods: {missing}"


def test_constructor_rejects_empty_command_list() -> None:
    with pytest.raises(ValueError, match="non-empty"):
        PtyDriver(command=[])


def test_constructor_rejects_non_positive_timeout() -> None:
    with pytest.raises(ValueError, match="default_timeout"):
        PtyDriver(command=[sys.executable, "-c", "pass"], default_timeout=0)


def test_interaction_before_spawn_raises_not_started() -> None:
    driver = PtyDriver(command=[sys.executable, "-c", "pass"])
    with pytest.raises(PtyDriverNotStarted):
        driver.inject_prompt("hi")
    with pytest.raises(PtyDriverNotStarted):
        driver.read_stdout()
    with pytest.raises(PtyDriverNotStarted):
        driver.expect_prompt_ready()
    with pytest.raises(PtyDriverNotStarted):
        driver.wait_exit()
    with pytest.raises(PtyDriverNotStarted):
        driver.write_stdin("hi")


# ---------------------------------------------------------------------------
# 2. Prompt-ready, inject_prompt, read_stdout round-trip
# ---------------------------------------------------------------------------


def test_expect_prompt_ready_returns_before_timeout_against_stub() -> None:
    """T02.16 AC bullet 2 — expect_prompt_ready returns within the timeout."""

    with _make_driver(_prompt_stub_source()) as driver:
        deadline = time.perf_counter() + 5.0
        before = driver.expect_prompt_ready(timeout=5.0)
        assert time.perf_counter() < deadline, (
            "expect_prompt_ready blocked past timeout"
        )
        assert "banner: stub up" in before


def test_inject_prompt_then_read_stdout_round_trips_text() -> None:
    with _make_driver(_prompt_stub_source()) as driver:
        driver.expect_prompt_ready()
        driver.inject_prompt("hello-from-test")
        # The stub echoes "echo: <line>" — concatenate read_stdout chunks
        # until we either see the marker or the child exits.
        collected = ""
        deadline = time.perf_counter() + 5.0
        while time.perf_counter() < deadline:
            chunk = driver.read_stdout(timeout=0.5)
            collected += chunk
            if "echo: hello-from-test" in collected:
                break
        assert "echo: hello-from-test" in collected


def test_write_stdin_does_not_append_newline() -> None:
    """``write_stdin`` is the raw escape hatch; it must not add ``\\r\\n``.

    PTY stdin runs in canonical (cooked) mode by default, so the child does
    not see typed input until a line terminator arrives. We therefore split
    the write into two parts: ``write_stdin("abcde")`` (no newline) followed
    by ``write_stdin("\\r")`` (terminator only). If ``write_stdin`` were
    secretly appending a newline, the stub's ``readline`` would unblock on
    the first call -- so the absence of any ``"got="`` output after the
    first call AND the presence of ``"got='abcde'"`` after the second call
    together pin the contract.
    """

    source = textwrap.dedent(
        """
        import sys
        sys.stdout.write("> \\r\\n"); sys.stdout.flush()
        line = sys.stdin.readline()
        sys.stdout.write("got=" + repr(line.rstrip()) + "\\r\\n")
        sys.stdout.flush()
        """
    ).strip()
    with _make_driver(source) as driver:
        driver.expect_prompt_ready()
        wrote = driver.write_stdin("abcde")
        assert wrote >= 5
        idle = driver.read_stdout(size=64, timeout=0.3)
        assert "got=" not in idle, (
            f"write_stdin appears to have auto-appended a newline: idle={idle!r}"
        )
        driver.write_stdin("\r")
        collected = ""
        deadline = time.perf_counter() + 5.0
        while time.perf_counter() < deadline:
            collected += driver.read_stdout(timeout=0.5)
            if "got='abcde'" in collected:
                break
        assert "got='abcde'" in collected, (
            f"expected stub to echo got='abcde' after newline; got: {collected!r}"
        )


def test_read_stdout_returns_empty_string_when_idle() -> None:
    """Polling for output when none is available must not block forever."""

    with _make_driver(_prompt_stub_source()) as driver:
        driver.expect_prompt_ready()
        # The stub is now blocked on stdin.readline(); no output should come.
        chunk = driver.read_stdout(size=64, timeout=0.2)
        assert chunk == ""


# ---------------------------------------------------------------------------
# 3. wait_exit — accurate exit-code capture
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("expected_exit", [0, 1, 42, 124])
def test_wait_exit_captures_exit_code_from_stub(expected_exit: int) -> None:
    """T02.16 AC bullet 3 — wait_exit returns the child's exit code."""

    with _make_driver(_prompt_stub_source(exit_code=expected_exit)) as driver:
        driver.expect_prompt_ready()
        driver.inject_prompt("anything")
        code = driver.wait_exit(timeout=5.0)
        assert code == expected_exit
        # Cached afterwards.
        assert driver.exit_code == expected_exit


def test_wait_exit_reports_signal_termination_as_negative() -> None:
    """Signal-killed children return a negative exit code (POSIX convention)."""

    driver = _make_driver(_hang_stub_source())
    driver.spawn()
    try:
        # Give the stub a moment to print its banner so the PTY is fully open.
        driver.read_stdout(timeout=0.5)
        driver.terminate(force=True)
        code = driver.wait_exit(timeout=5.0)
    finally:
        driver.close()
    assert code < 0, f"expected negative exit code for signal termination, got {code}"


def test_wait_exit_idempotent_after_clean_exit() -> None:
    with _make_driver(_prompt_stub_source(exit_code=3)) as driver:
        driver.expect_prompt_ready()
        driver.inject_prompt("x")
        first = driver.wait_exit(timeout=5.0)
        second = driver.wait_exit(timeout=5.0)
        assert first == second == 3


# ---------------------------------------------------------------------------
# 4. Failure modes — timeout and EOF
# ---------------------------------------------------------------------------


def test_expect_prompt_ready_raises_timeout_when_pattern_missing() -> None:
    with _make_driver(_hang_stub_source(), timeout=0.5) as driver:
        with pytest.raises(PtyDriverTimeout):
            driver.expect_prompt_ready(timeout=0.5)
        # Driver is still alive and recoverable — terminate explicitly.
        driver.terminate(force=True)


def test_expect_prompt_ready_raises_eof_when_child_dies_first() -> None:
    with _make_driver(_eof_stub_source(), timeout=2.0) as driver:
        with pytest.raises(PtyDriverEOF):
            driver.expect_prompt_ready(timeout=2.0)


def test_wait_exit_raises_timeout_when_child_still_alive() -> None:
    driver = _make_driver(_hang_stub_source())
    driver.spawn()
    try:
        with pytest.raises(PtyDriverTimeout):
            driver.wait_exit(timeout=0.3)
        # Recovery: terminate then wait.
        driver.terminate(force=True)
        code = driver.wait_exit(timeout=5.0)
        assert code < 0
    finally:
        driver.close()


# ---------------------------------------------------------------------------
# 5. Lifecycle hygiene
# ---------------------------------------------------------------------------


def test_double_spawn_while_alive_raises() -> None:
    driver = _make_driver(_hang_stub_source())
    driver.spawn()
    try:
        with pytest.raises(PtyDriverError):
            driver.spawn()
    finally:
        driver.terminate(force=True)
        driver.close()


def test_pid_returns_int_after_spawn() -> None:
    driver = _make_driver(_prompt_stub_source())
    assert driver.pid is None
    driver.spawn()
    try:
        assert isinstance(driver.pid, int) and driver.pid > 0
    finally:
        driver.terminate(force=True)
        driver.close()


def test_inject_prompt_rejects_bytes() -> None:
    with _make_driver(_prompt_stub_source()) as driver:
        driver.expect_prompt_ready()
        with pytest.raises(TypeError):
            driver.inject_prompt(b"bytes-not-allowed")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# 6. Real ``claude`` binary smoketest (opt-in; skips when binary missing)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    shutil.which("claude") is None,
    reason="real claude binary not installed on this host",
)
def test_real_claude_help_smoketest() -> None:
    """T02.16 AC bullet 2 (real binary path) — drive ``claude --help`` via PTY.

    ``claude --help`` prints its help text and exits with code 0. We do not
    assert any prompt-ready pattern here (``--help`` is non-interactive) —
    only that PtyDriver can spawn the real binary and capture its exit code
    accurately. The interactive ``expect_prompt_ready`` path is exercised by
    the stub tests above, which run on every host.
    """

    driver = PtyDriver(command=["claude", "--help"], default_timeout=10.0)
    driver.spawn()
    try:
        out = ""
        deadline = time.perf_counter() + 10.0
        while time.perf_counter() < deadline and driver.is_alive():
            out += driver.read_stdout(timeout=0.5)
        # Drain any remaining bytes.
        out += driver.read_stdout(timeout=0.5)
        code = driver.wait_exit(timeout=10.0)
    finally:
        driver.close()
    assert code == 0, f"claude --help exited non-zero: {code}\nOutput:\n{out}"
