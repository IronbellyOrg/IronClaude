"""T02.16 -- U-008 ``swarm validate-lenses`` registry-level validator tests.

Covers :func:`superclaude.cli.swarm.lenses._validate.validate_all`:

    1. Iterates every entry in the supplied registry and applies the
       five COMP-023 assertions via :func:`validate_lens`.
    2. Skips the COMP-026 ``custom`` escape-hatch lens.
    3. Returns one :class:`LensValidationFailure` per failing entry
       (per-entry fail-fast; first failing assertion only) in
       registry-iteration order.
    4. Wires the name-uniqueness assertion (assertion 4) registry-wide
       by deriving ``other_names`` from every other entry's
       ``LensEntry.name`` -- not from the dict keys.
    5. Returns an empty list when every non-custom entry passes.

The bundled :data:`LENSES` registry today carries placeholder entries
(see ``cli/swarm/lenses/__init__.py``); T02.23 replaces those with
fully-populated bodies and T02.17 ratifies the "7 of 8 pass" gate on
the populated set. The tests in this module therefore use synthesized
fixture registries to exercise the validator contract and pin
:func:`validate_all`'s behavior independent of the placeholder ↔
populated transition. One smoke test (``test_bundled_registry_*``)
exercises the real :data:`LENSES` import to confirm registry-iteration
order, custom-skip, and rule-identifier surfacing on the live placeholders.
"""

from __future__ import annotations

import pytest

from superclaude.cli.swarm.lenses import LENSES, LENS_NAMES
from superclaude.cli.swarm.lenses._validate import (
    CUSTOM_LENS_NAME,
    LensValidationFailure,
    RULE_FILE_REF_UNRESOLVED,
    RULE_INJECTION_SUBSTRING,
    RULE_NAME_DUPLICATE,
    RULE_NORMALIZER_STRATEGY,
    RULE_RECIPE_UNREGISTERED,
    RULE_SUSPECT_COUPLING,
    SUSPECT_FILES_PLACEHOLDER,
    validate_all,
)
from superclaude.cli.swarm.models import LensEntry
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE


# ---------------------------------------------------------------------------
# Fixtures -- fully-populated synthesised lens entries
# ---------------------------------------------------------------------------


def _passing_lens(**overrides) -> LensEntry:
    """Synthesised :class:`LensEntry` that passes every COMP-023 assertion."""
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


def _custom_lens() -> LensEntry:
    """The escape-hatch entry (intentionally exempt from validation)."""
    return LensEntry(name=CUSTOM_LENS_NAME)


@pytest.fixture
def accepting_recipe_checker():
    """Recipe checker that accepts every non-empty name (test isolation)."""

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
def accepting_strategy_checker():
    """Strategy checker that accepts every non-empty name (test isolation).

    FR-LENSREG.NS / T02.21 sixth assertion. Parallel to
    :func:`accepting_recipe_checker`; tests that exercise other rules
    use this so the strategy assertion does not spuriously fire.
    """

    def _check(strategy: str) -> bool:
        return bool(strategy)

    return _check


@pytest.fixture
def rejecting_recipe_checker():
    """Recipe checker that rejects every name (forces assertion 2 to fire)."""

    def _check(name: str) -> bool:
        return False

    return _check


@pytest.fixture
def rejecting_strategy_checker():
    """Strategy checker that rejects every name (forces assertion 6 to fire)."""

    def _check(strategy: str) -> bool:
        return False

    return _check


@pytest.fixture
def rejecting_file_resolver():
    """File resolver that rejects every path (forces assertion 1 to fire)."""

    def _resolve(path: str) -> bool:
        return False

    return _resolve


# ---------------------------------------------------------------------------
# Empty + custom-only registries -- baseline contracts
# ---------------------------------------------------------------------------


def test_empty_registry_returns_empty_list(
    accepting_recipe_checker, accepting_file_resolver
) -> None:
    """No entries => no failures."""
    assert (
        validate_all(
            {},
            recipe_checker=accepting_recipe_checker,
            file_resolver=accepting_file_resolver,
        )
        == []
    )


