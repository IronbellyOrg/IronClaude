# QA Report — Test-Assertion Actionability Lens (task-qualitative, content slice)

**Topic:** Per-Phase Turn-Budget Model — §6 Test Matrix (TM-0..TM-14)
**Date:** 2026-06-18
**Phase:** task-qualitative (test-assertion actionability lens)
**Fix authorization:** false (REPORT ONLY — no edits)
**Lens:** Does each TM-0..TM-14 test assert EXACTLY what §6 row states; any weakened, hollow, commented-out, trivially-truthy, or passes-for-the-wrong-reason assertion?

---

## Files in scope

- `tests/sprint/test_per_phase_budget.py` (NEW — TM-0,1,5,8,9,10,11,13,14)
- `tests/sprint/test_models.py::TestTurnLedger` (reuse — TM-2, TM-6)
- `tests/sprint/test_multi_phase.py` (reuse — TM-7)
- `tests/sprint/test_turn_ledger_concurrency.py` (reuse — TM-12)
- Spec §6: `.dev/brainstorms/20260618-per-phase-turn-budget/merged-requirements-FINAL.md`

---

## Per-TM verification (spec §6 row vs. test assertion)

Legend: **Faithful** = test asserts exactly what the row states, and passes for the right reason (real per-phase construction / real R-10 chain exercised, not a stub). **Weakened/Hollow** = an assertion softened, hollowed, or able to pass for the wrong reason.

| TM | Spec §6 row requires | Test node | Asserts exactly? | Right reason? | Verdict |
|----|----------------------|-----------|------------------|---------------|---------|
| TM-0 | 0 SKIPPED; all 3 PASS; SUCCESS; `available()==500` at each phase entry | `test_per_phase_budget.py::test_regression_3x5_no_global_pool_starvation` | Yes — asserts SUCCESS, 3 PASS, `skipped==[]`, and `available_at_entry==500` for all 3 ledgers; each task consumes 20 (>old per-phase share) | Yes — real `TurnLedger` constructed via `_capture_ledgers` factory; real `_run_task_subprocess` reconciliation runs | **Faithful** |
| TM-1 | fresh ledger/phase; distinct identities; `initial_budget==max_turns×len(tasks)` | `::test_per_phase_ledger_is_fresh_each_phase` | Yes — `len==3`, distinct `id()` set, pairwise `is not`, `initial_budget==100×n` per phase | Yes | **Faithful** |
| TM-2 | `available()==budget`, `consumed==0` for n∈{1,5} + defensive n=0 | `test_models.py::TestTurnLedger::test_per_phase_sizing_for_task_counts` | Yes — loops n∈{1,5}, plus n=0 boundary, all assert `available()==budget` and `consumed==0` | Yes — real `TurnLedger` arithmetic | **Faithful** |
| TM-5 | phase-2 fresh ledger unaffected (`available()` full) | `::test_phase1_reimbursement_does_not_affect_phase2` | Yes — asserts `phase1.reimbursed>0` (real reimbursement occurred), `phase2 is not phase1`, `phase2_available_at_entry==200`, `initial_budget==200` | Yes — drives real underspend (2<min_alloc 5) → genuine credit | **Faithful** |
| TM-6 | `hasattr(TurnLedger,'reset')` False; `consumed` non-decreasing | `test_models.py::TestTurnLedger::test_no_in_place_reset_and_consumed_monotonic` | Yes — asserts no `reset`/`reallocate`, monotonic trace, `consumed==15` | Yes | **Faithful** |
| TM-7 | legacy subprocess exec log (order/status/exit_code) byte-equivalent; does NOT cover wiring delta | `test_multi_phase.py::TestTM7LegacyExecutionLogGolden::test_task_then_legacy_execution_log_golden` | Yes — golden `execution_log == [(1,PASS,0),(2,PASS,0)]`; correctly scoped away from wiring | Yes — real task→legacy sprint via `execute_sprint` | **Faithful** |
| TM-8 | no NameError; legacy gets fresh `max_turns×1` ledger; wiring hook runs | `::test_legacy_phase_after_task_phase_has_fresh_ledger` | Mostly — asserts `legacy_ledger.initial_budget==7` (max_turns×1) and `2 in wiring_hook_phases`. See **F-1** (hook-ran assertion is indirect). | Yes — real legacy branch reached after task branch | **Faithful (with F-1 note)** |
| TM-9 | task1 PASS; tasks 2-3 SKIPPED; `remaining` populated; phase ERROR | `::test_single_task_overspend_trips_safety_net` | Yes — `T01.01==PASS`, `T01.02/03==SKIPPED`, `remaining=={T01.02,T01.03}`, phase_status==ERROR | Yes — real `execute_phase_tasks` + real `try_launch` gate trips on actual 28-turn overspend of the 30 pool | **Faithful (with F-3 note)** |
| TM-10 | phase 2 enters with full `max_turns×N₂` | `::test_heavy_phase1_cannot_starve_phase2` | Yes — asserts `phase1.available()==0` (precondition real), `phase2_available_at_entry==40`, `initial_budget==40` | Yes | **Faithful** |
| TM-11 | exactly one `TurnLedger.__init__`; skip→SKIPPED/exit 0 | `::test_skip_and_python_phases_construct_no_ledger` | Yes — `construct_count==1`, skip phase `SKIPPED` + `exit_code==0`. Accumulator is `_SprintWiringTotals` (not counted). See **F-2** (SystemExit). | Yes — real `__init__` spy; accumulator verified NOT a TurnLedger | **Faithful (with F-2 note)** |
| TM-12 | exactly `task_count` `try_launch()` succeed | `test_turn_ledger_concurrency.py::test_try_launch_admits_exactly_task_count_under_kgt1` | Yes — `granted==task_count` (8) with `2×task_count` attempts across ThreadPoolExecutor | Yes — real RLock atomic try_launch under contention | **Faithful** |
| TM-13 | `wiring_analyses_run==5` pinned, no Position B; `used`/`credited` sprint-cumulative | `::test_kpi_wiring_totals_accumulate_across_phases` | Yes — `Analyses run:==5`, `used==5` AND `!=2`, `credited==20` AND `!=8` (last-phase-only counter-asserts present) | Yes — real R-10 chain: `_SprintWiringTotals` add-sites (executor 2009/2400) + `build_kpi_report(turn_ledger=sprint_wiring_totals)` (2543) + real `gate-kpi-report.md` parsed | **Faithful** |
| TM-14 | `initial_budget==max_turns×len(tasks)` identical in full vs resume; over-provisioned pool never starves/trips | `::test_resume_window_sizes_phase_identically` | Yes — `full_budget==resume_budget==300`, `budget_skipped==[]` | Yes — real `FileHandoffStore` + validated-success skip-PASS path (executor 1441-1460) | **Faithful (with F-4 note)** |

