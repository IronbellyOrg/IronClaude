"""Tests for NFR-REL1 signal handling and per-eval cancellation (T03.07 / D-0050).

Covers:

* :class:`CancellationToken` — set / observe / wait / signum semantics.
* :class:`SignalHandlerInstaller` — install/restore lifecycle, on_signal
  callback, main-thread guard, idempotency.
* :class:`EvalRunner` integration:
  * Pre-cancelled token short-circuits the lifecycle and returns
    ``INTERRUPTED`` without spawning.
  * ``KeyboardInterrupt`` raised by an Expect (worker thread) with a
    cancellation token wired produces an ``INTERRUPTED`` outcome rather
    than re-raising.
  * Without a cancellation token, the existing FR-LC1 re-raise contract
    is preserved (regression guard for T03.05 AC4).
  * Per-eval timeout invokes ``executor.cancel()`` so the production
    PtyDriver subprocess is killed and the zombie is reaped; JSONL log
    records ``executor_cancel_*`` events under the ``timeout`` step.
* Optional acceptance: a real subprocess zombie reap via a PtyDriver
  attached to ``/bin/sh`` is exercised when ``pexpect`` is available so
  the production cancel path is verified end-to-end.

This file complements ``test_runner_class.py`` (T03.05 coverage) — the
runner-class tests still own the bare-lifecycle / JSONL / timeout
classification AC; this file owns the NFR-REL1 cancellation contract.
"""

from __future__ import annotations

import json
import signal
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

import pytest

from superclaude.cli.eval.config import EvalConfig
from superclaude.cli.eval.models import (
    EvalContext,
    EvalSpec,
    ExpectResult,
)
from superclaude.cli.eval.runner import (
    EvalRunner,
    ExecutorContext,
    LifecycleExecutor,
    ObservedRun,
)
from superclaude.cli.eval.signal_handler import (
    DEFAULT_INTERRUPT_SIGNALS,
    EXIT_INTERRUPTED,
    CancellationToken,
    SignalHandlerInstaller,
)


# ---------------------------------------------------------------------------
# CancellationToken unit tests
# ---------------------------------------------------------------------------


class TestCancellationToken:
    def test_initial_state_is_not_cancelled(self) -> None:
        token = CancellationToken()
        assert token.is_cancelled() is False
        assert token.signum is None

    def test_cancel_flips_flag(self) -> None:
        token = CancellationToken()
        first = token.cancel()
        assert first is True
        assert token.is_cancelled() is True

    def test_cancel_records_signum(self) -> None:
        token = CancellationToken()
        token.cancel(signum=signal.SIGTERM)
        assert token.signum == int(signal.SIGTERM)

    def test_second_cancel_returns_false(self) -> None:
        token = CancellationToken()
        assert token.cancel() is True
        # Second call observes an already-cancelled token.
        assert token.cancel() is False

    def test_second_cancel_does_not_overwrite_signum(self) -> None:
        token = CancellationToken()
        token.cancel(signum=signal.SIGINT)
        token.cancel(signum=signal.SIGTERM)
        # First signum captured wins so partial-summary readers see the
        # signal that actually started the cancellation.
        assert token.signum == int(signal.SIGINT)

    def test_wait_returns_true_when_already_cancelled(self) -> None:
        token = CancellationToken()
        token.cancel()
        assert token.wait(timeout=0.01) is True

    def test_wait_times_out_when_not_cancelled(self) -> None:
        token = CancellationToken()
        assert token.wait(timeout=0.01) is False

    def test_wait_unblocks_on_concurrent_cancel(self) -> None:
        token = CancellationToken()

        def _canceller() -> None:
            time.sleep(0.05)
            token.cancel(signum=signal.SIGINT)

        t = threading.Thread(target=_canceller)
        t.start()
        try:
            assert token.wait(timeout=2.0) is True
            assert token.is_cancelled()
            assert token.signum == int(signal.SIGINT)
        finally:
            t.join()

    def test_exit_interrupted_constant_value(self) -> None:
        # Per design-spec §4 the SIGINT/SIGTERM exit code is 3.
        assert EXIT_INTERRUPTED == 3

    def test_default_interrupt_signals_covers_sigint_sigterm(self) -> None:
        assert signal.SIGINT in DEFAULT_INTERRUPT_SIGNALS
        assert signal.SIGTERM in DEFAULT_INTERRUPT_SIGNALS


# ---------------------------------------------------------------------------
# SignalHandlerInstaller unit tests
# ---------------------------------------------------------------------------


