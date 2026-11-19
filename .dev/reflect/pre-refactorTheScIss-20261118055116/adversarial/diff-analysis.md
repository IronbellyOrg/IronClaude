# Diff Analysis: reviewer-card Comparison

## Metadata

- Generated: 2026-11-18T05:57:00Z
- Variants compared: 3 (variant-1 = reviewer 1, analyzer, sonnet; variant-2 = reviewer 2, qa, haiku; variant-3 = reviewer 3, refactorer, opus)
- Subject under review: the plan `TASK-WF-refactorTheScIss-20261118-054817` against its source prompt
- Total differences found: 2 structural, 9 content, 3 contradictions, 6 unique contributions, 3 shared assumptions
- Categories: structural (2), content (9), contradictions (3), unique (6), shared assumptions (3)
- Debate topic level of each point (AD-5): L1 surface, L2 structural, L3 state mechanics (tagged by signal words)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity | Level |
|---|---|---|---|---|---|---|
| S-001 | Overall verdict | PASS-WITH-GAPS (0.80) | PASS-WITH-GAPS (0.90) | FAIL (0.78), one blocking finding | High | L2 |
| S-002 | Granularity and format of findings | 4 findings, 2 medium and 2 note | 2 findings, both medium | 7 findings, 1 blocking, 3 medium, 3 note; each has an explicit fix | Low | L1 |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity | Level |
|---|---|---|---|---|---|---|
| C-001 | The clause "even though `full` is the default" in `issue.md:44` and `commands.md:371` becomes false once the default is picked from the issue | medium (F1): drop or reword it | medium (F2): remove it, keep the STOP rule | blocking (F1): drop it in Task 3 and Task 6, and add a test assertion | High | L1 |
| C-002 | Order of "bug gives full" against "unreadable gives worktree" in the new Wave 5 step | note (F3): put the unreadable check first, test the order | not raised | medium (F2): say which wins, pin the order in Task 5 | Medium | L3 |
| C-003 | What the `Level:` line prints when the claim finds an agent already launched (stored level wins) | medium (F2): print it only for `launched`, pin a phrase | not raised | medium (F4): print the stored level for `already_launched`, and name the failed worktree and failed launch cases | High | L3 |
| C-004 | Whether a test pins that the final output repeats the `Level:` line | not raised | medium (F1): add an assertion and a mutation check | touched only inside F4 (final output paths) | Medium | L2 |
| C-005 | The plan's Constraint says the thresholds live only in `refs/claim.md`, yet Tasks 3, 6, 7 and 8 copy them into five more places | not raised | not raised | medium (F3): reword the Constraint or drop the numbers from non-record files | Medium | L2 |
| C-006 | `SKILL.md` line 92 (source) against line 89 (plan) | coverage note: line 92 stays true, say so | not raised | note (F5): add one sentence that line 92 needs no change | Low | L1 |
| C-007 | The `-k "st7 or st9 or worker_contract"` filter in Task 1 | note (F4): drop `worker_contract` | not raised | not raised | Low | L1 |
| C-008 | Decision P4 in `docs/designs/sc-issue-claim-pipeline-flag.md` ("The default stop is an approved plan") gets no amendment | not raised | not raised | note (F6): add the note inside its last cell | Low | L2 |
| C-009 | Architecture reference cites of `refs/claim.md:<line>` shift when Wave 5 steps move down | not raised | not raised | note (F7): out of scope, or refresh in Task 6 | Low | L2 |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact |
|---|---|---|---|---|---|
| X-001 | Severity of the stale "default" clause (C-001) | medium | medium | blocking | Medium |
| X-002 | Whether coverage is complete | "no under-covered requirement" (it did not re-derive the 16 rows) | "all 16 have planned implementation coverage" | "also in the final output" is only partly covered, and bug against unreadable has no order | High |
| X-003 | Whether Task 5's planned test can detect an order mistake | not stated, but F3 says the test only checks that each sentence exists | "Task 5 specifies unreadable-case and ordering assertions capable of detecting its two stated mutations" | F2: "the Task 5 test does not pin which one" wins | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | Variant 3 | Five extra copies of the thresholds contradict the plan's single-source Constraint (C-005) | High |
| U-002 | Variant 2 | A test gap: removing the final-output `Level:` instruction would leave every planned assertion green (C-004) | Medium |
| U-003 | Variant 3 | Failed-worktree and failed-launch paths also need a stated final-output behaviour (part of C-003) | Medium |
| U-004 | Variant 3 | Decision P4 needs an amendment note (C-008) | Low |
| U-005 | Variant 1 | The `-k` filter selects nothing for `worker_contract` (C-007) | Low |
| U-006 | Variant 3 | Architecture cites are already off by two lines (C-009) | Low |

## Shared Assumptions

| # | Assumption | Source Agreement | Classification | Impact | Status | Level |
|---|---|---|---|---|---|---|
| A-001 | The coverage matrix's 16 inferred rows are a complete decomposition of the source prompt | No variant re-derived the rows; variants 1 and 3 say so, variant 2 read the matrix | UNSTATED | A missed requirement would stay missed in all three cards | Promoted | L2 |
| A-002 | The plan runs on a checkout that already carries the first package's staged edits, so the "default" wording it wants to rewrite is the new `full` wording | All three quote `issue.md:44` and `commands.md:371` as they are today | UNSTATED | If the plan ran on the older state, the stale-clause finding would not exist | Promoted | L3 |
| A-003 | A re-claim re-runs Wave 5 and so recomputes the level from `issue-summary.md` each time | Variants 1 and 3 build C-003 on it; variant 2 does not mention it | UNSTATED | The stored-level finding depends on a state that can change between claims | Promoted | L3 |

## Summary

- Total structural differences: 2
- Total content differences: 9
- Total contradictions: 3
- Total unique contributions: 6
- Total shared assumptions surfaced: 3 (UNSTATED: 3, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: S-001, C-001, C-003, X-002
