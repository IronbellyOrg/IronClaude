"""Collector tests (AD-6, AD-20; T4, T5, T40 in acceptance-tests.md)."""

from __future__ import annotations

import dataclasses
import json
import re
import threading
import time
from pathlib import Path

import pytest

import superclaude.cli.observe.collector as collector_module
from superclaude.cli.observe.adapter import LiveSource
from superclaude.cli.observe.collector import Collector, CycleResult, FixtureSource
from tests.observe.conftest import FakeDiscover, FakeRunner, make_envelope, make_rows

ORCA = "/opt/fake/orca"


def reply(n=2, has_more=False, cursor=None, total=None, tag="a"):
    rows = make_rows(n, 1)
    for i, row in enumerate(rows):
        row["dispatchId"] = f"w-{tag}-{i:03d}"
    envelope = make_envelope(rows, total=total, has_more=has_more)
    if cursor is not None:
        envelope["result"]["page"]["nextCursor"] = cursor
    return 0, json.dumps(envelope)


def live(responses, clock, argv_log, path=ORCA, **kw):
    runner = FakeRunner(argv_log, responses)
    discover = FakeDiscover(argv_log, path)
    return Collector(LiveSource(runner, discover), clock, **kw), runner, discover


# -- before the first poll, and no Orca ----------------------------------------------------------


def test_a_not_polled_result_exists_before_the_first_poll(fake_clock, argv_log):
    collector, runner, _ = live([reply()], fake_clock, argv_log)
    result = collector.latest()
    assert (result.cycle, result.state, result.mode) == (0, "NOT_POLLED", "live")
    assert (
        result.snapshot is None
        and result.coverage is None
        and result.last_success_mono is None
    )
    assert runner.calls == 0
    assert {f.name for f in dataclasses.fields(CycleResult)}.isdisjoint(
        {"stale", "is_stale"}
    )


def test_discovery_none_publishes_not_available_and_starts_no_cycle(
    fake_clock, argv_log
):
    collector, runner, discover = live([reply()], fake_clock, argv_log, path=None)
    first = collector.run_once()
    assert (first.state, first.cycle, first.code) == ("NOT_AVAILABLE", 1, "not-found")
    assert collector.run_once() is first and collector.run_once() is first
    assert runner.calls == 0 and discover.calls == 1


def test_the_thread_stops_by_itself_when_no_orca_is_available(fake_clock, argv_log):
    collector, runner, _ = live(
        [reply()], fake_clock, argv_log, path=None, interval=0.01
    )
    collector.start()
    wait_until(lambda: collector.latest().state == "NOT_AVAILABLE")
    wait_until(
        lambda: not any(t.name == "observe-collector" for t in threading.enumerate())
    )
    collector.stop()
    assert runner.calls == 0


def wait_until(predicate, timeout=5.0):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        if predicate():
            return
        time.sleep(0.005)
    raise AssertionError("condition not reached")


# -- T4: the call cap ------------------------------------------------------------------------------


def test_a_source_that_always_has_more_stops_at_the_cap_with_500_rows(
    fake_clock, argv_log
):
    counter = {"n": 0}

    def always_more(argv, timeout):
        counter["n"] += 1
        return reply(100, True, f"c{counter['n']}", 9999, tag=str(counter["n"]))

    collector, runner, _ = live([always_more], fake_clock, argv_log)
    result = collector.run_once()
    assert runner.calls == 5
    assert (result.state, result.code, result.cycle) == ("PARTIAL", None, 1)
    assert (
        result.coverage.partial
        and result.coverage.stopped_by_cap
        and result.coverage.has_more_at_stop
    )
    assert result.coverage.collected == 500 and len(result.snapshot.rows) == 500
    assert result.coverage.reported_total == 9999


# -- T5 and T40: time ----------------------------------------------------------------------------------


def test_a_call_that_exceeds_the_per_call_timeout_is_code_timeout_within_the_budget(
    fake_clock, argv_log
):
    def too_slow(argv, timeout):
        fake_clock.advance(
            timeout
        )  # the fake "sleeps" past the injected per-call timeout
        raise TimeoutError("slow")

    collector, runner, _ = live([too_slow], fake_clock, argv_log)
    result = collector.run_once()
    assert (result.state, result.code) == ("FAILED", "timeout")
    assert runner.timeouts == [10.0] and result.duration == 10.0 <= 15.0


def test_backoff_doubles_to_sixty_and_resets_after_a_success(fake_clock, argv_log):
    collector, _, _ = live(
        [(2, ""), (2, ""), (2, ""), (2, ""), reply(), (2, "")], fake_clock, argv_log
    )
    assert collector.next_interval == 15.0
    seen = []
    for _ in range(4):
        assert collector.run_once().state == "FAILED"
        seen.append(collector.next_interval)
    assert seen == [30.0, 60.0, 60.0, 60.0]
    assert collector.run_once().state == "OK" and collector.next_interval == 15.0
    assert collector.run_once().state == "FAILED" and collector.next_interval == 30.0


