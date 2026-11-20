# Merge Log: reviewer cards merged onto Variant 3

- Base: `variant-3-original.md` (Variant 3, opus:refactorer)
- Plan: `refactor-plan.md` (C1 to C9)
- Output: `../merged-card.md`
- Merge date: 2026-11-16
- Executor: merge-executor (claude-gw-tier1a[1m])
- Facts checked before copying: plan:23 ("code-assigned severity in `src/superclaude/cli/**/*.py`"), plan:38 ("returns Blocking for a hit", names `safety_route.py`), plan:74 ("following the added paragraph step by step"), source.md:22 ("the 35 percent target"), source.md:61 ("GR12 raise-only rule"), stage-requests/README.md lines 11, 18, 25 and 47-50 (Revision 4 cancels per-stage owner summaries). All match the cards.

## Changes

| # | Status | Before | After | Provenance tag |
|---|---|---|---|---|
| C1 | applied | Verdict: ship (base) | Verdict: revise, with the reason from V2's verdict (Task 1 against the ban on code-assigned severity, F1 blocking) | Base (original, modified) per Change #1 |
| C2 | applied | no blocking finding; base F1 first | merged F1 = V2 F1 verbatim, fix extended with the check that the narrowed Constraints text names `safety_route.py` and with V1's dissent (medium) | Variant 2 F1 merged per Change #2 |
| C3 | applied | no ledger finding | merged F4 = V1 F1, placed after the twin-pin finding (merged F3) | Variant 1 F1 merged per Change #3 |
| C4 | applied | no 35 percent finding | merged F5 = V1 F5, placed after the C3 insert | Variant 1 F5 merged per Change #4 |
| C5 | applied | no smoke-check finding | merged F7 = V1 F9, placed after the lint finding (merged F6) | Variant 1 F9 merged per Change #5 |
| C6 | applied | base F2, F3, F4, F5, F6 | unchanged text, renumbered F3, F6, F8, F9, F10 | Base (original) F<m>, kept per Change #6 |
| C7 | applied | base F7 with no dissent | merged F11 = base F7 plus the unresolved C-003 note (V1 F4 wording, V2 no defect, V3 grep; either fix acceptable) | Base (original, modified) F7 per Change #7 |
| C8 | applied | coverage about 95%, one miss (F7) | coverage about 93% (V1 90, V2 95, V3 95), misses F11, F5, F4, F1 | Base (original, modified) per Change #8 |
| C9 | applied | no shared-assumption section | `shared_assumptions:` after coverage_judgement: A-002 accepted 75%, A-003 rejected 95%, A-004 qualified 65% | debate appended per Change #9 |

Changes not made (per the plan's table): V1 F2/F6 (C-002), V2 F2 (C-012), V1 F8 as a fix (C-010) and a relabel of the conflict (S-002) are not carried as findings. C-002 and C-010 are kept as the two one-line notes the plan names, in a `notes:` section after `shared_assumptions:`.

Format-only adjustments (no content change):
- Header lines persona/model_class/model replaced by `merged: persona analyzer+qa+refactorer, base V3`; reviewer_model_self_report replaced by `merge_executor:` (both from the merge brief).
- The paths line (plan = ..., source = ...) from V1's header and diff-analysis.md:3 is carried so that the `plan:` and `source:` references of the merged findings resolve.
- V1 F1 and V1 F5: the " — " separator after the location replaced by a space to fit the base card shape. V1 F5's class label "A3 confirmed, drift-minor" shortened to "drift", because "A3" pointed at V1's own assumption list, which the merged card does not carry.
- V1 F9 had no evidence field; the evidence is the plan:74 phrase V1 quotes in its claim (verified at plan:74).

## Post-merge validation

- Structural integrity: findings F1 to F12 are contiguous; each carries one `(source: V<n> F<m>)` and the 12 sources are distinct (no duplicate finding). The blocking finding is first. Section order: header, paths, Verdict, findings, coverage_judgement, shared_assumptions, notes, merge_executor. Every section and finding has a `<!-- Source: ... -->` tag.
- Count discrepancy with the plan: the plan's Risk Summary says "F1 to F13", but its changes yield 12 findings (8 base findings plus 4 inserts by C2 to C5). No 13th finding is named by any change, so none was added.
- Internal references resolved: F1 to F12 references inside the Verdict, coverage_judgement, shared_assumptions and notes all point at existing merged ids. "F1 to F6" in merged F12 names the rule ids of test_review_severity_rule.py, not card ids. Unresolved and unchanged from the base: R1 to R4 in merged F2, F3, F6 and F12 name the reviewer brief's risk items, which the card does not define (base weakness under rubric C19; no change in the plan addresses it).
- New contradictions introduced: none. The base "ship" verdict and its claim that nothing blocks are replaced by C1; merged F12 says only that the pinned scans stay green, which does not conflict with F1.

## Summary

Planned 9, applied 9, failed 0, skipped 0.
