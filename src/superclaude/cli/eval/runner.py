"""FR-LC1 EvalRunner lifecycle skeleton.

This module lands the *skeleton* of the per-eval lifecycle the roadmap row
FR-LC1 / D-0048 (Task T03.04) declares. A single public entrypoint
``run_eval(spec, ...) -> EvalOutcome`` executes the seven-step sequence:

    1. build isolation  (HomeIsolation.setup)
    2. deploy hooks     (deploy_hooks_to)
    3. spawn            (executor.spawn)
    4. inject           (executor.inject)
    5. observe          (executor.observe)
    6. assert           (each ExpectCallable applied to an EvalContext)
    7. teardown         (HomeIsolation.teardown)

and maps the outcome to a DM-001 ``EvalOutcome`` (T03.01) following the
status-mapping rules documented in ``artifacts/D-0048/spec.md``:

* All applied ``ExpectCallable``s returned ``passed=True`` -> ``PASS``.
* At least one ``ExpectResult.passed`` is ``False`` and no harness
  exception fired -> ``FAIL``.
* Any exception other than ``KeyboardInterrupt`` / ``SystemExit`` raised
  during steps 1-6 -> ``ERRORED`` with ``error_class`` = fully-qualified
  exception classname.
* ``KeyboardInterrupt`` / ``SystemExit`` propagates so NFR-REL1
  (T03.07) can mark the outcome ``INTERRUPTED`` at the orchestrator
  layer. Teardown still runs with ``keep=True`` so the partial HOME
  survives for forensics.

The runner is intentionally testable without a real PTY: the spawn /
inject / observe trio is supplied as a :class:`LifecycleExecutor` protocol
so unit tests substitute stubs that return canned outputs. The COMP-004
runner class layer (T03.05 / D-0049) plugs in the concrete
``PtyDriver`` + ``ClaudeProcessAdapter`` executor and adds per-eval JSONL
logging and per-eval timeout enforcement.

Per-eval JSONL logging, per-eval timeout, signal handling, and the
SKIPPED capability-gate branch are explicitly out of scope; see
``artifacts/D-0048/spec.md`` for the full out-of-scope list.
"""

from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, ClassVar, Mapping, Optional, Protocol, Sequence

from .config import EvalConfig
from .hook_adapter import deploy_hooks_to
from .isolation import HomeIsolation
from .models import (
    EvalContext,
    EvalOutcome,
    EvalSpec,
    EvalStatus,
    ExpectResult,
)
from .retry import RetryOncePolicy
from .signal_handler import CancellationToken

__all__ = [
    "EvalRunner",
    "ExecutorContext",
    "ExpectCallable",
    "LifecycleExecutor",
    "ObservedRun",
    "run_eval",
]


# ---------------------------------------------------------------------------
# Public protocol surface
# ---------------------------------------------------------------------------


# An ExpectCallable is a function from ``EvalContext`` to ``ExpectResult``.
# FR-EXP1 (T04.01..T04.07) lands the concrete primitives; the runner only
# requires the callable contract today.
ExpectCallable = Callable[[EvalContext], ExpectResult]


@dataclass(frozen=True)
class ExecutorContext:
    """Post-isolation runtime state the executor needs.

    Carries the paths the runner has reserved for the eval's outputs plus
    the resolved environment overlay so the executor can spawn the
    subprocess against the per-eval HOME without re-deriving anything.

    Fields are intentionally minimal — the richer per-Expect
    :class:`EvalContext` (DM-010 / T03.03) is built *after* observe
    returns so it can carry the captured stdout/stderr/exit_code.
    """

    eval_spec: EvalSpec
    home: HomeIsolation
    home_path: Path
    run_dir: Path
    artifacts_dir: Path
    stdout_path: Path
    stderr_path: Path
    transcript_path: Path
    env: Mapping[str, str]


@dataclass(frozen=True)
class ObservedRun:
    """Result of the executor's spawn -> inject -> observe trio.

    The runner takes this and folds it into the :class:`EvalContext` that
    every :data:`ExpectCallable` receives in step 6.

    * ``exit_code``    — captured subprocess exit code; ``int``.
    * ``stdout``       — captured (PTY-stripped) stdout.
    * ``stderr``       — captured stderr.
    * ``duration_sec`` — wall-clock seconds from spawn to exit.
    * ``jsonl_paths``  — mapping of named JSONL log paths produced by the
      run (e.g. ``{"hook_log": ..., "telemetry": ...}``). Stored as an
      immutable :class:`Mapping`.
    * ``artifacts``    — mapping of artifact-name to absolute (or
      run-relative) path produced by the eval. Stored as an immutable
      :class:`Mapping`.
    """

    exit_code: int
    stdout: str
    stderr: str
    duration_sec: float
    jsonl_paths: Mapping[str, Path] = field(default_factory=dict)
    artifacts: Mapping[str, str] = field(default_factory=dict)


class LifecycleExecutor(Protocol):
    """Strategy that performs the spawn / inject / observe steps.

    Production code (T03.05) implements this on top of
    ``ClaudeProcessAdapter`` + ``PtyDriver``. Tests substitute a stub
    that records the call sequence and returns a canned
    :class:`ObservedRun`. Implementations should raise on failure;
    ``run_eval`` classifies any non-``KeyboardInterrupt`` /
    ``SystemExit`` exception as ``ERRORED``.
    """

    def spawn(self, ctx: ExecutorContext) -> None:  # pragma: no cover - protocol
        ...

    def inject(self, ctx: ExecutorContext) -> None:  # pragma: no cover - protocol
        ...

    def observe(self, ctx: ExecutorContext) -> ObservedRun:  # pragma: no cover - protocol
        ...


