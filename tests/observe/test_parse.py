"""Parser and merge tests (AD-7, AD-19; T22, T32 parse half, T39 in acceptance-tests.md)."""

from __future__ import annotations

import copy

import pytest

from superclaude.cli.observe.parse import (
    CONFLICT_BACKWARD,
    IDENTITY_UNKNOWN,
    ORDER_UNKNOWN,
    UNKNOWN,
    Question,
    ShapeError,
    merge,
    parse_page,
    parse_questions,
    parse_timestamp,
)

T0 = "2026-11-08T12:00:00Z"
T1 = "2026-11-08T12:00:10Z"
T2 = "2026-11-08T12:00:20Z"


def worker(dispatch="w-001", observed=None, evidence=None, kind="none", **extra):
    liveness = {"verdict": "alive", "source": "terminal"}
    if observed:
        liveness["observedAt"] = observed
    row = {
        "dispatchId": dispatch,
        "taskId": "t-001",
        "runId": "run-a",
        "workerState": "running",
        "dispatchStatus": "active",
        "terminalState": "active",
        "resource": {"id": "r-1", "worktreeId": "wt-1"},
        "projection": {
            "outcome": "none",
            "role": "worker",
            "provider": {"id": "claude"},
            "host": {"id": "local", "kind": "local"},
            "stage": {"worker": "coding", "dispatch": "running"},
            "nextAction": {"kind": kind},
            "liveness": liveness,
            "evidence": {"durable": False, "liveStatus": "live"},
        },
    }
    if evidence:
        row["projection"]["evidence"]["lastObservedAt"] = evidence
    row.update(extra)
    return row


def envelope(workers, has_more=False, total=UNKNOWN, **result):
    page = {"hasMore": has_more, "limit": 100}
    if total is not UNKNOWN:
        page["total"] = total
    body = {
        "workers": workers,
        "page": page,
        "scope": {"source": "all"},
        "counts": {"active": 1},
    }
    body.update(result)
    return {"result": body}


def page(workers, cycle=1, namespace="orca-a", base=0, **kw):
    return parse_page(envelope(workers, **kw), namespace, cycle, base)


def run_cycle(
    previous,
    workers,
    cycle,
    namespace="orca-a",
    cap=False,
    error=None,
    has_more=False,
    total=UNKNOWN,
):
    parsed = page(
        workers, cycle=cycle, namespace=namespace, has_more=has_more, total=total
    )
    return merge(previous, [parsed], cap, error, None)


def by_id(snapshot, dispatch):
    return next(r for r in snapshot.rows if r.dispatch_id == dispatch)


# -- T32: envelope is strict, rows are lenient ---------------------------------------

BROKEN = {
    "empty object": {},
    "not an object": [],
    "result null": {"result": None},
    "result missing": {"other": 1},
    "result not object": {"result": []},
    "workers missing": {"result": {"page": {"hasMore": False}}},
    "workers not a list": {"result": {"workers": {}, "page": {"hasMore": False}}},
    "workers string": {"result": {"workers": "x", "page": {"hasMore": False}}},
    "workers null": {"result": {"workers": None, "page": {"hasMore": False}}},
    "page missing": {"result": {"workers": []}},
    "hasMore missing": {"result": {"workers": [], "page": {}}},
    "hasMore string false": {"result": {"workers": [], "page": {"hasMore": "false"}}},
    "hasMore null": {"result": {"workers": [], "page": {"hasMore": None}}},
    "hasMore int": {"result": {"workers": [], "page": {"hasMore": 0}}},
}


@pytest.mark.parametrize("name", sorted(BROKEN))
def test_broken_envelope_is_a_shape_error_and_leaves_the_previous_snapshot(name):
    previous, _ = run_cycle(None, [worker()], cycle=1)
    frozen = copy.deepcopy(previous)
    with pytest.raises(ShapeError):
        merge(previous, [parse_page(BROKEN[name], "orca-a", 2)], False, None, None)
    assert previous == frozen


def test_missing_scope_and_total_are_unknown_for_that_field_only():
    body = envelope([worker()])
    del body["result"]["scope"]
    parsed = parse_page(body, "orca-a", 1)
    assert parsed.scope is UNKNOWN and parsed.total is UNKNOWN
    assert parsed.counts == {"active": 1}
    assert len(parsed.rows) == 1 and parsed.has_more is False


