"""Tests for the FR-LC1 EvalRunner lifecycle skeleton.

Covers cliEval Phase 3 / Task T03.04 acceptance criteria:

* ``run_eval(spec, ...)`` executes the seven-step lifecycle in order
  (build isolation -> deploy hooks -> spawn -> inject -> observe ->
  assert -> teardown) and returns an :class:`EvalOutcome` (DM-001).
* Harness exceptions during steps 1-6 -> status ``ERRORED`` with
  ``error_class`` set to the fully-qualified exception classname.
* At least one failing ``ExpectResult`` -> status ``FAIL``.
* All ``ExpectResult.passed == True`` -> status ``PASS`` (and an empty
  expects tuple is PASS by design).
* Teardown is best-effort: a failing teardown does NOT flip the status,
  and the optional ``on_teardown_error`` callback fires instead.
* ``KeyboardInterrupt`` / ``SystemExit`` propagate so NFR-REL1 (T03.07)
  can convert them into an ``INTERRUPTED`` outcome at the orchestrator
  layer; teardown still runs with ``keep=True``.

Cross-link: ``artifacts/D-0048/spec.md`` documents the contract these
tests pin. ``HomeIsolation`` (T02.11) is frozen, so the lifecycle tests
use ``FakeHome`` — a duck-typed double that exposes the same four-method
surface ``run_eval`` consumes. The COMP-006 isolation contract itself is
covered by ``test_home_isolation.py`` / ``test_atomic_setup.py``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import pytest

from superclaude.cli.eval.config import EvalConfig
from superclaude.cli.eval.hook_adapter import HookDeployFailed
from superclaude.cli.eval.models import (
    EvalContext,
    EvalSpec,
    ExpectResult,
)
from superclaude.cli.eval.runner import (
    ExecutorContext,
    LifecycleExecutor,
    ObservedRun,
    run_eval,
)

# ---------------------------------------------------------------------------
# FakeHome — duck-typed HomeIsolation double
# ---------------------------------------------------------------------------


class FakeHome:
    """Mutable HomeIsolation stand-in for lifecycle tests.

    The real ``HomeIsolation`` is a frozen dataclass so its methods cannot
    be monkey-patched per-test. ``run_eval`` only requires the four-method
    surface (``setup(*, config)``, ``env()``, ``teardown(keep)``,
    ``home_path``) so a plain duck-typed double works here. The COMP-006
    isolation contract is exercised by ``test_home_isolation.py`` /
    ``test_atomic_setup.py``; this fake exists solely to make lifecycle
    scripting (per-test setup / teardown overrides) ergonomic.

    ``setup_impl`` and ``teardown_impl`` are callables tests overwrite to
    script behaviour; the defaults materialise a per-eval HOME under
    ``home_root`` so EvalContext construction (which dereferences
    ``home.home_path``) works end to end.
    """

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
        # Captures the value the runner passed to teardown(keep=...).
        self.last_teardown_keep: bool | None = None

    def _default_setup(self, *, config: EvalConfig) -> Path:
        self.home_root.mkdir(parents=True, exist_ok=True)
        home = self.home_root / f"{self.eval_id}-fake"
        home.mkdir(parents=True, exist_ok=True)
        self._home_path = home
        return home

    def _default_teardown(self, keep: bool) -> None:
        # No-op: the directory is left on disk regardless of ``keep``; the
        # tests assert on ``last_teardown_keep``, not on the filesystem.
        return None

    # --- Surface the runner calls ------------------------------------------

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


# ---------------------------------------------------------------------------
# Stub executor + Expect helpers
# ---------------------------------------------------------------------------


@dataclass
class RecordingExecutor:
    """LifecycleExecutor stub recording call order + canned observe result."""

    call_log: list[str] = field(default_factory=list)
    observed: ObservedRun = field(
        default_factory=lambda: ObservedRun(
            exit_code=0,
            stdout="stdout-bytes",
            stderr="",
            duration_sec=0.5,
        )
    )
    spawn_exc: BaseException | None = None
    inject_exc: BaseException | None = None
    observe_exc: BaseException | None = None

    def spawn(self, ctx: ExecutorContext) -> None:
        self.call_log.append("spawn")
        if self.spawn_exc is not None:
            raise self.spawn_exc

    def inject(self, ctx: ExecutorContext) -> None:
        self.call_log.append("inject")
        if self.inject_exc is not None:
            raise self.inject_exc

    def observe(self, ctx: ExecutorContext) -> ObservedRun:
        self.call_log.append("observe")
        if self.observe_exc is not None:
            raise self.observe_exc
        return self.observed


# Sanity check that RecordingExecutor satisfies the Protocol structurally.
_PROTOCOL_CHECK: LifecycleExecutor = RecordingExecutor()


def passing_expect(name: str = "ok") -> Callable[[EvalContext], ExpectResult]:
    return lambda ctx: ExpectResult(name=name, passed=True)


def failing_expect(name: str = "fail") -> Callable[[EvalContext], ExpectResult]:
    return lambda ctx: ExpectResult(name=name, passed=False, message="nope")


def raising_expect(
    exc: BaseException, name: str = "boom"
) -> Callable[[EvalContext], ExpectResult]:
    def _go(ctx: EvalContext) -> ExpectResult:
        raise exc

    _go.__name__ = name
    return _go


def _invoke(
    *,
    spec: EvalSpec,
    home: FakeHome,
    config: EvalConfig,
    paths: dict[str, Path],
    executor: LifecycleExecutor,
    expects: tuple = (),
    deploy_hooks: Callable[[Path], None] | None = None,
    on_teardown_error: Callable[[BaseException], None] | None = None,
    keep_home_on_pass: bool = False,
):
    return run_eval(
        spec,
        home=home,  # type: ignore[arg-type]  # duck-typed double
        config=config,
        run_dir=paths["run_dir"],
        artifacts_dir=paths["artifacts_dir"],
        stdout_path=paths["stdout_path"],
        stderr_path=paths["stderr_path"],
        transcript_path=paths["transcript_path"],
        executor=executor,
        expect_callables=expects,
        deploy_hooks=deploy_hooks if deploy_hooks is not None else (lambda _p: None),
        on_teardown_error=on_teardown_error,
        keep_home_on_pass=keep_home_on_pass,
    )


# ---------------------------------------------------------------------------
# AC1: 7-step sequence executed in order
# ---------------------------------------------------------------------------


def test_run_eval_executes_all_seven_steps_in_order(
    eval_spec, home, eval_config, run_paths
):
    """The full sequence should hit setup -> deploy -> spawn -> inject ->
    observe -> assert -> teardown in exactly that order."""

    deploy_log: list[str] = []

    def deploy(home_path: Path) -> None:
        deploy_log.append("deploy_hooks")

    executor = RecordingExecutor()
    outcome = _invoke(
        spec=eval_spec,
        home=home,
        config=eval_config,
        paths=run_paths,
        executor=executor,
        expects=(passing_expect("ok"),),
        deploy_hooks=deploy,
    )

    assert outcome.status == "PASS"
    # setup runs before deploy_hooks runs before the executor sequence.
    assert home.call_log[0] == "setup"
    assert deploy_log == ["deploy_hooks"]
    assert executor.call_log == ["spawn", "inject", "observe"]
    # Teardown is last in the home call log.
    assert home.call_log[-1].startswith("teardown(")


# ---------------------------------------------------------------------------
# AC2: setup exception -> ERRORED
# ---------------------------------------------------------------------------


def test_run_eval_setup_exception_yields_errored(
    eval_spec, home, eval_config, run_paths
):
    def boom_setup(*, config: EvalConfig) -> Path:
        raise RuntimeError("setup blew up")

    home.setup_impl = boom_setup

    executor = RecordingExecutor()
    outcome = _invoke(
        spec=eval_spec,
        home=home,
        config=eval_config,
        paths=run_paths,
        executor=executor,
    )

    assert outcome.status == "ERRORED"
    assert outcome.error_class == "builtins.RuntimeError"
    assert outcome.expects == ()
    # Steps 1-5 failures pin duration to 0.0 per spec.
    assert outcome.duration_sec == 0.0
    # Executor was never touched.
    assert executor.call_log == []


# ---------------------------------------------------------------------------
# AC3: deploy_hooks exception -> ERRORED
# ---------------------------------------------------------------------------


def test_run_eval_deploy_hooks_exception_yields_errored(
    eval_spec, home, eval_config, run_paths
):
    failure = HookDeployFailed(
        error_tag="hooks-broken",
        home_path=Path("/tmp/whatever"),
        detail="hook deploy boom",
    )

    def deploy(_p: Path) -> None:
        raise failure

    executor = RecordingExecutor()
    outcome = _invoke(
        spec=eval_spec,
        home=home,
        config=eval_config,
        paths=run_paths,
        executor=executor,
        deploy_hooks=deploy,
    )

    assert outcome.status == "ERRORED"
    assert outcome.error_class.endswith("HookDeployFailed")
    assert outcome.expects == ()
    # Executor never saw a call after a failed deploy.
    assert executor.call_log == []
    assert outcome.duration_sec == 0.0


# ---------------------------------------------------------------------------
# AC4: spawn / inject / observe exceptions -> ERRORED
# ---------------------------------------------------------------------------


def test_run_eval_spawn_exception_yields_errored(
    eval_spec, home, eval_config, run_paths
):
    executor = RecordingExecutor(spawn_exc=RuntimeError("spawn died"))
    outcome = _invoke(
        spec=eval_spec,
        home=home,
        config=eval_config,
        paths=run_paths,
        executor=executor,
    )

    assert outcome.status == "ERRORED"
    assert outcome.error_class == "builtins.RuntimeError"
    assert executor.call_log == ["spawn"]
    assert outcome.duration_sec == 0.0


def test_run_eval_inject_exception_yields_errored(
    eval_spec, home, eval_config, run_paths
):
    executor = RecordingExecutor(inject_exc=ValueError("inject went wrong"))
    outcome = _invoke(
        spec=eval_spec,
        home=home,
        config=eval_config,
        paths=run_paths,
        executor=executor,
    )

    assert outcome.status == "ERRORED"
    assert outcome.error_class == "builtins.ValueError"
    assert executor.call_log == ["spawn", "inject"]


def test_run_eval_observe_exception_yields_errored(
    eval_spec, home, eval_config, run_paths
):
    executor = RecordingExecutor(observe_exc=OSError("pty closed early"))
    outcome = _invoke(
        spec=eval_spec,
        home=home,
        config=eval_config,
        paths=run_paths,
        executor=executor,
    )

    assert outcome.status == "ERRORED"
    assert outcome.error_class == "builtins.OSError"
    assert executor.call_log == ["spawn", "inject", "observe"]
    assert outcome.duration_sec == 0.0


# ---------------------------------------------------------------------------
# AC5: ExpectCallable raise -> ERRORED with partial expects
# ---------------------------------------------------------------------------


def test_run_eval_expect_raise_yields_errored(eval_spec, home, eval_config, run_paths):
    """An ExpectCallable that raises folds into ERRORED with the partial
    tuple of results gathered before the raise."""

    outcome = _invoke(
        spec=eval_spec,
        home=home,
        config=eval_config,
        paths=run_paths,
        executor=RecordingExecutor(),
        expects=(
            passing_expect("first"),
            raising_expect(RuntimeError("expect boom")),
            passing_expect("never_runs"),
        ),
    )

    assert outcome.status == "ERRORED"
    assert outcome.error_class == "builtins.RuntimeError"
    # Only the first (passing) result was recorded; the raising one and
    # everything after it is absent.
    assert len(outcome.expects) == 1
    assert outcome.expects[0].name == "first"
    assert outcome.expects[0].passed is True


# ---------------------------------------------------------------------------
# AC6: PASS only when all expects pass
# ---------------------------------------------------------------------------


def test_run_eval_passes_when_all_expects_pass(eval_spec, home, eval_config, run_paths):
    outcome = _invoke(
        spec=eval_spec,
        home=home,
        config=eval_config,
        paths=run_paths,
        executor=RecordingExecutor(),
        expects=(passing_expect("a"), passing_expect("b"), passing_expect("c")),
    )

    assert outcome.status == "PASS"
    assert outcome.error_class is None
    assert [r.name for r in outcome.expects] == ["a", "b", "c"]
    assert all(r.passed for r in outcome.expects)
    assert outcome.duration_sec == 0.5


def test_run_eval_empty_expects_yields_pass(eval_spec, home, eval_config, run_paths):
    """An eval with no Expects ran cleanly => PASS by design (spec §PASS
    precondition)."""

    outcome = _invoke(
        spec=eval_spec,
        home=home,
        config=eval_config,
        paths=run_paths,
        executor=RecordingExecutor(),
        expects=(),
    )
    assert outcome.status == "PASS"
    assert outcome.expects == ()


# ---------------------------------------------------------------------------
# AC7: any failing Expect -> FAIL
# ---------------------------------------------------------------------------


def test_run_eval_failing_expect_yields_fail(eval_spec, home, eval_config, run_paths):
    outcome = _invoke(
        spec=eval_spec,
        home=home,
        config=eval_config,
        paths=run_paths,
        executor=RecordingExecutor(),
        expects=(failing_expect("only"),),
    )
    assert outcome.status == "FAIL"
    assert outcome.error_class is None
    assert outcome.expects[0].passed is False


def test_run_eval_mixed_results_yields_fail(eval_spec, home, eval_config, run_paths):
    """Mixed pass/fail expects -> FAIL; all expects appear in the tuple."""

    outcome = _invoke(
        spec=eval_spec,
        home=home,
        config=eval_config,
        paths=run_paths,
        executor=RecordingExecutor(),
        expects=(passing_expect("a"), failing_expect("b"), passing_expect("c")),
    )
    assert outcome.status == "FAIL"
    # All three results landed — a failing Expect does NOT halt step 6
    # (unlike a raising one).
    assert [r.name for r in outcome.expects] == ["a", "b", "c"]
    assert [r.passed for r in outcome.expects] == [True, False, True]


# ---------------------------------------------------------------------------
# AC8: Teardown keep semantics
# ---------------------------------------------------------------------------


def test_run_eval_teardown_keep_true_on_errored(
    eval_spec, home, eval_config, run_paths
):
    outcome = _invoke(
        spec=eval_spec,
        home=home,
        config=eval_config,
        paths=run_paths,
        executor=RecordingExecutor(spawn_exc=RuntimeError("nope")),
    )

    assert outcome.status == "ERRORED"
    # Non-PASS outcomes force keep=True so the HOME survives forensics.
    assert home.last_teardown_keep is True


def test_run_eval_teardown_keep_true_on_fail(eval_spec, home, eval_config, run_paths):
    _invoke(
        spec=eval_spec,
        home=home,
        config=eval_config,
        paths=run_paths,
        executor=RecordingExecutor(),
        expects=(failing_expect(),),
    )
    assert home.last_teardown_keep is True


def test_run_eval_teardown_keep_false_on_pass_by_default(
    eval_spec, home, eval_config, run_paths
):
    _invoke(
        spec=eval_spec,
        home=home,
        config=eval_config,
        paths=run_paths,
        executor=RecordingExecutor(),
        expects=(passing_expect(),),
        keep_home_on_pass=False,
    )
    assert home.last_teardown_keep is False


def test_run_eval_teardown_keep_true_on_pass_when_requested(
    eval_spec, home, eval_config, run_paths
):
    _invoke(
        spec=eval_spec,
        home=home,
        config=eval_config,
        paths=run_paths,
        executor=RecordingExecutor(),
        expects=(passing_expect(),),
        keep_home_on_pass=True,
    )
    assert home.last_teardown_keep is True


# ---------------------------------------------------------------------------
# AC9: Teardown errors swallowed, callback invoked
# ---------------------------------------------------------------------------


def test_run_eval_teardown_error_swallowed_callback_invoked(
    eval_spec, home, eval_config, run_paths
):
    """A failing teardown must NOT flip status; the callback fires."""

    def boom_teardown(keep: bool) -> None:
        raise RuntimeError("teardown exploded")

    home.teardown_impl = boom_teardown

    captured: list[BaseException] = []
    outcome = _invoke(
        spec=eval_spec,
        home=home,
        config=eval_config,
        paths=run_paths,
        executor=RecordingExecutor(),
        expects=(passing_expect(),),
        on_teardown_error=captured.append,
    )

    # Status was PASS; teardown failure must NOT have flipped it.
    assert outcome.status == "PASS"
    assert len(captured) == 1
    assert isinstance(captured[0], RuntimeError)
    assert "teardown exploded" in str(captured[0])


def test_run_eval_teardown_error_without_callback_is_silent(
    eval_spec, home, eval_config, run_paths
):
    """Without a callback the teardown failure is simply swallowed."""

    def boom_teardown(keep: bool) -> None:
        raise OSError("teardown perm denied")

    home.teardown_impl = boom_teardown

    outcome = _invoke(
        spec=eval_spec,
        home=home,
        config=eval_config,
        paths=run_paths,
        executor=RecordingExecutor(),
        expects=(passing_expect(),),
    )
    # No exception bubbled; PASS preserved.
    assert outcome.status == "PASS"


# ---------------------------------------------------------------------------
# AC10: KeyboardInterrupt / SystemExit propagate; teardown(keep=True) runs
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "exc_type", [KeyboardInterrupt, SystemExit], ids=["sigint", "sysexit"]
)
def test_run_eval_keyboard_interrupt_propagates_with_teardown(
    exc_type, eval_spec, home, eval_config, run_paths
):
    executor = RecordingExecutor(spawn_exc=exc_type())

    with pytest.raises(exc_type):
        _invoke(
            spec=eval_spec,
            home=home,
            config=eval_config,
            paths=run_paths,
            executor=executor,
        )

    # NFR-REL1: teardown ran with keep=True so the partial HOME stays for
    # forensics.
    assert home.last_teardown_keep is True


def test_run_eval_keyboard_interrupt_in_expect_propagates(
    eval_spec, home, eval_config, run_paths
):
    """KeyboardInterrupt inside an ExpectCallable also propagates (not
    classified as ERRORED)."""

    with pytest.raises(KeyboardInterrupt):
        _invoke(
            spec=eval_spec,
            home=home,
            config=eval_config,
            paths=run_paths,
            executor=RecordingExecutor(),
            expects=(raising_expect(KeyboardInterrupt()),),
        )

    assert home.last_teardown_keep is True


# ---------------------------------------------------------------------------
# AC11: Returned outcome carries observed artifacts + duration
# ---------------------------------------------------------------------------


def test_run_eval_passes_observed_state_into_eval_context(
    eval_spec, home, eval_config, run_paths
):
    """The runner builds an EvalContext from observed state before
    invoking ExpectCallables — pin that ExpectCallables see the captured
    exit_code / stdout / duration."""

    seen: dict[str, object] = {}

    def inspecting_expect(ctx: EvalContext) -> ExpectResult:
        seen["exit_code"] = ctx.exit_code
        seen["stdout"] = ctx.stdout
        seen["duration_sec"] = ctx.duration_sec
        seen["eval_id"] = ctx.eval_spec.id
        seen["home_path"] = ctx.home_path
        return ExpectResult(name="inspect", passed=True)

    executor = RecordingExecutor(
        observed=ObservedRun(
            exit_code=42,
            stdout="captured-bytes",
            stderr="warnings",
            duration_sec=1.25,
        )
    )

    outcome = _invoke(
        spec=eval_spec,
        home=home,
        config=eval_config,
        paths=run_paths,
        executor=executor,
        expects=(inspecting_expect,),
    )

    assert outcome.status == "PASS"
    assert seen["exit_code"] == 42
    assert seen["stdout"] == "captured-bytes"
    assert seen["duration_sec"] == 1.25
    assert seen["eval_id"] == "ExampleEval1"
    assert isinstance(seen["home_path"], Path)


def test_run_eval_outcome_includes_observed_artifacts(
    eval_spec, home, eval_config, run_paths
):
    executor = RecordingExecutor(
        observed=ObservedRun(
            exit_code=0,
            stdout="",
            stderr="",
            duration_sec=0.1,
            artifacts={"hook_log": "hooks.jsonl"},
        )
    )

    outcome = _invoke(
        spec=eval_spec,
        home=home,
        config=eval_config,
        paths=run_paths,
        executor=executor,
    )

    assert outcome.status == "PASS"
    assert outcome.artifacts == {"hook_log": "hooks.jsonl"}
