# Phase 7 Gate A — Fix Applied (Step 7.GA5)

Single serial writer (executor, I20). 2 ACTIONABLE fixes for the crossref FAIL; INV-001 untouched.

| Finding | Fix | Files |
|---|---|---|
| F1 (CRITICAL) FR-9.5/T-1117 review-wins half-built | Added `_is_attributed_review(review, watermark)` helper + the FR-9.5 arbiter in `classify()`: at the S5 poll (watermark set) a genuine attributed re-review (review newer than watermark, not itself a decline) WINS over a co-occurring decline; initial poll (watermark=None) keeps decline-first (FR-9.1). Also excluded decline-shaped comments from the findings-comment count (a decline is never a finding). Added `test_t1117_ec22_attributed_rereview_wins_over_decline` (findings-review-wins, clean-review-wins, initial-decline-first, S5-decline-only). | classifier.py, test_detection_contract.py |
| F2 (IMPORTANT) 3 phantom matrix T-IDs | Renamed/tokened the covering tests: T-1113b (initial-poll decline), T-1114 (fallback invoke), T-1116 (verify-before-remediate). | test_auggie_fallback.py |

## Verification (post-fix)
- `pytest tests/pr_submit/` = **176 passed** (175 → +T-1117).
- `grep` confirms T-1113b / T-1114 / T-1116 / T-1117 each resolve to a real test (no phantom coverage).
- `ruff check` + `ruff format` clean on classifier.py, test_detection_contract.py, test_auggie_fallback.py.
- INV-001 NOT touched (fix is classifier-only; fsm.py round_counter increment unchanged — still 1 site).
- FR-9.1 (decline-first at initial poll) preserved; the existing 8 decline tests + all baseline still green.
- No skill file touched → no re-sync needed for this fix.

## Deferred (documented in consolidated findings)
- F3 (MINOR) T-1121/1122/1125 label drift — behavior fully covered, no churn.
