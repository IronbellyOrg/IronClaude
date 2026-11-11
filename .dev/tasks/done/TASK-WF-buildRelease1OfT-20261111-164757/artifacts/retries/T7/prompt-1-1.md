ae0f4ffa905d631877757f8ae850d56d25f87af6
Review one task for spec compliance.

Task brief: 
## Task 7: Build the collector `collector.py`

Depends on: Task 5, Task 6

Create `src/superclaude/cli/observe/collector.py` and `tests/observe/test_collector.py`, following `ARCHITECTURE-SPINE.md` AD-6 and AD-20 and the "Bounds per cycle" section of `adapter-contract.md`. Define the frozen `CycleResult` (cycle number, `mode` `fixture` or `live`, fixture variant, last `SourceResult` code, the merged `Snapshot` and `Coverage`, `last_success_mono`, `last_success_wall`, `source.namespace`, and no STALE flag), the `CycleSource` protocol with `FixtureSource(variant)` here (replays the fixture cycles in order and repeats the last; a `{"fail": code}` cycle becomes a failed `SourceResult`) and `LiveSource` from Task 6, and `Collector(source, clock)` with `start()` (one daemon thread waiting on a `threading.Event`, the shape of `OutputMonitor` in `src/superclaude/cli/sprint/monitor.py`), `latest()`, `run_once()` and `stop()`. Rules: publish a `NOT_POLLED` result before the first poll and a `NOT_AVAILABLE` result when discovery returns `None`; one cycle at a time, never overlapping; interval and cycle budget 15 s; after a failed cycle back off by doubling (PROPOSED) to a maximum of 60 s and return to 15 s after a success; each cycle reads pages through the source, parses them with `parse.parse_page`, calls `parse.merge` only when at least one page was read (a first-page failure keeps the previous `Snapshot`), and publishes one immutable `CycleResult` by replacing one reference under a lock; an overrunning cycle is cut at the budget, ends with code `overrun`, is `PARTIAL` if earlier pages were read and `FAILED` otherwise; the collector reads time only from the injected clock and computes no staleness; no LLM is called.

Acceptance criteria:
- [T7.AC1] `uv run pytest tests/observe/test_collector.py -v` passes.
- [T7.AC2] T4: with a fake runner that always says `hasMore=true`, one cycle stops at the 5-call cap and the published coverage is `PARTIAL` with 500 rows collected.
- [T7.AC3] T5: a fake runner that exceeds the injected per-call timeout gives code `timeout` and the cycle ends within the 15 s budget on the fake monotonic clock.
- [T7.AC4] T40: on a fake monotonic clock, backoff doubles and never exceeds 60 s, resets after a success, and an overrunning call is cut with code `overrun`; wall-clock jumps change nothing the collector records for staleness.
- [T7.AC5] A test shows a failed first-page cycle keeps the previous `Snapshot` and `last_success_*`, and a failed second page keeps the rows already read.
- [T7.AC6] A test shows two threads reading `latest()` while cycles publish never see a half-built result, and `start()` followed by `stop()` leaves no live thread.
- [T7.AC7] A test shows `FixtureSource("source-loss")` publishes failing cycles that keep the last good snapshot.

Global constraints: 
## Constraints