# ---------------------------------------------------------------------------
# Internal sentinel for "no observed run yet"
# ---------------------------------------------------------------------------


_NO_OBSERVED_RUN = ObservedRun(
    exit_code=-1,
    stdout="",
    stderr="",
    duration_sec=0.0,
    jsonl_paths=MappingProxyType({}),
    artifacts=MappingProxyType({}),
)


# ---------------------------------------------------------------------------
# Public entrypoint
# ---------------------------------------------------------------------------


def run_eval(
    spec: EvalSpec,
    *,
    home: HomeIsolation,
    config: EvalConfig,
    run_dir: Path,
    artifacts_dir: Path,
    stdout_path: Path,
    stderr_path: Path,
    transcript_path: Path,
    executor: LifecycleExecutor,
    expect_callables: Sequence[ExpectCallable] = (),
    deploy_hooks: Callable[[Path], None] = deploy_hooks_to,
    on_teardown_error: Optional[Callable[[BaseException], None]] = None,
    keep_home_on_pass: bool = False,
) -> EvalOutcome:
    """Execute the FR-LC1 7-step lifecycle and return an ``EvalOutcome``.

    The function is the *skeleton* on top of which COMP-004 EvalRunner
    (T03.05) layers per-eval JSONL logging and per-eval timeout
    enforcement. See ``artifacts/D-0048/spec.md`` for the full lifecycle
    + status-mapping contract.

    Arguments are keyword-only (after ``spec``) so future field
    additions cannot silently re-bind positional callers. The default
    ``deploy_hooks`` resolves to the COMP-014 ``deploy_hooks_to``
    function; tests inject a stub.

    Raises
    ------
    KeyboardInterrupt, SystemExit
        Re-raised verbatim after running ``home.teardown(keep=True)`` so
        NFR-REL1 (T03.07) can convert them into an ``INTERRUPTED``
        outcome at the orchestrator layer. Every other exception is
        captured and folded into an ``EvalOutcome`` with status
        ``ERRORED``.
    """

    # Per-step exception capture lives in ``_LifecycleState`` so the
    # status-mapping helper can read every step's result without
    # threading positional state through the function body.
    state = _LifecycleState(spec=spec)

    try:
        # Step 1 — build isolation. ``HomeIsolation.setup`` is itself
        # idempotency-guarded; the atomic-setup wrapper (T02.13) preserves
        # the partial HOME on failure so ``teardown(keep=True)`` keeps
        # forensic artifacts on disk.
        try:
            home.setup(config=config)
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException as exc:  # noqa: BLE001 — captured for status mapping
            state.record_harness_failure(step="setup", exc=exc)
            return _finalize(
                state=state,
                home=home,
                on_teardown_error=on_teardown_error,
                keep_home_on_pass=keep_home_on_pass,
            )

        home_path = home.home_path

        # Step 2 — deploy hooks. Injectable so tests stub the deploy
        # without a real ``hooks.json`` on disk.
        try:
            deploy_hooks(home_path)
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException as exc:  # noqa: BLE001 — captured for status mapping
            state.record_harness_failure(step="deploy_hooks", exc=exc)
            return _finalize(
                state=state,
                home=home,
                on_teardown_error=on_teardown_error,
                keep_home_on_pass=keep_home_on_pass,
            )

        # Build the executor's pre-observe view. ``env`` is taken from
        # ``HomeIsolation.env()`` so the executor sees the canonical
        # HOME / CLAUDE_SESSION_ID overlay.
        exec_ctx = ExecutorContext(
            eval_spec=spec,
            home=home,
            home_path=home_path,
            run_dir=run_dir,
            artifacts_dir=artifacts_dir,
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            transcript_path=transcript_path,
            env=MappingProxyType(dict(home.env())),
        )

        # Step 3 — spawn.
        try:
            executor.spawn(exec_ctx)
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException as exc:  # noqa: BLE001 — captured for status mapping
            state.record_harness_failure(step="spawn", exc=exc)
            return _finalize(
                state=state,
                home=home,
                on_teardown_error=on_teardown_error,
                keep_home_on_pass=keep_home_on_pass,
            )

        # Step 4 — inject.
        try:
            executor.inject(exec_ctx)
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException as exc:  # noqa: BLE001 — captured for status mapping
            state.record_harness_failure(step="inject", exc=exc)
            return _finalize(
                state=state,
                home=home,
                on_teardown_error=on_teardown_error,
                keep_home_on_pass=keep_home_on_pass,
            )

        # Step 5 — observe.
        try:
            observed = executor.observe(exec_ctx)
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException as exc:  # noqa: BLE001 — captured for status mapping
            state.record_harness_failure(step="observe", exc=exc)
            return _finalize(
                state=state,
                home=home,
                on_teardown_error=on_teardown_error,
                keep_home_on_pass=keep_home_on_pass,
            )
        state.record_observed(observed)

        # Step 6 — assert. Build the per-Expect EvalContext now that we
        # have stdout/stderr/exit_code/duration, then apply each
        # callable in declaration order. A callable that raises folds
        # into ERRORED with a partial ``expects`` tuple (whatever
        # callables ran before the raise).
        ctx = EvalContext.from_runner_state(
            eval_spec=spec,
            home=home,
            run_dir=run_dir,
            artifacts_dir=artifacts_dir,
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            transcript_path=transcript_path,
            jsonl_paths=observed.jsonl_paths,
            env=exec_ctx.env,
            exit_code=observed.exit_code,
            stdout=observed.stdout,
            stderr=observed.stderr,
            duration_sec=observed.duration_sec,
            artifacts=observed.artifacts,
        )

        for callable_ in expect_callables:
            try:
                result = callable_(ctx)
            except (KeyboardInterrupt, SystemExit):
                raise
            except BaseException as exc:  # noqa: BLE001
                state.record_harness_failure(step="assert", exc=exc)
                return _finalize(
                    state=state,
                    home=home,
                    on_teardown_error=on_teardown_error,
                    keep_home_on_pass=keep_home_on_pass,
                )
            state.record_expect(result)

        return _finalize(
            state=state,
            home=home,
            on_teardown_error=on_teardown_error,
            keep_home_on_pass=keep_home_on_pass,
        )

    except (KeyboardInterrupt, SystemExit):
        # NFR-REL1 contract: cooperative cancellation. Teardown the
        # partial HOME with ``keep=True`` so forensics survive, then
        # re-raise so the orchestrator's signal handler can convert this
        # into an ``INTERRUPTED`` outcome at the suite layer.
        _safe_teardown(home, keep=True, on_teardown_error=on_teardown_error)
        raise


