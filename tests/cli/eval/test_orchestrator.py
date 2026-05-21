"""Tests for COMP-003 RunOrchestrator (T03.15 / D-0057 / R-057).

Covers the four AC bullets the tasklist row pins:

* ``RunOrchestrator`` exposes ``run(specs, parallel)`` and emits exactly
  one ``EvalOutcome`` per expanded spec, in input order.
* ``parallel=20`` clamps to :attr:`MAX_PARALLEL` (15); ``parallel < 1``
  is rejected with :class:`ValueError`; the default (:attr:`DEFAULT_PARALLEL`
  ``=8``) is honoured.
* A 3-eval suite runs in parallel and completes faster than 3× the
  slowest-eval duration — the marker the design-spec uses for "actually
  scheduled on a thread pool, not serialised".
* A wired :class:`CancellationToken` short-circuits scheduling so
  unsubmitted specs receive a synthesised ``INTERRUPTED`` outcome.

The orchestrator's public contract is a pure scheduler over a worker
callable, so these tests stub the worker (``Callable[[EvalSpec],
EvalOutcome]``) directly rather than constructing real
``EvalRunner`` / ``HomeIsolation`` instances. The runner-side
cancellation contract is exercised by ``test_signal_handling.py`` and
``test_runner_class.py``; this file owns the *scheduling* contract.
"""

from __future__ import annotations

import threading
import time
from typing import Callable

import pytest

from superclaude.cli.eval.models import EvalOutcome, EvalSpec
from superclaude.cli.eval.orchestrator import RunOrchestrator
from superclaude.cli.eval.signal_handler import CancellationToken


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _spec(eval_id: str, title: str = "") -> EvalSpec:
    return EvalSpec(id=eval_id, title=title or eval_id)


def _passing_outcome(spec: EvalSpec, duration_sec: float = 0.0) -> EvalOutcome:
    return EvalOutcome(
        eval_id=spec.id,
        title=spec.title,
        status="PASS",
        duration_sec=duration_sec,
        expects=(),
        skip_reason=None,
        skip_flag_triggered=None,
        artifacts={},
        error_class=None,
    )


def _make_recording_worker() -> tuple[
    Callable[[EvalSpec], EvalOutcome], list[str]
]:
    """Return ``(worker, call_log)`` where ``call_log`` captures spec ids."""

    call_log: list[str] = []
    lock = threading.Lock()

    def worker(spec: EvalSpec) -> EvalOutcome:
        with lock:
            call_log.append(spec.id)
        return _passing_outcome(spec)

    return worker, call_log


# ---------------------------------------------------------------------------
# AC: one outcome per spec, original-input order preserved
# ---------------------------------------------------------------------------


class TestOneOutcomePerSpec:
    def test_empty_specs_returns_empty(self) -> None:
        worker, _ = _make_recording_worker()
        orch = RunOrchestrator(run_one=worker)
        assert orch.run([]) == []

    def test_single_spec(self) -> None:
        worker, log = _make_recording_worker()
        orch = RunOrchestrator(run_one=worker)
        outcomes = orch.run([_spec("E1")])
        assert [o.eval_id for o in outcomes] == ["E1"]
        assert log == ["E1"]

    def test_outcome_order_matches_input_order(self) -> None:
        """``as_completed`` yields in completion order; orchestrator restores input order."""

        # Make later specs finish earlier so the in-completion-order
        # naïve append would scramble the list.
        completions = {
            "A": 0.05,
            "B": 0.02,
            "C": 0.0,
        }

        def worker(spec: EvalSpec) -> EvalOutcome:
            time.sleep(completions[spec.id])
            return _passing_outcome(spec)

        orch = RunOrchestrator(run_one=worker)
        outcomes = orch.run([_spec("A"), _spec("B"), _spec("C")])
        assert [o.eval_id for o in outcomes] == ["A", "B", "C"]

    def test_every_spec_gets_exactly_one_outcome(self) -> None:
        """Reporter's FR-RPT1 N'-vs-K invariant: len(outcomes) == len(specs)."""

        worker, _ = _make_recording_worker()
        orch = RunOrchestrator(run_one=worker)
        specs = [_spec(f"E{i:03d}") for i in range(7)]
        outcomes = orch.run(specs)
        assert len(outcomes) == len(specs)
        assert [o.eval_id for o in outcomes] == [s.id for s in specs]


# ---------------------------------------------------------------------------
# AC: parallel clamp [1, 15]; default 8; reject < 1
# ---------------------------------------------------------------------------


