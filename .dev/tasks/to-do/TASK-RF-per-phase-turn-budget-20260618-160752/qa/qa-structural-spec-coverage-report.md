# QA Report — Report Validation (Template-Conformance / Spec-Coverage Lens)

**Topic:** Per-Phase Turn-Budget Model for the Sprint Runner
**Date:** 2026-06-18
**Phase:** report-validation (structural spec-coverage)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)
**Lens:** template-conformance / spec-coverage

**Spec:** `.dev/brainstorms/20260618-per-phase-turn-budget/merged-requirements-FINAL.md` (§4 R-1..R-10, §6 TM-0..TM-14 [TM-3/TM-4 do not exist], §8 K-1/K-2/K-3)
**Implementation:** `src/superclaude/cli/sprint/executor.py`, `models.py`
**Tests:** `tests/sprint/test_per_phase_budget.py`, `test_models.py`, `test_turn_ledger_concurrency.py`, `test_multi_phase.py`

---

## Method

Cross-walk every R-id against an actual code change in executor.py/models.py, every TM-id against a test function carrying the spec's EXACT node name, and verify K-2 comment / K-3 grep artifact / TM-0 marker presence. Evidence-first; each verdict cites file:line or spec ID.

## Overall Verdict: PASS

Every R-1..R-10 has a corresponding, correctly-placed code change in `executor.py`/`models.py`; every TM-0,1,2,5,6,7,8,9,10,11,12,13,14 has a real test function carrying the spec's exact node name (where the spec pins one) in the spec's named file; no R-/TM-/K- ID was silently dropped; the K-2 construction-site comment, K-3 grep artifact, and TM-0 `@pytest.mark.regression` marker are all present; the full spec-mandated suite is green (46 passed). The "≥5 planted spec-coverage errors" premise is NOT borne out — I found zero CRITICAL/IMPORTANT coverage gaps and one MINOR documentation-only observation. A false FAIL would be as much a process violation as a false PASS; the evidence below is cited file:line / spec ID for every verdict.

## R-item Coverage Matrix

| R-id | Spec requirement | Code evidence | Verdict |
|------|------------------|---------------|---------|
| R-1 | Delete global pre-loop ledger (`max_turns × len(active_phases)`); keep neighbors | Construction GONE; only `TurnLedger(` construction is per-phase @`executor.py:1920`. Removal-marker comment @`1824-1830`. `len(config.active_phases)` survives only in comment @1826, loop @1873, K-2 comment @1913, merge @2490 — none is a ledger construction | PASS |
| R-2 | Fresh phase-sized ledger after `continue` guards, before `if tasks:`; `else 1` floor; K-2 comment | `ledger = TurnLedger(initial_budget=config.max_turns * (len(tasks) if tasks else 1), reimbursement_rate=0.8)` @`executor.py:1920-1923`; `else 1` present; placed after guards, before `if tasks:` @1924 | PASS |
| R-3 | `available()==max_turns×task_count`, `consumed==0` at phase entry | Structural from R-2 fresh build; pinned by TM-0 (`available()==500` at each of 3 phases) @`test_per_phase_budget.py:222-225` | PASS |
| R-4 | Independence by construction (reimburse + wiring start at 0 each phase) | Consequence of R-2 (no new code required); pinned by TM-5 @`test_per_phase_budget.py:267` and TM-10 @472 | PASS (see MINOR-1) |
| R-5 | No gate code change; comment → "phase budget exhausted" safety-net | Safety-net framing comments @`executor.py:1273` (parallel) + `1465` (sequential); no gate logic change | PASS |
| R-6 | Legacy subprocess log byte-equiv; wiring-hook ledger input refined + documented | Docstring delta @`executor.py:821-839`; hook calls @1996 (task) / 2388 (legacy); deliberate-refinement wording present | PASS |
| R-7 | `TurnLedger` docstring tightened to per-instance/per-phase monotonicity; no method change | Docstring @`models.py:1018-1025`; no `reset`/`reallocate` added (TM-6 asserts `hasattr` False) | PASS |
| R-8 | python/skip phases construct no ledger | R-2 placement after both `continue` guards; comment @`executor.py:1900`; pinned by TM-11 (exactly one `__init__`) | PASS |
| R-9 | Fresh ledger built in parent before fan-out; all workers joined before next phase | K-2 invariant comment @`executor.py:1912-1919`; `__post_init__` RLock @`models.py:1044-1050`; pinned by TM-12 | PASS |
| R-10 | Sprint-level wiring accumulator; pass accumulator (not last-phase ledger) to `build_kpi_report` | `_SprintWiringTotals` dataclass @`executor.py:336-357`; instance @1842; add-sites @2009 (after task hook 1996) + 2400 (after legacy hook 2388); `turn_ledger=sprint_wiring_totals` @2543 | PASS |

