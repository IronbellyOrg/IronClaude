# Stage 3 Gate Verdict — rf-qa task-integrity (ADVERSARIAL)

**Date:** 2026-06-03
**Phase:** task-integrity (Stage 3 = Phase 5, Steps 5.1–5.12)
**Mode:** ADVERSARIAL STANCE, fix_authorization: true
**Spec:** SYNTHESIS.md §6 H6 + §7 M2/M4/L4

## VERDICT: **PASS**

Zero real defects found. Every criterion verified against source on disk + executed
tests. The one adversarial "over-launch" observation was disproven (consistent
cross-K reconcile behavior, NOT a regression — see criterion 5). No fixes applied.

---

## Per-criterion checklist

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | `_jsonl` lock (M2) | PASS | `logging_.py:31` `self._jsonl_lock = threading.Lock()` in `__init__` (once per logger); `_jsonl` (:295-301) wraps `open(...,'a'); f.write(line)` in `with self._jsonl_lock`. `write_task_complete` (:226-249) and `write_task_rerun_complete` (:210-224) both route through `_jsonl`. Line format unchanged (`json.dumps(data, default=str)+"\n"`). |
| 2 | `TurnLedger` atomic `try_launch` (H6) | PASS | `models.py:923` RLock created as NON-FIELD attr in `__post_init__`; `debit`/`credit`/`debit_wiring`/`credit_wiring` (:929-999) all `with self._lock`; `try_launch` (:947-962) checks `can_launch()` AND debits under one lock acquisition (RLock reentry into `debit`). **Empirically verified:** `TurnLedger(100)==TurnLedger(100)` → True; `_lock` absent from `dataclasses.asdict()`, absent from `repr`; eq tracks fields (False after `debit(5)`). No `to_dict`/asdict leaks the lock. |
| 3 | Budget gate uses `try_launch` | PASS | Sequential path `executor.py:1280` `if ledger is not None and not ledger.try_launch():`; parallel path `:1100` same. The former `can_launch()`-then-`debit()` pre-debit is gone (comment :1292 "try_launch already debited minimum_allocation"). K=1 skip/debit semantics preserved (see criterion 5). |
| 4 | DAG scheduler reuse (H6) | PASS | `scheduler.dependencies_of` (:41-71) reproduces `rerun_tasks._dependencies_of` (:438-451) union SHAPE: declared `TaskEntry.dependencies` ∪ recorded `TaskResult.task.dependencies`, order-preserving + de-duped, intra-set filtered, self-edges dropped. `scheduler.is_task_satisfied` (:109-121) mirrors `_is_satisfied` (:453-460) tri-state via `status.is_success`. `topological_launch_order` adds the wave wrapper (not a fresh parser). Cycles → `CycleError` (:95-101), never silently dropped; tasks ordered after deps. |
| 5 | K==1 byte-identical (CRITICAL) | PASS | Dispatch guard `executor.py:1220` `if task_parallelism > 1 and len(tasks) > 1:` — K=1 (or single-task) falls through to the unchanged sequential loop. Sequential calls `_run_one_task(..., lock=None)` (:1327); `_run_one_task` uses `contextlib.nullcontext()` when `lock is None` (:997) — no locking, identical to former inline block. **Empirically verified byte-identical:** K=1 and K=4 on the SAME 10-task/budget-15 setup both yield (10 passed, 0 skipped, consumed=50, 0 remaining). K=1 per-task tests (`test_executor.py`) green (the 5 failures there are baseline `.stdin` harness doubles). |
| 6 | No raw daemon threads / context-managed pool | PASS | `executor.py` audit: only `ThreadPoolExecutor` use is `:1155` `with ThreadPoolExecutor(max_workers=k) as pool:` (context-managed, joined on exit). No `Thread(`, no `daemon=True`. Shared mutations (env-capture :1111-1113, reconcile+hooks via `_run_one_task(lock=...)` :1114-1125, TUI :1143-1147) all lock-guarded. Handoff writes target distinct per-task files (`handoff_file` `phase-{N}-task-{id}.json`), atomic temp+replace (`handoff.py:56-60`). Test `test_executor.py::..._no_leaked_daemon_threads_in_executor` passes. |
| 7 | ≥4-writer/≥1000-run race test (M2) | PASS | `test_handoff_concurrency.py`: 4 threads × 300 = 1200 writes through guarded `_jsonl`; asserts exact line count (1200), every line `json.loads`-parses (catches tearing), payload multiset identical. Comment correctly notes it would FAIL against the lock-free writer. **Executed: 1 passed.** |
| 8 | TOCTOU test | PASS | `test_turn_ledger_concurrency.py`: 400 concurrent `try_launch` on a 20-launch budget (16 workers) → asserts EXACTLY 20 granted, `consumed == 20*5`, `available() < minimum` (no over-commit). **Executed: 1 passed.** |
| 9 | Wall-clock + DAG/resume (L4) | PASS | `test_handoff_performance.py`: (a) K=4 vs serial with 0.2s mock asserts `parallel < 0.5*serial`; (b) in-flight dependency (no handoff record) on resume → dependent `T01.02` launches strictly AFTER its unsatisfied dep `T01.01` (`launched.index(...)` ordering assertion), and the dep is NOT skipped (no validated-success record → runs). **Executed: 2 passed.** |
| 10 | No-regression | PASS | **Independently proven.** Ran `tests/sprint/ + isolation_layers_probe + test_sprint_wiring`: **1068 passed, 54 failed, 0 skipped** (matches summary exactly). `comm` set-diff of current-failures vs `pre-change-baseline.txt` (54 vs 54): **empty in BOTH directions** → ZERO new regressions, ZERO newly-fixed. Spot-checked failure cause = `'_WarnPopen' object has no attribute 'stdin'` (pre-existing harness-double, Path A single-session, NOT per-task code). NONE of the 54 are scheduler/parallel/concurrency tests. `make lint`: "All checks passed!". The 2 intentionally-updated assumption tests (`--budget`→`--max-turns` in `build_resume_output`; threading-absence→no-leaked-daemon) verified CORRECT: `models.py:1041` emits `--max-turns`; daemon test asserts no raw `Thread(`/`daemon=True` + `with ThreadPoolExecutor`, matching actual executor source. Both pass. |