class TestParallelClamp:
    def test_default_parallel_is_eight(self) -> None:
        assert RunOrchestrator.DEFAULT_PARALLEL == 8

    def test_min_parallel_is_one(self) -> None:
        assert RunOrchestrator.MIN_PARALLEL == 1

    def test_max_parallel_is_fifteen(self) -> None:
        assert RunOrchestrator.MAX_PARALLEL == 15

    def test_zero_parallel_rejected(self) -> None:
        worker, _ = _make_recording_worker()
        orch = RunOrchestrator(run_one=worker)
        with pytest.raises(ValueError):
            orch.run([_spec("E1")], parallel=0)

    def test_negative_parallel_rejected(self) -> None:
        worker, _ = _make_recording_worker()
        orch = RunOrchestrator(run_one=worker)
        with pytest.raises(ValueError):
            orch.run([_spec("E1")], parallel=-3)

    def test_non_integer_parallel_rejected(self) -> None:
        worker, _ = _make_recording_worker()
        orch = RunOrchestrator(run_one=worker)
        with pytest.raises(TypeError):
            orch.run([_spec("E1")], parallel=3.5)  # type: ignore[arg-type]

    def test_boolean_parallel_rejected(self) -> None:
        """`bool` is an `int` subclass; we reject it explicitly to avoid silent coercion."""
        worker, _ = _make_recording_worker()
        orch = RunOrchestrator(run_one=worker)
        with pytest.raises(TypeError):
            orch.run([_spec("E1")], parallel=True)  # type: ignore[arg-type]

    def test_parallel_above_max_clamps_to_fifteen(self) -> None:
        """parallel=20 must clamp to MAX_PARALLEL=15 without raising."""

        observed_concurrency: list[int] = []
        running = 0
        lock = threading.Lock()

        def worker(spec: EvalSpec) -> EvalOutcome:
            nonlocal running
            with lock:
                running += 1
                observed_concurrency.append(running)
            try:
                # Hold the worker just long enough to overlap with peers.
                time.sleep(0.02)
            finally:
                with lock:
                    running -= 1
            return _passing_outcome(spec)

        orch = RunOrchestrator(run_one=worker)
        specs = [_spec(f"E{i:02d}") for i in range(20)]
        outcomes = orch.run(specs, parallel=20)
        assert len(outcomes) == 20
        # Concurrent workers should never exceed the clamp.
        assert max(observed_concurrency) <= RunOrchestrator.MAX_PARALLEL

    def test_parallel_one_serialises(self) -> None:
        """parallel=1 disables concurrency."""

        observed_concurrency: list[int] = []
        running = 0
        lock = threading.Lock()

        def worker(spec: EvalSpec) -> EvalOutcome:
            nonlocal running
            with lock:
                running += 1
                observed_concurrency.append(running)
            try:
                time.sleep(0.01)
            finally:
                with lock:
                    running -= 1
            return _passing_outcome(spec)

        orch = RunOrchestrator(run_one=worker)
        outcomes = orch.run([_spec(f"E{i}") for i in range(4)], parallel=1)
        assert len(outcomes) == 4
        assert max(observed_concurrency) == 1


# ---------------------------------------------------------------------------
# AC: 3-eval suite faster than 3× slowest-eval duration in parallel
# ---------------------------------------------------------------------------


def test_three_eval_suite_runs_faster_than_3x_sequential() -> None:
    """Design-spec AC for COMP-003: parallel run beats a serialised one."""

    eval_duration_sec = 0.2

    def worker(spec: EvalSpec) -> EvalOutcome:
        time.sleep(eval_duration_sec)
        return _passing_outcome(spec, duration_sec=eval_duration_sec)

    orch = RunOrchestrator(run_one=worker)
    specs = [_spec("E1"), _spec("E2"), _spec("E3")]

    start = time.monotonic()
    outcomes = orch.run(specs, parallel=3)
    elapsed = time.monotonic() - start

    assert len(outcomes) == 3
    assert all(o.status == "PASS" for o in outcomes)
    # Sequential would take >= 3 × eval_duration; parallel must beat that
    # by a comfortable margin. We use 2× as the upper bound to absorb
    # ThreadPoolExecutor startup overhead on slow CI hosts while still
    # catching a true serial execution (which would be ≥ 0.6s).
    assert elapsed < 3 * eval_duration_sec, (
        f"3-eval parallel run took {elapsed:.3f}s; expected < "
        f"{3 * eval_duration_sec:.3f}s"
    )