## TM-item Coverage Matrix (exact node-name check)

| TM-id | Spec node name | Found | Verdict |
|-------|----------------|-------|---------|
| TM-0 | `test_per_phase_budget.py::test_regression_3x5_no_global_pool_starvation`, `@pytest.mark.regression` | def @176, marker @175, registered in `pyproject.toml:144` | PASS |
| TM-1 | `::test_per_phase_ledger_is_fresh_each_phase` | @230 | PASS |
| TM-2 | `test_models.py::TestTurnLedger` (class; n∈{1,5}+defensive n=0) | class @`test_models.py:626`; `test_per_phase_sizing_for_task_counts` @940 | PASS |
| TM-5 | `test_per_phase_budget.py` (reimburse phase1 / phase2 unaffected) | `test_phase1_reimbursement_does_not_affect_phase2` @267 | PASS |
| TM-6 | `test_models.py::TestTurnLedger` (no reset + monotonicity) | `test_no_in_place_reset_and_consumed_monotonic` @960 | PASS |
| TM-7 | `test_multi_phase.py` (task→legacy execution-log golden) | `test_task_then_legacy_execution_log_golden` @`test_multi_phase.py:197` | PASS |
| TM-8 | `::test_legacy_phase_after_task_phase_has_fresh_ledger` | @311 | PASS |
| TM-9 | `::test_single_task_overspend_trips_safety_net` | @424 (task1=28, tasks2-3 SKIPPED, phase ERROR all asserted) | PASS |
| TM-10 | `test_per_phase_budget.py` (heavy phase1 cannot starve phase2) | `test_heavy_phase1_cannot_starve_phase2` @472 | PASS |
| TM-11 | `::test_skip_and_python_phases_construct_no_ledger` | @516 | PASS |
| TM-12 | `test_turn_ledger_concurrency.py` (K>1, pool=task_count×min_alloc) | `test_try_launch_admits_exactly_task_count_under_kgt1` @`test_turn_ledger_concurrency.py:44` | PASS |
| TM-13 | `::test_kpi_wiring_totals_accumulate_across_phases` | @613 (asserts analyses_run==5, used==5, credited==20, single pinned value) | PASS |
| TM-14 | `::test_resume_window_sizes_phase_identically` | @678 | PASS |

TM-3 / TM-4 do not exist in the spec §6 matrix — correctly absent, not flagged.

## K-item Coverage

| K-id | Requirement | Evidence | Verdict |
|------|-------------|----------|---------|
| K-1 | Legacy late-phase wiring delta documented + pinned by TM-13 | Documented in hook docstring @`executor.py:821-839`; TM-13 pins it | PASS |
| K-2 | Sequential-phase invariant stated in construction-site comment | Comment @`executor.py:1912-1919` ("K-2 SEQUENTIAL-PHASE INVARIANT … phases run serially …") | PASS |
| K-3 | Pre-merge grep artifact for new ledger-wiring consumers | `phase-outputs/discovery/k3-premerge-grep.txt` (raw, 22 hits) + `k3-grep-summary.md` (classified clean) | PASS |

## kpi.py reader / accumulator field-mapping spot check

