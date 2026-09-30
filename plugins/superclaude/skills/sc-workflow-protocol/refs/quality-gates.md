# Quality gates + plan schema

`plan.md` frontmatter MUST include:

```yaml
schema: workflow-plan/1.0
source: <path>
strategy: systematic|agile|enterprise
depth: quick|standard|deep
slug: <slug>
```

Body MUST have headings: `## Project Goal`, `## Project Context`, `## Phases` (same names as `03_project_plan_template.md`). Each phase: Goal, Inputs, Outputs, Checkpoint, deps.

## Schema-min (quick)

- frontmatter keys present
- ≥1 phase
- no MDTM checklist dialect (`- [ ]` task items as the phase body)

## Full (standard/deep)

Schema-min plus:

- every phase has Inputs and Checkpoint
- deps acyclic
- phase count within depth cap
- output paths not under `.claude/skills|agents|commands`

Fail any check → STOP `E-GATE`. Do not leave a partial `plan.md` claimed as success.
