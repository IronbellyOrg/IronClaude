# Refactor Plan (Step 4)

Base: Variant 3 (reviewer-3 card). Merge target: `merged-verdict.md` — the panel's unified findings-v2 card that Wave 5 consumes.

## Planned Changes

1. **Fold R3 F2 into F1 at MAJOR** (fold conceded Round 1, ratified Round 2 point 1). Source: R3 F1+F2, R1 F1 citations. Target: merged finding M1. Risk: Low.
2. **Correct M1's sufficiency chain per INV-001** (MEDIUM, mandatory): a literal fresh execution rewrites tests+text to agree (byte-identical instruction, tasklist:44) and fails AC1 "no existing test is changed" (tasklist:53); against today's on-disk tests, Task 2's gate (tasklist:66) fails via the harness-block test (test:459) and old-summary test (test:482). Keep template-reuse as the second harm path. Drop the unsupported "fails Task 1 AC" headline reading. Risk: Low.
3. **Reword the non-blocking rationale per INV-007** (LOW): replace "documentation-level staleness only" with the QUALIFY'd form — non-blocking because the package is archived and no execution is pending; template reuse remains a live harm path. Risk: Low.
4. **Split C-002 into two dispositions per INV-003** (MEDIUM, mandatory): M2 = authorized expansion, INFO (spec:1 vs tasklist:20); M3 = matrix-record defect, MINOR (R2 F1: INF-003 records neither Task 3's SKILL.md edit nor Task 1's early-section addition). Risk: Low.
5. **Keep U-001 as M4 MINOR with INV-005 repair** (LOW): matrix-record observation stands (bundled spans in one row); drop the "loosely verified" leg — byte-exact pinning (tasklist:22/29, enforced test:281-287) verifies all spans jointly, which is stronger. Risk: Low.
6. **Keep U-002 as M5 INFO with INV-006 repair** (LOW): correct the rationale — the red log DOES show all three per-agent failures + the SKILL positive failure (t1-red.log:11-15) and rc=1 (:90); what is absent are the two negative tests, deselected by the -k filter, which is AC-compliant (tasklist:54). Risk: Low.
7. **Keep U-003 as M6 INFO with INV-002 + INV-004 repairs** (LOW): count corrected to 4 live byte-identical copies (3 agent files + the test constant; 7 with .claude/ sync mirrors); cause corrected to cross-package supersession (same-day rename package TASK-WF-renameTheScIssue-20261104-174359), not plan-internal error. Risk: Low.
8. **Keep U-004 as M7 INFO with INV-008 repair** (LOW): add the observable effect — the Task 2 gate executor mislabeled the two failing SKILL.md tests as `test:unrelated-red` (t2-green.log:75, progress.md T2 line), evidence the phrase "Task 1 agent tests" under-specifies which tests the gate covers. Risk: Low.

## Changes NOT Being Made

- Dropping R2's card despite lowest calibration: rejected — it contributes the panel's only matrix-integrity and evidence-visibility findings (advocates 1 and 3 both endorsed).
- Demoting M1 to MINOR (R1's Round-1 position): rejected post-R2 — R1 itself shifted to MAJOR; a severity anchored to a verified contradiction beats one anchored to a forecast.
- Classifying M6 as a deviation: rejected — duplication is spec-inherited design, INFO context only (unanimous).
- Re-running the test suite to prove the failure joints: rejected — the failures follow from text-vs-text comparison of pinned constants; INV-001's corrected chain cites the exact asserting lines instead.

## Review Status

Auto-approved (non-interactive).
