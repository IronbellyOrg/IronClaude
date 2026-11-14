# Refactor Plan Fix Log, Cycle 1

- Plan: `refactor-plan.md`
- Review: `refactor-plan-review.md` (VERDICT: FAIL)
- Date: 2026-11-08
- Scope: only the plan file was edited. F-01, the F-02 grep pattern, all severities and all coverage numbers are unchanged.

| id | What changed | Where |
|----|--------------|-------|
| B-01 | Step 1 of the new 7.17 branch now writes `phase-outputs/plans/OQ-<n>-<topic>-decision.md` in the TL 1142 form (`needs_human_decision: true`, `status: PENDING`, question, options, empty `OPERATOR DECISION:`, `Chosen:`, `Decided by:`, `Decision source:`), then appends a PENDING Execution Log row for 7.17, then HALTs before step 1.2 (TL 1142 Branch 1). The OQ-8 field names "Given by, Source" were removed. The resume step now fills that decision file and applies TL 1142 Branch 2 over it. The success test now checks the decision file exists with `status: PENDING`, exactly one PENDING row for 7.17, and the HALT. | Change 3, recommendation steps 1 and 3 and the success test |
| M-01 | The refusal path no longer cites INV-016. It cites INV-021's "If the owner declines, the plan works", records the refusal in `phase-outputs/discovery/1.0a-facts.md` as "cursor field present, no cursor template; the DESIGN 973 full-page lower bound applies", and states that 8.10 then keeps `ALLOWED_ORCA` at exactly 10, does not page by the cursor field, and treats a full page as truncated with a lower-bound total (TL 1482, TL 1485, DESIGN 973). | Change 3, recommendation step 3 |
| M-02 | Not changed; left as a review note, as the caller directed. | none |
| M-03 | The reason for rejecting "drop the append" was corrected: TL 2804 asks for one row per decision and TL 2802 already is that row. The chosen fix is kept because it leaves item 6.2 a checkable action, with the 6.2 row as an item-level record next to the build-time row. | Change 2, Risk; Changes NOT Being Made, row "INV-006 options" |
| M-04 | One note added: run the pattern with plain `grep`, never `-E`, and separate the appended row's cells with a pipe that has a space on each side. | Change 2, after the orchestrator check line |
| M-05 | Not changed; left as a review note, as the caller directed. | none |
| M-06 | Not changed; left as a review note, as the caller directed. | none |
| M-07 | Three `not_carried` rows added for INV-001, INV-002 and INV-017, each ADDRESSED, LOW, no gap, with the probe's evidence as the rationale. | Changes NOT Being Made table, after the INV-004 row |
