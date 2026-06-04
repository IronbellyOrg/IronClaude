---
name: init-lite
description: "Safely audit project-local SuperClaude context surfaces and write a non-destructive, context-optimized report (optional advisory scaffold)"
category: utility
complexity: low
allowed-tools: Read, Glob, Grep, Bash, Skill
mcp-servers: [serena]
personas: [analyzer]
version: "1.0.0"
---

# /sc:init-lite

Audit the project-local SuperClaude context surfaces (`CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, `.claude/commands/**/*.md`, `.claude/skills/**/SKILL.md`, `.claude/agents/*.md`), estimate their context weight deterministically, and write a non-destructive context-audit report. Existing context inputs are read-only; nothing is rewritten. Optionally scaffold advisory project-guidance files under `.dev/superclaude/`.

## Triggers

When the user wants a safe, read-only context audit of a project's SuperClaude surfaces, a context-weight estimate, or an opt-in advisory project-guidance scaffold — without mutating any existing context input.

## Usage

```text
/sc:init-lite --context-optimized [--project-root <dir>] [--output <path>] [--dry-run] [--scaffold] [--force]
```

## Arguments

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--context-optimized` | Yes | -- | Run the context-weight audit over project-local SuperClaude surfaces. |
| `--project-root` | No | `.` (current dir) | Project directory to audit. |
| `--output` | No | `<project-root>/.dev/superclaude/context-audit.md` | Report output path. |
| `--dry-run` | No | false | Render the report to stdout and write nothing; does not create `.dev/superclaude/`. |
| `--scaffold` | No | false | Also create advisory `project-guidance/SKILL.md` and `project-guidance/refs/README.md` under `.dev/superclaude/`. |
| `--force` | No | false | Overwrite init-lite-owned generated artifacts under `.dev/superclaude/` only; never context inputs. |

## Behavioral Summary

1. Discover only the project-local context surfaces listed above (read-only).
2. Estimate each surface's token weight as `ceil(bytes / 4)` and classify low/medium/high.
3. Write a context-audit report (default) bearing a generated marker, or render it to stdout (`--dry-run`).
4. Optionally create advisory project-guidance scaffold files (`--scaffold`).
5. Never modify `CLAUDE.md`, `.mcp.json`, or any `.claude/` asset under any flag combination.

The mechanical audit is also available as the `superclaude init-lite --context-optimized` CLI command; the protocol skill owns the orchestration, report schema, and safety gating.

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:init-lite-protocol

Pass the following context (user-provided flags, pass-through):

- Project root: resolved `--project-root` (default current directory)
- Output path: resolved `--output` (default `.dev/superclaude/context-audit.md`)
- Dry run: boolean `--dry-run`
- Scaffold: boolean `--scaffold`
- Force: boolean `--force`

Do NOT attempt to execute the init-lite audit using only this command file. The full audit/report/scaffold protocol and all safety invariants are in the protocol skill.

## Examples

```bash
# Default: write a context-audit report under .dev/superclaude/
/sc:init-lite --context-optimized

# Preview only — render the report, write nothing
/sc:init-lite --context-optimized --dry-run

# Audit a different project root
/sc:init-lite --context-optimized --project-root ../other-project

# Also create the advisory project-guidance scaffold
/sc:init-lite --context-optimized --scaffold

# Overwrite an existing init-lite-owned report
/sc:init-lite --context-optimized --force
```

## Boundaries

**Will:**

- Discover only project-local SuperClaude context surfaces (read-only)
- Estimate context weight deterministically (`ceil(bytes / 4)`)
- Write a non-destructive report under `.dev/superclaude/` by default, or to an explicit `--output` path when provided (or stdout on `--dry-run`)
- Optionally create advisory project-guidance scaffold files under `.dev/superclaude/`
- Invoke the protocol skill with the resolved flag context

**Will Not:**

- Modify `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, `.claude/commands/**`, `.claude/skills/**`, or `.claude/agents/**`
- Write anything when `--dry-run` is set
- Overwrite marker-less files unless `--force` is set and the target is under `.dev/superclaude/`
- Execute the audit protocol from this command file alone (that is the skill's job)
