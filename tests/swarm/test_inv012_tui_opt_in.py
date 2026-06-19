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

import ast
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
        getattr(param, "name", None) == "tui" or "--tui" in getattr(param, "opts", ())
        for param in run_cmd.params
    )


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="pty.openpty is POSIX-only; --tui PTY check skipped on Windows",
)
def test_pty_invocation_with_tui_flag_when_wired(tmp_path: Path) -> None:
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

    # The --tui dashboard gate requires BOTH a TTY (the PTY below) AND an
    # --output directory (so there is an execution-log.jsonl + .swarm-state.json
    # to tail -- the G2 design decision: no --output => synchronous path, no
    # dashboard). Provide a real --target (padded past the >=50 non-whitespace
    # byte IMM-4 floor so preflight passes) and a fresh --output dir so the run
    # reaches the dashboard instead of erroring at preflight.
    target = tmp_path / "target.py"
    target.write_text(
        "# pty smoke target\n"
        + "def hello() -> str:\n    return 'real stub dispatch'\n"
        + "# padding to clear the IMM-4 non-whitespace byte floor\n" * 6,
        encoding="utf-8",
    )
    output_dir = tmp_path / "out"

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
                "--transport",
                "stub",
                "--target",
                str(target),
                "--output",
                str(output_dir),
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
                "--transport",
                "stub",
                "--target",
                str(target),
                "--output",
                str(output_dir),
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


# ---------------------------------------------------------------------------
# FR-1 single-writer Console topology -- AST import-graph reachability audit.
#
# The dispatch worker thread (Approach A) must NEVER touch the Console/Live:
# its only output channel is the filesystem Logger. This audit proves -- via a
# true AST walk, not a substring grep -- that NONE of the worker-side surfaces
# (``dispatch.py``, ``execution/parallel.py``, and ``_run_worker`` which lives
# in ``dispatch.py``) import Rich or the swarm ``tui`` module, nor reference the
# names ``TUI`` / ``Live`` / ``Console`` / ``should_enable_tui``. A regression
# that imported ``Live`` into ``dispatch.py`` (re-arming the #181/#182/#184
# cross-thread render crash class) fails this audit. The audit is per-file (it
# walks each module's own symbol table, not the whole call graph); the runtime
# main-thread ``threading.get_ident()`` probe below is the transitive backstop.
# ---------------------------------------------------------------------------

# ``rich`` root covers rich.console / rich.live / rich.panel / rich.table.
_FORBIDDEN_TUI_IMPORT_ROOTS = {"rich"}
_FORBIDDEN_TUI_IMPORT_MODULES = {
    "rich",
    "rich.console",
    "rich.live",
    "rich.panel",
    "rich.table",
    "superclaude.cli.swarm.tui",
}
# Symbol names a worker-side module must never name (TUI surface + the gate).
_FORBIDDEN_TUI_NAMES = {"TUI", "Live", "Console", "should_enable_tui"}


