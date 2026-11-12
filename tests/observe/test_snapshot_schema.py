"""Snapshot v1 schema test (CAP-10, recorded owner decision 2; no ID assigned in acceptance-tests.md)."""

from __future__ import annotations

import copy
import json
import re
from importlib import resources

import pytest
from jsonschema import Draft7Validator

from superclaude.cli.observe.adapter import LiveSource
from superclaude.cli.observe.collector import Collector, FixtureSource
from superclaude.cli.observe.export import SCHEMA, snapshot_json
from superclaude.cli.observe.parse import VARIANTS, load_fixture
from superclaude.cli.observe.view import Session, build_view
from tests.observe.conftest import FakeDiscover, FakeRunner, make_envelope, make_rows

VALIDATOR = Draft7Validator(SCHEMA)


def every_snapshot(variant, clock):
    """The snapshot after each replayed cycle of a fixture variant."""
    collector = Collector(FixtureSource(variant), clock)
    for _ in range(len(load_fixture(variant).cycles)):
        yield json.loads(
            snapshot_json(build_view(collector.run_once(), Session(), clock))
        )


def live_snapshot(rows, clock, **kw):
    runner = FakeRunner([], [(0, json.dumps(make_envelope(rows, total=len(rows))))])
    result = Collector(LiveSource(runner, FakeDiscover([])), clock).run_once()
    return json.loads(snapshot_json(build_view(result, Session(), clock)))


def walk(value, path=()):
    """Every (path, key) and (path, scalar) in a JSON document."""
    if isinstance(value, dict):
        for key, inner in value.items():
            yield path, key
            yield from walk(inner, (*path, key))
    elif isinstance(value, list):
        for inner in value:
            yield from walk(inner, path)
    else:
        yield path, value


# -- the schema file ---------------------------------------------------------------------------------------------


def test_the_schema_ships_in_the_package_is_draft_7_and_closed_on_the_producer_side():
    text = (
        resources.files("superclaude.cli.observe")
        .joinpath("snapshot.schema.json")
        .read_text(encoding="utf-8")
    )
    assert json.loads(text) == SCHEMA
    Draft7Validator.check_schema(SCHEMA)
    assert SCHEMA["$schema"].endswith("draft-07/schema#")
    closed = [
        SCHEMA,
        SCHEMA["properties"]["producer"],
        SCHEMA["properties"]["source"],
        SCHEMA["properties"]["page"],
        SCHEMA["properties"]["collection"],
        SCHEMA["definitions"]["row"],
        SCHEMA["definitions"]["row"]["properties"]["stage"],
        SCHEMA["definitions"]["row"]["properties"]["liveness"],
        SCHEMA["definitions"]["row"]["properties"]["evidence"],
    ]
    assert all(node["additionalProperties"] is False for node in closed)


# -- every variant validates -----------------------------------------------------------------------------------------


@pytest.mark.parametrize("variant", VARIANTS)
def test_every_fixture_variant_snapshot_validates_after_every_cycle(
    fake_clock, variant
):
    count = 0
    for snapshot in every_snapshot(variant, fake_clock):
        assert list(VALIDATOR.iter_errors(snapshot)) == []
        assert (
            snapshot["schemaVersion"] == 1
            and snapshot["producer"]["name"] == "superclaude-observe"
        )
        count += 1
    assert count == len(load_fixture(variant).cycles)


def test_not_polled_and_not_available_snapshots_validate_with_unknown_status(
    fake_clock,
):
    never = Collector(FixtureSource("base"), fake_clock).latest()
    data = json.loads(snapshot_json(build_view(never, Session(), fake_clock)))
    assert list(VALIDATOR.iter_errors(data)) == []
    assert data["source"] == {
        "namespace": "UNKNOWN",
        "status": "UNKNOWN",
        "observedAt": "UNKNOWN",
    }
    assert data["page"] == {
        "hasMore": "UNKNOWN",
        "total": "UNKNOWN",
        "limit": "UNKNOWN",
    }
    assert (data["scope"], data["counts"], data["rows"]) == (
        "UNKNOWN",
        "UNKNOWN",
        [],
    ) and "collection" not in data
    unavailable = Collector(
        LiveSource(FakeRunner([]), FakeDiscover([], None)), fake_clock
    ).run_once()
    data = json.loads(snapshot_json(build_view(unavailable, Session(), fake_clock)))
    assert (
        list(VALIDATOR.iter_errors(data)) == []
        and data["source"]["status"] == "UNKNOWN"
    )


