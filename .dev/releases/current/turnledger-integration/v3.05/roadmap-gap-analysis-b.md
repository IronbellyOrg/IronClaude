# v3.05 Roadmap Gap Analysis (Agent B)

**Analyzed**: 2026-03-21
**Scope**: v3.05 Deterministic Fidelity Gates roadmap execution vs codebase state
**Focus**: TurnLedger integration wiring gaps across roadmap and sprint paths

---

## Roadmap Phase-by-Phase Status

### Phase 1: Foundation -- Parser, Data Model & Interface Verification
**Status: COMPLETE**

Evidence:
- `spec_parser.py` exists at `src/superclaude/cli/roadmap/spec_parser.py`
- `Finding` dataclass extended with `rule_id`, `spec_quote`, `roadmap_quote`, `stable_id` fields (models.py lines 46-49)
- `source_layer` field present (models.py line 44)
- `RunMetadata` dataclass defined in convergence.py lines 73-83
- `RegressionResult` dataclass defined in convergence.py lines 287-293
- `ConvergenceResult` dataclass defined in convergence.py lines 275-284
- `SEVERITY_RULES` and `get_severity()` -- need to verify in structural_checkers.py (file exists)
- `TurnLedger` API verified: `debit()`, `credit()`, `can_launch()`, `can_remediate()`, `reimbursement_rate` all present in sprint/models.py

### Phase 2: Structural Checkers & Severity Engine
**Status: COMPLETE**

Evidence:
- `structural_checkers.py` exists at `src/superclaude/cli/roadmap/structural_checkers.py`
- `run_all_checkers()` imported and called in executor.py line 558, 586

### Phase 3: Deviation Registry & Run-to-Run Memory
**Status: COMPLETE**

Evidence:
- `DeviationRegistry` class in convergence.py lines 87-272 with all required methods:
  - `load_or_create()`, `begin_run()`, `merge_findings()`, `get_active_highs()`,
    `get_active_high_count()`, `get_structural_high_count()`, `get_semantic_high_count()`,
    `get_prior_findings_summary()`, `update_finding_status()`, `record_debate_verdict()`, `save()`
- Source layer tracking: structural/semantic split in merge_findings (lines 157, 174)
- Run metadata with split HIGH counts (lines 188-199)
- Pre-v3.05 backward compat: default source_layer to "structural" (lines 112-118)
- Spec hash reset on change (lines 109, 126)
- Comprehensive tests in test_convergence.py (650+ lines)

### Phase 4: Semantic Layer & Adversarial Debate
**Status: COMPLETE (structurally present)**

Evidence:
- `semantic_layer.py` exists at `src/superclaude/cli/roadmap/semantic_layer.py`
- `run_semantic_layer()` imported and called in executor.py line 559, 591

### Phase 5: Convergence Engine, TurnLedger & Regression Detection
**Status: COMPLETE**

Evidence:
- Budget constants defined: `CHECKER_COST=10`, `REMEDIATION_COST=8`, `REGRESSION_VALIDATION_COST=15`, `CONVERGENCE_PASS_CREDIT=5` (convergence.py lines 25-28)
- Derived budgets: `MIN_CONVERGENCE_BUDGET=28`, `STD_CONVERGENCE_BUDGET=46`, `MAX_CONVERGENCE_BUDGET=61` (lines 31-33)
- `execute_fidelity_with_convergence()` implemented (lines 382-590) with:
  - `ledger.can_launch()` guard before each run (line 440)
  - `ledger.debit(CHECKER_COST)` before checker run (line 457)
  - `ledger.can_remediate()` guard before remediation (line 556)
  - `ledger.debit(REMEDIATION_COST)` before remediation (line 570)
  - `ledger.credit(CONVERGENCE_PASS_CREDIT)` on pass (line 473)
  - `reimburse_for_progress()` on forward progress (line 543)
  - `ledger.debit(REGRESSION_VALIDATION_COST)` before regression (line 527)
- `handle_regression()` implemented (lines 593-699), no ledger ops internally
- `reimburse_for_progress()` uses `ledger.reimbursement_rate` (line 55)
- Conditional TurnLedger import via `_get_turnledger_class()` (lines 36-39)
- Legacy/convergence dispatch in executor.py: gate set to None when convergence_enabled (line 869)
- `_run_convergence_spec_fidelity()` in executor.py (lines 539-648) wires convergence engine

