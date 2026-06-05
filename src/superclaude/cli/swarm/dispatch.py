"""T03.02 -- COMP-007 Wave 1 dispatch orchestration.

``dispatch_wave1`` is the single Wave-1 entrypoint. It receives the
:class:`PreflightResult` from Wave 0 plus a :class:`Transport`
implementation and returns one :class:`WorkerResult` per worker
fanned out in the dispatch wave.

Threading semantics & ParallelExecutor contract (AC-004 / NFR-001)
==================================================================

The dispatch fan-out MUST route through
:class:`superclaude.execution.parallel.ParallelExecutor`. The swarm
package is forbidden from instantiating
``concurrent.futures.ThreadPoolExecutor`` directly (AC-004) -- every
parallel surface in swarm goes through ``ParallelExecutor`` so a
future cancellation / quota / scheduling layer has a single seam to
extend. The IMM-3 acceptance criterion ("N workers overlap in
wall-clock") is verified against the ``stub`` transport in
``tests/swarm/test_imm3_parallel.py``.

Retry / timeout matrix (FR-017, NFR-010, NFR-011) -- §7
=======================================================

:func:`retry_policy` wraps every transport call with the spec §7
retry matrix. The matrix is enforced exactly once per worker slot:

    +-----------------+----------------+----------------+-------------+
    | Outcome         | http_code      | Default retry? | attempts    |
    +=================+================+================+=============+
    | ``success``     | 200            | no             | 1           |
    +-----------------+----------------+----------------+-------------+
    | 4xx proxy_error | 400..499       | no             | 1           |
    +-----------------+----------------+----------------+-------------+
    | 5xx proxy_error | 500..599       | yes (once)     | 1 or 2      |
    +-----------------+----------------+----------------+-------------+
    | timeout         | None           | no             | 1           |
    +-----------------+----------------+----------------+-------------+
    | network/other   | None           | no             | 1           |
    +-----------------+----------------+----------------+-------------+
    | parse_error     | 200 (usually)  | no             | 1           |
    +-----------------+----------------+----------------+-------------+

The per-class retry flags are read from
:class:`superclaude.cli.swarm.models.RetryPolicy` carried on
:class:`WorkerSpec.retry`; defaults encode the §7 matrix
(``on_5xx=True`` / ``on_5xx_backoff_sec=2`` / ``on_4xx=False`` /
``on_timeout=False``). Network / "other" exceptions are treated as
``proxy_error`` with ``http_code=None`` and are never retried by
policy (there is no ``on_network`` flag; spec §7 lists "5xx-retry-once
+ 4xx-no-retry" as the only retry branch).

Per-worker hard timeout is :attr:`WorkerSpec.timeout_sec` (NFR-010
default 180s). The same value is forwarded to ``transport.send`` so
the transport's own httpx timeout matches the dispatcher's budget.

Per-worker outcome recording (FR-017 surface)
============================================

For each worker slot the dispatcher records the outcome into a
:class:`WorkerResult` whose ``status`` field is one of the four
values declared by :data:`WorkerStatus` (per §5 Result Contract
Schema, ``merged-requirements.compressed.compressed.md`` L395):

* ``success``      -- ``transport.send`` returned a ``WorkerResult``
                      and the result's own ``status`` survives. This
                      is the only branch where the transport's status
                      passes through verbatim; the dispatch layer
                      stamps slot-index / elapsed_ms but does not
                      rewrite the transport call.
* ``timeout``      -- ``transport.send`` raised :class:`TimeoutError`
                      (or any subclass thereof). Surfaces NFR-010 +
                      FR-017's "timeout" matrix branch. Recorded as a
                      synthetic ``WorkerResult`` because the transport
                      did not return one.
* ``parse_error``  -- transport returned a result with
                      ``status='parse_error'`` (e.g. body received but
                      JSON parse failed at the transport layer). The
                      §7.4 salvage promotion ``parse_error -> success``
                      is a Wave-2 normalize concern (COMP-008, M4) and
                      is not applied here.
* ``proxy_error``  -- ``transport.send`` raised any other exception
                      (transport / network / 5xx-after-retry). The
                      dispatch layer maps the exception to a synthetic
                      ``WorkerResult`` so callers see exactly one
                      WorkerResult per worker slot regardless of how
                      the call terminated.

The full retry/backoff matrix (FR-017, NFR-011) -- e.g. 5xx retried
exactly once with backoff -- lands in T03.09 (``retry_policy``).
T03.02 records the terminal outcome of a single attempt; the retry
loop wraps ``transport.send`` once T03.09 lands but the per-worker
outcome shape recorded here remains stable.

Behaviour when ``transport`` is ``None``
========================================

When no transport is supplied, :func:`dispatch_wave1` returns an
empty list. This is the test-only "wire-only" path -- callers that
only want to assert the preflight->dispatch handshake (e.g. the
T03.01 smoke test) pass ``transport=None`` so the dispatch wave
becomes a no-op while the wiring surface remains exercised. Real
runs (``swarm run`` against ``--transport stub`` or
``--transport openai_compat``) always supply a concrete
:class:`Transport` implementation.
"""

