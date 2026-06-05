"""T01.14 -- DM-002 ``WorkerSpec`` field set + round-trip + validation.

Covers roadmap row R-012 / DM-002. WorkerSpec configures the per-worker
dispatch policy (count / models / timeout / temperature / retry rules).
This suite pins:

1. Every field listed in the roadmap DM-002 row is present on WorkerSpec
   (count, models, timeout_sec, temperature, retry sub-record).
2. Retry policy is a nested :class:`RetryPolicy` with the four sub-fields
   from the roadmap row (on_5xx, on_5xx_backoff_sec, on_4xx, on_timeout).
3. Defaults match NFR-010 (timeout_sec=180) and FR-017 / NFR-011 retry
   policy (5xx retry-once with backoff; 4xx / timeout / network no retry).
4. JSON round-trip is lossless for default and populated instances.
5. ``__post_init__`` validation rejects negative ``timeout_sec``.

STANDARD-tier task per phase-1-tasklist.md T01.14.
"""

from __future__ import annotations

import dataclasses
import typing

import pytest

from superclaude.cli.swarm.models import (
    RetryPolicy,
    WorkerSpec,
    from_dict,
    from_json,
    to_dict,
    to_json,
)


# Roadmap DM-002 row (.dev/releases/Current/MultiModelSwarm/roadmap.md L89)
# names exactly these fields. ``retry`` collapses the four dotted
# sub-fields (retry.on_5xx, retry.on_5xx_backoff_sec, retry.on_4xx,
# retry.on_timeout) into a nested RetryPolicy record.
EXPECTED_FIELDS: tuple[str, ...] = (
    "count",
    "models",
    "timeout_sec",
    "temperature",
    "retry",
)

EXPECTED_RETRY_FIELDS: tuple[str, ...] = (
    "on_5xx",
    "on_5xx_backoff_sec",
    "on_4xx",
    "on_timeout",
)


# ---------------------------------------------------------------------------
# Field-completeness.
# ---------------------------------------------------------------------------


def test_workerspec_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(WorkerSpec)


def test_workerspec_declares_every_dm002_field() -> None:
    """No field drift vs roadmap DM-002 row."""
    declared = tuple(f.name for f in dataclasses.fields(WorkerSpec))
    assert declared == EXPECTED_FIELDS, (
        f"WorkerSpec field set diverged from DM-002 row.\n"
        f"  declared: {declared}\n"
        f"  expected: {EXPECTED_FIELDS}"
    )


def test_workerspec_field_count_matches_dm002() -> None:
    """Sanity gate so accidental field additions/removals fail loudly."""
    assert len(dataclasses.fields(WorkerSpec)) == len(EXPECTED_FIELDS)


def test_retry_is_typed_as_retry_policy() -> None:
    hints = typing.get_type_hints(WorkerSpec)
    assert hints["retry"] is RetryPolicy


def test_retry_policy_declares_all_dotted_subfields() -> None:
    """RetryPolicy carries the four ``retry.*`` sub-fields from DM-002."""
    declared = tuple(f.name for f in dataclasses.fields(RetryPolicy))
    assert declared == EXPECTED_RETRY_FIELDS


def test_field_types_match_roadmap_row() -> None:
    """count:int; models:list[str]; timeout_sec:int; temperature:float."""
    hints = typing.get_type_hints(WorkerSpec)
    assert hints["count"] is int
    assert hints["timeout_sec"] is int
    assert hints["temperature"] is float
    # models: list[str]
    assert typing.get_origin(hints["models"]) is list
    assert typing.get_args(hints["models"]) == (str,)


def test_retry_policy_field_types() -> None:
    """retry.on_5xx:bool; retry.on_5xx_backoff_sec:int; retry.on_4xx:bool;
    retry.on_timeout:bool."""
    hints = typing.get_type_hints(RetryPolicy)
    assert hints["on_5xx"] is bool
    assert hints["on_5xx_backoff_sec"] is int
    assert hints["on_4xx"] is bool
    assert hints["on_timeout"] is bool


