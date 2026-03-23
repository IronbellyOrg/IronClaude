# Requirement Universe
**Roadmap**: v3.3-TurnLedger-Validation/roadmap.md
**Spec**: v3.3-requirements-spec.md
**Extraction date**: 2026-03-23
**Depth**: standard

---

## Spec File Reference Status (Step 0.1.5)

| Referenced Path | Source | Status | Notes |
|----------------|--------|--------|-------|
| `src/superclaude/cli/sprint/executor.py` | spec:L19-44 | FOUND | Canonical sprint executor |
| `src/superclaude/cli/sprint/models.py` | spec:L35,37 | FOUND | Sprint models |
| `src/superclaude/cli/roadmap/convergence.py` | spec:L40-41 | FOUND | Roadmap convergence module |
| `src/superclaude/cli/audit/wiring_gate.py` | spec:L45 | FOUND | Wiring gate |
| `src/superclaude/cli/sprint/kpi.py` | spec:L28 | FOUND | KPI module |
| `src/superclaude/cli/roadmap/executor.py` | spec:L319 | FOUND | Roadmap executor |
| `src/superclaude/cli/audit/reachability.py` | roadmap:1B.2 | NOT FOUND | New file to be created in Phase 1B |
| `src/superclaude/cli/roadmap/fidelity_checker.py` | roadmap:3A.2 | NOT FOUND | New file to be created in Phase 3 |
| `tests/v3.3/conftest.py` | roadmap:1A | NOT FOUND | New directory/file to be created |
| `tests/v3.3/test_wiring_points_e2e.py` | roadmap:2A | NOT FOUND | New file to be created |
| `tests/v3.3/test_turnledger_lifecycle.py` | roadmap:2B | NOT FOUND | New file to be created |
| `tests/v3.3/test_gate_rollout_modes.py` | roadmap:2C | NOT FOUND | New file to be created |
| `tests/v3.3/test_integration_regression.py` | roadmap:2D | NOT FOUND | New file to be created |
| `tests/v3.3/wiring_manifest.yaml` | roadmap:1B.4 | NOT FOUND | New file to be created |
| `tests/roadmap/test_convergence_wiring.py` | spec:FR-6.1 | NOT FOUND | To be created (FR-6.1 T07) |
| `tests/roadmap/test_convergence_e2e.py` | spec:FR-6.1 | NOT FOUND | To be created (FR-6.1 T11) |
| `tests/audit-trail/audit_trail.py` | spec:FR-7 | NOT FOUND | New module to be created |

**Note**: NOT FOUND paths for test files and new source modules are expected — they represent deliverables. Core production files are all FOUND. NOT FOUND status does not change coverage scoring.

---

## Requirement Registry

### FR-1: E2E Test Coverage for Wiring Points

