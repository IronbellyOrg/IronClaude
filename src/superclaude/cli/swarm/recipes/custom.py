"""T04.09 -- ``custom-py:module:func`` dynamic loader (COMP-021 / R-093).

Owns the canonical implementation of the dynamic loader that resolves a
``custom-py:<module>:<callable>`` recipe-name spec to a Recipe-conforming
object. T04.02 wired the minimal loader entry into
:mod:`superclaude.cli.swarm.recipes` so the ``custom`` REGISTRY slot
could resolve; T04.09 lands the dedicated module with hardened error
reporting and the trust-boundary review per OPS-005.

The Wave-2 normalize dispatcher
(:func:`superclaude.cli.swarm.normalize.normalize_wave2`) looks up
recipes by name in :data:`superclaude.cli.swarm.recipes.REGISTRY`. The
``custom-py:`` prefix is *not* a REGISTRY key -- it is a literal recipe
name handed in via :attr:`NormalizationSpec.recipe`. Callers that detect
the prefix on a spec route through :func:`load_custom_py(spec)` to
materialize the real Recipe; the ``custom`` REGISTRY slot itself carries
:class:`CustomPyDispatcher`, an actionable-error sentinel that fails
loudly if the dispatcher routes a literal ``custom`` key (rather than
the resolved spec) by accident.

Trust boundary (R-12 / OPS-005 / NFR-008)
=========================================

This loader imports an **arbitrary Python module by name** via
:func:`importlib.import_module` and looks up a named attribute on it.
Module import side-effects (top-level code, package ``__init__``
imports) run with the host process's full privileges. There is no
sandbox, no allow-list of permitted module roots, no taint analysis,
and no path containment. Callers MUST treat the spec string as
**trusted input**.

In practice the trust path is:

    1. A lens contributor authors a lens definition containing
       ``normalization.recipe: "custom-py:<module>:<func>"``.
    2. The lens is reviewed at PR time per OPS-005 (lens contribution
       policy). Reviewers verify the named module is part of the
       SuperClaude package tree or a vetted dependency.
    3. The lens validator (:mod:`superclaude.cli.swarm.lenses._validate`)
       statically inspects the recipe name string at preflight and
       refuses unknown REGISTRY recipe names; ``custom-py:`` strings
       are gated by the prefix check below.
    4. ``load_custom_py`` is called at Wave-2 normalize time and the
       module imports.

This loader is therefore the **last gate** between a lens definition
and arbitrary module execution. The hardening below (input
type-checking, structural validation of the spec, explicit non-empty
checks on each component, refusal of non-conforming targets) exists to
ensure that benign-looking lens edits cannot silently turn into
arbitrary-module-load primitives via malformed specs. It does **not**
attempt to detect *malicious* specs -- the OPS-005 review process owns
that boundary.

Specifically, this module DOES NOT:

* Walk the filesystem looking for candidate modules. The spec must
  name the dotted module path verbatim; no auto-discovery.
* Read package metadata, entry points, or plugin manifests. Recipes
  register either through the static REGISTRY assignment (open-class
  extension in :mod:`superclaude.cli.swarm.recipes`) or through this
  explicit ``custom-py:`` opt-in.
* Allow ``custom-py:`` specs that resolve to non-Python harnesses. The
  loader is Python-only by design (R-12). Non-Python lens contributors
  use ``passthrough`` and post-process raw bodies out-of-band.
* Re-execute or hot-reload modules across invocations. Each call uses
  the standard ``importlib`` cache; if a contributor needs reload-on-
  edit semantics, that is a development-environment concern outside
  the loader's scope.

Spec grammar
============

::

    spec       = "custom-py:" module-path ":" callable-name
    module-path = dotted Python module path; non-empty; passed
                  verbatim to ``importlib.import_module``.
    callable-name = attribute name on the imported module; non-empty.

Examples (valid):

* ``custom-py:my_pkg.recipes.priority:PriorityRecipe`` -- class target.
* ``custom-py:my_pkg.recipes:singleton_recipe`` -- pre-built instance.
* ``custom-py:my_pkg.deep.path.module:Recipe`` -- dotted module path.

Examples (rejected at the loader gate):

* ``""`` / ``None`` -- empty or non-string.
* ``bare-review-v1`` -- missing prefix; not a custom-py spec.
* ``custom-py`` -- missing both colons.
* ``custom-py:`` -- empty remainder.
* ``custom-py:no_colon_here`` -- no second colon → cannot locate
  callable name.
* ``custom-py::missing_module`` -- empty module path.
* ``custom-py:missing_func:`` -- empty callable name.

Target callable contract
========================

The resolved attribute MUST be one of:

* A **class** whose instances implement
  :class:`~superclaude.cli.swarm.recipes.Recipe`. The loader
  instantiates it via ``cls()`` (zero-arg constructor) -- lenses that
  need configuration encode it via ``NormalizationSpec.recipe_args``
  forwarded at ``normalize`` call time. A class that requires
  constructor arguments will surface a ``TypeError`` from ``cls()``
  rather than from the Protocol check.
* A **pre-built object** that already exposes the
  ``normalize(raw_output, args) -> NormalizedResult`` method. Useful
  when the contributor wants a singleton (e.g. a recipe that owns an
  internal LRU cache). The loader passes it back verbatim.

In both cases the loader validates :func:`isinstance` against the
runtime-checkable :class:`Recipe` Protocol and raises
:class:`TypeError` when the object does not conform. The Protocol is
structural; recipes do not need to inherit anything.

AC-011 boundary
===============

Custom recipes are bound by the same neutrality boundary as the
built-in recipes: they MUST NOT score, dedupe, or reorder findings.
T04.14 lands the boundary assertion test and runs it across every
REGISTRY entry; ``custom-py:`` specs are exercised through the
fixture-recipe harness in
:mod:`tests.swarm.test_recipe_custom_py`. The loader itself does not
police neutrality at load time -- AC-011 enforcement is behavioural,
not structural.
"""

