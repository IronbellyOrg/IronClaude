# Requirement Universe — v3.3 TurnLedger Validation

**Extracted from**: `v3.3-requirements-spec.md`
**Extraction date**: 2026-03-23
**Total requirements**: 84

## Spec File Reference Status (Step 0.1.5)

| Referenced Path | Source | Status | Notes |
|----------------|--------|--------|-------|
| `src/superclaude/cli/sprint/executor.py` | FR-1.1–FR-1.18 | FOUND | — |
| `src/superclaude/cli/sprint/kpi.py` | FR-1.11 | FOUND | — |
| `src/superclaude/cli/sprint/models.py` | FR-1.19–FR-1.20 | FOUND | — |
| `src/superclaude/cli/roadmap/convergence.py` | FR-1.15–FR-1.18, FR-2.1 | FOUND | — |
| `src/superclaude/cli/audit/wiring_gate.py` | FR-1.21, FR-5.1 | FOUND | — |
| `src/superclaude/cli/audit/reachability.py` | FR-4.2, Roadmap 1B.2 | NOT FOUND | To be created by roadmap |
| `src/superclaude/cli/roadmap/fidelity_checker.py` | FR-5.2, Roadmap 3A.2 | NOT FOUND | To be created by roadmap |
| `tests/v3.3/` | Test File Layout | NOT FOUND | To be created by roadmap |
| `tests/audit-trail/` | Test File Layout | NOT FOUND | To be created by roadmap |
| `tests/roadmap/test_convergence_wiring.py` | FR-6.1 T07 | FOUND | — |
| `tests/roadmap/test_convergence_e2e.py` | FR-6.1 T11 | FOUND | — |
| `src/superclaude/cli/pipeline/models.py` | Roadmap: GateCriteria | FOUND | — |

**Note**: NOT FOUND paths reference files to be created. This table is informational.

---

## Requirement Registry

### Workstream 1: E2E Test Coverage (FR-1)

- id: REQ-001 | text: "Every wiring point from the brainstorm test matrix has at least one E2E test that exercises the real production code path." | source: spec:FR-1 (L74-77) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-002 | text: "Tests MUST NOT mock gate functions or core orchestration logic. _subprocess_factory injection point acceptable." | source: spec:FR-1 (L78) | type: CONSTRAINT | priority: P0 | domain: wiring-e2e | cross_cutting: true
- id: REQ-003 | text: "FR-1.1: TurnLedger Construction — ledger.initial_budget == config.max_turns * len(config.active_phases), reimbursement_rate == 0.8, constructed BEFORE phase loop" | source: spec:FR-1.1 (L80-87) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-004 | text: "FR-1.2: ShadowGateMetrics constructed before phase loop" | source: spec:FR-1.2 (L89-92) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-005 | text: "FR-1.3: DeferredRemediationLog constructed with persist_path under results_dir" | source: spec:FR-1.3 (L95-99) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-006 | text: "FR-1.4: SprintGatePolicy(config) constructed and receives correct config" | source: spec:FR-1.4 (L101-105) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-007 | text: "FR-1.5: Phase with ### T01.01 headings → execute_phase_tasks() called. Task results contain expected task IDs." | source: spec:FR-1.5 (L107-113) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-008 | text: "FR-1.6: Phase WITHOUT task headings → ClaudeProcess subprocess spawned" | source: spec:FR-1.6 (L115-119) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-009 | text: "FR-1.7: run_post_phase_wiring_hook() called for per-task phases AND per-phase/ClaudeProcess phases. Wiring logger emits expected entries." | source: spec:FR-1.7 (L121-127) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-010 | text: "FR-1.21: check_wiring_report() wrapper called within wiring analysis flow, delegates to underlying analysis, returns valid report" | source: spec:FR-1.21 (L129-135) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-011 | text: "FR-1.8: run_post_task_anti_instinct_hook() returns tuple[TaskResult, TrailingGateResult | None]" | source: spec:FR-1.8 (L137-141) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-012 | text: "FR-1.9: Sprint with N phases (mixed) → all_gate_results contains results from ALL phases" | source: spec:FR-1.9 (L143-147) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-013 | text: "FR-1.10: gate_rollout_mode='full', failing gate → TrailingGateResult appended to remediation_log" | source: spec:FR-1.10 (L149-153) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-014 | text: "FR-1.11: build_kpi_report() called with (all_gate_results, remediation_log, ledger). gate-kpi-report.md written. Includes wiring_analyses_run, wiring_remediations_attempted, wiring_net_cost." | source: spec:FR-1.11 (L155-162) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-015 | text: "FR-1.12: _resolve_wiring_mode() called within run_post_task_wiring_hook(), NOT config.wiring_gate_mode directly" | source: spec:FR-1.12 (L164-168) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-016 | text: "FR-1.13: shadow mode + findings → _log_shadow_findings_to_remediation_log() creates synthetic TrailingGateResult with [shadow] prefix" | source: spec:FR-1.13 (L170-174) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-017 | text: "FR-1.14: BLOCKING lifecycle: _format_wiring_failure() → debit(remediation_cost) → _recheck_wiring() → pass: restore+credit / fail: persist FAIL" | source: spec:FR-1.14 (L176-185) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-018 | text: "FR-1.15: DeviationRegistry.load_or_create() receives exactly 3 positional args: (path, release_id, spec_hash)" | source: spec:FR-1.15 (L187-191) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-019 | text: "FR-1.16: registry.merge_findings() receives (structural_list, semantic_list, run_number) — 3 args" | source: spec:FR-1.16 (L193-197) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-020 | text: "FR-1.17: _run_remediation() converts dicts to Finding objects without AttributeError" | source: spec:FR-1.17 (L199-203) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-021 | text: "FR-1.18: TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET) uses 61" | source: spec:FR-1.18 (L205-209) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-022 | text: "FR-1.19: SHADOW_GRACE_INFINITE defined in models.py; when set, shadow mode never exits grace period" | source: spec:FR-1.19 (L211-217) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e
- id: REQ-023 | text: "FR-1.20: __post_init__() derives sprint config fields correctly; invalid/missing → sensible defaults" | source: spec:FR-1.20 (L219-225) | type: FUNCTIONAL | priority: P0 | domain: wiring-e2e

