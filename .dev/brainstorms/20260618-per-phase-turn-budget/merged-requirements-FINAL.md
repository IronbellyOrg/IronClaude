<!-- markdownlint-disable MD013 MD040 -->
---
title: "Per-Phase Turn-Budget Model for the Sprint Runner — FINAL Requirements (v3, reflect-validated)"
domain: architecture
strategy: systematic
status: design-only
spec_version: 3.0
reviewed_by: [spec-panel, sc-reflect-pre-deep]
review_mode: critique
review_focus: [requirements, architecture, testing, correctness, coverage]
adversarial_status: converged
convergence_note: "v1 reconciled 3 proposals. v2 spec-panel added the post-loop KPI wiring telemetry BLOCKER (D-4/R-10/TM-13) and re-anchored models.py. v3 (this doc) is the sc:reflect PRE/DEEP output: it APPLIES the orchestrator's two adjudications — OQ-1 → Position A (sprint-level wiring accumulator wired into build_kpi_report) and OQ-2 → hybrid (keep max_turns × len(tasks) sizing, soften the exactness wording, add a resume/dependency-wave note) — closing every open question. Both open questions are now RESOLVED, not escalated."
oq_status: "OQ-1 RESOLVED (Position A); OQ-2 RESOLVED (hybrid). No open questions remain. Spec is task-build-ready."
anchors_verified_in: "worktree/perPhaseturnBudget (HEAD = origin/master); executor.py + models.py + kpi.py anchors re-Read live on 2026-06-18 during the reflect pass"
created: 2026-06-18T14:25:00Z
revised: 2026-06-18
handoff_target: "/sc:task"
source_brief: ".dev/brainstorms/20260618-per-phase-turn-budget/seed-brief.md"
panel_review: ".dev/brainstorms/20260618-per-phase-turn-budget/spec-panel/PANEL-REVIEW.md"
reflect_audit: ".dev/brainstorms/20260618-per-phase-turn-budget/reflect-pre-spec.md"
supersedes: ".dev/brainstorms/20260618-per-phase-turn-budget/merged-requirements-v2.md"
---

# Per-Phase Turn-Budget Model — FINAL Requirements (Design Only, v3)

> **Do not implement from this section without re-confirming anchors.** Every `file:line` below was
> verified against this worktree on 2026-06-18 (executor.py, models.py, kpi.py all re-Read live during
> the sc:reflect pass). Re-`Read` each anchor at edit time.

> **v3 headline change:** the two open questions v2 escalated to the orchestrator are now **RESOLVED and
> applied in-spec**:
> - **OQ-1 → Position A.** A sprint-level wiring **accumulator IS required** and is the design. The KPI
>   report consumer chain is real and verified live: `build_kpi_report(..., turn_ledger=ledger)` at
>   `executor.py:2414-2418` reads `kpi.py:192-197` (`wiring_turns_used`/`wiring_turns_credited`/
>   `wiring_analyses_count`) and persists them to `gate-kpi-report.md` (`executor.py:2419-2420`). After
>   per-phase fresh-construct, the post-loop `ledger` is the **last phase's** instance → silent collapse of
>   sprint-cumulative wiring to last-phase-only. The accumulator restores sprint-cumulative fidelity. It is
>   **read-only summation** — it does NOT reintroduce a shared mutable BUDGET pool. R-10/D-4/TM-13 below say
>   "accumulator," not "accept last-phase-only."
> - **OQ-2 → hybrid (doc-precision).** Keep `max_turns × len(tasks)` sizing. Soften the Q7/D-1 exactness
>   invariant to acknowledge that on partial `--resume` runs the pool is over-provisioned (harmless — the
>   gate is a safety net). Add a one-line note on the `--resume`/dependency-wave interaction. No mechanism
>   change.

## 1. Problem (one paragraph)

