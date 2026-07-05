"""T03.02 -- COMP-007 Wave 1 dispatch unit tests.

Pins the per-worker outcome recording contract:

1. ``transport=None`` -> empty list (wire-only path).
2. ``workers_requested == 0`` -> empty list.
3. N transport returns ``status='success'`` -> N WorkerResults all
   stamped with the slot index in 0..N-1 order.
4. ``TimeoutError`` raised by transport -> ``status='timeout'`` with
   ``attempts=1`` and ``elapsed_ms`` populated.
5. Generic transport exception -> ``status='proxy_error'`` with
   ``attempts=1`` and ``elapsed_ms`` populated.
6. Transport returns ``status='parse_error'`` -> the parse_error
   status survives unmodified through dispatch (Wave-2 normalize is
   responsible for §7.4 salvage promotion, not dispatch).
7. Routing assertion: dispatch invokes
   :class:`superclaude.execution.parallel.ParallelExecutor` via the
   injected executor (proves AC-004 routing without grep).
8. Mixed-outcome dispatch records every slot's outcome with the
   matching slot index even when slots disagree.

The IMM-3 wall-clock overlap test lives in
``tests/swarm/test_imm3_parallel.py``.
"""

from __future__ import annotations

from typing import Any

import pytest

from superclaude.cli.swarm.dispatch import dispatch_wave1
from superclaude.cli.swarm.models import (
    Manifest,
    PreflightSummary,
    SwarmState,
    WorkerResult,
)
from superclaude.cli.swarm.preflight import PreflightResult
from superclaude.execution.parallel import ParallelExecutor

# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------


def _make_preflight(
    workers_requested: int, job_id: str = "job-dispatch"
) -> PreflightResult:
    manifest = Manifest(
        contract_version="1.0",
        job_id=job_id,
        preflight=PreflightSummary(
            target_checksum="deadbeef",
            workers_requested=workers_requested,
            transport_kind="stub",
        ),
    )
    state = SwarmState(state="preflight_ok", job_id=job_id)
    return PreflightResult(manifest=manifest, state=state)


class _SuccessTransport:
    """Returns a clean ``status='success'`` per call.

    Records each ``send`` call so the test can assert the per-slot
    invocation count.
    """

    def __init__(self) -> None:
        self.calls: list[tuple[str, int]] = []

    def send(self, prompt: str, timeout: int) -> WorkerResult:
        self.calls.append((prompt, timeout))
        return WorkerResult(status="success", http_code=200, attempts=1)


class _TimeoutTransport:
    def send(self, prompt: str, timeout: int) -> WorkerResult:
        raise TimeoutError("simulated 180s budget exhausted")


class _ProxyErrorTransport:
    def send(self, prompt: str, timeout: int) -> WorkerResult:
        raise RuntimeError("simulated 5xx after retry")


class _ParseErrorTransport:
    def send(self, prompt: str, timeout: int) -> WorkerResult:
        return WorkerResult(status="parse_error", http_code=200, attempts=1)


class _MixedTransport:
    """Stamps a different status per slot based on call order.

    Used to prove dispatch records the right outcome at the right
    slot index even when slots disagree.
    """

    def __init__(self, statuses: list[str]) -> None:
        self._statuses = list(statuses)
        self._cursor = 0
        self._lock = __import__("threading").Lock()

    def send(self, prompt: str, timeout: int) -> WorkerResult:
        with self._lock:
            status = self._statuses[self._cursor]
            self._cursor += 1
        if status == "timeout":
            raise TimeoutError("budget")
        if status == "proxy_error":
            raise RuntimeError("upstream")
        return WorkerResult(status=status, http_code=200, attempts=1)


# ---------------------------------------------------------------------------
# Wire-only branches
# ---------------------------------------------------------------------------


def test_dispatch_wave1_transport_none_returns_empty() -> None:
    """``transport=None`` short-circuits to an empty list."""
    preflight = _make_preflight(workers_requested=4)
    assert dispatch_wave1(preflight, transport=None) == []


def test_dispatch_wave1_zero_workers_returns_empty() -> None:
    """``workers_requested == 0`` short-circuits to an empty list."""
    preflight = _make_preflight(workers_requested=0)
    transport = _SuccessTransport()
    results = dispatch_wave1(preflight, transport=transport)
    assert results == []
    assert transport.calls == []


# ---------------------------------------------------------------------------
# Per-worker outcome recording
# ---------------------------------------------------------------------------


def test_dispatch_wave1_success_per_worker() -> None:
    """N success transports -> N results, indices 0..N-1, status='success'."""
    preflight = _make_preflight(workers_requested=3)
    transport = _SuccessTransport()
    results = dispatch_wave1(preflight, transport=transport, prompt="hello")
    assert len(results) == 3
    assert [r.index for r in results] == [0, 1, 2]
    assert all(r.status == "success" for r in results)
    assert all(r.attempts == 1 for r in results)
    assert all(r.http_code == 200 for r in results)
    assert len(transport.calls) == 3
    # Prompt + timeout reach the transport verbatim.
    assert all(call == ("hello", 180) for call in transport.calls)


