# v3.3 Requirement Universe

Extracted from: `v3.3-requirements-spec.md`
Extraction date: 2026-03-23

---

## Functional Requirements

### FR-1: E2E Test Coverage for Wiring Points

- id: "FR-1.1"
  text: "TurnLedger Construction Validation — Invoke execute_sprint() with minimal config. Assert ledger.initial_budget == config.max_turns * len(config.active_phases), ledger.reimbursement_rate == 0.8, ledger constructed BEFORE phase loop"
  source: "v3.3-requirements-spec.md:FR-1.1 (lines 80-88)"
  type: TEST
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-2.1"]

- id: "FR-1.2"
  text: "ShadowGateMetrics Construction — Assert ShadowGateMetrics() is constructed before phase loop"
  source: "v3.3-requirements-spec.md:FR-1.2 (lines 89-92)"
  type: TEST
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-1.1"]

- id: "FR-1.3"
  text: "DeferredRemediationLog Construction — Assert DeferredRemediationLog is constructed with persist_path under results_dir"
  source: "v3.3-requirements-spec.md:FR-1.3 (lines 95-99)"
  type: TEST
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-1.10", "FR-1.13"]

- id: "FR-1.4"
  text: "SprintGatePolicy Construction — Assert SprintGatePolicy(config) is constructed and receives the correct config"
  source: "v3.3-requirements-spec.md:FR-1.4 (lines 101-105)"
  type: TEST
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: []

- id: "FR-1.5"
  text: "Phase Delegation — Task Inventory Path — Create a phase file with ### T01.01 headings. Assert execute_phase_tasks() is called (not ClaudeProcess). Task results contain expected task IDs from the inventory"
  source: "v3.3-requirements-spec.md:FR-1.5 (lines 107-113)"
  type: TEST
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-1.6", "FR-2.2"]

- id: "FR-1.6"
  text: "Phase Delegation — Freeform Fallback Path — Create a phase file WITHOUT task headings. Assert ClaudeProcess subprocess is spawned"
  source: "v3.3-requirements-spec.md:FR-1.6 (lines 115-119)"
  type: TEST
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-1.5", "FR-2.3"]

- id: "FR-1.7"
  text: "Post-Phase Wiring Hook — Both Paths — Verify run_post_phase_wiring_hook() is called for per-task phases (executor.py:1199-1204) and per-phase/ClaudeProcess phases (executor.py:1407-1412)"
  source: "v3.3-requirements-spec.md:FR-1.7 (lines 121-127)"
  type: TEST
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: true
  related_reqs: ["FR-1.5", "FR-1.6", "FR-4.4", "FR-6.2-T02"]

- id: "FR-1.8"
  text: "Anti-Instinct Hook Return Type — Assert run_post_task_anti_instinct_hook() returns tuple[TaskResult, TrailingGateResult | None], not a bare TaskResult"
  source: "v3.3-requirements-spec.md:FR-1.8 (lines 129-133)"
  type: TEST
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-3.1"]

- id: "FR-1.9"
  text: "Gate Result Accumulation — Run a sprint with N phases (mix of task-inventory and freeform). Assert all_gate_results contains results from ALL phases"
  source: "v3.3-requirements-spec.md:FR-1.9 (lines 135-139)"
  type: TEST
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-1.11"]

- id: "FR-1.10"
  text: "Failed Gate → Remediation Log — Configure gate_rollout_mode='full', inject a failing gate. Assert failed TrailingGateResult is appended to remediation_log"
  source: "v3.3-requirements-spec.md:FR-1.10 (lines 141-145)"
  type: TEST
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-1.3", "FR-1.13", "FR-1.14"]

- id: "FR-1.11"
  text: "KPI Report Generation — Run sprint to completion. Assert build_kpi_report() called with all_gate_results, remediation_log, ledger. Report file gate-kpi-report.md written to results_dir. Report includes wiring KPI fields: wiring_analyses_run, wiring_remediations_attempted, wiring_net_cost"
  source: "v3.3-requirements-spec.md:FR-1.11 (lines 147-154)"
  type: TEST
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-1.9", "SC-5"]

- id: "FR-1.12"
  text: "Wiring Mode Resolution — Assert _resolve_wiring_mode() is called within run_post_task_wiring_hook(), NOT config.wiring_gate_mode used directly"
  source: "v3.3-requirements-spec.md:FR-1.12 (lines 156-160)"
  type: TEST
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-3.1"]

- id: "FR-1.13"
  text: "Shadow Findings → Remediation Log — Configure wiring_gate_mode='shadow', inject findings. Assert _log_shadow_findings_to_remediation_log() creates synthetic TrailingGateResult entries with [shadow] prefix"
  source: "v3.3-requirements-spec.md:FR-1.13 (lines 162-166)"
  type: TEST
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-1.3", "FR-1.10"]

- id: "FR-1.14"
  text: "BLOCKING Remediation Lifecycle — Configure wiring_gate_mode='full', inject blocking findings with sufficient budget. Assert full cycle: _format_wiring_failure() produces non-empty prompt, ledger.debit(config.remediation_cost) called, _recheck_wiring() called, on recheck pass: task status restored to PASS + wiring turns credited, on recheck fail: task status remains FAIL"
  source: "v3.3-requirements-spec.md:FR-1.14 (lines 168-178)"
  type: TEST
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-1.10", "FR-2.1"]

- id: "FR-1.14a"
  text: "BLOCKING Remediation sub-req: _format_wiring_failure() produces non-empty prompt"
  source: "v3.3-requirements-spec.md:FR-1.14 sub-item 1"
  type: ACCEPTANCE_CRITERION
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-1.14"]

