"""T01.23 + T02.21 -- DM-010 ``LensEntry`` field set + round-trip contract.

Covers roadmap row R-020 / DM-010 and the FR-LENSREG.NS / T02.21
anti-instinct remediation row 17a. The LensEntry dataclass is the
registry record consumed by Wave 0 preflight (FR-020 lens-driven
defaults expansion) and snapshot into :class:`Manifest` via
:class:`ResolvedLensEntry` (INV-001 / INV-016). This suite pins:

1. Every field listed in the roadmap DM-010 row is present on
   LensEntry, plus the FR-LENSREG.NS / T02.21 ``normalizer_strategy``
   extension (field-count assertion: 14 -- DM-010's 13 fields plus the
   T02.21 sixth contract field).
2. The ``stability`` Literal admits exactly the two values listed in
   the roadmap row (``stable`` / ``experimental``).
3. JSON round-trip is lossless for the default-stub instance and a
   populated instance.
4. ``LENSES`` dict can hold 8 entries (smoke test per T01.23 AC).
5. Construction with an out-of-enum ``stability`` raises ``ValueError``.

STRICT-tier task per §4.11 (schema-bearing dataclass; feeds Wave 0
preflight and manifest snapshot).
"""

from __future__ import annotations

import dataclasses
import typing

import pytest

from superclaude.cli.swarm.models import (
    LensEntry,
    Stability,
    from_dict,
    from_json,
    to_dict,
    to_json,
)

# Roadmap DM-010 row (.dev/releases/Current/MultiModelSwarm/roadmap.md L97)
# names exactly these 13 fields, in this order. Anti-instinct remediation
# row 17a (roadmap line 151, FR-LENSREG.NS / T02.21) appends a 14th field
# -- ``normalizer_strategy`` -- declared after ``recipe_name`` because
# both feed the recipe-resolution surfaces. Drift in either direction
# fails the completeness assertion.
EXPECTED_FIELDS: tuple[str, ...] = (
    "name",
    "description",
    "system_prompt_fragment",
    "user_template",
    "output_template_path",
    "recipe_name",
    "normalizer_strategy",
    "default_workers",
    "default_target_line_cap",
    "suspect",
    "tier",
    "recommended_next_command_template",
    "acceptance_notes",
    "stability",
)


# ---------------------------------------------------------------------------
# Field-completeness.
# ---------------------------------------------------------------------------


def test_lensentry_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(LensEntry)


def test_lensentry_declares_every_dm010_field() -> None:
    """No field drift vs roadmap DM-010 row."""
    declared = tuple(f.name for f in dataclasses.fields(LensEntry))
    assert declared == EXPECTED_FIELDS, (
        f"LensEntry field set diverged from DM-010 row.\n"
        f"  declared: {declared}\n"
        f"  expected: {EXPECTED_FIELDS}"
    )


def test_lensentry_field_count_is_14() -> None:
    """T01.23 AC + T02.21 extension: field count is 14.

    DM-010 row declares 13 fields. FR-LENSREG.NS / T02.21 appends one
    more (``normalizer_strategy``) per anti-instinct remediation row
    17a. Total expected: 14.
    """
    assert len(dataclasses.fields(LensEntry)) == 14


@pytest.mark.parametrize(
    "field_name,expected_type",
    [
        ("name", str),
        ("description", str),
        ("system_prompt_fragment", str),
        ("user_template", str),
        ("output_template_path", str),
        ("recipe_name", str),
        ("normalizer_strategy", str),
        ("default_workers", int),
        ("default_target_line_cap", int),
        ("suspect", bool),
        ("tier", str),
        ("recommended_next_command_template", str),
        ("acceptance_notes", str),
    ],
)
def test_scalar_field_types(field_name: str, expected_type: type) -> None:
    """Each scalar field carries the right Python type per DM-010."""
    hints = typing.get_type_hints(LensEntry)
    assert hints[field_name] is expected_type, (
        f"LensEntry.{field_name} should be typed as {expected_type.__name__}, "
        f"got {hints[field_name]!r}"
    )


# ---------------------------------------------------------------------------
# stability Literal enforcement.
# ---------------------------------------------------------------------------


def test_stability_literal_values() -> None:
    """Roadmap row lists exactly ``stable`` / ``experimental``."""
    args = typing.get_args(Stability)
    assert set(args) == {"stable", "experimental"}, (
        f"Stability admits {set(args)}; DM-010 row requires "
        "{'stable','experimental'}."
    )


def test_stability_default_is_stable() -> None:
    """Conservative default; experimental lenses opt in explicitly."""
    assert LensEntry().stability == "stable"


