# v3.05 Roadmap Gap Analysis (Agent A)

**Date**: 2026-03-21
**Scope**: v3.05 Deterministic Fidelity Gates -- roadmap vs codebase cross-reference
**Branch**: v3.0-AuditGates

---

## Roadmap Phase-by-Phase Status

### Phase 1: Foundation -- Parser, Data Model & Interface Verification
**Tasks**: T01.01-T01.07 (7 tasks)
**Status**: COMPLETE

**Evidence**:
- `spec_parser.py` exists at `src/superclaude/cli/roadmap/spec_parser.py` with `SpecSection` dataclass, `split_into_sections()`, `parse_document()`, YAML frontmatter extraction, table extraction, code block extraction, requirement ID regex, function signature extraction, `Literal[...]` enum extraction, threshold extraction, file path extraction, and `DIMENSION_SECTION_MAP` (convergence.py imports from it)
- `structural_checkers.py` imports `SpecSection`, `CodeBlock`, `FunctionSignature`, `MarkdownTable`, `ThresholdExpression`, `extract_*` functions from `spec_parser.py` -- confirming FR-2 and FR-5
- `Finding` dataclass in `models.py` confirmed extended (structural_checkers.py uses it with `rule_id` fields)
- `SEVERITY_RULES` dict and `get_severity()` function in `structural_checkers.py:42-76` -- all 19 canonical rules present
- `RunMetadata` dataclass in `convergence.py:73-84`
- `RegressionResult` dataclass in `convergence.py:287-293`
- `compute_stable_id()` in `convergence.py:61-69`
- `DeviationRegistry` in `convergence.py:87-272`
- `_get_turnledger_class()` conditional import in `convergence.py:36-39`
- Interface verification (TurnLedger API: `debit()`, `credit()`, `can_launch()`, `can_remediate()`, `reimbursement_rate`) confirmed in `sprint/models.py:518-563`

### Phase 2: Structural Checkers & Severity Engine
**Tasks**: T02.01-T02.05 (5 tasks)
**Status**: COMPLETE

**Evidence**:
- `structural_checkers.py` exists with all 5 checkers and `run_all_checkers()` at line 669
- `SEVERITY_RULES` contains all 19 canonical `(dimension, mismatch_type)` entries (lines 42-67)
- `get_severity()` raises `KeyError` on unknown combinations (line 76: direct dict lookup)
- Checker callable interface: `(spec_path, roadmap_path) -> list[Finding]`
- Checker registry maps dimension names to callables (imported by `run_all_checkers`)
- No shared mutable state between checkers (NFR-4)

### Phase 3: Deviation Registry & Run-to-Run Memory
**Tasks**: T03.01-T03.04 (4 tasks)
**Status**: COMPLETE

**Evidence**:
- `DeviationRegistry` in `convergence.py:87-272` with:
  - `source_layer` field support (lines 112-114 backward compat; line 174 new findings)
  - Stable ID computation via `compute_stable_id()` (line 159-160)
  - Cross-run comparison: `merge_findings()` matches by stable ID, marks FIXED (lines 143-199)
  - `first_seen_run` / `last_seen_run` tracking (lines 115-118, 165-166, 168-169)
  - Run metadata with split HIGH counts: `structural_high_count`, `semantic_high_count`, `total_high_count` (lines 188-199)
  - Spec version change detection -> registry reset (line 109-126)
  - Pre-v3.05 backward compatibility: default `source_layer` to `"structural"` (lines 112-114)
  - `ACTIVE` as valid status (line 166)
- `get_prior_findings_summary()` at line 226 (max 50, oldest-first truncation)
- `record_debate_verdict()` at line 246

### Phase 4: Semantic Layer & Adversarial Debate
**Tasks**: T04.01-T04.06 (6 tasks)
**Status**: COMPLETE

