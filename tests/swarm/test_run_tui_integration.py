"""INV-012 / FR-1..FR-7 -- ``swarm run --tui`` wiring integration tests.

These tests exercise the ``--tui`` wiring landed in
``cli/swarm/commands.py::run_cmd`` (Approach A: threaded dispatch + main-thread
file-tailing poller). Each covers one functional requirement of the driving
spec ``.dev/brainstorms/swarm-tui-wiring/merged-requirements.md``:

    * FR-3  -- ``--tui --detached`` AND ``--resume --tui`` both rejected
              (EXIT_USAGE), resume never enters the TUI loop.
    * FR-2  -- byte-identical no-regression on a non-TTY (``--tui`` is a no-op).
    * FR-5  -- a worker exception is re-raised UNMASKED after ``tui.stop()``.
    * FR-6  -- idempotent ``tui.stop()`` on clean / exception / SIGINT paths;
              SIGINT yields exit 130.
    * FR-7  -- forced-TTY run drives the dashboard from the tailed
              ``execution-log.jsonl`` (>=1 non-vacuous worker row, zero ANSI on
              the non-TTY CliRunner stream).
    * FR-4  -- the render poll loop's iteration ceiling bounds the spin while
              ``join()`` still drains the non-daemon worker.
    * C3/AC-004/NFR-001 -- ``dispatch_wave1`` / ``ParallelExecutor`` signatures
              stay frozen.

The forced-TTY seam monkeypatches ``should_enable_tui`` to ``True`` on the
SOURCE module ``superclaude.cli.swarm.tui`` because ``run_cmd`` resolves it via
a deferred function-local import (same idiom test_commands_run.py uses for
``dispatch_wave1``). New tests are UNMARKED -- no ``tui`` pytest marker is
registered and ``--strict-markers`` is on.
"""

from __future__ import annotations

import contextlib
import inspect
import os
import re
import sys
import threading

import pytest
from click.testing import CliRunner

import superclaude.cli.swarm.dispatch as dispatch_mod
import superclaude.cli.swarm.state as state_mod
import superclaude.cli.swarm.tui as tui_mod
from superclaude.cli.swarm import commands as commands_mod
from superclaude.cli.swarm.commands import (
    EXIT_OK,
    EXIT_USAGE,
    run_cmd,
)
from superclaude.cli.swarm.models import EventRecord, from_json
from superclaude.cli.swarm.tui import _project_workers
from superclaude.execution.parallel import ParallelExecutor

# ANSI detection (mirrors test_inv012_tui_opt_in.py:69-88 _assert_no_ansi).
_ANSI_CSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
_ANY_ESC_RE = re.compile(r"\x1b")


def _assert_no_ansi(payload: str, *, source: str) -> None:
    """Assert ``payload`` carries no terminal control sequences (INV-012)."""
    csi_match = _ANSI_CSI_RE.search(payload)
    esc_match = _ANY_ESC_RE.search(payload)
    assert csi_match is None and esc_match is None, (
        f"INV-012 violated: {source} contains terminal control bytes\n"
        f"  CSI match: {csi_match!r}\n"
        f"  ESC match: {esc_match!r}\n"
        f"  payload (first 400 chars): {payload[:400]!r}"
    )


def _write_padded_target(tmp_path, name: str = "target.py"):
    """Write a target file that clears the >=50 non-whitespace byte IMM-4 floor."""
    target = tmp_path / name
    target.write_text(
        "# tui wiring integration target\n"
        + "def hello() -> str:\n    return 'real stub dispatch'\n"
        + "# padding to clear the IMM-4 non-whitespace byte floor\n" * 6,
        encoding="utf-8",
    )
    return target


# ---------------------------------------------------------------------------
# FR-3 -- dual mutual-exclusion rejects (--tui --detached AND --resume --tui)
# ---------------------------------------------------------------------------


