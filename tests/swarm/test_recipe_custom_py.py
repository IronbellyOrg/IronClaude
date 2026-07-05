"""T04.09 -- ``custom-py:module:func`` dynamic loader tests (R-093 / COMP-021).

Pins the dedicated :mod:`superclaude.cli.swarm.recipes.custom` module
surface that T04.09 lands on top of the T04.02 ``__init__.py`` re-export
plumbing:

1. **Module surface**: ``custom.py`` exports ``load_custom_py``,
   ``CustomPyDispatcher``, and ``CUSTOM_PY_PREFIX`` directly, and the
   ``recipes`` package re-exports identically (same objects, not
   aliased copies).
2. **Spec parsing -- happy paths**: class target, pre-built instance,
   dotted module path; the loader returns a Recipe-conforming object.
3. **Spec parsing -- error paths**: hardened :class:`ValueError`
   messages for non-string specs, missing prefix, empty remainder,
   missing colon, empty module, empty callable. :class:`ImportError`
   for unknown modules. :class:`AttributeError` for unknown callable
   names. :class:`TypeError` when the resolved object lacks
   :meth:`normalize`.
4. **Trust boundary**: no auto-discovery -- the loader does not walk
   the filesystem, does not consult entry points, and does not import
   anything other than the literal module path the spec names.
5. **REGISTRY ``custom`` slot**: the :class:`CustomPyDispatcher` lives
   under ``REGISTRY['custom']`` and its :meth:`normalize` raises an
   actionable :class:`RuntimeError` if invoked directly (caller should
   have resolved the spec via :func:`load_custom_py` first).
6. **Dispatcher integration**: a resolved custom recipe runs end-to-end
   through :func:`normalize_wave2` and produces the expected
   ``final_path`` + ``.meta.json`` sidecar surface, preserving the
   recipe's body verbatim (AC-011 -- the dispatcher does not mutate
   recipe output).

The T04.02 ``test_recipe_protocol.py`` covers the same loader surface
from the Protocol-conformance angle; this file is the T04.09-owned
suite that pins the dedicated ``custom.py`` module shape and the
end-to-end dispatcher integration.
"""

from __future__ import annotations

import importlib
import json
import sys
import types
from pathlib import Path
from typing import Any

import pytest

from superclaude.cli.swarm import recipes
from superclaude.cli.swarm.models import WorkerResult
from superclaude.cli.swarm.normalize import normalize_wave2
from superclaude.cli.swarm.recipes import (
    CUSTOM_PY_PREFIX,
    REGISTRY,
    CustomPyDispatcher,
    NormalizedResult,
    Recipe,
    load_custom_py,
)
from superclaude.cli.swarm.recipes import custom as custom_mod

# ---------------------------------------------------------------------------
# Test fixtures -- conforming and non-conforming targets.
# ---------------------------------------------------------------------------


class _ClassRecipe:
    """Recipe class; instantiated with no args by the loader."""

    def normalize(self, raw_output: str, args: dict[str, Any]) -> NormalizedResult:
        del args
        return NormalizedResult(text=f"class:{raw_output}", salvaged=False)


class _SingletonRecipe:
    """Pre-built recipe instance with internal state -- passed verbatim."""

    def __init__(self, prefix: str = "singleton") -> None:
        self.prefix = prefix

    def normalize(self, raw_output: str, args: dict[str, Any]) -> NormalizedResult:
        del args
        return NormalizedResult(text=f"{self.prefix}:{raw_output}", salvaged=False)


class _NonRecipeObject:
    """No ``normalize`` method -- must be rejected by the Protocol check."""

    def something_else(self) -> str:
        return "nope"


def _install_fake_module(
    monkeypatch: pytest.MonkeyPatch,
    name: str,
    attrs: dict[str, Any],
) -> None:
    """Register a synthetic module on ``sys.modules`` for the test scope."""
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    monkeypatch.setitem(sys.modules, name, module)


# ---------------------------------------------------------------------------
# 1 -- Module surface
# ---------------------------------------------------------------------------


def test_custom_module_exports_loader_surface():
    """``custom.py`` directly exposes the loader symbols."""
    assert hasattr(custom_mod, "CUSTOM_PY_PREFIX")
    assert hasattr(custom_mod, "load_custom_py")
    assert hasattr(custom_mod, "CustomPyDispatcher")
    assert custom_mod.CUSTOM_PY_PREFIX == "custom-py:"


def test_custom_module_all_lists_expected_symbols():
    assert set(custom_mod.__all__) == {
        "CUSTOM_PY_PREFIX",
        "CustomPyDispatcher",
        "load_custom_py",
    }