**Evidence**:
- `semantic_layer.py` exists at `src/superclaude/cli/roadmap/semantic_layer.py` with:
  - `MAX_PROMPT_BYTES = 30_720` (line 24)
  - Budget ratio constants (lines 27-30): 60/20/15/5 allocation
  - `TRUNCATION_MARKER` template (line 32)
  - `RubricScores` dataclass (lines 50-56) with `weighted_score` property
  - `RUBRIC_WEIGHTS` (lines 40-45): evidence 30%, impact 25%, coherence 25%, concession 20%
  - `VERDICT_MARGIN_THRESHOLD = 0.15` (line 47)
  - `DEBATE_TOKEN_CAP = 5_000` (line 37)
  - `run_semantic_layer()` entry point (line 377)
  - Imported and called from `executor.py:559,591`

### Phase 5: Convergence Engine, TurnLedger & Regression Detection
**Tasks**: T05.01-T05.09 (9 tasks)
**Status**: COMPLETE

**Evidence**:
- **TurnLedger integration**: `_get_turnledger_class()` conditional import (convergence.py:36-39)
- **Cost constants** module-level in convergence.py: `CHECKER_COST=10`, `REMEDIATION_COST=8`, `REGRESSION_VALIDATION_COST=15`, `CONVERGENCE_PASS_CREDIT=5` (lines 23-28)
- **Derived budgets**: `MIN_CONVERGENCE_BUDGET=28`, `STD_CONVERGENCE_BUDGET=46`, `MAX_CONVERGENCE_BUDGET=61` (lines 31-33)
- **`reimburse_for_progress()`** helper (lines 42-58): uses `ledger.reimbursement_rate`, returns 0 when no progress, calls `ledger.credit()` only when credit > 0
- **`execute_fidelity_with_convergence()`** (lines 382-590): 3-run convergence loop with budget guards (`can_launch()`, `can_remediate()`), debit before checker runs, pass condition (0 active HIGHs), monotonic progress on structural only, semantic fluctuation logging, regression detection, CONVERGENCE_PASS_CREDIT on pass
- **Legacy/convergence dispatch**: `executor.py:418` checks `convergence_enabled` and routes to `_run_convergence_spec_fidelity()`; legacy path unchanged
- **`handle_regression()`** (lines 593-699): spawns 3 agents in isolated temp dirs, merges by stable ID, consolidated report, no ledger operations internally
- **`_create_validation_dirs()`** / **`_cleanup_validation_dirs()`** / **`_atexit_cleanup()`** (lines 331-379)
- **`_check_regression()`** (lines 296-328): structural-only regression detection (BF-3)
- **Pipeline executor wiring**: `_run_convergence_spec_fidelity()` in `executor.py:539-648` constructs `TurnLedger(initial_budget=STD_CONVERGENCE_BUDGET)` at line 572

### Phase 6: Remediation & Integration
**Tasks**: T06.01-T06.08 (8 tasks)
**Status**: PARTIAL

**Evidence of completion**:
- `remediate_executor.py` exists at `src/superclaude/cli/roadmap/remediate_executor.py`
- `_run_convergence_spec_fidelity()` wires structural checkers -> semantic layer -> convergence engine -> remediation (executor.py:539-648)
- Convergence result mapped to `StepResult` (executor.py:638-648)
- `_write_convergence_report()` produces spec-fidelity output (executor.py:651-691)
- `spec-fidelity` step gate set to `None` when `convergence_enabled` (executor.py:869)
- `_check_remediation_budget()` and `_print_terminal_halt()` exist in executor.py but are in the legacy path only

**Evidence of gaps** (partial):
- `fidelity.py` was NOT deleted -- `Glob` found no file, so this task is **COMPLETE** (deletion happened)
- The convergence wiring in `_run_convergence_spec_fidelity()` has a **call signature mismatch**: it calls `DeviationRegistry.load_or_create(path, ...)` with only 1 positional arg (executor.py:566) but the function signature requires 3 positional args: `(path, release_id, spec_hash)` (convergence.py:100). This is a **latent bug** that would crash at runtime.
- End-to-end verification (SC-1 through SC-6) was marked as pass in the execution log but no E2E test files were found confirming these criteria outside the sprint execution artifacts

---

## Present in Code (confirmed implemented)

