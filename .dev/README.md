# `.dev/` — Development & Iteration Workspace

## Rule (canonical)

> **Workspaces, fixtures, harness code, and iteration outputs go under `.dev/`, never under `.claude/skills/`. Eval workspaces use `.dev/eval-workspaces/<skill-name>/`.**

This is the single source of truth for *where iteration artefacts live*. `.claude/skills/<skill>/` is reserved for the **distributable skill package** (the `SKILL.md` plus its `refs/`, `rules/`, `templates/`, `scripts/`). Anything generated *by* a skill's evaluation, debugging, or release workflow belongs here under `.dev/`.

The enforcement layers that depend on this rule:
- **L2 (this file)** publishes the convention.
- **L2 (`.gitignore`)** matches `.claude/skills/*-workspace/` so misplaced workspaces never get committed.
- **L3 (skill prerequisites)** refuses `.claude/skills/...`, `.claude/agents/...`, `.claude/commands/...` as output destinations and redirects callers here.

## Subdirectories

| Path | Purpose |
|---|---|
| `benchmarks/` | Captured baseline benchmark runs (e.g. `v2.20-baseline/`) used as regression references. |
| `evals/` | Per-skill evaluation runs and scored outputs (one directory per eval campaign). |
| `eval-workspaces/` | **Canonical workspace location for skill evaluations.** One subdir per skill: `.dev/eval-workspaces/<skill-name>/`. |
| `releases/` | Release planning, in-flight releases (`current/`), completed work (`archive/`), backlog (`backlog/`), and templates (`templates/`). |
| `research/` | Free-form research notes, decision memos, and analysis artefacts that inform design decisions. |
| `resurrection-contracts/` | Recovery contracts (gate definitions) used when an audit needs to re-execute against a known good state. |
| `tasks/` | MDTM task files — `done/` holds completed tasks; loose `*.md` files are in-flight or staged work. |
| `test-fixtures/` | Static input fixtures used by skill harnesses and evals (e.g. `test-prd-user-auth.md`) plus `results/`. |
| `test-sprints/` | Sprint CLI smoke-test bundles used to validate the sprint pipeline end-to-end. |

## Where things go — quick decision guide

| If you are creating… | Put it under… |
|---|---|
| A skill's eval workspace | `.dev/eval-workspaces/<skill-name>/` |
| A scored eval run | `.dev/evals/<campaign-name>/` |
| A static input fixture for a skill or harness | `.dev/test-fixtures/` |
| A baseline benchmark to compare against | `.dev/benchmarks/<version>/` |
| Release planning / roadmaps / tasklists | `.dev/releases/current/<release-name>/` |
| Research notes or a decision memo | `.dev/research/` |
| An MDTM task file | `.dev/tasks/` (move to `tasks/done/` when complete) |
| The skill itself (SKILL.md, refs, rules, templates) | `src/superclaude/skills/<skill-name>/` → synced to `.claude/skills/<skill-name>/` |

If you find yourself wanting to write to `.claude/skills/<skill>-workspace/` or any sibling under `.claude/`, stop — that path is gitignored and the L3 prerequisite guard will refuse it. Redirect to `.dev/eval-workspaces/<skill-name>/`.
