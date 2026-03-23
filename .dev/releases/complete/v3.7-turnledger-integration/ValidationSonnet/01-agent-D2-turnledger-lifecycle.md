# Agent D2 — Domain: turnledger_lifecycle
## Coverage Assessment Report

**Agent**: D2
**Domain**: turnledger_lifecycle
**Spec**: v3.3-requirements-spec.md
**Roadmap**: roadmap.md
**Date**: 2026-03-23
**Requirements Assessed**: REQ-024 (FR-2.1), REQ-025 (FR-2.1a), REQ-026 (FR-2.2), REQ-027 (FR-2.3), REQ-028 (FR-2.4), REQ-SC2 (SC-2)

---

## Prior Context

A prior validation run identified FR-2.1a (`handle_regression()` reachability) as MISSING from the roadmap. This report re-examines every assigned requirement with fresh eyes against the current roadmap to determine whether gaps were addressed in the final merged roadmap.

---

## Coverage Assessments

---

### REQ-024: FR-2.1 — Convergence Path E2E

- **Spec source**: v3.3-requirements-spec.md §FR-2.1
- **Spec text**: "Exercise `execute_fidelity_with_convergence()` end-to-end. Assert: debit `CHECKER_COST` → run checkers → credit `CONVERGENCE_PASS_CREDIT` → `reimburse_for_progress()`; Assert: budget_snapshot recorded in registry runs; Assert: budget logging includes consumed/reimbursed/available"
- **Status**: COVERED
- **Match quality**: EXACT
- **Evidence**:
  - Roadmap location: Phase 2 §2B, Task 2B.1
  - Roadmap text: "2B.1 | FR-2.1 | Convergence path (v3.05): `execute_fidelity_with_convergence()` E2E — debit `CHECKER_COST` → run checkers → credit `CONVERGENCE_PASS_CREDIT` → `reimburse_for_progress()`; budget_snapshot recorded"
  - Additional roadmap location: Executive Summary §Delivery Outcomes
  - Additional roadmap text: "TurnLedger lifecycle validated across all execution paths (FR-2, SC-2)"
  - Additional roadmap location: Success Criteria Validation Matrix
  - Additional roadmap text: "SC-2 | 4/4 TurnLedger paths green | `test_turnledger_lifecycle.py` all pass | 2 | Yes"
  - Additional roadmap location: §New Files Created table
  - Additional roadmap text: "`tests/v3.3/test_turnledger_lifecycle.py` | 2B | FR-2 lifecycle tests"
- **Analysis**: Roadmap Task 2B.1 reproduces the spec's three assertions verbatim (debit/credit/reimburse chain, budget_snapshot, budget logging). The "budget logging includes consumed/reimbursed/available" sub-assertion is implicit in the "budget_snapshot recorded" coverage but the roadmap does not explicitly call it out as a separate assertion. However, the roadmap text for 2B.1 ends with "budget_snapshot recorded" — the spec also requires the logging to include "consumed/reimbursed/available" as a third distinct bullet. The roadmap collapses these into one statement. This is a minor omission in explicitness but the intent is clearly captured.
- **Confidence**: HIGH

---

### REQ-025: FR-2.1a — Regression Handler Reachability

- **Spec source**: v3.3-requirements-spec.md §FR-2.1a
- **Spec text**: "Assert `handle_regression()` is reachable from `_run_convergence_spec_fidelity` and is called on regression detection. Assert: when convergence detects a regression (score decreases between runs), `handle_regression()` is invoked. Assert: `handle_regression()` logs the regression event and adjusts budget accordingly. Spec reference: convergence.py, wiring manifest entry `v3.05-FR8`"
- **Status**: PARTIAL
- **Match quality**: WEAK
- **Evidence**:
  - Roadmap location (direct behavioral test): ABSENT — No task in Phase 2B (TurnLedger lifecycle tests) covers `handle_regression()` behavioral testing.
  - Roadmap location (wiring manifest): Phase 1 §1B.4, wiring manifest YAML embedded in spec
  - Roadmap text (1B.4): "1B.4 | FR-4.1 | Initial wiring manifest YAML for executor.py entry points — `tests/v3.3/wiring_manifest.yaml`"
  - Roadmap location (manifest content): The roadmap spec cross-references the wiring manifest in the spec document itself (§Wiring Manifest v3.3), which includes: `target: superclaude.cli.roadmap.convergence.handle_regression` / `from_entry: _run_convergence_spec_fidelity` / `spec_ref: "v3.05-FR8"`
  - Roadmap text (reachability gate): Phase 3 §3B.2: "3B.2 | FR-4.4, SC-7, SC-9 | Regression test: remove `run_post_phase_wiring_hook()` call → gate detects gap referencing v3.2-T02"