@pytest.mark.parametrize("stability", ["stable", "experimental"])
def test_stability_accepts_each_literal(stability: str) -> None:
    entry = LensEntry(stability=stability)  # type: ignore[arg-type]
    assert entry.stability == stability


def test_stability_rejects_unknown_value() -> None:
    """Dataclass-level guard rejects out-of-enum stability."""
    with pytest.raises(ValueError, match="stability"):
        LensEntry(stability="bogus")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Defaults that downstream tasks rely on.
# ---------------------------------------------------------------------------


def test_default_workers_compatible_with_status_floor() -> None:
    """``default_workers`` must be >= StatusPolicy.floor (2) by construction.

    Most built-in lenses use 3 workers (bare_review, refactor_find,
    spec_completeness, feasibility_probe, doc_completeness); some
    override to 4 (edge_case_hunt, troubleshoot_hypothesis). The
    dataclass default sits at 3 so the no-arg round-trip already
    composes safely with StatusPolicy floor=2.
    """
    assert LensEntry().default_workers >= 2


def test_default_target_line_cap_matches_truncation_default() -> None:
    """Mirrors :class:`Truncation` default per FR-SPEC-005."""
    assert LensEntry().default_target_line_cap == 4000


def test_suspect_defaults_false() -> None:
    """Conservative default; suspect lenses opt in explicitly."""
    assert LensEntry().suspect is False


# ---------------------------------------------------------------------------
# Round-trip contracts.
# ---------------------------------------------------------------------------


def test_default_instance_round_trips_via_dict() -> None:
    instance = LensEntry()
    restored = from_dict(LensEntry, to_dict(instance))
    assert restored == instance


def test_default_instance_round_trips_via_json() -> None:
    instance = LensEntry()
    restored = from_json(LensEntry, to_json(instance))
    assert restored == instance


def test_populated_instance_round_trips_via_json() -> None:
    """Populating every field still round-trips losslessly."""
    instance = LensEntry(
        name="bare-review",
        description="Unscaffolded native-instinct review",
        system_prompt_fragment="You are reviewing the block between <<<TARGET>>> and <<<END TARGET>>>.",
        user_template="Review the target block.\n\nTarget:\n{target}\n",
        output_template_path="templates/bare_review.md",
        recipe_name="bare_review",
        default_workers=3,
        default_target_line_cap=4000,
        suspect=True,
        tier="T2",
        recommended_next_command_template="/sc:foo {suspect_files}",
        acceptance_notes="entry passes validator; suspect_files in next-cmd template",
        stability="stable",
    )
    restored = from_json(LensEntry, to_json(instance))
    assert restored == instance


def test_round_trip_diff_is_empty() -> None:
    """Acceptance criterion: round-trip diff is empty."""
    instance = LensEntry(
        name="refactor_find",
        tier="T2-code",
        stability="experimental",
    )
    payload_before = to_dict(instance)
    restored = from_dict(LensEntry, payload_before)
    payload_after = to_dict(restored)
    assert payload_before == payload_after


def test_verbatim_strings_preserved_through_round_trip() -> None:
    """``system_prompt_fragment`` and ``user_template`` carry whitespace verbatim
    (no normalization at the dataclass layer, mirroring PromptSpec / DM-005)."""
    verbatim_fragment = "\n  leading + trailing whitespace  \n\n"
    verbatim_template = "{target}\n\n  --indent--  \n"
    instance = LensEntry(
        system_prompt_fragment=verbatim_fragment,
        user_template=verbatim_template,
    )
    restored = from_json(LensEntry, to_json(instance))
    assert restored.system_prompt_fragment == verbatim_fragment
    assert restored.user_template == verbatim_template


# ---------------------------------------------------------------------------
# Registry-shape smoke test (T01.23 AC: "LENSES dict can hold 8 entries").
# ---------------------------------------------------------------------------


def test_lenses_dict_holds_eight_entries() -> None:
    """The eight built-in lenses (COMP-024..030 + bare_review) compose
    into a single dict keyed by ``name`` without collision. The actual
    lens instances land with COMP-022..030 in M4; this test exercises
    the dataclass shape only."""
    names = (
        "bare_review",
        "refactor_find",
        "edge_case_hunt",
        "spec_completeness",
        "feasibility_probe",
        "troubleshoot_hypothesis",
        "doc_completeness",
        "code_quality",
    )
    lenses: dict[str, LensEntry] = {
        n: LensEntry(name=n, tier="T2", stability="stable") for n in names
    }
    assert len(lenses) == 8
    assert all(isinstance(v, LensEntry) for v in lenses.values())
    # Round-trip the whole registry as a sanity check.
    restored = {k: from_dict(LensEntry, to_dict(v)) for k, v in lenses.items()}
    assert restored == lenses
