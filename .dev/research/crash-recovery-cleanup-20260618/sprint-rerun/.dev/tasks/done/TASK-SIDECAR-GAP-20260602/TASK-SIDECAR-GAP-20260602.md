---
id: "TASK-SIDECAR-GAP-20260602"
title: "rerun-tasks sidecar gap — write task-results.json so merge-back refreshes canonical per-task status"
status: "🟢 Done"
type: "🐞 Fix"
priority: "🔼 High"
created_date: "2026-06-02"
updated_date: "2026-06-02"
start_date: "2026-06-02"
completion_date: "2026-06-02"
blocker_reason: ""
assigned_to: ""
related_docs:
- path: ".dev/tasks/to-do/TASK-SIDECAR-GAP-20260602/SPEC.md"
  description: "Driving spec — problem, fix shape, AC-1..AC-5, constraints"
- path: "src/superclaude/cli/sprint/rerun_tasks.py"
  description: "run_rerun_tasks merge-back path (insertion point ~1397-1411)"
- path: "src/superclaude/cli/sprint/recovery.py"
  description: "merge_recovery_bundle step 7 sidecar consumer (601-652) — DO NOT MODIFY"
- path: "tests/sprint/e2e_real/test_e2e_rerun_happy_path.py"
  description: "E2E-1 real-subprocess test — canonical assertion to flip to pass"
tags: [fix, sprint-cli, rerun, recovery, sidecar]
task_type: static
---

# rerun-tasks sidecar gap — write task-results.json so merge-back refreshes canonical per-task status

## Task Overview

`run_rerun_tasks` re-executes failed tasks and merges artifacts back, but never writes the
`task-results.json` sidecar that `merge_recovery_bundle` step 7 (`recovery.py:601-652`) needs to
splice refreshed per-task statuses into the canonical `phase-N-result.json`. Result: after a
successful rerun the canonical status stays `fail_recoverable` instead of `pass`, and the bundle
downgrades to PARTIAL. This task adds the ~12-line sidecar write in `run_rerun_tasks` and updates
tests. `merge_recovery_bundle` is correct and MUST NOT change. See `SPEC.md` for AC-1..AC-5.

## Phase 1: Implement the sidecar write

**Step 1.1:** Add the sidecar writer in `run_rerun_tasks`

- [x] Edit `src/superclaude/cli/sprint/rerun_tasks.py`. In `run_rerun_tasks`, on the successful
  merge-back path, AFTER `produced = sorted(...)` (currently ~line 1393-1397) and BEFORE the
  `merge_recovery_bundle(recovery, ...)` call (currently ~line 1411), insert a sidecar write so the
  merge can refresh canonical per-task statuses. Read the bundle's refreshed result JSON via
  `sub_config.phase_result_json(sub_phase_obj)`; filter its `task_results` list to entries whose
  `["task"]["task_id"]` is in `set(resolved)`; write that filtered list as JSON to
  `produced[0].parent / "task-results.json"` (this dir MUST equal `bundle.artifacts_produced[0].parent`
  which the merge reads — since `artifacts_produced=produced`, using `produced[0].parent` guarantees
  the match). Use the existing `_atomic_write_text` helper (rerun_tasks.py:663) and the already-imported
  `json`. Guard the empty-`produced` case (skip the write — AC-4 preserves R-F3). Suggested code (adapt
  variable names to the actual scope at the insertion point):
  ```python
  # Sidecar: serialize the rerun's refreshed task_results so merge_recovery_bundle
  # step 7 can splice the new statuses into the canonical phase-N-result.json (AC-1).
  if produced:
      _bundle_result = sub_config.phase_result_json(sub_phase_obj)
      if _bundle_result.exists():
          _bdata = json.loads(_bundle_result.read_text(encoding="utf-8"))
          _refreshed = [
              tr for tr in _bdata.get("task_results", [])
              if tr.get("task", {}).get("task_id") in set(resolved)
          ]
          # F1 (reflect-pre hardening): only write the sidecar when it covers EVERY
          # resolved task. merge_recovery_bundle's sidecar_ok=True branch drops the
          # affected tasks' prior entries and replaces them with the sidecar; a partial
          # sidecar would drop an uncovered task with NO replacement (data loss). If the
          # filtered list is incomplete, skip the write → fall back to R-F3 preserve
          # (AC-4). The _rerun_targets_passed gate (~1381) normally guarantees coverage.
          _covered = {tr.get("task", {}).get("task_id") for tr in _refreshed}
          if set(resolved).issubset(_covered):
              _atomic_write_text(
                  produced[0].parent / "task-results.json",
                  json.dumps(_refreshed, indent=2) + "\n",
              )
  ```
  Ensure: only `rerun_tasks.py` is edited; `merge_recovery_bundle` / `recovery.py` are untouched; the
  insertion sits inside the `if rerun_succeeded and merge_back:` block after `produced`; no change to
  the SHA-guard, retry-cap, or finalize logic. Mark complete once applied.

