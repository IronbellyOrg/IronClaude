# D3 option (a): `/sc:pr-submit` runs only in the coordinator's or a person's session

Position: `/sc:pr-submit` is never an Orca worker. After the workers finish, the coordinator (a top-level session) or the person runs it; pr-submit gets no Phase 4 changes (`SPEC:341`). This is the spec's current recommendation.

Citation key: `SPEC:N` = spec line; `PRS:N` = `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:N`; `PRC:N` = `src/superclaude/commands/pr-submit.md:N`; `HWW:N` = `src/superclaude/core/HOW-WE-WORK.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`.

## Safety
- The command says it is not headless. Its own boundary: "**Will Not:** run headless / imply a daemon" (`PRC:85`); the skill: "The monitor is an **attended, in-session** loop" and "Do NOT imply a background daemon" (`PRS:43-45`). A worker under `--unattended` is by definition a run with no person at the keyboard (`SPEC:54`). Running it as a worker contradicts the command's stated design.
- At its default `--monitor 3` it commits, pushes, retriggers review, and replies to and resolves threads (`HWW:221`, `HWW:307`; `PRC:83`), and the repo makes it the mandatory PR path (`CLAUDE.md:50`). Keeping it in a session where a person can watch keeps every outward step one hop from a person.
- Its HALTs (for example `pr_head_mismatch`, "follow the recovery steps in the HALT message", `PRC:28`) are written for an operator to act on.

## Reliability
- It must run top-level, never in a subagent (`PRS:47-49`); the coordinator is a top-level session, so it can run it as is (`CAPS:161`).
- No unverified pieces: under (b) the poll script's runtime per iteration is UNVERIFIED (`SPEC:394`) and the heartbeat rule depends on it (WC-10, `SPEC:74`).

## How a person works day to day
- One PR at a time from the coordinator's session; the person sees the review loop where they already talk to the coordinator. A run usually opens one PR at the end, so parallel PR monitoring is rarely needed.
- Weakness: while the coordinator polls (each wait up to the 600 s default, `PRC:49`, over up to `--max-rounds` cycles, `PRC:47`), it cannot service other workers' questions in that same turn.

## Implementation cost
- Zero: no pr-submit edits, no AC-4.3 run (`SPEC:276`), and 35 rather than 36 commands accept `--unattended` (`SPEC:195`). Reversible later by choosing (b) once a real need for parallel PR monitoring appears.
