# QA Report — Phase 5 (Validation: UV-only test run + lint + TM-0 regression gate)

**Topic:** Per-Phase Turn-Budget Model for the Sprint Runner (R-1..R-10, TM-0..TM-14)
**Task:** TASK-RF-per-phase-turn-budget-20260618-160752
**Date:** 2026-06-18
**Phase:** report-validation (Phase-Gate QA, Phase 5)
**Fix cycle:** N/A (cycle 1)
**Stance:** Adversarial — every artifact claim independently re-verified by re-running commands and reading source. Fix authorization: true.

---

## Overall Verdict: PASS

All four acceptance criteria verified by independent re-execution. The saved artifacts faithfully reflect the actual current state — no fabricated counts, no unsound fix, no source modification papering over a failure, no real lint error in any touched file. **No fixes were required.**

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | AC-1: Re-run spec §6 command → full pass, TM-0 + all 13 rows pass | PASS | Independent re-run: `46 passed in 4.32s`, 0 failed/0 errors. `test_regression_3x5_no_global_pool_starvation` (TM-0) PASSED; TM-11 PASSED. All 13 spec TM node names present & PASSED (cross-checked vs saved output). |
| 2 | AC-1: Artifacts faithfully reflect actual run (no fabricated counts) | PASS | Saved `pytest-output.txt` = `46 passed in 4.33s` matches my `4.32s` re-run line-for-line (same 46 nodes, same statuses). `test-summary.md` Run 2 = "46 passed, 0 failed" and `test-verdict.md` = "46 passed, 0 failed, 0 errors" — both match reality. |
| 3 | AC-2: TM-11 root cause is genuinely pre-existing, not a ledger-change defect | PASS | `models.py:442-450` `is_success` excludes `PhaseStatus.SKIPPED` (verified by Read). `executor.py:2495-2498` downgrades outcome→ERROR when `not all(is_success)`; `executor.py:2598-2602` raises `SystemExit(1)`. `git diff` of models.py/executor.py touches NONE of `is_success`/`SKIPPED`/`is_terminal`/outcome/exit logic. |
| 4 | AC-2: Fix is sound, assertions not weakened | PASS | Only `pytest.raises(SystemExit)` wrapping added (test_per_phase_budget.py:583-584), present exactly once, only in TM-11. Assertions intact: `construct_count[0] == 1` (L587), `status == SKIPPED` (L595), `exit_code == 0` (L596). `write_summary(sprint_result)` runs at executor.py:2573 BEFORE the raise at 2602 → `captured[0]` is populated → post-`with` assertions reachable (proven: green run would IndexError otherwise). |
| 5 | AC-2: No source file changed to make TM-11 pass | PASS | TM-11 fix is in untracked test file only. The sole executor.py diff hit on "SKIPPED" is a control-flow comment about gate-tripped tasks (not outcome/exit logic). models.py diff = +8 lines, none touching skip/outcome. |
| 6 | AC-3: ruff check + ruff format clean on all 6 touched files | PASS | `uv run --with ruff ruff check <6 files>` → "All checks passed!". `ruff format --check <6 files>` → "6 files already formatted". |
| 7 | AC-3: Sole `make lint` failure is pre-existing unrelated recommend.md | PASS | lint-output.txt error = `recommend.md has ## Activation but no matching skill directory: sc-recommend-protocol`. `git status` shows recommend.md NOT touched by this task; actual skill dir is `sc-recommend` (not `-protocol`) → pre-existing & unrelated to sprint-runner code. |
| 8 | AC-4: No regression in pre-existing reused tests | PASS | All 32 `TestTurnLedger` + 2 concurrency + 3 multi_phase (`TestThreePhaseHappyPath`, `TestHaltAtPhaseThree`, TM-7 golden) PASSED in the run. Total 46/46 green = zero regressions. |
| 9 | Spec §6 matrix is exactly 13 rows; TM-3/TM-4 do not exist | PASS | `grep -oE "TM-[0-9]+"` over `merged-requirements-FINAL.md` → exactly {0,1,2,5,6,7,8,9,10,11,12,13,14} = 13 IDs. TM-3/TM-4 absent from spec AND task file. Artifact claim accurate. |

---

## Summary

- Checks passed: 9 / 9
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (none required)

---

## Detailed Verification Evidence

### AC-1 — Independent re-run of the exact spec §6 command

Ran verbatim:
```
uv run pytest tests/sprint/test_per_phase_budget.py tests/sprint/test_models.py::TestTurnLedger tests/sprint/test_turn_ledger_concurrency.py tests/sprint/test_multi_phase.py -v
```
Result: **`46 passed in 4.32s`**, 0 failed, 0 errors. Per-file breakdown (from verbose output): per_phase_budget.py=9, test_models TestTurnLedger=32, concurrency=2, multi_phase=3 → 46 total. `test_regression_3x5_no_global_pool_starvation` (TM-0, the mandatory regression gate) **PASSED** at the top of the run. `test_skip_and_python_phases_construct_no_ledger` (TM-11) **PASSED**.

Faithfulness check: the saved `pytest-output.txt` records `46 passed in 4.33s` with the identical 46 node names and identical PASSED statuses as my re-run. `test-summary.md` (Run 2: "46 passed, 0 failed") and `test-verdict.md` ("46 passed, 0 failed, 0 errors") both match the actual current state. No fabricated counts.

