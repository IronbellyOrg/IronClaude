# Pipeline Layouts and Resume Idioms

Reference for the `crash-recovery` skill. Each pipeline has a distinct artifact layout and a canonical resume command or default auto-resume idiom. The skill's synthesis report should map detected state to one of these and emit the right recovery command.

A project can have multiple of these in flight simultaneously. Do not assume a single "active" pipeline — enumerate every layout that has recent activity.

## PRD pipeline (Product Requirements Documents)

**Created by:** `task-builder` skill, `/sc:pm`, or manual.
**Layout:**

```text
.dev/tasks/to-do/TASK-PRD-<timestamp>/
├── TASK-PRD-<timestamp>.md       # MDTM task file with checklist + frontmatter
├── BUILD-REQUEST*.md             # original prompt
└── research/                     # optional, parallel research notes
```

**Status signal:** YAML frontmatter `status:` field. Values: `🟢 Done`, `🟡 InProgress`, `🔴 Blocked`, `⚪ ToDo`.
**Recovery:** if `status: 🟡 InProgress`, re-invoke the `task` skill on the same file. It picks up at the first unchecked item.

```bash
# Resume idiom
# (from project root)
/sc:task .dev/tasks/to-do/TASK-PRD-<timestamp>/TASK-PRD-<timestamp>.md
```

If `status: 🟢 Done` but file is still in `to-do/`, the only thing left is the move:

```bash
mv .dev/tasks/to-do/TASK-PRD-<ts> .dev/tasks/done/
```

## TDD pipeline (Technical Design Documents)

**Created by:** `tdd` skill, often fed from a completed PRD.
**Layout:** identical to PRD but `TASK-TDD-<timestamp>/`. Frequently has a much larger `research/` subdir (10–20+ research notes per topic).
**Status signal:** same frontmatter `status:` field.
**Recovery:** same `/sc:task` idiom. If individual research notes are stubbed (file < 200 bytes or has frontmatter `status: stub`), they're regenerable independently — but check the task's checklist first.

## Spec / Tech Reference / Tech Research

**Created by:** `tech-research`, `tech-reference`, or various sc commands.
**Layout:**

- `.dev/research/<topic-slug>/` — multi-file research bundles, often with `00-extraction.md`, `01-...`, etc.
- `claudedocs/` — finished tech references and analyses
- `.dev/research/research-results/` — aggregated results
**Status signal:** harder to read directly. Look for frontmatter, presence of a `synthesis.md` or `report.md`, and file mtimes. Auggie codebase-retrieval is useful here.
**Recovery:** typically re-invoke the original skill with the same prompt. There's no formal resume protocol — the work is regenerable.

## Roadmap pipeline (`superclaude roadmap run`)

**Created by:** `superclaude roadmap run <spec.md>` CLI.
**Layout:**

```text
docs/generated/<run-slug>/        # or .dev/research/roadmap-*/
├── .roadmap-state.json           # AUTHORITATIVE state — step-by-step progress
├── extraction.md
├── roadmap.md  (or roadmap-opus-architect.md, roadmap-haiku-architect.md)
├── diff.md
├── debate.md
├── verification.md
└── *.err / *.log                 # per-step error logs if a step failed
```

**Status signal:** `.roadmap-state.json` is the ground truth. Each step has a `status: pass | fail | pending` and an `attempts` counter. The CLI retries failed steps up to a limit, so `attempts >= max` means it gave up.
**Recovery:**

```bash
# Resumes from the first non-pass step.
superclaude roadmap run <original-spec.md> --output <same-output-dir> --resume
```

If a step is stuck failing with `attempts >= max`, inspect the `*.err` file for that step — usually a sub-agent silently producing nothing (e.g. haiku-architect captured a "no tools, summary only" instruction and never wrote the variant file).

**Validate after resume:**

```bash
superclaude roadmap validate <output-dir>
```

## Tasklist pipeline (`superclaude tasklist`)

**Created by:** `superclaude tasklist` from a roadmap.
**Layout:**

```text
.dev/releases/current/<release-slug>/
├── tasklist-index.md             # entry point — lists all phase files
├── phase-1-tasklist.md
├── phase-2-tasklist.md
├── ...
└── TASKLIST_ROOT/                # generated structure for sprint to consume
    └── checkpoints/              # CP-P01-END.md, CP-P02-END.md, ... (often missing)
```

