"""T01.26 -- DM-013 WorkerResult + DM-014 SwarmState + DM-015 EventRecord.

Covers roadmap rows R-023 / R-024 / R-025 (DM-013, DM-014, DM-015 merged
per phase-1-tasklist.md T01.26). The three records share the JSONL /
state plumbing and emit together in M3, so the phase tasklist merges
their landing into a single STANDARD task -- this suite mirrors the
merger and pins all three field sets plus their respective Literal
enums in one place.

Per-record contract:

DM-013 WorkerResult (12 fields)
    Per-worker output entry emitted by the dispatcher (M3 -- COMP-007)
    for every worker fanned out from Wave 1; instances are collected
    into :class:`ResultContract.output_files` at Wave 3 reduce
    (COMP-009, M5). The :class:`Transport` Protocol (COMP-031, T01.11)
    returns one of these per call.

    Status Literal :data:`WorkerStatus` admits exactly the four values
    from §5 Result Contract Schema (``merged-requirements.compressed.
    compressed.md`` L395): ``success`` / ``timeout`` / ``parse_error`` /
    ``proxy_error``. ``http_code`` is :data:`Optional[int]` to model
    DM-013's ``http_code:int?``.

DM-014 SwarmState (3 fields)
    Wave-level coarse state persisted to ``.swarm-state.json`` via the
    state module (COMP-011, M3) using write-to-tmp + ``os.replace`` so
    transitions are never partial. Resume (M6 -- FR-015) reads this
    file to short-circuit to the appropriate wave.

    State Literal :data:`SwarmStateValue` admits exactly the five values
    from the roadmap row, in execution order: ``preflight_ok`` /
    ``dispatching`` / ``normalizing`` / ``reducing`` / ``terminal``.

DM-015 EventRecord (4 fields)
    Per-event append-only entry emitted by the logging_ module
    (COMP-012, M3) into ``event-log.jsonl``. Appends are
    lock-coordinated so concurrent transport workers cannot interleave
    bytes. The Markdown log is rendered from the same record stream so
    the two artifacts cannot drift.

    Event-type Literal :data:`EventType` admits exactly the five values
    from the roadmap row, in lifecycle order: ``worker_start`` /
    ``worker_progress`` / ``worker_done`` / ``wave_transition`` /
    ``terminal``. ``worker_index`` is :data:`Optional[int]` because the
    ``wave_transition`` / ``terminal`` event types are not per-worker.

This suite pins:

1. Every field listed in each roadmap row is present on its dataclass,
   in declaration order; no field drift.
2. Field types match the roadmap row exactly (including Optional shapes
   for ``WorkerResult.http_code`` and ``EventRecord.worker_index``).
3. Each Literal enum admits exactly the values from its roadmap row,
   and out-of-enum values raise ``ValueError`` at construction.
4. JSON round-trip is lossless for default and populated instances of
   each record. WorkerResult populated round-trip exercises the
   ``http_code`` Optional path with both ``None`` and an int.
   EventRecord populated round-trip exercises both ``worker_index``
   None (wave_transition / terminal) and int (worker_* events).
5. Defaults satisfy the no-arg construction contract so the
   aggregator's round-trip suite
   (``tests/swarm/test_models_round_trip.py``) keeps passing.

STANDARD-tier task per phase-1-tasklist.md T01.26.
"""

from __future__ import annotations

import dataclasses
import typing

import pytest

from superclaude.cli.swarm.models import (
    EventRecord,
    EventType,
    SwarmState,
    SwarmStateValue,
    WorkerResult,
    WorkerStatus,
    from_dict,
    from_json,
    to_dict,
    to_json,
)

# ---------------------------------------------------------------------------
# Expected field sets, drawn verbatim from the roadmap DM-### rows
# (.dev/releases/Current/MultiModelSwarm/roadmap.md L100-L102).
# ---------------------------------------------------------------------------


