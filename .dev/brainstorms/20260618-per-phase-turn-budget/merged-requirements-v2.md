---
title: "Per-Phase Turn-Budget Model for the Sprint Runner — Merged Requirements (v2, spec-panel reviewed)"
domain: architecture
strategy: systematic
status: design-only
spec_version: 2.0
reviewed_by: spec-panel
review_mode: critique
review_focus: [requirements, architecture, testing, correctness]
adversarial_status: converged
convergence_note: "3 proposals reconciled in v1. Spec-panel v2 added one BLOCKER-class finding (post-loop KPI wiring telemetry regression) that v1's within-file grep missed, corrected D-2, re-anchored models.py references, and tightened the test matrix. One open question (KPI accumulator vs accept-and-pin) is escalated to orchestrator adjudication."
anchors_verified_in: "worktree/perPhaseturnBudget (HEAD = origin/master), 2026-06-18 (executor.py exact; models.py re-anchored in v2)"
created: 2026-06-18T14:25:00Z
revised: 2026-06-18
handoff_target: "/sc:task"
source_brief: ".dev/brainstorms/20260618-per-phase-turn-budget/seed-brief.md"
panel_review: ".dev/brainstorms/20260618-per-phase-turn-budget/spec-panel/PANEL-REVIEW.md"
---

# Per-Phase Turn-Budget Model — Merged Requirements (Design Only, v2)

> **Do not implement from this section without re-confirming anchors.** Every `file:line` below was
> verified against this worktree on 2026-06-18. `executor.py` anchors are exact; `models.py` anchors were
> **re-anchored in v2** (v1 carried a uniform ~+110-line drift). Re-`Read` each anchor at edit time.

> **v2 headline change:** v1's claim that *no sprint-level wiring accumulator is needed* (Q5/R-4/D-2) was
> **falsified by a package-wide grep** the v1 risk register (K-3) had deferred. `kpi.py:193-197` reads three
> `wiring_*` fields off a `TurnLedger`, fed post-loop from `executor.py:2414-2418`. Making the ledger
> per-phase silently collapses the KPI report's sprint-cumulative wiring totals to last-phase-only. v2 adds
> **D-4, R-10, TM-13** and routes the fix-vs-accept decision to the orchestrator (OQ-1).

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
| **Q1 — reset mechanism** | **Fresh `TurnLedger` constructed per phase** (NOT an in-place `reset()`). | New object makes per-phase independence structural; dissolves C3/C4/C5. No new model API. **Verified safe under K>1** (see R-9 / D-3). | A + C |
| **Q2 — sizing timing** | **Lazy, at phase entry**, from `len(tasks)` computed by `_parse_phase_tasks` at `executor.py:1838`. | Single source of truth; no upfront re-parse. | A + B + C |
| **Q3 — legacy path budget** | Legacy (non-task) phase gets a fresh ledger sized **`max_turns × 1`**. The ledger **is** consulted on the legacy path (D-3). | One subprocess ⇒ one task-equivalent; prevents `NameError`; floors via `else 1`. | merge synthesis |
| **Q4 — reimbursement/credit on reset** | `consumed`/`reimbursed` start at **0 every phase**. No cross-phase credit carryover. | Carryover is the coupling we remove (S2). | A + B + C |
| **Q5 — wiring fields on reset (REVISED v2)** | Wiring counters start at **0 every phase** by fresh construction. **A sprint-level wiring accumulator IS required to preserve KPI-report fidelity** — UNLESS the orchestrator accepts last-phase-only KPI wiring as the new contract (OQ-1). v1's "no accumulator needed" is **withdrawn**. | C (corrected by spec-panel D-4) |
| **Q6 — reset placement** | Construct the fresh ledger **after the python/skip `continue` guards and after `tasks = _parse_phase_tasks(...)` at `executor.py:1838`, before `if tasks:` at `1839`** — covers BOTH task branch (`ledger=` @1860) and legacy fall-through (`ledger=` @2285). | python/skip phases `continue` earlier; both downstream branches need a bound fresh ledger. **Verified: placement defends both branches (D-3, F-C4).** | merge synthesis |
| **Q7 — gate semantics** | Gate becomes a **pure safety net**. With sizing `max_turns × task_count` + per-launch reconciliation (`executor.py:1125-1132`), the pool covers N tasks each consuming up to `max_turns`. A SKIP can only occur on genuine overspend. **Caveat (F-C5/OQ-2):** on `--resume` runs where tasks are skip-PASS without debiting, the pool is over-sized relative to actual work; "exactly covers N" is a worst-case bound, not a tight equality on resume. | B + C |