```yaml
- id: "REQ-001"
  text: "Every wiring point from the brainstorm test matrix has at least one E2E test that exercises the real production code path"
  source: "v3.3-requirements-spec.md:FR-1 (goal)"
  type: FUNCTIONAL
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-002"
  text: "Tests MUST NOT mock gate functions or core orchestration logic; _subprocess_factory injection is the only acceptable injection point"
  source: "v3.3-requirements-spec.md:FR-1 (constraint)"
  type: CONSTRAINT
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: true

- id: "REQ-003"
  text: "FR-1.1: Invoke execute_sprint() with a minimal config and assert: ledger.initial_budget == config.max_turns * len(config.active_phases); ledger.reimbursement_rate == 0.8; Ledger is constructed BEFORE the phase loop begins"
  source: "v3.3-requirements-spec.md:FR-1.1"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false
  related_reqs: ["REQ-SC1"]

- id: "REQ-004"
  text: "FR-1.2: Assert ShadowGateMetrics() is constructed before phase loop"
  source: "v3.3-requirements-spec.md:FR-1.2"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-005"
  text: "FR-1.3: Assert DeferredRemediationLog is constructed with persist_path under results_dir"
  source: "v3.3-requirements-spec.md:FR-1.3"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-006"
  text: "FR-1.4: Assert SprintGatePolicy(config) is constructed and receives the correct config"
  source: "v3.3-requirements-spec.md:FR-1.4"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-007"
  text: "FR-1.5: Phase delegation task inventory path — create phase file with ### T01.01 headings, assert execute_phase_tasks() is called (not ClaudeProcess), task results contain expected task IDs"
  source: "v3.3-requirements-spec.md:FR-1.5"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-008"
  text: "FR-1.6: Phase delegation freeform fallback — create phase file WITHOUT task headings, assert ClaudeProcess subprocess is spawned"
  source: "v3.3-requirements-spec.md:FR-1.6"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-009"
  text: "FR-1.7: Verify run_post_phase_wiring_hook() is called for BOTH per-task path (executor.py:1199-1204) AND per-phase/ClaudeProcess path (executor.py:1407-1412); wiring logger emits expected log entries for both"
  source: "v3.3-requirements-spec.md:FR-1.7"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-010"
  text: "FR-1.21: Assert check_wiring_report() wrapper (wiring_gate.py:1079) is called within wiring analysis flow; assert run_post_phase_wiring_hook() or run_post_task_wiring_hook() invokes check_wiring_report() as part of wiring analysis; assert wrapper delegates to underlying analysis and returns valid report structure"
  source: "v3.3-requirements-spec.md:FR-1.21"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-011"
  text: "FR-1.8: Assert run_post_task_anti_instinct_hook() returns tuple[TaskResult, TrailingGateResult | None], not a bare TaskResult"
  source: "v3.3-requirements-spec.md:FR-1.8"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-012"
  text: "FR-1.9: Run sprint with N phases (mix of task-inventory and freeform), assert all_gate_results contains results from ALL phases"
  source: "v3.3-requirements-spec.md:FR-1.9"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-013"
  text: "FR-1.10: Configure gate_rollout_mode='full', inject failing gate, assert failed TrailingGateResult is appended to remediation_log"
  source: "v3.3-requirements-spec.md:FR-1.10"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-014"
  text: "FR-1.11: Run sprint to completion, assert build_kpi_report() called with (all_gate_results, remediation_log, ledger), report file gate-kpi-report.md written to results_dir, report content includes wiring_analyses_run, wiring_remediations_attempted, wiring_net_cost"
  source: "v3.3-requirements-spec.md:FR-1.11"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false
  related_reqs: ["REQ-SC5"]

- id: "REQ-015"
  text: "FR-1.12: Assert _resolve_wiring_mode() is called within run_post_task_wiring_hook(), NOT config.wiring_gate_mode used directly"
  source: "v3.3-requirements-spec.md:FR-1.12"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-016"
  text: "FR-1.13: Configure wiring_gate_mode='shadow', inject findings, assert _log_shadow_findings_to_remediation_log() creates synthetic TrailingGateResult entries with [shadow] prefix"
  source: "v3.3-requirements-spec.md:FR-1.13"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-017"
  text: "FR-1.14: BLOCKING remediation lifecycle test — configure wiring_gate_mode='full', inject blocking findings with sufficient budget; assert full cycle: _format_wiring_failure() produces non-empty prompt; ledger.debit(config.remediation_cost) called; _recheck_wiring() called; on recheck pass: task status restored to PASS, wiring turns credited; on recheck fail: task status remains FAIL"
  source: "v3.3-requirements-spec.md:FR-1.14"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-018"
  text: "FR-1.15: Assert DeviationRegistry.load_or_create() receives exactly 3 positional args: (path, release_id, spec_hash)"
  source: "v3.3-requirements-spec.md:FR-1.15"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-019"
  text: "FR-1.16: Assert registry.merge_findings() receives (structural_list, semantic_list, run_number) — 3 args, correct positions"
  source: "v3.3-requirements-spec.md:FR-1.16"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-020"
  text: "FR-1.17: Assert _run_remediation() converts registry dicts to Finding objects without AttributeError"
  source: "v3.3-requirements-spec.md:FR-1.17"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-021"
  text: "FR-1.18: Assert TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET) uses 61 (not 46)"
  source: "v3.3-requirements-spec.md:FR-1.18"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-022"
  text: "FR-1.19: Assert SHADOW_GRACE_INFINITE constant is defined in models.py with expected sentinel value; assert when wiring_gate_grace_period is set to SHADOW_GRACE_INFINITE, shadow mode never exits grace period (wiring gate always credits back)"
  source: "v3.3-requirements-spec.md:FR-1.19"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-023"
  text: "FR-1.20: Assert __post_init__() correctly derives sprint config fields; assert derived fields (wiring_gate_enabled, wiring_gate_grace_period, wiring_analyses_count) are computed from base config values; assert invalid/missing base config produces sensible defaults"
  source: "v3.3-requirements-spec.md:FR-1.20"
  type: TEST
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false
```