| Deliverable | File:Line | FR |
|---|---|---|
| `spec_parser.py` with all extraction functions | `src/superclaude/cli/roadmap/spec_parser.py` | FR-2, FR-5 |
| `SpecSection` dataclass, `split_into_sections()` | `spec_parser.py` (imported by structural_checkers) | FR-5 |
| `DIMENSION_SECTION_MAP` | `spec_parser.py` | FR-5 |
| 5 structural checkers + `run_all_checkers()` | `structural_checkers.py:669` | FR-1 |
| `SEVERITY_RULES` (19 rules) + `get_severity()` | `structural_checkers.py:42-76` | FR-3 |
| `DeviationRegistry` with full FR-6 surface | `convergence.py:87-272` | FR-6 |
| `compute_stable_id()` | `convergence.py:61-69` | FR-6 |
| `RunMetadata` dataclass | `convergence.py:73-84` | FR-6, FR-10 |
| `source_layer` tracking, split HIGH counts | `convergence.py:188-199` | FR-6, BF-3 |
| `get_prior_findings_summary()` (max 50) | `convergence.py:226-239` | FR-10 |
| `first_seen_run` / `last_seen_run` tracking | `convergence.py` (multiple lines) | FR-10 |
| Pre-v3.05 backward compat defaults | `convergence.py:112-118` | FR-6, Risk #7 |
| `record_debate_verdict()` | `convergence.py:246-258` | FR-4.1 |
| `execute_fidelity_with_convergence()` | `convergence.py:382-590` | FR-7 |
| Budget guards: `can_launch()`, `can_remediate()` | `convergence.py:440,556` | FR-7 |
| `CHECKER_COST`, `REMEDIATION_COST`, etc. | `convergence.py:25-28` | FR-7 |
| `reimburse_for_progress()` | `convergence.py:42-58` | FR-7 |
| `CONVERGENCE_PASS_CREDIT` on early pass | `convergence.py:473` | FR-7, Risk #8 |
| Monotonic progress on structural only | `convergence.py:506` | FR-7, BF-3 |
| Semantic fluctuation logging | `convergence.py:493-503` | FR-7, BF-3 |
| `handle_regression()` | `convergence.py:593-699` | FR-8 |
| 3 parallel agents in temp dirs | `convergence.py:621-689` | FR-8 |
| try/finally + atexit cleanup | `convergence.py:698-699, 372-379` | FR-8, Risk #3 |
| `_check_regression()` structural-only | `convergence.py:296-328` | FR-8, BF-3 |
| `RegressionResult` dataclass | `convergence.py:287-293` | FR-7.1 |
| `ConvergenceResult` dataclass | `convergence.py:275-284` | FR-7 |
| Legacy/convergence dispatch | `executor.py:418` | NFR-7 |
| `_run_convergence_spec_fidelity()` wiring | `executor.py:539-648` | FR-7 |
| TurnLedger construction in convergence | `executor.py:572` | FR-7 |
| `_write_convergence_report()` | `executor.py:651-691` | FR-7 |
| Gate set to `None` in convergence mode | `executor.py:869` | FR-7, BF-2 |
| `MAX_PROMPT_BYTES = 30_720` | `semantic_layer.py:24` | FR-4.2, NFR-3 |
| Budget ratio constants | `semantic_layer.py:27-30` | FR-4.2 |
| `RubricScores`, rubric weights, verdict margin | `semantic_layer.py:40-56` | FR-4.1 |
| `run_semantic_layer()` entry point | `semantic_layer.py:377` | FR-4 |
| `fidelity.py` deleted | Not found by Glob | Phase 6 cleanup |

---

## Missing from Code (roadmap said to do, but not found)

### 1. `DeviationRegistry.load_or_create()` Call Signature Bug
**Expected**: 3 positional args `(path, release_id, spec_hash)` per convergence.py:100
**Actual**: Called with 1 arg in `executor.py:566`: `DeviationRegistry.load_or_create(config.output_dir / "deviation-registry.json")`
**Impact**: Runtime crash when convergence mode is activated. The executor wiring was never tested end-to-end.

### 2. `RemediationPatch` Dataclass
**Expected**: Defined in models.py per FR-9 (D-0009, D-0038)
**Found**: `RegressionResult` is defined in convergence.py. `RemediationPatch` definition was specified in Phase 1 (R-023) but its presence in `models.py` or `remediate_executor.py` is unconfirmed without reading remediate_executor.py fully. The roadmap spec required it.