### Workstream 2: TurnLedger Lifecycle (FR-2)

- id: REQ-024 | text: "Full debit/credit/reimbursement cycle for all 4 paths" | source: spec:FR-2 (L229-231) | type: FUNCTIONAL | priority: P0 | domain: turnledger-lifecycle
- id: REQ-025 | text: "FR-2.1: Convergence path — debit CHECKER_COST → run → credit CONVERGENCE_PASS_CREDIT → reimburse_for_progress(); budget_snapshot recorded" | source: spec:FR-2.1 (L233-239) | type: FUNCTIONAL | priority: P0 | domain: turnledger-lifecycle
- id: REQ-026 | text: "FR-2.1a: handle_regression() reachable from _run_convergence_spec_fidelity, called on regression, logs + adjusts budget" | source: spec:FR-2.1a (L241-246) | type: FUNCTIONAL | priority: P0 | domain: turnledger-lifecycle
- id: REQ-027 | text: "FR-2.2: Per-task path — pre-debit minimum_allocation → subprocess → reconcile; post-task hooks fire with ledger" | source: spec:FR-2.2 (L248-253) | type: FUNCTIONAL | priority: P0 | domain: turnledger-lifecycle
- id: REQ-028 | text: "FR-2.3: Per-phase path — debit_wiring() → analysis → credit_wiring() on non-blocking; wiring_analyses_count incremented" | source: spec:FR-2.3 (L255-259) | type: FUNCTIONAL | priority: P0 | domain: turnledger-lifecycle
- id: REQ-029 | text: "FR-2.4: Cross-path coherence — available() = initial_budget - consumed + reimbursed at every checkpoint" | source: spec:FR-2.4 (L261-265) | type: FUNCTIONAL | priority: P0 | domain: turnledger-lifecycle

### Workstream 3: Gate Rollout Modes (FR-3)

