# QA Report — Final Gate / Domain-Accuracy Lens (Sprint-Runner)

**Topic:** Per-phase turn-budget + concurrency model for the sprint runner
**Date:** 2026-06-18
**Phase:** report-validation (domain-accuracy lens)
**Lens:** sprint-runner domain correctness
**Fix authorization:** false (REPORT ONLY — no edits made)
**Spec of record:** `.dev/brainstorms/20260618-per-phase-turn-budget/merged-requirements-FINAL.md` (v3, R-1..R-10)

---

## Scope of this lens

I independently verified the per-phase ledger construction, the parallel fan-out
(`_execute_phase_tasks_parallel`), the serial `for phase` loop, the per-task
reconciliation, the `TurnLedger` model + RLock, and the R-9/K-2 thread-safety claims,
against the FINAL spec. Every finding below cites `file:line` evidence. I assumed
≥5 domain-correctness defects existed and hunted for races, stragglers, budget-coupling,
and sizing defects.

---

## Items Reviewed

| # | Check (domain invariant) | Result | Evidence |
|---|--------------------------|--------|----------|
| 1 | Fresh per-phase ledger fully built in PARENT thread before workers spawn | PASS | `executor.py:1920-1923` constructs `ledger` in the loop body (parent thread), then passes it to `execute_phase_tasks(... ledger=ledger ...)` at `executor.py:1941-1952`; the fan-out spawns workers only inside `_execute_phase_tasks_parallel` at `executor.py:1333`. RLock built at construction via `models.py:1044-1050` (`__post_init__`). No worker can observe a half-built ledger. |
| 2 | Each wave synchronously joined before next phase constructs its ledger (no straggler crosses a phase boundary) | PASS | `with ThreadPoolExecutor(max_workers=k) as pool:` + `wave_out = list(pool.map(...))` at `executor.py:1333-1334`; `with`-exit joins all workers, `list()` materializes. Function returns at `executor.py:1344-1345` only after the final wave. Serial loop `for phase in config.active_phases:` at `executor.py:1873` constructs the next ledger at `1920` only after the prior `execute_phase_tasks` returns. |
| 3 | K-2 sequential-phase invariant STATED at the construction site | PASS | `executor.py:1912-1919` — explicit `# K-2 SEQUENTIAL-PHASE INVARIANT (load-bearing precondition for R-9):` comment immediately above the `TurnLedger(...)` construction at `1920`. Matches R-2/K-2 spec requirement. |
| 4 | Budget strictly per-phase; only telemetry aggregated sprint-wide | PASS | Budget object rebuilt every phase (`executor.py:1920`); accumulator `_SprintWiringTotals` (`executor.py:335-357`) holds only 3 wiring counters and is NEVER read by `try_launch`/`available`/`can_run_wiring_gate` (those methods at `models.py:1052-1089, 1128-1132` reference only ledger fields). Accumulator passed to `build_kpi_report` at `executor.py:2540-2543`; budget gate reads only the per-phase `ledger`. |
| 5 | `else 1` floor genuinely prevents `initial_budget=0` on the legacy path | PASS | `executor.py:1921` `config.max_turns * (len(tasks) if tasks else 1)`. `_parse_phase_tasks` (`executor.py:1726-1758`) returns a TRUTHY list (`1740-1741`) or `None` (`1736`, `1758`) — never `[]`. So `tasks` falsy ⟹ legacy ⟹ floor `1`; `initial_budget == max_turns × 1 ≥ max_turns`. A 0 budget is unreachable. |
| 6 | python/skip phases never construct a ledger | PASS | python `continue` at `executor.py:1879-1880`; skip `continue` at `1883-1894`. Both precede the `_parse_phase_tasks` call (`1898`) and the `TurnLedger(...)` construction (`1920`). Those phases return before any ledger is allocated (R-8). |
| 7 | Per-task reconciliation debits/credits ACTUAL turns against the per-phase ledger | PASS | `executor.py:1163-1170`: `pre_allocated = ledger.minimum_allocation; if actual > pre_allocated: debit(actual - pre_allocated) elif actual < pre_allocated: credit(pre_allocated - actual)`. Matches D-1. `debit`/`credit` are RLock-guarded internally (`models.py:1056-1068`). |
| 8 | Ledger mutations are race-free under K>1 | PASS | `try_launch` is atomic check-and-debit under `_lock` (`models.py:1074-1089`); `debit`/`credit`/`debit_wiring`/`credit_wiring` all acquire `_lock` (`models.py:1060,1067,1103,1122`). RLock is reentrant so `try_launch`→`debit` nests safely. Reconcile sequence additionally wrapped in the shared worker `lock`/`guard` (`executor.py:1163`, `1300`, `1035`). |
| 9 | Wiring accumulation reads the right (post-hook) ledger fields, in the parent thread | PASS | Task path: accumulate at `executor.py:2009-2015` AFTER `run_post_phase_wiring_hook` at `1996-2002` and after `execute_phase_tasks` returned (workers joined). Legacy path mirror at `2400-2406` after hook at `2388-2394`. All reads in the serial parent thread. Per-task wiring (via `run_post_task_wiring_hook`, `executor.py:1186`) also mutates the same ledger fields, so the accumulator captures both per-task and per-phase wiring — correctly cumulative. |
| 10 | KPI report receives the ACCUMULATOR, not the last-phase ledger (D-4 regression closed) | PASS | `executor.py:2540-2543` `build_kpi_report(... turn_ledger=sprint_wiring_totals)`. `_SprintWiringTotals` exposes `wiring_turns_used`/`wiring_turns_credited`/`wiring_analyses_count` (`executor.py:355-357`) matching the `kpi.py:193/195/197` read contract. R-10 / OQ-1 Position A satisfied. |
| 11 | Legacy single-subprocess path binds a fresh ledger (no NameError) | PASS | Legacy path is the fall-through after the task-branch `continue` at `executor.py:2035`; `ledger` was bound at `1920` BEFORE the `if tasks:` branch, so the legacy wiring hook at `2388-2394` (`ledger=ledger`) and accumulation at `2400-2406` always see a bound fresh `max_turns × 1` ledger (D-3 / F-C4). |
| 12 | Removed global pre-loop construction; no `len(config.active_phases)` sizing remains | PASS | grep for `len(config.active_phases)` in executor.py returns only the R-1 explanatory comment at `executor.py:1826` — no live `TurnLedger` construction uses it. The pre-loop construction is gone; neighbors (`shadow_metrics` `1832`, `remediation_log` `1846`, `SprintGatePolicy` `1853`, `all_gate_results` `1856`) correctly remain pre-loop. |
| 13 | Per-task wiring mutation race-free on parallel path | PASS | The reconcile+hook block in `_run_one_task` runs under `with guard:` at `executor.py:1163`; `run_post_task_wiring_hook` at `1186` is inside that block, so per-task `debit_wiring`/`credit_wiring` are serialized across K>1 workers (in addition to the internal `_lock`). No wiring-counter race. |

