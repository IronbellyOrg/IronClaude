"""Swarm lenses -- ``LENSES`` registry (COMP-022 / T02.14 + T02.23).

This module is the **aggregator** for the eight built-in lens entries
the swarm pipeline consumes at Wave 0 preflight. It mirrors
``cli/swarm/recipes/__init__.py`` in role -- the registry surface is the
dict ``LENSES`` keyed by ``LensEntry.name`` (hyphenated, per §4.2 and
the roadmap COMP-019..COMP-026 rows). Module-level helper
:func:`get_lens` resolves a name to its entry or raises ``KeyError`` for
unknown names so callers can wrap that into a structured preflight
failure (:data:`preflight.RULE_UNKNOWN_LENS`).

T02.23 lands the populated bodies for the seven non-custom entries
sourced from ``cli/swarm/lenses/<name>.py`` (COMP-024..030). Each
module exports a ``LENS: LensEntry`` constant with the full DM-010 +
FR-LENSREG.NS field set; the aggregator imports those constants and
indexes them into :data:`LENSES`. The escape-hatch ``custom`` entry
remains a placeholder -- its prompt body flows in from
``--custom-prompt-dir`` at preflight per FR-021 / INV-003 and the
COMP-023 lens validator (T02.15) intentionally skips it.

Eight-entry inventory (mapped to roadmap COMP-024..COMP-030 + COMP-026):
    - ``bare-review``            -- COMP-024, stable, suspect:true,
      tier T2, default_workers=3, recipe ``bare-review-v1``.
    - ``refactor-find``          -- COMP-025 (experimental).
    - ``edge-case-hunt``         -- COMP-026 (experimental,
      default_workers=4).
    - ``spec-completeness``      -- COMP-027 (experimental).
    - ``feasibility-probe``      -- COMP-028 (experimental).
    - ``troubleshoot-hypothesis``-- COMP-029 (experimental,
      default_workers=4, recipe ``hypothesis_table_v1``).
    - ``doc-completeness``       -- COMP-030 (experimental).
    - ``custom``                 -- COMP-026 escape-hatch placeholder
      (intentionally bypasses the lens validator -- contents flow in
      from ``--custom-prompt-dir`` at preflight per FR-021 / INV-003).

Key convention:
    Hyphens (``bare-review``, not ``bare_review``) match ``LensEntry.name``
    on every fixture in ``tests/swarm/`` (see ``test_lens_defaults.py``)
    and the §4.2 mapping in
    ``.dev/releases/Current/MultiModelSwarm/merged-requirements.compressed.md``.
    Underscored variants (``bare_review``, ``refactor_find``, ...) name
    the Python module files under ``cli/swarm/lenses/<name>.py``.
"""

from __future__ import annotations

from typing import Iterable

from superclaude.cli.swarm.lenses.bare_review import LENS as _BARE_REVIEW_LENS
from superclaude.cli.swarm.lenses.doc_completeness import (
    LENS as _DOC_COMPLETENESS_LENS,
)
from superclaude.cli.swarm.lenses.edge_case_hunt import (
    LENS as _EDGE_CASE_HUNT_LENS,
)
from superclaude.cli.swarm.lenses.feasibility_probe import (
    LENS as _FEASIBILITY_PROBE_LENS,
)
from superclaude.cli.swarm.lenses.refactor_find import (
    LENS as _REFACTOR_FIND_LENS,
)
from superclaude.cli.swarm.lenses.reflect_review import LENS as _REFLECT_REVIEW_LENS
from superclaude.cli.swarm.lenses.spec_completeness import (
    LENS as _SPEC_COMPLETENESS_LENS,
)
from superclaude.cli.swarm.lenses.troubleshoot_hypothesis import (
    LENS as _TROUBLESHOOT_HYPOTHESIS_LENS,
)
from superclaude.cli.swarm.models import LensEntry

__all__ = ["LENSES", "LENS_NAMES", "get_lens", "iter_lenses"]


LENS_NAMES: tuple[str, ...] = (
    "bare-review",
    "refactor-find",
    "edge-case-hunt",
    "spec-completeness",
    "feasibility-probe",
    "troubleshoot-hypothesis",
    "doc-completeness",
    "reflect-review",
    "custom",
)
"""The eight well-known lens names in registry order.

Exposed as a tuple so the order is preserved for documentation surfaces
(`swarm validate-lenses` summary output, ``docs/dev/lens-contribution-policy.md``)
and so tests can pin the registry shape without relying on dict-iteration
order.
"""


def _custom_placeholder() -> LensEntry:
    """Build the ``custom`` escape-hatch placeholder entry.

    The COMP-023 lens validator skips entries whose ``name`` equals
    ``"custom"`` (escape hatch -- contents flow in from
    ``--custom-prompt-dir`` at preflight per FR-021 / INV-003), so this
    placeholder carries only ``name`` and uses the dataclass defaults
    for every other field. The round-trip suite
    (:meth:`ResolvedLensEntry.from_lens`) succeeds with the defaults.
    """
    return LensEntry(name="custom")


LENSES: dict[str, LensEntry] = {
    "bare-review": _BARE_REVIEW_LENS,
    "refactor-find": _REFACTOR_FIND_LENS,
    "edge-case-hunt": _EDGE_CASE_HUNT_LENS,
    "spec-completeness": _SPEC_COMPLETENESS_LENS,
    "feasibility-probe": _FEASIBILITY_PROBE_LENS,
    "troubleshoot-hypothesis": _TROUBLESHOOT_HYPOTHESIS_LENS,
    "doc-completeness": _DOC_COMPLETENESS_LENS,
    "reflect-review": _REFLECT_REVIEW_LENS,
    "custom": _custom_placeholder(),
}
"""Registry mapping lens name → :class:`LensEntry`.

Populated at module import: seven fully-populated entries
(COMP-024..030, sourced from ``cli/swarm/lenses/<name>.py``) plus the
``custom`` escape-hatch placeholder (COMP-026). Callers should consult
:func:`get_lens` rather than indexing this dict directly so unknown
names raise ``KeyError`` with a single canonical message.
"""


def get_lens(name: str) -> LensEntry:
    """Return the :class:`LensEntry` registered under ``name``.

    Raises:
        KeyError: ``name`` is not present in :data:`LENSES`. Callers in
            the preflight path wrap this into a :class:`PreflightFailure`
            with :data:`preflight.RULE_UNKNOWN_LENS` and a structured
            ``reason='lens-unknown'`` field.
    """
    try:
        return LENSES[name]
    except KeyError as exc:
        raise KeyError(name) from exc


def iter_lenses() -> Iterable[LensEntry]:
    """Yield every registered :class:`LensEntry` in :data:`LENS_NAMES` order.

    Provided for the COMP-023 lens validator (T02.15 / T02.16) and for
    ``swarm validate-lenses`` so the validator iterates a single
    canonical sequence regardless of dict-iteration order on older
    Python runtimes.
    """
    for name in LENS_NAMES:
        yield LENSES[name]
