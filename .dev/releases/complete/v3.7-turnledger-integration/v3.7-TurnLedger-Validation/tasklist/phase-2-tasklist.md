# Phase 2 -- Core E2E Test Suites

Write all E2E tests covering wiring points (FR-1), TurnLedger lifecycle (FR-2), gate rollout modes (FR-3), and remaining QA gaps (FR-6). This is the largest phase by volume (~57 tests). All tests must use `_subprocess_factory` injection and emit JSONL audit records via the `audit_trail` fixture from Phase 1.

---

### T02.01 -- Write 4 construction validation E2E tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-010 |
| Why | Validate that `TurnLedger`, `ShadowGateMetrics`, `DeferredRemediationLog`, and `SprintGatePolicy` construct correctly in real orchestration context (FR-1.1-FR-1.4) |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0009 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0009/spec.md`

**Deliverables:**
- 4 tests in `tests/v3.3/test_wiring_points_e2e.py`: construction validation for `TurnLedger`, `ShadowGateMetrics`, `DeferredRemediationLog`, `SprintGatePolicy`

**Steps:**
1. **[PLANNING]** Identify constructor signatures for all 4 classes from production code
2. **[PLANNING]** Determine required `_subprocess_factory` setup for each construction context
3. **[EXECUTION]** Create `tests/v3.3/test_wiring_points_e2e.py` with test class and shared fixtures
4. **[EXECUTION]** Write 4 tests: each constructs one class via real orchestration path, asserts instance type and required attributes
5. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_wiring_points_e2e.py::TestConstructionValidation -v`
6. **[COMPLETION]** All 4 tests emit JSONL audit records with `spec_ref` mapped to FR-1.1 through FR-1.4

**Acceptance Criteria:**
- 4 tests exist in `tests/v3.3/test_wiring_points_e2e.py` covering FR-1.1 through FR-1.4
- Each test constructs its target class via real orchestration (no direct constructor calls with mocked dependencies); includes specific assertions: `ledger.initial_budget` and `ledger.reimbursement_rate` for TurnLedger (FR-1.1), `persist_path` under `results_dir` for DeferredRemediationLog (FR-1.3)
- All tests use `_subprocess_factory` as the sole injection point
- All tests emit JSONL audit records via `audit_trail` fixture

**Validation:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py::TestConstructionValidation -v`
- Evidence: test output log and JSONL audit records

**Dependencies:** T01.02 (audit_trail fixture)
**Rollback:** Remove construction validation tests from test file

---

### T02.02 -- Write 2 phase delegation E2E tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011 |
| Why | Validate task-inventory path vs freeform fallback delegation and `_parse_phase_tasks()` return type (FR-1.5-FR-1.6) |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0010 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0010/spec.md`

**Deliverables:**
- 2 tests in `tests/v3.3/test_wiring_points_e2e.py`: task-inventory path delegation and freeform fallback; assert `_parse_phase_tasks()` return type is `list[TaskEntry] | None`

**Steps:**
1. **[PLANNING]** Identify the branching condition between task-inventory and freeform paths in executor
2. **[PLANNING]** Prepare phase configs: one with `### T01.01` headings (task-inventory), one without (freeform)
3. **[EXECUTION]** Write `test_task_inventory_path_delegation`: phase with task headings -> `execute_phase_tasks()` path
4. **[EXECUTION]** Write `test_freeform_fallback_delegation`: phase without task headings -> `ClaudeProcess` fallback path; assert `_parse_phase_tasks()` returns `list[TaskEntry] | None`
5. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "delegation" -v`
6. **[COMPLETION]** Emit audit records with spec_ref FR-1.5, FR-1.6

**Acceptance Criteria:**
- 2 tests exist covering task-inventory and freeform delegation paths
- `_parse_phase_tasks()` return type asserted as `list[TaskEntry] | None` in at least one test
- Tests use `_subprocess_factory` injection; no mocks on executor internals
- Both tests emit JSONL audit records

**Validation:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "delegation" -v`
- Evidence: test output log

**Dependencies:** T01.02
**Rollback:** Remove delegation tests

---

### T02.03 -- Write 2 post-phase wiring hook E2E tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-012 |
| Why | Prove `run_post_phase_wiring_hook()` fires on both per-task and per-phase/ClaudeProcess paths (FR-1.7) |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0011 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0011/spec.md`

**Deliverables:**
- 2 tests in `tests/v3.3/test_wiring_points_e2e.py`: post-phase wiring hook fires on per-task path and per-phase/ClaudeProcess path

**Steps:**
1. **[PLANNING]** Identify the two call sites for `run_post_phase_wiring_hook()` in executor
2. **[PLANNING]** Design assertions: hook invoked with correct arguments on each path
3. **[EXECUTION]** Write `test_post_phase_hook_per_task_path`: task-inventory execution -> hook fires with phase results
4. **[EXECUTION]** Write `test_post_phase_hook_claude_process_path`: freeform execution -> hook fires with ClaudeProcess results
5. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "post_phase_hook" -v`
6. **[COMPLETION]** Emit audit records with spec_ref FR-1.7

**Acceptance Criteria:**
- 2 tests prove hook fires on both per-task and per-phase/ClaudeProcess paths
- Assertions verify hook is called (not just that code path executes without error)
- Tests use `_subprocess_factory` injection only
- Both tests emit JSONL audit records

**Validation:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "post_phase_hook" -v`
- Evidence: test output log

**Dependencies:** T01.02
**Rollback:** Remove hook tests

---

### T02.04 -- Write 1 anti-instinct hook return type test

| Field | Value |
|---|---|
| Roadmap Item IDs | R-013 |
| Why | Validate `run_post_task_anti_instinct_hook()` returns `tuple[TaskResult, TrailingGateResult | None]` (FR-1.8) |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0012 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0012/spec.md`

**Deliverables:**
- 1 test in `tests/v3.3/test_wiring_points_e2e.py`: anti-instinct hook return type validation

