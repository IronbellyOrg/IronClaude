"""T02.21 / FR-LENSREG.NS -- ``normalizer_strategy`` field + validator.

Pins the sixth COMP-023 assertion landed by T02.21 per the
anti-instinct remediation row 17a contract:

    Each ``LENSES`` entry declares ``normalizer_strategy`` matching the
    prompt's expected output shape; validator asserts a registered
    Recipe matches the strategy.

The roadmap row R-047 / FR-LENSREG.NS is the contract source. This
suite covers:

    1. The field exists on :class:`LensEntry` with the expected type
       and default.
    2. ``validate_lens`` rejects an empty ``normalizer_strategy`` with
       :data:`RULE_NORMALIZER_STRATEGY`.
    3. ``validate_lens`` rejects an unknown strategy (predicate
       returns False) with :data:`RULE_NORMALIZER_STRATEGY`.
    4. ``validate_lens`` accepts a strategy that resolves via the
       ``strategy_checker`` predicate.
    5. The 6th assertion is bypassed for the ``custom`` escape-hatch
       lens (parity with the other five assertions).
    6. ``default_strategy_checker`` consults ``recipes.STRATEGIES`` /
       ``REGISTRY`` / ``__all__`` in declared order.
    7. ``validate_all`` propagates the failure through the registry
       surface with one :class:`LensValidationFailure` per failing
       entry.

Mutation-style coverage: dropping ``normalizer_strategy`` from a lens
or removing its registration from the strategy checker reverts the
6th assertion's status from PASS to FAIL.
"""

from __future__ import annotations

import dataclasses

import pytest

from superclaude.cli.swarm.lenses._validate import (
    CUSTOM_LENS_NAME,
    RULE_NORMALIZER_STRATEGY,
    SUSPECT_FILES_PLACEHOLDER,
    LensValidationFailure,
    default_strategy_checker,
    validate_all,
    validate_lens,
)
from superclaude.cli.swarm.models import LensEntry
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _passing_lens(**overrides) -> LensEntry:
    """:class:`LensEntry` that passes all six COMP-023 assertions.

    The baseline mirrors :func:`tests.swarm.test_lens_validator._passing_lens`
    so the FR-LENSREG.NS suite isolates the sixth assertion without
    depending on the validator-test internals.
    """
    fields = dict(
        name="bare-review",
        description="bare review skeleton",
        system_prompt_fragment=(
            "Review with care. " + CANONICAL_INJECTION_GUARD_SENTENCE
        ),
        user_template="Review: {{target}}",
        output_template_path="/abs/path/to/template.j2",
        recipe_name="bare-review-v1",
        normalizer_strategy="bug_list_v1",
        default_workers=3,
        default_target_line_cap=8000,
        suspect=True,
        tier="T2",
        recommended_next_command_template=(
            "sc:reflect on {job_id} " + SUSPECT_FILES_PLACEHOLDER
        ),
        acceptance_notes="",
        stability="stable",
    )
    fields.update(overrides)
    return LensEntry(**fields)


@pytest.fixture
def accepting_recipe_checker():
    """Recipe checker that accepts every non-empty name."""

    def _check(name: str) -> bool:
        return bool(name)

    return _check


@pytest.fixture
def accepting_file_resolver():
    """File resolver that accepts every non-empty / non-whitespace path."""

    def _resolve(path: str) -> bool:
        return bool(path and path.strip())

    return _resolve


@pytest.fixture
def strategy_checker_for_bug_list():
    """Strategy checker that resolves only ``bug_list_v1``."""

    def _check(strategy: str) -> bool:
        return strategy == "bug_list_v1"

    return _check


# ---------------------------------------------------------------------------
# Section 1 -- field-level contract on :class:`LensEntry`
# ---------------------------------------------------------------------------


def test_lensentry_declares_normalizer_strategy_field() -> None:
    """FR-LENSREG.NS adds ``normalizer_strategy:str`` to LensEntry."""
    field_names = {f.name for f in dataclasses.fields(LensEntry)}
    assert "normalizer_strategy" in field_names, (
        "LensEntry must declare a ``normalizer_strategy`` field per "
        "FR-LENSREG.NS / T02.21. Missing field breaks the validator's "
        "sixth assertion."
    )


