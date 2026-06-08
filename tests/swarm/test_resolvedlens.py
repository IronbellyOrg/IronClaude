"""T01.24 -- DM-011 ``ResolvedLensEntry`` field set + ``from_lens`` + round-trip.

Covers roadmap row R-021 / DM-011. The ResolvedLensEntry dataclass is
the **immutable snapshot** of the LensEntry selected at Wave 0
preflight; it is embedded into :class:`Manifest` (DM-016, T01.27) and
persisted as part of ``manifest.json`` so the INV-001 / INV-016
source-of-truth contract holds (the lens definition used at dispatch
is preserved byte-for-byte regardless of any later edits to the
LensEntry registry).

This suite pins:

1. Every field listed in the roadmap DM-011 row is present on
   ResolvedLensEntry, in declaration order (field-count assertion: 9).
2. The DM-011 field set is narrower than DM-010 -- the four LensEntry
   registry-only fields (``description``, ``output_template_path``,
   ``default_target_line_cap``, ``acceptance_notes``) are intentionally
   not part of the snapshot.
3. ``ResolvedLensEntry.from_lens(entry)`` copies exactly the nine
   DM-011 fields verbatim and does not propagate the excluded fields.
4. The snapshot is independently-owned -- mutating the originating
   LensEntry after the snapshot is taken does not mutate the snapshot
   (INV-001 / INV-016 anchor).
5. JSON round-trip is lossless for the default-stub instance and a
   populated instance.
6. Out-of-enum ``stability`` raises ``ValueError`` (mirrors LensEntry
   guard so a manually-constructed snapshot cannot smuggle an invalid
   value into ``manifest.json``).
7. The snapshot composes cleanly into a manifest-shaped payload
   (round-trips losslessly under the same JSON encoding the manifest
   uses), satisfying T01.24 validation "Snapshot round-trips into
   Manifest field."

STRICT-tier task per §4.11 (INV-001 / INV-016 source-of-truth anchor).
"""

from __future__ import annotations

import dataclasses
import typing

import pytest

from superclaude.cli.swarm.models import (
    LensEntry,
    ResolvedLensEntry,
    Stability,
    from_dict,
    from_json,
    to_dict,
    to_json,
)


# Roadmap DM-011 row (.dev/releases/Current/MultiModelSwarm/roadmap.md L98)
# names exactly these 9 fields, in this order. Drift in either direction
# fails the completeness assertion.
EXPECTED_FIELDS: tuple[str, ...] = (
    "name",
    "system_prompt_fragment",
    "user_template",
    "recipe_name",
    "default_workers",
    "suspect",
    "tier",
    "recommended_next_command_template",
    "stability",
)


# Fields the LensEntry registry record carries (DM-010 + FR-LENSREG.NS)
# that are deliberately excluded from the ResolvedLensEntry snapshot
# (DM-011). Each is either purely registry metadata, already expanded
# into a nested config dataclass (NormalizationSpec.template_path,
# Truncation.line_cap) at preflight, or -- in the case of
# ``normalizer_strategy`` -- a registry-validator-only contract per
# FR-LENSREG.NS / T02.21 that does not appear on the DM-011 manifest
# snapshot row. The choice is reversible by extending DM-011 in a
# follow-up task; for now it keeps the snapshot row stable.
EXCLUDED_LENS_FIELDS: frozenset[str] = frozenset(
    {
        "description",
        "output_template_path",
        "default_target_line_cap",
        "acceptance_notes",
        "normalizer_strategy",
    }
)


# ---------------------------------------------------------------------------
# Field-completeness.
# ---------------------------------------------------------------------------


def test_resolvedlens_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(ResolvedLensEntry)


def test_resolvedlens_declares_every_dm011_field() -> None:
    """No field drift vs roadmap DM-011 row."""
    declared = tuple(f.name for f in dataclasses.fields(ResolvedLensEntry))
    assert declared == EXPECTED_FIELDS, (
        f"ResolvedLensEntry field set diverged from DM-011 row.\n"
        f"  declared: {declared}\n"
        f"  expected: {EXPECTED_FIELDS}"
    )


def test_resolvedlens_field_count_is_9() -> None:
    """Acceptance criterion T01.24: snapshot carries exactly 9 fields."""
    assert len(dataclasses.fields(ResolvedLensEntry)) == 9


def test_resolvedlens_excludes_lens_registry_metadata() -> None:
    """The DM-011 snapshot must NOT carry the four registry-only LensEntry
    fields (``description``, ``output_template_path``,
    ``default_target_line_cap``, ``acceptance_notes``). Those are either
    not runtime-load-bearing or are expanded into nested config dataclasses
    at preflight."""
    declared = {f.name for f in dataclasses.fields(ResolvedLensEntry)}
    leaked = declared & EXCLUDED_LENS_FIELDS
    assert leaked == set(), (
        f"ResolvedLensEntry leaked LensEntry registry-only fields into the "
        f"snapshot: {sorted(leaked)}. DM-011 row excludes these intentionally."
    )


