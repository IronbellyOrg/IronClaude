# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Probing the emerging consensus ("FAIL-to-promote; task cannot be marked Done until Step 5.6 wrapper runs and exits 0"). Category 6 (sufficiency_challenge) is always-on because the consensus makes a "fix X (run 5.6) greens outcome Y (Done-eligible)" claim.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | guard_conditions | Consensus assumes `reflect_post` emptiness is the binding guard blocking Done | ADDRESSED | HIGH | task L31 `reflect_post: ""` + L430 "Done must never be marked while the post-reflect wrapper is missing" — guard confirmed present and binding |
| INV-002 | sufficiency_challenge | Consensus implies running Step 5.6 ALONE greens completion | UNADDRESSED | MEDIUM | Step 5.6 exit 0 is necessary but NOT sufficient: Step 5.7 (L430) additionally requires "every prior checklist item complete, final validation passed, no unresolved blocker." Ground truth: validation PASS scoped (L451), blockers "None unresolved" (L463) — so 5.7 CAN proceed after 5.6, but the consensus should state both gates, not just 5.6. Downstream condition that would falsify "5.6 alone is enough": a wrapper exit code of 10/11/2 (L426 halt-precedence). Not HIGH — refines rather than breaks the consensus. |
| INV-003 | state_variables | Consensus assumes the completion-date drift is a genuine state inconsistency, not a benign summary artifact | ADDRESSED | MEDIUM | task L436 (`Completion Date: 2026-07-02`) vs L60 (`completion_date: ""`) — real frontmatter/summary divergence; Variant 1 F#1 captures it |
| INV-004 | interaction_effects | Consensus treats "implementation PASS" and "completion-gate FAIL" as separable | ADDRESSED | LOW | Variant 1's Pass/Fail table explicitly separates implementation PASS from gate-state FAIL — no conflation |

## Summary

- **Total findings**: 4
- **ADDRESSED**: 3
- **UNADDRESSED**: 1
  - HIGH: 0
  - MEDIUM: 1 (INV-002 — sufficiency: consensus should name Step 5.7's additional preconditions, not just 5.6)
  - LOW: 0

**Convergence-gate impact:** 0 HIGH + UNADDRESSED invariants → convergence is NOT blocked by the invariant gate. INV-002 (MEDIUM) is surfaced as a warning and folded into the merged output as a precise "both gates, in order" completion condition so the consensus does not overclaim that 5.6 alone unblocks Done.