- **Finding**:
  - **Severity**: HIGH
  - **Gap description**: The roadmap covers `handle_regression()` reachability ONLY through the static AST reachability gate (via wiring manifest entry `v3.05-FR8` in 1B.4). It does NOT include a behavioral test that:
    1. Exercises `_run_convergence_spec_fidelity` with an actual regression scenario (score decrease between runs)
    2. Asserts `handle_regression()` is invoked at runtime
    3. Asserts `handle_regression()` logs the regression event and adjusts the budget

    Task 2B.1 covers FR-2.1 (convergence happy path) but makes no mention of the regression branch. The wiring manifest entry proves static reachability but does NOT prove the function is actually called when a regression is detected. FR-2.1a requires both: reachability AND behavioral invocation under regression conditions.

    The prior validation run's finding that "FR-2.1a missing from roadmap" remains materially correct. The manifest entry in 1B.4 adds static reachability coverage, but the behavioral testing gap persists.
  - **Impact**: The regression handler may be statically reachable but never exercised by any test. A bug in the regression-detection branch or in `handle_regression()`'s budget adjustment logic would go undetected.
  - **Recommended correction**: Add Task 2B.1a (or extend 2B.1) in Phase 2B: "Regression detection sub-test: configure two consecutive convergence runs where run 2 scores lower than run 1; assert `handle_regression()` is called; assert log event recorded; assert ledger budget adjusted." Also explicitly reference FR-2.1a in the 2B task table.
- **Confidence**: HIGH

---

### REQ-026: FR-2.2 — Sprint Per-Task Path

- **Spec source**: v3.3-requirements-spec.md §FR-2.2
- **Spec text**: "Exercise `execute_sprint()` → `execute_phase_tasks()` with task-inventory phase. Assert: pre-debit `minimum_allocation` → subprocess → reconcile actual vs pre-allocated; Assert: post-task hooks (wiring + anti-instinct) fire with ledger"
- **Status**: COVERED
- **Match quality**: EXACT
- **Evidence**:
  - Roadmap location: Phase 2 §2B, Task 2B.2
  - Roadmap text: "2B.2 | FR-2.2 | Sprint per-task path (v3.1): pre-debit `minimum_allocation` → subprocess → reconcile; post-task hooks fire with ledger"
  - Additional roadmap location: Appendix A §A.2
  - Roadmap text: "Phase 2 validates both branches via FR-1.5, FR-1.6, FR-2.2, FR-2.3, FR-2.4"
  - Additional roadmap location: §2B subtotal note
  - Roadmap text: "Subtotal: 4 tests covering SC-2."
- **Analysis**: Roadmap 2B.2 maps directly to FR-2.2's two assertions: the pre-debit/reconcile chain and the post-task hooks firing with ledger. The `reconcile actual vs pre-allocated` nuance is collapsed to "reconcile" but the intent is preserved. Both post-task hooks (wiring + anti-instinct) are implicitly covered — the roadmap says "post-task hooks fire with ledger" matching spec's "(wiring + anti-instinct)".
- **Confidence**: HIGH

---

### REQ-027: FR-2.3 — Sprint Per-Phase Path

- **Spec source**: v3.3-requirements-spec.md §FR-2.3
- **Spec text**: "Exercise `execute_sprint()` → ClaudeProcess fallback → `run_post_phase_wiring_hook()`. Assert: `debit_wiring()` called → analysis → `credit_wiring()` on non-blocking result; Assert: `wiring_analyses_count` incremented"
- **Status**: COVERED
- **Match quality**: EXACT
- **Evidence**:
  - Roadmap location: Phase 2 §2B, Task 2B.3
  - Roadmap text: "2B.3 | FR-2.3 | Sprint per-phase path (v3.2): `debit_wiring()` → analysis → `credit_wiring()` on non-blocking; `wiring_analyses_count` incremented"
  - Additional roadmap location: Appendix A §A.3
  - Roadmap text: "Phase 2 proves both call sites (FR-1.7); Phase 3 uses FR-4.4 to detect broken reachability ... Cross-Reference: FR-1.7, FR-3.1a–d, FR-4.4"
  - Additional roadmap location: §2B subtotal
  - Roadmap text: "Subtotal: 4 tests covering SC-2."