`run_sprint` builds **one** `TurnLedger` before the phase loop with
`initial_budget = config.max_turns * len(config.active_phases)` (`executor.py:1777-1780`) and shares that
single pool across every phase. `--max-turns` is documented as **"Max agent turns per phase"**
(`commands.py:92`), so the global pool diverges from the documented unit: a heavy early phase drains turns
later phases need. Once the pool nears empty, the per-task budget gate `try_launch()` returns False
(`executor.py:1231→1235` parallel, `1424→1430` sequential), later tasks are recorded `SKIPPED`,
`aggregate_task_results` (`executor.py:335`) counts them, and the phase is mapped to `PhaseStatus.ERROR`
(`executor.py:1881-1882`). Empirically: `max_turns=100 × 3 phases = 300`-turn pool; phases 5/6 errored after
309 cumulative turns (root cause: `.dev/troubleshoot/phase56-budget-exhaustion-20260617/REPORT.md`; note
that REPORT.md's anchors 1651-1653 / 1119-1130 are drifted — the live anchors are 1777-1780 / 1125-1132).

## 2. Converged Design Decisions (Q1–Q7) — all RESOLVED

| # | Decision | Rationale | Origin |
|---|----------|-----------|--------|
| **Q1 — reset mechanism** | **Fresh `TurnLedger` constructed per phase** (NOT an in-place `reset()`). | New object makes per-phase independence structural; dissolves C3/C4/C5. No new model API. **Verified safe under K>1** (see R-9 / D-3). | A + C |
| **Q2 — sizing timing** | **Lazy, at phase entry**, from `len(tasks)` computed by `_parse_phase_tasks` at `executor.py:1838`. | Single source of truth; no upfront re-parse. | A + B + C |
| **Q3 — legacy path budget** | Legacy (non-task) phase gets a fresh ledger sized **`max_turns × 1`**. The ledger **is** consulted on the legacy path (D-3). | One subprocess ⇒ one task-equivalent; prevents `NameError`; floors via `else 1`. | merge synthesis |
| **Q4 — reimbursement/credit on reset** | `consumed`/`reimbursed` start at **0 every phase**. No cross-phase credit carryover. | Carryover is the coupling we remove (S2). | A + B + C |
| **Q5 — wiring fields on reset (RESOLVED v3 = OQ-1 Position A)** | Wiring counters start at **0 every phase** by fresh construction. **A sprint-level wiring accumulator IS required and IS the design** — it preserves the KPI-report sprint-cumulative contract. v1's "no accumulator needed" is **withdrawn and replaced**, not left open. | C (corrected by spec-panel D-4; adjudicated OQ-1 → A) |
| **Q6 — reset placement** | Construct the fresh ledger **after the python/skip `continue` guards and after `tasks = _parse_phase_tasks(...)` at `executor.py:1838`, before `if tasks:` at `1839`** — covers BOTH task branch (`ledger=` @1860) and legacy fall-through (`ledger=` @2285). | python/skip phases `continue` earlier; both downstream branches need a bound fresh ledger. **Verified: placement defends both branches (D-3, F-C4).** | merge synthesis |
| **Q7 — gate semantics (RESOLVED v3 = OQ-2 hybrid wording)** | Gate becomes a **pure safety net**. With sizing `max_turns × task_count` + per-launch reconciliation (`executor.py:1125-1132`), the pool is **sized for the worst case of N tasks each consuming up to `max_turns`**. A SKIP can only occur on genuine overspend. **OQ-2 wording (resume):** on partial `--resume` runs where some tasks are skip-PASS without debiting, the pool is **over-provisioned** relative to actual work — this is harmless (the gate remains a safety net). "Exactly covers N" is a worst-case bound, **not** a tight equality on resume. See the `--resume`/dependency-wave note in §3 (D-1). | B + C; adjudicated OQ-2 → hybrid |

## 3. Key Merge-Verification Findings

- **D-1 (sizing is a worst-case bound; OQ-2 resume note).** `try_launch` debits `minimum_allocation` (=5) at
  launch; the task helper reconciles to actual: at `executor.py:1125-1132`,
  `pre_allocated = ledger.minimum_allocation; if actual > pre_allocated: debit(actual - pre_allocated) elif
  actual < pre_allocated: credit(pre_allocated - actual)`. So the pool drains by **actual** consumption.
  Sizing `max_turns × task_count` lets each task consume up to its full `max_turns` share.
  **OQ-2 resume/dependency-wave note (hybrid ruling):** the parallel path executes in dependency *waves*
  (`executor.py:1283`), and resume-skip (`executor.py:1209-1229`, `1396-1415`) can mark validated-success
  tasks `PASS` with `turns_consumed=0` **without** debiting. On such partial `--resume` runs the pool is
  sized for the full parsed `len(tasks)` but only a subset actually runs, so the pool is **over-provisioned,
  not tight** — which is harmless because the gate is a safety net (Q7). The "pool exactly covers N tasks"
  phrasing is therefore a worst-case bound, not an equality that holds on resume. *(v2 note retained: prose
  uses `minimum_allocation`, not the literal `5` — F-C3/F-X1.)*
- **D-2 (there IS a post-loop reader — confirmed live in v3).** A **package-wide** grep (re-run during the
  reflect pass) finds:
  - `executor.py:390` (`check_budget_guard`, ledger param) and `executor.py:949` (task helper, param) — in-function; **plus**
  - **`kpi.py:192-197`** reads `turn_ledger.wiring_turns_used / wiring_turns_credited / wiring_analyses_count`
    (`if turn_ledger is not None` @192; reads @193/195/197), reached from the **post-loop** call
    `build_kpi_report(..., turn_ledger=ledger)` at **`executor.py:2414-2418`**, persisted to
    `gate-kpi-report.md` at **`executor.py:2419-2420`**. This is the **only** post-loop ledger-wiring
    consumer in the package (verified live during reflect).
  ⇒ v1's "sprint-wiring accumulators are unnecessary / dead code" is **withdrawn.** See D-4 / R-10.
- **D-3 (legacy path DOES consult the ledger — VERIFIED).** The legacy claude-mode path calls
  `run_post_phase_wiring_hook(..., ledger=ledger, ...)` at `executor.py:2281-2287` (`ledger=ledger` @2285),
  which reads/mutates the ledger. Deleting the construction and building only on the task branch would
  `NameError` on every legacy phase. Q6 placement binds a fresh ledger for legacy phases too. **Whittaker
  divergence attack (F-C4) confirms both branches see a bound ledger — no NameError reachable.**
- **D-4 (KPI wiring telemetry regression — the BLOCKER).** Under R-1 (delete pre-loop construction) + R-2
  (rebind `ledger` fresh each iteration), the post-loop `executor.py:2417` passes the **final phase's** ledger
  to `build_kpi_report`, so `kpi.py:193/195/197` writes only the **last phase's** `wiring_*` into the
  persisted `gate-kpi-report.md`. Today's global pool reports **sprint-cumulative** wiring. This is a silent
  regression in an observable artifact. **Concrete trace (Accumulation Attack F-C1):** phase 1 runs 3
  analyses, phase 2 runs 2; old report says 5, new report says 2. **Resolution (OQ-1 → Position A):** R-10
  sprint-level accumulator. This is now the design, not an option.

## 4. Requirements (R-items)

> Format: anchor → behavioral change (prose) → verification. `executor.py`, `models.py`, and `kpi.py` anchors
> re-verified live during the reflect pass.

### R-1 — Remove the global pre-loop ledger construction
- **Anchor:** `executor.py:1777-1780` (`ledger = TurnLedger(initial_budget=config.max_turns * len(config.active_phases), reimbursement_rate=0.8)`).
- **Change:** Delete this construction. **Leave adjacent pre-loop infrastructure in place** — `shadow_metrics`
  (`1782`), `remediation_log` (`1786-1788`), `SprintGatePolicy(config)` (`1793`), `all_gate_results` (`1796`)
  legitimately accumulate across phases and must NOT move into the loop. **R-10's wiring accumulator (Position
  A) IS constructed here, alongside `shadow_metrics` at `1782`.**
