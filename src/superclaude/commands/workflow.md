---
name: workflow
description: "Generate a phased implementation plan from a PRD, spec, or feature prompt"
category: orchestration
complexity: standard
mcp-servers: [context7, playwright, morphllm, serena]
personas: [architect, analyzer, frontend, backend, security, devops, project-manager]
argument-hint: "<path-or-prompt> [--strategy systematic|agile|enterprise] [--depth quick|standard|deep] [--output DIR] [--handoff none|design|implement|tasklist]"
---

# /sc:workflow — Implementation Plan Generator

Produces a **phased plan** (`plan.md`). Does not implement code and does not emit sprint tasklists.

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
             [--output DIR]
             [--handoff none|design|implement|tasklist]
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `<path>` / `<prompt>` | required xor | File or inline prompt |
| `--strategy` | `systematic` | `systematic` \| `agile` \| `enterprise`. Enterprise + omitted depth → `deep` |
| `--depth` | `standard` | `quick` \| `standard` \| `deep` |
| `--output` | `.dev/workflow/<slug>/` | Must stay under `.dev/workflow/` |
| `--handoff` | `none` | `none` / `design` / `tasklist` = text; `implement` = Skill invoke |

Banned (`E-LEGACY`): `--parallel`, `--validate`, `--depth shallow|normal`.

## Behavioral Summary

Command file: parse flags → STOP on empty/banned → Activation. Protocol owns waves.

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

**Will:** write `.dev/workflow/<slug>/plan.md` + `return-contract.yaml`.

**Will Not:** mutate product code; emit `tasklist-index.md`; run `superclaude roadmap`.

## Related Commands

| Command | Difference |
|---------|------------|
| `/sc:implement` | Executes a spec/plan |
| `/sc:tasklist` | Sprint bundle from a **roadmap** |
| `/sc:roadmap` | CLI spec → roadmap.md |
| `/sc:design` | Architecture spec |

## CRITICAL BOUNDARIES

Plan only. Next: `/sc:implement @plan.md` or `/sc:tasklist` on a roadmap.
