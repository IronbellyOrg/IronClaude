# Quality gates + plan schema

`plan.md` frontmatter MUST include:

```yaml
schema: workflow-plan/1.1
source: <path>
strategy: systematic|agile|enterprise
depth: quick|standard|deep
slug: <slug>
version: "1"
priority: High|Medium|Low     # the source's own priority, else Medium; never inferred
created_date: "YYYY-MM-DD"    # today (UTC) from the session date; never invented
```

Body = `00_mdtm_template_simple_task.md` shape: `# <title>`, `Source:`, `Goal:`, optional `## Constraints`, `## Phase N:` group headings, `## Task N:` items with `Acceptance criteria:`.

## Schema-min (quick)

- frontmatter keys present; `priority` in enum; `created_date` is `YYYY-MM-DD`; `version` is a positive integer
- template comment and template 00 `[...]` placeholders removed
- ≥1 `## Task N:`; every Task has `Acceptance criteria:` with ≥1 bullet
- no checkbox (`- [ ]`, `- [x]`, `* [ ]`) or numbered (`1.`, `1)`) lines anywhere, fenced code included — `/sc:implement` enumerates them as tasks

## Full (standard/deep)

Schema-min plus:

- every `## Phase N:` has ≥1 Task before the next Phase
- Task numbers unique and contiguous from 1; `Depends on: Task K` only names a lower K
- phase count within depth cap
- output paths not under `.claude/skills|agents|commands`

Fail any check → STOP `E-GATE`. Do not leave a partial `plan.md` claimed as success.