**Steps:**
1. **[PLANNING]** Identify `run_post_task_anti_instinct_hook()` signature and return type contract
2. **[EXECUTION]** Write `test_anti_instinct_hook_return_type`: invoke hook via real orchestration, assert return is `tuple` with `TaskResult` first element and `TrailingGateResult | None` second element
3. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "anti_instinct" -v`
4. **[COMPLETION]** Emit audit record with spec_ref FR-1.8

**Acceptance Criteria:**
- 1 test asserts return type is `tuple[TaskResult, TrailingGateResult | None]`
- Test exercises hook through real orchestration path
- No mocks on hook internals
- Test emits JSONL audit record

**Validation:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "anti_instinct" -v`
- Evidence: test output log

**Dependencies:** T01.02
**Rollback:** Remove anti-instinct test

---

### T02.05 -- Write 2 gate result accumulation tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-014 |
| Why | Validate gate results accumulate across phases and failed gates produce remediation log entries (FR-1.9-FR-1.10) |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0013 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0013/spec.md`

**Deliverables:**
- 2 tests in `tests/v3.3/test_wiring_points_e2e.py`: gate result accumulation across phases; failed gate -> remediation log entry

**Steps:**
1. **[PLANNING]** Identify gate result accumulation mechanism and remediation log write path
2. **[EXECUTION]** Write `test_gate_result_accumulation`: multi-phase execution -> gate results from each phase accumulated in order
3. **[EXECUTION]** Write `test_failed_gate_remediation_log`: gate returns FAIL -> `DeferredRemediationLog` receives entry
4. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "gate_result" -v`
5. **[COMPLETION]** Emit audit records with spec_ref FR-1.9, FR-1.10

