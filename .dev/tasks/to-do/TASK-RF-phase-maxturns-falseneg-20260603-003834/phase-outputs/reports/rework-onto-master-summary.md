# Rework onto `origin/master` — Summary

**Date:** 2026-06-03
**Why:** The task was authored/executed against an older IronClaude snapshot
(branched off `feat/brv-mg-sibling-skill-cycle`). When preparing a clean PR, we
found `origin/master` had refactored the exact target area. The fix was re-applied
onto `origin/master` (commit base) so it merges cleanly. The original
against-old-base commit is `205a36b1` (full process provenance preserved in this
task folder).

## What master changed under us

- `TaskStatus.FAIL` was split into **`FAIL_TERMINAL` ("fail")** and
  **`FAIL_RECOVERABLE` ("fail_recoverable")** (transient/retryable failures, via
  a new `_is_transient_failure()` helper + the per-task rerun feature, PR #116).
  Both remain in `is_failure`; `is_success` was still strictly `== PASS`.
- The per-task switch became 4-way: `0→PASS`, `124→INCOMPLETE`,
  `_is_transient_failure→FAIL_RECOVERABLE`, `else→FAIL_TERMINAL`.
- **The false-negative bug still existed on master** — aggregation was still
  `all(r.status == TaskStatus.PASS …)`, so an overran-but-completed task
  (→ `FAIL_RECOVERABLE`) still failed the phase. The fix's purpose was intact.
- PR #119 (`2047a2ad`) had already fixed the fake-`Popen` `stdin` failures, so
  the previously-flagged 57-failure follow-up is largely resolved on master.

## How the fix was adapted (vs the original against-old-base form)

1. **models.py** — unchanged intent: add success-valued `PASS_RECOVERED`,
   `is_success` covers `(PASS, PASS_RECOVERED)`; `is_failure` left as master's
   `(FAIL_TERMINAL, FAIL_RECOVERABLE, INCOMPLETE)`.
2. **executor.py per-task switch** — the recovery branch is inserted as a new
   `elif` that takes **precedence over `_is_transient_failure`**:
   ```
   if   exit_code == 0:                                   PASS
   elif exit_code == 124:                                 INCOMPLETE
   elif detect_error_max_turns(p) and _task_completed_before_overrun(p): PASS_RECOVERED
   elif _is_transient_failure(p):                         FAIL_RECOVERABLE
   else:                                                  FAIL_TERMINAL
   ```
   **Design decision:** completion evidence (a success envelope before the
   terminal `error_max_turns` line) outranks the transient-failure
   classification — an overran-AFTER-completing task is a success, not a retry.
   `exit 0 → PASS` and `exit 124 → INCOMPLETE` are unchanged.
3. **executor.py aggregation** — both surfaces switched to `.is_success`
   (inline `all_passed` + `aggregate_task_results` `tasks_passed`); `tasks_failed`
   still counts `FAIL_TERMINAL` only.
4. **executor.py helper** — `_task_completed_before_overrun` + the
   `_TASK_SUCCESS_ENVELOPE_PATTERN` added after `_is_transient_failure`.
5. **tests** — the 4 per-task tests + 1 aggregation test re-applied; guard
   assertions updated `FAIL → FAIL_TERMINAL`. The overran-without-completion
   fixture has no `output_tokens` field, so `_is_transient_failure` returns False
   and the task stays `FAIL_TERMINAL` (deterministic).

## Gate results on the master-based branch

- ✅ 5 new tests pass.
- ✅ `make lint` exit 0 (`All checks passed!`).
- ✅ Full `tests/sprint/` suite: **zero regressions** — `git stash` baseline diff
  shows 18 failures on clean `origin/master`, identical to the 18 with the change
  (delta = the +5 new passes only).
- ✅ `make verify-sync` drift (`sc-bare-review`, `sc-persona-research-protocol`
  missing in `src/superclaude/skills/`) is **pre-existing on clean master** —
  unrelated to these Python changes; not touched.
- exit-124 timeout behaviour unchanged (still `INCOMPLETE`, still fails the phase).

## Pre-existing on master (out of scope)

18 `tests/sprint/` failures (TUI/monitor, integration-halt, multi-phase fixtures)
+ the skills verify-sync drift — pre-date this change; repo-owner follow-up.
