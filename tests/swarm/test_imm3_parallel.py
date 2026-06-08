"""T03.02 / T03.11 -- IMM-3 true-parallel dispatch verification.

IMM-3 mandates that ``dispatch_wave1`` fan workers out in genuine
wall-clock parallelism (not sequential, not attention-mediated). The
contract is verified against a fixture transport that sleeps for a
known interval per ``send`` call: if dispatch is genuinely parallel,
the wall-clock for N workers each sleeping ``S`` seconds is ~ S
(plus dispatch overhead), not N*S.

Phase-3 tasklist acceptance criterion (T03.02):

    "N workers dispatched concurrently against the stub transport
    (overlap window >= 80% of max(elapsed))."

We discharge that as: with N=4 workers each sleeping ``S=0.4s``, the
sequential baseline is ``N*S = 1.6s`` and the parallel target is
``< N*S * 0.4 = 0.64s``. A safety margin of 1.0s lets the test ride
out CI scheduler jitter without losing its discriminating power
(``1.0s < 1.6s`` still proves overlap; the 0.64s assertion is the
hard contract).

Phase-3 task T03.11 deepens this surface with:

* ``test_imm3_sequential_baseline_speedup`` -- measures the
  single-worker baseline wall-clock and asserts the N-worker parallel
  speedup is at least ``0.4 * N`` (i.e. parallel wall-clock is at
  most ``2.5x`` the single-worker baseline rather than the ``Nx``
  it would be for sequential dispatch). This is the formal
  speedup contract from the T03.11 acceptance criteria.
* ``test_imm3_parallel_group_invoked_exactly_once`` -- wraps
  ``ParallelExecutor.execute`` and asserts that ``dispatch_wave1``
  drives a *single* execute() call carrying exactly one
  :class:`ParallelGroup` (all N workers in one fan-out, no
  sequential staging).
"""

from __future__ import annotations

import threading
import time

import pytest

from superclaude.cli.swarm.dispatch import dispatch_wave1
from superclaude.cli.swarm.models import (
    Manifest,
    PreflightSummary,
    SwarmState,
    WorkerResult,
)
from superclaude.cli.swarm.preflight import PreflightResult
from superclaude.execution.parallel import ExecutionPlan, ParallelExecutor

# IMM-3 parallelism coverage (T08.03 / NFR-007). Module-level marker so
# every test in this file is selected by ``pytest -m imm``.
pytestmark = pytest.mark.imm


# Tunables -- chosen so the test runs quickly while still leaving a
# clear gap between sequential and parallel wall-clock.
_WORKERS = 4
_SLEEP_SEC = 0.4

# Hard contract: parallel wall-clock must be < 40% of sequential.
# Sequential = N * S = 1.6s; parallel target = 0.64s.
_PARALLEL_BUDGET_SEC = _WORKERS * _SLEEP_SEC * 0.4

# Soft safety: also assert wall-clock is well under sequential so
# the test still surfaces a regression on a heavily loaded CI host
# where the 0.4 ratio might flake.
_SOFT_BUDGET_SEC = 1.0