---

## Findings

The adversarial prior was "≥5 weakened/vague/non-executable assertions." After verifying every TM row against both the spec §6 row AND the production source it exercises, that prior is **not borne out as hollow/softened assertions**. The suite is unusually disciplined: every TM pins a concrete expected integer (no truthy-only checks), TM-13/TM-9/TM-5 carry explicit *counter-assertions* against the exact wrong-reason failure mode the spec warns about (e.g. `used != 2`, `credited != 8` rule out last-phase-only collapse), no assertion is commented-out, and the production R-10 chain / gate / reconciliation are exercised through `execute_sprint` rather than stubbed. The findings below are the genuine soft spots — all **MINOR**; none rises to a weakened or hollow core assertion, and none would mask a regression in the behavior its TM owns.

### F-1 (MINOR, IMPORTANT-adjacent) — TM-8 "wiring hook runs" is proven via a spy that *replaces* the real hook
**Node:** `test_per_phase_budget.py::test_legacy_phase_after_task_phase_has_fresh_ledger`
The spec §6 TM-8 row requires "wiring hook runs" on the legacy phase. The test proves this by patching `executor.run_post_phase_wiring_hook` with `_spy_wiring_hook` and asserting `2 in wiring_hook_phases`. This proves the *executor invoked something at the hook call-site* for phase 2, which is the load-bearing D-3 guarantee (no NameError, legacy branch reached, hook call-site exercised) — so the assertion is **faithful to its intent**. The soft spot: because the spy replaces the real passthrough, it cannot detect a regression *inside* the real hook (e.g. if the hook stopped reading the ledger). That residual is acceptable here because the wiring *behavior* is owned by TM-13, not TM-8; TM-8 owns only "reached + invoked + fresh `max_turns×1` ledger" — all of which it asserts concretely (`initial_budget==7`). No change required; documented so a future reader does not over-trust TM-8 as wiring-behavior coverage.

### F-2 (MINOR) — TM-11 wraps the whole sprint in `pytest.raises(SystemExit)`, which could mask an *unrelated* early exit
**Node:** `test_per_phase_budget.py::test_skip_and_python_phases_construct_no_ledger`
The skip phase makes `execute_sprint` exit non-zero (`SystemExit`), so the test correctly wraps the call. The core assertions (`construct_count[0]==1`; skip phase `SKIPPED`/`exit_code==0`) run *after* the `with pytest.raises` block and are concrete and faithful. The soft spot: `pytest.raises(SystemExit)` accepts ANY `SystemExit` (any code), so a spurious early exit *before* phase 3 constructs its ledger would still satisfy the context manager — but it would then be caught by `construct_count==1` failing (0 ≠ 1) and by the missing phase-2 result, so the masking is defended downstream. Hardening (optional): assert the exit code (`exc.value.code == 1`) as TM-7's sibling `test_halt_at_phase_three` does. MINOR.