def test_only_custom_lens_returns_empty_list(
    accepting_recipe_checker, accepting_file_resolver
) -> None:
    """A registry containing only the ``custom`` escape hatch passes."""
    registry = {CUSTOM_LENS_NAME: _custom_lens()}
    assert (
        validate_all(
            registry,
            recipe_checker=accepting_recipe_checker,
            file_resolver=accepting_file_resolver,
        )
        == []
    )


# ---------------------------------------------------------------------------
# Happy path -- 7 fully-populated entries + custom escape hatch all pass
# ---------------------------------------------------------------------------


def test_seven_populated_plus_custom_all_pass(
    accepting_recipe_checker, accepting_file_resolver, accepting_strategy_checker
) -> None:
    """Synthesised 8-entry registry: 7 fully-populated + custom => 0 failures.

    This is the U-008 success contract: ``validate-lenses`` exits 0 when
    every non-custom entry passes its six COMP-023 / FR-LENSREG.NS
    assertions and the ``custom`` escape hatch is skipped without
    inspection.
    """
    entries = {
        "bare-review": _passing_lens(name="bare-review", suspect=True),
        "refactor-find": _passing_lens(
            name="refactor-find",
            suspect=False,
            recommended_next_command_template="sc:next on {job_id}",
        ),
        "edge-case-hunt": _passing_lens(
            name="edge-case-hunt",
            suspect=False,
            recommended_next_command_template="sc:next on {job_id}",
        ),
        "spec-completeness": _passing_lens(
            name="spec-completeness",
            suspect=False,
            recommended_next_command_template="sc:next on {job_id}",
        ),
        "feasibility-probe": _passing_lens(
            name="feasibility-probe",
            suspect=False,
            recommended_next_command_template="sc:next on {job_id}",
        ),
        "troubleshoot-hypothesis": _passing_lens(
            name="troubleshoot-hypothesis",
            suspect=True,
        ),
        "doc-completeness": _passing_lens(
            name="doc-completeness",
            suspect=False,
            recommended_next_command_template="sc:next on {job_id}",
        ),
        CUSTOM_LENS_NAME: _custom_lens(),
    }
    failures = validate_all(
        entries,
        recipe_checker=accepting_recipe_checker,
        file_resolver=accepting_file_resolver,
        strategy_checker=accepting_strategy_checker,
    )
    assert failures == []


# ---------------------------------------------------------------------------
# Each of the 5 assertions surfaces via validate_all
# ---------------------------------------------------------------------------


def test_assertion_1_file_ref_surfaces(
    accepting_recipe_checker, accepting_file_resolver
) -> None:
    """Empty ``output_template_path`` => RULE_FILE_REF_UNRESOLVED."""
    registry = {
        "bare-review": _passing_lens(name="bare-review", output_template_path=""),
    }
    failures = validate_all(
        registry,
        recipe_checker=accepting_recipe_checker,
        file_resolver=accepting_file_resolver,
    )
    assert len(failures) == 1
    assert failures[0].rule == RULE_FILE_REF_UNRESOLVED
    assert failures[0].lens_name == "bare-review"


def test_assertion_2_recipe_surfaces(
    accepting_file_resolver, rejecting_recipe_checker
) -> None:
    """Unknown ``recipe_name`` => RULE_RECIPE_UNREGISTERED."""
    registry = {
        "bare-review": _passing_lens(name="bare-review"),
    }
    failures = validate_all(
        registry,
        recipe_checker=rejecting_recipe_checker,
        file_resolver=accepting_file_resolver,
    )
    assert len(failures) == 1
    assert failures[0].rule == RULE_RECIPE_UNREGISTERED


