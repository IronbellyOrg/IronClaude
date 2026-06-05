"""T03.04 -- COMP-012 logging_ module unit tests.

Pins the dual-format Logger contract:

1. :class:`EventRecord` JSON round-trip survives an append + parse via
   the logger (``to_json``/``from_json`` parity).
2. Single-thread emission produces one JSONL line per event and one
   Markdown line per event, in caller order.
3. Concurrent emission from 10 threads firing 10 events each (100
   total) yields exactly 100 parseable JSONL lines with no byte
   interleaving (NFR-002 / FR-026 lock-coordinated append).
4. Markdown surface is human-readable: each line begins with a dash,
   carries the ISO timestamp, event type, worker index, and payload
   k=v summary -- no JSON braces or escape noise.
5. Auto-stamped timestamps land on records the caller left blank; an
   explicit timestamp is preserved verbatim.
6. JSONL file is opened append-only -- a second logger instance
   pointed at the same path appends rather than truncating.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path

import pytest

from superclaude.cli.swarm.logging_ import Logger
from superclaude.cli.swarm.models import EventRecord, from_json


@pytest.fixture
def log_paths(tmp_path: Path) -> tuple[Path, Path]:
    """Return (jsonl_path, md_path) inside a job-scoped tmp directory."""
    job_dir = tmp_path / "job-output"
    job_dir.mkdir()
    return job_dir / "event-log.jsonl", job_dir / "event-log.md"


def test_event_record_roundtrip_through_logger(log_paths: tuple[Path, Path]) -> None:
    """EventRecord written via Logger parses back to an equal record."""
    jsonl_path, md_path = log_paths
    logger = Logger(jsonl_path, md_path)

    original = EventRecord(
        event_type="worker_done",
        timestamp="2026-06-01T09:00:00+00:00",
        worker_index=3,
        payload={"status": "success", "http_code": 200, "attempts": 1},
    )
    logger.log_event(original)

    lines = jsonl_path.read_text().splitlines()
    assert len(lines) == 1, "single event produces a single JSONL line"

    restored = from_json(EventRecord, lines[0])
    assert restored == original


def test_single_thread_emits_one_line_per_event(log_paths: tuple[Path, Path]) -> None:
    """Sequential log_event calls append in caller order."""
    jsonl_path, md_path = log_paths
    logger = Logger(jsonl_path, md_path)

    for index in range(5):
        logger.log_event(
            EventRecord(
                event_type="worker_start",
                timestamp=f"2026-06-01T09:00:0{index}+00:00",
                worker_index=index,
                payload={"slot": index},
            )
        )

    jsonl_lines = jsonl_path.read_text().splitlines()
    md_lines = md_path.read_text().splitlines()

    assert len(jsonl_lines) == 5
    assert len(md_lines) == 5

    for index, line in enumerate(jsonl_lines):
        record = from_json(EventRecord, line)
        assert record.worker_index == index
        assert record.event_type == "worker_start"


def test_markdown_surface_is_human_readable(log_paths: tuple[Path, Path]) -> None:
    """Each Markdown line begins with a dash and carries the event triple."""
    jsonl_path, md_path = log_paths
    logger = Logger(jsonl_path, md_path)

    logger.log_event(
        EventRecord(
            event_type="wave_transition",
            timestamp="2026-06-01T09:00:00+00:00",
            worker_index=None,
            payload={"from": "preflight_ok", "to": "dispatching"},
        )
    )

    md_text = md_path.read_text()
    assert md_text.startswith("- [")
    assert "wave_transition" in md_text
    assert "worker=-" in md_text
    assert "from=preflight_ok" in md_text
    assert "to=dispatching" in md_text
    # No JSON braces leaking into the human surface.
    assert "{" not in md_text
    assert "}" not in md_text


def test_concurrent_appends_produce_100_valid_jsonl_lines(
    log_paths: tuple[Path, Path],
) -> None:
    """10 threads firing 10 events each yield 100 cleanly parseable JSONL lines.

    Acceptance: ``JSONL appends serialized by threading.Lock; concurrent
    test parses every line`` (T03.04). Without the lock the underlying
    writes interleave and ``json.loads`` raises on at least one line.
    """
    jsonl_path, md_path = log_paths
    logger = Logger(jsonl_path, md_path)

    thread_count = 10
    events_per_thread = 10
    barrier = threading.Barrier(thread_count)

    def _worker(thread_id: int) -> None:
        barrier.wait()  # Maximize contention on first append.
        for index in range(events_per_thread):
            logger.log_event(
                EventRecord(
                    event_type="worker_progress",
                    worker_index=thread_id,
                    payload={
                        "thread": thread_id,
                        "step": index,
                        "note": "x" * 128,  # Make each line wide enough to expose interleaving.
                    },
                )
            )

    threads = [
        threading.Thread(target=_worker, args=(tid,))
        for tid in range(thread_count)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    raw = jsonl_path.read_text()
    lines = raw.splitlines()
    assert len(lines) == thread_count * events_per_thread, (
        f"expected {thread_count * events_per_thread} lines, got {len(lines)}"
    )
    # No interleaving: every line parses as JSON and rebuilds an EventRecord.
    parsed_pairs: set[tuple[int, int]] = set()
    for line in lines:
        payload = json.loads(line)  # raises if line is partial/interleaved
        record = from_json(EventRecord, line)
        assert record.event_type == "worker_progress"
        thread_id = payload["payload"]["thread"]
        step = payload["payload"]["step"]
        parsed_pairs.add((thread_id, step))
    # Every (thread, step) coordinate emitted is present exactly once.
    expected_pairs = {
        (tid, step)
        for tid in range(thread_count)
        for step in range(events_per_thread)
    }
    assert parsed_pairs == expected_pairs

    md_lines = md_path.read_text().splitlines()
    assert len(md_lines) == thread_count * events_per_thread, (
        "Markdown surface emits one line per event under contention"
    )


def test_auto_stamps_timestamp_when_caller_leaves_it_blank(
    log_paths: tuple[Path, Path],
) -> None:
    """A record with an empty timestamp gets a UTC ISO string at append."""
    jsonl_path, md_path = log_paths
    logger = Logger(jsonl_path, md_path)

    record = EventRecord(event_type="worker_start", worker_index=0)
    assert record.timestamp == ""

    logger.log_event(record)

    restored = from_json(EventRecord, jsonl_path.read_text().splitlines()[0])
    assert restored.timestamp != ""
    # ISO-8601 with timezone marker: contains 'T' and ends in '+00:00' or 'Z'.
    assert "T" in restored.timestamp


def test_explicit_timestamp_preserved(log_paths: tuple[Path, Path]) -> None:
    """A caller-supplied timestamp survives unchanged."""
    jsonl_path, md_path = log_paths
    logger = Logger(jsonl_path, md_path)

    stamp = "2026-06-01T09:00:00+00:00"
    logger.log_event(
        EventRecord(event_type="terminal", timestamp=stamp, payload={"outcome": "success"})
    )

    restored = from_json(EventRecord, jsonl_path.read_text().splitlines()[0])
    assert restored.timestamp == stamp


def test_jsonl_is_append_only_across_logger_instances(
    log_paths: tuple[Path, Path],
) -> None:
    """A second logger pointed at the same path appends, never truncates."""
    jsonl_path, md_path = log_paths

    first = Logger(jsonl_path, md_path)
    first.log_event(
        EventRecord(event_type="worker_start", worker_index=0, payload={"phase": 1})
    )

    # Drop the first logger; construct a fresh one at the same path.
    del first
    second = Logger(jsonl_path, md_path)
    second.log_event(
        EventRecord(event_type="worker_done", worker_index=0, payload={"phase": 1})
    )

    lines = jsonl_path.read_text().splitlines()
    assert len(lines) == 2, "second logger appended rather than truncating"
    first_record = from_json(EventRecord, lines[0])
    second_record = from_json(EventRecord, lines[1])
    assert first_record.event_type == "worker_start"
    assert second_record.event_type == "worker_done"