- id: "FR-1.14b"
  text: "BLOCKING Remediation sub-req: ledger.debit(config.remediation_cost) is called"
  source: "v3.3-requirements-spec.md:FR-1.14 sub-item 2"
  type: ACCEPTANCE_CRITERION
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-1.14"]

- id: "FR-1.14c"
  text: "BLOCKING Remediation sub-req: _recheck_wiring() is called, on pass → PASS restored + credited, on fail → FAIL persists"
  source: "v3.3-requirements-spec.md:FR-1.14 sub-items 3-5"
  type: ACCEPTANCE_CRITERION
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-1.14"]

- id: "FR-1.15"
  text: "Convergence Registry Args — Assert DeviationRegistry.load_or_create() receives exactly 3 positional args: (path, release_id, spec_hash)"
  source: "v3.3-requirements-spec.md:FR-1.15 (lines 179-183)"
  type: TEST
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-2.1"]

- id: "FR-1.16"
  text: "Convergence Merge Args — Assert registry.merge_findings() receives (structural_list, semantic_list, run_number) — 3 args, correct positions"
  source: "v3.3-requirements-spec.md:FR-1.16 (lines 185-189)"
  type: TEST
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-1.15"]

- id: "FR-1.17"
  text: "Convergence Remediation Dict→Finding — Assert _run_remediation() converts registry dicts to Finding objects without AttributeError"
  source: "v3.3-requirements-spec.md:FR-1.17 (lines 191-195)"
  type: TEST
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-1.14"]

- id: "FR-1.18"
  text: "Budget Constants — Assert TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET) uses 61 (not 46)"
  source: "v3.3-requirements-spec.md:FR-1.18 (lines 197-201)"
  type: TEST
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-2.1"]

- id: "FR-1-CONSTRAINT"
  text: "Tests MUST NOT mock gate functions or core orchestration logic. The _subprocess_factory injection point in execute_phase_tasks() is acceptable because it replaces the external claude binary, not internal logic."
  source: "v3.3-requirements-spec.md:FR-1 constraint (lines 77-78)"
  type: CONSTRAINT
  priority: P0
  domain: "testing-constraints"
  cross_cutting: true
  related_reqs: ["NFR-1"]

### FR-2: TurnLedger Lifecycle Integration Tests

- id: "FR-2.1"
  text: "Convergence Path (v3.05) — Exercise execute_fidelity_with_convergence() E2E. Assert: debit CHECKER_COST → run checkers → credit CONVERGENCE_PASS_CREDIT → reimburse_for_progress(). budget_snapshot recorded. Budget logging includes consumed/reimbursed/available"
  source: "v3.3-requirements-spec.md:FR-2.1 (lines 209-214)"
  type: TEST
  priority: P0
  domain: "turnledger-lifecycle"
  cross_cutting: false
  related_reqs: ["FR-1.15", "FR-1.16", "FR-1.18"]

- id: "FR-2.2"
  text: "Sprint Per-Task Path (v3.1) — Exercise execute_sprint() → execute_phase_tasks() with task-inventory phase. Assert: pre-debit minimum_allocation → subprocess → reconcile actual vs pre-allocated. Post-task hooks (wiring + anti-instinct) fire with ledger"
  source: "v3.3-requirements-spec.md:FR-2.2 (lines 216-221)"
  type: TEST
  priority: P0
  domain: "turnledger-lifecycle"
  cross_cutting: false
  related_reqs: ["FR-1.5", "FR-1.7", "FR-1.8"]

- id: "FR-2.3"
  text: "Sprint Per-Phase Path (v3.2) — Exercise execute_sprint() → ClaudeProcess fallback → run_post_phase_wiring_hook(). Assert: debit_wiring() called → analysis → credit_wiring() on non-blocking. wiring_analyses_count incremented"
  source: "v3.3-requirements-spec.md:FR-2.3 (lines 223-227)"
  type: TEST
  priority: P0
  domain: "turnledger-lifecycle"
  cross_cutting: false
  related_reqs: ["FR-1.6", "FR-1.7"]

- id: "FR-2.4"
  text: "Cross-Path Coherence — Sprint with mixed phases (some task-inventory, some freeform). Assert: ledger state is coherent after both paths execute. available() = initial_budget - consumed + reimbursed holds at every checkpoint"
  source: "v3.3-requirements-spec.md:FR-2.4 (lines 229-233)"
  type: TEST
  priority: P0
  domain: "turnledger-lifecycle"
  cross_cutting: true
  related_reqs: ["FR-2.2", "FR-2.3"]

### FR-3: Gate Rollout Mode Scenarios

- id: "FR-3.1a"
  text: "Mode=off — Anti-Instinct: Evaluate + ignore. Wiring: Skip analysis. Verify correct TaskStatus/GateOutcome, TurnLedger state, DeferredRemediationLog entries, ShadowGateMetrics recording"
  source: "v3.3-requirements-spec.md:FR-3.1 mode matrix (lines 242-253)"
  type: TEST
  priority: P0
  domain: "gate-modes"
  cross_cutting: false
  related_reqs: ["FR-1.12"]

- id: "FR-3.1b"
  text: "Mode=shadow — Anti-Instinct: Evaluate + record metrics. Wiring: Analyze + log + credit back. Verify correct TaskStatus/GateOutcome, TurnLedger state, DeferredRemediationLog entries, ShadowGateMetrics recording"
  source: "v3.3-requirements-spec.md:FR-3.1 mode matrix (lines 242-253)"
  type: TEST
  priority: P0
  domain: "gate-modes"
  cross_cutting: false
  related_reqs: ["FR-1.12", "FR-1.13"]

