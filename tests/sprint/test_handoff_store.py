"""Stage-1 — FileHandoffStore write/read round-trip + atomic-write tests."""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.sprint.handoff import FileHandoffStore
from superclaude.cli.sprint.models import (
    GateOutcome,
    HandoffRecord,
    Phase,
    SprintConfig,
    TaskEntry,
)


def _config(tmp_path: Path) -> SprintConfig:
    pf = tmp_path / "phase-1-tasklist.md"
    pf.write_text("# Phase 1\n")
    index = tmp_path / "tasklist-index.md"
    index.write_text("index\n")
    return SprintConfig(
        index_path=index,
        release_dir=tmp_path,
        phases=[Phase(number=1, file=pf, name="Phase 1")],
        start_phase=1,
        end_phase=1,
        max_turns=5,
    )


def _record() -> HandoffRecord:
    return HandoffRecord(
        schema_version=1,
        task_id="T01.01",
        phase=1,
        status="pass",
        gate_outcome=GateOutcome.PASS.value,
        turns_consumed=4,
        exit_code=0,
        output_path="/r/out.txt",
        started_at="2026-06-03T10:00:00+00:00",
        finished_at="2026-06-03T10:01:00+00:00",
        produced_artifacts=["/r/out.txt"],
        consumed_upstreams=["T01.00"],
    )


def test_write_then_read_round_trips(tmp_path: Path) -> None:
    config = _config(tmp_path)
    phase, task = config.phases[0], TaskEntry(task_id="T01.01", title="t")
    store = FileHandoffStore(config)

    store.write(_record(), phase=phase, task=task)
    got = store.read(phase=phase, task=task)

    assert got is not None
    assert got.task_id == "T01.01"
    assert got.status == "pass"
    assert got.gate_outcome == "pass"
    assert got.produced_artifacts == ["/r/out.txt"]
    assert got.consumed_upstreams == ["T01.00"]


def test_read_missing_returns_typed_none(tmp_path: Path) -> None:
    config = _config(tmp_path)
    phase, task = config.phases[0], TaskEntry(task_id="T01.99", title="absent")
    store = FileHandoffStore(config)
    assert store.read(phase=phase, task=task) is None


def test_on_disk_key_is_phase_qualified(tmp_path: Path) -> None:
    config = _config(tmp_path)
    phase, task = config.phases[0], TaskEntry(task_id="T01.01", title="t")
    store = FileHandoffStore(config)
    store.write(_record(), phase=phase, task=task)

    expected = config.results_dir / "handoff" / "phase-1-task-T01.01.json"
    assert config.handoff_file(phase, task) == expected
    assert expected.exists()


def test_write_leaves_no_tmp_file(tmp_path: Path) -> None:
    config = _config(tmp_path)
    phase, task = config.phases[0], TaskEntry(task_id="T01.01", title="t")
    store = FileHandoffStore(config)
    store.write(_record(), phase=phase, task=task)

    handoff_dir = config.results_dir / "handoff"
    leftover = list(handoff_dir.glob("*.tmp"))
    assert leftover == [], f"atomic write left a temp file behind: {leftover}"
