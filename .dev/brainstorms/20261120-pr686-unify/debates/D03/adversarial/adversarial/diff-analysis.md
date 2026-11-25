# Diff Analysis: position paper comparison (D03, PR 682 deletion of the issue pipeline)

## Metadata

- Generated: 2026-11-20 (UTC)
- Variants compared: 2 (variant 1 = OURS, "revert PR 682 and restore the gate"; variant 2 = CLAY, "keep PR 682")
- Total differences found: 18 (diff points that enter convergence: S 2, C 10, X 2, A 4)
- Categories: structural (2), content (10), contradictions (2), unique (9), shared assumptions (4)
- Taxonomy level per point is given in the last column of each table (L1 surface, L2 structural, L3 state mechanics)

## Structural Differences

| # | Area | Variant 1 (OURS) | Variant 2 (CLAY) | Severity | Level |
|---|------|------------------|------------------|----------|-------|
| S-001 | Section outline | Claim, Mechanism, Cited facts (9), Costs, Risks, Gets right | Same six sections, same order, 9 cited facts | Low | L1 |
| S-002 | What "Mechanism" describes | How to perform the revert (git revert, 3 conflicting files, rebase of the owner branch) | How the design replaces the gate (creation-time plan sections, hold check, write-ahead log) | Medium | L2 |

## Content Differences

| # | Topic | Variant 1 (OURS) approach | Variant 2 (CLAY) approach | Severity | Level |
|---|-------|---------------------------|---------------------------|----------|-------|
| C-001 | Did the code "run live"? | Eleven RECORDED lines (a to k) of the FU-1 live test on throwaway issue 452 (`issue-pipeline-fu1.md:108-118`); only the cron watcher never ran | PR 682 body: "never ran live", watcher `enabled: false` | Medium | L3 |
| C-002 | Protections pinned by tests (one winner on a race, kill between `worker-start` and `adopt-mark`, bot and edited approvals refused) | These exist only in the deleted tests; no code on master has them; replacement is design text (`orchestrator.md:568, 1108-1112`) | Replacement is specified with named PR B tests and the poll lock keeps one winner per cycle; admits it is not built | High | L3 |
| C-003 | Human approval of a plan before a worker builds | Gone and not replaced; `hold.py` checks headings only | Plan is reviewed at creation (`/sc:issue --create` requires Priority, Fix approach, Test plan, PRs 651 and 661); hold check is the poll-side backstop | High | L2 |
| C-004 | Same-login weakness (risk L-1, `owner-answers.md:126`) | Accepted risk the old safeguards (plan hash, plan reply unedited, label after reply) reduce; kept | Evidence that the actor-type rule cannot tell owner from agent (FU-1 record j) so the gate is weaker than it looks | Medium | L3 |
| C-005 | Removal order (`orchestrator.md:982`: package imports `issue_watch` symbols PR 686 deletes) | PR 686 and the restored package cannot land as written; a consequence to be settled by D01 | Reason to delete first so PR 686 needs no shim | Medium | L2 |
| C-006 | Cost of each choice | Revert: 3 conflicting files (CHANGELOG.md, WORKER-CONTRACT.md one line, `test_worker_contract.py`), guard re-review | Keep: owner branch (53 files, 975 lines of `complete.py` and tests) must be reworked | Medium | L2 |
| C-007 | Process: how the reversal came about | Reversed merged owner work (PRs 584, 591) in 66 minutes with no human review and without naming decision 6 | Written question to `@ironbelly` on issue 450 (2026-11-18 17:00:32) and stated reasons on issue 655 | Medium | L2 |
| C-008 | Stale text on master (`issue.md:85`, `SKILL.md:140`, `refs/claim.md:96`, runbooks) | Dangling references to the removed coordinator duty | Acknowledged; PR E adds banners | Low | L2 |
| C-009 | Guard and contract changes inside PR 682 | Guard comment at `launch-level-guard.sh:496` and G2 design now disagree | Careful scope: rule 2 kept, `ask`/`send` no `--to` bullet added (finding F14 of issue 665), worker-guard test rewritten, independent review PASS | Low | L3 |
| C-010 | Latency and burden of the gate | Concedes Q36 "latency approved for now" | Uses Q36 and the grant row per issue as the main cost of the gate | Low | L2 |

