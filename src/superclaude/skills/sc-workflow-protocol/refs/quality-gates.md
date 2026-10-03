# Quality gates + plan schema

The tasklist `<id>.md` (filename = full package directory basename + `.md`, including any collision suffix) frontmatter MUST include:

```yaml
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic|agile|enterprise
depth: quick|standard|deep
slug: <id>
version: "1"
priority: High|Medium|Low
created_date: "YYYY-MM-DD"
```

Field rules (outside the machine example; write values bare, never with trailing `#` comments): `source` is the package-relative snapshot, never the original absolute path. `slug` equals the package directory name, e.g. `TASK-WF-authLogin-20261001-063000`. `priority` is the source's own priority, else `Medium`; never inferred. `created_date` is today (UTC) from the session date; never invented.

Body = `00_mdtm_template_simple_task.md` shape: `# <title>`, `Source: ./source.md`, `Goal:`, optional `## Constraints`, `## Phase N:` group headings, `## Task N:` items with `Acceptance criteria:`.

Operational lookup fields and links are package-relative (`./…`) or repo-relative; none may embed an absolute path or an old `.dev/tasks/to-do/` prefix (the package later moves to `done/`). Quoting source text or forensic paths in prose is fine.

Delivery files named by tasks are repo-relative and canonical (`src/…`, `tests/…`). Task-owned evidence and generated outputs are written under `./artifacts/…` inside the package. Final verification belongs to the executor: no status field, no checkbox, no verification-only task.

## Schema-min (quick)

- frontmatter keys present; `schema` is exactly `workflow-plan/1.2`; `slug` equals the package directory name and matches `TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>[-2..-9]` with `<subject>` = `[a-z][A-Za-z0-9]{0,15}` (lower camelCase, max 16, no hyphens); the file is named exactly `<slug>.md`; `source` is `./source.md`; `priority` in enum; `created_date` is `YYYY-MM-DD`; `version` is a positive integer
- template comment and template 00 `[...]` placeholders removed
- ≥1 `## Task N:`; every Task has `Acceptance criteria:` with ≥1 bullet
- no checkbox (`- [ ]`, `- [x]`, `* [ ]`) or numbered (`1.`, `1)`) lines anywhere, fenced code included — `/sc:implement` enumerates them as tasks

## Full (standard/deep)

Schema-min plus:

- every `## Phase N:` has ≥1 Task before the next Phase
- Task numbers unique and contiguous from 1; `Depends on: Task K` only names a lower K
- phase count within depth cap
- output paths not under `.claude/skills|agents|commands`
- every source requirement is covered by at least one task (none silently dropped)

Fail any check → STOP `E-GATE`. A plan that fails the gate is deleted (the draft this run wrote, nothing else) and the package keeps `source.md` plus a `failed` contract; a failed package is never executable. Do not leave a partial `<id>.md` claimed as success.