@pytest.mark.parametrize("bad_total", [-1, "5", True, 1.5, None])
def test_total_that_is_not_a_non_negative_integer_is_unknown(bad_total):
    body = envelope([worker()])
    body["result"]["page"]["total"] = bad_total
    assert parse_page(body, "orca-a", 1).total is UNKNOWN
    body["result"]["page"]["total"] = 0
    assert parse_page(body, "orca-a", 1).total == 0


def test_missing_inner_projection_key_is_unknown_in_that_row_not_an_error():
    w = worker()
    del w["projection"]["liveness"]["verdict"]
    del w["projection"]["nextAction"]
    row = page([w]).rows[0]
    assert row.liveness_verdict is UNKNOWN and row.next_action_kind is UNKNOWN
    assert row.liveness_source == "terminal"
    assert {"liveness_verdict", "next_action_kind"} <= set(row.absent_fields)
    w2 = worker()
    del w2["projection"]
    assert page([w2]).rows[0].outcome is UNKNOWN


def test_json_null_and_absent_both_give_unknown_and_five_values_are_distinct():
    w = worker(taskId=None)
    del w["runId"]
    row = page([w]).rows[0]
    assert row.task_id is UNKNOWN and row.run_id is UNKNOWN
    for other in (None, 0, False, ""):
        assert UNKNOWN is not other and UNKNOWN != other
    assert repr(UNKNOWN) == "UNKNOWN"
    assert copy.deepcopy(UNKNOWN) is UNKNOWN and copy.copy(UNKNOWN) is UNKNOWN
    # a source value that is the text "unknown" is a string, not the sentinel
    assert page([worker(taskId="UNKNOWN")]).rows[0].task_id == "UNKNOWN"


def test_non_object_rows_are_counted_and_skipped_and_text_is_sanitized():
    parsed = page(
        [worker("w-1"), "text", 5, None, worker("w-2\nsecond-line", stage=None)]
    )
    assert [r.dispatch_id for r in parsed.rows] == ["w-1", "w-2 second-line"]
    assert parsed.malformed_rows == 3 and parsed.raw_count == 5
    w = worker()
    w["projection"]["stage"]["detail"] = "line1\nline2\x1b[31m"
    w["projection"]["stage"]["activity"] = "act\nivity"
    w["projection"]["role"] = "wo\nrker"
    row = page([w]).rows[0]
    assert row.stage_detail == "line1\nline2" and row.stage_activity == "act\nivity"
    assert row.role == "wo rker"


def test_unexpected_keys_are_counted_and_never_kept():
    w = worker(agentTerminalHandle="term_secret_handle", surprise={"x": 1})
    w["resource"]["terminalHandle"] = "term_other_secret"
    w["projection"]["mystery"] = "mystery-value"
    w["projection"]["nextAction"]["extra"] = "nested-extra-value"
    row = page([w]).rows[0]
    assert row.unrecognised_keys == 5
    text = repr(row)
    for leaked in (
        "term_secret_handle",
        "term_other_secret",
        "mystery",
        "nested-extra-value",
        "surprise",
    ):
        assert leaked not in text
    assert page([worker()]).rows[0].unrecognised_keys == 0


def test_fixture_frozen_is_never_set_by_parse_page():
    assert page([worker(fixtureOnly={"frozen": True})]).rows[0].fixture_frozen is False


# -- identity ---------------------------------------------------------------------------


@pytest.mark.parametrize("missing", ["absent", "null", "empty", "blank"])
def test_row_without_dispatch_id_keeps_a_per_cycle_identity_and_never_merges(missing):
    def anonymous():
        w = worker()
        if missing == "absent":
            del w["dispatchId"]
        else:
            w["dispatchId"] = {"null": None, "empty": "", "blank": "  \t "}[missing]
        return w

    snapshot, coverage = run_cycle(
        None, [anonymous(), anonymous(), worker("w-1")], cycle=1
    )
    anon = [r for r in snapshot.rows if r.dispatch_id is UNKNOWN]
    assert len(anon) == 2 and len({r.identity for r in anon}) == 2
    assert all(IDENTITY_UNKNOWN in r.flags and r.identity_unknown for r in anon)
    assert coverage.duplicates == 0 and coverage.identity_unknown_rows == 2
    assert anon[0].identity[1] is UNKNOWN and anon[0].identity[2] == 1


