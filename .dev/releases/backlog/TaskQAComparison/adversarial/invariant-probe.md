# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | All 3 variants assume the fix-or-flag binary is exhaustive — every QA finding is either auto-fixable or human-flag-worthy | UNADDRESSED | MEDIUM | None of the three define a third "needs-human-adjudication" state at the QA-finding level. V2 has Open Questions but only for research-gap failures; V3 has user adjudication only for tests-are-wrong. |
| INV-002 | guard_conditions | QA agent's claims that file:line X exists actually correspond to on-disk state (citation accuracy) | PARTIALLY ADDRESSED by V2 (AX-5 invented-content axis) | HIGH | V1 and V3 have no evidence-validator final gate. sc-reflect-protocol §11.2 has this as mandatory non-negotiable. Hallucinated findings would be auto-fixed under V1's fix_authorization:true potentially introducing bugs. Shared assumption A-002 formalises this gap. |
| INV-003 | count_divergence | V2's 3 gates produce strictly-decreasing marginal value (not actual diminishing returns) | UNADDRESSED | LOW | No empirical fold/cost data cited. V2's orthogonality claim survives Round 2 rebuttal but is not empirically validated. |
| INV-004 | collection_boundaries | Zero-output tasks (e.g., task that only updates frontmatter) handled correctly | PARTIALLY ADDRESSED by V1 (Phase 1 exemption) and V3 (EXEMPT tier), UNADDRESSED by V2 | LOW | V2's A.10/A.10.5 don't address zero-output edge case explicitly. |
| INV-005 | interaction_effects | When V1's phase-gate QA + V3's TFEP fire on the same task (composed pipeline), the interactions are well-defined | UNADDRESSED | MEDIUM | A `/task` execution could internally invoke `/sc:task` per-item. The interaction (does V1's phase-gate run after V3's TFEP? before? in parallel?) is not defined in any of the three skills. |
| INV-006 | sufficiency_challenge | The QA-finding-resolved verdict actually correlates with absence of the underlying defect (not just absence of the surface signal the QA agent looked for) | UNADDRESSED across all 3 variants | HIGH | The R0 PR #112 memory provides empirical falsification: inline rf-qa's fix passed inline-rf-qa's surface signal but missed the underlying defect that `/sc:reflect --mode post` caught (2 blindspots in M8 + M9). None of the three variants has a structural mechanism to detect this class of failure. |
| INV-007 | state_variables | Sub-agent verification crash / malformed output handled with graceful degradation | ADDRESSED by V2 (DNSP synthetic-finding protocol), PARTIALLY ADDRESSED by V1 (single-instance failure → defer to user), UNADDRESSED by V3 (forensic-ladder triggers on test failures but not on QA-agent crashes) | HIGH | V2's DNSP is the most rigorous handling of this case. V1 and V3 should adopt or document equivalent. |

## Summary

- **Total findings**: 7
- **ADDRESSED**: 1 (INV-007 in V2 only)
- **PARTIALLY ADDRESSED**: 3 (INV-002 by V2; INV-004 by V1+V3; INV-007 by V1+V2)
- **UNADDRESSED**: 4 (INV-001, INV-003, INV-005, INV-006)
- **By severity (UNADDRESSED)**:
  - HIGH: 2 (INV-002 outside V2; INV-006 across all 3)
  - MEDIUM: 2 (INV-001, INV-005)
  - LOW: 1 (INV-003)

## Convergence-Gate Impact

INV-006 is HIGH-severity UNADDRESSED across **all three variants**. Per protocol §convergence_detection.invariant_probe_gate, this BLOCKS convergence regardless of diff-point agreement score:

> CONVERGENCE BLOCKED: 1 HIGH-severity UNADDRESSED invariant(s) detected
> Blocking items: INV-006 (sufficiency_challenge — calibrator-disjoint-set / self-confirmation-bias gap)
> Evidence: R0 PR #112 memory entry `feedback_sc_reflect_vs_inline_rfqa.md`
> Action: Address the flagged item by adding an out-of-context independent verifier — `/sc:reflect --mode post` — between or after each inline QA cycle.

The gap is empirically demonstrated (R0 PR #112 inline rf-qa missed 2 blindspots; `/sc:reflect --mode post` caught both) and structurally absent in all three variants. This is not a failure of any one variant — it is a shared-assumption blindspot none of the three's QA-architectures alone fills.

The merged recommendation MUST add the missing structural mechanism to resolve INV-006 and downgrade A-001 from UNSTATED to ADDRESSED.
