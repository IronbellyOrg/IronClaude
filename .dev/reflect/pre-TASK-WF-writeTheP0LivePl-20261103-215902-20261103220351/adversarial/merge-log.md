# Merge Log

## Metadata
- Base: variant-1-original.md (reviewer-1, analyzer, sonnet)
- Plan: refactor-plan.md (auto-approved)
- Executor: orchestrator (manual fallback; no merge-executor sub-agent)
- Outputs: merged-verdict.yaml (full findings), merged-review-card.md (provenance and cross-cutting rules)
- Status: success (with warnings: manual debate, convergence 0.76 below the 0.80 advisory threshold)

## Applied changes

| # | Plan item | Result | Provenance |
|---|---|---|---|
| 1 | R-01 | R1-10 merged with R2-01, R3-05 and the Task 1 part of F-010 into D-002 | **Status**: applied |
| 2 | R-02 | D-006 added from R2-02, R3-06 at should-fix | **Status**: applied |
| 3 | R-03 | R1-04 merged with R3-04 into D-003 at should-fix | **Status**: applied |
| 4 | R-04 | R1-03 merged with R3-08 into D-004; stop rule rewritten per orca-capabilities.md:114, :125, :129 | **Status**: applied |
| 5 | R-05 | R1-09 merged with R3-09 into D-007 | **Status**: applied |
| 6 | R-06 | R1-05 fix replaced with pre-run help check plus R3-03 run-time rule (D-009) | **Status**: applied |
| 7 | R-07 | D-012 added from R2-03 at should-fix | **Status**: applied |
| 8 | R-08 | D-013 added from R3-07 | **Status**: applied |
| 9 | R-09 | Minors D-015, D-017..D-022 added | **Status**: applied |
| 10 | R-10 | R1-12 split: grep-exit part into D-016, rest D-023 | **Status**: applied |
| 11 | weakness | R1-11 downgraded to minor D-014 (weak) | **Status**: applied |
| 12 | weakness | D-005 marked to be applied with the blocking fixes (INV-007) | **Status**: applied |

## Post-merge validation
- `merged-verdict.yaml` parses; top-level keys are exactly merge_method, convergence_score, verdict, blocking_count, findings, unresolved_conflicts, unaddressed_invariants.
- 23 findings, ids D-001..D-023 contiguous; severities 2 blocking, 11 should-fix, 10 minor; blocking_count 2 matches.
- Every F-001..F-017 and every R1/R2/R3 finding appears in exactly one D source list or in the rejected list (F-016; R3-02), except three findings split by design: F-010 (D-002 for Task 1, D-006 for Tasks 2-5), R1-12 (D-016 grep exit, D-023 the rest) and R3-03 (D-019 severity, D-009 run-time rule).
- Contradiction re-scan: no D fix tells the executor to edit the plan mid-run or to stop a waiting worker on absence alone.
- Every `plan:<n>` evidence line was re-Read in this session against the current plan file.
