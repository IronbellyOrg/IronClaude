# BUILD REQUEST — PR #124 merge-conflict resolution + PASS_RECOVERED correctness fix

## Goal

Produce a mergeable, **correct** resolution of PR #124
(`feat/sprint-auto-resume-v435` → `master`). This has two distinct deliverables
that MUST land together in the same merge:

1. **(A) Conflict resolutions** — resolve the 4 conflict hunks across 3 files so
   the branch merges cleanly into `master`.
2. **(B) Correctness fix** — widen the `resume/` package's task-level success
   checks from identity-against-`PASS` to the PASS-family predicate, because
   `master` introduced `TaskStatus.PASS_RECOVERED` (#126) underneath this branch.
   This fix lives in **non-conflicted files** — the textual merge will NOT
   surface it, but shipping without it merges a known crash-tail regression.

## Context / provenance (all verified non-destructively via `git merge-tree`)

- PR #124 branch: `feat/sprint-auto-resume-v435` (tip `aedd0104`).
- Base: `master` (tip `1a00efb2`). merge-base = `86c46321`.
- `mergeable: CONFLICTING`, `mergeStateStatus: DIRTY`.
- master advanced under the branch via **#120** (per-task handoff + `--task-parallelism`)
  and **#126** (`PASS_RECOVERED` per-task status). The branch predates both.
- Every resolution below was materialized into a temp file and `py_compile`-verified.

## Deliverable A — the 4 conflict hunks

### A1. `CHANGELOG.md` (one hunk, lines ~7–55) — **keep BOTH**
Both sides added a distinct `###` section under `## [Unreleased]`; pure additive.
Resolution: remove the 3 conflict markers, keep both sections. Recommend the
v4.3.5 auto-resume section placed above the #120 "wire the per-task execution
path" section (cosmetic ordering only).

### A2. `src/superclaude/cli/sprint/commands.py` (two hunks) — **union, with a required insertion**
- Hunk 1 (decorators, ~191–235): union of master's `--handoff/--no-handoff`,
  `--resume`, `--task-parallelism` options with PR's `--fresh`, `--restart`,
  `--yes` options + `@click.pass_context`.
  **CRITICAL non-obvious detail:** the conflict boundary cuts mid-decorator —
  the shared `@click.option(` opener (the line immediately above the `<<<<<<<`)
  is consumed by BOTH sides' first option. A naïve marker-strip orphans PR's
  `"--fresh",` block and produces `IndentationError`. The resolution MUST insert
  a fresh `@click.option(` line immediately before the `"--fresh",` block.
  (Verified: without insertion → compile FAIL; with insertion → compile OK.)
- Hunk 2 (`def run(...)` params, ~255–262): clean union →
  `…state_dir_override, handoff_enabled, resume_task_id, task_parallelism, fresh, assume_yes`.
- The `run()` BODY already auto-merged correctly (PR's auto-resume block sits
  above master's `load_sprint_config(...)` call — disjoint regions). No body edit
  needed beyond the decorator/param unions. The `rerun-tasks` command and
  `_dispatch_resume_rerun` → `run_rerun_tasks` were verified safe (identical
  keyword-only signature on both branches).

### A3. `src/superclaude/cli/sprint/executor.py` (one hunk, ~354) — **take MASTER**
```
master:  report.tasks_passed = sum(1 for r in task_results if r.status.is_success)
PR:      report.tasks_passed = sum(1 for r in task_results if r.status == TaskStatus.PASS)
```
The merged `models.py` (auto-resolved to master) defines
`is_success = {PASS, PASS_RECOVERED}`. The PR's strict `== PASS` would silently
drop `PASS_RECOVERED` tasks from the count breakdown. Resolution: master's
`r.status.is_success`.

## Deliverable B — PASS_RECOVERED correctness fix (resume/ package)

`master` `executor.py:1011` assigns `TaskStatus.PASS_RECOVERED` to a per-task
result (non-zero exit but evidence of success — #121/#126); it is persisted into
`phase-N-result.json` `task_results[].status` as `"pass_recovered"` and read
back by `resume/planner.py`. The PR decides task success with identity checks
against `PASS` only. Six sites must widen to a **None-safe PASS-family predicate**
(`persisted_status is not None and persisted_status.is_success`, and the negation
for rerun / next-unfinished sets):

| File | Line | Current | Effect if unfixed |
|---|---|---|---|
| `resume/planner.py` | 163 | `is not TaskStatus.PASS` (rerun set) | re-runs a recovered (successful) task |
| `resume/planner.py` | 318 | `is TaskStatus.PASS` (last_completed) | misplaces boundary |
| `resume/planner.py` | 324 | `is not TaskStatus.PASS` (next_unfinished) | points resume at a completed task |
| `resume/integrity.py` | 123 | `signal_a_pass = is TaskStatus.PASS` | gate won't validate seam → STOP/quarantine |
| `resume/integrity.py` | 129 | `signal_b_pass = is TaskStatus.PASS` | same |
| `resume/drift.py` | 93 | COMPLETED set = `is TaskStatus.PASS` | drift scoring blind to recovered tasks |

NOTE: `planner.py:383` (`_is_pass_family_phase` via `PhaseStatus(...).is_success`)
is already PASS-family-safe; do NOT change it. Only the TASK-level identity
checks regressed.

Also required: a RED→GREEN regression test (in `tests/sprint/test_resume.py` or a
sibling) proving a `pass_recovered` tail task is NOT added to
`plan.rerun_task_ids` and IS treated as `last_completed`, plus an integrity-gate
assertion that a recovered seam validates (signal_a/signal_b pass).

## Acceptance / validation gates

- Working tree's existing uncommitted changes (modified `executor.py`,
  `handoff.py`, `test_executor.py`, `test_handoff_store.py` on `master`) MUST NOT
  be disturbed; do the resolution on the PR branch, not on a dirty `master`.
- All resolved files `py_compile` clean (already pre-verified for A2/A3).
- `uv run pytest tests/sprint/ -q` green (the one pre-existing
  `test_e2e_success::test_jsonl_events_for_each_phase` failure is documented in
  the PR as pre-existing on master — confirm it is the ONLY failure, do not
  attribute it here).
- `uv run ruff format --check src/ tests/` and `uv run ruff check` clean
  (CI runs `ruff format --check` separately from `make lint`).
- `make verify-sync` if any `src/superclaude/{skills,agents,commands}` touched
  (not expected here — this is CLI source, not synced components).
- PR target discipline: any push targets `origin` (`IronbellyOrg/IronClaude`);
  any `gh pr` uses `--repo IronbellyOrg/IronClaude`. NEVER upstream.
- NEVER stage `.claude/` paths.

## Out of scope

- No new auto-resume features; no refactor of the resume package beyond the
  6-site predicate widening + its regression test.
- The pre-existing markdownlint MD040 debt the PR already deferred stays deferred.
