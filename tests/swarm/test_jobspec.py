"""T01.13 -- DM-001 ``JobSpec`` field set + round-trip contract.

Covers roadmap row R-011 / DM-001. The JobSpec dataclass is the
top-level job specification serialized at job start; every downstream
artefact (manifest, contract, resume) reads from it. This suite pins:

1. Every field listed in the roadmap DM-001 row is present on JobSpec.
2. Field types match the roadmap row (nested dataclasses, Literal
   amalgamation_mode, Optional custom_prompt_dir).
3. JSON round-trip is lossless for both the default-stub instance and a
   populated instance with non-default nested records.
4. The ``amalgamation_mode`` Literal admits exactly the three values
   listed in the roadmap row (``raw`` / ``normalize`` / ``normalize+merge``).

STRICT-tier task per §4.11 (schema-bearing dataclass).
"""

from __future__ import annotations

import dataclasses
import typing

import pytest

from superclaude.cli.swarm.models import (
    AmalgamationMode,
    CallerInfo,
    JobSpec,
    NormalizationSpec,
    OutputSpec,
    PromptSpec,
    RuntimeSpec,
    StatusPolicy,
    TargetSpec,
    TransportSpec,
    WorkerSpec,
    from_dict,
    from_json,
    to_dict,
    to_json,
)


# Roadmap DM-001 row (.dev/releases/Current/MultiModelSwarm/roadmap.md L88)
# names exactly these fields, in this order. Drift in either direction
# fails the completeness assertion.
EXPECTED_FIELDS: tuple[str, ...] = (
    "spec_version",
    "job_id",
    "created",
    "caller",
    "lens",
    "custom_prompt_dir",
    "workers",
    "transport",
    "prompt",
    "target",
    "normalization",
    "output",
    "amalgamation_mode",
    "status_policy",
    "recommended_next_command_template",
    "recommended_next_command_substitutions",
    "runtime",
)


# Expected dataclass type for each nested field (keys: field name on
# JobSpec, values: the DM-### record type that field carries).
NESTED_DATACLASS_FIELDS: dict[str, type] = {
    "caller": CallerInfo,
    "workers": WorkerSpec,
    "transport": TransportSpec,
    "prompt": PromptSpec,
    "target": TargetSpec,
    "normalization": NormalizationSpec,
    "output": OutputSpec,
    "status_policy": StatusPolicy,
    "runtime": RuntimeSpec,
}


# ---------------------------------------------------------------------------
# Field-completeness.
# ---------------------------------------------------------------------------


def test_jobspec_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(JobSpec)


def test_jobspec_declares_every_dm001_field() -> None:
    """No field drift vs roadmap DM-001 row."""
    declared = tuple(f.name for f in dataclasses.fields(JobSpec))
    assert declared == EXPECTED_FIELDS, (
        f"JobSpec field set diverged from DM-001 row.\n"
        f"  declared: {declared}\n"
        f"  expected: {EXPECTED_FIELDS}"
    )


def test_jobspec_field_count_matches_dm001() -> None:
    """Sanity gate so accidental field additions/removals fail loudly."""
    assert len(dataclasses.fields(JobSpec)) == len(EXPECTED_FIELDS)


@pytest.mark.parametrize(
    "field_name,nested_cls",
    sorted(NESTED_DATACLASS_FIELDS.items()),
)
def test_nested_dataclass_field_types(field_name: str, nested_cls: type) -> None:
    """Each nested-record field carries the right DM-### type."""
    hints = typing.get_type_hints(JobSpec)
    assert hints[field_name] is nested_cls, (
        f"JobSpec.{field_name} should be typed as {nested_cls.__name__}, "
        f"got {hints[field_name]!r}"
    )


def test_custom_prompt_dir_is_optional() -> None:
    """DM-001 marks ``custom_prompt_dir:str?`` -- must accept None."""
    hints = typing.get_type_hints(JobSpec)
    field_type = hints["custom_prompt_dir"]
    # Optional[str] is Union[str, None] -- assert None is a permitted arm.
    args = typing.get_args(field_type)
    assert type(None) in args, (
        f"custom_prompt_dir must be Optional (Union[..., None]); got {field_type!r}"
    )


