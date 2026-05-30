"""Tests for the COMP-004 ``EvalRunner`` class (T03.05 / D-0049).

Pins the four acceptance bullets from the phase file:

* Class ``EvalRunner`` exposes ``run(spec) -> EvalOutcome``.
* Per-eval JSONL log is written under ``home_path/.eval-logs/`` and
  contains at least the four required events
  (``setup_started``, ``spawn_started``, ``assertion_started``,
  ``teardown_started``).
* Per-eval timeout is honoured: tasks exceeding
  ``EvalSpec.timeout_sec`` return outcome with status ``TIMEOUT``.
* JSONL format is deterministic and JSON-parseable.

The lifecycle skeleton itself is exercised by ``test_eval_lifecycle.py``;
this file focuses on the COMP-004 layering on top.
"""

from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

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

# ---------------------------------------------------------------------------
# FakeHome — same duck-typed surface used by test_eval_lifecycle.py
# ---------------------------------------------------------------------------


class FakeHome:
    """Mutable HomeIsolation stand-in for runner-class tests."""

    def __init__(
        self,
        *,
        eval_id: str,
        home_root: Path,
        session_id: str = "sess-001",
    ) -> None:
        self.eval_id = eval_id
        self.home_root = home_root
        self.session_id = session_id
        self.call_log: list[str] = []
        self._home_path: Path | None = None
        self.setup_impl: Callable[..., Path] = self._default_setup
        self.teardown_impl: Callable[[bool], None] = self._default_teardown
        self.last_teardown_keep: bool | None = None

    def _default_setup(self, *, config: EvalConfig) -> Path:
        self.home_root.mkdir(parents=True, exist_ok=True)
        home = self.home_root / f"{self.eval_id}-fake"
        home.mkdir(parents=True, exist_ok=True)
        self._home_path = home
        return home

    def _default_teardown(self, keep: bool) -> None:
        return None

    def setup(self, *, config: EvalConfig) -> Path:
        self.call_log.append("setup")
        return self.setup_impl(config=config)

    def teardown(self, keep: bool) -> None:
        self.call_log.append(f"teardown(keep={keep})")
        self.last_teardown_keep = keep
        return self.teardown_impl(keep)

    def env(self) -> dict[str, str]:
        return {
            "HOME": str(self.home_path),
            "CLAUDE_SESSION_ID": self.session_id,
        }

    @property
    def home_path(self) -> Path:
        if self._home_path is None:
            raise RuntimeError(
                "FakeHome.setup() must be called before accessing home_path"
            )
        return self._home_path

    @property
    def is_set_up(self) -> bool:
        return self._home_path is not None


# ---------------------------------------------------------------------------
# Stub LifecycleExecutor
# ---------------------------------------------------------------------------


@dataclass
class RecordingExecutor:
    call_log: list[str] = field(default_factory=list)
    observed: ObservedRun = field(
        default_factory=lambda: ObservedRun(
            exit_code=0,
            stdout="stdout-bytes",
            stderr="",
            duration_sec=0.5,
        )
    )
    observe_blocker: threading.Event | None = None
    observe_started_evt: threading.Event | None = None

    def spawn(self, ctx: ExecutorContext) -> None:
        self.call_log.append("spawn")

    def inject(self, ctx: ExecutorContext) -> None:
        self.call_log.append("inject")

    def observe(self, ctx: ExecutorContext) -> ObservedRun:
        self.call_log.append("observe")
        if self.observe_started_evt is not None:
            self.observe_started_evt.set()
        if self.observe_blocker is not None:
            # Block forever to simulate a hung subprocess. The runner's
            # per-eval timeout will fire; the thread is daemon so the
            # test process exits cleanly even though this event is never
            # set.
            self.observe_blocker.wait()
        return self.observed


_PROTOCOL_CHECK: LifecycleExecutor = RecordingExecutor()


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
def home(scratch_root: Path) -> FakeHome:
    return FakeHome(eval_id="ExampleEval1", home_root=scratch_root)


@pytest.fixture
def eval_spec() -> EvalSpec:
    return EvalSpec(id="ExampleEval1", title="example")


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


def make_runner(
    *,
    home: FakeHome,
    eval_config: EvalConfig,
    executor: LifecycleExecutor,
    run_paths: dict[str, Path],
    expects: tuple = (),
    deploy_hooks: Callable[[Path], None] | None = None,
    default_timeout_sec: float | None = None,
    keep_home_on_pass: bool = False,
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
        keep_home_on_pass=keep_home_on_pass,
        default_timeout_sec=default_timeout_sec,
    )


