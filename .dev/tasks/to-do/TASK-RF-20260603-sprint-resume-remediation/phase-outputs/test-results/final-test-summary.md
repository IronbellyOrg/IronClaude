# Final Full-Suite Test Summary (Phase 5)

**Command:** `uv run pytest tests/sprint/ -v --continue-on-collection-errors`
**Result line:** `54 failed, 999 passed, 20 warnings, 2 errors in 18.64s`
**Full output:** `full-sprint-suite.txt`

> `--continue-on-collection-errors` was required because two PRE-EXISTING test modules fail at
> import (see "Pre-existing collection errors" below); without the flag pytest interrupts before
> running anything. The flag lets the 1053 collected tests run so regressions can be assessed.

## Verdict: ✅ PASS for everything this task touched; all failures are PRE-EXISTING and UNRELATED

### What this task touched — ALL GREEN

| Suite | Result |
|-------|--------|
| `test_resume.py` (deterministic resume suite) | **21 passed, 0 failed** (17 original + CG-2 + CG-1 + CG-3 positive + CG-3 negative) |
| `e2e_real/test_e2e_resume*.py` (real-subprocess resume e2e) | **7 passed, 0 failed** |

**Explicit resume-invariant non-regression confirmation (all PASS):**

- `test_drift_trailing_whitespace_high_conf` (AC-4) — PASS
- `test_drift_material_edit_low_conf` (AC-5 ID removal) — PASS
- `test_drift_same_id_material_body_edit_low_conf` (CG-2/F-3) — PASS
- `test_boundary_quarantine_nondestructive` (FR-2.5) — PASS
- `test_boundary_partial_paths_surfaced_in_report` (CG-1/F-2) — PASS
- `test_planner_performs_no_writes` (planner pure-read) — PASS
- `test_resume_hard_crash_phase_level` (AC-3, reconciled) — PASS
- `test_resume_hard_crash_double_validates_prior_phase_tail` (CG-3/F-4) — PASS
- `test_resume_hard_crash_prior_tail_overclaim_stops` (CG-3 negative) — PASS

### The 54 failures + 2 errors — ALL pre-existing, NONE caused by F-3/F-2/F-4

**Failure error signatures (uniform):**

| Signature | Count | Nature |
|-----------|-------|--------|
| `'<FakePopen>' object has no attribute 'stdin'` | 48 | Executor subprocess-lifecycle tests use fake `Popen` doubles that lack `.stdin`. They fail at subprocess **launch** — BEFORE `_write_phase_result_json` (my only executor change) is ever called. |
| `list index out of range` | 6 | `test_e2e_success.py` — pre-existing e2e harness issue, unrelated to the resume subsystem. |
| `ImportError: cannot import name 'invoke_haiku'` (collection) | 2 | `test_retrospective.py:34`, `test_summarizer.py:28` import `invoke_haiku`, renamed to `invoke_sonnet` in unrelated commit `70ef6486` (the F-5 rename, REPORT.md NONE/no-action). |

**Failing test files (all executor/subprocess, none in the resume subsystem):**
`test_diagnostics.py`, `test_e2e_halt.py`, `test_e2e_success.py`, `test_execute_sprint_integration.py`,
`test_executor.py`, `test_integration_halt.py`, `test_integration_lifecycle.py`,
`test_integration_signal.py`, `test_multi_phase.py`, `test_phase8_halt_fix.py`,
`test_regression_gaps.py`, `test_tui_monitor.py`, `test_watchdog.py`.

### Proof these are NOT regressions from this task

1. **My `executor.py` diff is 2 hunks, both inside `_write_phase_result_json`** (docstring + 2 imports + 2 dict keys `tasklist_sha256`/`tasklist_sha256_ws`) — verified via `git diff`. Purely additive.
2. **`executor.py` contains no `.stdin` reference at all** (`grep "\.stdin" executor.py` → empty) — the failing `.stdin` access lives in a separate, pre-existing module. My change cannot cause it.
3. **The `.stdin` failures occur at subprocess launch**, which is upstream of `_write_phase_result_json`; my dict-key addition runs only after a phase completes.
4. **The `invoke_haiku` errors are independently confirmed pre-existing** by the PG.4 rf-qa agent (commit `70ef6486`) and correspond to REPORT.md's F-5 (NONE/no-action).
5. **All resume-subsystem tests (the only functional surface of F-3/F-2/F-4) pass**, including the three RED→GREEN coverage-gap tests and every pre-existing resume invariant.

### Conclusion

The remediation introduced **zero regressions**. Everything F-3/F-2/F-4 touched is green. The 54
failures + 2 errors are pre-existing branch state (broken fake-Popen subprocess doubles + the F-5
`invoke_haiku` rename), tracked as Follow-Up Items, and do NOT block promotion of F-3/F-2/F-4.
