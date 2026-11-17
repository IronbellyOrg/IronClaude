# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | count_divergence | Scoring matrix faithfully records advocate votes | UNADDRESSED->REMEDIATED | MEDIUM | First transcription corrupted S-001/U-002/U-003 R1 columns and V1's R2 picks; three contradictory unanimity counts. Matrix corrected in-place after probe; no majority winner or convergence status changes under corrected counts. |
| INV-002 | collection_boundaries | Every promoted diff point is scored | UNADDRESSED | LOW | diff-analysis declares 10 differences incl. promoted A-001; matrix has 9 rows. A-001 resolved by three prose QUALIFY responses, outside the scored collection. |
| INV-003 | state_variables | U-002 window self-heals (uninterrupted T1->T3 execution, Task 2 lands no sync state) | UNADDRESSED | LOW | A resume-from-interruption between T1 and T3 leaves the repo in the "benign" failing state; concessions not conditioned on uninterrupted execution. |
| INV-004 | state_variables | Landed tree persists to ship though tooling does not enforce it | ADDRESSED | LOW | Mechanism surfaced (sync-dev never writes plugins/), regeneration guard exists (byte-identical tests), all A-001 responses carry the landed-tree qualifier. |
| INV-005 | guard_conditions | tasklist:66 soundly narrows the staging rule | ADDRESSED | LOW | Guard textually grounded (advocate re-read); consistent with the AC-driven executor model used elsewhere; residual (no affirmative stage instruction) is exactly C-001, recorded separately. |
| INV-006 | guard_conditions | Byte-identical mirror tests gate the shipping path | UNADDRESSED | LOW | Test existence treated as enforcement; neither document verifies they run in CI/pre-commit for this change's path. |
| INV-007 | interaction_effects | C-001 and U-001 severities independent | ADDRESSED | LOW | Compound explicitly articulated in V2's R1 steelman and resolved in V2's R2 item 4; residual nit: matrix rows do not cross-reference. |
| INV-008 | interaction_effects | U-005 and U-006 independent | UNADDRESSED | LOW | Jointly: Task 1 has no testable constraint AND no well-defined completion gate; pair never assessed jointly; materiality low (joint severity does not exceed max individual). |
| INV-009 | sufficiency_challenge | All-non-blocking set suffices for a clean verdict unconditionally | UNADDRESSED->PARTIALLY REMEDIATED | MEDIUM | The "execution landed correctly" scope condition appeared only in prose, not the consensus record; a consumer reading only the matrix would conclude unconditional re-executability. SCOPE QUALIFIER now appended to the convergence section. Residual: the qualifier lives in the transcript, not yet in REPORT.md (carried to Wave 5). |

## Summary
- **Total findings**: 9
- **ADDRESSED**: 3 (all LOW)
- **UNADDRESSED at probe time**: 6 (2 MEDIUM: INV-001, INV-009 — both remediated or partially remediated in-transcript after the probe; 4 LOW: INV-002, INV-003, INV-006, INV-008 — recorded, none blocking)
- HIGH unaddressed: 0 — convergence gate PASSES (no HIGH-severity UNADDRESSED items)