### FR-2: TurnLedger Lifecycle Integration Tests

```yaml
- id: "REQ-024"
  text: "FR-2.1: Exercise execute_fidelity_with_convergence() end-to-end; assert debit CHECKER_COST → run checkers → credit CONVERGENCE_PASS_CREDIT → reimburse_for_progress(); assert budget_snapshot recorded in registry runs; assert budget logging includes consumed/reimbursed/available"
  source: "v3.3-requirements-spec.md:FR-2.1"
  type: TEST
  priority: P0
  domain: turnledger_lifecycle
  cross_cutting: false

- id: "REQ-025"
  text: "FR-2.1a: Assert handle_regression() is reachable from _run_convergence_spec_fidelity and is called on regression detection; assert when convergence detects regression (score decreases between runs), handle_regression() is invoked; assert handle_regression() logs regression event and adjusts budget accordingly"
  source: "v3.3-requirements-spec.md:FR-2.1a"
  type: TEST
  priority: P0
  domain: turnledger_lifecycle
  cross_cutting: false

- id: "REQ-026"
  text: "FR-2.2: Exercise execute_sprint() → execute_phase_tasks() with task-inventory phase; assert pre-debit minimum_allocation → subprocess → reconcile actual vs pre-allocated; assert post-task hooks (wiring + anti-instinct) fire with ledger"
  source: "v3.3-requirements-spec.md:FR-2.2"
  type: TEST
  priority: P0
  domain: turnledger_lifecycle
  cross_cutting: false

- id: "REQ-027"
  text: "FR-2.3: Exercise execute_sprint() → ClaudeProcess fallback → run_post_phase_wiring_hook(); assert debit_wiring() called → analysis → credit_wiring() on non-blocking result; assert wiring_analyses_count incremented"
  source: "v3.3-requirements-spec.md:FR-2.3"
  type: TEST
  priority: P0
  domain: turnledger_lifecycle
  cross_cutting: false

- id: "REQ-028"
  text: "FR-2.4: Sprint with mixed phases (task-inventory + freeform); assert ledger state coherent after both paths execute; assert available() = initial_budget - consumed + reimbursed holds at every checkpoint"
  source: "v3.3-requirements-spec.md:FR-2.4"
  type: TEST
  priority: P0
  domain: turnledger_lifecycle
  cross_cutting: false
```

### FR-3: Gate Rollout Mode Scenarios