def test_an_overrunning_call_is_cut_at_the_budget_with_code_overrun(
    fake_clock, argv_log
):
    def first_page(argv, timeout):
        fake_clock.advance(12)
        return reply(2, True, "c1", 9)

    def second_page(argv, timeout):
        assert (
            timeout == 3.0
        )  # the time left in the 15 s budget, not the 10 s call limit
        fake_clock.advance(timeout)
        raise TimeoutError("cut")

    collector, runner, _ = live([first_page, second_page], fake_clock, argv_log)
    result = collector.run_once()
    assert (result.state, result.code, result.duration) == ("PARTIAL", "overrun", 15.0)
    assert (
        result.coverage.stopped_by_error == "overrun" and result.coverage.collected == 2
    )
    assert runner.calls == 2


def test_wall_clock_jumps_change_nothing_recorded_for_staleness(fake_clock, argv_log):
    collector, _, _ = live([reply(), (2, "")], fake_clock, argv_log)
    ok = collector.run_once()
    mono, wall = ok.last_success_mono, ok.last_success_wall
    fake_clock.jump_wall(-7200)
    fake_clock.advance(20)
    failed = collector.run_once()
    assert failed.state == "FAILED"
    assert (failed.last_success_mono, failed.last_success_wall) == (mono, wall)
    assert (
        mono == 1000.0
    )  # the fake monotonic clock's start: nothing wall-based leaked in


# -- failures keep what was read ----------------------------------------------------------------------------


def test_a_failed_first_page_keeps_the_previous_snapshot_and_last_success(
    fake_clock, argv_log
):
    collector, _, _ = live([reply(3), (2, "", "boom")], fake_clock, argv_log)
    good = collector.run_once()
    fake_clock.advance(15)
    bad = collector.run_once()
    assert (bad.state, bad.code, bad.cycle, bad.diagnostic) == (
        "FAILED",
        "exit:2",
        2,
        "boom",
    )
    assert bad.snapshot is good.snapshot and bad.coverage is good.coverage
    assert bad.last_success_mono == good.last_success_mono == 1000.0


def test_a_failed_second_page_keeps_the_rows_already_read(fake_clock, argv_log):
    collector, _, _ = live(
        [reply(2, True, "c1", 9), (3, "", "late")], fake_clock, argv_log
    )
    result = collector.run_once()
    assert (result.state, result.code) == ("PARTIAL", "exit:3")
    assert (
        result.coverage.stopped_by_error == "exit:3" and len(result.snapshot.rows) == 2
    )
    assert result.last_success_mono is not None


def test_a_shape_error_on_the_first_page_is_failed_and_on_a_later_page_partial(
    fake_clock, argv_log
):
    broken = (0, json.dumps({"result": {"workers": "x", "page": {"hasMore": False}}}))
    collector, _, _ = live([reply(2), broken], fake_clock, argv_log)
    good = collector.run_once()
    bad = collector.run_once()
    assert (bad.state, bad.code) == (
        "FAILED",
        "shape",
    ) and bad.snapshot is good.snapshot
    collector, _, _ = live([reply(2, True, "c1", 9), broken], fake_clock, argv_log)
    result = collector.run_once()
    assert (result.state, result.code, len(result.snapshot.rows)) == (
        "PARTIAL",
        "shape",
        2,
    )


def test_rows_not_returned_by_the_next_cycle_stay_not_reobserved(fake_clock, argv_log):
    collector, _, _ = live([reply(3, tag="a"), reply(2, tag="b")], fake_clock, argv_log)
    collector.run_once()
    second = collector.run_once()
    assert len(second.snapshot.rows) == 5
    assert sum(1 for r in second.snapshot.rows if not r.reobserved) == 3


# -- publication and the thread -----------------------------------------------------------------------------


def test_readers_never_see_a_half_built_result_while_cycles_publish(
    fake_clock, argv_log
):
    counter = {"n": 0}

    def varying(argv, timeout):
        counter["n"] += 1
        return reply(5 + counter["n"] % 3, False, None, None, tag=str(counter["n"]))

    collector, _, _ = live([varying], fake_clock, argv_log)
    stop = threading.Event()
    problems: list[str] = []

    def reader():
        last = 0
        while not stop.is_set():
            result = collector.latest()
            if result.cycle < last:
                problems.append("cycle went backwards")
            last = result.cycle
            if result.state == "OK" and (
                result.snapshot is None
                or result.snapshot.cycle != result.cycle
                or result.coverage is None
                or result.coverage.collected
                != sum(1 for r in result.snapshot.rows if r.cycle == result.cycle)
            ):
                problems.append(f"inconsistent result at cycle {result.cycle}")

    threads = [threading.Thread(target=reader) for _ in range(2)]
    for t in threads:
        t.start()
    for _ in range(200):
        collector.run_once()
    stop.set()
    for t in threads:
        t.join(timeout=5)
    assert problems == [] and collector.latest().cycle == 200


