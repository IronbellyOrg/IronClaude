"""T01.19 -- DM-006 ``NormalizationSpec`` field set + round-trip.

Covers roadmap row R-016 / DM-006. NormalizationSpec configures the Wave 2
recipe pipeline (recipe name + output template + per-recipe args +
parse-error salvage policy). This suite pins:

1. Every field listed in the roadmap DM-006 row is present on
   NormalizationSpec (recipe, template_path, schema_version, recipe_args,
   on_parse_error).
2. The dotted ``on_parse_error.salvage`` / ``on_parse_error.retain_raw``
   sub-fields collapse into a nested :class:`OnParseError` dataclass.
3. Defaults match §4.1 spec block: ``schema_version="1.0"``,
   ``on_parse_error.salvage=True``, ``on_parse_error.retain_raw=True``
   (T01.19 acceptance).
4. JSON round-trip is lossless for default and populated instances.

STANDARD-tier task per phase-1-tasklist.md T01.19.
"""

from __future__ import annotations

import dataclasses
import typing

from superclaude.cli.swarm.models import (
    NormalizationSpec,
    OnParseError,
    from_dict,
    from_json,
    to_dict,
    to_json,
)


# Roadmap DM-006 row (.dev/releases/Current/MultiModelSwarm/roadmap.md L93)
# names exactly these top-level fields; on_parse_error is a nested dataclass
# (same pattern as RetryPolicy on WorkerSpec).
EXPECTED_FIELDS: tuple[str, ...] = (
    "recipe",
    "template_path",
    "schema_version",
    "recipe_args",
    "on_parse_error",
)

EXPECTED_ON_PARSE_ERROR_FIELDS: tuple[str, ...] = (
    "salvage",
    "retain_raw",
)


# ---------------------------------------------------------------------------
# Field-completeness.
# ---------------------------------------------------------------------------


def test_normalizationspec_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(NormalizationSpec)


def test_on_parse_error_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(OnParseError)


def test_normalizationspec_declares_every_dm006_field() -> None:
    """No field drift vs roadmap DM-006 row."""
    declared = tuple(f.name for f in dataclasses.fields(NormalizationSpec))
    assert declared == EXPECTED_FIELDS, (
        f"NormalizationSpec field set diverged from DM-006 row.\n"
        f"  declared: {declared}\n"
        f"  expected: {EXPECTED_FIELDS}"
    )


def test_normalizationspec_field_count_matches_dm006() -> None:
    """Sanity gate so accidental field additions/removals fail loudly."""
    assert len(dataclasses.fields(NormalizationSpec)) == len(EXPECTED_FIELDS)


def test_on_parse_error_declares_dm006_sub_fields() -> None:
    """The dotted on_parse_error.* sub-fields collapse into OnParseError."""
    declared = tuple(f.name for f in dataclasses.fields(OnParseError))
    assert declared == EXPECTED_ON_PARSE_ERROR_FIELDS


# ---------------------------------------------------------------------------
# Field-level type hints.
# ---------------------------------------------------------------------------


def test_recipe_is_typed_as_str() -> None:
    hints = typing.get_type_hints(NormalizationSpec)
    assert hints["recipe"] is str


def test_template_path_is_typed_as_str() -> None:
    hints = typing.get_type_hints(NormalizationSpec)
    assert hints["template_path"] is str


def test_schema_version_is_typed_as_str() -> None:
    hints = typing.get_type_hints(NormalizationSpec)
    assert hints["schema_version"] is str


def test_recipe_args_is_typed_as_dict() -> None:
    hints = typing.get_type_hints(NormalizationSpec)
    assert typing.get_origin(hints["recipe_args"]) is dict


def test_on_parse_error_is_typed_as_on_parse_error_dataclass() -> None:
    hints = typing.get_type_hints(NormalizationSpec)
    assert hints["on_parse_error"] is OnParseError


