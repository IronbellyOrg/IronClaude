"""Cross-skill / cross-module constants — single source of truth (R0.3 + R1.1).

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

- :class:`AdversarialReturn` — frozen-hashable dataclass for the canonical
  sc:adversarial return contract (10 fields per
  ``sc-adversarial-protocol/SKILL.md:432-443``).
- :class:`UnaddressedInvariant` — nested frozen dataclass for the
  ``unaddressed_invariants`` field (keeps the parent hashable per Step 6.2
  instruction).
- :data:`RETURN_CONTRACTS` — per-skill return-type registry per BUILD-REQUEST
  §MVR §5 example ``RETURN_CONTRACTS = {"sc:adversarial": AdversarialReturn}``.
- :data:`THRESHOLDS` — full registry of behavioral float thresholds previously
  inlined as default args / in-function literals across
  ``cli/roadmap/fingerprint.py``, ``cli/roadmap/spec_structural_audit.py``,
  and ``cli/roadmap/gates.py``.

The R0.3 constants are unchanged in R1.1; only the ``__all__`` export list and
the docstring grow. Arch-lint extends to the new names automatically via the
``__all__`` discovery in :mod:`superclaude.tools.arch_lint` (R1.1 also adds a
new ``ClassDef`` rule to catch dataclass shadowing).
"""

from __future__ import annotations

from dataclasses import dataclass
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
# variants in `fidelity_checker.py` — migrated in R1.1 Step 6.3).
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
# the adjacent scalars via :data:`THRESHOLDS` (below). The convergence pair
# itself remains a forward-looking entry awaiting a consumer.
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

# ---------------------------------------------------------------------------
# THRESHOLDS — extended float-threshold registry (R1.1).
#
# Behavioral float thresholds previously inlined as default args / in-function
# literals. Hierarchical dotted keys (`module.metric`) keep the registry
# future-extensible without nested dicts.
#
# Current entries (per phase-outputs/discovery/return-contracts-scope.md §E):
#   * "fingerprint.coverage_min" — was `min_coverage_ratio: float = 0.7` at
#     `cli/roadmap/fingerprint.py:171,205` and `>= 0.7` literal at
#     `cli/roadmap/gates.py:375` (Phase 6 D3 finding — missed by Phase 4
#     inventory).
#   * "structural_audit.adequacy_min" — was `threshold: float = 0.5` at
#     `cli/roadmap/spec_structural_audit.py:91`.
#
# Distinct from :data:`CONVERGENCE_THRESHOLDS` (per-skill ``(high, low)`` pair):
# THRESHOLDS holds single-scalar tunables used as default arguments or gate
# comparators inside individual modules.
# ---------------------------------------------------------------------------
THRESHOLDS: Final[dict[str, float]] = {
    "fingerprint.coverage_min": 0.7,
    "structural_audit.adequacy_min": 0.5,
}


# ---------------------------------------------------------------------------
# UnaddressedInvariant — nested dataclass for AdversarialReturn.
#
# Shape per sc-adversarial-protocol/SKILL.md:460 — each item in
# ``unaddressed_invariants`` is ``{id, category, assumption, severity}``.
# Frozen so the parent ``AdversarialReturn`` stays hashable (Step 6.2 invariant).
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class UnaddressedInvariant:
    """A HIGH-severity UNADDRESSED item from the sc:adversarial invariant probe.

    Fields per ``sc-adversarial-protocol/SKILL.md:460``.
    """

    id: str
    category: str
    assumption: str
    severity: str


# ---------------------------------------------------------------------------
# AdversarialReturn — canonical sc:adversarial return contract.
#
# Verbatim from sc-adversarial-protocol/SKILL.md:432-443 + field table at
# L449-460. Frozen + hashable per Step 6.2 instruction.
#
# Field nullability mirrors the prose: fields that the skill cannot determine
# (pipeline aborted before reaching that step) are typed ``X | None``.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class AdversarialReturn:
    """The sc:adversarial return contract.

    See ``sc-adversarial-protocol/SKILL.md:425-460`` for the verbatim shape.
    sc:adversarial MUST write this contract on every invocation, including
    failures. Fields unreachable at abort time are ``None``.

    The ``status`` enum is one of ``"success"``, ``"partial"``, ``"failed"``.
    The ``failure_stage`` enum is ``None`` on success, otherwise one of
    ``"variant_generation"``, ``"debate"``, ``"merge"``, ``"validation"``,
    ``"transport"``.
    The ``invocation_method`` enum is one of ``"skill-direct"``,
    ``"task-agent"``, ``"manual"``.
    """

    merged_output_path: str | None
    convergence_score: float | None
    artifacts_dir: str
    status: str
    base_variant: str | None
    unresolved_conflicts: int
    fallback_mode: bool
    failure_stage: str | None
    invocation_method: str
    unaddressed_invariants: tuple[UnaddressedInvariant, ...]


# ---------------------------------------------------------------------------
# RETURN_CONTRACTS — per-skill return-type registry.
#
# Per BUILD-REQUEST §MVR §5 example: ``RETURN_CONTRACTS = {"sc:adversarial":
# AdversarialReturn}``. Keys are canonical skill names matching
# ``~/.claude/commands/sc/<name>.md``.
#
# Only sc:adversarial has a programmatic, parseable return contract today
# (per phase-outputs/discovery/return-contracts-scope.md §B). Additional
# skills are added here as they migrate to the SoT pattern — no speculative
# entries.
# ---------------------------------------------------------------------------
RETURN_CONTRACTS: Final[dict[str, type]] = {
    "sc:adversarial": AdversarialReturn,
}


__all__ = [
    "ID_PATTERNS",
    "CONVERGENCE_THRESHOLDS",
    "GATE_FIELD_NAMES",
    "THRESHOLDS",
    "UnaddressedInvariant",
    "AdversarialReturn",
    "RETURN_CONTRACTS",
]
