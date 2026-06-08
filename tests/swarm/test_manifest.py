"""T01.27 -- DM-016 ``Manifest`` field set + round-trip + INV-016 immutability.

Covers roadmap row R-026 / DM-016. The Manifest dataclass is the
**durable source-of-truth artifact** persisted to ``manifest.json`` at
Wave 0 preflight (FR-016). INV-001 guarantees M6 resume reads
``manifest.resolved_lens_entry`` verbatim rather than re-resolving the
lens; INV-016 reinforces this by requiring the manifest to round-trip
byte-identically so a manifest written once and read back is bit-identical.

This suite pins:

1. Every field listed in the roadmap DM-016 row is present on Manifest,
   in declaration order (field-count assertion: 4 top-level keys after
   the ``preflight.*`` block collapses into nested
   :class:`PreflightSummary`).
2. The nested :class:`PreflightSummary` carries exactly the three
   ``preflight.*`` sub-fields named on the DM-016 row.
3. ``resolved_lens_entry`` is typed as :class:`ResolvedLensEntry` so the
   INV-001 / INV-016 source-of-truth contract holds: the snapshot stored
   on the manifest is the same shape M6 resume rehydrates from.
4. JSON round-trip is lossless for the default-stub instance and a
   populated instance.
5. ``resolved_lens_entry`` is preserved verbatim through the round-trip
   (T01.27 acceptance: "resolved_lens_entry preserved verbatim") --
   constructing a manifest from a :class:`ResolvedLensEntry.from_lens`
   snapshot and round-tripping it yields the same snapshot bytes.
6. INV-016 immutability: ``to_json`` is byte-identical across two
   encodings of the same Manifest (T01.27 acceptance: "Bytes-identical
   round-trip").
7. A Manifest carrying a populated ResolvedLensEntry rehydrates the
   snapshot via ``from_dict`` recursion (the M6 resume path).

STRICT-tier task per §4.11 (INV-001 / INV-016 source-of-truth anchor).
"""

from __future__ import annotations

import dataclasses
import typing

import pytest

from superclaude.cli.swarm.models import (
    LensEntry,
    Manifest,
    PreflightSummary,
    ResolvedLensEntry,
    from_dict,
    from_json,
    to_dict,
    to_json,
)

# Roadmap DM-016 row (.dev/releases/Current/MultiModelSwarm/roadmap.md L103)
# names ``contract_version``, ``job_id``, ``resolved_lens_entry``, and three
# dotted ``preflight.*`` sub-fields. The three sub-fields collapse into a
# single nested :class:`PreflightSummary` dataclass (same pattern as
# ``RetryPolicy`` on WorkerSpec and ``ContractTarget`` on ResultContract).
#
# F-P2-2 adds a fifth top-level field, ``caller_metadata`` (DM-020), so a
# caller-supplied OQ-009 override (suspect / tier) provided at Wave 0 persists
# in ``manifest.json`` and survives executor restart / resume rather than
# living only in-memory on PreflightResult. The field is versioned by the
# manifest's ``contract_version`` and defaulted (backward-compatible). See
# ``src/superclaude/cli/swarm/models.py::Manifest`` and the F-P2-2 remediation.
EXPECTED_TOP_LEVEL_FIELDS: tuple[str, ...] = (
    "contract_version",
    "job_id",
    "resolved_lens_entry",
    "preflight",
    "caller_metadata",
)


EXPECTED_PREFLIGHT_FIELDS: tuple[str, ...] = (
    "target_checksum",
    "workers_requested",
    "transport_kind",
)


# ---------------------------------------------------------------------------
# Field-completeness.
# ---------------------------------------------------------------------------


def test_manifest_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(Manifest)


def test_preflight_summary_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(PreflightSummary)


def test_manifest_declares_every_dm016_field() -> None:
    """No field drift vs roadmap DM-016 row (post-nested-collapse)."""
    declared = tuple(f.name for f in dataclasses.fields(Manifest))
    assert declared == EXPECTED_TOP_LEVEL_FIELDS, (
        f"Manifest field set diverged from DM-016 row.\n"
        f"  declared: {declared}\n"
        f"  expected: {EXPECTED_TOP_LEVEL_FIELDS}"
    )


def test_preflight_summary_declares_every_dm016_subfield() -> None:
    """The three ``preflight.*`` sub-fields on the DM-016 row collapse into
    PreflightSummary; no drift in either direction."""
    declared = tuple(f.name for f in dataclasses.fields(PreflightSummary))
    assert declared == EXPECTED_PREFLIGHT_FIELDS, (
        f"PreflightSummary field set diverged from DM-016 row.\n"
        f"  declared: {declared}\n"
        f"  expected: {EXPECTED_PREFLIGHT_FIELDS}"
    )