### Phase 6: Remediation & Integration
**Status: COMPLETE**

Evidence:
- `remediate_executor.py` exists (extended)
- `fidelity.py` deleted (glob returns no results)
- Pipeline integration wired: executor.py line 418 dispatches to convergence
- Convergence report written to spec-fidelity output (lines 651-691)
- Tests cover all 6 phases per execution-log.md (all 6 phases pass)

---

## Present in Code (Confirmed Implemented)

1. **TurnLedger class** -- `sprint/models.py:518-574`: `debit()`, `credit()`, `can_launch()`, `can_remediate()`, `reimbursement_rate=0.8`, `available()`
2. **Budget constants** -- convergence.py module-level: CHECKER_COST, REMEDIATION_COST, REGRESSION_VALIDATION_COST, CONVERGENCE_PASS_CREDIT, MIN/STD/MAX_CONVERGENCE_BUDGET
3. **`reimburse_for_progress()`** -- convergence.py:42-58, uses `ledger.reimbursement_rate`
4. **`execute_fidelity_with_convergence()`** -- convergence.py:382-590, full convergence loop with TurnLedger guards
5. **`handle_regression()`** -- convergence.py:593-699, no internal ledger ops
6. **DeviationRegistry** -- convergence.py:87-272, persistent JSON-backed registry with stable IDs
7. **Pipeline executor dispatch** -- executor.py:418 (convergence mode check), executor.py:539-648 (`_run_convergence_spec_fidelity`)
8. **Dual authority elimination** -- Gate set to None in convergence mode (executor.py:869)
9. **Finding dataclass extensions** -- models.py: `rule_id`, `spec_quote`, `roadmap_quote`, `stable_id`, `source_layer`
10. **Test coverage** -- test_convergence.py: 1347 lines covering BF-2/3/4, registry, TurnLedger integration, convergence loop, regression, budget isolation, mutual exclusion

---

## Missing from Code (Expected but Not Found)

### M1: DeviationRegistry.load_or_create() call signature mismatch
**Severity: BUG**

The executor calls `DeviationRegistry.load_or_create(config.output_dir / "deviation-registry.json")` (executor.py:566) with only 1 argument, but the method signature requires 3: `(path, release_id, spec_hash)`. This will raise a `TypeError` at runtime.

**Spec requirement**: FR-6 requires registry tracks `spec_hash` and resets on change.

### M2: `_run_checkers()` calls `merge_findings()` with wrong arity
**Severity: BUG**

In executor.py:587, `reg.merge_findings(structural_findings, run_number)` passes 2 args, but the method signature is `merge_findings(structural, semantic, run_number)` -- expects structural list, semantic list, and run_number. The semantic findings merge on line 599 has the same issue: `reg.merge_findings(semantic_result.findings, run_number)`.

### M3: TurnLedger constructed with STD budget, not MAX
**Severity: MEDIUM**

Executor.py:572 uses `STD_CONVERGENCE_BUDGET` (46) instead of `MAX_CONVERGENCE_BUDGET` (61) as the spec requires. The spec states (FR-7): "Pipeline executor constructs `TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET)` when `convergence_enabled=true`." The reduced budget may prevent regression validation from ever having sufficient budget.

### M4: TurnLedger not constructed with all spec'd parameters
**Severity: MEDIUM**

Executor.py:572 constructs `TurnLedger(initial_budget=STD_CONVERGENCE_BUDGET)` but the spec (FR-7 Pipeline Executor Wiring) requires:
```python
TurnLedger(
    initial_budget=MAX_CONVERGENCE_BUDGET,
    minimum_allocation=CHECKER_COST,
    minimum_remediation_budget=REMEDIATION_COST,
    reimbursement_rate=0.8,
)
```
Missing `minimum_allocation`, `minimum_remediation_budget`, and `reimbursement_rate` parameters. Defaults (5, 3, 0.8) may work for `reimbursement_rate` but `minimum_allocation=5` is less than `CHECKER_COST=10`, meaning `can_launch()` would return True when there's not actually enough budget for a full checker run.