from __future__ import annotations

import time
from typing import Callable, Optional

from superclaude.cli.swarm.logging_ import Logger
from superclaude.cli.swarm.models import EventRecord, WorkerResult, WorkerSpec
from superclaude.cli.swarm.preflight import PreflightResult
from superclaude.cli.swarm.transports import Transport
from superclaude.execution.parallel import ParallelExecutor, Task


__all__ = ["dispatch_wave1", "retry_policy"]


# NFR-010 -- 180s per-worker timeout default. Mirrors
# ``WorkerSpec.timeout_sec`` so callers that don't supply a worker
# spec (e.g. legacy smoke paths) still honour the contract.
_DEFAULT_TIMEOUT_SEC = 180


def _classify_http_code(http_code: Optional[int]) -> str:
    """Bucket the transport-reported HTTP status for the §7 matrix.

    Returns one of ``"5xx"`` / ``"4xx"`` / ``"other"``. ``None``
    collapses into ``"other"`` -- network / connection failures land
    here because no transport status was observed.
    """
    if http_code is None:
        return "other"
    if 500 <= http_code <= 599:
        return "5xx"
    if 400 <= http_code <= 499:
        return "4xx"
    return "other"


def _send_once(
    transport: Transport,
    prompt: str,
    timeout_sec: int,
) -> WorkerResult:
    """Issue a single ``transport.send`` call; return one WorkerResult.

    Translates the three terminal forms the transport may take into a
    single :class:`WorkerResult` shape so :func:`retry_policy` can
    reason uniformly over the §7 matrix:

    * Returned ``WorkerResult`` -- passes through with ``attempts``
      forced to 1 and ``elapsed_ms`` backfilled from this attempt's
      wall-clock if the transport left it at the zero default.
    * Raised :class:`TimeoutError` -- converted to a synthetic
      ``status='timeout'`` result with ``http_code=None``.
    * Raised any other :class:`Exception` -- converted to a synthetic
      ``status='proxy_error'`` result with ``http_code=None``. This is
      the network-/connection-failure branch.

    The returned :attr:`WorkerResult.elapsed_ms` is the effective
    per-attempt elapsed (transport-supplied if non-zero, else the
    dispatcher's wall-clock backfill); :func:`retry_policy` sums these
    across attempts on the retry branch.
    """
    start = time.monotonic()
    try:
        result = transport.send(prompt, timeout_sec)
    except TimeoutError:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        return WorkerResult(
            status="timeout",
            http_code=None,
            attempts=1,
            elapsed_ms=elapsed_ms,
        )
    except Exception:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        return WorkerResult(
            status="proxy_error",
            http_code=None,
            attempts=1,
            elapsed_ms=elapsed_ms,
        )

    elapsed_ms = int((time.monotonic() - start) * 1000)
    result.attempts = 1
    if result.elapsed_ms == 0:
        result.elapsed_ms = elapsed_ms
    return result


