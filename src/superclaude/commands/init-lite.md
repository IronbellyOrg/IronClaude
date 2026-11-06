---
name: init-lite
description: "Safely audit project-local SuperClaude context surfaces and write a non-destructive, context-optimized report (optional advisory scaffold)"
category: utility
complexity: low
allowed-tools: Read, Glob, Grep, Bash, Skill
mcp-servers: []
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
/sc:init-lite --context-optimized --unattended --report-dir <dir>   # worker mode, see Unattended mode
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
| `--unattended` | No | false | Worker mode: no step waits for a person; see Unattended mode. |
| `--report-dir` | With `--unattended` | -- | The directory that holds the worker contract (`--output` names the report file, not a directory). |

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
- Unattended: boolean `--unattended`
- Report directory: resolved `--report-dir` (only with `--unattended`)

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

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:init-lite` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only: its `--output <file>` names the report file, not a directory. Without `--report-dir` the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is the exception to Safety Invariants 2 and 3 of the protocol: it is the one write besides the report and the scaffold, and it is written also on `--dry-run`. `report_path` is the audit report (the `--output` path or `.dev/superclaude/context-audit.md`), null on `--dry-run`; `artifacts` lists only the scaffold files this run wrote, as printed on the tool's `Scaffold:` lines, one per file as it is written (files `--force` overwrote and a file written before a later scaffold write failed included), and is `[]` on `--dry-run` and when no `Scaffold:` line was printed. The run is succeeded when the audit finished, and failed otherwise.
- **Context inputs.** The command never modifies a context input.
- **Gates.** None, and no person-mode flag. Nested invocations: none.
- **Outward actions.** It pushes, commits and stages nothing.

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
  - Except `<report-dir>/return-contract.yaml` under `--unattended`
- Overwrite marker-less files unless `--force` is set and the target is under `.dev/superclaude/`
- Execute the audit protocol from this command file alone (that is the skill's job)
