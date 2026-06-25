# R-9 Thread-Safety Confirmation (K>1) — Step 2.8

**Task:** TASK-RF-per-phase-turn-budget-20260618-160752
**Date:** 2026-06-18
**Scope:** Verification only — R-9 requires NO code change beyond the K-2 construction-site comment added in Step 2.3. No concurrency logic was altered.

## Anchors observed (live, post-Phase-2 edits)

| Concern | File:line (current) | Evidence |
|---|---|---|
| Serial phase loop | `executor.py:1873` | `for phase in config.active_phases:` — phases iterate one at a time |
| Per-phase ledger constructed in PARENT thread | `executor.py:1920` | `ledger = TurnLedger(initial_budget=config.max_turns * (len(tasks) if tasks else 1), reimbursement_rate=0.8)` — runs in the loop body (parent thread), before any worker is spawned |
| K-2 invariant comment present | `executor.py:1912` | `# K-2 SEQUENTIAL-PHASE INVARIANT (load-bearing precondition for R-9):` (added Step 2.3) |
| Ledger passed to fan-out | `executor.py:1941` | `task_results, remaining, phase_gate_results = execute_phase_tasks(... ledger=ledger ...)` — the fully-built ledger is handed to the executor that fans out workers |
| Parallel fan-out entry | `executor.py:1196` | `def _execute_phase_tasks_parallel(` |
| Worker body | `executor.py:1244` | `def _worker(task, prior_context):` — each worker calls `ledger.try_launch()` under the ledger's RLock |
| Synchronous wave join | `executor.py:1333` | `with ThreadPoolExecutor(max_workers=k) as pool:` followed by `wave_out = list(pool.map(...))` — the `with` block exits only after every worker in the wave completes (`list(...)` forces materialization); the pool is joined before the next wave and before the function returns |
| RLock created before publication | `models.py:1036`, `models.py:1042` | `def __post_init__(self) -> None:` → `self._lock = threading.RLock()` — the lock exists the moment the dataclass is constructed, i.e. before the ledger is published to any worker |

## Join / sequence argument (F-C5 Sequence Attack)

1. **Construction precedes fan-out.** The per-phase `ledger` is built at `executor.py:1920` in the parent thread, fully initialized (including its RLock via `__post_init__` at `models.py:1042`), BEFORE it is passed to `execute_phase_tasks` at `executor.py:1941`. No worker can observe a half-built ledger.
2. **Each wave is synchronously joined.** Inside `_execute_phase_tasks_parallel`, every wave runs under `with ThreadPoolExecutor(max_workers=k) as pool:` (`executor.py:1333`) with `list(pool.map(...))`. The context-manager exit joins all worker threads; `list()` forces all results. The function returns only after the final wave is joined.
3. **Next phase waits for prior phase return.** Because the phase loop at `executor.py:1873` is serial, the next iteration's ledger construction (`executor.py:1920`) cannot run until the current `execute_phase_tasks` has returned — i.e. until all of this phase's workers are joined. **No straggler worker survives into the next phase**, and no phase ever shares a ledger with another.
4. **Within a phase, mutation is RLock-guarded.** `try_launch`/`debit`/`credit`/`debit_wiring`/`credit_wiring` all mutate under `self._lock` (RLock, reentrant so `try_launch` can call the already-guarded `debit`), so concurrent workers under K>1 cannot over-admit (this is exactly what TM-12 pins).

## K-2 invariant

The K-2 sequential-phase invariant is stated at the construction site (`executor.py:1912`, added in Step 2.3): the K>1 safety holds **only** because phases run serially with intra-phase fan-out; if a future change overlaps phases, the per-phase ledger would need explicit per-phase ownership.

## Verdict

**CONFIRMED.** The per-phase ledger model is thread-safe under K>1: built-before-publish, RLock-before-publication, synchronously joined per wave, and serially sequenced across phases. No code change required beyond the Step 2.3 K-2 comment, which is present.
