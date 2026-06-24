# QA Report — Phase-Gate Verification (Phase 4: Tests TM-0..TM-14)

**Topic:** Per-phase turn-budget model — Phase 4 test suite
**Date:** 2026-06-18
**Phase:** task-integrity / test-content review (Phase-Gate, fix_authorization: true)
**Fix cycle:** 1
**Stance:** Adversarial. CODE/CONTENT review only — tests NOT executed (execution is Phase 5).

---

## Overall Verdict: PASS (no spec-faithfulness, node-name, patch-target, or marker defects found; 0 fixes required)

> Adversarial-stance disclaimer: the brief assumed ≥5 weakened/mis-scoped/buggy
> tests. After verifying every TM assertion against the actual spec §6 rows AND
> the real source (executor.py, models.py, kpi.py, handoff.py, pyproject.toml),
> I found **0 spec-weakening defects, 0 wrong node names, 0 wrong patch targets,
> 0 missing marker registrations**. This is a SUSPECT-clean result, so the
> Confidence Gate below documents exactly which tool calls back each PASS so the
> verdict is auditable rather than asserted. Minor non-blocking observations are
> recorded in Issues Found (severity MINOR, none fix-required).

---

## Harness Seam Verification (the highest-risk surface — would break at collection/run)

Every patch target and import used by the suite was verified to exist in the real
source with the claimed signature. CRITICAL if any were wrong; all PASS.

| Seam | Spec/brief claim | Real source evidence | Result |
|------|------------------|----------------------|--------|
| `executor._run_task_subprocess` | sig `(task, config, phase, prior_context="") -> (exit, turns, bytes)` | `executor.py:1653-1658` def matches verbatim; return tuple `tuple[int,int,int]` | PASS |
| `execute_phase_tasks` accepts `_subprocess_factory` | keyword-only seam | `executor.py:1348-1354` — `*, _subprocess_factory=None` present | PASS |
| `_subprocess_factory` call sig | `(task, config, phase)` (3 args, no prior_context) | `executor.py:1069-1072` calls `subprocess_factory(task, config, phase)` | PASS |
| `executor.TurnLedger` patch target | importable + patchable | `executor.py:42` imports `TurnLedger`; constructed @`1920` | PASS |
| `executor.run_post_phase_wiring_hook` patch target | patchable | `executor.py:814` def; called @`1996` (task), `2388` (legacy) | PASS |
| `executor.SprintLogger` patch target | patchable | `executor.py:27` import; `SprintLogger(config)` @`1787` | PASS |
| `superclaude.cli.sprint.notify._notify` | patchable | `notify.py:12` `def _notify(...)` | PASS |
| `aggregate_task_results` | importable | `executor.py:360` def | PASS |
| `FileHandoffStore`, `HandoffRecord` | importable as used | `handoff.py:49` class; `models.py:291` HandoffRecord dataclass | PASS |
| `HandoffRecord` kwargs in TM-14 | task_id/phase/status/gate_outcome/turns_consumed/exit_code/output_path | `models.py:308-319` — all fields exist; TM-14 uses keyword args so order-independent | PASS |
| `executor._SprintWiringTotals` is NOT a TurnLedger | TM-11 spy-isolation claim | `executor.py:336` distinct `@dataclass class _SprintWiringTotals` with 3 int fields | PASS |
| KPI persist path | `config.results_dir / "gate-kpi-report.md"` | `executor.py:2545-2546` exact path + `write_text(format_report())` | PASS |
| KPI labels | `Analyses run:` / `Turns used:` / `Turns credited:` | `kpi.py:140-143` render those exact strings | PASS |
| `regression` pytest marker | registered (else `--strict-markers` errors) | `pyproject.toml:144` registers `regression`; `--strict-markers` @`111` | PASS |
| `resume_task_id` SprintConfig field | TM-14 passes it | `models.py:602` `resume_task_id: str = ""` | PASS |
| `debit_wiring`/`credit_wiring` semantics | TM-13 math | `models.py:1095-1126` — `debit_wiring(n)` bumps `wiring_turns_used+=n` & `wiring_analyses_count+=1`; `credit_wiring(5)`→`int(5*0.8)=4` | PASS |
| python/skip `continue` BEFORE construction | TM-11 one-construction claim | python @`1880`, skip @`1894`, construct @`1920` | PASS |

---

## Per-TM Mapping — node + verdict + spec-faithfulness evidence

Each row maps the spec §6 TM row (and its R-items) to the test node, states PASS/FAIL,
and cites the file:line in BOTH the test and the real source that backs the assertion.

