# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | All proposals assume `_REQUIREMENT_PATTERNS` (`spec_parser.py:329`) is stable and complete. If a future requirement family (e.g., `TC-NNN` for test cases) is added, all 5 proposals need an update; none surface this dependency. | UNADDRESSED | MEDIUM | `spec_parser.py:324-330` defines only 5 families. |
| INV-002 | guard_conditions | All proposals assume `canon(spec_id) ∈ canon(roadmap_ids)` ⇒ drift, NOT genuine phantom. A spec using BOTH `D1` and `D-01` simultaneously (intentional distinction) would be collapsed by all canonicalizers; no proposal guards against this. | UNADDRESSED | MEDIUM | Regex `\bD-?\d+\b` at `spec_parser.py:329` matches both forms; no proposal adds collision warning. |
| INV-003 | count_divergence | Fix-2's `_classify_fixability` uses count thresholds (e.g., `>= 2` for `CLASS_DRIFT`) but the threshold is not defined in the proposal — flagged as "calibration choice for adversarial review" in fix-2's grounding gaps. Without a defined threshold, the classifier is non-deterministic. | UNADDRESSED | HIGH | fix-2 grounding-gap line 91: "Did not measure whether the cardinality threshold for `CLASS_DRIFT` should be `>= 2` ... or `>= N`". |
| INV-004 | collection_boundaries | Empty-collection case: if `roadmap_ids` or `spec_ids` is empty, the set difference is well-defined (empty or full). All proposals inherit correct behavior. | ADDRESSED | LOW | Existing `extract_requirement_ids` returns `{}` when no IDs match. |
| INV-005 | interaction_effects | Fix-4 introduces new severity tier `ADVISORY`. Downstream consumers that switch-case on `Finding.severity` may not handle it. Fix-4 acknowledges this risk but does not enumerate consumers. | UNADDRESSED | MEDIUM | fix-4 line 80 acknowledges but doesn't perform consumer audit. |
| INV-006 | sufficiency_challenge | Will ANY of the 5 proposals' fix ALONE green the convergence loop for the TUIBBS artifacts? **YES, all 5** drop the 54 phantom_id HIGHs to 0 (verified by mechanical analysis of `convergence.py:343-357, 539` and the canonicalization semantics in each proposal). | ADDRESSED | HIGH | Mechanical analysis of the pass predicate, the regression check (monotone on structural HIGH count), and each proposal's emission semantics confirms all 5 sufficient. |

## Summary

- **Total findings**: 6
- **ADDRESSED**: 2 (INV-004 LOW, INV-006 HIGH — sufficiency confirmed)
- **UNADDRESSED**: 4
  - HIGH: 1 (INV-003 — fix-2 has undefined threshold; variant-conditional)
  - MEDIUM: 3 (INV-001, INV-002, INV-005)
  - LOW: 0

**AD-1 convergence-gate verdict**: INV-003 (HIGH UNADDRESSED) is variant-conditional — applies only if fix-2's classifier is incorporated. For the broader debate, INV-003 is a penalty input to the base-selection scoring rather than a hard gate. INV-001/002/005 (MEDIUM) are documented as follow-up considerations but do not block convergence.
