---
name: sc:workflow-protocol
description: "Behavioral protocol for /sc:workflow — PRD/spec to phased plan.md"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Skill
argument-hint: "<path-or-prompt> [--strategy systematic|agile|enterprise] [--depth quick|standard|deep] [--output DIR] [--handoff none|design|implement|tasklist]"
---

# /sc:workflow protocol

Invoked only via `/sc:workflow` Activation. Plan only. Wave 2 is **Synthesize**.

## Execution vocabulary

| Verb | Tool |
|------|------|
| Load ref | Read |
| Write artifact | Write |
| Invoke Skill | Skill (`sc:implement-protocol` only on `--handoff implement`) |

## Wave 0 — Parse

**Ref:** `refs/input-parse.md`

Entry: `$ARGUMENTS`. Exit: source path, flags, output dir created.

STOP codes in the ref. No plan file on STOP.

`--strategy enterprise` and omitted `--depth` → set `deep` + INFO.

## Wave 1 — Structure

**Ref:** `refs/phase-templates.md`

Entry: readable source. Exit: phase list with Goal/Inputs/Outputs/Checkpoint/deps.

If nothing actionable → STOP `E-NO-PHASES`.

Depth caps phase count (quick 2–4, standard 4–8, deep 6–12).

## Wave 2 — Synthesize

Write `<run>/plan.md` using headings from `src/superclaude/templates/workflow/03_project_plan_template.md` (Goal, Context, Phases). Do not copy MDTM 00–02.

If source was an inline prompt, `source.md` MUST already exist from Wave 0.

## Wave 3 — Gate

**Ref:** `refs/quality-gates.md`

quick = schema-min. standard/deep = full. Fail → STOP `E-GATE`.

## Wave 4 — Contract

**Refs:** `refs/return-contract.md`, `refs/overlap-routing.md`

Write `return-contract.yaml`. Apply handoff. Print plan path.

## Will / Will Not

**Will:** plan.md + return-contract under `.dev/workflow/`.

**Will Not:** product code, tasklist files, roadmap CLI, new agents, Task fan-out.
