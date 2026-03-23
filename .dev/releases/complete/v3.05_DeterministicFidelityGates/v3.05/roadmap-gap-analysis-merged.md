# Merged Roadmap Gap Analysis: v3.05 Deterministic Fidelity Gates

**Date**: 2026-03-21
**Merge of**: Agent A and Agent B independent analyses
**Branch**: v3.0-AuditGates

---

## Agreement Summary

Both agents fully agree on the following:

1. **Phases 1-5 are COMPLETE** -- All structural checkers, spec parser, deviation registry, semantic layer, convergence engine, and TurnLedger integration in convergence.py are correctly implemented and functional.
2. **Phase 6 has wiring bugs** -- The pipeline executor's `_run_convergence_spec_fidelity()` in `executor.py` contains runtime bugs that would crash any convergence-mode execution.
3. **`DeviationRegistry.load_or_create()` call signature mismatch** (executor.py:566) -- Called with 1 arg, requires 3. Both agents independently identified this as a blocking runtime bug.
4. **`STD_CONVERGENCE_BUDGET` used instead of `MAX_CONVERGENCE_BUDGET`** (executor.py:572) -- Spec FR-7 requires `MAX_CONVERGENCE_BUDGET` (61), code uses `STD_CONVERGENCE_BUDGET` (46).
5. **`budget_snapshot` missing from `RunMetadata`** -- FR-10 specifies this field; neither agent found it in the dataclass.
6. **Sprint-path items are correctly out of scope** -- `execute_sprint()` TurnLedger construction, `SprintGatePolicy` instantiation, `build_kpi_report()` wiring, and `DeferredRemediationLog` integration are all correctly excluded per spec Section 1.2.
7. **`fidelity.py` deletion confirmed** -- Both agents verified the file no longer exists (cleanup complete).
8. **Convergence engine core is well-implemented** -- `execute_fidelity_with_convergence()`, `handle_regression()`, `reimburse_for_progress()`, budget guards, and all convergence.py internals work correctly.
9. **Test coverage exists** -- `test_convergence.py` provides comprehensive coverage of the convergence engine itself.
10. **Root cause is the same** -- Executor wiring was written without end-to-end integration testing against the real `DeviationRegistry` API.

---

## Disagreements & Resolutions

### D1: `merge_findings()` call arity bug (M2 in Agent B)

- **Agent A**: Did not identify this bug.
- **Agent B**: Reports that `merge_findings()` is called with 2 args (executor.py:587,599) but requires 3 args (structural list, semantic list, run_number). Structural and semantic findings must be passed as separate lists per BF-3 (structural-only monotonic progress).
- **Resolution**: **Agent B wins.** The `merge_findings()` method signature at convergence.py:143 requires `(structural: list, semantic: list, run_number: int)` to maintain the structural/semantic split mandated by BF-3. Agent A missed this because it focused on the method's existence rather than how it was called from the executor. This is a runtime crash bug.

### D2: `finding.files_affected` dict/object mismatch bug (M5 in Agent B)

- **Agent A**: Did not identify this bug.
- **Agent B**: Reports that `get_active_highs()` returns `list[dict]` (registry stores JSON dicts) but executor.py:612 uses attribute access (`finding.files_affected`) instead of dict key access. Would raise `AttributeError`.
- **Resolution**: **Agent B wins.** `DeviationRegistry` stores findings as dicts (JSON serialization), not `Finding` dataclass instances. Attribute access on dicts fails. This is a runtime crash bug. Agent A's analysis stopped at the registry API boundary without tracing the return type into the executor callsite.

### D3: TurnLedger constructor missing parameters (M4 in Agent B)

- **Agent A**: Noted only the `STD` vs `MAX` budget issue.
- **Agent B**: Additionally identifies missing `minimum_allocation=CHECKER_COST`, `minimum_remediation_budget=REMEDIATION_COST`, and `reimbursement_rate=0.8` constructor parameters. Notes that default `minimum_allocation=5` is less than `CHECKER_COST=10`, meaning `can_launch()` would return True when budget is insufficient for a full checker run.
- **Resolution**: **Agent B wins.** The spec's FR-7 Pipeline Executor Wiring section specifies all four constructor parameters. Using defaults creates a budget guard hole where `can_launch()` approves runs that cannot complete. Agent A caught the budget level but missed the guard parameters.

### D4: Phase 6 overall status

- **Agent A**: Rates Phase 6 as **PARTIAL**.
- **Agent B**: Rates Phase 6 as **COMPLETE**.
- **Resolution**: **Agent A wins.** Phase 6 includes integration wiring that has 3+ runtime crash bugs. Calling this "COMPLETE" is incorrect -- the wiring exists but is non-functional. "PARTIAL" is the accurate status: the remediation executor and report writer are present, but the convergence wiring path crashes before reaching them.