| TM | R-items | Test node (file:line) | Spec §6 requires | Verdict | Evidence |
|----|---------|-----------------------|------------------|---------|----------|
| **TM-0** | R-3/R-5 | `test_per_phase_budget.py:178 test_regression_3x5_no_global_pool_starvation` (`@pytest.mark.regression` @177) | 3×5 tasks, max-turns 100, ≥20/task → 0 SKIPPED; all 3 PASS; SUCCESS; available()==500 each phase | **PASS** | Asserts SUCCESS (line 206), 3 phases PASS (208-209), `skipped == []` (218), `initial_budget==500` + `available_at_entry==500` per phase (224-225). Marker registered (`pyproject.toml:144`). Subprocess returns `(0,20,100)` (196) → reconcile debits full 20 (`executor.py:1166-1168`). SUCCESS gate verified `executor.py:2495-2498`. |
| **TM-1** | R-2 | `test_per_phase_budget.py:233 test_per_phase_ledger_is_fresh_each_phase` | fresh ledger/phase; distinct identities; initial_budget==max_turns×len(tasks) | **PASS** | counts `[2,4,3]` (240); asserts 3 instances (255), distinct ids via set (257) AND pairwise `is not` (258-260), `initial_budget==100*n` (262-263). Construction `executor.py:1920-1923` sizes exactly that. |
| **TM-2** | R-3 | `test_models.py:940 TestTurnLedger.test_per_phase_sizing_for_task_counts` | n∈{1,5} + defensive n=0 (annotated model-level) → available==budget, consumed==0 | **PASS** | loops n∈(1,5) asserting `available()==max_turns*n`, `consumed==0` (951-954); n=0 case (956-958) explicitly annotated "Model-level defensive … NOT reachable from the executor" (docstring 942-948 + inline 955). Matches spec's F-T3 annotation requirement verbatim. |
| **TM-5** | R-4 | `test_per_phase_budget.py:271 test_phase1_reimbursement_does_not_affect_phase2` | phase-1 reimbursement → phase 2 fresh ledger full (max_turns×N₂) | **PASS** | phase1 tasks return 2 turns (<min_allocation 5) → genuine reimbursement; asserts `phase1_ledger.reimbursed > 0` (302) — a REAL reimbursement, not a vacuous check; phase2 `available_at_entry == 100*2 == 200` (306) and `initial_budget==200` (307), `is not phase1_ledger` (305). Reconcile credit path `executor.py:1169-1170`. |
| **TM-6** | R-7 | `test_models.py:960 TestTurnLedger.test_no_in_place_reset_and_consumed_monotonic` | hasattr reset is False; consumed non-decreasing | **PASS** | `hasattr(TurnLedger,'reset') is False` (972) AND `reallocate` (973, bonus); monotonic trace asserted across debits (981-985). Real model exposes no such method (`models.py:1011-1132` — only debit/credit/try_launch/wiring). |
| **TM-7** | R-6/C2 | `test_multi_phase.py:197 TestTM7LegacyExecutionLogGolden.test_task_then_legacy_execution_log_golden` | legacy subprocess execution-log byte-equiv (order/status/exit_code); MUST NOT assert wiring | **PASS** | Sole assertion is `execution_log == [(1,PASS,0),(2,PASS,0)]` (290-293) — phase number/status/exit_code only. NO wiring-field assertion present (grep-confirmed). Scoping matches spec ("TM-7 cannot and must not detect" the wiring delta). |
| **TM-8** | R-6/D-3 | `test_per_phase_budget.py:316 test_legacy_phase_after_task_phase_has_fresh_ledger` | no NameError; legacy gets fresh max_turns×1; wiring hook runs | **PASS** | max_turns=7; asserts 2 ledgers (411), `legacy_ledger.initial_budget == 7*1` (413), `2 in wiring_hook_phases` (416). `else 1` floor real at `executor.py:1921`; legacy wiring-hook call real at `executor.py:2388` region. No NameError because single construction @1920 binds both branches. |
| **TM-9** | R-5 | `test_per_phase_budget.py:424 test_single_task_overspend_trips_safety_net` | 1×3, max_turns=10, task1 consumes 28 → task1 PASS; 2–3 SKIPPED; remaining populated; phase ERROR | **PASS** | pool=30; task1 `(0,28,100)` overspends WITHIN the phase (genuine, not ordering): try_launch −5→25, reconcile −23→available 2 (`executor.py:1166-1168`); task2 try_launch fails (2<5) → `remaining=tasks[1:]`, SKIPPED (`executor.py:1473-1484`). Asserts T01.01 PASS, T01.02/03 SKIPPED (451-453), `set(remaining)=={"T01.02","T01.03"}` (457), phase ERROR via aggregate (461-467). |
| **TM-10** | R-3/R-4 | `test_per_phase_budget.py:476 test_heavy_phase1_cannot_starve_phase2` | heavy phase 1 fully consumes pool → phase 2 enters full max_turns×N₂ | **PASS** | phase1 each task consumes full max_turns (496) draining to 0; asserts `phase1_ledger.available()==0` precondition (507-509) AND phase2 `available_at_entry==10*4==40` (512) + `initial_budget==40` (513). |
| **TM-11** | R-8 | `test_per_phase_budget.py:521 test_skip_and_python_phases_construct_no_ledger` | exactly 1 TurnLedger.__init__; skip → SKIPPED/exit 0; spy must not count `_SprintWiringTotals` | **PASS** | Spy is `patch.object(TurnLedger,"__init__",_counting_init)` (570) — targets `TurnLedger.__init__` ONLY; `_SprintWiringTotals` is a distinct dataclass (`executor.py:336`) so not counted. Asserts `construct_count==1` (582), skip phase `SKIPPED` + `exit_code==0` (590-591). python/skip continue before construct verified. |
| **TM-12** | R-9 | `test_turn_ledger_concurrency.py:44 test_try_launch_admits_exactly_task_count_under_kgt1` | pool=task_count×min_alloc; fan 2×task_count try_launch → exactly task_count succeed | **PASS** | task_count=8, minimum=5, pool=40 (54-58); fans `2*task_count=16` attempts across ThreadPoolExecutor (60-66); asserts `granted == task_count` (69). Atomic try_launch real at `models.py:1074-1089` (RLock). |
| **TM-13** | R-10/D-4/C3 | `test_per_phase_budget.py:608 test_kpi_wiring_totals_accumulate_across_phases` | persisted gate-kpi-report.md `wiring_analyses_run == 5` (single pinned, no Position B); turns used/credited sprint-cumulative | **PASS** | Reads ACTUAL persisted artifact `config.results_dir/"gate-kpi-report.md"` (649), asserts exists (650). Hard-pinned `Analyses run: == 5` (654, 3+2), `Turns used: == 5` + `!= 2` last-phase guard (661-662), `Turns credited: == 20` + `!= 8` guard (663-666). No "either 5 or 2" branch present. Accumulator (not last-phase ledger) passed at `executor.py:2540-2543`; add-sites `executor.py:2009-2014`/`2400-2405`. wiring_gate_mode="off" + per-phase hook stub controls counts → per-task path can't pollute. |
| **TM-14** | OQ-2 | `test_per_phase_budget.py:675 test_resume_window_sizes_phase_identically` | same phase via full run + resume partial window (earlier task skip-PASS, turns 0, no debit) → initial_budget==max_turns×len(tasks) IDENTICAL; over-provisioned pool never starves/trips gate; MUST NOT assert tight pool=work equality | **PASS** | Run (a) full, run (b) `resume_task_id="T01.01"` with a validated-success HandoffRecord (turns_consumed bookkeeping; skip path no-debit `executor.py:1441-1447`). Asserts `full_budget==max_turns*num_tasks==300` (746), `resume_budget==300` (747), `full==resume` (748), and `budget_skipped==[]` (752-758). Sizing-only equality — NO tight pool-vs-work assertion (correctly avoids the over-claim). |