class TestSignalHandlerInstaller:
    def _is_main_thread(self) -> bool:
        return threading.current_thread() is threading.main_thread()

    def test_install_and_restore_round_trip(self) -> None:
        """Installer must restore previous handlers on context-manager exit."""

        if not self._is_main_thread():
            pytest.skip("signal.signal requires main thread")

        previous = signal.getsignal(signal.SIGUSR1)
        token = CancellationToken()
        try:
            with SignalHandlerInstaller(token, signals=(signal.SIGUSR1,)):
                installed = signal.getsignal(signal.SIGUSR1)
                assert installed is not previous, (
                    "installer should have replaced SIGUSR1 handler"
                )
            after = signal.getsignal(signal.SIGUSR1)
            assert after is previous, "installer must restore previous handler"
        finally:
            signal.signal(signal.SIGUSR1, previous)

    def test_handler_sets_cancellation_token(self) -> None:
        if not self._is_main_thread():
            pytest.skip("signal.signal requires main thread")

        previous = signal.getsignal(signal.SIGUSR1)
        token = CancellationToken()
        try:
            with SignalHandlerInstaller(token, signals=(signal.SIGUSR1,)):
                signal.raise_signal(signal.SIGUSR1)
                # signal.raise_signal is synchronous on Linux; the handler
                # runs before the call returns.
                assert token.is_cancelled() is True
                assert token.signum == int(signal.SIGUSR1)
        finally:
            signal.signal(signal.SIGUSR1, previous)

    def test_on_signal_callback_invoked(self) -> None:
        if not self._is_main_thread():
            pytest.skip("signal.signal requires main thread")

        previous = signal.getsignal(signal.SIGUSR1)
        token = CancellationToken()
        seen: list[int] = []

        def _on_signal(signum: int, frame, tok: CancellationToken) -> None:
            seen.append(signum)

        try:
            with SignalHandlerInstaller(
                token, signals=(signal.SIGUSR1,), on_signal=_on_signal
            ):
                signal.raise_signal(signal.SIGUSR1)
                assert seen == [int(signal.SIGUSR1)]
        finally:
            signal.signal(signal.SIGUSR1, previous)

    def test_on_signal_callback_failure_is_swallowed(self) -> None:
        if not self._is_main_thread():
            pytest.skip("signal.signal requires main thread")

        previous = signal.getsignal(signal.SIGUSR1)
        token = CancellationToken()

        def _on_signal(signum: int, frame, tok: CancellationToken) -> None:
            raise RuntimeError("bookkeeping failed")

        try:
            with SignalHandlerInstaller(
                token, signals=(signal.SIGUSR1,), on_signal=_on_signal
            ):
                # Must not raise even though the callback raised.
                signal.raise_signal(signal.SIGUSR1)
                assert token.is_cancelled()
        finally:
            signal.signal(signal.SIGUSR1, previous)

    def test_install_twice_is_idempotent(self) -> None:
        if not self._is_main_thread():
            pytest.skip("signal.signal requires main thread")

        previous = signal.getsignal(signal.SIGUSR1)
        token = CancellationToken()
        installer = SignalHandlerInstaller(token, signals=(signal.SIGUSR1,))
        try:
            installer.install()
            after_first = signal.getsignal(signal.SIGUSR1)
            installer.install()
            after_second = signal.getsignal(signal.SIGUSR1)
            # Second install must not replace its own handler (which would
            # store its own handler as ``_previous`` and break restoration).
            assert after_second is after_first
            installer.restore()
            assert signal.getsignal(signal.SIGUSR1) is previous
        finally:
            signal.signal(signal.SIGUSR1, previous)

    def test_restore_without_install_is_noop(self) -> None:
        token = CancellationToken()
        installer = SignalHandlerInstaller(token, signals=(signal.SIGUSR1,))
        # Must not raise even though install was never called.
        installer.restore()

    def test_empty_signals_rejected(self) -> None:
        with pytest.raises(ValueError):
            SignalHandlerInstaller(CancellationToken(), signals=())

    def test_main_thread_guard(self) -> None:
        """Installing from a non-main thread raises ValueError."""

        token = CancellationToken()
        errors: list[BaseException] = []

        def _install() -> None:
            try:
                installer = SignalHandlerInstaller(
                    token, signals=(signal.SIGUSR1,)
                )
                installer.install()
            except BaseException as exc:  # noqa: BLE001
                errors.append(exc)

        t = threading.Thread(target=_install)
        t.start()
        t.join()
        assert errors, "expected install() to fail off the main thread"
        assert isinstance(errors[0], ValueError)


