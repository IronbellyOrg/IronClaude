# Option E (hybrid): sole-writer workers may commit locally; every outward action has one owner, the coordinator

Position paper for the git-ownership debate. Added because the evidence in options A and B splits along one line: local commits are safe for a worker exactly when it is the only writer in its worktree, while outward actions are safe only where the user's authorization is given directly.

Citation keys: as in `option-a.md` (`SPEC`, `CAPS`, `EVAL`, `HWW`, `[G]`, `[G:cl]`, `[G:wc]`, `[G:rc]`, `[G:pl]`, `GITDEMO`).

## The proposal
| Action | Owner | Condition |
|---|---|---|
| Push, PR (always `/sc:pr-submit --monitor 3`), review replies, issue or status comments, project updates, remote branch deletion, merge into a shared branch | Coordinator, in its main chat | Only when the user's own instruction names that action (D4, both options agree on this for the coordinator) |
| Create or remove run worktrees and local branches | Coordinator | Worktrees under `.dev/worktrees/` (`CLAUDE.md:299-302`); never remove a branch with unmerged commits or an open PR without the user's instruction (`EVAL:53`, F3) |
| Local commit of settled work in a shared worktree | Coordinator | At a quiescent point: no worker running in that worktree; stage only paths named in settled contracts plus `.dev/tasks` (`CLAUDE.md:37`) |
| Local commit inside a worker's own run (per-task commits, experiment branches) | That worker | Only if (1) the brief quotes the user's instruction authorizing local commits for this Task, (2) the worker is the only writer in its worktree, (3) for `/sc:implement`, only between tasks and never inside a parallel batch; it stages explicit paths plus `.dev/tasks`, never pushes, never merges, and lists each SHA in its contract's `artifacts` |
| Anything mutating git in a worktree shared with other running workers | Nobody but the coordinator at a quiescent point | Always |

## Correctness under parallel workers
- **Index lock:** a worker commits only in a worktree where it is the sole writer, and linked worktrees have separate index files (GITDEMO), so no two git writers share a lock. In a shared worktree only the coordinator commits, at quiescent points.
- **HEAD movement:** a worker's own commits move only its own worktree's HEAD (separate HEAD per linked worktree, GITDEMO). `/sc:implement`'s retry ladder stays valid when commits fall between tasks, because each task's baseline is recorded at its own start (`src/superclaude/skills/sc-implement-protocol/SKILL.md:114`; `refs/retry.md:41`) and a parallel batch has no ladder anyway (`SKILL.md:97`). The coordinator never commits in a worktree while an implement worker runs there.
- **Shared refs:** implement's pins live under `refs/superclaude/implement/<slug>/T<id>` (`SKILL.md:113`) and refs are shared across linked worktrees (GITDEMO), so two implement runs in two worktrees must use different slugs; the coordinator's brief gives each its own plan, which gives distinct slugs. UNVERIFIED for two runs of the same plan in two worktrees.
- **Per-task commits (#326):** possible, because the worker that knows task boundaries is the one committing.

## Safety and authorization
- Every outward action stays where the person gives the instruction, in the session `/sc:pr-submit` requires (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:47-49`), matching D3 (a) (`SPEC:341`) and the repo PR rule (`CLAUDE.md:50`). No worker pushes, so WC-9 stays exactly as strict as today for outward actions (`SPEC:73`).
- A local commit is not outward but still needs the user's ask (`CLAUDE.md:37`; `HWW:282` "Commit locally, show your lead what changed, and push only when they say go"). The worker's authority is the quoted instruction in its brief, as D4 (a) already requires for outward actions (`SPEC:346`). A local commit is reversible and invisible outside the machine until the coordinator pushes.
- **Audit trail:** worker commits are listed by SHA in contracts; every push, PR and comment is in the coordinator's transcript beside the instruction that authorized it.

## Recovery
- Worker crash mid-commit: a stale lock affects only its own worktree; the retry Task (WC-6) checks for it first. Commits made before the crash survive.
- Coordinator crash: as A; no outward action can be half-done by a worker, because workers do none.

## Context load on the coordinator
Lower than A when per-task commits are used (workers write their own messages); equal to A for outward actions, which are few per run.

## Fit with repo PR rules
Exact fit (`CLAUDE.md:50`; `HWW:223`: monitor 3 publishes only the cycle's fix commit to origin).

## How a person works day to day
The person says, for example, "run the plan in its own worktree, commit after each task, and open a PR when it passes". They see commits appear on the experiment branch during the run, and the PR is opened by the coordinator in their own chat. Without that instruction nothing is committed.

## Implementation cost
Spec: wording in WC-9, WC-11, section 2.3, the `/sc:git` row and D4 (this file's table). Commands: none in this spec's phases; the per-task commit step inside `/sc:implement` stays #326's feature (K3, `EVAL:63`), and until it exists a worker commits only through steps its brief adds after the command finishes.

## Weaknesses an opponent will press
1. Two owners for local commits means two rule sets to state and test.
2. A worker running raw git can still make a mistake inside its own worktree (wrong paths), and only the coordinator's later review catches it.
3. More worktrees means more cleanup (F3).
