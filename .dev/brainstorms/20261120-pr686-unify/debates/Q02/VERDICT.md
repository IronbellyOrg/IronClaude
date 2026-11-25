# Verdict Q02: Cleanup script may delete local branches

## Question
D13 left open whether the worktree cleanup script (issue 687) may run a local `git branch -d` after removing a merged worktree. Decide yes/no and the safe limits (merged-only, `-d` never `-D`, never the default branch, never a branch with an open PR, dry run first). Read D13 VERDICT.md and the issue text (`gh issue view 687 --repo IronbellyOrg/IronClaude`, read-only).

## Winner
HYBRID: yes, the script may run a local `git branch -d`, using issue 687's own rules and step order (Clay's text) plus a short list of added refusals (the owner's line), because the debate showed `-d` itself protects far less than D13 said.

## Winning recommendation
The unified spec must say all of the following. Issue 687 (Clay's request for a daily worktree cleanup, open) already puts `git branch -d` as step 4 of a removal, so this is an addendum to that issue, not a second rule set.

1. **Yes, local only, `-d` only.** The command is exactly `git branch -d <name>`. Never `-D`, never `--force`, never a remote branch delete (remote deletion stays human-only, `docs/designs/orchestrator.md` line 139 reading, and issue 687's "never does" list).
2. **`-d` is a backstop, not the gate.** The spec must say: `-d` means "merged to its upstream, or to the HEAD of the checkout the script runs in", not "its pull request landed". Measured (git 2.47.3, scratch repo): it deleted a branch that was pushed but not merged to HEAD; it deleted `integration` and `master` once merged. The gate is issue 687's rules 2 and 3 (own PR is MERGED; nothing added after it). The sentence in D13 VERDICT.md item 4, "`-d` refuses an unmerged branch", must not be used as the reason.
3. **Refusals added to issue 687's rules (the whole addendum):**
   - (a) Never delete `master`, `main`, `integration`, or the repo default branch read from `gh repo view`.
   - (b) Rule 2 gains one sentence: keep the branch if any PR with this head is OPEN (rule 2 as written takes "the newest merged one when there are several").
   - (c) Rule 2 also requires the merged PR's `headRepositoryOwner` to be one of ours.
   - (d) The dry run table prints "branch: would delete / would keep (reason)" per row and the merged PR's head SHA (so a branch can be recreated from `refs/pull/N/head` when `origin/<branch>` is gone).
   - (e) Rule 3 stays as written in issue 687: HEAD equals the PR's last head commit (`headRefOid`) or is an ancestor of it. No stricter check is added.
   - Not added, because something else provides them: "no other worktree has the branch checked out" (git refuses it) and "no open PR uses the branch as its base" (no measured case).
4. **Apply refusals (a) to (c) before the worktree is removed, as keep-the-whole-worktree rules, not only as a branch step.** Reason (an inference from `orca worktree rm --help`, not a measured result): for a worktree Orca lists, `orca worktree rm` "also attempts to delete the checked-out local branch, with or without --force", so a script that only skips its own `git branch -d` could not stop Orca from deleting `integration`. Issue 687 already lists Orca's branch behavior as unproved (open item 1); prove it before the build, and until then treat a refused branch as a kept worktree.
5. **Dry run first, and first week report-only.** Dry run is the default and `--apply` is the only way to remove (issue 687). The daily automation runs report-only for the first week (issue 687 rollout ladder). Who may run `--apply` stays under a grant row (the D13 rule), not decided here.
6. **A git refusal is "kept", not an error.** For a squash-merged branch whose remote branch is gone, `-d` always refuses (measured), so those branches stay until a person removes them; `-D` is never used to force it.
7. **Testable checks.** (i) The issue 687 acceptance test that records every command and fails on `--force`, `-D`, `rm`, `prune`, a push to anything but the evidence remote, or a remote branch delete stays. (ii) Four added cases: a worktree on `integration` with a merged PR is kept; an OPEN PR with the same head keeps the branch; a PR whose `headRepositoryOwner` is not ours is not accepted; the dry run table shows the branch action and the PR head SHA. (iii) No test may expect `-d` to refuse an unmerged but pushed branch.

## Strongest points
**OURS**
1. `git branch -d` has no default-branch or long-lived-branch protection and deleted a pushed, unmerged branch. Source: scratch repo `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q02/scratch/t`, tests T1, T5, T6, repeated by the Variant 1 advocate in `adversarial/adversarial/debate-transcript.md`.
2. `integration` is a real long-lived branch: `git ls-remote --heads origin integration` returned 141e97fe, and merged PRs #664, #658 and #640 (three pull requests into `master`) have `integration` as their head (`gh pr list --repo IronbellyOrg/IronClaude --head integration --state all`, read-only, 2026-11-20). Issue 687 has no branch-name guard (its only name guard is for folder names, rule table row 1).
3. The owner asked for branch cleanup "with extra rigid and strict validation" (issue 339, owner comment 2026-11-05 13:43Z, as quoted in D13 VERDICT.md); a per-row dry run of the branch action is what a person needs before `--apply`. Source: D13 VERDICT.md, Strongest points OURS 1.

**CLAY**
1. Issue 687 already specifies the sequence and a tested never-force surface: step 4, the "things the script never does" list, and an acceptance test that records every command. Source: `gh issue view 687 --repo IronbellyOrg/IronClaude`, section 3 step 4 and the acceptance list.
2. The nine rules, not `-d`, are the real safety layer, and a failed lookup keeps the worktree; git refuses the redundant cases itself (never-pushed unmerged, squash-merged with remote gone, branch used by another worktree; all reproduced in the scratch repo, tests T2 to T4). Extra guards would be code with its own bugs.
3. The loss is recoverable and the repo needs the cleanup: `deleteBranchOnMerge` is false and squash merge is allowed (`gh repo view IronbellyOrg/IronClaude`), so merged branches pile up; Orca already deletes the local branch itself (`orca worktree rm --help`).

## Clay strengths to adopt
1. **Issue 687's rule set and step order as the single base (no parallel guard list).** Why: both advocates agreed (S-002); it keeps one source of truth. Merge: the refusals above are an addendum to rules 1 to 3. Override: none.
2. **Rule 3 as written (equal or ancestor), no exact-equality check.** Why: a ref at an ancestor of the PR head holds no commit the PR head lacks, so exact equality protects nothing more; Clay's text is simpler and the owner's side withdrew the extra check. Merge: adopt as is.
3. **Drop the redundant "no other worktree" guard.** Why: git refuses it (measured). Merge: adopt as is.
4. **The never-force acceptance test and the report-only first week.** Why: they already exist in issue 687 and fit the owner's "rigid and strict" wording. Merge: adopt as is; the grant question for `--apply` stays with the D13 rule.
5. **A git refusal is reported "kept", not an error.** Why: fail-closed without noise. Merge: adopt as is, with the added statement that squash-merged branches with a gone remote will therefore stay.

## Our strengths that must be kept
- The refusal for `master`, `main`, `integration` and the default branch.
- The "any OPEN PR with this head keeps the branch" line and the PR owner check.
- The dry run branch column and the logged PR head SHA.
- The correct meaning of `-d` (backstop, not gate) in the spec text.
- The rule that the script must not delete more than Orca would, and that remote branch deletion stays human-only.

## Actions
| Action | Type | Target | Order or dependency |
|---|---|---|---|
| Owner confirms in chat that the script may run a local `git branch -d` under the limits in Winning recommendation items 1 to 7 (the agent records it; the owner writes no file) | DECISION | Issue 687 step 4; D13 VERDICT.md Actions row 7 | First; before any build |
| Add refusals (a) to (e), the dry run column, and the four test cases to the issue text | PR KEEP-ADAPT | Issue 687 (it is an issue; nothing is built) | After the decision above |
| Apply refusals (a) to (c) as keep-the-worktree rules checked before any removal | LOCAL CHANGE | Unified spec, cleanup step; issue 687 rules 1 and 2 | With the row above |
| Prove what `orca worktree rm` without `--force` does to the local branch (issue 687 open item 1) | DECISION | Issue 687 section 11, item 1 | Before the build starts |
| Replace D13's reason for the `-d` yes ("`-d` refuses an unmerged branch") with the corrected meaning in item 2 | DOC | D13 VERDICT.md, Winning recommendation item 4 (note for the unified rewrite, not an edit here) | With the unified spec |
| Keep who may run `--apply` under a grant row | DECISION | D13 rule (grant row); not reopened here | Unchanged |

## Implications
- **Watcher and claim pipeline:** none. This is the cleanup script only.
- **Coordinator and orchestrator:** the coordinator's list-then-apply cycle from D13 is unchanged. The coordinator contract (`src/superclaude/core/WORKER-CONTRACT.md` lines 236 and 237 in the master snapshot) already lets it delete a merged child branch and forbids a branch with an open PR or unmerged commits without the user's instruction; these limits match it.
- **Dashboard:** the dry run table with the branch column could feed the observer report (issue 409); not decided here (carried over from D13).
- **What the owner must know:** (1) For a squash-merged branch whose remote branch is gone, `-d` always refuses, and this checkout has 21 of 56 local branches with a `[gone]` upstream, so the script will leave exactly that class of branch in place; clearing them needs a person (`-D` stays forbidden). (2) If Orca deletes the branch itself, script-level refusals are bypassed unless the worktree is kept; that is why refusals (a) to (c) are worktree rules. (3) No linked worktree is on `master`, `main` or `integration` today, so the `integration` risk is latent, not live. (4) GitHub shows no owner approval of issue 687 (D13); the chat decision above is needed before a build.

## Confidence
85%. It would drop if the owner rules local branch deletion human-only (then the answer becomes "no, list only"), if the Orca test shows Orca ignores script refusals even for a kept worktree path (then Orca-listed worktrees need a different removal path), or if `integration` is retired (then refusal (a) shrinks to the default branch).

## Unverified
- What `orca worktree rm` without `--force` does to the local branch and to a dirty worktree (issue 687 open item 1; only the help text was read).
- Whether the owner approved issue 687 or this limit anywhere outside GitHub (D13 found none on GitHub).
- The owner's issue 339 comment (2026-11-05 13:43Z) was taken from D13 VERDICT.md, not re-fetched.
- Whether GitHub allows an OPEN PR whose head equals a merged PR's head (the rule 2 wording gap was not shown to occur).
- Whether Orca-created branches have an upstream set (45 of 56 local branches here do, but they include manual pushes), which decides how often `-d` succeeds after a squash merge.
- All tests ran on git 2.47.3 in a scratch repo; `-d` with a configured upstream whose remote branch still exists was tested only for an unmerged pushed branch (T1), not after a squash merge.
- Both advocates and both scoring passes were same-family agents run by one orchestrating session, not different models; the quantitative layer was partly estimated by hand and the winning margin is 5.9 points (0.900 against 0.841), mostly from the requirement-coverage metric, which is measured against the topic question's own list of limits.
- The line-number citations for issue 687 refer to the saved text of its body (`/tmp/q02-issue687.txt`), not GitHub line numbers.

## Debate artifacts
Adversarial skill ran (depth quick, one round, two advocates, two independent scoring passes, merge-executor). Under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q02/`:
- `position-OURS.md`, `position-CLAY.md`
- `adversarial/return-contract.yaml` (worker contract)
- `adversarial/merged-hybrid-position.md`
- `adversarial/adversarial/diff-analysis.md`
- `adversarial/adversarial/debate-transcript.md`
- `adversarial/adversarial/base-selection.md`
- `adversarial/adversarial/refactor-plan.md`
- `adversarial/adversarial/merge-log.md`
- `adversarial/adversarial/return-contract.yaml`
- `adversarial/adversarial/variant-1-original.md`, `variant-2-original.md`
- `scratch/t` (throwaway git repo used for the `git branch -d` tests)