- **Verification:** `grep "len(config.active_phases)"` no longer appears in any ledger construction. Confirm
  no reference to `ledger` exists between `1780` and the new construction point (`1838`).

### R-2 — Construct a fresh, phase-sized ledger at the tasks-resolution point
- **Anchor:** `executor.py:1838-1839` (immediately after `tasks = _parse_phase_tasks(phase, config)`, before `if tasks:`).
- **Change:** Construct `ledger = TurnLedger(initial_budget=config.max_turns * (len(tasks) if tasks else 1), reimbursement_rate=0.8)`.
  Runs once per task-or-legacy phase; binds `ledger` for both downstream branches. Placement is **after** the
  python/skip `continue` guards (`1819-1834`). **`else 1` is load-bearing** — it floors the legacy path so an
  `initial_budget=0` ledger cannot arise (F-C2: `_parse_phase_tasks` @1677 never returns a truthy empty list).
  Add a construction-site comment stating the **K-2 sequential-phase invariant** (phases run serially; this is
  the precondition for R-9's K>1 safety).
- **Verification:** Integration test captures the `ledger` per phase; assert `initial_budget == config.max_turns * len(tasks)`
  (task phases) / `== config.max_turns` (legacy), and object identity differs across phases (TM-1, TM-2).

### R-3 — Per-phase available budget == `max_turns × task_count` at every phase entry (core invariant)
- **Anchor:** sizing input `executor.py:1838`; `available()` formula `models.py:1044-1046`.
- **Change:** At entry to `execute_phase_tasks` (`executor.py:1856`), `ledger.available() == config.max_turns * len(tasks)`
  and `ledger.consumed == 0`, independent of any earlier phase.
- **Verification:** TM-0 asserts `available() == 500` at entry to each of 3 phases at `--max-turns 100`.

### R-4 — Independence by construction (reimbursement + wiring start at zero each phase)
- **Anchor:** `TurnLedger` field defaults `models.py:1024-1034`; fresh construction from R-2.
- **Change:** Each phase builds a new ledger, so `consumed`, `reimbursed`, and all four wiring fields begin at
  their dataclass defaults (0). No in-place mutation. **Independence of the *budget* is by construction;
  independence of *sprint-cumulative wiring telemetry* is NOT free — it is restored by the R-10 accumulator
  (OQ-1 Position A), which is read-only and does not couple budget across phases.**
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
  launch, monitor, `PhaseResult` assembly) is **byte-equivalent unchanged** — where "byte-equivalent" applies to
  the subprocess **execution log** ONLY (phase order, `PhaseStatus`, `exit_code`); the wiring-hook ledger input
  is **intentionally changed** (this is the deliberate refinement, NOT a regression). The ONLY delta: its
  post-phase wiring hook now receives a fresh `max_turns × 1` ledger instead of the cumulative global pool — a
  **deliberate refinement** (late legacy phases no longer silently skip wiring under an exhausted pool, since
  `can_run_wiring_gate` requires `available() >= minimum_remediation_budget`). Document this delta inline and in
  the wiring hook docstring.
