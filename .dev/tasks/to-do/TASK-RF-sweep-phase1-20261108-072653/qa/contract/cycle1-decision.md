# Cycle-1 decision (item 12.17)

Inputs: `verify-cycle1-rf-qa.md` (Verdict: PASS, Blocking count: 0), `verify-cycle1-rf-qa-qualitative.md` (Verdict: PASS, Blocking count: 0), `consolidated-findings-cycle0.md` (`F_0`, `|F_0|`) and `cycle-ledger.md` (the cycle-0 PASS set).

## F_1 and the cycle-1 PASS set

- `F_0` = {CON-F1, CON-F2}; `|F_0|` = 2.
- Marked OPEN by either verifier: none. Both verifiers mark both ids RESOLVED. New BLOCKING or MAJOR findings reported by either verifier: none (both Blocking counts are 0). Notes and follow-up candidates of the two verifiers never enter `F_1`.
- `F_1` = {} (the empty set).
- `|F_1|` = 0
- Cycle-1 PASS set: 82 check ids, every cycle-0 PASS check id, each marked PASS by both verifiers; listed in full in the section "Cycle-1 PASS set" at the end of this file and in the cycle-1 row of `cycle-ledger.md`.

## Halt checks, in order

- Regression: no check id of the cycle-0 PASS set is FAIL in either cycle-1 verifier report (0 FAIL rows in both reports; all 82 ids present in both).
- Monotonicity: `|F_1|` is 0, below `|F_0|` of 2, so the halt does not apply.

## Outcome

PASS at cycle 1

Items 12.18 to 12.20 are marked complete as SKIPPED.

## Cycle-1 PASS set

qa-contract-rule-report:C1 (item 12.6), qa-contract-rule-report:C2 (item 12.6), qa-contract-rule-report:C3 (item 12.6), qa-contract-rule-report:C4 (item 12.6), qa-contract-rule-report:C5 (item 12.6), qa-contract-rule-report:C6 (item 12.6), qa-contract-rule-report:C7 (item 12.6), qa-contract-rule-report:C8 (item 12.6), qa-contract-rule-report:C9 (item 12.6), qa-contract-rule-report:C10 (item 12.6), qa-contract-rule-report:C11 (item 12.6), qa-contract-rule-report:C12 (item 12.6), qa-contract-rule-report:C13 (item 12.6), qa-contract-rule-report:C14 (item 12.6), qa-contract-rule-report:C15 (item 12.6), qa-test-pins-report:C1 (item 12.7), qa-test-pins-report:C2 (item 12.7), qa-test-pins-report:C3 (item 12.7), qa-test-pins-report:C4 (item 12.7), qa-test-pins-report:C5 (item 12.7), qa-test-pins-report:C6 (item 12.7), qa-test-pins-report:C7 (item 12.7), qa-test-pins-report:C8 (item 12.7), qa-test-pins-report:C9 (item 12.7), qa-test-pins-report:C10 (item 12.7), qa-test-pins-report:C11 (item 12.7), qa-test-pins-report:C12 (item 12.7), qa-test-pins-report:C13 (item 12.7), qa-r7-guide-report:C1 (item 12.8), qa-r7-guide-report:C2 (item 12.8), qa-r7-guide-report:C3 (item 12.8), qa-r7-guide-report:C4 (item 12.8), qa-r7-guide-report:C5 (item 12.8), qa-r7-guide-report:C6 (item 12.8), qa-r7-guide-report:C7 (item 12.8), qa-r7-guide-report:C8 (item 12.8), qa-r7-guide-report:C9 (item 12.8), qa-r7-guide-report:C10 (item 12.8), qa-r7-guide-report:C11 (item 12.8), qa-r7-guide-report:C12 (item 12.8), qa-r7-guide-report:C13 (item 12.8), qa-r7-guide-report:C14 (item 12.8), qa-coordinator-cadence-report:C1 (item 12.9), qa-coordinator-cadence-report:C2 (item 12.9), qa-coordinator-cadence-report:C3 (item 12.9), qa-coordinator-cadence-report:C5 (item 12.9), qa-coordinator-cadence-report:C6 (item 12.9), qa-coordinator-cadence-report:C8 (item 12.9), qa-coordinator-cadence-report:C9 (item 12.9), qa-coordinator-cadence-report:C11 (item 12.9), qa-coordinator-cadence-report:C13 (item 12.9), qa-coordinator-cadence-report:C14 (item 12.9), qa-reader-clarity-report:C1 (item 12.10), qa-reader-clarity-report:C2 (item 12.10), qa-reader-clarity-report:C3 (item 12.10), qa-reader-clarity-report:C10 (item 12.10), qa-reader-clarity-report:C11 (item 12.10), qa-reader-clarity-report:C12 (item 12.10), qa-reader-clarity-report:C13 (item 12.10), qa-reader-clarity-report:C14 (item 12.10), qa-conventions-report:C1 (item 12.11), qa-conventions-report:C6 (item 12.11), qa-conventions-report:C8 (item 12.11), qa-conventions-report:C11 (item 12.11), qa-conventions-report:C12 (item 12.11), qa-conventions-report:C13 (item 12.11), qa-conventions-report:C14 (item 12.11), qa-master-contract-report:C1 (item 12.12), qa-master-contract-report:C2 (item 12.12), qa-master-contract-report:C3 (item 12.12), qa-master-contract-report:C4 (item 12.12), qa-master-contract-report:C5 (item 12.12), qa-master-contract-report:C6 (item 12.12), qa-master-contract-report:C7 (item 12.12), qa-master-contract-report:C8 (item 12.12), qa-master-contract-report:C9 (item 12.12), qa-master-contract-report:C10 (item 12.12), qa-master-contract-report:C11 (item 12.12), qa-master-contract-report:C12 (item 12.12), qa-master-contract-report:C13 (item 12.12), qa-master-contract-report:C14 (item 12.12), qa-master-contract-report:C15 (item 12.12)