def test_normalizer_strategy_defaults_to_empty_string() -> None:
    """Default empty so unset entries fail the validator explicitly."""
    assert LensEntry().normalizer_strategy == ""


def test_normalizer_strategy_is_str_typed() -> None:
    """Field carries ``str`` per the roadmap row text."""
    fields = {f.name: f for f in dataclasses.fields(LensEntry)}
    assert fields["normalizer_strategy"].type in (str, "str"), (
        f"normalizer_strategy must be str-typed; got "
        f"{fields['normalizer_strategy'].type!r}"
    )


def test_normalizer_strategy_assigned_at_construction() -> None:
    entry = _passing_lens(normalizer_strategy="hypothesis_table_v1")
    assert entry.normalizer_strategy == "hypothesis_table_v1"


# ---------------------------------------------------------------------------
# Section 2 -- validator: empty strategy is rejected
# ---------------------------------------------------------------------------


def test_empty_normalizer_strategy_rejected(
    accepting_recipe_checker, accepting_file_resolver
) -> None:
    """AC: ``validate-lenses`` fails when ``normalizer_strategy`` is missing."""
    entry = _passing_lens(normalizer_strategy="")
    failure = validate_lens(
        entry,
        recipe_checker=accepting_recipe_checker,
        file_resolver=accepting_file_resolver,
        strategy_checker=lambda s: True,  # would-otherwise resolve everything
    )
    assert failure is not None, (
        "Empty normalizer_strategy must surface RULE_NORMALIZER_STRATEGY; "
        "T02.21 AC: 'validate-lenses fails when normalizer_strategy is "
        "missing or unmatched'."
    )
    assert failure.rule == RULE_NORMALIZER_STRATEGY
    assert failure.path == "normalizer_strategy"
    assert failure.lens_name == "bare-review"


# ---------------------------------------------------------------------------
# Section 3 -- validator: unmatched strategy is rejected
# ---------------------------------------------------------------------------


def test_unknown_normalizer_strategy_rejected(
    accepting_recipe_checker, accepting_file_resolver
) -> None:
    """AC: validator asserts a registered Recipe matches the strategy."""
    entry = _passing_lens(normalizer_strategy="unknown_strategy_v9")

    def _empty_strategy_registry(strategy: str) -> bool:
        return False

    failure = validate_lens(
        entry,
        recipe_checker=accepting_recipe_checker,
        file_resolver=accepting_file_resolver,
        strategy_checker=_empty_strategy_registry,
    )
    assert failure is not None
    assert failure.rule == RULE_NORMALIZER_STRATEGY


def test_failure_message_names_failing_strategy(
    accepting_recipe_checker, accepting_file_resolver
) -> None:
    """Diagnostic surfaces the strategy value for grep-friendly output."""
    entry = _passing_lens(normalizer_strategy="bogus_strategy")
    failure = validate_lens(
        entry,
        recipe_checker=accepting_recipe_checker,
        file_resolver=accepting_file_resolver,
        strategy_checker=lambda s: False,
    )
    assert failure is not None
    assert "bogus_strategy" in failure.message
    assert "bare-review" in failure.message


# ---------------------------------------------------------------------------
# Section 4 -- validator: known strategy is accepted
# ---------------------------------------------------------------------------


def test_known_normalizer_strategy_accepted(
    accepting_recipe_checker,
    accepting_file_resolver,
    strategy_checker_for_bug_list,
) -> None:
    """Fully-populated entry with a resolvable strategy passes validation."""
    entry = _passing_lens(normalizer_strategy="bug_list_v1")
    assert (
        validate_lens(
            entry,
            recipe_checker=accepting_recipe_checker,
            file_resolver=accepting_file_resolver,
            strategy_checker=strategy_checker_for_bug_list,
        )
        is None
    )


# ---------------------------------------------------------------------------
# Section 5 -- custom escape hatch is exempt from assertion 6
# ---------------------------------------------------------------------------


