# Refactoring Plan

## Overview
- Base: Variant 1 (reviewer-1 card, sonnet:analyzer)
- Incorporated: Variant 2 (reviewer-2 card), debate consensus, invariant probe MEDIUM warnings
- Planned changes: 9; rejected: 3
- Overall risk: Low (all changes are finding-list edits; no finding's evidence changes)
- Output: merged-verdict.yaml in this directory (YAML, merge_method: adversarial)

## Planned Changes

1. **Verdict** — set `overall_verdict: not_ready` (was ready_with_notes). Source: X-001, Round 2 concession by the V1 advocate. Meaning recorded verbatim: "revise acceptance bullets, then run; scope, order and Fix 1-4 coverage are sound". Risk: Low.
2. **Add R2-4 as M-xx (medium)** — Task 8 acceptance passes a wrong README; badge must name actions/workflows/test.yml; boundary paragraph must say it cannot block; sync paragraph must say it does not push to master. Source: Variant 2 R2-4, C-008. Risk: Low.
3. **Extend R1-10** — include `<decided file input>` (tasklist:124) and the rule "fail if angle-bracket placeholders survive". Source: R2-7, C-004. Risk: Low.
4. **Extend R1-11** — state the concrete repoints (Task 7 -> Task 2; Task 3 and Task 4 -> Task 1) and that the current chain is safe but misstated. Source: R2-5, C-005. Risk: Low.
5. **Merge R1-2 with R2-6** — one finding stating both false-pass and false-fail directions of line-number slices. Source: C-003. Risk: Low.
6. **Merge R1-3 with R2-1** — one low finding; fix as a fenced command. Source: C-001. Risk: Low.
7. **Merge R1-4 with R2-2** — one medium finding (git stub delegation, gh stub count, env, shell); append INV-003 note that Actions' default shell is `bash -e {0}` without pipefail, so the stub should match the runner, not add pipefail. Source: C-002, INV-003. Risk: Low.
8. **Trim R1-12** — drop the .venv/uv.lock sub-claims (both gitignored); keep porcelain parsing and the .dev/reflect hazard; fold in INV-013 (implement retry ladder writes .dev/troubleshoot/, .dev/workflow/). Source: Round 2 V1 withdrawal, artifacts/shared-assumption-checks.md, INV-013. Raise to medium (correct run fails Task 9). Risk: Low.
9. **Append invariant warnings as separate medium findings** — INV-001 (Task 2 "ends with Decision:" vs Task 7 append), INV-002 (t6-fix1-notes.md not durable: package lives only in the worktree), INV-004 (failed `gh pr list` can end green with no PR), INV-007 (stub run 2 needs a fresh staged change), INV-014 (Tasks 6/7 never compare `on:`, job keys or step count). Source: invariant-probe.md. Risk: Low.

Also: unmapped_row_verdicts INF-041 -> partial (from V2); INF-045 -> gap (both); R1-8 severity -> low (calibrator + both advocates); R1-9 stays low and gains INV-016 (missing leftover lines 5, 34, 64-66).

## Changes NOT Being Made
- R2-3 (ask the user before Task 9): rejected; source.md:35 and :44 already decided; V2 advocate conceded (X-002, C-006).
- R2-8 remedy ("session report constraint"): rejected in favour of R1-8's artifact home (C-007).
- R2-9 / R2-10 as tasklist findings: kept only as reflect coverage-matrix corrections (no tasklist edit), recorded under `matrix_corrections`.

## Risk Summary
All changes edit the merged finding list only. Rollback: variant-1-original.md is unchanged on disk.

## Review Status
Auto-approved 2026-10-22T21:42:00Z (non-interactive).
