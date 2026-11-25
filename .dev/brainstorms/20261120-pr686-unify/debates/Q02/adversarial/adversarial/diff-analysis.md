# Diff Analysis: position paper comparison (Q02, local `git branch -d` in the worktree cleanup script)

## Metadata
- Generated: 2026-11-20 (UTC)
- Variants compared: 2 (Variant 1 = OURS, Variant 2 = CLAY)
- Total differences found: 14 (structural 2, content 7, contradictions 2, unique contributions 4 listed separately, shared assumptions 3)
- Debate diff points (denominator for convergence): 14 = S 2 + C 7 + X 2 + A 3
- Categories: structural (2), content (7), contradictions (2), unique (4), shared assumptions (3)
- Extra evidence gathered by the orchestrator before the debate (read-only, 2026-11-20): of 56 local branches in the main checkout, 45 have an upstream and 21 of those are `[gone]`; no linked worktree is on `master`, `main` or `integration`; `origin/integration` exists (141e97fe) and three merged PRs have `integration` as their head branch (#664, #658, #640, all into `master`).

## Structural Differences
| # | Area | Variant 1 (OURS) | Variant 2 (CLAY) | Severity |
|---|---|---|---|---|
| S-001 | Section layout | Claim, Mechanism, Cited facts (8), Cost, Risk, What it gets right | Same sections, 9 cited facts, plus a note on how issue 687 lines are counted | Low |
| S-002 | Where the rule set lives | Rules written as a new guard list added to issue 687 | Rules taken as they already stand in issue 687 sections 3, 6 and acceptance list | Medium |

## Content Differences
| # | Topic | Variant 1 (OURS) approach | Variant 2 (CLAY) approach | Severity |
|---|---|---|---|---|
| C-001 | May the script run a local `git branch -d`? | Yes, behind guards | Yes, as issue 687 step 4 says | Low (agreed) |
| C-002 | Default and long-lived branches | Explicit refusal for `master`, `main`, `integration` and the default branch from `gh repo view` | Only rule 1 (main checkout is skipped); no branch-name refusal | High |
| C-003 | Branch that still has an open PR | Explicit refusal: no PR in any state with this head is open, and no open PR uses the branch as its base | Rule 2 (own PR MERGED) and rule 3 (HEAD equals the PR head) are taken as sufficient | Medium |
| C-004 | Commit identity check | Branch must point at the merged PR's last head commit (`headRefOid`) | Rule 3 already says HEAD equals or is an ancestor of the PR head | Low (overlap) |
| C-005 | Branch checked out in another worktree | Listed as a guard | Not listed; git refuses it itself (both papers measured this) | Low (redundant) |
| C-006 | Dry-run output | Table gains a "branch: would delete / would keep (reason)" column | Table already has one decision and one reason per worktree; branch outcome appears only as "kept" after a refusal | Medium |
| C-007 | Authority to apply | No deletion without `--apply` under a grant | `--apply` is the only switch; the daily automation is switched to apply by Clay after one report-only week | Medium |

## Contradictions
| # | Point of conflict | Variant 1 position | Variant 2 position | Impact |
|---|---|---|---|---|
| X-001 | What `git branch -d` protects | "`-d` means pushed or merged, not 'its PR landed'" (fact 2; measured: deleted a pushed, unmerged branch) | Cites D13: "`-d` refuses an unmerged branch" (fact 8) as a safety reason, while also admitting the pushed-branch case under Risk | Medium |
| X-002 | Is an open-PR guard missing from the nine rules? | Fact 5: rule 2 takes the newest merged PR "when there are several", so a branch with an older merged PR and a newer open PR is not explicitly blocked | Mechanism: rules 2 and 3 cover it; HEAD must equal the merged PR's head | Medium |

## Unique Contributions
| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | Variant 1 | Evidence that `-d` has no default-branch or long-lived-branch protection (measured `integration` and `master` deletions) plus the real `integration` branch | High |
| U-002 | Variant 1 | "The script must not behave looser than Orca" (Orca's own rm keeps branches it cannot prove merged) | Medium |
| U-003 | Variant 2 | The never-force acceptance test (records every command, fails on `-D`, `rm`, `prune`, remote delete) already exists in issue 687 | High |
| U-004 | Variant 2 | Context that merged branches pile up (`deleteBranchOnMerge: false`, squash allowed), so the cleanup has a real job, and a deleted local branch is recoverable | Medium |

## Shared Assumptions
| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | `origin/<branch>` still exists when a local branch is removed, so "recreate from origin" works | Both say the branch "remains on GitHub" (V1 Cost/Risk, V2 Risk) | If the remote branch was deleted, recovery needs the PR ref `refs/pull/N/head`, not `origin/<branch>`; UNSTATED in both | UNSTATED (promoted) |
| A-002 | `git branch -d` judges "merged" against the branch's upstream if one is set, else against the HEAD of the checkout the script runs in; both treat it as one fixed test | Both rely on `-d` refusals (V1 facts 2-3, V2 fact 6) | 45 of 56 local branches here have an upstream; the guard state differs per branch and per checkout; UNSTATED in both | UNSTATED (promoted) |
| A-003 | `gh pr list --head <branch>` finds the right PR for a branch name | Both lean on issue 687 rule 2 | Same branch name in a fork or a reused name could match another PR; a state guard against a wrong match is not stated | UNSTATED (promoted) |

## Summary
- Total structural differences: 2
- Total content differences: 7
- Total contradictions: 2
- Total unique contributions: 4
- Total shared assumptions surfaced: 3 (UNSTATED: 3, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-002
