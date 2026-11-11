---
name: workflow
description: "Generate a phased implementation plan from a PRD, spec, or feature prompt"
category: orchestration
complexity: standard
mcp-servers: []
argument-hint: "<path-or-prompt> [--strategy systematic|agile|enterprise] [--depth quick|standard|deep] [--handoff none|design|implement|tasklist]"
---

# /sc:workflow — Implementation Plan Generator

Produces a **phased plan** (tasklist `<id>.md`, named exactly like its package directory) inside a new task package `.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>/` (`<subject>` = lower camelCase, max 16 chars, e.g. `authLogin`). Does not implement code and does not emit sprint tasklists.

## Triggers

Explicit: user types `/sc:workflow ...`, or another `/sc:*` command invokes `Skill sc:workflow-protocol`.

## Required Input

Exactly one source: an existing file path (`@path` ok) **or** leftover `$ARGUMENTS` as an inline prompt.

**STOP** `E-NO-SOURCE` on a bare `/sc:workflow`.

## Usage

```bash
/sc:workflow <path-or-prompt>
             [--strategy systematic|agile|enterprise]
             [--depth quick|standard|deep]
             [--handoff none|design|implement|tasklist]
/sc:workflow <path-or-prompt> --unattended --report-dir <dir>   # worker mode, see Unattended mode
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `<path>` / `<prompt>` | required xor | File or inline prompt |
| `--strategy` | `systematic` | `systematic` \| `agile` \| `enterprise`. Enterprise + omitted depth → `deep` |
| `--depth` | `standard` | `quick` \| `standard` \| `deep` |
| `--handoff` | `none` | `none` / `design` / `tasklist` = text; `implement` = Skill invoke |
| `--unattended` | off | Worker mode: no step waits for a person; see Unattended mode |
| `--report-dir` | none | With `--unattended`, the directory that holds the worker contract |

Banned (`E-LEGACY`): `--parallel`, `--validate`, `--depth shallow|normal`, and the retired `--output` (every plan goes to a new `.dev/tasks/to-do/<id>/` package; there is no destination override).

## Behavioral Summary

Command file: parse flags → STOP on empty/banned → Activation. Protocol owns waves. Final generation step (after the gate, before any handoff): advisory `/sc:reflect --mode pre` of the plan against the source; its report path/status is printed and recorded in `return-contract.yaml`.
The protocol runs one codegraph readiness check per run: a fresh index grounds the plan and that pre-check in the real code, otherwise Grep/Read do and the fallback is recorded.

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:workflow-protocol

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in `~/.claude/skills/sc-workflow-protocol/SKILL.md`.

## Examples

```bash
/sc:workflow docs/prd.md --strategy systematic --depth standard
/sc:workflow "add logout to the header" --handoff none
```

## Codegraph grounding

One codegraph readiness check per run, owned by the protocol (`~/.claude/CODEGRAPH.md` section 2, run at the start of Wave 1); this command never repeats it. Codegraph is used only when `index_state` is `fresh`. In any other state, or when a lookup fails, Grep, Glob and Read do the same job and the matching `graph:*` token is recorded in `<pkg>/artifacts/codegraph-grounding.md`. It never stops the run, fails the gate or changes the package status. `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` is honoured (`graph:disabled`).

| Step | Codegraph tool when fresh | Floor |
|------|---------------------------|-------|
| Wave 1, step 0 | `codegraph_status` (the readiness check) | guarded CLI `status`, else the floor |
| Wave 1 | `codegraph_search`, `codegraph_node` with `symbolsOnly:true`: resolve the files and symbols the source names | Glob, Grep, Read |
| Wave 2 | `codegraph_node` with `includeCode:true`, `codegraph_callers`, `codegraph_callees`, `codegraph_impact`: name real callers and dependents in tasks and acceptance criteria, order and size tasks by blast radius | Grep with a word-boundary pattern, then Read |
| Wave 4 pre-check | the same lookups, read-only | the same floor |

Under `--unattended` the same rules apply; no gate and no person-mode flag is added. The protocol (`~/.claude/skills/sc-workflow-protocol/SKILL.md`) holds the details.

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:workflow` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument (an inline prompt is a quoted argument); otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only; the retired `--output` stays `E-LEGACY`. Without `--report-dir` the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome, including each pre-creation STOP (`E-NO-SOURCE`, `E-EMPTY-SOURCE`, `E-BAD-FLAG`, `E-LEGACY`, `E-PACKAGE-COLLISION`), with the STOP code in `reason`. The package's own rule for those STOPs (no package, no yaml) is unchanged. Once a package exists, `artifacts` lists every other file the run wrote: the package's `return-contract.yaml`, its `source.md` when the snapshot was written, each file the reflect step wrote in its `<report-dir>/nested/reflect-<n>/` run directory (also when reflect failed), and `docs/memory/reflect/deviation-patterns-<slug>.md` when reflect wrote it; reflect's gitignored per-machine files (`.dev/reflect/runs.jsonl`, `.superclaude/memory/`) are left out (WC-4). `report_path` is the plan `<id>.md`. The package statuses success, partial and failed map to succeeded, partial and failed.
- **Handoff.** A `--handoff implement` is skipped (the implement executor accepts the flag only in a later phase) and recorded in the package contract as `partial` with one `unresolved` line. The `design` and `tasklist` handoffs are text and unchanged.
- **Gates.** None else, and no person-mode flag.
- **Nested invocations.** Under `--unattended` the Wave 4 reflect step receives `--unattended --output <report-dir>/nested/reflect-<n>/` (reflect's own directory flag; workflow's `--output` stays retired; `<n>` counts from 1 and is never reused), still without `--remediate`, and its contract is listed in `artifacts`, also when the call failed. A nested contract is read by the nested-result rule of `~/.claude/WORKER-CONTRACT.md`.
- **Outward actions.** The command does not stage `.dev/tasks` and leaves that to the coordinator; it pushes and commits nothing.

## Boundaries

**Will:** create one new package `.dev/tasks/to-do/<id>/` holding `<id>.md` (schema `workflow-plan/1.2`), `source.md` snapshot and `return-contract.yaml` (1.1). Never overwrites an existing package. Run `/sc:reflect --mode pre` (advisory, read-only on the plan) as the last plan-generation step, before any `--handoff`. Ground the plan in the real code through codegraph when the index is fresh.

**Will Not:** mutate product code; edit the plan from reflect findings; emit `tasklist-index.md`; run `superclaude roadmap`.

## Related Commands

| Command | Difference |
|---------|------------|
| `/sc:implement` | Executes a spec/plan |
| `/sc:tasklist` | Sprint bundle from a **roadmap** |
| `/sc:roadmap` | CLI spec → roadmap.md |
| `/sc:design` | Architecture spec |

## CRITICAL BOUNDARIES

Plan only. Next: `/sc:implement .dev/tasks/to-do/<id>/<id>.md` (not MDTM `/task`) or `/sc:tasklist` on a roadmap.