- id: "FR-3.1c"
  text: "Mode=soft — Anti-Instinct: Evaluate + record + credit/remediate. Wiring: Analyze + warn critical + credit back. Verify correct TaskStatus/GateOutcome, TurnLedger state, DeferredRemediationLog entries, ShadowGateMetrics recording"
  source: "v3.3-requirements-spec.md:FR-3.1 mode matrix (lines 242-253)"
  type: TEST
  priority: P0
  domain: "gate-modes"
  cross_cutting: false
  related_reqs: ["FR-1.12"]

- id: "FR-3.1d"
  text: "Mode=full — Anti-Instinct: Evaluate + record + credit/remediate + FAIL. Wiring: Analyze + block critical+major + remediate. Verify correct TaskStatus/GateOutcome, TurnLedger state, DeferredRemediationLog entries, ShadowGateMetrics recording"
  source: "v3.3-requirements-spec.md:FR-3.1 mode matrix (lines 242-253)"
  type: TEST
  priority: P0
  domain: "gate-modes"
  cross_cutting: false
  related_reqs: ["FR-1.12", "FR-1.14"]

- id: "FR-3.1-AC1"
  text: "Each mode test must verify correct TaskStatus / GateOutcome after hook execution"
  source: "v3.3-requirements-spec.md:FR-3.1 (lines 249-253)"
  type: ACCEPTANCE_CRITERION
  priority: P0
  domain: "gate-modes"
  cross_cutting: false
  related_reqs: ["FR-3.1a", "FR-3.1b", "FR-3.1c", "FR-3.1d"]

- id: "FR-3.1-AC2"
  text: "Each mode test must verify correct TurnLedger state (debits/credits match expected)"
  source: "v3.3-requirements-spec.md:FR-3.1 (lines 249-253)"
  type: ACCEPTANCE_CRITERION
  priority: P0
  domain: "gate-modes"
  cross_cutting: false
  related_reqs: ["FR-3.1a", "FR-3.1b", "FR-3.1c", "FR-3.1d"]

- id: "FR-3.1-AC3"
  text: "Each mode test must verify correct DeferredRemediationLog entries (present or absent)"
  source: "v3.3-requirements-spec.md:FR-3.1 (lines 249-253)"
  type: ACCEPTANCE_CRITERION
  priority: P0
  domain: "gate-modes"
  cross_cutting: false
  related_reqs: ["FR-3.1a", "FR-3.1b", "FR-3.1c", "FR-3.1d"]

- id: "FR-3.1-AC4"
  text: "Each mode test must verify correct ShadowGateMetrics recording (present or absent)"
  source: "v3.3-requirements-spec.md:FR-3.1 (lines 249-253)"
  type: ACCEPTANCE_CRITERION
  priority: P0
  domain: "gate-modes"
  cross_cutting: false
  related_reqs: ["FR-3.1a", "FR-3.1b", "FR-3.1c", "FR-3.1d"]

- id: "FR-3.2a"
  text: "Budget exhausted before task launch — Task marked SKIPPED, remaining tasks listed"
  source: "v3.3-requirements-spec.md:FR-3.2 (lines 257-260)"
  type: TEST
  priority: P0
  domain: "gate-modes"
  cross_cutting: false
  related_reqs: ["FR-2.4"]

- id: "FR-3.2b"
  text: "Budget exhausted before wiring analysis — Wiring hook skipped, task status unchanged"
  source: "v3.3-requirements-spec.md:FR-3.2 (lines 257-260)"
  type: TEST
  priority: P0
  domain: "gate-modes"
  cross_cutting: false
  related_reqs: []

- id: "FR-3.2c"
  text: "Budget exhausted before remediation — FAIL status persists, BUDGET_EXHAUSTED logged"
  source: "v3.3-requirements-spec.md:FR-3.2 (lines 257-260)"
  type: TEST
  priority: P0
  domain: "gate-modes"
  cross_cutting: false
  related_reqs: ["FR-1.14"]

- id: "FR-3.2d"
  text: "Budget exhausted mid-convergence — Halt with diagnostic, run_count < max_runs"
  source: "v3.3-requirements-spec.md:FR-3.2 (lines 257-260)"
  type: TEST
  priority: P0
  domain: "gate-modes"
  cross_cutting: false
  related_reqs: ["FR-2.1"]

- id: "FR-3.3"
  text: "Interrupted Sprint — Simulate signal interrupt mid-execution. Assert: KPI report is still written, remediation log persisted to disk, sprint outcome = INTERRUPTED"
  source: "v3.3-requirements-spec.md:FR-3.3 (lines 264-269)"
  type: TEST
  priority: P0
  domain: "gate-modes"
  cross_cutting: false
  related_reqs: ["FR-1.11"]

### FR-4: Reachability Eval Framework

- id: "FR-4.1"
  text: "Spec-Driven Wiring Manifest — YAML schema with entry_points section listing callable entry points and required_reachable section listing target symbols with spec references"
  source: "v3.3-requirements-spec.md:FR-4.1 (lines 277-325)"
  type: FUNCTIONAL
  priority: P0
  domain: "reachability"
  cross_cutting: false
  related_reqs: ["FR-4.2", "FR-4.3", "NFR-5"]

- id: "FR-4.2"
  text: "AST Call-Chain Analyzer — ast.parse() the entry point module → build call graph → resolve imports for cross-module calls → BFS/DFS reachability → report targets NOT in reachable set as GAP. Document limitations: dynamic dispatch false negatives, TYPE_CHECKING excluded, lazy imports inside functions included"
  source: "v3.3-requirements-spec.md:FR-4.2 (lines 327-342)"
  type: FUNCTIONAL
  priority: P0
  domain: "reachability"
  cross_cutting: false
  related_reqs: ["FR-4.1", "FR-4.3", "NFR-6"]

