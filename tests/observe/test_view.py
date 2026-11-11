"""View model tests (AD-8, AD-10; T9, T11, T13, T14, T15, T18, T20, T21, T31, T33, T34, T38, T42, T43, T47)."""

from __future__ import annotations

import json
import re
from datetime import timedelta
from pathlib import Path

import superclaude
import superclaude.cli.observe.view as view_module
from superclaude.cli.observe.adapter import LiveSource
from superclaude.cli.observe.collector import Collector, FixtureSource
from superclaude.cli.observe.parse import UNKNOWN
from superclaude.cli.observe.view import (
    ABSENT_IN_SOURCE,
    EMPTY_NOTICE,
    GAP_NOTICE,
    LEDGER_TITLE,
    NO_READ_YET,
    UNAVAILABLE,
    Session,
    aggregate,
    build_view,
    change_key,
    format_age,
    text_of,
)
from tests.observe.conftest import (
    BASE_TIME,
    FakeClock,
    FakeDiscover,
    FakeRunner,
    make_envelope,
    make_rows,
)


def fixture_result(variant, clock, cycles=1):
    collector = Collector(FixtureSource(variant), clock)
    result = None
    for _ in range(cycles):
        result = collector.run_once()
    return result


def live_collector(responses, clock, argv_log, path="/opt/fake/orca"):
    runner = FakeRunner(argv_log, responses)
    return Collector(LiveSource(runner, FakeDiscover(argv_log, path)), clock)


def rows_reply(rows, total=None, has_more=False, cursor=None, **result_extra):
    envelope = make_envelope(rows, total=total, has_more=has_more)
    if cursor is not None:
        envelope["result"]["page"]["nextCursor"] = cursor
    envelope["result"].update(result_extra)
    return 0, json.dumps(envelope)


def texts(view, with_gap=True):
    """Every string a screen or export could show for this view."""
    parts = [
        view.header1,
        view.header2,
        view.collected_text,
        view.ledger_title,
        *view.ledger_empty,
    ]
    parts += [t.text for t in view.counts_tokens]
    for note in (
        view.changes_line,
        view.filter_line,
        view.historical_note,
        view.duplicates_note,
        view.selection_note,
    ):
        if note:
            parts.append(note)
    for rv in view.all_rows:
        parts += [
            rv.dispatch_id,
            rv.run,
            rv.worker_state,
            rv.dispatch_status,
            rv.terminal_state,
            rv.outcome,
        ]
        parts += [rv.next_action, rv.liveness, rv.evidence_age, *rv.flags]
        parts += [f"{label}: {value}" for label, value in rv.inspector]
    if with_gap:
        parts.append(view.gap_notice)
    return parts


def build(result, clock, session=None):
    return build_view(result, session or Session(), clock)


# -- T13 and T38: unknown is never zero ----------------------------------------------------------------

ABSENT_LABELS = {
    "task_id": "taskId",
    "run_id": "runId",
    "worktree_id": "resource.worktreeId",
    "owner_dispatch_id": "resource.ownerDispatchId",
    "origin_dispatch_id": "resource.originDispatchId",
    "host_id": "projection.host.id",
    "workspace_id": "projection.workspace.id",
    "stage_worker": "projection.stage.worker (worker-reported)",
    "stage_dispatch": "projection.stage.dispatch (worker-reported)",
    "next_action_kind": "projection.nextAction.kind",
    "outcome": "projection.outcome",
}