def test_status_error_stale_and_ok_map_from_the_source_state(fake_clock):
    collector = Collector(FixtureSource("source-loss"), fake_clock)
    results = [collector.run_once() for _ in range(3)]
    ok = json.loads(snapshot_json(build_view(results[0], Session(), fake_clock)))
    assert ok["source"]["status"] == "OK" and "error" not in ok["source"]
    fake_clock.advance(50)
    stale = json.loads(snapshot_json(build_view(results[1], Session(), fake_clock)))
    assert stale["source"]["status"] == "STALE" and "error" not in stale["source"]
    failed = json.loads(snapshot_json(build_view(results[2], Session(), fake_clock)))
    assert (
        failed["source"]["status"] == "ERROR" and failed["source"]["error"] == "timeout"
    )
    for data in (ok, stale, failed):
        assert list(VALIDATOR.iter_errors(data)) == []


# -- the schema rejects what it must --------------------------------------------------------------------------------------


def test_schema_version_two_and_unknown_fields_are_rejected(fake_clock):
    data = next(every_snapshot("base", fake_clock))
    assert list(VALIDATOR.iter_errors(data)) == []
    wrong = copy.deepcopy(data)
    wrong["schemaVersion"] = 2
    assert list(VALIDATOR.iter_errors(wrong))
    for where in (
        lambda d: d.update(extra=1),
        lambda d: d["producer"].update(extra=1),
        lambda d: d["source"].update(extra=1),
        lambda d: d["page"].update(extra=1),
        lambda d: d["collection"].update(extra=1),
        lambda d: d["rows"][0].update(extra=1),
        lambda d: d["rows"][0]["stage"].update(detail="x"),
        lambda d: d["rows"][0]["liveness"].update(extra=1),
        lambda d: d["rows"][0]["evidence"].update(extra=1),
    ):
        mutated = copy.deepcopy(data)
        where(mutated)
        assert list(VALIDATOR.iter_errors(mutated)), where


def test_schema_rejects_wrong_types_missing_required_keys_and_misplaced_error(
    fake_clock,
):
    data = next(every_snapshot("base", fake_clock))
    mutations = [
        lambda d: d.pop("rows"),
        lambda d: d.update(cycle="1"),
        lambda d: d.update(generatedAt="yesterday"),
        lambda d: d["source"].update(status="BROKEN"),
        lambda d: d["source"].update(error="timeout"),  # error only with status ERROR
        lambda d: d["rows"][0].pop("nextAction"),
        lambda d: d["rows"][0].update(dispatchId=None),
        lambda d: d["rows"][0].update(absentFields=["a", "a"]),
        lambda d: d["page"].update(total=-1),
        lambda d: d["page"].update(hasMore="false"),
        lambda d: d["collection"].update(state="DONE"),
        lambda d: d.update(scope=None),
    ]
    for mutate in mutations:
        mutated = copy.deepcopy(data)
        mutate(mutated)
        assert list(VALIDATOR.iter_errors(mutated)), mutate
    failed = copy.deepcopy(data)
    failed["source"]["status"] = "ERROR"
    assert list(VALIDATOR.iter_errors(failed))  # ERROR needs the short code


# -- UNKNOWN versus a source value that is the text UNKNOWN -------------------------------------------------------------------


def test_missing_values_are_the_string_unknown_and_absent_fields_separate_them_from_source_text(
    fake_clock,
):
    rows = make_rows(2, 1)
    rows[0]["taskId"] = "UNKNOWN"  # a source value that is itself the text
    del rows[1]["taskId"]
    rows[1]["projection"]["nextAction"] = None
    del rows[1]["projection"]["liveness"]["observedAt"]
    data = live_snapshot(rows, fake_clock)
    assert list(VALIDATOR.iter_errors(data)) == []
    by_id = {row["dispatchId"]: row for row in data["rows"]}
    typed, absent = by_id["w-001"], by_id["w-002"]
    assert typed["taskId"] == "UNKNOWN" and "taskId" not in typed.get(
        "absentFields", []
    )
    assert absent["taskId"] == "UNKNOWN" and "taskId" in absent["absentFields"]
    assert absent["nextAction"] == "UNKNOWN" and "nextAction" in absent["absentFields"]
    assert (
        absent["liveness"]["observedAt"] == "UNKNOWN"
        and "liveness.observedAt" in absent["absentFields"]
    )
    assert absent["absentFields"] == sorted(absent["absentFields"])
    # no stand-in for a missing value: JSON null, 0, false and "" never appear for it
    for scalar in (
        absent["taskId"],
        absent["nextAction"],
        absent["liveness"]["observedAt"],
    ):
        assert (
            scalar == "UNKNOWN"
            and scalar is not None
            and scalar != ""
            and scalar is not False
        )