- id: "FR-4.2-LIM1"
  text: "AST analyzer documented limitation: Dynamic dispatch (getattr, **kwargs) produces false negatives"
  source: "v3.3-requirements-spec.md:FR-4.2 limitations (line 339)"
  type: CONSTRAINT
  priority: P1
  domain: "reachability"
  cross_cutting: false
  related_reqs: ["FR-4.2", "NFR-6"]

- id: "FR-4.2-LIM2"
  text: "AST analyzer documented limitation: Conditional imports (if TYPE_CHECKING) excluded from reachability"
  source: "v3.3-requirements-spec.md:FR-4.2 limitations (line 340)"
  type: CONSTRAINT
  priority: P1
  domain: "reachability"
  cross_cutting: false
  related_reqs: ["FR-4.2", "NFR-6"]

- id: "FR-4.2-LIM3"
  text: "AST analyzer documented limitation: Lazy imports inside functions ARE included (real runtime paths)"
  source: "v3.3-requirements-spec.md:FR-4.2 limitations (line 341)"
  type: CONSTRAINT
  priority: P1
  domain: "reachability"
  cross_cutting: false
  related_reqs: ["FR-4.2", "NFR-6"]

- id: "FR-4.3"
  text: "Reachability Gate Integration — Analyzer runs as pipeline gate: reads wiring manifest, runs AST analysis for each entry, produces PASS/FAIL report with unreachable targets and spec refs, integrates with GateCriteria infrastructure"
  source: "v3.3-requirements-spec.md:FR-4.3 (lines 344-352)"
  type: FUNCTIONAL
  priority: P0
  domain: "reachability"
  cross_cutting: true
  related_reqs: ["FR-4.1", "FR-4.2", "FR-5.3"]

- id: "FR-4.4"
  text: "Regression Test — Intentionally remove call to run_post_phase_wiring_hook() from execute_sprint(). Run reachability gate. Assert it detects the gap and references v3.2-T02"
  source: "v3.3-requirements-spec.md:FR-4.4 (lines 354-356)"
  type: TEST
  priority: P0
  domain: "reachability"
  cross_cutting: false
  related_reqs: ["FR-4.3", "SC-7", "SC-9"]

### FR-5: Pipeline Fixes

- id: "FR-5.1"
  text: "0-Files-Analyzed Assertion — In run_wiring_analysis() (wiring_gate.py:673+), if files_analyzed == 0 AND source directory is non-empty (contains *.py files): return FAIL report with failure_reason: '0 files analyzed from non-empty source directory'"
  source: "v3.3-requirements-spec.md:FR-5.1 (lines 361-369)"
  type: FUNCTIONAL
  priority: P0
  domain: "pipeline-fixes"
  cross_cutting: false
  related_reqs: ["SC-10"]

- id: "FR-5.1-TEST"
  text: "Test: Point run_wiring_analysis() at an empty directory. Assert FAIL, not silent PASS"
  source: "v3.3-requirements-spec.md:FR-5.1 test (line 369)"
  type: TEST
  priority: P0
  domain: "pipeline-fixes"
  cross_cutting: false
  related_reqs: ["FR-5.1"]

- id: "FR-5.2"
  text: "Impl-vs-Spec Fidelity Check — New check phase: reads spec FR-* items, searches implementation for evidence (function names, class names, docstring refs), reports FRs with no implementation evidence as gaps. Runs as additional checker in _run_checkers() alongside structural and semantic layers"
  source: "v3.3-requirements-spec.md:FR-5.2 (lines 371-382)"
  type: FUNCTIONAL
  priority: P0
  domain: "pipeline-fixes"
  cross_cutting: true
  related_reqs: ["SC-11"]

- id: "FR-5.2-TEST"
  text: "Test: Create spec with FR referencing a function → checker finds it. Remove function → checker flags gap"
  source: "v3.3-requirements-spec.md:FR-5.2 test (line 382)"
  type: TEST
  priority: P0
  domain: "pipeline-fixes"
  cross_cutting: false
  related_reqs: ["FR-5.2"]

- id: "FR-5.3"
  text: "Reachability Gate (Weakness #2) — Cross-reference to FR-4"
  source: "v3.3-requirements-spec.md:FR-5.3 (lines 384-386)"
  type: FUNCTIONAL
  priority: P0
  domain: "reachability"
  cross_cutting: false
  related_reqs: ["FR-4.3"]

### FR-6: Remaining QA Gaps

- id: "FR-6.1-T07"
  text: "v3.05 Gap T07 — tests/roadmap/test_convergence_wiring.py — 7 tests: Write tests"
  source: "v3.3-requirements-spec.md:FR-6.1 (lines 394-396)"
  type: TEST
  priority: P0
  domain: "qa-gaps"
  cross_cutting: false
  related_reqs: ["SC-8"]

- id: "FR-6.1-T11"
  text: "v3.05 Gap T11 — tests/roadmap/test_convergence_e2e.py — 6 tests for SC-1 through SC-6: Write tests"
  source: "v3.3-requirements-spec.md:FR-6.1 (lines 394-399)"
  type: TEST
  priority: P0
  domain: "qa-gaps"
  cross_cutting: false
  related_reqs: ["SC-8"]

- id: "FR-6.1-T12"
  text: "v3.05 Gap T12 — Smoke test convergence path: Write test"
  source: "v3.3-requirements-spec.md:FR-6.1 (lines 394-399)"
  type: TEST
  priority: P0
  domain: "qa-gaps"
  cross_cutting: false
  related_reqs: ["SC-8"]