def test_recipes_reexports_are_same_objects_as_custom_module():
    """T04.09: package re-exports must be the *same* objects, not copies."""
    assert recipes.load_custom_py is custom_mod.load_custom_py
    assert recipes.CustomPyDispatcher is custom_mod.CustomPyDispatcher
    assert recipes.CUSTOM_PY_PREFIX == custom_mod.CUSTOM_PY_PREFIX


def test_custom_module_docstring_records_trust_boundary():
    """Per T04.09 step 3: document trust boundary in module docstring."""
    docstring = custom_mod.__doc__ or ""
    assert "trust" in docstring.lower()
    # Trust boundary discussion must mention the relevant ops constraints
    # so contributors discover the review obligation without leaving the
    # file.
    assert "OPS-005" in docstring
    assert "importlib" in docstring.lower()


# ---------------------------------------------------------------------------
# 2 -- Loader happy paths
# ---------------------------------------------------------------------------


def test_load_custom_py_resolves_class_target(monkeypatch):
    _install_fake_module(
        monkeypatch,
        "superclaude_t0409_class_target",
        {"MyRecipe": _ClassRecipe},
    )

    recipe = load_custom_py("custom-py:superclaude_t0409_class_target:MyRecipe")

    assert isinstance(recipe, Recipe)
    assert isinstance(recipe, _ClassRecipe)
    # Functional check: the loader returned a working recipe.
    result = recipe.normalize("payload", {})
    assert isinstance(result, NormalizedResult)
    assert result.text == "class:payload"


def test_load_custom_py_resolves_instance_target(monkeypatch):
    prebuilt = _SingletonRecipe(prefix="custom")
    _install_fake_module(
        monkeypatch,
        "superclaude_t0409_instance_target",
        {"recipe": prebuilt},
    )

    recipe = load_custom_py("custom-py:superclaude_t0409_instance_target:recipe")

    # Pre-built instances are returned verbatim (singleton pattern).
    assert recipe is prebuilt
    result = recipe.normalize("payload", {})
    assert result.text == "custom:payload"


def test_load_custom_py_supports_dotted_module_path(monkeypatch):
    _install_fake_module(monkeypatch, "pkg_t0409", {})
    _install_fake_module(monkeypatch, "pkg_t0409.sub", {})
    _install_fake_module(
        monkeypatch,
        "pkg_t0409.sub.mod",
        {"Recipe2": _ClassRecipe},
    )

    recipe = load_custom_py("custom-py:pkg_t0409.sub.mod:Recipe2")

    assert isinstance(recipe, Recipe)


def test_load_custom_py_class_target_zero_arg_constructor_invoked(monkeypatch):
    """Loader must call ``cls()`` -- record the constructor call."""

    constructor_calls: list[tuple[Any, ...]] = []

    class TracingRecipe:
        def __init__(self) -> None:
            constructor_calls.append(())

        def normalize(self, raw_output: str, args: dict[str, Any]) -> NormalizedResult:
            del args
            return NormalizedResult(text=raw_output)

    _install_fake_module(
        monkeypatch,
        "superclaude_t0409_constructor_trace",
        {"TracingRecipe": TracingRecipe},
    )

    recipe = load_custom_py(
        "custom-py:superclaude_t0409_constructor_trace:TracingRecipe"
    )

    assert isinstance(recipe, TracingRecipe)
    assert constructor_calls == [()]


# ---------------------------------------------------------------------------
# 3 -- Loader error paths (hardened diagnostics)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("spec", "must_mention"),
    [
        ("", "custom-py:"),
        ("bare-review-v1", "custom-py:"),
        ("module:func", "custom-py:"),
        ("custom-py", "custom-py:"),  # missing colon entirely
        ("custom-py:", "<module>"),  # empty remainder
        ("custom-py:no_colon_here", "':' separator"),
        ("custom-py::missing_module", "<module>"),
        ("custom-py:missing_func:", "<callable>"),
    ],
)
def test_load_custom_py_malformed_specs_raise_actionable_value_error(
    spec, must_mention
):
    with pytest.raises(ValueError) as excinfo:
        load_custom_py(spec)
    message = str(excinfo.value)
    # Each error message must echo the failing spec so contributors can
    # locate the typo without re-reading the loader source.
    assert repr(spec) in message or spec in message
    # And must name the constraint that failed.
    assert must_mention in message


@pytest.mark.parametrize("bad", [None, 123, 12.5, [], {}, object()])
def test_load_custom_py_non_string_spec_raises_value_error(bad):
    with pytest.raises(ValueError) as excinfo:
        load_custom_py(bad)  # type: ignore[arg-type]
    assert "string" in str(excinfo.value).lower()


def test_load_custom_py_unknown_module_raises_import_error():
    with pytest.raises(ImportError):
        load_custom_py("custom-py:no_such_module_t0409_zzz:fn")


