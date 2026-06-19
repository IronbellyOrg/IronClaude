# Reviewer Card 2 — QA / Test-Fidelity Lens (TM-0..TM-14)

**Mode:** `/sc:reflect --mode post --depth deep` Tier-2 ensemble — REVIEWER 2 (qa persona)
**Stance:** Adversarial. Mandate: assume ≥3 tests are weak/hollow/mis-scoped and find them.
**Scope:** Test fidelity only — does each test assert EXACTLY its §6 row and is it mutation-sensitive (would it FAIL if the per-phase ledger logic were reverted to the old global pool)?
**Authoritative spec §6:** `.dev/brainstorms/20260618-per-phase-turn-budget/merged-requirements-FINAL.md` (TM-0,1,2,5,6,7,8,9,10,11,12,13,14; TM-3/TM-4 do not exist — confirmed absent, no spurious tests claiming those IDs).

---

## Suite-run result (mandatory self-run)

```
cd .../perPhaseturnBudget && uv run pytest \
  tests/sprint/test_per_phase_budget.py \
  tests/sprint/test_models.py::TestTurnLedger \
  tests/sprint/test_turn_ledger_concurrency.py \
  tests/sprint/test_multi_phase.py -q
=> 46 passed in 4.49s  (Python 3.13.13, pytest 9.1.0, superclaude 4.3.5)
```

GREEN confirmed. `regression` marker registered at `pyproject.toml:144` (`--strict-markers` is on at `:111`, so an unregistered marker would have hard-errored — registration is load-bearing and present).

---

## Harness-fidelity finding (applies to all `_drive_sprint` tests) — FAITHFUL

The shared helpers do NOT stub the budget logic:

- `_capture_ledgers` (`test_per_phase_budget.py:104-122`) patches `executor.TurnLedger` with a factory that calls the **real class** (`real_cls(*args, **kwargs)`, line 117) and records `(inst, inst.available())`. Real budget arithmetic runs; only a side-channel observer is added. Not a stub bypass.
- `_drive_sprint` (`:125-167`) patches only `_run_task_subprocess` (the spawn), `shutil.which`, `_notify`, `SprintLogger`. It does NOT patch `try_launch`/`debit`/`credit`/`execute_phase_tasks`. Verified against the real loop: the gate `if ledger is not None and not ledger.try_launch()` (`executor.py:1473`) and the reconcile `actual>pre_allocated→debit / actual<pre→credit` (`executor.py:1165-1170`) execute against the captured real ledger. The injected subprocess only supplies `turns_consumed`, which then drives the REAL reconciliation.
- The REAL per-phase construction site (`executor.py:1920-1921`, `initial_budget = max_turns * (len(tasks) if tasks else 1)`) and the REAL R-10 chain (`_SprintWiringTotals` @336; add-sites @2009-2014 task / @2400-2405 legacy; accumulator passed to `build_kpi_report` @2540-2543) are exercised, not mocked.

Conclusion: the harness exercises the real per-phase construction. No stub bypass. This is the single most important fidelity question for this suite and it passes.

---

## Per-TM verdict

| TM | Node | Verdict | Mutation-sensitive? (fails if reverted to global pool) |
|----|------|---------|--------------------------------------------------------|
| TM-0 | `test_per_phase_budget.py:176 test_regression_3x5_no_global_pool_starvation` | **FAITHFUL** | YES — triple-guarded |
| TM-1 | `:230 test_per_phase_ledger_is_fresh_each_phase` | **FAITHFUL** | YES |
| TM-2 | `test_models.py:940 test_per_phase_sizing_for_task_counts` | **FAITHFUL (model-only, correctly scoped)** | N/A (unit) |
| TM-5 | `test_per_phase_budget.py:267 test_phase1_reimbursement_does_not_affect_phase2` | **FAITHFUL** | YES |
| TM-6 | `test_models.py:960 test_no_in_place_reset_and_consumed_monotonic` | **FAITHFUL** | Partial (see WEAK-1) |
| TM-7 | `test_multi_phase.py:197 test_task_then_legacy_execution_log_golden` | **FAITHFUL (correctly scoped to exec-log only)** | NO (by design — see note) |
| TM-8 | `test_per_phase_budget.py:311 test_legacy_phase_after_task_phase_has_fresh_ledger` | **FAITHFUL** | YES |
| TM-9 | `:424 test_single_task_overspend_trips_safety_net` | **FAITHFUL** | Partial (see WEAK-2) |
| TM-10 | `:472 test_heavy_phase1_cannot_starve_phase2` | **FAITHFUL** | YES |
| TM-11 | `:516 test_skip_and_python_phases_construct_no_ledger` | **FAITHFUL (with caveat — see WEAK-3 / raises note)** | YES |
| TM-12 | `test_turn_ledger_concurrency.py:44 test_try_launch_admits_exactly_task_count_under_kgt1` | **FAITHFUL** | N/A (model concurrency) |
| TM-13 | `test_per_phase_budget.py:613 test_kpi_wiring_totals_accumulate_across_phases` | **FAITHFUL** | YES — strongest mutation guard in the suite |
| TM-14 | `:678 test_resume_window_sizes_phase_identically` | **FAITHFUL** | YES |