EXPECTED_WORKER_RESULT_FIELDS: tuple[str, ...] = (
    "index",
    "path",
    "raw_path",
    "meta_path",
    "final_path",
    "model_id",
    "model_label",
    "bytes",
    "status",
    "http_code",
    "attempts",
    "elapsed_ms",
)


EXPECTED_SWARM_STATE_FIELDS: tuple[str, ...] = (
    "state",
    "job_id",
    "updated",
)


EXPECTED_EVENT_RECORD_FIELDS: tuple[str, ...] = (
    "event_type",
    "timestamp",
    "worker_index",
    "payload",
)


# ---------------------------------------------------------------------------
# DM-013 WorkerResult -- field-completeness.
# ---------------------------------------------------------------------------


def test_worker_result_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(WorkerResult)


def test_worker_result_declares_every_dm013_field() -> None:
    """No field drift vs roadmap DM-013 row."""
    declared = tuple(f.name for f in dataclasses.fields(WorkerResult))
    assert declared == EXPECTED_WORKER_RESULT_FIELDS, (
        f"WorkerResult field set diverged from DM-013 row.\n"
        f"  declared: {declared}\n"
        f"  expected: {EXPECTED_WORKER_RESULT_FIELDS}"
    )


def test_worker_result_field_count_matches_dm013() -> None:
    """T01.26 acceptance: Field-count test for WorkerResult."""
    assert len(dataclasses.fields(WorkerResult)) == 12


@pytest.mark.parametrize(
    "field_name,expected_type",
    [
        ("index", int),
        ("path", str),
        ("raw_path", str),
        ("meta_path", str),
        ("final_path", str),
        ("model_id", str),
        ("model_label", str),
        ("bytes", int),
        ("attempts", int),
        ("elapsed_ms", int),
    ],
)
def test_worker_result_scalar_field_types(field_name: str, expected_type: type) -> None:
    hints = typing.get_type_hints(WorkerResult)
    assert hints[field_name] is expected_type, (
        f"WorkerResult.{field_name} should be typed as "
        f"{expected_type.__name__}, got {hints[field_name]!r}"
    )


def test_worker_result_http_code_is_optional_int() -> None:
    """DM-013 spells ``http_code:int?`` -- must accept None."""
    hints = typing.get_type_hints(WorkerResult)
    field_type = hints["http_code"]
    args = typing.get_args(field_type)
    assert type(None) in args, (
        f"http_code must be Optional (Union[..., None]); got {field_type!r}"
    )
    # The non-None arm should be int.
    non_none = [a for a in args if a is not type(None)]
    assert non_none == [int], f"http_code Optional arm should be int; got {non_none!r}"


# ---------------------------------------------------------------------------
# DM-013 WorkerResult -- status Literal enforcement.
# ---------------------------------------------------------------------------


def test_worker_status_literal_values() -> None:
    """T01.26 acceptance: Literal enums match roadmap exactly.

    §5 Result Contract Schema (``merged-requirements.compressed.compressed.md``
    L395) names exactly success / timeout / parse_error / proxy_error.
    """
    args = typing.get_args(WorkerStatus)
    assert set(args) == {"success", "timeout", "parse_error", "proxy_error"}, (
        f"WorkerStatus admits {set(args)}; T01.26 acceptance requires "
        "{'success','timeout','parse_error','proxy_error'}."
    )


def test_worker_status_default_is_success() -> None:
    """Conservative default so the no-arg round-trip suite keeps passing."""
    assert WorkerResult().status == "success"


@pytest.mark.parametrize("status", ["success", "timeout", "parse_error", "proxy_error"])
def test_worker_status_accepts_each_literal(status: str) -> None:
    result = WorkerResult(status=status)  # type: ignore[arg-type]
    assert result.status == status


def test_worker_status_rejects_unknown_value() -> None:
    """A manually-constructed WorkerResult cannot smuggle an out-of-enum
    status into ``output_files`` (FR-018 surface)."""
    with pytest.raises(ValueError, match="status"):
        WorkerResult(status="bogus")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# DM-013 WorkerResult -- defaults.