def test_dispatch_wave1_records_timeout_outcome() -> None:
    """``TimeoutError`` from transport -> ``WorkerResult(status='timeout')``."""
    preflight = _make_preflight(workers_requested=2)
    results = dispatch_wave1(preflight, transport=_TimeoutTransport())
    assert len(results) == 2
    assert all(r.status == "timeout" for r in results)
    assert [r.index for r in results] == [0, 1]
    assert all(r.attempts == 1 for r in results)
    # elapsed_ms is stamped by the dispatcher even when the transport
    # raised (so M5 reduce sees a non-zero wall-clock per slot).
    assert all(r.elapsed_ms >= 0 for r in results)


def test_dispatch_wave1_records_proxy_error_outcome() -> None:
    """Generic transport exception -> ``status='proxy_error'``."""
    preflight = _make_preflight(workers_requested=2)
    results = dispatch_wave1(preflight, transport=_ProxyErrorTransport())
    assert len(results) == 2
    assert all(r.status == "proxy_error" for r in results)
    assert [r.index for r in results] == [0, 1]
    assert all(r.attempts == 1 for r in results)


def test_dispatch_wave1_records_parse_error_outcome() -> None:
    """Transport returning ``parse_error`` survives unmodified.

    Wave-2 normalize (COMP-008, M4) owns §7.4 salvage promotion;
    dispatch must not rewrite the transport-returned status.
    """
    preflight = _make_preflight(workers_requested=2)
    results = dispatch_wave1(preflight, transport=_ParseErrorTransport())
    assert len(results) == 2
    assert all(r.status == "parse_error" for r in results)
    assert [r.index for r in results] == [0, 1]


def test_dispatch_wave1_records_mixed_outcomes_with_correct_indices() -> None:
    """Every slot's outcome is recorded at the matching slot index.

    Indices are positional, not call-order: even with concurrent
    fan-out, the returned list is sorted by ``index`` so a downstream
    Wave-3 reducer can rely on positional alignment with the requested
    worker slots.
    """
    preflight = _make_preflight(workers_requested=4)
    transport = _MixedTransport(
        statuses=["success", "timeout", "parse_error", "proxy_error"]
    )
    # max_workers=1 forces sequential dispatch so the slot->status
    # correspondence is deterministic for this assertion. The IMM-3
    # overlap test exercises the genuinely-parallel case separately.
    results = dispatch_wave1(
        preflight,
        transport=transport,
        parallel_executor=ParallelExecutor(max_workers=1),
    )
    assert [r.index for r in results] == [0, 1, 2, 3]
    assert [r.status for r in results] == [
        "success",
        "timeout",
        "parse_error",
        "proxy_error",
    ]


# ---------------------------------------------------------------------------
# Routing -- AC-004 / NFR-001 ParallelExecutor invocation mandate
# ---------------------------------------------------------------------------


def test_dispatch_wave1_routes_through_parallel_executor(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """AC-004: the injected ParallelExecutor.execute is the dispatch seam.

    Spy on ``ParallelExecutor.execute`` to prove dispatch goes through
    it. A future static-grep test (T03.15) covers the
    "no raw ``ThreadPoolExecutor()`` instantiation" half of the
    mandate; this test covers the "ParallelExecutor invocation site
    present" half.
    """
    preflight = _make_preflight(workers_requested=3)
    transport = _SuccessTransport()

    calls: dict[str, int] = {"plan": 0, "execute": 0}

    class _SpyExecutor(ParallelExecutor):
        def plan(self, tasks: Any) -> Any:  # type: ignore[override]
            calls["plan"] += 1
            return super().plan(tasks)

        def execute(self, plan: Any) -> Any:  # type: ignore[override]
            calls["execute"] += 1
            return super().execute(plan)

    results = dispatch_wave1(
        preflight,
        transport=transport,
        parallel_executor=_SpyExecutor(max_workers=3),
    )

    assert len(results) == 3
    assert calls["plan"] == 1, "dispatch should plan exactly once"
    assert calls["execute"] == 1, "dispatch should execute exactly once"


def test_dispatch_module_imports_parallel_executor() -> None:
    """AC-004: ``dispatch.py`` imports ``ParallelExecutor`` symbolically.

    Static guard against silent regressions: if a future refactor
    inlines a ``ThreadPoolExecutor`` the import goes away and this
    test fails before the runtime spy test would.
    """
    import superclaude.cli.swarm.dispatch as dispatch_mod

    assert hasattr(dispatch_mod, "ParallelExecutor"), (
        "dispatch.py must import ParallelExecutor (AC-004 / NFR-001)"
    )
    assert hasattr(dispatch_mod, "Task"), (
        "dispatch.py must import Task (ParallelExecutor task contract)"
    )


def test_dispatch_module_has_no_threadpool_executor_instantiation() -> None:
    """AC-004 static guard: ``dispatch.py`` body never instantiates TPE.

    Mirror of the grep validation in the tasklist; embedded here so
    the regression is caught in the unit suite without requiring a
    separate shell step. Allows the import line in
    ``superclaude.execution.parallel`` (which dispatch does NOT
    inline) but rejects any local ``ThreadPoolExecutor(`` token.
    """
    import inspect

    import superclaude.cli.swarm.dispatch as dispatch_mod

    source = inspect.getsource(dispatch_mod)
    assert "ThreadPoolExecutor(" not in source, (
        "dispatch.py must not instantiate ThreadPoolExecutor directly; "
        "route through ParallelExecutor (AC-004 / NFR-001)"
    )
