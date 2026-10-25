# Merge Log (refactor cycle 1)

## Metadata
- Base: Variant 1 (sonnet:analyzer, reviewer-1), variant-1-original.md
- Incorporated: Variant 2 (haiku slot, qa), consensus-summary.md, debate-transcript.md, invariant-probe.md (MEDIUM warnings and LOW rows)
- Plan: refactor-plan.md (10 planned changes)
- Output: merged-verdict.yaml
- Merge date: 2026-10-23T03:44:24Z
- Executor: merge-executor

## Changes Applied

| # | Status | Before (base) | After (merged) | Provenance |
|---|---|---|---|---|
| 1 | Applied | `overall_verdict: ready_with_notes` | `not_ready`, with the plan's verdict_meaning text; convergence 1.0 CONVERGED | X-001 |
| 2 | Applied | R1-1 medium, no fix detail on hash vs tooling roots | M-01 medium: Task 1 skips the three tooling roots and lists them in a separate named file; Constraints widened to pre-existing tooling files | R1-1, INV-008 |
| 3 | Applied | R1-2 medium, check on `--head` only | M-02 medium: static check on the `gh pr list` line, stub logs for runs (a) and (b) show `--head sync/framework`, plus push, list, create order assertion | R1-2, INV-004 |
| 4 | Applied | R1-12 low optional log precondition | M-03 medium (R2-1): renumber 1-9 with a one-parent chain; rename artifacts and cross-references by new number or keep old names, no partial rename (INV-001); hash the Codecov file at the end of the research task (INV-002); record the single-parent choice as a necessary deviation (INV-003) | R2-1, INV-001, INV-002, INV-003 |
| 5 | Applied | not present | M-04 medium: Task 6 stub runs prove `pwd` outside the repo and unchanged shared `.git/config` (`git config --get user.name` before and after) | INV-005 |
| 6 | Applied | not present | M-05 medium: header block needs `cannot block`, must not contain `until a human acknowledges`; summary item 3 must not contain `must require` or `should require` | INV-006 |
| 7 | Applied | R1-6 low (rename rule only) | M-06 low: `-z` emits `XY new\0old\0`; record both; old path MISSING; new path outside allow-list fails | R1-6, R2-3, round2-v2 byte evidence |
| 8 | Applied | not present (INF-057 was covered) | M-07 low: Task 7 leaves the Codecov research file unchanged (hash cmp); INF-057 verdict now partial | R2-5 (hash point per change 4) |
| 9 | Applied | not present | M-08 low: job-name check forbids `human review required`, not the bare word; requires `boundary` and `advisory` | R2-4 |
| 10 | Applied | R1-3, R1-4, R1-5, R1-7, R1-10 as in base | M-09 (R1-5, regex), M-10 (R1-10, zero `<`, quoted PR body), M-11 (R1-3 optional), M-12 (R1-4 optional), M-13 (C3 reduced to "say `advisory` in the warning instruction"), plus new M-14 (INV-007), M-15 (INV-009), M-16 (INV-010) | R1-3, R1-4, R1-5, R1-10, R2-7, INV-007, INV-009, INV-010 |

Also applied from the plan's "Changes NOT Being Made" section: R1-8, R1-9 and the R1-12 precondition idea listed under `rejected`; R2-8 carried under `matrix_corrections` only; unmapped row verdicts taken from the base with INF-057 changed to partial (R2-5) and INF-050 changed to covered (V2 and consensus; the Task 5 gap is optional hardening in M-11).

Choices not spelled out in the plan, kept minimal:
- R2-6 (same defect as R1-10) and R2-2 (same defect as R1-4) were added as extra sources on M-10 and M-12 rather than dropped.
- INV-012 and INV-014 (both ADDRESSED) were cited as sources on M-10 and M-09 only; INV-011 and INV-013 (ADDRESSED) are not carried.
- Finding `tasks` use the CURRENT tasklist numbers; the renumbering in M-03 is a recommendation, not applied to the finding list. M-03 lists tasks [2, 8, 9], M-04 lists [4, 6] (the Task 4 guard it compares against).
- INV-001, INV-002 and INV-003 are folded into M-03, so there are five medium findings while six medium invariant warnings are listed.

## Post-Merge Validation
- YAML parse: `yaml.safe_load` through `uv run python` succeeded; 16 findings loaded, 10 unmapped_row_verdicts, 3 rejected.
- Evidence and sources: every finding has a non-empty `evidence` list and `sources` list (checked in the same script, result True). Evidence strings are copied from the variant rows or probe rows.
- Verdict consistency: overall_verdict is `not_ready`; the file contains medium findings and no finding states the plan is ready, so no finding contradicts it.
- Severity counts: computed from findings: medium 5, low 11, high 0; matches `counts: {high: 0, medium: 5, low: 11}`.
- IDs are sequential M-01 to M-16, mediums first, then lows.
- No file other than merged-verdict.yaml and merge-log.md was written.

## Summary
- Planned changes: 10
- Applied: 10
- Failed: 0
- Skipped: 0