### 3. `--allow-regeneration` Guard Logic in Remediation
**Expected**: Per-patch diff-size guard at 30%, `fallback_apply()`, `check_morphllm_available()` (FR-9, D-0038, D-0039, D-0048)
**Status**: `remediate_executor.py` exists but the v3.05 delta changes (per-patch 30% threshold replacing per-file 50%, `RemediationPatch` application, `fallback_apply()`, `check_morphllm_available()`) were not verified.

### 4. End-to-End Verification Artifacts
**Expected**: SC-1 through SC-6 verification evidence, NFR-1 through NFR-7 tests
**Found**: Execution log marks Phase 6 as pass (22m 27s) but no test files in the codebase confirming E2E success criteria were produced. The wiring-verification gate analyzed 0 files (wiring-verification.md: `files_analyzed: 0`).

### 5. Open Question Documentation
**Expected**: OQ-1 through OQ-5 documented with decisions (D-0046)
**Status**: Not verified in codebase artifacts.

---

## TurnLedger Wiring Gaps

### TurnLedger Constructed in `execute_sprint()`
- **Status**: NOT wired in `execute_sprint()`. The sprint executor (`sprint/executor.py:843`) does NOT construct a TurnLedger.
- **What exists**: TurnLedger is constructed in `execute_phase_tasks()` callers and `run_post_task_wiring_hook()` callers -- but `execute_sprint()` itself uses the old per-phase subprocess model (lines 843-942) and never instantiates a TurnLedger. The TurnLedger was introduced for the sprint per-task executor pattern (`execute_phase_tasks` at line 689), which is a separate code path.
- **v3.05 scope clarification**: The v3.05 spec explicitly says "TurnLedger is consumed from `sprint/models.py` without modification" and scope boundary says "Sprint-level budget wiring (execute_sprint, execute_phase_tasks)" is OUT OF SCOPE. This is not a v3.05 gap.

### `SprintGatePolicy` Being Instantiated in Production
- **Status**: `SprintGatePolicy` is defined at `sprint/executor.py:56` and is used within the sprint executor for task-level gate evaluation. It is NOT related to v3.05 scope.
- **v3.05 relevance**: None. v3.05 operates within the roadmap pipeline (step 8), not the sprint executor.

### `attempt_remediation()` Called from Sprint/Convergence Code
- **Status**: `attempt_remediation()` lives in `pipeline/trailing_gate.py:354` and is part of the wiring gate remediation flow (v3.0 trailing gate infrastructure). It is NOT called from the v3.05 convergence engine.
- **v3.05 relevance**: The convergence engine calls `run_remediation(registry)` which delegates to `remediate_executor.py:execute_remediation()`. This is a different remediation path. `attempt_remediation()` is for trailing gate / wiring gate failures, not fidelity convergence.

### `build_kpi_report()` Called at Sprint Completion
- **Status**: `build_kpi_report()` in `sprint/kpi.py:137` takes `DeferredRemediationLog` and `TurnLedger` as optional parameters. It is called from the sprint executor flow, not from roadmap/convergence.
- **v3.05 relevance**: Not in v3.05 scope. The KPI report integration with convergence budget data would be a future enhancement (budget_snapshot in RunMetadata was specified but may not flow to KPI).

### `DeferredRemediationLog` Wired into Sprint Flow
- **Status**: `DeferredRemediationLog` is in `pipeline/trailing_gate.py:489` and is part of the trailing gate infrastructure. It tracks wiring gate failures for deferred remediation.
- **v3.05 relevance**: Not in v3.05 scope. The convergence engine uses `DeviationRegistry` as its finding store, not `DeferredRemediationLog`.

---

## Root Cause Analysis

### Why are these gaps present?

1. **The `DeviationRegistry.load_or_create()` call signature bug**: The executor wiring in `_run_convergence_spec_fidelity()` was written with an incorrect number of arguments. This indicates the convergence integration path was never exercised end-to-end during v3.05 development. The execution log shows all 6 phases passed, but the sprint executor runs tasks via Claude subprocess -- the actual Python code path may not have been invoked during the sprint.

