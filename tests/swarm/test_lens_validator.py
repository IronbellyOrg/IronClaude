"""T02.15 -- COMP-023 lens validator tests.

Covers :mod:`superclaude.cli.swarm.lenses._validate`:

    1. File-ref assertion              -- empty or unreadable
       ``output_template_path`` is rejected.
    2. Recipe-registered assertion     -- empty or unknown
       ``recipe_name`` is rejected.
    3. Suspect ↔ ``{suspect_files}``   -- bidirectional coupling on
       ``recommended_next_command_template``.
    4. Name-uniqueness assertion       -- collision in registry
       context is rejected.
    5. §11.5 substring assertion       -- missing
       :data:`schema.CANONICAL_INJECTION_GUARD_SENTENCE` is rejected;
       single-source mutation property pinned.

Plus structural / contract tests:

    * Fail-fast: only the first failing assertion is reported per
      entry.
    * ``custom`` lens is exempt (short-circuits to ``None``).
    * Each rule identifier is a stable string constant.
"""

from __future__ import annotations

import pytest

from superclaude.cli.swarm.lenses._validate import (
    CUSTOM_LENS_NAME,
    RULE_FILE_REF_UNRESOLVED,
    RULE_INJECTION_SUBSTRING,
    RULE_NAME_DUPLICATE,
    RULE_RECIPE_UNREGISTERED,
    RULE_SUSPECT_COUPLING,
    SUSPECT_FILES_PLACEHOLDER,
    LensValidationFailure,
    default_file_resolver,
    default_recipe_checker,
    validate_lens,
)
from superclaude.cli.swarm.models import LensEntry
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _passing_lens(**overrides) -> LensEntry:
    """Build a :class:`LensEntry` that passes every COMP-023 assertion.

    Tests start from this baseline and mutate one field at a time to
    isolate each assertion. Keeping the baseline here (not at module
    scope) yields a fresh instance per call so mutation tests don't
    leak across cases.
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
def stub_recipe_checker():
    """Recipe checker that accepts the baseline recipe and nothing else."""

    def _check(name: str) -> bool:
        return name == "bare-review-v1"

    return _check


@pytest.fixture
def stub_strategy_checker():
    """Strategy checker that accepts the baseline strategy and nothing else.

    FR-LENSREG.NS / T02.21 sixth assertion. Parallel to
    :func:`stub_recipe_checker`; isolates the strategy assertion so
    tests that exercise other rules can assume strategy resolution
    succeeds unless they explicitly override.
    """

    def _check(strategy: str) -> bool:
        return strategy == "bug_list_v1"

    return _check


@pytest.fixture
def stub_file_resolver():
    """File resolver that pretends every non-empty path resolves."""

    def _resolve(path: str) -> bool:
        return bool(path and path.strip())

    return _resolve


# ---------------------------------------------------------------------------
# Baseline -- the fully-populated lens passes
# ---------------------------------------------------------------------------


def test_passing_lens_returns_none(
    stub_recipe_checker, stub_file_resolver, stub_strategy_checker
) -> None:
    entry = _passing_lens()
    result = validate_lens(
        entry,
        recipe_checker=stub_recipe_checker,
        file_resolver=stub_file_resolver,
        strategy_checker=stub_strategy_checker,
    )
    assert result is None


# ---------------------------------------------------------------------------
# Assertion 1 -- file refs resolve
# ---------------------------------------------------------------------------


def test_empty_output_template_path_rejected(
    stub_recipe_checker, stub_file_resolver
) -> None:
    entry = _passing_lens(output_template_path="")
    failure = validate_lens(
        entry,
        recipe_checker=stub_recipe_checker,
        file_resolver=stub_file_resolver,
    )
    assert failure is not None
    assert failure.rule == RULE_FILE_REF_UNRESOLVED
    assert failure.path == "output_template_path"
    assert failure.lens_name == "bare-review"


def test_unresolvable_output_template_path_rejected(
    stub_recipe_checker,
) -> None:
    entry = _passing_lens(output_template_path="/no/such/file.j2")

    def _never_resolves(path: str) -> bool:
        return False

    failure = validate_lens(
        entry,
        recipe_checker=stub_recipe_checker,
        file_resolver=_never_resolves,
    )
    assert failure is not None
    assert failure.rule == RULE_FILE_REF_UNRESOLVED


def test_default_file_resolver_rejects_empty_path() -> None:
    assert default_file_resolver("") is False
    assert default_file_resolver("   ") is False


def test_default_file_resolver_rejects_missing_path(tmp_path) -> None:
    missing = tmp_path / "does-not-exist.j2"
    assert default_file_resolver(str(missing)) is False


def test_default_file_resolver_accepts_real_file(tmp_path) -> None:
    real = tmp_path / "template.j2"
    real.write_text("body", encoding="utf-8")
    assert default_file_resolver(str(real)) is True


# ---------------------------------------------------------------------------
# Assertion 2 -- recipe registered
# ---------------------------------------------------------------------------


def test_empty_recipe_name_rejected(stub_file_resolver) -> None:
    entry = _passing_lens(recipe_name="")
    failure = validate_lens(
        entry,
        recipe_checker=lambda name: True,
        file_resolver=stub_file_resolver,
    )
    assert failure is not None
    assert failure.rule == RULE_RECIPE_UNREGISTERED
    assert failure.path == "recipe_name"


def test_unknown_recipe_rejected(stub_file_resolver) -> None:
    entry = _passing_lens(recipe_name="unknown-recipe-v9")

    def _empty_registry(name: str) -> bool:
        return False

    failure = validate_lens(
        entry,
        recipe_checker=_empty_registry,
        file_resolver=stub_file_resolver,
    )
    assert failure is not None
    assert failure.rule == RULE_RECIPE_UNREGISTERED


def test_default_recipe_checker_rejects_empty_name() -> None:
    assert default_recipe_checker("") is False


def test_default_recipe_checker_rejects_unknown_name() -> None:
    # The recipes module ships with an empty __all__ today (T01.19 only
    # lands the NormalizationSpec dataclass; M4 lands the runtime). The
    # default checker correctly returns False for every name until then.
    assert default_recipe_checker("recipe-that-does-not-exist") is False


def test_default_recipe_checker_consults_registry(monkeypatch) -> None:
    """When ``recipes.REGISTRY`` exists, the default checker uses it."""
    from superclaude.cli.swarm import recipes

    monkeypatch.setattr(recipes, "REGISTRY", {"stub-v1": object()}, raising=False)
    try:
        assert default_recipe_checker("stub-v1") is True
        assert default_recipe_checker("other") is False
    finally:
        monkeypatch.undo()


# ---------------------------------------------------------------------------
# Assertion 3 -- suspect ↔ {suspect_files} coupling
# ---------------------------------------------------------------------------


def test_suspect_true_without_placeholder_rejected(
    stub_recipe_checker, stub_file_resolver
) -> None:
    entry = _passing_lens(
        suspect=True,
        recommended_next_command_template="sc:reflect on {job_id}",
    )
    failure = validate_lens(
        entry,
        recipe_checker=stub_recipe_checker,
        file_resolver=stub_file_resolver,
    )
    assert failure is not None
    assert failure.rule == RULE_SUSPECT_COUPLING
    assert failure.path == "recommended_next_command_template"


def test_suspect_false_with_placeholder_rejected(
    stub_recipe_checker, stub_file_resolver
) -> None:
    entry = _passing_lens(
        suspect=False,
        recommended_next_command_template=(
            "sc:next on {job_id} " + SUSPECT_FILES_PLACEHOLDER
        ),
    )
    failure = validate_lens(
        entry,
        recipe_checker=stub_recipe_checker,
        file_resolver=stub_file_resolver,
    )
    assert failure is not None
    assert failure.rule == RULE_SUSPECT_COUPLING


def test_suspect_false_without_placeholder_accepted(
    stub_recipe_checker, stub_file_resolver, stub_strategy_checker
) -> None:
    entry = _passing_lens(
        suspect=False,
        recommended_next_command_template="sc:next on {job_id}",
    )
    assert (
        validate_lens(
            entry,
            recipe_checker=stub_recipe_checker,
            file_resolver=stub_file_resolver,
            strategy_checker=stub_strategy_checker,
        )
        is None
    )


# ---------------------------------------------------------------------------
# Assertion 4 -- name uniqueness
# ---------------------------------------------------------------------------


def test_duplicate_name_rejected_in_registry_context(
    stub_recipe_checker, stub_file_resolver
) -> None:
    entry = _passing_lens(name="bare-review")
    failure = validate_lens(
        entry,
        recipe_checker=stub_recipe_checker,
        file_resolver=stub_file_resolver,
        other_names=["refactor-find", "bare-review", "edge-case-hunt"],
    )
    assert failure is not None
    assert failure.rule == RULE_NAME_DUPLICATE
    assert failure.path == "name"
    assert failure.lens_name == "bare-review"


def test_unique_name_accepted(
    stub_recipe_checker, stub_file_resolver, stub_strategy_checker
) -> None:
    entry = _passing_lens(name="bare-review")
    assert (
        validate_lens(
            entry,
            recipe_checker=stub_recipe_checker,
            file_resolver=stub_file_resolver,
            strategy_checker=stub_strategy_checker,
            other_names=["refactor-find", "edge-case-hunt"],
        )
        is None
    )


def test_name_uniqueness_skipped_when_no_registry_context(
    stub_recipe_checker, stub_file_resolver, stub_strategy_checker
) -> None:
    """Standalone validation (no ``other_names``) skips assertion 4."""
    entry = _passing_lens(name="bare-review")
    assert (
        validate_lens(
            entry,
            recipe_checker=stub_recipe_checker,
            file_resolver=stub_file_resolver,
            strategy_checker=stub_strategy_checker,
        )
        is None
    )


# ---------------------------------------------------------------------------
# Assertion 5 -- §11.5 substring
# ---------------------------------------------------------------------------


def test_missing_injection_substring_rejected(
    stub_recipe_checker, stub_file_resolver
) -> None:
    entry = _passing_lens(
        system_prompt_fragment="Review carefully but no guard sentence."
    )
    failure = validate_lens(
        entry,
        recipe_checker=stub_recipe_checker,
        file_resolver=stub_file_resolver,
    )
    assert failure is not None
    assert failure.rule == RULE_INJECTION_SUBSTRING
    assert failure.path == "system_prompt_fragment"


def test_present_injection_substring_accepted(
    stub_recipe_checker, stub_file_resolver, stub_strategy_checker
) -> None:
    entry = _passing_lens(
        system_prompt_fragment=(
            "Prelude. " + CANONICAL_INJECTION_GUARD_SENTENCE + " Postlude."
        )
    )
    assert (
        validate_lens(
            entry,
            recipe_checker=stub_recipe_checker,
            file_resolver=stub_file_resolver,
            strategy_checker=stub_strategy_checker,
        )
        is None
    )


def test_custom_required_substring_override_honored(
    stub_recipe_checker, stub_file_resolver, stub_strategy_checker
) -> None:
    """A caller's custom substring is checked instead of the default."""
    entry = _passing_lens(system_prompt_fragment="Wraps GUARD-SENTINEL around target.")
    assert (
        validate_lens(
            entry,
            recipe_checker=stub_recipe_checker,
            file_resolver=stub_file_resolver,
            strategy_checker=stub_strategy_checker,
            required_substring="GUARD-SENTINEL",
        )
        is None
    )
    failure = validate_lens(
        entry,
        recipe_checker=stub_recipe_checker,
        file_resolver=stub_file_resolver,
        strategy_checker=stub_strategy_checker,
        required_substring="OTHER-SENTINEL",
    )
    assert failure is not None
    assert failure.rule == RULE_INJECTION_SUBSTRING