def test_fr3_tui_detached_rejected(tmp_path) -> None:
    """FR-3 (a): ``--tui --detached`` -> EXIT_USAGE naming the incompatibility.

    The fresh-run ``if tui and detached:`` guard fires before the detached
    branch (which returns before dispatch), so the combination errors instead
    of silently launching detached and ignoring ``--tui``.
    """
    target = _write_padded_target(tmp_path)
    output_dir = tmp_path / "out"
    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        [
            "--tui",
            "--detached",
            "--lens",
            "bare-review",
            "--transport",
            "stub",
            "--target",
            str(target),
            "--output",
            str(output_dir),
        ],
    )
    assert result.exit_code == EXIT_USAGE, (
        f"--tui --detached must exit EXIT_USAGE (2); got {result.exit_code}\n"
        f"output:\n{result.output}"
    )
    assert "--tui" in result.output and "--detached" in result.output, (
        f"the reject must name the --tui/--detached incompatibility:\n{result.output}"
    )


def test_fr3_resume_tui_rejected_without_entering_tui_loop(
    tmp_path, monkeypatch
) -> None:
    """FR-3 (b): ``--resume --tui`` -> EXIT_USAGE, resume never enters the TUI.

    The ``if tui:`` guard inside the resume branch fires before
    ``_run_resume_branch`` runs, so ``--tui`` is rejected (not silently
    ignored) and the resume path provably never constructs the dashboard. A
    sentinel ``TUI`` that raises on construction proves it is never built.
    """

    class _ExplodingTUI:
        def __init__(self, *args, **kwargs):
            raise AssertionError(
                "FR-3 violation: TUI was constructed on the --resume path "
                "(resume must reject --tui before entering the TUI loop)"
            )

    # Patch the SOURCE module so the deferred function-local import in run_cmd
    # would pick up the exploding sentinel if the resume path ever built a TUI.
    monkeypatch.setattr(tui_mod, "TUI", _ExplodingTUI)

    output_dir = tmp_path / "out"
    output_dir.mkdir()
    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        [
            "--resume",
            "some-job-id",
            "--tui",
            "--output",
            str(output_dir),
        ],
    )
    assert result.exit_code == EXIT_USAGE, (
        f"--resume --tui must exit EXIT_USAGE (2); got {result.exit_code}\n"
        f"output:\n{result.output}\nexc:{result.exception!r}"
    )
    assert "--tui" in result.output and "--resume" in result.output, (
        f"the reject must name the --tui/--resume incompatibility:\n{result.output}"
    )
    # The exploding sentinel never fired -> TUI was never constructed -> the
    # resume path did not enter the TUI loop. (If it had, result.exception
    # would be the AssertionError above and exit_code would be 1.)
    assert result.exception is None or isinstance(result.exception, SystemExit), (
        f"resume path must not raise into the TUI loop; got {result.exception!r}"
    )


# ---------------------------------------------------------------------------
# FR-1 -- TUI.update runs ONLY on the main thread (runtime probe)
# ---------------------------------------------------------------------------


def test_fr1_tui_update_only_runs_on_main_thread(tmp_path, monkeypatch) -> None:
    """FR-1: every ``tui.update`` call is invoked on the main thread.

    Monkeypatches ``TUI.update`` with a probe recording
    ``threading.get_ident()`` on each call and drives a forced-TTY
    ``run_cmd --tui`` so the poll loop actually renders. The mandatory vacuity
    guard (``assert seen_idents``) proves the probe ran; the second assertion
    proves the single-writer Console topology (dispatch runs on the worker
    thread; only the main thread touches the Console).
    """
    main_ident = threading.get_ident()
    seen_idents: list[int] = []
    real_update = tui_mod.TUI.update

    def _probe(self, state, events):
        seen_idents.append(threading.get_ident())
        return real_update(self, state, events)

    monkeypatch.setattr(tui_mod.TUI, "update", _probe)
    # Force the gate open: run_cmd resolves should_enable_tui via a deferred
    # function-local import, so patch the SOURCE module.
    monkeypatch.setattr(tui_mod, "should_enable_tui", lambda *a, **k: True)

    target = _write_padded_target(tmp_path)
    output_dir = tmp_path / "out"
    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        [
            "--tui",
            "--lens",
            "bare-review",
            "--transport",
            "stub",
            "--target",
            str(target),
            "--output",
            str(output_dir),
        ],
    )

    assert result.exit_code == EXIT_OK, (
        f"forced-TTY --tui run must succeed; got {result.exit_code}\n"
        f"output:\n{result.output}\nexc:{result.exception!r}"
    )
    assert seen_idents, (
        "TUI.update was never invoked -- the FR-1 main-thread assertion is "
        "vacuous (the poll loop did not render)"
    )
    assert all(i == main_ident for i in seen_idents), (
        f"FR-1 violation: TUI.update ran off the main thread: {seen_idents} "
        f"vs main {main_ident}"
    )