# ---------------------------------------------------------------------------
# Internal state + classification helpers
# ---------------------------------------------------------------------------


@dataclass
class _LifecycleState:
    """Mutable per-call state captured by ``run_eval``.

    Kept private to the module — the public surface is ``EvalOutcome``.
    The dataclass groups everything the classification helper needs so
    the body of ``run_eval`` stays close to the seven-step structure
    without smuggling positional results through ``return`` tuples.
    """

    spec: EvalSpec
    observed: ObservedRun = _NO_OBSERVED_RUN
    expects: list[ExpectResult] = field(default_factory=list)
    harness_failure_step: Optional[str] = None
    harness_failure_exc: Optional[BaseException] = None

    def record_observed(self, observed: ObservedRun) -> None:
        self.observed = observed

    def record_expect(self, result: ExpectResult) -> None:
        self.expects.append(result)

    def record_harness_failure(self, *, step: str, exc: BaseException) -> None:
        self.harness_failure_step = step
        self.harness_failure_exc = exc


def _classify_outcome(state: _LifecycleState) -> tuple[EvalStatus, Optional[str]]:
    """Return ``(status, error_class)`` for the captured lifecycle state.

    Encodes the status-mapping rules from ``artifacts/D-0048/spec.md``:

    * Any captured harness exception -> ``ERRORED`` with the exception's
      fully-qualified classname.
    * Otherwise, all ``ExpectResult.passed == True`` -> ``PASS``.
    * Otherwise -> ``FAIL``.

    An empty ``expects`` tuple with no harness failure is ``PASS`` by
    design (the eval ran cleanly and the manifest asked nothing of it).
    """

    if state.harness_failure_exc is not None:
        exc = state.harness_failure_exc
        cls = type(exc)
        return "ERRORED", f"{cls.__module__}.{cls.__qualname__}"

    if all(result.passed for result in state.expects):
        return "PASS", None

    return "FAIL", None


def _finalize(
    *,
    state: _LifecycleState,
    home: HomeIsolation,
    on_teardown_error: Optional[Callable[[BaseException], None]],
    keep_home_on_pass: bool,
) -> EvalOutcome:
    """Run step 7 (teardown) and build the final ``EvalOutcome``.

    The ``keep`` flag follows the table in ``artifacts/D-0048/spec.md``:
    PASS honours ``keep_home_on_pass`` (default ``False``); every other
    status forces ``keep=True`` so failed/errored evals preserve their
    HOME for forensic inspection. Teardown failures are routed through
    ``on_teardown_error`` so they cannot flip a PASS into a FAIL — the
    design-spec invariant is that teardown is best-effort.
    """

    status, error_class = _classify_outcome(state)

    keep = True if status != "PASS" else keep_home_on_pass
    _safe_teardown(home, keep=keep, on_teardown_error=on_teardown_error)

    # ``duration_sec`` is ``0.0`` until observe completed. The observed
    # value (which may be 0.0 for a stub eval) is preserved verbatim
    # because the Reporter renders it without further interpretation.
    duration_sec = state.observed.duration_sec
    if state.harness_failure_step in {"setup", "deploy_hooks", "spawn", "inject", "observe"}:
        # Steps 1-5 failures: observe never ran cleanly, so duration is
        # not meaningful — pin to 0.0 so the Reporter's per-eval row
        # does not display a stale or misleading value.
        duration_sec = 0.0

    return EvalOutcome(
        eval_id=state.spec.id,
        title=state.spec.title,
        status=status,
        duration_sec=duration_sec,
        expects=tuple(state.expects),
        skip_reason=None,
        skip_flag_triggered=None,
        artifacts=dict(state.observed.artifacts),
        error_class=error_class,
    )


def _safe_teardown(
    home: HomeIsolation,
    *,
    keep: bool,
    on_teardown_error: Optional[Callable[[BaseException], None]],
) -> None:
    """Invoke ``home.teardown`` swallowing any failure.

    Teardown failures are best-effort by design (see
    ``artifacts/D-0048/spec.md`` and the ``HomeIsolation.teardown``
    docstring). The optional callback lets COMP-004 (T03.05) record
    teardown failures into its per-eval JSONL log without re-raising
    from the lifecycle.
    """

    try:
        home.teardown(keep=keep)
    except (KeyboardInterrupt, SystemExit):
        raise
    except BaseException as exc:  # noqa: BLE001 — swallowed per spec
        if on_teardown_error is not None:
            try:
                on_teardown_error(exc)
            except BaseException:  # noqa: BLE001 — callback failure is non-fatal
                pass


# ---------------------------------------------------------------------------
# COMP-004 EvalRunner class (T03.05 / D-0049)
# ---------------------------------------------------------------------------