---

## Adversarial probes performed (and their disposition)

1. **Suspected budget over-launch under K>1.** Observed 10 tasks PASS on a 15-turn
   budget (consumed=50). **Disproven as a defect:** K=1 produces the IDENTICAL
   (10, 0, 50, 0) outcome. Root cause is the pre-existing reconcile-credit model in
   `_run_one_task:999-1005` — a task consuming fewer turns than `minimum_allocation`
   credits the difference back, replenishing budget for later launches. This is
   consistent cross-K behavior (criterion 5 holds), and the TOCTOU primitive itself
   is correct in isolation (criterion 8). Not a regression; no fix warranted.

2. **Race on shared ledger in parallel path.** Confirmed the SPAWN (factory/real)
   runs BEFORE the lock (`_run_one_task:979-984`) and the ledger reconcile + hooks
   run UNDER `guard` (:997-1025). With `lock` supplied (K>1) the reconcile/hooks are
   serialized; with `lock=None` (K=1) `nullcontext`. No unguarded shared mutation.

3. **Determinism under K>1.** Results assembled in declared task order, not completion
   order (`_execute_phase_tasks_parallel:1166`). Empirically: K=4 result order ==
   declared order; no duplicate result ids; one result per task.

4. **DAG reuse authenticity.** Verified `scheduler.*` actually mirrors
   `rerun_tasks._dependencies_of`/`_is_satisfied` rather than re-parsing — read both.

## Fixes applied

None. No real defect found.

## No-regression note

54 failures == 54 baseline failures, provably identical node-id set (empty symmetric
diff). All are pre-existing `_WarnPopen.stdin` / IndexError harness doubles on the
Path A single-session fallback. Zero failures in any code this stage touched. Lint clean.

## Confidence

Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 12 | Grep/Bash: 11 | Glob: 0

## QA Complete
