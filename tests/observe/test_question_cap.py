"""The 100-row bound of the message read (T54; REPORT evidence file 14: 104 messages, 100 rows).

``check --all`` returns the newest 100 rows with no total and no truncation field, so a read of
exactly 100 rows may have lost older ones. The observer discloses that, keeps what it saw, and
never takes a count from ``result.count``.
"""

from __future__ import annotations

import copy
import json

from superclaude.cli.observe.adapter import LiveSource
from superclaude.cli.observe.collector import Collector
from superclaude.cli.observe.export import record_text, snapshot_json
from superclaude.cli.observe.parse import load_fixture
from superclaude.cli.observe.render import screen_lines
from superclaude.cli.observe.terminal import resolve_policy
from superclaude.cli.observe.view import (
    QUESTIONS_DISCLOSURE,
    QUESTIONS_WINDOW_FULL,
    Session,
    build_view,
)
from tests.observe.conftest import (
    QRUN,
    FakeDiscover,
    FakeRunner,
    make_envelope,
    make_question_envelope,
    make_question_rows,
    make_rows,
    routed_runner_responses,
)


def cap_envelope():
    return copy.deepcopy(load_fixture("question-cap-100").cycle(0).envelope)


def collector_for(messages, clock, argv_log, run_id):
    worker = (0, json.dumps(make_envelope(make_rows(3, 1), total=3)))
    runner = FakeRunner(argv_log, [routed_runner_responses(worker, messages)])
    return Collector(
        LiveSource(runner, FakeDiscover(argv_log)), clock, run_id=run_id, questions=True
    )


def ok(envelope):
    return 0, json.dumps(envelope)


def screen(result, clock, width=160, height=60):
    view = build_view(result, Session(), clock)
    return view, screen_lines(view, resolve_policy({}, "utf-8", {}, width, height))


def test_the_recorded_shape_fixture_is_exactly_100_question_rows_newest_first():
    envelope = cap_envelope()
    rows = envelope["result"]["messages"]
    assert len(rows) == 100 and all(r["type"] == "question" for r in rows)
    stamps = [r["created_at"] for r in rows]
    assert stamps == sorted(
        stamps, reverse=True
    )  # newest first, as check --all gives them
    assert len({r["id"] for r in rows}) == 100
    # No total, hasMore or truncation field: the loss cannot be seen in the reply itself.
    assert set(envelope["result"]) == {"acknowledged", "count", "messages", "runId"}


def test_a_100_row_reply_sets_window_full_and_the_panel_says_so(fake_clock, argv_log):
    collector = collector_for(ok(cap_envelope()), fake_clock, argv_log, "run-b")
    result = collector.run_once()
    assert result.question_state == "OK" and result.questions.window_full is True
    view, lines = screen(result, fake_clock)
    assert view.questions.window_full_text == QUESTIONS_WINDOW_FULL
    assert "window full: older questions may be missing" in lines
    flat = " ".join(" ".join(lines).split())
    assert QUESTIONS_DISCLOSURE in flat
    assert "bounded best effort; coverage unknown" in flat
    assert "seen, not resolved: 100+ (window full) |" in flat
    record = record_text(view)
    assert "window full: older questions may be missing" in record
    assert json.loads(snapshot_json(view))["questions"]["windowFull"] is True


def test_a_99_row_reply_is_not_window_full(fake_clock, argv_log):
    envelope = cap_envelope()
    envelope["result"]["messages"].pop()
    envelope["result"]["count"] = 99
    result = collector_for(ok(envelope), fake_clock, argv_log, "run-b").run_once()
    assert result.questions.window_full is False
    view, lines = screen(result, fake_clock)
    assert view.questions.window_full_text is None
    assert not any("window full" in line for line in lines)
    assert "seen, not resolved: 99 |" in " ".join(lines)
    # exactly 101 rows (more than the bound) is not "exactly 100" either
    over = make_question_envelope(make_question_rows(101))
    again = collector_for(ok(over), fake_clock, argv_log, QRUN).run_once()
    assert again.questions.window_full is False


def test_a_moved_window_keeps_the_dropped_questions_and_the_open_total_does_not_fall(
    fake_clock, argv_log
):
    first = make_question_envelope(make_question_rows(100, start=0))
    moved = make_question_envelope(make_question_rows(100, start=10))  # newest 100 only
    collector = collector_for([ok(first), ok(moved)], fake_clock, argv_log, QRUN)
    one = collector.run_once()
    two = collector.run_once()
    assert one.questions.open_total == 100 and two.questions.open_total == 110
    assert two.questions.window_full is True
    gone = [r for r in two.questions.records if not r.in_window]
    assert len(gone) == 10
    assert {r.question.qid for r in gone} == {f"msg_{i:012x}" for i in range(10)}
    view, lines = screen(two, fake_clock, height=200)
    assert view.questions.counts_line.startswith(
        "seen, not resolved: 110+ (window full) |"
    )
    assert sum("no longer in source window" in line for line in lines) == 10
    assert "window full: older questions may be missing" in lines


def test_the_panel_never_prints_a_total_taken_from_result_count(fake_clock, argv_log):
    envelope = cap_envelope()
    envelope["result"]["count"] = 7777  # a reply whose count disagrees with its rows
    result = collector_for(ok(envelope), fake_clock, argv_log, "run-b").run_once()
    view, lines = screen(result, fake_clock, height=200)
    everything = "\n".join([*lines, record_text(view), snapshot_json(view)])
    assert "7777" not in everything
    assert view.questions.counts_line.startswith(
        "seen, not resolved: 100+ (window full) |"
    )
    assert json.loads(snapshot_json(view))["questions"]["observedOpen"] == 100


def test_no_message_argv_has_peek_and_every_one_has_types_question(
    fake_clock, argv_log
):
    first = make_question_envelope(make_question_rows(100))
    collector = collector_for(
        [ok(first), ok(cap_envelope())], fake_clock, argv_log, QRUN
    )
    collector.run_once()
    collector.run_once()
    message = [a for a in argv_log if a[1:3] == ["orchestration", "check"]]
    assert len(message) == 2
    for argv in message:
        assert "--peek" not in argv
        assert argv[argv.index("--types") + 1] == "question"
        assert argv[argv.index("--all") : argv.index("--all") + 3] == [
            "--all",
            "--types",
            "question",
        ]
    assert not any(a for a in argv_log if "--peek" in a or "--ack" in a)
