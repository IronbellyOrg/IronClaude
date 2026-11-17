# Merge Log: merged review card, stage 3 plan, third review

## Metadata
- Base variant: variant-2-original.md (reviewer-2, qa persona, opus class)
- Incorporated: variant-1-original.md (reviewer-1, haiku class), invariant-probe.md (fault-finder), debate rounds
- Executor: merge-executor (Read, Grep, Glob, Write only)
- Merge date: 2026-11-16
- Output: .dev/reflect/pre-TASK-WF-blockerStage3-20261116-030158-20261116185913/adversarial/merged-review-card.md
- Findings: 15 (3 blocking: F1, F2, F3; 12 non-blocking: F4 to F8 Medium under Follow-up candidates, F9 to F15 minor)
- Finding text source: merge-input-findings.md (bodies, severities, blocking flags and categories kept as written)

## Changes Applied

| Change | Source | Target | Status |
|--------|--------|--------|--------|
| 1 | V1 F1 + V2 F4 + INV-003 (a), (b) | merged F1 (blocking) | applied |
| 2 | V2 F1 | merged F2 (blocking) | applied |
| 3 | V2 F5 + INV-001 | merged F3 (blocking, regraded) | applied |
| 4 | INV-002 + V2 F5 context | merged F4 (Medium, Follow-up candidates) | applied |
| 5 | V2 F2 | merged F5 (Medium, regraded) | applied |
| 6 | V2 F3 + V2 F10 (first half) | merged F6 (Medium, regraded) | applied |
| 7 | INV-003 (c), (d) | merged F7 (Medium) | applied |
| 8 | INV-004 | merged F8 (Medium) | applied |
| 9 | V1 F2 | merged F9 (minor, regraded) | applied |
| 10 | V2 F8 | merged F10 (minor) | applied |
| 11 | V2 F6 | merged F11 (minor) | applied |
| 12 | V2 F9 | merged F12 (minor) | applied |
| 13 | V2 F10 (second half) | merged F13 (minor) | applied |
| 14 | T1 card F2 | merged F14 (minor) | applied |
| 15 | T1 card F5 + INV-005 | merged F15 (minor) | applied |

Changes NOT being made (per plan, honoured): V2 F7 dropped; V2 F10 premise on rf-qa.md lines 389 and 476 dropped; the "reverses PLAN:80" claim softened (already in F2 text); INV-006 to INV-008 kept as Checked items.

## Post-Merge Validation
- Citations checked: 57 (F1 5, F2 4, F3 11, F4 4, F5 4, F6 6, F7 2, F8 2, F9 2, F10 2, F11 2, F12 2, F13 2, F14 3, F15 4). Each was looked up in the cited live file by quote; every quote sat on the cited line.
- Corrected (old line to new line): none.
- Removed: none.
- Totals: 3 blocking, 12 non-blocking, 15 findings; confirmed.
- Alias use: PLAN, SRC, S0, S4, SPEC, README, PRIOR defined in the second comment line; PRIOR and README are defined but cited only in the Earlier findings and Source comments. Every other path is repo-relative.
- Structure: heading line first, two comment lines, then Verdict, Earlier findings, Findings, Follow-up candidates, Checked, Self-report.
- Not done: no commands or tests were run; no other source files were opened.

## Summary
All 15 planned changes applied. 57 citations verified without any line move or removal. The card keeps the finding bodies of merge-input-findings.md unchanged; the only edits are layout (citations as bullets, trailing "citations:" label kept) and the added Source comments. The aliases comment omits the instruction sentence about re-reading lines, which is for the executor and not for the card.