def test_on_parse_error_fields_typed_as_bool() -> None:
    hints = typing.get_type_hints(OnParseError)
    assert hints["salvage"] is bool
    assert hints["retain_raw"] is bool


# ---------------------------------------------------------------------------
# Default values (T01.19 acceptance + §4.1 spec block).
# ---------------------------------------------------------------------------


def test_default_recipe_is_empty_string() -> None:
    """Caller / lens supplies; FR-020 lens-driven defaults expand at preflight."""
    assert NormalizationSpec().recipe == ""


def test_default_template_path_is_empty_string() -> None:
    """Caller / lens supplies; preflight expands from lens.output_template_path."""
    assert NormalizationSpec().template_path == ""


def test_default_schema_version_is_1_0() -> None:
    """§4.1 spec block default: schema_version="1.0"."""
    assert NormalizationSpec().schema_version == "1.0"


def test_default_recipe_args_is_empty_dict() -> None:
    assert NormalizationSpec().recipe_args == {}


def test_recipe_args_defaults_are_per_instance() -> None:
    """default_factory ensures no shared mutable default across instances."""
    a = NormalizationSpec()
    b = NormalizationSpec()
    a.recipe_args["k"] = "v"
    assert b.recipe_args == {}


def test_default_on_parse_error_salvage_is_true() -> None:
    """T01.19 acceptance + §7.4 default: salvage=True."""
    assert NormalizationSpec().on_parse_error.salvage is True


def test_default_on_parse_error_retain_raw_is_true() -> None:
    """T01.19 acceptance + §7.4 default: retain_raw=True."""
    assert NormalizationSpec().on_parse_error.retain_raw is True


def test_default_on_parse_error_instance_independence() -> None:
    """default_factory ensures distinct OnParseError instances per NormalizationSpec."""
    a = NormalizationSpec()
    b = NormalizationSpec()
    assert a.on_parse_error is not b.on_parse_error


# ---------------------------------------------------------------------------
# Round-trip contracts.
# ---------------------------------------------------------------------------


def test_default_instance_round_trips_via_dict() -> None:
    instance = NormalizationSpec()
    restored = from_dict(NormalizationSpec, to_dict(instance))
    assert restored == instance


def test_default_instance_round_trips_via_json() -> None:
    instance = NormalizationSpec()
    restored = from_json(NormalizationSpec, to_json(instance))
    assert restored == instance


def test_populated_instance_round_trips_via_json() -> None:
    instance = NormalizationSpec(
        recipe="findings_table_v1",
        template_path="/abs/path/to/template.j2",
        schema_version="1.0",
        recipe_args={"max_rows": 100, "include_metadata": True},
        on_parse_error=OnParseError(salvage=False, retain_raw=True),
    )
    restored = from_json(NormalizationSpec, to_json(instance))
    assert restored == instance


def test_custom_py_recipe_round_trips() -> None:
    """The custom-py:module:func dynamic loader form (COMP-021) round-trips."""
    instance = NormalizationSpec(
        recipe="custom-py:my.module:my_normalizer",
        template_path="/abs/output.j2",
    )
    restored = from_json(NormalizationSpec, to_json(instance))
    assert restored == instance
    assert restored.recipe == "custom-py:my.module:my_normalizer"


def test_round_trip_diff_is_empty() -> None:
    """Acceptance criterion: round-trip lossless."""
    instance = NormalizationSpec(
        recipe="bare-review-v1",
        template_path="/abs/bare-review.j2",
        schema_version="1.0",
        recipe_args={"strict": True},
        on_parse_error=OnParseError(salvage=True, retain_raw=False),
    )
    payload_before = to_dict(instance)
    restored = from_dict(NormalizationSpec, payload_before)
    payload_after = to_dict(restored)
    assert payload_before == payload_after


def test_on_parse_error_nested_round_trips_standalone() -> None:
    """OnParseError round-trips on its own (exported via __all__)."""
    instance = OnParseError(salvage=False, retain_raw=False)
    restored = from_json(OnParseError, to_json(instance))
    assert restored == instance
