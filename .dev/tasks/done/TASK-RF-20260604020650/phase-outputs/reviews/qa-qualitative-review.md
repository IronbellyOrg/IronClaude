# QA Report — Task Qualitative (post-completion operational validation)

**Topic:** TASK-RF-20260604020650 — PR #120 Medium fixes (M1 handle-leak, M2 unbounded watchdog, M3 corrupt-handoff crash, M4 scheduler tests)
**Date:** 2026-06-04
**Phase:** task-qualitative (EXECUTED task — evaluated against actual outputs on disk)
**Fix cycle:** N/A (single pass)
**Stance:** Adversarial — assumed errors present; verified every claim against actual files; regression-reverted all three source fixes to prove fail-before/pass-after.

---

## Overall Verdict: PASS

All four fixes (M1/M2/M3/M4) are correctly applied, operationally sound, and pinned by valid
regression tests. Every M1/M2/M3 test was independently proven to FAIL against the pre-fix code
(reverted in place, re-run, restored). The full sprint suite (1124 passed), ruff format, and ruff
lint are all green on the touched files. No issue of any severity found; no in-place fixes required.

## Items Reviewed (15-item task-qualitative checklist)

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | `uv run pytest tests/sprint/ -q` → 1124 passed/0 failed (66s); `ruff format --check src/ tests/` → 781 files clean; `ruff check` on 6 touched files → "All checks passed!" — all commands run live, all green. |
| 2 | Project convention compliance | none | PASS | Edits target `src/superclaude/cli/sprint/` and `tests/sprint/` directly (NOT `.claude/` synced output) — correct side of SoT boundary. UV used for all runs. `--strict-markers` active (pyproject.toml:110); only `unit` marker used (registered pyproject.toml:114). |
| 3 | Intra-phase execution simulation | none | PASS | Phases ordered M3→M1→M2→M4→verify. Each test reuses an already-defined helper (`_config` test_handoff_store.py:19; `_make_config` test_executor.py:35) or a self-contained local `_make_config` (test_poll_watchdog_ceiling.py:23). No item reads a file a later item creates. |
| 4 | Function signature verification | none | PASS | `FileHandoffStore.read(*, phase, task)` unchanged (handoff.py:62); `_poll_with_stall_watchdog(proc, config, *, output_path, on_stall, poll_interval)` guard-only change (executor.py:1402-1449); `_run_task_subprocess` wrapper added around poll, happy-path return (executor.py:1540-1548) intact. `TaskEntry(task_id,title,...,dependencies)` and `TaskResult(task,status=...)` constructors match models.py:31-43 / 172-188. |
| 5 | Module context analysis | none | PASS | No new imports in any of the 3 source edits (`json` already handoff.py:18; `time`/`ClaudeProcess` already in executor scope). M2 uses module-bound `time.monotonic` (patchable as `executor.time.monotonic`, exercised by the test). Docstring on `read` updated to document the corrupt→None contract. |
| 6 | Downstream consumer analysis (M3) | none | PASS | BOTH resume call sites — parallel `_worker` (executor.py:1103-1104) and sequential loop (executor.py:1277-1278) — guard `if _prior is not None and is_validated_success(_prior):`, so a corrupt-record `None` falls through to re-run the task. `is_validated_success` imported executor.py:26. Correct degrade-to-rerun semantics. |
| 7 | Test validity | none | PASS | All tests exercise real artifacts with realistic input: M3 writes 3 real corrupt byte-strings to the real on-disk handoff path; M1 drives the real `_run_task_subprocess` with a forced `KeyboardInterrupt`; M2 drives the real `_poll_with_stall_watchdog` with a never-exiting fake proc + deterministic clock; M4 calls the real scheduler functions. No stub/placeholder assertions. |
| 8 | Test coverage of primary use case | none | PASS | M4 covers diamond/linear/independent waves (+ permuted determinism), cycle detection (`.unresolved` + message), self-edge drop, unknown-dep filter, dep de-dup, recorded-dep union, tri-state oracle — 9 tests. M1/M2/M3 each cover the exact failure mode + (M2) kill-mode-unchanged + disabled-path companions. |
| 9 | Error path coverage | none | PASS | M3 except clause is the narrow `(json.JSONDecodeError, ValueError)` (NOT bare `except`) — covers all 3 corrupt inputs the test exercises (truncated/empty/garbage all raise JSONDecodeError ⊂ ValueError). M1 uses `except BaseException` so `KeyboardInterrupt` is caught; re-raises with bare `raise`. |
| 10 | Runtime failure-path trace | none | PASS | M1: `proc.terminate()` is safe on already-exited child — process.py:175-177 early-returns + `_close_handles()` (idempotent, exception-swallowing, process.py:238-244). M2: ceiling trips → loop exits → tail `proc.wait()` (executor.py:1475) bounds wait by `timeout_seconds` and returns 124 + closes handles on TimeoutExpired (process.py:162-170). Kill-mode `break` (executor.py:1469-1474) untouched. |
| 11 | Completion scope honesty | none | PASS | Task log counts match reality (full suite 1124 passed verified live). The two final Post-Completion items (Task Summary, frontmatter→Done) remain unchecked — correct, as this qualitative gate runs BEFORE the Done flip. The OPEN QUESTION (M2 fallback value) was resolved in-log to the recommended `getattr(proc,"timeout_seconds",3600)`, not ignored. |
| 12 | Ambient dependency completeness | none | PASS | M2 fix's only caller is `_run_task_subprocess` (executor.py:1534) where `proc` always has `timeout_seconds` (process.py:61); the `3600` fallback is defensive-only. New test file `test_poll_watchdog_ceiling.py` and `test_scheduler.py` are self-contained (no cross-import of test_executor helpers). All test imports resolve. |
| 13 | Kwarg sequencing red flags | none | PASS | No "add kwarg before add parameter" pattern. No signatures changed — all three fixes are body-internal (try/except wrap, loop-guard augmentation, try/except wrap). |
| 14 | Function existence claims | none | PASS | Grep-verified every claimed symbol: `CycleError`/`dependencies_of`/`topological_launch_order`/`is_task_satisfied` (scheduler.py); `TaskStatus.PASS_RECOVERED` (models.py:50, spelled correctly — NOT `PASS_RECORDED`); `config.timeout_seconds` confirmed ABSENT from models.py/config.py (would AttributeError — fix correctly avoids it). |
| 15 | Cross-reference accuracy | none | PASS | M4 expected outputs re-derived independently against the real scheduler.py algorithm (not just research prose): diamond `[[A],[B,C],[D]]`, cycle `.unresolved==[A,B,C]` + message string, self-edge/unknown-dep `dependencies_of(...)==[]`, de-dup `[B,C]`, recorded-union declared-then-recorded `[B,C]` — all match scheduler.py:57-119. |