- id: "FR-6.1-T14"
  text: "v3.05 Gap T14 — Regenerate wiring-verification artifact + validate"
  source: "v3.3-requirements-spec.md:FR-6.1 (lines 394-399)"
  type: FUNCTIONAL
  priority: P1
  domain: "qa-gaps"
  cross_cutting: false
  related_reqs: ["SC-8"]

- id: "FR-6.2-T02"
  text: "v3.2 Gap T02 — run_post_phase_wiring_hook() call: Already verified WIRED — write confirming test"
  source: "v3.3-requirements-spec.md:FR-6.2 (lines 405-408)"
  type: TEST
  priority: P0
  domain: "qa-gaps"
  cross_cutting: false
  related_reqs: ["FR-1.7", "SC-8"]

- id: "FR-6.2-T17-T22"
  text: "v3.2 Gaps T17-T22 — Integration tests, regression suite, gap closure audit: Write tests per spec"
  source: "v3.3-requirements-spec.md:FR-6.2 (lines 405-408)"
  type: TEST
  priority: P0
  domain: "qa-gaps"
  cross_cutting: false
  related_reqs: ["SC-8"]

### FR-7: Audit Trail Infrastructure

- id: "FR-7.1"
  text: "Test Output Format — Each test writes a JSONL audit record to {results_dir}/audit-trail.jsonl with 9-field schema: test_id, spec_ref, timestamp, assertion_type, inputs, observed, expected, verdict, evidence"
  source: "v3.3-requirements-spec.md:FR-7.1 (lines 417-441)"
  type: FUNCTIONAL
  priority: P0
  domain: "audit-trail"
  cross_cutting: true
  related_reqs: ["FR-7.2", "FR-7.3", "SC-12"]

- id: "FR-7.2"
  text: "Audit Trail Properties — Third party must determine from audit trail alone: (1) were real tests run (timestamp, duration, actual observed values), (2) tests run according to spec (spec_ref traces to code location), (3) results are real (observed contains concrete runtime values), (4) pass/fail determination is sound (expected vs observed explicit)"
  source: "v3.3-requirements-spec.md:FR-7.2 (lines 444-451)"
  type: FUNCTIONAL
  priority: P0
  domain: "audit-trail"
  cross_cutting: true
  related_reqs: ["FR-7.1", "SC-12"]

- id: "FR-7.2-PROP1"
  text: "Audit trail property: Were real tests run? — Timestamp, test duration, actual observed values (not static fixtures)"
  source: "v3.3-requirements-spec.md:FR-7.2 property 1"
  type: ACCEPTANCE_CRITERION
  priority: P0
  domain: "audit-trail"
  cross_cutting: false
  related_reqs: ["FR-7.2"]

- id: "FR-7.2-PROP2"
  text: "Audit trail property: Were tests run according to spec? — spec_ref traces to code location, inputs show configuration"
  source: "v3.3-requirements-spec.md:FR-7.2 property 2"
  type: ACCEPTANCE_CRITERION
  priority: P0
  domain: "audit-trail"
  cross_cutting: false
  related_reqs: ["FR-7.2"]

- id: "FR-7.2-PROP3"
  text: "Audit trail property: Are results real? — observed contains concrete runtime values, evidence describes what was checked"
  source: "v3.3-requirements-spec.md:FR-7.2 property 3"
  type: ACCEPTANCE_CRITERION
  priority: P0
  domain: "audit-trail"
  cross_cutting: false
  related_reqs: ["FR-7.2"]

- id: "FR-7.2-PROP4"
  text: "Audit trail property: Pass/fail determination is sound — expected vs observed comparison is explicit"
  source: "v3.3-requirements-spec.md:FR-7.2 property 4"
  type: ACCEPTANCE_CRITERION
  priority: P0
  domain: "audit-trail"
  cross_cutting: false
  related_reqs: ["FR-7.2"]

- id: "FR-7.3"
  text: "Audit Trail Runner — pytest fixture (audit_trail): opens audit-trail.jsonl in results directory, provides record(test_id, spec_ref, inputs, observed, expected, verdict, evidence) method, auto-flushes after each test, produces summary report at session end: total tests, passed, failed, coverage of wiring points"
  source: "v3.3-requirements-spec.md:FR-7.3 (lines 453-458)"
  type: FUNCTIONAL
  priority: P0
  domain: "audit-trail"
  cross_cutting: true
  related_reqs: ["FR-7.1", "FR-7.2"]

---

## Non-Functional Requirements

- id: "NFR-1"
  text: "Tests MUST NOT mock gate functions or core orchestration logic. _subprocess_factory injection acceptable for external binary replacement only"
  source: "v3.3-requirements-spec.md:FR-1 constraint (lines 77-78), Constraints section (line 614)"
  type: CONSTRAINT
  priority: P0
  domain: "testing-constraints"
  cross_cutting: true
  related_reqs: ["FR-1-CONSTRAINT"]

- id: "NFR-2"
  text: "UV only — uv run pytest, not python -m pytest"
  source: "v3.3-requirements-spec.md:Constraints (line 613)"
  type: CONSTRAINT
  priority: P0
  domain: "testing-constraints"
  cross_cutting: true
  related_reqs: []

- id: "NFR-3"
  text: "Baseline: ≥4894 passed, ≤3 pre-existing failures, 0 regressions"
  source: "v3.3-requirements-spec.md:Constraints (line 7, 616), Success Criteria SC-4"
  type: NON_FUNCTIONAL
  priority: P0
  domain: "testing-constraints"
  cross_cutting: true
  related_reqs: ["SC-4"]