def test_assertion_3_suspect_coupling_surfaces(
    accepting_recipe_checker, accepting_file_resolver
) -> None:
    """``suspect=True`` without ``{suspect_files}`` => RULE_SUSPECT_COUPLING."""
    registry = {
        "bare-review": _passing_lens(
            name="bare-review",
            suspect=True,
            recommended_next_command_template="sc:reflect on {job_id}",
        ),
    }
    failures = validate_all(
        registry,
        recipe_checker=accepting_recipe_checker,
        file_resolver=accepting_file_resolver,
    )
    assert len(failures) == 1
    assert failures[0].rule == RULE_SUSPECT_COUPLING


def test_assertion_4_name_uniqueness_surfaces(
    accepting_recipe_checker, accepting_file_resolver
) -> None:
    """Two entries declaring the same ``name`` => RULE_NAME_DUPLICATE on both.

    Two distinct dict keys both carry ``entry.name == 'bare-review'``.
    ``validate_all`` derives ``other_names`` from the *other* entry's
    ``name`` attribute, so each entry sees the duplicate in its own
    ``other_names`` list and assertion 4 fires for both.
    """
    registry = {
        "bare-review": _passing_lens(name="bare-review"),
        "alias-of-bare-review": _passing_lens(name="bare-review"),
    }
    failures = validate_all(
        registry,
        recipe_checker=accepting_recipe_checker,
        file_resolver=accepting_file_resolver,
    )
    assert len(failures) == 2
    assert all(f.rule == RULE_NAME_DUPLICATE for f in failures)
    assert all(f.lens_name == "bare-review" for f in failures)


def test_assertion_5_injection_substring_surfaces(
    accepting_recipe_checker, accepting_file_resolver
) -> None:
    """Missing §11.5 substring => RULE_INJECTION_SUBSTRING."""
    registry = {
        "bare-review": _passing_lens(
            name="bare-review",
            system_prompt_fragment="Review carefully. (no guard sentinel)",
        ),
    }
    failures = validate_all(
        registry,
        recipe_checker=accepting_recipe_checker,
        file_resolver=accepting_file_resolver,
    )
    assert len(failures) == 1
    assert failures[0].rule == RULE_INJECTION_SUBSTRING


# ---------------------------------------------------------------------------
# Fail-fast per-entry semantics + lens_name + iteration order
# ---------------------------------------------------------------------------


def test_per_entry_fail_fast_returns_first_assertion_only(
    accepting_file_resolver,
) -> None:
    """A single entry violating multiple assertions surfaces only the first."""
    registry = {
        "bare-review": _passing_lens(
            name="bare-review",
            output_template_path="",  # assertion 1 fails
            recipe_name="",  # would also fail assertion 2
            system_prompt_fragment="no guard sentence",  # would also fail 5
        ),
    }
    failures = validate_all(
        registry,
        recipe_checker=lambda name: False,
        file_resolver=accepting_file_resolver,
    )
    assert len(failures) == 1
    assert failures[0].rule == RULE_FILE_REF_UNRESOLVED


def test_multiple_failing_entries_each_get_one_failure(
    accepting_file_resolver, accepting_strategy_checker
) -> None:
    """One failure per failing entry; passing entries do not appear."""
    registry = {
        "bare-review": _passing_lens(name="bare-review"),  # PASS
        "refactor-find": _passing_lens(  # FAIL on assertion 1
            name="refactor-find",
            output_template_path="",
        ),
        "edge-case-hunt": _passing_lens(  # FAIL on assertion 2
            name="edge-case-hunt",
            recipe_name="",
        ),
    }
    failures = validate_all(
        registry,
        recipe_checker=lambda name: bool(name),
        file_resolver=accepting_file_resolver,
        strategy_checker=accepting_strategy_checker,
    )
    assert len(failures) == 2
    by_name = {f.lens_name: f.rule for f in failures}
    assert by_name["refactor-find"] == RULE_FILE_REF_UNRESOLVED
    assert by_name["edge-case-hunt"] == RULE_RECIPE_UNREGISTERED


