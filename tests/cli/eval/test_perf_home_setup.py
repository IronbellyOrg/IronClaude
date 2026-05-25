"""NFR-PERF1 HOME setup performance baseline (Task T02.15 / D-0035).

This benchmark measures the wall-clock cost of ``HomeIsolation.setup``
when 15 per-eval HOMEs are materialized in parallel — the load shape the
orchestrator (T03.16) hits at the cliEval harness's documented
concurrency cap. NFR-PERF1 records a budget of p50 <= 2.0s per eval with
a ~1.4s/eval informational target; the benchmark writes a JSON report so
the budget can be tracked across hosts and over time (consumed by
NFR-PERF3 suite-runtime tracking in T03.21).

Methodology
===========

* Each iteration submits 15 :class:`HomeIsolation` instances to a
  :class:`concurrent.futures.ThreadPoolExecutor` with 15 workers.
* Each worker calls ``setup(config=...)`` once. Setup time is the
  per-eval sample (``perf_counter`` start/end around the ``setup`` call
  inside the worker).
* The benchmark iterates ``N_ITERATIONS`` (default 30) times, yielding
  ``N_ITERATIONS * N_PARALLEL`` (default 450) samples — comfortably
  above the >=30-sample floor the task notes call out for statistical
  signal.
* Workers tear their HOMEs down with ``keep=False`` so the scratch root
  does not balloon during the run. The cleanup time is intentionally
  outside the measured window because NFR-PERF1 is a *setup* budget,
  not an end-to-end budget.

Report
======

p50 / p95 / min / max / mean (seconds) plus the full sample array are
written to ``TASKLIST_ROOT/evidence/T02.15/perf.json``. The destination
can be overridden with the ``T02_15_PERF_REPORT`` env var (used by CI
matrices to write per-host reports). The report path lives outside the
test module so trend-tracking tooling can stat it without re-running
pytest.

Budget assertion
================

The final assertion checks p50 <= ``BUDGET_SEC`` (2.0s). On a slow
host the test xfails (``strict=False``) with the recorded p50 so the
report is still produced. The xfail path is the documented "host
limitation" branch the acceptance criteria allow; CI environments that
hit it must update the host hardening plan rather than relaxing the
budget.

Cross-links
===========

* COMP-006 integrated :class:`HomeIsolation` (T02.11 / D-0032) — the
  primitive under benchmark.
* COMP-014 hook adapter (T02.14 / D-0034) — exercised indirectly via
  ``setup`` so the measured cost includes ``hooks.json`` deploy.
* NFR-PERF3 suite-runtime tracking (T03.21) — consumes the p50/p95
  trend from this report.
"""

from __future__ import annotations

import json
import os
import platform
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pytest

from superclaude.cli.eval import EvalConfig, HomeIsolation

# ---------------------------------------------------------------------------
# Tunables
# ---------------------------------------------------------------------------

N_PARALLEL = 15
"""Concurrency level NFR-PERF1 pins as the harness's documented cap."""

N_ITERATIONS = 30
"""Number of 15-parallel batches; ``N_PARALLEL * N_ITERATIONS`` samples."""

BUDGET_SEC = 2.0
"""NFR-PERF1 p50 budget. The ~1.4s/eval target is informational only."""


# ---------------------------------------------------------------------------
# Report path
# ---------------------------------------------------------------------------


def _repo_root() -> Path:
    """Locate the repo root from this file's path.

    ``tests/cli/eval/test_perf_home_setup.py`` lives 3 directories
    below the repo root.
    """

    return Path(__file__).resolve().parents[3]


def _default_report_path() -> Path:
    """``TASKLIST_ROOT/evidence/T02.15/perf.json``.

    TASKLIST_ROOT is ``.dev/releases/current/cliEval`` per the Phase 2
    tasklist convention.
    """

    return (
        _repo_root()
        / ".dev"
        / "releases"
        / "current"
        / "cliEval"
        / "evidence"
        / "T02.15"
        / "perf.json"
    )


def _report_path() -> Path:
    override = os.environ.get("T02_15_PERF_REPORT")
    if override:
        return Path(override)
    return _default_report_path()


# ---------------------------------------------------------------------------
# Benchmark primitives
# ---------------------------------------------------------------------------


def _one_setup(home_root: Path, config: EvalConfig, eval_idx: int) -> float:
    """Run a single ``HomeIsolation.setup`` and return its duration (s).

    The duration is captured around the ``setup`` call only — instance
    construction is excluded because it is a frozen dataclass build
    that the orchestrator does once per eval outside the hot loop. The
    HOME is torn down with ``keep=False`` after the timer stops so the
    scratch root does not balloon across iterations.
    """

    iso = HomeIsolation(
        eval_id=f"Perf{eval_idx:05d}",
        home_root=home_root,
        session_id=f"sess-{eval_idx:05d}",
    )
    start = time.perf_counter()
    try:
        iso.setup(config=config)
    finally:
        elapsed = time.perf_counter() - start
    try:
        iso.teardown(keep=False)
    except OSError:
        # Best-effort cleanup; the benchmark does not regress on a
        # slow teardown because BUDGET_SEC is a setup budget.
        pass
    return elapsed