def test_resolved_lens_entry_field_is_typed_resolvedlens() -> None:
    """The ``resolved_lens_entry`` field MUST be typed as
    :class:`ResolvedLensEntry` so the INV-001 / INV-016 source-of-truth
    contract holds: the snapshot the manifest carries is the same shape M6
    resume rehydrates from. Drifting to a raw dict / Any would break the
    snapshot guarantee."""
    hints = typing.get_type_hints(Manifest)
    assert hints["resolved_lens_entry"] is ResolvedLensEntry


def test_preflight_field_is_typed_preflight_summary() -> None:
    hints = typing.get_type_hints(Manifest)
    assert hints["preflight"] is PreflightSummary


@pytest.mark.parametrize(
    "field_name,expected_type",
    [
        ("contract_version", str),
        ("job_id", str),
    ],
)
def test_manifest_scalar_field_types(field_name: str, expected_type: type) -> None:
    hints = typing.get_type_hints(Manifest)
    assert hints[field_name] is expected_type, (
        f"Manifest.{field_name} should be typed as "
        f"{expected_type.__name__}, got {hints[field_name]!r}"
    )


@pytest.mark.parametrize(
    "field_name,expected_type",
    [
        ("target_checksum", str),
        ("workers_requested", int),
        ("transport_kind", str),
    ],
)
def test_preflight_scalar_field_types(field_name: str, expected_type: type) -> None:
    hints = typing.get_type_hints(PreflightSummary)
    assert hints[field_name] is expected_type, (
        f"PreflightSummary.{field_name} should be typed as "
        f"{expected_type.__name__}, got {hints[field_name]!r}"
    )


# ---------------------------------------------------------------------------
# Defaults.
# ---------------------------------------------------------------------------


def test_contract_version_default_mirrors_result_contract() -> None:
    """Manifest and its terminal ResultContract carry the same schema
    version so the schema layer (M2) can validate them under one rule."""
    assert Manifest().contract_version == "1.0"


def test_resolved_lens_entry_default_is_stub_instance() -> None:
    """The default exists so the aggregator's no-arg round-trip suite keeps
    passing; real instances come from ``ResolvedLensEntry.from_lens`` at
    preflight."""
    assert isinstance(Manifest().resolved_lens_entry, ResolvedLensEntry)


def test_preflight_default_is_stub_instance() -> None:
    assert isinstance(Manifest().preflight, PreflightSummary)


def test_preflight_summary_defaults_are_empty_sentinels() -> None:
    """PreflightSummary defaults are empty/zero sentinels stamped at Wave 0
    preflight emit (COMP-006)."""
    p = PreflightSummary()
    assert p.target_checksum == ""
    assert p.workers_requested == 0
    assert p.transport_kind == ""


# ---------------------------------------------------------------------------
# Round-trip contracts.
# ---------------------------------------------------------------------------


def test_default_instance_round_trips_via_dict() -> None:
    instance = Manifest()
    restored = from_dict(Manifest, to_dict(instance))
    assert restored == instance


def test_default_instance_round_trips_via_json() -> None:
    instance = Manifest()
    restored = from_json(Manifest, to_json(instance))
    assert restored == instance


def test_preflight_summary_round_trips_via_json() -> None:
    instance = PreflightSummary(
        target_checksum="deadbeefcafe",
        workers_requested=4,
        transport_kind="openai_compat",
    )
    restored = from_json(PreflightSummary, to_json(instance))
    assert restored == instance


def _populated_lens() -> LensEntry:
    """Same shape as the populated LensEntry used in the DM-011 suite so
    behaviour is consistent across the snapshot's tests."""
    return LensEntry(
        name="bare_review",
        description="Unscaffolded native-instinct review",
        system_prompt_fragment=(
            "You are reviewing the block between <<<TARGET>>> and <<<END TARGET>>>."
        ),
        user_template="Review the target block.\n\nTarget:\n{target}\n",
        output_template_path="templates/bare_review.md",
        recipe_name="bare_review",
        default_workers=3,
        default_target_line_cap=4000,
        suspect=True,
        tier="T2",
        recommended_next_command_template="/sc:foo {suspect_files}",
        acceptance_notes="entry passes validator",
        stability="stable",
    )


def _populated_manifest() -> Manifest:
    return Manifest(
        contract_version="1.0",
        job_id="00000000-0000-0000-0000-000000000000",
        resolved_lens_entry=ResolvedLensEntry.from_lens(_populated_lens()),
        preflight=PreflightSummary(
            target_checksum="deadbeefcafe",
            workers_requested=3,
            transport_kind="openai_compat",
        ),
    )


