---
spec_source: v3.3-requirements-spec.md
generated: "2026-03-23T00:00:00Z"
generator: requirements-extraction-agent-opus-4.6
functional_requirements: 7
nonfunctional_requirements: 6
total_requirements: 13
complexity_score: 0.82
complexity_class: HIGH
domains_detected: [backend, testing, static-analysis, pipeline, audit]
risks_identified: 5
dependencies_identified: 8
success_criteria_count: 12
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 109.0, started_at: "2026-03-23T03:08:27.917860+00:00", finished_at: "2026-03-23T03:10:16.936323+00:00"}
---

## Functional Requirements

### FR-1: E2E Test Coverage for Wiring Points

**Goal**: Every wiring point from the brainstorm test matrix has at least one E2E test exercising real production code paths.

**Constraint**: Tests MUST NOT mock gate functions or core orchestration logic. Only `_subprocess_factory` injection (replacing external `claude` binary) is acceptable.

| Sub-ID | Description | Spec Reference |
|--------|-------------|----------------|
| FR-1.1 | TurnLedger construction validation — assert `initial_budget`, `reimbursement_rate`, constructed before phase loop | executor.py:1127-1130 |
| FR-1.2 | ShadowGateMetrics construction — assert constructed before phase loop | executor.py:1132 |
| FR-1.3 | DeferredRemediationLog construction — assert `persist_path` under `results_dir` | executor.py:1133-1137 |
| FR-1.4 | SprintGatePolicy construction — assert receives correct config | executor.py:1139 |
| FR-1.5 | Phase delegation — task inventory path: phase with `### T01.01` headings triggers `execute_phase_tasks()` | executor.py:1183-1191 |
| FR-1.6 | Phase delegation — freeform fallback: phase without task headings triggers ClaudeProcess | executor.py:1210+ |
| FR-1.7 | Post-phase wiring hook fires on both per-task (1199-1204) and per-phase/ClaudeProcess (1407-1412) paths | executor.py:1199-1204, 1407-1412 |
| FR-1.8 | Anti-instinct hook returns `tuple[TaskResult, TrailingGateResult \| None]`, not bare `TaskResult` | executor.py:787-793 |
| FR-1.9 | Gate result accumulation — `all_gate_results` contains results from ALL phases (mixed types) | executor.py:1141, 1191 |
| FR-1.10 | Failed gate → remediation log: failing gate in `full` mode appends to `remediation_log` | executor.py:1016-1018, 619-645 |
| FR-1.11 | KPI report generation — `build_kpi_report()` called with correct args, file written, includes wiring KPI fields | executor.py:1486-1493, kpi.py:110-144 |
| FR-1.12 | Wiring mode resolution — `_resolve_wiring_mode()` called, not `config.wiring_gate_mode` directly | executor.py:421-447, 475 |
| FR-1.13 | Shadow findings → remediation log: shadow mode creates synthetic `TrailingGateResult` with `[shadow]` prefix | executor.py:619-645 |
| FR-1.14 | BLOCKING remediation lifecycle: format → debit → recheck → restore/fail | executor.py:554-608 |
| FR-1.14a | `_format_wiring_failure()` produces non-empty prompt | executor.py:653-696 |
| FR-1.14b | `ledger.debit(config.remediation_cost)` called | executor.py:554-608 |
| FR-1.14c | `_recheck_wiring()` called; pass → status restored, fail → status FAIL | executor.py:704-727 |
| FR-1.15 | Convergence registry receives exactly 3 positional args: `(path, release_id, spec_hash)` | convergence.py:101, executor.py:567-571 |
| FR-1.16 | `registry.merge_findings()` receives `(structural_list, semantic_list, run_number)` — 3 args | convergence.py:144-148, executor.py:597 |
| FR-1.17 | `_run_remediation()` converts dicts to `Finding` objects without `AttributeError` | executor.py:613-633 |
| FR-1.18 | `TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET)` uses 61, not 46 | convergence.py:33, executor.py:577-578 |

