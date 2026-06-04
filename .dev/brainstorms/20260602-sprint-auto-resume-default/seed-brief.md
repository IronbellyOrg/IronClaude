---
topic: "Make resume the default for `sprint run`: no flags required; the pipeline determines where the previous run was interrupted and runs as if the correct --start/--end (and per-task) options were supplied — analogous to /task auto-resume."
domain: architecture
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-06-02
---

# Seed Brief: sprint-auto-resume-default

## Problem Statement

Resuming an interrupted sprint is fully manual today. `superclaude sprint run <index>`
has no awareness of any prior run; the operator must read the halt message and retype
`--start N --end M` by hand (`cli/sprint/commands.py:190-291`, `models.py:677-684`). The
HALT output even advertises aspirational `--resume <task>`/`--budget <N>` flags that are
not real CLI options (`models.py:844-898`) — a usability gap the user wants closed.

The goal: running bare `superclaude sprint run <index>` (and bare `superclaude sprint
rerun-tasks <index>`) should auto-detect the interruption point from on-disk state and
execute as if the operator had supplied the correct options — mirroring how `/task`
auto-resumes an MDTM file with no extra arguments.

## Known Context (grounded in code)

- **Resume is 100% manual today.** `--start` defaults to `1`, `--end` to `0` (= last
  phase). The executor loops `for phase in config.active_phases` with no state inspection
  (`executor.py:1239`; `models.py:550-553`). No `--resume`/`--from`/`--auto` flag exists.
- **The resume signal is already persisted, just unread:**
  - `results/execution-log.jsonl` — chronological `phase_start` / `phase_complete` events
    with status (`logging_.py:61-107`).
  - `results/phase-N-result.json` — written *only* at phase completion (`executor.py:1304`,
    `:1612`); presence ⇒ phase done. Carries `task_results[]` (per-task status) +
    `recovery_history[]` (`executor.py:2053-2072`).
  - Phase transcripts (`phase-N-output.txt`) — already classifiable by the v4.3.0 rerun
    engine via `_classify_transcript` / `discover_failed_tasks_from_transcripts`
    (`rerun_tasks.py:550-640`).
- **Per-task status vocabulary exists:** `TaskStatus = {pass, fail, fail_recoverable,
  incomplete, skipped}` (`models.py:45-52`). `PhaseStatus` covers the lifecycle incl.
  `HALT`, `TIMEOUT`, `ERROR`, `PASS_MISSING_CHECKPOINT` (`models.py:270-293`).
- **No resume cursor on hard crash.** If the process dies mid-phase, no
  `phase-N-result.json` is written; the only trace is a `phase_start` with no matching
  `phase_complete`. There is no incremental "currently executing phase N, task T04.7"
  breadcrumb.
- **rerun-tasks already has the surgical machinery:** per-task re-execution, merge-back
  that refreshes canonical per-task status, and a content-SHA staleness guard
  (`_content_sha256_excluding_rerun_block`, `rerun_tasks.py:688-701`) that strips the
  `<!-- SUPERCLAUDE-RERUN -->` block before hashing. But `rerun-tasks` still *requires*
  explicit `--phase` (`commands.py:515-522`).
- **The `/task` analogy = "file is the state machine":** frontmatter `status` selects
  *which* task, checkbox `[x]/[ ]` locates *where*, first unchecked is the resume point,
  completed work is never re-run, and **ambiguity ⇒ list and ask, never auto-pick**
  (`skills/task/SKILL.md:50-56,86-104,282-291`).

## Constraints

- **C1 — Sprint phases are NOT idempotent** (unlike `/task` checkboxes). The resume seam
  must be actively verified, not blindly trusted.
- **C2 — Runs are expensive** (subprocess + tmux + real token cost). The auto-resume
  decision must be visible (print the inferred plan) and must avoid needless full-phase
  redos.
- **C3 — Reuse, don't reinvent.** Build on the v4.3.0 rerun engine's classifiers, per-task
  status, merge-back, and SHA-guard rather than parallel implementations.
- **C4 — Staleness must be semantic, not brittle.** A trailing-whitespace edit must not
  force a phase redo; drift detection is a *confidence assessment* with a ≥0.8 gate, ideally
  diffed against the git remote.
- **C5 — Backward compatible.** Explicit `--start`/`--end` must still work and must
  suppress auto-detect; auto-resume is the *default* only when those are omitted.

## Success Criteria (from user decisions)

- **S1 — No-arg auto-resume is the default** for `sprint run` AND `sprint rerun-tasks`.
- **S2 — Detect → print plan → proceed** by default (not silent, not confirm-gated) in the
  clean case; `--fresh`/`--no-resume` forces a clean run.
- **S3 — Resume-boundary integrity gate:** before resuming,
  (a) the **last confirmed-completed task** is deeply re-validated *with suspicion*, and
  (b) the **next unfinished task** is assumed partially done — half-finished artifacts are
  cleaned up or at least assessed. On a no-per-task-data crash, the phase is re-run but
  half-finished work is assessed/cleaned first.
- **S4 — Staleness assessment:** rescan tasklist, compare against completed work, ideally
  `git diff` vs remote, produce a safety-confidence score; ≥0.8 ⇒ prompt user then go;
  <0.8 ⇒ refuse silent resume and require explicit `--start`/`--fresh`.
- **S5 — Disambiguation:** if the resume point cannot be determined unambiguously, list
  candidates and require an explicit flag — never guess on an expensive run.

## Open Questions (carried into requirements)

- OQ1: Source of the resume cursor — derive purely from existing artifacts, or add a
  lightweight pre-phase breadcrumb to survive hard crashes? (Leaning: derive + emit a
  `phase_start` breadcrumb that already mostly exists.)
- OQ2: What exactly constitutes "doubly validated" for the last completed task — checkpoint
  re-verification, deliverable existence, or an LLM coherence pass?
- OQ3: How is "half-finished artifact cleanup" scoped safely (git stash vs. quarantine dir
  vs. report-only)?
- OQ4: Should the drift confidence assessment be a deterministic heuristic, an LLM judgment,
  or hybrid?

## Enrichment Context

Grounding performed via three parallel codebase sweeps (Explore agents) over
`cli/sprint/` (`commands.py`, `config.py`, `models.py`, `executor.py`, `recovery.py`,
`rerun_tasks.py`, `logging_.py`, `checkpoints.py`) and `skills/task/SKILL.md`. Full
findings inlined above. No external research required — this is a closed-world feature on
an existing codebase the team owns.
