# Base Selection
## Method and an honest deviation
The skill prescribes a 30-criterion binary rubric with dual-pass position-bias evaluation. That full rubric was NOT run: the variants are three reviewer cards of findings, not three artifacts to merge, so the rubric criteria for structure, clarity and risk coverage do not discriminate. Selection used the inputs this run actually has: calibrated confidence per card (blind calibrator), debate points won, and correctness (citations that failed on re-check). Recorded as fallback_mode: true in the return contract.

## Scores
| Variant | Calibrated C | Debate points won (winner or co-winner, of 16) | Failed or wrong claims on re-check | Findings kept after adjudication |
|---|---|---|---|---|
| V1 (analyzer) | 0.76 | 7 (C-002, C-003, C-005, C-007, C-008, X-003, C-001 co) | 1 (X-001) plus one overstated line range | F1, F2, F3 kept; F4, F5 kept as notes |
| V2 (qa) | 0.61 | 2 (C-004, C-004 co) | F3 blocking overstated; F5 withdrawn | F4 kept (blocking); F1, F2 duplicates |
| V3 (refactorer) | 0.76 | 7 (C-001, C-004 co, C-006, C-009, X-001, X-002, U-001) | 0 | F1..F9 kept |

Calibrated scores tie (0.76 vs 0.76, margin under 5 percent), so the tiebreaker applies: level 1 debate performance is a tie (7 vs 7); level 2 correctness: V3 has no failed citation and won the one point on which V1 was wrong (X-001), so V3 is the base.

## Selected Base: Variant 3 (refactorer, opus)
Strengths to preserve: golden-preservation analysis (X-001), user tier-override failure (C-006), pointer-switch test mechanism (U-001), smaller-option note (U-002), telemetry continuity (U-003).
Strengths to incorporate: from V1 the CLI test breakage (test_review_cli.py:52-62,76), the @default removal and the plugin mirror byte-identity risk; from V2 the call that the Task 4 versus Task 5 return contract is a real, blocking contradiction and that Task 1 should say it departs from the source's "single-model" wording on purpose.