def test_every_absent_field_renders_unknown_and_never_zero_or_false(fake_clock):
    view = build(fixture_result("missing-fields", fake_clock), fake_clock)
    checked = 0
    for rv in view.all_rows:
        inspector = dict(rv.inspector)
        for attr in rv.raw.absent_fields:
            label = ABSENT_LABELS.get(attr)
            if label is None:
                continue
            assert inspector[label] == ABSENT_IN_SOURCE, (rv.dispatch_id, attr)
            assert inspector[label] not in ("0", "false", "-", "")
            checked += 1
    assert checked >= 5
    by_dispatch = {rv.dispatch_id: rv for rv in view.all_rows}
    first = by_dispatch["w-001"]  # no liveness and no nextAction
    assert first.next_action == "unknown" and first.liveness == "unknown (unknown)"
    anonymous = next(rv for rv in view.all_rows if "identity unknown" in rv.flags)
    assert (
        anonymous.dispatch_id == "unknown"
        and dict(anonymous.inspector)["dispatchId"] == ABSENT_IN_SOURCE
    )
    assert (
        next(rv for rv in view.all_rows if rv.dispatch_id == "w-003").run == "unknown"
    )  # a JSON null
    assert (
        next(rv for rv in view.all_rows if rv.dispatch_id == "w-004").evidence_age
        == "unknown"
    )


def test_aggregates_with_unknown_members_render_n_plus_question_mark(fake_clock):
    assert aggregate(3, 0) == "3"
    assert aggregate(3, 2) == "3+? (2 unknown)" and aggregate(0, 4) == "0+? (4 unknown)"
    view = build(fixture_result("missing-fields", fake_clock), fake_clock)
    assert "runs seen: 1+? (1 unknown)" in [t.text for t in view.counts_tokens]
    clean = build(fixture_result("base", fake_clock), fake_clock)
    assert "runs seen: 8" in [t.text for t in clean.counts_tokens]


def test_a_source_value_that_is_the_text_unknown_is_quoted():
    assert text_of(UNKNOWN) == "unknown"
    assert text_of("unknown") == '"unknown"' and text_of("UNKNOWN") == '"UNKNOWN"'
    assert (
        text_of("running") == "running"
        and text_of(0) == "0"
        and text_of(False) == "false"
    )


def test_missing_fields_header_says_scope_unknown_and_total_unknown(fake_clock):
    view = build(fixture_result("missing-fields", fake_clock), fake_clock)
    assert "scope unknown" in view.header1 and view.scope_text == "scope unknown"
    assert "reported unknown" in view.collected_text


# -- T14 and T15: separate facts, nothing inferred ---------------------------------------------------------


def test_a_released_row_without_an_outcome_never_reads_done_complete_or_settled(
    fake_clock, argv_log
):
    rows = make_rows(2, 1)
    for row in rows:
        row["terminalState"] = "released"
        row["workerState"] = "exited"
        row["dispatchStatus"] = "exited"
        del row["projection"]["outcome"]
    collector = live_collector([rows_reply(rows, total=2)], fake_clock, argv_log)
    view = build(collector.run_once(), fake_clock, Session(show_historical=True))
    assert len(view.visible_rows) == 2
    for rv in view.visible_rows:
        assert rv.terminal_state == "released" and rv.outcome == "unknown"
    row_texts = " ".join(
        t
        for rv in view.all_rows
        for t in (
            rv.worker_state,
            rv.dispatch_status,
            rv.terminal_state,
            rv.outcome,
            rv.liveness,
            *rv.flags,
        )
    ).lower()
    for word in ("done", "complete", "settled"):
        assert word not in row_texts


def test_report_acceptance_tests_and_approval_are_unavailable_and_nothing_is_admitted(
    fake_clock,
):
    view = build(
        fixture_result("base", fake_clock), fake_clock, Session(focus="inspector")
    )
    for rv in view.all_rows:
        inspector = dict(rv.inspector)
        for fact in ("report status", "acceptance", "tests", "approval"):
            assert inspector[fact] == UNAVAILABLE
    assert not any("admitted" in t.lower() for t in texts(view))
    assert "admitted" not in repr(view).lower()


# -- T18: collected / reported ----------------------------------------------------------------------------------


def test_total_287_with_100_rows_reads_collected_100_of_reported_287_never_287_workers(
    fake_clock, argv_log
):
    collector = live_collector(
        [rows_reply(make_rows(100, 4), total=287)], fake_clock, argv_log
    )
    view = build(collector.run_once(), fake_clock)
    assert view.collected_text.startswith("collected 100 / reported 287")
    assert not any("287 workers" in t for t in texts(view))