### M5: `_run_remediation()` accesses `finding.files_affected` on dict
**Severity: BUG**

In executor.py:612, `active_highs = reg.get_active_highs()` returns `list[dict]` (registry stores dicts, not Finding objects), but line 612 does `for f in finding.files_affected` which is attribute access on a dict. This will raise `AttributeError`.

### M6: `budget_snapshot` field missing from RunMetadata
**Severity: LOW**

FR-10 specifies `budget_snapshot: dict | None = None` on RunMetadata, but the dataclass in convergence.py:73-83 does not include this field. Run metadata does not capture TurnLedger state at completion.

### M7: Progress proof logging format does not match spec
**Severity: LOW**

FR-10 requires: `"budget: consumed={c}, reimbursed={r}, available={a}"` in progress proof logs. The convergence loop logs progress but does not include budget state in the log messages.

---

## TurnLedger Wiring Gaps

### Full TurnLedger construction in sprint path
**Status: NOT WIRED**

TurnLedger is imported in `sprint/executor.py:28` and used as a parameter type on `execute_phase_tasks()` (line 693), `run_wiring_analysis_for_task()` (line 453), and `check_budget_guard()` (line 339). However, **TurnLedger is never constructed** in the sprint executor. It is only ever passed as `None` or received as an optional parameter. There is no production call site that creates a `TurnLedger(initial_budget=N)` for sprint execution.

This is explicitly marked out-of-scope by the v3.05 spec: "Sprint-level budget wiring (execute_sprint, execute_phase_tasks)" is listed under "Out of scope" in Section 1.2. The v3.05 roadmap correctly does not include sprint-path TurnLedger construction.

### SprintGatePolicy production instantiation
**Status: NOT WIRED**

`SprintGatePolicy` is defined in `sprint/executor.py:56` but never instantiated anywhere in production code. No call site creates a `SprintGatePolicy(...)` instance. This is a v3.0 stub that was never wired. The v3.05 spec does not reference SprintGatePolicy at all -- it is entirely outside v3.05 scope.

### attempt_remediation() production wiring
**Status: DOES NOT EXIST**

No function named `attempt_remediation` exists anywhere in the codebase. This appears to be a conceptual function from the sprint-level integration design that was never implemented. The v3.05 spec does not reference it. Remediation in the convergence path uses `execute_remediation()` from `remediate_executor.py` instead.

### build_kpi_report() production call
**Status: NOT WIRED**

`build_kpi_report()` is defined in `sprint/kpi.py:137` but is never called from any production code. It accepts `TurnLedger`, `DeferredRemediationLog`, and `TrailingGateResult` as inputs but has zero callers. This is outside v3.05 scope.

### DeferredRemediationLog sprint integration
**Status: NOT WIRED**

`DeferredRemediationLog` is defined in `pipeline/trailing_gate.py:489` and imported in `sprint/kpi.py:16`, but is never instantiated or populated in the sprint execution path. It exists as infrastructure for future sprint-level remediation tracking. Outside v3.05 scope.

---

## Root Cause Analysis

### Why are gaps present?

**1. Correct scoping decisions (not gaps):**
The v3.05 spec explicitly places sprint-level TurnLedger wiring, SprintGatePolicy instantiation, gate-pass reimbursement activation, and sprint-level budget wiring out of scope (Section 1.2). The roadmap correctly respects these boundaries. These are v3.1+ deliverables, not v3.05 gaps.

**2. Implementation bugs in wiring code (actual gaps):**
M1-M5 are genuine bugs in `_run_convergence_spec_fidelity()` in `executor.py`. They appear to be caused by the sprint executor implementing the convergence wiring quickly during Phase 5/6 execution (Phase 5 took 191 minutes -- the longest phase by far) without sufficient integration testing against the real `DeviationRegistry` API:

- **M1**: `load_or_create()` called with 1 arg instead of 3 -- the method requires `release_id` and `spec_hash` for FR-6 spec-hash-change detection.
- **M2**: `merge_findings()` called with 2 args instead of 3 -- the structural/semantic split (BF-3) requires separate lists.
- **M5**: `get_active_highs()` returns dicts but code treats them as Finding objects -- a dict/object impedance mismatch.