## 3. Key Merge-Verification Findings

- **D-1 (sizing is exact at worst case, not generous).** `try_launch` debits `minimum_allocation` (=5) at
  launch; the task helper reconciles to actual: at `executor.py:1125-1132`,
  `pre_allocated = ledger.minimum_allocation; if actual > pre_allocated: debit(actual - pre_allocated) elif
  actual < pre_allocated: credit(pre_allocated - actual)`. So the pool drains by **actual** consumption.
  Sizing `max_turns × task_count` lets each task consume up to its full `max_turns` share.
  *(v2 note: prose now uses `minimum_allocation`, not the literal `5` — F-C3/F-X1.)*
- **D-2 (CORRECTED v2 — there IS a post-loop reader).** A **package-wide** grep (not just within `run_sprint`)
  finds:
  - `executor.py:390` (`check_budget_guard`, ledger param) and `executor.py:949` (task helper, param) — in-function, as v1 reported; **plus**
  - **`kpi.py:193-197`** reads `turn_ledger.wiring_turns_used / wiring_turns_credited / wiring_analyses_count`,
    reached from the **post-loop** call `build_kpi_report(..., turn_ledger=ledger)` at **`executor.py:2414-2418`**.
  ⇒ v1's conclusion "sprint-wiring accumulators are unnecessary / dead code" is **withdrawn.** See D-4.
- **D-3 (legacy path DOES consult the ledger — VERIFIED).** The legacy claude-mode path calls
  `run_post_phase_wiring_hook(..., ledger=ledger, ...)` at `executor.py:2281-2287` (`ledger=ledger` @2285),
  which reads/mutates the ledger. Deleting the construction and building only on the task branch would
  `NameError` on every legacy phase. Q6 placement binds a fresh ledger for legacy phases too. **Whittaker
  divergence attack (F-C4) confirms both branches see a bound ledger — no NameError reachable.**
- **D-4 (NEW v2 — KPI wiring telemetry regression).** Under R-1 (delete pre-loop construction) + R-2 (rebind
  `ledger` fresh each iteration), the post-loop `executor.py:2417` passes the **final phase's** ledger to
  `build_kpi_report`, so `kpi.py:193-197` writes only the **last phase's** `wiring_*` into the persisted
  `gate-kpi-report.md`. Today's global pool reports **sprint-cumulative** wiring. This is a silent regression
  in an observable artifact. **Concrete trace (Accumulation Attack F-C1):** phase 1 runs 3 analyses, phase 2
  runs 2; old report says 5, new report says 2. Resolution: **R-10** (sprint-level accumulator) — OR explicit
  accept-and-pin per OQ-1 (orchestrator-adjudicated).

## 4. Requirements (R-items)

> Format: anchor → behavioral change (prose) → verification. `executor.py` anchors exact; `models.py` re-anchored.

### R-1 — Remove the global pre-loop ledger construction
- **Anchor:** `executor.py:1777-1780` (`ledger = TurnLedger(initial_budget=config.max_turns * len(config.active_phases), reimbursement_rate=0.8)`).
- **Change:** Delete this construction. **Leave adjacent pre-loop infrastructure in place** — `shadow_metrics`
  (`1782`), `remediation_log` (`1786-1788`), `SprintGatePolicy(config)` (`1793`), `all_gate_results` (`1796`)
  legitimately accumulate across phases and must NOT move into the loop. **(v2:** if R-10's accumulator is
  adopted, its construction also goes here, alongside `shadow_metrics`.)
- **Verification:** `grep "len(config.active_phases)"` no longer appears in any ledger construction. Confirm
  no reference to `ledger` exists between `1780` and the new construction point (`1838`).

### R-2 — Construct a fresh, phase-sized ledger at the tasks-resolution point
- **Anchor:** `executor.py:1838-1839` (immediately after `tasks = _parse_phase_tasks(phase, config)`, before `if tasks:`).
- **Change:** Construct `ledger = TurnLedger(initial_budget=config.max_turns * (len(tasks) if tasks else 1), reimbursement_rate=0.8)`.
  Runs once per task-or-legacy phase; binds `ledger` for both downstream branches. Placement is **after** the
  python/skip `continue` guards (`1819-1834`). **`else 1` is load-bearing** — it floors the legacy path so an
  `initial_budget=0` ledger cannot arise (F-C2: `_parse_phase_tasks` @1677 never returns a truthy empty list).