def test_absent_total_reads_reported_unknown(fake_clock, argv_log):
    collector = live_collector([rows_reply(make_rows(3, 1))], fake_clock, argv_log)
    view = build(collector.run_once(), fake_clock)
    assert view.collected_text == "collected 3 / reported unknown"


def test_coverage_literals(fake_clock, argv_log):
    counter = {"n": 0}

    def more(argv, timeout):
        counter["n"] += 1
        rows = make_rows(100, 1)
        for row in rows:
            row["dispatchId"] += f"-{counter['n']}"
        return rows_reply(rows, total=9999, has_more=True, cursor=f"c{counter['n']}")

    view = build(live_collector([more], fake_clock, argv_log).run_once(), fake_clock)
    partial = [t.text for t in view.counts_tokens if t.text.startswith("PARTIAL")]
    assert partial == [
        "PARTIAL: collected 500 of reported 9999 (newest first; oldest rows not read; long-running active workers may be among them)"
    ]
    assert view.collected_text == "collected 500 / reported 9999 (page 5)"

    stalled = build(
        live_collector(
            [rows_reply(make_rows(2, 1), total=9, has_more=True)], fake_clock, argv_log
        ).run_once(),
        fake_clock,
    )
    assert "PARTIAL (cursor missing or not advancing, page 1)" in [
        t.text for t in stalled.counts_tokens
    ]
    rejected = build(
        live_collector(
            [rows_reply(make_rows(2, 1), total=9, has_more=True, cursor="-bad")],
            fake_clock,
            argv_log,
        ).run_once(),
        fake_clock,
    )
    assert "PARTIAL (cursor rejected, page 1)" in [
        t.text for t in rejected.counts_tokens
    ]

    empty = rows_reply([], total=5, has_more=True, cursor="c2")
    paged = build(
        live_collector(
            [rows_reply(make_rows(2, 1), total=5, has_more=True, cursor="c1"), empty],
            fake_clock,
            argv_log,
        ).run_once(),
        fake_clock,
    )
    assert "PARTIAL (empty page 2)" in [t.text for t in paged.counts_tokens]

    def renamed(n):
        return [dict(r, dispatchId=r["dispatchId"] + "x") for r in make_rows(n, 1)]

    first_page = rows_reply(make_rows(2, 1), total=250, has_more=True, cursor="c1")
    changed = build(
        live_collector(
            [first_page, rows_reply(renamed(2), total=251)], fake_clock, argv_log
        ).run_once(),
        fake_clock,
    )
    assert (
        changed.collected_text == "collected 4 / reported 250-251 (changed during read)"
    )

    first_page = rows_reply(make_rows(2, 1), total=4, has_more=True, cursor="c1")
    two_pages = build(
        live_collector(
            [first_page, rows_reply(renamed(2), total=4)], fake_clock, argv_log
        ).run_once(),
        fake_clock,
    )
    assert two_pages.collected_text == "collected 4 / reported 4 (page 2)"


def test_cycle_overran_warnings_and_duplicates_have_their_literals(
    fake_clock, argv_log
):
    def first(argv, timeout):
        fake_clock.advance(12)
        return rows_reply(
            make_rows(2, 1),
            total=9,
            has_more=True,
            cursor="c1",
            warnings=["careful", "again"],
        )

    def second(argv, timeout):
        fake_clock.advance(timeout)
        raise TimeoutError

    view = build(
        live_collector([first, second], fake_clock, argv_log).run_once(), fake_clock
    )
    assert "cycle overran (15s)" in view.freshness_cells
    assert "source warnings: 2 (inspector)" in view.freshness_cells
    dup = build(fixture_result("duplicate-out-of-order", fake_clock), fake_clock)
    assert dup.duplicates_note == "1 duplicate rows ignored"


# -- T9 and T47: the question-source gap ------------------------------------------------------------------------------