**Acceptance Criteria:**
- 2 tests cover accumulation and failed-gate-to-remediation-log paths
- Accumulation test verifies ordering across multiple phases
- Failed gate test verifies `DeferredRemediationLog` receives an entry (not just that it doesn't crash)
- Both tests emit JSONL audit records

**Validation:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "gate_result" -v`
- Evidence: test output log

**Dependencies:** T01.02
**Rollback:** Remove gate result tests

---

### Checkpoint: Phase 2 / Tasks T02.01-T02.05

**Purpose:** Verify first batch of wiring point E2E tests (construction, delegation, hooks, accumulation) are passing before continuing with remaining FR-1 tests.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-T01-T05.md`
**Verification:**
- All 11 tests across T02.01-T02.05 pass
- JSONL audit records emitted for every test
- `_subprocess_factory` is the sole injection point in all tests

**Exit Criteria:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py -v` exits 0 for tests through T02.05
- Audit JSONL contains records with spec_refs FR-1.1 through FR-1.10
- No `mock.patch` usage on gate functions or orchestration logic

---

### T02.06 -- Write 1 KPI report field VALUES test

| Field | Value |
|---|---|
| Roadmap Item IDs | R-015 |
| Why | Assert KPI report field VALUES match computed expectations, not just field presence (FR-1.11, SC-5) |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0014 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0014/spec.md`

**Deliverables:**
- 1 test in `tests/v3.3/test_wiring_points_e2e.py`: KPI report generation with field VALUE assertions for `wiring_analyses_run`, `wiring_remediations_attempted`, `wiring_net_cost`

**Steps:**
1. **[PLANNING]** Identify KPI report generation path and field computation logic
2. **[EXECUTION]** Write `test_kpi_report_field_values`: run orchestration with known inputs -> assert `wiring_analyses_run`, `wiring_remediations_attempted`, `wiring_net_cost` match computed expectations
3. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "kpi_report" -v`
4. **[COMPLETION]** Emit audit record with spec_ref FR-1.11

**Acceptance Criteria:**
- Test asserts (a) `build_kpi_report()` called with `all_gate_results`, `remediation_log`, `ledger`; (b) `gate-kpi-report.md` written to `results_dir`; (c) field VALUES (not just presence) for `wiring_analyses_run`, `wiring_remediations_attempted`, `wiring_net_cost`
- Values computed from known test inputs match KPI report output; report file exists at expected path
- Test uses `_subprocess_factory` injection
- Test emits JSONL audit record

**Validation:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "kpi_report" -v`
- Evidence: test output log

**Dependencies:** T01.02
**Rollback:** Remove KPI test

---

### T02.07 -- Write 1 wiring mode resolution test

| Field | Value |
|---|---|
| Roadmap Item IDs | R-016 |
| Why | Validate `_resolve_wiring_mode()` correctly resolves mode from config (FR-1.12) |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0015 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0015/spec.md`

**Deliverables:**
- 1 test in `tests/v3.3/test_wiring_points_e2e.py`: wiring mode resolution via `_resolve_wiring_mode()`

**Steps:**
1. **[PLANNING]** Identify `_resolve_wiring_mode()` input contract and mode options (off, shadow, soft, full)
2. **[EXECUTION]** Write `test_wiring_mode_resolution`: configure `config.wiring_gate_mode`, invoke resolver, assert correct mode returned
3. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "wiring_mode" -v`
4. **[COMPLETION]** Emit audit record with spec_ref FR-1.12

**Acceptance Criteria:**
- Test validates `_resolve_wiring_mode()` returns the correct mode for given config
- At least one mode variant tested end-to-end
- No mocks on resolver internals
- Test emits JSONL audit record

**Validation:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "wiring_mode" -v`
- Evidence: test output log

**Dependencies:** T01.02
**Rollback:** Remove mode resolution test

---

### T02.08 -- Write 1 shadow findings remediation log test

| Field | Value |
|---|---|
| Roadmap Item IDs | R-017 |
| Why | Validate shadow findings are logged to remediation log with `[shadow]` prefix (FR-1.13) |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0016 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0016/spec.md`

**Deliverables:**
- 1 test in `tests/v3.3/test_wiring_points_e2e.py`: shadow findings -> remediation log with `[shadow]` prefix

**Steps:**
1. **[PLANNING]** Identify shadow mode configuration and remediation log write path
2. **[EXECUTION]** Write `test_shadow_findings_remediation_log`: run in shadow mode -> findings logged with `[shadow]` prefix in `DeferredRemediationLog`
3. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "shadow_findings" -v`
4. **[COMPLETION]** Emit audit record with spec_ref FR-1.13

**Acceptance Criteria:**
- Test verifies remediation log entries have `[shadow]` prefix when produced under shadow mode
- Test runs via real orchestration path with shadow mode configured
- No mocks on logging internals
- Test emits JSONL audit record

**Validation:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "shadow_findings" -v`
- Evidence: test output log

**Dependencies:** T01.02
**Rollback:** Remove shadow findings test

---

### T02.09 -- Write 3 BLOCKING remediation lifecycle tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-018 |
| Why | Validate the full BLOCKING remediation lifecycle: format -> debit -> recheck -> restore/fail (FR-1.14, FR-1.14a-c) |
| Effort | M |
| Risk | Medium |
| Risk Drivers | remediation lifecycle, multi-step |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0017 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0017/spec.md`
- `TASKLIST_ROOT/artifacts/D-0017/evidence.md`

**Deliverables:**
- 3 tests in `tests/v3.3/test_wiring_points_e2e.py`: BLOCKING remediation format step, debit-then-recheck step, restore-on-success/fail-on-failure step

**Steps:**
1. **[PLANNING]** Map the BLOCKING remediation lifecycle: format -> debit -> `_recheck_wiring()` -> restore/fail
2. **[PLANNING]** Design 3 test scenarios covering each lifecycle phase
3. **[EXECUTION]** Write `test_blocking_remediation_format`: remediation formats finding for recheck
4. **[EXECUTION]** Write `test_blocking_remediation_debit_recheck`: debit occurs, `_recheck_wiring()` executes
5. **[EXECUTION]** Write `test_blocking_remediation_restore_or_fail`: successful recheck restores state; failed recheck produces failure
6. **[VERIFICATION]** Sub-agent verification: all 3 lifecycle phases exercised end-to-end
7. **[COMPLETION]** Emit audit records with spec_ref FR-1.14, FR-1.14a, FR-1.14b, FR-1.14c

**Acceptance Criteria:**
- 3 tests cover 5 discrete assertions: (1) `_format_wiring_failure()` produces non-empty prompt, (2) `ledger.debit(config.remediation_cost)` called, (3) `_recheck_wiring()` called, (4) on pass: status=PASS AND wiring turns credited, (5) on fail: status=FAIL persists
- Tests exercise `_recheck_wiring()` internal path only; `attempt_remediation()` public API deferred to v3.4 (per OQ-5)
- All tests use `_subprocess_factory` injection; no mocks on remediation internals
- All tests emit JSONL audit records

**Validation:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "blocking_remediation" -v`
- Evidence: test output log with lifecycle trace

**Dependencies:** T01.02
**Rollback:** Remove remediation lifecycle tests
**Notes:** Per OQ-5, tests cover `_recheck_wiring()` (internal mechanism); `attempt_remediation()` public API deferred to v3.4.

---

### T02.10 -- Write 2 convergence registry construction/merge tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-019 |
| Why | Validate convergence registry 3-arg construction and `merge_findings()` 3-arg call signature (FR-1.15-FR-1.16) |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0018 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0018/spec.md`

**Deliverables:**
- 2 tests in `tests/v3.3/test_wiring_points_e2e.py`: 3-arg registry construction `(path, release_id, spec_hash)`; 3-arg `merge_findings()` call

**Steps:**
1. **[PLANNING]** Identify convergence registry constructor and `merge_findings()` signatures
2. **[EXECUTION]** Write `test_registry_3arg_construction`: construct with `(path, release_id, spec_hash)`, assert all 3 stored
3. **[EXECUTION]** Write `test_merge_findings_3arg`: call `merge_findings(structural, semantic, run_number)`, assert merged result
4. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "registry" -v`
5. **[COMPLETION]** Emit audit records with spec_ref FR-1.15, FR-1.16

**Acceptance Criteria:**
- 2 tests validate 3-arg construction and 3-arg merge call signatures
- Tests verify argument storage/usage, not just that calls don't crash
- No mocks on registry internals
- Both tests emit JSONL audit records

**Validation:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "registry" -v`
- Evidence: test output log

**Dependencies:** T01.02
**Rollback:** Remove registry tests

---

### Checkpoint: Phase 2 / Tasks T02.06-T02.10

**Purpose:** Verify second batch of wiring point tests (KPI, mode resolution, shadow, remediation, registry) before continuing with remaining FR-1 wiring tests.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-T06-T10.md`
**Verification:**
- All 8 tests across T02.06-T02.10 pass
- KPI test asserts field VALUES not just presence
- BLOCKING remediation lifecycle covers all 3 phases

**Exit Criteria:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py -v` exits 0 for all tests through T02.10
- Audit JSONL contains records with spec_refs FR-1.11 through FR-1.16
- No `mock.patch` usage in any test

---

### T02.11 -- Write 1 dict-to-Finding conversion test

| Field | Value |
|---|---|
| Roadmap Item IDs | R-020 |
| Why | Validate `_run_remediation()` handles dict-to-Finding conversion without AttributeError (FR-1.17) |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0019 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0019/spec.md`

**Deliverables:**
- 1 test in `tests/v3.3/test_wiring_points_e2e.py`: `_run_remediation()` dict-to-Finding conversion

**Steps:**
1. **[PLANNING]** Identify the dict-to-Finding conversion path in `_run_remediation()`
2. **[EXECUTION]** Write `test_dict_to_finding_conversion`: pass dict input to remediation path, assert no `AttributeError` and Finding object produced
3. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "dict_to_finding" -v`
4. **[COMPLETION]** Emit audit record with spec_ref FR-1.17

**Acceptance Criteria:**
- Test passes dict input through `_run_remediation()` and asserts Finding object produced without AttributeError
- Test exercises real remediation code path
- No mocks on conversion logic
- Test emits JSONL audit record

**Validation:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "dict_to_finding" -v`
- Evidence: test output log

**Dependencies:** T01.02
**Rollback:** Remove conversion test

---

### T02.12 -- Write 1 TurnLedger initial_budget=61 test

| Field | Value |
|---|---|
| Roadmap Item IDs | R-021 |
| Why | Validate `TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET)` uses value 61 (FR-1.18) |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0020 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0020/spec.md`

**Deliverables:**
- 1 test in `tests/v3.3/test_wiring_points_e2e.py`: `TurnLedger` initial budget = `MAX_CONVERGENCE_BUDGET` = 61, not 46 — regression guard against prior wrong constant

**Steps:**
1. **[PLANNING]** Locate `MAX_CONVERGENCE_BUDGET` constant definition
2. **[EXECUTION]** Write `test_turnledger_initial_budget_61`: assert `MAX_CONVERGENCE_BUDGET == 61` and `TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET).available() == 61`
3. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "initial_budget" -v`
4. **[COMPLETION]** Emit audit record with spec_ref FR-1.18

