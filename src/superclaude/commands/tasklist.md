---
name: tasklist
description: "Generate deterministic, Sprint CLI-compatible tasklist bundles from roadmaps with integrated roadmap validation"
category: utility
complexity: high
allowed-tools: Read, Glob, Grep, Write, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet, Task, Skill
mcp-servers: [context7]
personas: [analyzer, architect]
version: "2.0.0"
---

# /sc:tasklist

Generate a deterministic, Sprint CLI-compatible tasklist bundle from a roadmap file. Transforms roadmap items into phased, execution-ready task files with compliance tier classification and verification routing. After generation, automatically validates the tasklist against the source roadmap, patches any drift, and verifies corrections.

## Triggers

When the user requests roadmap-to-tasklist conversion, sprint planning from a roadmap, or tasklist generation for execution via `superclaude sprint run`.

## Usage

```text
/sc:tasklist <roadmap-path> [--spec <spec-path>] [--output <output-dir>] [--no-reflect]
```

Both `@file` syntax and explicit file paths are supported for `<roadmap-path>` and `--spec`.

## Behavioral Summary

Transforms a roadmap into a Sprint CLI-compatible multi-file tasklist bundle. The command parses arguments, validates inputs, derives the output directory, and invokes the `sc:tasklist-protocol` skill which contains the full generation algorithm. The command itself does not execute any generation logic.

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `<roadmap-path>` | Yes | -- | Path to roadmap file. Accepts `@file` reference or explicit path. |
| `--spec <spec-path>` | No | -- | Supplementary spec/context file for additional generation context. |
| `--output <output-dir>` | No | Auto-derived from roadmap `TASKLIST_ROOT` | Output directory for the tasklist bundle. |
| `--no-reflect` | No | off (false) | Escape hatch: skip both reflect gates (pre-reflect sign-off + templated post-reflect task). Set automatically by `--dry-run`. |
| `--unattended` | No | off (false) | Worker mode for a coordinator; applies only as a standalone argument token. Behaviour is in `## Unattended mode`; without it nothing changes. |
| `--report-dir <dir>` | No | -- | With `--unattended`: the directory that holds the worker contract and the nested contracts, instead of `--output`, never both. |

### TASKLIST_ROOT Auto-Derivation

When `--output` is not provided, `TASKLIST_ROOT` is derived from the roadmap content using this 3-step priority algorithm:

1. If the roadmap text contains a substring matching `.dev/releases/current/<segment>/` (first match), use that as `TASKLIST_ROOT`.
2. Else if the roadmap text contains a version token matching `v<digits>(.<digits>)+` (first match), set `TASKLIST_ROOT = .dev/releases/current/<version-token>/`.
3. Else fallback: `TASKLIST_ROOT = .dev/releases/current/v0.0-unknown/`.

## Input Validation

Before invoking the skill, the command validates all inputs. On any validation failure, the command emits an error and exits without invoking the skill. No partial output is written.

**Error format** (2 fields):

```text
error_code: <category string>
message: <human-readable description with corrective action>
```

**Validation checks:**

1. **Roadmap file exists and is readable**: `<roadmap-path>` resolves to a readable, non-empty file. Reject 0-byte or whitespace-only files.
   - Error: `error_code: EMPTY_INPUT` / `error_code: MISSING_FILE`
2. **Spec file exists (if provided)**: `--spec` path resolves to a readable file.
   - Error: `error_code: MISSING_FILE`
3. **Output parent directory exists (if provided)**: `--output` parent directory exists and is writable.
   - Error: `error_code: MISSING_FILE`
4. **TASKLIST_ROOT derivation succeeds (if --output not provided)**: The 3-step derivation algorithm produces a valid path.
   - Error: `error_code: DERIVATION_FAILED`

## Activation

**Classification**: STRICT -- multi-file generation operation with compliance tier integration.

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:tasklist-protocol

Pass the following context:

- Roadmap text: full content of the roadmap file
- Spec text (if provided): full content of the spec file
- Output directory: resolved TASKLIST_ROOT path

Do NOT attempt to generate the tasklist using only this command file.
The full generation algorithm is in the protocol skill.

## Examples

```bash
# Basic: generate tasklist from a roadmap
/sc:tasklist @.dev/releases/current/v2.0/roadmap.md

# With supplementary spec context
/sc:tasklist @roadmap.md --spec @specs/auth-system-prd.md

# Explicit output directory
/sc:tasklist @roadmap.md --output .dev/releases/current/v2.1/tasklist/

# Full invocation with all options
/sc:tasklist @.dev/releases/current/v3.0/roadmap.md --spec @specs/v3-prd.md --output .dev/releases/current/v3.0/tasklist/
```

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:tasklist` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** Exactly one of `--output <output-dir>` or `--report-dir <dir>`; both, or neither, is refused before any work and the refusal is printed in chat only. `--report-dir` follows the path rules of `--output`, and with `--report-dir` the bundle's `TASKLIST_ROOT` is derived as today. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is the path of `tasklist-index.md` in the tasklist output directory, never a bare file name. `artifacts` lists every validation file the run wrote (`validation/ValidationReport.md`, `validation/gate-results.txt`, and `validation/PatchChecklist.md` when corrections were needed), the phase files and the nested contracts; paths git ignores are left out (WC-4).
- **Person-mode flags.** None is refused. `--no-reflect` still skips Stage 10.5.
- **Gates.** Under `--unattended` the unresolved High or Medium HALT resolves as blocked, with the open blocking findings in `blocked_question`; the `needs_human_decision` HALT resolves as blocked too, with that item in `blocked_question`. There is no other gate.
- **Nested invocations.** Stage 9 passes `--compliance strict --unattended --report-dir <report-dir>/nested/task-<n>/` to every `sc:task` call, the Stage 10 loop-back re-entries included (`<n>` counts every call, from 1, never reused), and the Stage 9 gate reads each nested `sc:task` worker contract by the nested-result rule of `~/.claude/WORKER-CONTRACT.md`. Stage 10.5 passes `--unattended --output <report-dir>/nested/reflect-<n>/` to each reflect call (`<n>` in phase order, from 1) in place of `TASKLIST_ROOT/validation/reflect-pre/phase-<P>/`, so the reflect headless rule applies, and `validation/ValidationReport.md` cites those directories. Every nested contract is listed in `artifacts`, also when the call failed. Without `--unattended` Stage 10.5 is unchanged.
- **Outward actions.** It pushes, commits and stages nothing; no Python module or `superclaude tasklist` CLI behaviour changes.

## Boundaries

**Will:**

- Parse and validate input arguments
- Derive TASKLIST_ROOT from roadmap content
- Invoke the skill with validated context
- Report generated file paths on completion
- Validate generated tasklist against source roadmap (via skill stages 7-10)
- Produce validation artifacts in TASKLIST_ROOT/validation/

**Will Not:**

- Execute the generation algorithm (that is the skill's job)
- Modify source roadmap files
- Run `superclaude sprint run` (output is compatible; invocation is separate)
- Generate anything beyond the tasklist bundle and validation artifacts
