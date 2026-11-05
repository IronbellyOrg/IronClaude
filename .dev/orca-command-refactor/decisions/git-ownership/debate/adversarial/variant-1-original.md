# Option A: the coordinator runs every git and GitHub action itself, in its main chat

Position paper for the git-ownership debate. Argues A as strongly as the evidence allows.

Citation keys: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md`; `EVAL:N` = `.dev/orca-command-refactor/review/issue-326-evaluation.md`; `HWW:N` = `src/superclaude/core/HOW-WE-WORK.md`; `[G] N` = line N of `orca-ide skills get orchestration | cat -n`; `[G:cl] N`, `[G:wc] N`, `[G:rc] N`, `[G:pl] N` = line N of the `coordinator-loop`, `worker-contract`, `recovery-and-cleanup` and `placement-and-remote` references (`orca-ide skills get orchestration --reference references/<name>.md | cat -n`, CLI 1.4.237, read 2026-11-02). `GITDEMO` = a scratch-repo run in `/tmp` on 2026-11-02 with git 2.47.3 (details in Self-check below).

## The proposal
Workers never run a mutating git command. Each worker leaves its changes in the working tree and lists them in its `return-contract.yaml` (`artifacts`, `report_path`) and in `worker_done --files-modified`. The coordinator, in its own top-level chat, stages explicit paths, commits, creates and removes branches and worktrees, pushes, opens PRs through `/sc:pr-submit --monitor 3`, and posts issue or status comments, each only when the user's own instruction names that action.

## Correctness under parallel workers
- **One writer per repository index.** Git refuses a second writer: with `.git/index.lock` present, `git add` fails with "Unable to create '.../index.lock': File exists. Another git process seems to be running in this repository" (GITDEMO). Under A only one session ever takes that lock in a given worktree, so lock collisions between git writers cannot happen.
- **No cross-worker sweep.** Workers share the current worktree by default (`CAPS:115`; `[G:pl] 8-11`). A worker that ran `git add -A` would commit other workers' half-written files. The coordinator stages only the paths named in settled contracts.
- **HEAD movement is controllable.** `/sc:implement`'s retry ladder runs only if "HEAD has not moved" since the task's start (`src/superclaude/skills/sc-implement-protocol/refs/retry.md:41`); otherwise it halts `head-moved` (`retry.md:44`). Under A, the only thing that can move HEAD is the coordinator, so it can follow one rule: never commit in a worktree while an `/sc:implement` worker in that worktree is running. Under B or C the same rule must be enforced across several sessions.
- **Honest limit.** A cannot honour #326's "commit after each task" inside one `/sc:implement` run: the coordinator learns only of the whole run's `worker_done` (`[G] 88-90`), not of each task inside it. Under A, per-task commits wait for #326's own protocol change (`EVAL:63`, K3).

## Safety and authorization
- The repo commits only when asked (`CLAUDE.md:37`), pushes only with approval (`HWW:282`) and opens PRs only through `/sc:pr-submit --monitor 3` (`CLAUDE.md:50`). The person talks to the coordinator, so the instruction that authorizes an action and the session that performs it are the same. No second hop can lose, broaden or forge the authorization.
- `/sc:pr-submit` must run in the main orchestrating session, never in an Agent-tool subagent, and must never hand a side effect to a background shell or subagent (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:47-49,82-84`). The coordinator is such a session.
- `/sc:git` is already coordinator-only (`SPEC:156`), and `/sc:git` waits on a person for destructive operations (`src/superclaude/commands/git.md:90`), which only a session with a person present can satisfy.
- Spec D3 already recommends pr-submit stay with the coordinator or person (`SPEC:339-343`); A extends that to every outward action, which is spec D4 option (b) for outward actions (`SPEC:347`).
- **Audit trail:** one transcript (the coordinator's) holds every git decision, next to the contracts it read; the commits themselves are the durable record.

## Recovery when someone crashes
- **Worker crash:** nothing git-related to repair; the worker made no git call. Its partial files sit in the working tree; the coordinator decides from the contract (or its absence, `SPEC:69`) whether to stage them.
- **Coordinator crash mid-commit:** a stale `index.lock` may remain. The next coordinator session (or the person) inspects with `git status` and removes the stale lock only after proving no git process runs. The Run's state is durable in Orca (`[G] 51-52`), and the worktree is on disk.

## Context load on the coordinator
This is A's cost. Every commit needs the coordinator to read the contract's file list and write a commit message. `/sc:pr-submit`'s attended loop occupies the session for waits of up to 600 s per wait budget (`src/superclaude/commands/pr-submit.md:49`), during which the coordinator does not react to other workers. Mitigation: messages queue durably (`[G] 73-74`; `check` replays the oldest delivery until acknowledged, `[G] 120-124`), and D3 (a) already puts pr-submit after the workers finish (`SPEC:341`).

## Fit with repo PR rules
Exact fit: PRs go only through `/sc:pr-submit --monitor 3` on the fork (`CLAUDE.md:50`), run top-level (`SKILL.md:47-49`), after an approved push (`HWW:282`).

## How a person works day to day
The person tells the coordinator "commit and open a PR when the run passes". The coordinator does so in the same chat and shows the commit and PR link. Nothing new to learn. The person sees no extra terminal.

## Implementation cost
Lowest. No command changes: WC-9 already turns every outward default off in workers (`SPEC:73`). The spec needs only wording in section 2.3 (coordinator duties) and the `/sc:git` row.

## Weaknesses an opponent will press
1. No per-task commits inside a long `/sc:implement` run (#326 comment).
2. The coordinator's context grows with diffs and commit messages.
3. Orca's guide says a review-only `worker_done` "authorizes synthesis of findings, not coordinator file edits", and that PR preparation stays with the owner the user's plan names (`[G:cl] 62-65`). A commit is not a file edit, but a coordinator that also stages and prepares PRs is doing owner work unless the user's plan names it as owner.
4. Parallel experiments in separate worktrees each end on their own branch; the coordinator must commit in each worktree, which is more git work for one session.

## Self-check
GITDEMO: `git init` in `mktemp -d /tmp/gitlockdemo.XXXX`, created `.git/index.lock`, ran `git add f` (printed the fatal message above), removed the lock, added a linked worktree and printed `git rev-parse --git-path index` and `--git-path HEAD` for both (main `.git/index`, worktree `.git/worktrees/wt/index`; main `.git/HEAD`, worktree `.git/worktrees/wt/HEAD`), then created `refs/superclaude/demo` in the main checkout and resolved it from the linked worktree (it resolved). Directory deleted afterwards.
