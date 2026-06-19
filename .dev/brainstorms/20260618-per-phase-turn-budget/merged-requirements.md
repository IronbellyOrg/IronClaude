---
title: "Per-Phase Turn-Budget Model for the Sprint Runner — Merged Requirements"
domain: architecture
strategy: systematic
status: design-only
adversarial_status: converged
convergence_note: "3 proposals (minimal-blast architect / clean-model refactorer / test-invariant QA) reconciled. Central decision: fresh-construct per phase. A load-bearing claim shared by 2 of 3 proposals (legacy path never touches the ledger) was FALSIFIED during merge verification — see D-3 / R-6."
anchors_verified_in: "worktree/perPhaseturnBudget (HEAD = origin/master), 2026-06-18"
created: 2026-06-18T14:25:00Z
handoff_target: "/sc:task"
source_brief: ".dev/brainstorms/20260618-per-phase-turn-budget/seed-brief.md"
---

# Per-Phase Turn-Budget Model — Merged Requirements (Design Only)

> **Do not implement from this section without re-confirming anchors.** Every `file:line` below was
> verified against this worktree on 2026-06-18, but line numbers drift. Re-`Read` each anchor at edit time.

## 1. Problem (one paragraph)

`run_sprint` builds **one** `TurnLedger` before the phase loop with
`initial_budget = config.max_turns * len(config.active_phases)` (`executor.py:1777-1780`) and shares that
single pool across every phase. `--max-turns` is documented as **"Max agent turns per phase"**
(`commands.py:92`), so the global pool diverges from the documented unit: a heavy early phase drains turns
later phases need. Once the pool nears empty, the per-task budget gate `try_launch()` returns False
(`executor.py:1231→1235` parallel, `1424→1430` sequential), later tasks are recorded `SKIPPED`,
`aggregate_task_results` (`executor.py:335`) counts them, and the phase is mapped to `PhaseStatus.ERROR`
(`executor.py:1881-1882`). Empirically: `max_turns=100 × 3 phases = 300`-turn pool; phases 5/6 errored after
309 cumulative turns.

## 2. Converged Design Decisions (Q1–Q7)

| # | Decision | Rationale | Origin |
|---|----------|-----------|--------|
| **Q1 — reset mechanism** | **Fresh `TurnLedger` constructed per phase** (NOT an in-place `reset()` method). | A new object makes per-phase independence structural (`id` differs, all fields zero by construction). It *dissolves* the three constraint-risks C3/C4/C5 instead of mitigating them: no mid-reset race, no in-place monotonicity violation, no field-fate ambiguity. No new model API on `TurnLedger`. | A + C (over B) |
| **Q2 — sizing timing** | **Lazy, at phase entry**, from `len(tasks)` already computed by `_parse_phase_tasks` at `executor.py:1838`. | Single source of truth; no upfront re-parse; no second derivation to keep in sync. | A + B + C |
| **Q3 — legacy path budget** | Legacy (non-task) phase gets a fresh ledger sized **`max_turns × 1`**. The ledger **is** consulted on the legacy path (see D-3) — it must be bound. | One subprocess ⇒ one task-equivalent of budget; keeps the wiring hook's per-phase input self-consistent and prevents a `NameError`. | merge synthesis |
| **Q4 — reimbursement/credit on reset** | `consumed` and `reimbursed` start at **0 every phase** (free, by fresh construction). No cross-phase credit carryover. | Carryover is exactly the coupling we are removing (S2). | A + B + C |
| **Q5 — wiring fields on reset** | Wiring counters (`wiring_turns_used/credited/analyses_count`, `wiring_budget_exhausted`) start at **0 every phase**. **No sprint-level accumulator is added.** | Verified: nothing reads sprint-cumulative `wiring_*` or `ledger.available()` after the loop (only in-function reads at `executor.py:390` and `949`). An accumulator would be dead code. | C (corrected) |
| **Q6 — reset placement** | Construct the fresh ledger **after the python/skip `continue` guards and after `tasks = _parse_phase_tasks(...)` at `executor.py:1838`, before the `if tasks:` branch at `1839`** — so it covers BOTH the task branch and the legacy fall-through. | python/skip phases `continue` earlier and never reference a ledger; both the task path (`ledger=` @1860) and the legacy path (`ledger=` @2285) require a bound, fresh ledger. | merge synthesis (A's "above branches" + B/C's "lazy at 1838") |
| **Q7 — gate semantics** | The gate becomes a **pure safety net**. With sizing = `max_turns × task_count` and per-launch reconciliation to actual turns (`executor.py:1126-1131`), the pool exactly covers N tasks each consuming up to `max_turns`. A legitimate SKIP can only occur if tasks collectively overspend `max_turns × N` — a real anomaly, never phase ordering. | Distinguishes "correctly sized, never fires" from "fired on real overspend"; makes the global-pool bug un-reintroducible. | B + C |