---

### FR-2: TurnLedger Lifecycle Integration Tests

**Goal**: Prove full debit/credit/reimbursement cycle flows through production for all 4 paths.

| Sub-ID | Description | Key Assertions |
|--------|-------------|----------------|
| FR-2.1 | Convergence path (v3.05) — `execute_fidelity_with_convergence()` E2E | debit CHECKER_COST → run checkers → credit CONVERGENCE_PASS_CREDIT → reimburse_for_progress(); budget_snapshot recorded; budget logging correct |
| FR-2.2 | Sprint per-task path (v3.1) — `execute_sprint()` → `execute_phase_tasks()` | pre-debit minimum_allocation → subprocess → reconcile actual vs pre-allocated; post-task hooks fire with ledger |
| FR-2.3 | Sprint per-phase path (v3.2) — `execute_sprint()` → ClaudeProcess fallback | `debit_wiring()` → analysis → `credit_wiring()` on non-blocking; `wiring_analyses_count` incremented |
| FR-2.4 | Cross-path coherence — mixed task-inventory + freeform phases | Ledger coherent after both paths; `available() = initial_budget - consumed + reimbursed` at every checkpoint |

---

### FR-3: Gate Rollout Mode Scenarios

**Goal**: Every gate rollout mode tested for both execution paths.

| Sub-ID | Description |
|--------|-------------|
| FR-3.1a | Mode `off`: anti-instinct evaluates + ignores; wiring skips analysis |
| FR-3.1b | Mode `shadow`: anti-instinct evaluates + records; wiring analyzes + logs + credits back |
| FR-3.1c | Mode `soft`: anti-instinct evaluates + records + credit/remediate; wiring warns critical + credits back |
| FR-3.1d | Mode `full`: anti-instinct evaluates + records + credit/remediate + FAIL; wiring blocks critical+major + remediates |

Each mode must verify: correct `TaskStatus`/`GateOutcome`, correct `TurnLedger` state, correct `DeferredRemediationLog` entries, correct `ShadowGateMetrics` recording.

| Sub-ID | Budget Exhaustion Scenario | Expected Behavior |
|--------|---------------------------|-------------------|
| FR-3.2a | Budget exhausted before task launch | Task SKIPPED, remaining tasks listed |
| FR-3.2b | Budget exhausted before wiring analysis | Wiring hook skipped, status unchanged |
| FR-3.2c | Budget exhausted before remediation | FAIL persists, BUDGET_EXHAUSTED logged |
| FR-3.2d | Budget exhausted mid-convergence | Halt with diagnostic, run_count < max_runs |

| Sub-ID | Description |
|--------|-------------|
| FR-3.3 | Interrupted sprint: signal interrupt mid-execution → KPI report still written, remediation log persisted, outcome = INTERRUPTED |

---

### FR-4: Reachability Eval Framework (Hybrid A+D)

**Goal**: Static analysis tool detecting components built but unreachable from entry points.

| Sub-ID | Description |
|--------|-------------|
| FR-4.1 | Spec-driven wiring manifest: YAML schema declaring entry points and required reachable targets with spec references |
| FR-4.2 | AST call-chain analyzer: `ast.parse()` → call graph → BFS/DFS reachability from entry point; cross-module import resolution; handles lazy imports inside functions; documents limitations (dynamic dispatch, `TYPE_CHECKING`) |
| FR-4.3 | Reachability gate integration: reads manifest, runs AST analysis, produces structured PASS/FAIL report, integrates with `GateCriteria` infrastructure |
| FR-4.4 | Regression test: remove `run_post_phase_wiring_hook()` call → gate detects gap referencing v3.2-T02 |

---

### FR-5: Pipeline Fixes

