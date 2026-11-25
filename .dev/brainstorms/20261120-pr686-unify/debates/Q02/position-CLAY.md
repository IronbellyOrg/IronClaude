# Position CLAY (Q02): the script runs `git branch -d` after removing a merged worktree, as issue 687 specifies

## Claim
Issue 687 (Clay's request for a daily worktree cleanup, open, author `clayphi`) already decides it: step 4 of "what a removal is" is `git branch -d`, never `-D`. The nine rules in front of it and git's own refusal behind it make a separate guard list unnecessary. Adding more rules adds code and risk of its own for a branch that is recoverable from GitHub.

## Mechanism
Order of a removal: save `.dev` files, remove the worktree without `--force`, run `git branch -d <branch>`, read back. If git refuses ("not fully merged", as after a squash merge), the branch is reported "kept", which is not an error. Dry run is the default; `--apply` is the only way to remove. Rule 1 excludes the main checkout; rule 2 needs the worktree's own PR to be MERGED; rule 3 needs HEAD to equal the PR head.

## Cited facts
(Line numbers of issue 687 refer to its body saved by `gh issue view 687 --repo IronbellyOrg/IronClaude --json body --jq .body`, not to GitHub line numbers.)
1. Issue 687 body, section 3 step 4: "Remove the local branch with `git branch -d`, never `-D`... the branch is then reported as kept, which is not an error... the branch and its commits remain on GitHub and the worktree can be recreated."
2. Issue 687 section 3 "In scope for version 1": "(b) The local branch of each removed worktree, with `-d` only." Acceptance list: a removable worktree "is removed, and its local branch is removed with `-d`".
3. Issue 687 "Things the script never does": no `--force`, no `git branch -D`, no `rm`, no remote branch delete, no `git worktree prune`. An acceptance test records every command and fails on `-D`, `rm`, `prune`, any push but the evidence repo, any remote branch delete.
4. Issue 687 rule 1 skips the first (main) `git worktree list` entry and rule 2 uses PR state, squash-safe, "never from commit ancestry". Section 8 decision 9 leaves "delete branch on merge" as a repository setting to the owner.
5. `orca worktree rm --help`: Orca already attempts local-branch deletion with or without `--force` and keeps branches it cannot prove merged. The script's `-d` for non-Orca worktrees matches that behavior.
6. Measured (scratch repo, git 2.47.3): `git branch -d` refused a never-pushed unmerged branch, refused a squash-merged branch whose remote copy was deleted, and refused a branch checked out in another worktree. Issue 687 states the squash and dirty-worktree refusals were tested on 2026-11-20.
7. `WORKER-CONTRACT.md` lines 236-237 (master snapshot): the coordinator already removes a merged child with `orca worktree rm` "and deletes its branch".
8. D13 VERDICT.md recommends yes (Winning recommendation item 4): "`-d` refuses an unmerged branch and the owner asked for branch cleanup on 2026-11-05".
9. This repo allows squash merge and has `deleteBranchOnMerge: false` (`gh repo view IronbellyOrg/IronClaude`), so merged branches pile up locally and on GitHub; the manual cleanup of 2026-11-20 found 26 worktrees with "branch with no pull request" (issue 687 section 2).

## Cost
Nothing extra: one command in a sequence already specified.

## Risk
Residual: `-d` can delete a pushed branch not merged to HEAD (measured). Mitigated by rules 2 and 3 requiring a merged PR and HEAD at its head. A deleted local branch is recreated from `origin/<branch>`.

## What it gets right
One simple, tested, never-force rule set; dry run by default; failure keeps the branch; no model judgment in an irreversible act.