class _TuiSymbolVisitor(ast.NodeVisitor):
    """Collect forbidden TUI/Rich references and unguarded stdout writes."""

    def __init__(self) -> None:
        self.import_hits: list[tuple[int, str]] = []
        self.name_hits: list[tuple[int, str]] = []
        self.stdout_hits: list[tuple[int, str]] = []
        self._quiet_guard_depth = 0

    def _is_quiet_guard(self, node: ast.AST) -> bool:
        return (
            isinstance(node, ast.UnaryOp)
            and isinstance(node.op, ast.Not)
            and isinstance(node.operand, ast.Attribute)
            and node.operand.attr == "quiet"
            and isinstance(node.operand.value, ast.Name)
            and node.operand.value.id == "self"
        )

    def _is_quiet_guarded(self) -> bool:
        return self._quiet_guard_depth > 0

    def _sys_stream_attr(self, node: ast.Attribute) -> str | None:
        if (
            isinstance(node.value, ast.Name)
            and node.value.id == "sys"
            and node.attr in {"stdout", "stderr"}
        ):
            return f"sys.{node.attr}"
        if (
            isinstance(node.value, ast.Attribute)
            and isinstance(node.value.value, ast.Name)
            and node.value.value.id == "sys"
            and node.value.attr in {"stdout", "stderr"}
        ):
            return f"sys.{node.value.attr}.{node.attr}"
        return None

    def visit_Import(self, node: ast.Import) -> None:  # noqa: N802 -- ast API
        for alias in node.names:
            root = alias.name.split(".", 1)[0]
            if root in _FORBIDDEN_TUI_IMPORT_ROOTS or (
                alias.name in _FORBIDDEN_TUI_IMPORT_MODULES
            ):
                self.import_hits.append((node.lineno, alias.name))
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # noqa: N802
        module = node.module or ""
        root = module.split(".", 1)[0]
        if root in _FORBIDDEN_TUI_IMPORT_ROOTS or (
            module in _FORBIDDEN_TUI_IMPORT_MODULES
        ):
            self.import_hits.append((node.lineno, module))
        # Catch ``from superclaude.cli.swarm import tui`` and any
        # ``from ... import TUI / Live / Console / should_enable_tui``.
        for alias in node.names:
            if alias.name == "tui" or alias.name in _FORBIDDEN_TUI_NAMES:
                self.import_hits.append((node.lineno, f"{module}.{alias.name}"))
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:  # noqa: N802 -- ast API
        if self._is_quiet_guard(node.test):
            self._quiet_guard_depth += 1
            try:
                for stmt in node.body:
                    self.visit(stmt)
            finally:
                self._quiet_guard_depth -= 1
            for stmt in node.orelse:
                self.visit(stmt)
            return
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:  # noqa: N802 -- ast API
        if (
            isinstance(node.func, ast.Name)
            and node.func.id == "print"
            and not self._is_quiet_guarded()
        ):
            self.stdout_hits.append((node.lineno, "print"))
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:  # noqa: N802 -- ast API
        if node.id in _FORBIDDEN_TUI_NAMES:
            self.name_hits.append((node.lineno, node.id))
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:  # noqa: N802
        if node.attr in _FORBIDDEN_TUI_NAMES:
            self.name_hits.append((node.lineno, node.attr))
        stream_attr = self._sys_stream_attr(node)
        if stream_attr is not None and not self._is_quiet_guarded():
            self.stdout_hits.append((node.lineno, stream_attr))
        self.generic_visit(node)


_PARALLEL_WORKER_METHODS = {"plan", "execute", "_execute_group"}


def _scan_tui_symbols(path: Path) -> _TuiSymbolVisitor:
    """Parse ``path`` and return forbidden hits for its worker surface.

    This audit is per-file and non-transitive: it scans the two known worker
    surface modules' own ASTs, not the full call graph of every callable they
    invoke. If a new dispatch-reachable worker surface moves elsewhere, add it
    to ``worker_surfaces`` below.
    """
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    visitor = _TuiSymbolVisitor()
    if path.name == "parallel.py":
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name == "ParallelExecutor":
                for item in node.body:
                    if (
                        isinstance(item, ast.FunctionDef)
                        and item.name in _PARALLEL_WORKER_METHODS
                    ):
                        visitor.visit(item)
        return visitor
    visitor.visit(tree)
    return visitor


