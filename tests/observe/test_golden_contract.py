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