def test_anonymous_rows_are_replaced_by_a_complete_cycle_and_kept_by_a_partial_one():
    def anonymous():
        w = worker()
        del w["dispatchId"]
        return w

    first, _ = run_cycle(None, [anonymous(), worker("w-1")], cycle=1)
    complete, _ = run_cycle(first, [anonymous(), worker("w-1")], cycle=2)
    anon = [r for r in complete.rows if r.identity_unknown]
    assert len(anon) == 1 and anon[0].cycle == 2 and anon[0].reobserved

    partial, cov = run_cycle(
        first, [anonymous(), worker("w-1")], cycle=2, cap=True, has_more=True
    )
    assert cov.partial
    anon = sorted(
        (r for r in partial.rows if r.identity_unknown), key=lambda r: r.cycle
    )
    assert [(r.cycle, r.reobserved) for r in anon] == [(1, False), (2, True)]
    # rows with a real identity are unaffected either way
    for snap in (complete, partial):
        assert len([r for r in snap.rows if r.dispatch_id == "w-1"]) == 1


def test_same_dispatch_id_under_two_namespaces_stays_two_rows():
    pages = [
        page([worker("w-1")], namespace="orca-a"),
        page([worker("w-1")], namespace="orca-b", base=1),
    ]
    snapshot, coverage = merge(None, pages, False, None, None)
    assert len(snapshot.rows) == 2 and coverage.duplicates == 0
    assert {r.identity for r in snapshot.rows} == {("orca-a", "w-1"), ("orca-b", "w-1")}


# -- duplicates, order, time (T22) -----------------------------------------------------


def test_duplicates_within_a_cycle_are_dropped_and_counted_exactly():
    pages = [
        page([worker("w-1", observed=T1), worker("w-1", observed=T1), worker("w-2")]),
        page([worker("w-1", observed=T1), worker("w-3")], base=3),
    ]
    snapshot, coverage = merge(None, pages, False, None, None)
    assert [r.dispatch_id for r in snapshot.rows] == ["w-1", "w-2", "w-3"]
    assert coverage.duplicates == 2 and coverage.collected == 3


def test_within_a_cycle_the_newer_timestamp_wins_and_no_common_timestamp_flags_order_unknown():
    snapshot, _ = run_cycle(
        None,
        [
            worker("w-1", observed=T0, kind="old"),
            worker("w-1", observed=T2, kind="new"),
        ],
        1,
    )
    assert snapshot.rows[0].next_action_kind == "new" and snapshot.rows[0].flags == ()
    snapshot, _ = run_cycle(
        None,
        [
            worker("w-1", observed=T2, kind="first"),
            worker("w-1", observed=T0, kind="late"),
        ],
        1,
    )
    assert snapshot.rows[0].next_action_kind == "first"
    snapshot, _ = run_cycle(None, [worker("w-1", kind="a"), worker("w-1", kind="b")], 1)
    assert (
        snapshot.rows[0].flags == (ORDER_UNKNOWN,)
        and snapshot.rows[0].next_action_kind == "a"
    )


def test_an_older_observed_at_never_overwrites_a_newer_one():
    first, _ = run_cycle(None, [worker("w-1", observed=T2, kind="newer-data")], cycle=1)
    second, _ = run_cycle(
        first, [worker("w-1", observed=T0, kind="older-data")], cycle=2
    )
    row = by_id(second, "w-1")
    assert row.next_action_kind == "newer-data" and row.liveness_observed_at == T2
    assert (
        row.flags == (CONFLICT_BACKWARD,)
        and row.reobserved
        and row.last_seen_cycle == 2
    )


def test_newer_and_equal_timestamps_let_the_newer_cycle_win():
    first, _ = run_cycle(None, [worker("w-1", observed=T1, kind="c1")], cycle=1)
    newer, _ = run_cycle(first, [worker("w-1", observed=T2, kind="c2")], cycle=2)
    assert (
        by_id(newer, "w-1").next_action_kind == "c2" and by_id(newer, "w-1").flags == ()
    )
    equal, _ = run_cycle(first, [worker("w-1", observed=T1, kind="c2")], cycle=2)
    assert (
        by_id(equal, "w-1").next_action_kind == "c2" and by_id(equal, "w-1").flags == ()
    )


