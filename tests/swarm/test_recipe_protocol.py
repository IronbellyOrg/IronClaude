"""T04.02 -- Recipe Protocol + REGISTRY conformance tests (COMP-014/015).

Pins the open-class Recipe registry surface landed by T04.02:

    1. ``Recipe`` Protocol is structural (``@runtime_checkable``) and
       requires ``normalize(raw_output: str, args: dict) -> NormalizedResult``.
    2. ``NormalizedResult`` exposes the three documented fields
       (``text``, ``salvaged``, ``error``) with the right defaults.
    3. ``REGISTRY`` carries the six §3.3 recipe slots
       (``bare-review-v1``, ``findings_table_v1``, ``hypothesis_table_v1``,
       ``verdict_only_v1``, ``passthrough``, ``custom``).
    4. Every non-``None`` REGISTRY entry implements the Recipe Protocol
       via ``isinstance`` (structural conformance, no inheritance).
    5. The ``custom`` slot is the ``custom-py:`` dispatcher
       (:class:`CustomPyDispatcher`).
    6. :func:`load_custom_py` resolves ``custom-py:<module>:<func>``
       to a Recipe-conforming object for both the class-target and
       pre-instantiated-target shapes.
    7. Malformed ``custom-py:`` specs raise :class:`ValueError` with
       actionable diagnostics (missing prefix, missing colon, empty
       module, empty callable).
    8. Loader raises :class:`ImportError` for unknown modules,
       :class:`AttributeError` for unknown attributes, and
       :class:`TypeError` when the resolved object does not implement
       the Recipe Protocol.
    9. Open-class extension (AC-007): assigning a new Recipe object to
       a fresh ``REGISTRY`` key is observable via the public surface
       without core edits.

The tests intentionally do NOT inspect normalized body content -- AC-011
neutrality is covered by ``tests/swarm/test_recipe_no_judging.py``
(T04.14). This suite covers the registry / Protocol surface only.
"""

from __future__ import annotations

import sys
import types
from typing import Any

import pytest

from superclaude.cli.swarm import recipes
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
# Expected REGISTRY shape (§3.3 / FR-LENSREG.NS).
# ---------------------------------------------------------------------------


EXPECTED_RECIPE_NAMES: frozenset[str] = frozenset(
    {
        "bare-review-v1",
        "findings_table_v1",
        "hypothesis_table_v1",
        "verdict_only_v1",
        "passthrough",
        "custom",
    }
)


# ---------------------------------------------------------------------------
# 1 -- NormalizedResult field surface
# ---------------------------------------------------------------------------


def test_normalized_result_defaults_match_contract():
    result = NormalizedResult()
    assert result.text == ""
    assert result.salvaged is False
    assert result.error is None


def test_normalized_result_round_trip():
    result = NormalizedResult(text="hello", salvaged=True, error="recovered shape")
    assert result.text == "hello"
    assert result.salvaged is True
    assert result.error == "recovered shape"


# ---------------------------------------------------------------------------
# 2 -- Recipe Protocol is structural + runtime-checkable
# ---------------------------------------------------------------------------


class _ConformingRecipe:
    """Class that exposes the Recipe shape without inheriting Recipe."""

    def normalize(self, raw_output: str, args: dict[str, Any]) -> NormalizedResult:
        del raw_output, args
        return NormalizedResult(text="ok")


class _NonConformingObject:
    """Lacks the ``normalize`` method entirely."""


def test_recipe_protocol_accepts_structural_conformance():
    assert isinstance(_ConformingRecipe(), Recipe)


def test_recipe_protocol_rejects_non_conforming_object():
    assert not isinstance(_NonConformingObject(), Recipe)


# ---------------------------------------------------------------------------
# 3 -- REGISTRY shape: 6 expected entries
# ---------------------------------------------------------------------------


def test_registry_carries_six_recipe_slots():
    assert set(REGISTRY) == EXPECTED_RECIPE_NAMES
    assert len(REGISTRY) == 6


def test_strategies_mirrors_registry_keys():
    assert set(STRATEGIES) == EXPECTED_RECIPE_NAMES


# ---------------------------------------------------------------------------
# 4 -- Every non-None REGISTRY entry conforms to Recipe Protocol
# ---------------------------------------------------------------------------


def test_registry_entries_conform_to_protocol_or_are_sentinel():
    for name, entry in REGISTRY.items():
        # M2-era sentinel is permitted until T04.03..T04.08 swap in real
        # recipes; the dispatcher's passthrough fallback covers it.
        if entry is None:
            continue
        assert isinstance(entry, Recipe), (
            f"REGISTRY[{name!r}] (type {type(entry).__name__}) does not "
            "implement Recipe Protocol"
        )


def test_custom_slot_is_custom_py_dispatcher():
    entry = REGISTRY["custom"]
    assert isinstance(entry, CustomPyDispatcher)
    assert isinstance(entry, Recipe)


