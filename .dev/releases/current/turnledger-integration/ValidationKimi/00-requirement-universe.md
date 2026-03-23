# Requirement Universe: v3.3 TurnLedger Validation

**Source**: v3.3-requirements-spec.md
**Extracted**: 2026-03-23
**Total Requirements**: 54

---

## File Reference Status (Step 0.1.5)

| Referenced Path | Source | Status | Notes |
|----------------|--------|--------|-------|
| `src/superclaude/cli/sprint/executor.py` | spec.md:L19-44 | NOT_FOUND | Target codebase location |
| `src/superclaude/cli/sprint/kpi.py` | spec.md:L162 | NOT_FOUND | Target codebase location |
| `src/superclaude/cli/roadmap/convergence.py` | spec.md:L40 | NOT_FOUND | Target codebase location |
| `src/superclaude/cli/audit/wiring_gate.py` | spec.md:L397 | NOT_FOUND | Target codebase location |
| `src/superclaude/cli/roadmap/executor.py` | spec.md:L573 | NOT_FOUND | Target codebase location |
| `src/superclaude/cli/roadmap/fidelity_checker.py` | spec.md:L412 | NOT_FOUND | New file to be created |
| `src/superclaude/cli/audit/reachability.py` | spec.md:L359 | NOT_FOUND | New file to be created |
| `tests/v3.3/` | spec.md:L627 | NOT_FOUND | New test directory |
| `tests/audit-trail/audit_writer.py` | spec.md:L47 | NOT_FOUND | New file to be created |
| `tests/roadmap/` | spec.md:L637 | NOT_FOUND | Target test directory |

**Note**: NOT FOUND paths primarily reference target codebase files and new files to be created. This is expected for a validation-focused release.

---

## Functional Requirements (FR-*)

### FR-1: E2E Test Coverage for Wiring Points

| ID | Requirement Text | Source | Priority | Type | Cross-Cutting |
|----|-----------------|--------|----------|------|---------------|
| REQ-001 | TurnLedger Construction Validation: Invoke `execute_sprint()` with minimal config. Assert ledger.initial_budget == config.max_turns * len(config.active_phases), reimbursement_rate == 0.8, constructed BEFORE phase loop | spec.md:L80-87 | P0 | FUNCTIONAL | false |
| REQ-002 | ShadowGateMetrics Construction: Assert `ShadowGateMetrics()` constructed before phase loop | spec.md:L89-93 | P0 | FUNCTIONAL | false |
| REQ-003 | DeferredRemediationLog Construction: Assert constructed with persist_path under results_dir | spec.md:L95-100 | P0 | FUNCTIONAL | false |
| REQ-004 | SprintGatePolicy Construction: Assert `SprintGatePolicy(config)` constructed with correct config | spec.md:L101-106 | P0 | FUNCTIONAL | false |
| REQ-005 | Phase Delegation - Task Inventory Path: Create phase with `### T01.01` headings, assert `execute_phase_tasks()` called not ClaudeProcess | spec.md:L107-114 | P0 | FUNCTIONAL | false |
| REQ-006 | Phase Delegation - Freeform Fallback Path: Create phase WITHOUT task headings, assert ClaudeProcess subprocess spawned | spec.md:L115-120 | P0 | FUNCTIONAL | false |
| REQ-007 | Post-Phase Wiring Hook - Both Paths: Verify called for per-task phases (executor.py:1199-1204) and per-phase/ClaudeProcess phases (executor.py:1407-1412) | spec.md:L121-128 | P0 | FUNCTIONAL | true |
| REQ-007a | check_wiring_report() Wrapper Call: Assert called within wiring analysis flow, delegates and returns valid report | spec.md:L129-136 | P0 | FUNCTIONAL | false |
| REQ-008 | Anti-Instinct Hook Return Type: Assert returns `tuple[TaskResult, TrailingGateResult \| None]`, not bare TaskResult | spec.md:L137-142 | P0 | FUNCTIONAL | false |
| REQ-009 | Gate Result Accumulation: Run sprint with N phases (mix), assert all_gate_results contains results from ALL phases | spec.md:L143-148 | P0 | FUNCTIONAL | false |
| REQ-010 | Failed Gate → Remediation Log: Configure gate_rollout_mode="full", inject failing gate, assert failed TrailingGateResult appended to remediation_log | spec.md:L149-154 | P0 | FUNCTIONAL | false |
| REQ-011 | KPI Report Generation: Assert build_kpi_report() called with all_gate_results, remediation_log, ledger; report written to results_dir with wiring KPI fields | spec.md:L155-163 | P0 | FUNCTIONAL | true |
| REQ-012 | Wiring Mode Resolution: Assert `_resolve_wiring_mode()` called within run_post_task_wiring_hook(), NOT config.wiring_gate_mode used directly | spec.md:L164-169 | P0 | FUNCTIONAL | false |
| REQ-013 | Shadow Findings → Remediation Log: Configure wiring_gate_mode="shadow", inject findings, assert synthetic TrailingGateResult entries with [shadow] prefix | spec.md:L170-175 | P0 | FUNCTIONAL | false |
| REQ-014 | BLOCKING Remediation Lifecycle: Configure gate_rollout_mode="full", inject blocking findings, assert full cycle: _format_wiring_failure(), ledger.debit(), _recheck_wiring(), restore/credit on pass, FAIL on fail | spec.md:L176-186 | P0 | FUNCTIONAL | true |
| REQ-015 | Convergence Registry Args: Assert DeviationRegistry.load_or_create() receives exactly 3 positional args: (path, release_id, spec_hash) | spec.md:L187-192 | P0 | FUNCTIONAL | false |
| REQ-016 | Convergence Merge Args: Assert registry.merge_findings() receives (structural_list, semantic_list, run_number) — 3 args, correct positions | spec.md:L193-198 | P0 | FUNCTIONAL | false |
| REQ-017 | Convergence Remediation Dict→Finding: Assert _run_remediation() converts registry dicts to Finding objects without AttributeError | spec.md:L199-204 | P0 | FUNCTIONAL | false |
| REQ-018 | Budget Constants: Assert `TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET)` uses 61 (not 46) | spec.md:L205-210 | P0 | FUNCTIONAL | false |
| REQ-019 | SHADOW_GRACE_INFINITE Constant: Assert defined with sentinel value, when wiring_gate_grace_period set to it, shadow mode never exits grace period | spec.md:L211-218 | P0 | FUNCTIONAL | false |
| REQ-020 | Post-Init Config Derivation: Assert __post_init__() correctly derives sprint config fields from input config | spec.md:L219-226 | P0 | FUNCTIONAL | false |