# ---------------------------------------------------------------------------
# Default values (NFR-010 + FR-017 / NFR-011).
# ---------------------------------------------------------------------------


def test_default_timeout_sec_is_180_nfr010() -> None:
    """NFR-010: 180s default per-worker hard timeout."""
    assert WorkerSpec().timeout_sec == 180


def test_default_temperature() -> None:
    assert WorkerSpec().temperature == 0.2


def test_default_models_is_empty_list() -> None:
    """Lens expansion (FR-020) populates models at preflight."""
    assert WorkerSpec().models == []


def test_default_models_is_a_fresh_list_per_instance() -> None:
    """Guards against the classic mutable-default-argument trap."""
    a = WorkerSpec()
    b = WorkerSpec()
    a.models.append("model-x")
    assert b.models == []


def test_default_retry_policy_matches_fr017() -> None:
    """FR-017 / NFR-011: 5xx retry-once with backoff; 4xx / timeout no retry."""
    retry = WorkerSpec().retry
    assert retry.on_5xx is True
    assert retry.on_5xx_backoff_sec == 2
    assert retry.on_4xx is False
    assert retry.on_timeout is False


def test_default_retry_is_a_fresh_instance_per_workerspec() -> None:
    """Independent retry per WorkerSpec instance (default_factory contract)."""
    a = WorkerSpec()
    b = WorkerSpec()
    a.retry.on_4xx = True
    assert b.retry.on_4xx is False


# ---------------------------------------------------------------------------
# Validation -- negative timeouts rejected.
# ---------------------------------------------------------------------------


def test_negative_timeout_raises_value_error() -> None:
    with pytest.raises(ValueError, match="timeout_sec"):
        WorkerSpec(timeout_sec=-1)


def test_zero_timeout_is_allowed() -> None:
    """Zero is the boundary case (non-negative). Schema layer (M2) may
    enforce a stricter floor; the dataclass only rejects negatives."""
    spec = WorkerSpec(timeout_sec=0)
    assert spec.timeout_sec == 0


# ---------------------------------------------------------------------------
# Round-trip contracts.
# ---------------------------------------------------------------------------


def test_default_instance_round_trips_via_dict() -> None:
    instance = WorkerSpec()
    restored = from_dict(WorkerSpec, to_dict(instance))
    assert restored == instance


def test_default_instance_round_trips_via_json() -> None:
    instance = WorkerSpec()
    restored = from_json(WorkerSpec, to_json(instance))
    assert restored == instance


def test_populated_instance_round_trips_via_json() -> None:
    instance = WorkerSpec(
        count=8,
        models=["gpt-4o", "claude-sonnet-4-6", "deepseek-v3"],
        timeout_sec=240,
        temperature=0.7,
        retry=RetryPolicy(
            on_5xx=True,
            on_5xx_backoff_sec=5,
            on_4xx=True,
            on_timeout=True,
        ),
    )
    restored = from_json(WorkerSpec, to_json(instance))
    assert restored == instance


def test_round_trip_diff_is_empty() -> None:
    """Acceptance criterion: round-trip diff empty."""
    instance = WorkerSpec(count=2, models=["m1"], timeout_sec=60)
    payload_before = to_dict(instance)
    restored = from_dict(WorkerSpec, payload_before)
    payload_after = to_dict(restored)
    assert payload_before == payload_after


def test_nested_retry_is_dataclass_after_round_trip() -> None:
    """``from_dict`` recurses so ``restored.retry`` is a RetryPolicy,
    not a raw dict (would break downstream consumers in M3)."""
    restored = from_dict(WorkerSpec, to_dict(WorkerSpec()))
    assert isinstance(restored.retry, RetryPolicy)


def test_retry_policy_round_trips_standalone() -> None:
    """RetryPolicy is itself a round-trippable dataclass."""
    retry = RetryPolicy(on_5xx=False, on_5xx_backoff_sec=10, on_4xx=True, on_timeout=True)
    restored = from_json(RetryPolicy, to_json(retry))
    assert restored == retry