```yaml
- id: "REQ-029"
  text: "FR-3.1: Mode matrix — 4 modes (off, shadow, soft, full) tested for both execution paths (anti-instinct + wiring); each must verify correct TaskStatus/GateOutcome, TurnLedger state, DeferredRemediationLog entries, ShadowGateMetrics recording"
  source: "v3.3-requirements-spec.md:FR-3.1"
  type: TEST
  priority: P0
  domain: gate_rollout_modes
  cross_cutting: false

- id: "REQ-030"
  text: "FR-3.1a: off mode — Anti-Instinct evaluates + ignores; Wiring skips analysis"
  source: "v3.3-requirements-spec.md:FR-3.1 table"
  type: ACCEPTANCE_CRITERION
  priority: P0
  domain: gate_rollout_modes
  cross_cutting: false

- id: "REQ-031"
  text: "FR-3.1b: shadow mode — Anti-Instinct evaluates + records metrics; Wiring analyzes + logs + credits back"
  source: "v3.3-requirements-spec.md:FR-3.1 table"
  type: ACCEPTANCE_CRITERION
  priority: P0
  domain: gate_rollout_modes
  cross_cutting: false

- id: "REQ-032"
  text: "FR-3.1c: soft mode — Anti-Instinct evaluates + records + credits/remediates; Wiring analyzes + warns critical + credits back"
  source: "v3.3-requirements-spec.md:FR-3.1 table"
  type: ACCEPTANCE_CRITERION
  priority: P0
  domain: gate_rollout_modes
  cross_cutting: false

- id: "REQ-033"
  text: "FR-3.1d: full mode — Anti-Instinct evaluates + records + credits/remediates + FAIL; Wiring analyzes + blocks critical+major + remediates"
  source: "v3.3-requirements-spec.md:FR-3.1 table"
  type: ACCEPTANCE_CRITERION
  priority: P0
  domain: gate_rollout_modes
  cross_cutting: false

- id: "REQ-034"
  text: "FR-3.2a: Budget exhausted before task launch — task marked SKIPPED, remaining tasks listed"
  source: "v3.3-requirements-spec.md:FR-3.2 table"
  type: TEST
  priority: P0
  domain: gate_rollout_modes
  cross_cutting: false

- id: "REQ-035"
  text: "FR-3.2b: Budget exhausted before wiring analysis — wiring hook skipped, task status unchanged"
  source: "v3.3-requirements-spec.md:FR-3.2 table"
  type: TEST
  priority: P0
  domain: gate_rollout_modes
  cross_cutting: false

- id: "REQ-036"
  text: "FR-3.2c: Budget exhausted before remediation — FAIL status persists, BUDGET_EXHAUSTED logged"
  source: "v3.3-requirements-spec.md:FR-3.2 table"
  type: TEST
  priority: P0
  domain: gate_rollout_modes
  cross_cutting: false

- id: "REQ-037"
  text: "FR-3.2d: Budget exhausted mid-convergence — halt with diagnostic, run_count < max_runs"
  source: "v3.3-requirements-spec.md:FR-3.2 table"
  type: TEST
  priority: P0
  domain: gate_rollout_modes
  cross_cutting: false

- id: "REQ-038"
  text: "FR-3.3: Simulate signal interrupt mid-execution; assert KPI report is still written; remediation log is persisted to disk; sprint outcome = INTERRUPTED"
  source: "v3.3-requirements-spec.md:FR-3.3"
  type: TEST
  priority: P0
  domain: gate_rollout_modes
  cross_cutting: false
```

### FR-4: Reachability Eval Framework (Hybrid A+D)

```yaml
- id: "REQ-039"
  text: "FR-4.1: Spec-driven wiring manifest — each release spec declares a wiring_manifest section with entry_points and required_reachable; authoritative manifest has 13 entries including v3.1, v3.2, and v3.05 constructs"
  source: "v3.3-requirements-spec.md:FR-4.1"
  type: FUNCTIONAL
  priority: P0
  domain: reachability_framework
  cross_cutting: false

- id: "REQ-040"
  text: "FR-4.2: AST call-chain analyzer — inputs: entry point module + function name, target function FQN; algorithm: ast.parse() → walk AST → build call graph (function → set of called functions) → resolve imports → BFS/DFS from entry point → report targets NOT in reachable set as GAP"
  source: "v3.3-requirements-spec.md:FR-4.2"
  type: FUNCTIONAL
  priority: P0
  domain: reachability_framework
  cross_cutting: false

- id: "REQ-041"
  text: "FR-4.2 limitations: document dynamic dispatch produces false negatives; conditional imports (TYPE_CHECKING) excluded; lazy imports inside functions ARE included"
  source: "v3.3-requirements-spec.md:FR-4.2 limitations"
  type: CONSTRAINT
  priority: P1
  domain: reachability_framework
  cross_cutting: false

- id: "REQ-042"
  text: "FR-4.3: Reachability gate integration — reads wiring manifest, runs AST analysis per entry, produces structured PASS/FAIL report with unreachable targets and spec references; integrates with existing GateCriteria infrastructure"
  source: "v3.3-requirements-spec.md:FR-4.3"
  type: FUNCTIONAL
  priority: P0
  domain: reachability_framework
  cross_cutting: false

- id: "REQ-043"
  text: "FR-4.4: Regression test — intentionally remove call to run_post_phase_wiring_hook() from execute_sprint(); run reachability gate; assert it detects gap and references correct spec (v3.2-T02)"
  source: "v3.3-requirements-spec.md:FR-4.4"
  type: TEST
  priority: P0
  domain: reachability_framework
  cross_cutting: false
  related_reqs: ["REQ-SC7", "REQ-SC9"]
```