## Contradictions

| # | Point of Conflict | Variant 1 position | Variant 2 position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Statement "never ran live" | Text of fact 3: "only half true" (FU-1 live record of the handoff on issue 452) | Facts 1 and 9 and the Claim: "never ran in production", watcher off | Medium: both are true at different scope (watcher cron vs the handoff pieces); resolves by scoping the claim |
| X-002 | Meaning of the issue 450 comment | Fact 2: reversal had no recorded agreement of the owner | Fact 2: ruling "came from a written question to the owner" | Medium: both quote the same text (`@ironbelly ... What do you think?`) and agree no answer exists; they disagree on whether silence is consent |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 | Concrete revert mechanics: only 3 of 36 files changed on master since 682 (`git diff --name-only 01e7a9e23 origin/master`) | High |
| U-002 | 1 | Owner branch edits the exact guard case (`launch-level-guard.sh:445-455`) PR 682 removed and adds `complete.py` | High |
| U-003 | 1 | Named tests that pin the protections (`test_approval_concurrency.py:60,71`, `test_approval_crash.py:45`, ...) | High |
| U-004 | 1 | Master text still refers to the removed coordinator duty | Medium |
| U-005 | 2 | Design 7.2 and 7.3 give a file-by-file removal plan and what guard G2 still needs | Medium |
| U-006 | 2 | Plan sections are now enforced at issue creation (`SKILL.md:102`, PRs 651, 661) | High |
| U-007 | 2 | Separable hardening in PR 682: no-`--to` bullet (F14), rewritten worker-guard test, cli-groups doc fix | High |
| U-008 | 2 | PR B test rows for write-ahead log and exclusive create (`orchestrator.md:1108-1112`) | Medium |
| U-009 | 2 | Actor-type weakness shown by FU-1 record j | Medium |

## Shared Assumptions

Agreement points found: (a) the watcher is off today so nothing is exposed; (b) guard rule 2 and the no-`--to` contract sentence must survive; (c) the gate costs latency and a coordinator; (d) PR B does not exist so equal double-start protection is not built.

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|-------|-----------|------------------|----------------|--------|--------|
| A-001 | The watcher stays disabled (or capped at launch level none) until the owner decides, so the time window for the missing gate is harmless | (a) | UNSTATED (V2 states it as fact 9; V1 never contests it); partly CONTRADICTED by owner row R18 (generated config is `enabled: true`), held back only by the closed ship gate R33 | Medium | Promoted, level L3 (state) |
| A-002 | "The owner" who rules on the gate is one identifiable person whose recorded decisions bind | (c) and the process facts | UNSTATED in V2 (design calls Clay "the owner"), STATED in V1 (ironbelly, decision 6) | High | Promoted, level L2 |
| A-003 | A revert PR (or a keep) can be settled independently of D01 (whether any approval gate should exist) | (d) | UNSTATED: V1 mentions D01 as a risk; V2 never does | High | Promoted, level L2 |
| A-004 | The restored or replacement double-start protection is judged by test presence, not by a live measurement | (d) | UNSTATED: neither paper shows the replacement or the restore has been run against a real race | Medium | Promoted, level L3 (race condition) |

## Summary

- Total structural differences: 2
- Total content differences: 10
- Total contradictions: 2
- Total unique contributions: 9
- Total shared assumptions surfaced: 4 (UNSTATED: 4, STATED: 0 as a whole, CONTRADICTED: 1 in part, A-001)
- Highest-severity items: C-002, C-003, A-002, A-003
- Taxonomy counts: L1 1, L2 11 (S-002, C-003, C-005, C-006, C-007, C-008, C-010, A-002, A-003 plus X-001 X-002 grouped as L2), L3 6 (C-001, C-002, C-004, C-009, A-001, A-004)
- total_diff_points for convergence = S 2 + C 10 + X 2 + A 4 = 18
