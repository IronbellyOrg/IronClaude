# SPEC — rerun-tasks sidecar gap: merge-back must refresh canonical per-task status

## Problem (driving need)

After a successful `superclaude sprint rerun-tasks` rerun **with merge-back**, the
canonical `phase-N-result.json` still shows the reran task as `fail_recoverable`,
**not** `pass`. The task is genuinely re-executed (output renamed to `.failed-<ts>`,
fresh PASS output written, `recovery_history` recorded), but the operator-visible
per-task status is stale.

**Root cause (verified):** `merge_recovery_bundle` step 7 (`recovery.py:601-652`)
refreshes per-task statuses **only** from a `task-results.json` sidecar in the
bundle's results dir (`bundle.artifacts_produced[0].parent`). When that sidecar is
absent (`sidecar_ok=False`) it deliberately preserves prior entries and records a
`result-json-not-refreshed` failure (R-F3 no-data-loss), downgrading the bundle to
PARTIAL. **`run_rerun_tasks` never writes that sidecar** (`grep` confirms zero
references in `rerun_tasks.py`), so the refresh never fires. Surfaced by the real-
subprocess e2e harness `tests/sprint/e2e_real/test_e2e_rerun_happy_path.py`.

## Fix shape

`run_rerun_tasks`, on the successful merge-back path, must serialize the rerun's
refreshed `task_results` (for the affected/`resolved` task IDs) from the bundle's
`phase-N-result.json` into `<bundle>/results/task-results.json` **before** calling
`merge_recovery_bundle`. Shapes already match: both canonical and bundle result JSONs
are written by `_write_phase_result_json` using `TaskResult.to_dict()`
(`models.py:184-194`, nested `{"task":{"task_id":...},...}`), which is exactly what
the splice filter at `recovery.py:641` consumes. **Do NOT modify
`merge_recovery_bundle`** — it already consumes the sidecar correctly.

## Acceptance Criteria

- **AC-1** — On successful merge-back, `run_rerun_tasks` writes
  `<bundle>/results/task-results.json` (a JSON list) containing the rerun's
  `task_results` entries for exactly the affected task IDs, in `TaskResult.to_dict()`
  shape. The sidecar dir MUST equal `bundle.artifacts_produced[0].parent`.
- **AC-2** — After merge, the canonical `phase-N-result.json` shows each reran task's
  status as `pass`; the prior `fail_recoverable` entry is replaced (no duplicate
  task_id entries); `recovery_history` remains populated.
- **AC-3** — With the sidecar present + readable, the merge records **no**
  `result-json-not-refreshed` failure and the bundle status is `SUCCESS`.
- **AC-4** — R-F3 preserved: when `produced` is empty / sidecar unwritable, prior
  behavior (preserve prior entries, PARTIAL, no silent drop) is unchanged.
- **AC-5** — `tests/sprint/e2e_real/` E2E-1 canonical assertion flips to expect
  `pass`; recovery + rerun_tasks suites stay green; `ruff` clean; zero regressions.

## Constraints

- Edit ONLY `src/superclaude/cli/sprint/rerun_tasks.py` (sidecar write) + test files.
- Worktree only; no `.claude/` edits; `rerun_tasks.py` is `cli/` (not a skill) so no
  `make sync-dev` needed.
- Reuse existing helpers: `_atomic_write_text` (rerun_tasks.py:663), `json` (already
  imported). Insertion point: after `produced = sorted(...)` (~1397), before
  `merge_recovery_bundle(...)` (~1411).
