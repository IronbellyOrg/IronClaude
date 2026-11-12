---
name: sweep
description: "Read Orca Runs, worktrees and sessions once and publish one report that says what each session is doing, which ones wait on a person, and what could not be read"
category: utility
complexity: basic
mcp-servers: []
personas: []
argument-hint: "[--run <id>]... [--window <N>h|<N>d] [--root <dir>] [--output <dir>]"
allowed-tools: Skill
---

# /sc:sweep: Read-only Report on Orca Runs, Worktrees and Sessions

Reads the Orca Runs you name (or the Run bound to this terminal), the worktrees of this checkout and the Claude Code sessions in the activity window, and publishes one Markdown report under `<root>/.dev/sweeps/`. The report puts every session into one of eight classes (for example working, waiting on a person, idle, finished, stalled (proved), or could not determine), lists what waits on a person and why, and lists every source it could not read. It only reads: it changes nothing in Orca, in git or in any worktree, and the report is the one file it adds.

The report also states, as facts to review, `Safe to close`, `Removable` and `Next inspection` (what to read next); these are observations, not advice, and the coordinator or person decides. In Phase 1 the classes stalled (proved) and fenced are not observed, so a zero count there means nothing; the report says so.

`/sc:sweep` is coordinator or person only. It is on the never-as-worker list in `~/.claude/WORKER-CONTRACT.md`, so a dispatched worker never runs it.

## Triggers

Explicit only: the coordinator runs `/sc:sweep` inside its liveness sweep pass, at most once every 5 minutes (WC-16 in `~/.claude/WORKER-CONTRACT.md`), or a person types it. Nothing starts it automatically.

## Usage

```text
/sc:sweep                                  # the Run bound to this terminal, window 6h
/sc:sweep --run run_0123456789ab           # one named Run
/sc:sweep --run run_0123456789ab --run run_fedcba987654 --window 2d
/sc:sweep --root /path/to/checkout --output /path/to/checkout/.dev/sweeps/archive
```

## Options

| Flag | Default | Meaning |
|---|---|---|
| `--run <id>` | the Run bound to this terminal | An Orca Run id (`run_` plus 12 lowercase hex digits). Repeat the flag to read several Runs; duplicates are read once. When no Run is bound and none is named, the command exits with a message that asks for `--run <id>`. |
| `--window <N>h\|<N>d` | `6h` | How far back a session counts as active. `<N>` is 1 to 9999, at most `720h` or `30d`. |
| `--root <dir>` | the checkout found by walking up from the current folder | The checkout root; it must hold `.git`. |
| `--output <dir>` | `<root>/.dev/sweeps/` | The report folder. It must be `<root>/.dev/sweeps/` or a folder below it, and must not overlap the folders the sweep reads. |

There is no worker mode and no flag for one.

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:sweep-protocol

Pass the user's flags unchanged. Do NOT proceed using only this command file. The installed skill is:

- `~/.claude/skills/sc-sweep-protocol/SKILL.md`

When a project checkout holds its own copy (a dev checkout that ran `make sync-dev`), the dual surface is:

- `.claude/skills/sc-sweep-protocol/SKILL.md`

Skills read `~/.claude/skills/` first. The skill runs the `superclaude sweep run` command, reads the report it names, and prints the counts and the report path. It adds no recommendation and takes no action.

## Boundaries

**Will:**

- Run `superclaude sweep run` with the flags you gave and print the session counts and the report path
- Read the published report so the counts and the report agree

**Will Not:**

- Change anything in Orca, git or a worktree, or write any file except the one report
- Add advice or a next step of its own to the report or to the reply
- Run as a dispatched worker