**Acceptance Criteria:**
- Test asserts `MAX_CONVERGENCE_BUDGET == 61` and TurnLedger initial budget matches
- Value 61 is not hardcoded in test — test reads `MAX_CONVERGENCE_BUDGET` constant
- No mocks
- Test emits JSONL audit record

**Validation:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "initial_budget" -v`
- Evidence: test output log

**Dependencies:** T01.02
**Rollback:** Remove budget test

---

### T02.13 -- Write 1 SHADOW_GRACE_INFINITE behavior test

| Field | Value |
|---|---|
| Roadmap Item IDs | R-022 |
| Why | Validate `SHADOW_GRACE_INFINITE` constant value and grace period behavior under shadow mode (FR-1.19) |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0021 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0021/spec.md`

**Deliverables:**
- 1 test in `tests/v3.3/test_wiring_points_e2e.py`: `SHADOW_GRACE_INFINITE` constant and shadow mode grace period behavior

**Steps:**
1. **[PLANNING]** Locate `SHADOW_GRACE_INFINITE` constant and understand grace period mechanism
2. **[EXECUTION]** Write `test_shadow_grace_infinite`: assert constant value and verify grace period is effectively infinite under shadow mode
3. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "shadow_grace" -v`
4. **[COMPLETION]** Emit audit record with spec_ref FR-1.19

**Acceptance Criteria:**
- Test asserts (a) `SHADOW_GRACE_INFINITE` constant value matches expected sentinel and (b) when `wiring_gate_grace_period == SHADOW_GRACE_INFINITE`, shadow mode never exits grace period and wiring gate always credits back
- Grace period behavior validated through real orchestration context under shadow mode
- No mocks
- Test emits JSONL audit record

**Validation:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "shadow_grace" -v`
- Evidence: test output log

**Dependencies:** T01.02
**Rollback:** Remove grace test

---

### T02.14 -- Write 1 __post_init__() config field derivation test

| Field | Value |
|---|---|
| Roadmap Item IDs | R-023 |
| Why | Validate `__post_init__()` correctly derives config fields and sets defaults (FR-1.20) |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0022 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0022/spec.md`

**Deliverables:**
- 1 test in `tests/v3.3/test_wiring_points_e2e.py`: `__post_init__()` config field derivation and defaults

**Steps:**
1. **[PLANNING]** Identify `__post_init__()` derived fields and default values
2. **[EXECUTION]** Write `test_post_init_config_derivation`: construct config, assert derived fields match expected defaults
3. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "post_init" -v`
4. **[COMPLETION]** Emit audit record with spec_ref FR-1.20

**Acceptance Criteria:**
- Test validates (a) derived fields (`wiring_gate_enabled`, `wiring_gate_grace_period`, `wiring_analyses_count`) from `__post_init__()` match expected defaults and (b) invalid or missing base config values produce sensible defaults
- Construction uses real config path (not mocked dataclass)
- No mocks on `__post_init__` internals
- Test emits JSONL audit record

**Validation:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "post_init" -v`
- Evidence: test output log

**Dependencies:** T01.02
**Rollback:** Remove post_init test

---

### T02.15 -- Write 1 check_wiring_report() wrapper test

| Field | Value |
|---|---|
| Roadmap Item IDs | R-024 |
| Why | Validate `check_wiring_report()` wrapper is called, delegates correctly, and returns valid report (FR-1.21) |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0023 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0023/spec.md`

**Deliverables:**
- 1 test in `tests/v3.3/test_wiring_points_e2e.py`: `check_wiring_report()` delegation and return validation

**Steps:**
1. **[PLANNING]** Identify `check_wiring_report()` delegation target and return type
2. **[EXECUTION]** Write `test_check_wiring_report_wrapper`: invoke wrapper, assert it delegates and returns valid report
3. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "wiring_report" -v`
4. **[COMPLETION]** Emit audit record with spec_ref FR-1.21

**Acceptance Criteria:**
- Test verifies (a) `check_wiring_report()` is called within wiring analysis flow, (b) delegates to underlying analysis (not a no-op stub), (c) returns valid report structure with expected fields
- Return value structure validated (not just non-None); delegation verified (not just wrapper existence)
- No mocks on wrapper or delegate
- Test emits JSONL audit record

**Validation:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "wiring_report" -v`
- Evidence: test output log

**Dependencies:** T01.02
**Rollback:** Remove wrapper test

---

### Checkpoint: Phase 2 / Tasks T02.11-T02.15

**Purpose:** Verify remaining FR-1 wiring point tests complete the SC-1 target of >=20 wiring point E2E tests.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-T11-T15.md`
**Verification:**
- All 5 tests pass (T02.11-T02.15)
- Cumulative wiring point test count >= 20 (T02.01-T02.15 = 24 tests total)
- SC-1 criterion met

**Exit Criteria:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py -v` exits 0 with >= 20 tests passing
- All FR-1.1 through FR-1.21 sub-requirements have at least one test
- SC-1 validated

---

### T02.16 -- Write convergence path E2E test (v3.05)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-025 |
| Why | Validate full convergence path: debit CHECKER_COST -> run checkers -> credit CONVERGENCE_PASS_CREDIT -> reimburse_for_progress(); budget_snapshot recorded (FR-2.1) |
| Effort | M |
| Risk | Medium |
| Risk Drivers | cross-cutting scope (convergence pipeline) |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0024 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0024/spec.md`

**Deliverables:**
- 1 test in `tests/v3.3/test_turnledger_lifecycle.py`: `execute_fidelity_with_convergence()` E2E with budget assertions

**Steps:**
1. **[PLANNING]** Map convergence path: debit -> checkers -> credit -> reimburse; identify budget observation points
2. **[PLANNING]** Determine expected budget values at each step for known test inputs
3. **[EXECUTION]** Create `tests/v3.3/test_turnledger_lifecycle.py` with test class
4. **[EXECUTION]** Write `test_convergence_path_v305`: execute convergence, assert budget logging includes consumed/reimbursed/available at each step
5. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_turnledger_lifecycle.py -k "convergence_path" -v`
6. **[COMPLETION]** Emit audit record with spec_ref FR-2.1

