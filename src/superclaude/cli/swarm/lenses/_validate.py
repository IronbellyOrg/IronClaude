"""Lens validator (COMP-023 / T02.15 + FR-LENSREG.NS / T02.21) -- 6-assertion lens-entry check.

This module is the COMP-023 lens validator landed by T02.15 and extended
by T02.21 with the FR-LENSREG.NS sixth assertion. It checks a single
:class:`LensEntry` (or, via T02.16's ``validate_all``, every entry in
:data:`superclaude.cli.swarm.lenses.LENSES`) against six cross-field
assertions drawn verbatim from the roadmap COMP-023 row plus
anti-instinct remediation row 17a::

    1. File refs resolve            -- ``output_template_path`` is a
       non-empty path and the referenced file is readable.
    2. Recipe registered            -- ``recipe_name`` is non-empty and
       resolves against the recipe registry (default: introspection of
       :mod:`superclaude.cli.swarm.recipes`).
    3. Suspect ↔ suspect_files      -- when ``suspect=True``, the
       ``recommended_next_command_template`` must contain the
       ``{suspect_files}`` placeholder so the downstream skill driver
       can substitute the suspect-file list. When ``suspect=False`` the
       placeholder is not allowed (would dangle at substitution time).
    4. Name uniqueness              -- the entry's ``name`` does not
       collide with any other entry's ``name`` in the registry. Checked
       only when a registry context is supplied via ``other_names``.
    5. §11.5 substring              -- ``system_prompt_fragment``
       contains :data:`schema.CANONICAL_INJECTION_GUARD_SENTENCE` (or
       the caller's override) so workers see the injection-guard frame
       on the lens path identically to the JSON-Schema and
       ``--custom-prompt-dir`` paths (INV-003 / INV-014 parity).
    6. Normalizer-strategy          -- ``normalizer_strategy`` is
       non-empty and resolves against a registered Recipe
       (FR-LENSREG.NS / T02.21). Strategy lookup defaults to consulting
       ``recipes.STRATEGIES`` / ``REGISTRY`` / ``__all__`` -- the same
       surfaces assertion 2 uses for ``recipe_name``.

The validator **fails fast on first violation**: :func:`validate_lens`
returns the first :class:`LensValidationFailure` it produces and skips
remaining assertions for that entry. Callers that want the full list
across a registry use :func:`validate_all` (T02.16) which collects one
failure per entry.

The ``custom`` lens (COMP-026 escape hatch) is intentionally exempt --
its prompt body flows in from ``--custom-prompt-dir`` at preflight per
FR-021 / INV-003 and is validated on the escape-hatch path (T02.05 /
T02.07). :func:`validate_lens` short-circuits to ``None`` when invoked
on the ``custom`` entry so callers do not need to special-case the
skip themselves.

Pluggability:
    Each external dependency (recipe registry, filesystem) is injectable
    via a callable. Tests pass stub callables to exercise individual
    assertions without touching disk or the real recipe module; the M2
    runtime call sites (``swarm validate-lenses`` per T02.20) consume
    the module-level defaults.

Diagnostic shape:
    :class:`LensValidationFailure` mirrors
    :class:`schema.SchemaValidationFailure` and
    :class:`preflight.PreflightFailure` -- stable ``rule`` identifier,
    dotted ``path``, human-readable ``message``, plus the offending
    ``lens_name``. Tests assert on the rule identifier (not on message
    phrasing) so future copy edits don't break the suite.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, List, Mapping, Optional

from superclaude.cli.swarm.models import LensEntry
from superclaude.cli.swarm.schema import (
    CANONICAL_INJECTION_GUARD_SENTENCE,
    contains_required_substring,
)


__all__ = [
    "CUSTOM_LENS_NAME",
    "LensValidationFailure",
    "RULE_FILE_REF_UNRESOLVED",
    "RULE_INJECTION_SUBSTRING",
    "RULE_NAME_DUPLICATE",
    "RULE_NORMALIZER_STRATEGY",
    "RULE_RECIPE_UNREGISTERED",
    "RULE_SUSPECT_COUPLING",
    "SUSPECT_FILES_PLACEHOLDER",
    "default_file_resolver",
    "default_recipe_checker",
    "default_strategy_checker",
    "validate_all",
    "validate_lens",
]


# ---------------------------------------------------------------------------
# Constants -- rule identifiers and well-known tokens
# ---------------------------------------------------------------------------


CUSTOM_LENS_NAME: str = "custom"
"""Name of the COMP-026 escape-hatch lens that is exempt from validation.