def test_the_missing_fields_variant_has_unknown_everywhere_the_source_was_silent(
    fake_clock,
):
    data = next(every_snapshot("missing-fields", fake_clock))
    assert (
        data["page"]["total"] == "UNKNOWN"
        and data["scope"] == "UNKNOWN"
        and data["counts"] == "UNKNOWN"
    )
    for row in data["rows"]:
        for _, scalar in walk(row):
            assert scalar is not None
    first = next(r for r in data["rows"] if r["dispatchId"] == "w-001")
    assert first["liveness"] == {
        "verdict": "UNKNOWN",
        "source": "UNKNOWN",
        "observedAt": "UNKNOWN",
    }
    assert {
        "liveness.verdict",
        "liveness.source",
        "liveness.observedAt",
        "nextAction",
    } <= set(first["absentFields"])
    anonymous = next(r for r in data["rows"] if r["dispatchId"] == "UNKNOWN")
    assert "dispatchId" in anonymous["absentFields"]


# -- nothing sensitive leaves the observer ---------------------------------------------------------------------------------------

FORBIDDEN_KEYS = {
    "detail",
    "activity",
    "terminalHandle",
    "agentTerminalHandle",
    "worktreeId",
    "endpointId",
    "ownershipState",
    "releaseState",
    "warnings",
    "nextCursor",
    "body",
    "prompt",
    "content",
    "credentials",
    "token",
    "password",
    "secret",
    "message",
    "messages",
}
FORBIDDEN_WORDS = (
    "prompt",
    "credential",
    "password",
    "secret",
    "token",
    "worktree",
    "terminal handle",
    "stage.detail",
    "stage.activity",
)


@pytest.mark.parametrize("variant", VARIANTS)
def test_snapshots_carry_no_forbidden_keys_words_or_fixture_input_values(
    fake_clock, variant
):
    fixture = load_fixture(variant)
    withheld: set[str] = set()
    for cycle in fixture.cycles:
        for worker in (cycle.envelope or {}).get("result", {}).get("workers", []):
            if not isinstance(worker, dict):
                continue
            stage = worker.get("projection", {}).get("stage", {})
            resource = worker.get("resource", {})
            withheld |= {
                v
                for v in (
                    stage.get("detail"),
                    stage.get("activity"),
                    resource.get("worktreeId"),
                    worker.get("agentTerminalHandle"),
                    resource.get("terminalHandle"),
                )
                if isinstance(v, str) and len(v) > 3
            }
    for snapshot in every_snapshot(variant, fake_clock):
        text = json.dumps(snapshot)
        key_names = {key for _, key in _only_keys(snapshot)}
        assert key_names.isdisjoint(FORBIDDEN_KEYS), key_names & FORBIDDEN_KEYS
        lowered = text.lower()
        assert not any(word in lowered for word in FORBIDDEN_WORDS)
        for value in withheld:
            assert value not in text, value


def _only_keys(value, path=()):
    if isinstance(value, dict):
        for key, inner in value.items():
            yield path, key
            yield from _only_keys(inner, (*path, key))
    elif isinstance(value, list):
        for inner in value:
            yield from _only_keys(inner, path)


# -- ordering and optional groups ----------------------------------------------------------------------------------------------------


