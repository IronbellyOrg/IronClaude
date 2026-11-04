# Option B: workers run their own git, under rules the brief sets

Position paper for the git-ownership debate. Argues B as strongly as the evidence allows.

Citation keys: as in `option-a.md` (`SPEC`, `CAPS`, `EVAL`, `HWW`, `[G]`, `[G:cl]`, `[G:wc]`, `[G:rc]`, `[G:pl]`, `GITDEMO`).

## The proposal
Each worker commits its own work when the brief authorizes it: for example `/sc:implement` commits after each task's `complete` line, and an experiment worker commits on its own branch. The brief states which git actions are allowed (local commit only; or commit plus push; or a PR through `/sc:pr-submit` under D3 (b)), quoting the user's instruction (D4 (a), `SPEC:346`). The coordinator only plans, reads contracts and merges results.

## Correctness under parallel workers
- **Strongest case: one worker per worktree.** Each linked worktree has its own index and its own HEAD (`.git/worktrees/<name>/index` and `.../HEAD`, GITDEMO), so two workers in two worktrees never contend for `index.lock` and never move each other's HEAD. #326 asks for exactly this layout: "Branching and worktrees when performing parallel experiments" (issue #326 owner comment, read with `gh issue view 326`), and the evaluation folds it into WC-11 (`EVAL:52`, F2).
- **Per-task commits are only possible here.** Inside a long `/sc:implement` run, only the worker knows when a task ends. A commit between one task's `complete` line and the next task's start keeps the retry ladder valid, because the ladder compares HEAD with the value recorded at that task's start (`src/superclaude/skills/sc-implement-protocol/refs/retry.md:41`; Q0 records it, `src/superclaude/skills/sc-implement-protocol/SKILL.md:114`). The coordinator cannot time such a commit (`EVAL:51`, F1).
- **The worker knows its own files.** It wrote them, so it stages exact paths; the coordinator would reconstruct them from `--files-modified`.
- **Honest limit, shared worktree.** Two workers committing in one worktree contend for `index.lock` (GITDEMO: "Another git process seems to be running in this repository"), a `git add -A` sweeps the other worker's files, and any commit moves the shared HEAD, which halts every running `/sc:implement` task in that worktree with `head-moved` (`retry.md:41,44`). B is therefore safe only with one committing worker per worktree. Workers share the current worktree by default (`CAPS:115`), so B forces a worktree per committing worker.
- **Implement's own batches.** Inside one implement run, a parallel batch never gets a retry ladder (`SKILL.md:97`), so in-run commits must wait for a batch's last `complete` line too.

## Safety and authorization
- The repo commits only when asked (`CLAUDE.md:37`). Under B the "ask" reaches the worker second-hand, through a brief the coordinator wrote. D4 (a) makes that acceptable only when the coordinator quotes the user's instruction naming the action for that task (`SPEC:346`).
- `/sc:implement` today says acceptance never "authorizes commit, PR, merge or release" (`src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:63,67`), so implement-side commits are a deliberate protocol change (#326 K3, `EVAL:63`).
- `/sc:git` cannot be the tool: it has no unattended mode and waits on a person for destructive operations (`src/superclaude/commands/git.md:90`; `SPEC:156`). Workers would run plain `git` under the brief's rules.
- Pushes and PRs from workers need D3 (b) and the section 3 pr-submit row (`SPEC:137`, `SPEC:342`). A worker is a top-level session, so `/sc:pr-submit`'s top-level rule is met (`CAPS:161`).
- **Audit trail:** every commit is in `git log` with the worker's message; the worker's contract lists the commit SHA. But authorizations are spread over many briefs and transcripts.

## Recovery when someone crashes
- A worker that crashes mid-commit leaves a stale `index.lock` in its own worktree only; other worktrees are unaffected (separate index files, GITDEMO). The retry is a new Task (WC-6, `SPEC:70`) in the same worktree, which must first clear the stale lock, a step no command has today.
- Already-committed tasks survive the crash, which is #326's point: work is not lost "until all of the work is done in a tasklist".

## Context load on the coordinator
Lowest of all options for local commits: the coordinator reads contracts and SHAs, not diffs. It still owns merging branches back, which is git work in its own chat (so B still needs A for merges).

## Fit with repo PR rules
Acceptable only if PRs still go through `/sc:pr-submit --monitor 3` (`CLAUDE.md:50`). A worker opening PRs needs D3 (b), which the spec does not recommend (`SPEC:343`).

## How a person works day to day
The person sees commits appear on several experiment branches while the run proceeds, and gets a list of branches to compare. More branches and worktrees to clean up (#326 asks for cleanup, `EVAL:53`, F3).

## Implementation cost
Highest. Every committing command needs a commit step, a stale-lock rule and a contract field for SHAs; implement needs K3; the coordinator needs a worktree-per-worker placement rule and a merge step. All of it is new behaviour in commands, against the spec's additive-edits rule for P1-P3 (`SPEC:172`).

## Weaknesses an opponent will press
1. Unsafe in the default shared worktree (index lock, sweep, HEAD movement).
2. Authorization reaches the actor second-hand.
3. Pushes, PRs and comments from workers multiply outward actions across sessions, which the spec's WC-9 exists to prevent (`SPEC:73`).
4. Merges still need a single owner, so B is never complete on its own.