**Status signal:** existence of phase files and checkpoint files. The presence of `tasklist-index.md` means generation succeeded; missing checkpoint files mean the sprint hasn't run yet (or got recovered from a different source).
**Recovery:** regenerate from the source roadmap if phase files are incomplete. The pipeline is deterministic given the same roadmap.

## Sprint pipeline (`superclaude sprint run`)

**Created by:** `superclaude sprint run <tasklist-index.md>` CLI — executes the multi-phase tasklist.
**Layout:**

```text
.dev/releases/current/<release-slug>/
├── manifest.json                 # checkpoint manifest, summary of expected files
├── execution-log.jsonl           # one event per phase: sprint_start, phase_complete
├── execution-log.md              # human-readable mirror
├── .sprint-exitcode              # last exit code (single number)
└── (the tasklist files above)
```

**Status signal:** `results/phase-N-result.json` is the authoritative completion signal: a present phase result with a PASS-family status means that phase finished. `execution-log.jsonl` corroborates progress, but a hard crash can tear the final ledger line. `.sprint-exitcode` mirrors the overall last sprint exit.
**Recovery:**

```bash
# Canonical resume command (v4.3.5+): bare run auto-detects the interrupted phase
# from on-disk state, prints the plan, asks for confirmation, and resumes there.
superclaude sprint run <release>/tasklist-index.md

# Unattended recovery: auto-confirm the detected plan.
superclaude sprint run <release>/tasklist-index.md --yes

# Or replay just one phase explicitly (bypasses auto-detection):
superclaude sprint run <release>/tasklist-index.md --start 6 --end 6

# Discard prior state and start clean (alias: --restart):
superclaude sprint run <release>/tasklist-index.md --fresh
```

Use `--yes` / `-y`, `SUPERCLAUDE_SPRINT_ASSUME_YES=1`, or `CI=1` for unattended/automated recovery.

**Prefer granular rerun when only a few tasks failed (v4.3.0+; auto-detect in v4.3.5+).** If the phase
mostly passed and only specific tasks failed — especially on a transient cause
(API outage, timeout) rather than a logic defect — suggest re-running just those
tasks instead of the whole phase. This re-executes only the named or auto-detected
tasks in an isolated bundle and merges results back into the canonical results + tasklist:

```bash
# Auto-detect the failed recoverable tasks, then merge back.
superclaude sprint rerun-tasks <release>/tasklist-index.md

# Or surgically re-run explicit failed tasks of a phase, then merge back.
superclaude sprint rerun-tasks <release>/tasklist-index.md --phase 7 --tasks T07.11,T07.12

# Preview the explicit plan first without mutating anything:
superclaude sprint rerun-tasks <release>/tasklist-index.md --phase 7 --tasks T07.11,T07.12 --dry-run
```

Inspect `phase-N-result.json` (per-task statuses) to identify which tasks to
nominate; tasks classified `fail_recoverable` (transient) are the usual
candidates. `--restore` recovers from a botched merge-back. When the WHOLE phase
must be redone, use the bare `sprint run` auto-resume command or pass an explicit
`--start/--end` window.

When a phase shows `status: error`, read the corresponding `phase-N-tasklist.md` to understand what was being attempted, and look for stderr in the JSONL `output_bytes` / `error_bytes` fields.

## Task (MDTM) — individual task files

**Created by:** `task-builder`, `tdd`, `prd`, or any of the *_TASK_ skills.
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

## Adversarial / Cleanup-Audit / Release-Split

These produce artifact bundles, not stateful pipelines. If found mid-run (e.g. `.dev/research/process-improvement-debate/` with only partial files), the safest recovery is to re-invoke the original skill — they're not designed for fine-grained resume.

## Resurrection contracts

**Location:** `.dev/resurrection-contracts/`
**Purpose:** explicit machine-readable contracts for restarting blocked work — a project-owned hand-off note. If one exists for the current state, prefer its instructions over generic resume idioms.

## Multi-initiative reality

A typical post-crash project has 3–7 of these in various states. Examples:

- One sprint that failed at phase 6
- Two PRD tasks in `to-do/` (one mid-progress, one untouched)
- A roadmap pipeline that ran fine yesterday
- A research bundle from last week sitting in `.dev/research/`
- A resurrection contract pinned for one specific blocked item

The recovery report must enumerate **all** of them. The user knows what they care about. Filtering down to one is wrong.
