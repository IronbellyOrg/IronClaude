# Refactoring Plan (Q02)

## Overview
- Base: Variant 1 (OURS), `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q02/adversarial/adversarial/variant-1-original.md`
- Incorporated from: Variant 2 (CLAY), `.../variant-2-original.md`
- Planned changes: 7 (additions 4, removals 2, restructure 1)
- Overall risk: Low (all changes are text edits to a position paper; no code)
- Output file: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q02/adversarial/merged-hybrid-position.md`

## Planned Changes

### Change 1: Rewrite the Mechanism as an addendum to issue 687's rules (S-002)
- Source: Variant 2, Mechanism and Claim
- Target: Variant 1 "Mechanism"
- Approach: restructure
- Rationale: both advocates say keep issue 687's rule set and step order in place and add only the branch-specific refusals; no parallel guard list (S-002, 75%)
- Risk: Low
- Content: the mechanism says the order is issue 687's (save `.dev`, remove without `--force`, `git branch -d`, read back) and that the branch step has exactly these added refusals.

### Change 2: Keep the default and long-lived branch refusal (C-002, base strength)
- Source: Variant 1 Mechanism and facts 2 to 4; Variant 2 concession 2
- Target: Mechanism
- Approach: keep, tighten wording
- Rationale: C-002 won by Variant 1 at 92%. Refuse `master`, `main`, `integration` and the repo default branch from `gh repo view`. Cite `origin/integration` at 141e97fe and merged PRs #664, #658, #640 whose head is `integration`. State that today's risk is latent (no worktree on those names now; today's `integration` tip fails rule 3) but the fix is a few lines.

### Change 3: Replace the open-PR guard with one line in rule 2 (C-003, X-002)
- Source: both advocates (HYBRID)
- Target: Mechanism
- Approach: replace
- Rationale: "keep the branch if any PR with this head is OPEN" (one added sentence in rule 2). Remove "no open PR uses it as its base" (speculative; no measured case; both advocates). State the wording gap of rule 2 ("newest merged one when there are several") as evidence, marked as not shown to occur in practice.

### Change 4: Remove two guards that git or rule 3 already provide (C-004, C-005)
- Source: Variant 1 concessions 1 and 2; Variant 2 strength 3
- Target: Mechanism
- Approach: delete
- Rationale: drop "no other worktree has it checked out" (git refuses it: `cannot delete branch ... used by worktree`) and the exact `headRefOid` match; use rule 3 as written (HEAD equals the merged PR's last head commit or is an ancestor of it). Record the reason: a ref at an ancestor of the PR head holds no commit the PR head lacks.

### Change 5: Add the dry-run branch column and the logged PR head SHA (C-006, A-001)
- Source: Variant 1 (C-006); both advocates on A-001
- Target: Mechanism
- Approach: insert
- Rationale: the table prints "branch: would delete / would keep (reason)" per row, plus the merged PR's head SHA so a branch can be recreated from `refs/pull/N/head` when `origin/<branch>` is gone (21 of 56 local branches here have an upstream that is `[gone]`).

### Change 6: Add the never-force acceptance test and the PR owner check (U-003, A-003)
- Source: Variant 2 facts 3 and advocate A-003 answer
- Target: Mechanism and Cost
- Approach: insert
- Rationale: add the issue 687 acceptance test (records every command, fails on `--force`, `-D`, `rm`, `prune`, a push to anything but the evidence remote, a remote branch delete), and extend rule 2 to require the PR's `headRepositoryOwner` to be ours and its head SHA to match. Cost line changes from "about 4 tests" to the number of added cases (open-PR line, default branch refusal, dry-run column, owner check), without inventing a count beyond "four".

### Change 7: Add the rollout step and the correction of `-d`'s meaning (C-007, X-001, A-002)
- Source: Variant 2 (rollout); Variant 1 fact 2
- Target: Claim, Risk
- Approach: insert
- Rationale: state plainly that `-d` means "merged to its upstream, or to the HEAD of the checkout the script runs in", not "its PR landed", so rules 2 and 3 are the gate and `-d` is a last backstop; the daily automation runs report-only for the first week before `--apply` (issue 687 rollout ladder). Whether the coordinator may run `--apply` stays under a grant row (D13), not decided here.

## Changes NOT Being Made
| Diff point | Variant 2 approach | Why the base wins |
|---|---|---|
| C-002 | No branch-name refusal; rely on rule 1 and git | `-d` deleted `master` and `integration` in the scratch repo; V2 conceded |
| C-006 | Branch outcome shown only after a refusal | A person approving `--apply` cannot see which branches go; V2 conceded |
| X-001 | D13's "`-d` refuses an unmerged branch" as the safety reason | Reproduced counter-case (`feat-pushed`); V2 withdrew it |

## Risk Summary
| Change | Risk | Impact if wrong | Rollback |
|---|---|---|---|
| 1 | Low | A reader misses the added refusals | Re-edit text |
| 2 | Low | A branch name missing from the list | Add the name |
| 3 | Low | Over-keeping a branch (cosmetic) | Remove the sentence |
| 4 | Low | A redundant guard later proves needed | Re-add it |
| 5 | Low | Column omitted by the builder | Fix the issue text |
| 6 | Low | Owner check blocks a valid same-owner PR | Relax the check |
| 7 | Low | Overstates what `-d` checks | Reword |

## Review Status
Auto-approved (unattended, non-interactive). Timestamp: 2026-11-20.