# ---------------------------------------------------------------------------
# Test doubles for EvalRunner integration tests
# ---------------------------------------------------------------------------


class FakeHome:
    """Mutable HomeIsolation stand-in (mirrors test_runner_class.FakeHome)."""

    def __init__(
        self,
        *,
        eval_id: str,
        home_root: Path,
        session_id: str = "sess-signal",
    ) -> None:
        self.eval_id = eval_id
        self.home_root = home_root
        self.session_id = session_id
        self.call_log: list[str] = []
        self._home_path: Optional[Path] = None
        self.last_teardown_keep: Optional[bool] = None

    def setup(self, *, config: EvalConfig) -> Path:
        self.call_log.append("setup")
        self.home_root.mkdir(parents=True, exist_ok=True)
        home = self.home_root / f"{self.eval_id}-fake"
        home.mkdir(parents=True, exist_ok=True)
        self._home_path = home
        return home

    def teardown(self, keep: bool) -> None:
        self.last_teardown_keep = keep
        self.call_log.append(f"teardown({keep})")

    def env(self) -> dict[str, str]:
        return {"HOME": str(self.home_path), "CLAUDE_SESSION_ID": self.session_id}

    @property
    def home_path(self) -> Path:
        if self._home_path is None:
            raise RuntimeError("setup() has not run")
        return self._home_path

    @property
    def is_set_up(self) -> bool:
        return self._home_path is not None


@dataclass
class CancelRecordingExecutor:
    """Executor that records ``cancel()`` invocations from the runner."""

    call_log: list[str] = field(default_factory=list)
    cancel_count: int = 0
    cancel_error: Optional[BaseException] = None
    observe_blocker: Optional[threading.Event] = None
    observe_started_evt: Optional[threading.Event] = None
    observed: ObservedRun = field(
        default_factory=lambda: ObservedRun(
            exit_code=0,
            stdout="ok",
            stderr="",
            duration_sec=0.1,
        )
    )

    def spawn(self, ctx: ExecutorContext) -> None:
        self.call_log.append("spawn")

    def inject(self, ctx: ExecutorContext) -> None:
        self.call_log.append("inject")

    def observe(self, ctx: ExecutorContext) -> ObservedRun:
        self.call_log.append("observe")
        if self.observe_started_evt is not None:
            self.observe_started_evt.set()
        if self.observe_blocker is not None:
            self.observe_blocker.wait()
        return self.observed

    def cancel(self) -> None:
        self.cancel_count += 1
        self.call_log.append("cancel")
        if self.cancel_error is not None:
            raise self.cancel_error


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def scratch_root(tmp_path: Path) -> Path:
    root = tmp_path / "scratch"
    root.mkdir()
    return root


@pytest.fixture
def eval_config(scratch_root: Path) -> EvalConfig:
    return EvalConfig(allowed_scratch_roots=(scratch_root,))


@pytest.fixture
def run_paths(tmp_path: Path) -> dict[str, Path]:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    artifacts_dir = run_dir / "artifacts"
    artifacts_dir.mkdir()
    return {
        "run_dir": run_dir,
        "artifacts_dir": artifacts_dir,
        "stdout_path": artifacts_dir / "stdout.log",
        "stderr_path": artifacts_dir / "stderr.log",
        "transcript_path": artifacts_dir / "pty.transcript",
    }


def _make_runner(
    *,
    home: FakeHome,
    eval_config: EvalConfig,
    executor: LifecycleExecutor,
    run_paths: dict[str, Path],
    expects: tuple = (),
    deploy_hooks: Optional[Callable[[Path], None]] = None,
    default_timeout_sec: Optional[float] = None,
    cancellation_token: Optional[CancellationToken] = None,
) -> EvalRunner:
    return EvalRunner(
        home=home,  # type: ignore[arg-type]
        config=eval_config,
        executor=executor,
        run_dir=run_paths["run_dir"],
        artifacts_dir=run_paths["artifacts_dir"],
        stdout_path=run_paths["stdout_path"],
        stderr_path=run_paths["stderr_path"],
        transcript_path=run_paths["transcript_path"],
        expect_callables=expects,
        deploy_hooks=deploy_hooks if deploy_hooks is not None else (lambda _p: None),
        default_timeout_sec=default_timeout_sec,
        cancellation_token=cancellation_token,
    )


