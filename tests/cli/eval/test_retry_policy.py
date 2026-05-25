"""Tests for the NFR-REL2 bounded retry policy (T03.08 / D-0051).

Pins the four acceptance bullets from the phase file:

* ``EvalRunner`` default ``retry_count == 0``; verified by a test that
  builds an ``EvalRunner`` against a counting executor, induces a FAIL,
  and confirms the executor's spawn/inject/observe trio is called
  exactly once (no automatic re-execution).
* ``EvalRunner`` rejects any non-zero ``retry_count`` at construction
  time so an accidental caller sweep cannot silently re-run failing
  evals and break the FR-RPT1 N'-vs-K invariant.
* The ``MCP_FLAKY_TAG`` constant exists on the class so future R3-mit
  (T05.23) retry-once work has a single, named pin to extend.
* The ``--eval <id>`` subset re-run path is documented in
  ``docs/eval/retry.md``.

The retry policy is a contract, not a code path: the runner does not
ship retry logic today. These tests therefore guard *absence* — they
fail loudly if the runner ever starts re-executing failed evals
without the OQ-10 work landing first.
"""

from __future__ import annotations

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
# FakeHome — duck-typed stand-in mirroring test_runner_class.py's surface
# ---------------------------------------------------------------------------


class FakeHome:
    """Minimal HomeIsolation stand-in for retry-policy tests."""

    def __init__(self, *, eval_id: str, home_root: Path) -> None:
        self.eval_id = eval_id
        self.home_root = home_root
        self._home_path: Path | None = None

    def setup(self, *, config: EvalConfig) -> Path:
        self.home_root.mkdir(parents=True, exist_ok=True)
        home = self.home_root / f"{self.eval_id}-fake"
        home.mkdir(parents=True, exist_ok=True)
        self._home_path = home
        return home

    def teardown(self, keep: bool) -> None:
        return None

    def env(self) -> dict[str, str]:
        return {"HOME": str(self.home_path), "CLAUDE_SESSION_ID": "sess-001"}

    @property
    def home_path(self) -> Path:
        if self._home_path is None:
            raise RuntimeError("FakeHome.setup() must be called before home_path")
        return self._home_path

    @property
    def is_set_up(self) -> bool:
        return self._home_path is not None


@dataclass
class CountingExecutor:
    """LifecycleExecutor that counts every spawn/inject/observe call.

    The retry-policy AC requires that a FAIL outcome must *not* trigger
    a second execution. We assert ``spawn_count == inject_count ==
    observe_count == 1`` after ``runner.run(spec)`` returns a FAIL.
    """

    observed: ObservedRun = field(
        default_factory=lambda: ObservedRun(
            exit_code=1,
            stdout="failed-output",
            stderr="boom",
            duration_sec=0.25,
        )
    )
    spawn_count: int = 0
    inject_count: int = 0
    observe_count: int = 0

    def spawn(self, ctx: ExecutorContext) -> None:
        self.spawn_count += 1

    def inject(self, ctx: ExecutorContext) -> None:
        self.inject_count += 1

    def observe(self, ctx: ExecutorContext) -> ObservedRun:
        self.observe_count += 1
        return self.observed


_PROTOCOL_CHECK: LifecycleExecutor = CountingExecutor()


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
    return FakeHome(eval_id="RetryPolicyEval1", home_root=scratch_root)


@pytest.fixture
def eval_spec() -> EvalSpec:
    return EvalSpec(id="RetryPolicyEval1", title="retry-policy")


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


def _failing_expect() -> Callable[[EvalContext], ExpectResult]:
    def _expect(ctx: EvalContext) -> ExpectResult:
        return ExpectResult(name="boom", passed=False, message="induced fail")

    _expect.__name__ = "boom"
    return _expect


def _make_runner(
    *,
    home: FakeHome,
    eval_config: EvalConfig,
    executor: CountingExecutor,
    run_paths: dict[str, Path],
    expects: tuple = (),
    retry_count: int | None = None,
) -> EvalRunner:
    kwargs: dict = dict(
        home=home,  # type: ignore[arg-type]
        config=eval_config,
        executor=executor,
        run_dir=run_paths["run_dir"],
        artifacts_dir=run_paths["artifacts_dir"],
        stdout_path=run_paths["stdout_path"],
        stderr_path=run_paths["stderr_path"],
        transcript_path=run_paths["transcript_path"],
        expect_callables=expects,
        deploy_hooks=lambda _p: None,
    )
    if retry_count is not None:
        kwargs["retry_count"] = retry_count
    return EvalRunner(**kwargs)


# ---------------------------------------------------------------------------
# AC1: DEFAULT_RETRY_COUNT is zero
# ---------------------------------------------------------------------------


def test_default_retry_count_is_zero():
    """The NFR-REL2 contract: default retry_count is 0."""

    assert EvalRunner.DEFAULT_RETRY_COUNT == 0


# ---------------------------------------------------------------------------
# AC2: a FAIL outcome does NOT trigger a second execution
# ---------------------------------------------------------------------------


def test_fail_outcome_does_not_retry(eval_spec, home, eval_config, run_paths):
    """FR-LC1 + NFR-REL2: a failing eval runs the executor exactly once.

    The runner does not ship retry logic, so this test guards against
    silent regressions: if a future change ever wraps run_eval in a
    retry loop, the counting executor's spawn/inject/observe trio will
    rise above 1 and this test will fail loudly.
    """

    executor = CountingExecutor()
    runner = _make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(_failing_expect(),),
    )

    outcome = runner.run(eval_spec)

    assert outcome.status == "FAIL"
    assert executor.spawn_count == 1, (
        f"NFR-REL2 violated: spawn called {executor.spawn_count} times "
        "(expected 1 — retries are disabled)"
    )
    assert executor.inject_count == 1
    assert executor.observe_count == 1