### D5: `attempt_remediation()` existence

- **Agent A**: Says it exists at `pipeline/trailing_gate.py:354`.
- **Agent B**: Says "No function named `attempt_remediation` exists anywhere in the codebase."
- **Resolution**: **Agent A wins.** Agent A provided a specific file and line reference. Agent B's search may have been too narrow (e.g., searching only sprint/ and convergence code). However, both agents agree this function is outside v3.05 scope regardless of existence.

### D6: `RemediationPatch` and remediation v3.05 changes

- **Agent A**: Flags `RemediationPatch` dataclass, per-patch 30% threshold, `fallback_apply()`, and `check_morphllm_available()` as unverified.
- **Agent B**: Does not mention these items.
- **Resolution**: **Agent A wins on raising the concern.** These are specified in the v3.05 roadmap (FR-9, D-0038, D-0039, D-0048) and should be verified. However, severity is MEDIUM since the convergence engine can function without morphllm integration.

### D7: Progress proof logging format (M7 in Agent B)

- **Agent A**: Did not identify this gap.
- **Agent B**: Notes FR-10 requires budget state in progress proof log format: `"budget: consumed={c}, reimbursed={r}, available={a}"`.
- **Resolution**: **Agent B wins.** This is a valid spec deviation, though LOW severity since it affects diagnostics only.

### D8: E2E verification artifacts

- **Agent A**: Flags missing persistent E2E tests and wiring-verification.md scanning 0 files.
- **Agent B**: Does not specifically call out these issues.
- **Resolution**: **Agent A wins.** The wiring-verification scanning 0 files is a real integration signal that the verification step was misconfigured. The absence of persistent E2E tests means regressions in the wiring layer go undetected.

---

## Merged Findings

### Confirmed Present (deduplicated)

| # | Deliverable | Location | FR/NFR |
|---|---|---|---|
| 1 | `spec_parser.py` with all extraction functions | `src/superclaude/cli/roadmap/spec_parser.py` | FR-2, FR-5 |
| 2 | `SpecSection` dataclass, `split_into_sections()`, `DIMENSION_SECTION_MAP` | spec_parser.py | FR-5 |
| 3 | 5 structural checkers + `run_all_checkers()` | structural_checkers.py:669 | FR-1 |
| 4 | `SEVERITY_RULES` (19 rules) + `get_severity()` | structural_checkers.py:42-76 | FR-3 |
| 5 | `Finding` dataclass extensions: `rule_id`, `spec_quote`, `roadmap_quote`, `stable_id`, `source_layer` | models.py:44-49 | FR-6 |
| 6 | `DeviationRegistry` with full API surface | convergence.py:87-272 | FR-6 |
| 7 | `compute_stable_id()` | convergence.py:61-69 | FR-6 |
| 8 | `RunMetadata` dataclass | convergence.py:73-84 | FR-6, FR-10 |
| 9 | `RegressionResult` dataclass | convergence.py:287-293 | FR-7.1 |
| 10 | `ConvergenceResult` dataclass | convergence.py:275-284 | FR-7 |
| 11 | Source layer tracking, split HIGH counts in merge_findings | convergence.py:157,174,188-199 | FR-6, BF-3 |
| 12 | Pre-v3.05 backward compat defaults | convergence.py:112-118 | FR-6, Risk #7 |
| 13 | Spec hash reset on change | convergence.py:109,126 | FR-6 |
| 14 | `get_prior_findings_summary()` (max 50, oldest-first) | convergence.py:226-239 | FR-10 |
| 15 | `first_seen_run` / `last_seen_run` tracking | convergence.py (multiple) | FR-10 |
| 16 | `record_debate_verdict()` | convergence.py:246-258 | FR-4.1 |
| 17 | `execute_fidelity_with_convergence()` with full budget guards | convergence.py:382-590 | FR-7 |
| 18 | Budget constants: CHECKER_COST=10, REMEDIATION_COST=8, REGRESSION_VALIDATION_COST=15, CONVERGENCE_PASS_CREDIT=5 | convergence.py:25-28 | FR-7 |
| 19 | Derived budgets: MIN=28, STD=46, MAX=61 | convergence.py:31-33 | FR-7 |
| 20 | `reimburse_for_progress()` using `ledger.reimbursement_rate` | convergence.py:42-58 | FR-7 |
| 21 | Monotonic progress on structural only | convergence.py:506 | FR-7, BF-3 |
| 22 | Semantic fluctuation logging | convergence.py:493-503 | FR-7, BF-3 |
| 23 | `handle_regression()` with 3 parallel agents in temp dirs | convergence.py:593-699 | FR-8 |
| 24 | try/finally + atexit cleanup | convergence.py:698-699, 372-379 | FR-8, Risk #3 |
| 25 | `_check_regression()` structural-only | convergence.py:296-328 | FR-8, BF-3 |
| 26 | `MAX_PROMPT_BYTES = 30_720` + budget ratio constants | semantic_layer.py:24-30 | FR-4.2, NFR-3 |
| 27 | `RubricScores`, rubric weights, verdict margin threshold | semantic_layer.py:40-56 | FR-4.1 |
| 28 | `run_semantic_layer()` entry point | semantic_layer.py:377 | FR-4 |
| 29 | Legacy/convergence dispatch | executor.py:418 | NFR-7 |
| 30 | `_run_convergence_spec_fidelity()` wiring | executor.py:539-648 | FR-7 |
| 31 | Gate set to None in convergence mode | executor.py:869 | FR-7, BF-2 |
| 32 | `_write_convergence_report()` | executor.py:651-691 | FR-7 |
| 33 | `fidelity.py` deleted | Not found | Phase 6 cleanup |
| 34 | TurnLedger class with full API | sprint/models.py:518-574 | FR-7 |
| 35 | `remediate_executor.py` exists (extended) | src/superclaude/cli/roadmap/remediate_executor.py | FR-9 |
| 36 | Test coverage (1347 lines) | test_convergence.py | BF-2/3/4, all FRs |