## Self-Audit (mandatory)

1. **Factual claims independently verified against source:** 30+. Including: all 3 source fixes read at their exact lines; process.py terminate/wait/_close_handles contracts (lines 159-244); scheduler.py full algorithm (1-119); models.py TaskStatus/TaskEntry/TaskResult; absence of `config.timeout_seconds`; both M3 call sites; marker registration; all 4 test files in full.
2. **Files read:** `handoff.py`, `executor.py` (4 regions), `process.py`, `scheduler.py`, `models.py`, `test_scheduler.py`, `test_poll_watchdog_ceiling.py`, `test_handoff_store.py` (M3 test), `test_executor.py` (M1 test), all 3 research files, the task file (full), gate-result.md, task-integrity-verdict.md.
3. **Why trust the 0-issue verdict:** I did not merely read the fixes — I **reverted each of the three source fixes in place and re-ran the paired test**, proving each test genuinely catches the bug: M2 warn-mode test HUNG for 60s (timeout-killed, exit 143) on the unbounded pre-fix loop; M1 test failed with `AssertionError: cleanup (terminate) did not run on the exception path (M1)`; M3 test failed with `json.decoder.JSONDecodeError`. Then restored both files and confirmed 18/18 green. This is direct evidence the tests are not trivially passing.
4. **Web research:** None performed (all verification was local-file-bound). N/A for Tavily.

## Regression-Proof Evidence (fail-before / pass-after)

| Fix | Revert applied | Pre-fix result | Post-restore result |
|-----|---------------|----------------|---------------------|
| M2 | loop guard → `while underlying.poll() is None:` | test **HANGS** (60s timeout, exit 143) — genuine infinite spin (no monotonic call in steady-state loop body, so ticks iterator never exhausts) | PASS |
| M1 | removed try/except wrapper | `AssertionError: cleanup (terminate) did not run on the exception path (M1)` | PASS |
| M3 | removed try/except → bare parse | `json.decoder.JSONDecodeError: Expecting property name... (char 34)` | PASS |

## Confidence

- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep/Bash-grep: 12 | Glob: 0 | Bash(run): 9

## Issues Found

None. No issue of any severity.

## Actions Taken

- No in-place fixes required (the work was correct).
- Temporary regression-revert/restore of `executor.py` and `handoff.py` performed for verification only; both files confirmed restored to fixed state (grep-verified `except BaseException` at executor.py:1537 and `except (json.JSONDecodeError, ValueError)` at handoff.py:75) and the touched-test set re-run green (18 passed) after restore.

## Recommendations

- Proceed to the final Post-Completion items: write the Task Summary and flip frontmatter `status` → "🟢 Done" with `completion_date` (the Phase 6 structural gate already recorded PASS, so the Done flip is authorized).

## QA Complete