**Acceptance Criteria:**
- Test exercises full `execute_fidelity_with_convergence()` path end-to-end
- Budget assertions cover consumed, reimbursed, and available values (not just final state)
- `budget_snapshot` recorded during execution
- Test emits JSONL audit record

**Validation:**
- `uv run pytest tests/v3.3/test_turnledger_lifecycle.py -k "convergence_path" -v`
- Evidence: test output log with budget trace

**Dependencies:** T01.02
**Rollback:** Remove convergence path test

---

### T02.17 -- Write sprint per-task path E2E test (v3.1)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-026 |
| Why | Validate sprint per-task path: pre-debit minimum_allocation -> subprocess -> reconcile; post-task hooks fire (FR-2.2) |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0025 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0025/spec.md`

**Deliverables:**
- 1 test in `tests/v3.3/test_turnledger_lifecycle.py`: sprint per-task path with pre-debit, subprocess, reconcile, post-task hooks

**Steps:**
1. **[PLANNING]** Map per-task path: pre-debit `minimum_allocation` -> subprocess via `_subprocess_factory` -> reconcile
2. **[EXECUTION]** Write `test_sprint_per_task_path_v31`: execute per-task path, assert pre-debit occurs, subprocess runs, reconciliation updates ledger, post-task hooks fire
3. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_turnledger_lifecycle.py -k "per_task" -v`
4. **[COMPLETION]** Emit audit record with spec_ref FR-2.2

**Acceptance Criteria:**
- Test validates pre-debit, subprocess execution, reconciliation, and post-task hook firing
- Ledger state assertions at each lifecycle point
- Uses `_subprocess_factory` injection
- Test emits JSONL audit record

**Validation:**
- `uv run pytest tests/v3.3/test_turnledger_lifecycle.py -k "per_task" -v`
- Evidence: test output log

**Dependencies:** T01.02
**Rollback:** Remove per-task path test

---

### T02.18 -- Write sprint per-phase path E2E test (v3.2)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-027 |
| Why | Validate sprint per-phase path: debit_wiring() -> analysis -> credit_wiring() on non-blocking; wiring_analyses_count incremented (FR-2.3) |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0026 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0026/spec.md`

**Deliverables:**
- 1 test in `tests/v3.3/test_turnledger_lifecycle.py`: sprint per-phase path with debit_wiring, analysis, credit_wiring, and analyses count

**Steps:**
1. **[PLANNING]** Map per-phase path: `debit_wiring()` -> analysis -> `credit_wiring()` on non-blocking
2. **[EXECUTION]** Write `test_sprint_per_phase_path_v32`: execute per-phase path, assert debit occurs, analysis runs, credit on non-blocking, `wiring_analyses_count` incremented
3. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_turnledger_lifecycle.py -k "per_phase" -v`
4. **[COMPLETION]** Emit audit record with spec_ref FR-2.3

**Acceptance Criteria:**
- Test validates debit_wiring, analysis execution, credit_wiring on non-blocking outcome, and wiring_analyses_count increment
- Ledger state correct after phase completion
- Uses `_subprocess_factory` injection
- Test emits JSONL audit record

**Validation:**
- `uv run pytest tests/v3.3/test_turnledger_lifecycle.py -k "per_phase" -v`
- Evidence: test output log

**Dependencies:** T01.02
**Rollback:** Remove per-phase path test

---

### T02.19 -- Write cross-path coherence test

| Field | Value |
|---|---|
| Roadmap Item IDs | R-028 |
| Why | Validate `available() = initial_budget - consumed + reimbursed` invariant at every phase checkpoint across mixed paths (FR-2.4) |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0027 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0027/spec.md`

**Deliverables:**
- 1 test in `tests/v3.3/test_turnledger_lifecycle.py`: cross-path coherence with mixed task-inventory + freeform phases

**Steps:**
1. **[PLANNING]** Design multi-phase scenario with mixed task-inventory and freeform phases
2. **[EXECUTION]** Write `test_cross_path_coherence`: run mixed phases, assert `available() == initial_budget - consumed + reimbursed` after each phase completion (per OQ-6)
3. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_turnledger_lifecycle.py -k "cross_path" -v`
4. **[COMPLETION]** Emit audit record with spec_ref FR-2.4

**Acceptance Criteria:**
- Test exercises mixed task-inventory and freeform phases in a single sprint
- Budget invariant `available() = initial_budget - consumed + reimbursed` asserted after each phase checkpoint
- Assertion frequency per OQ-6: per-phase completion (not per-task or per-hook)
- Test emits JSONL audit record

**Validation:**
- `uv run pytest tests/v3.3/test_turnledger_lifecycle.py -k "cross_path" -v`
- Evidence: test output log with per-phase budget snapshots

**Dependencies:** T01.02
**Rollback:** Remove cross-path test

---

### T02.20 -- Write 1 handle_regression() test

| Field | Value |
|---|---|
| Roadmap Item IDs | R-029 |
| Why | Validate `handle_regression()` covers reachability, regression detection, logging, and budget adjustment (FR-2.1a) |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0028 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0028/spec.md`

**Deliverables:**
- 1 test in `tests/v3.3/test_turnledger_lifecycle.py`: `handle_regression()` with reachability, detection, logging, budget

**Steps:**
1. **[PLANNING]** Identify `handle_regression()` contract: reachability check, detection logic, logging, budget adjustment
2. **[EXECUTION]** Write `test_handle_regression`: trigger regression scenario, assert detection, logging, and budget adjustment occur
3. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_turnledger_lifecycle.py -k "handle_regression" -v`
4. **[COMPLETION]** Emit audit record with spec_ref FR-2.1a

**Acceptance Criteria:**
- Test validates regression detection, logging output, and budget adjustment
- Test exercises real `handle_regression()` path
- No mocks on regression handling
- Test emits JSONL audit record

**Validation:**
- `uv run pytest tests/v3.3/test_turnledger_lifecycle.py -k "handle_regression" -v`
- Evidence: test output log