The accumulator field is `wiring_analyses_count`; the persisted report field is `wiring_analyses_run`. The reader maps them correctly: `report.wiring_analyses_run = turn_ledger.wiring_analyses_count` @`kpi.py:197`. The `_SprintWiringTotals` accumulator exposes exactly the three attribute names the reader reads (`wiring_turns_used` @193, `wiring_turns_credited` @195, `wiring_analyses_count` @197) — confirmed @`executor.py:355-357`. No field-name mismatch.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | R-1 removal (no `active_phases`-sized ledger construction) | PASS | `executor.py:1920` is the only `TurnLedger(` construction; per-phase sized |
| 2 | R-2 placement + `else 1` floor + sizing | PASS | `executor.py:1920-1923` after both guards, before `if tasks:` @1924 |
| 3 | R-3 entry invariant | PASS | TM-0 asserts `available()==500` @`test_per_phase_budget.py:222-225` |
| 4 | R-4 independence | PASS | TM-5 @267 (`phase2_available_at_entry==200`), TM-10 @472 |
| 5 | R-5 gate safety-net comments, no logic change | PASS | comments @`executor.py:1273`,`1465` |
| 6 | R-6 legacy delta documented | PASS | docstring @`executor.py:821-839` |
| 7 | R-7 models docstring per-instance monotonicity | PASS | `models.py:1018-1025`; no mutator added |
| 8 | R-8 skip/python no ledger | PASS | comment @`executor.py:1900`; TM-11 @516 |
| 9 | R-9 thread-safety / RLock + parent-build | PASS | K-2 comment @`executor.py:1912`; RLock @`models.py:1044`; TM-12 @44 |
| 10 | R-10 accumulator + arg-swap | PASS | `_SprintWiringTotals` @336; add-sites @2009/2400; arg @2543 |
| 11 | TM-0..14 exact node names present | PASS | matrix above; all `::node` names match the spec |
| 12 | TM-0 `@pytest.mark.regression` present + registered | PASS | marker @175; `pyproject.toml:144` |
| 13 | K-2 construction-site comment | PASS | `executor.py:1912-1919` |
| 14 | K-3 grep artifact on disk | PASS | `phase-outputs/discovery/k3-premerge-grep.txt` + `k3-grep-summary.md` |
| 15 | No silently-dropped R-/TM-/K- ID | PASS | all 10 R, all 13 TM, all 3 K accounted for |
| 16 | Suite green | PASS | `uv run pytest … -v` → 46 passed in 4.33s |
| 17 | kpi reader / accumulator field mapping | PASS | `kpi.py:197` maps `wiring_analyses_count`→`wiring_analyses_run` |

## Summary
- Checks passed: 17 / 17
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| MINOR-1 | MINOR | `phase-2-5-output-summary.md:10` (manifest only — NOT a code defect) | The review-scope summary's "Modified / new SOURCE files" R-id column for `executor.py` lists `R-1,R-2,R-3,R-5,R-6,R-8,R-9,R-10` and omits **R-4**. R-4 ("independence by construction") is genuinely covered — it requires no new code (it is a structural consequence of R-2's fresh per-phase construction) and is test-pinned by TM-5 (`executor.py:1920` fresh build → TM-5 @`test_per_phase_budget.py:267`) and TM-10 @472. This is a documentation/manifest completeness nit in the summary's ID-tagging, not a missing code change or a dropped requirement. | Optionally add `R-4` to the executor.py R-id column in the summary manifest, annotated "(no new code — structural consequence of R-2; verified by TM-5/TM-10)". No source/test change needed. |

## Confidence Gate

**Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 3 | Grep: 0 | Glob: 0 | Bash: 7 (each Bash call directly verified specific R-/TM-/K- items via grep/sed/pytest against the cited files; no padding)

All checklist items were VERIFIED with tool output (file:line citations above). No item is UNCHECKED or UNVERIFIABLE. Web research not required — every claim verified is intrinsically local (code/spec/test files in this worktree), so source-truth-first applied throughout; Tavily-first rule not triggered.

## Self-Audit

The premise asserted ≥5 planted spec-coverage errors. I searched adversarially: cross-walked all 10 R-ids to placed code, all 13 TM-ids to exact-node-name test functions, checked the accumulator/reader field-name mapping for a silent mismatch (none — `wiring_analyses_count`→`wiring_analyses_run` @`kpi.py:197` is correct), checked R-2's load-bearing `else 1` floor (present), checked the R-10 add-site ordering relative to the wiring hooks (task add @2009 after hook @1996; legacy add @2400 after hook @2388 — both correct), and ran the suite (46 passed). The only deviation found is a manifest-level ID-tagging omission (R-4) that is behaviorally covered. Reporting a fabricated FAIL to satisfy the "≥5 errors" framing would itself be a false verdict. Evidence supports PASS.

## Recommendations
- Proceed. No code or test change is gated on this lens.
- Optional (non-blocking): add R-4 to the summary manifest's executor.py R-id column for completeness (MINOR-1).

## QA Complete

**OVERALL VERDICT: PASS** — All 10 R-items, all 13 TM-items (exact node names), and K-1/K-2/K-3 are present and correct; suite green (46 passed); one MINOR manifest-only documentation nit (R-4 untagged in the summary, but behaviorally covered). Zero CRITICAL/IMPORTANT spec-coverage gaps.
