# Merge Log

## Metadata

- Base: Variant A (`variant-1-original.md`; reviewer 1, analyzer, sonnet)
- Incorporated: `variant-2-original.md` (B), `invariant-probe.md`, `round2-variant-A.md`, `round2-variant-B.md`
- Plan: `refactor-plan.md` (14 planned changes, 4 rejected alternatives)
- Executor: merge-executor (opus)
- Output: `merged-verdict.yaml`
- Changes applied: 14 of 14
- Status: COMPLETE (no change skipped or failed)
- Timestamp: 2026-11-08T19:01:31Z

### Finding id mapping

The plan names M-F6 (heartbeat) and M-F7 (brief ownership) for new findings, but base R1-F6 and R1-F7 stay as unchanged findings and the plan's change 13 cites "M-F7 of A, the absence rules". To keep ids contiguous and unique, base findings keep their numbers and the two new blocking findings move to the end.

| Merged id | From | Plan id |
|---|---|---|
| M-F1 - M-F5 | R1-F1 - R1-F5 (rewritten by changes 3, 4, 5, 6, 2) | M-F1 - M-F5 |
| M-F6 - M-F9 | R1-F6 - R1-F9 (unchanged) | - |
| M-F10 | replaces withdrawn R1-F10 (change 8) | M-F10 |
| M-F11 | R1-F11 (unchanged) | - |
| M-F12 - M-F19 | new (changes 9, 10, 11) | M-F12 - M-F19 |
| M-F20 | new, heartbeat (change 1) | M-F6 |
| M-F21 | new, brief ownership (change 7) | M-F7 |

## Changes Applied

| # | Status | Target | Before -> After | Provenance |
|---|---|---|---|---|
| 1 | applied | M-F20 (plan M-F6) | none -> drift/blocking heartbeat finding: route conditions on spawn only; smoke check must cover spawn and a heartbeat interval > 5 min in Tasks 6, 9, 11 | R2-F3 + INV-014 |
| 2 | applied | M-F5 | R1-F5 (unchanged-condition drop + k=1 tail) -> adds Task 1 :44 vs Task 6 :125 conflict, single skip predicate, where it is evaluated, what `close` writes, sweep copies live text not r1.md; k=1 tail kept; drift/blocking | R1-F5 class + R2-F2 content + INV-002 |
| 3 | applied | M-F1 | remedy "scope pin to loop section or rewrite line 220" -> keep whole-file pin; rewrite line 220 under owner decision naming the template (installed copy differs at byte 401); add to drift exclusions; necessary/blocking | R1-F1 class + R2-F1 remedy; round2-A evidence 3; INV-016 |
| 4 | applied | M-F2 | two missing Task 7 assertions -> adds false spec premise (git ls-files only) and expectation that all other tracked-file scans apply once committed | R1-F2 + round2-A evidence 4 + INV-003 |
| 5 | applied | M-F3 | "add it to Constraints" -> Constraints must list test_routing_refresh.py so Task 8's report-not-fix rule applies; frozen-test context added | R1-F3 + INV-017 |
| 6 | applied | M-F4 | "Task 2 cannot meet its AC" -> ordering defect plus E-CAP vs E-TERMINAL order pin; E-TERMINAL test uses a ledger ended at review 2 | R1-F4 + round2-A evidence 5 + INV-019 |
| 7 | applied | M-F21 (plan M-F7) | none -> necessary/blocking brief-ownership finding; owner decision required | INV-001 |
| 8 | applied | M-F10 | R1-F10 U3/W/O disjointness -> narrower minor note: U3 = headline_raw on :99 fixture; define U3 as loop-row analogue of Arm B + one AC; sweep-challenge storage | INV-008 + INV-009 |
| 9 | applied | M-F12 | none -> minor guard-loss finding (spec-panel.md:261 guards not carried) | INV-005 |
| 10 | applied | M-F13, M-F14, M-F15 | none -> three minor spec-origin owner notes (reviser rules/byte size; bytes per claim; S1 skip rule) | INV-004; R2-F4; INV-006 |
| 11 | applied | M-F16 - M-F19 | none -> four minor kernel-definition findings | INV-007, INV-010, INV-011, INV-013 |
| 12 | applied | `notes` | none -> four LOW notes | INV-012, INV-015, INV-020, INV-021 |
| 13 | applied | `coverage` | none -> B's map relabelled `referenced_by_a_task`; INF-005/058/104 moved to `true_gaps` (back M-F7); INF-134 added (backs M-F20) | B lexical_misses/true_gaps; X-001 |
| 14 | applied | header | reviewer-card header -> verdict FAIL, merge_method adversarial, convergence_score 1.0, convergence_status BLOCKED_BY_INVARIANTS (resolved by carrying INV-001 as M-F21 and INV-002 as M-F5); t1_deviation_agreement kept | debate |

### Executor choices the plan did not state

- Classes for changes 9-11 were not given. Used `drift` for M-F12 and M-F16 - M-F19 (plan omissions or undefined behaviour), `necessary` for M-F13 - M-F15 (the plan labels them spec-origin owner notes). Grades follow the plan (minor).
- `t1_deviation_agreement` D1 and D4 referenced R1-F10 and R1-F11; rewritten to M-F10 and M-F11 so the references resolve. Wording otherwise unchanged.
- `coverage.checked_by_an_ac` is a statement, not a list: neither reviewer verified any row as AC-checked, so no row was placed there.
- Refs: `src/superclaude/commands/spec-panel.md` and `tests/...` paths are written repo-relative (paths established in the inputs). `source.md`, the plan file, `install_templates.py` and `merged-requirements.md` are written as cited in the inputs, because their directories are not stated there. No new file:line ref was introduced.

## Post-Merge Validation

- Structural integrity: PASS. Re-read with `yaml.safe_load`: parses; top-level keys are exactly merge_method, verdict, convergence_score, convergence_status, source_cards, findings, notes, coverage, t1_deviation_agreement, rejected_alternatives. All 21 findings carry exactly the field set id, class, grade, task, spec_ref, plan_ref, claim, recommendation, source. Ids M-F1 - M-F21 are unique and contiguous.
- Internal references: PASS. Ids referenced outside `findings` are M-F7, M-F10, M-F11, M-F20; all exist. No R1-/R2- id remains outside `source` tags.
- Contradiction re-scan:
  - Rejected alternatives vs findings: no finding uses class `regression` (X-002/X-003 respected); M-F1 contains no scope-the-pin remedy (C-001 respected); M-F10 makes no disjointness claim (C-012 respected); INF-005/058/104 are true gaps, not covered (X-001 respected). No finding is both blocking and rejected.
  - No new contradiction found. One dependency to note: if the owner resolves M-F21 by changing the S1 briefs beyond a one-line substitution, the M-F8 check (reverse the substitution and `cmp`) must change with it. This is a sequencing dependency, not a contradiction in the merged card.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 14 | 14 | 0 | 0 |

Merged verdict: FAIL; 21 findings, 7 blocking (M-F1, M-F2, M-F3, M-F4, M-F5, M-F20, M-F21), 14 minor.
