<!-- Provenance: produced by /sc:adversarial -->
<!-- Base: Variant 1 (OURS) -->
<!-- Incorporated from: Variant 2 (CLAY) -->
<!-- Merge date: 2026-11-20 -->

# Position HYBRID (Q02): a local `git branch -d` is allowed, as an addendum to issue 687's rules, with these added refusals

<!-- Source: Base (original, modified) - title now states the hybrid position (Changes #1, #2, #3) -->

## Claim

<!-- Source: Base (original, modified) - guard-list framing replaced by "addendum to issue 687"; "-d" meaning corrected per Change #7 -->
The owner asked for branch cleanup with "extra rigid and strict validation" (issue 339, the owner's issue for one orchestrator for all sessions; owner comment 2026-11-05 13:43Z, quoted in D13 VERDICT.md). Issue 687 (Clay's request for a daily worktree cleanup, open, author `clayphi`) already makes `git branch -d` step 4 of a removal, never `-D`. The answer is yes: a local `git branch -d` is allowed, as an addendum to issue 687's rules. It is not a second rule set. The addendum adds a short list of refusals that git and issue 687 do not already give.

`-d` is not itself the guard. It means "merged to its upstream, or to the HEAD of the checkout the script runs in". It does not mean "its pull request landed". So issue 687's rules 2 and 3 are the gate, and `-d` is a last backstop behind them. The reason D13 VERDICT.md gave for a yes ("`-d` refuses an unmerged branch") is not relied on here, because a measured counter-case exists (fact 3).

## Mechanism

<!-- Source: Base (original, modified) - restructured as an addendum to issue 687's rules; Variant 2 (CLAY), Mechanism and Claim - merged per Change #1 -->
The order of a removal stays exactly as issue 687 has it: save `.dev` files, remove the worktree without `--force`, run `git branch -d <branch>`, read back. Issue 687's nine rules stay as written. Its handling of a git refusal also stays: if git refuses (for example "not fully merged" after a squash merge), the branch is reported "kept", which is not an error. Dry run is the default and `--apply` is the only way to remove. Whether the coordinator may run `--apply` stays under a grant row (D13) and is not decided here.

The branch step adds exactly these refusals and nothing else:

<!-- Source: Base (original, modified) - keep and tighten wording per Change #2 -->
1. **Default and long-lived branches.** Never delete `master`, `main`, `integration`, or the repo default branch as read from `gh repo view`. This is a few lines of code. Today's risk is latent: no linked worktree sits on those names now (checked read-only with `git worktree list --porcelain` on 2026-11-20, recorded in diff-analysis.md), and today's `integration` tip fails issue 687's rule 3 (checked by the V1 advocate with `git merge-base --is-ancestor`). The refusal protects the day a worktree on `integration` has a merged PR whose head is `integration`.

<!-- Source: Base (original, modified) - open-PR guard replaced by one added line in rule 2, per Change #3 (both advocates, HYBRID); the "open PR uses it as its base" guard is removed as speculative -->
2. **Open PR on the same head.** One added sentence in issue 687's rule 2: keep the branch if any PR with this head is OPEN. Rule 2 as written takes the "newest merged" PR "when there are several", so an older merged PR next to a newer open one is not named. No case of this was shown to occur in practice; the sentence closes the wording gap only. The earlier idea of also refusing when an open PR uses the branch as its base is dropped: no measured case supports it.

<!-- Source: Variant 2 (CLAY), fact 3 and advocate A-003 answer - merged per Change #6 -->
3. **PR owner check.** Rule 2 also requires the merged PR's `headRepositoryOwner` to be ours, so a PR from a fork with the same branch name cannot stand in. Rule 3 then compares the worktree's HEAD with that PR's head commit.

<!-- Source: Base (original, modified) - "no other worktree" guard and exact headRefOid match removed per Change #4 (C-004, C-005) -->
Two guards from the earlier draft are not added, because something else already provides them:
- "No other worktree has the branch checked out". Git refuses this itself (`cannot delete branch ... used by worktree`; measured, fact 7).
- An exact match of the PR's last head commit (`headRefOid`). Rule 3 is used as written in issue 687: HEAD equals the pull request's last head commit (`headRefOid`), or is an ancestor of it (checked against the issue text, rule table row 3). A ref at an ancestor of the PR head holds no commit the PR head lacks.

<!-- Source: Base (original, modified) - dry-run column kept; logged PR head SHA added per Change #5 (C-006, A-001) -->
4. **Dry run shows the branch action.** The table prints "branch: would delete / would keep (reason)" per row, plus the merged PR's head SHA. With that SHA, a branch can be recreated from `refs/pull/N/head` when `origin/<branch>` is gone. This matters here: 21 of 56 local branches in the main checkout have an upstream that is `[gone]` (measured read-only with `git for-each-ref` on 2026-11-20, recorded in diff-analysis.md).

<!-- Source: Variant 2 (CLAY), fact 3 - merged per Change #6; Base (original) for the command form -->
5. **Never force.** The command is exactly `git branch -d <name>` (never `-D`, never `--force`). Remote branches are never touched. Issue 687's acceptance test stays: it records every command and fails on `--force`, `-D`, `rm`, `prune`, a push to anything but the evidence remote, or a remote branch delete.

## Cited facts

<!-- Source: Base (original), facts 1 to 8, kept or reworded; Variant 2 (CLAY) facts 1 to 3 and 6 - merged per Changes #1, #4, #6 -->
1. Owner comment on issue 339 (the owner's issue: one orchestrator for all sessions), 2026-11-05 13:43Z: cleanup of worktrees and branches "with extra rigid and strict validation". Source: D13 VERDICT.md, Strongest points OURS 1 (`gh issue view 339`).
2. Issue 687 (Clay's request for a daily worktree cleanup) body, section 3 step 4: "Remove the local branch with `git branch -d`, never `-D`... the branch is then reported as kept, which is not an error... the branch and its commits remain on GitHub and the worktree can be recreated." Its scope list says "(b) The local branch of each removed worktree, with `-d` only." Its "Things the script never does" list has no `--force`, no `git branch -D`, no `rm`, no remote branch delete, no `git worktree prune`. (Line references are to the issue body saved by `gh issue view 687 --repo IronbellyOrg/IronClaude --json body --jq .body`, not GitHub line numbers.) Source: Variant 2 facts 1 to 3.
3. Measured in a scratch repo (git 2.47.3, `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q02/scratch/t`): `git branch -d feat-pushed` deleted a branch that was pushed but NOT merged to HEAD (git only warned "merged to origin/feat-pushed, but not yet merged to HEAD"). So `-d` means "pushed or merged", not "its PR landed".
4. Same test: `git branch -d integration` (merged into master) succeeded, and `git branch -d master` from another branch succeeded. `-d` has no default-branch or long-lived-branch protection.
5. This repo has a long-lived `integration` branch on origin (`git ls-remote --heads origin integration` returned 141e97fe...) and the project CLAUDE.md names the flow `master <- integration <- feature/*`. Merged PRs #664, #658 and #640 (three merged pull requests into `master`) have `integration` as their head (`gh pr list --repo IronbellyOrg/IronClaude --head integration --state all`, read-only, 2026-11-20). A worktree on `integration` with a merged PR could pass issue 687's rules 2 and 3 as written, which is why refusal 1 exists.
6. Issue 687 rule 2 takes the "newest merged" PR "when there are several" (rule table, row 2). A branch with an older merged PR and a newer open PR is not explicitly named by rule 2. Only rule 3 (HEAD at the merged PR head) catches new commits. This wording gap is not shown to occur in practice.
7. Measured in the same scratch repo (git 2.47.3): `git branch -d` refused a never-pushed unmerged branch, refused a squash-merged branch whose remote copy was deleted, and refused a branch checked out in another worktree. Issue 687 states the squash and dirty-worktree refusals were tested on 2026-11-20. Source: Variant 2 fact 6.
8. `WORKER-CONTRACT.md` lines 236-237 (master snapshot) already let the coordinator delete a child branch after merge-back, and forbid removing "a worktree or branch that holds unmerged commits, an open PR, uncommitted changes..." without the user's instruction. The owner's contract already states the open-PR and unmerged limits.
9. `docs/designs/orchestrator.md` line 139 (ADD5): "deleting branches is human-only, rule 1", and issue 687 keeps remote branch deletion human-only. Local `-d` is a different, recoverable act.
10. `orca worktree rm --help`: removal "also attempts to delete the checked-out local branch, with or without --force. Orca retains branches it knows predated the worktree and any branch whose changes it cannot prove are already merged." So Orca-listed worktrees already lose their local branch; the script must not behave looser than Orca.

## Cost

<!-- Source: Base (original, modified) - test count reworded per Change #6 -->
Four added cases: the open-PR line in rule 2, the default and long-lived branch refusal, the dry-run branch column with the logged PR head SHA, and the PR owner check. Issue 687's own acceptance test (the never-force command recorder) is reused and is not new. No new tool, and no parallel guard list: the refusals sit inside issue 687's existing step order.

## Risk

<!-- Source: Base (original, modified) - rollout step and "-d" correction added per Change #7; owner-check risk per Change #6 -->
Over-strict guards leave stale local branches; that is a cosmetic cost. The PR owner check may block a valid same-owner PR; relax it if so. Under-strict guards delete `integration` or a branch that still has an open PR; recovery needs the reflog or the remote copy. The residual risk is that `-d` can delete a pushed branch not merged to HEAD (measured, fact 3). Rules 2 and 3 plus the added refusals are what contain it, since `-d` is only a backstop.

Rollout follows issue 687's ladder: the daily automation runs report-only for the first week before `--apply` is used. Who may run `--apply` stays under a grant row (D13), not decided here.

## What it gets right

<!-- Source: Base (original), reworded to match the hybrid -->
Fail-closed everywhere, a human-visible dry run that shows each branch outcome before anyone approves `--apply`, remote deletion left to a person, one rule set (issue 687's) with a short addendum instead of a second list, and no reliance on one git flag to carry the safety case.