def test_dropping_injection_substring_fails_validation(
    stub_recipe_checker, stub_file_resolver, stub_strategy_checker
) -> None:
    """Mutation test (T02.15 validation): dropping §11.5 substring fails."""
    # Start from a passing entry, then mutate just the §11.5 substring out.
    entry = _passing_lens()
    assert (
        validate_lens(
            entry,
            recipe_checker=stub_recipe_checker,
            file_resolver=stub_file_resolver,
            strategy_checker=stub_strategy_checker,
        )
        is None
    )
    mutated = _passing_lens(
        system_prompt_fragment="Review carefully -- no guard sentence here."
    )
    failure = validate_lens(
        mutated,
        recipe_checker=stub_recipe_checker,
        file_resolver=stub_file_resolver,
        strategy_checker=stub_strategy_checker,
    )
    assert failure is not None
    assert failure.rule == RULE_INJECTION_SUBSTRING


# ---------------------------------------------------------------------------
# Custom-lens escape hatch
# ---------------------------------------------------------------------------


def test_custom_lens_skipped() -> None:
    """The ``custom`` lens is exempt and short-circuits to None."""
    entry = LensEntry(name=CUSTOM_LENS_NAME)  # all other fields at defaults
    # No stubs passed; the function must not call any of them.
    assert validate_lens(entry) is None


