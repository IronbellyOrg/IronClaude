---
name: sc:init-lite-protocol
description: "Full behavioral protocol for sc:init-lite — a safe, non-destructive audit of project-local SuperClaude context surfaces with a context-optimized report and optional advisory scaffold"
allowed-tools: Read, Glob, Grep, Write, Bash
argument-hint: "--context-optimized [--project-root <dir>] [--output <path>] [--dry-run] [--scaffold] [--force]"
---

# /sc:init-lite — Context-Optimized Init (Lite)

<!-- Extended metadata (for documentation, not parsed):
category: utility
complexity: low
mcp-servers: [serena]
personas: [analyzer]
version: 1.0.0
-->

## Triggers

sc:init-lite-protocol is invoked ONLY by the `sc:init-lite` command via `Skill sc:init-lite-protocol` in its `## Activation` section. It is never invoked directly by users.

Activation conditions:

- User runs `/sc:init-lite --context-optimized` in Claude Code.
- Any of `--project-root`, `--output`, `--dry-run`, `--scaffold`, `--force` are passed through from the command.

Do NOT invoke this skill directly. Use the `sc:init-lite` command.

## 1. Purpose

Produce a deterministic, non-destructive audit of a project's local SuperClaude context surfaces so an operator can see what loads into context and decide — by hand — what to slim down. The skill never rewrites existing context inputs; its only writes are a generated report and (opt-in) advisory scaffold files under `.dev/superclaude/`.

The mechanical audit is implemented as the `superclaude init-lite --context-optimized` CLI command (`src/superclaude/cli/init_lite.py`). The protocol's preferred execution path is to invoke that CLI with the resolved flags and surface its output; the safety invariants below are the contract the CLI already enforces and that this skill must preserve if it ever performs the audit directly.

## 2. Inputs

| Field | Source | Default |
|-------|--------|---------|
| project_root | `--project-root` | current directory |
| output | `--output` | `<project-root>/.dev/superclaude/context-audit.md` |
| dry_run | `--dry-run` | false |
| scaffold | `--scaffold` | false |
| force | `--force` | false |

`project_root` must be an existing directory (validated at the CLI boundary). A relative `--output` value resolves against `--project-root`, not the current working directory.

## 3. Workflow

1. **Discover** only project-local context surfaces under `project_root` (read-only): `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, every markdown file under `.claude/commands/**/*.md`, every `.claude/skills/**/SKILL.md`, and `.claude/agents/*.md`. Missing surfaces are reported, never created.
2. **Estimate** each surface's token weight as `ceil(bytes / 4)` and classify: `low` (< 1000), `medium` (1000–4000), `high` (> 4000).
3. **Report**:
   - Default: write the audit to `output` (which carries the generated marker `<!-- generated-by: superclaude init-lite context-audit v1 -->`), including the per-surface table and manual (non-automatic) optimization recommendations.
   - `--dry-run`: render the report to stdout and write nothing — do NOT create `.dev/superclaude/`.
4. **Scaffold** (only when `--scaffold`): create advisory `project-guidance/SKILL.md` and `project-guidance/refs/README.md` under `.dev/superclaude/`; idempotent (existing files are left intact unless `--force`).
5. **Surface** the resulting paths and the token summary to the user.

Preferred implementation: shell out to `superclaude init-lite` with the resolved flags via Bash and relay its output.

## 4. Safety Invariants (non-negotiable)

1. **Read-only context inputs** — never modify `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, `.claude/commands/**`, `.claude/skills/**`, or `.claude/agents/**` under ANY flag combination.
2. **Dry-run writes nothing** — and does not create `.dev/superclaude/`.
3. **Default = report only** — the only write is the marked report at `output`.
4. **Scaffold is opt-in and scoped** — exactly two files under `.dev/superclaude/project-guidance/`.
5. **`--force` is scope-limited** — marker-less overwrites are allowed only for init-lite-owned targets under `.dev/superclaude/`; never for files elsewhere, and never for a context input.
6. **No marker, no `--force`** — if `output` exists without the generated marker, fail with a clear error rather than overwrite. Marked reports may be overwritten on re-run at the default path or at an explicit `--output` path.

## 5. Outputs

- `.dev/superclaude/context-audit.md` (or `--output`) — the context-audit report (default / non-dry-run).
- `.dev/superclaude/project-guidance/SKILL.md` and `refs/README.md` — only with `--scaffold`.

No `refs/` are required for this skill; the report schema is small and lives in the CLI implementation. Add a lazy `refs/` file only if a future, substantially larger report/scaffold template is introduced.

## Boundaries

**Will:** discover surfaces read-only, estimate weight deterministically, write a non-destructive report (or stdout on dry-run), optionally scaffold advisory guidance, preserve all safety invariants.

**Will Not:** modify any target-project context input, write under `.claude/`, write anything on `--dry-run`, overwrite marker-less files unless `--force` is set and the target is under `.dev/superclaude/`, or perform automatic context migration.
