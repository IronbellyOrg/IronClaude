"""T01.22 -- DM-009 ``RuntimeSpec`` field set + round-trip + mode validation.

Covers roadmap row R-019 / DM-009. RuntimeSpec parameterizes the executor's
runtime knobs: inline vs detached mode (AC-008 / FR-014), log_level for the
durable monitoring layer (M7), and on_completion policy for the done sentinel
(DM-017) + stdout contract emission (FR-030). This suite pins:

1. Every field listed in the roadmap DM-009 row is present on
   RuntimeSpec (mode, log_level, on_completion) and no others.
2. The dotted ``on_completion.write_done_sentinel`` /
   ``on_completion.print_contract_to_stdout`` sub-fields collapse into a
   nested :class:`OnCompletion` dataclass.
3. ``mode`` is typed as :data:`RuntimeMode` =
   ``Literal['inline','detached']`` (T01.22 acceptance).
4. Defaults match FR-SPEC-007 + §4.1 spec block: ``mode='inline'``,
   ``log_level='info'``, ``on_completion.write_done_sentinel=True``,
   ``on_completion.print_contract_to_stdout=True``.
5. JSON round-trip is lossless for default and populated instances.
6. ``__post_init__`` validation rejects invalid ``mode`` values
   (T01.22 acceptance: "Mode-validation test").

STANDARD-tier task per phase-1-tasklist.md T01.22.
"""

from __future__ import annotations

import dataclasses
import typing

import pytest

from superclaude.cli.swarm.models import (
    OnCompletion,
    RuntimeMode,
    RuntimeSpec,
    from_dict,
    from_json,
    to_dict,
    to_json,
)


# Roadmap DM-009 row (.dev/releases/Current/MultiModelSwarm/roadmap.md L96)
# names exactly these top-level fields; on_completion is a nested dataclass
# (same pattern as RetryPolicy on WorkerSpec, OnParseError on NormalizationSpec).
EXPECTED_FIELDS: tuple[str, ...] = (
    "mode",
    "log_level",
    "on_completion",
)

EXPECTED_ON_COMPLETION_FIELDS: tuple[str, ...] = (
    "write_done_sentinel",
    "print_contract_to_stdout",
)


# ---------------------------------------------------------------------------
# Field-completeness.
# ---------------------------------------------------------------------------


def test_runtimespec_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(RuntimeSpec)


def test_on_completion_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(OnCompletion)


def test_runtimespec_declares_every_dm009_field() -> None:
    """No field drift vs roadmap DM-009 row."""
    declared = tuple(f.name for f in dataclasses.fields(RuntimeSpec))
    assert declared == EXPECTED_FIELDS, (
        f"RuntimeSpec field set diverged from DM-009 row.\n"
        f"  declared: {declared}\n"
        f"  expected: {EXPECTED_FIELDS}"
    )


def test_runtimespec_field_count_matches_dm009() -> None:
    """Sanity gate so accidental field additions/removals fail loudly."""
    assert len(dataclasses.fields(RuntimeSpec)) == len(EXPECTED_FIELDS)


def test_on_completion_declares_dm009_sub_fields() -> None:
    """The dotted on_completion.* sub-fields collapse into OnCompletion."""
    declared = tuple(f.name for f in dataclasses.fields(OnCompletion))
    assert declared == EXPECTED_ON_COMPLETION_FIELDS


# ---------------------------------------------------------------------------
# Field-level type hints.
# ---------------------------------------------------------------------------


def test_mode_is_typed_as_runtime_mode_literal() -> None:
    """T01.22 acceptance: ``mode`` is Literal['inline','detached']."""
    hints = typing.get_type_hints(RuntimeSpec)
    assert hints["mode"] is RuntimeMode


def test_runtime_mode_literal_values() -> None:
    """The Literal enumerates exactly the two allowed runtime modes."""
    assert typing.get_args(RuntimeMode) == ("inline", "detached")


def test_log_level_is_typed_as_str() -> None:
    hints = typing.get_type_hints(RuntimeSpec)
    assert hints["log_level"] is str