- **Analysis**: Roadmap 2B.3 reproduces the spec's two assertions verbatim: the debit/analysis/credit chain on non-blocking result, and the `wiring_analyses_count` increment. All three spec elements (ClaudeProcess fallback path, debit/credit wiring cycle, counter increment) are present in the roadmap task description.
- **Confidence**: HIGH

---

### REQ-028: FR-2.4 — Cross-Path Coherence

- **Spec source**: v3.3-requirements-spec.md §FR-2.4
- **Spec text**: "Sprint with mixed phases (some task-inventory, some freeform). Assert: ledger state is coherent after both paths execute; Assert: `available()` = `initial_budget - consumed + reimbursed` holds at every checkpoint"
- **Status**: COVERED
- **Match quality**: EXACT
- **Evidence**:
  - Roadmap location: Phase 2 §2B, Task 2B.4
  - Roadmap text: "2B.4 | FR-2.4 | Cross-path coherence: mixed task-inventory + freeform phases; `available() = initial_budget - consumed + reimbursed` at every phase checkpoint"
  - Additional roadmap location: Open Questions §Q.6
  - Roadmap text: "Assert `available()` invariant after each phase completion — this is where the ledger state is observable and deterministic. Per-task or per-hook is too granular and couples tests to internal sequencing."
- **Analysis**: Roadmap 2B.4 matches the spec exactly: mixed phases, coherence assertion, and the specific formula `available() = initial_budget - consumed + reimbursed`. The Open Questions entry adds implementation guidance (assert at phase boundaries, not per-hook), which refines but does not contradict the spec. The spec's "at every checkpoint" is interpreted as "after each phase completion" — a reasonable and documented implementation choice.
- **Confidence**: HIGH

---

### REQ-SC2: SC-2 — TurnLedger Lifecycle All 4 Paths

- **Spec source**: v3.3-requirements-spec.md §Success Criteria, SC-2
- **Spec text**: "TurnLedger lifecycle covered for ALL 4 paths (convergence, per-task, per-phase, cross-path) | Metric: Convergence, per-task, per-phase, cross-path | Phase: 2"
- **Status**: PARTIAL
- **Match quality**: SEMANTIC
- **Evidence**:
  - Roadmap location: §2B subtotal note
  - Roadmap text: "Subtotal: 4 tests covering SC-2."
  - Roadmap location: Success Criteria Validation Matrix
  - Roadmap text: "SC-2 | 4/4 TurnLedger paths green | `test_turnledger_lifecycle.py` all pass | 2 | Yes"
  - Roadmap location: Executive Summary §Delivery Outcomes
  - Roadmap text: "TurnLedger lifecycle validated across all execution paths (FR-2, SC-2)"
  - Roadmap location: Phase 2 §2B tasks 2B.1–2B.4 (covering all 4 paths by FR reference)
- **Finding**:
  - **Severity**: HIGH
  - **Gap description**: SC-2 requires ALL 4 paths to be covered. The roadmap maps SC-2 to 4 tasks (2B.1–2B.4) covering convergence (FR-2.1), per-task (FR-2.2), per-phase (FR-2.3), and cross-path (FR-2.4). Three of these four paths are fully covered with exact spec mapping. However, Task 2B.1 (the convergence path) is PARTIAL with respect to FR-2.1a: the regression branch of the convergence path is not behaviorally tested. Since SC-2 requires the convergence path to be fully covered, and FR-2.1a is part of that path's lifecycle (it defines what happens when convergence detects a regression), SC-2's "convergence" coverage is incomplete.

    The roadmap's assertion "4/4 TurnLedger paths green" is accurate for the happy-path convergence scenario but does not account for the regression sub-path, which is a distinct lifecycle branch within the convergence path.
  - **Impact**: The SC-2 success criterion cannot be declared fully met if the regression branch of the convergence lifecycle remains untested. A release claiming SC-2 green would be technically misleading.
  - **Recommended correction**: Extend Task 2B.1 with the regression detection sub-scenario (as described in REQ-025 recommended correction). Once 2B.1 covers both happy-path and regression sub-paths, SC-2 can legitimately claim all 4 paths green.