**Sub-total FR-1**: 21 requirements (REQ-001 through REQ-020)

### FR-2: TurnLedger Lifecycle Integration Tests

| ID | Requirement Text | Source | Priority | Type | Cross-Cutting |
|----|-----------------|--------|----------|------|---------------|
| REQ-021 | Convergence Path (v3.05): Exercise execute_fidelity_with_convergence() E2E, assert debit CHECKER_COST → run checkers → credit CONVERGENCE_PASS_CREDIT → reimburse_for_progress(), budget_snapshot recorded | spec.md:L233-240 | P0 | FUNCTIONAL | true |
| REQ-021a | Regression Handler Reachability: Assert handle_regression() reachable and called on regression detection | spec.md:L240-246 | P0 | FUNCTIONAL | false |
| REQ-022 | Sprint Per-Task Path (v3.1): Exercise execute_sprint() → execute_phase_tasks(), assert pre-debit minimum_allocation → subprocess → reconcile, post-task hooks fire with ledger | spec.md:L248-254 | P0 | FUNCTIONAL | true |
| REQ-023 | Sprint Per-Phase Path (v3.2): Exercise execute_sprint() → ClaudeProcess fallback → run_post_phase_wiring_hook(), assert debit_wiring() → analysis → credit_wiring(), wiring_analyses_count incremented | spec.md:L255-260 | P0 | FUNCTIONAL | true |
| REQ-024 | Cross-Path Coherence: Sprint with mixed phases, assert ledger state coherent after both paths, available() = initial_budget - consumed + reimbursed at every checkpoint | spec.md:L261-266 | P0 | FUNCTIONAL | true |

**Sub-total FR-2**: 5 requirements (REQ-021 through REQ-024, plus REQ-021a)

### FR-3: Gate Rollout Mode Scenarios

