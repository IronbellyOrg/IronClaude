"""T02.23 -- bundled 7 non-custom lens entry files pass the validator.

Covers the T02.23 acceptance criteria:

    1. Seven lens files exist under ``cli/swarm/lenses/`` for the
       non-custom built-ins (COMP-024..030).
    2. Each module exports a ``LENS: LensEntry`` constant declaring the
       DM-010 + FR-LENSREG.NS field set: ``name``,
       ``system_prompt_fragment``, ``user_template``, ``recipe_name``,
       ``normalizer_strategy``, ``default_workers``, ``suspect``,
       ``tier``, ``recommended_next_command_template``, ``stability``.
    3. Per-lens field guards: ``bare-review.suspect == True``,
       ``bare-review.tier == "T2"``, ``bare-review.default_workers == 3``;
       ``edge-case-hunt.default_workers == 4``;
       ``troubleshoot-hypothesis.default_workers == 4``.
    4. All 7 non-custom entries pass the COMP-023 lens validator
       (``validate-lenses`` exit 0 on the bundled set).
    5. The aggregator (``cli/swarm/lenses/__init__.py``) wires each
       LENS constant into :data:`LENSES` under the matching key, with
       ``custom`` retained as the escape-hatch placeholder.

The validator-pass test exercises the real default checkers (recipe
registry + strategy registry from
:mod:`superclaude.cli.swarm.recipes`) so a regression in either
registry surface (T02.23 adds the registry seeds for the 7 built-ins
to ``recipes/__init__.py``) breaks here in lockstep with the lens
authoring.
"""

from __future__ import annotations

import importlib

import pytest

from superclaude.cli.swarm.lenses import LENS_NAMES, LENSES
from superclaude.cli.swarm.lenses._validate import (
    CUSTOM_LENS_NAME,
    validate_all,
    validate_lens,
)
from superclaude.cli.swarm.models import LensEntry
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

# ---------------------------------------------------------------------------
# Inventory: the 7 non-custom lens module names + their registry keys.
# Keep the (module, key) pairing explicit so a rename on either side trips
# the test immediately.
# ---------------------------------------------------------------------------


NON_CUSTOM_LENS_MODULES: tuple[tuple[str, str], ...] = (
    ("superclaude.cli.swarm.lenses.bare_review", "bare-review"),
    ("superclaude.cli.swarm.lenses.refactor_find", "refactor-find"),
    ("superclaude.cli.swarm.lenses.edge_case_hunt", "edge-case-hunt"),
    ("superclaude.cli.swarm.lenses.spec_completeness", "spec-completeness"),
    ("superclaude.cli.swarm.lenses.feasibility_probe", "feasibility-probe"),
    (
        "superclaude.cli.swarm.lenses.troubleshoot_hypothesis",
        "troubleshoot-hypothesis",
    ),
    ("superclaude.cli.swarm.lenses.doc_completeness", "doc-completeness"),
    ("superclaude.cli.swarm.lenses.reflect_review", "reflect-review"),
)


# ---------------------------------------------------------------------------
# Module shape -- each of the 8 modules exports a ``LENS`` constant.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "module_path,registry_key",
    NON_CUSTOM_LENS_MODULES,
    ids=[key for _, key in NON_CUSTOM_LENS_MODULES],
)
def test_lens_module_exports_lens_constant(module_path: str, registry_key: str) -> None:
    mod = importlib.import_module(module_path)
    assert hasattr(mod, "LENS"), f"{module_path} missing LENS constant"
    assert isinstance(mod.LENS, LensEntry)
    assert mod.LENS.name == registry_key


@pytest.mark.parametrize(
    "module_path,registry_key",
    NON_CUSTOM_LENS_MODULES,
    ids=[key for _, key in NON_CUSTOM_LENS_MODULES],
)
def test_lens_module_lens_is_registered_under_matching_key(
    module_path: str, registry_key: str
) -> None:
    mod = importlib.import_module(module_path)
    assert LENSES[registry_key] is mod.LENS


# ---------------------------------------------------------------------------
# DM-010 + FR-LENSREG.NS field set -- every populated lens declares each
# field non-empty / explicit.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "key",
    [key for _, key in NON_CUSTOM_LENS_MODULES],
)
def test_lens_declares_full_dm010_field_set(key: str) -> None:
    lens = LENSES[key]
    # AC: name, system_prompt_fragment, user_template, recipe_name,
    # default_workers, suspect, tier, recommended_next_command_template,
    # stability.
    assert lens.name == key
    assert lens.system_prompt_fragment, f"{key}: empty system_prompt_fragment"
    assert lens.user_template, f"{key}: empty user_template"
    assert lens.recipe_name, f"{key}: empty recipe_name"
    assert lens.normalizer_strategy, f"{key}: empty normalizer_strategy"
    assert lens.default_workers >= 2, f"{key}: default_workers below floor"
    assert isinstance(lens.suspect, bool)
    assert lens.tier, f"{key}: empty tier"
    assert lens.recommended_next_command_template, (
        f"{key}: empty recommended_next_command_template"
    )
    assert lens.stability in ("stable", "experimental")


