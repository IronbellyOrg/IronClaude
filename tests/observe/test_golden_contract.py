"""Contract tests over the four redacted golden worker-list samples (release-gates.md data gate; T32)."""

from __future__ import annotations

import copy
import json
import re
from importlib import resources

import pytest
from rich.cells import cell_len

from superclaude.cli.observe.adapter import LiveSource
from superclaude.cli.observe.collector import Collector, FixtureSource
from superclaude.cli.observe.parse import FIXTURE_PACKAGE, load_fixture
from superclaude.cli.observe.render import screen_lines
from superclaude.cli.observe.terminal import resolve_policy
from superclaude.cli.observe.view import Session, build_view
from tests.observe import record_golden
from tests.observe.conftest import FakeDiscover, FakeRunner
from tests.observe.test_fixtures import SENSITIVE

GOLDEN = ("golden-success", "golden-missing", "golden-stale", "golden-contradictory")


def result_of(name, clock, cycles=1):
    collector = Collector(FixtureSource(name), clock)
    for _ in range(cycles):
        result = collector.run_once()
    return result


def view_of(result, clock, show_historical=True):
    return build_view(result, Session(show_historical=show_historical), clock)


def policy(width, height=40):
    return resolve_policy({}, "utf-8", {}, width, height)


# -- success --------------------------------------------------------------------------------------------------


def test_the_success_sample_parses_and_renders_at_160_116_and_80_columns(fake_clock):
    result = result_of("golden-success", fake_clock)
    assert (
        result.state == "PARTIAL" and result.code is None
    )  # hasMore is true in the live reply
    view = view_of(result, fake_clock)
    assert len(view.all_rows) == 100 and result.coverage.reported_total == 428
    assert any(
        t.text.startswith("PARTIAL: collected 100 of reported 428")
        for t in view.counts_tokens
    )
    for width in (160, 116, 80):
        lines = screen_lines(view, policy(width))
        assert lines and all(cell_len(line) <= width for line in lines)
        assert any("collected 100 / reported 428" in line for line in lines)
    assert "scope=all" in view.header1


def test_the_success_sample_is_redacted_to_stable_placeholders():
    data = load_fixture("golden-success").cycle(0).envelope["result"]
    rows = data["workers"]
    assert all(re.fullmatch(r"w-\d{3}", r["dispatchId"]) for r in rows)
    assert all(re.fullmatch(r"run-[a-z]+", r["runId"]) for r in rows)
    assert all(re.fullmatch(r"t-\d{3}", r["taskId"]) for r in rows)
    assert all(r["projection"]["stage"]["detail"] == "redacted detail" for r in rows)
    assert (
        data["page"]["nextCursor"] == "cursor-1"
    )  # the opaque live cursor is never kept
    for row in rows:  # keys outside the verified set survive by name only
        for key in set(row) - {
            "dispatchId",
            "taskId",
            "runId",
            "workerState",
            "dispatchStatus",
            "terminalState",
            "resource",
            "projection",
        }:
            assert row[key] == "redacted"


# -- missing --------------------------------------------------------------------------------------------------------


def test_the_missing_sample_reads_scope_unknown_reported_unknown_and_unknown_for_the_removed_key(
    fake_clock,
):
    result = result_of("golden-missing", fake_clock)
    view = view_of(result, fake_clock)
    assert view.scope_text == "scope unknown" and "scope unknown" in view.header1
    assert view.collected_text.endswith("reported unknown")
    first = next(rv for rv in view.all_rows if rv.dispatch_id == "w-001")
    # the recorder removes liveness.verdict from the first row (real rows always carry it)
    assert "liveness_verdict" in first.raw.absent_fields
    assert first.liveness.startswith("unknown (")
    assert (
        dict(first.inspector)["projection.nextAction.kind"]
        != "unknown (absent in source)"
    )
    assert all(
        rv.dispatch_id != "unknown" for rv in view.all_rows
    )  # a missing inner key is not an error


# -- stale ---------------------------------------------------------------------------------------------------------------


