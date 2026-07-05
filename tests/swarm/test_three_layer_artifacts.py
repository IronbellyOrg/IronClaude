"""T07.14 -- NFR-004 three-layer durable monitoring artifact set.

Roadmap row R-129 / NFR-004 requires that every terminal swarm job
leaves four sibling artifacts under the caller-supplied ``--output``
directory so detached / tmux / subprocess callers can recover the full
post-mortem state without re-attaching to the executor process:

    1. ``.swarm-state.json``      -- DM-014 :class:`SwarmState`,
       written by :func:`state.write_state` atomically (tmp + os.replace).
       Carries the wave-level coarse phase (``preflight_ok`` /
       ``dispatching`` / ``normalizing`` / ``reducing`` / ``terminal``)
       and the canonical ``job_id``.

    2. ``execution-log.jsonl``    -- canonical event stream, one JSON
       object per line. Written by the COMP-012 :class:`Logger`
       lock-coordinated under append-only ``O_APPEND``.

    3. ``execution-log.md``       -- human-readable rendering of the
       same event stream, one dash-prefixed line per record. Cannot
       drift from the JSONL surface because both files are appended
       under the same critical section.

    4. ``done.json``              -- DM-017 :class:`DoneSentinel`,
       written by :func:`reduce.emit_done_sentinel` atomically. The
       single-file polling marker FR-027 / FR-029 / FR-014 require so
       ``until [ -f done.json ]`` consumers can short-circuit the
       moment the run reaches terminal.

This module verifies the **artifact set** is emitted and the four
records cross-reference consistently after a full reduce-path
terminal classification. The earlier T07.13 test
(``test_done_sentinel.py``) pins the done-sentinel writer in
isolation; T07.14 stitches the building blocks together into a
stub-driven end-to-end run and asserts that all four files land in
the same output directory with mutually-agreeing field values
(``job_id``, ``terminal_status`` / ``status``, ``contract_path``).

The composition mirrors the canonical lifecycle the M5 executor
wires up in production: dispatch fans out via the stub transport
with the :class:`Logger` wired → reduce emits the contract and the
done sentinel → the state file flips to ``terminal``. The stub
transport keeps the test hermetic (no network, no real subprocess)
while exercising the real Logger + reduce + state writers
end-to-end.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from superclaude.cli.swarm.commands import (
    EXECUTION_LOG_JSONL_FILENAME,
    EXECUTION_LOG_MD_FILENAME,
    SWARM_STATE_FILENAME,
    TERMINAL_STATE_VALUE,
)
from superclaude.cli.swarm.dispatch import dispatch_wave1
from superclaude.cli.swarm.logging_ import Logger
from superclaude.cli.swarm.models import (
    EventRecord,
    Manifest,
    PreflightSummary,
    SwarmState,
    WorkerResult,
    from_dict,
    from_json,
)
from superclaude.cli.swarm.preflight import PreflightResult
from superclaude.cli.swarm.reduce import (
    CONTRACT_FILENAME,
    DONE_SENTINEL_FILENAME,
    emit_done_sentinel,
    reduce_wave3,
)
from superclaude.cli.swarm.state import read_state, write_state

# ---------------------------------------------------------------------------
# Stub harness -- assembles the four artifacts under one output directory.
# ---------------------------------------------------------------------------


JOB_ID: str = "job-T07.14-three-layer"
WORKERS_REQUESTED: int = 3


class _StubTransport:
    """Deterministic in-process transport: every send returns success.

    Mirrors the ``_SuccessTransport`` used by
    ``tests/swarm/test_dual_log_emission.py`` so the artifact emission
    path stays decoupled from the M3 concrete transports. The stub
    yields :class:`WorkerResult` instances dispatch can record on the
    JSONL ``worker_done`` events.
    """

    def send(self, prompt: str, timeout: int) -> WorkerResult:
        return WorkerResult(status="success", http_code=200, attempts=1)


def _make_preflight() -> PreflightResult:
    """Return a stub :class:`PreflightResult` for the dispatcher.

    The manifest carries the same ``job_id`` the state file + contract
    will record so the cross-artifact consistency assertions can
    triangulate on a single canonical id.
    """
    manifest = Manifest(
        contract_version="1.0",
        job_id=JOB_ID,
        preflight=PreflightSummary(
            target_checksum="deadbeef",
            workers_requested=WORKERS_REQUESTED,
            transport_kind="stub",
        ),
    )
    state = SwarmState(state="preflight_ok", job_id=JOB_ID)
    return PreflightResult(manifest=manifest, state=state)


def _run_stub_pipeline(output_dir: Path) -> dict[str, Path]:
    """Drive a stub terminal run that stamps all four NFR-004 artifacts.

    Composition mirrors the production lifecycle:

        1. :class:`Logger` instantiated against the canonical
           ``execution-log.jsonl`` / ``execution-log.md`` siblings.
        2. :func:`dispatch_wave1` fans out three stub workers; the
           logger appends ``wave_transition`` + per-slot
           ``worker_start`` / ``worker_done`` records.
        3. :func:`reduce_wave3` classifies the IMM-5 status, writes
           ``return-contract.yaml``, and -- via the explicit
           :func:`emit_done_sentinel` call below -- stamps
           ``done.json`` next to the contract.
        4. :func:`write_state` flips ``.swarm-state.json`` to the
           ``terminal`` phase carrying the canonical ``job_id``.

    Returns the absolute paths of every artifact written so the
    per-file assertions can read them back without re-deriving the
    filename constants from the modules under test.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    jsonl_path = output_dir / EXECUTION_LOG_JSONL_FILENAME
    md_path = output_dir / EXECUTION_LOG_MD_FILENAME
    contract_path = output_dir / CONTRACT_FILENAME
    state_path = output_dir / SWARM_STATE_FILENAME
    done_path = output_dir / DONE_SENTINEL_FILENAME

    logger = Logger(jsonl_path=jsonl_path, md_path=md_path)
    worker_results = dispatch_wave1(
        _make_preflight(), transport=_StubTransport(), logger=logger
    )

    contract = reduce_wave3(
        worker_results,
        mode="raw",
        output_dir=output_dir,
        workers_requested=WORKERS_REQUESTED,
        job_id=JOB_ID,
    )
    emit_done_sentinel(contract.status, contract_path)

    # Flip the state to ``terminal`` last so the on-disk record reflects
    # the post-reduce phase the M5 executor will stamp once it wires
    # the IMM-5 classification into the state machine.
    write_state(
        state_path,
        SwarmState(state=TERMINAL_STATE_VALUE, job_id=JOB_ID),
    )

    return {
        "state": state_path,
        "jsonl": jsonl_path,
        "md": md_path,
        "done": done_path,
        "contract": contract_path,
    }


