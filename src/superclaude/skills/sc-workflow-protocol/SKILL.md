---
name: sc:workflow-protocol
description: "Behavioral protocol for /sc:workflow — PRD/spec to phased tasklist (<id>.md)"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Skill, mcp__codegraph__codegraph_status, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_callees, mcp__codegraph__codegraph_impact
argument-hint: "<path-or-prompt> [--strategy systematic|agile|enterprise] [--depth quick|standard|deep] [--handoff none|design|implement|tasklist]"
---

<!-- Extended metadata (for documentation, not parsed):
mcp-servers: [codegraph]
-->

# /sc:workflow protocol

Invoked only via `/sc:workflow` Activation. Plan only. Wave 2 is **Synthesize**.

## Execution vocabulary

| Verb | Tool |
|------|------|
| Load ref | Read |
| Write artifact | Write |
| Invoke Skill | Skill (`sc:reflect-protocol` in Wave 4; `sc:implement-protocol` only on `--handoff implement`) |
| Codegraph lookup | `mcp__codegraph__codegraph_<tool>` (exact names), only when `index_state` is `fresh` |

## Codegraph grounding

Rules, the closed `graph:*` token list and the caller-row, cap and read-before-cite rules are in `~/.claude/CODEGRAPH.md` (section 2 readiness, section 3 tokens, sections 5 and 6 rules, caps and `shown/total`). This protocol points there and copies none of it.

- **One readiness check per run.** Step 0 of Wave 1 (the package exists, before any lookup) runs section 2 of the guide once. It records `index_state`, `checked_at`, `worktree_root`, `projectPath`, the access mode and any `graph:*` token under `## Run state` in `<pkg>/artifacts/codegraph-grounding.md`. Later waves read that record and never run the check again.
- **Fresh only.** Codegraph runs only when `index_state` is `fresh` and its lookup tools are listed, with `projectPath` on every call. In any other state, or when a lookup fails or returns nothing, that step uses Grep, Glob and Read (the permanent floor, normal evidence) and the matching `graph:*` token goes into the grounding note. This never stops the run, fails the gate or changes the package status.
- **Rows are leads.** A graph row locates code and is not a citation: Read the range before a task names it. A caller row gives the caller's definition, so a task says "calls X" only after the call site is confirmed under guide section 5; otherwise it names the caller as a dependent. An empty answer never means "no callers".

| Step | Job | Codegraph tool when fresh | Floor |
|------|-----|---------------------------|-------|
| Wave 1, step 0 | Readiness check | `codegraph_status {projectPath}` | guarded CLI `status` per the guide, else the floor |
| Wave 1 | Resolve the files and symbols the source names; outline each named file | `codegraph_search {query, kind?, limit}`, `codegraph_node {file, symbolsOnly:true}`, and for an area overview `codegraph_files {format:"grouped", maxDepth:2}` (outside `allowed-tools`: called only when the session lists it, else Glob) | Glob, Grep for definitions, Read |
| Wave 2 | Body of each changed symbol; real callers and dependents; blast radius | `codegraph_node {symbol, file?, includeCode:true}`, `codegraph_callers {symbol, file?, limit}`, `codegraph_callees`, `codegraph_impact {symbol, depth:1}` | Grep with a word-boundary pattern, then Read each site |
| Wave 4 pre-check | The same lookups, read-only | the same tools | the same floor |

- **Sub-agent briefs.** Any brief this protocol writes for a sub-agent carries `index_state`, `checked_at`, `worktree_root` and the `projectPath` to pass; the receiver calls codegraph only when `index_state: fresh`, otherwise Grep and Read. The Wave 4 `/sc:reflect --mode pre` call takes flags only, so it cannot receive that state: reflect runs its own readiness check, which this run does not count as a second one.
- **Artifact.** `<pkg>/artifacts/codegraph-grounding.md` has the sections `## Run state`, `## Resolved symbols`, `## Dependents` and `## Pre-check`. It is a file this run wrote, so under `--unattended` it is listed in `artifacts` by the rule "every other file the run wrote" in the `## Unattended mode` section of the `workflow` command file. It adds no plan field and no contract key.

## Wave 0 — Parse

**Ref:** `refs/input-parse.md`

Entry: `$ARGUMENTS`. Validate all input and flags first (`--output` is retired → `E-LEGACY`); only then create the exclusive package `.dev/tasks/to-do/<id>/` and write the `source.md` snapshot (every source, file or prompt). Exit: source snapshot, flags, package `<pkg>`.

STOP codes in the ref. No package, no plan file, no yaml on a pre-creation STOP.

`.dev/tasks/` is always staged (`git add .dev/tasks`): the package and its `artifacts/` included. Never gitignore it, never leave it untracked, and never write "never stage" about it in a generated plan (Constraints included). Staging is not committing.

Under `--unattended` that staging is deferred to the coordinator (`~/.claude/WORKER-CONTRACT.md`): this run does not stage `.dev/tasks`. Also apply the `## Unattended mode` section of the `workflow` command file: the installed copy `~/.claude/commands/sc/workflow.md`, or the project copy `.claude/commands/sc/workflow.md`.