def test_start_then_stop_leaves_no_live_thread(fake_clock, argv_log):
    collector, runner, _ = live([reply()], fake_clock, argv_log, interval=0.005)
    collector.start()
    collector.start()  # a second start does not add a thread
    assert sum(1 for t in threading.enumerate() if t.name == "observe-collector") == 1
    wait_until(lambda: collector.latest().cycle >= 3)
    collector.stop()
    assert not any(t.name == "observe-collector" for t in threading.enumerate())
    cycles = collector.latest().cycle
    time.sleep(0.05)
    assert collector.latest().cycle == cycles  # nothing runs after stop()


def test_cycles_never_overlap_even_when_called_from_two_threads(fake_clock, argv_log):
    active = {"now": 0, "max": 0}
    guard = threading.Lock()

    def slow(argv, timeout):
        with guard:
            active["now"] += 1
            active["max"] = max(active["max"], active["now"])
        time.sleep(0.02)
        with guard:
            active["now"] -= 1
        return reply()

    collector, _, _ = live([slow], fake_clock, argv_log)
    threads = [
        threading.Thread(target=lambda: [collector.run_once() for _ in range(5)])
        for _ in range(2)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=10)
    assert active["max"] == 1 and collector.latest().cycle == 10


# -- fixture mode -----------------------------------------------------------------------------------------------


def test_source_loss_fixture_publishes_failing_cycles_that_keep_the_last_good_snapshot(
    fake_clock,
):
    collector = Collector(FixtureSource("source-loss"), fake_clock)
    results = [collector.run_once() for _ in range(6)]
    assert [r.state for r in results] == [
        "OK",
        "OK",
        "FAILED",
        "FAILED",
        "FAILED",
        "FAILED",
    ]
    assert [r.code for r in results] == [
        None,
        None,
        "timeout",
        "timeout",
        "exit:2",
        "exit:2",
    ]
    for failing in results[2:]:
        assert failing.snapshot is results[1].snapshot
        assert failing.last_success_mono == results[1].last_success_mono
        assert len(failing.snapshot.rows) == 5
    assert results[0].mode == "fixture" and results[0].fixture_variant == "source-loss"
    assert results[0].namespace == "fixture:source-loss"


def test_base_fixture_replays_two_cycles_then_repeats_and_marks_the_frozen_row(
    fake_clock,
):
    collector = Collector(FixtureSource("base"), fake_clock)
    first, second, third = (collector.run_once() for _ in range(3))
    assert len(first.snapshot.rows) == 80 and first.coverage.collected == 80
    assert [r.dispatch_id for r in first.snapshot.rows if r.fixture_frozen] == ["w-003"]
    kinds = {r.dispatch_id: r.next_action_kind for r in second.snapshot.rows}
    assert kinds["w-005"] == "approve"
    assert {r.dispatch_id: r.next_action_kind for r in first.snapshot.rows}[
        "w-005"
    ] == "none"
    assert len(third.snapshot.rows) == 80 and all(
        r.reobserved for r in third.snapshot.rows
    )


@pytest.mark.parametrize(
    "variant",
    [
        "uneven",
        "shared-unmapped",
        "historical",
        "long-identifiers",
        "missing-fields",
        "duplicate-out-of-order",
        "empty",
        "injection",
    ],
)
def test_every_other_variant_runs_through_a_cycle(fake_clock, variant):
    result = Collector(FixtureSource(variant), fake_clock).run_once()
    assert result.state in ("OK", "PARTIAL") and result.snapshot is not None


def test_empty_variant_publishes_ok_with_no_rows_and_total_zero(fake_clock):
    result = Collector(FixtureSource("empty"), fake_clock).run_once()
    assert (
        result.state == "OK"
        and result.snapshot.rows == ()
        and result.coverage.reported_total == 0
    )


def test_duplicate_variant_counts_duplicates_and_flags_the_backward_timestamp(
    fake_clock,
):
    collector = Collector(FixtureSource("duplicate-out-of-order"), fake_clock)
    first = collector.run_once()
    assert first.coverage.duplicates == 1 and first.coverage.collected == 3
    second = collector.run_once()
    flags = {r.dispatch_id: r.flags for r in second.snapshot.rows}
    assert flags["w-001"] == ("conflict (time went back)",)
    assert flags["w-003"] == ("order unknown",)


# -- hygiene --------------------------------------------------------------------------------------------------------


def test_the_collector_reads_time_only_from_the_injected_clock():
    text = Path(collector_module.__file__).read_text(encoding="utf-8")
    assert not re.search(
        r"^\s*(import time|from time|import datetime|from datetime)", text, re.M
    )
    assert not re.search(r"\btime\.(monotonic|time|sleep|perf_counter)\(", text)
    assert "subprocess" not in text and "observe.view" not in text