# ---------------------------------------------------------------------------


def test_worker_result_defaults_are_safe_for_round_trip() -> None:
    result = WorkerResult()
    assert result.index == 0
    assert result.path == ""
    assert result.raw_path == ""
    assert result.meta_path == ""
    assert result.final_path == ""
    assert result.model_id == ""
    assert result.model_label == ""
    assert result.bytes == 0
    assert result.http_code is None
    assert result.attempts == 1
    assert result.elapsed_ms == 0


# ---------------------------------------------------------------------------
# DM-013 WorkerResult -- round-trip.
# ---------------------------------------------------------------------------


def test_worker_result_default_round_trips_via_dict() -> None:
    instance = WorkerResult()
    restored = from_dict(WorkerResult, to_dict(instance))
    assert restored == instance


def test_worker_result_default_round_trips_via_json() -> None:
    instance = WorkerResult()
    restored = from_json(WorkerResult, to_json(instance))
    assert restored == instance


def test_worker_result_populated_round_trips_via_json() -> None:
    """Populated WorkerResult with a real ``http_code`` round-trips."""
    instance = WorkerResult(
        index=2,
        path="/abs/path/to/output-02-haiku.md",
        raw_path="/abs/path/to/output-02-haiku.raw",
        meta_path="/abs/path/to/output-02-haiku.meta.json",
        final_path="/abs/path/to/output-02-haiku.md",
        model_id="claude-haiku-4.5",
        model_label="Claude Haiku 4.5",
        bytes=4096,
        status="success",
        http_code=200,
        attempts=1,
        elapsed_ms=12340,
    )
    restored = from_json(WorkerResult, to_json(instance))
    assert restored == instance


def test_worker_result_optional_http_code_round_trips_as_none() -> None:
    """Stub transport (COMP-033) emits WorkerResult without HTTP code."""
    instance = WorkerResult(status="success", http_code=None)
    restored = from_json(WorkerResult, to_json(instance))
    assert restored.http_code is None
    assert restored == instance


def test_worker_result_optional_http_code_round_trips_as_int() -> None:
    instance = WorkerResult(status="proxy_error", http_code=502, attempts=2)
    restored = from_json(WorkerResult, to_json(instance))
    assert restored.http_code == 502
    assert restored == instance


def test_worker_result_round_trip_diff_is_empty() -> None:
    """Round-trip diff is empty (acceptance criterion)."""
    instance = WorkerResult(
        index=1,
        path="/x.md",
        raw_path="/x.raw",
        meta_path="/x.meta.json",
        final_path="/x.md",
        model_id="m",
        model_label="M",
        bytes=128,
        status="timeout",
        http_code=None,
        attempts=2,
        elapsed_ms=180000,
    )
    payload_before = to_dict(instance)
    restored = from_dict(WorkerResult, payload_before)
    payload_after = to_dict(restored)
    assert payload_before == payload_after


# ---------------------------------------------------------------------------
# DM-014 SwarmState -- field-completeness.
# ---------------------------------------------------------------------------


def test_swarm_state_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(SwarmState)


def test_swarm_state_declares_every_dm014_field() -> None:
    """No field drift vs roadmap DM-014 row."""
    declared = tuple(f.name for f in dataclasses.fields(SwarmState))
    assert declared == EXPECTED_SWARM_STATE_FIELDS, (
        f"SwarmState field set diverged from DM-014 row.\n"
        f"  declared: {declared}\n"
        f"  expected: {EXPECTED_SWARM_STATE_FIELDS}"
    )


def test_swarm_state_field_count_matches_dm014() -> None:
    """T01.26 acceptance: Field-count test for SwarmState."""
    assert len(dataclasses.fields(SwarmState)) == 3


@pytest.mark.parametrize(
    "field_name,expected_type",
    [
        ("job_id", str),
        ("updated", str),
    ],
)
def test_swarm_state_scalar_field_types(field_name: str, expected_type: type) -> None:
    hints = typing.get_type_hints(SwarmState)
    assert hints[field_name] is expected_type


