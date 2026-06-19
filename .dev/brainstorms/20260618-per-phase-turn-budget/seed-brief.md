---
topic: "Design a per-phase turn-budget model for the sprint runner so each phase gets its OWN independent budget that resets at phase end, sized by that phase's task count — replacing today's single global pool that lets one heavy phase starve later ones."
domain: architecture
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-06-18T14:19:29Z
anchors_verified_in: worktree/perPhaseturnBudget (HEAD = origin/master)
anchors_note: "All file:line anchors in the originating topic were drifted (diagnosed on branch worktree-segfault-repro). Anchors below are re-verified against THIS worktree."
---

# Seed Brief: per-phase turn-budget model

## Problem Statement

The sprint runner allocates a **single global turn budget** for an entire sprint and
shares it across all phases. One heavy early phase can consume turns that later phases
need, so later phases' tasks are gated out (`SKIPPED`) and then mis-reported as `error`.
We want each phase to receive its **own independent budget, sized by that phase's task
count, that resets at the phase boundary**, so no phase can starve another — while
preserving documented `--max-turns` semantics and the legacy single-subprocess
(non-task) phase path.

## Known Context (verified against this worktree)

**Root cause — global ledger built once, before the loop:**
- `executor.py:1777-1780` — `ledger = TurnLedger(initial_budget=config.max_turns * len(config.active_phases), reimbursement_rate=0.8)` is constructed **once**, before the phase loop.
- `executor.py:1813` — `for phase in config.active_phases:` the loop never re-allocates or resets the ledger.
- The same `ledger` instance is threaded into the per-task path: `execute_phase_tasks(..., ledger=ledger, ...)` at `executor.py:1856-1867` (the `ledger=ledger` kwarg is line **1860**).

**Where the pool drains (per-task gates):**
- Parallel path (K>1): `_execute_phase_tasks_parallel._worker` (def `executor.py:1158`, worker `1206`) gate at `executor.py:1231` — `if ledger is not None and not ledger.try_launch():` → `status=TaskStatus.SKIPPED` at `1235`.
- Sequential path (K=1): `execute_phase_tasks` body gate at `executor.py:1424` — same `try_launch()` → `SKIPPED` at `1430`.
- `try_launch()` (`models.py:956-971`) atomically `can_launch()`-then-`debit(minimum_allocation)` under an RLock; returns False without debiting when `available() < minimum_allocation` (=5).

**How SKIPPED becomes error:**
- `aggregate_task_results` (def `executor.py:335`) counts `remaining` / SKIPPED tasks; for a phase with un-attempted tasks the phase report is no longer `PASS` → mapped to `PhaseStatus.ERROR` at `executor.py:1881-1882`.

**Phase task inventory source:**
- `_parse_phase_tasks(phase, config)` (def `executor.py:1677`) is already called per-iteration at `executor.py:1838` and returns `list[TaskEntry] | None`. `len(tasks)` for the current phase is therefore already available at phase entry — this is the natural sizing input.

**TurnLedger model (`models.py:901-1014`):**
- Fields: `initial_budget`, `consumed=0`, `reimbursed=0`, `reimbursement_rate=0.8`, `minimum_allocation=5`, `minimum_remediation_budget=3`, plus wiring fields `wiring_turns_used=0`, `wiring_turns_credited=0`, `wiring_budget_exhausted=0`, `wiring_analyses_count=0`.
- `available() = initial_budget - consumed + reimbursed`.
- Has a non-field `_lock` (RLock) created in `__post_init__`.
- Wiring methods: `debit_wiring`, `credit_wiring` (floor-to-zero `int(turns*rate)`), `can_run_wiring_gate`. Wiring hook runs post-phase via `run_post_phase_wiring_hook(..., ledger=ledger)` at `executor.py:1911-1917`.
- Per-task reimbursement: in the task helper, `ledger.credit(int(task_result.turns_consumed * ledger.reimbursement_rate))` (around `executor.py:921-927`).