## 3. Key Merge-Verification Findings (why this design beats each single proposal)

- **D-1 (sizing is exact, not generous).** `try_launch` debits `minimum_allocation = 5` at launch, then the
  task helper reconciles to actual turns: `if actual > pre_allocated: ledger.debit(actual - 5) elif actual < 5:
  ledger.credit(5 - actual)` (`executor.py:1126-1131`). So the pool drains by **actual** consumption. Sizing
  `max_turns × task_count` therefore lets each task consume up to its full `max_turns` share — exactly the
  documented semantics — and the gate only fires on genuine overspend.
- **D-2 (no accumulator).** `grep` for post-loop reads of `wiring_turns_*` / `ledger.available` returns only
  `executor.py:390` (`check_budget_guard`, takes ledger as a param) and `949` (task helper, param). The ledger
  is a local in `run_sprint`, never returned. ⇒ Proposals A & B's sprint-wiring accumulators are unnecessary.
- **D-3 (legacy path DOES consult the ledger — falsifies B & C).** Proposals B and C both asserted "the legacy
  path never consults the ledger." **False.** The legacy claude-mode path calls
  `run_post_phase_wiring_hook(phase, config, phase_result, ledger=ledger, ...)` at **`executor.py:2281-2287`**
  (the `ledger=ledger` kwarg is line **2285**). That hook reads/mutates the ledger
  (`can_run_wiring_gate`/`debit_wiring`/`credit_wiring`, `executor.py:530-662`). Consequence: Proposal C's
  "delete the pre-loop construction, build only on the task branch" would raise `NameError` on every legacy
  phase. The converged placement (Q6) binds a fresh ledger for legacy phases too, fixing this.

## 4. Requirements (R-items)

> Format: anchor → behavioral change (prose, no code dumps) → verification.

### R-1 — Remove the global pre-loop ledger construction
- **Anchor:** `executor.py:1777-1780` (`ledger = TurnLedger(initial_budget=config.max_turns * len(config.active_phases), reimbursement_rate=0.8)`).
- **Change:** Delete this construction. **Leave the adjacent pre-loop infrastructure in place** —
  `shadow_metrics` (`1782`), `remediation_log` (`1786-1788`), `SprintGatePolicy(config)` (`1793`),
  `all_gate_results` (`1796`) all legitimately accumulate across phases and must NOT move into the loop.
- **Verification:** `grep "len(config.active_phases)"` no longer appears in any ledger construction. Confirm
  no reference to `ledger` exists between `1780` and the new construction point (`1838`) — verified clean today.

### R-2 — Construct a fresh, phase-sized ledger at the tasks-resolution point
- **Anchor:** `executor.py:1838-1839` (immediately after `tasks = _parse_phase_tasks(phase, config)`, before `if tasks:`).
- **Change:** Construct `ledger = TurnLedger(initial_budget=config.max_turns * (len(tasks) if tasks else 1), reimbursement_rate=0.8)`.
  This single statement runs once per task-or-legacy phase, sizing the pool to that phase's own work, and binds
  `ledger` for both downstream branches. Placement is **after** the python/skip `continue` guards
  (`1819-1834`) so those phases never construct or reference a ledger.
- **Verification:** Integration test captures the `ledger` handed to each phase; assert
  `initial_budget == config.max_turns * len(tasks)` (task phases) / `== config.max_turns` (legacy phases), and
  object identity differs across phases (R-4/TM-1, TM-2).

### R-3 — Per-phase available budget == `max_turns × task_count` at every phase entry (core invariant)
- **Anchor:** sizing input `executor.py:1838`; `available()` formula `models.py:934-936`.
- **Change:** At entry to `execute_phase_tasks` (`executor.py:1856`), `ledger.available() == config.max_turns * len(tasks)`
  and `ledger.consumed == 0`, independent of any earlier phase.
- **Verification:** The mandatory regression (TM-0) asserts `available() == 500` at entry to each of 3 phases at `--max-turns 100`.

### R-4 — Independence by construction (reimbursement + wiring start at zero each phase)
- **Anchor:** `TurnLedger` field defaults `models.py:914-924`; fresh construction from R-2.
- **Change:** Because each phase builds a new ledger, `consumed`, `reimbursed`, and all four wiring fields begin
  at their dataclass defaults (0). No in-place mutation, no field-fate special-casing. **No sprint-level wiring
  accumulator is introduced** (D-2).
- **Verification:** Unit assert a freshly constructed ledger reports `consumed==0, reimbursed==0, wiring_*==0`;
  integration assert phase 2's ledger is unaffected by phase 1 reimbursement/wiring (TM-5, TM-10).