def test_missing_both_timestamps_or_no_common_field_or_unparsable_flags_order_unknown():
    first, _ = run_cycle(None, [worker("w-1", kind="c1")], cycle=1)
    second, _ = run_cycle(first, [worker("w-1", kind="c2")], cycle=2)
    row = by_id(second, "w-1")
    assert row.flags == (ORDER_UNKNOWN,) and row.next_action_kind == "c2"
    # no common field: liveness in one cycle, evidence in the other
    a, _ = run_cycle(None, [worker("w-1", observed=T1)], cycle=1)
    b, _ = run_cycle(a, [worker("w-1", evidence=T2, kind="c2")], cycle=2)
    assert by_id(b, "w-1").flags == (ORDER_UNKNOWN,)
    # unparsable counts as absent
    c, _ = run_cycle(a, [worker("w-1", observed="not a time", kind="c3")], cycle=2)
    assert (
        by_id(c, "w-1").flags == (ORDER_UNKNOWN,)
        and by_id(c, "w-1").next_action_kind == "c3"
    )


def test_evidence_timestamps_are_compared_with_evidence_timestamps():
    a, _ = run_cycle(None, [worker("w-1", evidence=T2, kind="newer")], cycle=1)
    b, _ = run_cycle(a, [worker("w-1", evidence=T0, kind="older")], cycle=2)
    assert by_id(b, "w-1").next_action_kind == "newer" and by_id(b, "w-1").flags == (
        CONFLICT_BACKWARD,
    )


def test_a_flag_clears_on_the_next_clean_cycle():
    a, _ = run_cycle(None, [worker("w-1", kind="c1")], cycle=1)
    b, _ = run_cycle(a, [worker("w-1", kind="c2")], cycle=2)
    c, _ = run_cycle(
        b, [worker("w-1", observed=T1, kind="c3")], cycle=3
    )  # b has no liveness stamp: unknown again
    d, _ = run_cycle(c, [worker("w-1", observed=T2, kind="c4")], cycle=4)
    assert by_id(d, "w-1").flags == ()


# -- the row set across cycles ---------------------------------------------------------


def test_a_row_missing_from_the_next_cycle_stays_with_reobserved_false():
    first, _ = run_cycle(None, [worker("w-1"), worker("w-2")], cycle=1)
    second, _ = run_cycle(first, [worker("w-2")], cycle=2)
    assert [(r.dispatch_id, r.reobserved, r.last_seen_cycle) for r in second.rows] == [
        ("w-2", True, 2),
        ("w-1", False, 1),
    ]
    third, _ = run_cycle(second, [worker("w-2")], cycle=3)
    assert (
        by_id(third, "w-1").reobserved is False
        and by_id(third, "w-1").last_seen_cycle == 1
    )


def test_coverage_records_totals_empty_pages_has_more_and_changes():
    p1 = page([worker("w-1")], total=250, has_more=True)
    p2 = page([worker("w-2")], total=251, has_more=True, base=1)
    snapshot, cov = merge(None, [p1, p2], True, None, None)
    assert (
        cov.page_totals == (250, 251)
        and cov.total_changed
        and cov.reported_total == 251
    )
    assert (
        cov.has_more_at_stop
        and cov.stopped_by_cap
        and cov.partial
        and cov.state == "PARTIAL"
    )
    assert snapshot.total == 251 and snapshot.has_more is True

    empty = page([], total=5, base=1)
    _, cov = merge(
        None, [page([worker("w-1")], total=5, has_more=True), empty], False, None, None
    )
    assert cov.empty_page == 2 and cov.partial

    _, cov = merge(None, [page([worker("w-1")], total=3)], False, None, None)
    assert cov.state == "MISMATCH" and cov.mismatch and not cov.partial
    _, cov = merge(None, [page([worker("w-1")], total=1)], False, None, None)
    assert cov.state == "COMPLETE"
    _, cov = merge(None, [page([worker("w-1")], total=1)], False, "timeout", None)
    assert cov.partial and cov.stopped_by_error == "timeout"
    _, cov = merge(None, [page([worker("w-1")])], False, None, None)
    assert cov.reported_total is UNKNOWN and cov.state == "COMPLETE"


def test_merge_needs_at_least_one_page():
    with pytest.raises(ValueError):
        merge(None, [], False, None, None)