`--strategy enterprise` and omitted `--depth` → set `deep` + INFO.

## Wave 1 — Structure

**Ref:** `refs/phase-templates.md`

Entry: readable source. Exit: phase list with Goal/Inputs/Outputs/Checkpoint/deps.

Step 0 (once per run): the codegraph readiness check of `## Codegraph grounding`; then resolve the files and symbols the source names (codegraph when fresh, else Glob, Grep and Read) and record them under `## Resolved symbols` in `<pkg>/artifacts/codegraph-grounding.md`.

If nothing actionable → STOP `E-NO-PHASES`.

Depth caps phase count (quick 2–4, standard 4–8, deep 6–12).

## Wave 2 — Synthesize

Write `<pkg>/<id>.md` (the full package directory basename + `.md`, e.g. `TASK-WF-authLogin-20261001-063000.md`; never `plan.md`) from the bundled `refs/00_mdtm_template_simple_task.md`: Read it from this skill's directory and follow the rules in its HTML comment, then remove the comment and unused placeholders. Frontmatter keys (schema `workflow-plan/1.2`, `slug` = package id, `source: ./source.md`) and fill rules: `refs/quality-gates.md`.

Each Wave 1 phase → `## Phase N:` then its `## Task N:` headings (numbered 1..N across the plan). Phase Inputs → files/sections named in the task body; Outputs → the body and `Acceptance criteria:` of the task that produces each one (every Output lands in some task); Checkpoint → the last task's `Acceptance criteria:`; deps → `Depends on: Task K`.

Ground each task in the real code: its body names the real files and symbols it changes (repo-relative), and its `Acceptance criteria:` name the real callers and dependents that must keep working or be updated (recorded under `## Dependents` of the grounding artifact; codegraph when fresh, else Grep and Read). Size and order tasks by blast radius: a symbol with many dependents gets its own task, the tasks that update its dependents follow it with `Depends on: Task K`, and a change reaching more files than one task can hold is split, still within the depth cap.

`source.md` MUST already exist from Wave 0 (snapshot of the file or the inline prompt) before `<id>.md` is written.

## Wave 3 — Gate

**Ref:** `refs/quality-gates.md`

quick = schema-min. standard/deep = full. Fail → STOP `E-GATE`.

## Wave 4 — Reflect

**Pre-check (advisory, before the reflect call).** For each task, confirm that the files it names exist, its symbols resolve and its listed dependents are real, and list dependents of the touched symbols that no task names (codegraph when fresh, else Grep, Glob and Read; no new readiness check). Write the result under `## Pre-check` in `<pkg>/artifacts/codegraph-grounding.md` and print a one-line count with the plan path. It never edits `<id>.md` and never changes `status`; a failure of this step is only a `graph:*` note.

Final step of plan generation; runs only after Wave 3 passed, and **before** the Wave 5 contract and any `--handoff` (so an unreflected plan is never implemented). Invoke `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` via Skill (`sc:reflect-protocol`), defaults for every other flag, no `--remediate`. Record reflect's `status` and `report_path` (from its `return-contract.yaml`) as `reflect_status` / `reflect_report_path`, and print both with the plan path.

Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRACT.md`) that call passes `--unattended --output <report-dir>/nested/reflect-<n>/` (reflect's own directory flag; workflow's `--output` stays retired; `<n>` counts from 1 and is never reused), still without `--remediate`, and the nested contract is listed in `artifacts`, also when the call failed.

Advisory and read-only: never edit, delete, or regenerate `<id>.md` from findings, and never change the workflow `status` because of them. Reflect unavailable or `failed` → `reflect_status: skipped|failed`, `reflect_report_path: null`, one `unresolved` line; still proceed to Wave 5.

## Wave 5 — Contract

**Refs:** `refs/return-contract.md`, `refs/overlap-routing.md`

Write `<pkg>/return-contract.yaml` (contract 1.1: stable `slug`, `./<id>.md`, `./source.md`, `reflect_*`) **before** any `implement` handoff. Apply handoff; a failed `implement` handoff on a valid plan is `partial`, a failed generation is `failed`.

After an `implement` handoff the package may have moved to `done/` (executor-owned archive). Resolve the actual location by id (`.dev/tasks/to-do/<id>` vs `.dev/tasks/done/<id>`, `test -e || test -L`): only if the package still exists at `to-do/` may you rewrite the contract (e.g. to `partial`), and never recreate a directory or write into a path whose package is absent. Only `done/` exists → leave the archived contract untouched, report the failure/outcome in chat, print the actual `done/` plan path. Both exist → mutate neither and report the conflict. Print the plan path at its actual location.

## Will / Will Not

**Will:** one new package `.dev/tasks/to-do/<id>/` with `<id>.md`, `source.md`, `return-contract.yaml`; ground the plan in the real code through codegraph when the index is fresh. Never overwrites or reuses an existing package. Run `/sc:reflect --mode pre` (advisory) on the gated plan as the final generation step, before any handoff.

**Will Not:** product code, tasklist files, roadmap CLI, new agents, Task fan-out; modify the plan from reflect findings.
