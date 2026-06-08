# Shared-State Inventory (Step 5.1, before the Stage-3 scheduler)

Enumerates every shared mutable touched in the `execute_phase_tasks` per-task loop
(and the lock-free `_jsonl` writer), per SYNTHESIS H6. Stages 0-2 rely on the
**sequential single-writer invariant**; Stage 3 (K>1) breaks it, so each object
below needs single-writer discipline, a lock, or a per-worker copy + merge.

Anchored against the live source at execution time (line numbers drift; anchor by
symbol). All sites verified by grep/Read; none fabricated.

| Shared object | Mutated at (symbol + line) | Read-modify-write? | Required Stage-3 discipline |
|---|---|---|---|
| `results: list[TaskResult]` | `execute_phase_tasks` — `results.append(...)` at the budget-skip (executor.py:1022), budget-skip loop (:1041), resume-skip append, and the main per-task append after hooks (~:1100) | append (order-sensitive under K>1) | Per-worker local result + ordered merge at join, OR a lock around append. Final order must follow the scheduler's launch order, not completion order. |
| `remaining: list[str]` | `remaining = [t.task_id for t in tasks[i:]]` on budget exhaustion (executor.py:1039) | assignment (loop-position dependent) | Compute under the ledger lock / at the join barrier; "remaining" loses meaning under concurrent launch, so derive it from the set of unlaunched/undebited tasks, not loop index `i`. |
| `gate_results: list[TrailingGateResult]` | `gate_results.append(gate_result)` (~executor.py:1097) | append | Per-worker collect + merge, OR lock (same as `results`). |
| TUI state (`tui.update`, `_tui_state`) | `tui.update(sprint_result, _tui_state, phase)` per task (executor.py:1056-1061) | external mutation of shared TUI/`sprint_result` | Marshal TUI updates through a single lock (or a single UI thread); concurrent `tui.update` from K workers must not interleave render state. |
| `shadow_metrics: ShadowGateMetrics` | mutated inside `run_post_task_anti_instinct_hook` (called per task) | counter increments (RMW) | Lock around the hook's metric mutation, OR per-worker metrics + merge. |
| `remediation_log: DeferredRemediationLog` | mutated inside `run_post_task_wiring_hook` (called per task) | append/RMW + persists to `remediation.json` | Lock around the hook's log mutation + its file write. |
| `sprint_result: SprintResult` | read + passed to `tui.update` (executor.py:1061); phase_results appended in `execute_sprint` | read here; mutated in caller | Treat as read-only inside the per-task loop; guard via the TUI lock. |
| `SprintLogger._jsonl` | `open(self.config.execution_log_jsonl, "a"); f.write(...)` (logging_.py:290-291) — **lock-free** | append (non-atomic interleave/tear under K>1) | **threading.Lock per SprintLogger (Step 5.2).** Covers ALL events incl. the Stage-0/1 `write_task_complete` writer and `write_task_rerun_complete`. |
| `TurnLedger` (`consumed`/`reimbursed`) | `debit` (models.py:916-920), `credit` (:922-926); check-then-act `can_launch` (:928) → `debit` (executor.py:1053) | yes — `+=`; **TOCTOU spans can_launch→debit** | **threading.Lock + atomic `try_launch()` (Step 5.3-5.4).** Per-method guards are insufficient; check-and-debit must be one atomic op. |
| `logger.write_task_complete` (Stage 0/1 writer) | routes through `_jsonl` (executor.py per-task write block) | n/a (delegates) | Covered transitively by the `_jsonl` lock (Step 5.2) — explicitly in scope per H6/M2. |
| `handoff_store.write` (Stage 1 writer) | `FileHandoffStore.write` → atomic temp+replace to `phase-{N}-task-{id}.json` | per-task SEPARATE file | **No shared-state hazard:** each task writes its own distinct file via atomic temp+replace; concurrent writers target different paths. No lock needed. |

## Summary of required disciplines

1. **`_jsonl` → per-logger `threading.Lock`** (Step 5.2) — covers all events including `write_task_complete`.
2. **`TurnLedger` → lock + atomic `try_launch()`** (Step 5.3) and switch the gate to it (Step 5.4) — fixes the can_launch→debit TOCTOU.
3. **`results`/`gate_results`/`remaining` → per-worker collect + ordered merge** (or a lock) in the K>1 path (Step 5.7); K=1 keeps the unchanged sequential path.
4. **TUI / `shadow_metrics` / `remediation_log` → lock** around their per-task mutations under K>1.
5. **`handoff_store.write` → already safe** (per-task distinct files, atomic temp+replace).
