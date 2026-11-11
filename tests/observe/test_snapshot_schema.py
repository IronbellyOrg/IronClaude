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
