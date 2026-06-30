# Research Notes: PR #124 merge-conflict resolution + PASS_RECOVERED correctness fix

**Date:** 2026-06-04
**Scenario:** A (explicit — orchestrator pre-verified all resolutions via `git merge-tree` + `py_compile`)
**Depth Tier:** Quick (small, well-bounded scope; 3 researchers, 0 web)
**Track Count:** 1

---

## EXISTING_FILES

PR branch `feat/sprint-auto-resume-v435` (tip `aedd0104`) → `master` (tip `1a00efb2`).
merge-base `86c46321`. `mergeable: CONFLICTING`, `mergeStateStatus: DIRTY`.

**Conflicted files (3, from `git merge-tree --write-tree --name-only`):**
- `CHANGELOG.md` — 1 hunk (~lines 7–55). Both sides added a distinct `###`
  section under `## [Unreleased]`. Additive.
- `src/superclaude/cli/sprint/commands.py` — 2 hunks. Hunk 1 = `@click.option`
  decorators on `run()`; Hunk 2 = `def run(...)` param list. Both additive unions.
- `src/superclaude/cli/sprint/executor.py` — 1 hunk (~line 354). Semantic: the
  `tasks_passed` aggregation line.

**Coupled (auto-merged clean, NO markers, but semantically relevant):**
- `src/superclaude/cli/sprint/models.py` — auto-merged to master's `TaskStatus`
  (adds `PASS_RECOVERED`; `is_success = {PASS, PASS_RECOVERED}`).
- `src/superclaude/cli/sprint/resume/planner.py` — task-level success via
  `is TaskStatus.PASS` at lines 163, 318, 324.
- `src/superclaude/cli/sprint/resume/integrity.py` — `signal_a_pass` /
  `signal_b_pass` via `is TaskStatus.PASS` at lines 123, 129.
- `src/superclaude/cli/sprint/resume/drift.py` — COMPLETED set via
  `is TaskStatus.PASS` at line 93.
- `src/superclaude/cli/sprint/rerun_tasks.py` — `run_rerun_tasks` signature
  BYTE-IDENTICAL on both branches (dispatch from commands.py is safe).
- `pyproject.toml` — auto-merged to `4.3.5` (PR's bump).
- `tests/sprint/test_executor.py`, `tests/sprint/test_cli_contract.py` —
  auto-merged clean, compile, no duplicate test defs.

## PATTERNS_AND_CONVENTIONS

- UV for all Python ops. `uv run pytest`, `uv run ruff check`,
  `uv run ruff format --check src/ tests/` (CI runs format-check separately
  from `make lint`).
- `TaskStatus` enum is the success-status source of truth. master broadened
  `is_success` to `{PASS, PASS_RECOVERED}`; correctness depends on callers
  using `.is_success` rather than identity `is TaskStatus.PASS`.
- Click alias pattern: `--fresh` and `--restart` both target dest `fresh`
  (already in PR branch — not a defect).
- Conflict-resolution discipline: do NOT disturb the working tree's existing
  uncommitted changes on `master`; perform resolution on the PR branch.

## GAPS_AND_QUESTIONS

- Does any OTHER non-conflicted file (outside resume/) make `is TaskStatus.PASS`
  task-level identity checks that master's PASS_RECOVERED now breaks? (Researcher
  to sweep the whole sprint package.)
- Exact current line numbers in resume/*.py on the PR branch HEAD (line numbers
  cited were from `git show origin/feat/...` — researcher to confirm against the
  checked-out branch state, since they may shift after conflict resolution edits).
- Are there existing tests in `tests/sprint/test_resume.py` whose assertions
  encode the `== PASS` assumption and would need updating alongside the fix?

## RECOMMENDED_OUTPUTS

- `research/01-conflict-hunks-verified.md` — exact conflict hunks + verified
  resolutions for all 3 files (incl. the `@click.option(` insertion subtlety and
  the master-side executor choice), with compile evidence.
- `research/02-pass-recovered-coupling.md` — full enumeration of the resume/
  identity-check sites, the persisted-status data path, and any test assertions
  encoding `== PASS`; plus a codebase-wide sweep for other `is TaskStatus.PASS`
  task-level checks.
- `research/03-validation-and-test-surface.md` — the test/lint/verify command
  surface, existing `test_resume.py` structure, and where a RED→GREEN regression
  test for the PASS_RECOVERED fix should live + its naming/fixture conventions.

## SUGGESTED_PHASES

Builder should structure the generated task file roughly as:
- Phase 1 — Branch setup (check out PR branch, confirm clean base, rebase onto
  origin/master if needed per CLAUDE.md pre-PR checks).
- Phase 2 — Deliverable A: resolve the 3 conflicted files (CHANGELOG keep-both;
  commands.py union + `@click.option(` insertion; executor.py take-master),
  one item per file, each with a `py_compile` verification.
- Phase 3 — Deliverable B: widen the 6 resume/ identity-check sites to the
  None-safe PASS-family predicate, one item per file (planner ×3 sites,
  integrity ×2 sites, drift ×1 site).
- Phase 4 — RED→GREEN regression test proving a `pass_recovered` tail task is
  NOT in `rerun_task_ids` and IS `last_completed` (+ integrity-gate recovered
  seam validates).
- Phase 5 — Full validation: `uv run pytest tests/sprint/ -q`, ruff check +
  format-check; confirm the only failure is the documented pre-existing
  `test_e2e_success::test_jsonl_events_for_each_phase`.
- Phase 6 — Completion (status → Done).

## TEMPLATE_NOTES

Template **02 (complex)** — multi-phase, has discovery/build/test/verify, a
conditional (rebase-if-behind), and quality gates. Tier Quick (3 researchers).
TESTING_REQUIREMENTS=UNIT (the regression test + full sprint suite).
VALIDATION_REQUIREMENTS = py_compile per resolved file + ruff check + ruff
format-check + full sprint pytest. QA_GATE_REQUIREMENTS=FINAL_ONLY.

## AMBIGUITIES_FOR_USER

- Deliverable B (PASS_RECOVERED widening) is technically beyond "resolve the
  conflicts" but is required for a *correct* merge. The operator already chose
  (in-session) to include both A and B in one task. Builder should still surface
  this as an explicit note so the executor understands B touches non-conflicted
  files. Otherwise intent is clear.
