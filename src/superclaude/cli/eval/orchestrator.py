"""COMP-003 RunOrchestrator — parallel eval scheduler.

Task T03.15 / Deliverable D-0057 / Roadmap row R-057 (COMP-003).

The orchestrator is the single component that turns a sequence of
expanded :class:`EvalSpec` rows into a sequence of :class:`EvalOutcome`
rows by scheduling per-spec :class:`EvalRunner` workers through
``concurrent.futures.ThreadPoolExecutor + as_completed`` — the AC6
pattern the design-spec pins for cliEval. The implementation deliberately
mirrors the shape used by ``src/superclaude/cli/prd/executor.py:774-802``
so a reader switching between the PRD pipeline and the eval harness sees
the same scheduling skeleton.

Responsibilities
================

The orchestrator owns three cross-cutting concerns the lifecycle layer
intentionally defers:

1. **Concurrency budget.** ``max_workers`` is clamped to ``[1, 15]`` per
   design-spec §11 (NFR-PERF2) with a default of ``8``. Values outside
   the range either raise (``parallel < 1``) or saturate to the upper
   bound (``parallel > 15``). The clamp is enforced once at the top of
   :meth:`RunOrchestrator.run` so the rest of the body can trust the
   effective value.
2. **Outcome contract.** :class:`RunOrchestrator` guarantees one
   :class:`EvalOutcome` per input :class:`EvalSpec` in the original
   sequence order. The Reporter (COMP-008 / T03.13) enforces the
   N'-vs-K invariant on top of this — the orchestrator never elides a
   spec.
3. **Cooperative cancellation.** When a shared
   :class:`CancellationToken` is wired (NFR-REL1 / T03.07), the
   orchestrator stops submitting new work as soon as it observes the
   token cancelled. Specs that were never submitted synthesise an
   ``INTERRUPTED`` outcome at the orchestrator layer so the per-spec
   contract still holds.  In-flight runners observe the same token via
   :class:`EvalRunner` and convert worker-thread
   ``KeyboardInterrupt`` / ``SystemExit`` into ``INTERRUPTED`` outcomes
   themselves — the orchestrator never has to translate an exception
   into a status.

The orchestrator deliberately does *not* install signal handlers. Signal
installation is the CLI dispatcher's job (Phase 4): the dispatcher
allocates a :class:`CancellationToken`, wraps the orchestrator call in a
:class:`SignalHandlerInstaller`, and hands the token down so the eval
runners observe the same cancellation flag the signal handler flips.

Worker contract
===============

The orchestrator does not construct :class:`EvalRunner` instances
itself. Building an :class:`EvalRunner` requires per-eval HOME
isolation, scratch paths, executor wiring, and an expect-callable
sequence — none of which the orchestrator can resolve. Instead the
caller supplies a ``run_one: Callable[[EvalSpec], EvalOutcome]`` worker
that wraps everything from ``HomeIsolation`` allocation through
:meth:`EvalRunner.run` into a single closure. Production callers will
typically write::

    def run_one(spec: EvalSpec) -> EvalOutcome:
        home = HomeIsolation(eval_id=spec.id, ...)
        runner = EvalRunner(home=home, ...)
        return runner.run(spec)

This indirection keeps the orchestrator a pure scheduling primitive and
makes unit-testing trivial — tests substitute a stub worker that returns
a canned outcome without touching the filesystem.

If the worker raises (e.g. construction failure, unexpected propagation
of ``KeyboardInterrupt`` because the caller declined to wire a token),
the orchestrator folds the exception into an ``ERRORED`` outcome
recording the fully-qualified exception classname — the same shape
:func:`run_eval` (T03.04) emits when a harness step fails. This keeps
the per-spec contract intact even when a worker misbehaves.
"""

from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from typing import Callable, ClassVar, Optional, Sequence

from .disk_budget import DISK_BUDGET_EXCEEDED_REASON, DiskBudgetPoller
from .models import EvalOutcome, EvalSpec
from .signal_handler import CancellationToken

