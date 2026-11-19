# File-Based Session Memory (Design Note)

This note explains how IronClaude keeps session memory in plain markdown files under `<project>/.superclaude/memory/`, and which commands, agents and skills read and write it. It is for maintainers who change `/sc:pm`, the PM agent or a skill that uses the store. Line numbers were taken at tag v5.0.0 and re-read for the PM agent in 6.0.0, which removed the `save` and `load` commands that used to be part of the store (and with them the read-only fallback to the old Serena folder).

For the user-facing view, see [Session management](../user-guide/session-management.md). For the separate error-learning store under `docs/memory/`, see [Memory system](../user-guide/memory-system.md).

## Contents

1. [Parts and files](#parts-and-files)
2. [Store layout](#store-layout)
3. [Keys and write rules](#keys-and-write-rules)
4. [Who reads and writes the store](#who-reads-and-writes-the-store)
5. [Why files and not an MCP server](#why-files-and-not-an-mcp-server)
6. [Stores this is not](#stores-this-is-not)
7. [Changing the store](#changing-the-store)

## Parts and files

There is no Python or shell code behind the store. It is a set of instructions in command, agent and skill files, which Claude follows with its Read, Write and Glob tools. Because the behaviour is prompt-driven, the wording and file contents a session produces can vary between runs.

| Part | File |
|---|---|
| PM command | `src/superclaude/commands/pm.md` |
| PM agent | `src/superclaude/agents/pm-agent.md` (section "Session Lifecycle", lines 19-35) |
| PM protocol skill | `src/superclaude/skills/sc-pm-protocol/SKILL.md` (lines 21-54) |
| Other skills that use the store | `sc-task-protocol`, `sc-reflect-protocol`, `sc-crash-recovery` (see [Who reads and writes the store](#who-reads-and-writes-the-store)) |

## Store layout

- **Location.** Each memory is `<project>/.superclaude/memory/<key>.md`, flat markdown, with subfolders allowed for topics (`pm-agent.md:21`).
- **Project root.** `<project>` is the git top-level of the current directory (`git rev-parse --show-toplevel`), or the current directory when it is not inside git (`pm-agent.md:21`).
- **One store per worktree.** `git rev-parse --show-toplevel` returns the root of the worktree you are in, so each git worktree of the same repository has its own `.superclaude/memory/` and does not see the others' memories (`pm-agent.md:21`).
- **Kept out of git.** On the first write, if `<project>/.superclaude/.gitignore` is absent, the writer creates it with the single line `*` (`pm-agent.md:21`). The whole `.superclaude/` folder, including the `.gitignore` itself, is then ignored. The skills that write their own subfolders repeat this rule before writing (`sc-task-protocol/SKILL.md:319`, `sc-reflect-protocol/SKILL.md:329`).

Example layout after a few sessions:

```text
<project>/.superclaude/
├── .gitignore                          # contains the single line: *
└── memory/
    ├── pm_context.md                   # single-owner, overwritten
    ├── last_session.md                 # single-owner, overwritten
    ├── next_actions.md                 # single-owner, overwritten
    ├── checkpoint-20261102-1430.md     # parallel key, written once
    ├── learning/patterns/<name>.md     # PM protocol topic subfolder
    ├── reflect/last-pass-<slug>.md     # /sc:reflect subfolder
```

## Keys and write rules

The rules exist so that several sessions in one worktree can write without overwriting each other's work.

| Kind | Keys | Rule | Source |
|---|---|---|---|
| Single-owner | `pm_context`, `last_session`, `next_actions` | Overwritten whole on each write | `pm-agent.md:21` |
| Single-owner (PM only) | `current_plan` | Overwritten whole | `pm-agent.md:21`, `sc-pm-protocol/SKILL.md:23` |
| Parallel | `checkpoint`, `decision`, handoffs | Written as `<key>-<session-or-timestamp>.md` and never edited in place | `pm-agent.md:21` |

Subfolder keys follow the same split. For example, `/sc:reflect` overwrites `reflect/last-pass-{slug}.md` whole and writes `reflect/handoff-{slug}-{timestamp}.md` once (`sc-reflect-protocol/SKILL.md:539-541`).

## Who reads and writes the store

### `/sc:pm` and the PM agent

`/sc:pm` loads the `sc:pm-protocol` skill before acting (`pm.md:51-52`). The PM agent and the protocol both describe the same lifecycle:

- **Start:** Glob `.superclaude/memory/**/*.md`, then Read `pm_context.md`, `current_plan.md`, `last_session.md` and `next_actions.md` (`pm-agent.md:30-35`, `sc-pm-protocol/SKILL.md:28-32`).
- **During work:** write the goal to `current_plan.md` and progress to `checkpoint-<timestamp>.md` (`pm-agent.md:54,67`, `sc-pm-protocol/SKILL.md:45-46`).
- **End:** write `last_session.md`, `next_actions.md` and `pm_context.md` (`sc-pm-protocol/SKILL.md:52-54`).
- **Learning files:** solutions, patterns and mistakes go under `learning/solutions/`, `learning/patterns/` and `learning/mistakes/` (`sc-pm-protocol/SKILL.md:115,159,168`); the general key pattern `[category]/[subcategory]/[identifier]` maps to `.superclaude/memory/[category]/[subcategory]/[identifier].md` (`sc-pm-protocol/SKILL.md:132`).

`pm.md:12` and `pm.md:16` describe the PM agent as always active and restoring context at every session start. No hook does this: none of the SessionStart hooks in `src/superclaude/hooks/hooks.json:3-43` reads `.superclaude/memory/`, and `src/superclaude/scripts/session-init.sh` (the first SessionStart hook) does not mention memory. The restore happens only when the PM agent or the `sc:pm-protocol` skill is loaded into the session and Claude follows its instructions.

### Other skills

| Skill | Use of the store | Source |
|---|---|---|
| `sc-task-protocol` | Reads relevant memories before work; saves session state to `task/session-<timestamp>.md` | `sc-task-protocol/SKILL.md:90,304,319` |
| `sc-reflect-protocol` | Reads and writes `reflect/` files; the `--remediate` MDTM route writes a handoff file whose key task-builder reads | `sc-reflect-protocol/SKILL.md:259,329-331,537-547` |
| `sc-crash-recovery` | Counts memory files and spawns a project-memory investigator only when the store has files | `sc-crash-recovery/SKILL.md:62,79`, `sc-crash-recovery/scripts/bootstrap_scan.sh:153-154` |

## Why files and not an MCP server

5.0.0 removed Serena and codebase-memory-mcp (Breaking Change 1, `docs/releases/v5.0.0.md:194-198`). Memory moved to plain files so that it needs no MCP server. Plain files also make the store easy to inspect, copy between worktrees by hand, or delete. Before 5.0.0 the PM command and two since-removed commands, `save` and `load`, kept memories through Serena in `<project>/.serena/memories/` (`docs/releases/v5.0.0.md:154,196`). 5.0.0 let `load` read that folder as a one-release, read-only fallback; 6.0.0 removed both commands and the fallback, so nothing reads `.serena/memories/` now. A user who still has memories there copies them across by hand (`docs/getting-started/upgrading.md`, Step 5).

## Stores this is not

Two other "memory" folders exist. Keep them apart when you change any of the three.

| Store | Location | Written by | Source |
|---|---|---|---|
| Session memory (this note) | `<project>/.superclaude/memory/` | `/sc:pm`, PM agent, the skills above | `pm-agent.md:21` |
| Reflexion error-learning | `docs/memory/solutions_learned.jsonl` under the current directory (or `REFLEXION_OUTPUT_DIR`), plus a sibling `docs/mistakes/` | `ReflexionPattern` in Python | `src/superclaude/pm_agent/reflexion.py:14-17,65-77` |
| Claude Code auto memory | `~/.claude/projects/<key>/memory/` | Claude Code itself; the freshness SessionStart hook prints a short index of it | `src/superclaude/hooks/scripts/freshness-session-start.sh:60-62` |

## Changing the store

1. Change the rule in every file that states it, not just one: `agents/pm-agent.md`, `skills/sc-pm-protocol/SKILL.md`, and any skill above that repeats the location or the `.gitignore` rule.
2. Run `make sync-dev` and then `make verify-sync`. Stage only the `src/superclaude/` side, never `.claude/`.
3. Keep the user guide [Session management](../user-guide/session-management.md) in step with the rule.