- Shorthand used in the tasks below. SPECDIR is `.dev/issues/409/bmad/spec-orca-observer/`; it holds the canonical contract: `SPEC.md` and its companions `ARCHITECTURE-SPINE.md` (decisions AD-1 to AD-20 and conditional decisions CD-1 to CD-16), `adapter-contract.md`, `rendering-rules.md`, `acceptance-tests.md` (tests T1 to T51), `release-gates.md`, `snapshot-export-schema.md` and `unverified-register.md`. SNAPSRC is `.dev/issues/409/tuibbs-review/architecture-options.md` (last section, the frozen snapshot fields). The package is `src/superclaude/cli/observe/` and its tests are `tests/observe/`. Where SPECDIR and the older `.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md` differ, SPECDIR wins.
- Scope is release 1 (R1: live `worker-list`, COUNTS and freshness strips, worker ledger with the verbatim `projection.nextAction.kind` column, capped paging, STALE after 45 s, changes since last look, the one-line question-source notice, the JSON snapshot) plus the offline R0 pieces R1 needs (key-reader spike, sanitizer, cell-width truncation, NO_COLOR and ASCII, fixture variants, text export, fixture mode). The owner chose the staged direction and confirmed Python + Rich with snapshot export in `.dev/issues/409/owner-decisions-20261108.md` (items 1 and 5), so the side-by-side R0 renders of the Attention Ledger and Decision Desk that were only input to that choice are not built.
- Out of scope, not built even as stubs: question rows and any `check`, `inbox` or message read (R2), the SEEN IS NOT RESOLVED and RETAIN CONTEXT panels, the Decision Desk (R3), `--include-remote` (R4), every write path into Orca (approve, retry, terminate, spawn, merge, reply, instruct), persisting the last-look baseline, the `read k of N Runs since start` header token and its collector counters (CD-10 default places it in the Attention Ledger header only), any Go or TUIBBS code, and moving `_find_orca()`.
- Acceptance tests not built because they serve only the excluded views: T7, T10, T17, T19, T45, T46, T50 and T51, and the question half of T12 and T47. Every other test in `acceptance-tests.md` that applies to the ledger view is mapped to a task below, plus the snapshot schema test (no ID assigned in the spec).
- Authorization evidence. The owner's message of 2026-11-11, "Proceed with building the first release", is taken as the go for R0 and R1, including registering `superclaude observe` (reading 1 of "production integration" in `release-gates.md`) and live read-only `worker-list` calls. Caveat: `release-gates.md` says the owner's own dated selection record (check AC-S) states the confirmed reading and the direction. No task here writes that record, and it stays a reviewer-checked item. The final report must say it was not seen.
- Live Orca calls. Only two kinds are ever made, both read-only, both through `adapter.py`: `worker-list --json --limit 100` polling (optional `--run <runId>`, optional `--cursor <value>`, no shell) and the one startup discovery through `_find_orca()` in `src/superclaude/cli/install_user_setup.py` (runs `skills list --json`, at most two candidates, 10 s each, once per process, outside the 15 s cycle budget and the 5-call cap). No key maps to an Orca call. The forbidden set (plain `check`, `--ack`, `--wait`, `--retry-request`, `dispatch`, `inbox`, any other verb) is checked before every call and is never shortened.
- Defaults taken for open owner questions (SPECDIR `ARCHITECTURE-SPINE.md` CD table), changeable by the owner: CD-2 change flags use `stage.worker`, `stage.dispatch`, `nextAction.kind`, `liveness.verdict` and `stage.detail` and `stage.activity` stay inspector-only; CD-3 snapshot rows use timestamp order; CD-4 only the spec-fixed height rules; CD-5 truncation glyph `>`; CD-6 `--once` prints the record text to stdout, `--snapshot PATH` sets the snapshot file, the default directory is `~/.local/state/superclaude/observe/`, files are 0600 and replaced atomically; CD-8 empty palette (plain text, meaning in words); CD-16 a ledger row does not name a shared `worktreeId`.
- Plan-author rules that close gaps in the spec (PROPOSED, the owner may change them). The state directory honours `XDG_STATE_HOME` when set so tests stay out of the real home folder. `--once` with a live source writes a snapshot only when `--snapshot` is given. Fixture mode (`--fixture <variant>`) never calls Orca and never writes a snapshot unless `--snapshot` is given. A failed key-reader spike blocks the interactive tasks and is reported to the owner; the Textual switch in AD-14 is applied only on the owner's say-so, and both toolkits are never built.
- Data handling. Raw Orca output is never logged, committed, or kept in fixtures; committed fixtures hold only redacted identifiers (no absolute path, terminal handle, token or credential). Worker free text (`stage.detail`, `stage.activity`) and failed-poll stderr are shown after control-character sanitizing, labelled `worker-reported`; they are not redacted and no credential or terminal-handle field is exported.
- No code is copied from TUIBBS-scp (AGPL-3.0); the design prototype `canvas.py` is never imported. Python 3.10 compatible, no new dependency (`rich`, `click`, `jsonschema` and `pexpect` are already dependencies in `pyproject.toml`), UV only (`uv run pytest tests/observe -v`, `uv run ruff check src/superclaude/cli/observe tests/observe`), and nothing is written under `.claude/`. Every task leaves ruff clean for the files it touches.
- A fact the source does not give is the single `UNKNOWN` sentinel (never `None`, `0`, `False`, `""`) and renders as the word `unknown`. Facts with no verified source render `unavailable (no source)`. Worker text always renders as literal text, never parsed as Rich markup.

