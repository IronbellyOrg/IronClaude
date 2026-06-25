"""T02.14 -- ``LENSES`` registry + :func:`get_lens` helper tests.

Covers the COMP-022 scaffold landed by T02.14:

    - Registry exports the eight well-known keys (bare-review,
      refactor-find, edge-case-hunt, spec-completeness,
      feasibility-probe, troubleshoot-hypothesis, doc-completeness,
      custom) in canonical :data:`LENS_NAMES` order.
    - Every entry is a :class:`LensEntry`.
    - :func:`get_lens` resolves known names verbatim and raises
      ``KeyError`` for unknown names.
    - Registry entries round-trip through
      :meth:`ResolvedLensEntry.from_lens` (snapshot intact, per the
      T02.14 acceptance criterion).

T02.23 will replace the placeholder bodies with fully-populated lens
fields. This test pins the *registry shape* (count, names, types,
helper contract) which T02.23 must preserve.
"""

from __future__ import annotations

import pytest

from superclaude.cli.swarm.lenses import (
    LENS_NAMES,
    LENSES,
    get_lens,
    iter_lenses,
)
from superclaude.cli.swarm.models import LensEntry, ResolvedLensEntry


EXPECTED_LENS_NAMES: tuple[str, ...] = (
    "bare-review",
    "refactor-find",
    "edge-case-hunt",
    "spec-completeness",
    "feasibility-probe",
    "troubleshoot-hypothesis",
    "doc-completeness",
    "reflect-review",
    "custom",
)


# ---------------------------------------------------------------------------
# Registry shape
# ---------------------------------------------------------------------------


def test_registry_has_exactly_nine_entries() -> None:
    assert len(LENSES) == 9


def test_registry_contains_nine_canonical_names() -> None:
    assert set(LENSES.keys()) == set(EXPECTED_LENS_NAMES)


def test_lens_names_tuple_matches_canonical_order() -> None:
    assert LENS_NAMES == EXPECTED_LENS_NAMES


def test_every_entry_is_a_lens_entry() -> None:
    for name, entry in LENSES.items():
        assert isinstance(entry, LensEntry), name


def test_entry_name_field_matches_registry_key() -> None:
    for name, entry in LENSES.items():
        assert entry.name == name


# ---------------------------------------------------------------------------
# ``get_lens`` helper
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", EXPECTED_LENS_NAMES)
def test_get_lens_resolves_every_known_name(name: str) -> None:
    entry = get_lens(name)
    assert isinstance(entry, LensEntry)
    assert entry.name == name
    assert entry is LENSES[name]  # identity, not just equality


def test_get_lens_unknown_raises_keyerror() -> None:
    with pytest.raises(KeyError) as excinfo:
        get_lens("no-such-lens")
    assert excinfo.value.args[0] == "no-such-lens"


def test_get_lens_empty_string_raises_keyerror() -> None:
    with pytest.raises(KeyError):
        get_lens("")


# ---------------------------------------------------------------------------
# Round-trip: registry → ResolvedLensEntry snapshot intact
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", EXPECTED_LENS_NAMES)
def test_registry_entry_round_trips_to_resolved_snapshot(name: str) -> None:
    entry = LENSES[name]
    snapshot = ResolvedLensEntry.from_lens(entry)
    assert isinstance(snapshot, ResolvedLensEntry)
    # The nine DM-011 fields mirror the LensEntry verbatim.
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


# ---------------------------------------------------------------------------
# ``iter_lenses`` helper
# ---------------------------------------------------------------------------


def test_iter_lenses_yields_nine_entries_in_canonical_order() -> None:
    yielded = list(iter_lenses())
    assert len(yielded) == 9
    assert [entry.name for entry in yielded] == list(EXPECTED_LENS_NAMES)
    for entry in yielded:
        assert isinstance(entry, LensEntry)