def test_live_mode_shows_the_gap_notice_and_the_ledger_title_and_derives_nothing_from_count(
    fake_clock, argv_log
):
    collector = live_collector(
        [rows_reply(make_rows(3, 1), total=3, count=999)], fake_clock, argv_log
    )
    view = build(collector.run_once(), fake_clock)
    assert (
        view.gap_notice
        == GAP_NOTICE
        == 'Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"'
    )
    assert view.ledger_title == LEDGER_TITLE == "worker-reported, not questions"
    assert not any("999" in t for t in texts(view))
    assert not any("no questions" in t for t in texts(view, with_gap=False))


# -- T11 and T42: freshness ------------------------------------------------------------------------------------------


def test_freshness_cell_ok_stale_and_failed_with_ages_and_values_keep_their_last_reading(
    fake_clock,
):
    collector = Collector(FixtureSource("source-loss"), fake_clock)
    good = collector.run_once()
    collector.run_once()
    fake_clock.advance(4)
    assert build(good, fake_clock).freshness_cells[0] == "worker-list OK 4s"
    fake_clock.advance(48)
    stale = build(good, fake_clock)
    assert (
        stale.freshness_cells[0] == "worker-list STALE 52s"
        and stale.source_state == "STALE"
    )
    fake_clock.advance(8)  # the same result at 60 s: a minute
    assert build(good, fake_clock).freshness_cells[0] == "worker-list STALE 1m"
    failed = collector.run_once()  # third cycle of the fixture: {"fail": "timeout"}
    view = build(failed, fake_clock)
    assert (
        view.freshness_cells[0] == "worker-list FAILED (timeout) 1m"
        and view.source_state == "FAILED"
    )
    assert (
        len(view.all_rows) == 5
        and view.as_of != "never"
        and f"as of {view.as_of}" in view.header1
    )

    def cells(v):
        return [
            (rv.worker_state, rv.outcome, rv.liveness, rv.terminal_state)
            for rv in v.all_rows
        ]

    assert cells(view) == cells(build(good, fake_clock))  # no value turns into "failed"
    exit_failed = Collector(FixtureSource("source-loss"), fake_clock)
    for _ in range(5):
        last = exit_failed.run_once()
    assert (
        build(last, fake_clock)
        .freshness_cells[0]
        .startswith("worker-list FAILED (exit 2)")
    )


def test_stale_is_exactly_forty_five_seconds_on_the_monotonic_clock(fake_clock):
    result = fixture_result("base", fake_clock)
    fake_clock.advance(44)
    assert build(result, fake_clock).source_state == "OK"
    fake_clock.advance(1)
    assert build(result, fake_clock).source_state == "STALE"
    fake_clock.jump_wall(-7200)  # a wall-clock jump changes nothing about staleness
    assert build(result, fake_clock).source_state == "STALE"


def test_before_the_first_poll_and_when_no_orca_is_available(fake_clock, argv_log):
    collector = live_collector([rows_reply([])], fake_clock, argv_log)
    view = build(collector.latest(), fake_clock)
    assert (
        view.source_state == "NOT_POLLED"
        and view.freshness_cells[0] == "worker-list NOT POLLED"
    )
    assert "as of never" in view.header1
    assert view.collected_text == "collected unknown / reported unknown"
    assert (
        view.ledger_empty == (NO_READ_YET,) == ("no successful worker-list read yet",)
    )
    unavailable = build(
        live_collector([rows_reply([])], fake_clock, argv_log, path=None).run_once(),
        fake_clock,
    )
    assert unavailable.source_state == "NOT_AVAILABLE"
    assert (
        unavailable.freshness_cells[0]
        == "worker-list NOT AVAILABLE (no Orca CLI validated)"
    )
    assert unavailable.ledger_empty == (NO_READ_YET,)