- **Verification:** Characterization test pins the legacy **subprocess execution log** (phase order,
  `PhaseStatus`, `exit_code`) unchanged (TM-7). A separate test asserts a legacy phase **following** a task
  phase does not `NameError` and gets a fresh `max_turns × 1` ledger (TM-8). **The wiring-input delta is pinned
  by TM-13, not TM-7** (TM-7 pins only the unchanged subprocess log and cannot detect the wiring delta).

### R-7 — Monotonicity (C4) preserved within a phase; reset is an object boundary, not in-place mutation
- **Anchor:** `debit` monotonicity `models.py:1048-1053`; class docstring `models.py:1011-1022`.
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
  `__post_init__` RLock `models.py:1036-1042`.
- **Change:** The per-phase ledger is constructed in the parent thread (R-2) before `execute_phase_tasks` fans
  out workers; `_lock` is created in `__post_init__` before publication. **VERIFIED (F-C5 Sequence Attack):**
  each wave is joined via the synchronous `with ThreadPoolExecutor` + `list(pool.map(...))` block; the function
  returns only after the final wave; the serial `for phase` loop (`executor.py:1813`) constructs the next ledger
  only after the prior `execute_phase_tasks` returns. No straggler worker can survive into the next phase. No
  worker sees a half-built or mid-reset ledger. **K-2 sequential-phase invariant (F-A3) is the load-bearing
  precondition — state it in the R-2 construction-site comment.**
