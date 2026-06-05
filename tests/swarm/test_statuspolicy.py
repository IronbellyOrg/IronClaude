"""T01.21 -- DM-008 ``StatusPolicy`` field set + round-trip + IMM-5 defaults.

Covers roadmap row R-018 / DM-008. StatusPolicy parameterizes the Wave 3
reduce status-determination logic (COMP-009, M5). The IMM-5 status matrix
(``M==N`` -> success / ``2<=M<N`` -> partial / ``M<2`` -> failed /
``M==N==2 && success_first`` -> success tie-break) reads these three fields
at job time. This suite pins:

1. Every field listed in the roadmap DM-008 row is present on
   StatusPolicy (floor, success_first, partial_threshold) and no others.
2. Defaults match IMM-5 + T01.21 acceptance: ``floor=2``,
   ``success_first=True``, ``partial_threshold=2``.
3. JSON round-trip is lossless for default and populated instances.

Cross-field consistency validation (e.g. ``partial_threshold >= floor``)
is the COMP-005 schema layer's job per the dataclass docstring; this suite
intentionally does not assert against inconsistent combinations.

STANDARD-tier task per phase-1-tasklist.md T01.21.
"""

from __future__ import annotations

import dataclasses
import typing

from superclaude.cli.swarm.models import (
    StatusPolicy,
    from_dict,
    from_json,
    to_dict,
    to_json,
)


# Roadmap DM-008 row (.dev/releases/Current/MultiModelSwarm/roadmap.md L95)
# names exactly these three top-level fields. No dotted sub-fields, so no
# nested dataclass is required (unlike DM-002/DM-003/DM-006).
EXPECTED_FIELDS: tuple[str, ...] = (
    "floor",
    "success_first",
    "partial_threshold",
)


# ---------------------------------------------------------------------------
# Field-completeness.
# ---------------------------------------------------------------------------


def test_statuspolicy_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(StatusPolicy)


def test_statuspolicy_declares_every_dm008_field() -> None:
    """No field drift vs roadmap DM-008 row."""
    declared = tuple(f.name for f in dataclasses.fields(StatusPolicy))
    assert declared == EXPECTED_FIELDS, (
        f"StatusPolicy field set diverged from DM-008 row.\n"
        f"  declared: {declared}\n"
        f"  expected: {EXPECTED_FIELDS}"
    )


def test_statuspolicy_field_count_matches_dm008() -> None:
    """Sanity gate so accidental field additions/removals fail loudly."""
    assert len(dataclasses.fields(StatusPolicy)) == len(EXPECTED_FIELDS)


# ---------------------------------------------------------------------------
# Field-level type hints.
# ---------------------------------------------------------------------------


def test_floor_is_typed_as_int() -> None:
    hints = typing.get_type_hints(StatusPolicy)
    assert hints["floor"] is int


def test_success_first_is_typed_as_bool() -> None:
    hints = typing.get_type_hints(StatusPolicy)
    assert hints["success_first"] is bool


def test_partial_threshold_is_typed_as_int() -> None:
    hints = typing.get_type_hints(StatusPolicy)
    assert hints["partial_threshold"] is int


# ---------------------------------------------------------------------------
# Default values (T01.21 acceptance + IMM-5).
# ---------------------------------------------------------------------------


def test_default_floor_is_2() -> None:
    """IMM-5: ``M<2`` -> failed; floor=2 is the failed/partial boundary."""
    assert StatusPolicy().floor == 2


def test_default_success_first_is_true() -> None:
    """IMM-5 tie-break: ``M==N==2 && success_first`` -> success."""
    assert StatusPolicy().success_first is True


def test_default_partial_threshold_is_2() -> None:
    """IMM-5: ``2<=M<N`` -> partial; lower bound mirrors floor by default."""
    assert StatusPolicy().partial_threshold == 2


def test_imm5_defaults_match_roadmap_row() -> None:
    """T01.21 acceptance: ``floor=2, success_first=True, partial_threshold=2``."""
    policy = StatusPolicy()
    assert (policy.floor, policy.success_first, policy.partial_threshold) == (
        2,
        True,
        2,
    )


# ---------------------------------------------------------------------------
# Round-trip contracts.
# ---------------------------------------------------------------------------


def test_default_instance_round_trips_via_dict() -> None:
    instance = StatusPolicy()
    restored = from_dict(StatusPolicy, to_dict(instance))
    assert restored == instance


def test_default_instance_round_trips_via_json() -> None:
    instance = StatusPolicy()
    restored = from_json(StatusPolicy, to_json(instance))
    assert restored == instance


def test_populated_instance_round_trips_via_json() -> None:
    instance = StatusPolicy(
        floor=3,
        success_first=False,
        partial_threshold=4,
    )
    restored = from_json(StatusPolicy, to_json(instance))
    assert restored == instance


def test_success_first_false_round_trips() -> None:
    """Round-trip preserves a non-default success_first (callers may opt out
    of the IMM-5 M==N==2 tie-break)."""
    instance = StatusPolicy(success_first=False)
    restored = from_json(StatusPolicy, to_json(instance))
    assert restored == instance
    assert restored.success_first is False


def test_round_trip_diff_is_empty() -> None:
    """Acceptance criterion: round-trip lossless on populated instance."""
    instance = StatusPolicy(
        floor=1,
        success_first=False,
        partial_threshold=3,
    )
    payload_before = to_dict(instance)
    restored = from_dict(StatusPolicy, payload_before)
    payload_after = to_dict(restored)
    assert payload_before == payload_after


def test_dict_payload_shape_is_flat() -> None:
    """DM-008 has no dotted sub-fields; to_dict yields a 3-key flat dict."""
    payload = to_dict(StatusPolicy())
    assert set(payload.keys()) == {"floor", "success_first", "partial_threshold"}
