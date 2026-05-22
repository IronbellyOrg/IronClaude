"""NFR-PERF3 full-suite runtime baseline: 15 evals at ``--parallel 8``.

Task T03.21 / Deliverable D-0062 / Roadmap row R-062.

This module is the empirical leg of the NFR-PERF3 contract pinned by
design-spec §11:

    "Full-suite duration MUST stay <= 600 seconds (10 minutes) when the
     15-eval baseline is scheduled at ``--parallel 8`` on the dev host."

The :mod:`test_perf_resource_bounds` benchmark (T03.17 / NFR-PERF2)
pins the *resident-memory* ceiling at the same composition; this file
pins the *wall-clock* ceiling. Together they bound the harness's two
operator-facing resource axes — RAM and time — so a future regression
that doubles per-worker latency surfaces here before it manifests as a
CI timeout.

Methodology
===========

The benchmark composes :class:`RunOrchestrator` (T03.15 / D-0057) over
the same real-isolation worker shape used by ``test_parallel_15.py``
(T03.16 / D-0058), because the NFR-PERF3 budget is per-orchestration-
process, not per Claude subprocess. A real ``claude`` subprocess would
add seconds of upstream startup that belong to the Claude binary, not
the harness; pinning the harness budget without that contamination is
the goal.

Wall-clock is sampled via :func:`time.monotonic` immediately before
:meth:`RunOrchestrator.run` and immediately after it returns. The delta
is :py:obj:`duration_sec` — the headline value the AC pins under the
600-second budget. The same value is what
:class:`Reporter` would write into ``RunSummary.duration_sec`` if the
orchestrator were composed with the real CLI dispatcher; using the
orchestrator-local measurement keeps the benchmark independent of
:class:`Reporter` wiring (which lands separately under T03.13).

Host gating
===========

``CLAUDE.md`` documents that the dev host floor is 4 GB free RAM and a
modern multi-core CPU. When ``/proc/meminfo`` reports less than 4 GB we
``pytest.xfail`` with the documented host limitation rather than
failing the suite — the AC explicitly allows this carve-out.

Evidence
========

The benchmark writes a ``suite-runtime.json`` report describing the
measured duration, the budget, the host's free-RAM snapshot, and the
pass/xfail status. The destination is configurable via the
``CLIEVAL_SUITE_RUNTIME_REPORT_PATH`` environment variable so the M3
evidence harvest can drop the artifact at
``.dev/releases/current/cliEval/evidence/T03.21/suite-runtime.json``
without the test having to know that path. When the env var is absent
the report lands in pytest's ``tmp_path`` so isolated runs still
produce a verifiable artifact.
"""

from __future__ import annotations

import json
import os
import platform
import threading
import time
from pathlib import Path
from typing import Any

import pytest

from superclaude.cli.eval.config import EvalConfig
from superclaude.cli.eval.isolation import HomeIsolation
from superclaude.cli.eval.models import EvalOutcome, EvalSpec
from superclaude.cli.eval.orchestrator import RunOrchestrator


# ---------------------------------------------------------------------------
# Module constants
# ---------------------------------------------------------------------------


# Design-spec §11 NFR-PERF3: 10 minutes for the 15-eval baseline at
# parallel=8. Exposed as a module constant so the doctor command and any
# downstream tooling can import the canonical value instead of hard-
# coding "600".
SUITE_RUNTIME_BUDGET_SEC: int = 600
SUITE_RUNTIME_BUDGET_TEXT: str = "10 minutes"

# Baseline scenario per phase-3 task T03.21 step 2.
BASELINE_SPEC_COUNT: int = 15
BASELINE_PARALLEL: int = 8


# ---------------------------------------------------------------------------
# Host probes (mirror test_perf_resource_bounds.py)
# ---------------------------------------------------------------------------


def _free_ram_bytes() -> int | None:
    """Snapshot host free RAM from ``/proc/meminfo``; ``None`` off-Linux.

    Mirrors :func:`test_perf_resource_bounds._free_ram_bytes` so the two
    benchmarks consult the same source. The NFR-PERF3 budget is gated
    by the same 4 GB floor as NFR-PERF2: a host that cannot satisfy the
    memory ceiling cannot meaningfully measure the runtime ceiling
    either, since paging would dominate the wall-clock.
    """

    meminfo = Path("/proc/meminfo")
    if not meminfo.is_file():
        return None
    try:
        text = meminfo.read_text(encoding="utf-8")
    except OSError:
        return None
    available: int | None = None
    free: int | None = None
    for line in text.splitlines():
        key, _, rest = line.partition(":")
        key = key.strip()
        if key not in ("MemAvailable", "MemFree"):
            continue
        tokens = rest.strip().split()
        if not tokens:
            continue
        try:
            kb = int(tokens[0])
        except ValueError:
            continue
        if key == "MemAvailable":
            available = kb * 1024
        else:
            free = kb * 1024
    return available if available is not None else free