def test_custom_lens_name_constant_is_custom() -> None:
    assert CUSTOM_LENS_NAME == "custom"


# ---------------------------------------------------------------------------
# Fail-fast contract
# ---------------------------------------------------------------------------


def test_fail_fast_returns_first_assertion_only(
    stub_file_resolver,
) -> None:
    """Multiple violations present, only the first (assertion 1) reported."""
    # Empty file ref AND empty recipe name AND missing substring; the
    # fail-fast order means we should only see assertion 1.
    entry = _passing_lens(
        output_template_path="",
        recipe_name="",
        system_prompt_fragment="no guard here",
    )
    failure = validate_lens(
        entry,
        recipe_checker=lambda name: False,
        file_resolver=stub_file_resolver,
    )
    assert failure is not None
    assert failure.rule == RULE_FILE_REF_UNRESOLVED


def test_fail_fast_skips_remaining_after_recipe_failure(
    stub_file_resolver,
) -> None:
    """Recipe failure short-circuits assertions 3-5."""
    entry = _passing_lens(
        recipe_name="",  # assertion 2 fails
        recommended_next_command_template="no placeholder",  # would fail 3
        system_prompt_fragment="no guard",  # would fail 5
    )
    failure = validate_lens(
        entry,
        recipe_checker=lambda name: True,
        file_resolver=stub_file_resolver,
    )
    assert failure is not None
    assert failure.rule == RULE_RECIPE_UNREGISTERED


# ---------------------------------------------------------------------------
# Diagnostic shape
# ---------------------------------------------------------------------------


def test_lens_validation_failure_is_frozen_dataclass() -> None:
    failure = LensValidationFailure(
        rule=RULE_FILE_REF_UNRESOLVED,
        path="output_template_path",
        message="example",
        lens_name="bare-review",
    )
    with pytest.raises(Exception):  # FrozenInstanceError subclass of Exception
        failure.rule = RULE_RECIPE_UNREGISTERED  # type: ignore[misc]


def test_rule_constants_are_stable_strings() -> None:
    assert RULE_FILE_REF_UNRESOLVED == "lens.file_ref_unresolved"
    assert RULE_RECIPE_UNREGISTERED == "lens.recipe_unregistered"
    assert RULE_SUSPECT_COUPLING == "lens.suspect_files_coupling"
    assert RULE_NAME_DUPLICATE == "lens.name_duplicate"
    assert RULE_INJECTION_SUBSTRING == "lens.injection_substring_missing"


def test_suspect_files_placeholder_constant() -> None:
    assert SUSPECT_FILES_PLACEHOLDER == "{suspect_files}"