### F-3 (MINOR) — TM-9 re-derives phase status in the test instead of asserting the executor's mapping
**Node:** `test_per_phase_budget.py::test_single_task_overspend_trips_safety_net`
TM-9 calls `execute_phase_tasks` directly (sequential path) and then computes `phase_status = PhaseStatus.PASS if report.status == "PASS" else PhaseStatus.ERROR` *in the test body* before asserting it is ERROR. The PASS/SKIPPED/`remaining` assertions are real outputs of the production gate (faithful, right-reason). But the final "phase is ERROR" assertion re-implements the executor's aggregate→status mapping rather than observing it, so it cannot catch a regression in that mapping itself. The aggregate (`report.status`) IS a real production output, so the test still proves "non-PASS aggregate on overspend"; only the last mapping hop is test-side. This matches the spec row literally (the row says "phase ERROR") but the stronger end-to-end form would assert `pr.status == PhaseStatus.ERROR` off a full `execute_sprint` `phase_results` entry (as TM-0 does for PASS). MINOR — the behavior it owns (gate trips, tasks skipped, remaining populated) is fully real.

### F-4 (MINOR) — TM-14 asserts "never trips the gate" only via `budget_skipped == []`, not via a positive available()-at-entry check
**Node:** `test_per_phase_budget.py::test_resume_window_sizes_phase_identically`
The spec §6 TM-14 row requires "the over-provisioned pool never starves and never trips the gate spuriously." The test proves this by asserting no task is SKIPPED for budget reasons (`budget_skipped == []`). That is a valid, concrete observation of the requirement. The identical-sizing assertion (`full_budget == resume_budget == 300`) is fully faithful and is the heart of the OQ-2 parity claim. The soft spot: "never starves" is shown only by the *absence* of a SKIPPED status, not by a positive check that `available()` stayed `>= minimum_allocation` through the resume window — a strictly weaker observation. Acceptable because a budget-starve in this harness manifests exactly as a SKIPPED task, so the negative check is behaviorally equivalent here. MINOR.

### F-5 (MINOR, advisory) — `_capture_ledgers` semantics ("available at construction == initial_budget") is an invariant the suite relies on but does not itself assert
**Nodes:** TM-0, TM-1, TM-5, TM-10 (all via the `_capture_ledgers` helper)
Four tests read `available_at_construction` from the helper and treat it as "the budget the phase sees AT ENTRY." This is true *only because* a fresh ledger has `consumed == 0` at construction time — which is exactly what R-3/R-4 require and what TM-2 independently pins (`consumed == 0`). So the invariant is covered (by TM-2), just not at the helper. No defect — flagged so the cross-test dependency is explicit: if TM-2 were ever weakened, the "at entry" semantics of TM-0/1/5/10 would silently degrade to "at construction." Advisory only.

---

## Hollow / wrong-reason scan (explicit negative findings)

The prompt asked specifically for harness stubs that bypass real per-phase construction and over-broad mocks that mask regressions. Result of that scan:

- **No bypass of real per-phase construction.** `_capture_ledgers` constructs the **real** `TurnLedger` (`real_cls(*args, **kwargs)`) and only records it — budget arithmetic runs for real. TM-11 spies `TurnLedger.__init__` but calls `orig_init`, so construction is real. Confirmed against `tests/sprint/test_per_phase_budget.py:113-122, 552-556`.
- **No trivially-truthy / placeholder-fixture tests.** No `assert x` truthy-only checks on the budget path; no `# Test`-style placeholder fixtures; every numeric assertion pins an exact value. (AX-4 weakened-criteria axis: did not fire.)
- **R-10 is the real code under test in TM-13, not a stub.** The `_phase_wiring_hook` stub only bumps the per-phase ledger's `debit_wiring`/`credit_wiring`; the accumulation (`executor.py:2009-2013` task, `2400-2404` legacy) and the `build_kpi_report(turn_ledger=sprint_wiring_totals)` swap (`executor.py:2540-2543`) are production code, and the assertion reads the **persisted** `gate-kpi-report.md`. The `used != 2` / `credited != 8` counter-assertions specifically rule out the last-phase-only regression Position A exists to prevent. (AX-2 contradictions / AX-3 omissions: did not fire.)
- **KPI label strings verified live.** `_parse_kpi_int` keys on `"Analyses run:"`, `"Turns used:"`, `"Turns credited:"` — all three exist verbatim in `kpi.py:140-143`. The parser is not asserting against a label that the producer never emits (a common silent-skip hollow pattern). Confirmed.
- **TM-9 factory signature matches production.** `_subprocess_factory(task, config, phase)` is invoked exactly as `subprocess_factory(task, config, phase)` at `executor.py:1070-1072`. No arity mismatch that would make the factory silently unused. (AX-5 invented-content: did not fire — every patched symbol exists in source.)