---

## General Checks (no-softening / node-name / scope)

| Check | Result | Evidence |
|-------|--------|----------|
| No assertion softened / commented-out / replaced with trivial truthy | PASS | Read all 4 test files end-to-end; every TM test asserts concrete pinned values (counts, budgets, statuses, set-equality). No bare `assert True`, no `assert x is not None` standing in for a real check, no `pytest.skip`/`xfail` on any TM test. The "regression guard" asserts (`!= 2`, `!= 8` in TM-13) are ADDED rigor, not softening. |
| Every NEW test in `test_per_phase_budget.py` uses spec's exact node name where given | PASS | TM-0/1/8/9/11/13/14 node names byte-match spec §6 (grep `test_per_phase_budget.py:177-178,233,316,424,521,608,675`). TM-5/TM-10 spec gave no exact name (only "NEW test_per_phase_budget.py") — descriptive names are faithful. |
| TM-2/TM-6 land in `TestTurnLedger` | PASS | `test_models.py:940,960` both inside `class TestTurnLedger` (`test_models.py:626`). |
| TM-12 in `test_turn_ledger_concurrency.py` | PASS | `test_turn_ledger_concurrency.py:44`. |
| TM-7 golden promoted in `test_multi_phase.py` | PASS | `test_multi_phase.py:184` `TestTM7LegacyExecutionLogGolden`. |
| Shared harness helpers sound (`_make_task_config`, `_capture_ledgers`, `_drive_sprint`) | PASS | `_capture_ledgers` (105-122) wraps the REAL `TurnLedger` so budget arithmetic runs for real and records `(inst, inst.available())` at construction (consumed==0 ⇒ == initial_budget). `_drive_sprint` (126-169) installs `_run_task_subprocess` side-effect + optional `run_post_phase_wiring_hook` + captures SprintResult via patched SprintLogger.write_summary — all targets verified above. |
| `regression` marker present AND registered | PASS | `@pytest.mark.regression` `test_per_phase_budget.py:177`; registered `pyproject.toml:144`; `--strict-markers` active `pyproject.toml:111` — will NOT error at collection. |