def test_poll_age_and_evidence_age_are_separate_facts(fake_clock, argv_log):
    rows = make_rows(2, 1)
    old = (BASE_TIME - timedelta(minutes=20)).strftime("%Y-%m-%dT%H:%M:%SZ")
    for row in rows:
        row["projection"]["evidence"]["lastObservedAt"] = old
        row["projection"]["liveness"]["observedAt"] = old
    result = live_collector(
        [rows_reply(rows, total=2)], fake_clock, argv_log
    ).run_once()
    fake_clock.advance(4)
    view = build(result, fake_clock)
    assert view.poll_age == "4s" and view.source_state == "OK"
    assert view.freshness_cells[0] == "worker-list OK 4s"
    assert {rv.evidence_age for rv in view.all_rows} == {"20m"}


def test_format_age():
    assert [format_age(s) for s in (-5, 0, 4, 59, 60, 119, 3599, 3600, 7300)] == [
        "0s",
        "0s",
        "4s",
        "59s",
        "1m",
        "1m",
        "59m",
        "1h",
        "2h",
    ]


# -- T20, CD-16: shared worktrees --------------------------------------------------------------------------------------


def test_sessions_sharing_a_worktree_stay_two_rows_with_the_same_worktree_in_each_inspector(
    fake_clock,
):
    view = build(fixture_result("shared-unmapped", fake_clock), fake_clock)
    assert len(view.all_rows) == 3
    by_dispatch = {rv.dispatch_id: dict(rv.inspector) for rv in view.all_rows}
    assert (
        by_dispatch["w-001"]["resource.worktreeId"]
        == "wt-shared"
        == by_dispatch["w-002"]["resource.worktreeId"]
    )
    assert by_dispatch["w-003"]["resource.worktreeId"] == ABSENT_IN_SOURCE
    assert not any("conflict" in t.lower() for t in texts(view))


# -- T21: historical rows ----------------------------------------------------------------------------------------------------


def test_historical_rows_are_hidden_by_default_and_listed_with_their_state_on_toggle(
    fake_clock,
):
    result = fixture_result("historical", fake_clock)
    hidden = build(result, fake_clock)
    assert hidden.historical_note == "5 historical hidden (h)"
    assert len(hidden.visible_rows) == 4 and len(hidden.all_rows) == 9
    states = {rv.dispatch_id: rv.terminal_state for rv in hidden.visible_rows}
    assert states == {
        "w-001": "active",
        "w-007": "unknown",
        "w-008": "orphaned",
        "w-009": "active",
    }
    shown = build(result, fake_clock, Session(show_historical=True))
    assert shown.historical_note is None and len(shown.visible_rows) == 9
    assert {rv.terminal_state for rv in shown.visible_rows} >= {
        "released",
        "retained",
        "orphaned",
        "unknown",
    }

    def counts(v):
        return [
            t.text
            for t in v.counts_tokens
            if t.text.startswith(("collected", "source counts"))
        ]

    assert counts(hidden) == counts(shown)  # the toggle never changes source counts


# -- T31, T33, T34 -------------------------------------------------------------------------------------------------------------


def test_cost_is_unavailable_never_a_dollar_amount_and_elapsed_time_is_only_an_age(
    fake_clock,
):
    view = build(fixture_result("base", fake_clock), fake_clock)
    assert "cost unavailable" in [t.text for t in view.counts_tokens]
    assert not any("$" in t or "%" in t for t in texts(view))
    assert all(
        re.fullmatch(r"\d+[smh]|unknown", rv.evidence_age) for rv in view.all_rows
    )


def test_empty_fixture_reads_exactly_the_not_proof_text_and_names_the_scope(fake_clock):
    view = build(fixture_result("empty", fake_clock), fake_clock)
    assert view.ledger_empty == (
        EMPTY_NOTICE,
        "worker-list returned 0 workers in scope=bound",
    )
    assert (
        EMPTY_NOTICE == "no observed items in this source window; not proof none exist"
    )
    assert "one Run only" in view.header1 and "scope=bound" in view.header1
    assert not any("no questions" in t for t in texts(view, with_gap=False))


