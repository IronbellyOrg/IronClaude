# Refactoring Plan (merge of reviewer cards into one verdict)

## Overview
- Base: variant-1-original.md (analyzer). Incorporated: variant-2 (qa) and variant-3 (refactorer).
- Planned changes: 7. Rejected alternatives: 6. Overall risk: Low (additive and regrading edits to a review verdict).
- Review status: auto-approved (non-interactive).

## Planned Changes

| # | Source | Target in base | Change | Rationale (debate evidence) | Risk |
|---|---|---|---|---|---|
| 1 | base F3 | severity | Regrade keys-line finding from MEDIUM to BLOCKING Regression | Final ruling C-002 (all three advocates, Round 2): breaks the named constraint "link off behaves exactly as today" (view.py:914) | Low |
| 2 | base F6 | severity and fix | Regrade the Task 6 snapshot check from MEDIUM to BLOCKING Gap; use V2's fix (limit the dispatch-id exclusion to the `questions` group, keep the `rows[].dispatchId` of the linked worker, keep byte-identity with the link-off snapshot); correct the citation to export.py:131-145 and :195 | Final ruling C-003 (unanimous); V1's own cite (export.py:75-86) was the record writer | Low |
| 3 | V2 F3 | new check | Add the byte-for-byte link-off screen comparison (questions on, 160/116/80) as the acceptance check for change 1; V3's lighter option (pin the keys-line text and the selection) noted | Round 2 V3: no questions-on screen golden exists, so a reference must be captured before Task 4 | Low |
| 4 | V2 F4 | new finding | Add desk missing-value and stale/as-of assertions (C-009) | Final ruling MEDIUM Gap (unanimous) | Low |
| 5 | V3 F6 | new finding | Add the AD-18 / CAP-12 reconciliation edit to Task 7 (C-011) | Final ruling MEDIUM Drift (V2 conceded BLOCKING in Round 2) | Low |
| 6 | V3 F8 | new finding | Extend `make_question_rows` instead of a new builder that drops `body` and `to_handle` (C-012) | Final ruling MEDIUM Drift (unanimous) | Low |
| 7 | V3 F9 | new finding | Add rendering-rules.md lines 21, 24 and the line-43 R3 clause, plus the evicted-selection note (C-013); drop V3's line 40 | Final ruling MEDIUM Gap, narrowed in Round 2 | Low |

## Changes NOT Being Made
| Point | Non-base approach | Why not |
|---|---|---|
| C-007 | V3 graded the HELP-string wording MEDIUM Regression and proposed editing the pinned assertion | Final ruling NOTE: appending a sentence keeps the pinned sentence; editing the assertion is the wrong fix (V3 conceded) |
| C-008 | V2 graded the invalid-`dispatchId` reason MEDIUM | Final NOTE (V2 conceded): any unlinked reason is acceptable |
| C-010 | V3 asked to split Task 4 as a MEDIUM Drift | Final NOTE: reviewability, not correctness |
| C-014 | V3 asked to record the unrecorded post-link default re-confirm | Final NOTE: bookkeeping, listed in the notes line |
| C-015 | V1 and V3 said INF-009 had no or only a constraint check; V2 said MEDIUM | Final NOTE: test_commands.py:652-668 already pins the argv; folded into change 1's `--once` test |
| V2's "a realistic linked fixture cannot pass" | V2 F1 wording | Overstated (V2 conceded): a linked question whose worker row is absent can pass; the defect is the whole-snapshot exclusion against the found-worker case |

## Risk Summary
All changes edit a review document, not the plan or code. Rollback: restore variant-1-original.md.

## Review Status
Auto-approved. Timestamp 2026-11-17T06:56Z.
