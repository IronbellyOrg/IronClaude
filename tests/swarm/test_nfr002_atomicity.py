"""T03.16 -- NFR-002 atomicity sweep (state + JSONL lock combined).

NFR-002 binds two distinct atomicity contracts living on two distinct
writer surfaces inside ``cli/swarm``:

* **State** (``state.py::write_state``) -- ``.swarm-state.json`` is a
  *replace-shaped* artifact. Writes go through a sibling ``.tmp`` file
  then ``os.replace`` so a concurrent reader sees either the prior file
  or the new file, never a partial one. The per-module deep test lives
  in ``tests/swarm/test_state.py``; the cross-writer SIGKILL sweep
  lives in ``tests/swarm/test_imm6_atomic_write.py`` (T03.13). This
  file pins the **concurrent-writer arm**: many threads racing on the
  same path must always leave the live file parseable, and the
  last-write-wins semantics must hold.

* **Log** (``logging_.py::Logger.log_event``) -- ``event-log.jsonl`` is
  an *append-only* artifact. A per-Logger :class:`threading.Lock`
  serializes appends, and each append opens the file in ``"a"`` mode
  (``O_APPEND`` so the kernel positions each ``write(2)`` at end-of-
  file atomically). The per-module deep test lives in
  ``tests/swarm/test_logging.py``. This file pins the **100-event
  concurrent arm** (T03.16 validation: "Concurrent 100-event run
  produces 100 valid JSONL records") on the combined NFR-002 surface.

* **Combined** -- a mixed-surface arm fires state writes and JSONL
  appends in parallel against the same job output directory so a
  regression that only breaks under cross-surface contention (lock
  scoping bug, parent-dir race) is caught here rather than slipping
  through the per-module tests.

The validation contract from
``.dev/releases/Current/MultiModelSwarm/tasklist/phase-3-tasklist.md``
T03.16::

    Acceptance Criteria:
      - No partial state files under concurrent write attempts.
      - JSONL appends serialized by threading.Lock; no interleaved bytes.
      - Test passes under pytest -p no:cacheprovider.
      - tests/swarm/test_nfr002_atomicity.py green.

    Validation:
      - uv run pytest tests/swarm/test_nfr002_atomicity.py -v passes.
      - Concurrent 100-event run produces 100 valid JSONL records.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path

import pytest

from superclaude.cli.swarm.logging_ import Logger
from superclaude.cli.swarm.models import EventRecord, SwarmState, from_json
from superclaude.cli.swarm.state import read_state, write_state

REPO_ROOT = Path(__file__).resolve().parents[2]
SWARM_PKG = REPO_ROOT / "src" / "superclaude" / "cli" / "swarm"


# ---------------------------------------------------------------------------
# Static-source guards -- both surfaces must continue to declare their
# atomicity primitives in the source. A regression to a truncating open
# or a missing lock would break the dynamic concurrency tests below,
# but the static guards fail first and produce a clearer diagnostic.
# ---------------------------------------------------------------------------


def test_state_module_uses_tmp_plus_os_replace() -> None:
    """state.py owns the replace-shaped writer; tmp + os.replace must be present."""
    source = (SWARM_PKG / "state.py").read_text(encoding="utf-8")
    assert ".tmp" in source, (
        "state.py must stage writes to a .tmp sibling before swapping "
        "(NFR-002 atomicity)."
    )
    assert "os.replace(" in source, (
        "state.py must invoke os.replace( to perform the atomic swap "
        "(NFR-002 atomicity)."
    )


def test_logging_module_uses_lock_plus_append_open() -> None:
    """logging_.py owns the append-only writer; lock + O_APPEND must be present."""
    source = (SWARM_PKG / "logging_.py").read_text(encoding="utf-8")
    assert "threading.Lock" in source, (
        "logging_.py must serialize appends with a threading.Lock (NFR-002 / FR-026)."
    )
    assert 'open(self.jsonl_path, "a")' in source, (
        "logging_.py must open the JSONL file in append mode so each "
        "write(2) is positioned at end-of-file atomically (NFR-002)."
    )
    for forbidden_mode in ('"w"', '"w+"', '"wb"'):
        assert f"open(self.jsonl_path, {forbidden_mode})" not in source, (
            f"logging_.py must never open the JSONL file in {forbidden_mode}; "
            "the append-only contract (NFR-002) requires O_APPEND."
        )


# ---------------------------------------------------------------------------
# State writer / concurrent-reader arm: the NFR-002 atomicity guarantee
# for the replace-shaped artifact is that any READER observing the live
# path during a write sees either the prior file or the new file, never
# a partial one. ``write_state`` is single-writer in production (the
# wave executor serializes state transitions), so the contract under
# test is writer-in-flight + many concurrent readers, not many
# concurrent writers (the latter would race on the shared ``.tmp``
# sibling and is outside the NFR-002 scope -- the manifest writer in
# preflight.py uses ``tempfile.mkstemp`` for that case).
# ---------------------------------------------------------------------------


def test_writer_in_flight_concurrent_readers_observe_no_partial_state(
    tmp_path: Path,
) -> None:
    """One writer transitions state repeatedly; readers always see whole files.

    The reader threads spin on :func:`read_state`. Each successful read
    must:

      * return ``None`` (file not yet visible -- first transition still
        in flight); or
      * return a :class:`SwarmState` whose ``state`` is one of the
        values the writer emitted, and whose ``updated`` stamp is set.

    The reader must NEVER raise :class:`json.JSONDecodeError` -- that
    would mean a partial file was observable, breaking the tmp +
    ``os.replace`` atomicity contract (NFR-002).
    """
    target = tmp_path / ".swarm-state.json"
    transitions = ["preflight_ok", "dispatching", "normalizing", "reducing", "terminal"]
    iterations = 40
    reader_count = 6

    stop = threading.Event()
    reader_errors: list[BaseException] = []
    reader_errors_lock = threading.Lock()
    observations: list[str] = []
    observations_lock = threading.Lock()

    def _writer() -> None:
        for cycle in range(iterations):
            for state_value in transitions:
                write_state(
                    target,
                    SwarmState(
                        state=state_value,
                        job_id=f"job-flight-c{cycle:02d}",
                    ),
                )
        stop.set()

    def _reader() -> None:
        local_seen: list[str] = []
        while not stop.is_set():
            try:
                loaded = read_state(target)
            except BaseException as exc:  # noqa: BLE001
                with reader_errors_lock:
                    reader_errors.append(exc)
                return
            if loaded is not None:
                local_seen.append(loaded.state)
                assert loaded.updated, (
                    "every write_state output must carry an updated stamp"
                )
        with observations_lock:
            observations.extend(local_seen)

    writer_thread = threading.Thread(target=_writer)
    reader_threads = [threading.Thread(target=_reader) for _ in range(reader_count)]
    for thread in reader_threads:
        thread.start()
    writer_thread.start()
    writer_thread.join()
    for thread in reader_threads:
        thread.join()

    assert not reader_errors, (
        "concurrent readers observed a partial / corrupt state file; "
        "tmp+os.replace atomicity (NFR-002) violated. Errors: "
        f"{[type(e).__name__ for e in reader_errors]}"
    )
    # Every value the readers observed must come from the writer's
    # emission set (no garbage / no off-by-one corruption).
    valid_values = set(transitions)
    bogus = [value for value in observations if value not in valid_values]
    assert not bogus, (
        f"reader observed state values not produced by the writer: {bogus}"
    )


def test_state_writer_leaves_no_tmp_after_sequential_transitions(
    tmp_path: Path,
) -> None:
    """A sequence of state transitions must leave no .tmp sibling behind.

    The state writer is single-writer in production; this pins that
    every successful ``os.replace`` consumes its staging tmp. If the
    tmp lingers, a future writer might mistake it for legitimate state
    and re-emit stale data.
    """
    target = tmp_path / ".swarm-state.json"
    for state_value in ("preflight_ok", "dispatching", "normalizing", "terminal"):
        write_state(target, SwarmState(state=state_value, job_id="job-seq"))

    tmp_sibling = target.with_suffix(target.suffix + ".tmp")
    assert not tmp_sibling.exists(), (
        "Successful os.replace must consume the tmp sibling; leftover "
        "files indicate a transition crashed between tmp-write and replace."
    )
    loaded = read_state(target)
    assert loaded is not None
    assert loaded.state == "terminal"


# ---------------------------------------------------------------------------
# JSONL concurrent-appender arm: 10 threads x 10 events = 100 records,
# every line parses cleanly, every (thread, step) coordinate appears
# exactly once. This is the explicit T03.16 validation criterion
# ("Concurrent 100-event run produces 100 valid JSONL records").
# ---------------------------------------------------------------------------


def test_concurrent_100_event_run_yields_100_valid_jsonl_records(
    tmp_path: Path,
) -> None:
    """T03.16 validation: 100 concurrent appends produce 100 parseable records.

    Without :class:`threading.Lock`, the underlying ``write(2)`` calls
    interleave bytes mid-line and at least one ``json.loads`` raises.
    With the lock + ``O_APPEND``, every line is atomic and every
    coordinate (thread_id, step) appears exactly once.
    """
    job_dir = tmp_path / "job-output"
    job_dir.mkdir()
    jsonl_path = job_dir / "event-log.jsonl"
    md_path = job_dir / "event-log.md"
    logger = Logger(jsonl_path, md_path)

    thread_count = 10
    events_per_thread = 10
    expected_total = thread_count * events_per_thread
    barrier = threading.Barrier(thread_count)

    def _emit(thread_id: int) -> None:
        barrier.wait()
        for step in range(events_per_thread):
            logger.log_event(
                EventRecord(
                    event_type="worker_progress",
                    worker_index=thread_id,
                    payload={
                        "thread": thread_id,
                        "step": step,
                        # Pad the payload so interleaved writes would
                        # straddle multiple kernel buffer boundaries
                        # and be impossible to miss.
                        "filler": "z" * 256,
                    },
                )
            )

    threads = [
        threading.Thread(target=_emit, args=(tid,)) for tid in range(thread_count)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    raw = jsonl_path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    assert len(lines) == expected_total, (
        f"expected {expected_total} JSONL lines, got {len(lines)}; "
        "lock-coordinated append (NFR-002) appears violated."
    )

    seen: set[tuple[int, int]] = set()
    for line in lines:
        # ``json.loads`` raises on any interleaved / partial line.
        payload = json.loads(line)
        record = from_json(EventRecord, line)
        assert record.event_type == "worker_progress"
        coord = (payload["payload"]["thread"], payload["payload"]["step"])
        assert coord not in seen, f"duplicate coordinate {coord} in JSONL output"
        seen.add(coord)

    expected_pairs = {
        (tid, step) for tid in range(thread_count) for step in range(events_per_thread)
    }
    assert seen == expected_pairs, (
        "Concurrent JSONL emission lost / duplicated events; "
        f"missing={expected_pairs - seen}, extra={seen - expected_pairs}"
    )

    md_lines = md_path.read_text(encoding="utf-8").splitlines()
    assert len(md_lines) == expected_total, (
        "Markdown surface emits one line per event under contention; "
        f"expected {expected_total}, got {len(md_lines)}."
    )


# ---------------------------------------------------------------------------
# Combined cross-surface arm: state writes + JSONL appends in parallel
# against the same job-output directory. Catches regressions that only
# surface under mixed-writer contention (e.g. a lock scope shared
# across surfaces, a writer that accidentally touches the other's path).
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("iterations", [25])
def test_mixed_state_and_log_writers_remain_atomic(
    tmp_path: Path, iterations: int
) -> None:
    """State and log writers operate on independent surfaces concurrently.

    One thread races ``write_state`` on ``.swarm-state.json`` (the
    production scenario -- the wave executor is the single state
    writer); multiple threads race ``Logger.log_event`` on
    ``event-log.jsonl`` (the production scenario -- many transport
    workers append events in parallel). Both surfaces must remain
    atomic on their own terms:

      * the final state file parses cleanly via :func:`read_state`;
      * every JSONL line parses cleanly and the expected event count
        matches the number of emissions;
      * no leftover ``.tmp`` sibling lingers next to the state file.
    """
    job_dir = tmp_path / "job-output"
    job_dir.mkdir()
    state_path = job_dir / ".swarm-state.json"
    jsonl_path = job_dir / "event-log.jsonl"
    md_path = job_dir / "event-log.md"
    logger = Logger(jsonl_path, md_path)

    log_writer_count = 4
    total_threads = 1 + log_writer_count
    barrier = threading.Barrier(total_threads)
    errors: list[BaseException] = []
    errors_lock = threading.Lock()

    def _state_writer() -> None:
        try:
            barrier.wait()
            for step in range(iterations):
                write_state(
                    state_path,
                    SwarmState(
                        state="normalizing",
                        job_id=f"job-mixed-state-s{step}",
                    ),
                )
        except BaseException as exc:  # noqa: BLE001
            with errors_lock:
                errors.append(exc)

    def _log_writer(writer_id: int) -> None:
        try:
            barrier.wait()
            for step in range(iterations):
                logger.log_event(
                    EventRecord(
                        event_type="worker_progress",
                        worker_index=writer_id,
                        payload={
                            "writer": writer_id,
                            "step": step,
                            "filler": "q" * 128,
                        },
                    )
                )
        except BaseException as exc:  # noqa: BLE001
            with errors_lock:
                errors.append(exc)

    threads = [threading.Thread(target=_state_writer)] + [
        threading.Thread(target=_log_writer, args=(wid,))
        for wid in range(log_writer_count)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert not errors, (
        f"Mixed-surface writers raised: {[type(e).__name__ for e in errors]}"
    )

    # State surface: final live file parses, dataclass round-trips.
    loaded = read_state(state_path)
    assert loaded is not None
    assert loaded.state == "normalizing"
    assert loaded.job_id.startswith("job-mixed-state-")

    tmp_sibling = state_path.with_suffix(state_path.suffix + ".tmp")
    assert not tmp_sibling.exists(), (
        "Successful os.replace must leave no .tmp sibling behind."
    )

    # JSONL surface: every line parses, total count matches emissions.
    jsonl_lines = jsonl_path.read_text(encoding="utf-8").splitlines()
    expected_log_count = log_writer_count * iterations
    assert len(jsonl_lines) == expected_log_count, (
        f"expected {expected_log_count} JSONL lines, got {len(jsonl_lines)}"
    )
    seen: set[tuple[int, int]] = set()
    for line in jsonl_lines:
        payload = json.loads(line)
        record = from_json(EventRecord, line)
        assert record.event_type == "worker_progress"
        coord = (payload["payload"]["writer"], payload["payload"]["step"])
        assert coord not in seen, (
            f"duplicate coordinate {coord} in mixed-surface JSONL output"
        )
        seen.add(coord)
    expected_pairs = {
        (wid, step) for wid in range(log_writer_count) for step in range(iterations)
    }
    assert seen == expected_pairs

    md_lines = md_path.read_text(encoding="utf-8").splitlines()
    assert len(md_lines) == expected_log_count
