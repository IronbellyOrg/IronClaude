# D3 option (c): hand pr-submit off to its own person-owned agent tab, unsupervised

Position: pr-submit is never a supervised worker (as in (a)) and gets no `--unattended` mode. When the person wants several PRs monitored at once, the coordinator, on the person's instruction, launches each pr-submit run as an Orca full handoff: a fresh Claude agent in that change's worktree with the slash command as its prompt (`ORCA agent launch --agent claude --worktree <id> --prompt "/sc:pr-submit --monitor 3 --head <branch> ..." --json`, `[CLI]` lines 49-52). The new tab is an ordinary session the person owns; the coordinator does not create a Task or wait on it (`[CLI]` lines 27-31).

Citation key: `SPEC:N` = spec line; `PRS:N` = `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:N`; `PRC:N` = `src/superclaude/commands/pr-submit.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `[CLI] N` / `[G] N` = line N of `orca-ide skills get orca-cli` / `orca-ide skills get orchestration` (1.4.237).

## Why a third option
(a) is safe but serial; (b) gives parallelism but makes an attended, top-level, "Will Not: run headless" command (`PRC:85`; `PRS:43-49`) into an unattended worker. (c) gives parallelism with the command exactly as it is today: each run is a normal top-level session in a visible tab, which is what pr-submit requires.

## Safety
- pr-submit runs unchanged, with every HALT and guard as written (`PRC:28`, `PRC:85`). A HALT waits in a visible tab, and a person's tab has no readiness limit (`CAPS:52`, "No time limit was observed for a person's launch tab").
- Orca's guide makes this the correct route for unsupervised work: "The user asks to hand off ownership or start another agent/worktree without supervision | Handoff owner | Use `orca-cli`; create no Run, Task, or Dispatch" (`[G]` line 39).
- The launch itself starts an outward loop, so the coordinator does it only when the person's instruction names it (D4).

## Reliability
- No worker-contract pieces at all: no heartbeat, no contract file, no `worker_done`. The run-log in `--output-dir` (`PRC:55`) and `--resume` (`PRC:56`) work as today.
- Weakness: the coordinator gets no completion signal. The person reads each tab, or the coordinator reads the run-log file later. Whether a slash command passed as `--prompt` runs as a slash command is UNVERIFIED; the spec's own workers depend on the same argv prompt mechanism for Claude (`CAPS:47`).

## How a person works day to day
- One tab per PR, each showing the review loop live; the person steps in only on a HALT. The coordinator's session stays free.

## Implementation cost
- One sentence in section 4 / D3 of the spec; no pr-submit edits, no AC-4.3. Cost to switch to (b) later is unchanged.