__all__ = ["RunOrchestrator", "EvalWorker", "allocate_session_id"]


# A worker callable receives an :class:`EvalSpec` and returns the
# corresponding :class:`EvalOutcome`. Production wiring composes
# ``EvalRunner.run`` with the per-spec resource allocation the
# orchestrator deliberately does not own.
EvalWorker = Callable[[EvalSpec], EvalOutcome]


def allocate_session_id(*, run_id: str, eval_id: str) -> str:
    """Return a deterministic, run-scoped session_id for one (run_id, eval_id) pair.

    Per M5 — session_id identifier policy lives here (the orchestrator) rather
    than ad-hoc at each call site. Combining the run-id (unique per ``eval run``
    invocation via ``_new_run_id``) with the eval_id guarantees:

    * Within a run, each eval gets a distinct session_id (orthogonal to eval_id).
    * Across runs, the same eval_id never collides on session_id even if a
      run-dir is reused (future-proofing against replay scenarios).
    * Deterministic for a given (run_id, eval_id) pair, so reporters and
      forensic tooling can re-derive the session_id from artifacts.
    """

    return f"sess-{run_id}-{eval_id}"


class RunOrchestrator:
    """Schedule per-spec eval workers in parallel via ``ThreadPoolExecutor``.

    Parameters
    ----------
    run_one:
        Worker callable invoked once per :class:`EvalSpec`. Returns the
        :class:`EvalOutcome` for that spec. Worker exceptions are folded
        into an ``ERRORED`` outcome — the orchestrator never re-raises
        out of :meth:`run`.
    cancellation_token:
        Optional :class:`CancellationToken` shared with the CLI
        dispatcher's signal handler (NFR-REL1 / T03.07). When the token
        is set, the orchestrator stops submitting new work and
        synthesises an ``INTERRUPTED`` outcome for every spec that was
        never scheduled.
    disk_budget_poller:
        Optional :class:`DiskBudgetPoller` enforcing the NFR-PERF4
        ``--max-disk-mb`` budget (T03.19 / D-0060 / R-060). When wired,
        the orchestrator starts the poller before submission, checks
        :meth:`DiskBudgetPoller.is_breached` alongside the cancellation
        token between submissions, and synthesises a ``SKIPPED`` outcome
        with ``skip_reason="disk_budget_exceeded"`` for every spec that
        was never scheduled after a breach. In-flight workers run to
        completion — the poller never interrupts a thread. A disabled
        poller (``max_disk_mb=0``) is silently no-op'd by
        :meth:`DiskBudgetPoller.start`, so the orchestrator can be wired
        with a poller unconditionally.
    """

    DEFAULT_PARALLEL: ClassVar[int] = 8
    MIN_PARALLEL: ClassVar[int] = 1
    MAX_PARALLEL: ClassVar[int] = 15

    def __init__(
        self,
        *,
        run_one: EvalWorker,
        cancellation_token: Optional[CancellationToken] = None,
        disk_budget_poller: Optional[DiskBudgetPoller] = None,
    ) -> None:
        if not callable(run_one):
            raise TypeError("run_one must be callable")
        self._run_one = run_one
        self._cancellation_token = cancellation_token
        self._disk_budget_poller = disk_budget_poller

    # ------------------------------------------------------------------
    # Public surface
    # ------------------------------------------------------------------

    def run(
        self,
        specs: Sequence[EvalSpec],
        *,
        parallel: int = DEFAULT_PARALLEL,
    ) -> list[EvalOutcome]:
        """Execute every spec in parallel and return one outcome per spec.

        Parameters
        ----------
        specs:
            Expanded :class:`EvalSpec` sequence (post FR-EXP1 expansion).
            The returned list preserves this order so the Reporter
            renders rows deterministically.
        parallel:
            Requested concurrency level. Clamped to
            ``[MIN_PARALLEL, MAX_PARALLEL]``; values below the minimum
            raise :class:`ValueError`, values above the maximum saturate
            to ``MAX_PARALLEL``. Defaults to :attr:`DEFAULT_PARALLEL`.

        Returns
        -------
        list[EvalOutcome]
            One :class:`EvalOutcome` per input spec, in the input order.
        """

        # The minimum-bound rejection is the only hard failure: a
        # negative or zero concurrency value is almost certainly a
        # caller bug (CLI argument parsing should have caught it
        # earlier) and silently coercing it would mask the bug. An
        # upper-bound value, by contrast, is the documented behaviour
        # of design-spec §11 — "parallel=20 clamps to 15" — and the
        # orchestrator must honour it without raising.
        if not isinstance(parallel, int) or isinstance(parallel, bool):
            raise TypeError(
                f"parallel must be int; got {type(parallel).__name__}"
            )
        if parallel < self.MIN_PARALLEL:
            raise ValueError(
                f"parallel must be >= {self.MIN_PARALLEL}; got {parallel}"
            )
        max_workers = min(parallel, self.MAX_PARALLEL)

        if not specs:
            return []

        # Pre-allocate the result slots so we can fill them by index as
        # futures complete. ``as_completed`` yields in completion order,
        # not submission order, so we cannot append blindly.
        outcomes: list[Optional[EvalOutcome]] = [None] * len(specs)

        # Indices for specs that were never submitted because the token
        # was already cancelled when the scheduler reached them. They
        # receive a synthesised ``INTERRUPTED`` outcome below.
        cancelled_indices: list[int] = []
        # Indices for specs that were never submitted because the
        # disk-budget poller flipped its breach flag. They receive a
        # synthesised ``SKIPPED`` outcome with ``skip_reason ==
        # "disk_budget_exceeded"`` so the Reporter can distinguish a
        # disk-budget abort from a SIGINT.
        disk_budget_skipped_indices: list[int] = []

        # The poller is started before the submission loop so it has at
        # least one tick of head-start. It is shut down in a ``finally``
        # so an unhandled exception in the pool body still releases the
        # background thread.
        poller = self._disk_budget_poller
        if poller is not None:
            poller.start()
        try:
            with ThreadPoolExecutor(
                max_workers=max_workers, thread_name_prefix="cliEval"
            ) as pool:
                futures: dict[Future[EvalOutcome], int] = {}

                for index, spec in enumerate(specs):
                    # Cooperative cancellation: once the token flips, stop
                    # submitting new work. Already-running workers observe
                    # the token themselves (via :class:`EvalRunner`) and
                    # convert to INTERRUPTED outcomes; we synthesise an
                    # INTERRUPTED row for every spec that did not even
                    # reach the pool so the per-spec contract still holds.
                    #
                    # Cancellation is checked *before* the disk-budget
                    # breach so a SIGINT received concurrently with a
                    # breach routes the spec to INTERRUPTED (operator
                    # intent dominates a resource limit).
                    if self._is_cancelled():
                        cancelled_indices.append(index)
                        continue
                    if self._is_disk_budget_exceeded():
                        disk_budget_skipped_indices.append(index)
                        continue
                    future = pool.submit(self._invoke_worker, spec)
                    futures[future] = index

                # Drain the pool. ``as_completed`` is the AC6 idiom — it
                # yields each future the instant its worker returns,
                # letting downstream readers (telemetry, TUI) update in
                # near real-time without waiting for the slowest eval.
                # In-flight workers continue to completion even after a
                # disk-budget breach — the AC6 contract requires "in-
                # flight evals complete" before the run exits.
                for future in as_completed(futures):
                    index = futures[future]
                    spec = specs[index]
                    try:
                        outcomes[index] = future.result()
                    except BaseException as exc:  # noqa: BLE001 — see docstring
                        # The worker should fold its own harness errors
                        # into an ERRORED outcome via :func:`run_eval`. We
                        # only get here when the worker itself raised
                        # (construction failure, unwired-token
                        # KeyboardInterrupt propagation, etc.). Translate
                        # to ERRORED so :meth:`run` never re-raises.
                        outcomes[index] = self._errored_outcome(spec, exc)
        finally:
            if poller is not None:
                poller.stop()

        # Backfill INTERRUPTED outcomes for never-submitted specs after
        # the pool has shut down so we cannot race with an in-flight
        # cancellation.
        for index in cancelled_indices:
            outcomes[index] = self._interrupted_outcome(specs[index])
        # Backfill SKIPPED outcomes for specs we declined to submit
        # because the disk budget was breached. Same post-shutdown
        # placement as the INTERRUPTED backfill — once we are here the
        # pool has drained, so the synthesised outcomes cannot race
        # with an in-flight result.
        for index in disk_budget_skipped_indices:
            outcomes[index] = self._disk_budget_skipped_outcome(specs[index])

        # Every slot must be populated by now. The cast filters the
        # ``Optional[...]`` typing without runtime cost; the assertion
        # guards against a future regression.
        assert all(o is not None for o in outcomes), (
            "RunOrchestrator: one or more outcome slots were left empty"
        )
        return [o for o in outcomes if o is not None]

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _invoke_worker(self, spec: EvalSpec) -> EvalOutcome:
        """Indirection so subclasses / tests can hook the call site."""
        return self._run_one(spec)

    def _is_cancelled(self) -> bool:
        token = self._cancellation_token
        return token is not None and token.is_cancelled()

    def _is_disk_budget_exceeded(self) -> bool:
        """``True`` when the wired poller has flagged a budget breach.

        Returns ``False`` when no poller was wired or the poller is
        still healthy. Mirrors :meth:`_is_cancelled` so the submission
        loop reads naturally.
        """
        poller = self._disk_budget_poller
        return poller is not None and poller.is_breached()

    @staticmethod
    def _disk_budget_skipped_outcome(spec: EvalSpec) -> EvalOutcome:
        """Build a SKIPPED outcome for a spec that lost out to the disk budget.

        ``skip_reason`` carries the stable
        :data:`disk_budget.DISK_BUDGET_EXCEEDED_REASON` token so the
        Reporter can match on the constant without parsing free-form
        text. ``skip_flag_triggered`` records the CLI flag operators
        toggle to relax the budget, mirroring the convention used by
        capability-gate skips elsewhere in the harness.
        """
        return EvalOutcome(
            eval_id=spec.id,
            title=spec.title,
            status="SKIPPED",
            duration_sec=0.0,
            expects=(),
            skip_reason=DISK_BUDGET_EXCEEDED_REASON,
            skip_flag_triggered="--max-disk-mb",
            artifacts={},
            error_class=None,
        )

    @staticmethod
    def _interrupted_outcome(spec: EvalSpec) -> EvalOutcome:
        """Build the synthesised ``INTERRUPTED`` outcome for a skipped spec.

        Mirrors :meth:`EvalRunner._make_interrupted_outcome` so the
        reporter cannot distinguish an in-flight cancellation from an
        orchestrator-level one — both shapes are byte-identical.
        """
        return EvalOutcome(
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

    @staticmethod
    def _errored_outcome(spec: EvalSpec, exc: BaseException) -> EvalOutcome:
        """Fold a worker exception into a DM-001 ``ERRORED`` outcome.

        ``error_class`` is the fully-qualified exception classname so
        the Reporter can group identical harness failures across runs
        without parsing free-form messages. Matches the format
        :func:`run_eval` uses for in-runner harness failures.
        """
        cls = type(exc)
        return EvalOutcome(
            eval_id=spec.id,
            title=spec.title,
            status="ERRORED",
            duration_sec=0.0,
            expects=(),
            skip_reason=None,
            skip_flag_triggered=None,
            artifacts={},
            error_class=f"{cls.__module__}.{cls.__qualname__}",
        )
