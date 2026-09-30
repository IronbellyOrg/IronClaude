---
title: sc:workflow v3 — command + skill + refs
type: component
source: merged-requirements.md
created: 2026-09-30
---

# Design spec: `/sc:workflow` v3

## 1. Intent

Split the monolith `src/superclaude/commands/workflow.md` into the three-tier SuperClaude layout. Product remains a **plan**, not an executor and not a sprint CLI.

```
/sc:workflow <path|prompt>  →  Skill sc:workflow-protocol
                            →  .dev/workflow/<slug>/plan.md
                            +  return-contract.yaml
```

SoT for requirements: `merged-requirements.md` (FR-001–017). This spec maps those FRs to files and waves.

## 2. Files to add/change

| Action | Path |
|--------|------|
| Rewrite | `src/superclaude/commands/workflow.md` |
| Add | `src/superclaude/skills/sc-workflow-protocol/SKILL.md` |
| Add | `refs/input-parse.md` |
| Add | `refs/phase-templates.md` |
| Add | `refs/overlap-routing.md` |
| Add | `refs/quality-gates.md` |
| Add | `refs/return-contract.md` |
| Add | one small test under `tests/` that greps Activation + five refs + no Execute step |
| Sync | `make sync-dev` (do not git-add `.claude/` mirrors) |

Do **not** add agents, Python CLI, MDTM forks, or MCP server entries.

## 3. Command (interface only)

Copy the shape of `src/superclaude/commands/implement.md`.

```
/sc:workflow <path-or-prompt>
             [--strategy systematic|agile|enterprise]
             [--depth quick|standard|deep]
             [--output DIR]
             [--handoff none|design|implement|tasklist]
```

Defaults: strategy=`systematic`, depth=`standard` (enterprise+omitted depth → `deep`), handoff=`none`, output=`.dev/workflow/<slug>/`.

`## Activation` MUST invoke `Skill sc:workflow-protocol` before any wave.

Banned (STOP `E-LEGACY`): `--parallel`, `--validate`, `--depth shallow|normal`.

Command file 80–150 lines. No wave steps in the command.

STOP (skill Wave 0, codes in `refs/input-parse.md`):

| Code | When |
|------|------|
| `E-NO-SOURCE` | no path and no prompt, or two file tokens |
| `E-EMPTY-SOURCE` | whitespace-only source |
| `E-BAD-FLAG` | unknown enum |
| `E-OUTPUT-PATH` | `--output` not under `.dev/workflow/` |
| `E-MISSING-DIR` | `--output` parent missing |
| `E-LEGACY` | banned tokens above |
| `E-GATE` | Wave 3: plan missing required headings or zero phases |
| `E-NO-PHASES` | Wave 1 extracted nothing actionable from source |

Overwrite: same slug rewrites `plan.md` in place (no resume). Hash8 on inline prompts avoids most collisions.

## 4. Skill waves

```
Wave 0 Parse       refs/input-parse.md
Wave 1 Structure   refs/phase-templates.md
Wave 2 Synthesize  write plan.md (schema in quality-gates.md)
Wave 3 Gate        refs/quality-gates.md
Wave 4 Contract    refs/return-contract.md + overlap-routing.md
```

`allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Skill`
No `Task` (no fan-out). Bash: mkdir/existence of output dir only. Writes only under `.dev/workflow/` (or `--output` under that root). SKILL.md ≤ ~500 lines.

## 5. plan.md

Frontmatter: `schema: workflow-plan/1.0`, source, strategy, depth, slug.
Headings from `src/superclaude/templates/workflow/03_project_plan_template.md`: Goal, Context, Phases (Goal, Inputs, Outputs, Checkpoint, deps). Not MDTM checklists.

## 6. Overlap

| Neighbor | Workflow does | Workflow does not |
|----------|---------------|-------------------|
| implement | `--handoff implement` → Skill | write product code |
| tasklist | print how to run `/sc:tasklist` on a **roadmap** | invoke on plan.md; emit tasklist files |
| roadmap | INFO if source already looks like a roadmap | run `superclaude roadmap` |
| design | print `/sc:design @plan.md` | invoke design |

## 7. Sequence diagram

```
User → command.md (parse flags / STOP)
     → Skill sc-workflow-protocol
        → W0 parse
        → W1 structure
        → W2 write plan.md
        → W3 gates
        → W4 yaml + handoff
     → user
```

## 8. Test

One pytest: read command + skill tree from `src/superclaude/`. Assert Activation string, five ref files exist, command has no `**Execute**` behavioral step, `mcp-servers: []` or omitted.

## 9. Out of scope

Resume, ledger, deps.yaml, Task fan-out, new agents, Magic/Playwright/Morphllm/Serena-required, `claudedocs/`, `--spec/--prd` aliases.
