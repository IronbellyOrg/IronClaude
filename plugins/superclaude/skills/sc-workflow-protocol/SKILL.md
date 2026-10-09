---
name: sc:workflow-protocol
description: "Behavioral protocol for /sc:workflow — PRD/spec to phased tasklist (<id>.md)"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Skill
argument-hint: "<path-or-prompt> [--strategy systematic|agile|enterprise] [--depth quick|standard|deep] [--handoff none|design|implement|tasklist]"
---

# /sc:workflow protocol

Invoked only via `/sc:workflow` Activation. Plan only. Wave 2 is **Synthesize**.

## Execution vocabulary

| Verb | Tool |
|------|------|
| Load ref | Read |
| Write artifact | Write |
| Invoke Skill | Skill (`sc:reflect-protocol` in Wave 4; `sc:implement-protocol` only on `--handoff implement`) |

## Wave 0 — Parse

**Ref:** `refs/input-parse.md`

Entry: `$ARGUMENTS`. Validate all input and flags first (`--output` is retired → `E-LEGACY`); only then create the exclusive package `.dev/tasks/to-do/<id>/` and write the `source.md` snapshot (every source, file or prompt). Exit: source snapshot, flags, package `<pkg>`.

STOP codes in the ref. No package, no plan file, no yaml on a pre-creation STOP.

`--strategy enterprise` and omitted `--depth` → set `deep` + INFO.

## Wave 1 — Structure

**Ref:** `refs/phase-templates.md`

Entry: readable source. Exit: phase list with Goal/Inputs/Outputs/Checkpoint/deps.

If nothing actionable → STOP `E-NO-PHASES`.

Depth caps phase count (quick 2–4, standard 4–8, deep 6–12).

## Wave 2 — Synthesize

Write `<pkg>/<id>.md` (the full package directory basename + `.md`, e.g. `TASK-WF-authLogin-20261001-063000.md`; never `plan.md`) from `src/superclaude/templates/workflow/00_mdtm_template_simple_task.md`: follow the rules in its HTML comment, then remove the comment and unused placeholders. Frontmatter keys (schema `workflow-plan/1.2`, `slug` = package id, `source: ./source.md`) and fill rules: `refs/quality-gates.md`.

Each Wave 1 phase → `## Phase N:` then its `## Task N:` headings (numbered 1..N across the plan). Phase Inputs → files/sections named in the task body; Outputs → the body and `Acceptance criteria:` of the task that produces each one (every Output lands in some task); Checkpoint → the last task's `Acceptance criteria:`; deps → `Depends on: Task K`.

`source.md` MUST already exist from Wave 0 (snapshot of the file or the inline prompt) before `<id>.md` is written.

## Wave 3 — Gate

**Ref:** `refs/quality-gates.md`

quick = schema-min. standard/deep = full. Fail → STOP `E-GATE`.

## Wave 4 — Reflect

Final step of plan generation; runs only after Wave 3 passed, and **before** the Wave 5 contract and any `--handoff` (so an unreflected plan is never implemented). Invoke `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` via Skill (`sc:reflect-protocol`), defaults for every other flag, no `--remediate`. Record reflect's `status` and `report_path` (from its `return-contract.yaml`) as `reflect_status` / `reflect_report_path`, and print both with the plan path.

Advisory and read-only: never edit, delete, or regenerate `<id>.md` from findings, and never change the workflow `status` because of them. Reflect unavailable or `failed` → `reflect_status: skipped|failed`, `reflect_report_path: null`, one `unresolved` line; still proceed to Wave 5.

## Wave 5 — Contract

**Refs:** `refs/return-contract.md`, `refs/overlap-routing.md`

Write `<pkg>/return-contract.yaml` (contract 1.1: stable `slug`, `./<id>.md`, `./source.md`, `reflect_*`) **before** any `implement` handoff. Apply handoff; a failed `implement` handoff on a valid plan is `partial`, a failed generation is `failed`.

After an `implement` handoff the package may have moved to `done/` (executor-owned archive). Resolve the actual location by id (`.dev/tasks/to-do/<id>` vs `.dev/tasks/done/<id>`, `test -e || test -L`): only if the package still exists at `to-do/` may you rewrite the contract (e.g. to `partial`), and never recreate a directory or write into a path whose package is absent. Only `done/` exists → leave the archived contract untouched, report the failure/outcome in chat, print the actual `done/` plan path. Both exist → mutate neither and report the conflict. Print the plan path at its actual location.

## Will / Will Not

**Will:** one new package `.dev/tasks/to-do/<id>/` with `<id>.md`, `source.md`, `return-contract.yaml`. Never overwrites or reuses an existing package. Run `/sc:reflect --mode pre` (advisory) on the gated plan as the final generation step, before any handoff.

**Will Not:** product code, tasklist files, roadmap CLI, new agents, Task fan-out; modify the plan from reflect findings.