### Spec-mandated spot checks (all PASS)

- **TM-0**: `@pytest.mark.regression` present (`:175`) + registered (`pyproject.toml:144`); asserts `available()==500` at each of 3 phase entries (`:220-222`), `skipped==[]` (`:215`), all phases PASS (`:206`), `SUCCESS` (`:203`). Reversion check: old pool → one ledger of budget 300, so `len(ledgers)==3` (`:219`) fails, `initial_budget==500` fails, AND 300 turns drain the 300-pool → skips appear. Triple-guarded. ✔
- **TM-9**: task1 PASS / task2,3 SKIPPED (`:451-453`); `remaining=={"T01.02","T01.03"}` populated (`:457`); phase mapped ERROR (`:463`). Overspend is GENUINE within-phase: budget=30, task1 reconciles to actual=28 (debit 5 then debit 23 → available=2 < min_allocation 5), real gate trips. Traced against `executor.py:1165-1170` + `1473`. ✔
- **TM-13**: reads the PERSISTED `gate-kpi-report.md` (`:652-654`), pins `Analyses run: == 5` single value (`:657`) with `!=2` last-phase guard implicit via `used != 2`/`credited != 8` (`:665,669`). Math verified against real model: `debit_wiring(1)`→used+1,count+1; `credit_wiring(5)`→`int(5*0.8)=4`. P1(3)+P2(2): used 5, credited 20, count 5. Last-phase-only revert → 2/8/2 → all three asserts fail. The strongest hollow-proof test here. ✔
- **TM-11**: spy targets `TurnLedger.__init__` ONLY (`patch.object(TurnLedger,"__init__",...)`, `:566`), NOT the accumulator; the accumulator is a `_SprintWiringTotals` (confirmed `executor.py:336`, not a TurnLedger), so it is correctly invisible to the spy. Asserts exactly one construction (`:587`), skip→SKIPPED/exit 0 (`:595-596`). ✔
- **TM-7**: asserts ONLY the execution log `(number, status, exit_code)` (`test_multi_phase.py:285-291`); no wiring assertion. Correctly scoped per R-6/§6 ("Does NOT cover wiring delta — see TM-13"). ✔

---

## Deviation list (4-category taxonomy)

No **Regression** and no **Drift** found at the spec-vs-test-matrix level: every TM row maps to a node that asserts its specified condition, with correct file placement matching §6's "File (reuse)" column. The findings below are **weaknesses within faithful tests** (test-quality observations), not divergences from the spec's intent — I classify each.

### WEAK-1 — TM-6 monotonicity arm is a tautology-leaning assertion — **Drift (minor, test-internal)**
`test_models.py:960`. The load-bearing half (`hasattr(TurnLedger,'reset') is False`, `:972-973`) is genuinely the requirement and faithful. The monotonicity half (`:976-985`) debits a fixed increasing sequence `(3,0,7,5)` and asserts `consumed` non-decreasing — but `consumed` can ONLY increase by construction (there is no decrement API), so this arm would pass for ANY ledger implementation that has a `debit`. It does not discriminate the per-phase model from anything. It is duplicative of the much stronger `test_budget_monotonicity_*` already in the same class (`:755,763`). Not wrong, just non-load-bearing. Spec R-7's real teeth are the `hasattr` arm, which IS present — so the TM-6 verdict stays FAITHFUL.

### WEAK-2 — TM-9 asserts ERROR via a RE-DERIVATION, not the executor's own mapping — **Necessary deviation (acceptable, but weaker than TM-0)**
`test_per_phase_budget.py:461-463`. TM-9 calls `execute_phase_tasks(...)` directly (not the full `execute_sprint`), so it never observes the executor's real phase→`PhaseStatus.ERROR` mapping. It re-implements that mapping in the test: `phase_status = PASS if report.status=="PASS" else ERROR` (`:462`). This is a **characterization of the test's own logic**, not of the executor's. If the executor's status-mapping logic changed, TM-9 would not catch it — it would keep asserting its own re-derived value. The PASS/SKIPPED/`remaining` assertions ARE faithful (they come from the real `execute_phase_tasks` return), so the core safety-net behavior is genuinely pinned; only the "phase ERROR" clause is softened. Spec §6 TM-9 lists "phase ERROR" as an assert — the test technically covers it but via a parallel re-derivation rather than the SUT. Contrast TM-0 (`:206`), which asserts `pr.status == PhaseStatus.PASS` straight off the real `SprintResult`. Recommend (non-blocking) TM-9 drive through `execute_sprint` to assert the real `PhaseStatus.ERROR`. Verdict stays FAITHFUL because the discriminating behavior (which tasks SKIP, `remaining`) is real.