def test_stale_comes_from_monotonic_time_since_the_last_success_not_from_sample_timestamps(
    fake_clock,
):
    collector = Collector(FixtureSource("golden-stale"), fake_clock)
    good = collector.run_once()
    fake_clock.advance(44)
    assert view_of(good, fake_clock).source_state == "OK"
    fake_clock.advance(1)
    stale = view_of(good, fake_clock)
    assert (
        stale.source_state == "STALE"
        and stale.freshness_cells[0] == "worker-list STALE 45s"
    )
    fake_clock.jump_wall(-3600)  # wall-clock jumps change nothing
    assert view_of(good, fake_clock).source_state == "STALE"
    failing = [collector.run_once() for _ in range(3)]
    view = view_of(failing[-1], fake_clock)
    assert [r.state for r in failing] == ["FAILED"] * 3
    assert (
        view.freshness_cells[0] == "worker-list FAILED (timeout) 45s"
    )  # FAILED outranks STALE
    assert failing[-1].snapshot is good.snapshot and len(view.all_rows) == 100


def test_a_fresh_poll_with_old_evidence_timestamps_is_not_stale(fake_clock):
    result = result_of("golden-success", fake_clock)
    fake_clock.jump_wall(
        20 * 60
    )  # the worker evidence is now 20 minutes old; the poll is fresh
    view = view_of(result, fake_clock)
    assert view.source_state == "OK" and view.poll_age == "0s"
    ages = {rv.evidence_age for rv in view.all_rows}
    assert "20m" in ages  # the newest evidence in the sample
    assert all(
        re.fullmatch(r"\d+[mh]|unknown", age) for age in ages
    )  # none of it is seconds old


# -- contradictory ---------------------------------------------------------------------------------------------------------


def test_the_contradictory_sample_shows_duplicates_and_a_backward_timestamp(fake_clock):
    collector = Collector(FixtureSource("golden-contradictory"), fake_clock)
    first = collector.run_once()
    assert view_of(first, fake_clock).duplicates_note == "1 duplicate rows ignored"
    second = collector.run_once()
    view = view_of(second, fake_clock)
    row = next(rv for rv in view.all_rows if rv.dispatch_id == "w-001")
    assert "conflict (time went back)" in row.flags
    assert (
        row.raw.liveness_observed_at
        != load_fixture("golden-contradictory")
        .cycle(1)
        .envelope["result"]["workers"][0]["projection"]["liveness"]["observedAt"]
    )


# -- T32: a broken envelope keeps the last good snapshot -------------------------------------------------------------------


def broken_copies():
    base = load_fixture("golden-success").cycle(0).envelope
    for label, mutate in (
        ("no result", lambda d: d.pop("result")),
        ("no workers", lambda d: d["result"].pop("workers")),
        ("no hasMore", lambda d: d["result"]["page"].pop("hasMore")),
        ("hasMore string", lambda d: d["result"]["page"].update(hasMore="false")),
        ("workers not a list", lambda d: d["result"].update(workers={})),
    ):
        copied = copy.deepcopy(base)
        mutate(copied)
        yield label, copied


@pytest.mark.parametrize("label", [label for label, _ in broken_copies()])
def test_removing_result_workers_or_has_more_gives_failed_shape_with_the_last_good_snapshot(
    fake_clock, argv_log, label
):
    good = json.dumps(load_fixture("golden-success").cycle(0).envelope)
    broken = json.dumps(dict(broken_copies())[label])
    runner = FakeRunner(argv_log, [(0, good), (0, broken)])
    collector = Collector(LiveSource(runner, FakeDiscover(argv_log)), fake_clock)
    first = collector.run_once()
    second = collector.run_once()
    assert (second.state, second.code) == ("FAILED", "shape")
    assert second.snapshot is first.snapshot and len(second.snapshot.rows) == 100
    view = view_of(second, fake_clock)
    assert view.freshness_cells[0].startswith("worker-list FAILED (shape)")
    assert second.last_success_mono == first.last_success_mono


# -- nothing sensitive is committed ---------------------------------------------------------------------------------------------


