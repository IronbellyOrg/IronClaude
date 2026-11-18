# Pipeline Layouts and Resume Idioms

Reference for the `crash-recovery` skill. Each pipeline has a distinct artifact layout and a canonical resume command or default auto-resume idiom. The skill's synthesis report should map detected state to one of these and emit the right recovery command.

A project can have multiple of these in flight simultaneously. Do not assume a single "active" pipeline — enumerate every layout that has recent activity.

## Roadmap skill (`/roadmap`)

**Created by:** the `roadmap` skill (an MDTM roadmap composer; it builds phase task files with `task-builder`).
**Layout:**

```text
.dev/tasks/to-do/TASK-ROADMAP-<...>/
├── TASK-ROADMAP-<...>.md         # MDTM task file for the roadmap build
├── .roadmap-state.json           # input hash, roadmap status, build requests generated
├── ROADMAP-<PROJECT>.md          # the roadmap document
├── build-requests/               # BUILD_REQUEST-phase-NN-*.md
├── research/                     # research notes (research-notes.md has `Status:`)
└── qa/                           # QA reports
```

**Status signal:** the task file's checklist (`- [ ]` open, `- [x]` done) and `.roadmap-state.json`. `research/research-notes.md` with `Status: In Progress` means scope discovery was interrupted.
**Recovery:**

```bash
# The roadmap skill reads the task file and the state file and picks up at the first unchecked item.
/roadmap <original input>
# or resume the task file directly:
/task .dev/tasks/to-do/TASK-ROADMAP-<...>/TASK-ROADMAP-<...>.md
```

## Task (MDTM) — individual task files

**Created by:** `task-builder`, or any of the *_TASK_ skills.
**Layout:**

- `.dev/tasks/to-do/<TASK-ID>.md` or `.dev/tasks/to-do/<TASK-ID>/<TASK-ID>.md`
- `.dev/tasks/done/<TASK-ID>.md` for completed
**Status signal:** YAML frontmatter `status:`. Checklist items use `- [ ]` (open), `- [x]` (done), `- [-]` (skipped).
**Recovery:**

```bash
# task skill picks up at first unchecked item
/sc:task .dev/tasks/to-do/<TASK-ID>.md
# or natural-language: "resume the task at <path>"
```

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