def test_envelope_fields_are_sanitized_and_counted():
    body = envelope(
        [worker()],
        warnings=["warn\x1b[31m one", 5, "two\nlines"],
        scope={"source": "bo\x07und"},
    )
    parsed = parse_page(body, "orca-a", 1)
    assert parsed.warnings == ("warn one", "two lines")
    assert parsed.scope == {"source": "bound"}
    assert parsed.limit == 100


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (T0, 1794139200.0),
        ("2026-11-08T12:00:00+00:00", 1794139200.0),
        ("2026-11-08T12:00:00", 1794139200.0),
        (1794139200, 1794139200.0),
        (1794139200000, 1794139200.0),
        ("garbage", None),
        ("", None),
        (True, None),
        (None, None),
        (float("nan"), None),
        (UNKNOWN, None),
    ],
)
def test_parse_timestamp(value, expected):
    assert parse_timestamp(value) == expected


# -- R2: question rows (probe shapes: evidence files 03, 14 and 24 of the gate research) ----------

QRUN = "run_14cfcbd8edf2"
OTHER_RUN = "run_c1badaa6576b"


def qrow(i=1, **extra):
    row = {
        "id": f"msg_{i:012x}",
        "run_id": QRUN,
        "delivery_contract": "current_delivery",
        "from_handle": "term_synthetic",
        "to_handle": f"run:{QRUN}",
        "subject": f"probe question {i}",
        "body": "SECRET BODY synthetic",
        "type": "question",
        "priority": "normal",
        "thread_id": None,
        "payload": {"secret": "synthetic"},
        "created_at": f"2026-11-11T20:01:{10 + i:02d}Z",
        "delivered_at": None,
    }
    row.update(extra)
    return row


def qenvelope(rows, run=QRUN):
    return {
        "id": "env",
        "ok": True,
        "result": {
            "acknowledged": None,
            "count": len(rows),
            "messages": rows,
            "runId": run,
        },
    }


def test_a_two_row_envelope_parses_to_two_question_rows():
    parsed = parse_questions(qenvelope([qrow(2), qrow(1)]), "orca-a", 3, QRUN)
    assert len(parsed.rows) == 2 and parsed.raw_count == 2
    first = parsed.rows[0]
    assert isinstance(first, Question)
    assert (first.qid, first.run_id, first.subject) == (
        "msg_000000000002",
        QRUN,
        "probe question 2",
    )
    assert (first.priority, first.from_handle, first.namespace) == (
        "normal",
        "term_synthetic",
        "orca-a",
    )
    assert first.thread_id is UNKNOWN  # a JSON null is a fact the source did not give
    assert first.created_at == "2026-11-11T20:01:12Z"
    assert isinstance(first.created_epoch, float)
    assert (parsed.cycle, parsed.run_id) == (3, QRUN)
    assert parsed.contradictory_rows == parsed.malformed_rows == parsed.duplicates == 0


@pytest.mark.parametrize(
    "broken",
    [
        {},
        [],
        None,
        {"result": None},
        {"result": []},
        {"result": {"runId": QRUN}},
        {"result": {"messages": None}},
        {"result": {"messages": {}}},
        {"result": {"messages": "x"}},
        {"result": {"messages": 5}},
        {"ok": False, "error": {"code": "consumer_fenced"}},
    ],
)
def test_result_messages_must_be_a_json_list(broken):
    with pytest.raises(ShapeError):
        parse_questions(broken, "orca-a", 1, QRUN)


def test_a_status_row_and_a_wrong_run_row_are_dropped_and_counted():
    rows = [
        qrow(1),
        qrow(2, type="status"),
        qrow(3, run_id=OTHER_RUN),
        qrow(4, type=None),
        qrow(5, type="Question"),
    ]
    parsed = parse_questions(qenvelope(rows), "orca-a", 1, QRUN)
    assert [q.qid for q in parsed.rows] == ["msg_000000000001"]
    assert parsed.contradictory_rows == 4 and parsed.raw_count == 5


def test_without_a_requested_run_the_reported_run_is_the_check():
    rows = [qrow(1), qrow(2, run_id=OTHER_RUN)]
    parsed = parse_questions(qenvelope(rows), "orca-a", 1)
    assert len(parsed.rows) == 1 and parsed.contradictory_rows == 1
    assert parsed.run_id == QRUN


