"""FR-4 -- ``_tail_events`` byte-offset / exactly-once / partial-line tailer.

Focused unit tests for ``commands._tail_events(path, offset)`` -- the
byte-offset JSONL tailer the ``--tui`` main-thread poll loop uses to read
``EventRecord``s appended to ``execution-log.jsonl``. Pins the two distinct
disciplines that distinguish a complete-but-malformed line from a partial
trailing line:

    * A PARTIAL trailing line (no terminating newline) is buffered: the offset
      is NOT advanced past it, so the next poll re-reads it once complete and a
      half-written JSON object is never fed to ``from_json``.
    * A COMPLETE (newline-terminated) line ALWAYS advances the offset,
      regardless of parse outcome: a corrupt complete line is skipped (omitted)
      and advanced past, so it never re-parses (no infinite reparse / stall).

Also confirms the tailed records project to a NON-VACUOUS worker row via
``_project_workers``. New tests are UNMARKED.
"""

from __future__ import annotations

from superclaude.cli.swarm.commands import _tail_events
from superclaude.cli.swarm.models import EventRecord, to_json
from superclaude.cli.swarm.tui import _project_workers


def _line(rec: EventRecord) -> str:
    """Serialize an EventRecord to one newline-terminated JSONL line."""
    return to_json(rec) + "\n"


_REC_START = EventRecord(
    event_type="worker_start",
    timestamp="2026-06-18T12:00:00+00:00",
    worker_index=0,
    payload={"model_label": "stub-model-00", "timeout_sec": 180},
)
_REC_DONE = EventRecord(
    event_type="worker_done",
    timestamp="2026-06-18T12:00:03+00:00",
    worker_index=0,
    payload={"status": "success", "elapsed_ms": 3210, "model_label": "stub-model-00"},
)


def test_tail_events_partial_line_buffered_then_exactly_once(tmp_path) -> None:
    """Partial trailing line is buffered (no raise); completes next poll once."""
    log = tmp_path / "execution-log.jsonl"
    line1 = _line(_REC_START)
    line2 = _line(_REC_DONE)

    # 1) rec1 (complete) + a PARTIAL rec2 (no trailing newline).
    split = 20
    log.write_bytes((line1 + line2[:split]).encode("utf-8"))
    events, offset = _tail_events(log, 0)
    assert [e.event_type for e in events] == ["worker_start"], (
        "only the complete line should be delivered; the partial line must NOT "
        f"be delivered and must NOT raise: got {[e.event_type for e in events]}"
    )
    # Offset advanced exactly to the last complete newline (end of line1).
    assert offset == len(line1.encode("utf-8")), (
        f"offset must stop at the last complete newline; got {offset} "
        f"expected {len(line1.encode('utf-8'))}"
    )

    # 2) Append the remainder of rec2 -> now a complete line.
    with log.open("ab") as fh:
        fh.write(line2[split:].encode("utf-8"))
    events2, offset2 = _tail_events(log, offset)
    assert [e.event_type for e in events2] == ["worker_done"], (
        f"completed line must be delivered exactly once; got "
        f"{[e.event_type for e in events2]}"
    )

    # 3) Third poll, no new bytes -> nothing re-delivered (exactly-once).
    events3, offset3 = _tail_events(log, offset2)
    assert events3 == [], f"exactly-once violated: re-delivered {events3}"
    assert offset3 == offset2, "offset must not move when there are no new bytes"


def test_tail_events_corrupt_complete_line_skipped_and_advanced(tmp_path) -> None:
    """A COMPLETE-but-malformed line is skipped + advanced (no stall)."""
    log = tmp_path / "execution-log.jsonl"
    # A complete (newline-terminated) but malformed JSON line, then a valid one.
    malformed = "{not valid json}\n"
    valid = _line(_REC_DONE)
    content = malformed + valid
    log.write_bytes(content.encode("utf-8"))

    events, offset = _tail_events(log, 0)
    # (a) malformed skipped (not in list, no exception out of the helper);
    # (c) the subsequent valid record delivered exactly once.
    assert [e.event_type for e in events] == ["worker_done"], (
        "a corrupt COMPLETE line must be skipped while the following valid "
        f"record is delivered; got {[e.event_type for e in events]}"
    )
    # (b) offset advanced PAST the corrupt line (beyond ALL complete bytes).
    assert offset == len(content.encode("utf-8")), (
        f"offset must advance past the corrupt complete line; got {offset} "
        f"expected {len(content.encode('utf-8'))}"
    )

    # (d) follow-up poll with no new bytes -> empty (no re-parse / no stall).
    events_b, offset_b = _tail_events(log, offset)
    assert events_b == [], (
        f"corrupt complete line must not re-deliver / stall; got {events_b}"
    )
    assert offset_b == offset, "offset must not move with no new bytes"


def test_tail_events_records_project_to_non_vacuous_worker_row(tmp_path) -> None:
    """The tailed records project to >=1 advanced (non-pending) worker row."""
    log = tmp_path / "execution-log.jsonl"
    log.write_bytes((_line(_REC_START) + _line(_REC_DONE)).encode("utf-8"))

    events, _offset = _tail_events(log, 0)
    assert [e.event_type for e in events] == ["worker_start", "worker_done"]

    projected = _project_workers(events)
    assert len(projected) >= 1, "projection must yield >=1 worker row"
    assert any(snap.status != "pending" for snap in projected.values()), (
        "projection is vacuous: every worker row is still 'pending' -- a real "
        f"advanced worker_done was not folded in: {projected}"
    )