def test_load_custom_py_unknown_attribute_raises_attribute_error(monkeypatch):
    _install_fake_module(
        monkeypatch,
        "superclaude_t0409_missing_attr",
        {},  # module is importable but exposes nothing
    )
    with pytest.raises(AttributeError) as excinfo:
        load_custom_py("custom-py:superclaude_t0409_missing_attr:no_such_fn")
    message = str(excinfo.value)
    # Message must name the spec, module, and missing attribute so
    # contributors see all three at the failure site.
    assert "superclaude_t0409_missing_attr" in message
    assert "no_such_fn" in message


def test_load_custom_py_non_conforming_target_raises_type_error(monkeypatch):
    _install_fake_module(
        monkeypatch,
        "superclaude_t0409_non_conforming",
        {"not_a_recipe": _NonRecipeObject},
    )
    with pytest.raises(TypeError) as excinfo:
        load_custom_py("custom-py:superclaude_t0409_non_conforming:not_a_recipe")
    message = str(excinfo.value)
    # Must reference the Recipe Protocol signature so contributors see
    # what shape the loader expected.
    assert "Recipe" in message
    assert "normalize" in message


def test_load_custom_py_non_conforming_instance_raises_type_error(monkeypatch):
    """Pre-built instances are also Protocol-checked."""
    _install_fake_module(
        monkeypatch,
        "superclaude_t0409_non_conforming_inst",
        {"recipe": _NonRecipeObject()},
    )
    with pytest.raises(TypeError):
        load_custom_py("custom-py:superclaude_t0409_non_conforming_inst:recipe")


# ---------------------------------------------------------------------------
# 4 -- Trust boundary: no auto-discovery
# ---------------------------------------------------------------------------


def test_loader_does_not_walk_filesystem(monkeypatch, tmp_path):
    """No filesystem traversal -- loader uses importlib only.

    Drop a directory containing a tantalizing ``recipe.py`` onto
    ``sys.path`` and prove that the loader still raises ImportError if
    the spec does not name the module verbatim. The presence of the
    file on disk must not be enough to "auto-discover" a recipe.
    """
    decoy_dir = tmp_path / "decoy_pkg"
    decoy_dir.mkdir()
    (decoy_dir / "__init__.py").write_text("", encoding="utf-8")
    (decoy_dir / "recipe.py").write_text(
        "class Whatever:\n"
        "    def normalize(self, raw_output, args):\n"
        "        return None\n",
        encoding="utf-8",
    )
    monkeypatch.syspath_prepend(str(tmp_path))

    # Spec names a module that does NOT exist; the loader must not
    # discover ``decoy_pkg.recipe`` even though it's adjacent on
    # sys.path.
    with pytest.raises(ImportError):
        load_custom_py("custom-py:totally_unrelated_module_t0409:Whatever")


def test_loader_does_not_consult_entry_points(monkeypatch):
    """Loader must use literal module path -- no entry-point lookups."""

    # If the loader inadvertently called importlib.metadata.entry_points,
    # this monkeypatch would surface as an unexpected call. We do not
    # assert "never called", just that the loader's error path runs
    # purely on importlib.import_module (the ImportError from the bogus
    # spec confirms it walked the standard import machinery).
    sentinel_calls: list[str] = []

    real_entry_points = getattr(importlib.metadata, "entry_points", None)

    def _trap_entry_points(*args, **kwargs):
        sentinel_calls.append("entry_points called")
        if real_entry_points is not None:
            return real_entry_points(*args, **kwargs)
        raise AssertionError("loader called entry_points unexpectedly")

    monkeypatch.setattr(importlib.metadata, "entry_points", _trap_entry_points)
    with pytest.raises(ImportError):
        load_custom_py("custom-py:still_no_such_module_t0409:fn")

    assert sentinel_calls == []  # loader stayed on importlib.import_module


# ---------------------------------------------------------------------------
# 5 -- CustomPyDispatcher in REGISTRY['custom']
# ---------------------------------------------------------------------------


def test_registry_custom_slot_is_custom_py_dispatcher():
    entry = REGISTRY["custom"]
    assert isinstance(entry, CustomPyDispatcher)
    assert isinstance(entry, Recipe)


def test_custom_py_dispatcher_direct_call_raises_actionable_runtime_error():
    dispatcher = CustomPyDispatcher()
    with pytest.raises(RuntimeError) as excinfo:
        dispatcher.normalize("body", {})
    message = str(excinfo.value)
    # Error must point the caller at the correct recovery path so the
    # accidental routing surfaces loudly.
    assert "load_custom_py" in message
    assert CUSTOM_PY_PREFIX in message