def test_rows_are_newest_first_with_untimed_rows_last_and_ties_by_dispatch_id(
    fake_clock,
):
    rows = make_rows(5, 1)
    stamp = "2026-11-08T11:00:00Z"
    for row in rows:
        row["projection"]["liveness"]["observedAt"] = stamp
    rows[0]["projection"]["liveness"]["observedAt"] = "2026-11-08T11:30:00Z"  # newest
    rows[1]["dispatchId"] = (
        "w-000"  # ties with w-003..w-005 on the timestamp, sorts first by id
    )
    del rows[2]["projection"]["liveness"]["observedAt"]
    del rows[2]["projection"]["evidence"][
        "lastObservedAt"
    ]  # untimed: after every timed row
    data = live_snapshot(rows, fake_clock)
    assert [r["dispatchId"] for r in data["rows"]] == [
        "w-001",
        "w-000",
        "w-004",
        "w-005",
        "w-003",
    ]


def test_historical_rows_are_in_the_snapshot_and_collection_fields_are_filled(
    fake_clock,
):
    data = next(every_snapshot("historical", fake_clock))
    assert len(data["rows"]) == 9
    assert {r["terminalState"] for r in data["rows"]} >= {
        "released",
        "retained",
        "orphaned",
        "UNKNOWN",
    }
    assert data["collection"] == {
        "state": "COMPLETE",
        "collected": 9,
        "changedDuringRead": False,
        "duplicatesIgnored": 0,
    }
    dup = list(every_snapshot("duplicate-out-of-order", fake_clock))
    assert dup[0]["collection"]["duplicatesIgnored"] == 1
    assert [r["dispatchId"] for r in dup[1]["rows"] if r.get("orderUnknown")] == [
        "w-003"
    ]


def test_not_reobserved_rows_carry_the_flag_and_output_is_indented_and_sorted(
    fake_clock,
):
    rows = make_rows(3, 1)
    runner = FakeRunner(
        [],
        [
            (0, json.dumps(make_envelope(rows, total=3))),
            (0, json.dumps(make_envelope(rows[:2], total=2))),
        ],
    )
    collector = Collector(LiveSource(runner, FakeDiscover([])), fake_clock)
    collector.run_once()
    text = snapshot_json(build_view(collector.run_once(), Session(), fake_clock))
    data = json.loads(text)
    flagged = [r["dispatchId"] for r in data["rows"] if r.get("notReobserved")]
    assert flagged == ["w-003"]
    assert text == json.dumps(data, indent=2, sort_keys=True)
    assert re.match(r'^\{\n  "collection"', text)


# -- R2: the optional questions group (ids, times and counts only) --------------------------------------------------------

from superclaude.cli.observe.export import snapshot_dict  # noqa: E402
from tests.observe.conftest import (  # noqa: E402
    QRUN,
    make_question_envelope,
    make_question_error,
    make_question_rows,
    routed_runner_responses,
)

WITHHELD_QUESTION_KEYS = {"subject", "body", "from_handle", "to_handle", "payload"}


def question_cycle(message, clock, cycles=1, **kw):
    worker = (0, json.dumps(make_envelope(make_rows(3, 1), total=3)))
    runner = FakeRunner([], [routed_runner_responses(worker, message)])
    collector = Collector(
        LiveSource(runner, FakeDiscover([])), clock, run_id=QRUN, questions=True, **kw
    )
    result = None
    for _ in range(cycles):
        result = collector.run_once()
    return collector, result


def ok_pair(rows):
    return 0, json.dumps(make_question_envelope(rows))


def questions_snapshot(message, clock, cycles=1):
    _, result = question_cycle(message, clock, cycles)
    return json.loads(snapshot_json(build_view(result, Session(), clock)))


def test_a_snapshot_with_questions_on_validates_and_keeps_schema_version_1(fake_clock):
    snapshot = questions_snapshot(ok_pair(make_question_rows(3)), fake_clock)
    assert not list(VALIDATOR.iter_errors(snapshot))
    assert snapshot["schemaVersion"] == 1
    group = snapshot["questions"]
    assert group["runId"] == QRUN and group["state"] == "OK"
    assert group["observedOpen"] == 3 and group["closureEvidence"] == "unavailable"
    assert (group["windowFull"], group["retained"], group["evicted"]) == (False, 3, 0)
    assert "code" not in group
    assert [i["id"] for i in group["items"]] == [
        "msg_000000000000",
        "msg_000000000001",
        "msg_000000000002",
    ]
    for item in group["items"]:
        assert set(item) == {"id", "createdAt", "ageSeconds", "inWindow"}
        assert item["inWindow"] is True and isinstance(item["ageSeconds"], float)