def test_fixture_mode_marks_frozen_rows_and_live_mode_reads_unavailable(
    fake_clock, argv_log
):
    fixture = build(fixture_result("base", fake_clock), fake_clock)
    assert [rv.dispatch_id for rv in fixture.all_rows if rv.frozen] == ["w-003"]
    assert all(("FROZEN" in rv.flags) == rv.frozen for rv in fixture.all_rows)
    assert (
        fixture.synthetic_banner == "SYNTHETIC FIXTURE base, not Orca data"
        and fixture.synthetic_banner in fixture.header1
    )
    live = build(
        live_collector(
            [rows_reply(make_rows(3, 1), total=3)], fake_clock, argv_log
        ).run_once(),
        fake_clock,
    )
    tokens = [t.text for t in live.counts_tokens]
    assert (
        "SETTLED unavailable (no source)" in tokens
        and "POLICY FROZEN unavailable (no source)" in tokens
    )
    assert not any(rv.frozen for rv in live.all_rows) and live.synthetic_banner is None
    assert "mode=live" in live.header1


# -- T43: overflow ------------------------------------------------------------------------------------------------------------------


def test_plus_n_more_never_counts_the_selected_row(fake_clock):
    result = fixture_result("base", fake_clock)
    plain = build(result, fake_clock, Session(show_historical=True))
    target = plain.visible_rows[50].identity
    view = build(result, fake_clock, Session(selected=target, show_historical=True))
    window = view.window(10)
    assert window.shown == 10 and window.total == 80 and window.text == "10/80 shown"
    assert any(rv.selected for rv in window.rows)  # the selected row is kept in view
    assert window.more == 70 and window.more_text == "+70 more"
    assert view.footer(window).endswith("shown 10/80 | collected 80 / reported 80")
    assert "shown 80/80 | collected 80 / reported 80" in view.footer(view.window(None))
    # selected row not in the visible set (filtered out): it is not counted in "+N more" either
    row_view = view.selected
    narrowed = build(
        result,
        fake_clock,
        Session(
            selected=target,
            selected_row=row_view.raw,
            filter_text="run-a",
            show_historical=True,
        ),
    )
    assert target not in {rv.identity for rv in narrowed.visible_rows}
    nw = narrowed.window(4)
    assert nw.total == 10 and nw.more == 6
    everything = view.window(None)
    assert (everything.shown, everything.more, everything.more_text) == (80, 0, "")
    assert view.window(500).text == "80/80 shown"


def test_window_without_a_selection_starts_at_the_top(fake_clock):
    view = build(
        fixture_result("base", fake_clock), fake_clock, Session(show_historical=True)
    )
    window = view.window(5)
    assert [rv.dispatch_id for rv in window.rows] == [
        rv.dispatch_id for rv in view.visible_rows[:5]
    ]
    assert window.more == 75


# -- header, filter, changes, selection --------------------------------------------------------------------------------------------


def test_filter_line_names_the_expression_and_counts(fake_clock):
    view = build(
        fixture_result("base", fake_clock), fake_clock, Session(filter_text="run-a")
    )
    assert view.filter_line == "filter run-a: 10 of 80 collected"
    assert (
        len(view.visible_rows) == 7
    )  # 3 of the 10 are historical and hidden by default
    assert view.historical_note == "3 historical hidden (h)"
    assert "collected 80 / reported 80" in view.collected_text
    assert build(fixture_result("base", fake_clock), fake_clock).filter_line is None


def test_next_action_is_verbatim_and_blank_reads_unknown(fake_clock, argv_log):
    rows = make_rows(3, 1)
    rows[0]["projection"]["nextAction"]["kind"] = "Review-Needed "
    rows[1]["projection"]["nextAction"]["kind"] = "   "
    del rows[2]["projection"]["nextAction"]
    view = build(
        live_collector([rows_reply(rows, total=3)], fake_clock, argv_log).run_once(),
        fake_clock,
    )
    by_dispatch = {rv.dispatch_id: rv.next_action for rv in view.all_rows}
    assert by_dispatch == {
        "w-001": "Review-Needed ",
        "w-002": "unknown",
        "w-003": "unknown",
    }


