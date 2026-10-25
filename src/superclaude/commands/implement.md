---
name: implement
description: "Middleweight spec executor — walk a spec/PRD/tasklist, per-task spec-compliance QA, one-line ledger"
category: workflow
complexity: standard
argument-hint: "<path-or-prompt> [--resume] [--ledger <path>] [--skip-final-review]"
---

# /sc:implement — Middleweight Spec Executor

Walk a spec, PRD, tasklist, informal writeup, or inline prompt. After each task, verify that task against its acceptance criteria (the source itself, when informal). Lint and tests are extras, never the pass/fail.

## Triggers

**Explicit only.** Activates only when:

1. The user types `/sc:implement ...`
2. Another `/sc:*` command invokes `Skill sc:implement-protocol` with a path or prompt

Does not auto-activate from conversational "implement this" without this command.

## Required Input

**MANDATORY**: a source — one of:

- An existing file: spec, PRD, tasklist, or informal markdown/prose
- Inline prompt / general instructions in `$ARGUMENTS` (no file)

**STOP** if both are missing (bare `/sc:implement`) or the invocation uses removed flags. Informal prose and prompts are valid sources; they become one task whose AC is the source text.

```
Usage: /sc:implement <path-to-spec|prd|tasklist|notes> | /sc:implement <prompt>
STOP: need a source (file or prompt). Will not invent scope beyond that source.
```

## Usage

```bash
/sc:implement <path>
/sc:implement --spec <path>
/sc:implement --prd <path>
/sc:implement --tasklist <path>
/sc:implement Add logout to the header and wire it to /logout
/sc:implement <path> --resume
/sc:implement <path> --ledger <ledger-path>
/sc:implement <path> --skip-final-review
```

`--spec`, `--prd`, `--tasklist` are aliases for one file. A non-path remainder is an inline prompt.

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `<path>` / `--spec` / `--prd` / `--tasklist` | one of path or prompt | Existing file (formal or informal) |
| `<prompt>` | one of path or prompt | Inline instructions; persisted under `.dev/implement/<slug>/source.md` |
| `--resume` | implicit if a matching ledger exists | Continue from first non-complete task |
| `--ledger <path>` | `.dev/implement/<slug>/progress.md` | Override; MUST live under `.dev/implement/`. Managed packages always use the sibling `progress.md`; any other value STOPs |
| `--skip-final-review` | off | Skip the N>1 whole-list pass. On a managed package it also blocks archiving (FINAL is mandatory there) |

Banned tokens (STOP `E-LEGACY`, even if a path is also present): the four removed flags named in the protocol skill STOP table. Pass a spec path instead.

## Managed workflow packages

Managed packages: the ledger is the sibling `progress.md`, a fresh FINAL is mandatory, and only the archive helper moves the package; details in `refs/managed-workspace.md` of the protocol skill.

## Behavioral Flow

The command file performs only:

1. Parse `$ARGUMENTS` → one source path, or leftover text as prompt, + optional flags
2. STOP on empty invocation / banned grammar (usage above)
3. Hand off via Activation
4. On skill return, print the ledger path

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:implement-protocol

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in the protocol skill at
`~/.claude/skills/sc-implement-protocol/SKILL.md`.

## Boundaries

**Will Not:**

- Invent scope beyond the given source
- Treat a bare `/sc:implement` with no path and no prompt as a source
- Treat lint or tests as the pass/fail
- Invoke `/task` or `/sc:task`
- Import MDTM F1, 6-agent phase gates, or `/sc:reflect` as the per-task gate
- Auto-commit, open PRs, or release (a managed archive is not any of these)
- Move a package by any means other than the archive helper

Examples, boundaries and related commands: see the protocol skill (`~/.claude/skills/sc-implement-protocol/SKILL.md`).

## Completion

The run is done when every enumerable task has a `complete` ledger line (verdict `compliant`, or non-compliant plus an operator `Ruling:`). A `compliant` line may carry open minor/note findings recorded in the task's notes file. Suggest `/sc:test` and `/sc:git` only as optional next steps.
