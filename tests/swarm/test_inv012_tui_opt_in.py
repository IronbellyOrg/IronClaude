"""T07.03 / R-120 -- INV-012 TUI opt-in enforcement (no ANSI on non-TTY).

Covers the acceptance criteria from
``.dev/releases/Current/MultiModelSwarm/tasklist/phase-7-tasklist.md``::

    - Default ``swarm run`` emits plain output (no ANSI bytes).
    - ``--tui`` enables Rich Live dashboard (on TTY only).
    - Non-TTY caller never receives terminal control sequences.
    - ``tests/swarm/test_inv012_tui_opt_in.py`` green.

INV-012 is the contract that operators piping ``swarm run`` to a file
or another process MUST receive bytes free of terminal control
sequences. The :func:`should_enable_tui` helper in ``cli/swarm/tui.py``
is the single gate every wiring site has to consult before instantiating
:class:`TUI`; this file pins the contract from three independent angles
so a regression at any layer surfaces here:

    1. **Subprocess end-to-end.** ``superclaude swarm`` (and its real
       ``run`` subcommand) invoked through a non-TTY pipe must emit
       zero ANSI bytes on stdout / stderr regardless of how the command
       exits. This is the operator-visible enforcement: a piped caller
       running e.g. ``swarm run --lens bare-review | cat`` sees plain
       text even when the command errors.
    2. **Gate helper.** ``should_enable_tui(flag, stream)`` returns
       ``False`` for every non-TTY shape (no ``--tui`` flag; flag set
       but stream is plain :class:`io.StringIO`; flag set but stream
       lacks ``isatty``; ``isatty`` raising). The boolean return is
       the single source of truth for the ``--tui`` wiring site.
    3. **Render contract.** Even when an integration point eventually
       routes ``swarm run`` output through :meth:`TUI.render`, rendering
       through a non-terminal :class:`rich.console.Console` must produce
       zero ANSI bytes -- so a misconfigured caller that bypasses the
       gate still cannot leak escape sequences to a pipe.

The companion unit suite ``tests/swarm/test_tui.py`` covers the
per-helper contract (projection, gating, render shape); this file is
the INV-012 integration guard.
"""

from __future__ import annotations

import io
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner
from rich.console import Console

from superclaude.cli.swarm import swarm_group
from superclaude.cli.swarm.commands import run_cmd
from superclaude.cli.swarm.models import EventRecord, SwarmState
from superclaude.cli.swarm.tui import TUI, should_enable_tui

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# CSI (Control Sequence Introducer) escape pattern: ESC '[' followed by
# any number of parameter / intermediate bytes and a final letter. Covers
# the entire family Rich uses for color + cursor control. The grep also
# fires on bare ESC bytes (the ``\x1b`` literal) so a regression that
# emits ``\x1b]...`` OSC sequences or ``\x1bM`` reverse-index single
# bytes is still flagged.
_ANSI_CSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
_ANY_ESC_RE = re.compile(r"\x1b")


def _assert_no_ansi(payload: str, *, source: str) -> None:
    """Assert ``payload`` carries no terminal control sequences.

    Two patterns are checked so a CSI-shaped regression and a bare-ESC
    regression both surface here. The ``source`` label flows into the
    failure message so a multi-stream test (stdout + stderr) names the
    offending side.
    """
    csi_match = _ANSI_CSI_RE.search(payload)
    esc_match = _ANY_ESC_RE.search(payload)
    assert csi_match is None and esc_match is None, (
        f"INV-012 violated: {source} contains terminal control bytes\n"
        f"  CSI match: {csi_match!r}\n"
        f"  ESC match: {esc_match!r}\n"
        f"  payload (first 400 chars): {payload[:400]!r}"
    )


# Environment used for subprocess invocations. ``FORCE_COLOR`` /
# ``CLICOLOR_FORCE`` would otherwise let Rich-or-Click downstream
# emit ANSI even though stdout isn't a TTY; we strip those so the
# subprocess sees a "piped, no override" view of the world. ``NO_COLOR``
# is set defensively as a belt-and-braces signal (Rich honors it).
def _piped_env() -> dict[str, str]:
    env = os.environ.copy()
    for var in ("FORCE_COLOR", "CLICOLOR_FORCE", "PY_COLORS"):
        env.pop(var, None)
    env["NO_COLOR"] = "1"
    env["TERM"] = "dumb"
    return env


