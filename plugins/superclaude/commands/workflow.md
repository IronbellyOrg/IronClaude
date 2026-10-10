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
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `<path>` / `<prompt>` | required xor | File or inline prompt |
| `--strategy` | `systematic` | `systematic` \| `agile` \| `enterprise`. Enterprise + omitted depth → `deep` |
| `--depth` | `standard` | `quick` \| `standard` \| `deep` |
| `--handoff` | `none` | `none` / `design` / `tasklist` = text; `implement` = Skill invoke |

Banned (`E-LEGACY`): `--parallel`, `--validate`, `--depth shallow|normal`, and the retired `--output` (every plan goes to a new `.dev/tasks/to-do/<id>/` package; there is no destination override).

## Behavioral Summary

Command file: parse flags → STOP on empty/banned → Activation. Protocol owns waves. Final generation step (after the gate, before any handoff): advisory `/sc:reflect --mode pre` of the plan against the source; its report path/status is printed and recorded in `return-contract.yaml`.

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:workflow-protocol

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in `src/superclaude/skills/sc-workflow-protocol/SKILL.md`.

## Examples

```bash
/sc:workflow docs/prd.md --strategy systematic --depth standard
/sc:workflow "add logout to the header" --handoff none
```

## Boundaries

**Will:** create one new package `.dev/tasks/to-do/<id>/` holding `<id>.md` (schema `workflow-plan/1.2`), `source.md` snapshot and `return-contract.yaml` (1.1). Never overwrites an existing package. Run `/sc:reflect --mode pre` (advisory, read-only on the plan) as the last plan-generation step, before any `--handoff`.

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