### FR-5: Pipeline Fixes

```yaml
- id: "REQ-044"
  text: "FR-5.1: In run_wiring_analysis() (wiring_gate.py:673+), after file collection: if files_analyzed == 0 AND source directory non-empty (contains *.py files): return FAIL report with failure_reason: '0 files analyzed from non-empty source directory'"
  source: "v3.3-requirements-spec.md:FR-5.1"
  type: FUNCTIONAL
  priority: P0
  domain: pipeline_fixes
  cross_cutting: false

- id: "REQ-045"
  text: "FR-5.1 test: Point run_wiring_analysis() at non-empty directory where file collection returns 0 analyzed files; assert FAIL, not silent PASS"
  source: "v3.3-requirements-spec.md:FR-5.1 test"
  type: TEST
  priority: P0
  domain: pipeline_fixes
  cross_cutting: false
  related_reqs: ["REQ-SC10"]

- id: "REQ-046"
  text: "FR-5.2: New check phase that: (1) reads spec's declared FR-* items; (2) for each FR, searches implementation codebase for evidence (function names, class names, docstring references); (3) reports FRs with no implementation evidence as gaps"
  source: "v3.3-requirements-spec.md:FR-5.2"
  type: FUNCTIONAL
  priority: P0
  domain: pipeline_fixes
  cross_cutting: false

- id: "REQ-047"
  text: "FR-5.2 integration point: runs as additional checker in _run_checkers() alongside structural and semantic layers"
  source: "v3.3-requirements-spec.md:FR-5.2 integration"
  type: INTEGRATION
  priority: P0
  domain: pipeline_fixes
  cross_cutting: false

- id: "REQ-048"
  text: "FR-5.2 test: Create spec with FR referencing a function; assert checker finds it; remove function; assert checker flags the gap"
  source: "v3.3-requirements-spec.md:FR-5.2 test"
  type: TEST
  priority: P0
  domain: pipeline_fixes
  cross_cutting: false
  related_reqs: ["REQ-SC11"]

- id: "REQ-049"
  text: "FR-5.3: Reachability Gate (Weakness #2) — this IS FR-4; cross-referenced here for traceability"
  source: "v3.3-requirements-spec.md:FR-5.3"
  type: DEPENDENCY
  priority: P0
  domain: pipeline_fixes
  cross_cutting: false
```

### FR-6: Remaining QA Gaps