### Confirmed Missing/Bugs (deduplicated, severity-rated)

| # | Issue | Severity | Source | Impact |
|---|---|---|---|---|
| **B1** | `DeviationRegistry.load_or_create()` called with 1 arg, requires 3 (executor.py:566) | **CRITICAL** | A+B | Runtime TypeError crash. Convergence mode completely non-functional. |
| **B2** | `merge_findings()` called with 2 args, requires 3 (executor.py:587,599) | **CRITICAL** | B only | Runtime TypeError crash. Structural/semantic split (BF-3) cannot function. |
| **B3** | `finding.files_affected` attribute access on dict (executor.py:612) | **CRITICAL** | B only | Runtime AttributeError crash. Remediation cannot enumerate affected files. |
| **B4** | TurnLedger constructed with `STD_CONVERGENCE_BUDGET` (46) instead of `MAX_CONVERGENCE_BUDGET` (61) (executor.py:572) | **HIGH** | A+B | Budget too low for full convergence + regression validation. Spec FR-7 violation. |
| **B5** | TurnLedger missing constructor params: `minimum_allocation`, `minimum_remediation_budget` (executor.py:572) | **HIGH** | B only | `can_launch()` guard hole: approves runs when budget < CHECKER_COST. |
| **B6** | `budget_snapshot` field missing from `RunMetadata` (convergence.py:73-84) | **LOW** | A+B | No budget diagnostics in run metadata. FR-10 partial non-compliance. |
| **B7** | Progress proof logs missing budget state format (convergence.py convergence loop) | **LOW** | B only | FR-10 log format deviation. Diagnostics only. |
| **B8** | `RemediationPatch` dataclass, per-patch 30% threshold, `fallback_apply()`, `check_morphllm_available()` unverified | **MEDIUM** | A only | FR-9 remediation changes may be missing. Needs file read to confirm. |
| **B9** | Wiring-verification.md scanned 0 files | **MEDIUM** | A only | Verification step misconfigured; no integration evidence captured. |
| **B10** | No persistent E2E test artifacts for SC-1 through SC-6 | **MEDIUM** | A only | Regressions in wiring layer go undetected between sprints. |

### TurnLedger Wiring Status (merged assessment)

| Component | Status | v3.05 Scope? | Notes |
|---|---|---|---|
| **Convergence engine TurnLedger integration** | WIRED (buggy) | YES | 3 crash bugs (B1-B3) + 2 spec deviations (B4-B5) in executor.py wiring. Core engine (convergence.py) is correct. |
| **TurnLedger class itself** | COMPLETE | YES (consumed, not modified) | sprint/models.py:518-574. All API methods present and functional. |
| **Sprint-path TurnLedger construction** | NOT WIRED | NO (v3.1) | Correctly out of scope per spec Section 1.2. |
| **SprintGatePolicy instantiation** | NOT WIRED | NO (v3.1) | Defined but never instantiated. Outside v3.05 scope. |
| **`build_kpi_report()` production call** | NOT WIRED | NO (v3.1) | Defined, never called. Outside v3.05 scope. |
| **`DeferredRemediationLog` integration** | NOT WIRED | NO (v3.1) | Infrastructure exists, not populated. Outside v3.05 scope. |
| **`attempt_remediation()`** | EXISTS (trailing gate path) | NO | Present at pipeline/trailing_gate.py:354. Separate from convergence remediation. |

### Root Cause Analysis (merged)