def test_custom_lens_skips_normalizer_strategy_assertion() -> None:
    """``custom`` is exempt from validation per COMP-026 / FR-021 / INV-003.

    The escape-hatch lens's prompt content flows in from
    ``--custom-prompt-dir`` at preflight; validating its registry row
    would only invite drift.
    """
    entry = LensEntry(name=CUSTOM_LENS_NAME, normalizer_strategy="")
    assert validate_lens(entry) is None


# ---------------------------------------------------------------------------
# Section 6 -- default_strategy_checker behavior across recipes surfaces
# ---------------------------------------------------------------------------


def test_default_strategy_checker_rejects_empty() -> None:
    assert default_strategy_checker("") is False


def test_default_strategy_checker_rejects_unknown() -> None:
    """Until M4 lands the recipes runtime, no strategy resolves."""
    assert default_strategy_checker("strategy-that-does-not-exist") is False


def test_default_strategy_checker_consults_strategies_set(monkeypatch) -> None:
    from superclaude.cli.swarm import recipes

    monkeypatch.setattr(recipes, "STRATEGIES", {"bug_list_v1"}, raising=False)
    try:
        assert default_strategy_checker("bug_list_v1") is True
        assert default_strategy_checker("other") is False
    finally:
        monkeypatch.undo()


def test_default_strategy_checker_consults_strategies_dict(monkeypatch) -> None:
    """``STRATEGIES`` may be a mapping (strategy -> recipe identifier)."""
    from superclaude.cli.swarm import recipes

    monkeypatch.setattr(
        recipes, "STRATEGIES", {"bug_list_v1": "bare-review-v1"}, raising=False
    )
    try:
        assert default_strategy_checker("bug_list_v1") is True
        assert default_strategy_checker("other") is False
    finally:
        monkeypatch.undo()


def test_default_strategy_checker_consults_registry_keys(monkeypatch) -> None:
    """``REGISTRY`` keyed on strategy names resolves the strategy.

    The default lookup consults STRATEGIES first; clear it so the
    REGISTRY branch is observable. T02.23 populates a real STRATEGIES
    dict in ``recipes/__init__.py`` for the bundled lenses; this test
    pins the REGISTRY-fallback behavior independent of that population.
    """
    from superclaude.cli.swarm import recipes

    if hasattr(recipes, "STRATEGIES"):
        monkeypatch.delattr(recipes, "STRATEGIES", raising=False)
    monkeypatch.setattr(recipes, "REGISTRY", {"bug_list_v1": object()}, raising=False)
    try:
        assert default_strategy_checker("bug_list_v1") is True
        assert default_strategy_checker("other") is False
    finally:
        monkeypatch.undo()


def test_default_strategy_checker_consults_registry_strategy_attr(
    monkeypatch,
) -> None:
    """``REGISTRY`` values may declare a ``.strategy`` attribute.

    Clears STRATEGIES (populated by T02.23) so the REGISTRY-attribute
    branch is observable.
    """
    from superclaude.cli.swarm import recipes

    class _Recipe:
        strategy = "bug_list_v1"

    if hasattr(recipes, "STRATEGIES"):
        monkeypatch.delattr(recipes, "STRATEGIES", raising=False)
    monkeypatch.setattr(
        recipes, "REGISTRY", {"bare-review-v1": _Recipe()}, raising=False
    )
    try:
        assert default_strategy_checker("bug_list_v1") is True
        assert default_strategy_checker("other") is False
    finally:
        monkeypatch.undo()


def test_default_strategy_checker_consults_all_fallback(monkeypatch) -> None:
    """When neither STRATEGIES nor REGISTRY exist, ``__all__`` is the fallback."""
    from superclaude.cli.swarm import recipes

    # Make sure neither STRATEGIES nor REGISTRY shadows the __all__ branch.
    if hasattr(recipes, "STRATEGIES"):
        monkeypatch.delattr(recipes, "STRATEGIES", raising=False)
    if hasattr(recipes, "REGISTRY"):
        monkeypatch.delattr(recipes, "REGISTRY", raising=False)
    monkeypatch.setattr(recipes, "__all__", ["bug_list_v1"], raising=False)
    try:
        assert default_strategy_checker("bug_list_v1") is True
        assert default_strategy_checker("other") is False
    finally:
        monkeypatch.undo()