Kept as a local constant rather than importing
:data:`schema.CUSTOM_LENS_NAME` to keep the validator's dependency graph
minimal and to document the contract at this layer: the validator skips
this single name. The two constants must stay in sync; the regression
test ``test_lens_validator.test_custom_lens_skipped`` pins the
behavior.
"""


SUSPECT_FILES_PLACEHOLDER: str = "{suspect_files}"
"""Placeholder token expected in next-command templates when ``suspect=True``.

Substituted at downstream skill-driver time with the suspect-file list
(see T02.23 ``bare_review`` ``recommended_next_command_template``). The
suspect-coupling assertion checks for the literal token; mutation of
this constant breaks the test in lockstep with the validator so the
contract stays single-source.
"""


RULE_FILE_REF_UNRESOLVED: str = "lens.file_ref_unresolved"
"""Assertion 1 -- ``output_template_path`` empty or not readable on disk."""

RULE_RECIPE_UNREGISTERED: str = "lens.recipe_unregistered"
"""Assertion 2 -- ``recipe_name`` empty or unknown to the recipe registry."""

RULE_SUSPECT_COUPLING: str = "lens.suspect_files_coupling"
"""Assertion 3 -- ``suspect`` <-> ``{suspect_files}`` placeholder mismatch."""

RULE_NAME_DUPLICATE: str = "lens.name_duplicate"
"""Assertion 4 -- ``name`` collides with another entry in the registry."""

RULE_INJECTION_SUBSTRING: str = "lens.injection_substring_missing"
"""Assertion 5 -- §11.5 required substring missing from ``system_prompt_fragment``."""

RULE_NORMALIZER_STRATEGY: str = "lens.normalizer_strategy_unmatched"
"""Assertion 6 -- ``normalizer_strategy`` empty or unmatched against a registered recipe.

Anti-instinct remediation row 17a (FR-LENSREG.NS / T02.21) adds this
sixth contract assertion. The roadmap text reads "Each ``LENSES`` entry
declares ``normalizer_strategy`` matching the prompt's expected output
shape; validator asserts a registered Recipe matches the strategy". The
rule identifier is namespaced under ``lens.`` to parallel the prior five
assertions; tests assert on the identifier so message phrasing can
evolve.
"""


# ---------------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LensValidationFailure:
    """One structured rejection reason from the COMP-023 lens validator.

    Fields:
        rule       -- a stable identifier from the ``RULE_*`` constants
                      above. Tests assert on this identifier (not on
                      ``message``) so phrasing can evolve.
        path       -- dotted path to the offending field on the
                      :class:`LensEntry` (e.g.
                      ``"output_template_path"``,
                      ``"system_prompt_fragment"``). Empty for
                      whole-entry rejections.
        message    -- human-readable summary suitable for the
                      ``swarm validate-lenses`` CLI surface.
        lens_name  -- the ``LensEntry.name`` of the failing entry, so a
                      mixed-list failure trace identifies which entry
                      surfaced each rule.
    """

    rule: str
    path: str
    message: str
    lens_name: str


# ---------------------------------------------------------------------------
# Pluggable dependencies -- recipe registry + filesystem
# ---------------------------------------------------------------------------


RecipeChecker = Callable[[str], bool]
"""Predicate: does this recipe name resolve in the recipe registry?"""


StrategyChecker = Callable[[str], bool]
"""Predicate: does this normalizer_strategy resolve to a registered recipe?