- **Confidence**: HIGH

---

## Critical Check Results

### Check 1: Does roadmap 2B explicitly cover FR-2.1a?

**Finding**: NO. Task 2B.1 in the roadmap reads: "FR-2.1 | Convergence path (v3.05): `execute_fidelity_with_convergence()` E2E — debit `CHECKER_COST` → run checkers → credit `CONVERGENCE_PASS_CREDIT` → `reimburse_for_progress()`; budget_snapshot recorded". There is no mention of FR-2.1a, `handle_regression()`, or regression detection in Task 2B.1 or anywhere in Phase 2B.

### Check 2: Does wiring manifest 1B.4 include handle_regression() entry?

**Finding**: YES, but conditionally. The wiring manifest content defined in the spec (§Wiring Manifest v3.3) includes:
```
- target: superclaude.cli.roadmap.convergence.handle_regression
  from_entry: _run_convergence_spec_fidelity
  spec_ref: "v3.05-FR8"
```
Task 1B.4 directs creation of "Initial wiring manifest YAML for executor.py entry points — `tests/v3.3/wiring_manifest.yaml`". The roadmap does not explicitly state that `handle_regression` will appear in the generated manifest file. The manifest content in the spec document serves as the authoritative definition, and the roadmap's 1B.4 task references "FR-4.1" (the manifest schema requirement), which points back to the spec. This creates an implicit chain: 1B.4 produces the manifest → the spec defines its content → that content includes `handle_regression`. This is an IMPLICIT link, not an explicit one. The static reachability coverage is therefore present but indirect.

### Check 3: Does SC-2 require convergence path separately from sprint paths?

**Finding**: YES. SC-2 explicitly lists "Convergence, per-task, per-phase, cross-path" as four separate items with the metric "4/4 TurnLedger paths green". The convergence path is distinct from the sprint paths. The roadmap correctly treats them as separate tasks (2B.1 vs 2B.2–2B.4), but the convergence path coverage is incomplete due to the missing FR-2.1a behavioral test.

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total requirements assessed | 6 |
| COVERED | 3 (REQ-024, REQ-026, REQ-027) |
| PARTIAL | 2 (REQ-025, REQ-SC2) |
| MISSING | 0 |
| CONFLICTING | 0 |
| IMPLICIT | 0 |
| Match quality EXACT | 3 |
| Match quality SEMANTIC | 1 |
| Match quality WEAK | 1 |
| Match quality NONE | 0 |

| Severity | Count | Requirements |
|----------|-------|-------------|
| CRITICAL | 0 | — |
| HIGH | 2 | REQ-025 (FR-2.1a), REQ-SC2 |
| MEDIUM | 0 | — |
| LOW | 0 | — |

### Coverage Rate
- Fully covered: 3/6 (50%)
- Partially covered: 2/6 (33%)
- Uncovered: 0/6 (0%)
- Effective coverage (counting PARTIAL as 0.5): 4/6 (67%)

### Root Cause

Both gaps (REQ-025 and REQ-SC2) share the same root cause: the behavioral regression sub-path within the convergence lifecycle (FR-2.1a, `handle_regression()`) has no corresponding E2E test task in the roadmap. The static reachability gate (via the wiring manifest) catches whether `handle_regression()` is reachable from `_run_convergence_spec_fidelity`, but it does NOT verify:
1. That the regression detection logic triggers `handle_regression()` under the correct conditions
2. That `handle_regression()` logs the regression event
3. That `handle_regression()` adjusts the budget correctly

This is a single targeted gap. A single additional test task in Phase 2B would resolve both REQ-025 and the convergence-path incompleteness in REQ-SC2.

### Priority Action

**Add Task 2B.1a to Phase 2B** in `tests/v3.3/test_turnledger_lifecycle.py`:
> FR-2.1a — Regression detection path: configure two consecutive convergence runs where run 2 yields a lower score than run 1; assert `handle_regression()` is invoked; assert regression event is logged; assert ledger budget is adjusted as specified.

This single addition closes both HIGH-severity findings.
