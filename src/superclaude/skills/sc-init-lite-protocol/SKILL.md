---
name: sc-init-lite-protocol
description: "Behavioral protocol for /sc:init-lite — safe, non-destructive audit of project-local SuperClaude context surfaces with optional advisory scaffolding under .dev/superclaude/."
allowed-tools: Read, Glob, Grep, Write, Bash
argument-hint: "--context-optimized [--project-root <dir>] [--output <path>] [--dry-run] [--scaffold] [--force]"
---

# sc-init-lite-protocol — Context-Optimized init-lite Audit

<!-- Extended metadata (for documentation, not parsed):
category: utility
complexity: low
mcp-servers: []
personas: [analyzer, architect]
version: 1.0.0
-->

## Triggers

`sc-init-lite-protocol` is invoked ONLY by the `/sc:init-lite` command via `Skill sc-init-lite-protocol` in its `## Activation` section. It is never invoked directly by users.

Activation conditions:

- The user runs `/sc:init-lite --context-optimized [...]` in Claude Code.
- The command passes through `--context-optimized`, `--project-root`, `--output`, `--dry-run`, `--scaffold`, and `--force` exactly as the user provided them.

Do NOT invoke this skill directly. Use the `/sc:init-lite` command.

## 1. Purpose

Help an operator understand and lighten the SuperClaude context their project loads on every session, WITHOUT mutating any context inputs. The protocol:

1. Discovers project-local context surfaces (read-only).
2. Estimates each surface's context weight deterministically.
3. Produces a markdown audit report at `.dev/superclaude/context-audit.md` (or `--output`) with advisory recommendations.
4. Optionally scaffolds advisory project-guidance starter files under `.dev/superclaude/project-guidance/` when `--scaffold` is passed.

The Python CLI module `superclaude.cli.init_lite` already implements the algorithm. The skill's job here is to map user intent to the correct CLI invocation, surface safety boundaries, and explain results.

## 2. Discovery Scope (Read-Only)

Scan exactly these project-local files under `--project-root` (default: current working directory):

- `CLAUDE.md`
- `.mcp.json`
- `.claude/settings.json`
- `.claude/commands/**/*.md`
- `.claude/skills/**/SKILL.md`
- `.claude/agents/*.md`

NEVER scan or modify anything else. NEVER read user home `~/.claude/` from this skill.

## 3. Deterministic Token Estimate & Buckets

For each discovered surface, compute `estimate = ceil(bytes / 4)`. Classify:

| Estimate | Bucket |
|----------|--------|
| `< 1000` | `low` |
| `1000`–`4000` (inclusive) | `medium` |
| `> 4000` | `high` |

These thresholds are pinned by the CLI module and verified in tests; do NOT vary them per project.

## 4. Mode Semantics

| Flag combination | Behavior |
|------------------|----------|
| default (no `--dry-run`, no `--scaffold`) | Write the audit report to `.dev/superclaude/context-audit.md` (or `--output`). Create the parent directory if needed. Do NOT create the scaffold. |
| `--dry-run` | Render the report to stdout. Write nothing. Do NOT create `.dev/superclaude/`. |
| `--scaffold` (without `--dry-run`) | In addition to writing the report, create `.dev/superclaude/project-guidance/SKILL.md` and `.dev/superclaude/project-guidance/refs/README.md` if missing. |
| `--force` | Permits overwriting init-lite-owned report/scaffold files (identified by the generated marker `<!-- generated-by: superclaude init-lite context-audit v1 -->`). NEVER overwrites context inputs. |

## 5. Safety Invariants (Non-Negotiable)

- NEVER modify `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, `.claude/commands/**`, `.claude/skills/**`, or `.claude/agents/**` under the target project.
- NEVER create any file or directory under the target project's `.claude/`.
- NEVER write anything when `--dry-run` is set.
- NEVER overwrite an existing output file that does NOT start with the generated marker `<!-- generated-by: superclaude init-lite context-audit v1 -->` unless `--force` is set; refuse with a clear error instead.
- The `Edit` tool is intentionally absent from this skill's `allowed-tools` so the agent cannot patch existing context inputs in-place.

## 6. Behavioral Flow

1. **Receive flags** from the command Activation handoff. If `--context-optimized` is missing, surface the usage error from the CLI rather than improvising a fallback.
2. **Invoke the CLI** by running `superclaude init-lite --context-optimized [...]` with the flags the user provided. The Python CLI module performs discovery, token estimation, report rendering, and conditional writes.
3. **Surface results** to the user: the report path (or stdout dump for `--dry-run`), the biggest contributor, and the overall bucket.
4. **Recommend next steps** only if the overall bucket is `medium` or `high`: suggest moving non-essential `CLAUDE.md` sections into `.dev/superclaude/project-guidance/refs/<topic>.md`. Do not perform that move automatically.

## 7. Outputs

| Output | Trigger | Path |
|--------|---------|------|
| Audit report | default | `<project-root>/.dev/superclaude/context-audit.md` (or `--output`) |
| Audit report (stdout) | `--dry-run` | rendered to stdout, nothing written |
| Scaffold skill stub | `--scaffold` | `<project-root>/.dev/superclaude/project-guidance/SKILL.md` |
| Scaffold refs README | `--scaffold` | `<project-root>/.dev/superclaude/project-guidance/refs/README.md` |

## 8. Lazy Refs Policy

This skill intentionally ships without `refs/`. The behavioral protocol fits within `SKILL.md` and the report template lives inside the Python CLI. If a future iteration needs bulky templates (e.g., a long advisory-recommendations corpus), add them under `refs/` and explicitly `Read` them only at the phase where they are needed — per the developer-guide token-efficiency rule that `refs/` content loads on demand, not at session start.

## 9. Failure Surfaces

| Condition | Expected response |
|-----------|-------------------|
| `--project-root` does not exist or is not a directory | CLI raises `click.UsageError`; skill surfaces it verbatim. |
| Existing output file lacks generated marker, `--force` not set | CLI raises `click.ClickException`; skill suggests re-running with `--force` only if the operator confirms intent. |
| No context surfaces found | Report still written (or echoed), noting "No project-local SuperClaude context surfaces detected." |

## 10. Why this is safe by default

The protocol is read-only on context inputs. All writes are confined to `.dev/superclaude/` under the target project. `--dry-run` performs zero writes. `--force` only relaxes the marker check for files the skill itself owns. Together these invariants make the command safe to run on unfamiliar projects.
