"""T04.10 -- Recipe REGISTRY enumeration + validation (R-094 / FR-010 / D-0076).

T04.02 (``test_recipe_protocol.py``) pins the Protocol surface, the
``custom-py:`` loader semantics, and the set-equality + length checks
on REGISTRY. This suite is the dedicated **enumeration** gate per
T04.10's acceptance criteria:

    1. All six §3.3 recipes are resolvable by name from
       :data:`REGISTRY` (parametrized per-slot existence check).
    2. Each REGISTRY entry implements the :class:`Recipe` Protocol
       (parametrized per-slot ``isinstance(entry, Recipe)``).
    3. Each non-dispatcher entry round-trips a benign body to a
       :class:`NormalizedResult` (parametrized smoke invocation -- the
       "callable signature" half of AC).
    4. The ``custom`` slot loads dynamically when given a fixture
       ``custom-py:`` spec via :func:`load_custom_py`.
    5. :data:`STRATEGIES` mirrors REGISTRY slot-for-slot.
    6. ``len(REGISTRY) == 6`` is asserted as a hard contract (the
       T04.02 sibling asserts ``>= 6`` to keep open-class extension
       safe; T04.10 pins the **bundled** count at exactly six).

This suite intentionally does **not** re-test recipe content shape
(covered by ``test_recipe_<name>.py`` per recipe) or AC-011 neutrality
(covered by ``test_recipe_no_judging.py`` -- T04.14). The value-add
here is per-slot enumeration with parametrize so a single missing or
mis-registered recipe surfaces as a single failing parameter rather
than as a downstream dispatcher failure.
"""

from __future__ import annotations

import sys
import types
from typing import Any

import pytest

from superclaude.cli.swarm.recipes import (
    CUSTOM_PY_PREFIX,
    REGISTRY,
    STRATEGIES,
    CustomPyDispatcher,
    NormalizedResult,
    Recipe,
    load_custom_py,
)

# ---------------------------------------------------------------------------
# Expected REGISTRY enumeration (§3.3 / FR-LENSREG.NS).
# ---------------------------------------------------------------------------


EXPECTED_RECIPE_NAMES: tuple[str, ...] = (
    "bare-review-v1",
    "findings_table_v1",
    "hypothesis_table_v1",
    "verdict_only_v1",
    "passthrough",
    "custom",
)


NON_DISPATCHER_RECIPE_NAMES: tuple[str, ...] = tuple(
    name for name in EXPECTED_RECIPE_NAMES if name != "custom"
)


# Minimal args envelope accepted by every bundled recipe. The non-custom
# recipes consult ``status`` (parse_error salvage) plus the standard
# meta-sidecar fields (lens / tier / target / generated / etc.); the
# passthrough recipe ignores ``args`` entirely. This shape is what the
# Wave-2 dispatcher hands recipes in production -- keeping it here as a
# single source of truth lets the parametrized smoke test exercise every
# bundled recipe through one consistent surface.
def _benign_args(
    *, lens: str = "refactor-find", tier: str = "T2-code"
) -> dict[str, Any]:
    return {
        "status": "success",
        "lens": lens,
        "tier": tier,
        "suspect": False,
        "target": "/tmp/example/target.py",
        "target_checksum": "deadbeefcafe",
        "target_truncated": False,
        "model_id": "m",
        "model_label": "M",
        "caller_label": "",
        "elapsed_ms": 12345,
        "generated": "2026-06-01T11:19:39Z",
    }


# ---------------------------------------------------------------------------
# 1 -- Hard-pinned size (T04.10 AC: ``len(REGISTRY) == 6``)
# ---------------------------------------------------------------------------


def test_registry_size_is_exactly_six():
    """T04.10 AC: 'len(REGISTRY) == 6 asserted'."""
    assert len(REGISTRY) == 6


def test_strategies_size_is_exactly_six():
    assert len(STRATEGIES) == 6


def test_registry_keys_equal_expected_six_recipe_names():
    assert set(REGISTRY) == set(EXPECTED_RECIPE_NAMES)


def test_strategies_mirrors_registry_slot_for_slot():
    assert set(STRATEGIES) == set(REGISTRY)
    # Strategy names parallel recipe names today (N-to-1 mapping per
    # __init__.py docstring).
    for name in REGISTRY:
        assert STRATEGIES[name] == name


# ---------------------------------------------------------------------------
# 2 -- Per-slot resolvability (parametrized enumeration)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", EXPECTED_RECIPE_NAMES)
def test_recipe_resolvable_by_name(name: str):
    """T04.10 AC: 'All 6 recipes resolvable by name from REGISTRY'."""
    entry = REGISTRY[name]
    assert entry is not None, (
        f"REGISTRY[{name!r}] is None; the M2-era sentinel must be "
        "replaced by a concrete recipe before T04.10 can pass."
    )