@pytest.fixture
def stub_run_artifacts(tmp_path: Path) -> dict[str, Path]:
    """Yield the artifact-path map after a complete stub terminal run."""
    output_dir = tmp_path / "swarm-out"
    return _run_stub_pipeline(output_dir)


# ---------------------------------------------------------------------------
# Presence -- all four NFR-004 artifacts land under the output dir.
# ---------------------------------------------------------------------------


def test_all_four_artifacts_present_post_stub_run(
    stub_run_artifacts: dict[str, Path],
) -> None:
    """T07.14 AC: ``All four artifacts emitted`` and named per spec.

    The validation line spells out the on-disk shape: ``.swarm-state.json``,
    ``execution-log.jsonl``, ``execution-log.md``, ``done.json`` --
    all under the caller-supplied ``--output`` directory.
    """
    for label in ("state", "jsonl", "md", "done"):
        path = stub_run_artifacts[label]
        assert path.is_file(), (
            f"NFR-004 artifact {label} missing at {path}; "
            f"expected on-disk after terminal classification"
        )


def test_four_artifacts_share_an_output_directory(
    stub_run_artifacts: dict[str, Path],
) -> None:
    """NFR-013 path-confinement corollary: every artifact is a sibling.

    A caller polling ``until [ -f done.json ]`` then reading the
    contract relies on the four artifacts being siblings under one
    operator-supplied root. A drifted parent would break the
    monitoring patterns demonstrated in T07.10.
    """
    parents = {p.parent for p in stub_run_artifacts.values()}
    assert len(parents) == 1, (
        f"NFR-004 artifacts must share one output dir; got {parents!r}"
    )