---

## Adversarial deep-dive on the four CRITICAL categories

I was tasked to assume ≥5 defects in the race / straggler / budget-coupling / sizing
classes and flag any as CRITICAL. I drove each attack to a concrete code trace:

- **Race (half-built ledger).** Attempted: a worker observing `ledger` before `_lock`
  exists. Refuted — `_lock` is created in `__post_init__` (`models.py:1044-1050`) which
  runs during `TurnLedger(...)` at `executor.py:1920`, strictly before the object is
  passed to the fan-out at `1941`. No publication-before-init window.
- **Race (concurrent debit over-admit).** Attempted: two workers both pass the gate and
  both debit. Refuted — `try_launch` collapses check-and-debit into one `_lock`-held
  critical section (`models.py:1085-1089`). This is exactly TM-12's pin.
- **Straggler across phase boundary.** Attempted: a worker from phase N still running when
  phase N+1 builds its ledger. Refuted — `list(pool.map(...))` + `with`-exit join
  (`executor.py:1333-1334`) fully drains the pool before `_execute_phase_tasks_parallel`
  returns (`1344`), and the serial loop (`1873`) blocks the next `1920` construction until
  return. Verified independently of the R-9 confirmation note (which I corroborated, not
  relied upon).
- **Budget-coupling (telemetry leaks into gating).** Attempted: the sprint accumulator
  feeding back into a launch/wiring decision. Refuted — `_SprintWiringTotals`
  (`executor.py:335-357`) is consumed only by `build_kpi_report` (`2540-2543`); it has no
  method and is never referenced by `try_launch`/`available`/`can_run_wiring_gate`. Budget
  fields (`initial_budget`/`consumed`/`reimbursed`) are rebuilt every phase at `1920`.