```yaml
- id: "REQ-050"
  text: "FR-6.1 T07: Write 7 tests in tests/roadmap/test_convergence_wiring.py"
  source: "v3.3-requirements-spec.md:FR-6.1 table T07"
  type: TEST
  priority: P0
  domain: qa_gaps
  cross_cutting: false

- id: "REQ-051"
  text: "FR-6.1 T11: Write 6 tests for v3.3-SC-1 through v3.3-SC-6 in tests/roadmap/test_convergence_e2e.py"
  source: "v3.3-requirements-spec.md:FR-6.1 table T11"
  type: TEST
  priority: P0
  domain: qa_gaps
  cross_cutting: false

- id: "REQ-052"
  text: "FR-6.1 T12: Write smoke test for convergence path"
  source: "v3.3-requirements-spec.md:FR-6.1 table T12"
  type: TEST
  priority: P0
  domain: qa_gaps
  cross_cutting: false

- id: "REQ-053"
  text: "FR-6.1 T14: Regenerate wiring-verification artifact + validate"
  source: "v3.3-requirements-spec.md:FR-6.1 table T14"
  type: PROCESS
  priority: P1
  domain: qa_gaps
  cross_cutting: false

- id: "REQ-054"
  text: "FR-6.2 T02: run_post_phase_wiring_hook() call — already verified WIRED — write confirming test"
  source: "v3.3-requirements-spec.md:FR-6.2 table T02"
  type: TEST
  priority: P0
  domain: qa_gaps
  cross_cutting: false

- id: "REQ-055"
  text: "FR-6.2 T17-T22: Integration tests, regression suite, gap closure audit — write tests per this spec"
  source: "v3.3-requirements-spec.md:FR-6.2 table T17-T22"
  type: TEST
  priority: P0
  domain: qa_gaps
  cross_cutting: false
```

### FR-7: Audit Trail Infrastructure

```yaml
- id: "REQ-056"
  text: "FR-7.1: Each test writes JSONL audit record to {results_dir}/audit-trail.jsonl with 9-field schema: test_id, spec_ref, timestamp, assertion_type, inputs, observed, expected, verdict, evidence, duration_ms"
  source: "v3.3-requirements-spec.md:FR-7.1"
  type: FUNCTIONAL
  priority: P0
  domain: audit_trail
  cross_cutting: true

- id: "REQ-057"
  text: "FR-7.2: Third party with no prior knowledge MUST determine from audit trail alone: were real tests run (timestamp, duration, actual observed values); were tests run per spec (spec_ref traces to code, inputs show config); are results real (observed has concrete runtime values); pass/fail determination is sound (explicit expected vs observed comparison)"
  source: "v3.3-requirements-spec.md:FR-7.2"
  type: QUALITY_GATE
  priority: P0
  domain: audit_trail
  cross_cutting: true

- id: "REQ-058"
  text: "FR-7.3: pytest fixture (audit_trail) that: opens audit-trail.jsonl in results_dir; provides record(test_id, spec_ref, assertion_type, inputs, observed, expected, verdict, evidence) method; assertion_type must match FR-7.1 schema field; duration_ms auto-computed; auto-flushes after each test; produces summary report at session end: total tests, passed, failed, coverage of wiring points"
  source: "v3.3-requirements-spec.md:FR-7.3"
  type: FUNCTIONAL
  priority: P0
  domain: audit_trail
  cross_cutting: true
```

### Non-Functional Requirements

```yaml
- id: "REQ-NFR1"
  text: "NFR-1: No mocking gate functions or core orchestration logic; _subprocess_factory is the only allowed injection point for external process replacement"
  source: "v3.3-requirements-spec.md:FR-1 constraint, roadmap NFR-1"
  type: NON_FUNCTIONAL
  priority: P0
  domain: constraints
  cross_cutting: true

- id: "REQ-NFR2"
  text: "NFR-2: All Python execution via UV — uv run pytest, not python -m pytest"
  source: "v3.3-requirements-spec.md:Constraints"
  type: NON_FUNCTIONAL
  priority: P0
  domain: constraints
  cross_cutting: true

- id: "REQ-NFR3"
  text: "NFR-3: Full test suite must pass with ≥4894 passed, ≤3 pre-existing failures, 0 regressions"
  source: "v3.3-requirements-spec.md:Constraints, Phase 4"
  type: NON_FUNCTIONAL
  priority: P0
  domain: constraints
  cross_cutting: true

- id: "REQ-NFR4"
  text: "NFR-4: Every test must emit a JSONL audit trail record"
  source: "v3.3-requirements-spec.md:Constraints"
  type: NON_FUNCTIONAL
  priority: P0
  domain: audit_trail
  cross_cutting: true

- id: "REQ-NFR5"
  text: "NFR-5: Spec-driven manifest is source of truth for reachability gate; every known wiring point from FR-1 must have a manifest entry"
  source: "v3.3-requirements-spec.md:FR-4.1 preamble, roadmap Phase 4 task 4.4"
  type: NON_FUNCTIONAL
  priority: P0
  domain: reachability_framework
  cross_cutting: false

- id: "REQ-NFR6"
  text: "NFR-6: AST analyzer limitations documented in module docstring"
  source: "v3.3-requirements-spec.md:FR-4.2 limitations, roadmap 1B.3"
  type: NON_FUNCTIONAL
  priority: P1
  domain: reachability_framework
  cross_cutting: false
```