### R-5 — Gate unchanged in code; redefined as safety net
- **Anchor:** parallel gate `executor.py:1231→1235`, sequential gate `executor.py:1424→1430`; per-launch reconciliation `executor.py:1126-1131`.
- **Change:** **No code change to the gate.** With R-2 sizing it can no longer fire from phase ordering. Update
  the nearby comment/log string to read "phase budget exhausted" rather than implying a sprint-level limit.
- **Verification:** TM-0 asserts the SKIPPED branch is never taken in phases 2–3 under a non-exhausting budget;
  TM-9 asserts it still fires on a forced single-phase overspend (safety net intact).

### R-6 — Legacy non-task path: subprocess behavior unchanged; ledger input becomes per-phase (intended, documented)
- **Anchor:** legacy branch `executor.py:1939-2287`; wiring-hook call `executor.py:2281-2287` (`ledger=ledger` @2285).
- **Change:** The legacy single-`ClaudeProcess` execution path (isolation dir, `SessionResetPolicy`, launch,
  monitor, `PhaseResult` assembly) is **byte-equivalent unchanged**. The ONLY delta: its post-phase wiring hook
  now receives a fresh `max_turns × 1` ledger instead of the cumulative global pool. This is a **deliberate
  refinement** — under the old bug, late legacy phases could see a near-empty pool and silently skip wiring
  analysis (`can_run_wiring_gate` requires `available() >= 3`); per-phase sizing restores intended wiring
  behavior. Document this delta inline at the construction site and in the wiring hook's docstring.
- **Verification:** Characterization test pins the legacy **subprocess execution log** (phase order,
  `PhaseStatus`, `exit_code`) as unchanged (TM-7). A separate test asserts a legacy phase **following** a task
  phase does not `NameError` and receives a fresh `max_turns × 1` ledger (TM-8 — the regression guarding D-3).

### R-7 — Monotonicity (C4) preserved within a phase; reset is an object boundary, not an in-place mutation
- **Anchor:** `debit` monotonicity `models.py:938-943`; class docstring `models.py:902-912`.
- **Change:** No change to `debit`/`credit`/`try_launch`. Because there is no in-place reset, `consumed` never
  decreases on a live instance — the documented within-ledger monotonicity invariant is never crossed. Optionally
  tighten the docstring to say monotonicity is per-instance (i.e., per-phase).
- **Verification:** Unit assert `TurnLedger` exposes no `reset`/`reallocate` mutator (guards Q1 against a future
  contributor reintroducing an in-place reset); pair with the existing monotonicity test (TM-6).

### R-8 — python/skip-mode phases never construct or touch a ledger
- **Anchor:** `executor.py:1819-1820` (python `continue`), `1823-1834` (skip `continue`).
- **Change:** Construction (R-2) sits after both `continue` guards, so these phases allocate no ledger and pass
  none to any callee. Behavior unchanged.
- **Verification:** TM-11 — sprint mixing skip + python + one task phase; spy on `TurnLedger.__init__`; assert
  exactly one construction (the task phase); skip phase still records `PhaseStatus.SKIPPED, exit_code=0`.

### R-9 — Thread-safety under K>1 (C3): fresh ledger fully built before workers spawn
- **Anchor:** parallel worker fan-out `_execute_phase_tasks_parallel` (`executor.py:1158`, worker `1206`, gate `1231`); ledger passed at `1860`; `__post_init__` RLock `models.py:926-932`.
- **Change:** The per-phase ledger is constructed in the parent thread (R-2) before `execute_phase_tasks` fans
  out workers; the `_lock` RLock is created in `__post_init__` before the instance is published. No worker ever
  sees a half-built or mid-reset ledger. `execute_phase_tasks` joins all workers before returning, so the next
  phase's construction cannot race a straggler.
- **Verification:** TM-12 — size a ledger `initial_budget = task_count × minimum_allocation`, fan
  `2 × task_count` `try_launch()` calls across a `ThreadPoolExecutor`; assert exactly `task_count` succeed
  (reuses the existing harness in `tests/sprint/test_turn_ledger_concurrency.py`).

## 5. CLI / Contract Preservation

- **C1 — `--max-turns` semantics preserved.** No flag or help change (`commands.py:92` stays
  "Max agent turns per phase"). The fix realigns the *runtime* with the already-documented per-phase unit.
- **C2 — legacy path preserved.** Subprocess execution unchanged (R-6); only the wiring-hook ledger input is
  refined, documented, and characterization-pinned.

## 6. Test Matrix