def test_the_questions_group_carries_the_failure_code_and_window_flags(fake_clock):
    fenced = (1, json.dumps(make_question_error("consumer_fenced")))
    snapshot = questions_snapshot(
        [ok_pair(make_question_rows(100)), fenced], fake_clock, cycles=2
    )
    assert not list(VALIDATOR.iter_errors(snapshot))
    group = snapshot["questions"]
    assert (group["state"], group["code"]) == ("FAILED", "consumer-fenced")
    assert group["windowFull"] is True and group["retained"] == 100
    first = questions_snapshot(fenced, fake_clock)
    assert first["questions"]["observedOpen"] == "UNKNOWN"  # nothing read, never 0
    assert not list(VALIDATOR.iter_errors(first))


def test_a_snapshot_with_questions_off_has_no_questions_key_and_is_unchanged(
    fake_clock,
):
    snapshot = live_snapshot(make_rows(3, 1), fake_clock)
    assert "questions" not in snapshot and not list(VALIDATOR.iter_errors(snapshot))
    for variant in VARIANTS:
        for shot in every_snapshot(variant, fake_clock):
            assert "questions" not in shot


def test_exported_question_json_holds_no_subject_body_handle_or_payload_key(fake_clock):
    rows = make_question_rows(3, subject="visible only on screen")
    snapshot = questions_snapshot(ok_pair(rows), fake_clock)
    keys = {key for _, key in _only_keys(snapshot["questions"])}
    assert keys.isdisjoint(WITHHELD_QUESTION_KEYS), keys
    text = json.dumps(snapshot)
    for forbidden in (
        "visible only on screen",
        "synthetic body",
        "term_synthetic",
        "run:run_",
    ):
        assert forbidden not in text, forbidden


def test_an_unparsable_created_time_exports_the_string_unknown(fake_clock):
    rows = make_question_rows(1)
    rows[0]["created_at"] = None
    snapshot = questions_snapshot(ok_pair(rows), fake_clock)
    (item,) = snapshot["questions"]["items"]
    assert (item["createdAt"], item["ageSeconds"]) == ("UNKNOWN", "UNKNOWN")
    assert not list(VALIDATOR.iter_errors(snapshot))


def test_the_schema_rejects_a_misshaped_questions_group(fake_clock):
    good = questions_snapshot(ok_pair(make_question_rows(1)), fake_clock)
    for mutate in (
        lambda g: g.update(closureEvidence="available"),
        lambda g: g.update(observedOpen="-1"),
        lambda g: g.update(state="DONE"),
        lambda g: g.update(subject="leak"),
        lambda g: g["items"][0].update(subject="leak"),
        lambda g: g["items"][0].pop("id"),
    ):
        bad = copy.deepcopy(good)
        mutate(bad["questions"])
        assert list(VALIDATOR.iter_errors(bad))


def test_retention_exceeded_exports_unknown_with_the_retained_count(fake_clock):
    import dataclasses

    from superclaude.cli.observe.parse import parse_questions
    from superclaude.cli.observe.questions import merge_questions

    _, result = question_cycle(ok_pair(make_question_rows(1)), fake_clock)
    state = None
    for start in range(0, 1001, 100):
        rows = make_question_rows(min(100, 1001 - start), start=start)
        parsed = parse_questions(make_question_envelope(rows), "ns", 1, QRUN)
        state = merge_questions(state, parsed.rows, 1 + start // 100, True, True, QRUN)
    over = dataclasses.replace(result, questions=state)
    snapshot = json.loads(snapshot_json(build_view(over, Session(), fake_clock)))
    group = snapshot["questions"]
    assert (group["observedOpen"], group["retained"], group["evicted"]) == (
        "UNKNOWN",
        1000,
        1,
    )
    assert not list(VALIDATOR.iter_errors(snapshot))


def test_snapshot_dict_and_json_agree_on_the_questions_group(fake_clock):
    _, result = question_cycle(ok_pair(make_question_rows(2)), fake_clock)
    view = build_view(result, Session(), fake_clock)
    assert (
        json.loads(snapshot_json(view))["questions"] == snapshot_dict(view)["questions"]
    )