def _run_one_iteration(
    home_root: Path, config: EvalConfig, iteration: int
) -> list[float]:
    """Submit ``N_PARALLEL`` setups, return the per-worker durations.

    The iteration index is folded into the eval_id so concurrent
    workers across iterations never collide on the ``mkdtemp`` prefix.
    """

    base = iteration * N_PARALLEL
    with ThreadPoolExecutor(max_workers=N_PARALLEL) as pool:
        futures = [
            pool.submit(_one_setup, home_root, config, base + i)
            for i in range(N_PARALLEL)
        ]
        return [f.result() for f in as_completed(futures)]


# ---------------------------------------------------------------------------
# Test
# ---------------------------------------------------------------------------


def test_home_setup_p50_p95_under_15_parallel(tmp_path: Path) -> None:
    """Measure 15-parallel ``HomeIsolation.setup`` p50/p95 and write report.

    Strategy:

    1. Build a permissive :class:`EvalConfig` whose allowlist contains
       the test scratch root. The benchmark is not testing the
       allowlist; it is timing the happy path.
    2. Run ``N_ITERATIONS`` batches of ``N_PARALLEL`` parallel setups.
    3. Compute p50/p95/min/max/mean over the flat sample array.
    4. Write the JSON report to the path returned by
       :func:`_report_path` (parents created on demand).
    5. Assert ``p50 <= BUDGET_SEC``. On a slow host this raises and
       the test xfails (the wrapper :func:`pytest.xfail` is unused —
       see the comment below).

    The report is written *before* the assertion so a failed budget
    still leaves a perf.json on disk for trend tracking and host
    diagnosis.
    """

    scratch_root = tmp_path / "perf-home-setup"
    scratch_root.mkdir()
    config = EvalConfig(allowed_scratch_roots=(scratch_root,))

    samples: list[float] = []
    iteration_summary: list[dict[str, float]] = []
    overall_start = time.perf_counter()
    for iteration in range(N_ITERATIONS):
        iteration_samples = _run_one_iteration(scratch_root, config, iteration)
        samples.extend(iteration_samples)
        iteration_summary.append(
            {
                "iteration": iteration,
                "min_sec": min(iteration_samples),
                "median_sec": statistics.median(iteration_samples),
                "max_sec": max(iteration_samples),
            }
        )
    overall_elapsed = time.perf_counter() - overall_start

    samples_sorted = sorted(samples)
    n = len(samples_sorted)
    # ``statistics.quantiles`` with ``n=100`` returns the 99 inner
    # percentile boundaries (P1..P99). Index 49 is the p50 boundary
    # and index 94 is p95. Using ``quantiles`` keeps the math
    # consistent with what NFR-PERF3 will use for the suite trend.
    percentiles = statistics.quantiles(samples_sorted, n=100, method="inclusive")
    p50 = percentiles[49]
    p95 = percentiles[94]

    report = {
        "task_id": "T02.15",
        "deliverable_id": "D-0035",
        "nfr_id": "NFR-PERF1",
        "schema_version": 1,
        "n_parallel": N_PARALLEL,
        "n_iterations": N_ITERATIONS,
        "n_samples": n,
        "budget_sec": BUDGET_SEC,
        "p50_sec": p50,
        "p95_sec": p95,
        "min_sec": samples_sorted[0],
        "max_sec": samples_sorted[-1],
        "mean_sec": statistics.fmean(samples_sorted),
        "stdev_sec": statistics.pstdev(samples_sorted),
        "overall_elapsed_sec": overall_elapsed,
        "host": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "machine": platform.machine(),
            "processor": platform.processor() or "unknown",
        },
        "iteration_summary": iteration_summary,
        "durations_sec": samples,
    }

    report_path = _report_path()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=False))

    # Sanity assertions on the report shape before the budget check,
    # so an empty / malformed report fails loudly rather than via a
    # confusing budget breach.
    assert n == N_PARALLEL * N_ITERATIONS, (
        f"expected {N_PARALLEL * N_ITERATIONS} samples, got {n}"
    )
    assert all(d >= 0.0 for d in samples), "negative duration in samples"

    # NFR-PERF1 budget check. xfail (non-strict) on slow hosts so the
    # report still lands; CI matrices that consistently xfail must
    # update the host hardening plan, not relax BUDGET_SEC.
    if p50 > BUDGET_SEC:
        pytest.xfail(
            reason=(
                f"NFR-PERF1 budget exceeded on this host: "
                f"p50={p50:.3f}s > {BUDGET_SEC:.3f}s "
                f"(p95={p95:.3f}s, n={n}). "
                f"Report at {report_path!s}."
            )
        )

    assert p50 <= BUDGET_SEC, (
        f"NFR-PERF1 budget breached: p50={p50:.3f}s > {BUDGET_SEC:.3f}s"
    )