def test_custom_py_dispatcher_satisfies_recipe_protocol_for_registry_check():
    """T04.10 conformance check: every REGISTRY entry implements Recipe."""
    assert isinstance(CustomPyDispatcher(), Recipe)


# ---------------------------------------------------------------------------
# 6 -- Dispatcher integration (resolved custom recipe through normalize_wave2)
# ---------------------------------------------------------------------------


def _make_worker(
    tmp_path: Path,
    index: int,
    *,
    status: str,
    body: str,
) -> WorkerResult:
    raw_path = tmp_path / f"worker-{index:02d}.raw.md"
    raw_path.write_text(body, encoding="utf-8")
    return WorkerResult(
        index=index,
        path=str(tmp_path / f"worker-{index:02d}.md"),
        raw_path=str(raw_path),
        meta_path=str(tmp_path / f"worker-{index:02d}.meta.json"),
        final_path=str(tmp_path / f"worker-{index:02d}.final.md"),
        model_id=f"model-{index}",
        model_label=f"Model {index}",
        bytes=len(body.encode("utf-8")),
        status=status,
        http_code=200 if status == "success" else None,
        attempts=1,
        elapsed_ms=42,
    )


def test_resolved_custom_recipe_runs_end_to_end_through_normalize_wave2(
    monkeypatch, tmp_path
):
    """End-to-end: resolve spec, register under a fresh REGISTRY key,
    route a worker through ``normalize_wave2`` -- the loader output
    must be Protocol-callable and the dispatcher must persist the
    body verbatim.
    """
    _install_fake_module(
        monkeypatch,
        "superclaude_t0409_dispatch_e2e",
        {"MyRecipe": _ClassRecipe},
    )
    recipe = load_custom_py("custom-py:superclaude_t0409_dispatch_e2e:MyRecipe")

    # Register under a transient key so normalize_wave2 can look it up
    # by name. (The dispatcher itself does NOT inspect spec strings;
    # that wiring lives upstream -- this test confirms a *resolved*
    # custom recipe behaves like any other REGISTRY entry.)
    monkeypatch.setitem(REGISTRY, "_t0409_custom_e2e", recipe)

    worker = _make_worker(tmp_path, 0, status="success", body="hello")
    [out] = normalize_wave2([worker], "_t0409_custom_e2e")

    assert out.status == "success"
    final_body = Path(worker.final_path).read_text(encoding="utf-8")
    # Recipe output is preserved verbatim -- dispatcher does not mutate.
    assert final_body == "class:hello"

    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["recipe"] == "_t0409_custom_e2e"
    assert meta["salvaged"] is False
    assert meta["status"] == "success"


def test_resolved_custom_recipe_salvage_flag_promotes_parse_error(
    monkeypatch, tmp_path
):
    """A custom recipe can opt into salvage promotion via the standard
    ``NormalizedResult.salvaged=True`` flag -- the dispatcher honours
    it identically to the built-in recipes.
    """

    class SalvagingRecipe:
        def normalize(self, raw_output: str, args: dict[str, Any]) -> NormalizedResult:
            del args
            return NormalizedResult(text=f"recovered:{raw_output}", salvaged=True)

    _install_fake_module(
        monkeypatch,
        "superclaude_t0409_salvage",
        {"Salvager": SalvagingRecipe},
    )
    recipe = load_custom_py("custom-py:superclaude_t0409_salvage:Salvager")
    monkeypatch.setitem(REGISTRY, "_t0409_custom_salvage", recipe)

    worker = _make_worker(tmp_path, 1, status="parse_error", body="raw")
    [out] = normalize_wave2([worker], "_t0409_custom_salvage")

    # parse_error -> success promotion fires because the recipe set
    # salvaged=True and returned non-empty text.
    assert out.status == "success"
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["salvaged"] is True
    assert meta["status"] == "success"


def test_resolved_custom_recipe_preserves_findings_verbatim(monkeypatch):
    """AC-011 boundary: loader does not mutate recipe output (no
    scoring/dedup/reorder injected by the loader path)."""

    class PreservingRecipe:
        def normalize(self, raw_output: str, args: dict[str, Any]) -> NormalizedResult:
            del args
            # Return the body unchanged -- if the loader added any
            # post-processing layer, this assertion would fail.
            return NormalizedResult(text=raw_output, salvaged=False)

    _install_fake_module(
        monkeypatch,
        "superclaude_t0409_ac011",
        {"Preserve": PreservingRecipe},
    )
    recipe = load_custom_py("custom-py:superclaude_t0409_ac011:Preserve")

    body = (
        "- Finding A\n"
        "- Finding B\n"
        "- Finding A\n"  # duplicate must survive
        "- Finding C\n"
    )
    result = recipe.normalize(body, {})
    assert result.text == body
    assert result.text.count("Finding A") == 2  # duplicate preserved