@pytest.mark.parametrize("name", GOLDEN)
def test_golden_files_hold_no_path_handle_token_credential_url_or_escape_byte(name):
    text = (
        resources.files(FIXTURE_PACKAGE)
        .joinpath(f"{name}.json")
        .read_text(encoding="utf-8")
    )
    assert "\x1b" not in text and text.isascii()
    for what, pattern in SENSITIVE.items():
        assert not pattern.search(text), f"{name}: {what}"
    assert not re.search(r"[A-Za-z0-9_+=-]{32,}", text.replace("redacted", ""))


# -- the recorder's redaction ------------------------------------------------------------------------------------------------------


def synthetic_envelope():
    return {
        "result": {
            "workers": [
                {
                    "dispatchId": "disp_9f8e7d6c5b4a39281706",
                    "taskId": "task_real_1",
                    "runId": "run_real_9",
                    "agentTerminalHandle": "term_abcdef0123456789abcdef0123456789",
                    "workerState": "running",
                    "dispatchStatus": "dispatched",
                    "terminalState": "retained",
                    "resource": {
                        "id": "res_real",
                        "worktreeId": "/home/someone/work/tree",
                        "ownerDispatchId": "disp_9f8e7d6c5b4a39281706",
                        "originDispatchId": "disp_somebody_else",
                        "terminalHandle": "term_secret",
                        "ownershipState": "owned",
                    },
                    "projection": {
                        "outcome": "in_progress",
                        "host": {"id": "host.example.com", "kind": "local"},
                        "workspace": {"id": "/home/someone/work", "kind": "worktree"},
                        "stage": {
                            "worker": "ready",
                            "dispatch": "dispatched",
                            "detail": "editing /etc/passwd with token sk-abcdef0123456789abcdef",
                            "activity": "x",
                        },
                        "nextAction": {"kind": "none"},
                        "liveness": {
                            "verdict": "live",
                            "source": "agent_status",
                            "observedAt": "2026-01-01T10:00:00Z",
                        },
                        "evidence": {
                            "durable": True,
                            "liveStatus": "fresh",
                            "lastObservedAt": "2026-01-01T09:59:00Z",
                        },
                        "attention": {"free": "text"},
                    },
                },
                {"dispatchId": "disp_second", "workerState": "idle"},
                "not an object",
            ],
            "page": {
                "hasMore": True,
                "total": 9,
                "limit": 100,
                "nextCursor": "opaque/cursor==",
            },
            "scope": {"source": "bound", "runId": "run_real_9"},
            "counts": {"released": 3, "note": "text"},
            "warnings": ["a warning with /home/path"],
        }
    }


def test_redaction_replaces_identifiers_free_text_paths_handles_and_cursors():
    out = record_golden.redact(synthetic_envelope())
    text = json.dumps(out)
    for leaked in (
        "disp_",
        "task_real",
        "run_real",
        "term_",
        "/home",
        "/etc",
        "sk-",
        "someone",
        "example.com",
        "opaque",
        "secret",
        "text",
    ):
        assert leaked not in text, leaked
    rows = out["result"]["workers"]
    assert [r["dispatchId"] for r in rows] == ["w-001", "w-002"]
    first = rows[0]
    assert (
        first["taskId"] == "t-001"
        and first["runId"] == "run-a"
        and first["agentTerminalHandle"] == "redacted"
    )
    assert (
        first["resource"]["ownerDispatchId"] == "w-001"
        and first["resource"]["originDispatchId"] == "w-ext-1"
    )
    assert (
        first["resource"]["worktreeId"] == "wt-001"
        and first["resource"]["terminalHandle"] == "redacted"
    )
    assert (
        first["projection"]["stage"]["detail"] == "redacted detail"
        and first["projection"]["attention"] == "redacted"
    )
    assert first["projection"]["host"] == {"kind": "local", "id": "host-a"}
    assert out["result"]["page"] == {
        "hasMore": True,
        "total": 9,
        "limit": 100,
        "nextCursor": "cursor-1",
    }
    assert out["result"]["scope"] == {"source": "bound"} and out["result"][
        "counts"
    ] == {"released": 3}
    assert out["result"]["warnings"] == ["redacted warning"]