from __future__ import annotations

import importlib
from typing import Any

from superclaude.cli.swarm.recipes import NormalizedResult, Recipe


__all__ = [
    "CUSTOM_PY_PREFIX",
    "CustomPyDispatcher",
    "load_custom_py",
]


CUSTOM_PY_PREFIX: str = "custom-py:"
"""Recipe-name prefix that selects the dynamic Python loader (AC-007).

Recipe names beginning with this prefix are not looked up in
:data:`superclaude.cli.swarm.recipes.REGISTRY` by direct key. Instead
:func:`load_custom_py` parses the remainder of the string as
``<module>:<callable>`` and returns the named callable as a Recipe.
"""


def _split_spec(spec: str) -> tuple[str, str]:
    """Parse ``custom-py:<module>:<callable>`` into ``(module, callable)``.

    Returns the dotted module path and the callable attribute name.
    Raises :class:`ValueError` with a precise diagnostic for every
    malformed shape -- the spec, the failing constraint, and the
    canonical grammar.

    The split uses :meth:`str.rpartition` so module paths containing
    colons (rare; tooling sometimes encodes versions that way) still
    parse with the last colon as the callable separator. An empty
    module or empty callable after the split is rejected.
    """
    if not isinstance(spec, str):
        raise ValueError(
            f"custom-py spec must be a string; got {type(spec).__name__}"
        )
    if not spec.startswith(CUSTOM_PY_PREFIX):
        raise ValueError(
            f"custom-py spec must start with {CUSTOM_PY_PREFIX!r}; got {spec!r}"
        )
    remainder = spec[len(CUSTOM_PY_PREFIX):]
    if not remainder:
        raise ValueError(
            f"custom-py spec missing <module>:<callable>; got {spec!r}"
        )
    if ":" not in remainder:
        raise ValueError(
            f"custom-py spec must be {CUSTOM_PY_PREFIX}<module>:<callable>; "
            f"missing ':' separator in {spec!r}"
        )
    module_path, _, func_name = remainder.rpartition(":")
    if not module_path:
        raise ValueError(
            f"custom-py spec has empty <module>; expected "
            f"{CUSTOM_PY_PREFIX}<module>:<callable>; got {spec!r}"
        )
    if not func_name:
        raise ValueError(
            f"custom-py spec has empty <callable>; expected "
            f"{CUSTOM_PY_PREFIX}<module>:<callable>; got {spec!r}"
        )
    return module_path, func_name