**Dependencies:** T01.02
**Rollback:** Remove regression test

---

### Checkpoint: Phase 2 / Tasks T02.16-T02.20

**Purpose:** Verify all TurnLedger lifecycle tests (FR-2) complete and SC-2 is met.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-T16-T20.md`
**Verification:**
- All 5 TurnLedger lifecycle tests pass
- Budget invariant validated at phase checkpoints
- All 4 execution paths (convergence, per-task, per-phase, cross-path) exercised

**Exit Criteria:**
- `uv run pytest tests/v3.3/test_turnledger_lifecycle.py -v` exits 0 with 5 tests passing
- SC-2 (4/4 TurnLedger paths green) validated
- Audit JSONL contains records with spec_refs FR-2.1 through FR-2.4

---

### T02.21 -- Write 8 gate mode x path E2E tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-030 |
| Why | Validate 4 modes (off, shadow, soft, full) x 2 paths (anti-instinct + wiring) with TaskStatus, GateOutcome, TurnLedger state, remediation log, shadow metrics (FR-3.1a-d) |
| Effort | L |
| Risk | Medium |
| Risk Drivers | cross-cutting scope (4 modes x 2 paths), multi-file |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0029 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0029/spec.md`
- `TASKLIST_ROOT/artifacts/D-0029/evidence.md`

**Deliverables:**
- 8 tests in `tests/v3.3/test_gate_rollout_modes.py`: 4 modes x 2 paths, each verifying TaskStatus/GateOutcome, TurnLedger state, DeferredRemediationLog entries, ShadowGateMetrics recording

**Steps:**
1. **[PLANNING]** Map the 4x2 test matrix: off/shadow/soft/full x anti-instinct/wiring
2. **[PLANNING]** Identify expected outcomes per cell: TaskStatus, GateOutcome, ledger state, remediation log entries, shadow metrics
3. **[EXECUTION]** Create `tests/v3.3/test_gate_rollout_modes.py` with parametrized test structure
4. **[EXECUTION]** Write 8 tests: each configures mode, runs path, asserts all 4 outcome dimensions
5. **[EXECUTION]** For shadow mode tests: verify `ShadowGateMetrics` recording without blocking execution
6. **[VERIFICATION]** Sub-agent verification: all 8 mode/path combinations validated with correct outcomes
7. **[COMPLETION]** All tests emit JSONL audit records with spec_ref FR-3.1a through FR-3.1d

**Acceptance Criteria:**
- 8 tests exist covering all 4 modes x 2 paths combinations
- Each test asserts all 4 outcome dimensions: TaskStatus/GateOutcome, TurnLedger state, DeferredRemediationLog, ShadowGateMetrics
- All tests use `_subprocess_factory` injection; no mocks on gate or mode resolution
- All tests emit JSONL audit records

**Validation:**
- `uv run pytest tests/v3.3/test_gate_rollout_modes.py -k "mode" -v`
- Evidence: test output log with per-mode outcomes

**Dependencies:** T01.02
**Rollback:** Remove mode matrix tests

---

### T02.22 -- Write 4 budget exhaustion scenario tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-031 |
| Why | Validate budget exhaustion at 4 points: before task launch, before wiring, before remediation, mid-convergence (FR-3.2a-d, SC-6) |
| Effort | M |
| Risk | Medium |
| Risk Drivers | cross-cutting scope (4 exhaustion points) |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0030 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0030/spec.md`

**Deliverables:**
- 4 tests in `tests/v3.3/test_gate_rollout_modes.py`: (a) before task launch: SKIPPED + remaining tasks listed (FR-3.2a), (b) before wiring: hook skipped + task status unchanged (FR-3.2b), (c) before remediation: FAIL persists + BUDGET_EXHAUSTED logged (FR-3.2c), (d) mid-convergence: halt with diagnostic + run_count < max_runs (FR-3.2d)

**Steps:**
1. **[PLANNING]** Identify budget exhaustion detection logic at each of the 4 points
2. **[EXECUTION]** Write `test_budget_exhaustion_before_task_launch`: set budget to 0, attempt task -> graceful halt
3. **[EXECUTION]** Write `test_budget_exhaustion_before_wiring`: exhaust budget after task but before wiring gate -> skip wiring
4. **[EXECUTION]** Write `test_budget_exhaustion_before_remediation`: exhaust before remediation -> skip remediation
5. **[EXECUTION]** Write `test_budget_exhaustion_mid_convergence`: exhaust during convergence loop -> exit loop gracefully
6. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_gate_rollout_modes.py -k "budget_exhaustion" -v`
7. **[COMPLETION]** All tests emit JSONL audit records with spec_ref FR-3.2a through FR-3.2d

**Acceptance Criteria:**
- 4 tests cover all budget exhaustion scenarios per FR-3.2a-d
- Each test confirms graceful behavior (no crash, appropriate skip/halt) on budget exhaustion
- Tests co-located with mode tests in `test_gate_rollout_modes.py` per roadmap design decision
- All tests emit JSONL audit records

**Validation:**
- `uv run pytest tests/v3.3/test_gate_rollout_modes.py -k "budget_exhaustion" -v`
- Evidence: test output log

**Dependencies:** T01.02
**Rollback:** Remove budget exhaustion tests

---

### T02.23 -- Write 1 interrupted sprint SIGINT test

| Field | Value |
|---|---|
| Roadmap Item IDs | R-032 |
| Why | Validate interrupted sprint via SIGINT produces KPI report, persists remediation log, sets outcome=INTERRUPTED (FR-3.3, OQ-1) |
| Effort | M |
| Risk | Medium |
| Risk Drivers | signal handling, platform-specific |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0031 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0031/spec.md`

**Deliverables:**
- 1 test in `tests/v3.3/test_gate_rollout_modes.py`: interrupted sprint via `os.kill(os.getpid(), signal.SIGINT)` with KPI/remediation/outcome assertions

**Steps:**
1. **[PLANNING]** Design signal delivery mechanism: `os.kill(os.getpid(), signal.SIGINT)` per OQ-1
2. **[EXECUTION]** Write `test_interrupted_sprint_sigint`: start sprint, send SIGINT mid-execution, assert KPI report written, remediation log persisted, outcome = INTERRUPTED
3. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_gate_rollout_modes.py -k "sigint" -v`
4. **[COMPLETION]** Emit audit record with spec_ref FR-3.3

