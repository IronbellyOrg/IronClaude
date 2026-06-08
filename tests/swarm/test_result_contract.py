"""T01.25 -- DM-012 ``ResultContract`` field set + round-trip contract.

Covers roadmap row R-022 / DM-012. The ResultContract dataclass is the
**caller-facing terminal artifact** emitted at Wave 3 reduce (COMP-009,
M5) per FR-018; it is written to ``return-contract.yaml`` and, when
``RuntimeSpec.on_completion.print_contract_to_stdout`` is True, printed
to stdout so non-Claude callers (``subprocess.run(...)``, FR-030) can
parse it without reading artefacts off disk.

This suite pins:

1. Every field listed in the roadmap DM-012 row is present on
   ResultContract, in declaration order. The four ``target.*`` dotted
   sub-fields collapse into a single nested :class:`ContractTarget`
   record (same pattern as :class:`RetryPolicy` on :class:`WorkerSpec`),
   leaving **19 top-level keys** on the contract -- one per record
   enumerated in the T01.25 acceptance block. The phase-tasklist
   validation line citing "18 top-level keys" is an off-by-one against
   the same acceptance enumeration; this suite trusts the enumeration.
2. Field types match the roadmap row (nested CallerInfo / ContractTarget
   / CallerMetadata / Artifacts dataclasses, ``list[WorkerResult]``,
   Literal ``status``, Literal ``amalgamation_mode``, Optional
   ``merged_path``).
3. ``status`` is a Literal admitting exactly the three values from the
   T01.25 acceptance criterion (``success`` / ``partial`` / ``failed``);
   out-of-enum values raise ``ValueError`` at construction.
4. ``ContractTarget`` carries the four DM-012 ``target.*`` sub-fields
   verbatim and defaults match §5 Result Contract Schema (truncation_line_cap
   mirrors FR-SPEC-005 / 4000).
5. JSON round-trip is lossless for the default-stub instance, a
   populated instance with non-default nested records, and a populated
   instance with a non-empty ``output_files`` list -- exercising the
   T01.25 round-trip-helper extension that recurses into
   ``list[<dataclass>]`` so populated lists rebuild as
   :class:`WorkerResult` instances rather than raw dicts.
6. ``merged_path`` is Optional and round-trips as ``None`` (matches the
   §5 "null when amalgamation_mode != normalize+merge OR M < 2" rule
   surface).
7. Helper internals: the new ``_list_dataclass_item_type`` helper is
   not strictly part of the public surface, but the round-trip test
   for populated ``output_files`` would silently rebuild
   ``list[dict]`` instead of ``list[WorkerResult]`` if the helper
   regressed -- this is caught by the equality assertion in the
   populated round-trip plus a direct ``isinstance`` check.

STRICT-tier task per §4.11 Critical Path Override (caller-facing
contract; INV-001 / INV-016 / FR-018 anchor). HIGH risk per T01.25
because the contract surface drives every non-Claude caller's parsing
contract -- any field drift here cascades into M5 emitter (COMP-009),
M6 resume reads, and M7 detached-mode contract retrieval.
"""

from __future__ import annotations

import dataclasses
import typing

import pytest

from superclaude.cli.swarm.models import (
    AmalgamationMode,
    Artifacts,
    CallerInfo,
    CallerMetadata,
    ContractTarget,
    ResultContract,
    ResultStatus,
    WorkerResult,
    from_dict,
    from_json,
    to_dict,
    to_json,
)