def test_a_response_for_another_run_is_dropped_even_for_rows_without_a_run_id():
    row = {"id": "msg_x", "type": "question"}  # no run_id of its own
    parsed = parse_questions(
        qenvelope([row, qrow(1)], run=OTHER_RUN), "orca-a", 1, QRUN
    )
    assert parsed.rows == () and parsed.contradictory_rows == 2


def test_absent_fields_read_unknown_and_never_none_zero_or_false():
    parsed = parse_questions(
        qenvelope([{"id": "msg_x", "type": "question"}]), "orca-a", 1, QRUN
    )
    (row,) = parsed.rows
    for name in ("run_id", "from_handle", "subject", "priority", "thread_id"):
        assert getattr(row, name) is UNKNOWN, name
    assert row.created_at is UNKNOWN and row.created_epoch is UNKNOWN


def test_an_unparsable_created_time_has_no_epoch_but_keeps_its_text():
    (row,) = parse_questions(
        qenvelope([qrow(1, created_at="last tuesday")]), "orca-a", 1, QRUN
    ).rows
    assert row.created_at == "last tuesday" and row.created_epoch is UNKNOWN


def test_markup_in_a_subject_stays_literal_text():
    (row,) = parse_questions(
        qenvelope([qrow(1, subject="[bold]loud[/bold] [link=x]y[/link]")]),
        "orca-a",
        1,
        QRUN,
    ).rows
    assert row.subject == "[bold]loud[/bold] [link=x]y[/link]"


def test_no_parsed_object_keeps_a_body_payload_or_recipient():
    parsed = parse_questions(qenvelope([qrow(1)]), "orca-a", 1, QRUN)
    (row,) = parsed.rows
    for name in ("body", "payload", "to_handle", "dispatch_id", "delivered_at"):
        assert not hasattr(row, name) and not hasattr(parsed, name), name
    assert "SECRET" not in repr(parsed) and "run:" not in repr(parsed)


INJECTIONS = [
    "a\x1b[31mred\x1b[0mb",
    "link \x1b]8;;http://evil.example\x07click\x1b]8;;\x07 end",
    "bidi ‮evil‬ text",
    "c1 \x9b31m and \x9d0;title\x9c done",
    "unterminated \x1b]0;title and more",
    "bell \x07 and \x00 nul",
]


@pytest.mark.parametrize("subject", INJECTIONS)
def test_an_injection_subject_leaves_no_escape_c1_or_format_character(subject):
    import unicodedata

    (row,) = parse_questions(
        qenvelope([qrow(1, subject=subject, from_handle=subject, priority=subject)]),
        "orca-a",
        1,
        QRUN,
    ).rows
    for value in (row.subject, row.from_handle, row.priority):
        assert isinstance(value, str)
        for ch in value:
            assert ch != "\x1b" and not 0x80 <= ord(ch) <= 0x9F, repr(value)
            assert unicodedata.category(ch) not in ("Cf", "Cc"), repr(value)


def test_a_row_without_an_id_has_no_identity_and_duplicate_ids_are_counted():
    rows = [qrow(1), qrow(1), qrow(2, id=None), qrow(3, id="  "), qrow(4, id=7), "x", 5]
    parsed = parse_questions(qenvelope(rows), "orca-a", 1, QRUN)
    assert parsed.duplicates == 1 and parsed.malformed_rows == 2
    assert parsed.identity_unknown_rows == 3
    flagged = [q for q in parsed.rows if q.identity_unknown]
    assert len(flagged) == 3 and all(q.qid is UNKNOWN for q in flagged)
    assert [q.qid for q in parsed.rows if not q.identity_unknown] == [
        "msg_000000000001"
    ]


def test_identity_comes_from_message_id_and_never_a_dispatch_id():
    (row,) = parse_questions(
        qenvelope([qrow(1, dispatchId="w-001", dispatch_id="w-002")]), "orca-a", 1, QRUN
    ).rows
    assert row.qid == "msg_000000000001"
    assert "w-001" not in repr(row) and "w-002" not in repr(row)


def test_a_non_ascii_deeply_nested_subject_becomes_text_not_an_error():
    nested = {"a": {"b": {"c": [1, 2, {"d": "é"}]}}}
    (row,) = parse_questions(
        qenvelope([qrow(1, subject=nested)]), "orca-a", 1, QRUN
    ).rows
    assert isinstance(row.subject, str) and "é" in row.subject