**Acceptance Criteria:**
- Test sends `SIGINT` via `os.kill(os.getpid(), signal.SIGINT)` per OQ-1 architect recommendation
- KPI report is written despite interruption
- Remediation log is persisted despite interruption
- Sprint outcome is `INTERRUPTED`

**Validation:**
- `uv run pytest tests/v3.3/test_gate_rollout_modes.py -k "sigint" -v`
- Evidence: test output log

**Dependencies:** T01.02
**Rollback:** Remove SIGINT test
**Notes:** Per OQ-1, test SIGINT only; SIGTERM/SIGHUP are out of scope.

---

### Checkpoint: Phase 2 / Tasks T02.21-T02.25

**Purpose:** Verify gate rollout mode matrix and budget exhaustion tests complete SC-3 and SC-6.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-T21-T25.md`
**Verification:**
- All 13 tests across T02.21-T02.23 pass (8 mode + 4 budget + 1 SIGINT)
- SC-3 (8+ gate mode scenarios) validated
- SC-6 (4/4 budget exhaustion) validated

**Exit Criteria:**
- `uv run pytest tests/v3.3/test_gate_rollout_modes.py -v` exits 0 with 13 tests passing
- All FR-3.1a-d and FR-3.2a-d have at least one test
- Interrupted sprint test produces INTERRUPTED outcome

---

### T02.24 -- Verify and extend wiring test assertions (FR-6.1 T07)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-033 |
| Why | Verify 7 existing wiring tests in `tests/roadmap/test_convergence_wiring.py` cover all FR-1 integration points; add missing assertions (FR-6.1 T07) |
| Effort | S |
| Risk | Low |
| Risk Drivers | review scope |
| Tier | EXEMPT |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0032 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0032/spec.md`

**Deliverables:**
- Verified/extended `tests/roadmap/test_convergence_wiring.py` with >= 7 assertions covering all FR-1 integration points; all existing tests being extended retrofitted with `audit_trail` fixture usage per REQ-078 (every test must emit JSONL record)

**Steps:**
1. **[PLANNING]** Read existing `tests/roadmap/test_convergence_wiring.py` to audit current coverage
2. **[PLANNING]** Map existing tests against FR-1 integration points; identify gaps
3. **[EXECUTION]** Add missing assertions for any untested wiring callbacks (target: 7 assertions minimum)
4. **[EXECUTION]** Retrofit `audit_trail` fixture usage into all tests per REQ-078
5. **[VERIFICATION]** Run `uv run pytest tests/roadmap/test_convergence_wiring.py -v`
6. **[COMPLETION]** Document which assertions were added and which FR-1 points they cover

**Acceptance Criteria:**
- `tests/roadmap/test_convergence_wiring.py` has >= 7 assertions covering FR-1 integration points
- All tests use `audit_trail` fixture per REQ-078
- No new `mock.patch` usage on gate functions
- Coverage gaps documented in evidence

**Validation:**
- `uv run pytest tests/roadmap/test_convergence_wiring.py -v`
- Evidence: audit of existing vs new assertions

**Dependencies:** T01.02
**Rollback:** Revert assertion additions

---

### T02.25 -- Extend convergence E2E tests for SC-1 through SC-6

| Field | Value |
|---|---|
| Roadmap Item IDs | R-034 |
| Why | Extend existing `tests/roadmap/test_convergence_e2e.py` tests to explicitly assert SC-1 through SC-6 acceptance criteria (FR-6.1 T11) |
| Effort | S |
| Risk | Low |
| Risk Drivers | review scope |
| Tier | EXEMPT |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0033 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0033/spec.md`

**Deliverables:**
- Extended `tests/roadmap/test_convergence_e2e.py` with explicit assertions for SC-1 through SC-6 (6 SC-level assertions); `audit_trail` fixture retrofitted

**Steps:**
1. **[PLANNING]** Read existing `tests/roadmap/test_convergence_e2e.py` to audit current SC coverage
2. **[PLANNING]** Map each SC-1 through SC-6 to a verifiable assertion
3. **[EXECUTION]** Add explicit assertion for each SC (target: 6 SC-level assertions)
4. **[EXECUTION]** Retrofit `audit_trail` fixture usage per REQ-078
5. **[VERIFICATION]** Run `uv run pytest tests/roadmap/test_convergence_e2e.py -v`
6. **[COMPLETION]** Document SC mapping

**Acceptance Criteria:**
- `tests/roadmap/test_convergence_e2e.py` has explicit assertions for SC-1 through SC-6
- All tests use `audit_trail` fixture per REQ-078
- No new `mock.patch` usage
- SC mapping documented in evidence

**Validation:**
- `uv run pytest tests/roadmap/test_convergence_e2e.py -v`
- Evidence: SC-to-assertion mapping

**Dependencies:** T01.02
**Rollback:** Revert SC assertion additions

---

### T02.26 -- Add convergence smoke test

| Field | Value |
|---|---|
| Roadmap Item IDs | R-035 |
| Why | Add smoke test for convergence path; verify target file location before implementation (FR-6.1 T12) |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0034 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0034/spec.md`

**Deliverables:**
- Convergence smoke test in `tests/roadmap/test_convergence_smoke.py` (existing) or `test_convergence_e2e.py`

**Steps:**
1. **[PLANNING]** Verify target file location: check if `test_convergence_smoke.py` exists, else use `test_convergence_e2e.py`
2. **[EXECUTION]** Add smoke test: minimal convergence path execution -> assert no crash and basic output produced
3. **[VERIFICATION]** Run smoke test
4. **[COMPLETION]** Emit audit record

**Acceptance Criteria:**
- Smoke test exists in verified target file; all existing tests being extended retrofitted with `audit_trail` fixture per REQ-078
- Test exercises convergence path with minimal setup
- No mocks on convergence internals
- Test emits JSONL audit record via `audit_trail` fixture

**Validation:**
- Manual check: smoke test passes in target file
- Evidence: test output

**Dependencies:** T01.02
**Rollback:** Remove smoke test

