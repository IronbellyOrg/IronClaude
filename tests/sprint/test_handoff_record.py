"""Stage-1 H4/M7 — HandoffRecord schema round-trip + forward-compat tests."""

from __future__ import annotations

from datetime import datetime, timezone

from superclaude.cli.sprint.models import (
    GateOutcome,
    HandoffRecord,
    TaskEntry,
    TaskResult,
    TaskStatus,
)

_H4_FIELDS = (
    "schema_version",
    "task_id",
    "phase",
    "status",
    "gate_outcome",
    "turns_consumed",
    "exit_code",
    "output_path",
    "started_at",
    "finished_at",
    "produced_artifacts",
    "consumed_upstreams",
)


def _record() -> HandoffRecord:
    return HandoffRecord(
        schema_version=1,
        task_id="T01.02",
        phase=1,
        status="pass",
        gate_outcome="pass",
        turns_consumed=7,
        exit_code=0,
        output_path="/r/phase-1-task-T01.02-output.txt",
        started_at="2026-06-03T10:00:00+00:00",
        finished_at="2026-06-03T10:01:00+00:00",
        produced_artifacts=["/r/phase-1-task-T01.02-output.txt"],
        consumed_upstreams=["T01.01"],
    )


def test_to_from_dict_round_trips_every_h4_field() -> None:
    rec = _record()
    d = rec.to_dict()
    # Every H4 field is present in the serialized dict.
    assert set(d) == set(_H4_FIELDS)
    back = HandoffRecord.from_dict(d)
    for f in _H4_FIELDS:
        assert getattr(back, f) == getattr(rec, f), f"field {f} did not round-trip"


def test_from_task_result_derives_shared_fields_and_attaches_deltas() -> None:
    started = datetime(2026, 6, 3, 10, 0, 0, tzinfo=timezone.utc)
    finished = datetime(2026, 6, 3, 10, 2, 0, tzinfo=timezone.utc)
    result = TaskResult(
        task=TaskEntry(task_id="T02.03", title="Third", dependencies=["T02.02"]),
        status=TaskStatus.PASS,
        turns_consumed=5,
        exit_code=0,
        started_at=started,
        finished_at=finished,
        gate_outcome=GateOutcome.PASS,
        output_path="/r/phase-2-task-T02.03-output.txt",
    )
    rec = HandoffRecord.from_task_result(
        result,
        phase=2,
        produced_artifacts=["/r/phase-2-task-T02.03-output.txt"],
        consumed_upstreams=["T02.02"],
    )
    assert rec.task_id == "T02.03"
    assert rec.phase == 2
    assert rec.status == "pass"  # TaskStatus.PASS.value
    assert rec.gate_outcome == "pass"  # GateOutcome.PASS.value, NOT a dict or None
    assert rec.turns_consumed == 5
    assert rec.exit_code == 0
    assert rec.started_at == started.isoformat()
    assert rec.finished_at == finished.isoformat()
    assert rec.produced_artifacts == ["/r/phase-2-task-T02.03-output.txt"]
    assert rec.consumed_upstreams == ["T02.02"]


def test_from_dict_tolerates_unknown_future_field() -> None:
    # M7 migration-safe: a record written by a NEWER schema carries an extra key.
    # An old reader must accept it without raising (the unknown key is ignored).
    d = _record().to_dict()
    d["a_field_from_the_future"] = {"nested": [1, 2, 3]}
    rec = HandoffRecord.from_dict(d)  # must NOT raise
    assert rec.task_id == "T01.02"
    assert rec.schema_version == 1


def test_schema_version_present_and_defaults_to_one() -> None:
    assert _record().schema_version == 1
    # Default construction also yields schema_version 1.
    assert HandoffRecord().schema_version == 1
    # And a dict missing schema_version degrades to 1.
    d = _record().to_dict()
    del d["schema_version"]
    assert HandoffRecord.from_dict(d).schema_version == 1