# ---------------------------------------------------------------------------
# FR-2 -- byte-identical no-regression on a non-TTY (--tui is a no-op)
# ---------------------------------------------------------------------------


def test_fr2_tui_is_noop_on_non_tty(tmp_path) -> None:
    """FR-2: on a non-TTY, ``--tui`` triggers no thread/tail/Rich side effects.

    Runs ``run_cmd`` twice with identical args -- once without ``--tui`` and
    once with -- both to the default (non-TTY) CliRunner stream, and asserts an
    identical exit code, identical ``worker_done`` event count, and ZERO ANSI
    on BOTH. On a non-TTY ``should_enable_tui`` returns False, so ``--tui``
    routes to the unchanged synchronous dispatch path (no divergence).
    """
    target = _write_padded_target(tmp_path)
    out_off = tmp_path / "out_off"
    out_on = tmp_path / "out_on"

    def _invoke(extra: list[str], outdir) -> object:
        return CliRunner().invoke(
            run_cmd,
            extra
            + [
                "--lens",
                "bare-review",
                "--transport",
                "stub",
                "--target",
                str(target),
                "--output",
                str(outdir),
            ],
        )

    result_off = _invoke([], out_off)
    result_on = _invoke(["--tui"], out_on)

    assert result_off.exit_code == EXIT_OK, (
        f"baseline (no --tui) must succeed; got {result_off.exit_code}\n"
        f"{result_off.output}"
    )
    assert result_on.exit_code == result_off.exit_code, (
        "FR-2: --tui must not change the exit code on a non-TTY; "
        f"got off={result_off.exit_code} on={result_on.exit_code}"
    )

    _assert_no_ansi(result_off.output, source="FR-2 baseline (no --tui)")
    _assert_no_ansi(result_on.output, source="FR-2 --tui on a non-TTY")

    log_off = (out_off / "execution-log.jsonl").read_text(encoding="utf-8")
    log_on = (out_on / "execution-log.jsonl").read_text(encoding="utf-8")
    assert log_off.count("worker_done") == log_on.count("worker_done") == 3, (
        "FR-2: --tui must produce identical worker_done event content on a "
        f"non-TTY; off={log_off.count('worker_done')} "
        f"on={log_on.count('worker_done')}"
    )


