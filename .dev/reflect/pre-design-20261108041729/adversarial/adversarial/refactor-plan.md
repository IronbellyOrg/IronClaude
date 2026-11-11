# Refactoring Plan

## Overview
- Base: variant 3 (`variant-3-original.md`, reviewer 3 card)
- Incorporated from: variant 1 (sonnet) and variant 2 (haiku)
- Output: one merged review card with the settled findings, one blocking finding, severities as settled by the debate
- Change count: 8 planned, 7 rejected or narrowed
- Overall risk: Low (content merge of review findings)
- Output path for the merged artifact: `.dev/reflect/pre-design-20261108041729/adversarial/merged-reviewer-verdict.md`

## Planned Changes

| # | Change | Source | Target in base | Rationale (debate evidence) | Risk |
|---|---|---|---|---|---|
| 1 | Add to R3-F1 the checker range `test_worker_contract.py:2005-2012` and the rule that `gh api -X POST` lines must not be classified read-only (`:3150-3156`); state that the new keys must be rebuilt from the post-edit text | V1 R1-F1; A-002 QUALIFY (V1, V3) | R3-F1 evidence and recommendation | C-001 95%; A-002 QUALIFY | Low |
| 2 | Add a new finding for the strength of Task 8's new tests (exact output formats of specification 2.4; Q7 type rules and Q8 depth pairs), severity minor-to-medium, not blocking | V2 R2-F1, R2-F2; V1 and V3 advocates | new finding after R3-F2 | C-002 75%; V2's advocate conceded blocking was too strong | Low |
| 3 | Add finding for the Will / Will Not test that reads only `SKILL`, so Task 7's "keep unchanged" proves no agreement | V2 R2-F3 | new finding | C-009 90% | Low |
| 4 | Extend R3-F3 (`complexity-field.json`) to name the Task 1 and Task 2 gap in the plan (the plan never names the file) | V1 R1-F3 | R3-F3 | C-004 85% | Low |
| 5 | Add finding that Constraint 5 ("writes exactly two things") also leaves out the retained mode label, not only the pushback comment | V1 R1-F5, V2 R2-F4 | new finding | C-005 85% | Low |
| 6 | Add the `orgs/` scanner guard: the regex must handle the spaced spelling (V3) and the self-check test must feed a prose sentence that must not be reported (V1) | V1 R1-F4 | R3-F6 | C-002 | Low |
| 7 | Add finding that no new Task 8 test pins what Task 3 adds to `SKILL.md`, so a revert of Task 3 turns only the Task 7 test red | V1 R1-F6 (narrowed), V3 advocate | new finding | X-001 65% | Low |
| 8 | Fix severity labels: all findings except C-001 are minor or medium; list the severity disagreement in the card notes | debate | card header | V2 advocate concession | Low |

## Changes NOT Being Made

| Point | Non-base approach | Why rejected |
|---|---|---|
| R2-F1, R2-F2 "blocking" label | V2 | Task 8 copies design tests 4 and 6 (source.md:114, :116); the gap is inherited from the design, so it is Medium |
| R1-F6 "reverting any of Tasks 1-5 leaves no new test red" | V1 | Wrong for Task 4: new test 5 asserts the scout headings. Only the Task 3 version (change 7) is kept |
| R1-F7 matrix task-id note | V1 | Correct but not actionable; kept out of the card |
| R1-F2 as a separate finding | V1 | Same as R3-F2 in the base; V3's version is more concrete |
| R3-F7 severity | base | Lowered to Low: the ambiguity at `SKILL.md:107` vs `:121` pre-dates the plan |
| R3-F4 `create.md:34` half | base | Already in Task 2's scope; only the worker half stays |
| R3-F5 line 330 | base | Partly covered by Task 10's acceptance; lines 34 and 331 stay |

## Risk Summary
All changes are additive edits to a findings list; rollback is to keep the base card unchanged.

## Review Status
Auto-approved (non-interactive).