# ---------------------------------------------------------------------------
# Per-lens field guards (T02.23 acceptance criterion).
# ---------------------------------------------------------------------------


def test_bare_review_field_guards() -> None:
    lens = LENSES["bare-review"]
    assert lens.suspect is True
    assert lens.tier == "T2"
    assert lens.default_workers == 3
    assert lens.stability == "stable"
    # suspect=True requires {suspect_files} in the next-cmd template
    # (COMP-023 assertion 3).
    assert "{suspect_files}" in lens.recommended_next_command_template


def test_edge_case_hunt_workers_is_four() -> None:
    assert LENSES["edge-case-hunt"].default_workers == 4


def test_troubleshoot_hypothesis_workers_is_four() -> None:
    assert LENSES["troubleshoot-hypothesis"].default_workers == 4


@pytest.mark.parametrize(
    "key",
    [
        "refactor-find",
        "edge-case-hunt",
        "spec-completeness",
        "feasibility-probe",
        "troubleshoot-hypothesis",
        "doc-completeness",
    ],
)
def test_experimental_lenses_are_marked_experimental(key: str) -> None:
    """Every non-bare-review lens ships at experimental stability per spec §3.3."""
    assert LENSES[key].stability == "experimental"


# ---------------------------------------------------------------------------
# §11.5 substring is present in every non-custom system_prompt_fragment.
# Mirrors COMP-023 assertion 5 from the validator side; pins the
# parent-spec INV-003 / INV-014 parity at the bundled-content level so a
# future copy edit cannot silently drop the guard sentence from any one
# lens.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "key",
    [key for _, key in NON_CUSTOM_LENS_MODULES],
)
def test_system_prompt_fragment_contains_injection_guard(key: str) -> None:
    assert CANONICAL_INJECTION_GUARD_SENTENCE in LENSES[key].system_prompt_fragment


# ---------------------------------------------------------------------------
# Validator pass -- the U-008 entry point (T02.16).
# ---------------------------------------------------------------------------


def test_validate_all_returns_no_failures_on_bundled_registry() -> None:
    failures = validate_all(LENSES)
    assert failures == [], (
        "Bundled LENSES registry must pass validate-lenses on the "
        "real default checkers (recipe + strategy + file resolver)."
    )


@pytest.mark.parametrize(
    "key",
    [key for _, key in NON_CUSTOM_LENS_MODULES],
)
def test_validate_lens_passes_per_entry(key: str) -> None:
    other_names = [name for name in LENS_NAMES if name != key]
    failure = validate_lens(LENSES[key], other_names=other_names)
    assert failure is None, f"{key}: {failure}"


# ---------------------------------------------------------------------------
# Custom escape-hatch entry remains intentionally exempt and placeholder-shaped.
# ---------------------------------------------------------------------------


def test_custom_entry_is_placeholder() -> None:
    custom = LENSES[CUSTOM_LENS_NAME]
    assert custom.name == CUSTOM_LENS_NAME
    assert custom.system_prompt_fragment == ""
    assert custom.recipe_name == ""
    assert custom.normalizer_strategy == ""


def test_validate_all_skips_custom_lens() -> None:
    # The bundled registry passes; mutating only `custom` to a junk shape
    # must still produce zero failures since `custom` is skipped.
    custom = LENSES[CUSTOM_LENS_NAME]
    junk = LensEntry(name=CUSTOM_LENS_NAME)  # all dataclass defaults
    # Build a registry where `custom` is replaced with a deliberately-empty
    # entry; every other entry is unchanged.
    mutated = dict(LENSES)
    mutated[CUSTOM_LENS_NAME] = junk
    failures = validate_all(mutated)
    assert failures == [], (
        "Custom escape-hatch lens must be skipped regardless of body."
    )
    # Sanity: the un-mutated entry is the actual placeholder.
    assert custom.name == CUSTOM_LENS_NAME


# ---------------------------------------------------------------------------
# Registry shape preserved (T02.14 / T02.17 gate -- 8 total entries,
# 7 non-custom + 1 custom).
# ---------------------------------------------------------------------------


def test_registry_has_nine_entries() -> None:
    assert len(LENSES) == 9


def test_registry_non_custom_count_is_eight() -> None:
    non_custom = [e for e in LENSES.values() if e.name != CUSTOM_LENS_NAME]
    assert len(non_custom) == 8