def test_failures_preserve_registry_iteration_order(
    accepting_file_resolver,
) -> None:
    """Failures appear in the dict-insertion order of the registry."""
    registry = {
        "first": _passing_lens(name="first", output_template_path=""),
        "second": _passing_lens(name="second", output_template_path=""),
        "third": _passing_lens(name="third", output_template_path=""),
    }
    failures = validate_all(
        registry,
        recipe_checker=lambda name: True,
        file_resolver=accepting_file_resolver,
    )
    assert [f.lens_name for f in failures] == ["first", "second", "third"]


def test_failure_carries_lens_name_for_diagnostics(
    accepting_recipe_checker, accepting_file_resolver
) -> None:
    """The AC "failure surfaces first failing assertion + entry name"."""
    registry = {
        "edge-case-hunt": _passing_lens(
            name="edge-case-hunt",
            system_prompt_fragment="no guard",
        ),
    }
    failures = validate_all(
        registry,
        recipe_checker=accepting_recipe_checker,
        file_resolver=accepting_file_resolver,
    )
    assert len(failures) == 1
    assert isinstance(failures[0], LensValidationFailure)
    assert failures[0].lens_name == "edge-case-hunt"
    assert failures[0].rule == RULE_INJECTION_SUBSTRING


# ---------------------------------------------------------------------------
# Custom-lens escape hatch
# ---------------------------------------------------------------------------


def test_custom_lens_is_skipped_in_mixed_registry(
    accepting_recipe_checker, accepting_file_resolver, accepting_strategy_checker
) -> None:
    """A bogus ``custom`` entry surrounded by valid entries is skipped.

    Mutation: were the validator to inspect ``custom``, the empty
    ``output_template_path`` here would surface :data:`RULE_FILE_REF_UNRESOLVED`.
    The test confirms that does NOT happen.
    """
    registry = {
        "bare-review": _passing_lens(name="bare-review"),
        CUSTOM_LENS_NAME: LensEntry(
            name=CUSTOM_LENS_NAME,
            output_template_path="",  # would fail assertion 1 if inspected
            recipe_name="",  # would fail assertion 2 if inspected
            system_prompt_fragment="no guard",  # would fail assertion 5
        ),
    }
    failures = validate_all(
        registry,
        recipe_checker=accepting_recipe_checker,
        file_resolver=accepting_file_resolver,
        strategy_checker=accepting_strategy_checker,
    )
    assert failures == []


def test_skip_is_keyed_on_entry_name_not_dict_key(
    accepting_recipe_checker, accepting_file_resolver
) -> None:
    """The custom-skip predicate is ``entry.name == CUSTOM_LENS_NAME``, not the dict key.

    A registry that keys an entry under a non-custom dict key but
    declares ``entry.name == 'custom'`` must still be skipped, and a
    registry that keys an entry under the dict key ``'custom'`` but
    declares a different ``entry.name`` must still be validated. This
    pins the contract documented in :func:`validate_lens` and prevents
    a future regression that switches the skip predicate to the dict key.
    """
    # Case 1: non-custom dict key, custom entry.name → skipped.
    registry1 = {
        "shadow-custom": LensEntry(name=CUSTOM_LENS_NAME),  # would fail if inspected
    }
    assert (
        validate_all(
            registry1,
            recipe_checker=accepting_recipe_checker,
            file_resolver=accepting_file_resolver,
        )
        == []
    )

    # Case 2: custom dict key, non-custom entry.name → validated and fails.
    registry2 = {
        CUSTOM_LENS_NAME: LensEntry(name="actually-not-custom"),
    }
    failures = validate_all(
        registry2,
        recipe_checker=accepting_recipe_checker,
        file_resolver=accepting_file_resolver,
    )
    assert len(failures) == 1
    assert failures[0].lens_name == "actually-not-custom"


# ---------------------------------------------------------------------------
# Default-argument pluggability mirrors validate_lens
# ---------------------------------------------------------------------------


