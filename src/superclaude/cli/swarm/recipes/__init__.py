"""Swarm recipes -- normalization recipe modules (COMP-014 / COMP-015).

T04.02 lands the canonical :class:`Recipe` Protocol, the
:class:`NormalizedResult` dataclass, the open-class :data:`REGISTRY`
dispatch table, and the ``custom-py:module:func`` dynamic loader entry.
T04.03..T04.09 replace the M2-era ``None`` sentinels in :data:`REGISTRY`
with concrete recipe objects per the §3.3 inventory:

    - ``bare-review-v1``       -- ports t2_normalize.py (bare-review lens).
    - ``findings_table_v1``    -- shared shape for findings-table lenses
      (refactor-find, edge-case-hunt, doc-completeness).
    - ``hypothesis_table_v1``  -- hypothesis table (troubleshoot-hypothesis).
    - ``verdict_only_v1``      -- minimal verdict shape (spec-completeness,
      feasibility-probe).
    - ``passthrough``          -- raw amalgamation mode passthrough.
    - ``custom``               -- ``custom-py:module:func`` dynamic loader
      dispatcher entry (T04.09 lands the concrete loader module).

Recipe Protocol (FR-LENSREG.NS / §3.3 / AC-007)
==============================================

Each registered Recipe implements
``normalize(raw_output: str, args: dict) -> NormalizedResult``. The
Protocol is structural (``@runtime_checkable``) so any object exposing
that signature conforms regardless of inheritance -- consumer modules
( ``normalize.py``, recipe modules T04.03..T04.09, fixture recipes in
``tests/swarm/`` ) all share the same shape.

AC-011 boundary
---------------

Recipes own the per-worker shape transformation and MUST NOT score,
dedupe, or reorder findings. T04.14 lands the boundary assertion test;
this module's docstring records the contract so contributors see it
where the Protocol is declared.

custom-py:module:func dynamic loader
====================================

:func:`load_custom_py` parses a ``custom-py:<module>:<func>`` spec
string, imports the named module via ``importlib.import_module``, and
returns the named callable as a Recipe-conforming object. The loader
is Python-only by design (R-12 / OPS-005); non-Python harnesses use
``passthrough`` and post-process raw bodies. T04.02 wired the minimum
loader entry so the ``custom`` REGISTRY slot resolves and lens callers
can declare ``custom-py:`` recipe names today; T04.09 lands the
dedicated :mod:`superclaude.cli.swarm.recipes.custom` module with the
hardened error reporting + trust-boundary review per OPS-005, and this
package re-exports the loader surface from there so the import path
:func:`superclaude.cli.swarm.recipes.load_custom_py` stays stable.

Strategies registry
===================

:data:`STRATEGIES` mirrors :data:`REGISTRY` keys. FR-LENSREG.NS / T02.21
hooks the lens validator's
:func:`superclaude.cli.swarm.lenses._validate.default_strategy_checker`
into this dict so every bundled lens binds to a known normalizer output
shape before the M4 recipe runtime lands. The mapping is N-to-1 today
(strategy name == recipe name); M4 may expand if a single recipe needs
to emit multiple output shapes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Protocol, runtime_checkable

__all__: list[str] = [
    # Public Protocol + value types.
    "NormalizedResult",
    "Recipe",
    # Registry surfaces.
    "REGISTRY",
    "STRATEGIES",
    # Dynamic loader (custom-py:module:func).
    "CUSTOM_PY_PREFIX",
    "CustomPyDispatcher",
    "load_custom_py",
    # Recipe-name string tokens (kept for back-compat with the M2/M3
    # validator surface that introspected ``__all__`` for membership).
    "bare-review-v1",
    "findings_table_v1",
    "hypothesis_table_v1",
    "verdict_only_v1",
    "passthrough",
    "custom",
]


# ---------------------------------------------------------------------------
# Public value type + Protocol
# ---------------------------------------------------------------------------


@dataclass
class NormalizedResult:
    """Per-worker recipe output (COMP-008 / FR-028).

    Attributes:
        text: normalized body. The Wave-2 dispatcher writes this verbatim
            to ``WorkerResult.final_path``; the dispatcher does not
            inspect content.
        salvaged: ``True`` when the recipe recovered structure from a
            transport-flagged ``parse_error`` body. The §7.4
            ``parse_error -> success`` promotion in
            :func:`superclaude.cli.swarm.normalize.normalize_wave2`
            keys on this flag.
        error: optional recipe-side error message. ``None`` on success.
            Recipes signal recoverable shape problems by returning a
            non-``None`` ``error`` rather than raising; the dispatcher
            still emits the meta sidecar with this string recorded.
    """

    text: str = ""
    salvaged: bool = False
    error: Optional[str] = None


@runtime_checkable
class Recipe(Protocol):
    """Structural protocol for Wave-2 recipes (FR-LENSREG.NS / §3.3).

    Implementers expose a single ``normalize`` method that maps a raw
    worker body + recipe-specific kwargs to a :class:`NormalizedResult`.
    Use ``@runtime_checkable`` so the lens validator and dispatcher can
    detect Protocol conformance via :func:`isinstance` without forcing
    recipes to inherit a base class.

    AC-011: recipes preserve all findings -- no scoring, dedup, or
    reorder transforms. T04.14 lands the boundary assertion test.
    """

    def normalize(self, raw_output: str, args: dict[str, Any]) -> NormalizedResult: ...


# ---------------------------------------------------------------------------
# custom-py:module:func dynamic loader
# ---------------------------------------------------------------------------
#
# T04.09 owns the dedicated :mod:`superclaude.cli.swarm.recipes.custom`
# module; this package re-exports the public surface so the import path
# ``from superclaude.cli.swarm.recipes import load_custom_py`` (and the
# corresponding ``CustomPyDispatcher`` / ``CUSTOM_PY_PREFIX`` names) stay
# stable for callers wired against the T04.02 layout. The import is
# deferred to this point in the module so the :class:`Recipe` Protocol
# and :class:`NormalizedResult` dataclass are defined before
# ``custom.py`` imports back from us.

# ---------------------------------------------------------------------------
# Open-class REGISTRY + strategy registry
# ---------------------------------------------------------------------------
# T04.03 -- import the concrete bare_review_v1 recipe at module load so
# the REGISTRY entry resolves without a fallback. Import is deferred to
# this point in the module so the Recipe Protocol + NormalizedResult are
# already defined when bare_review_v1 imports ``NormalizedResult`` back
# from us. The relative order of these deferred imports is immaterial
# (bare_review_v1 does not import from custom, and vice versa).
from superclaude.cli.swarm.recipes.bare_review_v1 import BareReviewV1  # noqa: E402
from superclaude.cli.swarm.recipes.custom import (  # noqa: E402
    CUSTOM_PY_PREFIX,
    CustomPyDispatcher,
    load_custom_py,
)

# T04.04 -- findings_table_v1 lens-shared recipe (refactor-find,
# edge-case-hunt, doc-completeness).
from superclaude.cli.swarm.recipes.findings_table_v1 import (  # noqa: E402
    FindingsTableV1,
)

# T04.05 -- hypothesis_table_v1 recipe (troubleshoot-hypothesis).
from superclaude.cli.swarm.recipes.hypothesis_table_v1 import (  # noqa: E402
    HypothesisTableV1,
)

# T04.08 -- passthrough recipe (raw amalgamation mode).
from superclaude.cli.swarm.recipes.passthrough import Passthrough  # noqa: E402

# T04.07 -- verdict_only_v1 recipe (spec-completeness, feasibility-probe).
from superclaude.cli.swarm.recipes.verdict_only_v1 import VerdictOnlyV1  # noqa: E402

REGISTRY: dict[str, Optional[Recipe]] = {
    "bare-review-v1": BareReviewV1(),
    "findings_table_v1": FindingsTableV1(),
    "hypothesis_table_v1": HypothesisTableV1(),
    "verdict_only_v1": VerdictOnlyV1(),
    "passthrough": Passthrough(),
    "custom": CustomPyDispatcher(),
}
"""Open-class recipe registry (COMP-014 / COMP-015 / AC-007).

