"""Cross-skill / cross-module constants — single source of truth (R0.3).

This module is the **source of truth** for cross-skill / cross-module constants.
Per Contract #5 + #8 (master:§Recurrence #7 + master:§Flaw 5), no other module
may redefine these constants — ``make lint-architecture`` enforces this via
:mod:`superclaude.tools.arch_lint`.

The R0.3 surface lands the minimal constant set per BUILD-REQUEST §R0 item 3 +
§MVR §5:

- :data:`ID_PATTERNS` — requirement-ID regex bodies per family (FR/NFR/SC/G/D).
- :data:`CONVERGENCE_THRESHOLDS` — per-skill ``(high, low)`` convergence pair
  per BUILD-REQUEST §MVR §5 example.
- :data:`GATE_FIELD_NAMES` — canonical frontmatter field names that gate
  predicates consume (the ``ambiguous_deviations`` key being the most-cited
  per master:§Flaw 5 prose-vs-impl alignment hazard).

R1.1 (Phase 6 in the task) extends this module with:

- ``RETURN_CONTRACTS`` — per-skill return-type schemas (e.g. the
  ``AdversarialReturn`` shape per §MVR §5).
- A full threshold registry (fingerprint min_coverage_ratio,
  structural-audit threshold, etc.) reconciling the adjacent scalars that
  currently live in ``cli/roadmap/fingerprint.py``, ``spec_structural_audit.py``,
  and ``gates.py``.

The TODO comment on :data:`ID_PATTERNS` flags the G-family deviation from the
BUILD-REQUEST §MVR §5 illustrative shape (which lists only FR/NFR/SC/D); G is
required to honor Contract #8 against the pre-existing
``spec_parser.py:328`` extractor.
"""

from __future__ import annotations

from typing import Final

# ---------------------------------------------------------------------------
# ID_PATTERNS — requirement-ID regex bodies per family.
#
# Deviation from BUILD-REQUEST §MVR §5 illustrative shape (intentional, logged
# in phase-outputs/discovery/contracts-consumer-sites.md §E):
#   * G-family added — required to honor Contract #8 against the pre-existing
#     extractor at `cli/roadmap/spec_parser.py:328` (Phase 2 D1 informational
#     deviation).
#   * NFR pattern is the broader `r"NFR-\d+(?:\.\d+)?"` (BUILD-REQUEST is
#     `r"NFR-\d+"`). The broader pattern preserves existing spec corpora
#     that legitimately use `NFR-N.M` sub-IDs (e.g., sc-reflect spec).
#     R1.1 reconciles by either widening the SoT or adding an
#     `NFR_SUB` family — see contracts-consumer-sites.md §E.
#
# Pattern bodies do NOT include word-boundary anchors `\b…\b`. Consumers that
# need anchored matching (e.g. `spec_parser._REQUIREMENT_PATTERNS`) wrap with
# `\b{ID_PATTERNS["FR"]}\b` at compile time. Keeping bodies anchor-free keeps
# the SoT regex composable for non-word-boundary contexts (heading-anchored
# variants in `fidelity_checker.py` — deferred to R1.1).
# ---------------------------------------------------------------------------
ID_PATTERNS: Final[dict[str, str]] = {
    "FR": r"FR-\d+(?:\.\d+)?",
    "NFR": r"NFR-\d+(?:\.\d+)?",  # broader than BUILD-REQUEST verbatim — see §E
    "SC": r"SC-\d+",
    "G": r"G-\d+",  # added per Phase 2 D1 deviation — see header comment
    "D": r"D-?\d+",
}

# ---------------------------------------------------------------------------
# CONVERGENCE_THRESHOLDS — per-skill ``(high, low)`` convergence threshold pair.
#
# Per BUILD-REQUEST §MVR §5 example. R0.3 lands the registry as a
# forward-looking SoT entry (no consumer currently reads the pair — adjacent
# scalars like `min_coverage_ratio` and `threshold` live in
# `cli/roadmap/fingerprint.py` / `spec_structural_audit.py`). R1.1 reconciles
# via the extended threshold registry.
#
# Semantics (per §MVR §5):
#   * first element = high-bound (target convergence threshold)
#   * second element = low-bound (regression floor)
# ---------------------------------------------------------------------------
CONVERGENCE_THRESHOLDS: Final[dict[str, tuple[float, float]]] = {
    "sc:roadmap": (0.7, 0.5),
    "sc:release-split": (0.7, 0.5),
}

# ---------------------------------------------------------------------------
# GATE_FIELD_NAMES — canonical frontmatter field names that gate predicates
# consume. Centralizing these names eliminates the
# ``ambiguous_count``/``ambiguous_deviations`` field-mismatch class of bug
# documented at `cli/roadmap/gates.py:18` (B-1).
# ---------------------------------------------------------------------------
GATE_FIELD_NAMES: Final[dict[str, dict[str, str]]] = {
    "deviation_analysis": {
        "ambiguous": "ambiguous_deviations",
    },
}

__all__ = [
    "ID_PATTERNS",
    "CONVERGENCE_THRESHOLDS",
    "GATE_FIELD_NAMES",
]