def test_custom_dispatcher_normalize_raises_actionable_error():
    dispatcher = REGISTRY["custom"]
    with pytest.raises(RuntimeError) as excinfo:
        dispatcher.normalize("body", {})
    assert CUSTOM_PY_PREFIX in str(excinfo.value)
    assert "load_custom_py" in str(excinfo.value)


# ---------------------------------------------------------------------------
# 5 -- custom-py:module:func dynamic loader (happy paths)
# ---------------------------------------------------------------------------


def _install_fake_module(monkeypatch, name: str, attrs: dict[str, Any]) -> None:
    """Register a synthetic module on ``sys.modules`` for the test scope."""
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    monkeypatch.setitem(sys.modules, name, module)


def test_load_custom_py_resolves_class_target(monkeypatch):
    _install_fake_module(
        monkeypatch,
        "superclaude_test_custom_py_class",
        {"MyRecipe": _ConformingRecipe},
    )

    recipe = load_custom_py("custom-py:superclaude_test_custom_py_class:MyRecipe")
    assert isinstance(recipe, Recipe)
    # Class is instantiated with no arguments.
    assert isinstance(recipe, _ConformingRecipe)


def test_load_custom_py_resolves_instance_target(monkeypatch):
    pre_built = _ConformingRecipe()
    _install_fake_module(
        monkeypatch,
        "superclaude_test_custom_py_instance",
        {"singleton": pre_built},
    )

    recipe = load_custom_py("custom-py:superclaude_test_custom_py_instance:singleton")
    assert recipe is pre_built


def test_load_custom_py_supports_dotted_module_path(monkeypatch):
    _install_fake_module(
        monkeypatch,
        "pkg_test_custom_py.sub.mod",
        {"Recipe2": _ConformingRecipe},
    )
    # Also register parent packages so importlib.import_module resolves.
    _install_fake_module(monkeypatch, "pkg_test_custom_py", {})
    _install_fake_module(monkeypatch, "pkg_test_custom_py.sub", {})

    recipe = load_custom_py("custom-py:pkg_test_custom_py.sub.mod:Recipe2")
    assert isinstance(recipe, Recipe)


# ---------------------------------------------------------------------------
# 6 -- custom-py:module:func dynamic loader (error paths)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "spec",
    [
        "",
        "bare-review-v1",
        "module:func",
        "custom-py",
        "custom-py:",
        "custom-py:no_colon_here",
        "custom-py::missing_module",
        "custom-py:missing_func:",
    ],
)
def test_load_custom_py_rejects_malformed_specs(spec):
    with pytest.raises(ValueError):
        load_custom_py(spec)


def test_load_custom_py_non_string_raises_value_error():
    with pytest.raises(ValueError):
        load_custom_py(None)  # type: ignore[arg-type]


def test_load_custom_py_unknown_module_raises_import_error():
    with pytest.raises(ImportError):
        load_custom_py("custom-py:no_such_module_zzz_xyz:fn")


def test_load_custom_py_unknown_attribute_raises_attribute_error(monkeypatch):
    _install_fake_module(
        monkeypatch,
        "superclaude_test_custom_py_missing_attr",
        {},
    )
    with pytest.raises(AttributeError):
        load_custom_py("custom-py:superclaude_test_custom_py_missing_attr:no_such_fn")


def test_load_custom_py_non_conforming_target_raises_type_error(monkeypatch):
    _install_fake_module(
        monkeypatch,
        "superclaude_test_custom_py_non_conforming",
        {"not_a_recipe": _NonConformingObject},
    )
    with pytest.raises(TypeError):
        load_custom_py(
            "custom-py:superclaude_test_custom_py_non_conforming:not_a_recipe"
        )


# ---------------------------------------------------------------------------
# 7 -- Open-class extension (AC-007)
# ---------------------------------------------------------------------------


def test_open_class_registry_accepts_new_recipe(monkeypatch):
    """Contributors can register additional recipes without core edits."""
    new_name = "experimental_extra_v1"
    monkeypatch.setitem(REGISTRY, new_name, _ConformingRecipe())
    assert new_name in REGISTRY
    entry = REGISTRY[new_name]
    assert isinstance(entry, Recipe)


# ---------------------------------------------------------------------------
# 8 -- Module surface sanity
# ---------------------------------------------------------------------------


def test_module_exports_protocol_and_registry():
    assert hasattr(recipes, "Recipe")
    assert hasattr(recipes, "NormalizedResult")
    assert hasattr(recipes, "REGISTRY")
    assert hasattr(recipes, "STRATEGIES")
    assert hasattr(recipes, "load_custom_py")
    assert hasattr(recipes, "CustomPyDispatcher")
    assert hasattr(recipes, "CUSTOM_PY_PREFIX")
    assert recipes.CUSTOM_PY_PREFIX == "custom-py:"


def test_registry_length_assertion_in_acceptance_criteria():
    """Mirrors T04.02 acceptance:
    ``from superclaude.cli.swarm.recipes import REGISTRY;
       assert len(REGISTRY) >= 6``.
    """
    from superclaude.cli.swarm.recipes import REGISTRY

    assert len(REGISTRY) >= 6
