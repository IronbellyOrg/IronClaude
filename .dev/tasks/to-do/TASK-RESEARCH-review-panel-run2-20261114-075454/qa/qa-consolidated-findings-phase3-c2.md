# Gate 1 Review 2 - Consolidated Findings (Phase 3, fix cycle 2 input)

Task: TASK-RESEARCH-review-panel-run2-20261114-075454, Item 3.21
Sources: `qa/qa-consolidated-findings-phase3.md` (review 1, F_0 = 11), `qa/qa-verification-structural-phase3-c1.md` (VERDICT: FAIL, F_1 = 2), `qa/qa-verification-content-phase3-c1.md` (VERDICT: PASS, F_1 = 0), `qa/gate1-cycle-control.md` (decision: FAIL at review 2, continue with fix cycle 2).
Status: Complete

## Result of fix cycle 1

All 11 blocking findings of review 1 (P3-001 to P3-010 and P3-013) were verified FIXED by both verifiers. Two NEW blocking findings were introduced by the fix itself (both in value-ledger table rows). No finding from table 1b (carried to item 5.08 by owner decision) or table 1c (minor) is in scope.

## Blocking findings STILL-OPEN or NEW after fix cycle 1

| ID | Severity | Blocking | File | Location | Finding | Evidence | Proposed fix | Originating reports |
|----|----------|----------|------|----------|---------|----------|--------------|---------------------|
| P3-C2-001 | IMPORTANT | Y | research/24-value-ledger-evidence-consumers.md | row VL-24-211 (L224) | NEW, introduced by the P3-007 fix. The row has an unescaped `|` inside a backticked command, so it has 8 unescaped pipes instead of 7 and the Destination cell reads wrong. Destination is the field the value inventory (one destination per item) is built from. | structural verification report: pipe count of the row is 8; every other `| VL-24-` row has 7. | Escape the pipe inside the backticked command as `\|` (or rephrase the command without a pipe), then re-run the pipe count: every `| VL-` row in ledgers 19-24 must have exactly 7 unescaped pipes. | qa-verification-structural-phase3-c1 (NEW-1) |
| P3-C2-002 | IMPORTANT | Y | research/20-value-ledger-e2-study.md | row VL-20-625 (L636) | NEW, introduced by the P3-013 fix. Same defect: a bare `| wc -l` inside a `git ls-tree` command breaks the row's six-column shape and contradicts the ledger's own statement that every row has all six columns. | structural verification report: pipe count of the row is above 7. | Escape the pipe as `\|` (or rephrase), then re-run the same pipe count over all six ledgers. | qa-verification-structural-phase3-c1 (NEW-2) |

## Review 2 Item Status (research files 01-24, after verification 1)

Files 01-19, 21, 22 and 23 are PASS (no open or new blocking finding). Files 20 and 24 are FAIL (one open blocking finding each).

| File | Status | Open blocking | Findings |
|------|--------|---------------|----------|
| 01 to 19 | PASS | 0 | none |
| 20-value-ledger-e2-study.md | FAIL | 1 | P3-C2-002 |
| 21-value-ledger-brainstorms.md | PASS | 0 | none |
| 22-value-ledger-collab-designs.md | PASS | 0 | none |
| 23-value-ledger-e1-e3-code.md | PASS | 0 | none |
| 24-value-ledger-evidence-consumers.md | FAIL | 1 | P3-C2-001 |

## Counts

F_1 = 2 (P3-C2-001, P3-C2-002), exactly as computed in Item 3.20. F_0 was 11.

## Minor findings (notes, never fixed, never rechecked)

From the structural verification report (section 5, seven notes) and the content verification report (six notes). Those named in the reports' summaries:
- VL-20-005 and VL-20-561 still say 95 combo directories while VL-20-625 says 96.
- Duplicate DROP rows VL-19-483, VL-19-491, VL-19-736, VL-19-789 and VL-21-726 still repeat "4 verdict flips".
- research/06 L292 engine comparison cell still reads "8/13 layout/copy drift" although 3 of the 8 are an unparseable contract.
- research/09 L107 wording tension with the new "`--resume` for gateway ids [UNVERIFIED]" tag.
- Gap items added by fix cycle 1 are numbered out of order in 06 and 07.
- E2 raw-data counts and the "five never caught" list were carried from corrected files, not re-derived.
The remaining notes are in the two reports.

## Verdict

FAIL (F_1 = 2 > 0). Next: fix cycle 2 (Item 3.22).