### WEAK-3 / `pytest.raises(SystemExit)` judgment on TM-11 — **Necessary deviation (legitimate accommodation, NOT a mask)**
`test_per_phase_budget.py:583`. I judge this a **legitimate accommodation of pre-existing skip-phase behavior**, not a mask. Rationale:
1. The `SystemExit` is orthogonal to TM-11's assertions. A sprint containing a SKIP phase exits non-zero because `PhaseStatus.SKIPPED ∉ is_success` (confirmed `test_models.py:92`, `SKIPPED → is_success False`), so the sprint outcome is ERROR → `SystemExit(1)`. This is identical to the documented pattern in `test_multi_phase.py:168` (`TestHaltAtPhaseThree` wraps `execute_sprint` in `pytest.raises(SystemExit)` and checks `exc.value.code == 1`).
2. The two TM-11 assertions both read state captured **before** the exit: `construct_count` is mutated inside `__init__` during the loop (`:587`), and `captured[0]` is populated by `write_summary` which fires before the outcome-driven exit (`:592-596`).
3. **However** — TM-11's `pytest.raises(SystemExit)` is broad: it does not assert `exc.value.code`. `test_multi_phase.py:170` does (`assert exc.value.code == 1`). A bare `pytest.raises(SystemExit)` would swallow an *unexpected* `SystemExit(0)` or a different exit path. Minor hardening gap, not a correctness mask. Recommend pinning `.code == 1` for parity with the sibling test. Verdict FAITHFUL.

### Note on TM-7 "not mutation-sensitive" — **Authorized (by design)**
TM-7 would pass under the old global pool too, because it asserts only the subprocess execution log, which the refactor leaves byte-equivalent. This is INTENTIONAL per R-6/§6 (the wiring delta is pinned by TM-13, not TM-7). Correctly scoped; flagged here only so the ensemble doesn't mis-read its insensitivity as a defect.

---

## Adversarial mandate disclosure

I was instructed to assume ≥3 tests are weak and to find them. I surfaced 3 genuine test-quality weaknesses (WEAK-1 tautology-leaning monotonicity arm; WEAK-2 re-derived ERROR mapping; WEAK-3 un-pinned exit code). I judge **none of them to rise to a spec deviation (Drift/Regression) that would falsify a TM row** — each test still pins its load-bearing §6 condition through real SUT behavior. I explicitly did NOT manufacture a fourth finding to hit a quota. The strongest tests (TM-0, TM-13, TM-10, TM-8, TM-5, TM-1, TM-14) are all robustly mutation-sensitive: I confirmed by tracing each against the real construction site (`executor.py:1920-1921`), the real gate (`:1473`), the real reconcile (`:1165-1170`), and the real R-10 chain (`:336`, `:2009-2014`, `:2400-2405`, `:2540-2543`).

---

## [INFERRED] (not directly verified, lower confidence)

- **[INFERRED]** TM-12's `@pytest.mark.thread_safety` is registered (`pyproject.toml:136`) and the test is the K>1 admission check §6 specifies; I verified the assertion shape (`granted == task_count`, `:67`) but did NOT re-run it under a stress harness to confirm the RLock actually prevents over-admission under real contention — pytest's single run with `2×task_count` attempts across ≤16 workers is a probabilistic, not exhaustive, race check. Faithful to §6, but its power against a subtle lock bug is statistical.
- **[INFERRED]** I did not exhaustively confirm that `_make_task_config`'s default `wiring_gate_mode="off"` / `wiring_gate_scope="none"` produce a pass-through wiring hook in EVERY path; TM-13 overrides the hook entirely so it's unaffected, but TM-8's `_spy_wiring_hook` relies on "off → passthrough" being true (comment `:374`). I read the assertion but did not trace `run_post_phase_wiring_hook` end-to-end under `off`.
- **[INFERRED]** The `_parse_kpi_int` helper (`:605-610`) does `line.rsplit(maxsplit=1)[-1]` against label substrings "Turns used:", "Turns credited:", "Analyses run:". I confirmed these labels exist in `kpi.py:140-143`. I did NOT confirm no OTHER line in the report contains those substrings such that the FIRST match is the intended one — `_parse_kpi_int` returns on first match, so a duplicate-substring line above the real one would silently mis-parse. Low risk given the current report format, but unverified.

---

## Calibrated self-confidence: **0.86**

Basis: I read all 5 target files in full, re-Read the live executor construction site / gate / reconcile / R-10 chain and the kpi.py reader/labels, ran the suite myself (46 passed), and traced reversion-sensitivity for the load-bearing TMs against real source line numbers. Confidence is held below 0.9 by: (a) the three `[INFERRED]` items I did not exhaustively verify (thread-safety race power, off-mode passthrough, KPI label uniqueness); (b) I did not run a true mutation test (e.g. revert R-10/R-2 and re-run) — my reversion claims are by source-trace reasoning, strong but not executed.

## One-line verdict

All 13 TM rows are **FAITHFUL** and the suite is GREEN with real (non-stubbed) per-phase ledger exercise; three minor, non-blocking test-quality weaknesses (TM-6 tautology arm, TM-9 re-derived ERROR mapping, TM-11 un-pinned exit code) are noted but none falsifies a spec row — recommend ACCEPT with optional hardening.