| Sub-ID | Description | Production Change |
|--------|-------------|-------------------|
| FR-5.1 | 0-files-analyzed assertion (Weakness #3): if `files_analyzed == 0` AND source dir non-empty → return FAIL, not silent PASS; include `failure_reason` | wiring_gate.py:673+ |
| FR-5.2 | Impl-vs-spec fidelity check (Weakness #4): new checker reads spec FRs, searches implementation for evidence, reports gaps; integrates into `_run_checkers()` | New checker module |
| FR-5.3 | Reachability gate (Weakness #2): cross-ref to FR-4 | See FR-4 |

---

### FR-6: Remaining QA Gaps

#### FR-6.1: v3.05 Gaps

| Gap ID | Description | Action |
|--------|-------------|--------|
| T07 | `tests/roadmap/test_convergence_wiring.py` — 7 tests | Write tests |
| T11 | `tests/roadmap/test_convergence_e2e.py` — 6 tests (SC-1 through SC-6) | Write tests |
| T12 | Smoke test convergence path | Write test |
| T14 | Regenerate wiring-verification artifact | Generate + validate |

#### FR-6.2: v3.2 Gaps

| Gap ID | Description | Action |
|--------|-------------|--------|
| T02 | `run_post_phase_wiring_hook()` — already verified WIRED | Write confirming test |
| T17-T22 | Integration tests, regression suite, gap closure audit | Write tests per spec |

---

### FR-7: Audit Trail Infrastructure

| Sub-ID | Description |
|--------|-------------|
| FR-7.1 | JSONL audit record per test: `test_id`, `spec_ref`, `timestamp`, `assertion_type`, `inputs`, `observed`, `expected`, `verdict`, `evidence` |
| FR-7.2 | Third-party verifiability: real tests run (timestamps, durations, actual values), spec-traced, concrete runtime observations, explicit pass/fail determination |
| FR-7.3 | Pytest `audit_trail` fixture: opens JSONL, provides `record()` method, auto-flushes, produces summary report (total/passed/failed/wiring coverage) |

---

## Non-Functional Requirements

### NFR-1: No Mocking of Internal Logic

Tests MUST NOT mock gate functions or core orchestration logic. Only `_subprocess_factory` injection (replacing the external `claude` binary) is permitted. This ensures tests exercise real production code paths.

### NFR-2: UV-Only Python Environment

All Python operations must use UV (`uv run pytest`, `uv pip install`). Never use `python -m`, bare `pip`, or `python script.py` directly.

### NFR-3: Zero Regression Baseline

Test suite must maintain baseline: ≥4894 passed, ≤3 pre-existing failures, 0 new regressions introduced by v3.3 changes.

### NFR-4: Audit Trail Completeness

Every test must emit a JSONL audit record. The audit trail must be independently verifiable by a third party with no prior project knowledge.

### NFR-5: Spec-Driven Manifest as Source of Truth

The wiring manifest YAML is the authoritative source for reachability gate validation. Any wiring point not in the manifest is not checked; any point in the manifest MUST be reachable.

### NFR-6: AST Analyzer Documented Limitations

The AST call-chain analyzer must explicitly document its limitations: dynamic dispatch (`getattr`, `**kwargs`) produces false negatives; `TYPE_CHECKING` conditionals excluded; lazy imports inside functions ARE included.

---

## Complexity Assessment

**Score**: 0.82 — **HIGH**

**Rationale**:

| Factor | Score | Justification |
|--------|-------|---------------|
| Scope breadth | 0.85 | 7 top-level FRs spanning E2E tests, lifecycle integration, mode matrices, static analysis tooling, pipeline fixes, QA gaps, and audit infrastructure |
| Cross-component coupling | 0.80 | Tests span executor, models, convergence, kpi, wiring_gate, and a new AST analyzer module; 4 distinct execution paths must be validated |
| Novel tooling | 0.85 | FR-4 requires building an AST-based reachability analyzer from scratch with cross-module import resolution |
| Test volume | 0.75 | 50+ individual test scenarios across 6 test files plus 2 existing test files to extend |
| Production code changes | 0.70 | Limited to 2 pipeline fixes (FR-5.1, FR-5.2) plus reachability gate integration (FR-4.3) |
| Verification complexity | 0.90 | Audit trail must be third-party verifiable; success criteria require cross-validation against spec |
| Phased dependencies | 0.75 | 4 sequential phases with hard dependencies; Phase 2 blocked on Phase 1, Phase 3 on Phase 1, Phase 4 on all |

---

## Architectural Constraints

1. **Branch constraint**: Must branch from `v3.0-v3.2-Fidelity`
2. **No production code modifications** beyond pipeline fixes FR-5.1, FR-5.2, and FR-4.3 reachability gate integration
3. **`_subprocess_factory` is the only acceptable injection point** — all other internal logic must run as-is
4. **Test file layout prescribed**: `tests/v3.3/` directory with specific file names; `tests/roadmap/` for convergence tests; `tests/audit-trail/` for JSONL writer
5. **JSONL audit format**: Fixed schema with 8 required fields per record
6. **Wiring manifest YAML format**: Fixed schema with `entry_points` and `required_reachable` sections
7. **AST analyzer must be a standalone module** (implied by Phase 1 independence and `test_reachability_eval.py` testing it in isolation)
8. **Impl-vs-spec fidelity checker integrates into `_run_checkers()`** alongside existing structural and semantic layers
9. **`MAX_CONVERGENCE_BUDGET = 61`** — hardcoded constant, not configurable
10. **Pipeline outputs go to `results_dir`** — audit trail JSONL, KPI report, remediation log all written there

---

## Risk Inventory

1. **R-1 (HIGH)**: AST analyzer can't resolve lazy imports — Dynamic dispatch and `getattr` calls produce false negatives in reachability analysis. **Mitigation**: Explicitly handle `from X import Y` inside function bodies; maintain test coverage against known lazy imports in executor.py.

2. **R-2 (MEDIUM)**: E2E tests flaky due to subprocess timing — Real subprocess invocations introduce non-deterministic timing. **Mitigation**: Use `_subprocess_factory` for deterministic execution; reserve real subprocess tests for a separate smoke suite.

3. **R-3 (MEDIUM)**: Impl-vs-spec checker has high false-positive rate — Simple function-name matching may miss renamed or refactored implementations. **Mitigation**: Start with exact function-name matching; defer NLP-based matching to v3.4.

4. **R-4 (LOW)**: Audit trail JSONL grows unbounded — Continuous test runs accumulate large files. **Mitigation**: One file per test run, rotated by timestamp.

5. **R-5 (LOW)**: 0-files-analyzed fix breaks existing tests — The 2 pre-existing wiring pipeline failures may be related to this behavior. **Mitigation**: Investigate pre-existing failures before patching; ensure fix is additive, not breaking.

---

## Dependency Inventory

1. **`ast` module (stdlib)** — Python standard library AST parser for FR-4.2 reachability analyzer
2. **`pytest` (>=7.0.0)** — Test framework; fixture infrastructure for `audit_trail` (FR-7.3)
3. **`_subprocess_factory` injection point** — Existing test infrastructure in `execute_phase_tasks()` for replacing external `claude` binary
4. **`GateCriteria` infrastructure** — Existing gate framework that FR-4.3 reachability gate must integrate with
5. **`_run_checkers()` hook** — Existing checker orchestration in convergence that FR-5.2 impl-vs-spec checker plugs into
6. **`wiring_gate.py:run_wiring_analysis()`** — Existing function modified by FR-5.1 (0-files-analyzed assertion)
7. **`v3.0-v3.2-Fidelity` branch** — Required base branch; all verified constructs in code state snapshot must be present
8. **JSONL format** — Standard newline-delimited JSON; no external library needed but implies structured schema contract

---

## Success Criteria

| ID | Criterion | Metric | Acceptance Threshold | Phase |
|----|-----------|--------|---------------------|-------|
| SC-1 | All 20+ wiring points have ≥1 E2E test | Count of tests mapped to FR-1 sub-IDs | ≥ 20 tests | 2 |
| SC-2 | TurnLedger lifecycle covered for all 4 paths | Convergence, per-task, per-phase, cross-path suites pass | 4/4 paths green | 2 |
| SC-3 | Gate rollout modes covered (off/shadow/soft/full) | 4 modes × 2 paths | ≥ 8 scenarios passing | 2 |
| SC-4 | Zero regressions from baseline | Full suite pass count | ≥ 4894 passed, ≤ 3 pre-existing failures | 4 |
| SC-5 | KPI report accuracy validated | Integration test field-value comparison | All wiring KPI fields match expected | 2 |
| SC-6 | Budget exhaustion paths validated | 4 exhaustion scenarios | 4/4 scenarios passing | 2 |
| SC-7 | Eval framework catches known-bad state | Regression test: break wiring → detected | 1/1 detection | 3 |
| SC-8 | Remaining QA gaps closed | v3.05 T07/T11/T12/T14, v3.2 T02/T17-T22 | All gap tests passing | 2 |
| SC-9 | Reachability gate catches unreachable code | Hybrid A+D on intentionally broken wiring | Detection with correct spec ref | 3 |
| SC-10 | 0-files-analyzed produces FAIL | Assertion test on empty directory | FAIL returned, not silent PASS | 3 |
| SC-11 | Impl-vs-spec fidelity check exists | New checker finds/flags missing implementations | 1+ gap detected in synthetic test | 3 |
| SC-12 | Audit trail is third-party verifiable | JSONL output meets all 4 verification properties (FR-7.2) | Manual review confirms | 2 |

---

## Open Questions

1. **Signal handling for FR-3.3 (Interrupted Sprint)**: Which signal(s) must be handled — `SIGINT` only, or also `SIGTERM`/`SIGHUP`? The spec says "simulate signal interrupt" but doesn't specify which signal or the mechanism for simulation in tests.

2. **Impl-vs-spec checker granularity (FR-5.2)**: The spec says "searches implementation codebase for evidence of implementation (function names, class names, docstring references)." What constitutes sufficient evidence? A matching function name? A docstring citing the FR ID? This directly impacts false-positive rate (R-3).

3. **Audit trail fixture scope (FR-7.3)**: Should the `audit_trail` fixture be session-scoped (one file per `pytest` invocation) or function-scoped (allowing per-test customization)? The spec implies session-scoped ("Opens... in the results directory", "summary report at session end") but doesn't explicitly state it.

4. **Wiring manifest location**: FR-4.1 declares the manifest schema but doesn't specify where the YAML file lives at runtime. Is it embedded in the release spec markdown, a standalone `.yaml` file in the release directory, or loaded from a Python constant?

5. **`attempt_remediation()` boundary**: The spec notes "attempt_remediation() full integration" is deferred to v3.3 deferral. But FR-1.14 tests the BLOCKING remediation lifecycle which calls `_recheck_wiring()`. What is the exact boundary between what v3.3 tests and what is deferred? Is `_recheck_wiring()` the same as or different from `attempt_remediation()`?

6. **Cross-path coherence checkpoint frequency (FR-2.4)**: The spec says "available() = initial_budget - consumed + reimbursed holds at every checkpoint." What defines a checkpoint — after each phase, after each task, or after each hook invocation?

7. **Pre-existing 3 failures identity**: The baseline states "3 pre-existing failures." Are these documented? R-5 notes the 0-files-analyzed fix may be related to "2 pre-existing wiring pipeline failures" — are these part of the 3, and what is the third?

8. **Reachability gate CI integration**: FR-4.3 says the gate integrates with `GateCriteria` infrastructure, but should it also run as part of the standard `uv run pytest` suite, or only in the pipeline? This affects test file placement and fixture dependencies.