def _passing_expect(name: str = "ok") -> Callable[[EvalContext], ExpectResult]:
    def _expect(ctx: EvalContext) -> ExpectResult:
        return ExpectResult(name=name, passed=True)

    _expect.__name__ = name
    return _expect


def _read_jsonl(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


# ---------------------------------------------------------------------------
# AC: Pre-cancelled token short-circuits to INTERRUPTED without spawning.
# ---------------------------------------------------------------------------


def test_pre_cancelled_token_returns_interrupted_without_spawn(
    scratch_root, eval_config, run_paths
):
    home = FakeHome(eval_id="PreCancel1", home_root=scratch_root)
    executor = CancelRecordingExecutor()
    token = CancellationToken()
    token.cancel(signum=signal.SIGINT)

    runner = _make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(_passing_expect(),),
        cancellation_token=token,
    )

    outcome = runner.run(EvalSpec(id="PreCancel1", title="pre"))

    assert outcome.status == "INTERRUPTED"
    assert outcome.error_class is None
    assert outcome.duration_sec == 0.0
    # Never spawned because cancellation observed at entry.
    assert "spawn" not in executor.call_log
    assert "observe" not in executor.call_log
    # Setup also never ran — the runner returns before HomeIsolation.setup.
    assert "setup" not in home.call_log


# ---------------------------------------------------------------------------
# AC: KeyboardInterrupt with a wired token converts to INTERRUPTED outcome.
# ---------------------------------------------------------------------------


def test_keyboard_interrupt_with_token_returns_interrupted(
    scratch_root, eval_config, run_paths
):
    home = FakeHome(eval_id="MidInterrupt1", home_root=scratch_root)
    executor = CancelRecordingExecutor()
    token = CancellationToken()

    def _boom(ctx: EvalContext) -> ExpectResult:
        # Simulate the user hitting Ctrl-C during assertion evaluation.
        raise KeyboardInterrupt("user hit Ctrl-C")

    runner = _make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(_boom,),
        cancellation_token=token,
    )

    outcome = runner.run(EvalSpec(id="MidInterrupt1", title="mid"))

    assert outcome.status == "INTERRUPTED"
    # Worker did reach observe before the interrupt fired (assertion step).
    assert "observe" in executor.call_log
    # Token observed the cancellation that the runner forwarded.
    assert token.is_cancelled() is True
    # Cancel was invoked on the executor as part of cleanup.
    assert executor.cancel_count == 1

    log_path = home.home_path / ".eval-logs" / "MidInterrupt1.jsonl"
    assert log_path.is_file(), "JSONL log missing"
    rows = _read_jsonl(log_path)
    events = [r["event"] for r in rows]
    assert "interrupted_fired" in events
    assert "executor_cancel_started" in events
    assert "executor_cancel_completed" in events
    outcome_rows = [r for r in rows if r["event"] == "outcome"]
    assert outcome_rows and outcome_rows[0]["extra"]["status"] == "INTERRUPTED"


def test_keyboard_interrupt_without_token_propagates(
    scratch_root, eval_config, run_paths
):
    """Regression guard: T03.05 AC4 still holds when no token is wired."""

    home = FakeHome(eval_id="LegacyInterrupt", home_root=scratch_root)
    executor = CancelRecordingExecutor()

    def _boom(ctx: EvalContext) -> ExpectResult:
        raise KeyboardInterrupt("user hit Ctrl-C")

    runner = _make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(_boom,),
        # cancellation_token deliberately not wired.
    )

    with pytest.raises(KeyboardInterrupt):
        runner.run(EvalSpec(id="LegacyInterrupt", title="legacy"))


# ---------------------------------------------------------------------------
# AC: Per-eval timeout invokes executor.cancel() and records the event.
# ---------------------------------------------------------------------------


def test_timeout_invokes_executor_cancel(scratch_root, eval_config, run_paths):
    """Per-eval timeout must trigger executor.cancel() so the PtyDriver dies."""

    home = FakeHome(eval_id="TimeoutCancel1", home_root=scratch_root)
    blocker = threading.Event()
    observe_started = threading.Event()
    executor = CancelRecordingExecutor(
        observe_blocker=blocker,
        observe_started_evt=observe_started,
    )

    runner = _make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(_passing_expect(),),
        default_timeout_sec=0.05,
    )

    outcome = runner.run(EvalSpec(id="TimeoutCancel1", title="tcancel"))
    blocker.set()

    assert outcome.status == "TIMEOUT"
    assert observe_started.is_set()
    # The cancel call must have run from the main thread before the
    # runner returned the TIMEOUT outcome.
    assert executor.cancel_count == 1

    log_path = home.home_path / ".eval-logs" / "TimeoutCancel1.jsonl"
    rows = _read_jsonl(log_path)
    events = [r["event"] for r in rows]
    assert "timeout_fired" in events
    assert "executor_cancel_started" in events
    assert "executor_cancel_completed" in events
    # Cancel-started precedes teardown so the subprocess dies first.
    assert events.index("executor_cancel_started") < events.index(
        "teardown_started"
    )