def test_worker_surfaces_have_zero_tui_reachability() -> None:
    """FR-1: dispatch.py / parallel.py / _run_worker never touch TUI/stdout.

    An AST audit proving the worker-side surfaces cannot import Rich or the
    swarm ``tui`` module, reference ``TUI`` / ``Live`` / ``Console`` /
    ``should_enable_tui``, or perform unguarded stdout/stderr writes. The audit
    is per-file (non-transitive) and includes a MANDATORY vacuity guard plus
    mutation guards so it cannot pass on a no-op.
    """
    repo_root = Path(__file__).resolve().parent.parent.parent
    dispatch_path = repo_root / "src" / "superclaude" / "cli" / "swarm" / "dispatch.py"
    parallel_path = repo_root / "src" / "superclaude" / "execution" / "parallel.py"

    worker_surfaces = [dispatch_path, parallel_path]
    scanned = 0
    for path in worker_surfaces:
        assert path.is_file(), (
            f"FR-1 audit target missing: {path}; cannot prove zero TUI reachability"
        )
        visitor = _scan_tui_symbols(path)
        scanned += 1
        assert not visitor.import_hits, (
            f"FR-1 violation: {path.name} imports a forbidden TUI/Rich module "
            f"(worker-side code must never touch the Console): "
            f"{visitor.import_hits}"
        )
        assert not visitor.name_hits, (
            f"FR-1 violation: {path.name} references a forbidden TUI symbol "
            f"(TUI/Live/Console/should_enable_tui): {visitor.name_hits}"
        )
        assert not visitor.stdout_hits, (
            f"FR-1 violation: {path.name} performs unguarded stdout/stderr "
            f"writes on a worker surface: {visitor.stdout_hits}"
        )

    # _run_worker lives in dispatch.py, so scanning dispatch.py covers the
    # ``_run_worker`` reachability requirement. Pin that fact so a future move
    # of _run_worker to another module re-surfaces the coverage gap here.
    dispatch_src = dispatch_path.read_text(encoding="utf-8")
    assert "def _run_worker(" in dispatch_src, (
        "_run_worker is expected to live in dispatch.py (covered by this "
        "audit); if it moved, extend the worker_surfaces list to include "
        "its new home so FR-1 reachability stays covered."
    )

    # Vacuity guard (MANDATORY): the audit must have actually scanned modules.
    assert scanned >= 1, "FR-1 audit scanned zero modules -- audit is vacuous"

    # Mutation guard: feed a synthetic source with the forbidden import and a
    # forbidden name reference; the visitor MUST flag both, proving the audit
    # cannot silently pass on a no-op.
    synthetic = "import rich.live\nx = Live()\n"
    mutant = _TuiSymbolVisitor()
    mutant.visit(ast.parse(synthetic))
    assert mutant.import_hits, (
        "FR-1 mutation guard failed: visitor did NOT flag a synthetic "
        "'import rich.live' -- the audit is not actually detecting imports"
    )
    assert mutant.name_hits, (
        "FR-1 mutation guard failed: visitor did NOT flag a synthetic 'Live' "
        "reference -- the audit is not actually detecting name references"
    )


def test_stdout_write_detector_is_not_a_noop() -> None:
    """FR-1 mutation guard: stdout writes are flagged unless quiet-gated."""
    unguarded = """
import sys
print('x')
sys.stdout.write('x')
"""
    mutant = _TuiSymbolVisitor()
    mutant.visit(ast.parse(unguarded))
    stdout_kinds = {kind for _, kind in mutant.stdout_hits}
    assert "print" in stdout_kinds, (
        "FR-1 stdout mutation guard failed: visitor did NOT flag a synthetic "
        "unguarded print()"
    )
    assert any(kind.startswith("sys.stdout") for kind in stdout_kinds), (
        "FR-1 stdout mutation guard failed: visitor did NOT flag a synthetic "
        "unguarded sys.stdout write"
    )

    guarded = """
import sys
class Worker:
    def run(self):
        if not self.quiet:
            print('x')
            sys.stdout.write('x')
            sys.stderr.flush()
"""
    guarded_mutant = _TuiSymbolVisitor()
    guarded_mutant.visit(ast.parse(guarded))
    assert not guarded_mutant.stdout_hits, (
        "FR-1 stdout mutation guard failed: visitor flagged stdout writes "
        "reachable only under if not self.quiet"
    )