Start sha: ae0f4ffa905d631877757f8ae850d56d25f87af6
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/observe/adapter.py b/src/superclaude/cli/observe/adapter.py
index cc54811dc..012d15d8c 100644
--- a/src/superclaude/cli/observe/adapter.py
+++ b/src/superclaude/cli/observe/adapter.py
@@ -293,6 +293,7 @@ class LiveSource:
     """Pages through ``worker-list`` for one cycle, within the call cap and the time budget."""
 
     mode = "live"
+    variant = None  # only fixture sources have a variant
 
     def __init__(
         self,
diff --git a/src/superclaude/cli/observe/collector.py b/src/superclaude/cli/observe/collector.py
new file mode 100644
index 000000000..9e92cf2dd
--- /dev/null
+++ b/src/superclaude/cli/observe/collector.py
@@ -0,0 +1,255 @@
+"""The collector: one single-flight, bounded polling loop that publishes ``CycleResult`` (AD-6, AD-20).
+
+It reads pages through one ``CycleSource``, parses them, merges them into the row set and
+publishes one immutable result per cycle by replacing a single reference under a lock. It
+reads time only from the injected clock and decides nothing about staleness.
+"""
+
+from __future__ import annotations
+
+import threading
+from dataclasses import dataclass
+from typing import Any, Protocol
+
+from superclaude.cli.observe.adapter import SourceResult
+from superclaude.cli.observe.parse import (
+    Coverage,
+    ParsedPage,
+    ShapeError,
+    Snapshot,
+    apply_frozen,
+    load_fixture,
+    merge,
+    parse_page,
+)
+
+INTERVAL = 15.0  # seconds between cycle starts
+CYCLE_BUDGET = 15.0  # a cycle never runs longer than this
+MAX_BACKOFF = 60.0  # after failures the wait doubles, never above this
+JOIN_TIMEOUT = 5.0  # how long stop() waits for the polling thread
+
+
+@dataclass(frozen=True)
+class CycleResult:
+    """Everything one cycle published. No STALE flag: ``view.py`` derives it from the clock."""
+
+    cycle: int
+    mode: str  # "fixture" | "live"
+    fixture_variant: str | None
+    state: str  # "NOT_POLLED" | "NOT_AVAILABLE" | "OK" | "FAILED" | "PARTIAL"
+    code: (
+        str | None
+    )  # last SourceResult code, e.g. "timeout", "exit:2", "shape", "overrun"
+    diagnostic: str  # sanitized, at most 2 KiB
+    snapshot: Snapshot | None  # the last good merged row set
+    coverage: Coverage | None  # coverage of the last cycle that read a page
+    last_success_mono: float | None  # monotonic time of the last cycle that read a page
+    last_success_wall: float | None  # wall time of the same moment (display only)
+    namespace: str
+    duration: float = 0.0  # monotonic seconds this cycle took
+
+
+class CycleSource(Protocol):
+    """What the collector needs from a source: ``LiveSource`` or ``FixtureSource``."""
+
+    mode: str
+    variant: str | None
+
+    @property
+    def available(self) -> bool: ...
+
+    @property
+    def namespace(self) -> str: ...
+
+    def read_pages(
+        self, clock: Any, budget_deadline: float, run_id: str | None = None
+    ) -> SourceResult: ...
+
+
+class FixtureSource:
+    """Replays a fixture variant's cycles in order and repeats the last (never calls Orca)."""
+
+    mode = "fixture"
+
+    def __init__(self, variant: str) -> None:
+        self.variant = variant
+        self._fixture = load_fixture(variant)
+        self._index = 0
+        self.frozen_positions: frozenset = frozenset()  # of the cycle read last
+
+    @property
+    def available(self) -> bool:
+        return True
+
+    @property
+    def namespace(self) -> str:
+        return f"fixture:{self.variant}"
+
+    def read_pages(
+        self, clock: Any, budget_deadline: float, run_id: str | None = None
+    ) -> SourceResult:
+        entry = self._fixture.cycle(self._index)
+        self._index += 1
+        self.frozen_positions = entry.frozen
+        if entry.envelope is None:
+            return SourceResult("FAILED", code=entry.fail)
+        return SourceResult("OK", pages=(entry.envelope,), calls=1)
+
+
+class Collector:
+    """Drives one source on a timer; ``latest()`` is the one published reference."""
+
+    def __init__(
+        self,
+        source: CycleSource,
+        clock: Any,
+        interval: float = INTERVAL,
+        budget: float = CYCLE_BUDGET,
+        max_backoff: float = MAX_BACKOFF,
+        run_id: str | None = None,
+    ) -> None:
+        self._source = source
+        self._clock = clock
+        self._interval = interval
+        self._budget = budget
+        self._max_backoff = max_backoff
+        self._run_id = run_id
+        self._wait = interval
+        self._lock = threading.Lock()  # guards the published reference
+        self._cycle_lock = threading.Lock()  # one cycle at a time
+        self._stop = threading.Event()
+        self._thread: threading.Thread | None = None
+        self._latest = CycleResult(
+            cycle=0,
+            mode=source.mode,
+            fixture_variant=source.variant,
+            state="NOT_POLLED",
+            code=None,
+            diagnostic="",
+            snapshot=None,
+            coverage=None,
+            last_success_mono=None,
+            last_success_wall=None,
+            namespace="",
+        )
+
+    # -- publication -----------------------------------------------------------------------
+    def latest(self) -> CycleResult:
+        with self._lock:
+            return self._latest
+
+    def _publish(self, result: CycleResult) -> CycleResult:
+        with self._lock:
+            self._latest = result
+        return result
+
+    @property
+    def next_interval(self) -> float:
+        """Seconds to wait before the next cycle: the interval, doubled after failures."""
+        return self._wait
+
+    # -- one cycle -------------------------------------------------------------------------
+    def run_once(self) -> CycleResult:
+        """One synchronous cycle (used by ``--once``, by tests and by the polling thread)."""
+        with self._cycle_lock:
+            previous = self.latest()
+            if not self._source.available:
+                if previous.state == "NOT_AVAILABLE":
+                    return previous
+                return self._publish(
+                    CycleResult(
+                        cycle=previous.cycle + 1,
+                        mode=previous.mode,
+                        fixture_variant=previous.fixture_variant,
+                        state="NOT_AVAILABLE",
+                        code="not-found",
+                        diagnostic="",
+                        snapshot=None,
+                        coverage=None,
+                        last_success_mono=None,
+                        last_success_wall=None,
+                        namespace="",
+                    )
+                )
+            number = previous.cycle + 1
+            started = self._clock.monotonic()
+            reply = self._source.read_pages(
+                self._clock, started + self._budget, self._run_id
+            )
+            namespace = self._source.namespace
+            pages: list[ParsedPage] = []
+            error = reply.code if reply.state != "OK" else None
+            base = 0
+            frozen = getattr(self._source, "frozen_positions", frozenset())
+            for raw in reply.pages:
+                try:
+                    parsed = parse_page(raw, namespace, number, base)
+                except ShapeError:
+                    error = "shape"  # a broken page ends the read; earlier pages still count
+                    break
+                pages.append(apply_frozen(parsed, frozen, base))
+                base += parsed.raw_count
+            duration = self._clock.monotonic() - started
+            common: dict[str, Any] = {
+                "cycle": number,
+                "mode": previous.mode,
+                "fixture_variant": previous.fixture_variant,
+                "diagnostic": reply.diagnostic,
+                "namespace": namespace,
+                "duration": duration,
+            }
+            if not pages:
+                # First page failed: the previous snapshot, coverage and last success stay.
+                self._wait = min(self._wait * 2, self._max_backoff)
+                return self._publish(
+                    CycleResult(
+                        state="FAILED",
+                        code=error or "json",
+                        snapshot=previous.snapshot,
+                        coverage=previous.coverage,
+                        last_success_mono=previous.last_success_mono,
+                        last_success_wall=previous.last_success_wall,
+                        **common,
+                    )
+                )
+            snapshot, coverage = merge(
+                previous.snapshot, pages, reply.capped, error, self._clock
+            )
+            self._wait = self._interval
+            return self._publish(
+                CycleResult(
+                    state="PARTIAL" if coverage.partial else "OK",
+                    code=error,
+                    snapshot=snapshot,
+                    coverage=coverage,
+                    last_success_mono=self._clock.monotonic(),
+                    last_success_wall=self._clock.wall(),
+                    **common,
+                )
+            )
+
+    # -- the polling thread --------------------------------------------------------------------
+    def start(self) -> None:
+        """Start the daemon polling thread (the ``OutputMonitor`` shape); safe to call twice."""
+        if self._thread is not None and self._thread.is_alive():
+            return
+        self._stop.clear()
+        self._thread = threading.Thread(
+            target=self._loop, name="observe-collector", daemon=True
+        )
+        self._thread.start()
+
+    def _loop(self) -> None:
+        while not self._stop.is_set():
+            result = self.run_once()
+            if result.state == "NOT_AVAILABLE":
+                return  # no Orca CLI validated: no cycle ever starts
+            if self._stop.wait(self.next_interval):
+                return
+
+    def stop(self) -> None:
+        self._stop.set()
+        thread = self._thread
+        if thread is not None:
+            thread.join(timeout=JOIN_TIMEOUT)
+        self._thread = None
diff --git a/src/superclaude/cli/observe/parse.py b/src/superclaude/cli/observe/parse.py
index f50dca53a..d4f29ca38 100644
--- a/src/superclaude/cli/observe/parse.py
+++ b/src/superclaude/cli/observe/parse.py
@@ -586,15 +586,22 @@ class Fixture:
                 f"fixture cycle {index} is a failure ({entry.fail}), it has no page"
             )
         parsed = parse_page(entry.envelope, namespace, cycle, source_rank_base)