- **Verification:** TM-12 — size `initial_budget = task_count × minimum_allocation`, fan `2 × task_count`
  `try_launch()` across a `ThreadPoolExecutor`; assert exactly `task_count` succeed.

### R-10 — (OQ-1 Position A — RESOLVED) Preserve sprint-cumulative wiring telemetry via a sprint-level accumulator
- **Anchor:** pre-loop accumulator construction next to `shadow_metrics` (`executor.py:1782`); per-phase add
  after the task-path wiring hook (`executor.py:1911-1917`, add after `1917`) and after the legacy-path wiring
  hook (`executor.py:2281-2287`, add after `2287`); post-loop KPI build `executor.py:2414-2418`
  (`build_kpi_report(..., turn_ledger=...)` @2417); reader `kpi.py:192-197`; persisted artifact write
  `executor.py:2419-2420`; `build_kpi_report` signature `kpi.py:151-158`.
- **Problem (D-4/F-A1/F-C1):** Per-phase ledgers mean the post-loop `ledger` is the final phase's instance, so
  the KPI report's `wiring_turns_used / wiring_turns_credited / wiring_analyses_run` collapse from
  sprint-cumulative to last-phase-only — a silent regression in `gate-kpi-report.md`.
- **Change (REQUIRED — Position A, OQ-1 adjudicated):** Introduce a sprint-scoped wiring accumulator
  constructed **pre-loop next to `shadow_metrics` at `executor.py:1782`**, holding three int counters
  (`wiring_turns_used`, `wiring_turns_credited`, `wiring_analyses_count`). **After each phase's wiring hook
  runs** — task path after `executor.py:1917`, legacy path after `executor.py:2287` — **add the just-finished
  phase ledger's wiring fields into the accumulator** (read-only summation; the per-phase ledger is not
  mutated). **Pass the ACCUMULATOR (not the last-phase `ledger`) to `build_kpi_report` at `executor.py:2417`.**
  This restores the pre-fix sprint-cumulative KPI semantics with **no coupling of the *budget* across phases**
  — only telemetry is aggregated. (`build_kpi_report`'s `turn_ledger` param @`kpi.py:156` accepts any object
  exposing the three `wiring_*` attributes it reads at `kpi.py:193/195/197`; the accumulator is shaped to that
  read contract, OR `build_kpi_report` is given a thin wiring-totals param — either is acceptable provided the
  three persisted KPI fields reflect sprint-cumulative totals.)
- **Why this does NOT reintroduce the shared budget pool:** the accumulator carries only the three observable
  wiring telemetry counters and is **never read by `try_launch`/`available()`/`can_run_wiring_gate`** — it has
  zero effect on gating. The per-phase budget (`initial_budget`, `consumed`, `reimbursed`) remains strictly
  per-phase and independent (R-3/R-4). This is the SRP separation Fowler flagged: independent budget,
  cumulative observability.
- **Verification:** TM-13 (Position A pinned — see matrix).

## 5. CLI / Contract Preservation

- **C1 — `--max-turns` semantics preserved.** No flag/help change (`commands.py:92` stays "Max agent turns per phase").
- **C2 — legacy subprocess path preserved.** Subprocess **execution log** unchanged (R-6); only the wiring-hook
  ledger input is refined, documented, and pinned (TM-13). "Unchanged" is scoped to the subprocess execution
  log; the wiring-input delta is the deliberate, documented refinement (not a silent change).
