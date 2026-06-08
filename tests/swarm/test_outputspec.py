"""T01.20 -- DM-007 ``OutputSpec`` field set + round-trip.

Covers roadmap row R-017 / DM-007. OutputSpec configures the M3 output
writer (per-worker file paths, naming template, atomicity, sidecar policy).
This suite pins:

1. Every field listed in the roadmap DM-007 row is present on
   OutputSpec (dir, filename_template, lens_name, atomic_write,
   emit_meta_sidecar) and no others.
2. Defaults match §4.1 spec block + T01.20 acceptance:
   ``filename_template="{lens}-{index:02d}-{model_slug}.md"``,
   ``atomic_write=True`` (IMM-6 alignment), ``emit_meta_sidecar=True``.
3. JSON round-trip is lossless for default and populated instances.

Path-confinement validation (NFR-013) is the M3 output writer's job per
T01.20 acceptance ("Path-confinement validation deferred to M3"); this
suite intentionally does not assert against unsafe `dir` values.

STANDARD-tier task per phase-1-tasklist.md T01.20.
"""

from __future__ import annotations

import dataclasses
import typing

from superclaude.cli.swarm.models import (
    OutputSpec,
    from_dict,
    from_json,
    to_dict,
    to_json,
)


# Roadmap DM-007 row (.dev/releases/Current/MultiModelSwarm/roadmap.md L94)
# names exactly these five top-level fields. No dotted sub-fields (unlike
# DM-002/DM-003/DM-006), so no nested dataclass is required.
EXPECTED_FIELDS: tuple[str, ...] = (
    "dir",
    "filename_template",
    "lens_name",
    "atomic_write",
    "emit_meta_sidecar",
)


# ---------------------------------------------------------------------------
# Field-completeness.
# ---------------------------------------------------------------------------


def test_outputspec_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(OutputSpec)


def test_outputspec_declares_every_dm007_field() -> None:
    """No field drift vs roadmap DM-007 row."""
    declared = tuple(f.name for f in dataclasses.fields(OutputSpec))
    assert declared == EXPECTED_FIELDS, (
        f"OutputSpec field set diverged from DM-007 row.\n"
        f"  declared: {declared}\n"
        f"  expected: {EXPECTED_FIELDS}"
    )


def test_outputspec_field_count_matches_dm007() -> None:
    """Sanity gate so accidental field additions/removals fail loudly."""
    assert len(dataclasses.fields(OutputSpec)) == len(EXPECTED_FIELDS)


# ---------------------------------------------------------------------------
# Field-level type hints.
# ---------------------------------------------------------------------------


def test_dir_is_typed_as_str() -> None:
    hints = typing.get_type_hints(OutputSpec)
    assert hints["dir"] is str


def test_filename_template_is_typed_as_str() -> None:
    hints = typing.get_type_hints(OutputSpec)
    assert hints["filename_template"] is str


def test_lens_name_is_typed_as_str() -> None:
    hints = typing.get_type_hints(OutputSpec)
    assert hints["lens_name"] is str


def test_atomic_write_is_typed_as_bool() -> None:
    hints = typing.get_type_hints(OutputSpec)
    assert hints["atomic_write"] is bool


def test_emit_meta_sidecar_is_typed_as_bool() -> None:
    hints = typing.get_type_hints(OutputSpec)
    assert hints["emit_meta_sidecar"] is bool


# ---------------------------------------------------------------------------
# Default values (T01.20 acceptance + §4.1 spec block).
# ---------------------------------------------------------------------------


def test_default_dir_is_empty_string() -> None:
    """Caller supplies abs path; schema layer (M2) validates shape."""
    assert OutputSpec().dir == ""


def test_default_filename_template_matches_section_4_1_canonical_form() -> None:
    """§4.1 spec block + FR-020 expansion both use this template."""
    assert OutputSpec().filename_template == "{lens}-{index:02d}-{model_slug}.md"


def test_default_lens_name_is_empty_string() -> None:
    """Propagated from job.lens at preflight (FR-020), not at construction."""
    assert OutputSpec().lens_name == ""


def test_default_atomic_write_is_true() -> None:
    """T01.20 acceptance: atomic_write defaults to True (IMM-6 alignment)."""
    assert OutputSpec().atomic_write is True


def test_default_emit_meta_sidecar_is_true() -> None:
    """§4.1 spec block default: emit_meta_sidecar=True."""
    assert OutputSpec().emit_meta_sidecar is True


# ---------------------------------------------------------------------------
# Round-trip contracts.
# ---------------------------------------------------------------------------


def test_default_instance_round_trips_via_dict() -> None:
    instance = OutputSpec()
    restored = from_dict(OutputSpec, to_dict(instance))
    assert restored == instance


def test_default_instance_round_trips_via_json() -> None:
    instance = OutputSpec()
    restored = from_json(OutputSpec, to_json(instance))
    assert restored == instance


def test_populated_instance_round_trips_via_json() -> None:
    instance = OutputSpec(
        dir="/abs/path/to/job-outputs",
        filename_template="{lens}-{index:02d}-{model_slug}.md",
        lens_name="bare-review",
        atomic_write=True,
        emit_meta_sidecar=True,
    )
    restored = from_json(OutputSpec, to_json(instance))
    assert restored == instance


def test_atomic_write_false_round_trips() -> None:
    """Round-trip preserves a non-default atomic_write (schema layer may
    accept or reject False — that's M2's job, not this dataclass)."""
    instance = OutputSpec(atomic_write=False)
    restored = from_json(OutputSpec, to_json(instance))
    assert restored == instance
    assert restored.atomic_write is False


def test_emit_meta_sidecar_false_round_trips() -> None:
    """A caller suppressing the sidecar still round-trips losslessly."""
    instance = OutputSpec(emit_meta_sidecar=False)
    restored = from_json(OutputSpec, to_json(instance))
    assert restored == instance
    assert restored.emit_meta_sidecar is False


def test_round_trip_diff_is_empty() -> None:
    """Acceptance criterion: round-trip lossless on populated instance."""
    instance = OutputSpec(
        dir="/abs/path/to/output-dir",
        filename_template="{lens}-{index:02d}-{model_slug}.md",
        lens_name="roadmap-review",
        atomic_write=True,
        emit_meta_sidecar=False,
    )
    payload_before = to_dict(instance)
    restored = from_dict(OutputSpec, payload_before)
    payload_after = to_dict(restored)
    assert payload_before == payload_after


def test_custom_filename_template_round_trips() -> None:
    """A caller-supplied template (not the §4.1 default) survives round-trip."""
    instance = OutputSpec(
        filename_template="{lens}_{model_slug}_{index}.json",
    )
    restored = from_json(OutputSpec, to_json(instance))
    assert restored == instance
    assert restored.filename_template == "{lens}_{model_slug}_{index}.json"