- id: REQ-030 | text: "Every gate rollout mode tested for both execution paths" | source: spec:FR-3 (L268-269) | type: FUNCTIONAL | priority: P0 | domain: gate-modes
- id: REQ-031 | text: "FR-3.1a: Mode 'off' — AI: evaluate+ignore; wiring: skip" | source: spec:FR-3.1 (L276) | type: FUNCTIONAL | priority: P0 | domain: gate-modes
- id: REQ-032 | text: "FR-3.1b: Mode 'shadow' — AI: evaluate+record; wiring: analyze+log+credit back" | source: spec:FR-3.1 (L277) | type: FUNCTIONAL | priority: P0 | domain: gate-modes
- id: REQ-033 | text: "FR-3.1c: Mode 'soft' — AI: evaluate+record+credit/remediate; wiring: analyze+warn+credit back" | source: spec:FR-3.1 (L278) | type: FUNCTIONAL | priority: P0 | domain: gate-modes
- id: REQ-034 | text: "FR-3.1d: Mode 'full' — AI: evaluate+record+credit/remediate+FAIL; wiring: analyze+block+remediate" | source: spec:FR-3.1 (L279) | type: FUNCTIONAL | priority: P0 | domain: gate-modes
- id: REQ-035 | text: "Each mode test verifies: TaskStatus/GateOutcome, TurnLedger state, DeferredRemediationLog, ShadowGateMetrics" | source: spec:FR-3.1 (L281-286) | type: ACCEPTANCE_CRITERION | priority: P0 | domain: gate-modes | cross_cutting: true
- id: REQ-036 | text: "FR-3.2a: Budget exhausted before task launch → SKIPPED, remaining listed" | source: spec:FR-3.2 (L291) | type: FUNCTIONAL | priority: P0 | domain: gate-modes
- id: REQ-037 | text: "FR-3.2b: Budget exhausted before wiring → hook skipped, status unchanged" | source: spec:FR-3.2 (L292) | type: FUNCTIONAL | priority: P0 | domain: gate-modes
- id: REQ-038 | text: "FR-3.2c: Budget exhausted before remediation → FAIL persists, BUDGET_EXHAUSTED logged" | source: spec:FR-3.2 (L293) | type: FUNCTIONAL | priority: P0 | domain: gate-modes
- id: REQ-039 | text: "FR-3.2d: Budget exhausted mid-convergence → halt with diagnostic, run_count < max_runs" | source: spec:FR-3.2 (L294) | type: FUNCTIONAL | priority: P0 | domain: gate-modes
- id: REQ-040 | text: "FR-3.3: Interrupted sprint — KPI report written, remediation log persisted, outcome=INTERRUPTED" | source: spec:FR-3.3 (L296-302) | type: FUNCTIONAL | priority: P1 | domain: gate-modes

### Workstream 4: Reachability (FR-4)

- id: REQ-041 | text: "FR-4.1: Wiring manifest YAML with entry_points + required_reachable sections" | source: spec:FR-4.1 (L309-357) | type: FUNCTIONAL | priority: P0 | domain: reachability
- id: REQ-042 | text: "FR-4.2: AST call-chain analyzer — ast.parse(), call graph, BFS/DFS, cross-module imports" | source: spec:FR-4.2 (L359-368) | type: FUNCTIONAL | priority: P0 | domain: reachability
- id: REQ-043 | text: "FR-4.2 limitations documented: dynamic dispatch false negatives, TYPE_CHECKING excluded, lazy imports included" | source: spec:FR-4.2 (L370-373) | type: CONSTRAINT | priority: P1 | domain: reachability
- id: REQ-044 | text: "FR-4.3: Reachability gate — reads manifest, AST analysis, PASS/FAIL, integrates GateCriteria" | source: spec:FR-4.3 (L375-383) | type: FUNCTIONAL | priority: P0 | domain: reachability
- id: REQ-045 | text: "FR-4.4: Regression test — remove run_post_phase_wiring_hook() → gate detects, references v3.2-T02" | source: spec:FR-4.4 (L385-388) | type: TEST | priority: P0 | domain: reachability
- id: REQ-046 | text: "Wiring manifest has 13 entries covering v3.1/v3.2/v3.05 including handle_regression" | source: spec:Wiring Manifest (L563-621) | type: DATA_MODEL | priority: P0 | domain: reachability

### Workstream 5: Pipeline Fixes (FR-5)