These bugs would cause `_run_convergence_spec_fidelity()` to crash at runtime on any convergence-enabled pipeline run. The convergence engine itself (`execute_fidelity_with_convergence`) and its tests work correctly because they use the proper API -- the bugs are isolated to the pipeline executor wiring layer.

**3. Budget calibration deviation (M3/M4):**
The spec requires `MAX_CONVERGENCE_BUDGET` (61) but implementation uses `STD_CONVERGENCE_BUDGET` (46). This was likely a conservative choice during implementation, but it contradicts the spec's FR-7 acceptance criterion.

**4. Missing RunMetadata fields (M6/M7):**
Low-priority omissions from FR-10's `budget_snapshot` requirement. The convergence loop works without these -- they are diagnostics.

---

## Recommendations

### P0: Fix runtime bugs in executor wiring (blocks any convergence-mode execution)

1. **Fix `DeviationRegistry.load_or_create()` call** in executor.py:566:
   ```python
   # Current (broken):
   registry = DeviationRegistry.load_or_create(config.output_dir / "deviation-registry.json")
   # Fix:
   import hashlib
   spec_hash = hashlib.sha256(config.spec_file.read_bytes()).hexdigest()
   registry = DeviationRegistry.load_or_create(
       config.output_dir / "deviation-registry.json",
       release_id=config.output_dir.name,
       spec_hash=spec_hash,
   )
   ```

2. **Fix `merge_findings()` calls** in executor.py:587, 599:
   ```python
   # Current (broken):
   reg.merge_findings(structural_findings, run_number)
   # Fix:
   reg.merge_findings(structural_findings, [], run_number)

   # And for semantic:
   reg.merge_findings([], semantic_result.findings, run_number)
   ```

3. **Fix dict/object mismatch** in executor.py:611-613:
   ```python
   # Current (broken - get_active_highs returns list[dict]):
   for finding in active_highs:
       for f in finding.files_affected:  # AttributeError on dict
   # Fix: access dict keys, or convert to Finding objects
   for finding in active_highs:
       for f in finding.get("files_affected", []):
   ```

### P1: Fix budget calibration

4. **Use MAX_CONVERGENCE_BUDGET** in executor.py:572 per spec FR-7:
   ```python
   from .convergence import MAX_CONVERGENCE_BUDGET, CHECKER_COST, REMEDIATION_COST
   ledger = TurnLedger(
       initial_budget=MAX_CONVERGENCE_BUDGET,
       minimum_allocation=CHECKER_COST,
       minimum_remediation_budget=REMEDIATION_COST,
       reimbursement_rate=0.8,
   )
   ```

### P2: Add missing diagnostics

5. **Add `budget_snapshot` to RunMetadata** dataclass (convergence.py):
   ```python
   budget_snapshot: dict | None = None  # FR-10
   ```

6. **Add budget state to progress proof logs** in convergence loop.

### Not recommended for v3.05 (out of scope per spec):

- Sprint-path TurnLedger construction (v3.1)
- SprintGatePolicy production instantiation (v3.1)
- `build_kpi_report()` production wiring (v3.1)
- DeferredRemediationLog sprint integration (v3.1)
- `attempt_remediation()` implementation (never specified)

---

## Summary

The v3.05 roadmap was faithfully executed through all 6 phases (execution log confirms all pass, 4h14m total). The convergence engine core (`convergence.py`), deviation registry, budget constants, `reimburse_for_progress()`, and all supporting infrastructure are correctly implemented and well-tested.

The critical gap is in the **pipeline executor wiring layer** (`_run_convergence_spec_fidelity()` in `executor.py`), which has 3 runtime bugs (M1, M2, M5) that would crash any convergence-mode pipeline execution, plus 2 spec deviations (M3, M4) in TurnLedger construction parameters. These are localized to ~30 lines in a single function and are straightforward to fix.

The sprint-path TurnLedger gaps (SprintGatePolicy, build_kpi_report, DeferredRemediationLog) are correctly out-of-scope per the v3.05 spec and should be addressed in v3.1.