-        if not entry.frozen:
-            return parsed
-        rows = tuple(
-            replace(row, fixture_frozen=True)
-            if row.source_rank - source_rank_base in entry.frozen
-            else row
-            for row in parsed.rows
-        )
-        return replace(parsed, rows=rows)
+        return apply_frozen(parsed, entry.frozen, source_rank_base)
+
+
+def apply_frozen(
+    parsed: ParsedPage, frozen: frozenset, source_rank_base: int = 0
+) -> ParsedPage:
+    """Set ``fixture_frozen`` on the rows at the given raw positions (fixture mode only)."""
+    if not frozen:
+        return parsed
+    rows = tuple(
+        replace(row, fixture_frozen=True)
+        if row.source_rank - source_rank_base in frozen
+        else row
+        for row in parsed.rows
+    )
+    return replace(parsed, rows=rows)
 
 
 def load_fixture(variant: str) -> Fixture:
diff --git a/tests/observe/test_collector.py b/tests/observe/test_collector.py
new file mode 100644
index 000000000..5782a379e
--- /dev/null
+++ b/tests/observe/test_collector.py
@@ -0,0 +1,420 @@
+"""Collector tests (AD-6, AD-20; T4, T5, T40 in acceptance-tests.md)."""
+
+from __future__ import annotations
+
+import dataclasses
+import json
+import re
+import threading
+import time
+from pathlib import Path
+
+import pytest
+
+import superclaude.cli.observe.collector as collector_module
+from superclaude.cli.observe.adapter import LiveSource
+from superclaude.cli.observe.collector import Collector, CycleResult, FixtureSource
+from tests.observe.conftest import FakeDiscover, FakeRunner, make_envelope, make_rows
+
+ORCA = "/opt/fake/orca"
+
+
+def reply(n=2, has_more=False, cursor=None, total=None, tag="a"):
+    rows = make_rows(n, 1)
+    for i, row in enumerate(rows):
+        row["dispatchId"] = f"w-{tag}-{i:03d}"
+    envelope = make_envelope(rows, total=total, has_more=has_more)
+    if cursor is not None:
+        envelope["result"]["page"]["nextCursor"] = cursor
+    return 0, json.dumps(envelope)
+
+
+def live(responses, clock, argv_log, path=ORCA, **kw):
+    runner = FakeRunner(argv_log, responses)
+    discover = FakeDiscover(argv_log, path)
+    return Collector(LiveSource(runner, discover), clock, **kw), runner, discover
+
+
+# -- before the first poll, and no Orca ----------------------------------------------------------
+
+
+def test_a_not_polled_result_exists_before_the_first_poll(fake_clock, argv_log):
+    collector, runner, _ = live([reply()], fake_clock, argv_log)
+    result = collector.latest()
+    assert (result.cycle, result.state, result.mode) == (0, "NOT_POLLED", "live")
+    assert (
+        result.snapshot is None
+        and result.coverage is None
+        and result.last_success_mono is None
+    )
+    assert runner.calls == 0
+    assert {f.name for f in dataclasses.fields(CycleResult)}.isdisjoint(
+        {"stale", "is_stale"}
+    )
+
+
+def test_discovery_none_publishes_not_available_and_starts_no_cycle(
+    fake_clock, argv_log
+):
+    collector, runner, discover = live([reply()], fake_clock, argv_log, path=None)
+    first = collector.run_once()
+    assert (first.state, first.cycle, first.code) == ("NOT_AVAILABLE", 1, "not-found")
+    assert collector.run_once() is first and collector.run_once() is first
+    assert runner.calls == 0 and discover.calls == 1
+
+
+def test_the_thread_stops_by_itself_when_no_orca_is_available(fake_clock, argv_log):
+    collector, runner, _ = live(
+        [reply()], fake_clock, argv_log, path=None, interval=0.01
+    )
+    collector.start()
+    wait_until(lambda: collector.latest().state == "NOT_AVAILABLE")
+    wait_until(
+        lambda: not any(t.name == "observe-collector" for t in threading.enumerate())
+    )
+    collector.stop()
+    assert runner.calls == 0
+
+
+def wait_until(predicate, timeout=5.0):
+    end = time.monotonic() + timeout
+    while time.monotonic() < end:
+        if predicate():
+            return
+        time.sleep(0.005)
+    raise AssertionError("condition not reached")
+
+
+# -- T4: the call cap ------------------------------------------------------------------------------
+
+
+def test_a_source_that_always_has_more_stops_at_the_cap_with_500_rows(
+    fake_clock, argv_log
+):
+    counter = {"n": 0}
+
+    def always_more(argv, timeout):
+        counter["n"] += 1
+        return reply(100, True, f"c{counter['n']}", 9999, tag=str(counter["n"]))
+
+    collector, runner, _ = live([always_more], fake_clock, argv_log)
+    result = collector.run_once()
+    assert runner.calls == 5
+    assert (result.state, result.code, result.cycle) == ("PARTIAL", None, 1)
+    assert (
+        result.coverage.partial
+        and result.coverage.stopped_by_cap
+        and result.coverage.has_more_at_stop
+    )
+    assert result.coverage.collected == 500 and len(result.snapshot.rows) == 500
+    assert result.coverage.reported_total == 9999
+
+
+# -- T5 and T40: time ----------------------------------------------------------------------------------
+
+
+def test_a_call_that_exceeds_the_per_call_timeout_is_code_timeout_within_the_budget(
+    fake_clock, argv_log
+):
+    def too_slow(argv, timeout):
+        fake_clock.advance(
+            timeout
+        )  # the fake "sleeps" past the injected per-call timeout
+        raise TimeoutError("slow")
+
+    collector, runner, _ = live([too_slow], fake_clock, argv_log)
+    result = collector.run_once()
+    assert (result.state, result.code) == ("FAILED", "timeout")
+    assert runner.timeouts == [10.0] and result.duration == 10.0 <= 15.0
+
+
+def test_backoff_doubles_to_sixty_and_resets_after_a_success(fake_clock, argv_log):
+    collector, _, _ = live(
+        [(2, ""), (2, ""), (2, ""), (2, ""), reply(), (2, "")], fake_clock, argv_log
+    )
+    assert collector.next_interval == 15.0
+    seen = []
+    for _ in range(4):
+        assert collector.run_once().state == "FAILED"
+        seen.append(collector.next_interval)
+    assert seen == [30.0, 60.0, 60.0, 60.0]
+    assert collector.run_once().state == "OK" and collector.next_interval == 15.0
+    assert collector.run_once().state == "FAILED" and collector.next_interval == 30.0
+
+
+def test_an_overrunning_call_is_cut_at_the_budget_with_code_overrun(
+    fake_clock, argv_log
+):
+    def first_page(argv, timeout):
+        fake_clock.advance(12)
+        return reply(2, True, "c1", 9)
+
+    def second_page(argv, timeout):
+        assert (
+            timeout == 3.0
+        )  # the time left in the 15 s budget, not the 10 s call limit
+        fake_clock.advance(timeout)
+        raise TimeoutError("cut")
+
+    collector, runner, _ = live([first_page, second_page], fake_clock, argv_log)
+    result = collector.run_once()
+    assert (result.state, result.code, result.duration) == ("PARTIAL", "overrun", 15.0)
+    assert (
+        result.coverage.stopped_by_error == "overrun" and result.coverage.collected == 2
+    )
+    assert runner.calls == 2
+
+
+def test_wall_clock_jumps_change_nothing_recorded_for_staleness(fake_clock, argv_log):
+    collector, _, _ = live([reply(), (2, "")], fake_clock, argv_log)
+    ok = collector.run_once()
+    mono, wall = ok.last_success_mono, ok.last_success_wall
+    fake_clock.jump_wall(-7200)
+    fake_clock.advance(20)
+    failed = collector.run_once()
+    assert failed.state == "FAILED"
+    assert (failed.last_success_mono, failed.last_success_wall) == (mono, wall)
+    assert (
+        mono == 1000.0
+    )  # the fake monotonic clock's start: nothing wall-based leaked in
+
+
+# -- failures keep what was read ----------------------------------------------------------------------------
+
+
+def test_a_failed_first_page_keeps_the_previous_snapshot_and_last_success(
+    fake_clock, argv_log
+):
+    collector, _, _ = live([reply(3), (2, "", "boom")], fake_clock, argv_log)
+    good = collector.run_once()
+    fake_clock.advance(15)
+    bad = collector.run_once()
+    assert (bad.state, bad.code, bad.cycle, bad.diagnostic) == (
+        "FAILED",
+        "exit:2",
+        2,
+        "boom",
+    )
+    assert bad.snapshot is good.snapshot and bad.coverage is good.coverage
+    assert bad.last_success_mono == good.last_success_mono == 1000.0
+
+
+def test_a_failed_second_page_keeps_the_rows_already_read(fake_clock, argv_log):
+    collector, _, _ = live(
+        [reply(2, True, "c1", 9), (3, "", "late")], fake_clock, argv_log
+    )
+    result = collector.run_once()
+    assert (result.state, result.code) == ("PARTIAL", "exit:3")
+    assert (
+        result.coverage.stopped_by_error == "exit:3" and len(result.snapshot.rows) == 2
+    )
+    assert result.last_success_mono is not None
+
+
+def test_a_shape_error_on_the_first_page_is_failed_and_on_a_later_page_partial(
+    fake_clock, argv_log
+):
+    broken = (0, json.dumps({"result": {"workers": "x", "page": {"hasMore": False}}}))
+    collector, _, _ = live([reply(2), broken], fake_clock, argv_log)
+    good = collector.run_once()
+    bad = collector.run_once()
+    assert (bad.state, bad.code) == (
+        "FAILED",
+        "shape",
+    ) and bad.snapshot is good.snapshot
+    collector, _, _ = live([reply(2, True, "c1", 9), broken], fake_clock, argv_log)
+    result = collector.run_once()
+    assert (result.state, result.code, len(result.snapshot.rows)) == (
+        "PARTIAL",
+        "shape",
+        2,
+    )
+
+
+def test_rows_not_returned_by_the_next_cycle_stay_not_reobserved(fake_clock, argv_log):
+    collector, _, _ = live([reply(3, tag="a"), reply(2, tag="b")], fake_clock, argv_log)
+    collector.run_once()
+    second = collector.run_once()
+    assert len(second.snapshot.rows) == 5
+    assert sum(1 for r in second.snapshot.rows if not r.reobserved) == 3
+
+
+# -- publication and the thread -----------------------------------------------------------------------------
+
+
+def test_readers_never_see_a_half_built_result_while_cycles_publish(
+    fake_clock, argv_log
+):
+    counter = {"n": 0}
+
+    def varying(argv, timeout):
+        counter["n"] += 1
+        return reply(5 + counter["n"] % 3, False, None, None, tag=str(counter["n"]))
+
+    collector, _, _ = live([varying], fake_clock, argv_log)
+    stop = threading.Event()
+    problems: list[str] = []
+
+    def reader():
+        last = 0
+        while not stop.is_set():
+            result = collector.latest()
+            if result.cycle < last:
+                problems.append("cycle went backwards")
+            last = result.cycle
+            if result.state == "OK" and (
+                result.snapshot is None
+                or result.snapshot.cycle != result.cycle
+                or result.coverage is None
+                or result.coverage.collected
+                != sum(1 for r in result.snapshot.rows if r.cycle == result.cycle)
+            ):
+                problems.append(f"inconsistent result at cycle {result.cycle}")
+
+    threads = [threading.Thread(target=reader) for _ in range(2)]
+    for t in threads:
+        t.start()
+    for _ in range(200):
+        collector.run_once()
+    stop.set()
+    for t in threads:
+        t.join(timeout=5)
+    assert problems == [] and collector.latest().cycle == 200
+
+
+def test_start_then_stop_leaves_no_live_thread(fake_clock, argv_log):
+    collector, runner, _ = live([reply()], fake_clock, argv_log, interval=0.005)
+    collector.start()
+    collector.start()  # a second start does not add a thread
+    assert sum(1 for t in threading.enumerate() if t.name == "observe-collector") == 1
+    wait_until(lambda: collector.latest().cycle >= 3)
+    collector.stop()
+    assert not any(t.name == "observe-collector" for t in threading.enumerate())
+    cycles = collector.latest().cycle
+    time.sleep(0.05)
+    assert collector.latest().cycle == cycles  # nothing runs after stop()
+
+
+def test_cycles_never_overlap_even_when_called_from_two_threads(fake_clock, argv_log):
+    active = {"now": 0, "max": 0}
+    guard = threading.Lock()
+
+    def slow(argv, timeout):
+        with guard:
+            active["now"] += 1
+            active["max"] = max(active["max"], active["now"])
+        time.sleep(0.02)
+        with guard:
+            active["now"] -= 1
+        return reply()
+
+    collector, _, _ = live([slow], fake_clock, argv_log)
+    threads = [
+        threading.Thread(target=lambda: [collector.run_once() for _ in range(5)])
+        for _ in range(2)
+    ]
+    for t in threads:
+        t.start()
+    for t in threads:
+        t.join(timeout=10)
+    assert active["max"] == 1 and collector.latest().cycle == 10
+
+
+# -- fixture mode -----------------------------------------------------------------------------------------------
+
+
+def test_source_loss_fixture_publishes_failing_cycles_that_keep_the_last_good_snapshot(
+    fake_clock,
+):
+    collector = Collector(FixtureSource("source-loss"), fake_clock)
+    results = [collector.run_once() for _ in range(6)]
+    assert [r.state for r in results] == [
+        "OK",
+        "OK",
+        "FAILED",
+        "FAILED",
+        "FAILED",
+        "FAILED",
+    ]
+    assert [r.code for r in results] == [
+        None,
+        None,
+        "timeout",
+        "timeout",
+        "exit:2",
+        "exit:2",
+    ]
+    for failing in results[2:]:
+        assert failing.snapshot is results[1].snapshot
+        assert failing.last_success_mono == results[1].last_success_mono
+        assert len(failing.snapshot.rows) == 5
+    assert results[0].mode == "fixture" and results[0].fixture_variant == "source-loss"
+    assert results[0].namespace == "fixture:source-loss"
+
+
+def test_base_fixture_replays_two_cycles_then_repeats_and_marks_the_frozen_row(
+    fake_clock,
+):
+    collector = Collector(FixtureSource("base"), fake_clock)
+    first, second, third = (collector.run_once() for _ in range(3))
+    assert len(first.snapshot.rows) == 80 and first.coverage.collected == 80
+    assert [r.dispatch_id for r in first.snapshot.rows if r.fixture_frozen] == ["w-003"]
+    kinds = {r.dispatch_id: r.next_action_kind for r in second.snapshot.rows}
+    assert kinds["w-005"] == "approve"
+    assert {r.dispatch_id: r.next_action_kind for r in first.snapshot.rows}[
+        "w-005"
+    ] == "none"
+    assert len(third.snapshot.rows) == 80 and all(
+        r.reobserved for r in third.snapshot.rows
+    )
+
+
+@pytest.mark.parametrize(
+    "variant",
+    [
+        "uneven",
+        "shared-unmapped",
+        "historical",
+        "long-identifiers",
+        "missing-fields",
+        "duplicate-out-of-order",
+        "empty",
+        "injection",
+    ],
+)
+def test_every_other_variant_runs_through_a_cycle(fake_clock, variant):
+    result = Collector(FixtureSource(variant), fake_clock).run_once()
+    assert result.state in ("OK", "PARTIAL") and result.snapshot is not None
+
+
+def test_empty_variant_publishes_ok_with_no_rows_and_total_zero(fake_clock):
+    result = Collector(FixtureSource("empty"), fake_clock).run_once()
+    assert (
+        result.state == "OK"
+        and result.snapshot.rows == ()
+        and result.coverage.reported_total == 0
+    )
+
+
+def test_duplicate_variant_counts_duplicates_and_flags_the_backward_timestamp(
+    fake_clock,
+):
+    collector = Collector(FixtureSource("duplicate-out-of-order"), fake_clock)
+    first = collector.run_once()
+    assert first.coverage.duplicates == 1 and first.coverage.collected == 3
+    second = collector.run_once()
+    flags = {r.dispatch_id: r.flags for r in second.snapshot.rows}
+    assert flags["w-001"] == ("conflict (time went back)",)
+    assert flags["w-003"] == ("order unknown",)
+
+
+# -- hygiene --------------------------------------------------------------------------------------------------------
+
+
+def test_the_collector_reads_time_only_from_the_injected_clock():
+    text = Path(collector_module.__file__).read_text(encoding="utf-8")
+    assert not re.search(
+        r"^\s*(import time|from time|import datetime|from datetime)", text, re.M
+    )
+    assert not re.search(r"\btime\.(monotonic|time|sleep|perf_counter)\(", text)
+    assert "subprocess" not in text and "observe.view" not in text

Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (none)

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