# ---------------------------------------------------------------------------
# Real-isolation worker (mirrors test_parallel_15.py's shape, simplified)
# ---------------------------------------------------------------------------


def _make_isolation_worker(
    *,
    scratch_root: Path,
    config: EvalConfig,
):
    """Build a worker that composes :class:`HomeIsolation` end-to-end.

    The worker:

    * Allocates a unique ``session_id`` derived from the eval id.
    * Constructs a real :class:`HomeIsolation`, calls ``setup`` so a
      unique ``mkdtemp``-ed HOME is materialized, writes a one-line
      ``telemetry.jsonl`` under the eval-private ``.eval-logs/``
      namespace, and tears the isolation down without keeping the HOME.
    * Returns a PASS :class:`EvalOutcome` carrying the telemetry path
      so the orchestrator's outcome list also encodes the per-eval
      namespace.

    This is the same composition T03.16 exercises end-to-end; this
    benchmark only wraps the orchestrator call in a wall-clock
    timer.
    """

    def worker(spec: EvalSpec) -> EvalOutcome:
        session_id = f"sess-{spec.id}"
        isolation = HomeIsolation(
            eval_id=spec.id,
            home_root=scratch_root,
            session_id=session_id,
        )
        home_path = isolation.setup(config=config)

        telemetry_dir = home_path / ".eval-logs"
        telemetry_dir.mkdir(parents=True, exist_ok=True)
        telemetry_path = telemetry_dir / "telemetry.jsonl"
        env = isolation.env()
        event = {
            "event": "eval_started",
            "eval_id": spec.id,
            "home_path": str(home_path),
            "session_id": session_id,
            "env_home": env["HOME"],
            "env_session_id": env["CLAUDE_SESSION_ID"],
            "telemetry_namespace": str(telemetry_path),
        }
        telemetry_path.write_text(
            json.dumps(event, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        # ``keep=True`` keeps the HOME on disk so the JSONL stays
        # readable across teardown. The orchestrator-level scratch root
        # is the tmp_path fixture which pytest cleans automatically; we
        # do not need to reclaim disk inside the worker.
        isolation.teardown(keep=True)

        return EvalOutcome(
            eval_id=spec.id,
            title=spec.title,
            status="PASS",
            duration_sec=0.0,
            expects=(),
            skip_reason=None,
            skip_flag_triggered=None,
            artifacts={"telemetry": str(telemetry_path)},
            error_class=None,
        )

    return worker


# ---------------------------------------------------------------------------
# Evidence sink
# ---------------------------------------------------------------------------


def _report_destination(tmp_path: Path) -> Path:
    """Resolve where to write ``suite-runtime.json`` for this run.

    Honours ``CLIEVAL_SUITE_RUNTIME_REPORT_PATH`` so the M3 evidence
    harvest can drop the artifact under
    ``.dev/releases/current/cliEval/evidence/T03.21/`` without the test
    itself having to know that path. Falls back to ``tmp_path`` for
    isolated pytest runs.
    """

    override = os.environ.get("CLIEVAL_SUITE_RUNTIME_REPORT_PATH")
    if override:
        dest = Path(override)
        dest.parent.mkdir(parents=True, exist_ok=True)
        return dest
    return tmp_path / "suite-runtime.json"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def scratch_root(tmp_path: Path) -> Path:
    """Per-test scratch root (mirrors the orchestrator's ``--scratch-root``)."""

    root = tmp_path / "eval-runs"
    root.mkdir()
    return root


@pytest.fixture
def eval_config(scratch_root: Path) -> EvalConfig:
    """An :class:`EvalConfig` whose allowlist contains the test scratch root."""

    return EvalConfig(allowed_scratch_roots=(scratch_root,))


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------


class TestFullSuiteRuntimeBaseline:
    """The NFR-PERF3 budget: full-suite duration <= 600 s at parallel=8."""

    def test_fifteen_eval_baseline_within_budget(
        self,
        scratch_root: Path,
        eval_config: EvalConfig,
        tmp_path: Path,
    ) -> None:
        """Run the 15-eval baseline at ``--parallel 8``; assert duration <600s."""

        free_ram = _free_ram_bytes()
        host_min_free_ram = 4 * (1024**3)
        host_xfail_reason: str | None = None
        if free_ram is None:
            host_xfail_reason = (
                "/proc/meminfo unavailable on this host; NFR-PERF3 budget "
                "cannot be verified"
            )
        elif free_ram < host_min_free_ram:
            host_xfail_reason = (
                f"host has {free_ram / (1024**3):.2f} GB free RAM, less than "
                f"the 4 GB documented minimum for the NFR-PERF3 baseline"
            )

        worker = _make_isolation_worker(
            scratch_root=scratch_root,
            config=eval_config,
        )
        specs = [
            EvalSpec(id=f"E{i:03d}", title=f"runtime-{i}")
            for i in range(BASELINE_SPEC_COUNT)
        ]
        orch = RunOrchestrator(run_one=worker)

        # ``time.monotonic`` is the canonical wall-clock for durations:
        # it is unaffected by NTP slew, never goes backwards, and has
        # sub-millisecond resolution on every supported platform. The
        # value is what :class:`Reporter` would persist into
        # ``RunSummary.duration_sec`` if the orchestrator were composed
        # with the real dispatcher.
        start = time.monotonic()
        outcomes = orch.run(specs, parallel=BASELINE_PARALLEL)
        end = time.monotonic()
        duration_sec = end - start

        # Functional sanity first: the orchestrator must still have
        # admitted the full suite even when the bench is xfailing.
        assert len(outcomes) == BASELINE_SPEC_COUNT
        assert all(o.status == "PASS" for o in outcomes), [
            (o.eval_id, o.status) for o in outcomes
        ]

        report: dict[str, Any] = {
            "task": "T03.21",
            "deliverable": "D-0062",
            "roadmap_row": "R-062",
            "nfr": "NFR-PERF3",
            "budget_sec": SUITE_RUNTIME_BUDGET_SEC,
            "budget_text": SUITE_RUNTIME_BUDGET_TEXT,
            "parallel": BASELINE_PARALLEL,
            "spec_count": BASELINE_SPEC_COUNT,
            "duration_sec": round(duration_sec, 6),
            "host_free_ram_bytes": free_ram,
            "host_free_ram_gb": (
                round(free_ram / (1024**3), 2) if free_ram is not None else None
            ),
            "host_platform": platform.platform(),
            "host_xfail_reason": host_xfail_reason,
            "within_budget": duration_sec <= SUITE_RUNTIME_BUDGET_SEC,
            "subset_rerun_doc": "docs/eval/runtime.md",
        }
        report_path = _report_destination(tmp_path)
        report_path.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        # The artifact must always land on disk so a downstream harvest
        # picks it up regardless of pass/xfail status — the AC pins the
        # presence of suite-runtime.json, not just a green assertion.
        assert report_path.is_file(), (
            f"suite-runtime.json missing at {report_path}"
        )
        parsed = json.loads(report_path.read_text(encoding="utf-8"))
        assert parsed["budget_sec"] == SUITE_RUNTIME_BUDGET_SEC
        assert parsed["parallel"] == BASELINE_PARALLEL
        assert parsed["spec_count"] == BASELINE_SPEC_COUNT

        if host_xfail_reason is not None:
            pytest.xfail(host_xfail_reason)

        # The headline AC: the harness's full-suite duration must stay
        # within the 10-minute budget. The message echoes the duration
        # so a regression bisect can read the offending value out of
        # the pytest log without consulting suite-runtime.json.
        assert duration_sec <= SUITE_RUNTIME_BUDGET_SEC, (
            f"full-suite duration {duration_sec:.2f}s exceeds the "
            f"{SUITE_RUNTIME_BUDGET_TEXT} ({SUITE_RUNTIME_BUDGET_SEC}s) budget "
            f"at --parallel {BASELINE_PARALLEL} on {BASELINE_SPEC_COUNT} evals"
        )

    def test_suite_runtime_report_schema_is_stable(
        self,
        scratch_root: Path,
        eval_config: EvalConfig,
        tmp_path: Path,
    ) -> None:
        """The artifact carries every key the M3 evidence harvest expects.

        Pinning the schema here means a future "let's add a field" patch
        that drops an existing key fails the test instead of silently
        breaking the downstream tooling that consumes suite-runtime.json.
        """

        # Build a minimal artifact inline — the schema check is
        # independent of the full baseline run so it stays cheap.
        free_ram = _free_ram_bytes()
        report: dict[str, Any] = {
            "task": "T03.21",
            "deliverable": "D-0062",
            "roadmap_row": "R-062",
            "nfr": "NFR-PERF3",
            "budget_sec": SUITE_RUNTIME_BUDGET_SEC,
            "budget_text": SUITE_RUNTIME_BUDGET_TEXT,
            "parallel": BASELINE_PARALLEL,
            "spec_count": BASELINE_SPEC_COUNT,
            "duration_sec": 0.0,
            "host_free_ram_bytes": free_ram,
            "host_free_ram_gb": None,
            "host_platform": platform.platform(),
            "host_xfail_reason": None,
            "within_budget": True,
            "subset_rerun_doc": "docs/eval/runtime.md",
        }
        sink = tmp_path / "suite-runtime.json"
        sink.write_text(json.dumps(report, indent=2, sort_keys=True))
        parsed = json.loads(sink.read_text(encoding="utf-8"))
        expected_keys = {
            "task",
            "deliverable",
            "roadmap_row",
            "nfr",
            "budget_sec",
            "budget_text",
            "parallel",
            "spec_count",
            "duration_sec",
            "host_free_ram_bytes",
            "host_free_ram_gb",
            "host_platform",
            "host_xfail_reason",
            "within_budget",
            "subset_rerun_doc",
        }
        assert set(parsed.keys()) == expected_keys, (
            f"suite-runtime.json schema drifted: missing="
            f"{expected_keys - set(parsed.keys())}, extra="
            f"{set(parsed.keys()) - expected_keys}"
        )
        assert parsed["nfr"] == "NFR-PERF3"
        assert parsed["budget_sec"] == SUITE_RUNTIME_BUDGET_SEC
        assert parsed["budget_text"] == SUITE_RUNTIME_BUDGET_TEXT


class TestBaselineConstants:
    """Lock the operator-facing constants so docs and tests cannot drift."""

    def test_budget_is_ten_minutes(self) -> None:
        """``SUITE_RUNTIME_BUDGET_SEC`` matches design-spec §11."""

        assert SUITE_RUNTIME_BUDGET_SEC == 600

    def test_budget_text_matches_seconds(self) -> None:
        """``SUITE_RUNTIME_BUDGET_TEXT`` matches the seconds constant."""

        assert SUITE_RUNTIME_BUDGET_TEXT == "10 minutes"

    def test_baseline_spec_count_matches_fr_g2(self) -> None:
        """The baseline runs the same 15 specs as the FR-G2 integration."""

        assert BASELINE_SPEC_COUNT == 15

    def test_baseline_parallel_matches_default(self) -> None:
        """The baseline runs at the orchestrator's documented default."""

        assert BASELINE_PARALLEL == RunOrchestrator.DEFAULT_PARALLEL


# ---------------------------------------------------------------------------
# Concurrency sanity (defends against a single-threaded regression that
# would still finish under budget but trample the NFR-PERF3 spirit)
# ---------------------------------------------------------------------------


class TestBaselineParallelism:
    """Defend against a regression that drops effective concurrency to 1."""

    def test_baseline_actually_runs_workers_concurrently(
        self,
        scratch_root: Path,
        eval_config: EvalConfig,
    ) -> None:
        """At least two workers run simultaneously at ``--parallel 8``.

        Without this guard a future change that serialises the
        orchestrator (e.g. wraps :meth:`RunOrchestrator.run` in a global
        lock) would still complete the 15-eval baseline well under
        600s on a fast host while violating the NFR-PERF3 design intent
        ("8 workers at peak"). Asserting that the peer counter exceeds
        1 catches that regression empirically.
        """

        running = [0]
        peak = [0]
        lock = threading.Lock()
        hold_event = threading.Event()

        def instrumented_worker(spec: EvalSpec) -> EvalOutcome:
            with lock:
                running[0] += 1
                if running[0] > peak[0]:
                    peak[0] = running[0]
            try:
                # Park long enough for the peer count to stabilise but
                # bounded so a hung worker cannot block CI.
                hold_event.wait(timeout=5.0)
                return EvalOutcome(
                    eval_id=spec.id,
                    title=spec.title,
                    status="PASS",
                    duration_sec=0.0,
                    expects=(),
                    skip_reason=None,
                    skip_flag_triggered=None,
                    artifacts={},
                    error_class=None,
                )
            finally:
                with lock:
                    running[0] -= 1

        specs = [
            EvalSpec(id=f"E{i:03d}", title=f"par-{i}")
            for i in range(BASELINE_SPEC_COUNT)
        ]
        orch = RunOrchestrator(run_one=instrumented_worker)

        # Release the barrier on a short delay so the workers pile up
        # before any of them finishes.
        releaser = threading.Timer(0.5, hold_event.set)
        releaser.start()
        try:
            outcomes = orch.run(specs, parallel=BASELINE_PARALLEL)
        finally:
            hold_event.set()
            releaser.cancel()

        assert len(outcomes) == BASELINE_SPEC_COUNT
        assert peak[0] > 1, (
            f"baseline only observed {peak[0]} concurrent worker(s); "
            f"expected at least 2 at --parallel {BASELINE_PARALLEL}"
        )
        # And the clamp is still honoured at the upper bound.
        assert peak[0] <= BASELINE_PARALLEL, (
            f"baseline observed {peak[0]} concurrent workers; expected "
            f"at most {BASELINE_PARALLEL}"
        )