---

## Self-Audit

**(a) Reliance list — structural items NOT re-checked (delegated to rf-qa structural gate):**
- Relied on structural QA for: test files exist at the stated paths, are syntactically importable, and the test node names are well-formed. I did not run the suite (`fix_authorization: false`, report-only).

**(b) Independent semantic checks (≥1 required, INV-019):**
- Verified `_SprintWiringTotals` accumulator exists and is passed to `build_kpi_report` — `grep` + `Read` of `executor.py:336-357, 2009-2013, 2400-2404, 2540-2543`. (TM-13 right-reason.)
- Verified KPI label strings the TM-13 parser depends on exist verbatim — `grep` of `kpi.py:140-143`. (TM-13 right-reason.)
- Verified `debit_wiring`/`credit_wiring` arithmetic (`+= turns`, `+= 1` analyses; `int(turns*rate)` credit) — `Read` of `models.py:1095-1126`. (TM-13 expected-value math 5/20/5 confirmed.)
- Verified the sequential SKIPPED gate + `remaining` population on `try_launch()` failure — `Read` of `executor.py:1473-1484`. (TM-9 right-reason.)
- Verified the resume validated-success skip-PASS path (`turns_consumed=0`, no debit) — `Read` of `executor.py:1441-1460`. (TM-14 right-reason.)
- Verified `_subprocess_factory` arity matches production call-site — `Read` of `executor.py:1069-1072`. (TM-9 right-reason.)

**Confidence:** Verified: 14/14 TM rows | Unverifiable: 0 | Unchecked: 0 | Confidence: 100% (against the actionability lens; suite not executed by design).
**Tool engagement:** Read: 7 | Grep/Bash-grep: 4 | Glob: 0 | Bash: 0
**Tool-engagement summary:** No web research performed (all verification local-file-bound) — Tavily not invoked.

---

## Summary
- TM rows reviewed: 14 / 14
- Faithful to spec §6 (exact assertion, right reason): 14 / 14
- Weakened / hollow / commented-out / trivially-truthy core assertions: **0**
- Passes-for-wrong-reason (stub bypass / over-broad mock masking a regression): **0**
- MINOR soft-spots (residual coverage / hardening opportunities): 5 (F-1..F-5)
- CRITICAL / IMPORTANT: 0

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| F-1 | MINOR | `test_per_phase_budget.py::test_legacy_phase_after_task_phase_has_fresh_ledger` | "wiring hook runs" proven via a spy that replaces the real hook; cannot detect a regression inside the real hook (acceptable — wiring behavior owned by TM-13) | Optional: add a non-replacing assertion or note TM-8 is not wiring-behavior coverage |
| F-2 | MINOR | `test_per_phase_budget.py::test_skip_and_python_phases_construct_no_ledger` | `pytest.raises(SystemExit)` accepts any exit code; a spurious early exit is masked at the CM (defended downstream by `construct_count==1`) | Optional: assert `exc.value.code == 1` (as `test_halt_at_phase_three` does) |
| F-3 | MINOR | `test_per_phase_budget.py::test_single_task_overspend_trips_safety_net` | Final "phase ERROR" is re-derived in the test from `report.status` rather than observed off a real `phase_results` entry | Optional: assert `pr.status == PhaseStatus.ERROR` via full `execute_sprint` (as TM-0 does for PASS) |
| F-4 | MINOR | `test_per_phase_budget.py::test_resume_window_sizes_phase_identically` | "never starves" shown only by `budget_skipped == []` (absence of SKIPPED), not a positive `available() >= minimum_allocation` check | Optional: capture the resume ledger's available()-at-entry and assert it stayed sufficient |
| F-5 | MINOR (advisory) | `test_per_phase_budget.py` `_capture_ledgers` (TM-0/1/5/10) | "available at construction == budget seen at entry" relies on `consumed==0`-at-construction, asserted only by TM-2, not at the helper | None — cross-test dependency documented |

## Actions Taken
None — `fix_authorization: false`, report-only.

## Recommendations
- The suite is green-light from the actionability lens. None of F-1..F-5 blocks the gate; all are optional hardening.
- If any single hardening is taken, prefer **F-3** (assert ERROR off a real `execute_sprint` phase result) — it is the one finding that converts a test-side re-derivation into a true end-to-end observation of the executor's status mapping, the behavior most likely to silently regress.

## QA Complete

---

## Overall Verdict: PASS — all 14 TM rows (TM-0..TM-14) assert exactly what spec §6 requires and pass for the right reason; 0 weakened/hollow/commented-out/trivially-truthy assertions and 0 wrong-reason (stub-bypass/over-broad-mock) failures found. Five MINOR optional-hardening soft-spots (F-1..F-5) documented; none blocks the gate.