def test_redaction_shifts_every_timestamp_by_one_constant_so_the_newest_lands_on_the_anchor():
    out = record_golden.redact(synthetic_envelope())
    live = out["result"]["workers"][0]["projection"]
    assert live["liveness"]["observedAt"] == "2026-11-08T12:00:00Z"
    assert (
        live["evidence"]["lastObservedAt"] == "2026-11-08T11:59:00Z"
    )  # the one-minute gap survives


def test_redaction_refuses_something_that_is_not_a_worker_list_envelope():
    for bad in ({}, {"result": {}}, {"result": {"workers": "x"}}, [], None):
        with pytest.raises(ValueError):
            record_golden.redact(bad)


def test_the_four_golden_kinds_are_derived_from_one_sample():
    kinds = record_golden.variants(record_golden.redact(synthetic_envelope()))
    assert set(kinds) == set(GOLDEN)
    assert "scope" not in kinds["golden-missing"]["cycles"][0]["result"]
    assert "total" not in kinds["golden-missing"]["cycles"][0]["result"]["page"]
    assert [c.get("fail") for c in kinds["golden-stale"]["cycles"]] == [
        None,
        "timeout",
        "timeout",
        "timeout",
    ]
    first, second = kinds["golden-contradictory"]["cycles"]
    ids = [w["dispatchId"] for w in first["result"]["workers"]]
    assert len(ids) == 3 and ids[0] == ids[-1]
    assert (
        second["result"]["workers"][0]["projection"]["liveness"]["observedAt"]
        < "2026-11-08T12:00:00Z"
    )


# -- R2: the four redacted samples of the message read (data gate; T55) ---------------------------------------------------

from superclaude.cli.observe.adapter import RunnerFailure  # noqa: E402
from superclaude.cli.observe.view import QUESTIONS_NOT_HELD  # noqa: E402
from tests.observe import record_golden_questions  # noqa: E402
from tests.observe.conftest import (  # noqa: E402
    make_envelope,
    make_rows,
    routed_runner_responses,
)

QUESTION_GOLDEN = (
    "golden-question-success",
    "golden-question-missing",
    "golden-question-stale",
    "golden-question-contradictory",
)
GOLDEN_RUN = "run-a"
MESSAGE_KEYS = set(record_golden_questions.MESSAGE_KEYS)


def golden_cycles(name):
    """The recorded cycles of one sample as raw runner replies (error envelopes exit 1)."""
    replies = []
    for cycle in load_fixture(name).cycles:
        if cycle.envelope is None:

            def fail(argv, timeout, code=cycle.fail):
                raise RunnerFailure(code)

            replies.append(fail)
        else:
            status = 0 if cycle.envelope.get("ok") is True else 1
            replies.append((status, json.dumps(cycle.envelope)))
    return replies


def golden_collector(name, clock):
    worker = (0, json.dumps(make_envelope(make_rows(2, 1), total=2)))
    runner = FakeRunner([], [routed_runner_responses(worker, golden_cycles(name))])
    return Collector(
        LiveSource(runner, FakeDiscover([])),
        clock,
        run_id=GOLDEN_RUN,
        questions=True,
    )


def test_t55_the_success_sample_parses_to_its_two_questions_at_every_width(fake_clock):
    result = golden_collector("golden-question-success", fake_clock).run_once()
    assert result.state == "OK" and result.question_state == "OK"
    state = result.questions
    assert [r.question.qid for r in state.records] == [
        "msg_000000000002",
        "msg_000000000001",
    ]  # oldest created first
    assert [r.question.subject for r in state.records] == [
        "probe self q1",
        "probe A question",
    ]
    assert state.open_total == 2 and state.window_full is False
    assert result.question_read.raw_count == 2
    view = view_of(result, fake_clock)
    for width in (160, 116, 80):
        lines = screen_lines(view, policy(width))
        assert all(cell_len(line) <= width for line in lines)
        assert "COORDINATOR QUESTIONS" in lines
        assert sum("reason unknown" in line for line in lines) == 2