2. **TurnLedger not in `execute_sprint()`**: This was explicitly scoped out in the v3.05 spec. Section 1.2 states: "Sprint-level budget wiring (execute_sprint, execute_phase_tasks)" is OUT OF SCOPE. The v3.05 TurnLedger integration is specific to the roadmap convergence engine (step 8 of the roadmap pipeline), not the sprint executor.

3. **`SprintGatePolicy`, `attempt_remediation`, `build_kpi_report`, `DeferredRemediationLog`**: These are sprint/trailing-gate infrastructure from v3.0, not v3.05 deliverables. The v3.05 roadmap does not reference any of these. They belong to a different integration path (sprint per-task execution with wiring gates).

4. **E2E verification artifacts missing**: The sprint execution completed in 4h 14m with all phases passing, but the verification was done within the sprint subprocess context. No persistent test artifacts (pytest tests, scripts) were created to continuously verify SC-1 through SC-6.

5. **Wiring verification scanned 0 files**: The `wiring-verification.md` report shows `files_analyzed: 0`, `files_skipped: 0`. This suggests the wiring verification step targeted the wrong directory or the target directory was empty at scan time.

### Classification:

| Gap | Root Cause |
|---|---|
| `load_or_create()` signature mismatch | Task was present; code was written but not tested end-to-end |
| TurnLedger not in `execute_sprint()` | Correctly scoped out of v3.05 |
| Sprint infrastructure not wired | Not in v3.05 scope; belongs to v3.0/v3.1 sprint integration |
| E2E verification artifacts | Tasks marked complete but no persistent evidence |
| Wiring verification empty scan | Integration wiring issue (target directory wrong) |

---

## Recommendations

### Critical (must fix before convergence mode can be activated)

1. **Fix `DeviationRegistry.load_or_create()` call in executor.py:566**
   - Change from: `DeviationRegistry.load_or_create(config.output_dir / "deviation-registry.json")`
   - Change to: `DeviationRegistry.load_or_create(config.output_dir / "deviation-registry.json", release_id=config.output_dir.name, spec_hash=hashlib.sha256(config.spec_file.read_bytes()).hexdigest())`
   - This is a blocking runtime bug.

2. **Add integration test for `_run_convergence_spec_fidelity()` end-to-end path**
   - Test should exercise the full wiring: TurnLedger construction -> registry load -> checkers -> semantic -> convergence loop -> result mapping to StepResult
   - This was specified as T05.09 (D-0037: dual budget mutual exclusion) and T06.03 (D-0041: step 8 pipeline wiring) but no persistent test exists.

### Important (should fix for production readiness)

3. **Verify `remediate_executor.py` v3.05 changes**
   - Confirm `RemediationPatch` dataclass exists
   - Confirm per-patch 30% threshold (was 50% per-file)
   - Confirm `fallback_apply()` exists
   - Confirm `check_morphllm_available()` exists

4. **Fix wiring verification target directory**
   - The scan analyzed 0 files, which means the target directory was wrong or empty. This should point to the roadmap output directory containing the generated code.

5. **Use `MAX_CONVERGENCE_BUDGET` instead of `STD_CONVERGENCE_BUDGET` in executor.py:572**
   - The merged roadmap spec says: "Pipeline executor constructs `TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET)` when convergence enabled"
   - Current code uses `STD_CONVERGENCE_BUDGET` (46 turns) instead of `MAX_CONVERGENCE_BUDGET` (61 turns)
   - This limits the convergence engine to fewer runs than the spec intended

### Future (v3.1+ scope)

6. **Sprint-level TurnLedger integration**
   - Wire TurnLedger construction in `execute_sprint()` for per-phase budget tracking
   - Connect `build_kpi_report()` with convergence budget snapshots
   - Wire gate-pass reimbursement in the sprint loop (v3.1 scope per spec section 1.2)

7. **Budget snapshot in RunMetadata**
   - FR-10 specifies `budget_snapshot: dict | None = None` on RunMetadata
   - Current `RunMetadata` dataclass (convergence.py:73-84) does not include this field
   - Add for convergence diagnostics

8. **Persistent E2E verification tests**
   - Create pytest tests that verify SC-1 through SC-6 using real or fixture inputs
   - These should run as part of the normal test suite, not only during sprint execution