- **Verification:** Integration test captures the `ledger` per phase; assert `initial_budget == config.max_turns * len(tasks)`
  (task phases) / `== config.max_turns` (legacy), and object identity differs across phases (TM-1, TM-2).

### R-3 — Per-phase available budget == `max_turns × task_count` at every phase entry (core invariant)
- **Anchor:** sizing input `executor.py:1838`; `available()` formula `models.py:1044-1046` *(re-anchored v2; was 934-936)*.
- **Change:** At entry to `execute_phase_tasks` (`executor.py:1856`), `ledger.available() == config.max_turns * len(tasks)`
  and `ledger.consumed == 0`, independent of any earlier phase.
- **Verification:** TM-0 asserts `available() == 500` at entry to each of 3 phases at `--max-turns 100`.

### R-4 — Independence by construction (reimbursement + wiring start at zero each phase)
- **Anchor:** `TurnLedger` field defaults `models.py:1024-1034` *(re-anchored v2; was 914-924)*; fresh construction from R-2.
- **Change:** Each phase builds a new ledger, so `consumed`, `reimbursed`, and all four wiring fields begin at
  their dataclass defaults (0). No in-place mutation. **(v2 correction:** independence of the *budget* is by
  construction; independence of *sprint-cumulative wiring telemetry* is NOT free — see R-10/D-4. v1's "no
  accumulator introduced" is superseded.)
- **Verification:** Unit assert a freshly constructed ledger reports `consumed==0, reimbursed==0, wiring_*==0`;
  integration assert phase 2's ledger is unaffected by phase 1 reimbursement/wiring (TM-5, TM-10).

### R-5 — Gate unchanged in code; redefined as safety net
- **Anchor:** parallel gate `executor.py:1231→1235`, sequential gate `executor.py:1424→1430`; reconciliation `executor.py:1125-1132`.
- **Change:** **No code change to the gate.** With R-2 sizing it can no longer fire from phase ordering. Update
  the nearby comment/log string to read "phase budget exhausted" rather than implying a sprint-level limit.
- **Verification:** TM-0 asserts the SKIPPED branch is never taken in phases 2–3 under a non-exhausting budget;
  TM-9 asserts it still fires on a forced single-phase overspend.

### R-6 — Legacy non-task path: subprocess execution unchanged; ledger input becomes per-phase (intended, documented)
- **Anchor:** legacy branch `executor.py:1939-2287`; wiring-hook call `executor.py:2281-2287` (`ledger=ledger` @2285).
- **Change:** The legacy single-`ClaudeProcess` **subprocess execution** path (isolation dir, `SessionResetPolicy`,
  launch, monitor, `PhaseResult` assembly) is **byte-equivalent unchanged** *(scope clarified v2 per F-R3:
  "byte-equivalent" applies to the subprocess execution log ONLY; the wiring-hook ledger input is intentionally
  changed)*. The ONLY delta: its post-phase wiring hook now receives a fresh `max_turns × 1` ledger instead of
  the cumulative global pool — a **deliberate refinement** (late legacy phases no longer silently skip wiring
  under an exhausted pool, since `can_run_wiring_gate` requires `available() >= minimum_remediation_budget`).
  Document this delta inline and in the wiring hook docstring.
- **Verification:** Characterization test pins the legacy **subprocess execution log** (phase order,
  `PhaseStatus`, `exit_code`) unchanged (TM-7). A separate test asserts a legacy phase **following** a task
  phase does not `NameError` and gets a fresh `max_turns × 1` ledger (TM-8). **The wiring-input delta is pinned
  by TM-13, not TM-7** *(v2 correction per F-T2: TM-7 pins only the unchanged subprocess log and cannot detect
  the wiring delta)*.

### R-7 — Monotonicity (C4) preserved within a phase; reset is an object boundary, not in-place mutation
- **Anchor:** `debit` monotonicity `models.py:1048-1053` *(re-anchored v2; was 938-943)*; class docstring `models.py:1012-1022`.
- **Change:** No change to `debit`/`credit`/`try_launch`. No in-place reset ⇒ `consumed` never decreases on a
  live instance. Optionally tighten the docstring to say monotonicity is per-instance (per-phase).
- **Verification:** Unit assert `TurnLedger` exposes no `reset`/`reallocate` mutator; pair with the existing
  monotonicity test (TM-6).

### R-8 — python/skip-mode phases never construct or touch a ledger
- **Anchor:** `executor.py:1819-1820` (python `continue`), `1823-1834` (skip `continue`).
- **Change:** Construction (R-2) sits after both `continue` guards; these phases allocate no ledger. Unchanged behavior.
- **Verification:** TM-11 — sprint mixing skip + python + one task phase; spy on `TurnLedger.__init__`; assert
  exactly one construction; skip phase records `PhaseStatus.SKIPPED, exit_code=0`.

### R-9 — Thread-safety under K>1 (C3): fresh ledger fully built before workers spawn; all workers joined before next phase
- **Anchor:** parallel fan-out `_execute_phase_tasks_parallel` (def `executor.py:1158`, worker `1206`, gate `1231`,
  wave join `with ThreadPoolExecutor(...) as pool` @`1288-1289`, return @`1300`); ledger passed @`1860`;
  `__post_init__` RLock `models.py:1036-1042` *(re-anchored v2)*.
- **Change:** The per-phase ledger is constructed in the parent thread (R-2) before `execute_phase_tasks` fans
  out workers; `_lock` is created in `__post_init__` before publication. **VERIFIED (F-C5 Sequence Attack):**
  each wave is joined via the synchronous `with ThreadPoolExecutor` + `list(pool.map(...))` block; the function
  returns only after the final wave; the serial `for phase` loop constructs the next ledger only after the prior
  `execute_phase_tasks` returns. No straggler worker can survive into the next phase. No worker sees a half-built
  or mid-reset ledger.
- **Verification:** TM-12 — size `initial_budget = task_count × minimum_allocation`, fan `2 × task_count`
  `try_launch()` across a `ThreadPoolExecutor`; assert exactly `task_count` succeed.

### R-10 — (NEW v2) Preserve sprint-cumulative wiring telemetry for the KPI report
- **Anchor:** post-loop KPI build `executor.py:2414-2418` (`build_kpi_report(..., turn_ledger=ledger)`);
  reader `kpi.py:193-197`; `build_kpi_report` signature `kpi.py:151-158`.
- **Problem (D-4/F-A1/F-C1):** Per-phase ledgers mean the post-loop `ledger` is the final phase's instance, so
  the KPI report's `wiring_turns_used / wiring_turns_credited / wiring_analyses_run` collapse from
  sprint-cumulative to last-phase-only — a silent regression in `gate-kpi-report.md`.
- **Change (RECOMMENDED — Position A, pending OQ-1 adjudication):** Introduce a sprint-scoped wiring
  accumulator constructed pre-loop (next to `shadow_metrics`, `executor.py:1782`) with three int counters
  (`wiring_turns_used`, `wiring_turns_credited`, `wiring_analyses_count`). After each phase's wiring hook runs
  (task path after `executor.py:1917`; legacy path after `2287`), add the just-finished phase ledger's wiring
  fields into the accumulator. Pass the **accumulator** (not the last-phase ledger) to `build_kpi_report` at
  `2417`. This restores the pre-fix sprint-cumulative KPI semantics with no coupling of the *budget* across
  phases.
- **Alternative (Position B — accept + pin):** If the orchestrator decides KPI wiring totals are advisory and
  last-phase-only is acceptable, **do not** add the accumulator; instead document the contract change at
  `executor.py:2417` and characterization-pin it. **Either way, the change must be deliberate and tested (TM-13).**
- **Verification:** TM-13 (see matrix).

## 5. CLI / Contract Preservation

- **C1 — `--max-turns` semantics preserved.** No flag/help change (`commands.py:92` stays "Max agent turns per phase").
- **C2 — legacy subprocess path preserved.** Subprocess execution unchanged (R-6); only the wiring-hook ledger
  input is refined, documented, and pinned (TM-13).
- **C3 — (NEW v2) `gate-kpi-report.md` wiring totals.** Either preserved sprint-cumulative (R-10 Position A) or
  intentionally redefined last-phase-only (Position B). NOT silently changed.

## 6. Test Matrix

| ID | Tier | Scenario | Asserts | File (reuse) |
|----|------|----------|---------|--------------|
| **TM-0** | **Regression (mandatory)** | 3 phases × 5 tasks, `--max-turns 100`, per-task factory consuming ≥20 turns | **0 SKIPPED**; all 3 phases PASS; sprint SUCCESS; `available()==500` at each phase entry | **NEW** `tests/sprint/test_per_phase_budget.py::test_regression_3x5_no_global_pool_starvation`, `@pytest.mark.regression` |
| TM-1 | Integration | 3 task phases, varied counts | fresh ledger per phase; distinct identities; `initial_budget == max_turns × len(tasks)` | NEW `test_per_phase_budget.py::test_per_phase_ledger_is_fresh_each_phase` |
| TM-2 | Unit | `TurnLedger(initial_budget=max_turns*n)` for n∈{1,5}; **plus a model-level defensive `n=0` case (NOT a reachable executor path — F-T3)** | `available()==initial_budget`, `consumed==0` | `tests/sprint/test_models.py::TestTurnLedger` (exists) |
| TM-5 | Integration | reimbursement in phase 1 | phase 2 fresh ledger unaffected (`available()` full) | NEW `test_per_phase_budget.py` |
| TM-6 | Unit | no in-place reset mutator + intra-phase monotonicity | `hasattr(TurnLedger,'reset')` is False; `consumed` non-decreasing | `test_models.py::TestTurnLedger` (exists) |
| TM-7 | Characterization | task phase → legacy (freeform) phase | legacy **subprocess execution log** (order/status/exit_code) byte-equivalent to baseline. **Does NOT cover wiring delta — see TM-13** | `tests/sprint/test_multi_phase.py` (exists; promote to golden) |
| TM-8 | Integration (D-3 guard) | legacy phase after a task phase | no `NameError`; legacy phase gets fresh `max_turns × 1` ledger; wiring hook runs | NEW `test_per_phase_budget.py::test_legacy_phase_after_task_phase_has_fresh_ledger` |
| TM-9 | Integration (safety net) | 1 phase × 3 tasks, `max_turns=10`, task 1 consumes 28 | task 1 PASS; tasks 2–3 SKIPPED; `remaining` populated; phase ERROR | NEW `test_per_phase_budget.py::test_single_task_overspend_trips_safety_net` |
| TM-10 | Integration (starvation impossibility) | heavy phase 1 fully consumes its pool | phase 2 enters with full `max_turns × N₂` | NEW `test_per_phase_budget.py` |
| TM-11 | Integration | skip + python + task phases | exactly one `TurnLedger.__init__`; skip → SKIPPED/exit 0 | NEW `test_per_phase_budget.py::test_skip_and_python_phases_construct_no_ledger` |
| TM-12 | Concurrency | K>1, pool = `task_count × min_allocation` | exactly `task_count` `try_launch()` succeed | `tests/sprint/test_turn_ledger_concurrency.py` (exists) |
| **TM-13** | **Integration (D-4/R-10 guard — NEW v2)** | multi-phase sprint where ≥2 phases each run wiring analysis (e.g. phase 1 → 3 analyses, phase 2 → 2) | **Position A:** `gate-kpi-report.md` reports `wiring_analyses_run == 5` (sprint-cumulative). **Position B:** reports `== 2` (last-phase) AND the documented contract note is present. Pin whichever OQ-1 selects. | **NEW** `test_per_phase_budget.py::test_kpi_wiring_totals_across_phases` |

**Run:** `uv run pytest tests/sprint/test_per_phase_budget.py tests/sprint/test_models.py::TestTurnLedger tests/sprint/test_turn_ledger_concurrency.py tests/sprint/test_multi_phase.py -v`

## 7. Blast-Radius Summary

| Site | Anchor | Nature |
|------|--------|--------|
| Remove global construction | `executor.py:1777-1780` | delete 1 statement (keep neighbors) |
| Add per-phase construction | `executor.py:1838-1839` | add 1 statement (covers both branches) |
| Gate | `executor.py:1231-1235`, `1424-1430` | comment/log string only |
| Legacy wiring input | `executor.py:2281-2287` | no code change; document delta |
| **KPI wiring accumulator (R-10, Position A)** | **pre-loop @`executor.py:1782`; per-phase add after `1917`/`2287`; pass @`2417`** | **NEW v2: ~1 small class/3 fields + 2 add-sites + 1 arg swap — OR zero code + doc note + pin (Position B)** |
| `TurnLedger` model | `models.py:1011-1124` *(re-anchored v2)* | **unchanged** (no new method) |

Net (Position A): **one statement deleted, one added, plus a small sprint-wiring accumulator**, comment/docstring
touch-ups, and the test suite. Net (Position B): one deleted, one added, plus a documented KPI contract change.
`TurnLedger` itself is not modified either way.

## 8. Open Risks Carried to Implementation

- **K-1 (wiring delta on legacy late phases).** R-6 intentionally changes the wiring hook's ledger input on
  legacy phases. Mitigation: documented + **TM-13** *(v2: re-pointed from TM-7, which cannot detect it)*.
- **K-2 (sequential-phase assumption — PROMOTED to stated invariant per F-A3).** The design's K>1 safety holds
  **only** because phases run serially (`for phase` loop @`executor.py:1813`) with intra-phase fan-out. State
  this invariant in the construction-site comment. If a future change overlaps phases, per-phase ledgers need
  per-phase ownership.
- **K-3 (RESOLVED in v2).** v1 deferred a package-wide audit; v2 performed it and found `kpi.py:193-197` →
  D-4/R-10. Remaining: re-run `grep -rn "\.wiring_turns\|\.wiring_analyses\|turn_ledger=" src/superclaude/cli/sprint`
  immediately before merge to catch any new consumer added since this review.
- **K-4 (NEW v2 — OQ-1 unresolved).** The accumulator-vs-accept decision (R-10) is escalated to orchestrator
  adjudication; implementation must wait on that ruling.

## 9. Handoff

Ready for **`/sc:task`** (feature/bugfix template) **after OQ-1 is adjudicated**. Recommended entry once resolved:
`/sc:task "Implement per-phase turn-budget per .dev/brainstorms/20260618-per-phase-turn-budget/merged-requirements-v2.md (design-only; R-1..R-10 + TM-0..TM-13; honor the OQ-1 ruling for R-10)"`.
Do not auto-implement; this document is design-only.

---

## Changelog (v1 → v2)

| # | Change | Driving finding | Why |
|---|--------|-----------------|-----|
| 1 | **Added D-4 + R-10 + TM-13**: post-loop KPI wiring telemetry regression and its fix/accept paths | F-A1 (BLOCKER), F-C1 (CRITICAL), F-T1 | `kpi.py:193-197` reads the post-loop ledger (`executor.py:2414-2418`); per-phase ledgers silently collapse sprint-cumulative wiring KPIs to last-phase-only. v1 missed this. |
| 2 | **Corrected D-2**: now reports the package-wide grep result naming `kpi.py:193-197`; withdrew "accumulator is dead code" | F-A2, F-R1 | v1's conclusion rested on a within-`run_sprint` grep; K-3 had deferred the package-wide search that falsifies it. |
| 3 | **Revised Q5 and R-4**: withdrew "no sprint-level accumulator is added"; now "accumulator required unless OQ-1 accepts last-phase-only" | F-R1, D-4 | Same root cause as #1; keeps the decision table honest. |
| 4 | **Re-anchored ALL `models.py` references** (class 1011-1124, fields 1024-1034, `available()` 1044-1046, `debit` 1048-1053, `__post_init__` 1036-1042) | F-X1 | v1 carried a uniform ~+110-line drift on models.py (executor.py anchors were exact). |
| 5 | **Re-pointed K-1's mitigation from TM-7 to TM-13**; scoped TM-7 to "subprocess execution log only" | F-T2 (MAJOR) | TM-7 pins the *unchanged* subprocess log and structurally cannot detect the wiring-input delta it was cited to guard. |
| 6 | **Scoped R-6 "byte-equivalent"** to the subprocess execution log; called out the intended wiring delta | F-R3 | "byte-equivalent unchanged" over-claimed given the admitted K-1 delta. |
| 7 | **Replaced prose literal `5` with `minimum_allocation`** in D-1/R-5 reconciliation description | F-C3, F-X1 | Code uses `pre_allocated = ledger.minimum_allocation` (`executor.py:1128`); hardcoding 5 desyncs if the default changes. |
| 8 | **Annotated TM-2's zero-task case** as model-level/defensive, not a reachable executor path | F-T3 | `_parse_phase_tasks` never returns a truthy empty list; `if tasks:` excludes both None and `[]`; `else 1` floors legacy. |
| 9 | **Promoted K-2 (sequential-phase) to a stated invariant** for the construction-site comment | F-A3 | It is the load-bearing precondition for R-9's verified K>1 safety. |
| 10 | **Marked R-9, D-3, Q6 placement as VERIFIED** (not assumed) with the join/divergence evidence | F-A4, F-C4, F-C5 | Panel re-Read the live code: workers are joined per wave before return; both branches see a bound ledger. The strongest parts of the design now carry their proof. |
| 11 | **Added OQ-1 and OQ-2** to the handoff as orchestrator-adjudicated; added K-4 | OQ-1, OQ-2 | Two decisions where experts genuinely split (KPI accumulator scope; resume-run sizing exactness). |