def test_artifact_filenames_match_module_constants(
    stub_run_artifacts: dict[str, Path],
) -> None:
    """Pin the on-disk names to the public module constants.

    A rename of ``SWARM_STATE_FILENAME`` / ``EXECUTION_LOG_*_FILENAME``
    / ``DONE_SENTINEL_FILENAME`` without updating the monitoring
    patterns doc (T07.10) or the status / logs subcommands would
    break operator workflows; this assertion ties the test to the
    same constants those callers grep against.
    """
    assert stub_run_artifacts["state"].name == SWARM_STATE_FILENAME
    assert stub_run_artifacts["jsonl"].name == EXECUTION_LOG_JSONL_FILENAME
    assert stub_run_artifacts["md"].name == EXECUTION_LOG_MD_FILENAME
    assert stub_run_artifacts["done"].name == DONE_SENTINEL_FILENAME


# ---------------------------------------------------------------------------
# Per-artifact shape -- each file parses through the canonical dataclass.
# ---------------------------------------------------------------------------


def test_state_file_parses_as_swarm_state(
    stub_run_artifacts: dict[str, Path],
) -> None:
    """``.swarm-state.json`` round-trips through :func:`read_state`."""
    state = read_state(stub_run_artifacts["state"])
    assert state is not None
    assert state.state == TERMINAL_STATE_VALUE
    assert state.job_id == JOB_ID
    # ``updated`` is stamped by ``write_state`` on every write; the
    # state module guarantees a non-empty ISO 8601 UTC string.
    assert state.updated, "write_state must stamp SwarmState.updated"


def test_jsonl_log_parses_end_to_end(
    stub_run_artifacts: dict[str, Path],
) -> None:
    """Every JSONL line is valid JSON AND rebuilds an :class:`EventRecord`.

    In-process equivalent of ``jq . < execution-log.jsonl`` exiting 0.
    For a 3-worker stub run the record stream is the opening
    ``wave_transition`` + 3 ``worker_start`` + 3 ``worker_done`` +
    closing ``wave_transition`` = 8 lines.
    """
    lines = stub_run_artifacts["jsonl"].read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2 + WORKERS_REQUESTED * 2, (
        f"expected {2 + WORKERS_REQUESTED * 2} log lines for "
        f"{WORKERS_REQUESTED} stub workers; got {len(lines)}"
    )
    records: list[EventRecord] = []
    for line in lines:
        json.loads(line)  # raises on truncation/interleaving
        records.append(from_json(EventRecord, line))
    assert records[0].event_type == "wave_transition"
    assert records[-1].event_type == "wave_transition"


def test_markdown_log_renders_one_line_per_event(
    stub_run_artifacts: dict[str, Path],
) -> None:
    """``execution-log.md`` shares the JSONL stream's record count."""
    jsonl_lines = stub_run_artifacts["jsonl"].read_text(encoding="utf-8").splitlines()
    md_lines = stub_run_artifacts["md"].read_text(encoding="utf-8").splitlines()
    assert len(md_lines) == len(jsonl_lines), (
        "Markdown and JSONL surfaces share one record stream; "
        "drift in line counts means the Logger emitted to only "
        "one of the two files"
    )
    for line in md_lines:
        assert line.startswith("- ["), (
            f"every Markdown event line starts with a dash + ISO ts; got {line!r}"
        )


def test_done_sentinel_parses_as_done_sentinel(
    stub_run_artifacts: dict[str, Path],
) -> None:
    """``done.json`` carries the DM-017 field set + a real terminal status."""
    payload = json.loads(stub_run_artifacts["done"].read_text(encoding="utf-8"))
    assert set(payload) == {"atomic_write", "terminal_status", "contract_path"}
    assert payload["atomic_write"] is True
    assert payload["terminal_status"] in {"success", "partial", "failed"}
    assert payload["contract_path"], "done.json must point at the contract"


# ---------------------------------------------------------------------------
# Cross-artifact consistency -- terminal status / job_id triangulation.
# ---------------------------------------------------------------------------


def test_done_sentinel_terminal_status_matches_contract_status(
    stub_run_artifacts: dict[str, Path],
) -> None:
    """``done.json:terminal_status`` == ``return-contract.yaml:status``.

    T07.14 AC: ``Cross-references (terminal status) match across artifacts``.
    A drift between the sentinel and the contract would mean a poller
    reading ``done.json`` and a poller reading the contract see
    different verdicts for the same run -- exactly the post-mortem
    confusion NFR-004 exists to prevent.
    """
    done = json.loads(stub_run_artifacts["done"].read_text(encoding="utf-8"))
    contract = yaml.safe_load(
        stub_run_artifacts["contract"].read_text(encoding="utf-8")
    )
    assert done["terminal_status"] == contract["status"], (
        f"done.json terminal_status={done['terminal_status']!r} vs "
        f"return-contract.yaml status={contract['status']!r}"
    )