def passing_expect(name: str = "ok"):
    def _expect(ctx: EvalContext) -> ExpectResult:
        return ExpectResult(name=name, passed=True)

    _expect.__name__ = name
    return _expect


def failing_expect(name: str = "nope"):
    def _expect(ctx: EvalContext) -> ExpectResult:
        return ExpectResult(name=name, passed=False, message="bad")

    _expect.__name__ = name
    return _expect


def read_jsonl(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


# ---------------------------------------------------------------------------
# AC1: run(spec) returns an EvalOutcome (PASS through the lifecycle)
# ---------------------------------------------------------------------------


def test_run_returns_eval_outcome(eval_spec, home, eval_config, run_paths):
    executor = RecordingExecutor()
    runner = make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(passing_expect("ok"),),
    )

    outcome = runner.run(eval_spec)

    assert outcome.status == "PASS"
    assert outcome.eval_id == "ExampleEval1"
    assert outcome.title == "example"
    assert executor.call_log == ["spawn", "inject", "observe"]
    assert home.call_log[0] == "setup"
    assert home.call_log[-1].startswith("teardown(")


def test_run_returns_fail_when_expect_fails(eval_spec, home, eval_config, run_paths):
    executor = RecordingExecutor()
    runner = make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(failing_expect("bad"),),
    )

    outcome = runner.run(eval_spec)

    assert outcome.status == "FAIL"
    assert outcome.expects[0].passed is False


# ---------------------------------------------------------------------------
# AC2: JSONL log written under home_path/.eval-logs/ with required events
# ---------------------------------------------------------------------------


def test_jsonl_log_written_with_required_events(
    eval_spec, home, eval_config, run_paths
):
    executor = RecordingExecutor()
    runner = make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(passing_expect("ok"),),
    )

    outcome = runner.run(eval_spec)
    assert outcome.status == "PASS"

    log_path = home.home_path / ".eval-logs" / "ExampleEval1.jsonl"
    assert log_path.is_file(), f"JSONL log missing at {log_path}"

    rows = read_jsonl(log_path)
    events = [row["event"] for row in rows]

    # AC requires at least these four events.
    for required in (
        "setup_started",
        "spawn_started",
        "assertion_started",
        "teardown_started",
    ):
        assert required in events, f"missing required event {required!r} in {events}"

    # Event ordering: setup_started precedes spawn_started precedes
    # assertion_started precedes teardown_started.
    idx = {name: events.index(name) for name in events}
    assert idx["setup_started"] < idx["spawn_started"]
    assert idx["spawn_started"] < idx["assertion_started"]
    assert idx["assertion_started"] < idx["teardown_started"]


def test_jsonl_format_is_deterministic(eval_spec, home, eval_config, run_paths):
    """Each JSONL row carries the documented five-field shape."""

    executor = RecordingExecutor()
    runner = make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(passing_expect("ok"),),
    )

    runner.run(eval_spec)

    log_path = home.home_path / ".eval-logs" / "ExampleEval1.jsonl"
    rows = read_jsonl(log_path)
    assert rows, "expected at least one row"

    for row in rows:
        assert set(row.keys()) == {"event", "ts_offset_sec", "eval_id", "step", "extra"}
        assert isinstance(row["event"], str)
        assert isinstance(row["ts_offset_sec"], (int, float))
        assert row["ts_offset_sec"] >= 0
        assert row["eval_id"] == "ExampleEval1"
        assert isinstance(row["step"], str)
        assert isinstance(row["extra"], dict)


def test_assertion_event_includes_index_and_name(
    eval_spec, home, eval_config, run_paths
):
    executor = RecordingExecutor()
    runner = make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(passing_expect("first"), passing_expect("second")),
    )
    runner.run(eval_spec)

    log_path = home.home_path / ".eval-logs" / "ExampleEval1.jsonl"
    rows = read_jsonl(log_path)
    starts = [r for r in rows if r["event"] == "assertion_started"]
    assert len(starts) == 2
    assert starts[0]["extra"]["index"] == 0
    assert starts[0]["extra"]["name"] == "first"
    assert starts[1]["extra"]["index"] == 1
    assert starts[1]["extra"]["name"] == "second"


def test_outcome_event_records_final_status(eval_spec, home, eval_config, run_paths):
    executor = RecordingExecutor()
    runner = make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(failing_expect("bad"),),
    )
    runner.run(eval_spec)

    log_path = home.home_path / ".eval-logs" / "ExampleEval1.jsonl"
    rows = read_jsonl(log_path)
    outcome_rows = [r for r in rows if r["event"] == "outcome"]
    assert len(outcome_rows) == 1
    assert outcome_rows[0]["extra"]["status"] == "FAIL"