- id: REQ-047 | text: "FR-5.1: files_analyzed==0 AND non-empty dir → FAIL with failure_reason" | source: spec:FR-5.1 (L393-401) | type: FUNCTIONAL | priority: P0 | domain: pipeline-fixes
- id: REQ-048 | text: "FR-5.1 test: non-empty dir, 0 analyzed → assert FAIL" | source: spec:FR-5.1 (L401) | type: TEST | priority: P0 | domain: pipeline-fixes
- id: REQ-049 | text: "FR-5.2: Impl-vs-spec fidelity checker — reads FRs, searches codebase, reports gaps" | source: spec:FR-5.2 (L403-414) | type: FUNCTIONAL | priority: P0 | domain: pipeline-fixes
- id: REQ-050 | text: "FR-5.2 integration: additional checker in _run_checkers()" | source: spec:FR-5.2 (L412) | type: INTEGRATION | priority: P0 | domain: pipeline-fixes
- id: REQ-051 | text: "FR-5.2 test: spec FR → checker finds function; remove → checker flags gap" | source: spec:FR-5.2 (L414) | type: TEST | priority: P0 | domain: pipeline-fixes
- id: REQ-052 | text: "FR-5.3 = FR-4 (cross-reference)" | source: spec:FR-5.3 (L416-418) | type: DEPENDENCY | priority: P0 | domain: pipeline-fixes | related_reqs: [REQ-041..044]

### Workstream 6: QA Gaps (FR-6)

- id: REQ-053 | text: "T07: test_convergence_wiring.py — 7 tests" | source: spec:FR-6.1 (L428) | type: TEST | priority: P0 | domain: qa-gaps
- id: REQ-054 | text: "T11: test_convergence_e2e.py — 6 tests for SC-1 through SC-6" | source: spec:FR-6.1 (L429) | type: TEST | priority: P0 | domain: qa-gaps
- id: REQ-055 | text: "T12: Smoke test convergence path" | source: spec:FR-6.1 (L430) | type: TEST | priority: P0 | domain: qa-gaps
- id: REQ-056 | text: "T14: Regenerate wiring-verification artifact + validate" | source: spec:FR-6.1 (L431) | type: PROCESS | priority: P1 | domain: qa-gaps
- id: REQ-057 | text: "T02: Confirming test for run_post_phase_wiring_hook()" | source: spec:FR-6.2 (L439) | type: TEST | priority: P0 | domain: qa-gaps
- id: REQ-058 | text: "T17-T22: Integration tests, regression suite, gap closure audit" | source: spec:FR-6.2 (L440) | type: TEST | priority: P0 | domain: qa-gaps

### Workstream 7: Audit Trail (FR-7)

- id: REQ-059 | text: "FR-7.1: JSONL audit record with 9 fields" | source: spec:FR-7.1 (L448-474) | type: FUNCTIONAL | priority: P0 | domain: audit-trail
- id: REQ-060 | text: "FR-7.2: Third-party verifiability — 4 properties" | source: spec:FR-7.2 (L477-484) | type: NON_FUNCTIONAL | priority: P0 | domain: audit-trail
- id: REQ-061 | text: "FR-7.3: audit_trail pytest fixture with record(), auto-flush, session summary" | source: spec:FR-7.3 (L486-493) | type: FUNCTIONAL | priority: P0 | domain: audit-trail

### Success Criteria

- id: REQ-062 | text: "SC-1: ≥20 wiring point E2E tests mapped to FR-1" | source: spec:SC-1 (L548) | type: SUCCESS_CRITERION | priority: P0 | domain: wiring-e2e
- id: REQ-063 | text: "SC-2: TurnLedger 4/4 paths" | source: spec:SC-2 (L549) | type: SUCCESS_CRITERION | priority: P0 | domain: turnledger-lifecycle
- id: REQ-064 | text: "SC-3: 8+ gate mode scenarios" | source: spec:SC-3 (L550) | type: SUCCESS_CRITERION | priority: P0 | domain: gate-modes
- id: REQ-065 | text: "SC-4: ≥4894 passed, ≤3 pre-existing, 0 regressions" | source: spec:SC-4 (L551) | type: SUCCESS_CRITERION | priority: P0 | domain: qa-gaps | cross_cutting: true
- id: REQ-066 | text: "SC-5: KPI field VALUES match expectations" | source: spec:SC-5 (L552) | type: SUCCESS_CRITERION | priority: P0 | domain: wiring-e2e
- id: REQ-067 | text: "SC-6: 4 budget exhaustion scenarios" | source: spec:SC-6 (L553) | type: SUCCESS_CRITERION | priority: P0 | domain: gate-modes
- id: REQ-068 | text: "SC-7: Break wiring → detected" | source: spec:SC-7 (L554) | type: SUCCESS_CRITERION | priority: P0 | domain: reachability
- id: REQ-069 | text: "SC-8: QA gaps closed" | source: spec:SC-8 (L555) | type: SUCCESS_CRITERION | priority: P0 | domain: qa-gaps
- id: REQ-070 | text: "SC-9: Reachability detects broken wiring" | source: spec:SC-9 (L556) | type: SUCCESS_CRITERION | priority: P0 | domain: reachability
- id: REQ-071 | text: "SC-10: 0-files → FAIL" | source: spec:SC-10 (L557) | type: SUCCESS_CRITERION | priority: P0 | domain: pipeline-fixes
- id: REQ-072 | text: "SC-11: Fidelity checker exists and works" | source: spec:SC-11 (L558) | type: SUCCESS_CRITERION | priority: P0 | domain: pipeline-fixes
- id: REQ-073 | text: "SC-12: Audit trail verifiable" | source: spec:SC-12 (L559) | type: SUCCESS_CRITERION | priority: P0 | domain: audit-trail