# ---------------------------------------------------------------------------
# REG-1 -- real-PTY smoke for concurrent worker stdout while Live is active
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    sys.platform == "win32" or not hasattr(os, "openpty"),
    reason="pty is POSIX-only",
)
def test_tui_real_pty_no_crash_under_concurrent_worker_stdout(
    tmp_path, monkeypatch
) -> None:
    """REG-1: worker-thread stdout on a real PTY must not crash Rich Live."""
    monkeypatch.setattr(commands_mod, "_TUI_POLL_INTERVAL_SEC", 0.01)
    monkeypatch.setattr(commands_mod, "_TUI_POLL_MAX_ITERATIONS", 20)

    real_dispatch = dispatch_mod.dispatch_wave1

    def _dispatch_with_stdout(*args, **kwargs):
        # Runs inside the swarm-wave1 worker thread. Delay briefly so the main
        # thread has started Live, then write to the real PTY-backed stdout.
        threading.Event().wait(0.05)
        for index in range(3):
            print(f"worker-stdout-race-{index}", flush=True)
            threading.Event().wait(0.01)
        return real_dispatch(*args, **kwargs)

    monkeypatch.setattr(dispatch_mod, "dispatch_wave1", _dispatch_with_stdout)

    target = _write_padded_target(tmp_path)
    output_dir = tmp_path / "pty"
    master_fd, slave_fd = os.openpty()
    captured: list[bytes] = []
    exit_code = EXIT_OK
    raised: BaseException | None = None

    try:
        with os.fdopen(slave_fd, "w", buffering=1, encoding="utf-8") as slave:
            with contextlib.redirect_stdout(slave), contextlib.redirect_stderr(slave):
                try:
                    run_cmd.main(
                        args=_tui_args(target, output_dir),
                        prog_name="swarm run",
                        standalone_mode=False,
                    )
                except SystemExit as exc:
                    exit_code = int(exc.code or 0)
                except BaseException as exc:  # noqa: BLE001 -- asserted below
                    raised = exc
                    exit_code = 1

        os.set_blocking(master_fd, False)
        while True:
            try:
                chunk = os.read(master_fd, 4096)
            except BlockingIOError:
                break
            except OSError:
                break
            if not chunk:
                break
            captured.append(chunk)
    finally:
        os.close(master_fd)

    output = b"".join(captured).decode("utf-8", errors="replace")
    assert raised is None, (
        "real-PTY --tui run must not raise under concurrent worker stdout; "
        f"got {raised!r}\noutput:\n{output[:1000]}"
    )
    assert exit_code == EXIT_OK, (
        f"real-PTY --tui run must exit cleanly; got {exit_code}\n"
        f"output:\n{output[:1000]}"
    )
    assert "worker-stdout-race-" in output, (
        "REG-1 smoke did not exercise concurrent worker stdout; PTY output was:\n"
        f"{output[:1000]}"
    )
    assert "Traceback" not in output, (
        "REG-1 violation: concurrent worker stdout under Live produced a traceback:\n"
        f"{output[:1000]}"
    )


# ---------------------------------------------------------------------------
# FR-5 -- a worker exception is re-raised UNMASKED after tui.stop()
# ---------------------------------------------------------------------------


def test_fr5_worker_exception_reraised_unmasked_after_stop(
    tmp_path, monkeypatch
) -> None:
    """FR-5: the ORIGINAL worker exception reaches the caller, after stop()."""

    def _boom(*args, **kwargs):
        raise RuntimeError("boom-FR5")

    # run_cmd resolves dispatch_wave1 via a deferred import from the dispatch
    # source module; patch it there so the threaded worker calls the boom fake.
    monkeypatch.setattr(dispatch_mod, "dispatch_wave1", _boom)
    monkeypatch.setattr(tui_mod, "should_enable_tui", lambda *a, **k: True)

    # Spy on TUI.stop to confirm it ran (terminal restored) before the re-raise.
    stop_calls: list[int] = []
    real_stop = tui_mod.TUI.stop

    def _stop_spy(self):
        stop_calls.append(1)
        return real_stop(self)

    monkeypatch.setattr(tui_mod.TUI, "stop", _stop_spy)

    target = _write_padded_target(tmp_path)
    output_dir = tmp_path / "out"
    result = CliRunner().invoke(
        run_cmd,
        [
            "--tui",
            "--lens",
            "bare-review",
            "--transport",
            "stub",
            "--target",
            str(target),
            "--output",
            str(output_dir),
        ],
    )

    # (a) non-zero exit.
    assert result.exit_code != 0, (
        "FR-5: a worker exception must yield a non-zero exit; got "
        f"{result.exit_code}\noutput:\n{result.output}"
    )
    # (b) the ORIGINAL exception/message reaches the caller (not masked).
    assert isinstance(result.exception, RuntimeError), (
        f"FR-5: original RuntimeError must reach the caller; got {result.exception!r}"
    )
    assert "boom-FR5" in str(result.exception), (
        f"FR-5: original message must not be masked; got {result.exception!r}"
    )
    # (c) tui.stop() ran (idempotent teardown before the re-raise).
    assert stop_calls, "FR-5: tui.stop() did not run before the worker re-raise"


