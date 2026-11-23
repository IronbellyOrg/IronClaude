# Merge Log

## Metadata
- Base variant: Variant 2 (`variant-2-original.md`, reviewer-2 card, opus:qa)
- Incorporated variant: Variant 1 (`variant-1-original.md`, reviewer-1 card, haiku:analyzer)
- Executor: merge-executor
- Plan: `refactor-plan.md` (auto-approved 2026-11-10T05:40:00Z)
- Changes applied: 17 of 17
- Status: success
- Timestamp: 2026-11-10

## Changes Applied

| # | Target | Status | Provenance tag | Citation check |
|---|---|---|---|---|
| 1 | M-01 | applied | Variant 2 QA-05 base + Variant 1 R1-01 | 5 of 5 verbatim (R1-01 first, QA-05 after, no exact duplicates) |
| 2 | M-02 | applied | Variant 1 R1-02 | 3 of 3 verbatim |
| 3 | M-03 | applied | Variant 1 R1-03 | 3 of 3 verbatim |
| 4 | M-04 | applied | Variant 2 QA-01 | 4 of 4 verbatim |
| 5 | M-05 | applied | Variant 2 QA-02 base + Variant 1 R1-06 | 4 of 4 verbatim (3 R1-06 strings, then QA-02's extra `merged-requirements.md:385`; duplicates dropped) |
| 6 | M-06 | applied | Variant 2 QA-09 | 3 of 3 verbatim |
| 7 | M-07 | applied | Variant 1 R1-04 | 3 of 3 verbatim |
| 8 | M-08 | applied | Variant 1 R1-05 | 3 of 3 verbatim |
| 9 | M-09 | applied | Variant 2 QA-06 base + Variant 1 R1-07 | 4 of 4 verbatim (duplicates dropped) |
| 10 | M-10 | applied | Variant 2 QA-03 | 4 of 4 verbatim |
| 11 | M-11 | applied | Variant 2 QA-04 | 4 of 4 verbatim (plan:118 kept, as the plan directs) |
| 12 | M-12 | applied | Variant 2 QA-07 | 3 of 3 verbatim |
| 13 | M-13 | applied | Variant 2 QA-08 | 4 of 4 verbatim |
| 14 | M-14 | applied | Variant 2 QA-10 | 3 of 3 verbatim |
| 15 | M-15 | applied | Variant 2 QA-11 | 3 of 3 verbatim |
| 16 | M-16 | applied | Variant 2 QA-12 | 3 of 3 verbatim |
| 17 | N-01 to N-09 table | applied | refactor-plan.md Change #17 (orchestrator-verified, not card citations) | Not card citations; `...` shorthand expanded to the full plan path (0 `...TASK` left) |

Layout followed: provenance header comments, title and 3-line summary, Judge rulings 1-7, Merged findings (fields in the required order, one provenance comment per block), Missed by both cards, Severity counts.

## Post-Merge Validation

- Structural integrity: pass. Heading hierarchy is H1, then H2 sections (Judge rulings, Merged findings, Missed by both cards, Severity counts), then H3 per M entry; no skipped levels. 16 `### M-` headings, ids contiguous M-01 to M-16. N ids N-01 to N-09 contiguous. Every M block has all 8 fields (id, sources, severity, plan_task, claim, evidence_file_line, suggested_fix, disposition).
- Citation verbatim check: pass. A line-by-line script check found 56 evidence strings in `merged-output.md` and 0 not present, character for character, as a quoted string in `variant-1-original.md` or `variant-2-original.md`. The 56 split as M-01 5, M-02 3, M-03 3, M-04 4, M-05 4, M-06 3, M-07 3, M-08 3, M-09 4, M-10 4, M-11 4, M-12 3, M-13 4, M-14 3, M-15 3, M-16 3. R1-01 and R1-04/R1-05 style single-string values were written as one-item lists where needed (M-01's R1-01 value is the first list item). The check confirms each string exists in some card; the per-finding assignment follows the plan's Sources lines and was read against the card text.
- Severity counts: blocking 6 (M-01 to M-06), minor 10 (M-07 to M-16), rejected outright 0, partial rejections 4 (QA-04, QA-08, QA-11, QA-12); summary and counts table match the entries.
- Internal references: pass. M-01 refers to M-02, M-08 refers to N-06, N-03 to N-04 and N-07 refer to M-01, M-02, M-04; all targets exist. Judge rulings 1-7 are the plan's rulings restated.
- Contradiction re-scan: pass. Severities match the plan's rulings (T33 blocking, R1-04 minor, QA-09 blocking narrowed, QA-03 and QA-04 minor); no entry contradicts a ruling. Not checked: citation line numbers were not re-read against the source files (the plan says to copy card strings, not to re-verify them).

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 17 | 17 | 0 | 0 |

Note: the convergence line in `merged-output.md` states BLOCKED_BY_INVARIANTS (INV-001, INV-002), taken from `debate-transcript.md` lines 6-8 and 89, since the plan gave only "0.91 with the invariant-gate status".
