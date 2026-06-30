# A.10 Consolidated Structural Findings — TASK-RF-submit-pr-20260611-030241

Source reports: `qa-task-validation-b2-report.md` (VERDICT: PASS), `qa-task-validation-structure-report.md` (VERDICT: FAIL).
Fix authorization: a SINGLE fix agent applies ALL items below (I20 serialized).

## MUST-FIX

### F1 (IMPORTANT) — Stale/nonexistent phase references misdirect the proceed-path
- **Step 2.6** (~L214): on FAIL says "re-run Step 2.5 before proceeding to **Phase 3**" — there is NO Phase 3 (the next stage is **Phase Gate A → Phase 4**). Replace the forward target with the actual next stage (Phase Gate A / Phase 4).
- **Step 11.6** (~L416): writes "**Phase 12** final QA authorized" — there is NO Phase 12; the final QA stage is **Phase Gate B**. Replace "Phase 12" with "Phase Gate B".
- **Step 2.6 PASS branch** (~MINOR, fold in): the "Phase 4+ AUTHORIZED" wording implies Step 2.6 is the authorizer when **Phase Gate A** is the real downstream authorizer. Reword so the L5 contract-verdict gate's PASS reads as "Phase 2 DET contract locked-for-build; Phase Gate A may proceed" rather than implying it authorizes Phase 4 directly. Keep the L5 gate mechanics intact.

## SHOULD-FIX (MINOR, actionable)

### F2 (MINOR) — Undocumented Python-enum state-name adaptation
The `models.py` state enum uses `S4_HALT_BEFORE_PUSH` (correct — the spec's primed `S4'_HALT_BEFORE_PUSH` apostrophe is an illegal Python identifier char), while prose/refs use `S4'_HALT_BEFORE_PUSH`. This is a legitimate adaptation but is undocumented. Add a one-line note to `## Execution Context` Key Constraints (or the Deviations log) stating: "Python state enums drop the prime: spec `S4'_HALT_BEFORE_PUSH` → enum `S4_HALT_BEFORE_PUSH` (apostrophe illegal in identifiers); refs/prose retain the primed spec name." This pre-empts a false internal-consistency flag at Phase Gate B.

### F3 (MINOR) — Forward-dependency reconciliation note (2.4 ↔ Phase 10 fixtures)
Step 2.4's classifier/detection test uses an inline payload; the durable fixtures land in Phase 10. Add a short note to Step 2.4 (or the relevant Phase 10 fixture item) that the inline payload is provisional and the Phase 10 fixture set supersedes it (so the executor swaps, not duplicates).

## ACCEPT AS-IS (no change)
- B2 minor: QA-gate spawn items paraphrase the lens prompt rather than embedding byte-verbatim. ACCEPTED — items are self-contained and this matches project convention (memory `feedback_rfqa_adversarial_pattern`); do NOT expand to verbatim.
- B2 minor: Step 5.1 ref+module+__init__ coupling and Step 4.3 dual-path `remap_severity` re-export — both branches fully specified; leave as-is unless the F1 edits touch them.

## VERIFICATION AFTER FIX
Re-read Steps 2.4, 2.6, 11.6, the Execution Context Key Constraints block, and the Deviations log. Confirm: no reference to a nonexistent "Phase 3" or "Phase 12" remains; the L5 gate proceed-targets name real stages (Phase Gate A / Phase Gate B); the state-enum deviation is documented; the L5 gate mechanics are unchanged.