# ---------------------------------------------------------------------------
# Section 7 -- validate_all propagates the failure
# ---------------------------------------------------------------------------


def test_validate_all_surfaces_strategy_failure(
    accepting_recipe_checker, accepting_file_resolver
) -> None:
    """A registry entry with empty strategy surfaces one failure."""
    registry = {
        "bare-review": _passing_lens(name="bare-review", normalizer_strategy=""),
    }
    failures = validate_all(
        registry,
        recipe_checker=accepting_recipe_checker,
        file_resolver=accepting_file_resolver,
        strategy_checker=lambda s: True,
    )
    assert len(failures) == 1
    assert failures[0].rule == RULE_NORMALIZER_STRATEGY
    assert failures[0].lens_name == "bare-review"


def test_validate_all_surfaces_unmatched_strategy_failure(
    accepting_recipe_checker, accepting_file_resolver
) -> None:
    """Strategy that doesn't resolve surfaces one failure per entry."""
    registry = {
        "bare-review": _passing_lens(
            name="bare-review", normalizer_strategy="unknown_v9"
        ),
        "refactor-find": _passing_lens(
            name="refactor-find",
            suspect=False,
            recommended_next_command_template="sc:next on {job_id}",
            normalizer_strategy="also_unknown",
        ),
    }
    failures = validate_all(
        registry,
        recipe_checker=accepting_recipe_checker,
        file_resolver=accepting_file_resolver,
        strategy_checker=lambda s: False,
    )
    assert len(failures) == 2
    assert {f.lens_name for f in failures} == {"bare-review", "refactor-find"}
    assert all(f.rule == RULE_NORMALIZER_STRATEGY for f in failures)


def test_validate_all_clean_when_strategy_resolves(
    accepting_recipe_checker,
    accepting_file_resolver,
    strategy_checker_for_bug_list,
) -> None:
    """Strategy that resolves clears the registry."""
    registry = {
        "bare-review": _passing_lens(name="bare-review"),
    }
    failures = validate_all(
        registry,
        recipe_checker=accepting_recipe_checker,
        file_resolver=accepting_file_resolver,
        strategy_checker=strategy_checker_for_bug_list,
    )
    assert failures == []


# ---------------------------------------------------------------------------
# Mutation-style guard: removing the field flips the verdict
# ---------------------------------------------------------------------------


def test_dropping_normalizer_strategy_flips_validation_to_fail(
    accepting_recipe_checker,
    accepting_file_resolver,
    strategy_checker_for_bug_list,
) -> None:
    """Mutation: a passing entry that drops normalizer_strategy fails."""
    passing = _passing_lens()
    assert (
        validate_lens(
            passing,
            recipe_checker=accepting_recipe_checker,
            file_resolver=accepting_file_resolver,
            strategy_checker=strategy_checker_for_bug_list,
        )
        is None
    )
    mutated = _passing_lens(normalizer_strategy="")
    failure = validate_lens(
        mutated,
        recipe_checker=accepting_recipe_checker,
        file_resolver=accepting_file_resolver,
        strategy_checker=strategy_checker_for_bug_list,
    )
    assert failure is not None
    assert failure.rule == RULE_NORMALIZER_STRATEGY


# ---------------------------------------------------------------------------
# Rule-identifier stability
# ---------------------------------------------------------------------------


def test_rule_normalizer_strategy_constant_is_stable_string() -> None:
    """Tests assert on the rule identifier; pin its value."""
    assert RULE_NORMALIZER_STRATEGY == "lens.normalizer_strategy_unmatched"


def test_failure_is_a_lens_validation_failure(
    accepting_recipe_checker, accepting_file_resolver
) -> None:
    """The 6th assertion's failure carries the standard diagnostic shape."""
    entry = _passing_lens(normalizer_strategy="")
    failure = validate_lens(
        entry,
        recipe_checker=accepting_recipe_checker,
        file_resolver=accepting_file_resolver,
        strategy_checker=lambda s: True,
    )
    assert isinstance(failure, LensValidationFailure)
