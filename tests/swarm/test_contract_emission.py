"""T05.07 -- ``return-contract.yaml`` emission contract.

Pins the four acceptance criteria for the FR-018 / DM-012 contract
emitter (:func:`superclaude.cli.swarm.reduce.emit_contract`):

1. **DM-012 field completeness.** The YAML payload carries every
   top-level key declared on :class:`ResultContract` in declaration
   order, plus the nested-record sub-fields (:class:`ContractTarget`,
   :class:`CallerInfo`, :class:`CallerMetadata`, :class:`Artifacts`,
   per-entry :class:`WorkerResult` shape). Drift in either direction --
   a missing key, a renamed key, an extra key not on the dataclass --
   fails the completeness assertion.
2. **Valid YAML.** :func:`yaml.safe_load` round-trips the emitted
   payload to a Python dict that round-trips back through
   :func:`superclaude.cli.swarm.models.from_dict` into an equal
   :class:`ResultContract` instance. ``sort_keys=False`` is asserted
   at the emitter (declaration-order preservation matters for
   non-Python callers that diff the file as text per FR-030).
3. **Atomic write via tmp + ``os.replace``.** The emitter routes
   through ``reduce._atomic_write_bytes`` which uses
   ``tempfile.mkstemp`` + ``os.fsync`` + ``os.replace``. The test asserts
   the static-source contract (the symbol appears in the writer body)
   and the runtime contract (no ``.tmp`` siblings after success; a
   second emission atomically replaces the first with no corruption).
4. **``recommended_next_command`` template substitution.** The
   rendered string lands on ``contract.recommended_next_command`` (the
   on-disk YAML) with placeholders resolved from the supplied
   substitutions dict. Missing placeholders pass through unchanged
   (renderer is forgiving per FR-018; strict missing-key detection
   lives at the M2 schema layer).

Scope boundary vs ``tests/swarm/test_reduce.py``: the reduce file
exercises orchestration glue (status / merge trigger / output
confinement / emit_to_disk toggle); this file is the DM-012 surface
audit -- it pins the contract's shape on disk independent of the
orchestrator path.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest
import yaml

from superclaude.cli.swarm.models import (
    AmalgamationMode,
    Artifacts,
    CallerInfo,
    CallerMetadata,
    ContractTarget,
    ResultContract,
    ResultStatus,
    StatusPolicy,
    WorkerResult,
    from_dict,
    to_dict,
)
from superclaude.cli.swarm.reduce import (
    CONTRACT_FILENAME,
    emit_contract,
    reduce_wave3,
)

# DM-012 row declaration order (.dev/releases/Current/MultiModelSwarm/roadmap.md
# L99). Mirrors EXPECTED_FIELDS in tests/swarm/test_result_contract.py; kept
# inline here so a regression in either place fails independently.
DM012_TOP_LEVEL_KEYS: tuple[str, ...] = (
    "contract_version",
    "status",
    "job_id",
    "started",
    "finished",
    "elapsed_ms",
    "caller",
    "lens",
    "lens_source",
    "target",
    "workers_requested",
    "workers_succeeded",
    "workers_failed",
    "output_files",
    "amalgamation_mode",
    "merged_path",
    "caller_metadata",
    "recommended_next_command",
    "artifacts",
)


# Nested-record sub-fields (DM-012 dotted target.* / DM-018 / DM-019 / DM-020).
DM012_TARGET_KEYS: tuple[str, ...] = (
    "path",
    "checksum",
    "truncated",
    "truncation_line_cap",
)
DM018_ARTIFACTS_KEYS: tuple[str, ...] = (
    "manifest_path",
    "state_path",
    "event_log_jsonl",
    "event_log_md",
    "done_sentinel",
)
DM019_CALLER_KEYS: tuple[str, ...] = (
    "skill",
    "skill_version",
    "invocation_label",
    "kind",
)
DM020_METADATA_KEYS: tuple[str, ...] = (
    "suspect",
    "tier",
)
DM013_WORKER_KEYS: tuple[str, ...] = (
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


# ---------------------------------------------------------------------------
# Fixture helpers.
# ---------------------------------------------------------------------------


def _fully_populated_contract() -> ResultContract:
    """A contract with every nested record and one WorkerResult filled in.

    Drives the completeness assertions: a no-default field that the
    emitter silently drops would diverge from this fixture's payload
    on round-trip. Keeps every Literal arm exercised (status=success,
    amalgamation_mode=normalize+merge, kind=claude, worker status=success).
    """
    return ResultContract(
        contract_version="1.0",
        status="success",
        job_id="2026-06-01T13-25-39Z-bare-review-abcd",
        started="2026-06-01T13:25:39+00:00",
        finished="2026-06-01T13:26:01+00:00",
        elapsed_ms=22000,
        caller=CallerInfo(
            skill="sc-bare-review",
            skill_version="1.0",
            invocation_label="t05.07-suite",
            kind="claude",
        ),
        lens="bare-review",
        lens_source="registry",
        target=ContractTarget(
            path="/abs/path/to/target.py",
            checksum="deadbeefcafe",
            truncated=False,
            truncation_line_cap=4000,
        ),
        workers_requested=3,
        workers_succeeded=3,
        workers_failed=0,
        output_files=[
            WorkerResult(
                index=i,
                path=f"worker-{i:02d}.md",
                raw_path=f"worker-{i:02d}.raw.md",
                meta_path=f"worker-{i:02d}.meta.json",
                final_path=f"worker-{i:02d}.final.md",
                model_id=f"model-{i}",
                model_label=f"label-{i}",
                bytes=100 + i,
                status="success",
                http_code=200,
                attempts=1,
                elapsed_ms=500 + i,
            )
            for i in range(3)
        ],
        amalgamation_mode="normalize+merge",
        merged_path="/abs/path/to/merged.md",
        caller_metadata=CallerMetadata(suspect=True, tier="T2"),
        recommended_next_command="/sc:adversarial --compare a.md b.md",
        artifacts=Artifacts(
            manifest_path="/abs/manifest.json",
            state_path="/abs/.swarm-state.json",
            event_log_jsonl="/abs/event-log.jsonl",
            event_log_md="/abs/event-log.md",
            done_sentinel="/abs/done.json",
        ),
    )


# ---------------------------------------------------------------------------
# Acceptance 1 -- DM-012 field completeness.
# ---------------------------------------------------------------------------


def test_emit_contract_returns_expected_path(tmp_path: Path) -> None:
    """Returned Path equals ``output_dir / 'return-contract.yaml'``."""
    contract = ResultContract()
    written = emit_contract(contract, tmp_path)
    assert written == tmp_path / CONTRACT_FILENAME
    assert written.exists()


def test_emitted_yaml_carries_every_dm012_top_level_key(tmp_path: Path) -> None:
    """Every DM-012 key appears at the top level of the YAML payload."""
    emit_contract(_fully_populated_contract(), tmp_path)
    payload = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    assert set(payload.keys()) == set(DM012_TOP_LEVEL_KEYS), (
        f"Emitted contract keys diverged from DM-012.\n"
        f"  on disk: {sorted(payload.keys())}\n"
        f"  expected: {sorted(DM012_TOP_LEVEL_KEYS)}"
    )


def test_emitted_yaml_preserves_dm012_declaration_order(tmp_path: Path) -> None:
    """``sort_keys=False`` -> top-level keys appear in DM-012 declaration order.

    Non-Python callers (``subprocess.run(...)`` -> ``yq`` / text diff
    per FR-030) rely on the order being stable for human-readable
    diffs across runs.
    """
    emit_contract(_fully_populated_contract(), tmp_path)
    payload = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    assert tuple(payload.keys()) == DM012_TOP_LEVEL_KEYS


def test_emitted_yaml_target_subfields_complete(tmp_path: Path) -> None:
    emit_contract(_fully_populated_contract(), tmp_path)
    payload = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    assert set(payload["target"].keys()) == set(DM012_TARGET_KEYS)


def test_emitted_yaml_caller_subfields_complete(tmp_path: Path) -> None:
    emit_contract(_fully_populated_contract(), tmp_path)
    payload = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    assert set(payload["caller"].keys()) == set(DM019_CALLER_KEYS)


def test_emitted_yaml_caller_metadata_subfields_complete(tmp_path: Path) -> None:
    emit_contract(_fully_populated_contract(), tmp_path)
    payload = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    assert set(payload["caller_metadata"].keys()) == set(DM020_METADATA_KEYS)


def test_emitted_yaml_artifacts_subfields_complete(tmp_path: Path) -> None:
    emit_contract(_fully_populated_contract(), tmp_path)
    payload = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    assert set(payload["artifacts"].keys()) == set(DM018_ARTIFACTS_KEYS)


def test_emitted_yaml_output_files_carry_dm013_keys(tmp_path: Path) -> None:
    """Each ``output_files`` entry carries the full DM-013 WorkerResult shape."""
    emit_contract(_fully_populated_contract(), tmp_path)
    payload = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    assert isinstance(payload["output_files"], list)
    assert len(payload["output_files"]) == 3
    for entry in payload["output_files"]:
        assert set(entry.keys()) == set(DM013_WORKER_KEYS), (
            f"WorkerResult entry keys diverged from DM-013.\n"
            f"  on disk: {sorted(entry.keys())}\n"
            f"  expected: {sorted(DM013_WORKER_KEYS)}"
        )


def test_emitted_yaml_field_count_matches_dataclass(tmp_path: Path) -> None:
    """Number of top-level keys equals dataclasses.fields() count.

    This is the cross-check against
    :mod:`tests.swarm.test_result_contract` (which pins 19 from the
    dataclass side); here we pin from the on-disk side so a future
    field add that lands on the dataclass but not in the emitter is
    caught here too.
    """
    declared = tuple(f.name for f in dataclasses.fields(ResultContract))
    emit_contract(_fully_populated_contract(), tmp_path)
    payload = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    assert len(payload) == len(declared) == 19


# ---------------------------------------------------------------------------
# Acceptance 2 -- valid YAML + lossless round-trip.
# ---------------------------------------------------------------------------


def test_emitted_yaml_is_valid_and_round_trips_to_equal_contract(tmp_path: Path) -> None:
    instance = _fully_populated_contract()
    emit_contract(instance, tmp_path)
    payload = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    restored = from_dict(ResultContract, payload)
    assert restored == instance


def test_emitted_yaml_default_stub_round_trips(tmp_path: Path) -> None:
    """No-arg ResultContract round-trips losslessly through emit + yaml.safe_load."""
    instance = ResultContract()
    emit_contract(instance, tmp_path)
    payload = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    restored = from_dict(ResultContract, payload)
    assert restored == instance


def test_emitted_yaml_uses_utf8_unicode(tmp_path: Path) -> None:
    """``allow_unicode=True`` -- non-ASCII content survives the round-trip
    verbatim rather than being escaped to ``\\uXXXX`` sequences (matters
    for invocation_label and recommended_next_command which may carry
    multilingual content per FR-030 / scribe-persona contexts)."""
    instance = ResultContract(
        caller=CallerInfo(invocation_label="audit-éàü-1", kind="claude"),
        recommended_next_command="/sc:foo --note 'résumé'",
    )
    emit_contract(instance, tmp_path)
    text = (tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8")
    assert "audit-éàü-1" in text
    assert "résumé" in text


@pytest.mark.parametrize("status", list(["success", "partial", "failed"]))
def test_emitted_yaml_status_round_trips_each_literal(
    tmp_path: Path, status: str
) -> None:
    """Each :data:`ResultStatus` arm survives the emit round-trip."""
    instance = ResultContract(status=status)  # type: ignore[arg-type]
    emit_contract(instance, tmp_path)
    payload = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    assert payload["status"] == status


@pytest.mark.parametrize(
    "mode", list(["raw", "normalize", "normalize+merge"])
)
def test_emitted_yaml_amalgamation_mode_round_trips_each_literal(
    tmp_path: Path, mode: str
) -> None:
    """Each :data:`AmalgamationMode` arm survives the emit round-trip."""
    instance = ResultContract(amalgamation_mode=mode)  # type: ignore[arg-type]
    emit_contract(instance, tmp_path)
    payload = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    assert payload["amalgamation_mode"] == mode


def test_emitted_yaml_merged_path_none_serializes_as_yaml_null(tmp_path: Path) -> None:
    """Optional[str] None -> YAML ``null`` -> Python ``None`` (not ``"None"``)."""
    instance = ResultContract(merged_path=None)
    emit_contract(instance, tmp_path)
    payload = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    assert payload["merged_path"] is None


def test_emitted_yaml_merged_path_string_round_trips(tmp_path: Path) -> None:
    instance = ResultContract(merged_path="/abs/path/to/merged.md")
    emit_contract(instance, tmp_path)
    payload = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    assert payload["merged_path"] == "/abs/path/to/merged.md"


# ---------------------------------------------------------------------------
# Acceptance 3 -- atomic write via tmp + os.replace.
# ---------------------------------------------------------------------------


REDUCE_SRC_PATH = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "superclaude"
    / "cli"
    / "swarm"
    / "reduce.py"
)


def test_atomic_write_uses_tmp_and_os_replace() -> None:
    """Static-source assertion: the contract writer uses tmp + ``os.replace``.

    Mirrors the cross-writer sweep in
    :mod:`tests.swarm.test_imm6_atomic_write` -- a regression to a
    naive ``open(path, "wb")`` truncating write here would silently
    break IMM-6 / NFR-002 on the caller-facing contract.
    """
    source = REDUCE_SRC_PATH.read_text(encoding="utf-8")
    assert "tempfile.mkstemp" in source, (
        "reduce._atomic_write_bytes must use tempfile.mkstemp"
    )
    assert "os.replace(" in source, (
        "reduce._atomic_write_bytes must swap via os.replace"
    )
    assert "os.fsync" in source, (
        "reduce._atomic_write_bytes must fsync the tmp file before swap"
    )


def test_emit_contract_leaves_no_tmp_siblings(tmp_path: Path) -> None:
    """Successful emit -> no ``.tmp`` sibling lingers under output_dir."""
    emit_contract(_fully_populated_contract(), tmp_path)
    leftovers = [p for p in tmp_path.iterdir() if p.suffix == ".tmp"]
    assert leftovers == []


def test_emit_contract_overwrite_is_atomic(tmp_path: Path) -> None:
    """A second emit atomically replaces the first -- no partial state.

    Reads back the live file after each emit; the contents must match
    the second instance exactly (not the first, not a half-merged
    blend).
    """
    first = ResultContract(status="partial", job_id="run-1")
    second = ResultContract(status="success", job_id="run-2")

    emit_contract(first, tmp_path)
    after_first = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    assert after_first["job_id"] == "run-1"
    assert after_first["status"] == "partial"

    emit_contract(second, tmp_path)
    after_second = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    assert after_second["job_id"] == "run-2"
    assert after_second["status"] == "success"
    # No .tmp leftovers after the overwrite either.
    assert [p for p in tmp_path.iterdir() if p.suffix == ".tmp"] == []


def test_emit_contract_creates_missing_parent_directory(tmp_path: Path) -> None:
    """``output_dir`` need not exist -- the emitter mkdir's it.

    Mirrors the contract that the M5 executor's preflight materializes
    the output directory; this guard keeps the emitter usable in
    isolation by tests / one-off callers.
    """
    target_dir = tmp_path / "deep" / "nested" / "output"
    written = emit_contract(ResultContract(), target_dir)
    assert written == target_dir / CONTRACT_FILENAME
    assert written.exists()


def test_emit_contract_writes_under_supplied_output_dir(tmp_path: Path) -> None:
    """NFR-013 path confinement: nothing lands outside ``output_dir``."""
    output_dir = tmp_path / "confined"
    output_dir.mkdir()
    emit_contract(_fully_populated_contract(), output_dir)

    # Only the contract file under output_dir.
    children = sorted(p.name for p in output_dir.iterdir())
    assert children == [CONTRACT_FILENAME]
    # Nothing landed at the parent (other than the confined/ dir itself).
    siblings = sorted(p.name for p in tmp_path.iterdir())
    assert siblings == ["confined"]


# ---------------------------------------------------------------------------
# Acceptance 4 -- recommended_next_command template substitution.
# ---------------------------------------------------------------------------


def test_recommended_next_command_substitution_via_reduce_wave3(tmp_path: Path) -> None:
    """Template + substitutions resolve in the rendered command string."""
    contract = reduce_wave3(
        worker_results=[
            WorkerResult(index=0, status="success"),
            WorkerResult(index=1, status="success"),
        ],
        mode="normalize",
        output_dir=tmp_path,
        recommended_next_command_template=(
            "/sc:adversarial --merged {merged} --job {job_id} --lens {lens}"
        ),
        recommended_next_command_substitutions={
            "merged": "merged.md",
            "job_id": "abc-123",
            "lens": "bare-review",
        },
        lens="bare-review",
    )

    expected = (
        "/sc:adversarial --merged merged.md --job abc-123 --lens bare-review"
    )
    # Stamped on the in-memory contract.
    assert contract.recommended_next_command == expected
    # AND landed verbatim on the YAML payload.
    payload = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    assert payload["recommended_next_command"] == expected


def test_recommended_next_command_missing_placeholder_passes_through(
    tmp_path: Path,
) -> None:
    """Missing keys leave ``{placeholder}`` in the rendered string.

    Strict missing-key detection is the M2 schema layer's job; the
    emitter's renderer is forgiving so a partial substitutions dict
    never raises and the caller can still inspect the (un-rendered)
    template tail.
    """
    contract = reduce_wave3(
        worker_results=[
            WorkerResult(index=0, status="success"),
            WorkerResult(index=1, status="success"),
        ],
        mode="normalize",
        output_dir=tmp_path,
        recommended_next_command_template="/sc:foo --a {a} --b {missing}",
        recommended_next_command_substitutions={"a": "alpha"},
    )
    assert contract.recommended_next_command == "/sc:foo --a alpha --b {missing}"


def test_recommended_next_command_empty_template_yields_empty_string(
    tmp_path: Path,
) -> None:
    """No template + no substitutions -> rendered command is the empty string."""
    contract = reduce_wave3(
        worker_results=[
            WorkerResult(index=0, status="success"),
            WorkerResult(index=1, status="success"),
        ],
        mode="normalize",
        output_dir=tmp_path,
    )
    assert contract.recommended_next_command == ""
    payload = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    assert payload["recommended_next_command"] == ""


def test_recommended_next_command_no_substitutions_keeps_template_verbatim(
    tmp_path: Path,
) -> None:
    """Template without placeholders survives the renderer unchanged."""
    contract = reduce_wave3(
        worker_results=[
            WorkerResult(index=0, status="success"),
            WorkerResult(index=1, status="success"),
        ],
        mode="normalize",
        output_dir=tmp_path,
        recommended_next_command_template="/sc:noop --static",
    )
    assert contract.recommended_next_command == "/sc:noop --static"


# ---------------------------------------------------------------------------
# Cross-acceptance -- emit_contract <-> to_dict consistency.
# ---------------------------------------------------------------------------


def test_emit_contract_payload_matches_to_dict_output(tmp_path: Path) -> None:
    """The on-disk YAML payload equals ``to_dict(contract)``.

    Catches accidental serializer customization (extra wrappers,
    renamed keys) that would diverge from the dataclass surface
    audited by :mod:`tests.swarm.test_result_contract`.
    """
    instance = _fully_populated_contract()
    emit_contract(instance, tmp_path)
    payload = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    assert payload == to_dict(instance)


def test_emit_contract_payload_is_a_mapping_at_root(tmp_path: Path) -> None:
    """YAML root must be a mapping (callers parse ``.field`` lookups)."""
    emit_contract(ResultContract(), tmp_path)
    payload = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)


def test_emit_contract_idempotent_on_unchanged_contract(tmp_path: Path) -> None:
    """Two emits of the same instance produce byte-identical files."""
    instance = _fully_populated_contract()
    emit_contract(instance, tmp_path)
    first_bytes = (tmp_path / CONTRACT_FILENAME).read_bytes()
    emit_contract(instance, tmp_path)
    second_bytes = (tmp_path / CONTRACT_FILENAME).read_bytes()
    assert first_bytes == second_bytes


# ---------------------------------------------------------------------------
# Sanity -- module-level constants don't drift.
# ---------------------------------------------------------------------------


def test_contract_filename_constant_is_return_contract_yaml() -> None:
    """The phase-tasklist + DM-012 spec pin the filename verbatim."""
    assert CONTRACT_FILENAME == "return-contract.yaml"


def test_status_policy_default_does_not_affect_emit(tmp_path: Path) -> None:
    """``emit_contract`` is policy-agnostic -- it serializes whatever
    status the contract carries. Used here to pin that the IMM-5
    decision is *not* re-run at emit time (status drift would surface
    as a regression at this gate)."""
    instance = ResultContract(status="partial", workers_requested=3, workers_succeeded=2)
    emit_contract(instance, tmp_path)
    payload = yaml.safe_load((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    assert payload["status"] == "partial"
    # Policy is not part of the contract surface (it lives on JobSpec /
    # Manifest); confirm the emitter does not leak it onto the payload.
    assert "status_policy" not in payload
    # Sanity: the unused import keeps the symbol available for future
    # parametrize cases without altering the emit surface.
    _ = StatusPolicy()  # noqa: F841
    _ = AmalgamationMode  # noqa: F841
    _ = ResultStatus  # noqa: F841
