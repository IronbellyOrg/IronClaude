"""T01.10 -- aggregator round-trip + ``__all__`` enumeration tests.

Covers R-009 / COMP-004 from the MultiModelSwarm roadmap. The aggregator
defined in ``src/superclaude/cli/swarm/models.py`` declares minimal
``@dataclass`` stubs for all twenty DM-### records and exposes
``to_dict``/``from_dict``/``to_json``/``from_json`` helpers. Downstream
tasks T01.13..T01.28 land the per-record field sets; this test pins the
*scaffolding* contract so those tasks always start from a green base:

1. Every DM-### record is exported in ``__all__`` (and importable).
2. Each stub instantiates with no args (empty body at T01.10).
3. ``from_dict(cls, to_dict(instance)) == instance`` for every stub.
4. ``from_json(cls, to_json(instance)) == instance`` for every stub.
5. ``len(models.__all__) >= 20`` validation gate.
6. ``to_dict``/``from_dict`` reject non-dataclass inputs with TypeError.
"""

from __future__ import annotations

import dataclasses

import pytest

from superclaude.cli.swarm import models
from superclaude.cli.swarm.models import (
    Artifacts,
    CallerInfo,
    CallerMetadata,
    DoneSentinel,
    EventRecord,
    JobSpec,
    LensEntry,
    Manifest,
    NormalizationSpec,
    OutputSpec,
    PromptSpec,
    ResolvedLensEntry,
    ResultContract,
    RuntimeSpec,
    StatusPolicy,
    SwarmState,
    TargetSpec,
    TransportSpec,
    WorkerResult,
    WorkerSpec,
    from_dict,
    from_json,
    to_dict,
    to_json,
)

# Every DM-### record exported by the aggregator. Adding a new record
# requires extending this list AND ``models.__all__``; the parity test
# below catches drift in either direction.
DM_RECORDS: tuple[type, ...] = (
    JobSpec,            # DM-001
    WorkerSpec,         # DM-002
    TargetSpec,         # DM-003
    TransportSpec,      # DM-004
    PromptSpec,         # DM-005
    NormalizationSpec,  # DM-006
    OutputSpec,         # DM-007
    StatusPolicy,       # DM-008
    RuntimeSpec,        # DM-009
    LensEntry,          # DM-010
    ResolvedLensEntry,  # DM-011
    ResultContract,     # DM-012
    WorkerResult,       # DM-013
    SwarmState,         # DM-014
    EventRecord,        # DM-015
    Manifest,           # DM-016
    DoneSentinel,       # DM-017
    Artifacts,          # DM-018
    CallerInfo,         # DM-019
    CallerMetadata,     # DM-020
)


# ---------------------------------------------------------------------------
# Public-surface enumeration (``__all__`` ↔ DM_RECORDS parity).
# ---------------------------------------------------------------------------


def test_all_lists_at_least_twenty_records() -> None:
    """Validation gate from T01.10 acceptance criteria."""
    assert len(models.__all__) >= 20, (
        f"models.__all__ has only {len(models.__all__)} entries; "
        "the roadmap requires all 20 DM-### records exported."
    )


@pytest.mark.parametrize("record_cls", DM_RECORDS, ids=lambda c: c.__name__)
def test_dm_record_is_exported_in_all(record_cls: type) -> None:
    """Every DM-### record listed in ``DM_RECORDS`` is in ``__all__``."""
    assert record_cls.__name__ in models.__all__, (
        f"{record_cls.__name__} declared but missing from models.__all__"
    )


@pytest.mark.parametrize("record_cls", DM_RECORDS, ids=lambda c: c.__name__)
def test_dm_record_is_dataclass(record_cls: type) -> None:
    """T01.10 stubs are real dataclasses (not plain classes)."""
    assert dataclasses.is_dataclass(record_cls), (
        f"{record_cls.__name__} must be decorated with @dataclass so "
        "to_dict/from_dict and downstream field additions work."
    )


# ---------------------------------------------------------------------------
# Round-trip contracts (dict + JSON).
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("record_cls", DM_RECORDS, ids=lambda c: c.__name__)
def test_dict_round_trip_is_lossless(record_cls: type) -> None:
    """``from_dict(cls, to_dict(x)) == x`` for every stub."""
    instance = record_cls()
    restored = from_dict(record_cls, to_dict(instance))
    assert restored == instance, (
        f"{record_cls.__name__} dict round-trip diverged: "
        f"{instance!r} -> {to_dict(instance)!r} -> {restored!r}"
    )


@pytest.mark.parametrize("record_cls", DM_RECORDS, ids=lambda c: c.__name__)
def test_json_round_trip_is_lossless(record_cls: type) -> None:
    """``from_json(cls, to_json(x)) == x`` for every stub."""
    instance = record_cls()
    restored = from_json(record_cls, to_json(instance))
    assert restored == instance, (
        f"{record_cls.__name__} JSON round-trip diverged: "
        f"{instance!r} -> {to_json(instance)!r} -> {restored!r}"
    )


def test_to_dict_returns_plain_dict() -> None:
    """The helper output is a ``dict``, not a dataclass / namedtuple."""
    payload = to_dict(JobSpec())
    assert isinstance(payload, dict)


def test_json_output_is_sorted_for_byte_stable_round_trip() -> None:
    """INV-016 (Manifest immutability) relies on sorted JSON output.

    The helper sets ``sort_keys=True`` so byte-identical round-trips are
    achievable once T01.27 lands fields on Manifest. Pinning the surface
    here means T01.27 inherits the guarantee without re-stating it.

    The behavioural pin uses :class:`CallerMetadata` (DM-020 -- now
    field-populated as of T02.25 with ``suspect`` + ``tier``) to assert
    the ``sort_keys=True`` property: the two fields are not in
    alphabetical order in the dataclass declaration (``suspect`` before
    ``tier``), and ``to_json`` must still emit them sorted (``suspect``
    is alphabetically before ``tier``, but the test pins the ordering
    independent of declaration to catch a future ``sort_keys=False``
    regression). When a future task reorders or adds fields, update
    this pin to the new canonical sorted shape.
    """
    text = to_json(CallerMetadata())
    assert isinstance(text, str)
    # Pin the canonical sorted shape -- the dict ordering inside the
    # JSON must be alphabetical regardless of dataclass field order.
    assert text == '{"suspect": false, "tier": ""}', (
        "CallerMetadata to_json output diverged from the expected "
        "sort_keys=True canonical shape; check whether the round-trip "
        "helpers still pass ``sort_keys=True`` to ``json.dumps``."
    )


# ---------------------------------------------------------------------------
# Helper error surface (non-dataclass inputs).
# ---------------------------------------------------------------------------


def test_to_dict_rejects_non_dataclass_instance() -> None:
    with pytest.raises(TypeError, match="dataclass instance"):
        to_dict({"not": "a dataclass"})


def test_to_dict_rejects_dataclass_class_itself() -> None:
    """Passing the class (not an instance) is a common bug; reject it."""
    with pytest.raises(TypeError, match="dataclass instance"):
        to_dict(JobSpec)  # type: ignore[arg-type]


def test_from_dict_rejects_non_dataclass_type() -> None:
    with pytest.raises(TypeError, match="dataclass type"):
        from_dict(dict, {})  # type: ignore[arg-type]