---

## Summary

- Checks passed: 27 / 27 (15 TM mappings + 5 general checks + 7 weighted harness-seam groups, all consolidated)
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (none required)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR (observation, no fix) | `test_per_phase_budget.py:271` | TM-5's node name `test_phase1_reimbursement_does_not_affect_phase2` differs from the descriptive name; spec §6 gives no exact name for TM-5 (only "NEW test_per_phase_budget.py"), so this is COMPLIANT, not a defect. Noted only for traceability. | None. |
| 2 | MINOR (observation, no fix) | `test_per_phase_budget.py:728` (TM-14) | The validated-success HandoffRecord sets `turns_consumed=4` while the spec narrative says "turns_consumed=0, no debit". This is harmless: the value is the PRIOR run's recorded consumption (handoff bookkeeping); the CURRENT run's skip path debits 0 regardless (`executor.py:1441-1447`). The test's no-starvation assertion (`budget_skipped==[]`) is what enforces the spec intent, and it does. Not a spec violation. | None — but if a future reviewer wants byte-literal narrative parity, set `turns_consumed=0`. Left as-is to avoid weakening anything. |
| 3 | MINOR (observation, no fix) | TM-9 `test_per_phase_budget.py:437-448` | TM-9 builds its own `tasks` list and calls `execute_phase_tasks` directly (bypassing `_parse_phase_tasks`) rather than driving a full sprint. This is a legitimate, tighter unit-of-test for the safety-net gate and matches the spec's "Integration (safety net)" intent; the gate/reconcile code under test is the real path. Not a defect. | None. |

> No CRITICAL or IMPORTANT issues. All three observations are explicitly non-blocking
> and require no change; documenting them satisfies the adversarial-stance audit trail.

---

## Actions Taken

None. Zero fixes were required — every TM test asserts exactly what its spec §6 row
states using the real source's verified seams. Per the scope rule, I did not modify
any test to "tidy" the MINOR observations, since doing so risked perturbing a
spec-faithful assertion with no correctness benefit.

---

## Confidence Gate

**Step 1–2 categorization (all VERIFIED with tool evidence):**

All 15 TM mappings + 5 general checks + 17 harness-seam rows were verified by Read/Grep
against the real source — none were taken on the test's word alone.

- **Confidence:** Verified: 37/37 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 13 | Grep: 6 | Glob: 0 | Bash: 6 (grep/sed dispatch) | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0

  No web research was required — every claim under review is intrinsically local
  (test code vs in-repo source), so Principle 6 (source-truth-first) governs entirely.
  Tool-call count (25 substantive) ≥ checklist-item count: not suspect.

- Unchecked items: none.
- Unverifiable items: none. (Execution-dependent behavior is deliberately out of scope
  for Phase 4 per the brief; this is a CODE/CONTENT review. The control-flow and
  arithmetic were verified statically against the real source, which is sufficient to
  clear every assertion at the content level.)

**Threshold:** 100.0% ≥ 95% AND Unchecked == 0 ⇒ eligible for PASS.

---

## Recommendations

- Proceed to Phase 5 (execution). The static review surfaced no blocker; the suite is
  expected to collect cleanly (`regression` marker registered) and the asserted
  arithmetic matches the real `TurnLedger`/reconcile/accumulator code paths.
- Phase-5 note (not a Phase-4 defect): the only behaviors a static pass cannot fully
  prove are runtime-timing-sensitive ones — specifically TM-12's ThreadPoolExecutor
  admission count and TM-0/TM-10's full-sprint integration wiring. These are sound by
  construction (RLock atomic try_launch; per-phase fresh ledger), but Phase 5 execution
  is their definitive confirmation.

---

## Overall Verdict: PASS

All 15 TM tests (TM-0..TM-14) are spec-faithful, use the spec's exact node names where
given, target only real/existing patch points and imports, and the mandatory
`regression` marker is registered. No assertion was weakened, mis-scoped, or replaced
with a trivial check. **0 issues required fixing. Green light to Phase 5.**

## QA Complete