def test_changed_rows_are_starred_and_counted_since_the_baseline(fake_clock):
    first = fixture_result("base", fake_clock)
    second = fixture_result("base", fake_clock, cycles=2)
    baseline = {r.identity: change_key(r) for r in first.snapshot.rows}
    marked = Session(
        baseline=baseline, mark_wall_time=BASE_TIME.timestamp(), marked=True
    )
    view = build(second, fake_clock, marked)
    assert [rv.dispatch_id for rv in view.all_rows if rv.changed] == ["w-005"]
    assert view.changes_line == "changed since 12:00 (1)"
    restart = build(
        second,
        fake_clock,
        Session(baseline=baseline, mark_wall_time=BASE_TIME.timestamp(), marked=False),
    )
    assert (
        restart.changes_line
        == "new baseline at 12:00 (observer started) | changed since 12:00 (1)"
    )
    # added and removed rows count too
    smaller = dict(baseline)
    gone = next(iter(smaller))
    del smaller[gone]
    smaller[("fixture:base", "w-gone")] = ()
    counted = build(
        second,
        fake_clock,
        Session(baseline=smaller, mark_wall_time=BASE_TIME.timestamp(), marked=True),
    )
    assert (
        counted.changes_line == "changed since 12:00 (3)"
    )  # w-005 changed, one added, one removed
    assert build(second, fake_clock, Session()).changes_line is None  # no baseline yet


def test_a_selected_row_that_left_the_source_stays_selected_with_a_placeholder(
    fake_clock, argv_log
):
    collector = live_collector(
        [
            rows_reply(make_rows(3, 1), total=3),
            rows_reply(make_rows(3, 1)[:2], total=2),
        ],
        fake_clock,
        argv_log,
    )
    first = collector.run_once()
    gone = next(r for r in first.snapshot.rows if r.dispatch_id == "w-003")
    only_two = Collector(FixtureSource("empty"), fake_clock).run_once()
    view = build(
        only_two, fake_clock, Session(selected=gone.identity, selected_row=gone)
    )
    assert view.selection_note == "selected w-003 no longer in source window"
    assert view.selected is not None and "not reobserved" in view.selected.flags
    present = build(
        first, fake_clock, Session(selected=gone.identity, selected_row=gone)
    )
    assert present.selection_note is None and present.selected.selected


def test_inspector_is_built_only_in_inspector_focus_with_full_ids_and_worker_reported_labels(
    fake_clock,
):
    result = fixture_result("long-identifiers", fake_clock)
    ident = build(result, fake_clock).visible_rows[1].identity
    view = build(result, fake_clock, Session(focus="inspector", selected=ident))
    labels = [label for label, _ in view.inspector]
    assert (
        "projection.stage.detail (worker-reported)" in labels
        and "unrecognised keys" in labels
    )
    assert dict(view.inspector)["dispatchId"] == view.selected.raw.dispatch_id
    assert build(result, fake_clock, Session(selected=ident)).inspector is None


def test_source_warnings_and_poll_errors_are_listed_in_the_inspector(
    fake_clock, argv_log
):
    rows = make_rows(1, 1)
    collector = live_collector(
        [rows_reply(rows, total=1, warnings=["w one"]), (2, "", "\x1b[31mboom")],
        fake_clock,
        argv_log,
    )
    collector.run_once()
    failed = collector.run_once()
    view = build(
        failed,
        fake_clock,
        Session(focus="inspector", selected=failed.snapshot.rows[0].identity),
    )
    inspector = dict(view.inspector)
    assert (
        inspector["source warning"] == "w one"
        and inspector["last poll error (sanitized)"] == "boom"
    )


# -- typed snapshot fields on the View (AD-10) ------------------------------------------------------------------------------------------