def test_drift3_reader_error_does_not_mask_worker_crash(tmp_path, monkeypatch) -> None:
    """DRIFT-3: reader exceptions must not bypass worker crash re-raise."""
    sentinel = RuntimeError("boom-DRIFT3-worker")

    def _boom(*args, **kwargs):
        raise sentinel

    monkeypatch.setattr(dispatch_mod, "dispatch_wave1", _boom)
    monkeypatch.setattr(tui_mod, "should_enable_tui", lambda *a, **k: True)

    real_read_state = state_mod.read_state
    read_failures: list[int] = []

    def _read_state_raises_once(path):
        if not read_failures:
            read_failures.append(1)
            raise ValueError("boom-DRIFT3-reader")
        return real_read_state(path)

    monkeypatch.setattr(state_mod, "read_state", _read_state_raises_once)

    stop_calls: list[int] = []
    real_stop = tui_mod.TUI.stop

    def _stop_spy(self):
        stop_calls.append(1)
        return real_stop(self)

    monkeypatch.setattr(tui_mod.TUI, "stop", _stop_spy)

    target = _write_padded_target(tmp_path)
    result = CliRunner().invoke(run_cmd, _tui_args(target, tmp_path / "drift3"))

    assert read_failures, "DRIFT-3 regression seam did not raise the reader error"
    assert result.exception is sentinel, (
        "DRIFT-3: worker exception must dominate a reader error; got "
        f"{result.exception!r}\noutput:\n{result.output}"
    )
    assert "boom-DRIFT3-reader" not in str(result.exception), (
        f"DRIFT-3: reader error masked the worker crash: {result.exception!r}"
    )
    assert stop_calls, "DRIFT-3: tui.stop() did not run before worker re-raise"


def test_drift4_sigint_does_not_mask_worker_crash(tmp_path, monkeypatch) -> None:
    """DRIFT-4: worker crash dominates a concurrent SIGINT path."""
    sentinel = RuntimeError("boom-DRIFT4-worker")

    def _boom(*args, **kwargs):
        raise sentinel

    monkeypatch.setattr(dispatch_mod, "dispatch_wave1", _boom)
    monkeypatch.setattr(tui_mod, "should_enable_tui", lambda *a, **k: True)

    stop_calls: list[int] = []
    real_stop = tui_mod.TUI.stop

    def _stop_spy(self):
        stop_calls.append(1)
        return real_stop(self)

    def _update_raises_kbd(self, state, events):
        raise KeyboardInterrupt

    monkeypatch.setattr(tui_mod.TUI, "stop", _stop_spy)
    monkeypatch.setattr(tui_mod.TUI, "update", _update_raises_kbd)

    target = _write_padded_target(tmp_path)
    result = CliRunner().invoke(run_cmd, _tui_args(target, tmp_path / "drift4"))

    assert result.exception is sentinel, (
        "DRIFT-4: worker exception must dominate concurrent SIGINT; got "
        f"exit={result.exit_code} exception={result.exception!r}\n"
        f"output:\n{result.output}"
    )
    assert result.exit_code != 130, (
        "DRIFT-4: concurrent worker crash must not be surfaced as clean SIGINT "
        f"Exit(130); got {result.exit_code}"
    )
    assert stop_calls, "DRIFT-4: tui.stop() did not run before worker re-raise"


# ---------------------------------------------------------------------------
# FR-6 -- idempotent tui.stop() on clean / exception / SIGINT exit paths
# ---------------------------------------------------------------------------


