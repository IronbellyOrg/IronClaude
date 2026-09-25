# Codebase context — sc:implement rewrite

quality_tier: primary (auggie)

## Current implement command

- `src/superclaude/commands/implement.md` — only implementation. No skill, no Activation.
- Mirrors: `plugins/superclaude/commands/implement.md`, installed command copies.
- Behavioral mode: personas + MCP, free-form feature description, flags `--type/--framework/--safe/--with-tests`.
- Completion: compiles, basic functionality, ready for `/sc:test` then `/sc:git`.

## Required architecture (once Activation is added)

- Thin command (~80–150 lines): flags, examples, boundaries, `## Activation` → `Skill sc:implement-protocol`.
- Protocol skill: `src/superclaude/skills/sc-implement-protocol/SKILL.md` + `refs/` loaded per phase. SKILL.md max ~500 lines.
- `make lint-architecture` Check 1: command with Activation must have `sc-<name>-protocol` or `sc-<name>` skill dir.
- Edit `src/superclaude/` then `make sync-dev`. Do not stage `.claude/skills`.

Canonical thin-dispatcher examples:

- `src/superclaude/commands/reflect.md` → `Skill sc:reflect-protocol`
- `src/superclaude/commands/brainstorm.md` → `Skill sc:brainstorm-protocol`
- `src/superclaude/commands/auggie-review.md` → `Skill sc:auggie-review-protocol`

## Existing ledgers (do not copy wholesale)

| Mechanism | Where | Weight |
|---|---|---|
| F1 checklist on disk | `src/superclaude/skills/task/SKILL.md` | Heavy: re-read file, one item, 6-agent phase-gate QA, post-completion 4-step |
| Execution log table | sc-tasklist-protocol `execution-log.md` | Sprint/tasklist, not implement |
| Reflect per-task verdicts | sc-reflect-protocol `per_task_verdicts` | Post-hoc audit, not an executor |
| TurnLedger | sprint CLI | Budget, not spec QA |

Implement should steal the **idea** (progress on disk, one line per task) not these schemas.

## Related commands (boundaries)

- `/sc:task` — compliance-tiered task execution (STRICT/STANDARD/LIGHT). Different job.
- `/task` — MDTM F1 executor. Different job.
- `/sc:workflow` — generates workflows from PRDs; does not execute them.
- `/sc:tdd` — builds an MDTM task then hands to `/task`. Heavier path.
- `/sc:test` / `/sc:git` — current implement's "next step"; extras stay optional, not the gate.
