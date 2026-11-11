"""Question retention tests (T11, T12, T46 in acceptance-tests.md; FR-17 in the PRD)."""

from __future__ import annotations

import dataclasses

import pytest

from superclaude.cli.observe.parse import UNKNOWN, Question
from superclaude.cli.observe.questions import (
    NO_LONGER_IN_WINDOW,
    RETENTION_BOUND,
    RETENTION_EXCEEDED,
    QuestionState,
    merge_questions,
    window_is_full,
)

RUN = "run_14cfcbd8edf2"
OTHER = "run_c1badaa6576b"


def q(i, run=RUN, created=None, **kw):
    epoch = 1_794_000_000.0 + i if created is None else created
    return Question(
        qid=f"msg_{i:06d}",
        run_id=run,
        namespace="orca-a",
        subject=f"question {i}",
        created_at="2026-11-11T20:01:11Z",
        created_epoch=epoch,
        **kw,
    )


def ids(state):
    return [r.question.qid for r in state.records]


def test_a_good_read_retains_rows_oldest_created_first_unknown_last():
    rows = [q(3), q(1, created=UNKNOWN), q(2)]
    state = merge_questions(None, rows, 1, False, True, RUN)
    assert ids(state) == ["msg_000002", "msg_000003", "msg_000001"]
    assert state.open_total == 3 and state.open_total_text == "3"
    assert state.retained == 3 and state.evicted == 0
    assert (state.last_read_cycle, state.never_read) == (1, False)
    assert all(r.in_window and r.first_seen_cycle == 1 for r in state.records)


def test_nothing_is_ever_closed_and_closure_evidence_is_unavailable():
    state = merge_questions(None, [q(1)], 1, False, True, RUN)
    assert state.closure_evidence == "unavailable (no source)"
    assert not any("closed" in f.name for f in dataclasses.fields(state.records[0]))
    assert not hasattr(state.records[0], "closed")


def test_t11_a_failed_read_keeps_every_record_and_changes_nothing():
    state = merge_questions(None, [q(1), q(2)], 1, True, True, RUN)
    after = merge_questions(state, [], 2, False, False, RUN)
    assert after is state
    assert after.window_full is True and after.last_read_cycle == 1
    assert ids(after) == ids(state)
    assert all(r.in_window for r in after.records)


def test_t12_a_question_missing_from_the_next_good_read_stays_marked():
    first = merge_questions(None, [q(1), q(2)], 1, False, True, RUN)
    second = merge_questions(first, [q(2), q(3)], 2, False, True, RUN)
    by_id = {r.question.qid: r for r in second.records}
    assert set(by_id) == {"msg_000001", "msg_000002", "msg_000003"}
    assert by_id["msg_000001"].in_window is False
    assert by_id["msg_000001"].status_text == NO_LONGER_IN_WINDOW
    assert by_id["msg_000001"].last_seen_cycle == 1
    assert by_id["msg_000002"].in_window and by_id["msg_000002"].first_seen_cycle == 1
    assert by_id["msg_000002"].last_seen_cycle == 2
    assert by_id["msg_000003"].first_seen_cycle == 2
    assert (
        second.open_total == 3
    )  # a question leaving the window never lowers the total
    third = merge_questions(second, [q(1)], 3, False, True, RUN)  # it comes back
    assert {r.question.qid: r.in_window for r in third.records}["msg_000001"] is True


def test_an_empty_good_read_keeps_everything_marked_and_never_closes():
    first = merge_questions(None, [q(1), q(2)], 1, False, True, RUN)
    second = merge_questions(first, [], 2, False, True, RUN)
    assert second.open_total == 2
    assert all(not r.in_window for r in second.records)


def test_a_handled_question_that_orca_still_returns_is_listed_again_as_open():
    # Known limit: ``check --all`` rows carry no read or acknowledged marker (REPORT 2.2,
    # steps 8 and 9), so the observer cannot tell a handled question from a fresh one.
    first = merge_questions(None, [q(1)], 1, False, True, RUN)
    handled_and_still_returned = merge_questions(first, [q(1)], 2, False, True, RUN)
    (record,) = handled_and_still_returned.records
    assert record.in_window and handled_and_still_returned.open_total == 1
    assert handled_and_still_returned.closure_evidence == "unavailable (no source)"


def test_t46_1001_distinct_questions_never_lower_the_open_total():
    state = None
    totals = []
    for start in range(0, 1001, 100):
        batch = [q(i) for i in range(start, min(start + 100, 1001))]
        state = merge_questions(state, batch, start // 100 + 1, True, True, RUN)
        totals.append(state.open_total)
    assert totals == sorted(totals) and totals[-1] == 1001
    assert state.retained == RETENTION_BOUND == 1000
    assert state.evicted == 1 and state.open_total == 1001
    assert state.open_total_text == RETENTION_EXCEEDED == "unknown (retention exceeded)"
    assert "msg_000000" not in ids(state)  # the oldest created is the one evicted
    assert "msg_001000" in ids(state)
    again = merge_questions(state, [], 99, False, False, RUN)
    assert again.open_total == 1001 and again.retained == 1000


def test_two_runs_with_the_same_message_id_stay_two_records():
    rows = [q(1, run=RUN), q(1, run=OTHER)]
    state = merge_questions(None, rows, 1, False, True, RUN)
    assert state.retained == 2
    assert {r.key for r in state.records} == {
        (OTHER, "msg_000001"),
        (RUN, "msg_000001"),
    }


def test_a_row_without_its_own_run_uses_the_run_that_was_read():
    state = merge_questions(None, [q(1, run=UNKNOWN)], 1, False, True, RUN)
    assert state.records[0].key == (RUN, "msg_000001")


def test_rows_without_an_identity_are_counted_and_not_retained():
    rows = [q(1), dataclasses.replace(q(2), qid=UNKNOWN, flags=("identity unknown",))]
    state = merge_questions(None, rows, 1, False, True, RUN)
    assert state.retained == 1 and state.identity_unknown_rows == 1


@pytest.mark.parametrize(
    "n,expected", [(99, False), (100, True), (101, False), (0, False)]
)
def test_window_full_means_exactly_100_rows(n, expected):
    assert window_is_full(n) is expected


def test_window_full_is_carried_by_the_state_and_cleared_by_a_smaller_read():
    state = merge_questions(None, [q(1)], 1, True, True, RUN)
    assert state.window_full is True
    state = merge_questions(state, [q(1)], 2, False, True, RUN)
    assert state.window_full is False


def test_merge_is_pure_the_previous_state_is_not_modified():
    first = merge_questions(None, [q(1)], 1, False, True, RUN)
    snapshot = (first.records, first.evicted, first.window_full)
    merge_questions(first, [q(2)], 2, True, True, RUN)
    assert (first.records, first.evicted, first.window_full) == snapshot
    assert isinstance(first, QuestionState)
    with pytest.raises(dataclasses.FrozenInstanceError):
        first.evicted = 5  # type: ignore[misc]