class _SleepingTransport:
    """Sleeps ``_SLEEP_SEC`` per call before returning success.

    Records the (start, end) wall-clock per call so the test can
    confirm overlap directly (call N's start < call 0's end).
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.intervals: list[tuple[float, float]] = []

    def send(self, prompt: str, timeout: int) -> WorkerResult:
        start = time.monotonic()
        time.sleep(_SLEEP_SEC)
        end = time.monotonic()
        with self._lock:
            self.intervals.append((start, end))
        return WorkerResult(status="success", http_code=200, attempts=1)


def _make_preflight(workers_requested: int) -> PreflightResult:
    manifest = Manifest(
        contract_version="1.0",
        job_id="job-imm3",
        preflight=PreflightSummary(
            target_checksum="cafebabe",
            workers_requested=workers_requested,
            transport_kind="stub",
        ),
    )
    return PreflightResult(
        manifest=manifest,
        state=SwarmState(state="preflight_ok", job_id="job-imm3"),
    )


def test_imm3_parallel_wall_clock_under_sequential_budget() -> None:
    """IMM-3 contract: N workers overlap; wall-clock << N*S.

    The fixture transport sleeps ``_SLEEP_SEC`` per call. If
    dispatch were sequential, total wall-clock would be
    ``_WORKERS * _SLEEP_SEC`` (1.6s). The assertion below requires
    wall-clock under 40% of that, i.e. < 0.64s, which is only
    achievable when all ``_WORKERS`` workers run concurrently.
    """
    preflight = _make_preflight(workers_requested=_WORKERS)
    transport = _SleepingTransport()

    start = time.monotonic()
    results = dispatch_wave1(
        preflight,
        transport=transport,
        parallel_executor=ParallelExecutor(max_workers=_WORKERS),
    )
    elapsed = time.monotonic() - start

    assert len(results) == _WORKERS
    assert all(r.status == "success" for r in results)
    assert [r.index for r in results] == list(range(_WORKERS))

    # Hard contract -- parallelism proven.
    assert elapsed < _PARALLEL_BUDGET_SEC, (
        f"dispatch_wave1 wall-clock {elapsed:.3f}s exceeds parallel budget "
        f"{_PARALLEL_BUDGET_SEC:.3f}s; "
        f"sequential baseline would be {_WORKERS * _SLEEP_SEC:.3f}s. "
        "AC-004 / IMM-3 regression: dispatch is not fanning workers in "
        "wall-clock parallel."
    )
    # Soft safety floor -- catches a regression even under CI jitter.
    assert elapsed < _SOFT_BUDGET_SEC


def test_imm3_worker_intervals_overlap() -> None:
    """Direct overlap assertion: at least two workers' intervals overlap.

    Stronger than the wall-clock budget assertion -- proves the
    concurrency was real rather than merely fast. We require that
    the latest worker start be earlier than the earliest worker end;
    i.e. there is a moment when every worker is in-flight.
    """
    preflight = _make_preflight(workers_requested=_WORKERS)
    transport = _SleepingTransport()

    dispatch_wave1(
        preflight,
        transport=transport,
        parallel_executor=ParallelExecutor(max_workers=_WORKERS),
    )

    assert len(transport.intervals) == _WORKERS
    latest_start = max(start for start, _end in transport.intervals)
    earliest_end = min(end for _start, end in transport.intervals)
    # If all workers were in-flight simultaneously at some moment,
    # the latest start happened before the earliest end.
    assert latest_start < earliest_end, (
        "no overlapping window across worker intervals -- dispatch is "
        "sequential or thread-starved. "
        f"intervals={transport.intervals!r}"
    )


def test_imm3_sequential_baseline_speedup() -> None:
    """T03.11 -- formal sequential-baseline speedup assertion.

    Measures the single-worker wall-clock (N=1, one sleep of S) as
    the baseline, then runs N workers and asserts the speedup is at
    least ``0.4 * N``. With true parallelism the N-worker wall-clock
    is ~ baseline (overhead aside); with sequential dispatch it would
    be ``N * baseline``, yielding a speedup of 1. The 0.4 * N floor
    catches the regression while tolerating CI scheduler jitter.
    """
    baseline_transport = _SleepingTransport()
    baseline_preflight = _make_preflight(workers_requested=1)
    baseline_start = time.monotonic()
    baseline_results = dispatch_wave1(
        baseline_preflight,
        transport=baseline_transport,
        parallel_executor=ParallelExecutor(max_workers=1),
    )
    baseline_elapsed = time.monotonic() - baseline_start
    assert len(baseline_results) == 1
    assert baseline_results[0].status == "success"

    parallel_transport = _SleepingTransport()
    parallel_preflight = _make_preflight(workers_requested=_WORKERS)
    parallel_start = time.monotonic()
    parallel_results = dispatch_wave1(
        parallel_preflight,
        transport=parallel_transport,
        parallel_executor=ParallelExecutor(max_workers=_WORKERS),
    )
    parallel_elapsed = time.monotonic() - parallel_start
    assert len(parallel_results) == _WORKERS

    # Speedup = (N workers' sequential work) / (parallel wall-clock).
    # Sequential work estimate is N * baseline_elapsed, which mirrors
    # the cost of running the N-worker fan-out one at a time.
    speedup = (_WORKERS * baseline_elapsed) / parallel_elapsed
    floor = 0.4 * _WORKERS
    assert speedup >= floor, (
        f"speedup {speedup:.2f}x below floor {floor:.2f}x "
        f"(baseline={baseline_elapsed:.3f}s, parallel={parallel_elapsed:.3f}s, "
        f"N={_WORKERS}). AC-004 / IMM-3 regression: dispatch is not "
        "fanning workers in wall-clock parallel."
    )


class _GroupCountingExecutor(ParallelExecutor):
    """ParallelExecutor that records every plan + execute invocation.

    Used by ``test_imm3_parallel_group_invoked_exactly_once`` to assert
    that ``dispatch_wave1`` drives a single execute() call carrying
    exactly one ParallelGroup -- i.e. all N workers fan out in one
    parallel group rather than being staged across multiple groups
    (which would collapse back to a sequential schedule).
    """

    def __init__(self, max_workers: int) -> None:
        super().__init__(max_workers=max_workers)
        self.execute_calls: list[ExecutionPlan] = []
        self.group_counts: list[int] = []

    def execute(self, plan: ExecutionPlan):  # type: ignore[override]
        self.execute_calls.append(plan)
        self.group_counts.append(len(plan.groups))
        return super().execute(plan)


def test_imm3_parallel_group_invoked_exactly_once() -> None:
    """T03.11 -- ParallelGroup invoked exactly once per dispatch.

    Asserts the dispatch wave fires a single ``execute()`` call whose
    plan carries exactly one ParallelGroup containing all ``N`` worker
    tasks. A regression that splits workers across multiple groups
    (e.g. accidental dependencies, per-worker recursion) would
    serialise the fan-out and silently break IMM-3 even when the
    wall-clock assertion happens to pass under CI jitter.
    """
    preflight = _make_preflight(workers_requested=_WORKERS)
    transport = _SleepingTransport()
    executor = _GroupCountingExecutor(max_workers=_WORKERS)

    results = dispatch_wave1(
        preflight,
        transport=transport,
        parallel_executor=executor,
    )

    assert len(results) == _WORKERS
    assert len(executor.execute_calls) == 1, (
        f"dispatch_wave1 invoked execute() {len(executor.execute_calls)} times; "
        "IMM-3 contract requires exactly one fan-out call per wave."
    )
    assert executor.group_counts == [1], (
        f"dispatch plan carried {executor.group_counts} ParallelGroup(s); "
        "IMM-3 requires a single group holding all N workers."
    )
    only_plan = executor.execute_calls[0]
    assert len(only_plan.groups[0].tasks) == _WORKERS, (
        f"single ParallelGroup contained {len(only_plan.groups[0].tasks)} "
        f"tasks; expected {_WORKERS}."
    )