@dataclass
class _LogEvent:
    """Single JSONL line buffered by :class:`EvalRunner`.

    The buffer holds events until ``home_path`` is known; once setup
    completes the buffer is flushed to disk and subsequent events are
    appended directly. Field shape matches the JSONL contract documented
    in ``artifacts/D-0049/spec.md``.
    """

    event: str
    ts_offset_sec: float
    eval_id: str
    step: str
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        # Build an ordered dict so JSON diff output stays stable; the
        # round() pin is documented in D-0049/spec.md ("Rounded to
        # microseconds so JSON diff output stays compact and stable.").
        return {
            "event": self.event,
            "ts_offset_sec": round(self.ts_offset_sec, 6),
            "eval_id": self.eval_id,
            "step": self.step,
            "extra": dict(self.extra),
        }


class _JsonlLog:
    """Thread-safe buffer + writer for the per-eval JSONL log.

    The runner emits events from both the worker thread (every
    lifecycle step except timeout teardown) and the main thread (the
    ``timeout_fired`` + ``outcome`` events). A lock keeps the ordered
    list of buffered events consistent and `write()` deterministic.
    """

    def __init__(self, *, eval_id: str, clock: Callable[[], float]) -> None:
        self._eval_id = eval_id
        self._clock = clock
        self._start = clock()
        self._lock = threading.Lock()
        self._events: list[_LogEvent] = []

    def _ts_offset(self) -> float:
        return self._clock() - self._start

    def emit(self, event: str, *, step: str, extra: Optional[Mapping[str, Any]] = None) -> None:
        evt = _LogEvent(
            event=event,
            ts_offset_sec=self._ts_offset(),
            eval_id=self._eval_id,
            step=step,
            extra=dict(extra or {}),
        )
        with self._lock:
            self._events.append(evt)

    def snapshot(self) -> tuple[_LogEvent, ...]:
        with self._lock:
            return tuple(self._events)

    def write_to(self, path: Path) -> None:
        """Materialise the buffered events as one JSON object per line.

        Failures are best-effort: the JSONL log is a forensic artifact,
        not a load-bearing part of the outcome contract.
        """
        with self._lock:
            events = list(self._events)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8") as fh:
                for evt in events:
                    fh.write(json.dumps(evt.to_dict(), sort_keys=False))
                    fh.write("\n")
        except OSError:  # noqa: BLE001 — best-effort log write
            return


class _LoggingHomeProxy:
    """Duck-typed proxy around ``HomeIsolation`` emitting setup/teardown events.

    ``HomeIsolation`` is a frozen dataclass so we cannot subclass-and-
    override its setup/teardown methods. Wrapping the instance keeps the
    skeleton (``run_eval``) untouched while letting ``EvalRunner`` log
    the four required events at the exact lifecycle boundary.
    """

    def __init__(self, home: Any, log: _JsonlLog) -> None:
        self._home = home
        self._log = log

    def setup(self, *, config: EvalConfig) -> Path:
        self._log.emit(EvalRunner.EVENT_SETUP_STARTED, step="setup")
        try:
            home_path = self._home.setup(config=config)
        except BaseException:
            raise
        self._log.emit(
            EvalRunner.EVENT_SETUP_COMPLETED,
            step="setup",
            extra={"home_path": str(home_path)},
        )
        return home_path

    def teardown(self, keep: bool) -> None:
        self._log.emit(
            EvalRunner.EVENT_TEARDOWN_STARTED,
            step="teardown",
            extra={"keep": keep},
        )
        try:
            self._home.teardown(keep)
        except BaseException as exc:
            cls = type(exc)
            self._log.emit(
                EvalRunner.EVENT_TEARDOWN_ERROR,
                step="teardown",
                extra={
                    "error_class": f"{cls.__module__}.{cls.__qualname__}",
                    "message": str(exc),
                },
            )
            raise
        self._log.emit(EvalRunner.EVENT_TEARDOWN_COMPLETED, step="teardown")

    def env(self) -> Mapping[str, str]:
        return self._home.env()

    @property
    def home_path(self) -> Path:
        return self._home.home_path


class _LoggingExecutor:
    """LifecycleExecutor proxy emitting spawn/inject/observe events."""

    def __init__(self, executor: LifecycleExecutor, log: _JsonlLog) -> None:
        self._executor = executor
        self._log = log

    def spawn(self, ctx: "ExecutorContext") -> None:
        self._log.emit(EvalRunner.EVENT_SPAWN_STARTED, step="spawn")
        self._executor.spawn(ctx)

    def inject(self, ctx: "ExecutorContext") -> None:
        self._log.emit(EvalRunner.EVENT_INJECT_STARTED, step="inject")
        self._executor.inject(ctx)

    def observe(self, ctx: "ExecutorContext") -> ObservedRun:
        self._log.emit(EvalRunner.EVENT_OBSERVE_STARTED, step="observe")
        observed = self._executor.observe(ctx)
        self._log.emit(
            EvalRunner.EVENT_OBSERVE_COMPLETED,
            step="observe",
            extra={
                "exit_code": observed.exit_code,
                "duration_sec": observed.duration_sec,
            },
        )
        return observed


def _wrap_expect_with_log(
    callable_: ExpectCallable, *, index: int, log: _JsonlLog
) -> ExpectCallable:
    """Return a wrapped ExpectCallable that emits assertion events.

    The wrapper preserves the original signature so ``run_eval`` cannot
    tell it is being observed. The original callable's ``__name__`` is
    captured into the ``assertion_started`` / ``assertion_completed``
    event payloads so post-mortem tooling can correlate JSONL rows with
    DSL primitives.
    """

    name = getattr(callable_, "__name__", None)
    if name == "<lambda>":
        name = None

    def _logging_expect(ctx: EvalContext) -> ExpectResult:
        log.emit(
            EvalRunner.EVENT_ASSERTION_STARTED,
            step="assert",
            extra={"index": index, "name": name},
        )
        result = callable_(ctx)
        log.emit(
            EvalRunner.EVENT_ASSERTION_COMPLETED,
            step="assert",
            extra={"index": index, "name": name, "passed": bool(result.passed)},
        )
        return result

    # Preserve attributes so frameworks that introspect __name__ still work.
    _logging_expect.__wrapped__ = callable_  # type: ignore[attr-defined]
    if name is not None:
        _logging_expect.__name__ = name
    return _logging_expect


