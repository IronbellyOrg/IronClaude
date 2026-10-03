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
| `tasks/` | MDTM task files — `done/` holds completed tasks; loose `*.md` files are in-flight or staged work. Also holds **workflow task packages** (`to-do/TASK-WF-*/`, `done/TASK-WF-*/`) — see [Workflow task packages](#workflow-task-packages). |
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
| A `/sc:workflow` plan (implementation tasklist) | Created for you as `.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>/`; `/sc:implement` moves it to `.dev/tasks/done/` after a fresh final review |
| The skill itself (SKILL.md, refs, rules, templates) | `src/superclaude/skills/<skill-name>/` → synced to `.claude/skills/<skill-name>/` |

If you find yourself wanting to write to `.claude/skills/<skill>-workspace/` or any sibling under `.claude/`, stop — that path is gitignored and the L3 prerequisite guard will refuse it. Redirect to `.dev/eval-workspaces/<skill-name>/`.

## Workflow task packages

`/sc:workflow` creates one **new** package per generation (it never overwrites one): `.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>/` (UTC; `<subject>` is lower camelCase, max 16 chars, e.g. `authLogin`; `-2`..`-9` suffix on a collision in `to-do/` or `done/`). The tasklist file is named exactly like the package directory plus `.md` (`TASK-WF-authLogin-20261001-063000.md`, collision suffix included). `--output` is retired — there is no destination override.

```text
.dev/tasks/to-do/TASK-WF-<id>/
├── <id>.md                # tasklist = directory basename + .md; schema workflow-plan/1.2, slug == directory name
├── source.md              # snapshot of the source (file or inline prompt)
├── return-contract.yaml   # contract 1.1, ./ package-relative links
├── progress.md            # added by /sc:implement (the ledger; state lives here)
└── artifacts/             # task-owned evidence/outputs added by /sc:implement
```

- **Run it with `/sc:implement`**, not MDTM `/task`: `/sc:implement .dev/tasks/to-do/<id>/<id>.md`. Delivery code, tests and docs stay in their canonical repo paths; only task evidence lives in `artifacts/`.
- **Completion.** After every task is complete, `/sc:implement` runs a fresh independent final review (every archive attempt, even for a one-task plan) and then a small helper moves the whole package to `.dev/tasks/done/<id>/`. No commit, PR, merge or release is implied.
- **Archiving is Linux-only and fail-closed.** It uses `renameat2(RENAME_NOREPLACE)`; on another OS, an unsupported filesystem/kernel, a cross-filesystem move or any existing destination it refuses and leaves the package in `to-do/` — it never falls back to `mv`/copy.
- **Interrupted archive.** An existing `<package>/.archiving` marker always stops the next run. After you confirm the original run has stopped, clear it explicitly with the helper's `--clear-marker <token>` (the token is in `.archiving/owner`); nothing reclaims it automatically.
- **Look in both places.** To find work, scan `.dev/tasks/to-do/TASK-WF-*/` (in flight) and `.dev/tasks/done/TASK-WF-*/` (finished). A package present in both is a conflict: stop and resolve it by hand.
- **Preserved legacy runs.** Plans generated before this layout (`workflow-plan/1.1`, `.dev/workflow/<slug>/`) and their path-hashed ledgers under `.dev/implement/` keep working unchanged; they are not migrated.
