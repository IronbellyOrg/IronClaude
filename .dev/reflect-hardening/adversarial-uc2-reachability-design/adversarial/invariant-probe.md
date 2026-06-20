# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis (against the "C-canonical at 1.6.0, B refactored" consensus)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | interaction_effects | When B (later) and C coexist, the two verdicts never conflict for the same root cause. | UNADDRESSED → addressed-by-decision | HIGH | An unwired feature whose annotated sink is never hit yields C `unreachable`/Regression AND B `UNREACHED`/degrade for the *same* defect. B's "fail-open, does not force Tier 2" posture could mask/soften C's Regression → false-PASS inversion. Requires an explicit precedence invariant. |
| INV-002 | sufficiency_challenge | "Make C canonical at 1.6.0" ALONE resolves M-028/M-029/M-030/M-031/M-042. | UNADDRESSED → addressed-by-decision | HIGH | Necessary, NOT sufficient. Falsifiers: M-028 persists unless B's contract item is re-pointed off 1.6.0; M-029 persists unless B rebases its SKILL.md edits onto post-C baseline; M-030 persists unless C-040's intent is re-expressed as a B-side guard; M-031 persists unless eval ids are re-allocated; M-042 persists unless the M-008 debate adopts the new ownership. Four concrete downstream edits + one debate update are required. |
| INV-003 | count_divergence | B's eval ids 37-41 remain valid. | UNADDRESSED → addressed-by-decision | MEDIUM | B hardcodes "ids 37-41" and "ids 19/20 unchanged". If C registers first at 1.6.0, C consumes the next free ids; B's 37-41 is invalidated and must be re-allocated. |
| INV-004 | guard_conditions | B (at 1.7.0) can edit the protocol freely. | UNADDRESSED → addressed-by-decision | MEDIUM | B must *extend* C's already-shipped 1.6.0 report-template / deviation-taxonomy additively (as C did to 1.5.0), preserving C's real-boot-only Regression semantics — not overwrite them. |
| INV-005 | state_variables | The 1.6.0 slot is free to assign to C. | ADDRESSED | MEDIUM | Verified: git shows tasklists untracked and code unchanged (dirty=0M/12U) — neither contract edit is in-flight, so assigning 1.6.0 to C is currently safe. Re-verify immediately before B/C land if the parallel session has progressed. |
| INV-006 | collection_boundaries | Report rendering handles "both subsystems inactive". | ADDRESSED | LOW | UC-1 omits reachability AND an empty production surface omits runtime_surface → the template must render "nothing to report" for both without implying a defect. Minor rendering hygiene. |

## Summary
- **Total findings:** 6
- **ADDRESSED (at probe time):** 2 (INV-005, INV-006)
- **UNADDRESSED at probe time:** 4 (INV-001, INV-002 HIGH; INV-003, INV-004 MEDIUM)
  - All four are **carried into the decision as binding preconditions** (see refactor-plan.md), moving them to addressed-by-decision. No HIGH item is left silently unaddressed.
- **Convergence impact:** because the two HIGH items are explicitly incorporated as mandatory requirements on the B-refactor / coexistence step, the invariant gate does not block the primary decision (C-canonical). They DO block *immediate* coexistence (Variant 3) — which is an additional reason to sequence rather than union.