- id: "NFR-4"
  text: "Audit trail: Every test must emit a JSONL record"
  source: "v3.3-requirements-spec.md:Constraints (line 617)"
  type: CONSTRAINT
  priority: P0
  domain: "audit-trail"
  cross_cutting: true
  related_reqs: ["FR-7.1", "FR-7.3"]

- id: "NFR-5"
  text: "Spec-driven manifest: Wiring manifest is the source of truth for reachability gate"
  source: "v3.3-requirements-spec.md:Constraints (line 618)"
  type: CONSTRAINT
  priority: P0
  domain: "reachability"
  cross_cutting: false
  related_reqs: ["FR-4.1"]

- id: "NFR-6"
  text: "Documented limitations in AST analyzer module docstring: dynamic dispatch false negatives, TYPE_CHECKING exclusion, lazy imports included"
  source: "v3.3-requirements-spec.md:FR-4.2 (lines 338-341)"
  type: CONSTRAINT
  priority: P1
  domain: "reachability"
  cross_cutting: false
  related_reqs: ["FR-4.2-LIM1", "FR-4.2-LIM2", "FR-4.2-LIM3"]

---

## Success Criteria

- id: "SC-1"
  text: "All 20+ wiring points have ≥1 E2E test — Test count ≥ 20, mapped to FR-1"
  source: "v3.3-requirements-spec.md:Success Criteria (line 513)"
  type: SUCCESS_CRITERION
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-1.1" through "FR-1.18"]

- id: "SC-2"
  text: "TurnLedger lifecycle covered for all 4 paths — Convergence, per-task, per-phase, cross-path"
  source: "v3.3-requirements-spec.md:Success Criteria (line 514)"
  type: SUCCESS_CRITERION
  priority: P0
  domain: "turnledger-lifecycle"
  cross_cutting: false
  related_reqs: ["FR-2.1", "FR-2.2", "FR-2.3", "FR-2.4"]

- id: "SC-3"
  text: "Gate rollout modes covered (off/shadow/soft/full) — 4 modes × 2 paths = 8+ scenarios"
  source: "v3.3-requirements-spec.md:Success Criteria (line 515)"
  type: SUCCESS_CRITERION
  priority: P0
  domain: "gate-modes"
  cross_cutting: false
  related_reqs: ["FR-3.1a", "FR-3.1b", "FR-3.1c", "FR-3.1d"]

- id: "SC-4"
  text: "Zero regressions from baseline — ≥4894 passed, ≤3 pre-existing failures"
  source: "v3.3-requirements-spec.md:Success Criteria (line 516)"
  type: SUCCESS_CRITERION
  priority: P0
  domain: "testing-constraints"
  cross_cutting: true
  related_reqs: ["NFR-3"]

- id: "SC-5"
  text: "KPI report accuracy validated — Integration test proves field values match"
  source: "v3.3-requirements-spec.md:Success Criteria (line 517)"
  type: SUCCESS_CRITERION
  priority: P0
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-1.11"]

- id: "SC-6"
  text: "Budget exhaustion paths validated — 4 exhaustion scenarios tested"
  source: "v3.3-requirements-spec.md:Success Criteria (line 518)"
  type: SUCCESS_CRITERION
  priority: P0
  domain: "gate-modes"
  cross_cutting: false
  related_reqs: ["FR-3.2a", "FR-3.2b", "FR-3.2c", "FR-3.2d"]

- id: "SC-7"
  text: "Eval framework catches known-bad state — Regression test: break wiring → detected"
  source: "v3.3-requirements-spec.md:Success Criteria (line 519)"
  type: SUCCESS_CRITERION
  priority: P0
  domain: "reachability"
  cross_cutting: false
  related_reqs: ["FR-4.4"]

- id: "SC-8"
  text: "Remaining QA gaps closed — v3.05 T07/T11/T12/T14, v3.2 T02/T17-T22"
  source: "v3.3-requirements-spec.md:Success Criteria (line 520)"
  type: SUCCESS_CRITERION
  priority: P0
  domain: "qa-gaps"
  cross_cutting: false
  related_reqs: ["FR-6.1-T07", "FR-6.1-T11", "FR-6.1-T12", "FR-6.1-T14", "FR-6.2-T02", "FR-6.2-T17-T22"]

- id: "SC-9"
  text: "Reachability gate catches unreachable code — Hybrid A+D detects intentionally broken wiring"
  source: "v3.3-requirements-spec.md:Success Criteria (line 521)"
  type: SUCCESS_CRITERION
  priority: P0
  domain: "reachability"
  cross_cutting: false
  related_reqs: ["FR-4.4"]

- id: "SC-10"
  text: "0-files-analyzed produces FAIL — Assertion added, test proves it"
  source: "v3.3-requirements-spec.md:Success Criteria (line 522)"
  type: SUCCESS_CRITERION
  priority: P0
  domain: "pipeline-fixes"
  cross_cutting: false
  related_reqs: ["FR-5.1"]

- id: "SC-11"
  text: "Impl-vs-spec fidelity check exists — New checker finds and flags missing implementations"
  source: "v3.3-requirements-spec.md:Success Criteria (line 523)"
  type: SUCCESS_CRITERION
  priority: P0
  domain: "pipeline-fixes"
  cross_cutting: false
  related_reqs: ["FR-5.2"]

- id: "SC-12"
  text: "Audit trail is third-party verifiable — JSONL output with all 4 verification properties"
  source: "v3.3-requirements-spec.md:Success Criteria (line 524)"
  type: SUCCESS_CRITERION
  priority: P0
  domain: "audit-trail"
  cross_cutting: true
  related_reqs: ["FR-7.1", "FR-7.2", "FR-7.3"]

---

## Scope / Exclusion Requirements

