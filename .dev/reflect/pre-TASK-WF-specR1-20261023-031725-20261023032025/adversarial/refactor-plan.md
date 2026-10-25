# Refactoring Plan (refactor cycle 1)

## Overview
- Base: Variant 1 (reviewer-1 card, sonnet:analyzer)
- Incorporated: Variant 2, debate consensus (consensus-summary.md), invariant probe MEDIUM warnings
- Output: merged-verdict.yaml (YAML, merge_method: adversarial)
- Risk: Low (finding-list edits only)

## Planned Changes

1. **Verdict** — `overall_verdict: not_ready`; meaning: "cycle-0 findings fixed except the items below; two medium acceptance defects, one medium structural miss and six medium probe warnings remain; scope and Fix 1-4 coverage sound". Source: X-001.
2. **Keep R1-1 medium** with the consensus fix (Task 1 skips the three tooling roots when hashing and lists them in a separate file, not in t1-hashes-before.txt; Constraints widened to cover pre-existing tooling files, INV-008). Sources: R1-1, INV-008.
3. **Keep R1-2 medium** with the consensus fix (static check on the `gh pr list` line; stub logs of runs (a) and (b) show `--head sync/framework`). Add INV-004: assert the stub log order push, then list, then create. Sources: R1-2, INV-004.
4. **Add R2-1 medium** (source:82 ancestors) with the renumbering, plus INV-001 (rename artifacts and cross-references by new task number, or keep old artifact names and say so; no partial renaming), INV-002 (hash ./artifacts/t2-codecov-v4.md, or its renamed successor, at the end of the Codecov research task), INV-003 (single-parent Depends cannot satisfy every clause of source:82; record the choice as a necessary deviation in Constraints). Sources: R2-1, INV-001, INV-002, INV-003.
5. **Add INV-005 medium** — Task 6 stub runs must prove `pwd` is outside the repository and that the shared `.git/config` is unchanged afterwards (`git config --get user.name` before and after). Source: INV-005.
6. **Add INV-006 medium** — header block must contain `cannot block` (or equivalent fixed phrase) and must not contain `until a human acknowledges`; summary item 3 must not contain `must require` or `should require`. Source: INV-006.
7. **Merge R1-6 with R2-3 (low)** — -z emits `XY new\0old\0`; record both; old path MISSING; new path outside the allow-list fails. Sources: R1-6, R2-3, round2-v2 byte evidence.
8. **Add R2-5 (low)** — Task 7 must leave the Codecov research file unchanged (hash cmp). Source: R2-5 (hash point per change 4).
9. **Add R2-4 (low)** — job-name check forbids `human review required`, not the bare word. Source: R2-4.
10. **Keep R1-5, R1-10 (low)**; R1-3 and R1-4 as low optional hardening; C3 note reduced to "say `advisory` in the warning instruction". Add INV-007 (renders must list the five paths, not "(diff unavailable)"), INV-009 (Task 9 positive check uses the same status flags as Task 1), INV-010 (leftover line numbers are base numbers). Sources: R1-3, R1-4, R1-5, R1-10, R2-7, INV-007, INV-009, INV-010.

## Changes NOT Being Made
- R1-8 (source:80 instructs the conclusion), R1-9 (line 30 not a publish-workflow leftover per source:81): dropped by both advocates.
- R2-8: kept only under matrix_corrections.
- R1-12's log-precondition idea: superseded by the renumbering.

## Review Status
Auto-approved 2026-10-23T03:44:00Z (non-interactive).