def retry_policy(
    transport: Transport,
    prompt: str,
    spec: Optional[WorkerSpec] = None,
    *,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> WorkerResult:
    """Wrap ``transport.send`` with the §7 retry/timeout matrix.

    Implements FR-017 (per-worker timeout + retry policy), NFR-010
    (180s default timeout), and NFR-011 (5xx-once retry-with-backoff).
    The matrix is documented in the module docstring; the short form
    is: 200 → no retry; 4xx → no retry; 5xx → retry once with
    backoff; timeout → no retry; network/other → no retry. The
    per-class flags are read from ``spec.retry`` so callers can
    override (e.g. a debug lens that disables 5xx retry).

    Args:
        transport: a :class:`Transport` implementation. The call is
            issued exactly once on the no-retry branches and at most
            twice on the 5xx-retry branch.
        prompt: the fully-assembled prompt body forwarded verbatim to
            ``transport.send`` (the transport MUST NOT re-normalize per
            COMP-031).
        spec: optional :class:`WorkerSpec` carrying the
            :class:`~superclaude.cli.swarm.models.RetryPolicy` (FR-017
            flags + backoff) and ``timeout_sec`` (NFR-010 budget). When
            ``None`` the default :class:`WorkerSpec` is used, which
            encodes the §7 defaults verbatim (timeout=180s,
            on_5xx=True, on_5xx_backoff_sec=2, on_4xx=False,
            on_timeout=False).
        sleep_fn: backoff sleep injection. Defaults to
            :func:`time.sleep`; tests pass a recording stub so the
            matrix can be exercised deterministically.

    Returns:
        Exactly one :class:`WorkerResult` carrying the terminal
        outcome. ``attempts`` is 1 on every non-retry branch and 2 on
        the 5xx-retry branch (even when the second attempt itself is a
        5xx). ``elapsed_ms`` is the cumulative wall-clock across all
        attempts (backoff sleep is *not* included so the timing metric
        reflects transport work, not policy delay -- this matches the
        convention dispatch already uses for the single-attempt path).
        ``http_code`` survives from whichever attempt produced the
        terminal outcome.
    """
    if spec is None:
        spec = WorkerSpec()

    timeout_sec = spec.timeout_sec if spec.timeout_sec > 0 else _DEFAULT_TIMEOUT_SEC
    retry = spec.retry

    first = _send_once(transport, prompt, timeout_sec)

    should_retry = False
    if first.status == "proxy_error":
        bucket = _classify_http_code(first.http_code)
        if bucket == "5xx" and retry.on_5xx:
            should_retry = True
        elif bucket == "4xx" and retry.on_4xx:
            should_retry = True
        # ``other`` (no http_code -- network / connection failure)
        # is never retried by policy; spec §7 only lists 5xx-retry.
    elif first.status == "timeout" and retry.on_timeout:
        should_retry = True

    if not should_retry:
        return first

    # 5xx-once retry surface: sleep for the configured backoff, then
    # issue the second attempt. ``attempts`` is stamped to 2 and
    # ``elapsed_ms`` is the cumulative transport wall-clock across
    # both attempts (backoff itself is excluded -- it is policy
    # overhead, not transport work).
    backoff = max(0, retry.on_5xx_backoff_sec)
    if backoff > 0:
        sleep_fn(backoff)

    second = _send_once(transport, prompt, timeout_sec)
    second.attempts = 2
    second.elapsed_ms = first.elapsed_ms + second.elapsed_ms
    return second


def _run_worker(
    index: int,
    transport: Transport,
    prompt: str,
    spec: WorkerSpec,
    logger: Optional[Logger] = None,
) -> WorkerResult:
    """Run a single worker slot through :func:`retry_policy`.

    This is the per-task callable handed to ``ParallelExecutor``. It
    MUST NOT raise -- every terminal outcome (success / timeout /
    parse_error / proxy_error) is encoded into the returned
    :class:`WorkerResult`. The dispatch layer then collects the
    futures' results without needing exception handling at the
    fan-out site (ParallelExecutor records exceptions but loses the
    slot-index correspondence).

    When ``logger`` is supplied (T03.10 / FR-026), emits a paired
    ``worker_start`` / ``worker_done`` event for the slot. Logging is
    lock-coordinated inside :class:`Logger`, so concurrent workers
    cannot interleave bytes on either log surface.
    """
    if logger is not None:
        logger.log_event(
            EventRecord(
                event_type="worker_start",
                worker_index=index,
                payload={"timeout_sec": spec.timeout_sec},
            )
        )
    result = retry_policy(transport, prompt, spec)
    result.index = index
    if logger is not None:
        logger.log_event(
            EventRecord(
                event_type="worker_done",
                worker_index=index,
                payload={
                    "status": result.status,
                    "http_code": result.http_code,
                    "attempts": result.attempts,
                    "elapsed_ms": result.elapsed_ms,
                },
            )
        )
    return result


def dispatch_wave1(
    preflight_result: PreflightResult,
    transport: Optional[Transport] = None,
    *,
    prompt: str = "",
    parallel_executor: Optional[ParallelExecutor] = None,
    worker_spec: Optional[WorkerSpec] = None,
    logger: Optional[Logger] = None,
) -> list[WorkerResult]:
    """Fan ``prompt`` across N workers via ``ParallelExecutor``.

    AC-004 / NFR-001 compliance: dispatch routes through
    :class:`superclaude.execution.parallel.ParallelExecutor`; the
    swarm package never instantiates
    ``concurrent.futures.ThreadPoolExecutor`` directly. IMM-3
    parallelism is verified against the stub transport in
    ``tests/swarm/test_imm3_parallel.py``.

    Per-worker outcome recording: one :class:`WorkerResult` per
    worker slot, with ``status`` populated to one of
    ``success`` / ``timeout`` / ``parse_error`` / ``proxy_error``
    (see module docstring for the mapping). Slot ``index`` is stamped
    in 0..N-1 order; the returned list is sorted by ``index`` so
    callers can rely on positional correspondence with the requested
    worker slots.

    Args:
        preflight_result: the :class:`PreflightResult` returned by
            :func:`superclaude.cli.swarm.preflight.run_preflight`.
            ``preflight_result.manifest.preflight.workers_requested``
            drives the fan-out count.
        transport: a :class:`Transport` implementation
            (e.g. ``OpenAICompatTransport``, ``StubTransport``).
            When ``None`` the function returns an empty list -- this
            is the wire-only path used by the T03.01 smoke test;
            real runs always supply a transport.
        prompt: the fully-assembled prompt body to send. Passed
            verbatim to ``transport.send`` (the transport MUST NOT
            re-normalize per COMP-031). Defaults to an empty string
            so the wiring path can be exercised without the full M4
            prompt-assembly contract.
        parallel_executor: optional pre-configured
            :class:`ParallelExecutor` (tests inject a small
            ``max_workers`` to exercise queueing). When ``None`` a
            new executor is constructed sized to
            ``workers_requested`` so all slots can overlap.
        worker_spec: optional :class:`WorkerSpec` carrying
            ``timeout_sec`` (NFR-010) and the :class:`RetryPolicy`
            (FR-017 / NFR-011). Defaults to the §7 matrix.
        logger: optional :class:`~superclaude.cli.swarm.logging_.Logger`
            wired by the run command (T03.10 / FR-026). When supplied,
            dispatch emits one ``wave_transition`` event before the
            fan-out, paired ``worker_start`` / ``worker_done`` events
            per slot, and one closing ``wave_transition`` event into
            the dual JSONL + Markdown surfaces. When ``None`` dispatch
            is silent -- this keeps the wire-only path (T03.01 smoke)
            and unit tests free of log artefacts.

    Returns:
        A list of :class:`WorkerResult` instances sorted by
        ``index`` (0..N-1). Empty list when ``transport`` is ``None``
        or ``workers_requested == 0``.
    """
    if transport is None:
        return []

    workers_requested = preflight_result.manifest.preflight.workers_requested
    if workers_requested <= 0:
        return []

    # WorkerSpec carries both NFR-010 timeout and the FR-017 / NFR-011
    # retry sub-policy; default encodes the §7 matrix verbatim so the
    # legacy smoke path (no spec supplied) still matches the contract.
    effective_spec = worker_spec if worker_spec is not None else WorkerSpec()

    # Size the executor to the worker count so every slot can overlap
    # in wall-clock (IMM-3). Tests that want to exercise queueing
    # inject their own ParallelExecutor with a smaller max_workers.
    executor = parallel_executor or ParallelExecutor(max_workers=workers_requested)

    # T03.10 / FR-026 -- coarse wave_transition events bracket the
    # per-worker stream so operators tailing ``execution-log.md`` see
    # the wave boundaries without parsing JSONL. Logging is opt-in;
    # the wire-only callers (T03.01 smoke, dispatch unit tests) pass
    # ``logger=None`` and the dispatch path stays silent.
    if logger is not None:
        logger.log_event(
            EventRecord(
                event_type="wave_transition",
                payload={
                    "from": preflight_result.state.state,
                    "to": "dispatching",
                    "workers_requested": workers_requested,
                },
            )
        )

    def _make_callable(slot_index: int):
        # Default-arg binding captures slot_index per task (avoids the
        # late-binding closure trap that would collapse every task
        # onto the loop's terminal value).
        def _call() -> WorkerResult:
            return _run_worker(slot_index, transport, prompt, effective_spec, logger)

        return _call

    tasks = [
        Task(
            id=f"worker-{index:02d}",
            description=f"swarm worker slot {index}",
            execute=_make_callable(index),
            depends_on=[],
        )
        for index in range(workers_requested)
    ]

    plan = executor.plan(tasks)
    raw_results = executor.execute(plan)

    # ParallelExecutor returns Dict[task.id -> WorkerResult]. Re-key
    # by slot index so the returned list is positionally aligned
    # with the requested worker slots. A None entry would indicate
    # an unexpected exception escaped _run_worker -- guard against
    # that by synthesising a proxy_error outcome so the per-worker
    # invariant (exactly one WorkerResult per slot) holds even under
    # contract violation.
    results: list[WorkerResult] = []
    for index in range(workers_requested):
        outcome = raw_results.get(f"worker-{index:02d}")
        if isinstance(outcome, WorkerResult):
            results.append(outcome)
        else:
            results.append(
                WorkerResult(index=index, status="proxy_error", attempts=1)
            )

    # T03.10 -- closing wave_transition. M4 normalize / M5 reduce will
    # stamp their own transitions; dispatch closes its own wave so the
    # event stream remains linearizable across phases.
    if logger is not None:
        success_count = sum(1 for r in results if r.status == "success")
        logger.log_event(
            EventRecord(
                event_type="wave_transition",
                payload={
                    "from": "dispatching",
                    "to": "dispatched",
                    "results_collected": len(results),
                    "success_count": success_count,
                },
            )
        )
    return results