# ---------------------------------------------------------------------------
# DM-014 SwarmState -- state Literal enforcement.
# ---------------------------------------------------------------------------


def test_swarm_state_literal_values() -> None:
    """T01.26 acceptance: Literal enums match roadmap exactly.

    Roadmap DM-014 row names exactly preflight_ok / dispatching /
    normalizing / reducing / terminal in execution order.
    """
    args = typing.get_args(SwarmStateValue)
    assert set(args) == {
        "preflight_ok",
        "dispatching",
        "normalizing",
        "reducing",
        "terminal",
    }, (
        f"SwarmStateValue admits {set(args)}; T01.26 acceptance requires the "
        "5-value execution-order enum from DM-014."
    )


def test_swarm_state_default_is_preflight_ok() -> None:
    assert SwarmState().state == "preflight_ok"


@pytest.mark.parametrize(
    "state",
    ["preflight_ok", "dispatching", "normalizing", "reducing", "terminal"],
)
def test_swarm_state_accepts_each_literal(state: str) -> None:
    instance = SwarmState(state=state)  # type: ignore[arg-type]
    assert instance.state == state


def test_swarm_state_rejects_unknown_value() -> None:
    with pytest.raises(ValueError, match="state"):
        SwarmState(state="bogus")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# DM-014 SwarmState -- round-trip.
# ---------------------------------------------------------------------------


def test_swarm_state_default_round_trips_via_dict() -> None:
    instance = SwarmState()
    restored = from_dict(SwarmState, to_dict(instance))
    assert restored == instance


def test_swarm_state_default_round_trips_via_json() -> None:
    instance = SwarmState()
    restored = from_json(SwarmState, to_json(instance))
    assert restored == instance


def test_swarm_state_populated_round_trips_via_json() -> None:
    instance = SwarmState(
        state="dispatching",
        job_id="2026-06-01T05-23-38Z-bare-review-7f3a",
        updated="2026-06-01T05:23:39+00:00",
    )
    restored = from_json(SwarmState, to_json(instance))
    assert restored == instance


def test_swarm_state_round_trip_diff_is_empty() -> None:
    instance = SwarmState(
        state="terminal",
        job_id="abc",
        updated="2026-06-01T05:30:00+00:00",
    )
    payload_before = to_dict(instance)
    restored = from_dict(SwarmState, payload_before)
    payload_after = to_dict(restored)
    assert payload_before == payload_after


# ---------------------------------------------------------------------------
# DM-015 EventRecord -- field-completeness.
# ---------------------------------------------------------------------------


def test_event_record_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(EventRecord)


def test_event_record_declares_every_dm015_field() -> None:
    """No field drift vs roadmap DM-015 row."""
    declared = tuple(f.name for f in dataclasses.fields(EventRecord))
    assert declared == EXPECTED_EVENT_RECORD_FIELDS, (
        f"EventRecord field set diverged from DM-015 row.\n"
        f"  declared: {declared}\n"
        f"  expected: {EXPECTED_EVENT_RECORD_FIELDS}"
    )


def test_event_record_field_count_matches_dm015() -> None:
    """T01.26 acceptance: Field-count test for EventRecord."""
    assert len(dataclasses.fields(EventRecord)) == 4


def test_event_record_timestamp_is_str() -> None:
    hints = typing.get_type_hints(EventRecord)
    assert hints["timestamp"] is str


def test_event_record_worker_index_is_optional_int() -> None:
    """DM-015 spells ``worker_index:int?`` -- must accept None."""
    hints = typing.get_type_hints(EventRecord)
    field_type = hints["worker_index"]
    args = typing.get_args(field_type)
    assert type(None) in args, (
        f"worker_index must be Optional (Union[..., None]); got {field_type!r}"
    )
    non_none = [a for a in args if a is not type(None)]
    assert non_none == [int], (
        f"worker_index Optional arm should be int; got {non_none!r}"
    )


