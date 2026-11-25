# Opportunity map: where /sc:brainstorm spawns sub-agents

Read on 2026-11-11 from `src/superclaude/`. Line numbers are from that read.

## Spawn points (all use the in-session `Task` tool)

| # | Where | What spawns | Shape | Evidence |
|---|-------|-------------|-------|----------|
| S1 | brainstorm Wave 2A (enrichment) | up to 3 Task agents: codebase scan, light research, deep research | parallel, 120s timeout each, partial-OK | `skills/sc-brainstorm-protocol/SKILL.md:179`, `refs/handoff-routing.md:77` |
| S2 | adversarial Mode B variant generation (called from brainstorm Wave 3) | one Task agent per `--agents` spec (N = 2 to 7) writes one proposal | parallel, single shot | `skills/sc-adversarial-protocol/SKILL.md:2203-2231` |
| S3 | adversarial Round 1 advocates | one Task agent per variant, `max_turns: 5`, model from agent spec | parallel, all in one message block | `SKILL.md:1021-1055` |
| S4 | adversarial Round 2 rebuttals | one agent per advocate | SEQUENTIAL (each sees earlier rebuttals) | `SKILL.md:1077-1093` |
| S5 | adversarial scoring / merge | Task with opus or sonnet | single | `SKILL.md:1965-1968` |

Not spawns (stay in the main session): Wave 0 validation, Wave 1 Socratic dialogue (talks to the user), Wave 2B agent-spec composition (pure logic), Wave 4 handoff (`Skill` calls to tasklist / task-builder).

## Primitives that would change

| File | Change needed | Size |
|------|---------------|------|
| `skills/sc-brainstorm-protocol/SKILL.md` | Execution Vocabulary table, `allowed-tools` (Task -> Bash for `orca`), Wave 2A dispatch, Wave 3 token accounting (line 371 says "measured from Task notification"), hard-kill rule at 1.25x estimate | medium |
| `skills/sc-brainstorm-protocol/refs/handoff-routing.md` | enrichment dispatch (line 77) | small |
| `skills/sc-brainstorm-protocol/refs/agent-spec-builder.md` | model aliases `opus/sonnet/haiku` become Orca `--agent` + `--model` ids; token budget table | small |
| `commands/brainstorm.md` | new flag (for example `--runtime task|orca`), Related Commands | small |
| `skills/sc-adversarial-protocol/SKILL.md` (2985 lines) + `refs/agent-specs.md`, `refs/debate-protocol.md` | S2 to S5 dispatch blocks | LARGE, and shared with every other caller of sc:adversarial (roadmap, troubleshoot, reflect, spec-panel and others) |
| new ref | worker prompt file template, `worker_done` result-file contract, polling loop, failure and retry rules | new |

## Orca facts verified from `orca ... --help` (CLI 1.4.245)

- `orca orchestration worker-start --spec <text> --agent claude|codex|... --model <id> --worktree current|new-child` starts one supervised worker; `worker-read`, `worker-show`, `worker-stop`, `dispatch`, `ask`, `send`, `check` exist.
- `--agent` accepts more than Claude (codex, cursor, opencode and others), so a debate can use truly different model families.
- Worker output is read back with `worker-read --source auto|transcript`; there is no token-usage field in the help text (UNVERIFIED whether one exists elsewhere).
- Orca must be running and the session must be inside an Orca worktree. Skills here are installed into OTHER projects (CLAUDE.md rule), where Orca may not exist.

## Known process rules in this user's memory (apply to any Orca refactor)

- A `turn_started` receipt is not proof a worker is working; verify on screen.
- A coordinator must keep polling and re-arm waits.
- Never pass Orca link flags (`--issue`, `--pr`) for this repo.