# Roadmap DM-012 row (.dev/releases/Current/MultiModelSwarm/roadmap.md L99)
# names exactly these top-level fields, in this order. The four dotted
# ``target.*`` sub-fields collapse into the ``target`` nested record
# (:class:`ContractTarget`), same pattern as ``retry`` on WorkerSpec and
# ``on_completion`` on RuntimeSpec. Drift in either direction fails the
# completeness assertion.
EXPECTED_FIELDS: tuple[str, ...] = (
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


# Expected dataclass type for each nested-record field (keys: field name
# on ResultContract, values: the DM-### record / nested type that field
# carries).
NESTED_DATACLASS_FIELDS: dict[str, type] = {
    "caller": CallerInfo,
    "target": ContractTarget,
    "caller_metadata": CallerMetadata,
    "artifacts": Artifacts,
}


# Sub-fields carried by the nested :class:`ContractTarget` record (the
# four dotted ``target.*`` keys from the roadmap row).
EXPECTED_TARGET_FIELDS: tuple[str, ...] = (
    "path",
    "checksum",
    "truncated",
    "truncation_line_cap",
)


# ---------------------------------------------------------------------------
# Field-completeness on ResultContract.
# ---------------------------------------------------------------------------


def test_result_contract_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(ResultContract)


def test_result_contract_declares_every_dm012_field() -> None:
    """No field drift vs roadmap DM-012 row."""
    declared = tuple(f.name for f in dataclasses.fields(ResultContract))
    assert declared == EXPECTED_FIELDS, (
        f"ResultContract field set diverged from DM-012 row.\n"
        f"  declared: {declared}\n"
        f"  expected: {EXPECTED_FIELDS}"
    )


def test_result_contract_top_level_key_count_is_19() -> None:
    """T01.25 acceptance criterion enumeration carries 19 records.

    The phase-tasklist validation line ("Field-completeness assertion:
    18 top-level keys") is an off-by-one against its own acceptance
    block -- the acceptance enumeration itself names exactly 19. This
    suite pins 19 to match the enumeration and roadmap row.
    """
    assert len(dataclasses.fields(ResultContract)) == 19


@pytest.mark.parametrize(
    "field_name,nested_cls",
    sorted(NESTED_DATACLASS_FIELDS.items()),
)
def test_nested_dataclass_field_types(field_name: str, nested_cls: type) -> None:
    """Each nested-record field carries the right DM-### / nested type."""
    hints = typing.get_type_hints(ResultContract)
    assert hints[field_name] is nested_cls, (
        f"ResultContract.{field_name} should be typed as "
        f"{nested_cls.__name__}, got {hints[field_name]!r}"
    )


@pytest.mark.parametrize(
    "field_name,expected_type",
    [
        ("contract_version", str),
        ("job_id", str),
        ("started", str),
        ("finished", str),
        ("elapsed_ms", int),
        ("lens", str),
        ("lens_source", str),
        ("workers_requested", int),
        ("workers_succeeded", int),
        ("workers_failed", int),
        ("recommended_next_command", str),
    ],
)
def test_scalar_field_types(field_name: str, expected_type: type) -> None:
    """Each scalar field carries the right Python type per DM-012."""
    hints = typing.get_type_hints(ResultContract)
    assert hints[field_name] is expected_type, (
        f"ResultContract.{field_name} should be typed as "
        f"{expected_type.__name__}, got {hints[field_name]!r}"
    )


def test_output_files_is_list_of_worker_result() -> None:
    """``output_files`` is ``list[WorkerResult]`` per DM-012 row."""
    hints = typing.get_type_hints(ResultContract)
    field_type = hints["output_files"]
    assert typing.get_origin(field_type) is list, (
        f"output_files should be a list, got {field_type!r}"
    )
    args = typing.get_args(field_type)
    assert args == (WorkerResult,), (
        f"output_files should be list[WorkerResult], got list{list(args)!r}"
    )


def test_merged_path_is_optional() -> None:
    """DM-012 marks ``merged_path:str?`` -- must accept None."""
    hints = typing.get_type_hints(ResultContract)
    field_type = hints["merged_path"]
    # Optional[str] is Union[str, None] -- assert None is a permitted arm.
    args = typing.get_args(field_type)
    assert type(None) in args, (
        f"merged_path must be Optional (Union[..., None]); got {field_type!r}"
    )


# ---------------------------------------------------------------------------
# status Literal enforcement.
# ---------------------------------------------------------------------------


def test_status_literal_values() -> None:
    """T01.25 acceptance: ``status`` admits exactly success / partial / failed."""
    args = typing.get_args(ResultStatus)
    assert set(args) == {"success", "partial", "failed"}, (
        f"ResultStatus admits {set(args)}; T01.25 acceptance requires "
        "{'success','partial','failed'}."
    )


def test_status_default_is_success() -> None:
    """Conservative default so the no-arg round-trip suite keeps passing.

    Real instances are stamped by IMM-5 at Wave 3 reduce (COMP-009).
    """
    assert ResultContract().status == "success"


@pytest.mark.parametrize("status", ["success", "partial", "failed"])
def test_status_accepts_each_literal(status: str) -> None:
    contract = ResultContract(status=status)  # type: ignore[arg-type]
    assert contract.status == status


def test_status_rejects_unknown_value() -> None:
    """A manually-constructed contract cannot smuggle an out-of-enum
    status into ``return-contract.yaml`` (FR-018 surface)."""
    with pytest.raises(ValueError, match="status"):
        ResultContract(status="bogus")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# amalgamation_mode Literal alignment with JobSpec.
# ---------------------------------------------------------------------------


def test_amalgamation_mode_is_amalgamation_literal() -> None:
    """ResultContract reuses :data:`AmalgamationMode` so the contract's
    type contract matches its source (JobSpec)."""
    hints = typing.get_type_hints(ResultContract)
    assert hints["amalgamation_mode"] is AmalgamationMode


def test_amalgamation_mode_default_is_normalize_merge() -> None:
    """Mirrors JobSpec default per §4.1 (full pipeline)."""
    assert ResultContract().amalgamation_mode == "normalize+merge"


# ---------------------------------------------------------------------------
# ContractTarget nested record.
# ---------------------------------------------------------------------------


def test_contract_target_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(ContractTarget)


def test_contract_target_declares_every_target_dotted_field() -> None:
    """ContractTarget carries the four DM-012 ``target.*`` sub-fields."""
    declared = tuple(f.name for f in dataclasses.fields(ContractTarget))
    assert declared == EXPECTED_TARGET_FIELDS, (
        f"ContractTarget field set diverged from DM-012 target.* sub-fields.\n"
        f"  declared: {declared}\n"
        f"  expected: {EXPECTED_TARGET_FIELDS}"
    )


@pytest.mark.parametrize(
    "field_name,expected_type",
    [
        ("path", str),
        ("checksum", str),
        ("truncated", bool),
        ("truncation_line_cap", int),
    ],
)
def test_contract_target_field_types(field_name: str, expected_type: type) -> None:
    hints = typing.get_type_hints(ContractTarget)
    assert hints[field_name] is expected_type, (
        f"ContractTarget.{field_name} should be typed as "
        f"{expected_type.__name__}, got {hints[field_name]!r}"
    )


def test_contract_target_truncation_line_cap_default_mirrors_truncation() -> None:
    """Default mirrors :class:`Truncation` (FR-SPEC-005 / 4000)."""
    assert ContractTarget().truncation_line_cap == 4000


def test_contract_target_truncated_default_is_false() -> None:
    """Default: no truncation occurred."""
    assert ContractTarget().truncated is False


# ---------------------------------------------------------------------------
# Defaults that downstream tasks rely on.
# ---------------------------------------------------------------------------


def test_contract_version_default_is_1_0() -> None:
    """Mirrors §5 spec block + manifest contract_version (T01.27)."""
    assert ResultContract().contract_version == "1.0"


def test_merged_path_default_is_none() -> None:
    """§5: null when ``amalgamation_mode != normalize+merge`` OR ``M < 2``."""
    assert ResultContract().merged_path is None


def test_output_files_default_is_empty_list() -> None:
    assert ResultContract().output_files == []


def test_worker_counts_default_to_zero() -> None:
    contract = ResultContract()
    assert contract.workers_requested == 0
    assert contract.workers_succeeded == 0
    assert contract.workers_failed == 0


# ---------------------------------------------------------------------------
# Round-trip contracts.
# ---------------------------------------------------------------------------


def test_default_instance_round_trips_via_dict() -> None:
    instance = ResultContract()
    restored = from_dict(ResultContract, to_dict(instance))
    assert restored == instance


def test_default_instance_round_trips_via_json() -> None:
    instance = ResultContract()
    restored = from_json(ResultContract, to_json(instance))
    assert restored == instance


def test_populated_instance_round_trips_via_json() -> None:
    """Populating scalar + nested-dataclass fields still round-trips.

    Nested dataclasses other than ContractTarget (CallerInfo,
    CallerMetadata, Artifacts) are themselves still M1 stubs (empty);
    the populated values exercise the scalar / Literal / Optional /
    nested-dataclass paths.
    """
    instance = ResultContract(
        contract_version="1.0",
        status="success",
        job_id="2026-06-01T05-23-38Z-bare-review-7f3a",
        started="2026-06-01T05:23:38+00:00",
        finished="2026-06-01T05:24:01+00:00",
        elapsed_ms=23000,
        caller=CallerInfo(),
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
        output_files=[],
        amalgamation_mode="normalize+merge",
        merged_path="/abs/path/to/merged.md",
        caller_metadata=CallerMetadata(),
        recommended_next_command="/sc:adversarial --compare a.md b.md",
        artifacts=Artifacts(),
    )
    restored = from_json(ResultContract, to_json(instance))
    assert restored == instance


def test_populated_output_files_round_trip_as_worker_result_instances() -> None:
    """T01.25 helper extension: ``list[<dataclass>]`` must rebuild as
    dataclass instances, not raw dicts. Without the
    ``_list_dataclass_item_type`` branch in ``from_dict``, ``output_files``
    would round-trip as ``list[dict]`` and equality would fail (and the
    M5 contract emitter would silently emit dicts where it expected
    WorkerResult instances).

    WorkerResult is still an empty stub at M1 (fields land in T01.26),
    so ``WorkerResult() == WorkerResult()`` holds but ``WorkerResult() !=
    {}``. That asymmetry is precisely what this test guards.
    """
    instance = ResultContract(
        output_files=[WorkerResult(), WorkerResult(), WorkerResult()],
    )
    restored = from_json(ResultContract, to_json(instance))
    assert restored == instance
    assert len(restored.output_files) == 3
    for item in restored.output_files:
        assert isinstance(item, WorkerResult), (
            f"output_files entry should rebuild as WorkerResult, got {type(item).__name__}"
        )


def test_round_trip_diff_is_empty() -> None:
    """Acceptance criterion: round-trip diff is empty."""
    instance = ResultContract(
        contract_version="1.0",
        status="partial",
        job_id="abc",
        elapsed_ms=42,
        lens="custom",
        lens_source="custom",
        target=ContractTarget(path="/x", checksum="abc123", truncated=True),
        workers_requested=4,
        workers_succeeded=3,
        workers_failed=1,
        merged_path=None,
    )
    payload_before = to_dict(instance)
    restored = from_dict(ResultContract, payload_before)
    payload_after = to_dict(restored)
    assert payload_before == payload_after


def test_optional_merged_path_round_trips_as_none() -> None:
    instance = ResultContract(merged_path=None)
    restored = from_json(ResultContract, to_json(instance))
    assert restored.merged_path is None


def test_optional_merged_path_round_trips_as_str() -> None:
    instance = ResultContract(merged_path="/abs/path/to/merged.md")
    restored = from_json(ResultContract, to_json(instance))
    assert restored.merged_path == "/abs/path/to/merged.md"


def test_nested_caller_is_dataclass_after_round_trip() -> None:
    """``from_dict`` must recurse so each nested field rebuilds as its
    DM-### type, not a raw dict (would silently break the contract
    emitter in M5 and any caller introspecting the rebuilt struct)."""
    restored = from_dict(ResultContract, to_dict(ResultContract()))
    assert isinstance(restored.caller, CallerInfo)
    assert isinstance(restored.target, ContractTarget)
    assert isinstance(restored.caller_metadata, CallerMetadata)
    assert isinstance(restored.artifacts, Artifacts)


def test_contract_target_round_trips_independently() -> None:
    """ContractTarget is part of the public surface (exported in
    ``__all__``); round-trip works standalone too."""
    instance = ContractTarget(
        path="/abs/path",
        checksum="abc123",
        truncated=True,
        truncation_line_cap=2048,
    )
    restored = from_json(ContractTarget, to_json(instance))
    assert restored == instance


def test_byte_identical_round_trip_under_sorted_json() -> None:
    """``to_json`` uses ``sort_keys=True`` so a second encoding of the
    restored contract must be byte-identical to the first. FR-018 /
    INV-016 surfaces rely on this once the M5 emitter lands so a
    contract written once and read back is bit-identical."""
    instance = ResultContract(
        contract_version="1.0",
        status="success",
        job_id="abc",
        elapsed_ms=1,
        lens="bare-review",
        lens_source="registry",
        target=ContractTarget(path="/x", checksum="abc123"),
        workers_requested=2,
        workers_succeeded=2,
        merged_path="/merged.md",
        output_files=[WorkerResult(), WorkerResult()],
    )
    encoded_once = to_json(instance)
    restored = from_json(ResultContract, encoded_once)
    encoded_twice = to_json(restored)
    assert encoded_once == encoded_twice