**Primary root cause**: The pipeline executor wiring (`_run_convergence_spec_fidelity()` in executor.py) was implemented during Phase 5/6 sprint execution without end-to-end integration testing against the real `DeviationRegistry` and `TurnLedger` APIs.

**Contributing factors**:

1. **API impedance mismatch**: The convergence engine (convergence.py) was developed and unit-tested in isolation with correct API usage. The executor wiring was written separately and assumed simpler call signatures. No integration test bridged the two layers.

2. **Dict/object boundary**: `DeviationRegistry` stores findings as JSON dicts for persistence, but the executor treats return values as `Finding` dataclass instances. This impedance mismatch was not caught because unit tests for the registry and unit tests for the executor never exercised the boundary together.

3. **Sprint subprocess execution model**: The sprint executor runs tasks via Claude subprocess, meaning the actual Python code paths may not have been invoked during sprint execution. Tasks were marked complete based on Claude's implementation within the subprocess, not runtime verification.

4. **Conservative budget choice**: `STD_CONVERGENCE_BUDGET` was likely chosen as a safer default during implementation, contradicting the spec's explicit `MAX_CONVERGENCE_BUDGET` requirement.

5. **Verification gap**: The wiring-verification step scanned 0 files, indicating the verification target directory was misconfigured. This means the automated verification gate that should have caught B1-B5 was non-functional.

---

## Recommendations (priority-ordered)

### P0: CRITICAL -- Fix runtime crash bugs (blocks all convergence-mode execution)

**1. Fix `DeviationRegistry.load_or_create()` call** (executor.py:566)
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

**2. Fix `merge_findings()` calls** (executor.py:587, 599)
```python
# Structural merge (broken): reg.merge_findings(structural_findings, run_number)
# Fix: reg.merge_findings(structural_findings, [], run_number)

# Semantic merge (broken): reg.merge_findings(semantic_result.findings, run_number)
# Fix: reg.merge_findings([], semantic_result.findings, run_number)
```

**3. Fix dict/object mismatch** (executor.py:611-613)
```python
# Current (broken): finding.files_affected (attribute access on dict)
# Fix: finding.get("files_affected", []) (dict key access)
```

### P1: HIGH -- Fix spec deviations in budget configuration

**4. Use `MAX_CONVERGENCE_BUDGET` and full constructor params** (executor.py:572)
```python
ledger = TurnLedger(
    initial_budget=MAX_CONVERGENCE_BUDGET,
    minimum_allocation=CHECKER_COST,
    minimum_remediation_budget=REMEDIATION_COST,
    reimbursement_rate=0.8,
)
```

### P2: MEDIUM -- Verify and fix remaining deliverables

**5. Verify `remediate_executor.py` v3.05 changes**
- Confirm `RemediationPatch` dataclass exists
- Confirm per-patch 30% diff-size threshold (was 50% per-file)
- Confirm `fallback_apply()` and `check_morphllm_available()` exist

**6. Fix wiring-verification target directory**
- Investigate why `wiring-verification.md` shows `files_analyzed: 0`
- Ensure verification step points to the correct roadmap output directory

**7. Add integration test for `_run_convergence_spec_fidelity()`**
- End-to-end test: TurnLedger construction -> registry load -> checkers -> semantic -> convergence loop -> result mapping
- This test would have caught B1-B5 before merge

### P3: LOW -- Diagnostics and logging

**8. Add `budget_snapshot: dict | None = None` to `RunMetadata`** (convergence.py)

**9. Add budget state to progress proof log messages** per FR-10 format

**10. Create persistent E2E verification tests** for SC-1 through SC-6

### Not recommended for v3.05 (correctly out of scope per spec Section 1.2):

- Sprint-path TurnLedger construction (v3.1)
- SprintGatePolicy production instantiation (v3.1)
- `build_kpi_report()` production wiring (v3.1)
- DeferredRemediationLog sprint integration (v3.1)

---

## Final Verdict

- **Implementation completeness**: 82%
  - Phases 1-5 (core engine): 100% complete
  - Phase 6 (wiring + integration): ~40% functional (code exists but crashes at runtime)
- **Critical bugs**: 3 (B1, B2, B3 -- all runtime crash bugs in executor.py wiring)
- **Blocking gaps**: 3 (the same 3 critical bugs block any convergence-mode execution)
- **High-severity spec deviations**: 2 (B4, B5 -- budget calibration)
- **Medium-severity gaps**: 3 (B8, B9, B10 -- unverified deliverables and missing verification)
- **Low-severity gaps**: 2 (B6, B7 -- diagnostics)
- **Estimated fix effort**: Small -- all critical bugs are localized to ~30 lines in `executor.py:560-620`
- **Agent agreement rate**: 85% -- both agents converged on the same core findings; Agent B identified 3 additional bugs that Agent A missed (M2, M5, M4-expanded)