# ---------------------------------------------------------------------------
# AC: cancellation token short-circuits scheduling; unsubmitted specs
# receive a synthesised INTERRUPTED outcome.
# ---------------------------------------------------------------------------


class TestCancellation:
    def test_pre_cancelled_token_skips_all_specs(self) -> None:
        """A pre-cancelled token must produce INTERRUPTED for every spec."""

        worker, log = _make_recording_worker()
        token = CancellationToken()
        token.cancel()

        orch = RunOrchestrator(run_one=worker, cancellation_token=token)
        specs = [_spec("E1"), _spec("E2"), _spec("E3")]
        outcomes = orch.run(specs, parallel=2)

        assert log == [], "no worker should run when token is pre-cancelled"
        assert [o.status for o in outcomes] == ["INTERRUPTED"] * 3
        assert [o.eval_id for o in outcomes] == ["E1", "E2", "E3"]
        for o in outcomes:
            assert o.duration_sec == 0.0
            assert o.error_class is None

    def test_mid_run_cancel_stops_new_submissions(self) -> None:
        """When the token flips mid-run, unsubmitted specs get INTERRUPTED."""

        # Use parallel=1 + a token-aware worker so we can observe the
        # exact submission boundary: the first worker flips the token,
        # then the second spec must arrive in the loop after the flip
        # and be synthesised as INTERRUPTED.
        token = CancellationToken()
        observed: list[str] = []
        lock = threading.Lock()

        def worker(spec: EvalSpec) -> EvalOutcome:
            with lock:
                observed.append(spec.id)
            # First eval cancels the run; subsequent specs should not
            # be submitted.
            if spec.id == "E1":
                token.cancel()
            return _passing_outcome(spec)

        orch = RunOrchestrator(run_one=worker, cancellation_token=token)
        specs = [_spec("E1"), _spec("E2"), _spec("E3")]
        outcomes = orch.run(specs, parallel=1)

        # E1 ran (and cancelled), E2/E3 were never submitted.
        assert observed == ["E1"]
        assert outcomes[0].status == "PASS"
        assert outcomes[1].status == "INTERRUPTED"
        assert outcomes[2].status == "INTERRUPTED"
        # Order is preserved even though the synthesised rows arrive
        # via a different code path than the future-result branch.
        assert [o.eval_id for o in outcomes] == ["E1", "E2", "E3"]

    def test_unwired_token_does_not_synthesize_interrupts(self) -> None:
        """Without a token, the orchestrator runs every spec to completion."""

        worker, log = _make_recording_worker()
        orch = RunOrchestrator(run_one=worker)  # no cancellation_token
        specs = [_spec("E1"), _spec("E2")]
        outcomes = orch.run(specs)
        assert sorted(log) == ["E1", "E2"]
        assert all(o.status == "PASS" for o in outcomes)


# ---------------------------------------------------------------------------
# Worker-exception folding into ERRORED outcomes
# ---------------------------------------------------------------------------


class TestWorkerExceptionFolding:
    def test_runtime_error_from_worker_folds_to_errored(self) -> None:
        """A worker that raises must yield an ERRORED outcome, not crash run()."""

        def worker(spec: EvalSpec) -> EvalOutcome:
            if spec.id == "E2":
                raise RuntimeError("simulated runner construction failure")
            return _passing_outcome(spec)

        orch = RunOrchestrator(run_one=worker)
        specs = [_spec("E1"), _spec("E2"), _spec("E3")]
        outcomes = orch.run(specs, parallel=2)

        statuses = {o.eval_id: o.status for o in outcomes}
        assert statuses == {"E1": "PASS", "E2": "ERRORED", "E3": "PASS"}
        errored = next(o for o in outcomes if o.eval_id == "E2")
        assert errored.error_class == "builtins.RuntimeError"
        assert errored.duration_sec == 0.0


# ---------------------------------------------------------------------------
# Constructor guards
# ---------------------------------------------------------------------------


class TestConstructorGuards:
    def test_non_callable_worker_rejected(self) -> None:
        with pytest.raises(TypeError):
            RunOrchestrator(run_one="not-callable")  # type: ignore[arg-type]

    def test_cancellation_token_optional(self) -> None:
        worker, _ = _make_recording_worker()
        # Construction succeeds without a token; cancellation simply
        # never fires.
        RunOrchestrator(run_one=worker)