Six entries -- the five built-in recipes plus the ``custom-py:`` loader
dispatcher under the ``custom`` slot. T04.03..T04.08 swap the ``None``
sentinels for concrete Recipe objects; the lens validator
(:func:`superclaude.cli.swarm.lenses._validate.default_recipe_checker`)
treats either ``None`` or a Protocol-conforming object as "registered".

The Wave-2 dispatcher
(:func:`superclaude.cli.swarm.normalize.normalize_wave2`) falls back to
its private ``_PassthroughFallback`` when ``REGISTRY[name] is None`` so
the M3 -> M4 handshake works through the T04.03..T04.08 sequence.

Open-class: contributors register additional recipes by assigning
``REGISTRY[<name>] = MyRecipe()`` at import time (AC-007 verification
"open-class extension verified by adding a recipe without core edits").
"""


STRATEGIES: dict[str, str] = {
    "bare-review-v1": "bare-review-v1",
    "findings_table_v1": "findings_table_v1",
    "hypothesis_table_v1": "hypothesis_table_v1",
    "verdict_only_v1": "verdict_only_v1",
    "passthrough": "passthrough",
    "custom": "custom",
}
"""FR-LENSREG.NS normalizer-strategy registry (T02.21 / T02.23).

Strategy names parallel recipe names today. The lens validator
(:func:`superclaude.cli.swarm.lenses._validate.default_strategy_checker`)
consults this dict's keys to ratify that each bundled lens binds to a
known normalizer output shape. M4 may expand to N-to-M when a single
recipe needs to emit multiple shapes; the M2 contract -- "validator
asserts a registered Recipe matches the strategy" -- is preserved
because the strategy key still resolves to a recipe identifier.
"""
