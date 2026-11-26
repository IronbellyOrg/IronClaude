# Refactor plan (merge into variant 3)

Base: `variant-3-original.md`. Others: `variant-1-original.md`, `variant-2-original.md`. Debate evidence: `debate/round1-advocate-{1,2,3}.md`, `scoring/round1-votes.json`. Severity rule: the review severity rule of the session style (Blocking = Decision, Missing or Safety; Medium = real defect nothing named rests on; Note = form only). `PLAN` = the plan file, `DESIGN` = its `source.md`.

## Final merged rows (grades by Round 1 majority of three advocates)

| Row | Diff point | Source | Grade | Label | Action |
|---|---|---|---|---|---|
| M-01 | C-001 Task 28 no-key reply rule contradicts DESIGN:387 (FR-122); pinned again in Task 28 and Task 34 | V2 | Blocking (Decision) | HIGH | add to base; first-review M-10 recorded as regressed |
| M-02 | C-002 Task 19 rewrites `git.md` with no plugin twin copy and `cmp` until Task 25 | V3 | Blocking (Decision) | HIGH | keep |
| M-03 | C-003 / C-017 Task 4 from-scratch env and git-lfs make `snapshot_lossless` always false on this machine; Task 5 tests only the false case | V3 | Medium | - | keep, merge the advisory |
| M-04 | C-004 Task 32 base-commit comparison in the permanent test file vs CI depth 1 | V3 | Medium | - | keep |
| M-05 | C-005 override of T-16 recorded only for Task 32 `_ALLOW`; Tasks 26, 30, 31 edit scanned files | V3 | Medium (votes Note, Blocking, Medium; median Medium) | - | keep |
| M-06 | C-006 Task 31 grep forbids `reason=index-locked` in `SKILL.md`, matching Task 26's own stop | V3 | Medium | - | keep |
| M-07 | C-007 test-first Constraint cannot be followed in Tasks 19 to 23 and 26 to 33 | V1 | Medium | - | add |
| M-08 | C-008 `validate_argv(argv)` cannot tell agent argv from the runner's private-index call | V1, V3 | Medium (votes Note, Medium, Medium) | - | keep |
| M-09 | C-009 Task 17 acceptance lacks FR-109 / T-19 cases | V1 | Medium | - | add |
| M-10 | C-010 `record-skipped` not tied to the flag | V1 | Medium | - | add |
| M-11 | C-011 `version` argv form undefined | V1 | Note | - | add |
| M-12 | C-012 Task 13 cites a `why` the design does not name | V1 | Note | - | add |
| M-13 | C-013 Task 30 `git diff` compares with the index, not the base | V1, V3 | Note | - | keep |
| M-14 | C-015 Task 9 says nine regexes, lines hold eleven compiled patterns | V3 | Note | - | keep |
| M-15 | C-016 checks reading `git ls-files` see new files only after commit | V3 | Note | - | keep |
| M-16 | C-018 NFR-013 has no acceptance check (first-review M-27, carried forward) | V2 | Note | - | add |

Counts: Blocking 2 (label HIGH 2), Medium 8 (M-03 to M-10; the C-003 and C-017 advisory are one row, M-03), Note 6 (M-11 to M-16). The merge executor must print the exact counts it ends with; the orchestrator reconciles them with `return-contract.yaml`.

C-014 (budget tightness) is not a defect by majority and is dropped. C-019 (26-id disposition) is a coverage note, not a finding.

## Changes not being made

- V1's "No Blocking defect found" verdict is rejected (X-002 settled for V2).
- V2's Blocking grade for C-004, C-005, C-006, C-010 is rejected: no named decision, acceptance check or quoted number changes if the text is corrected.
- V1 and V3 status "first-review M-10 resolved" is replaced by "regressed" (X-001 settled for V2).

## Required form of the merged output

Prior-blocker table (first-review M-01 to M-11: ten resolved, M-10 regressed), the deviation table above with plan and design evidence lines, a coverage note for the 26 unnamed ids (17 inactive or historical, 8 covered, 1 gap), the finding counts, and a `follow-up candidates` list for the Medium rows. Keep every citation as written in the variant cards; the evidence validator will check them.