def test_errored_outcome_does_not_retry(eval_spec, home, eval_config, run_paths):
    """An ERRORED outcome (executor raises) also runs exactly once.

    Mirrors ``test_fail_outcome_does_not_retry`` for the harness-error
    branch so a future retry sweep cannot silently re-run a harness
    failure either.
    """

    class RaisingExecutor:
        def __init__(self) -> None:
            self.spawn_count = 0
            self.inject_count = 0
            self.observe_count = 0

        def spawn(self, ctx: ExecutorContext) -> None:
            self.spawn_count += 1

        def inject(self, ctx: ExecutorContext) -> None:
            self.inject_count += 1
            raise RuntimeError("injected harness failure")

        def observe(self, ctx: ExecutorContext) -> ObservedRun:  # pragma: no cover
            self.observe_count += 1
            return ObservedRun(exit_code=0, stdout="", stderr="", duration_sec=0.0)

    executor = RaisingExecutor()
    runner = _make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,  # type: ignore[arg-type]
        run_paths=run_paths,
    )

    outcome = runner.run(eval_spec)

    assert outcome.status == "ERRORED"
    assert executor.spawn_count == 1
    assert executor.inject_count == 1
    assert executor.observe_count == 0  # inject raised; observe never reached


# ---------------------------------------------------------------------------
# AC3: non-zero retry_count is rejected at construction time
# ---------------------------------------------------------------------------


def test_non_zero_retry_count_rejected(home, eval_config, run_paths):
    """The runner refuses retry_count != 0 until R3-mit (T05.23) lands."""

    executor = CountingExecutor()
    with pytest.raises(ValueError) as excinfo:
        _make_runner(
            home=home,
            eval_config=eval_config,
            executor=executor,
            run_paths=run_paths,
            retry_count=1,
        )
    msg = str(excinfo.value)
    assert "retry_count" in msg
    assert "NFR-REL2" in msg
    assert "--eval" in msg


@pytest.mark.parametrize("bad", [-1, 2, 10])
def test_other_non_zero_retry_count_rejected(
    bad, home, eval_config, run_paths
):
    executor = CountingExecutor()
    with pytest.raises(ValueError):
        _make_runner(
            home=home,
            eval_config=eval_config,
            executor=executor,
            run_paths=run_paths,
            retry_count=bad,
        )


def test_explicit_zero_retry_count_accepted(
    eval_spec, home, eval_config, run_paths
):
    """Passing the default value explicitly must continue to work."""

    executor = CountingExecutor()
    runner = _make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        retry_count=0,
    )
    outcome = runner.run(eval_spec)
    assert outcome.status == "PASS"  # no expects, no observed failure
    assert executor.spawn_count == 1


# ---------------------------------------------------------------------------
# AC4: MCP_FLAKY_TAG constant exists for future R3-mit (T05.23) work
# ---------------------------------------------------------------------------


def test_mcp_flaky_tag_constant_defined():
    """R3-mit (T05.23) will key retry-once on this tag string."""

    assert hasattr(EvalRunner, "MCP_FLAKY_TAG")
    assert EvalRunner.MCP_FLAKY_TAG == "MCP-flaky"
    assert isinstance(EvalRunner.MCP_FLAKY_TAG, str)


# ---------------------------------------------------------------------------
# AC5: monkeypatch sanity — even injecting a retry hook does not loop
# ---------------------------------------------------------------------------


def test_monkeypatched_runner_confirms_no_retry_loop(
    eval_spec, home, eval_config, run_paths, monkeypatch
):
    """Documented monkeypatch path from the phase file's acceptance.

    The AC says: "verified by a test that monkeypatches EvalRunner and
    confirms no retries occur on failure." We monkeypatch the public
    ``run`` method to record how many times it is invoked by an outer
    caller. Internally, ``run`` must call the executor's spawn/inject/
    observe trio exactly once per call — never invoking itself
    recursively to retry.
    """

    executor = CountingExecutor()
    runner = _make_runner(
        home=home,
        eval_config=eval_config,
        executor=executor,
        run_paths=run_paths,
        expects=(_failing_expect(),),
    )

    calls: list[str] = []
    original_run = runner.run

    def wrapped(spec):
        calls.append(spec.id)
        return original_run(spec)

    monkeypatch.setattr(runner, "run", wrapped)

    outcome = runner.run(eval_spec)

    assert outcome.status == "FAIL"
    # The outer ``run`` is called exactly once by the test; the runner
    # does not invoke ``run`` recursively (no retry loop).
    assert calls == [eval_spec.id]
    # And the executor saw exactly one round-trip.
    assert (executor.spawn_count, executor.inject_count, executor.observe_count) == (
        1,
        1,
        1,
    )


# ---------------------------------------------------------------------------
# AC6: docs/eval/retry.md documents the --eval subset re-run path
# ---------------------------------------------------------------------------


def test_retry_docs_present_and_describe_subset_path():
    """The phase-file AC: docs/eval/retry.md documents the path."""

    repo_root = Path(__file__).resolve().parents[3]
    docs_path = repo_root / "docs" / "eval" / "retry.md"
    assert docs_path.exists(), f"Expected docs at {docs_path}"
    text = docs_path.read_text(encoding="utf-8")
    # Token-level guards so a future doc reorg cannot silently strip
    # the NFR-REL2 contract from the doc.
    assert "NFR-REL2" in text
    assert "--eval" in text
    assert "MCP-flaky" in text
    assert "retry_count" in text
