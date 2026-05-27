---
name: init-lite
description: "Audit project-local SuperClaude context surfaces and (optionally) scaffold advisory project-guidance files; non-destructive by default."
category: utility
complexity: low
allowed-tools: Read, Glob, Grep, Bash, Skill
mcp-servers: []
personas: [analyzer, architect]
version: "1.0.0"
---

# /sc:init-lite

Audit project-local SuperClaude context surfaces (`CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, `.claude/commands/**`, `.claude/skills/**/SKILL.md`, `.claude/agents/*.md`), estimate their context weight deterministically, and write a non-destructive context audit report. Optionally scaffold advisory project-guidance files under `.dev/superclaude/project-guidance/`. Never mutates context inputs.

## Triggers

When the user asks to audit a project's SuperClaude context footprint, estimate which context surfaces are heaviest, or scaffold an advisory project-guidance starter — without rewriting existing context inputs.

## Usage

```text
/sc:init-lite --context-optimized [--project-root <dir>] [--output <path>] [--dry-run] [--scaffold] [--force]
```

## Behavioral Summary

The command discovers only project-local SuperClaude context surfaces, computes a deterministic `ceil(bytes / 4)` token estimate for each, classifies them into `low` / `medium` / `high` buckets, and writes a markdown audit report. `--dry-run` renders the report to stdout and writes nothing. `--scaffold` additionally creates advisory starter files under `.dev/superclaude/project-guidance/`. `--force` permits overwriting init-lite-owned report/scaffold files (identified by the generated marker); it NEVER overwrites `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, or any `.claude/` asset.

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--context-optimized` | Yes | -- | Selects the context-optimized audit mode (currently the only mode). |
| `--project-root <dir>` | No | current working directory | Project root to audit. |
| `--output <path>` | No | `.dev/superclaude/context-audit.md` (under project root) | Report output path. |
| `--dry-run` | No | false | Render the report to stdout; write nothing to disk. |
| `--scaffold` | No | false | Also create advisory `.dev/superclaude/project-guidance/SKILL.md` and `refs/README.md`. |
| `--force` | No | false | Overwrite init-lite-owned report/scaffold files. Never overwrites context inputs. |

## Input Validation

1. **`--context-optimized` required**: emitting `/sc:init-lite` without `--context-optimized` is a usage error.
2. **`--project-root` is a directory**: if provided, the path MUST resolve to an existing directory.
3. **Output ownership check**: if `--output` (or the default path) exists and does NOT start with the init-lite generated marker, the command refuses to overwrite unless `--force` is passed.

## Activation

**Classification**: SAFE -- read-only audit + bounded `.dev/` write.

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc-init-lite-protocol

Pass the following context (the user-provided flags, unchanged):

- `--context-optimized` flag
- `--project-root` value (or current working directory)
- `--output` value (or default)
- `--dry-run` flag
- `--scaffold` flag
- `--force` flag

Do NOT attempt to execute the audit using only this command file. The full protocol — discovery scope, token estimate formula, report format, scaffold contents, and no-mutation invariants — lives in the protocol skill.

## Examples

```bash
# Default: write the audit report to .dev/superclaude/context-audit.md
/sc:init-lite --context-optimized

# Dry-run: render to stdout, write nothing
/sc:init-lite --context-optimized --dry-run

# Scaffold advisory project-guidance starter files alongside the report
/sc:init-lite --context-optimized --scaffold

# Audit a different project root
/sc:init-lite --context-optimized --project-root /path/to/other/project

# Overwrite an init-lite-owned report (won't touch CLAUDE.md or .claude/)
/sc:init-lite --context-optimized --force
```

## Boundaries

**Will:**

- Read project-local context surfaces (`CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, `.claude/commands/**/*.md`, `.claude/skills/**/SKILL.md`, `.claude/agents/*.md`).
- Compute deterministic `ceil(bytes / 4)` token estimates and classify into low/medium/high buckets.
- Write the audit report to `.dev/superclaude/context-audit.md` (or `--output`) with the generated marker.
- Optionally create advisory scaffold files under `.dev/superclaude/project-guidance/`.
- Refuse to overwrite a non-marker output unless `--force` is passed.

**Will Not:**

- Modify `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, `.claude/commands/**`, `.claude/skills/**`, or `.claude/agents/**`.
- Create or write under `.claude/` in the target project.
- Write anything when `--dry-run` is set.
- Stage or commit any files; output discoverability is left to the operator.