def test_timeout_swallows_cancel_failure(scratch_root, eval_config, run_paths):
    """A cancel() that raises must not block the TIMEOUT outcome."""

    home = FakeHome(eval_id="TimeoutCancelErr", home_root=scratch_root)
    blocker = threading.Event()
    executor = CancelRecordingExecutor(
        observe_blocker=blocker,
        cancel_error=RuntimeError("subprocess already gone"),
    )

    runner = _make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(_passing_expect(),),
        default_timeout_sec=0.05,
    )

    outcome = runner.run(EvalSpec(id="TimeoutCancelErr", title="errcancel"))
    blocker.set()

    assert outcome.status == "TIMEOUT"
    assert executor.cancel_count == 1

    log_path = home.home_path / ".eval-logs" / "TimeoutCancelErr.jsonl"
    rows = _read_jsonl(log_path)
    events = [r["event"] for r in rows]
    assert "executor_cancel_error" in events
    err_row = next(r for r in rows if r["event"] == "executor_cancel_error")
    assert err_row["extra"]["error_class"].endswith("RuntimeError")


def test_executor_without_cancel_logs_skipped(scratch_root, eval_config, run_paths):
    """Executors without cancel() get an executor_cancel_skipped event."""

    @dataclass
    class NoCancelExecutor:
        call_log: list[str] = field(default_factory=list)

        def spawn(self, ctx: ExecutorContext) -> None:
            self.call_log.append("spawn")

        def inject(self, ctx: ExecutorContext) -> None:
            self.call_log.append("inject")

        def observe(self, ctx: ExecutorContext) -> ObservedRun:
            self.call_log.append("observe")
            time.sleep(1.0)  # exceed budget
            return ObservedRun(exit_code=0, stdout="", stderr="", duration_sec=0)

    home = FakeHome(eval_id="NoCancel1", home_root=scratch_root)
    executor = NoCancelExecutor()

    runner = _make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,  # type: ignore[arg-type]
        run_paths=run_paths,
        expects=(_passing_expect(),),
        default_timeout_sec=0.05,
    )

    outcome = runner.run(EvalSpec(id="NoCancel1", title="nocancel"))
    assert outcome.status == "TIMEOUT"

    log_path = home.home_path / ".eval-logs" / "NoCancel1.jsonl"
    rows = _read_jsonl(log_path)
    events = [r["event"] for r in rows]
    assert "executor_cancel_skipped" in events
    skipped = next(r for r in rows if r["event"] == "executor_cancel_skipped")
    assert "cancel" in skipped["extra"]["reason"]


# ---------------------------------------------------------------------------
# AC: Real subprocess kill + zombie reap path (production cancel surface).
# ---------------------------------------------------------------------------


def test_pty_driver_terminate_kills_real_subprocess(tmp_path: Path) -> None:
    """End-to-end: PtyDriver.terminate(force=True) + close() reaps the child.

    This pins NFR-REL1's "kill PtyDriver + reap zombie" requirement against
    a real subprocess so a regression in pexpect behaviour or our wrapper
    would fail. Skipped automatically when ``pexpect`` is not installed.
    """

    pexpect = pytest.importorskip("pexpect")
    from superclaude.cli.eval.pty_driver import PtyDriver

    driver = PtyDriver(command=["/bin/sh", "-c", "sleep 30"])
    driver.spawn()
    pid = driver.pid
    assert pid is not None and pid > 0

    # Sanity: process is alive before termination.
    proc_path = Path(f"/proc/{pid}")
    assert proc_path.exists(), "child process should be running"

    driver.terminate(force=True)
    driver.close()

    # Allow a brief window for the OS to reap the zombie.
    deadline = time.monotonic() + 5.0
    while proc_path.exists() and time.monotonic() < deadline:
        time.sleep(0.05)

    assert not proc_path.exists(), (
        f"/proc/{pid} should be gone after terminate(force=True)+close()"
    )