def test_done_sentinel_contract_path_points_at_emitted_contract(
    stub_run_artifacts: dict[str, Path],
) -> None:
    """``done.json:contract_path`` resolves to the actual contract file.

    Consumers that read the sentinel first (cheap JSON parse) then
    follow the path to the contract (richer YAML payload) rely on the
    pointer being correct. A bad pointer is silently broken until a
    consumer dereferences it.
    """
    done = json.loads(stub_run_artifacts["done"].read_text(encoding="utf-8"))
    expected_contract = stub_run_artifacts["contract"]
    assert Path(done["contract_path"]) == expected_contract


def test_state_job_id_matches_contract_job_id(
    stub_run_artifacts: dict[str, Path],
) -> None:
    """``.swarm-state.json:job_id`` == ``return-contract.yaml:job_id``.

    The triple :class:`SwarmState` + :class:`ResultContract` +
    :class:`DoneSentinel` must agree on the canonical job identifier;
    otherwise ``swarm status --job <id>`` and ``swarm logs --job <id>``
    would surface different jobs from the same output directory.
    """
    state = read_state(stub_run_artifacts["state"])
    assert state is not None
    contract = yaml.safe_load(
        stub_run_artifacts["contract"].read_text(encoding="utf-8")
    )
    assert state.job_id == contract["job_id"] == JOB_ID


def test_state_phase_is_terminal_after_done_sentinel_emitted(
    stub_run_artifacts: dict[str, Path],
) -> None:
    """``.swarm-state.json:state`` flips to ``terminal`` post-reduce.

    DM-014 wires the sentinel emit to "immediately after
    :class:`SwarmState.state` flips to ``terminal``"; the on-disk
    state file therefore reflects the terminal phase whenever
    ``done.json`` exists. ``swarm status``'s exit-code policy
    (terminal-with-non-success → exit 1) keys off this exact
    field.
    """
    state = read_state(stub_run_artifacts["state"])
    assert state is not None
    assert state.state == TERMINAL_STATE_VALUE


def test_state_round_trips_through_dataclass(
    stub_run_artifacts: dict[str, Path],
) -> None:
    """The on-disk JSON rebuilds a :class:`SwarmState` losslessly.

    Catches drift between :func:`state.write_state` and
    :func:`state.read_state` -- a serialization mismatch would
    surface here even when each file individually parses.
    """
    raw = json.loads(stub_run_artifacts["state"].read_text(encoding="utf-8"))
    restored = from_dict(SwarmState, raw)
    assert restored.state == TERMINAL_STATE_VALUE
    assert restored.job_id == JOB_ID
    assert restored.updated


def test_three_layer_set_is_complete_and_consistent(
    stub_run_artifacts: dict[str, Path],
) -> None:
    """End-to-end T07.14 acceptance line: ``all four artifacts emitted
    and consistent``.

    Aggregates the per-artifact presence + cross-reference checks into
    a single assertion block so a CI failure on this name immediately
    surfaces an NFR-004 regression.
    """
    # Presence.
    for label, path in stub_run_artifacts.items():
        assert path.is_file(), f"NFR-004 artifact {label} missing at {path}"

    # State.
    state = read_state(stub_run_artifacts["state"])
    assert state is not None
    assert state.state == TERMINAL_STATE_VALUE
    assert state.job_id == JOB_ID

    # Done sentinel.
    done = json.loads(stub_run_artifacts["done"].read_text(encoding="utf-8"))
    assert done["terminal_status"] in {"success", "partial", "failed"}

    # Contract.
    contract = yaml.safe_load(
        stub_run_artifacts["contract"].read_text(encoding="utf-8")
    )

    # Cross-references.
    assert done["terminal_status"] == contract["status"]
    assert Path(done["contract_path"]) == stub_run_artifacts["contract"]
    assert state.job_id == contract["job_id"] == JOB_ID

    # Logs share record stream.
    jsonl_lines = stub_run_artifacts["jsonl"].read_text(encoding="utf-8").splitlines()
    md_lines = stub_run_artifacts["md"].read_text(encoding="utf-8").splitlines()
    assert len(jsonl_lines) == len(md_lines) > 0