| ID | Tier | Scenario | Asserts | File (reuse) |
|----|------|----------|---------|--------------|
| **TM-0** | **Regression (mandatory)** | 3 phases × 5 tasks, `--max-turns 100`, per-task factory consuming ≥20 turns (defeats old 300 pool) | **0 SKIPPED**; all 3 phases PASS; sprint SUCCESS; `available()==500` at each phase entry | **NEW** `tests/sprint/test_per_phase_budget.py::test_regression_3x5_no_global_pool_starvation`, `@pytest.mark.regression` |
| TM-1 | Integration | 3 task phases, varied task counts | one fresh ledger per phase; distinct identities; `initial_budget == max_turns × len(tasks)` each | NEW `test_per_phase_budget.py::test_per_phase_ledger_is_fresh_each_phase` |
| TM-2 | Unit | `TurnLedger(initial_budget=max_turns*n)` for n∈{1,5,0-guarded} | `available()==initial_budget`, `consumed==0` | `tests/sprint/test_models.py::TestTurnLedger` (exists) |
| TM-5 | Integration | reimbursement in phase 1 | phase 2 fresh ledger unaffected (`available()` full) | NEW `test_per_phase_budget.py` |
| TM-6 | Unit | no in-place reset mutator + intra-phase monotonicity | `hasattr(TurnLedger,'reset')` is False; `consumed` non-decreasing between constructions | `test_models.py::TestTurnLedger` (exists) |
| TM-7 | Characterization | task phase → legacy (freeform) phase | legacy subprocess execution log (order/status/exit_code) byte-equivalent to baseline | `tests/sprint/test_multi_phase.py` (exists; promote `test_three_phase_happy_path` assertions to a golden) |
| TM-8 | Integration (D-3 guard) | legacy phase after a task phase | no `NameError`; legacy phase gets fresh `max_turns × 1` ledger; wiring hook runs | NEW `test_per_phase_budget.py::test_legacy_phase_after_task_phase_has_fresh_ledger` |
| TM-9 | Integration (safety net) | 1 phase × 3 tasks, `max_turns=10`, task 1 consumes 28 | task 1 PASS; tasks 2–3 SKIPPED; `remaining` populated; phase ERROR | NEW `test_per_phase_budget.py::test_single_task_overspend_trips_safety_net` |
| TM-10 | Integration (starvation impossibility) | heavy phase 1 fully consumes its pool | phase 2 still enters with full `max_turns × N₂` | NEW `test_per_phase_budget.py` |
| TM-11 | Integration | skip + python + task phases | exactly one `TurnLedger.__init__`; skip → SKIPPED/exit 0 | NEW `test_per_phase_budget.py::test_skip_and_python_phases_construct_no_ledger` |
| TM-12 | Concurrency | K>1, pool = `task_count × min_allocation` | exactly `task_count` `try_launch()` succeed | `tests/sprint/test_turn_ledger_concurrency.py` (exists) |

**Run:** `uv run pytest tests/sprint/test_per_phase_budget.py tests/sprint/test_models.py::TestTurnLedger tests/sprint/test_turn_ledger_concurrency.py tests/sprint/test_multi_phase.py -v`

## 7. Blast-Radius Summary

| Site | Anchor | Nature |
|------|--------|--------|
| Remove global construction | `executor.py:1777-1780` | delete 1 statement (keep neighbors) |
| Add per-phase construction | `executor.py:1838-1839` | add 1 statement (covers both branches) |
| Gate | `executor.py:1231-1235`, `1424-1430` | comment/log string only |
| Legacy wiring input | `executor.py:2281-2287` | no code change; document delta |
| `TurnLedger` model | `models.py:901-1014` | **unchanged** (no new method) |

Net: **one statement deleted, one added**, plus comment/docstring touch-ups and the test suite. `TurnLedger`
itself is not modified.

## 8. Open Risks Carried to Implementation

- **K-1 (wiring delta on legacy late phases).** R-6 intentionally changes the wiring hook's ledger input on
  legacy phases. If any downstream consumer expected wiring to stay suppressed under budget pressure, that
  changes. Mitigation: documented + TM-7/TM-8.
- **K-2 (sequential-phase assumption).** The design assumes phases execute sequentially (the `for phase` loop is
  serial) with intra-phase K>1 fan-out. If a future change overlaps phases, per-phase ledgers would need
  per-phase ownership. Mitigation: note the assumption in the construction-site comment.
- **K-3 (external ledger consumers).** Assumes nothing outside `run_sprint` reads the ledger's sprint-cumulative
  state (verified for this file; not re-audited across the whole package). Mitigation: a package-wide
  `grep "\.wiring_turns"` before merge.

## 9. Handoff

Ready for **`/sc:task`** (feature/bugfix template). Recommended entry:
`/sc:task "Implement per-phase turn-budget per .dev/brainstorms/20260618-per-phase-turn-budget/merged-requirements.md (design-only doc; R-1..R-9 + TM-0..TM-12)"`.
Do not auto-implement; this document is design-only.