# ---------------------------------------------------------------------------
# AC3: Per-eval timeout honoured → status TIMEOUT
# ---------------------------------------------------------------------------


def test_run_returns_timeout_when_observe_hangs(home, eval_config, run_paths):
    """A hung observe step must return an outcome with status TIMEOUT.

    The observe step blocks on an ``Event`` that is never set; the
    runner's per-eval timeout (50 ms) fires, reclassifies the outcome
    as TIMEOUT, and returns. The daemon worker thread is abandoned —
    NFR-REL1 (T03.07) is responsible for reaping it in production.
    """

    spec = EvalSpec(id="HangEval1", title="hang", timeout_sec=1)
    # Use default_timeout_sec to short-circuit the integer-second
    # minimum from EvalSpec.timeout_sec (which is typed as int seconds).
    blocker = threading.Event()
    observe_started = threading.Event()
    executor = RecordingExecutor(
        observe_blocker=blocker,
        observe_started_evt=observe_started,
    )

    # Re-bind home to the right eval id so the JSONL path matches the
    # spec id (the FakeHome derives the home dir from its construction
    # arg, not from the spec).
    fake_home = FakeHome(eval_id="HangEval1", home_root=home.home_root)

    runner = make_runner(
        home=fake_home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(passing_expect("noop"),),
        default_timeout_sec=0.05,  # 50 ms
    )

    t0 = time.monotonic()
    outcome = runner.run(spec)
    elapsed = time.monotonic() - t0

    # Unblock the worker so it can exit (daemon thread; not strictly
    # required for test correctness but keeps the fixture clean).
    blocker.set()

    assert observe_started.is_set(), "observe should have started before timeout"
    assert outcome.status == "TIMEOUT"
    assert outcome.error_class == "builtins.TimeoutError"
    assert outcome.eval_id == "HangEval1"
    # Runner returned promptly after the timeout budget elapsed.
    assert elapsed < 2.0, f"runner took {elapsed:.2f}s — timeout did not fire"


def test_timeout_event_recorded_in_jsonl(home, eval_config, run_paths):
    spec = EvalSpec(id="HangEval2", title="hang2")
    blocker = threading.Event()
    executor = RecordingExecutor(observe_blocker=blocker)

    fake_home = FakeHome(eval_id="HangEval2", home_root=home.home_root)
    runner = make_runner(
        home=fake_home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(passing_expect(),),
        default_timeout_sec=0.05,
    )

    outcome = runner.run(spec)
    blocker.set()

    assert outcome.status == "TIMEOUT"

    log_path = fake_home.home_path / ".eval-logs" / "HangEval2.jsonl"
    rows = read_jsonl(log_path)
    events = [r["event"] for r in rows]
    assert "timeout_fired" in events
    # The outcome row records TIMEOUT explicitly.
    outcome_rows = [r for r in rows if r["event"] == "outcome"]
    assert outcome_rows and outcome_rows[0]["extra"]["status"] == "TIMEOUT"


def test_no_timeout_when_spec_timeout_unset(eval_spec, home, eval_config, run_paths):
    """Without a spec timeout or default, the runner does not abort."""

    executor = RecordingExecutor()  # quick, deterministic observe
    runner = make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(passing_expect(),),
        default_timeout_sec=None,
    )
    outcome = runner.run(eval_spec)
    assert outcome.status == "PASS"


# ---------------------------------------------------------------------------
# AC4: KeyboardInterrupt in worker propagates to caller
# ---------------------------------------------------------------------------


def test_keyboard_interrupt_in_expect_propagates(
    eval_spec, home, eval_config, run_paths
):
    def boom(ctx: EvalContext) -> ExpectResult:
        raise KeyboardInterrupt("user hit Ctrl-C")

    executor = RecordingExecutor()
    runner = make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(boom,),
    )

    with pytest.raises(KeyboardInterrupt):
        runner.run(eval_spec)

    # JSONL still flushes — partial events survive Ctrl-C.
    log_path = home.home_path / ".eval-logs" / "ExampleEval1.jsonl"
    assert log_path.is_file()


# ---------------------------------------------------------------------------
# Sanity: log directory matches the documented constant
# ---------------------------------------------------------------------------


def test_log_dir_relpath_constant():
    assert EvalRunner.LOG_DIR_RELPATH == Path(".eval-logs")