def test_populated_instance_round_trips_via_json() -> None:
    """Populating every field still round-trips losslessly through the
    nested-dataclass-recursing helpers."""
    instance = _populated_manifest()
    restored = from_json(Manifest, to_json(instance))
    assert restored == instance


def test_round_trip_diff_is_empty() -> None:
    """Acceptance criterion: round-trip diff is empty."""
    instance = _populated_manifest()
    payload_before = to_dict(instance)
    restored = from_dict(Manifest, payload_before)
    payload_after = to_dict(restored)
    assert payload_before == payload_after


def test_resolved_lens_entry_preserved_verbatim_through_round_trip() -> None:
    """T01.27 acceptance: ``resolved_lens_entry`` preserved verbatim. The
    snapshot bytes that go into the manifest are the same bytes M6 resume
    reads back -- the INV-001 anchor."""
    snapshot = ResolvedLensEntry.from_lens(_populated_lens())
    instance = Manifest(
        contract_version="1.0",
        job_id="job-1",
        resolved_lens_entry=snapshot,
        preflight=PreflightSummary(
            target_checksum="deadbeef",
            workers_requested=3,
            transport_kind="openai_compat",
        ),
    )
    restored = from_json(Manifest, to_json(instance))
    assert restored.resolved_lens_entry == snapshot
    # Verbatim strings (whitespace-sensitive fields) survive intact.
    assert (
        restored.resolved_lens_entry.system_prompt_fragment
        == snapshot.system_prompt_fragment
    )
    assert restored.resolved_lens_entry.user_template == snapshot.user_template


def test_resolved_lens_entry_rehydrated_as_dataclass_not_dict() -> None:
    """The M6 resume path reads ``manifest.resolved_lens_entry`` and treats
    it as a :class:`ResolvedLensEntry`. The round-trip helpers must rebuild
    the snapshot as a dataclass instance, not leave it as a raw dict."""
    instance = _populated_manifest()
    restored = from_json(Manifest, to_json(instance))
    assert isinstance(restored.resolved_lens_entry, ResolvedLensEntry)
    assert isinstance(restored.preflight, PreflightSummary)


# ---------------------------------------------------------------------------
# INV-016 byte-identical round-trip (T01.27 validation: "Bytes-identical
# round-trip").
# ---------------------------------------------------------------------------


def test_byte_identical_round_trip_for_default_instance() -> None:
    """INV-016: two encodings of the same default Manifest must be
    byte-identical (``to_json`` uses ``sort_keys=True``)."""
    instance = Manifest()
    encoded_once = to_json(instance)
    restored = from_json(Manifest, encoded_once)
    encoded_twice = to_json(restored)
    assert encoded_once == encoded_twice


def test_byte_identical_round_trip_for_populated_instance() -> None:
    """INV-016 source-of-truth contract: a populated manifest written once
    and read back must re-serialize bit-identical."""
    instance = _populated_manifest()
    encoded_once = to_json(instance)
    restored = from_json(Manifest, encoded_once)
    encoded_twice = to_json(restored)
    assert encoded_once == encoded_twice


def test_byte_identical_round_trip_across_multiple_cycles() -> None:
    """Round-trip stability across more than one cycle -- a manifest that
    flows through executor -> attach -> resume must remain byte-identical
    regardless of how many read/write cycles intervene."""
    instance = _populated_manifest()
    encoded = to_json(instance)
    for _ in range(5):
        restored = from_json(Manifest, encoded)
        re_encoded = to_json(restored)
        assert re_encoded == encoded
        encoded = re_encoded


# ---------------------------------------------------------------------------
# Snapshot independence (INV-001 reinforcement at the Manifest level).
# ---------------------------------------------------------------------------


def test_round_trip_decouples_manifest_from_originating_lens_entry() -> None:
    """INV-001 anchor at the Manifest level: once a Manifest carries a
    :class:`ResolvedLensEntry` snapshot, editing the originating LensEntry
    must not affect the manifest's snapshot. The round-trip path further
    decouples the rebuilt instance from any in-memory aliasing."""
    entry = _populated_lens()
    snapshot = ResolvedLensEntry.from_lens(entry)
    instance = Manifest(
        resolved_lens_entry=snapshot,
        preflight=PreflightSummary(transport_kind="openai_compat"),
    )
    encoded = to_json(instance)
    # Mutate the LensEntry post-encode.
    entry.system_prompt_fragment = "MUTATED"
    entry.recommended_next_command_template = "MUTATED"
    # Restored manifest still carries the snapshot's original values.
    restored = from_json(Manifest, encoded)
    assert restored.resolved_lens_entry.system_prompt_fragment != "MUTATED"
    assert restored.resolved_lens_entry.recommended_next_command_template != "MUTATED"