def test_event_record_payload_is_dict() -> None:
    hints = typing.get_type_hints(EventRecord)
    assert typing.get_origin(hints["payload"]) is dict, (
        f"payload should be dict; got {hints['payload']!r}"
    )


# ---------------------------------------------------------------------------
# DM-015 EventRecord -- event_type Literal enforcement.
# ---------------------------------------------------------------------------


def test_event_type_literal_values() -> None:
    """T01.26 acceptance: Literal enums match roadmap exactly.

    Roadmap DM-015 row names exactly worker_start / worker_progress /
    worker_done / wave_transition / terminal in lifecycle order.
    """
    args = typing.get_args(EventType)
    assert set(args) == {
        "worker_start",
        "worker_progress",
        "worker_done",
        "wave_transition",
        "terminal",
    }, (
        f"EventType admits {set(args)}; T01.26 acceptance requires the "
        "5-value lifecycle-order enum from DM-015."
    )


def test_event_record_default_event_type_is_worker_start() -> None:
    assert EventRecord().event_type == "worker_start"


@pytest.mark.parametrize(
    "event_type",
    [
        "worker_start",
        "worker_progress",
        "worker_done",
        "wave_transition",
        "terminal",
    ],
)
def test_event_record_accepts_each_literal(event_type: str) -> None:
    instance = EventRecord(event_type=event_type)  # type: ignore[arg-type]
    assert instance.event_type == event_type


def test_event_record_rejects_unknown_event_type() -> None:
    with pytest.raises(ValueError, match="event_type"):
        EventRecord(event_type="bogus")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# DM-015 EventRecord -- defaults.
# ---------------------------------------------------------------------------


def test_event_record_defaults() -> None:
    record = EventRecord()
    assert record.event_type == "worker_start"
    assert record.timestamp == ""
    assert record.worker_index is None
    assert record.payload == {}


# ---------------------------------------------------------------------------
# DM-015 EventRecord -- round-trip.
# ---------------------------------------------------------------------------


def test_event_record_default_round_trips_via_dict() -> None:
    instance = EventRecord()
    restored = from_dict(EventRecord, to_dict(instance))
    assert restored == instance


def test_event_record_default_round_trips_via_json() -> None:
    instance = EventRecord()
    restored = from_json(EventRecord, to_json(instance))
    assert restored == instance


def test_event_record_populated_per_worker_round_trips() -> None:
    """worker_* events carry an integer worker_index."""
    instance = EventRecord(
        event_type="worker_done",
        timestamp="2026-06-01T05:23:51+00:00",
        worker_index=2,
        payload={"status": "success", "http_code": 200, "elapsed_ms": 12340},
    )
    restored = from_json(EventRecord, to_json(instance))
    assert restored == instance
    assert restored.worker_index == 2


def test_event_record_populated_wave_transition_round_trips() -> None:
    """wave_transition / terminal events carry worker_index=None."""
    instance = EventRecord(
        event_type="wave_transition",
        timestamp="2026-06-01T05:24:00+00:00",
        worker_index=None,
        payload={"from": "dispatching", "to": "normalizing"},
    )
    restored = from_json(EventRecord, to_json(instance))
    assert restored == instance
    assert restored.worker_index is None


def test_event_record_terminal_round_trips() -> None:
    instance = EventRecord(
        event_type="terminal",
        timestamp="2026-06-01T05:24:01+00:00",
        worker_index=None,
        payload={"status": "success"},
    )
    restored = from_json(EventRecord, to_json(instance))
    assert restored == instance


def test_event_record_round_trip_diff_is_empty() -> None:
    instance = EventRecord(
        event_type="worker_progress",
        timestamp="2026-06-01T05:23:45+00:00",
        worker_index=0,
        payload={"chunk_bytes": 256},
    )
    payload_before = to_dict(instance)
    restored = from_dict(EventRecord, payload_before)
    payload_after = to_dict(restored)
    assert payload_before == payload_after