# ---------------------------------------------------------------------------
# 3 -- Per-slot Protocol conformance (parametrized enumeration)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", EXPECTED_RECIPE_NAMES)
def test_recipe_implements_protocol(name: str):
    """T04.10 AC: 'Each entry implements Recipe Protocol (callable signature)'."""
    entry = REGISTRY[name]
    assert isinstance(entry, Recipe), (
        f"REGISTRY[{name!r}] (type {type(entry).__name__}) does not "
        "implement the Recipe Protocol -- missing or wrong-shaped "
        "normalize(raw_output, args) -> NormalizedResult method."
    )
    # Protocol membership implies the method exists; assert it's
    # callable for the same reason isinstance does -- belt + braces.
    assert callable(getattr(entry, "normalize", None))


# ---------------------------------------------------------------------------
# 4 -- Per-slot smoke invocation (parametrized enumeration)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", NON_DISPATCHER_RECIPE_NAMES)
def test_non_dispatcher_recipe_returns_normalized_result(name: str):
    """Smoke-invoke each bundled recipe on a benign body.

    The dispatcher entry (``custom``) is excluded -- it raises
    :class:`RuntimeError` by design when called directly (callers must
    go through :func:`load_custom_py`). That contract is exercised in
    :func:`test_custom_dispatcher_raises_when_called_directly` below.
    """
    entry = REGISTRY[name]
    raw_body = "# benign body\nhello world\n"
    result = entry.normalize(raw_body, _benign_args())
    assert isinstance(result, NormalizedResult), (
        f"{name} returned {type(result).__name__}, expected NormalizedResult"
    )
    # `text` and `salvaged` always populated; `error` is None on the
    # happy path for every bundled recipe.
    assert isinstance(result.text, str)
    assert isinstance(result.salvaged, bool)


# ---------------------------------------------------------------------------
# 5 -- Custom-py dispatcher slot + dynamic loading via fixture spec
# ---------------------------------------------------------------------------


class _FixtureRecipe:
    """In-test fixture conforming to the Recipe Protocol structurally."""

    def normalize(self, raw_output: str, args: dict[str, Any]) -> NormalizedResult:
        del args
        return NormalizedResult(text=f"fixture:{raw_output}")


def test_custom_slot_is_custom_py_dispatcher_instance():
    entry = REGISTRY["custom"]
    assert isinstance(entry, CustomPyDispatcher)
    assert isinstance(entry, Recipe)


def test_custom_dispatcher_raises_when_called_directly():
    """The dispatcher slot is a routing hint, not a usable recipe."""
    entry = REGISTRY["custom"]
    with pytest.raises(RuntimeError) as excinfo:
        entry.normalize("body", {})
    # The error directs callers to the dynamic loader.
    msg = str(excinfo.value)
    assert CUSTOM_PY_PREFIX in msg
    assert "load_custom_py" in msg


def test_custom_py_loader_resolves_fixture_recipe(monkeypatch):
    """T04.10 AC: 'Custom-py loads dynamically when given a fixture spec'.

    Install a synthetic module on ``sys.modules`` exposing a
    Recipe-conforming class, then resolve it through the dispatcher's
    public loader entry. The loader must return a Protocol-conforming
    object that produces a :class:`NormalizedResult` on invocation.
    """
    module_name = "superclaude_test_t04_10_registry_fixture"
    module = types.ModuleType(module_name)
    module.MyFixtureRecipe = _FixtureRecipe  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, module_name, module)

    recipe = load_custom_py(f"{CUSTOM_PY_PREFIX}{module_name}:MyFixtureRecipe")

    assert isinstance(recipe, Recipe)
    result = recipe.normalize("payload", {})
    assert isinstance(result, NormalizedResult)
    assert result.text == "fixture:payload"


def test_custom_py_loader_resolves_preinstantiated_fixture(monkeypatch):
    """Loader also accepts a module-level Recipe instance (not just classes)."""
    module_name = "superclaude_test_t04_10_registry_instance"
    pre_built = _FixtureRecipe()
    module = types.ModuleType(module_name)
    module.singleton = pre_built  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, module_name, module)

    recipe = load_custom_py(f"{CUSTOM_PY_PREFIX}{module_name}:singleton")
    assert recipe is pre_built


# ---------------------------------------------------------------------------
# 6 -- Surface sanity: the REGISTRY is the public dispatch table
# ---------------------------------------------------------------------------


def test_registry_is_mutable_dict_for_open_class_extension():
    """AC-007 open-class extension: REGISTRY supports runtime assignment.

    The dispatcher and lens validator both read REGISTRY at call time,
    so contributors registering ``REGISTRY[name] = MyRecipe()`` at
    import time must see the addition without core edits. Pinning the
    mutable-dict shape here protects that contract from a future
    refactor to e.g. ``MappingProxyType``.
    """
    assert isinstance(REGISTRY, dict)


def test_no_duplicate_recipe_identities():
    """Each bundled slot holds a distinct recipe object.

    Two slots pointing at the same instance would mask a registration
    bug (e.g. copy-paste from passthrough into another slot). The
    custom dispatcher is unique because it routes via load_custom_py;
    every other slot binds to its own recipe class.
    """
    identities = {name: id(REGISTRY[name]) for name in EXPECTED_RECIPE_NAMES}
    assert len(set(identities.values())) == len(EXPECTED_RECIPE_NAMES), (
        f"duplicate REGISTRY entry identities: {identities}"
    )