- id: "SCOPE-OUT-1"
  text: "Pipeline Weakness #1 (source_dir targeting): Already fixed — OUT OF SCOPE"
  source: "v3.3-requirements-spec.md:Out of Scope (line 64)"
  type: CONSTRAINT
  priority: P3
  domain: "scope"
  cross_cutting: false
  related_reqs: []

- id: "SCOPE-OUT-2"
  text: "Pipeline Weakness #5 (convergence disables spec-fidelity): Deferred to v3.4"
  source: "v3.3-requirements-spec.md:Out of Scope (line 65)"
  type: CONSTRAINT
  priority: P3
  domain: "scope"
  cross_cutting: false
  related_reqs: []

- id: "SCOPE-OUT-3"
  text: "Production code modifications beyond pipeline fixes #2/#3/#4: OUT OF SCOPE"
  source: "v3.3-requirements-spec.md:Out of Scope (line 66)"
  type: CONSTRAINT
  priority: P3
  domain: "scope"
  cross_cutting: false
  related_reqs: []

- id: "SCOPE-OUT-4"
  text: "attempt_remediation() full integration: noted as v3.3 deferral in code"
  source: "v3.3-requirements-spec.md:Out of Scope (line 67)"
  type: CONSTRAINT
  priority: P3
  domain: "scope"
  cross_cutting: false
  related_reqs: []

- id: "SCOPE-OUT-5"
  text: "Runtime instrumentation: rejected in favor of static analysis"
  source: "v3.3-requirements-spec.md:Out of Scope (line 68)"
  type: CONSTRAINT
  priority: P3
  domain: "scope"
  cross_cutting: false
  related_reqs: []

---

## Risk Requirements

- id: "RISK-1"
  text: "AST analyzer can't resolve lazy imports — Severity HIGH. Mitigation: Explicitly handle 'from X import Y' inside function bodies; test against known lazy imports in executor.py"
  source: "v3.3-requirements-spec.md:Risk Assessment (lines 500-501)"
  type: RISK_MITIGATION
  priority: P0
  domain: "reachability"
  cross_cutting: false
  related_reqs: ["FR-4.2", "FR-4.2-LIM3"]

- id: "RISK-2"
  text: "E2E tests flaky due to subprocess timing — Severity MEDIUM. Mitigation: Use _subprocess_factory for deterministic execution"
  source: "v3.3-requirements-spec.md:Risk Assessment (lines 500-502)"
  type: RISK_MITIGATION
  priority: P1
  domain: "testing-constraints"
  cross_cutting: true
  related_reqs: ["NFR-1"]

- id: "RISK-3"
  text: "Impl-vs-spec checker has high false-positive rate — Severity MEDIUM. Mitigation: Start with exact function-name matching; iterate NLP in v3.4"
  source: "v3.3-requirements-spec.md:Risk Assessment (lines 500-503)"
  type: RISK_MITIGATION
  priority: P1
  domain: "pipeline-fixes"
  cross_cutting: false
  related_reqs: ["FR-5.2"]

- id: "RISK-4"
  text: "Audit trail JSONL grows unbounded — Severity LOW. Mitigation: One file per test run, rotated by timestamp"
  source: "v3.3-requirements-spec.md:Risk Assessment (lines 500-504)"
  type: RISK_MITIGATION
  priority: P2
  domain: "audit-trail"
  cross_cutting: false
  related_reqs: ["FR-7.1"]

- id: "RISK-5"
  text: "0-files-analyzed fix breaks existing tests — Severity LOW. Mitigation: Investigate 2 pre-existing wiring pipeline failures before patching"
  source: "v3.3-requirements-spec.md:Risk Assessment (lines 500-505)"
  type: RISK_MITIGATION
  priority: P1
  domain: "pipeline-fixes"
  cross_cutting: false
  related_reqs: ["FR-5.1"]

---

## Process / Sequencing Requirements

- id: "SEQ-1"
  text: "Phase 1 (Infrastructure) has no dependencies, can start immediately"
  source: "v3.3-requirements-spec.md:Phased Implementation (line 469)"
  type: SEQUENCING
  priority: P1
  domain: "sequencing"
  cross_cutting: true
  related_reqs: []

- id: "SEQ-2"
  text: "Phase 2 depends on Phase 1 — audit trail fixture must exist"
  source: "v3.3-requirements-spec.md:Phased Implementation (line 477)"
  type: SEQUENCING
  priority: P1
  domain: "sequencing"
  cross_cutting: true
  related_reqs: []

- id: "SEQ-3"
  text: "Phase 3 depends on Phase 1 (AST analyzer) and Phase 2 (establishes baseline)"
  source: "v3.3-requirements-spec.md:Phased Implementation (line 485)"
  type: SEQUENCING
  priority: P1
  domain: "sequencing"
  cross_cutting: true
  related_reqs: []

- id: "SEQ-4"
  text: "Phase 4 depends on Phases 1-3 complete"
  source: "v3.3-requirements-spec.md:Phased Implementation (line 492)"
  type: SEQUENCING
  priority: P1
  domain: "sequencing"
  cross_cutting: true
  related_reqs: []

---

## File Change Requirements

- id: "FILE-NEW-1"
  text: "New file: src/superclaude/cli/audit/reachability.py — AST-based reachability analyzer"
  source: "v3.3-requirements-spec.md:Test File Layout + FR-4.2"
  type: FUNCTIONAL
  priority: P0
  domain: "reachability"
  cross_cutting: false
  related_reqs: ["FR-4.2"]

- id: "FILE-NEW-2"
  text: "New file: src/superclaude/cli/roadmap/fidelity_checker.py — Impl-vs-spec checker"
  source: "v3.3-requirements-spec.md:FR-5.2"
  type: FUNCTIONAL
  priority: P0
  domain: "pipeline-fixes"
  cross_cutting: false
  related_reqs: ["FR-5.2"]