def load_custom_py(spec: str) -> Recipe:
    """Resolve a ``custom-py:<module>:<callable>`` spec to a Recipe.

    The full trust-boundary discussion lives in the module docstring;
    the short form: this loader imports an arbitrary Python module by
    name and returns a named attribute on it. Callers MUST treat the
    spec as trusted input (PR-reviewed lens definitions per OPS-005).

    Spec grammar:
        ``custom-py:<module-dotted-path>:<callable-name>``

    The ``<callable-name>`` MUST resolve to either:

    * a **class** whose instances implement
      :class:`~superclaude.cli.swarm.recipes.Recipe`; the loader
      instantiates it with ``cls()``, or
    * a **callable object** that already conforms to the
      :class:`Recipe` Protocol (passed back unchanged).

    Args:
        spec: the recipe name string. Must start with
            :data:`CUSTOM_PY_PREFIX`. Both the module path and the
            callable name must be non-empty.

    Returns:
        A :class:`Recipe`-conforming object ready for the Wave-2
        dispatcher to call.

    Raises:
        ValueError: when ``spec`` is malformed (non-string, missing
            prefix, missing colon, empty module, or empty callable).
            The exception message names the failing constraint and
            echoes the spec so contributors can locate the typo.
        ImportError: when the named module cannot be imported. Raised
            by :func:`importlib.import_module`; the loader does not
            wrap or swallow this so contributors see the real cause
            (typically a missing dependency or a typo in the module
            path).
        AttributeError: when the module imports cleanly but does not
            expose the named callable. The message records the spec,
            module path, and missing attribute name.
        TypeError: when the resolved object does not implement the
            :class:`Recipe` Protocol -- e.g. a module-level constant,
            a function without the right signature, or a class whose
            instance lacks ``normalize``. The message records the
            resolved object's type so contributors can compare it to
            the Protocol shape.
    """
    module_path, func_name = _split_spec(spec)

    module = importlib.import_module(module_path)
    try:
        target = getattr(module, func_name)
    except AttributeError as exc:
        raise AttributeError(
            f"custom-py spec {spec!r}: module {module_path!r} has no "
            f"attribute {func_name!r}"
        ) from exc

    # Two acceptable target shapes:
    #   1. A class -> instantiate with no args (T04.09 acceptance:
    #      "Loader resolves custom-py:module:func strings to callable
    #      Recipe"). Lenses pass configuration via ``recipe_args`` at
    #      normalize() call time, so the class itself takes no
    #      constructor arguments.
    #   2. A pre-built Recipe-conforming object -> use verbatim. This
    #      is the singleton pattern (one recipe instance shared across
    #      every worker; the recipe is expected to be stateless or to
    #      manage its own internal caches).
    if isinstance(target, type):
        instance = target()
    else:
        instance = target

    if not isinstance(instance, Recipe):
        raise TypeError(
            f"custom-py spec {spec!r}: resolved object "
            f"(type {type(instance).__name__}) does not implement Recipe "
            f"Protocol (normalize(raw_output, args) -> NormalizedResult)"
        )
    return instance


class CustomPyDispatcher:
    """REGISTRY entry that routes via :func:`load_custom_py`.

    The :data:`superclaude.cli.swarm.recipes.REGISTRY` is keyed on
    recipe NAMES; ``custom-py:<module>:<func>`` specs are *not* literal
    keys -- they are recipe names that callers route through
    :func:`load_custom_py` to materialize a Recipe. The ``custom`` slot
    in REGISTRY therefore carries this dispatcher object, whose
    :meth:`normalize` method exists only to fail loudly with an
    actionable error if a caller accidentally invokes it directly
    (rather than first resolving the spec via :func:`load_custom_py`).

    The actionable-error contract is part of T04.10's registry
    conformance check (every REGISTRY entry must implement the Recipe
    Protocol) -- the dispatcher implements ``normalize`` so the
    Protocol check passes, and the implementation raises so that any
    accidental routing surfaces as a loud failure rather than a silent
    no-op.
    """

    def normalize(
        self, raw_output: str, args: dict[str, Any]
    ) -> NormalizedResult:
        del raw_output, args
        raise RuntimeError(
            "CustomPyDispatcher.normalize called directly -- callers must "
            f"resolve {CUSTOM_PY_PREFIX}<module>:<func> specs via "
            "recipes.load_custom_py(spec) before invoking the recipe."
        )
