# Option C: a dedicated, long-lived git session (an Orca worker that only does git)

Position paper for the git-ownership debate. Argues C as strongly as the evidence allows.

Citation keys: as in `option-a.md` (`SPEC`, `CAPS`, `EVAL`, `HWW`, `[G]`, `[G:cl]`, `[G:wc]`, `[G:rc]`, `[G:pl]`, `GITDEMO`).

## The proposal
The coordinator starts one extra Claude worker, the "git session", that no person uses directly. Every git or GitHub action is a small Task the coordinator gives it ("stage these paths, commit with this message", "push branch X", "run `/sc:pr-submit --monitor 3 ...`", "post this status comment"). Other workers never run mutating git. The coordinator reads worker contracts, decides the action and forwards the user's authorization in the brief.

## How Orca can keep it alive (verified mechanics)
- **One Task per action, same terminal.** Orca's reuse pattern: after a settlement, "When the same exact agent has immediate follow-up work, recover the proven handle and transfer cleanup ownership to the new Dispatch": `worker-show --dispatch <id>` then `worker-start --task <next_task_id> --terminal <agent_terminal_handle>` (`[G:cl] 46-55`). Each action therefore gets its own Task, Dispatch, `worker_done` and outcome, which is the per-action audit record.
- **Strict serialization for free.** A terminal that already owns an active Dispatch rejects a second one (`runtime_error`, "a target terminal that already owns an active Dispatch", `[G:rc] 108`). Only one git action can run at a time, so the git session never contends with itself for `index.lock`.
- **Keeping it alive between actions.** After each settlement the coordinator must immediately reuse, retain or release the terminal (`[G] 166-170`). Reuse needs "immediate follow-up work" (`[G:cl] 48-50`); otherwise retention is allowed "only when the user explicitly wants the settled terminal kept live" (`[G:rc] 157`). So C needs the user to request retention once at run start. Release of a reused terminal is listed among terminals that "are retained" (`[G:rc] 160-161`); what that means for the git session's final cleanup is UNVERIFIED.
- **A single never-ending Task is not an option.** The worker contract says do only the current Task and, after `worker_done`, "end the dispatched turn and idle. Do not poll" (`[G] 80-82,91-93`; `[G:wc] 77-80`). A loop Task that polls `check` for instructions would have no per-action outcome and would break that rule.
- **Depth.** The coordinator starts the git session, so it is a depth-1 worker (`CAPS:97-101`); it starts nothing itself.

## Staying in sync with workers' files
- **Same worktree:** the git session sees workers' files directly on disk; nothing to sync. It must act only at quiescent points: no worker writing in that worktree, and no `/sc:implement` worker running there, because a commit moves HEAD and halts that worker's retry ladder (`src/superclaude/skills/sc-implement-protocol/refs/retry.md:41,44`).
- **Separate experiment worktrees:** the git session runs `git -C <worktree>` per action; each linked worktree has its own index and HEAD (GITDEMO). Placement in the brief names the worktree (`SPEC:79`).

## Correctness under parallel workers
Same as A: one writer, explicit paths from contracts. Better than A in one respect: a long `/sc:pr-submit` monitor loop (waits up to a 600 s budget, `src/superclaude/commands/pr-submit.md:49`) runs in the git session, so the coordinator keeps processing other workers' messages meanwhile.

## Safety and authorization
- The git session is a top-level session, so it may run `/sc:pr-submit` (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:47-49`; `CAPS:161`). But it is a worker, so pr-submit there is D3 (b) and needs the section 3 pr-submit row (HALTs as blocked, wait splitting, `SPEC:137`).
- Authorization takes one hop: user to coordinator, coordinator quotes it in the git Task's brief (D4 (a), `SPEC:346`). The audit trail is the clearest of all options: one Task per action, each with its brief (the quoted authorization), its `worker_done` and its contract.
- `/sc:git` itself cannot be the tool yet: no unattended mode, waits for confirmation on destructive operations (`src/superclaude/commands/git.md:90`). The git session runs plain git and `/sc:pr-submit` until #326 delivers an unattended `/sc:git`.

## Relation to #326's "central relay"
#326 wants `/sc:git` to be "a central relay for all other commands to use" (issue #326, Phase 2-P). Commands cannot call another session (SA-2, WC-8, `SPEC:72`, `SPEC:170`), so the relay cannot be something commands call. C is the orchestration-level version of the relay: one place where every git action happens, fed by the coordinator. If #326 later gives `/sc:git` an unattended mode, the git session runs `/sc:git` instead of raw git, with no change to the design.

## Recovery
- Git session crash mid-action: Orca reports liveness (`CAPS:122-126`); the coordinator inspects `git status` (or asks a fresh git session to), clears a stale lock only after proving no git process runs, and re-issues the action as a new Task (WC-6, `SPEC:70`). A failed `worker-start` still owns its terminal and must be released (`[G:rc] 163-165`).
- Worker crash: no git state to repair, as in A.

## Context load on the coordinator
Lower than A: the git session reads diffs and writes commit messages; the coordinator writes one-line briefs and reads contracts. The git session's own context grows over a long run (reuse keeps the conversation); UNVERIFIED how reuse injects the next task into a running Claude session (CAPS:47 shows argv injection only for fresh launches).

## Fit with repo PR rules
Fits if the git session runs `/sc:pr-submit --monitor 3` (`CLAUDE.md:50`) under an authorization quoted in its brief; conflicts with the spec's D3 recommendation (a) (`SPEC:341`).

## How a person works day to day
The person sees one extra Orca terminal named for git, and approves its retention once. They still tell the coordinator what to commit or push.

## Implementation cost
Medium: a git-action brief template, a contract shape for git results (SHAs, branch, PR URL), a retention step, quiescence rules, and pr-submit's P4 changes if it runs there.

## Weaknesses an opponent will press
1. An extra hop and an extra 60-second readiness start (`CAPS:44`) for actions that take seconds.
2. Retention needs an explicit user request (`[G:rc] 157`); without it the session is released after each action and C degrades to "a fresh git worker per action".
3. It needs D3 (b) for PRs, which the spec does not recommend.
4. It does not solve per-task commits inside `/sc:implement` (the coordinator still sees only the run's end).