- **C3 — `gate-kpi-report.md` wiring totals preserved sprint-cumulative (OQ-1 Position A / R-10).** The
  accumulator keeps the persisted artifact's `wiring_turns_used` / `wiring_turns_credited` /
  `wiring_analyses_run` sprint-cumulative, exactly as today's global pool reports them. NOT silently changed,
  NOT redefined to last-phase-only.

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
| **TM-13** | **Integration (D-4/R-10 guard — OQ-1 Position A PINNED)** | multi-phase sprint where ≥2 phases each run wiring analysis (e.g. phase 1 → 3 analyses, phase 2 → 2) | **`gate-kpi-report.md` reports `wiring_analyses_run == 5` (sprint-cumulative)** via the R-10 accumulator passed to `build_kpi_report` at `executor.py:2417`; also assert `wiring_turns_used`/`wiring_turns_credited` are the sprint-cumulative sums, not last-phase-only. **Single pinned expected value — no Position B branch.** | **NEW** `test_per_phase_budget.py::test_kpi_wiring_totals_accumulate_across_phases` |
| **TM-14** | **Integration (OQ-2 resume-parity — NEW v3)** | same phase reached two ways: (a) full run; (b) `--start`/`--resume` partial window where an earlier task is skip-PASS (`turns_consumed=0`, no debit) | the phase's `initial_budget == max_turns × len(tasks)` is **identical** in both runs (sizing independent of `len(active_phases)` and of resume-skips); the over-provisioned pool never starves and never trips the gate spuriously | **NEW** `test_per_phase_budget.py::test_resume_window_sizes_phase_identically` |

**Run:** `uv run pytest tests/sprint/test_per_phase_budget.py tests/sprint/test_models.py::TestTurnLedger tests/sprint/test_turn_ledger_concurrency.py tests/sprint/test_multi_phase.py -v`

## 7. Blast-Radius Summary

| Site | Anchor | Nature |
|------|--------|--------|
| Remove global construction | `executor.py:1777-1780` | delete 1 statement (keep neighbors) |
| Add per-phase construction | `executor.py:1838-1839` | add 1 statement (covers both branches) + K-2 invariant comment |
| Gate | `executor.py:1231-1235`, `1424-1430` | comment/log string only |
| Legacy wiring input | `executor.py:2281-2287` | no code change; document delta |
| **KPI wiring accumulator (R-10, Position A — RESOLVED)** | **construct pre-loop @`executor.py:1782`; per-phase add after `1917` (task) / `2287` (legacy); pass accumulator @`2417`; reader `kpi.py:192-197`** | **small accumulator (~1 class or 3 fields) + 2 add-sites + 1 arg swap; read-only summation** |
| `TurnLedger` model | `models.py:1011-1124` | **unchanged** (no new method) |

Net: **one statement deleted, one added, plus a small sprint-wiring accumulator** (read-only), comment/docstring
touch-ups, and the test suite (TM-0..TM-14). `TurnLedger` itself is not modified.

## 8. Open Risks Carried to Implementation

- **K-1 (wiring delta on legacy late phases).** R-6 intentionally changes the wiring hook's ledger input on
  legacy phases. Mitigation: documented + **TM-13** (TM-7 cannot detect it).
- **K-2 (sequential-phase assumption — STATED INVARIANT per F-A3).** The design's K>1 safety holds **only**
  because phases run serially (`for phase` loop @`executor.py:1813`) with intra-phase fan-out. State this
  invariant in the construction-site comment. If a future change overlaps phases, per-phase ledgers need
  per-phase ownership.
- **K-3 (pre-merge grep).** Re-run
  `grep -rn "\.wiring_turns\|\.wiring_analyses\|turn_ledger=" src/superclaude/cli/sprint` immediately before
  merge to catch any new ledger-wiring consumer added since this review. (At review time the only post-loop
  consumer is `kpi.py:192-197` via `executor.py:2417`.)

## 9. Handoff

Ready for **`/sc:task`** (feature/bugfix template). **No open questions remain** — OQ-1 (Position A) and OQ-2
(hybrid) are resolved and applied above. Recommended entry:
`/sc:task "Implement per-phase turn-budget per .dev/brainstorms/20260618-per-phase-turn-budget/merged-requirements-FINAL.md (design-only; R-1..R-10 + TM-0..TM-14; R-10 = OQ-1 Position A sprint-level wiring accumulator wired into build_kpi_report; Q7/D-1 = OQ-2 hybrid resume wording)"`.
Do not auto-implement; this document is design-only.

---

## Changelog (v2 → v3, sc:reflect PRE/DEEP)