def test_the_view_carries_every_typed_snapshot_field_as_a_full_value(fake_clock):
    view = build(fixture_result("base", fake_clock), fake_clock)
    meta = view.meta
    assert (meta.cycle, meta.namespace, meta.source_status, meta.source_error) == (
        1,
        "fixture:base",
        "OK",
        None,
    )
    assert (
        meta.generated_at == "2026-11-08T12:00:00Z"
        and meta.source_observed_at == "2026-11-08T12:00:00Z"
    )
    assert (meta.producer_name, meta.producer_version) == (
        "superclaude-observe",
        superclaude.__version__,
    )
    assert (meta.has_more, meta.total, meta.limit) == (False, 80, 100)
    assert meta.scope == {"source": "all"} and set(meta.counts) == {
        "active",
        "reclaimable",
        "retained",
        "released",
    }
    assert (
        meta.collection_state,
        meta.collection_collected,
        meta.collection_changed_during_read,
        meta.collection_duplicates_ignored,
    ) == ("COMPLETE", 80, False, 0)
    assert all(rv.raw.dispatch_id == rv.dispatch_id for rv in view.all_rows)
    not_polled = build(
        Collector(FixtureSource("base"), fake_clock).latest(), fake_clock
    ).meta
    assert (
        not_polled.source_status == "UNKNOWN"
        and not_polled.source_observed_at is UNKNOWN
    )
    assert (
        not_polled.scope is UNKNOWN
        and not_polled.collection_state is None
        and not_polled.total is UNKNOWN
    )
    collector = Collector(FixtureSource("source-loss"), fake_clock)
    for _ in range(3):
        failed = collector.run_once()
    assert (
        build(failed, fake_clock).meta.source_status,
        build(failed, fake_clock).meta.source_error,
    ) == ("ERROR", "timeout")
    fake_clock.advance(60)
    assert build(failed, fake_clock).meta.source_status == "ERROR"
    stale_cycle = fixture_result("base", fake_clock)
    fake_clock.advance(50)
    assert build(stale_cycle, fake_clock).meta.source_status == "STALE"


def test_all_rows_are_in_timestamp_order_newest_first_with_untimed_rows_last(
    fake_clock,
):
    view = build(fixture_result("duplicate-out-of-order", fake_clock), fake_clock)
    assert [rv.dispatch_id for rv in view.all_rows] == ["w-001", "w-002", "w-003"]
    assert [rv.dispatch_id for rv in view.visible_rows] == [
        "w-001",
        "w-002",
    ]  # w-003 is released
    base = build(fixture_result("base", fake_clock), fake_clock)
    assert [rv.dispatch_id for rv in base.all_rows[:3]] == ["w-001", "w-002", "w-003"]


# -- purity --------------------------------------------------------------------------------------------------------------------------------


class StrictClock:
    """Only the three clock methods exist; anything else raises."""

    def __init__(self, clock: FakeClock):
        self._clock = clock

    def monotonic(self):
        return self._clock.monotonic()

    def wall(self):
        return self._clock.wall()

    def local_tz(self):
        return self._clock.local_tz()


def test_same_inputs_build_equal_views_and_build_view_does_no_io(fake_clock):
    result = fixture_result("injection", fake_clock)
    session = Session(filter_text="w-inj", show_historical=True)
    strict = StrictClock(fake_clock)
    assert build_view(result, session, strict) == build_view(result, session, strict)
    assert build_view(result, Session(), strict) == build_view(
        result, Session(), strict
    )
    text = Path(view_module.__file__).read_text(encoding="utf-8")
    assert not re.search(
        r"^\s*(import time|from time|import datetime|from datetime|import os|import pathlib|from pathlib)",
        text,
        re.M,
    )
    assert not re.search(r"\b(time|datetime)\.\w+\(|\bopen\(", text)
    assert not re.search(r"observe\.(adapter|collector|render|export)\b", text)
    assert session == Session(
        filter_text="w-inj", show_historical=True
    )  # inputs untouched


def test_view_reexports_unknown_and_is_the_only_place_that_names_it_as_a_screen_word():
    assert view_module.UNKNOWN is UNKNOWN
    for name in ("export.py", "render.py"):
        path = Path(view_module.__file__).with_name(name)
        if path.exists():
            assert "observe.parse" not in path.read_text(encoding="utf-8")