@pytest.mark.parametrize(
    "field_name,expected_type",
    [
        ("name", str),
        ("system_prompt_fragment", str),
        ("user_template", str),
        ("recipe_name", str),
        ("default_workers", int),
        ("suspect", bool),
        ("tier", str),
        ("recommended_next_command_template", str),
    ],
)
def test_scalar_field_types(field_name: str, expected_type: type) -> None:
    """Each scalar field carries the right Python type per DM-011."""
    hints = typing.get_type_hints(ResolvedLensEntry)
    assert hints[field_name] is expected_type, (
        f"ResolvedLensEntry.{field_name} should be typed as "
        f"{expected_type.__name__}, got {hints[field_name]!r}"
    )


# ---------------------------------------------------------------------------
# stability Literal enforcement (mirrors LensEntry guard).
# ---------------------------------------------------------------------------


def test_stability_default_is_stable() -> None:
    """Conservative default mirrors LensEntry."""
    assert ResolvedLensEntry().stability == "stable"


@pytest.mark.parametrize("stability", ["stable", "experimental"])
def test_stability_accepts_each_literal(stability: str) -> None:
    snapshot = ResolvedLensEntry(stability=stability)  # type: ignore[arg-type]
    assert snapshot.stability == stability


def test_stability_rejects_unknown_value() -> None:
    """A manually-constructed snapshot cannot smuggle an out-of-enum value
    into ``manifest.json`` (INV-016 reinforcement)."""
    with pytest.raises(ValueError, match="stability"):
        ResolvedLensEntry(stability="bogus")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Defaults that downstream tasks rely on.
# ---------------------------------------------------------------------------


def test_default_workers_compatible_with_status_floor() -> None:
    """``default_workers`` default mirrors LensEntry (3); composes safely
    with StatusPolicy.floor=2."""
    assert ResolvedLensEntry().default_workers >= 2


def test_suspect_defaults_false() -> None:
    """Conservative default mirrors LensEntry."""
    assert ResolvedLensEntry().suspect is False


# ---------------------------------------------------------------------------
# from_lens classmethod.
# ---------------------------------------------------------------------------


def _populated_lens() -> LensEntry:
    """A populated LensEntry that distinguishes every DM-011 field."""
    return LensEntry(
        name="bare_review",
        description="Unscaffolded native-instinct review",  # excluded
        system_prompt_fragment=(
            "You are reviewing the block between <<<TARGET>>> and "
            "<<<END TARGET>>>."
        ),
        user_template="Review the target block.\n\nTarget:\n{target}\n",
        output_template_path="templates/bare_review.md",  # excluded
        recipe_name="bare_review",
        default_workers=3,
        default_target_line_cap=4000,  # excluded
        suspect=True,
        tier="T2",
        recommended_next_command_template="/sc:foo {suspect_files}",
        acceptance_notes="entry passes validator",  # excluded
        stability="stable",
    )


def test_from_lens_returns_resolved_lens_entry() -> None:
    snapshot = ResolvedLensEntry.from_lens(_populated_lens())
    assert isinstance(snapshot, ResolvedLensEntry)


def test_from_lens_copies_every_dm011_field_verbatim() -> None:
    """Each of the 9 DM-011 fields flows verbatim from the LensEntry."""
    entry = _populated_lens()
    snapshot = ResolvedLensEntry.from_lens(entry)
    assert snapshot.name == entry.name
    assert snapshot.system_prompt_fragment == entry.system_prompt_fragment
    assert snapshot.user_template == entry.user_template
    assert snapshot.recipe_name == entry.recipe_name
    assert snapshot.default_workers == entry.default_workers
    assert snapshot.suspect == entry.suspect
    assert snapshot.tier == entry.tier
    assert (
        snapshot.recommended_next_command_template
        == entry.recommended_next_command_template
    )
    assert snapshot.stability == entry.stability


def test_from_lens_does_not_propagate_excluded_fields() -> None:
    """The snapshot's encoded payload must not contain any excluded
    LensEntry registry-only field, even if the originating LensEntry
    populated those fields."""
    snapshot = ResolvedLensEntry.from_lens(_populated_lens())
    payload = to_dict(snapshot)
    for excluded in EXCLUDED_LENS_FIELDS:
        assert excluded not in payload, (
            f"Snapshot leaked excluded LensEntry field {excluded!r} into "
            f"its encoded payload: {payload}"
        )