def test_on_completion_is_typed_as_on_completion_dataclass() -> None:
    hints = typing.get_type_hints(RuntimeSpec)
    assert hints["on_completion"] is OnCompletion


def test_on_completion_fields_typed_as_bool() -> None:
    hints = typing.get_type_hints(OnCompletion)
    assert hints["write_done_sentinel"] is bool
    assert hints["print_contract_to_stdout"] is bool


# ---------------------------------------------------------------------------
# Default values (T01.22 acceptance + FR-SPEC-007 / §4.1 spec block).
# ---------------------------------------------------------------------------


def test_default_mode_is_inline() -> None:
    """T01.22 acceptance: defaults ``mode='inline'`` (M7 detached is opt-in)."""
    assert RuntimeSpec().mode == "inline"


def test_default_log_level_is_info() -> None:
    """§4.1 spec block default: ``log_level: info`` (L333)."""
    assert RuntimeSpec().log_level == "info"


def test_default_on_completion_write_done_sentinel_is_true() -> None:
    """FR-SPEC-007 default: write_done_sentinel=True."""
    assert RuntimeSpec().on_completion.write_done_sentinel is True


def test_default_on_completion_print_contract_to_stdout_is_true() -> None:
    """FR-SPEC-007 default: print_contract_to_stdout=True (FR-030 stdout contract)."""
    assert RuntimeSpec().on_completion.print_contract_to_stdout is True


def test_default_on_completion_instance_independence() -> None:
    """default_factory ensures distinct OnCompletion instances per RuntimeSpec."""
    a = RuntimeSpec()
    b = RuntimeSpec()
    assert a.on_completion is not b.on_completion


# ---------------------------------------------------------------------------
# Validation (T01.22 acceptance: mode-validation test).
# ---------------------------------------------------------------------------


def test_invalid_mode_raises_value_error() -> None:
    """T01.22 acceptance: construction with bogus ``mode`` raises."""
    with pytest.raises(ValueError, match="mode"):
        RuntimeSpec(mode="bogus")  # type: ignore[arg-type]


def test_mode_inline_is_accepted() -> None:
    """Sanity: the default inline mode constructs without error."""
    spec = RuntimeSpec(mode="inline")
    assert spec.mode == "inline"


def test_mode_detached_is_accepted() -> None:
    """Sanity: the M7 detached mode constructs without error."""
    spec = RuntimeSpec(mode="detached")
    assert spec.mode == "detached"


# ---------------------------------------------------------------------------
# Round-trip contracts.
# ---------------------------------------------------------------------------


def test_default_instance_round_trips_via_dict() -> None:
    instance = RuntimeSpec()
    restored = from_dict(RuntimeSpec, to_dict(instance))
    assert restored == instance


def test_default_instance_round_trips_via_json() -> None:
    instance = RuntimeSpec()
    restored = from_json(RuntimeSpec, to_json(instance))
    assert restored == instance


def test_populated_instance_round_trips_via_json() -> None:
    instance = RuntimeSpec(
        mode="detached",
        log_level="debug",
        on_completion=OnCompletion(
            write_done_sentinel=False,
            print_contract_to_stdout=False,
        ),
    )
    restored = from_json(RuntimeSpec, to_json(instance))
    assert restored == instance


def test_round_trip_diff_is_empty() -> None:
    """Acceptance criterion: round-trip lossless."""
    instance = RuntimeSpec(
        mode="detached",
        log_level="warn",
        on_completion=OnCompletion(
            write_done_sentinel=True,
            print_contract_to_stdout=False,
        ),
    )
    payload_before = to_dict(instance)
    restored = from_dict(RuntimeSpec, payload_before)
    payload_after = to_dict(restored)
    assert payload_before == payload_after


def test_on_completion_nested_round_trips_standalone() -> None:
    """OnCompletion round-trips on its own (exported via __all__)."""
    instance = OnCompletion(write_done_sentinel=False, print_contract_to_stdout=True)
    restored = from_json(OnCompletion, to_json(instance))
    assert restored == instance