### Success Criteria (as Requirements)

```yaml
- id: "REQ-SC1"
  text: "SC-1: All 20+ wiring points have ≥1 E2E test — test count ≥20, mapped to FR-1"
  source: "v3.3-requirements-spec.md:SC-1"
  type: SUCCESS_CRITERION
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-SC2"
  text: "SC-2: TurnLedger lifecycle covered for all 4 paths — Convergence, per-task, per-phase, cross-path"
  source: "v3.3-requirements-spec.md:SC-2"
  type: SUCCESS_CRITERION
  priority: P0
  domain: turnledger_lifecycle
  cross_cutting: false

- id: "REQ-SC3"
  text: "SC-3: Gate rollout modes covered (off/shadow/soft/full) — 4 modes × 2 paths = 8+ scenarios"
  source: "v3.3-requirements-spec.md:SC-3"
  type: SUCCESS_CRITERION
  priority: P0
  domain: gate_rollout_modes
  cross_cutting: false

- id: "REQ-SC4"
  text: "SC-4: Zero regressions from baseline — ≥4894 passed, ≤3 pre-existing failures"
  source: "v3.3-requirements-spec.md:SC-4"
  type: SUCCESS_CRITERION
  priority: P0
  domain: constraints
  cross_cutting: false

- id: "REQ-SC5"
  text: "SC-5: KPI report accuracy validated — integration test proves field VALUES are correct (not just present): wiring_analyses_run, wiring_remediations_attempted, wiring_net_cost match computed expectations from test inputs"
  source: "v3.3-requirements-spec.md:SC-5"
  type: SUCCESS_CRITERION
  priority: P0
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-SC6"
  text: "SC-6: Budget exhaustion paths validated — 4 exhaustion scenarios tested"
  source: "v3.3-requirements-spec.md:SC-6"
  type: SUCCESS_CRITERION
  priority: P0
  domain: gate_rollout_modes
  cross_cutting: false

- id: "REQ-SC7"
  text: "SC-7: Eval framework catches known-bad state — regression test: break wiring → detected"
  source: "v3.3-requirements-spec.md:SC-7"
  type: SUCCESS_CRITERION
  priority: P0
  domain: reachability_framework
  cross_cutting: false

- id: "REQ-SC8"
  text: "SC-8: Remaining QA gaps closed — v3.05 T07/T11/T12/T14, v3.2 T02/T17-T22"
  source: "v3.3-requirements-spec.md:SC-8"
  type: SUCCESS_CRITERION
  priority: P0
  domain: qa_gaps
  cross_cutting: false

- id: "REQ-SC9"
  text: "SC-9: Reachability gate catches unreachable code — Hybrid A+D detects intentionally broken wiring"
  source: "v3.3-requirements-spec.md:SC-9"
  type: SUCCESS_CRITERION
  priority: P0
  domain: reachability_framework
  cross_cutting: false

- id: "REQ-SC10"
  text: "SC-10: 0-files-analyzed produces FAIL — assertion added, test proves it"
  source: "v3.3-requirements-spec.md:SC-10"
  type: SUCCESS_CRITERION
  priority: P0
  domain: pipeline_fixes
  cross_cutting: false

- id: "REQ-SC11"
  text: "SC-11: Impl-vs-spec fidelity check exists — new checker finds and flags missing implementations"
  source: "v3.3-requirements-spec.md:SC-11"
  type: SUCCESS_CRITERION
  priority: P0
  domain: pipeline_fixes
  cross_cutting: false

- id: "REQ-SC12"
  text: "SC-12: Audit trail is third-party verifiable — JSONL output with all 4 verification properties"
  source: "v3.3-requirements-spec.md:SC-12"
  type: SUCCESS_CRITERION
  priority: P0
  domain: audit_trail
  cross_cutting: false
```