**CLI semantics (must preserve):**
- `commands.py:92` — `--max-turns` help is **"Max agent turns per phase (default: 100)"**. The documented unit is *per phase*; the global pool (`max_turns × phase_count`) is the runtime that diverges from the doc.

**Legacy non-task path:**
- When `_parse_phase_tasks` returns falsy, the phase falls through to the single-`ClaudeProcess` (legacy) path below `executor.py:1839 if tasks:`. The legacy path's interaction with the ledger must remain behaviorally unchanged.

**Empirical failure:** max_turns=100 × 3 phases = 300-turn pool; phases 5/6 errored after 309 cumulative turns were spent by earlier phases.

## Constraints

- C1. Preserve documented `--max-turns` = "Max agent turns per phase" semantics (no CLI flag/help change required by the fix).
- C2. Preserve legacy single-subprocess (non-task) phase behavior unchanged.
- C3. Thread-safety: the budget is mutated by K>1 parallel workers under `_lock`; any reset/re-alloc must not break the RLock invariant or introduce a race.
- C4. Monotonicity of `consumed` is currently a documented invariant *within a ledger*; a reset crosses that boundary and must be deliberate, not an accident.
- C5. Wiring-analysis budget fields and reimbursement/credit must have a defined fate across a reset (carry over vs. reset to zero).
- C6. Minimal blast radius: `ledger` is referenced at ~25 sites in executor.py; the design should localize the change (ideally the construction site + loop) rather than re-plumb every call.

## Success Criteria

- S1. A 3-phase × ~5-task sprint at `--max-turns 100` launches **every** task (zero spurious SKIPPED) — the regression test.
- S2. No phase's consumption can reduce another phase's available budget (starvation impossible by construction).
- S3. Each phase's budget = `max_turns × (task count of THAT phase)` (task phases), resolved from `_parse_phase_tasks` for that phase.
- S4. Legacy non-task phase path unchanged (byte-equivalent execution log where applicable).
- S5. Wiring + reimbursement semantics behave per an explicit, documented decision across the reset.
- S6. Change is testable with unit + integration coverage and a defined per-phase budget assertion.

## Open Questions (the decisions proposals must converge on)

- Q1. **Reset mechanism**: construct a *fresh* `TurnLedger` per loop iteration vs. add a `reset()`/`reallocate()` method that mutates the existing instance in place. (Trade: clean state + GC of `_lock` vs. preserving cross-phase telemetry accumulation.)
- Q2. **Sizing timing**: size lazily at phase entry from the current phase's `len(tasks)` (the value already computed at `executor.py:1838`) vs. precompute all phases upfront. (Lazy avoids double-parsing and handles dynamic inventories; upfront enables a pre-flight total.)
- Q3. **Legacy path budget**: what `initial_budget` does a non-task phase's ledger get? (e.g., `max_turns × 1`, since the legacy path launches one subprocess) — and does the legacy path even consult the ledger today?
- Q4. **Reimbursement/credit fate on reset**: reset `reimbursed`/`consumed` to 0 each phase (true independence) — confirm this is the intent and that no cross-phase credit carryover is expected.
- Q5. **Wiring fields fate on reset**: reset wiring counters per phase vs. accumulate across the sprint for end-of-sprint telemetry. (Post-phase wiring hook at `1911` runs *within* a phase, so it should see that phase's ledger.)
- Q6. **Where to place the reset**: top of the loop body (`after 1813`, before the skip/python/task branches) vs. only on the task branch (`at 1839`). Python/skip-mode phases launch no subprocess — do they need a ledger at all?
- Q7. **Aggregate/halt interplay**: with per-phase budgets sized to task count, can the budget gate ever legitimately SKIP a task (and thus produce a non-PASS phase), or does correct sizing make the gate a pure safety net? Define expected behavior when a single task overspends its `max_turns`.