| ID | Requirement Text | Source | Priority | Type | Cross-Cutting |
|----|-----------------|--------|----------|------|---------------|
| REQ-025 | Mode Matrix - off: Anti-instinct evaluate+ignore, wiring skip analysis | spec.md:L274-276 | P0 | FUNCTIONAL | false |
| REQ-026 | Mode Matrix - shadow: Anti-instinct evaluate+record metrics, wiring analyze+log+credit back | spec.md:L277 | P0 | FUNCTIONAL | false |
| REQ-027 | Mode Matrix - soft: Anti-instinct evaluate+record+credit/remediate, wiring analyze+warn critical+credit back | spec.md:L278 | P0 | FUNCTIONAL | false |
| REQ-028 | Mode Matrix - full: Anti-instinct evaluate+record+credit/remediate+FAIL, wiring analyze+block critical+major+remediate | spec.md:L279 | P0 | FUNCTIONAL | false |
| REQ-029 | Each mode verification: Correct TaskStatus/GateOutcome, TurnLedger state, DeferredRemediationLog entries, ShadowGateMetrics recording | spec.md:L281-286 | P0 | ACCEPTANCE_CRITERION | false |
| REQ-030 | Budget Exhaustion - before task launch: Task marked SKIPPED, remaining tasks listed | spec.md:L291 | P0 | FUNCTIONAL | false |
| REQ-031 | Budget Exhaustion - before wiring analysis: Wiring hook skipped, task status unchanged | spec.md:L292 | P0 | FUNCTIONAL | false |
| REQ-032 | Budget Exhaustion - before remediation: FAIL status persists, BUDGET_EXHAUSTED logged | spec.md:L293 | P0 | FUNCTIONAL | false |
| REQ-033 | Budget Exhaustion - mid-convergence: Halt with diagnostic, run_count < max_runs | spec.md:L294 | P0 | FUNCTIONAL | false |
| REQ-034 | Interrupted Sprint: Simulate signal interrupt, assert KPI report written, remediation log persisted, outcome = INTERRUPTED | spec.md:L296-302 | P0 | FUNCTIONAL | false |

**Sub-total FR-3**: 10 requirements (REQ-025 through REQ-034)

### FR-4: Reachability Eval Framework

| ID | Requirement Text | Source | Priority | Type | Cross-Cutting |
|----|-----------------|--------|----------|------|---------------|
| REQ-035 | Spec-Driven Wiring Manifest: Release spec declares wiring_manifest section with entry_points and required_reachable | spec.md:L309-358 | P0 | CONFIG | true |
| REQ-036 | AST Call-Chain Analyzer: Parse entry point module, build call graph, resolve imports, BFS/DFS reachability, report targets NOT in reachable set | spec.md:L359-375 | P0 | FUNCTIONAL | true |
| REQ-037 | Reachability Gate Integration: Runs as pipeline gate, reads manifest, runs AST analysis, produces PASS/FAIL report, integrates with GateCriteria | spec.md:L376-384 | P0 | FUNCTIONAL | true |
| REQ-038 | Regression Test: Intentionally remove call to run_post_phase_wiring_hook(), assert gate detects gap referencing v3.2-T02 | spec.md:L385-389 | P0 | TEST | false |

**Sub-total FR-4**: 4 requirements (REQ-035 through REQ-038)

### FR-5: Pipeline Fixes