| # | Change | Driving finding | Why |
|---|--------|-----------------|-----|
| 1 | **Applied OQ-1 → Position A.** Q5/R-4/R-10/D-4/C3/TM-13 now mandate the sprint-level wiring accumulator and require passing the **accumulator** (not the last-phase ledger) to `build_kpi_report` at `executor.py:2417`. Added explicit anchors `executor.py:2414-2418`, `kpi.py:192-197`, `executor.py:2419-2420`. Removed the "accept last-phase-only" Position B hedge. | Orchestrator adjudication (mandatory remediation #1); reflect re-verified the consumer chain live | v2 left this open (OQ-1/K-4); a task-builder cannot proceed with an unresolved core decision. Position A is read-only summation — no shared budget pool reintroduced. |
| 2 | **Applied OQ-2 → hybrid.** Q7 + D-1 invariant wording softened to "sized for the worst case of N tasks each consuming up to `max_turns`; on partial `--resume` runs some tasks are skip-PASS without debiting, so the pool is over-provisioned (harmless — the gate is a safety net)." Added the `--resume`/dependency-wave note in D-1. | Orchestrator adjudication (mandatory remediation #2) | v2's "exactly covers N" over-claimed on resume runs (F-T4/OQ-2). Doc-precision fix, no mechanism change. |
| 3 | **Pinned TM-13 to a single expected value** (`wiring_analyses_run == 5`, sprint-cumulative) and removed the Position A/B conditional. | reflect gap G-2 (qa + analyzer): a test asserting "either 5 or 2" is not runnable | A handed-off test matrix must contain concrete expected values. |
| 4 | **Added TM-14** (resume-window parity): the same phase sizes identically via full run and via `--start`/`--resume`. | reflect gap G-5 / F-T4 (qa + analyzer) | Makes the OQ-2 resume note testable rather than prose-only. |
| 5 | **Scoped C2/S4 "legacy unchanged"** to the subprocess execution log; named the wiring-input delta as the deliberate refinement. | reflect gap G-4 (analyzer + architect) | "Unchanged" over-claimed given the intended wiring delta; removes reader over-trust. |
| 6 | **Promoted oq_status / frontmatter** to record both OQ resolutions and `reviewed_by: [spec-panel, sc-reflect-pre-deep]`. | reflect remediation framing | Downstream (task-builder) must see no dangling open question. |
| 7 | **Re-verified every load-bearing anchor live** during the reflect pass and corrected D-2's KPI reader span to `kpi.py:192-197` (the `if turn_ledger is not None` guard is @192). | anti-fabrication discipline | Anchors are exact as of 2026-06-18 HEAD = origin/master. |

## Changelog (v1 → v2) — retained for provenance

| # | Change | Driving finding |
|---|--------|-----------------|
| 1 | Added D-4 + R-10 + TM-13 (post-loop KPI wiring telemetry regression) | F-A1 (BLOCKER), F-C1 (CRITICAL), F-T1 |
| 2 | Corrected D-2 (package-wide grep naming `kpi.py:193-197`); withdrew "accumulator is dead code" | F-A2, F-R1 |
| 3 | Revised Q5 and R-4 (withdrew "no sprint-level accumulator") | F-R1, D-4 |
| 4 | Re-anchored ALL `models.py` references (~+110-line drift fixed) | F-X1 |
| 5 | Re-pointed K-1's mitigation from TM-7 to TM-13; scoped TM-7 to subprocess log | F-T2 |
| 6 | Scoped R-6 "byte-equivalent" to the subprocess execution log | F-R3 |
| 7 | Replaced prose literal `5` with `minimum_allocation` in D-1/R-5 | F-C3, F-X1 |
| 8 | Annotated TM-2's zero-task case as model-level/defensive | F-T3 |
| 9 | Promoted K-2 (sequential-phase) to a stated invariant | F-A3 |
| 10 | Marked R-9, D-3, Q6 placement as VERIFIED with join/divergence evidence | F-A4, F-C4, F-C5 |
| 11 | Added OQ-1 and OQ-2 to the handoff (now RESOLVED in v3) | OQ-1, OQ-2 |