def test_defaults_invoke_module_level_helpers(monkeypatch) -> None:
    """Calling ``validate_all`` without overrides uses the module defaults.

    Mutation-style guard: replacing the module defaults via monkeypatch
    is observable through ``validate_all``'s output. The test confirms
    that the defaults are wired through and not hardcoded.
    """
    from superclaude.cli.swarm.lenses import _validate as mod

    calls: list[str] = []

    def fake_recipe_checker(name: str) -> bool:
        calls.append(f"recipe:{name}")
        return True

    def fake_file_resolver(path: str) -> bool:
        calls.append(f"file:{path}")
        return True

    def fake_strategy_checker(strategy: str) -> bool:
        calls.append(f"strategy:{strategy}")
        return True

    monkeypatch.setattr(mod, "default_recipe_checker", fake_recipe_checker)
    monkeypatch.setattr(mod, "default_file_resolver", fake_file_resolver)
    monkeypatch.setattr(mod, "default_strategy_checker", fake_strategy_checker)

    registry = {"bare-review": _passing_lens(name="bare-review")}
    failures = validate_all(registry)
    assert failures == []
    assert any(c.startswith("recipe:") for c in calls)
    assert any(c.startswith("file:") for c in calls)
    assert any(c.startswith("strategy:") for c in calls)


def test_required_substring_override_is_honored(
    accepting_recipe_checker, accepting_file_resolver, accepting_strategy_checker
) -> None:
    """Custom substring is checked instead of the canonical sentence."""
    registry = {
        "bare-review": _passing_lens(
            name="bare-review",
            system_prompt_fragment="frame target with GUARD-SENTINEL.",
        ),
    }
    # With the override matching, no failures.
    assert (
        validate_all(
            registry,
            recipe_checker=accepting_recipe_checker,
            file_resolver=accepting_file_resolver,
            strategy_checker=accepting_strategy_checker,
            required_substring="GUARD-SENTINEL",
        )
        == []
    )
    # With a different override, assertion 5 fires.
    failures = validate_all(
        registry,
        recipe_checker=accepting_recipe_checker,
        file_resolver=accepting_file_resolver,
        strategy_checker=accepting_strategy_checker,
        required_substring="OTHER-SENTINEL",
    )
    assert len(failures) == 1
    assert failures[0].rule == RULE_INJECTION_SUBSTRING


# ---------------------------------------------------------------------------
# Bundled LENSES registry smoke -- iteration + custom-skip on placeholders
# ---------------------------------------------------------------------------


def test_bundled_registry_iterates_eight_non_custom_entries(
    accepting_recipe_checker, accepting_file_resolver
) -> None:
    """Against the bundled :data:`LENSES`, validate_all visits 8 non-custom
    entries and skips ``custom`` -- confirmed by counting failures with a
    file-resolver that rejects every path.

    The bundled registry today carries placeholder bodies
    (``cli/swarm/lenses/__init__.py``); T02.23 replaces the placeholders
    with populated entries and T02.17 ratifies the "7 of 8 pass" gate.
    This test pins the iteration shape and custom-skip behavior
    independent of that population transition: a rejecting file resolver
    surfaces exactly one ``RULE_FILE_REF_UNRESOLVED`` per non-custom
    entry, no matter what their (placeholder vs populated) bodies look
    like for the remaining four assertions.
    """
    failures = validate_all(
        LENSES,
        recipe_checker=accepting_recipe_checker,
        file_resolver=lambda path: False,
    )
    # Exactly 8 non-custom entries → 8 failures.
    assert len(failures) == 8
    # No failure carries lens_name == 'custom'.
    assert all(f.lens_name != CUSTOM_LENS_NAME for f in failures)
    # Failure lens_names match the 8 non-custom LENS_NAMES.
    non_custom_names = [n for n in LENS_NAMES if n != CUSTOM_LENS_NAME]
    assert [f.lens_name for f in failures] == non_custom_names
    # First failing assertion is the file-ref one in every case.
    assert all(f.rule == RULE_FILE_REF_UNRESOLVED for f in failures)


def test_bundled_registry_returns_list_type() -> None:
    """``validate_all`` returns a ``list`` -- the U-008 surface is list-shaped."""
    out = validate_all(LENSES, file_resolver=lambda p: False, recipe_checker=lambda n: True)
    assert isinstance(out, list)
