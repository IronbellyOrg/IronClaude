# Position OURS (Q02): a local `git branch -d` is allowed only behind our own explicit guards, and `-d` is not itself the guard

## Claim
The owner asked for branch cleanup with "extra rigid and strict validation" (issue 339, owner comment 2026-11-05 13:43Z, quoted in D13 VERDICT.md). So the answer is a guarded yes, never a bare `git branch -d` that relies on git to refuse unsafe cases. Git's `-d` is a weak check. The script must carry its own list of refusals, show the branch action in the dry run, and delete nothing without `--apply` under a grant.

## Mechanism
After `git worktree remove` (no `--force`), the script deletes the local branch only if ALL hold: the worktree passed the nine rules; the branch is not the repo default branch (`master`) nor a long-lived branch (`integration`, `main`); no PR (any state) with this head is open and no open PR uses it as its base; no other worktree has it checked out; the commit it points at is the merged PR's last head commit (`headRefOid`); the command is exactly `git branch -d <name>` (never `-D`, never `--force`). The dry run prints "branch: would delete / would keep (reason)" per row. Remote branches are never touched.

## Cited facts
1. Owner comment on issue 339 (the owner's issue: one orchestrator for all sessions), 2026-11-05 13:43Z: cleanup of worktrees and branches "with extra rigid and strict validation". Source: D13 VERDICT.md, Strongest points OURS 1 (`gh issue view 339`).
2. Measured in a scratch repo (git 2.47.3, `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q02/scratch/t`): `git branch -d feat-pushed` deleted a branch that was pushed but NOT merged to HEAD (git only warned "merged to origin/feat-pushed, but not yet merged to HEAD"). So `-d` means "pushed or merged", not "its PR landed".
3. Same test: `git branch -d integration` (merged into master) succeeded, and `git branch -d master` from another branch succeeded. `-d` has no default-branch or long-lived-branch protection.
4. This repo has a long-lived `integration` branch on origin (`git ls-remote --heads origin integration` returned 141e97fe...) and the project CLAUDE.md names the flow `master <- integration <- feature/*`. A worktree on `integration` with a merged PR would pass rules 2 and 3 of issue 687 as written.
5. Issue 687 rule 2 takes the "newest merged" PR "when there are several" (rule table, row 2). A branch with an older merged PR and a newer open PR is not explicitly blocked by an open-PR check on the branch itself; only rule 3 (HEAD equals the merged PR head) catches new commits.
6. `WORKER-CONTRACT.md` lines 236-237 (master snapshot) already let the coordinator delete a child branch after merge-back, and forbid removing "a worktree or branch that holds unmerged commits, an open PR, uncommitted changes..." without the user's instruction. The owner's contract already states the open-PR and unmerged limits.
7. `docs/designs/orchestrator.md` line 139 (ADD5): "deleting branches is human-only, rule 1", and issue 687 keeps remote branch deletion human-only. Local `-d` is a different, recoverable act.
8. `orca worktree rm --help`: removal "also attempts to delete the checked-out local branch, with or without --force. Orca retains branches it knows predated the worktree and any branch whose changes it cannot prove are already merged." So Orca-listed worktrees already lose their local branch; the script must not behave looser than Orca.

## Cost
A guard list (default branch from `gh repo view`, a small named set, open-PR lookup, `headRefOid` match) and one extra table column. About 4 tests. No new tool.

## Risk
Over-strict guards leave stale local branches; that is a cosmetic cost. Under-strict guards delete `integration` or a branch that still has an open PR; recovery needs the reflog or the remote copy.

## What it gets right
Fail-closed everywhere, a human-visible dry run, remote deletion left to a person, and no reliance on one git flag to carry the safety case.
