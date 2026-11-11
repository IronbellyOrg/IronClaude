"""The collector: one single-flight, bounded polling loop that publishes ``CycleResult`` (AD-6, AD-20).

It reads pages through one ``CycleSource``, parses them, merges them into the row set and
publishes one immutable result per cycle by replacing a single reference under a lock. It
reads time only from the injected clock and decides nothing about staleness.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Any, Protocol

from superclaude.cli.observe.adapter import SourceResult
from superclaude.cli.observe.parse import (
    Coverage,
    ParsedPage,
    ShapeError,
    Snapshot,
    apply_frozen,
    load_fixture,
    merge,
    parse_page,
)

INTERVAL = 15.0  # seconds between cycle starts
CYCLE_BUDGET = 15.0  # a cycle never runs longer than this
MAX_BACKOFF = 60.0  # after failures the wait doubles, never above this
JOIN_TIMEOUT = 5.0  # how long stop() waits for the polling thread


@dataclass(frozen=True)
class CycleResult:
    """Everything one cycle published. No STALE flag: ``view.py`` derives it from the clock."""

    cycle: int
    mode: str  # "fixture" | "live"
    fixture_variant: str | None
    state: str  # "NOT_POLLED" | "NOT_AVAILABLE" | "OK" | "FAILED" | "PARTIAL"
    code: (
        str | None
    )  # last SourceResult code, e.g. "timeout", "exit:2", "shape", "overrun"
    diagnostic: str  # sanitized, at most 2 KiB
    snapshot: Snapshot | None  # the last good merged row set
    coverage: Coverage | None  # coverage of the last cycle that read a page
    last_success_mono: float | None  # monotonic time of the last cycle that read a page
    last_success_wall: float | None  # wall time of the same moment (display only)
    namespace: str
    duration: float = 0.0  # monotonic seconds this cycle took


class CycleSource(Protocol):
    """What the collector needs from a source: ``LiveSource`` or ``FixtureSource``."""

    mode: str
    variant: str | None

    @property
    def available(self) -> bool: ...

    @property
    def namespace(self) -> str: ...

    def read_pages(
        self, clock: Any, budget_deadline: float, run_id: str | None = None
    ) -> SourceResult: ...


class FixtureSource:
    """Replays a fixture variant's cycles in order and repeats the last (never calls Orca)."""

    mode = "fixture"

    def __init__(self, variant: str) -> None:
        self.variant = variant
        self._fixture = load_fixture(variant)
        self._index = 0
        self.frozen_positions: frozenset = frozenset()  # of the cycle read last

    @property
    def available(self) -> bool:
        return True

    @property
    def namespace(self) -> str:
        return f"fixture:{self.variant}"

    def read_pages(
        self, clock: Any, budget_deadline: float, run_id: str | None = None
    ) -> SourceResult:
        entry = self._fixture.cycle(self._index)
        self._index += 1
        self.frozen_positions = entry.frozen
        if entry.envelope is None:
            return SourceResult("FAILED", code=entry.fail)
        return SourceResult("OK", pages=(entry.envelope,), calls=1)


class Collector:
    """Drives one source on a timer; ``latest()`` is the one published reference."""

    def __init__(
        self,
        source: CycleSource,
        clock: Any,
        interval: float = INTERVAL,
        budget: float = CYCLE_BUDGET,
        max_backoff: float = MAX_BACKOFF,
        run_id: str | None = None,
    ) -> None:
        self._source = source
        self._clock = clock
        self._interval = interval
        self._budget = budget
        self._max_backoff = max_backoff
        self._run_id = run_id
        self._wait = interval
        self._lock = threading.Lock()  # guards the published reference
        self._cycle_lock = threading.Lock()  # one cycle at a time
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._latest = CycleResult(
            cycle=0,
            mode=source.mode,
            fixture_variant=source.variant,
            state="NOT_POLLED",
            code=None,
            diagnostic="",
            snapshot=None,
            coverage=None,
            last_success_mono=None,
            last_success_wall=None,
            namespace="",
        )

    # -- publication -----------------------------------------------------------------------
    def latest(self) -> CycleResult:
        with self._lock:
            return self._latest

    def _publish(self, result: CycleResult) -> CycleResult:
        with self._lock:
            self._latest = result
        return result

    @property
    def next_interval(self) -> float:
        """Seconds to wait before the next cycle: the interval, doubled after failures."""
        return self._wait

    # -- one cycle -------------------------------------------------------------------------
    def run_once(self) -> CycleResult:
        """One synchronous cycle (used by ``--once``, by tests and by the polling thread)."""
        with self._cycle_lock:
            previous = self.latest()
            if not self._source.available:
                if previous.state == "NOT_AVAILABLE":
                    return previous
                return self._publish(
                    CycleResult(
                        cycle=previous.cycle + 1,
                        mode=previous.mode,
                        fixture_variant=previous.fixture_variant,
                        state="NOT_AVAILABLE",
                        code="not-found",
                        diagnostic="",
                        snapshot=None,
                        coverage=None,
                        last_success_mono=None,
                        last_success_wall=None,
                        namespace="",
                    )
                )
            number = previous.cycle + 1
            started = self._clock.monotonic()
            reply = self._source.read_pages(
                self._clock, started + self._budget, self._run_id
            )
            namespace = self._source.namespace
            pages: list[ParsedPage] = []
            error = reply.code if reply.state != "OK" else None
            base = 0
            frozen = getattr(self._source, "frozen_positions", frozenset())
            for raw in reply.pages:
                try:
                    parsed = parse_page(raw, namespace, number, base)
                except ShapeError:
                    error = "shape"  # a broken page ends the read; earlier pages still count
                    break
                pages.append(apply_frozen(parsed, frozen, base))
                base += parsed.raw_count
            duration = self._clock.monotonic() - started
            common: dict[str, Any] = {
                "cycle": number,
                "mode": previous.mode,
                "fixture_variant": previous.fixture_variant,
                "diagnostic": reply.diagnostic,
                "namespace": namespace,
                "duration": duration,
            }
            if not pages:
                # First page failed: the previous snapshot, coverage and last success stay.
                self._wait = min(self._wait * 2, self._max_backoff)
                return self._publish(
                    CycleResult(
                        state="FAILED",
                        code=error or "json",
                        snapshot=previous.snapshot,
                        coverage=previous.coverage,
                        last_success_mono=previous.last_success_mono,
                        last_success_wall=previous.last_success_wall,
                        **common,
                    )
                )
            snapshot, coverage = merge(
                previous.snapshot, pages, reply.capped, error, self._clock
            )
            self._wait = self._interval
            return self._publish(
                CycleResult(
                    state="PARTIAL" if coverage.partial else "OK",
                    code=error,
                    snapshot=snapshot,
                    coverage=coverage,
                    last_success_mono=self._clock.monotonic(),
                    last_success_wall=self._clock.wall(),
                    **common,
                )
            )

    # -- the polling thread --------------------------------------------------------------------
    def start(self) -> None:
        """Start the daemon polling thread (the ``OutputMonitor`` shape); safe to call twice."""
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._loop, name="observe-collector", daemon=True
        )
        self._thread.start()

    def _loop(self) -> None:
        while not self._stop.is_set():
            result = self.run_once()
            if result.state == "NOT_AVAILABLE":
                return  # no Orca CLI validated: no cycle ever starts
            if self._stop.wait(self.next_interval):
                return

    def stop(self) -> None:
        self._stop.set()
        thread = self._thread
        if thread is not None:
            thread.join(timeout=JOIN_TIMEOUT)
        self._thread = None