---

### T02.27 -- Regenerate wiring-verification artifact

| Field | Value |
|---|---|
| Roadmap Item IDs | R-036 |
| Why | Regenerate the wiring-verification artifact and validate it reflects current codebase state (FR-6.1 T14) |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0035 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0035/spec.md`

**Deliverables:**
- Regenerated wiring-verification artifact in `docs/generated/`

**Steps:**
1. **[PLANNING]** Locate existing wiring-verification artifact generation process
2. **[EXECUTION]** Regenerate artifact reflecting current v3.3 codebase state
3. **[EXECUTION]** Validate regenerated artifact against known wiring points
4. **[VERIFICATION]** Manual review of generated artifact
5. **[COMPLETION]** Record artifact path and generation timestamp

**Acceptance Criteria:**
- Wiring-verification artifact regenerated in `docs/generated/`
- Artifact reflects current codebase wiring state
- Artifact is self-contained and readable without tribal knowledge
- Generation timestamp recorded

**Validation:**
- Manual check: artifact exists in `docs/generated/` and is non-empty
- Evidence: artifact file path

**Dependencies:** T02.01 through T02.23 (artifact should reflect all new tests)
**Rollback:** Restore previous artifact version

---

### T02.28 -- Write confirming run_post_phase_wiring_hook() test

| Field | Value |
|---|---|
| Roadmap Item IDs | R-037 |
| Why | Confirming test for `run_post_phase_wiring_hook()` to close FR-6.2 T02 gap (may overlap T02.03) |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0036 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0036/spec.md`

**Deliverables:**
- 1 confirming test in `tests/v3.3/test_wiring_points_e2e.py` for `run_post_phase_wiring_hook()` (FR-6.2 T02)

**Steps:**
1. **[PLANNING]** Review T02.03 coverage; determine if additional confirming test adds value beyond existing hook tests
2. **[EXECUTION]** Write confirming test that validates `run_post_phase_wiring_hook()` specifically (distinct from the 2 path tests in T02.03 if coverage gap exists)
3. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "run_post_phase_wiring_hook" -v`
4. **[COMPLETION]** Emit audit record with spec_ref FR-6.2 T02

**Acceptance Criteria:**
- Confirming test exists for `run_post_phase_wiring_hook()` in `tests/v3.3/test_wiring_points_e2e.py`
- Test adds coverage value beyond T02.03 (or documents overlap if coverage already sufficient)
- No mocks on hook internals
- Test emits JSONL audit record

**Validation:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py -k "run_post_phase_wiring_hook" -v`
- Evidence: test output log

**Dependencies:** T01.02
**Rollback:** Remove confirming test
**Notes:** May overlap T02.03 (FR-1.7 post-phase wiring hook both-paths tests); check 2A.3 coverage first before implementing. Depends on Phase 2A completion.

---

### T02.29 -- Write 6-test integration + regression suite (T17-T22)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-038 |
| Why | Close FR-6.2 T17-T22 gaps: cross-phase ledger, mode switch, concurrent gate, audit completeness, manifest coverage, full pipeline E2E |
| Effort | L |
| Risk | Medium |
| Risk Drivers | cross-cutting scope (6 distinct integration scenarios) |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0037 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0037/spec.md`
- `TASKLIST_ROOT/artifacts/D-0037/evidence.md`

**Deliverables:**
- 6 tests in `tests/v3.3/test_integration_regression.py`: T17 (cross-phase ledger coherence — ledger state correct across multiple phases), T18 (mode switch mid-sprint — mode change handled correctly), T19 (concurrent gate evaluation — no state corruption), T20 (audit completeness — all test events recorded in audit trail), T21 (manifest coverage — wiring manifest covers all entry points), T22 (full pipeline E2E — end-to-end pipeline execution)

**Steps:**
1. **[PLANNING]** Map T17-T22 requirements to specific test scenarios
2. **[PLANNING]** Identify shared fixtures needed for integration tests
3. **[EXECUTION]** Create `tests/v3.3/test_integration_regression.py`
4. **[EXECUTION]** Write `test_cross_phase_ledger` (T17): ledger state correct across multiple phases
5. **[EXECUTION]** Write `test_mode_switch` (T18): mode change mid-sprint handled correctly
6. **[EXECUTION]** Write `test_concurrent_gate` (T19): concurrent gate evaluation doesn't corrupt state
7. **[EXECUTION]** Write `test_audit_completeness` (T20): all test events recorded in audit trail
8. **[EXECUTION]** Write `test_manifest_coverage` (T21): wiring manifest covers all entry points
9. **[EXECUTION]** Write `test_full_pipeline_e2e` (T22): end-to-end pipeline execution
10. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_integration_regression.py -v`
11. **[COMPLETION]** All tests emit JSONL audit records

**Acceptance Criteria:**
- 6 tests exist in `tests/v3.3/test_integration_regression.py` covering T17-T22
- All tests exercise real orchestration paths via `_subprocess_factory`
- No `mock.patch` on gate functions or orchestration logic
- All tests emit JSONL audit records

**Validation:**
- `uv run pytest tests/v3.3/test_integration_regression.py -v`
- Evidence: test output log with all 6 passing

**Dependencies:** T01.02, T01.07 (manifest for T21)
**Rollback:** Delete `tests/v3.3/test_integration_regression.py`

---

### Checkpoint: End of Phase 2

**Purpose:** Confirm all E2E test suites pass and SC-1 through SC-6, SC-8, SC-12 are validated before production code changes in Phase 3.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-END.md`
**Verification:**
- All E2E tests pass across 4 test files: `test_wiring_points_e2e.py`, `test_turnledger_lifecycle.py`, `test_gate_rollout_modes.py`, `test_integration_regression.py`
- SC-1 (>=20 wiring tests), SC-2 (4/4 paths), SC-3 (8+ modes), SC-5 (KPI values), SC-6 (4/4 budget), SC-8 (QA gaps), SC-12 (audit trail) all green
- Audit trail JSONL emitted for every test with spec_ref tracing

**Exit Criteria:**
- `uv run pytest tests/v3.3/ tests/roadmap/ -v` exits 0
- Wiring point E2E test count >= 20
- All `audit_trail` JSONL records parseable and spec-traced