### Constraints

- id: REQ-074 | text: "UV only" | source: spec:Constraints (L648) | type: CONSTRAINT | priority: P0 | cross_cutting: true
- id: REQ-075 | text: "No mocks on gate functions" | source: spec:Constraints (L649) | type: CONSTRAINT | priority: P0 | cross_cutting: true
- id: REQ-076 | text: "Branch from v3.0-v3.2-Fidelity" | source: spec:Constraints (L650) | type: CONSTRAINT | priority: P0
- id: REQ-077 | text: "Baseline: 4894 passed, 3 pre-existing" | source: spec:Constraints (L651) | type: CONSTRAINT | priority: P0 | cross_cutting: true
- id: REQ-078 | text: "Every test emits JSONL audit record" | source: spec:Constraints (L652) | type: CONSTRAINT | priority: P0 | cross_cutting: true
- id: REQ-079 | text: "Manifest is source of truth for reachability" | source: spec:Constraints (L653) | type: CONSTRAINT | priority: P0

### Sequencing

- id: REQ-080 | text: "Phase 1 no dependencies, produces audit trail + AST analyzer" | source: spec:Phased Plan (L498-504) | type: SEQUENCING | priority: P1 | cross_cutting: true
- id: REQ-081 | text: "Phase 2 depends on Phase 1 (audit trail)" | source: spec:Phased Plan (L506-512) | type: SEQUENCING | priority: P1
- id: REQ-082 | text: "Phase 3 depends on Phase 1 (AST) + Phase 2 (baseline)" | source: spec:Phased Plan (L514-519) | type: SEQUENCING | priority: P1
- id: REQ-083 | text: "Phase 4 depends on Phases 1-3" | source: spec:Phased Plan (L522-528) | type: SEQUENCING | priority: P1

### Risk Mitigations

- id: REQ-084 | text: "AST analyzer handles lazy imports; test against executor.py" | source: spec:Risk (L536) | type: RISK_MITIGATION | priority: P1
- id: REQ-085 | text: "E2E tests use _subprocess_factory; no real subprocesses" | source: spec:Risk (L537) | type: RISK_MITIGATION | priority: P1
- id: REQ-086 | text: "Fidelity checker: exact name matching, not NLP" | source: spec:Risk (L538) | type: RISK_MITIGATION | priority: P1
- id: REQ-087 | text: "Audit JSONL one file per run, timestamped" | source: spec:Risk (L539) | type: RISK_MITIGATION | priority: P2
- id: REQ-088 | text: "Investigate 3 pre-existing failures before FR-5.1 patch" | source: spec:Risk (L540) | type: RISK_MITIGATION | priority: P1

### Test Layout

- id: REQ-089 | text: "Test file layout as specified in spec" | source: spec:Test File Layout (L626-642) | type: CONSTRAINT | priority: P1

---

## Summary

| Category | Count |
|----------|-------|
| FUNCTIONAL | 41 |
| TEST | 8 |
| CONSTRAINT | 8 |
| SUCCESS_CRITERION | 12 |
| NON_FUNCTIONAL | 1 |
| INTEGRATION | 1 |
| SEQUENCING | 4 |
| RISK_MITIGATION | 5 |
| DEPENDENCY | 1 |
| DATA_MODEL | 1 |
| PROCESS | 1 |
| ACCEPTANCE_CRITERION | 1 |
| **TOTAL** | **84** |
