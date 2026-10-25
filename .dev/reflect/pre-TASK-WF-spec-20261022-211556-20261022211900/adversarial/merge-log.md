# Merge Log

## Metadata
- Base: Variant 1 (reviewer-1 card, sonnet:analyzer), variant-1-original.md
- Incorporated: variant-2-original.md, debate-transcript.md, invariant-probe.md (MEDIUM warnings)
- Plan: refactor-plan.md (9 planned changes plus the "Also" line; 3 changes not made)
- Executor: merge-executor
- Output: merged-verdict.yaml
- Status: Success (all planned changes applied, none failed or skipped)
- Timestamp: 2026-10-22T21:42:34Z

## Changes Applied

| # | Change | Status | Before -> After | Provenance |
|---|---|---|---|---|
| 1 | Verdict | applied | `ready_with_notes` -> `not_ready`; verdict_meaning "revise acceptance bullets, then run; scope, order and Fix 1-4 coverage are sound" | X-001, Round 2 V1 concession |
| 2 | Add R2-4 | applied | absent -> M-04 (medium, Task 8): badge must name actions/workflows/test.yml, boundary paragraph says it cannot block, sync paragraph says it does not push to master | R2-4, C-008 |
| 3 | Extend R1-10 | applied | `<t1-head>` only -> M-17 also covers `<decided file input>` (tasklist:124) and the "fail if angle-bracket placeholders survive" rule | R1-10, R2-7, C-004 |
| 4 | Extend R1-11 | applied | optional chain note -> M-18 states repoints (Task 7 -> Task 2; Task 3 and Task 4 -> Task 1) and that the chain is safe but misstated | R1-11, R2-5, C-005 |
| 5 | Merge R1-2 + R2-6 | applied | two low findings -> M-11 (low), false-pass and false-fail directions of line-number slices | R1-2, R2-6, C-003 |
| 6 | Merge R1-3 + R2-1 | applied | low + medium -> M-12 (low), fenced-command fix | R1-3, R2-1, C-001 |
| 7 | Merge R1-4 + R2-2 | applied | two findings -> M-02 (medium): git stub delegation, gh stub count, GITHUB_REPOSITORY, shell; INV-003 note added (runner default is `bash -e {0}`, no pipefail, so stub matches runner) | R1-4, R2-2, INV-003, C-002 |
| 8 | Trim R1-12 | applied | low with .venv/uv.lock sub-claims -> M-05 (medium), sub-claims dropped, porcelain parsing and .dev/reflect hazard kept, INV-013 folded in (.dev/troubleshoot/, .dev/workflow/, remediate package folder) | R1-12, INV-013, Round 2 V1 withdrawal |
| 9 | Append invariant warnings | applied | none -> M-06 (INV-001), M-07 (INV-002), M-08 (INV-004), M-09 (INV-007), M-10 (INV-014), each medium | invariant-probe.md |
| Also | Row verdicts and severities | applied | INF-041 -> partial (from V2); INF-045 -> gap; R1-8 -> low (M-15); R1-9 stays low (M-16) and gains INV-016 | X-003, calibrator, INV-016 |

Unchanged carry-overs from the base: R1-1 -> M-01, R1-5 -> M-03, R1-6 -> M-13, R1-7 -> M-14. R2-9 and R2-10 recorded under `matrix_corrections`. The three rejected changes are recorded under `rejected`.

## Post-Merge Validation
- YAML parses: checked with `uv run python -c` using `yaml.safe_load` on merged-verdict.yaml. It loaded without error.
- Every finding has evidence: checked in the same script. Findings with empty evidence: none. Findings with empty sources: none. Evidence citations were copied from the source variants and probe rows.
- No finding contradicts `overall_verdict: not_ready`: there are 10 medium findings that need bullet revisions before the run, and none argue the plan is ready or that scope, order or coverage are wrong. No high findings, consistent with the verdict meaning.
- Findings by severity: 18 total, medium 10 (M-01 to M-10), low 8 (M-11 to M-18), high 0. The `counts` field matches.
- Other keys present: invariant_warnings (6), unmapped_row_verdicts (7), matrix_corrections (4 entries), rejected (3).

## Summary
- Planned: 9 changes plus the "Also" line
- Applied: 9 plus the "Also" line
- Failed: 0
- Skipped: 0
- Note: the merged file adds no content beyond the plan, the variants and the probe. The recommendations in M-07, M-08 and M-10 are drawn from the probe rows; M-06's recommendation (identify the Decision line by its prefix) is a direct restatement of INV-001.
