# Gate 5 cycle control (Items 6.62 and 6.67)

Date: 2026-11-14

## Inputs read (Item 6.62)

- `qa/qa-anti-omission-consolidated-findings.md`: `F_0 = 0`, verdict PASS. Review 1 Item Status: all report sections PASS (0 blocking omissions). The four Gate 5 reports (agents 1 to 4) are each `Status: Complete`, verdict PASS, 0 blocking under the grading override. The independent recount found one process finding, `P6A-RC-1` (agent 2, `synth-04-external-findings.md`: enumerated 145 against a recount of 182, below the 0.9 line of 163.8). Agent 2's whole partition was re-run (`qa/qa-anti-omission-report-2-rerun.md`, `qa/qa-anti-omission-enumeration-2-rerun.md`); the recount of the rerun reached 176 against 182 (0.967 of the recount) for `synth-04`, and 1685/1685 and 868/868 for the two ledgers, so `P6A-RC-1` is CLOSED-BY-RERUN under the rule of Item 6.58 and is not counted in `F_0`.
- `qa/qa-anti-omission-fix-log-c1.md`: `No fix required: zero blocking omissions at review 1`.
- `qa/qa-anti-omission-verification-structural-c1.md` and `qa/qa-anti-omission-verification-content-c1.md`: both `Skipped: no fix required (F_0 = 0)`, so each counts as `F_1 = 0`.

## Computation

- `F_0 = 0`.
- `F_1 = 0` (union of the two skipped verifications, deduplicated; `P6A-RC-1` is CLOSED-BY-RERUN and is not open).

## Decision, in the required order

1. REGRESSION: no report section that was PASS at review 1 has a blocking finding now (no fix was applied). Regression list: none. Rule not fired.
2. MONOTONICITY: `F_1 = 0`, so the condition `F_1 > 0 and F_1 >= F_0` is false. Rule not fired.
3. PROCEED: `F_1 = 0`.

PASS at review 2

Rule that fired: proceed (`F_1 = 0`). Next action: items 6.63-6.67 are skipped (each writes its skip note), then the final validation (Item 6.68).

Code-derived recovered claims verified against code (copied from each verification report):

- Structural verification (c1): `RECOVERED_VERIFIED_AGAINST_CODE=0 of 0` (skipped; no claim was recovered).
- Content verification (c1): `RECOVERED_VERIFIED_AGAINST_CODE=0 of 0` (skipped; no claim was recovered).
- Sum: 0 of 0 (no code-derived recovered claim exists, so none is counted open in `F_1`).

Grading note: grading override (`qa/grading-override.md`) applied at Gate 5; blocking omissions are those that meet its three conditions. The minor omissions of the four agents (10, 81, 46 plus 13 pair-check notes, 5) are follow-up notes only (never fixed, never rechecked).

## Item 6.67 (cycle 2 control and final verdict)

Cycle 2 skipped; Gate 5 verdict PASS

Recorded: F_0 = 0, F_1 = 0, F_2 = not computed (cycle 2 not run). Regression list: none. Rule that fired: proceed (PASS at review 2). Cycle 2 verification lines: `RECOVERED_VERIFIED_AGAINST_CODE=0 of 0` (structural c2, skipped), `RECOVERED_VERIFIED_AGAINST_CODE=0 of 0` (content c2, skipped); sum 0 of 0. Next action: final validation (Item 6.68).
