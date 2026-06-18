---
status: success
tier_reached: 1
type: bug
confidence: 0.95
scope: src/superclaude/cli/sprint/
---

# Troubleshoot Report — Phase 5/6 "error without running tasks" = global turn-budget exhaustion

## Summary

The phases did **not** fail on dependency resolution or the scheduler. The unrun tasks are recorded
`status=skipped, turns=0`, which is set by exactly one mechanism — the **`TurnLedger` budget gate**.
The sprint's **global** turn budget (`max_turns × num_active_phases`) was exhausted right after phase-5
task T05.01, so every subsequent task was `SKIPPED`, and skipped tasks make `aggregate_task_results`
report the phase as `error`. The originally-suspected dependency/scheduler bug is **refuted** by the
`skipped`/`turns=0` evidence.

## Diagnosis (confidence 0.95, single-domain: budget model)

- The ledger is sized **once, globally**, before the phase loop:
  `ledger = TurnLedger(initial_budget=config.max_turns * len(config.active_phases))` — `executor.py:1651-1653`.
- The run was `--start 4 --max-turns 100` → `active_phases = {4,5,6}` (3) → **initial_budget = 100 × 3 = 300 turns.**
- The per-task launch gate atomically debits/refuses against this one pool:
  `if ledger is not None and not ledger.try_launch(): return TaskResult(status=SKIPPED…)` — `executor.py:1119-1130`
  (and the sequential mirror at `executor.py:1097-1104`). `try_launch` returns False when
  `available() = initial_budget − consumed + reimbursed < minimum_allocation` — `models.py:938,956,960-975`.
- **The arithmetic matches the observed cutoff exactly.** Cumulative turns from the execution log:
  `T04.01=22 + T04.02=78 + T04.03=90 + T04.04=36 + T04.05=16 + T05.01=67 = 309`. At 309 > 300 the pool is
  negative, so T05.02/03/04 skip (phase 5 → error) and at phase 6 the pool is already exhausted → all 5
  tasks skip in 0.0006 s (phase 6 → error). `aggregate_task_results` (`executor.py:327-368`) counts the
  skips, so `tasks_passed < tasks_total` → phase status `error`.

**Why this is a real defect, not just "use a bigger number":** `max_turns × num_phases` budgets `max_turns`
*per phase* — correct for the legacy one-subprocess-per-phase model. The **per-task path spawns N subprocesses
per phase**, each able to consume up to `max_turns`. Here a single phase burned **242 turns** against its
100-turn share, starving all later phases from one global pool. The CLI help even documents `--max-turns`
as "Max agent turns **per phase**", which the per-task global pool contradicts. The failure also surfaces
misleadingly as "phase error" instead of "budget exhausted".

## Evidence

- `results/phase-5-result.json` → `T05.01: pass (67 turns)`, `T05.02/03/04: skipped (0 turns)`; phase `status=error`.
- `results/phase-6-result.json` → `T06.01..T06.05: skipped (0 turns)`; phase `status=error`; `duration 0.0006 s`.
- `execution-log.jsonl` → per-task `turns` (22/78/90/36/16/67) summing to 309 before the first skip.
- `src/superclaude/cli/sprint/executor.py:1651-1653` — `initial_budget = config.max_turns * len(config.active_phases)` (global, created before the `for phase in config.active_phases` loop at `:1728`).
- `src/superclaude/cli/sprint/executor.py:1119-1130` — `try_launch()` False → `TaskStatus.SKIPPED` + added to `remaining`.
- `src/superclaude/cli/sprint/models.py:906-975` — `TurnLedger.available()/can_launch()/try_launch()`.
- `src/superclaude/cli/sprint/executor.py:327-368` — `aggregate_task_results` counts skipped → phase `error`.

## Proposed Fix (not applied — diagnose-only; no --fix)

**Immediate workaround (no code change):** raise the budget so the global pool covers all tasks. Empirically
this sprint averages ~50 turns/task across ~4–5 tasks/phase, so budget ≈ `tasks × 60`. For the 3-phase
window that is ~`--max-turns 500` (→ pool 1500). Re-run the unfinished phases:
`superclaude sprint run <index> --start 5 --max-turns 500` (phase 4 already passed).

**Code fix (recommended) — size the per-task ledger by task count, not phase count.** In `execute_sprint`
(`executor.py:1651`), when phases use the per-task path, base the budget on the **total task inventory**, e.g.
`initial_budget = config.max_turns * total_task_count` (sum of `_parse_phase_tasks` lengths across active
phases), or **reset/allocate the ledger per-phase** (`max_turns` per phase, fresh each iteration) so one heavy
phase cannot starve later phases. Either aligns the pool with the documented "per phase" semantics of
`--max-turns`.

**Secondary (observability):** when a phase ends with budget-skipped tasks, surface "phase N halted: turn
budget exhausted (consumed X / budget Y), Z tasks skipped" instead of a bare `error`, so the cause is not
mistaken for a logic/dependency failure (the `AggregatedPhaseReport` already carries `remaining_task_ids`
and `budget_remaining` — `executor.py:280-282,364`).

## Risk + Rollback

- Workaround is zero-risk (a flag value).
- The code fix changes budget sizing only; guard with a test asserting a 3-phase × 5-task sprint at
  `--max-turns 100` yields a pool that lets every task launch (no spurious SKIPPED), and that the legacy
  per-phase path budget is unchanged.

## Next Steps

- Re-run with a larger `--max-turns` to complete phases 5–6 now.
- To land the code fix: re-invoke `/sc:troubleshoot … --fix` (Tier 3 builds an MDTM task), or hand the
  "size per-task ledger by task count / reset per-phase" change to `/sc:task`.

## Grounding Gaps

None — every citation re-Read against the working tree; the cumulative-turn arithmetic (309 vs 300) is
derived directly from `execution-log.jsonl`.