def test_from_lens_snapshot_is_independent_of_source() -> None:
    """INV-001 / INV-016 anchor: mutating the originating LensEntry after
    the snapshot is taken does not mutate the snapshot."""
    entry = _populated_lens()
    snapshot = ResolvedLensEntry.from_lens(entry)
    # Mutate the LensEntry post-snapshot.
    entry.system_prompt_fragment = "MUTATED"
    entry.recommended_next_command_template = "MUTATED"
    entry.tier = "MUTATED"
    # Snapshot retains the original values.
    assert snapshot.system_prompt_fragment != "MUTATED"
    assert snapshot.recommended_next_command_template != "MUTATED"
    assert snapshot.tier != "MUTATED"


def test_from_lens_preserves_experimental_stability() -> None:
    entry = LensEntry(name="refactor_find", stability="experimental")
    snapshot = ResolvedLensEntry.from_lens(entry)
    assert snapshot.stability == "experimental"


# ---------------------------------------------------------------------------
# Round-trip contracts.
# ---------------------------------------------------------------------------


def test_default_instance_round_trips_via_dict() -> None:
    instance = ResolvedLensEntry()
    restored = from_dict(ResolvedLensEntry, to_dict(instance))
    assert restored == instance


def test_default_instance_round_trips_via_json() -> None:
    instance = ResolvedLensEntry()
    restored = from_json(ResolvedLensEntry, to_json(instance))
    assert restored == instance


def test_populated_instance_round_trips_via_json() -> None:
    """Populating every field still round-trips losslessly."""
    instance = ResolvedLensEntry(
        name="bare_review",
        system_prompt_fragment="You are reviewing <<<TARGET>>>...<<<END TARGET>>>.",
        user_template="Review the target block.\n\nTarget:\n{target}\n",
        recipe_name="bare_review",
        default_workers=3,
        suspect=True,
        tier="T2",
        recommended_next_command_template="/sc:foo {suspect_files}",
        stability="stable",
    )
    restored = from_json(ResolvedLensEntry, to_json(instance))
    assert restored == instance


def test_round_trip_diff_is_empty() -> None:
    """Acceptance criterion: round-trip diff is empty."""
    instance = ResolvedLensEntry.from_lens(_populated_lens())
    payload_before = to_dict(instance)
    restored = from_dict(ResolvedLensEntry, payload_before)
    payload_after = to_dict(restored)
    assert payload_before == payload_after


def test_verbatim_strings_preserved_through_round_trip() -> None:
    """``system_prompt_fragment`` and ``user_template`` carry whitespace
    verbatim (no normalization at the dataclass layer, mirroring PromptSpec
    / DM-005 and LensEntry / DM-010)."""
    verbatim_fragment = "\n  leading + trailing whitespace  \n\n"
    verbatim_template = "{target}\n\n  --indent--  \n"
    instance = ResolvedLensEntry(
        system_prompt_fragment=verbatim_fragment,
        user_template=verbatim_template,
    )
    restored = from_json(ResolvedLensEntry, to_json(instance))
    assert restored.system_prompt_fragment == verbatim_fragment
    assert restored.user_template == verbatim_template


# ---------------------------------------------------------------------------
# Manifest-shape composition smoke test
# (T01.24 validation: "Snapshot round-trips into Manifest field.").
# ---------------------------------------------------------------------------


def test_snapshot_round_trips_when_embedded_in_manifest_shape() -> None:
    """Manifest (DM-016, T01.27) will carry the snapshot as
    ``resolved_lens_entry``. The full Manifest dataclass lands in T01.24a's
    successor T01.27; this test exercises the embedding shape now by
    encoding/decoding the snapshot inside a Manifest-shaped wrapper dict
    using the same JSON encoding the aggregator's round-trip helpers use.

    This guards against any encoding asymmetry that would only surface
    when the snapshot is read back as part of a larger Manifest payload
    (e.g. byte-identical round-trip required by INV-016).
    """
    snapshot = ResolvedLensEntry.from_lens(_populated_lens())
    manifest_shaped = {
        "contract_version": "1.0",
        "job_id": "00000000-0000-0000-0000-000000000000",
        "resolved_lens_entry": to_dict(snapshot),
        "preflight": {
            "target_checksum": "deadbeef",
            "workers_requested": 3,
            "transport_kind": "stub",
        },
    }
    # Round-trip through JSON, then rebuild the snapshot from the embedded
    # payload, and confirm equality.
    import json

    encoded = json.dumps(manifest_shaped, sort_keys=True)
    decoded = json.loads(encoded)
    rebuilt = from_dict(ResolvedLensEntry, decoded["resolved_lens_entry"])
    assert rebuilt == snapshot


def test_byte_identical_round_trip_under_sorted_json() -> None:
    """INV-016 reinforcement: ``to_json`` uses ``sort_keys=True`` so a
    second encoding of the restored snapshot must be byte-identical to
    the first. Manifest persistence in T01.27 relies on this."""
    instance = ResolvedLensEntry.from_lens(_populated_lens())
    encoded_once = to_json(instance)
    restored = from_json(ResolvedLensEntry, encoded_once)
    encoded_twice = to_json(restored)
    assert encoded_once == encoded_twice