| ID | Requirement Text | Source | Priority | Type | Cross-Cutting |
|----|-----------------|--------|----------|------|---------------|
| REQ-039 | 0-Files-Analyzed Assertion: If files_analyzed == 0 AND source dir non-empty, return FAIL with failure_reason | spec.md:L393-401 | P0 | FUNCTIONAL | false |
| REQ-040 | Impl-vs-Spec Fidelity Check: Reads spec FRs, searches codebase for evidence, reports FRs with no implementation evidence as gaps | spec.md:L403-415 | P0 | FUNCTIONAL | true |
| REQ-041 | Reachability Gate (Weakness #2): This IS FR-4, cross-referenced for traceability | spec.md:L416-419 | P0 | FUNCTIONAL | true |

**Sub-total FR-5**: 3 requirements (REQ-039 through REQ-041)

### FR-6: Remaining QA Gaps

| ID | Requirement Text | Source | Priority | Type | Cross-Cutting |
|----|-----------------|--------|----------|------|---------------|
| REQ-042 | v3.05 Gap T07: tests/roadmap/test_convergence_wiring.py — 7 tests | spec.md:L426-429 | P1 | TEST | false |
| REQ-043 | v3.05 Gap T11: tests/roadmap/test_convergence_e2e.py — 6 tests for SC-1 through SC-6 | spec.md:L429 | P1 | TEST | false |
| REQ-044 | v3.05 Gap T12: Smoke test convergence path | spec.md:L430 | P1 | TEST | false |
| REQ-045 | v3.05 Gap T14: Regenerate wiring-verification artifact | spec.md:L431 | P1 | PROCESS | false |
| REQ-046 | v3.2 Gap T02: run_post_phase_wiring_hook() call — already WIRED, write confirming test | spec.md:L438-440 | P1 | TEST | false |
| REQ-047 | v3.2 Gap T17-T22: Integration tests, regression suite, gap closure audit | spec.md:L440 | P1 | TEST | false |

**Sub-total FR-6**: 6 requirements (REQ-042 through REQ-047)

### FR-7: Audit Trail Infrastructure

| ID | Requirement Text | Source | Priority | Type | Cross-Cutting |
|----|-----------------|--------|----------|------|---------------|
| REQ-048 | Test Output Format: Each test writes JSONL audit record with 9 fields: test_id, spec_ref, timestamp, assertion_type, inputs, observed, expected, verdict, evidence | spec.md:L448-476 | P0 | DATA_MODEL | true |
| REQ-049 | Audit Trail Properties: Third party MUST determine from trail alone: real tests run, run according to spec, results real, pass/fail sound | spec.md:L478-484 | P0 | NON_FUNCTIONAL | true |
| REQ-050 | Audit Trail Runner: pytest fixture opens JSONL, provides record() method with auto-computed duration_ms, auto-flushes, produces summary report | spec.md:L485-494 | P0 | FUNCTIONAL | true |

**Sub-total FR-7**: 3 requirements (REQ-048 through REQ-050)

---

## Success Criteria (SC-*)

| ID | Requirement Text | Source | Priority | Type | Cross-Cutting |
|----|-----------------|--------|----------|------|---------------|
| REQ-SC-001 | SC-1: ≥20 wiring point E2E tests, count tests mapped to FR-1 sub-IDs | spec.md:L548 | P0 | SUCCESS_CRITERION | false |
| REQ-SC-002 | SC-2: TurnLedger lifecycle covered for all 4 paths | spec.md:L549 | P0 | SUCCESS_CRITERION | false |
| REQ-SC-003 | SC-3: Gate rollout modes covered (off/shadow/soft/full), 4 modes × 2 paths = 8+ scenarios | spec.md:L550 | P0 | SUCCESS_CRITERION | false |
| REQ-SC-004 | SC-4: Zero regressions from baseline, ≥4894 passed, ≤3 pre-existing failures | spec.md:L551 | P0 | SUCCESS_CRITERION | false |
| REQ-SC-005 | SC-5: KPI report accuracy validated, field VALUES correct not just present | spec.md:L552 | P0 | SUCCESS_CRITERION | false |
| REQ-SC-006 | SC-6: Budget exhaustion paths validated, 4 scenarios tested | spec.md:L553 | P0 | SUCCESS_CRITERION | false |
| REQ-SC-007 | SC-7: Eval framework catches known-bad state, break wiring → detected | spec.md:L554 | P0 | SUCCESS_CRITERION | false |
| REQ-SC-008 | SC-8: Remaining QA gaps closed, T07/T11/T12/T14, T02/T17-T22 | spec.md:L555 | P0 | SUCCESS_CRITERION | false |
| REQ-SC-009 | SC-9: Reachability gate catches unreachable code | spec.md:L556 | P0 | SUCCESS_CRITERION | false |
| REQ-SC-010 | SC-10: 0-files-analyzed produces FAIL, assertion added and tested | spec.md:L557 | P0 | SUCCESS_CRITERION | false |
| REQ-SC-011 | SC-11: Impl-vs-spec fidelity check exists, finds and flags missing implementations | spec.md:L558 | P0 | SUCCESS_CRITERION | false |
| REQ-SC-012 | SC-12: Audit trail third-party verifiable, JSONL with all 4 verification properties | spec.md:L559 | P0 | SUCCESS_CRITERION | false |

**Sub-total SC**: 12 requirements (REQ-SC-001 through REQ-SC-012)

---

## Summary Statistics

| Category | Count |
|----------|-------|
| Functional Requirements (FR-*) | 42 |
| Success Criteria (SC-*) | 12 |
| **Total Requirements** | **54** |

| Priority | Count |
|----------|-------|
| P0 (Critical/Must) | 48 |
| P1 (Important/Should) | 6 |

| Cross-Cutting | Count |
|-------------|-------|
| true | 15 |
| false | 39 |