- **Sizing (`initial_budget=0`).** Attempted: an empty-list `tasks` driving a 0 budget.
  Refuted — `_parse_phase_tasks` provably never returns `[]` (`executor.py:1736,1740-1741,1758`),
  so the `else 1` legacy floor at `1921` is the only path for a falsy `tasks`, yielding
  `max_turns × 1`.

No defect in any of the four CRITICAL categories survived its trace.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix (advisory — fix_authorization:false) |
|---|----------|----------|-------|---------------------------------------------------|
| 1 | OBSERVATION (not a defect) | `executor.py:1920`, `run_post_phase_wiring_hook` docstring `executor.py:829-840` | `wiring_budget_exhausted` is now per-phase: under the OLD global pool it latched for the rest of the sprint once tripped; with a fresh ledger each phase it resets, so every phase re-enters wiring with full budget. This is the *intended* R-6 refinement (spec §8 K-1, lines 269-270) and is documented at `executor.py:829-840`. Flagged only for traceability — it is a deliberate, spec-sanctioned behavior change, NOT a regression. | None. Behavior matches R-6 / K-1 and is pinned by TM-13. |
| 2 | MINOR (doc/anchor drift, non-blocking) | spec `merged-requirements-FINAL.md` R-9 anchors vs live code | The FINAL spec's R-9 anchors (def `1158`, worker `1206`, gate `1231`, wave-join `1288-1289`, return `1300`, ledger passed `1860`) are stale relative to the live file: actual def `1196`, worker `1244`, gate `1276`, wave-join `1333`, return `1344`, ledger passed `1941`. The R-9 threadsafety confirmation note (`r9-threadsafety-confirmation.md`) already records the CORRECTED live anchors (`1196/1244/1333/1941/1920`), so the implementation tracked them correctly. The drift is in the design doc only. | Non-blocking. If the spec is retained as a living reference, refresh its R-9 anchor list to match the confirmation note. Does not affect code correctness. |

---

## Summary

- Domain invariants checked: 13 / 13
- PASS: 13
- FAIL: 0
- CRITICAL defects (race / straggler / budget-coupling / sizing): **0**
- Issues found: 2 — neither is a code defect (1 deliberate spec-sanctioned behavior change; 1 design-doc anchor drift)
- Issues fixed in-place: 0 (fix_authorization: false — report only)

The per-phase budget + concurrency model is domain-correct against the FINAL spec
(R-1..R-10, K-2):

- Fresh per-phase ledger constructed in the parent thread before workers spawn (built-before-publish, RLock-before-publish).
- Each wave synchronously joined; serial phase loop prevents any straggler from crossing a phase boundary.
- K-2 sequential-phase invariant explicitly stated at the construction site (`executor.py:1912-1919`).
- Budget strictly per-phase; only the 3 wiring telemetry counters aggregate sprint-wide via `_SprintWiringTotals`, which has zero effect on gating.
- `else 1` floor proven to make `initial_budget=0` unreachable; python/skip phases allocate no ledger.

## Confidence

**Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**

All 13 invariants were checked with direct tool evidence (file:line citations above).
Threshold (≥95%, UNCHECKED==0) met for a non-FAIL verdict.

## Tool engagement

**Read: 9 | Grep: 1 | Glob: 0 | Bash: 1**
(No web research performed — all claims are intrinsically local/source-truth; Tavily-first
rule not triggered. tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0.)

Tool-engagement note: tool calls (11) ≥ invariants checked (13) is NOT satisfied as a raw
count because several Read calls covered multiple invariants each (e.g. the single
`executor.py:1810-1940` Read covered invariants 1, 3, 4, 5, 6, 11, 12; the `models.py` Read
covered 7, 8). Each invariant is individually backed by a specific cited file:line range, so
the verification is not padded — the lower call count reflects dense, multi-invariant reads,
not skipped checks.

---

## Overall Verdict: PASS — no race, straggler, budget-coupling, or sizing defect found; per-phase budget + concurrency model is domain-correct against the FINAL spec (R-1..R-10, K-2). 2 non-blocking observations (1 intended behavior change, 1 design-doc anchor drift); 0 CRITICAL.