def test_t55_the_missing_sample_fails_by_shape_then_by_no_active_terminal_and_keeps_questions(
    fake_clock,
):
    cycles = load_fixture("golden-question-missing").cycles
    assert "messages" not in cycles[1].envelope["result"]
    assert cycles[2].envelope["error"]["code"] == "no_active_terminal"
    collector = golden_collector("golden-question-missing", fake_clock)
    good = collector.run_once()
    shape = collector.run_once()
    assert (shape.question_state, shape.question_code) == ("FAILED", "shape")
    assert shape.questions is good.questions and shape.state == "OK"
    gone = collector.run_once()
    assert (gone.question_state, gone.question_code) == ("FAILED", "no-active-terminal")
    assert gone.questions is good.questions
    panel = view_of(gone, fake_clock).questions
    assert panel.state == "FAILED" and QUESTIONS_NOT_HELD in panel.state_lines
    assert (
        panel.counts_line.startswith("seen, not resolved: 2 |")
        and len(panel.lines) == 2
    )


def test_t55_the_stale_sample_is_stale_after_45_seconds_with_the_questions_kept(
    fake_clock,
):
    collector = golden_collector("golden-question-stale", fake_clock)
    good = collector.run_once()
    fake_clock.advance(44)
    assert view_of(good, fake_clock).questions.state == "OK"
    fake_clock.advance(1)
    stale = view_of(good, fake_clock).questions
    assert stale.state == "STALE" and stale.state_lines[0] == "question read: STALE 45s"
    assert len(stale.lines) == 2 and stale.counts_line.startswith(
        "seen, not resolved: 2 |"
    )
    fake_clock.jump_wall(-3600)  # wall-clock jumps change nothing
    assert view_of(good, fake_clock).questions.state == "STALE"
    failing = [collector.run_once() for _ in range(3)]
    view = view_of(failing[-1], fake_clock).questions
    assert [r.question_code for r in failing] == ["timeout"] * 3
    assert view.state == "FAILED" and len(view.lines) == 2  # FAILED outranks STALE
    assert failing[-1].questions is good.questions


def test_t55_the_contradictory_sample_drops_and_counts_foreign_rows_then_shows_fenced(
    fake_clock,
):
    cycles = load_fixture("golden-question-contradictory").cycles
    kinds = [m["type"] for m in cycles[1].envelope["result"]["messages"]]
    assert kinds.count("status") == 1 and len(kinds) == 4
    assert {m["run_id"] for m in cycles[1].envelope["result"]["messages"]} == {
        "run-a",
        "run-b",
    }
    collector = golden_collector("golden-question-contradictory", fake_clock)
    collector.run_once()
    mixed = collector.run_once()
    assert mixed.question_state == "OK" and mixed.question_read.contradictory_rows == 2
    assert mixed.questions.retained == 2  # nothing foreign was retained
    panel = view_of(mixed, fake_clock).questions
    assert "2 contradictory rows ignored" in panel.notes
    fenced = collector.run_once()
    assert (fenced.question_state, fenced.question_code) == (
        "FAILED",
        "consumer-fenced",
    )
    assert fenced.questions is mixed.questions
    assert "Run run-b, not Run run-a" in cycles[2].envelope["error"]["message"]


@pytest.mark.parametrize("name", QUESTION_GOLDEN)
def test_question_golden_files_hold_no_path_handle_token_credential_url_or_escape_byte(
    name,
):
    text = (
        resources.files(FIXTURE_PACKAGE)
        .joinpath(f"{name}.json")
        .read_text(encoding="utf-8")
    )
    assert "\x1b" not in text and text.isascii()
    for what, pattern in SENSITIVE.items():
        assert not pattern.search(text), f"{name}: {what}"
    assert not re.search(r"run_[0-9a-f]{12}|term_|msg_[0-9a-f]*[a-f][0-9a-f]*\b", text)
    for cycle in load_fixture(name).cycles:
        for message in ((cycle.envelope or {}).get("result") or {}).get("messages", []):
            assert set(message) == MESSAGE_KEYS  # key names kept, none added
            assert (
                message["body"] == "redacted" and message["from_handle"] == "redacted"
            )
            assert re.fullmatch(r"msg_\d{12}", message["id"])