**Step 1.2:** Lint Phase 1

- [x] Run single-line Bash `cd /config/workspace/IronClaude/.claude/worktrees/SprintReRun && uv run ruff check src/superclaude/cli/sprint/rerun_tasks.py 2>&1` and confirm "All checks passed". If violations, fix them. Mark complete.

## Phase 2: Tests

**Step 2.1:** Add a focused merge-refresh unit test

- [x] Edit `tests/sprint/test_recovery.py` — in `class TestMergeRecoveryBundle`, add
  `test_merge_refreshes_canonical_status_from_sidecar`: seed a canonical `phase-N-result.json` with one
  task at `fail_recoverable`, place a `task-results.json` sidecar in the bundle results dir with that
  task at `pass` (matching `TaskResult.to_dict()` nested shape `{"task":{"task_id":...},"status":"pass",...}`),
  construct a `RecoveryBundle(affected_tasks=[tid], artifacts_produced=[<a file under that results dir>], ...)`,
  call `merge_recovery_bundle`, and assert the canonical `phase-N-result.json` now shows the task as
  `pass` with no duplicate entry and bundle status SUCCESS (AC-2/AC-3). Add a sibling assertion (or a
  second test) that WITHOUT the sidecar the prior entry is preserved and a `result-json-not-refreshed`
  failure is recorded (AC-4). Read the existing `TestMergeRecoveryBundle` tests + `merge_recovery_bundle`
  signature first to match the real call shape. Mark complete.

**Step 2.2:** Flip the E2E-1 canonical assertion

- [x] Edit `tests/sprint/e2e_real/test_e2e_rerun_happy_path.py` — change the canonical-result assertion
  from "honest gap" (T01.02 stays `fail_recoverable` / bundle-only PASS) to **AC-2**: after the rerun +
  merge, the canonical `phase-1-result.json` shows `T01.02` status `pass` (replaced, no duplicate),
  `recovery_history` populated, and tasks `T01.01`/`T01.03` unchanged. Remove/adjust the inline comment
  documenting the gap. Keep all other real-subprocess assertions intact. **F2 (reflect-pre hardening):**
  also add a DIRECT assertion that the sidecar `<bundle>/results/task-results.json` exists after the
  rerun (explicit AC-1 evidence that `run_rerun_tasks` wrote it, not just transitive via canonical PASS).
  Mark complete.

**Step 2.3:** Run the affected suites

- [x] Run single-line Bash `cd /config/workspace/IronClaude/.claude/worktrees/SprintReRun && uv run pytest tests/sprint/e2e_real/ tests/sprint/test_recovery.py tests/sprint/test_rerun_tasks.py tests/sprint/test_rerun_tasks_e2e.py tests/sprint/test_rerun_tasks_failure_modes.py -q 2>&1 | tail -15` and confirm all pass (AC-5). If a test fails because of a wrong assumption, fix the test/code; do not weaken an assertion to force green. Mark complete.

## Phase 3: Validate

**Step 3.1:** Final lint + regression confirmation

- [x] Run single-line Bash `cd /config/workspace/IronClaude/.claude/worktrees/SprintReRun && uv run ruff check src/superclaude/cli/sprint/rerun_tasks.py tests/sprint/test_recovery.py tests/sprint/e2e_real/ 2>&1 | tail -3` (expect clean). Then confirm the only files changed are `rerun_tasks.py` + the two test files via `git status --short`. Mark complete.

## Task Log / Notes 📋

### Execution Log

**[2026-06-02]** - Executed via /task F1 loop (chain: /sc:design → /sc:reflect --pre PASS → /task → /sc:reflect --post PASS). Steps 1.1–3.1 all complete. Added the `task-results.json` sidecar writer in `run_rerun_tasks` (`rerun_tasks.py:1414-1436`, with the F1 completeness guard at :1432) + 2 merge unit tests (`test_recovery.py`) + strengthened E2E-1 Proof 5 to AC-2 (canonical T01.02 → `pass`) + direct sidecar-exists assertion. `merge_recovery_bundle`/`recovery.py` untouched. Evidence: ruff clean; 39 affected sprint tests pass. /sc:reflect --post: status success, AC-1..AC-5 satisfied, 0 Drift/0 Regression, R-F3 preserved (reflect-post-report.md). Promotion suppressed (--no-promote). Task marked Done.

### Phase Findings