def test_recommended_next_command_substitutions_is_dict() -> None:
    """DM-001 marks ``recommended_next_command_substitutions:dict``."""
    hints = typing.get_type_hints(JobSpec)
    origin = typing.get_origin(hints["recommended_next_command_substitutions"])
    assert origin is dict


# ---------------------------------------------------------------------------
# amalgamation_mode Literal enforcement.
# ---------------------------------------------------------------------------


def test_amalgamation_mode_literal_values() -> None:
    """Roadmap row lists exactly ``raw`` / ``normalize`` / ``normalize+merge``."""
    args = typing.get_args(AmalgamationMode)
    assert set(args) == {"raw", "normalize", "normalize+merge"}, (
        f"AmalgamationMode admits {set(args)}; DM-001 row requires "
        "{'raw','normalize','normalize+merge'}."
    )


def test_amalgamation_mode_default_is_normalize_merge() -> None:
    """Default mode matches §7 amalgamation contract (full pipeline)."""
    assert JobSpec().amalgamation_mode == "normalize+merge"


@pytest.mark.parametrize("mode", ["raw", "normalize", "normalize+merge"])
def test_amalgamation_mode_accepts_each_literal(mode: str) -> None:
    spec = JobSpec(amalgamation_mode=mode)  # type: ignore[arg-type]
    assert spec.amalgamation_mode == mode


# ---------------------------------------------------------------------------
# Round-trip contracts.
# ---------------------------------------------------------------------------


def test_default_instance_round_trips_via_dict() -> None:
    instance = JobSpec()
    restored = from_dict(JobSpec, to_dict(instance))
    assert restored == instance


def test_default_instance_round_trips_via_json() -> None:
    instance = JobSpec()
    restored = from_json(JobSpec, to_json(instance))
    assert restored == instance


def test_populated_instance_round_trips_via_json() -> None:
    """Populating scalar + nested-dataclass fields still round-trips.

    Nested dataclasses are themselves still M1 stubs (empty), so the
    populated values exercise the scalar / dict / Optional / Literal
    paths and verify ``from_dict`` rebuilds nested instances (not raw
    dicts) so the equality check holds.
    """
    instance = JobSpec(
        spec_version="1.0",
        job_id="swarm-job-1234",
        created="2026-06-01T04:45:38+00:00",
        caller=CallerInfo(),
        lens="bare-review",
        custom_prompt_dir="/tmp/prompts",
        workers=WorkerSpec(),
        transport=TransportSpec(),
        prompt=PromptSpec(),
        target=TargetSpec(),
        normalization=NormalizationSpec(),
        output=OutputSpec(),
        amalgamation_mode="raw",
        status_policy=StatusPolicy(),
        recommended_next_command_template="/sc:foo {{job_id}}",
        recommended_next_command_substitutions={"job_id": "swarm-job-1234"},
        runtime=RuntimeSpec(),
    )
    restored = from_json(JobSpec, to_json(instance))
    assert restored == instance


def test_round_trip_diff_is_empty() -> None:
    """Acceptance criterion: round-trip diff is empty."""
    instance = JobSpec(
        spec_version="1.0",
        job_id="abc",
        lens="bare-review",
        custom_prompt_dir=None,
    )
    payload_before = to_dict(instance)
    restored = from_dict(JobSpec, payload_before)
    payload_after = to_dict(restored)
    assert payload_before == payload_after


def test_optional_custom_prompt_dir_round_trips_as_none() -> None:
    instance = JobSpec(custom_prompt_dir=None)
    restored = from_json(JobSpec, to_json(instance))
    assert restored.custom_prompt_dir is None


def test_nested_caller_is_dataclass_after_round_trip() -> None:
    """``from_dict`` must recurse so ``restored.caller`` is a CallerInfo,
    not a raw dict (would silently break the contract emitter in M5)."""
    restored = from_dict(JobSpec, to_dict(JobSpec()))
    assert isinstance(restored.caller, CallerInfo)
    assert isinstance(restored.workers, WorkerSpec)
    assert isinstance(restored.runtime, RuntimeSpec)
