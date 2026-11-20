# Merge Log

## Metadata

- Base: variant 2 (`variant-2-original.md`)
- Executor: merge-executor agent (sonnet class), output `merged-verdict.yaml`
- Changes applied: 9 of 9 planned (`refactor-plan.md`)
- Status: applied, with two orchestrator corrections after the fact
- Timestamp: 2026-11-20T18:20:00Z
- Note: the merge executor was told to run no commands, so the orchestrator parsed the YAML afterwards: it loads, has the keys merge_method, verdict, convergence_score, base_variant, source_cards, blocked_by_invariants, unresolved_conflicts, findings (14), checked_and_found_sound (9), coverage_gaps (7).

## Changes Applied

| # | Change | Status |
|---|---|---|
| 1 | Merged ordering finding M-1 (hard cases PLAN 62, 73, 108, 161, 174; declared deferrals not blocking; collector-test gap) | applied |
| 2 | M-2 pull-request step missing, with the INV-006 handoff-note caveat | applied |
| 3 | M-3 15 rows, not 14 | applied |
| 4 | M-4 Task 1 fallback for item 1, plus INV-002 | applied |
| 5 | M-5 open-pull-request proof | applied |
| 6 | M-7 helper fetch regraded to MEDIUM | applied |
| 7 | M-6 patch-and-bundle regraded to MEDIUM, listed as UNRESOLVED | applied |
| 8 | M-8 (INV-001) and M-9 (INV-003) added as BLOCKING | applied; grade ground chosen by the executor (Missing, Safety) |
| 9 | INV-004, INV-005, INV-007, INV-008, INV-009 added as notes | applied; INV-004 graded MEDIUM although the probe rated it HIGH (per plan change 9) |

## Orchestrator corrections

- M-8 grade ground changed from Missing to Decision: the defect is an acceptance check that cannot be met, which is the Decision clause. Severity unchanged.
- M-9 grade ground Safety kept: the runner is the safety boundary and a denylist lets unlisted mutating commands pass.

## Post-Merge Validation

- Structural integrity: YAML parses; one finding list; no heading rules apply.
- Internal references: every finding cites an input file or the plan, the spec snapshot or a repository file; the Wave 5 evidence-validator re-reads them.
- Contradiction re-scan: no new contradiction was introduced; the one open conflict (C-003 grade) is listed under unresolved_conflicts.

## Summary

Planned 9, applied 9, failed 0, skipped 0.
