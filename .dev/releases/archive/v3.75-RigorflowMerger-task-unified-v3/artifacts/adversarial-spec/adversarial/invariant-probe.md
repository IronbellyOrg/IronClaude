# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

The fault-finder agent probed the emerging consensus from Round 2 against the 5-category boundary-condition checklist.

**Emerging consensus probed:** Ship TU-001/003/004/007 task-side + SE-001..005 sprint-side + TUI top-5; defer TU-002/005/006/Q1/Q2/SE-006; preserve carry-overs; introduce limited migration-guide-addressable breaks; deterministic BLOCKED state replaces soft prompt; classification header schema extends to include BLOCKED.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | Carry-over strings (`SC:TASK-UNIFIED:CLASSIFICATION`, `--caller task-unified`) are state that persists across this release; no consensus position documents what `/sc:forensic` actually does with the string. | ADDRESSED | MEDIUM | Variant A §4.2 acknowledges A-005 unresolved; Variant C §8.2 promotes A-005 to gating investigation. Consensus position is "preserve verbatim until A-005 clears." |
| INV-002 | guard_conditions | When TU-004 introduces the deterministic BLOCKED state, in-flight tasks that were classified under the old soft-prompt may have ambiguous behavior. No variant specifies behavior for tasks that started under old behavior but cross a release boundary. | UNADDRESSED | MEDIUM | Round 2 transcripts: none of A/B/C address in-flight task behavior at release-boundary transition. This is an implementation detail, not a spec-level guard. |
| INV-003 | collection_boundaries | The mandatory completion checklist (TU-007) is presented as 6 conditions across all variants, but the LW source verification is `[inference]`. If the canonical list has a different count, the empty-collection (zero-condition) or single-element (one-condition) edge cases are undefined. | ADDRESSED | LOW | Variant C §5.3 parameterizes tests over investigation output, handling any condition count >= 1. A and B's placeholder lists implicitly assume count = 6. C's approach mitigates the unknown-count risk. |
| INV-004 | interaction_effects | TU-001 #3 (missing classification header → FAIL) and TU-004 (deterministic BLOCKED header emission) interact at the header-output point: if a task is on the BLOCKED branch, does the header it emits satisfy TU-001 #3 or fail it? | ADDRESSED | LOW | Consensus position: BLOCKED is a valid TIER value in the extended header schema. A header containing `TIER: BLOCKED` satisfies the "header present" condition of TU-001 #3. INV-004 interaction is non-conflicting; documented in merged output §3.5. |
| INV-005 | interaction_effects | The audit log (Q11) is written from multiple call sites: TU-001 CRITICAL FAIL, TU-004 BLOCKED override, `--skip-compliance` usage. No variant specifies write-ordering or atomicity guarantees when two of these fire on the same task. | UNADDRESSED | MEDIUM | Audit log infrastructure specs in A/B/C describe append-only semantics but not ordering across multiple write paths in the same task lifecycle. Mitigation: implementation-level (use a single mutex'd writer); not a spec-level invariant. |

## Summary

- **Total findings:** 5
- **ADDRESSED:** 3 (INV-001, INV-003, INV-004)
- **UNADDRESSED:** 2 (INV-002, INV-005)
  - **HIGH:** 0
  - **MEDIUM:** 2 (INV-002, INV-005)
  - **LOW:** 0

## Convergence gate decision

- HIGH-severity UNADDRESSED count: **0**
- **Gate: PASSES.** Convergence is not blocked by invariant violations.
- MEDIUM-severity items are logged as warnings; recommended for implementation-phase resolution but do not block release-spec adoption.

## Recommendations for merged spec

1. **INV-002:** Add a one-line implementation note to §3.5 of the merged spec: "Tasks that started before TU-004 deployment continue under their original classification; the BLOCKED state applies only to tasks initiated after deployment."
2. **INV-005:** Add a one-line audit log contract to the merged spec's §3.7/3.8 audit log section: "Audit log writes within a single task lifecycle MUST be serialized through a single writer; ordering is preserved per-task, not globally."
3. **INV-004:** No spec change needed; already addressed by extending TIER enum to include BLOCKED.
