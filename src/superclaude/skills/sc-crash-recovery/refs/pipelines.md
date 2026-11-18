# Pipeline Layouts and Resume Idioms

Reference for the `crash-recovery` skill. Each pipeline has a distinct artifact layout and a canonical resume command or default auto-resume idiom. The skill's synthesis report should map detected state to one of these and emit the right recovery command.

A project can have multiple of these in flight simultaneously. Do not assume a single "active" pipeline — enumerate every layout that has recent activity.

## Older task files (`TASK-*` from earlier releases)

**Created by:** the `task-builder` and `roadmap` skills of earlier releases (a task file `.dev/tasks/to-do/<TASK-ID>.md`, or a `TASK-ROADMAP-*` folder with `.roadmap-state.json`), run with `/task`. Those skills were removed in 6.1.0, so nothing resumes such a file by its old loop any more.
**Status signal:** YAML frontmatter `status:`; checklist items `- [ ]` (open), `- [x]` (done), `- [-]` (skipped); for a roadmap folder also `.roadmap-state.json`. Detect and report them as before.
**Recovery:** `/sc:implement` cannot import the old completion state: it lists every checkbox, checked or not, as a task and skips only tasks its own ledger shows complete. To finish an old file, copy its open items (`- [ ]`) into a new plain list and run `/sc:implement <that list>` (or plan them with `/sc:workflow`). This skill never deletes or moves such files.

## Workflow task packages (`TASK-WF-*`, `/sc:workflow` + `/sc:implement`)

**Created by:** `/sc:workflow` (one new package per generation). **Route to `/sc:implement`, never to MDTM `/task` or `/sc:task`.**
**Layout (scan BOTH locations):**

```text
.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>/   # in flight
.dev/tasks/done/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>/    # archived (finished)
├── <id>.md  source.md  return-contract.yaml              # <id>.md = tasklist named like the dir; workflow-plan/1.2, contract 1.1, ./ links
├── progress.md                                           # ledger — the state; no status: frontmatter
└── artifacts/                                            # task-owned evidence
```

**Status signal:** `progress.md` — `T<id>: complete verdict=…` lines, `FINAL:` and `ARCHIVE:` lines. Location is archive state: in `done/` = archived; in `to-do/` with every task complete = **archive-blocked**, not finished.
**Recovery:**

```bash
# resume or retry the archive gate (the same path works after a move: it reports the actual done/ path)
/sc:implement .dev/tasks/to-do/<id>/<id>.md   # <id> = TASK-WF-<camelSubject>-<YYYYMMDD>-<HHMMSS>[-N]
```

- Present in both `to-do/` and `done/` → conflict. Report it; do not merge, move or delete either copy.
- `<package>/.archiving` exists → a previous archive run was interrupted (maybe mid-move). Never delete it automatically and never infer the owner is dead from `FINAL:`/`ARCHIVE:` lines. After the operator confirms the original run has stopped: `uv run --no-project python <implement skill dir>/scripts/archive_workspace.py --root <checkout root> --package <package dir> --clear-marker <token in .archiving/owner>`.
- Archiving is Linux-only and fail-closed (`renameat2` no-replace; no `mv`/copy fallback). It implies no commit, PR or release.
- Runs created before this layout (`.dev/workflow/<slug>/plan.md`, `workflow-plan/1.1`, path-hashed `.dev/implement/<slug>/progress.md`) are preserved legacy runs: resume them with `/sc:implement <plan path>` as before; do not migrate them.

## Adversarial / Cleanup-Audit / Release-Split

These produce artifact bundles, not stateful pipelines. If found mid-run (e.g. `.dev/research/process-improvement-debate/` with only partial files), the safest recovery is to re-invoke the original skill — they're not designed for fine-grained resume.

## Resurrection contracts

**Location:** `.dev/resurrection-contracts/`
**Purpose:** explicit machine-readable contracts for restarting blocked work — a project-owned hand-off note. If one exists for the current state, prefer its instructions over generic resume idioms.

## Multi-initiative reality

A typical post-crash project has 3–7 of these in various states. Examples:

- One workflow task package whose `/sc:implement` run stopped at task 6
- Two PRD tasks in `to-do/` (one mid-progress, one untouched)
- A roadmap build that ran fine yesterday
- A research bundle from last week sitting in `.dev/research/`
- A resurrection contract pinned for one specific blocked item

The recovery report must enumerate **all** of them. The user knows what they care about. Filtering down to one is wrong.