def _tui_args(target, output_dir) -> list[str]:
    return [
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


def test_fr6_stop_runs_on_all_three_exit_paths(tmp_path, monkeypatch) -> None:
    """FR-6: tui.stop() runs (idempotent) on clean / exception / SIGINT exits.

    The SIGINT path additionally asserts the exit code is SPECIFICALLY 130
    (128 + SIGINT 2), surfaced deterministically by the run_cmd glue after the
    finally restores the terminal.
    """
    target = _write_padded_target(tmp_path)

    # (a) CLEAN -- a forced-TTY run to completion: stop() called exactly once,
    #     and a second explicit stop() is a no-op (idempotent).
    with monkeypatch.context() as m:
        m.setattr(tui_mod, "should_enable_tui", lambda *a, **k: True)
        stop_calls: list[int] = []
        captured: dict = {}
        real_stop = tui_mod.TUI.stop

        def _stop_spy(self):
            stop_calls.append(1)
            captured["tui"] = self
            return real_stop(self)

        m.setattr(tui_mod.TUI, "stop", _stop_spy)
        result = CliRunner().invoke(run_cmd, _tui_args(target, tmp_path / "clean"))
        assert result.exit_code == EXIT_OK, (
            f"clean --tui run must succeed; got {result.exit_code}\n"
            f"{result.output}\n{result.exception!r}"
        )
        assert len(stop_calls) == 1, (
            f"FR-6 clean: stop() must be called exactly once during the run; "
            f"got {len(stop_calls)}"
        )
        # A second explicit stop() must be a harmless no-op (idempotent).
        captured["tui"].stop()
        assert captured["tui"]._live is None, (
            "FR-6 clean: stop() is not idempotent -- _live not cleared after a "
            "second stop()"
        )

    # (b) EXCEPTION -- dispatch raises: stop() still runs (shares the FR-5 seam).
    def _boom(*args, **kwargs):
        raise RuntimeError("boom-FR6")

    with monkeypatch.context() as m:
        m.setattr(dispatch_mod, "dispatch_wave1", _boom)
        m.setattr(tui_mod, "should_enable_tui", lambda *a, **k: True)
        exc_stop_calls: list[int] = []
        real_stop = tui_mod.TUI.stop

        def _exc_stop_spy(self):
            exc_stop_calls.append(1)
            return real_stop(self)

        m.setattr(tui_mod.TUI, "stop", _exc_stop_spy)
        result = CliRunner().invoke(run_cmd, _tui_args(target, tmp_path / "exc"))
        assert result.exit_code != 0, (
            f"FR-6 exception: a worker exception must exit non-zero; got "
            f"{result.exit_code}"
        )
        assert exc_stop_calls, "FR-6 exception: stop() did not run on the error path"

    # (c) SIGINT -- KeyboardInterrupt during the poll loop: stop() runs AND the
    #     exit code is SPECIFICALLY 130.
    with monkeypatch.context() as m:
        m.setattr(tui_mod, "should_enable_tui", lambda *a, **k: True)
        sigint_stop_calls: list[int] = []
        real_stop = tui_mod.TUI.stop

        def _sigint_stop_spy(self):
            sigint_stop_calls.append(1)
            return real_stop(self)

        def _update_raises_kbd(self, state, events):
            raise KeyboardInterrupt

        m.setattr(tui_mod.TUI, "stop", _sigint_stop_spy)
        m.setattr(tui_mod.TUI, "update", _update_raises_kbd)
        result = CliRunner().invoke(run_cmd, _tui_args(target, tmp_path / "sigint"))
        assert result.exit_code == 130, (
            f"FR-6 SIGINT: an uncaught KeyboardInterrupt must surface as exit "
            f"130 (128+2); got {result.exit_code}\n{result.exception!r}"
        )
        assert sigint_stop_calls, (
            "FR-6 SIGINT: stop() did not run on the interrupt path "
            "(terminal not restored)"
        )


# ---------------------------------------------------------------------------
# FR-7 -- forced-TTY run drives the dashboard from the tailed execution log
# ---------------------------------------------------------------------------


def test_fr7_forced_tty_run_drives_dashboard_from_tailed_log(
    tmp_path, monkeypatch
) -> None:
    """FR-7: a forced-TTY ``--tui`` run projects >=1 worker row from the log.

    Drives a real stub dispatch with the gate forced open, then projects the
    durable ``execution-log.jsonl`` via ``_project_workers`` and asserts a
    non-vacuous (advanced, non-pending) worker row sourced from the tailed log.
    A ``_tail_events`` spy proves the dashboard tail path actually ran (the
    regression guard: this path only executes when ``--tui`` is wired AND the
    gate is open). The INV-012 companion asserts zero ANSI on the non-TTY
    CliRunner stream.
    """
    monkeypatch.setattr(tui_mod, "should_enable_tui", lambda *a, **k: True)

    # Regression guard: spy on the module-level _tail_events so we can prove the
    # --tui dashboard tail loop actually ran. If --tui were unwired (or the gate
    # never opened), this spy would record zero calls and the assertion fails.
    tail_calls: list[int] = []
    real_tail = commands_mod._tail_events

    def _tail_spy(path, offset):
        tail_calls.append(1)
        return real_tail(path, offset)

    monkeypatch.setattr(commands_mod, "_tail_events", _tail_spy)

    target = _write_padded_target(tmp_path)
    output_dir = tmp_path / "out"
    result = CliRunner().invoke(
        run_cmd,
        [
            "--tui",
            "--lens",
            "bare-review",
            "--transport",
            "stub",
            "--target",
            str(target),
            "--output",
            str(output_dir),
        ],
    )

    assert result.exit_code == EXIT_OK, (
        f"forced-TTY --tui run must succeed; got {result.exit_code}\n"
        f"output:\n{result.output}\nexc:{result.exception!r}"
    )
    # Regression guard: the dashboard tail path executed (proves --tui wired).
    assert tail_calls, (
        "FR-7: _tail_events was never called -- the --tui dashboard tail loop "
        "did not run (regression: --tui unwired or gate never opened)"
    )

    # INV-012 companion: zero ANSI on the non-TTY CliRunner stream.
    _assert_no_ansi(result.output, source="FR-7 run_cmd --tui")

    # >=1 non-vacuous worker row sourced from the tailed execution-log.jsonl.
    jsonl = output_dir / "execution-log.jsonl"
    assert jsonl.is_file(), f"execution-log.jsonl missing under {output_dir}"
    records = [
        from_json(EventRecord, line)
        for line in jsonl.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    projected = _project_workers(records)
    assert len(projected) >= 1, (
        f"FR-7: projection must yield >=1 worker row from the tailed log; "
        f"got {projected}"
    )
    advanced = [s for s in projected.values() if s.status != "pending"]
    assert advanced, (
        "FR-7: projection is vacuous -- every worker row is still 'pending'; "
        f"no advanced row sourced from the log: {projected}"
    )
    # The stub transport stamps status='success' + model_label='stub-model-00'.
    assert any(s.status == "success" for s in advanced), (
        f"FR-7: expected a successful stub worker row; got {advanced}"
    )


# ---------------------------------------------------------------------------
# FR-4 -- the render-loop iteration ceiling bounds the spin without
#         truncating the non-daemon worker (anti-spin backstop).
# ---------------------------------------------------------------------------


def test_fr4_render_ceiling_bounds_spin_without_truncating_worker(
    tmp_path, monkeypatch
) -> None:
    """FR-4: the render poll loop exits at the ceiling; join() still completes.

    Injects a tiny ``_TUI_POLL_MAX_ITERATIONS`` ceiling and a worker that stays
    alive PAST it (a bounded block after the real dispatch). Asserts (a) the
    render loop exits after exactly ``ceiling`` renders -- bounded, no hang --
    and (b) ``join()`` then completes so the worker is NOT truncated and the run
    reaches its terminal ``EXIT_OK`` (the ceiling guarded only the render spin).
    """
    monkeypatch.setattr(tui_mod, "should_enable_tui", lambda *a, **k: True)
    monkeypatch.setattr(commands_mod, "_TUI_POLL_INTERVAL_SEC", 0.0)
    ceiling = 2
    monkeypatch.setattr(commands_mod, "_TUI_POLL_MAX_ITERATIONS", ceiling)

    # Wrap the real dispatch so the worker stays alive (a bounded ~0.3s block)
    # well past the 2-iteration render ceiling, then returns the real result so
    # the downstream continuation runs unchanged.
    real_dispatch = dispatch_mod.dispatch_wave1

    def _slow_dispatch(*args, **kwargs):
        result = real_dispatch(*args, **kwargs)
        threading.Event().wait(0.3)  # outlive the render ceiling; never set
        return result

    monkeypatch.setattr(dispatch_mod, "dispatch_wave1", _slow_dispatch)

    # Count render iterations via the per-iteration _tail_events call.
    tail_calls: list[int] = []
    real_tail = commands_mod._tail_events

    def _tail_spy(path, offset):
        tail_calls.append(1)
        return real_tail(path, offset)

    monkeypatch.setattr(commands_mod, "_tail_events", _tail_spy)

    target = _write_padded_target(tmp_path)
    output_dir = tmp_path / "out"
    result = CliRunner().invoke(
        run_cmd,
        [
            "--tui",
            "--lens",
            "bare-review",
            "--transport",
            "stub",
            "--target",
            str(target),
            "--output",
            str(output_dir),
        ],
    )

    # (a) the render loop exited AT THE CEILING (exactly `ceiling` renders while
    #     the worker was still alive), not because the worker died -> bounded
    #     spin, no hang.
    assert len(tail_calls) == ceiling, (
        f"FR-4: render loop must break at the ceiling ({ceiling} renders); "
        f"got {len(tail_calls)} (a different count means the loop did not honor "
        "the ceiling)"
    )
    # (b) after the ceiling broke the loop, join() completed and the run reached
    #     its terminal EXIT_OK -- the non-daemon worker was NOT truncated.
    assert result.exit_code == EXIT_OK, (
        f"FR-4: join() must complete the worker after the render ceiling; the "
        f"run must reach EXIT_OK. got {result.exit_code}\n"
        f"output:\n{result.output}\nexc:{result.exception!r}"
    )


# ---------------------------------------------------------------------------
# C3 / AC-004 / NFR-001 -- frozen signatures (dispatch_wave1 / ParallelExecutor)
# ---------------------------------------------------------------------------


def test_frozen_signatures_unchanged() -> None:
    """C3/AC-004/NFR-001: dispatch_wave1 + ParallelExecutor signatures frozen.

    The TUI wiring must NOT alter these signatures (the poll loop lives in the
    caller, run_cmd, not in dispatch_wave1). Pinned via ``inspect.signature``
    so any accidental drift introduced by the wiring fails here.
    """
    # dispatch_wave1: positional preflight_result, transport=None, then five
    # keyword-only params transport_for_slot / prompt / parallel_executor /
    # worker_spec / logger.
    sig = inspect.signature(dispatch_mod.dispatch_wave1)
    params = list(sig.parameters.values())
    names = [p.name for p in params]
    assert names == [
        "preflight_result",
        "transport",
        "transport_for_slot",
        "prompt",
        "parallel_executor",
        "worker_spec",
        "logger",
    ], f"dispatch_wave1 parameter names/order drifted: {names}"

    kinds = {p.name: p.kind for p in params}
    assert kinds["preflight_result"] == inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert kinds["transport"] == inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert sig.parameters["transport"].default is None
    for kw in (
        "transport_for_slot",
        "prompt",
        "parallel_executor",
        "worker_spec",
        "logger",
    ):
        assert kinds[kw] == inspect.Parameter.KEYWORD_ONLY, (
            f"dispatch_wave1 param {kw!r} must stay keyword-only; got {kinds[kw]}"
        )
    assert sig.parameters["transport_for_slot"].default is None
    assert sig.parameters["prompt"].default == ""
    assert sig.parameters["parallel_executor"].default is None
    assert sig.parameters["worker_spec"].default is None
    assert sig.parameters["logger"].default is None

    # ParallelExecutor: __init__(self, max_workers: int = 10) + plan + execute.
    init_sig = inspect.signature(ParallelExecutor.__init__)
    init_names = list(init_sig.parameters)
    assert init_names == ["self", "max_workers"], (
        f"ParallelExecutor.__init__ signature drifted: {init_names}"
    )
    assert init_sig.parameters["max_workers"].default == 10, (
        "ParallelExecutor.__init__ max_workers default drifted from 10: "
        f"{init_sig.parameters['max_workers'].default}"
    )
    assert callable(getattr(ParallelExecutor, "plan", None)), (
        "ParallelExecutor.plan missing (NFR-001 frozen surface)"
    )
    assert callable(getattr(ParallelExecutor, "execute", None)), (
        "ParallelExecutor.execute missing (NFR-001 frozen surface)"
    )