class EvalRunner:
    """COMP-004 per-eval runner with JSONL logging + timeout enforcement.

    Wraps the FR-LC1 lifecycle skeleton (``run_eval``) in a class that
    owns two cross-cutting concerns the skeleton intentionally deferred:

    1. A per-eval JSONL log under
       ``home_path/.eval-logs/<eval_id>.jsonl`` covering every
       lifecycle transition.
    2. Per-eval timeout enforcement — when
       ``EvalSpec.timeout_sec`` is set, the runner returns an
       ``EvalOutcome`` with status ``TIMEOUT`` if the lifecycle does not
       complete within budget.

    See ``artifacts/D-0049/spec.md`` for the full contract.
    """

    LOG_DIR_RELPATH: ClassVar[Path] = Path(".eval-logs")

    # NFR-REL2 (T03.08 / D-0051): the bounded retry policy. Failed evals
    # are *not* retried automatically; the user re-runs them with
    # ``superclaude eval run --eval <id>`` after diagnosing. The
    # constants below pin the contract so future R3-mit work (T05.23)
    # has a single place to extend: tags carrying ``MCP_FLAKY_TAG`` will
    # be eligible for one in-process retry once OQ-10 closes. Until
    # then, ``retry_count`` is required to be exactly
    # ``DEFAULT_RETRY_COUNT`` and any non-zero value is rejected at
    # construction time. See ``docs/eval/retry.md`` for the user-facing
    # subset re-run guidance.
    DEFAULT_RETRY_COUNT: ClassVar[int] = 0
    MCP_FLAKY_TAG: ClassVar[str] = "MCP-flaky"

    EVENT_SETUP_STARTED: ClassVar[str] = "setup_started"
    EVENT_SETUP_COMPLETED: ClassVar[str] = "setup_completed"
    EVENT_HOOKS_DEPLOYED: ClassVar[str] = "hooks_deployed"
    EVENT_SPAWN_STARTED: ClassVar[str] = "spawn_started"
    EVENT_INJECT_STARTED: ClassVar[str] = "inject_started"
    EVENT_OBSERVE_STARTED: ClassVar[str] = "observe_started"
    EVENT_OBSERVE_COMPLETED: ClassVar[str] = "observe_completed"
    EVENT_ASSERTION_STARTED: ClassVar[str] = "assertion_started"
    EVENT_ASSERTION_COMPLETED: ClassVar[str] = "assertion_completed"
    EVENT_TEARDOWN_STARTED: ClassVar[str] = "teardown_started"
    EVENT_TEARDOWN_COMPLETED: ClassVar[str] = "teardown_completed"
    EVENT_TEARDOWN_ERROR: ClassVar[str] = "teardown_error"
    EVENT_TIMEOUT_FIRED: ClassVar[str] = "timeout_fired"
    EVENT_INTERRUPTED_FIRED: ClassVar[str] = "interrupted_fired"
    EVENT_EXECUTOR_CANCEL_STARTED: ClassVar[str] = "executor_cancel_started"
    EVENT_EXECUTOR_CANCEL_COMPLETED: ClassVar[str] = "executor_cancel_completed"
    EVENT_EXECUTOR_CANCEL_ERROR: ClassVar[str] = "executor_cancel_error"
    EVENT_EXECUTOR_CANCEL_SKIPPED: ClassVar[str] = "executor_cancel_skipped"
    EVENT_OUTCOME: ClassVar[str] = "outcome"

    def __init__(
        self,
        *,
        home: HomeIsolation,
        config: EvalConfig,
        executor: LifecycleExecutor,
        run_dir: Path,
        artifacts_dir: Path,
        stdout_path: Path,
        stderr_path: Path,
        transcript_path: Path,
        expect_callables: Sequence[ExpectCallable] = (),
        deploy_hooks: Callable[[Path], None] = deploy_hooks_to,
        keep_home_on_pass: bool = False,
        default_timeout_sec: Optional[float] = None,
        clock: Callable[[], float] = time.monotonic,
        cancellation_token: Optional[CancellationToken] = None,
        retry_count: int = DEFAULT_RETRY_COUNT,
        retry_policy: Optional[RetryOncePolicy] = None,
        home_factory: Optional[Callable[[], HomeIsolation]] = None,
    ) -> None:
        # NFR-REL2 (T03.08): the harness produces a deterministic
        # single-pass run. ``retry_count`` is accepted as a constructor
        # parameter so callers can document intent, but until R3-mit
        # (T05.23) lands the MCP-flaky retry-once branch the only
        # accepted value is the default. Reject anything else loudly so
        # an accidental sweep does not silently re-execute evals and
        # break the orchestrator's N'-vs-K invariant (FR-RPT1 / T03.11).
        if retry_count != self.DEFAULT_RETRY_COUNT:
            raise ValueError(
                f"EvalRunner retry_count must be {self.DEFAULT_RETRY_COUNT} "
                f"(NFR-REL2 bounded retry policy); got {retry_count!r}. "
                "Re-run failing evals via 'superclaude eval run --eval <id>' "
                "instead — see docs/eval/retry.md."
            )

        self._home = home
        self._config = config
        self._executor = executor
        self._run_dir = run_dir
        self._artifacts_dir = artifacts_dir
        self._stdout_path = stdout_path
        self._stderr_path = stderr_path
        self._transcript_path = transcript_path
        self._expect_callables = tuple(expect_callables)
        self._deploy_hooks = deploy_hooks
        self._keep_home_on_pass = keep_home_on_pass
        self._default_timeout_sec = default_timeout_sec
        self._clock = clock
        self._cancellation_token = cancellation_token
        self._retry_count = retry_count
        # R3-mit (T05.23 / D-0101): retry-once policy. ``retry_policy``
        # is the immutable decision module; ``home_factory`` produces a
        # fresh ``HomeIsolation`` for the retry attempt (the first
        # attempt's HOME has already been torn down by the time the
        # policy is consulted). When ``home_factory`` is ``None`` the
        # runner reuses ``self._home`` — practical for test stubs whose
        # ``setup()`` is callable across teardown; production callers
        # SHOULD wire a factory because ``HomeIsolation.setup`` raises
        # on the second call. Policy is orthogonal to ``retry_count``:
        # both can coexist, the strict NFR-REL2 guard above still
        # rejects ``retry_count != 0``.
        self._retry_policy = retry_policy
        self._home_factory = home_factory

    # ------------------------------------------------------------------
    # Public surface
    # ------------------------------------------------------------------

    def run(self, spec: EvalSpec) -> EvalOutcome:
        """Execute the per-eval lifecycle and return an ``EvalOutcome``.

        Wraps :func:`run_eval` with logging proxies + a per-eval timeout
        budget. The lifecycle itself is unchanged — every step still
        runs through the FR-LC1 skeleton — so the status mapping rules
        from ``D-0048/spec.md`` apply verbatim except for the TIMEOUT
        branch this class adds.

        When a :class:`CancellationToken` is wired (NFR-REL1 / T03.07)
        and the token is already cancelled at entry, the runner skips
        the lifecycle entirely and returns an ``INTERRUPTED`` outcome.
        Cancellations that arrive mid-flight are observed cooperatively
        through the orchestrator (T03.15); the runner itself records
        ``INTERRUPTED`` if the worker raises ``KeyboardInterrupt``
        (matching the FR-LC1 skeleton's re-raise behaviour) only when a
        cancellation_token is wired, otherwise propagation is preserved.

        R3-mit (T05.23 / D-0101): when a :class:`RetryOncePolicy` is
        wired and the spec carries ``MCP_FLAKY_TAG``, a non-PASS first
        attempt is retried exactly once. The final outcome (whether
        the retry recovered to PASS or the failure persisted) carries
        the ``mcp_server_flaky`` artifact in ``outcome.artifacts`` so
        post-mortem tooling can identify retries without re-parsing
        the per-eval JSONL log.
        """

        outcome = self._execute_once(spec)

        # R3-mit retry-once branch. Consulted only when the policy is
        # wired AND the first attempt warrants a retry per the policy's
        # taxonomy (eligible spec + flaky status). The retry attempt
        # uses a fresh ``HomeIsolation`` from ``home_factory`` (when
        # provided) so the second lifecycle sees the same setup
        # contract as the first; without a factory the original home
        # is reused, which only works for test stubs whose ``setup()``
        # is callable across teardown.
        if self._retry_policy is not None and self._retry_policy.should_retry(spec, outcome):
            if self._home_factory is not None:
                self._home = self._home_factory()
            retry_outcome = self._execute_once(spec)
            outcome = self._retry_policy.annotate(retry_outcome)

        return outcome

    def _execute_once(self, spec: EvalSpec) -> EvalOutcome:
        """Execute the lifecycle exactly once and return the outcome.

        Internal helper that owns the FR-LC1 skeleton invocation, the
        per-eval JSONL log lifecycle, the timeout watchdog, and the
        cancellation-token cooperative exit. ``run()`` invokes this
        once for a non-retried eval and twice when the R3-mit policy
        warrants a retry.
        """

        log = _JsonlLog(eval_id=spec.id, clock=self._clock)
        timeout_sec = self._resolve_timeout(spec)

        # NFR-REL1: cooperative cancellation. If the signal handler has
        # already flipped the token before we even start the worker,
        # return INTERRUPTED immediately so the orchestrator does not
        # waste a HomeIsolation setup on an eval whose result will be
        # discarded anyway.
        if self._cancellation_token is not None and self._cancellation_token.is_cancelled():
            return self._make_interrupted_outcome(spec=spec, log=log)

        # Holders for the worker thread. ``outcome_holder`` is populated
        # on clean return; ``exc_holder`` is populated when run_eval
        # raised (KeyboardInterrupt / SystemExit, mainly — every other
        # exception is folded into an ERRORED outcome by run_eval
        # itself).
        outcome_holder: dict[str, EvalOutcome] = {}
        exc_holder: dict[str, BaseException] = {}

        logged_home = _LoggingHomeProxy(self._home, log)
        logged_executor = _LoggingExecutor(self._executor, log)
        wrapped_expects = tuple(
            _wrap_expect_with_log(c, index=i, log=log)
            for i, c in enumerate(self._expect_callables)
        )

        # The wrapped ``deploy_hooks`` emits ``hooks_deployed`` once the
        # underlying call returns; the spec does not require this event
        # but it is the natural place to record that step 2 completed.
        original_deploy = self._deploy_hooks

        def logged_deploy(home_path: Path) -> None:
            original_deploy(home_path)
            log.emit(EvalRunner.EVENT_HOOKS_DEPLOYED, step="deploy_hooks")

        # ``on_teardown_error`` is invoked by ``_safe_teardown`` when
        # teardown raises. The proxy already logs the failure via
        # ``EVENT_TEARDOWN_ERROR``; the callback is a no-op so the
        # caller-injected behaviour (preserved by FR-LC1) keeps working
        # if a future caller wires one through ``EvalRunner``.
        def on_teardown_error(_exc: BaseException) -> None:
            return None

        def worker() -> None:
            try:
                outcome_holder["result"] = run_eval(
                    spec,
                    home=logged_home,  # type: ignore[arg-type]  # duck-typed proxy
                    config=self._config,
                    run_dir=self._run_dir,
                    artifacts_dir=self._artifacts_dir,
                    stdout_path=self._stdout_path,
                    stderr_path=self._stderr_path,
                    transcript_path=self._transcript_path,
                    executor=logged_executor,  # type: ignore[arg-type]  # duck-typed proxy
                    expect_callables=wrapped_expects,
                    deploy_hooks=logged_deploy,
                    on_teardown_error=on_teardown_error,
                    keep_home_on_pass=self._keep_home_on_pass,
                )
            except BaseException as exc:  # noqa: BLE001 — captured for re-raise
                exc_holder["exc"] = exc

        # ``daemon=True`` so a hung worker cannot block process exit.
        # NFR-REL1 (T03.07) wires the PtyDriver kill + zombie reap that
        # makes a hung worker rare in production.
        thread = threading.Thread(
            target=worker,
            name=f"EvalRunner[{spec.id}]",
            daemon=True,
        )
        thread.start()
        thread.join(timeout=timeout_sec)

        if thread.is_alive():
            return self._handle_timeout(spec=spec, log=log, timeout_sec=timeout_sec)

        # Worker returned. Either run_eval produced an outcome or raised
        # an interrupt; the latter must propagate to the orchestrator so
        # NFR-REL1 can mark INTERRUPTED. Flush the JSONL log first so
        # the partial events survive the re-raise.
        if "exc" in exc_holder:
            exc = exc_holder["exc"]
            # NFR-REL1 (T03.07): when a cancellation token is wired, the
            # runner converts a worker-thread KeyboardInterrupt /
            # SystemExit directly into an ``INTERRUPTED`` outcome so the
            # orchestrator's ThreadPoolExecutor + as_completed loop never
            # has to translate an exception into a status. Without a
            # token, propagation is preserved verbatim so the FR-LC1
            # contract (and the existing ``test_runner_class.py`` AC4
            # case) stays unchanged.
            if (
                self._cancellation_token is not None
                and isinstance(exc, (KeyboardInterrupt, SystemExit))
            ):
                self._cancellation_token.cancel()
                return self._make_interrupted_outcome(spec=spec, log=log)
            self._flush_log(log)
            raise exc

        outcome = outcome_holder["result"]
        # Record the terminal classification so post-mortem tooling can
        # tell whether the run ended cleanly or was reclassified.
        log.emit(
            EvalRunner.EVENT_OUTCOME,
            step="outcome",
            extra={
                "status": outcome.status,
                "duration_sec": outcome.duration_sec,
                "error_class": outcome.error_class,
            },
        )
        self._flush_log(log)
        return outcome

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _resolve_timeout(self, spec: EvalSpec) -> Optional[float]:
        """Return the resolved per-eval timeout, or ``None`` for unbounded.

        ``spec.timeout_sec`` takes precedence; if absent or 0 the
        runner falls back to ``default_timeout_sec``. ``0`` is treated
        as "use the default" rather than "no timeout" because a literal
        zero would always fire and is never useful in practice.
        """
        spec_timeout = spec.timeout_sec
        if spec_timeout is not None and spec_timeout > 0:
            return float(spec_timeout)
        if self._default_timeout_sec is not None and self._default_timeout_sec > 0:
            return float(self._default_timeout_sec)
        return None

    def _handle_timeout(
        self,
        *,
        spec: EvalSpec,
        log: _JsonlLog,
        timeout_sec: Optional[float],
    ) -> EvalOutcome:
        """Emit timeout events, attempt best-effort teardown, return outcome.

        NFR-REL1 (T03.07) extends the T03.05 timeout path with a
        subprocess kill + zombie reap step: if the wired executor
        exposes a ``cancel()`` method (the production
        ``ClaudeProcessAdapter`` + ``PtyDriver`` does), the runner calls
        it from the main thread so the PtyDriver child terminates and
        ``wait()`` reaps the zombie before the orchestrator collects
        the next outcome. Failure is swallowed because the TIMEOUT
        outcome must always return cleanly; the JSONL log records the
        cancel attempt.
        """
        budget = float(timeout_sec) if timeout_sec is not None else 0.0
        log.emit(
            EvalRunner.EVENT_TIMEOUT_FIRED,
            step="timeout",
            extra={"timeout_sec": budget},
        )

        # NFR-REL1: kill the executor's subprocess + reap zombie before
        # we attempt teardown. Documented on D-0050/spec.md.
        self._cancel_executor(log=log, reason="timeout")

        log.emit(
            EvalRunner.EVENT_TEARDOWN_STARTED,
            step="teardown",
            extra={"keep": True},
        )
        try:
            # The worker may still hold references to the HomeIsolation
            # instance; HomeIsolation.teardown is idempotent enough that
            # a main-thread call is safe even if the worker is mid-step.
            # Failures are swallowed so the TIMEOUT outcome always
            # returns cleanly.
            if getattr(self._home, "is_set_up", False):
                self._home.teardown(keep=True)
        except BaseException as exc:  # noqa: BLE001 — best-effort
            cls = type(exc)
            log.emit(
                EvalRunner.EVENT_TEARDOWN_ERROR,
                step="teardown",
                extra={
                    "error_class": f"{cls.__module__}.{cls.__qualname__}",
                    "message": str(exc),
                },
            )

        outcome = EvalOutcome(
            eval_id=spec.id,
            title=spec.title,
            status="TIMEOUT",
            duration_sec=budget,
            expects=(),
            skip_reason=None,
            skip_flag_triggered=None,
            artifacts={},
            error_class="builtins.TimeoutError",
        )
        log.emit(
            EvalRunner.EVENT_OUTCOME,
            step="outcome",
            extra={
                "status": outcome.status,
                "duration_sec": outcome.duration_sec,
                "error_class": outcome.error_class,
            },
        )
        self._flush_log(log)
        return outcome

    def _cancel_executor(self, *, log: _JsonlLog, reason: str) -> None:
        """Best-effort PtyDriver kill + zombie reap on the wired executor.

        The production executor (``ClaudeProcessAdapter`` driving a
        ``PtyDriver``) exposes a ``cancel()`` method that calls
        ``PtyDriver.terminate(force=True)`` followed by ``close()`` so
        the child process is signalled and ``wait()`` reaps the
        resulting zombie. Test stubs that do not need cancellation
        simply omit the method — ``getattr`` returns ``None`` and the
        runner skips the step.

        Failures are swallowed so a flaky cancel cannot block a
        TIMEOUT / INTERRUPTED outcome from returning. The JSONL log
        records ``executor_cancel_*`` events under the ``timeout``
        step so post-mortem tooling can confirm the kill attempt
        landed.
        """
        cancel = getattr(self._executor, "cancel", None)
        if cancel is None or not callable(cancel):
            log.emit(
                EvalRunner.EVENT_EXECUTOR_CANCEL_SKIPPED,
                step=reason,
                extra={"reason": "executor has no cancel() method"},
            )
            return
        log.emit(
            EvalRunner.EVENT_EXECUTOR_CANCEL_STARTED,
            step=reason,
            extra={},
        )
        try:
            cancel()
        except BaseException as exc:  # noqa: BLE001 — best-effort kill
            cls = type(exc)
            log.emit(
                EvalRunner.EVENT_EXECUTOR_CANCEL_ERROR,
                step=reason,
                extra={
                    "error_class": f"{cls.__module__}.{cls.__qualname__}",
                    "message": str(exc),
                },
            )
            return
        log.emit(
            EvalRunner.EVENT_EXECUTOR_CANCEL_COMPLETED,
            step=reason,
            extra={},
        )

    def _make_interrupted_outcome(
        self, *, spec: EvalSpec, log: _JsonlLog
    ) -> EvalOutcome:
        """Build an ``INTERRUPTED`` outcome and flush the JSONL log.

        Used when:

        * The cancellation token was already set before
          ``EvalRunner.run`` started (skip the lifecycle entirely).
        * The worker raised ``KeyboardInterrupt`` / ``SystemExit`` and
          a cancellation token is wired (NFR-REL1 cooperative path).

        ``duration_sec`` is pinned to ``0.0`` because no observable
        portion of the lifecycle ran; the Reporter renders the column
        verbatim so a stale value would confuse downstream readers.
        """
        log.emit(
            EvalRunner.EVENT_INTERRUPTED_FIRED,
            step="interrupt",
            extra={},
        )
        # Best-effort cancel: if the executor was mid-flight when the
        # interrupt arrived, kill its subprocess + reap zombie.
        self._cancel_executor(log=log, reason="interrupt")
        # Best-effort teardown so a partial HOME (forensic artefact) is
        # preserved when isolation already ran.
        if getattr(self._home, "is_set_up", False):
            log.emit(
                EvalRunner.EVENT_TEARDOWN_STARTED,
                step="teardown",
                extra={"keep": True},
            )
            try:
                self._home.teardown(keep=True)
            except BaseException as exc:  # noqa: BLE001 — best-effort
                cls = type(exc)
                log.emit(
                    EvalRunner.EVENT_TEARDOWN_ERROR,
                    step="teardown",
                    extra={
                        "error_class": f"{cls.__module__}.{cls.__qualname__}",
                        "message": str(exc),
                    },
                )

        outcome = EvalOutcome(
            eval_id=spec.id,
            title=spec.title,
            status="INTERRUPTED",
            duration_sec=0.0,
            expects=(),
            skip_reason=None,
            skip_flag_triggered=None,
            artifacts={},
            error_class=None,
        )
        log.emit(
            EvalRunner.EVENT_OUTCOME,
            step="outcome",
            extra={
                "status": outcome.status,
                "duration_sec": outcome.duration_sec,
                "error_class": outcome.error_class,
            },
        )
        self._flush_log(log)
        return outcome

    def _flush_log(self, log: _JsonlLog) -> None:
        """Write the buffered JSONL log under ``home_path/.eval-logs/``.

        Best-effort: if ``home_path`` is not yet resolvable (setup
        failed before ``home_path`` was assigned) the events are
        discarded. The JSONL log is a forensic artifact, never
        load-bearing for outcome classification.
        """
        home_path = self._resolve_home_path()
        if home_path is None:
            return
        # ``eval_id`` is regex-guarded by FR-SCH2 upstream so it is safe
        # to use verbatim in a filename. We still take the first event
        # for the id to avoid trusting any later mutation.
        snapshot = log.snapshot()
        if not snapshot:
            return
        eval_id = snapshot[0].eval_id
        log_path = home_path / self.LOG_DIR_RELPATH / f"{eval_id}.jsonl"
        log.write_to(log_path)

    def _resolve_home_path(self) -> Optional[Path]:
        """Return the per-eval HOME path if available, ``None`` otherwise.

        ``HomeIsolation.home_path`` raises when setup has not run; we
        catch that and return ``None`` so a setup-time failure never
        promotes itself into a runner exception.
        """
        try:
            return Path(self._home.home_path)
        except Exception:  # noqa: BLE001 — home_path may raise pre-setup
            return None