### Process Requirements

```yaml
- id: "REQ-PROC1"
  text: "Phased implementation: Phase 1 (Infrastructure) → Phase 2 (Test Coverage, depends on Phase 1A) → Phase 3 (Pipeline Fixes, depends on Phase 1B + Phase 2) → Phase 4 (Validation, depends on all)"
  source: "v3.3-requirements-spec.md:Phased Implementation Plan"
  type: SEQUENCING
  priority: P0
  domain: constraints
  cross_cutting: false

- id: "REQ-PROC2"
  text: "Branch from v3.0-v3.2-Fidelity branch"
  source: "v3.3-requirements-spec.md:Constraints"
  type: CONSTRAINT
  priority: P0
  domain: constraints
  cross_cutting: false

- id: "REQ-PROC3"
  text: "Phase 4 validation: run full test suite (assert ≥4894 passed ≤3 pre-existing failures 0 regressions); run reachability gate on current codebase; generate audit trail summary report; cross-validate SC-* success criteria each has at least one passing test"
  source: "v3.3-requirements-spec.md:Phased Implementation Plan Phase 4"
  type: PROCESS
  priority: P0
  domain: constraints
  cross_cutting: false
```

### Risk Requirements

```yaml
- id: "REQ-RISK1"
  text: "Risk R1: AST analyzer false negatives on dynamic dispatch — mitigation: handle from-X-import-Y inside function bodies; test against known lazy imports in executor.py"
  source: "v3.3-requirements-spec.md:Risk Assessment"
  type: RISK_MITIGATION
  priority: P1
  domain: reachability_framework
  cross_cutting: false

- id: "REQ-RISK2"
  text: "Risk R2: E2E test flakiness from subprocess timing — mitigation: use _subprocess_factory; no real subprocess in E2E; reserve real subprocess for smoke test"
  source: "v3.3-requirements-spec.md:Risk Assessment"
  type: RISK_MITIGATION
  priority: P1
  domain: wiring_e2e_tests
  cross_cutting: false

- id: "REQ-RISK3"
  text: "Risk R3: Impl-vs-spec checker false positives — mitigation: start with exact function-name/class-name matching only; no NLP/fuzzy matching; fail-open on ambiguous matches; synthetic positive and negative tests"
  source: "v3.3-requirements-spec.md:Risk Assessment"
  type: RISK_MITIGATION
  priority: P1
  domain: pipeline_fixes
  cross_cutting: false
```

### Out of Scope

The following items are explicitly OUT OF SCOPE per spec. Excluded from coverage scoring (P3):
- Pipeline Weakness #1 (`source_dir` targeting) — already fixed
- Pipeline Weakness #5 (convergence disables spec-fidelity) — deferred to v3.4
- Production code modifications beyond FR-5.1/5.2 and FR-4.3
- `attempt_remediation()` full integration — noted as v3.3 deferral in code
- Runtime instrumentation (rejected in favor of static analysis)

---

## Summary Statistics

| Category | Count |
|----------|-------|
| Functional Requirements | 11 |
| Test Requirements | 33 |
| Non-Functional Requirements | 6 |
| Success Criteria | 12 |
| Process/Constraint Requirements | 5 |
| Acceptance Criteria | 4 |
| Risk Mitigations | 3 |
| Integration Requirements | 1 |
| Dependency/Cross-Ref | 1 |
| **TOTAL (P0+P1, in scope)** | **76** |
| Out of scope (P3) | 5 |

**Domains identified**: wiring_e2e_tests, turnledger_lifecycle, gate_rollout_modes, reachability_framework, pipeline_fixes, qa_gaps, audit_trail, constraints