FR-LENSREG.NS / T02.21. Kept as a distinct alias from :data:`RecipeChecker`
so the M4 recipe runtime can swap in a strategy-aware lookup (e.g. one
that scans recipes for their declared output-shape attribute) without
forcing every caller of :func:`validate_lens` to switch predicates.
"""


FileResolver = Callable[[str], bool]
"""Predicate: does this path resolve to a readable file on disk?"""


def default_recipe_checker(name: str) -> bool:
    """Default recipe-registry lookup -- introspects :mod:`recipes`.

    The recipe runtime lands in M4 (DM-006 dispatch + ``on_parse_error``
    salvage / retain_raw policies); until then
    :mod:`superclaude.cli.swarm.recipes` carries only the module
    docstring and an empty ``__all__``. This default checker consults,
    in order:

        1. ``recipes.REGISTRY`` if it exists and is a ``dict`` -- M4
           recipe runtime's expected surface (the dict maps
           ``recipe_name`` to a recipe callable / class).
        2. ``recipes.__all__`` -- a fallback for the M2/M3 interim where
           recipes register themselves only by exporting from the
           package init.

    Returns ``False`` for any name not present in either surface; tests
    that need a specific recipe to "be registered" inject a stub via
    the ``recipe_checker`` parameter of :func:`validate_lens` rather
    than mutating the recipes module.
    """
    if not name:
        return False
    try:
        from superclaude.cli.swarm import recipes  # noqa: PLC0415
    except ImportError:
        return False
    registry = getattr(recipes, "REGISTRY", None)
    if isinstance(registry, dict):
        return name in registry
    all_names = getattr(recipes, "__all__", None)
    if isinstance(all_names, (list, tuple)):
        return name in all_names
    return False


def default_strategy_checker(strategy: str) -> bool:
    """Default ``normalizer_strategy`` lookup -- introspects :mod:`recipes`.

    FR-LENSREG.NS / T02.21. The strategy names the prompt's expected
    output shape; a registered recipe must produce that shape for the
    lens to be acceptable. Until the M4 recipe runtime lands, the
    recipes module carries only a docstring and an empty ``__all__``;
    this default checker consults, in order:

        1. ``recipes.STRATEGIES`` if it exists -- the explicit
           strategy registry surface the M4 recipe runtime is expected
           to expose (set / frozenset / list / tuple of strategy names,
           or a dict whose keys are strategy names mapping to recipe
           identifiers).
        2. ``recipes.REGISTRY`` if it exists -- if a recipe object
           declares a ``strategy`` attribute, a match on that attribute
           also resolves the strategy. Treats ``REGISTRY`` keys as
           strategy candidates too, so an M4 runtime that keys the
           registry on strategy names rather than recipe names still
           works.
        3. ``recipes.__all__`` -- a final fallback for the M2/M3 interim
           where recipes register themselves only by exporting from the
           package init. Same surface :func:`default_recipe_checker`
           uses.

    Returns ``False`` for any name not present in either surface; tests
    that need a specific strategy to "be registered" inject a stub via
    the ``strategy_checker`` parameter of :func:`validate_lens` rather
    than mutating the recipes module.
    """
    if not strategy:
        return False
    try:
        from superclaude.cli.swarm import recipes  # noqa: PLC0415
    except ImportError:
        return False
    strategies = getattr(recipes, "STRATEGIES", None)
    if isinstance(strategies, dict):
        return strategy in strategies
    if isinstance(strategies, (set, frozenset, list, tuple)):
        return strategy in strategies
    registry = getattr(recipes, "REGISTRY", None)
    if isinstance(registry, dict):
        if strategy in registry:
            return True
        for recipe in registry.values():
            if getattr(recipe, "strategy", None) == strategy:
                return True
    all_names = getattr(recipes, "__all__", None)
    if isinstance(all_names, (list, tuple)):
        return strategy in all_names
    return False


def default_file_resolver(path: str) -> bool:
    """Default file-existence check -- :meth:`pathlib.Path.is_file`.

    Returns ``True`` only when ``path`` is a non-empty string that
    resolves to an existing regular file. Symlinks are resolved through
    by :meth:`Path.is_file` so a templates directory that ships its
    files as symlinks (e.g. ``.claude/`` mirror layout) passes
    transparently.

    Empty / whitespace-only paths return ``False`` -- the assertion 1
    check then surfaces ``RULE_FILE_REF_UNRESOLVED`` rather than letting
    the empty path propagate downstream.
    """
    if not path or not path.strip():
        return False
    try:
        return Path(path).is_file()
    except OSError:
        return False


# ---------------------------------------------------------------------------
# Individual assertion helpers -- each tested in isolation per T02.15 AC
# ---------------------------------------------------------------------------


def _check_file_refs(
    entry: LensEntry, file_resolver: FileResolver
) -> Optional[LensValidationFailure]:
    """Assertion 1 -- ``output_template_path`` resolves to a readable file.

    The path must be non-empty (an empty string is rejected before
    delegating to ``file_resolver`` so the diagnostic message is
    specific) and the resolver must return ``True``. Failure carries
    :data:`RULE_FILE_REF_UNRESOLVED` and points the dotted path at
    ``output_template_path`` so callers can surface a precise field.
    """
    path = entry.output_template_path
    if not path:
        return LensValidationFailure(
            rule=RULE_FILE_REF_UNRESOLVED,
            path="output_template_path",
            message=(
                f"Lens {entry.name!r}: output_template_path is empty -- "
                "every non-custom lens must declare a readable template "
                "path (COMP-023 file-ref assertion)."
            ),
            lens_name=entry.name,
        )
    if not file_resolver(path):
        return LensValidationFailure(
            rule=RULE_FILE_REF_UNRESOLVED,
            path="output_template_path",
            message=(
                f"Lens {entry.name!r}: output_template_path "
                f"{path!r} does not resolve to a readable file "
                "(COMP-023 file-ref assertion)."
            ),
            lens_name=entry.name,
        )
    return None


def _check_recipe_registered(
    entry: LensEntry, recipe_checker: RecipeChecker
) -> Optional[LensValidationFailure]:
    """Assertion 2 -- ``recipe_name`` is non-empty and registered.

    Empty ``recipe_name`` is rejected with a distinct message so the
    "you forgot to set the recipe" branch is obvious in the CLI output.
    Otherwise the pluggable ``recipe_checker`` decides; the default
    (:func:`default_recipe_checker`) consults the recipes module's
    ``REGISTRY`` or ``__all__``.
    """
    recipe_name = entry.recipe_name
    if not recipe_name:
        return LensValidationFailure(
            rule=RULE_RECIPE_UNREGISTERED,
            path="recipe_name",
            message=(
                f"Lens {entry.name!r}: recipe_name is empty -- every "
                "non-custom lens must bind to a registered recipe "
                "(COMP-023 recipe assertion)."
            ),
            lens_name=entry.name,
        )
    if not recipe_checker(recipe_name):
        return LensValidationFailure(
            rule=RULE_RECIPE_UNREGISTERED,
            path="recipe_name",
            message=(
                f"Lens {entry.name!r}: recipe_name {recipe_name!r} is "
                "not registered in the recipe registry "
                "(COMP-023 recipe assertion)."
            ),
            lens_name=entry.name,
        )
    return None


def _check_suspect_coupling(
    entry: LensEntry,
) -> Optional[LensValidationFailure]:
    """Assertion 3 -- ``suspect`` <-> ``{suspect_files}`` placeholder.

    Bidirectional: ``suspect=True`` requires the placeholder so the
    downstream skill driver can substitute the suspect-file list;
    ``suspect=False`` forbids the placeholder so it does not dangle at
    substitution time with no value to inject.
    """
    template = entry.recommended_next_command_template
    has_placeholder = SUSPECT_FILES_PLACEHOLDER in template
    if entry.suspect and not has_placeholder:
        return LensValidationFailure(
            rule=RULE_SUSPECT_COUPLING,
            path="recommended_next_command_template",
            message=(
                f"Lens {entry.name!r}: suspect=True but "
                "recommended_next_command_template is missing the "
                f"{SUSPECT_FILES_PLACEHOLDER!r} placeholder "
                "(COMP-023 suspect-coupling assertion)."
            ),
            lens_name=entry.name,
        )
    if not entry.suspect and has_placeholder:
        return LensValidationFailure(
            rule=RULE_SUSPECT_COUPLING,
            path="recommended_next_command_template",
            message=(
                f"Lens {entry.name!r}: suspect=False but "
                "recommended_next_command_template contains the "
                f"{SUSPECT_FILES_PLACEHOLDER!r} placeholder -- "
                "the placeholder would dangle with no value to "
                "substitute (COMP-023 suspect-coupling assertion)."
            ),
            lens_name=entry.name,
        )
    return None


def _check_name_unique(
    entry: LensEntry, other_names: Iterable[str]
) -> Optional[LensValidationFailure]:
    """Assertion 4 -- ``entry.name`` does not collide with ``other_names``.

    ``other_names`` is the set of other lens names in the registry
    context. When the validator runs standalone (no registry passed),
    the caller supplies an empty iterable and this assertion is a
    no-op. :func:`validate_all` (T02.16) builds the set from the
    registry's keys minus the current entry's name.
    """
    if entry.name in set(other_names):
        return LensValidationFailure(
            rule=RULE_NAME_DUPLICATE,
            path="name",
            message=(
                f"Lens {entry.name!r}: name collides with another "
                "registered lens entry -- names must be unique "
                "(COMP-023 name-uniqueness assertion)."
            ),
            lens_name=entry.name,
        )
    return None


def _check_injection_substring(
    entry: LensEntry, required_substring: str
) -> Optional[LensValidationFailure]:
    """Assertion 5 -- §11.5 required substring in ``system_prompt_fragment``.

    Delegates to :func:`schema.contains_required_substring` so the
    lens path uses the **same** predicate as the JSON-Schema and
    ``--custom-prompt-dir`` paths. A mutation of that predicate
    changes the verdict on every path together; that is the
    INV-003 / INV-014 parity property.

    Empty ``required_substring`` is treated as "guard disabled" by
    :func:`schema.contains_required_substring` and short-circuits to
    ``True`` -- the validator does not second-guess a caller that
    explicitly opted out (parity with the schema layer's behavior).
    """
    if not contains_required_substring(
        entry.system_prompt_fragment, required_substring
    ):
        return LensValidationFailure(
            rule=RULE_INJECTION_SUBSTRING,
            path="system_prompt_fragment",
            message=(
                f"Lens {entry.name!r}: system_prompt_fragment does "
                f"not contain the §11.5 required substring "
                f"{required_substring!r} -- every non-custom lens "
                "must frame its prompt with the injection guard "
                "(COMP-023 §11.5 substring assertion)."
            ),
            lens_name=entry.name,
        )
    return None


def _check_normalizer_strategy(
    entry: LensEntry, strategy_checker: StrategyChecker
) -> Optional[LensValidationFailure]:
    """Assertion 6 -- ``normalizer_strategy`` resolves against a recipe.

    FR-LENSREG.NS / T02.21. The strategy declares the output shape the
    prompt expects; the validator asserts a registered Recipe matches
    the strategy. Empty ``normalizer_strategy`` is rejected with a
    dedicated message so the "you forgot to set the strategy" branch is
    obvious in the ``swarm validate-lenses`` CLI output. Otherwise the
    pluggable ``strategy_checker`` decides; the default
    (:func:`default_strategy_checker`) consults the recipes module's
    ``STRATEGIES`` / ``REGISTRY`` / ``__all__`` surfaces in order.
    """
    strategy = entry.normalizer_strategy
    if not strategy:
        return LensValidationFailure(
            rule=RULE_NORMALIZER_STRATEGY,
            path="normalizer_strategy",
            message=(
                f"Lens {entry.name!r}: normalizer_strategy is empty -- "
                "every non-custom lens must declare a normalizer_strategy "
                "that matches the prompt's expected output shape "
                "(COMP-023 / FR-LENSREG.NS strategy assertion)."
            ),
            lens_name=entry.name,
        )
    if not strategy_checker(strategy):
        return LensValidationFailure(
            rule=RULE_NORMALIZER_STRATEGY,
            path="normalizer_strategy",
            message=(
                f"Lens {entry.name!r}: normalizer_strategy {strategy!r} "
                "does not resolve against any registered recipe -- "
                "validator asserts a registered Recipe matches the "
                "strategy (COMP-023 / FR-LENSREG.NS strategy assertion)."
            ),
            lens_name=entry.name,
        )
    return None


# ---------------------------------------------------------------------------
# Public entry point -- fail-fast single-entry validator
# ---------------------------------------------------------------------------


def validate_lens(
    entry: LensEntry,
    *,
    recipe_checker: Optional[RecipeChecker] = None,
    file_resolver: Optional[FileResolver] = None,
    strategy_checker: Optional[StrategyChecker] = None,
    other_names: Iterable[str] = (),
    required_substring: str = CANONICAL_INJECTION_GUARD_SENTENCE,
) -> Optional[LensValidationFailure]:
    """Run the six COMP-023 assertions against ``entry``.

    Returns the **first** :class:`LensValidationFailure` (fail-fast per
    the T02.15 acceptance criterion) or ``None`` when the entry is
    valid. The assertion order is the COMP-023 order extended by the
    FR-LENSREG.NS / T02.21 sixth assertion:

        1. file refs              -- ``output_template_path``
        2. recipe registered      -- ``recipe_name``
        3. suspect coupling       -- ``{suspect_files}`` placeholder
        4. name uniqueness        -- vs ``other_names``
        5. §11.5 substring        -- ``system_prompt_fragment``
        6. normalizer_strategy    -- strategy resolves to a registered
                                     recipe (FR-LENSREG.NS / T02.21)

    The ``custom`` lens (COMP-026 escape hatch) is exempt: invoking
    :func:`validate_lens` on an entry whose ``name`` equals
    :data:`CUSTOM_LENS_NAME` returns ``None`` without running any
    assertion. Its prompt content flows in from ``--custom-prompt-dir``
    at preflight (FR-021) and is validated on the escape-hatch path
    (T02.05 / T02.07) so duplicating the checks here would only invite
    drift.

    Pluggable dependencies:

        * ``recipe_checker`` -- predicate ``(name) -> bool``. Defaults
          to :func:`default_recipe_checker` (introspects the recipes
          module). Tests stub this to assert each branch without
          mutating the recipes registry.
        * ``file_resolver`` -- predicate ``(path) -> bool``. Defaults
          to :func:`default_file_resolver` (:meth:`pathlib.Path.is_file`).
          Tests stub this to avoid touching disk.
        * ``strategy_checker`` -- predicate ``(strategy) -> bool``.
          Defaults to :func:`default_strategy_checker` (introspects
          ``recipes.STRATEGIES`` / ``REGISTRY`` / ``__all__``). Tests
          stub this to assert the FR-LENSREG.NS branch in isolation.
        * ``other_names`` -- iterable of other lens names in the
          registry context, for the name-uniqueness assertion. Empty
          when validating a single entry standalone.
        * ``required_substring`` -- §11.5 substring to enforce.
          Defaults to :data:`schema.CANONICAL_INJECTION_GUARD_SENTENCE`
          so the lens path agrees with the JSON-Schema and
          ``--custom-prompt-dir`` paths byte-for-byte. Override only
          when a caller has explicitly configured a non-default guard.
    """
    if entry.name == CUSTOM_LENS_NAME:
        return None

    if recipe_checker is None:
        recipe_checker = default_recipe_checker
    if file_resolver is None:
        file_resolver = default_file_resolver
    if strategy_checker is None:
        strategy_checker = default_strategy_checker

    for check in (
        lambda e: _check_file_refs(e, file_resolver),
        lambda e: _check_recipe_registered(e, recipe_checker),
        _check_suspect_coupling,
        lambda e: _check_name_unique(e, other_names),
        lambda e: _check_injection_substring(e, required_substring),
        lambda e: _check_normalizer_strategy(e, strategy_checker),
    ):
        failure = check(entry)
        if failure is not None:
            return failure
    return None


# ---------------------------------------------------------------------------
# Registry-level entry point -- U-008 ``swarm validate-lenses`` driver
# ---------------------------------------------------------------------------


def validate_all(
    registry: Mapping[str, LensEntry],
    *,
    recipe_checker: Optional[RecipeChecker] = None,
    file_resolver: Optional[FileResolver] = None,
    strategy_checker: Optional[StrategyChecker] = None,
    required_substring: str = CANONICAL_INJECTION_GUARD_SENTENCE,
) -> List[LensValidationFailure]:
    """Run the five COMP-023 assertions against every entry in ``registry``.

    Iterates the registry in dict-insertion order and applies
    :func:`validate_lens` to each entry, collecting one
    :class:`LensValidationFailure` per failing entry (the first-failing
    assertion -- :func:`validate_lens` is itself fail-fast). Returns an
    empty list when every non-custom entry passes.

    Name-uniqueness assertion (assertion 4) is wired registry-wide here:
    for each entry, ``other_names`` is built from the ``name`` attribute
    of every *other* entry in the registry (not the dict keys, since the
    contract is "no two entries declare the same ``LensEntry.name``" --
    dict keys are unique by definition). A registry with two entries
    keyed differently but sharing the same ``entry.name`` therefore
    surfaces :data:`RULE_NAME_DUPLICATE` on both, one failure per entry.

    Custom-lens escape hatch:
        The entry whose ``name`` equals :data:`CUSTOM_LENS_NAME` is
        skipped without running any assertion -- its prompt body flows
        in from ``--custom-prompt-dir`` at preflight per FR-021 /
        INV-003 and is validated on the escape-hatch path
        (T02.05 / T02.07). The skip is per-entry, so a registry that
        ships only ``custom`` returns an empty failure list.

    Args:
        registry: Mapping from lens key to :class:`LensEntry`. Typical
            caller is :data:`superclaude.cli.swarm.lenses.LENSES`; tests
            inject synthesized fixtures to exercise specific branches.
        recipe_checker: Predicate forwarded to :func:`validate_lens`.
            Defaults to :func:`default_recipe_checker`.
        file_resolver: Predicate forwarded to :func:`validate_lens`.
            Defaults to :func:`default_file_resolver`.
        required_substring: §11.5 substring forwarded to
            :func:`validate_lens`. Defaults to
            :data:`schema.CANONICAL_INJECTION_GUARD_SENTENCE` so the
            ``swarm validate-lenses`` surface enforces the same guard
            byte-for-byte as the JSON-Schema and ``--custom-prompt-dir``
            paths.

    Returns:
        A list of :class:`LensValidationFailure` -- one per failing
        entry, in registry-iteration order. Empty when every non-custom
        entry passes. The U-008 CLI driver (T02.20 ``validate-lenses``)
        renders this list and exits non-zero when it is non-empty.
    """
    if recipe_checker is None:
        recipe_checker = default_recipe_checker
    if file_resolver is None:
        file_resolver = default_file_resolver
    if strategy_checker is None:
        strategy_checker = default_strategy_checker

    failures: List[LensValidationFailure] = []
    for key, entry in registry.items():
        if entry.name == CUSTOM_LENS_NAME:
            continue
        other_names = [
            other.name
            for other_key, other in registry.items()
            if other_key != key
        ]
        failure = validate_lens(
            entry,
            recipe_checker=recipe_checker,
            file_resolver=file_resolver,
            strategy_checker=strategy_checker,
            other_names=other_names,
            required_substring=required_substring,
        )
        if failure is not None:
            failures.append(failure)
    return failures