- id: "FILE-NEW-3"
  text: "New test directory: tests/v3.3/ with conftest.py, all FR test files"
  source: "v3.3-requirements-spec.md:Test File Layout (lines 592-607)"
  type: FUNCTIONAL
  priority: P0
  domain: "testing-constraints"
  cross_cutting: false
  related_reqs: []

- id: "FILE-MOD-1"
  text: "Modified: src/superclaude/cli/audit/wiring_gate.py — FR-5.1: 0-files-analyzed assertion"
  source: "v3.3-requirements-spec.md:FR-5.1"
  type: FUNCTIONAL
  priority: P0
  domain: "pipeline-fixes"
  cross_cutting: false
  related_reqs: ["FR-5.1"]

- id: "FILE-MOD-2"
  text: "Modified: src/superclaude/cli/roadmap/executor.py — FR-5.2: wire fidelity_checker into _run_checkers()"
  source: "v3.3-requirements-spec.md:FR-5.2"
  type: FUNCTIONAL
  priority: P0
  domain: "pipeline-fixes"
  cross_cutting: false
  related_reqs: ["FR-5.2"]

- id: "FILE-MOD-3"
  text: "Modified: tests/roadmap/test_convergence_wiring.py — FR-6.1 T07: extend/verify tests"
  source: "v3.3-requirements-spec.md:FR-6.1"
  type: FUNCTIONAL
  priority: P0
  domain: "qa-gaps"
  cross_cutting: false
  related_reqs: ["FR-6.1-T07"]

- id: "FILE-MOD-4"
  text: "Modified: tests/roadmap/test_convergence_e2e.py — FR-6.1 T11/T12: extend tests"
  source: "v3.3-requirements-spec.md:FR-6.1"
  type: FUNCTIONAL
  priority: P0
  domain: "qa-gaps"
  cross_cutting: false
  related_reqs: ["FR-6.1-T11", "FR-6.1-T12"]

---

## Open Questions / Architect Decisions

- id: "OQ-1"
  text: "Signal handling for FR-3.3 — Architect recommends: Test SIGINT only via os.kill(os.getpid(), signal.SIGINT)"
  source: "v3.3-requirements-spec.md:Open Questions (line 283)"
  type: DECISION
  priority: P1
  domain: "gate-modes"
  cross_cutting: false
  related_reqs: ["FR-3.3"]

- id: "OQ-2"
  text: "Impl-vs-spec checker granularity — Architect recommends: exact function-name or class-name match as minimum evidence"
  source: "v3.3-requirements-spec.md:Open Questions (line 284)"
  type: DECISION
  priority: P1
  domain: "pipeline-fixes"
  cross_cutting: false
  related_reqs: ["FR-5.2", "RISK-3"]

- id: "OQ-3"
  text: "Audit trail fixture scope — Architect recommends: Session-scoped, one JSONL per pytest invocation"
  source: "v3.3-requirements-spec.md:Open Questions (line 285)"
  type: DECISION
  priority: P1
  domain: "audit-trail"
  cross_cutting: false
  related_reqs: ["FR-7.3"]

- id: "OQ-4"
  text: "Wiring manifest location — Architect recommends: standalone YAML at tests/v3.3/wiring_manifest.yaml"
  source: "v3.3-requirements-spec.md:Open Questions (line 286)"
  type: DECISION
  priority: P1
  domain: "reachability"
  cross_cutting: false
  related_reqs: ["FR-4.1"]

- id: "OQ-5"
  text: "attempt_remediation() boundary — v3.3 tests FR-1.14 (internal _recheck_wiring()). Full integration test deferred to v3.4"
  source: "v3.3-requirements-spec.md:Open Questions (line 287)"
  type: DECISION
  priority: P1
  domain: "wiring-e2e"
  cross_cutting: false
  related_reqs: ["FR-1.14", "SCOPE-OUT-4"]

- id: "OQ-6"
  text: "Checkpoint frequency for FR-2.4 — Architect recommends: Assert available() invariant after each phase completion"
  source: "v3.3-requirements-spec.md:Open Questions (line 288)"
  type: DECISION
  priority: P1
  domain: "turnledger-lifecycle"
  cross_cutting: false
  related_reqs: ["FR-2.4"]

- id: "OQ-7"
  text: "Pre-existing 3 failures — Architect recommends: Investigate before Phase 3, document them, FR-5.1 fix may reduce to 1"
  source: "v3.3-requirements-spec.md:Open Questions (line 289)"
  type: DECISION
  priority: P1
  domain: "testing-constraints"
  cross_cutting: false
  related_reqs: ["NFR-3", "RISK-5"]

- id: "OQ-8"
  text: "Reachability gate CI placement — Architect recommends: Include in standard uv run pytest via tests/v3.3/test_reachability_eval.py"
  source: "v3.3-requirements-spec.md:Open Questions (line 290)"
  type: DECISION
  priority: P1
  domain: "reachability"
  cross_cutting: false
  related_reqs: ["FR-4.3"]

---

## Summary Statistics

| Category | Count |
|----------|-------|
| Functional Requirements (FR-*) | 42 |
| Non-Functional Requirements (NFR-*) | 6 |
| Success Criteria (SC-*) | 12 |
| Scope Exclusions (SCOPE-OUT-*) | 5 |
| Risk Mitigations (RISK-*) | 5 |
| Sequencing Constraints (SEQ-*) | 4 |
| File Change Requirements (FILE-*) | 7 |
| Open Questions / Decisions (OQ-*) | 8 |
| **TOTAL** | **89** |
