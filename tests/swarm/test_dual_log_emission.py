"""T03.10 -- COMP-012 dual-format log emission verification.

FR-026 / FR-045 mandate that every dispatch wave emit a paired
``execution-log.jsonl`` (canonical, append-only, lock-coordinated) and
``execution-log.md`` (human-readable) into the job's ``--output``
directory. The two files share the same record stream so they cannot
drift; dispatch wires the Logger from T03.04 into worker callbacks
and brackets the wave with two ``wave_transition`` events.

Acceptance criteria pinned here (phase-3 tasklist L358..L362):

1. ``execution-log.jsonl`` exists post-dispatch with one record per
   event (paired ``worker_start`` + ``worker_done`` per slot, plus the
   opening and closing ``wave_transition`` events).
2. ``execution-log.md`` exists with human-readable rendering of the
   same events (one dash-prefixed line per event, no JSON noise).
3. Concurrent append produces no interleaved / corrupt JSONL lines --
   every line parses cleanly, no two events share the same byte
   range (NFR-002 lock-coordinated append).
4. Both files parse end-to-end -- ``json.loads`` over every JSONL
   line and the round-trip ``from_json(EventRecord, line)`` rebuilds
   the records without raising. This is the ``jq . < execution-log.jsonl
   exits 0`` validation gate from the tasklist, expressed in-process so
   the test runs in the default ``uv run pytest`` lane without depending
   on ``jq`` being installed on the CI host.
"""

from __future__ import annotations

import json
from pathlib import Path

from superclaude.cli.swarm.dispatch import dispatch_wave1
from superclaude.cli.swarm.logging_ import Logger
from superclaude.cli.swarm.models import (
    EventRecord,
    Manifest,
    PreflightSummary,
    SwarmState,
    WorkerResult,
    from_json,
)
from superclaude.cli.swarm.preflight import PreflightResult


def _make_preflight(
    workers_requested: int, job_id: str = "job-dual-log"
) -> PreflightResult:
    manifest = Manifest(
        contract_version="1.0",
        job_id=job_id,
        preflight=PreflightSummary(
            target_checksum="cafebabe",
            workers_requested=workers_requested,
            transport_kind="stub",
        ),
    )
    state = SwarmState(state="preflight_ok", job_id=job_id)
    return PreflightResult(manifest=manifest, state=state)


class _SuccessTransport:
    def send(self, prompt: str, timeout: int) -> WorkerResult:
        return WorkerResult(status="success", http_code=200, attempts=1)


def _bootstrap_logger(out_dir: Path) -> tuple[Logger, Path, Path]:
    """Construct a Logger pointed at the canonical FR-045 filenames."""
    jsonl_path = out_dir / "execution-log.jsonl"
    md_path = out_dir / "execution-log.md"
    return Logger(jsonl_path, md_path), jsonl_path, md_path


def test_dispatch_emits_both_log_files_side_by_side(tmp_path: Path) -> None:
    """Dispatch with logger wired -> JSONL + Markdown both exist + non-empty.

    Acceptance: ``execution-log.jsonl exists post-dispatch with one
    record per event`` and ``execution-log.md exists with human-readable
    rendering of the same events`` (T03.10).
    """
    logger, jsonl_path, md_path = _bootstrap_logger(tmp_path)
    preflight = _make_preflight(workers_requested=3)
    transport = _SuccessTransport()

    results = dispatch_wave1(preflight, transport=transport, logger=logger)

    assert len(results) == 3
    assert jsonl_path.exists(), "FR-045: execution-log.jsonl must be emitted"
    assert md_path.exists(), "FR-045: execution-log.md must be emitted"
    assert jsonl_path.read_text(), "JSONL log must not be empty after dispatch"
    assert md_path.read_text(), "Markdown log must not be empty after dispatch"