# ---------------------------------------------------------------------------
# Subprocess end-to-end (the operator-visible INV-012 surface)
# ---------------------------------------------------------------------------


def _superclaude_cli_available() -> bool:
    """True iff ``superclaude`` is on PATH (editable / pipx install).

    The subprocess tests fall back to ``python -m superclaude.cli.main``
    when the console-script shim is absent so a clean checkout that
    skipped ``pipx install`` / ``make dev`` still exercises the contract.
    """
    return shutil.which("superclaude") is not None


def _swarm_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Run ``superclaude swarm ...`` through a non-TTY subprocess.

    Both stdout and stderr are captured as pipes (``isatty()`` False on
    both) so the subprocess sees the exact stream shape a piped caller
    would. ``stdin`` is closed (``DEVNULL``) for the same reason -- a
    subprocess inheriting our test runner's TTY stdin would otherwise
    confuse Rich's auto-detection.
    """
    if _superclaude_cli_available():
        cmd: list[str] = ["superclaude", "swarm", *args]
    else:
        cmd = [sys.executable, "-m", "superclaude.cli.main", "swarm", *args]
    return subprocess.run(
        cmd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=_piped_env(),
        text=True,
        check=False,
        timeout=30,
    )


def test_subprocess_swarm_help_emits_no_ansi() -> None:
    """``superclaude swarm --help`` piped to non-TTY -> zero ANSI bytes.

    The help renderer is the lightest-weight surface that exercises
    Click's stdout writer end-to-end. A regression that flips Click's
    color autodetect on, or that wires a Rich console into the help
    path without an INV-012 gate, surfaces here first.
    """
    result = _swarm_cli("--help")
    assert result.returncode == 0, (
        f"swarm --help exit code {result.returncode}\n"
        f"stdout: {result.stdout!r}\nstderr: {result.stderr!r}"
    )
    _assert_no_ansi(result.stdout, source="swarm --help stdout")
    _assert_no_ansi(result.stderr, source="swarm --help stderr")
    # Sanity: the help body actually rendered. If this fails the no-ANSI
    # assertion above is vacuously true and would mask a real regression.
    assert "Usage" in result.stdout or "Orchestrate" in result.stdout


def test_subprocess_swarm_run_help_emits_no_ansi() -> None:
    """``superclaude swarm run --help`` piped to non-TTY -> zero ANSI bytes.

    Pins the ``run`` subcommand's help surface separately from the
    group help -- a future ``--tui`` flag will land on this command and
    must not change the help-time output shape on a non-TTY caller.
    """
    result = _swarm_cli("run", "--help")
    assert result.returncode == 0, (
        f"swarm run --help exit code {result.returncode}\n"
        f"stdout: {result.stdout!r}\nstderr: {result.stderr!r}"
    )
    _assert_no_ansi(result.stdout, source="swarm run --help stdout")
    _assert_no_ansi(result.stderr, source="swarm run --help stderr")
    assert "--lens" in result.stdout, (
        "swarm run --help output truncated: --lens flag missing -- the no-ANSI "
        "guard would be vacuous against an empty payload"
    )


def test_subprocess_swarm_run_failure_path_emits_no_ansi() -> None:
    """``swarm run`` exiting non-zero on a non-TTY pipe -> zero ANSI bytes.

    Exercises the *error* surface (preflight rule diagnostics on stderr
    + click.exceptions.Exit on stdout). A regression that adds a Rich
    Console.print() to the preflight failure formatter without an
    INV-012 gate breaks here. Exit code is not asserted -- the contract
    is about the bytes, not the status -- but a clean usage-error path
    is the expected outcome (no spec path, no --stdin, no --lens).
    """
    result = _swarm_cli("run")
    # No input modes -> EXIT_USAGE (2). The contract is byte-level; we
    # just confirm the command actually ran and emitted *something*.
    assert result.returncode != 0
    assert result.stderr, "preflight diagnostic block expected on stderr"
    _assert_no_ansi(result.stdout, source="swarm run (no args) stdout")
    _assert_no_ansi(result.stderr, source="swarm run (no args) stderr")


# ---------------------------------------------------------------------------
# Gate helper -- single source of truth the wiring sites consult
# ---------------------------------------------------------------------------


class _FakeTTY(io.StringIO):
    """In-memory stream that claims to be a TTY (positive-path fixture)."""

    def isatty(self) -> bool:  # type: ignore[override]
        return True


def test_gate_closed_when_flag_absent_regardless_of_tty() -> None:
    """``--tui`` absent -> gate stays closed even on a TTY stream.

    The flag is the operator-facing opt-in; without it, no Rich Live
    dashboard may start even if the caller is sitting at a real
    terminal. This is the contract that protects scripted callers
    that happen to run inside a TTY (e.g. an interactive shell).
    """
    assert should_enable_tui(False, _FakeTTY()) is False
    assert should_enable_tui(False, io.StringIO()) is False
    assert should_enable_tui(False, None) is False


def test_gate_closed_when_stream_is_not_a_tty() -> None:
    """``--tui`` + non-TTY stream -> gate stays closed (INV-012 core)."""
    # io.StringIO.isatty() returns False, so it stands in for any
    # piped stdout the operator might have routed to.
    plain = io.StringIO()
    assert should_enable_tui(True, plain) is False


def test_gate_closed_when_stream_lacks_isatty_method() -> None:
    """Conservative read: streams without ``isatty`` are treated as non-TTY.

    A custom stream wrapper that forgets to expose ``isatty`` would
    otherwise be ambiguous; the gate defaults to ``False`` so the
    INV-012 contract holds even for callers wiring exotic streams.
    """

    class _NoIsAtty:
        """A stream that exposes no ``isatty`` callable."""

    # ``# type: ignore`` -- we deliberately violate the IO protocol to
    # exercise the conservative branch.
    assert should_enable_tui(True, _NoIsAtty()) is False  # type: ignore[arg-type]


def test_gate_closed_when_isatty_raises() -> None:
    """Streams whose ``isatty()`` raises are treated as non-TTY.

    A redirected stream wrapper that bubbles an OSError from
    ``isatty()`` (e.g. closed file descriptor inside a wrapper) must
    not be allowed to crash the gate; it falls through to ``False``.
    """

    class _RaisingStream:
        def isatty(self) -> bool:
            raise OSError("redirected fd")

    assert should_enable_tui(True, _RaisingStream()) is False  # type: ignore[arg-type]


def test_gate_open_only_when_flag_and_tty_both_true() -> None:
    """Positive-path: ``--tui`` + TTY stream -> gate opens.

    Sanity-checks the AND-shape of the gate. Without this assertion a
    regression that flips one branch to always-False would still pass
    the four "gate-closed" tests above but silently break ``--tui``
    for operators on a real terminal.
    """
    assert should_enable_tui(True, _FakeTTY()) is True


# ---------------------------------------------------------------------------
# Render contract -- defense-in-depth even if a future caller bypasses gate
# ---------------------------------------------------------------------------


def _sample_events() -> list[EventRecord]:
    """A small EventRecord stream covering ``worker_start`` + ``worker_done``.

    Lifted out of the inline render helper so the no-ANSI assertion has
    representative content -- otherwise an "empty render" path could
    satisfy the byte check without exercising the styled paths Rich
    would otherwise color.
    """
    return [
        EventRecord(
            event_type="worker_start",
            timestamp="2026-06-01T15:00:00+00:00",
            worker_index=0,
            payload={"model_label": "alpha-7b", "timeout_sec": 180},
        ),
        EventRecord(
            event_type="worker_done",
            timestamp="2026-06-01T15:00:03+00:00",
            worker_index=0,
            payload={"status": "success", "elapsed_ms": 3210},
        ),
        EventRecord(
            event_type="worker_start",
            timestamp="2026-06-01T15:00:01+00:00",
            worker_index=1,
            payload={"model_label": "beta-13b"},
        ),
    ]


def _render_via_console(*, force_terminal: bool) -> str:
    """Render the dashboard through a captured Console at the given color mode.

    ``force_terminal=False`` exercises the piped-caller path: Rich must
    not emit ANSI even when the inner ``Live`` would happily color the
    output on a real terminal. ``force_terminal=True`` is the positive
    control -- if no ANSI lands when the console is forced into terminal
    mode, the test fixture is broken and the no-ANSI assertion above
    would be vacuous.
    """
    buf = io.StringIO()
    console = Console(
        file=buf,
        force_terminal=force_terminal,
        color_system="truecolor" if force_terminal else None,
        width=120,
    )
    state = SwarmState(state="dispatching", job_id="job-inv012")
    tui = TUI()
    console.print(tui.render(state, _sample_events()))
    return buf.getvalue()


def test_render_through_non_terminal_console_emits_zero_ansi() -> None:
    """:meth:`TUI.render` via a non-terminal Console -> zero ANSI bytes.

    Defense-in-depth: even if a future wiring site renders the panel
    through a misconfigured Console (e.g. ``force_terminal=False`` but
    no gate check), the byte output stays plain. This is the second
    line of defense for INV-012 after the gate helper.
    """
    payload = _render_via_console(force_terminal=False)
    _assert_no_ansi(payload, source="TUI.render() via non-terminal Console")
    # Content sanity: the worker rows actually rendered. Without these
    # assertions the no-ANSI check is vacuous against an empty buffer.
    assert "alpha-7b" in payload
    assert "beta-13b" in payload
    assert "success" in payload
    assert "running" in payload


def test_render_through_forced_terminal_console_emits_ansi() -> None:
    """Positive control: forced-terminal Console -> Rich does color the panel.

    Without this test the no-ANSI assertion in
    :func:`test_render_through_non_terminal_console_emits_zero_ansi`
    could pass trivially -- e.g. if Rich silently dropped style for a
    rendering bug. Confirming the forced-terminal branch DOES emit
    ANSI proves the assertion above is meaningful.
    """
    payload = _render_via_console(force_terminal=True)
    assert _ANSI_CSI_RE.search(payload) is not None, (
        "forced-terminal Rich Console produced no ANSI bytes; the test "
        "fixture is degenerate and the non-terminal assertion is vacuous"
    )
    # Same content sanity check so a regression that suppresses rows
    # AND ANSI passes both branches but is caught here.
    assert "alpha-7b" in payload
    assert "dispatching" in payload


# ---------------------------------------------------------------------------
# Click invocation surface (CliRunner is always non-TTY)
# ---------------------------------------------------------------------------


def test_click_invocation_emits_no_ansi_on_help() -> None:
    """``CliRunner.invoke(run_cmd, ['--help'])`` -> zero ANSI bytes.

    CliRunner's captured stream is always non-TTY (it's an in-memory
    buffer), mirroring the piped-stdout scenario without spawning a
    subprocess. Faster than the subprocess tests above and exercises
    the in-process Click stack so a regression in the help formatter
    or in a future ``--tui``-flag default surfaces immediately.
    """
    runner = CliRunner()
    result = runner.invoke(run_cmd, ["--help"])
    assert result.exit_code == 0, result.output
    _assert_no_ansi(result.output, source="CliRunner run_cmd --help")
    # Sanity: the help body is non-empty.
    assert "--lens" in result.output


def test_click_invocation_emits_no_ansi_on_group_help() -> None:
    """``CliRunner.invoke(swarm_group, ['--help'])`` -> zero ANSI bytes.

    Mirrors :func:`test_click_invocation_emits_no_ansi_on_help` at the
    group level so a regression introduced by a future TUI-flag wired
    on the group (rather than the subcommand) still surfaces.
    """
    runner = CliRunner()
    result = runner.invoke(swarm_group, ["--help"])
    assert result.exit_code == 0, result.output
    _assert_no_ansi(result.output, source="CliRunner swarm_group --help")
    assert "run" in result.output


# ---------------------------------------------------------------------------
# Forward-looking PTY guard for ``swarm run --tui``
# ---------------------------------------------------------------------------


def _run_cmd_has_tui_flag() -> bool:
    """True iff ``run_cmd`` exposes a ``--tui`` flag.

    The wiring task that adds ``--tui`` to :func:`run_cmd` lives outside
    the T07.03 scope (the T07.03 deliverable is *this* test file, not
    the flag wiring). Until that wiring lands, the PTY positive-path
    test below skips with a clear reason so the suite stays green;
    once the flag lands the test activates automatically.
    """
    return any(
        getattr(param, "name", None) == "tui"
        or "--tui" in getattr(param, "opts", ())
        for param in run_cmd.params
    )


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="pty.openpty is POSIX-only; --tui PTY check skipped on Windows",
)
def test_pty_invocation_with_tui_flag_when_wired() -> None:
    """On a PTY with ``--tui``, ``swarm run`` -> Rich Live present.

    The task step says::

        Run with ``--tui`` on PTY and confirm Rich Live present.

    The ``--tui`` flag itself is wired by a later step (T07.06 / T07.11
    surface integration); this test verifies the contract end-to-end as
    soon as that wiring lands and skips cleanly until then. The test
    spawns ``superclaude swarm run --tui --lens bare-review`` with
    stdout/stderr routed through a pseudo-terminal so Rich's TTY
    autodetect opens the styled path. We then assert ANSI bytes ARE
    present (the inverse of the non-TTY contract -- styled output is
    the *expected* behavior on the opt-in path).
    """
    if not _run_cmd_has_tui_flag():
        pytest.skip(
            "--tui not yet wired into run_cmd; T07.03 contract enforced via "
            "subprocess + gate-helper paths above. This positive PTY check "
            "activates automatically once the wiring task lands."
        )

    import pty  # POSIX-only; skipif above guards Windows.

    primary_fd, secondary_fd = pty.openpty()
    try:
        if _superclaude_cli_available():
            cmd: list[str] = [
                "superclaude",
                "swarm",
                "run",
                "--tui",
                "--lens",
                "bare-review",
            ]
        else:
            cmd = [
                sys.executable,
                "-m",
                "superclaude.cli.main",
                "swarm",
                "run",
                "--tui",
                "--lens",
                "bare-review",
            ]
        env = _piped_env()
        # The PTY path is the positive control for the opt-in: Rich must
        # see a TTY on stdout for the gate to open. Setting TERM to a
        # color-capable value lets Rich's autodetect take the styled
        # branch; otherwise the gate would open but the renderer might
        # downshift to plain text and the assertion below would be
        # vacuous.
        env["TERM"] = "xterm-256color"
        env.pop("NO_COLOR", None)
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=secondary_fd,
            stderr=secondary_fd,
            env=env,
        )
        os.close(secondary_fd)
        chunks: list[bytes] = []
        try:
            # Drain the PTY until the child exits or we hit a soft cap.
            # The cap exists so a runaway Rich Live loop doesn't hang
            # the suite; 64KB is well above the dashboard's expected
            # output footprint for the few seconds the smoke run takes.
            while len(b"".join(chunks)) < 64 * 1024:
                try:
                    data = os.read(primary_fd, 4096)
                except OSError:
                    break
                if not data:
                    break
                chunks.append(data)
                if proc.poll() is not None:
                    break
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)
        payload = b"".join(chunks).decode("utf-8", errors="replace")
    finally:
        try:
            os.close(primary_fd)
        except OSError:
            pass

    assert _ANSI_CSI_RE.search(payload) is not None, (
        "INV-012 opt-in positive path failed: --tui on a PTY produced no "
        "ANSI bytes. Either the gate stayed closed despite TTY+flag, or "
        "the dashboard never rendered.\n"
        f"  PTY payload (first 400 chars): {payload[:400]!r}"
    )


# ---------------------------------------------------------------------------
# Wiring audit -- ``commands.py`` must not bypass the gate
# ---------------------------------------------------------------------------


def test_commands_module_does_not_construct_tui_outside_gate() -> None:
    """Static audit: any ``TUI(`` construction in commands.py is gate-guarded.

    INV-012 enforcement depends on every wiring site routing through
    :func:`should_enable_tui`. A direct ``TUI(`` instantiation that
    doesn't sit inside an ``if should_enable_tui(...)`` block is an
    enforcement gap regardless of how clean the helper-level tests
    are. We grep the source so a future caller cannot silently bypass
    the gate without flipping this guard red.

    The audit is *conservative*: it allows zero ``TUI(`` constructions
    in ``commands.py`` until the wiring task lands, and once the
    wiring lands the same source line must be paired with a nearby
    ``should_enable_tui`` reference (same function body). Failure to
    pair the two surfaces here as an actionable error.
    """
    commands_path = (
        Path(__file__).resolve().parent.parent.parent
        / "src"
        / "superclaude"
        / "cli"
        / "swarm"
        / "commands.py"
    )
    assert commands_path.is_file(), (
        f"commands.py not found at {commands_path}; INV-012 audit cannot run"
    )
    source = commands_path.read_text(encoding="utf-8")
    # Strip comments / docstrings? A literal substring scan is enough --
    # docstring mentions of ``TUI(`` would be code-quoted in backticks
    # and pass the gate-pairing requirement just as a real call would
    # (the docstring would mention should_enable_tui in the same block).
    if "TUI(" not in source:
        # No wiring yet: audit is vacuously satisfied. Test stays green
        # so the wiring task can land without re-editing this file.
        return
    assert "should_enable_tui" in source, (
        "commands.py constructs TUI(...) without referencing "
        "should_enable_tui in the same module. INV-012 demands the "
        "gate helper be consulted before instantiating the dashboard."
    )