All 13 spec TM node names cross-checked against the saved output — every one present and PASSED (TM-0, TM-1, TM-2, TM-5, TM-6, TM-7, TM-8, TM-9, TM-10, TM-11, TM-12, TM-13, TM-14).

### AC-2 — TM-11 fix soundness (does NOT mask a regression)

Root cause confirmed pre-existing by reading source:
- `src/superclaude/cli/sprint/models.py:442-450` — `PhaseStatus.is_success` returns membership in {PASS, PASS_NO_SIGNAL, PASS_NO_REPORT, PASS_RECOVERED, PREFLIGHT_PASS, PASS_MISSING_CHECKPOINT}. `PhaseStatus.SKIPPED` (defined L422) is **NOT** in this set.
- `executor.py:2495-2498` — `if not all(r.status.is_success ...): outcome = ERROR`.
- `executor.py:2598-2602` — `_exitcode = 0 if outcome == SUCCESS else 1; if _exitcode != 0: raise SystemExit(_exitcode)`.

Therefore any sprint containing a skip phase yields outcome ERROR → `SystemExit(1)`, independent of the per-phase ledger change. Proven NOT introduced by this task: `git diff src/superclaude/cli/sprint/models.py src/superclaude/cli/sprint/executor.py` touches none of `is_success`, `SKIPPED` membership, `is_terminal`, the `outcome == SUCCESS` check, or the `SystemExit` line. The only executor.py diff line mentioning "SKIPPED" is a comment describing gate-tripped-task recording — not outcome/exit logic.

Fix is the minimal correct test-only change: `with pytest.raises(SystemExit): execute_sprint(config)` (test_per_phase_budget.py:583-584), present exactly once and only in TM-11 (the other 6 `execute_sprint` calls in the file are unwrapped because they construct task-only sprints that return SUCCESS).

Assertions verified intact and NOT weakened:
- L587: `assert construct_count[0] == 1` (exactly one `TurnLedger.__init__` — only the task phase).
- L595: `assert skip_results[0].status == PhaseStatus.SKIPPED`.
- L596: `assert skip_results[0].exit_code == 0`.

Reachability of post-exit assertions proven: `logger.write_summary(sprint_result)` executes at `executor.py:2573` inside the `try` block, BEFORE the `finally` and BEFORE the `raise SystemExit` at L2602. So the spy's `captured` list is populated before the exit; `captured[0]` (L592) does not IndexError — confirmed by the green run (a non-populated capture would have raised IndexError and failed the test).

No source file (executor.py / models.py) was changed to make TM-11 pass.

### AC-3 — Lint conclusion

`uv run --with ruff ruff check` on all 6 touched files (`executor.py`, `models.py`, `test_per_phase_budget.py`, `test_models.py`, `test_turn_ledger_concurrency.py`, `test_multi_phase.py`) → **"All checks passed!"**. `ruff format --check` on the same 6 → **"6 files already formatted"**.

The sole `make lint` failure is the pre-existing architecture-lint error: `src/superclaude/commands/recommend.md has ## Activation but no matching skill directory: sc-recommend-protocol`. Verified unrelated: `git status` shows `recommend.md` is NOT among this task's modified files, and the actual skill directory is named `sc-recommend` (not `sc-recommend-protocol`), a naming mismatch that predates and is orthogonal to the sprint-runner change. lint-architecture aborts before ruff runs, which is why ruff was invoked directly on the touched files — a legitimate, documented sequencing.

### AC-4 — No regression in reused tests

All pre-existing reused tests pass in the run: 32 `TestTurnLedger` cases (incl. boundary, monotonicity, decay, sustainability), 2 concurrency cases, and the 3 multi_phase cases (`test_three_phase_happy_path`, `test_halt_at_phase_three`, TM-7 `test_task_then_legacy_execution_log_golden`). 46/46 green confirms zero regressions across the reused suite. (Note: the "24 pre-existing reused tests" figure in test-verdict.md is a descriptive subset count; the load-bearing fact — all reused tests still pass with no regression — is verified.)

---

## Issues Found

None.

---

## Actions Taken

No fixes required — all artifacts faithfully represent reality, the TM-11 fix is sound and test-only, all touched files are lint-clean, and the regression gate (TM-0) passes.

---

## Recommendations

- Phase 5 is GREEN. Safe to proceed to Phase 6 / task completion.
- Carry forward the pre-existing `recommend.md` architecture-lint error as a known, out-of-scope item (it is unrelated to this task and must not be "fixed" here per scope discipline).

---

## Confidence Gate

**Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 4 | Grep/Bash-grep: 9 | Glob: 0 | Bash: 10 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0

No web research was required — every claim is local source-truth (re-run commands, source files, git diff). Every checklist item is VERIFIED with cited tool output; none unverifiable, none unchecked.

---

## Overall verdict line

**PASS** — Phase 5 validation artifacts are faithful; TM-11 fix is sound and test-only; all 6 touched files are ruff-clean; the sole make-lint error is the pre-existing, unrelated `recommend.md` architecture-lint failure; TM-0 regression gate and all 13 spec §6 TM rows pass on an independent re-run (46 passed, 0 failed, 0 errors). No fixes applied (none required).

## QA Complete