def test_jsonl_parses_end_to_end(tmp_path: Path) -> None:
    """Every JSONL line parses as JSON and rebuilds an EventRecord.

    In-process equivalent of ``jq . < execution-log.jsonl`` exiting 0
    (tasklist L366). Also asserts the record stream contains the
    expected event-type triple: opening ``wave_transition``, N pairs
    of ``worker_start`` / ``worker_done``, and a closing
    ``wave_transition``.
    """
    logger, jsonl_path, _ = _bootstrap_logger(tmp_path)
    preflight = _make_preflight(workers_requested=2)

    dispatch_wave1(preflight, transport=_SuccessTransport(), logger=logger)

    lines = jsonl_path.read_text().splitlines()
    # 2 wave_transitions (open + close) + 2 workers * 2 events (start/done)
    assert len(lines) == 2 + 2 * 2

    records: list[EventRecord] = []
    for line in lines:
        json.loads(line)  # raises if line is truncated/interleaved
        records.append(from_json(EventRecord, line))

    event_types = [r.event_type for r in records]
    assert event_types[0] == "wave_transition"
    assert event_types[-1] == "wave_transition"
    # The middle stretch is exactly the worker_start/worker_done pairs
    # for each slot, in some interleaving consistent with parallel
    # execution. Multiset equality is the right assertion here.
    assert sorted(event_types[1:-1]) == sorted(
        ["worker_start", "worker_start", "worker_done", "worker_done"]
    )

    worker_indices = sorted(
        r.worker_index for r in records if r.worker_index is not None
    )
    assert worker_indices == [0, 0, 1, 1]


def test_markdown_renders_one_dash_line_per_event(tmp_path: Path) -> None:
    """Markdown surface is human-readable; one dash-prefixed line per event.

    Acceptance: ``execution-log.md exists with human-readable rendering
    of the same events`` (T03.10).
    """
    logger, jsonl_path, md_path = _bootstrap_logger(tmp_path)
    preflight = _make_preflight(workers_requested=2)

    dispatch_wave1(preflight, transport=_SuccessTransport(), logger=logger)

    md_lines = md_path.read_text().splitlines()
    jsonl_lines = jsonl_path.read_text().splitlines()
    assert len(md_lines) == len(jsonl_lines), (
        "Markdown and JSONL streams must share record count (no drift)"
    )
    for line in md_lines:
        assert line.startswith("- ["), (
            "every Markdown event line begins with a dash + ISO timestamp"
        )
        # No JSON braces leak into the human surface.
        assert "{" not in line
        assert "}" not in line


def test_concurrent_dispatch_produces_no_interleaved_jsonl(tmp_path: Path) -> None:
    """Concurrent appends from N parallel workers yield clean JSONL.

    Acceptance: ``Concurrent append test produces no interleaved/corrupt
    lines in JSONL`` (T03.10). N=8 workers fan out genuinely in parallel
    through ParallelExecutor; the per-Logger threading.Lock serializes
    the JSONL appends so every line parses cleanly.
    """
    logger, jsonl_path, _ = _bootstrap_logger(tmp_path)
    preflight = _make_preflight(workers_requested=8)

    dispatch_wave1(preflight, transport=_SuccessTransport(), logger=logger)

    lines = jsonl_path.read_text().splitlines()
    # 2 wave_transitions + 8 workers * 2 events = 18.
    assert len(lines) == 2 + 8 * 2

    parsed_slots: list[int] = []
    for line in lines:
        payload = json.loads(line)  # raises on interleaving
        if payload["event_type"] == "worker_done":
            parsed_slots.append(payload["worker_index"])
    assert sorted(parsed_slots) == list(range(8)), (
        "every worker slot must produce exactly one worker_done event"
    )


def test_logger_none_keeps_dispatch_silent(tmp_path: Path) -> None:
    """``logger=None`` -> no log files created (wire-only path stays silent).

    The wire-only smoke path (T03.01) passes ``logger=None``; dispatch
    must not stamp files into the cwd or output dir as a side effect.
    """
    jsonl_path = tmp_path / "execution-log.jsonl"
    md_path = tmp_path / "execution-log.md"
    preflight = _make_preflight(workers_requested=2)

    dispatch_wave1(preflight, transport=_SuccessTransport(), logger=None)

    assert not jsonl_path.exists()
    assert not md_path.exists()


def test_worker_done_payload_carries_terminal_outcome(tmp_path: Path) -> None:
    """``worker_done`` event payload reflects the WorkerResult fields.

    Operators reading ``execution-log.jsonl`` for post-mortem need the
    terminal outcome (status / http_code / attempts / elapsed_ms) on
    each worker_done event so they can rebuild the per-slot timeline
    without cross-referencing the result contract.
    """
    logger, jsonl_path, _ = _bootstrap_logger(tmp_path)
    preflight = _make_preflight(workers_requested=1)

    dispatch_wave1(preflight, transport=_SuccessTransport(), logger=logger)

    records = [
        from_json(EventRecord, line)
        for line in jsonl_path.read_text().splitlines()
    ]
    done_events = [r for r in records if r.event_type == "worker_done"]
    assert len(done_events) == 1
    payload = done_events[0].payload
    assert payload["status"] == "success"
    assert payload["http_code"] == 200
    assert payload["attempts"] == 1
    assert "elapsed_ms" in payload