def synthetic_question_envelope():
    return {
        "id": "552b2108-e561-4dd8-abb6-6d64b5c292e0",
        "ok": True,
        "result": {
            "acknowledged": None,
            "count": 2,
            "messages": [
                {
                    "id": "msg_28c906cf3d97",
                    "run_id": "run_14cfcbd8edf2",
                    "delivery_contract": "current_delivery",
                    "from_handle": "term_a39d3e66-a4f7-481e-bbf2-7f6ec8329e4f",
                    "to_handle": "run:run_14cfcbd8edf2",
                    "subject": "probe",
                    "body": "SECRET text",
                    "type": "question",
                    "priority": "normal",
                    "thread_id": None,
                    "payload": {"k": "v"},
                    "created_at": "2026-11-11T20:01:18Z",
                    "delivered_at": None,
                    "extra_key": "something",
                },
                {
                    "id": "msg_2d0e7d2264e5",
                    "run_id": "run_14cfcbd8edf2",
                    "type": "status",
                },
            ],
            "runId": "run_14cfcbd8edf2",
        },
        "_meta": {"runtimeId": "a7ee70a1-2e8b-4476-a228-51e9c7019b3f"},
    }


def test_the_recorder_redacts_ids_handles_bodies_and_extra_keys_and_keeps_key_names():
    runs = record_golden_questions.Names("run-{n}")
    ids = record_golden_questions.Names("{n}")
    out = record_golden_questions.redact_envelope(
        synthetic_question_envelope(),
        envelope_id="env-001",
        runs=runs,
        messages=ids,
        shift=0.0,
    )
    text = json.dumps(out)
    for leaked in (
        "run_14",
        "msg_28",
        "term_",
        "SECRET",
        "a7ee70a1",
        "552b2108",
        "something",
        'k": "v',
    ):
        assert leaked not in text, leaked
    first = out["result"]["messages"][0]
    assert first["id"] == "msg_000000000001" and first["run_id"] == "run-1"
    assert first["to_handle"] == "run:run-1" and first["from_handle"] == "redacted"
    assert first["body"] == "redacted" and first["extra_key"] == "redacted"
    assert out["result"]["runId"] == "run-1" and out["id"] == "env-001"
    assert out["_meta"] == {"runtimeId": "redacted"}


def test_the_recorder_redacts_the_run_ids_inside_an_error_message_and_shifts_times():
    error = {
        "id": "x",
        "ok": False,
        "error": {
            "code": "consumer_fenced",
            "message": "bound to Run run_14cfcbd8edf2, not Run run_c1badaa6576b. Nothing changed.",
        },
    }
    out = record_golden_questions.redact_envelope(
        error,
        envelope_id="env-9",
        runs=record_golden_questions.Names("run-{n}"),
        messages=record_golden_questions.Names("{n}"),
        shift=0.0,
    )
    assert out["error"] == {
        "code": "consumer_fenced",
        "message": "bound to Run run-1, not Run run-2. Nothing changed.",
    }
    envelope = synthetic_question_envelope()
    shifted = record_golden_questions.redact_envelope(
        envelope,
        envelope_id="e",
        runs=record_golden_questions.Names("run-{n}"),
        messages=record_golden_questions.Names("{n}"),
        shift=3600.0,
    )
    assert shifted["result"]["messages"][0]["created_at"] == "2026-11-11T21:01:18Z"
    for bad in (
        {},
        {"ok": True},
        {"ok": True, "result": {"messages": "x"}},
        {"ok": False, "error": 5},
    ):
        with pytest.raises(ValueError):
            record_golden_questions.redact_envelope(
                bad,
                envelope_id="e",
                runs=record_golden_questions.Names("run-{n}"),
                messages=record_golden_questions.Names("{n}"),
                shift=0.0,
            )
