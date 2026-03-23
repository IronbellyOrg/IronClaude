# Phase 4 -- Integration Testing and Validation

End-to-end validation of the full wiring gate pipeline including budget flows, the cli-portify retrospective (detecting the original `step_runner=None` no-op bug), and performance benchmarking. All code from Phases 1-3 must be complete before this phase begins.

---

### T04.01 -- Write cli-portify Fixture Integration Test

| Field | Value |
|---|---|
| Roadmap Item IDs | R-034 |
| Why | The cli-portify fixture is the non-negotiable behavioral contract — it must produce exactly 1 WiringFinding(unwired_callable) to validate the gate would have caught the original no-op bug. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | data (fixture fidelity to real defect), breaking (behavioral contract) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0021 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0021/evidence.md`

**Deliverables:**
1. cli-portify fixture integration test in `tests/audit/test_wiring_integration.py` producing exactly 1 `WiringFinding(unwired_callable)` (SC-010)

**Steps:**
1. **[PLANNING]** Read FR: T10, SC-010 requirements; study the original cli-portify `step_runner=None` no-op bug pattern
2. **[PLANNING]** Design fixture that reproduces the exact defect pattern: a callable declared but never wired into dispatch
3. **[EXECUTION]** Create fixture in `tests/audit/` that models the cli-portify package structure with the no-op wiring defect
4. **[EXECUTION]** Write integration test asserting `analyze_unwired_callables()` returns exactly 1 finding with `finding_type='unwired_callable'`
5. **[EXECUTION]** Assert finding details reference the specific unwired callable (the `step_runner` equivalent)
6. **[VERIFICATION]** `uv run pytest tests/audit/test_wiring_integration.py -v` exits 0 with exactly 1 finding produced
7. **[COMPLETION]** Record test results and finding details to D-0021/evidence.md

**Acceptance Criteria:**
- `tests/audit/test_wiring_integration.py` exists with cli-portify fixture integration test
- Test produces exactly 1 `WiringFinding` with `finding_type='unwired_callable'` (SC-010 behavioral contract)
- Finding references the specific unwired callable matching the original no-op bug pattern
- `uv run pytest tests/audit/test_wiring_integration.py -v` exits 0

**Validation:**
- `uv run pytest tests/audit/test_wiring_integration.py -v`
- Evidence: test output and finding details archived to D-0021/evidence.md

**Dependencies:** T01.02, T01.05 (analyzer and gate must exist)
**Rollback:** Delete `tests/audit/test_wiring_integration.py`

---

### T04.02 -- Write Budget Scenario Integration Tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-035, R-036, R-037, R-038 |
| Why | Integration tests validate the full budget flow including floor-to-zero credit, BLOCKING remediation, null-ledger compatibility, and shadow deferred logging across the execution pipeline. |
| Effort | M |
| Risk | High |
| Risk Drivers | data (budget arithmetic edge cases), breaking (remediation flow), rollback (null-ledger path) |
| Tier | STRICT |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0022 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0022/evidence.md`

**Deliverables:**
1. 4 budget scenario integration tests in `tests/pipeline/test_full_flow.py`: Scenario 5 (credit floor, SC-012), Scenario 6 (BLOCKING remediation), Scenario 7 (null-ledger compat, SC-014), Scenario 8 (shadow deferred log)

**Steps:**
1. **[PLANNING]** Read FR: T12 budget scenario specifications for Scenarios 5-8
2. **[PLANNING]** Review SC-012 (debit/credit correctness), SC-013 (reimbursement consumed), SC-014 (null-ledger compat) acceptance criteria
3. **[EXECUTION]** Write Scenario 5 test: `credit_wiring(1, 0.8)` returns 0 credits in pipeline context (SC-012 integration validation)
4. **[EXECUTION]** Write Scenario 6 test: BLOCKING mode triggers remediation, budget debited, BUDGET_EXHAUSTED on depletion
5. **[EXECUTION]** Write Scenario 7 test: `ledger is None` path matches prior behavior — no budget operations, no crashes (SC-014)
6. **[EXECUTION]** Write Scenario 8 test: SHADOW mode defers finding log without modifying task status
7. **[VERIFICATION]** `uv run pytest tests/pipeline/test_full_flow.py -k "wiring or budget" -v` exits 0 with all 4 scenarios passing
8. **[COMPLETION]** Record test results to D-0022/evidence.md

**Acceptance Criteria:**
- `tests/pipeline/test_full_flow.py` contains 4 wiring budget scenario integration tests
- Scenario 5 explicitly asserts floor-to-zero: `credit_wiring(1, 0.8)` returns 0 in pipeline context (SC-012)
- Scenario 7 asserts null-ledger behavioral equivalence (SC-014)
- `uv run pytest tests/pipeline/test_full_flow.py -k "wiring or budget" -v` exits 0

**Validation:**
- `uv run pytest tests/pipeline/test_full_flow.py -k "wiring or budget" -v`
- Evidence: test output log archived to D-0022/evidence.md

**Dependencies:** T02.04, T02.05, T02.06, T02.07, T02.08
**Rollback:** Delete wiring budget test functions from `tests/pipeline/test_full_flow.py`

---

### T04.03 -- Run Retrospective Validation Against cli_portify

| Field | Value |
|---|---|
| Roadmap Item IDs | R-039 |
| Why | Running the analysis against the actual `cli_portify/` directory validates that the gate would have detected the original step_runner=None no-op bug in real code, not just fixtures. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | data (real codebase analysis), performance (real file count) |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0023 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0023/evidence.md`

**Deliverables:**
1. Retrospective validation report confirming analysis of actual `cli_portify/` detects the original `step_runner=None` no-op bug (SC-010, FR: T11)

**Steps:**
1. **[PLANNING]** Locate `cli_portify/` directory in the repository; confirm it contains the original defect pattern
2. **[PLANNING]** Review SC-010 acceptance: analysis must detect the no-op bug, not just pass on fixtures
3. **[EXECUTION]** Run `analyze_unwired_callables()` against actual `cli_portify/` directory
4. **[EXECUTION]** Capture findings report; verify at least 1 finding of type `unwired_callable` referencing the step_runner pattern
5. **[VERIFICATION]** Confirm finding matches SC-010 behavioral contract (detection of original no-op bug in real code)
6. **[COMPLETION]** Record retrospective validation report to D-0023/evidence.md

**Acceptance Criteria:**
- Analysis run against actual `cli_portify/` directory produces at least 1 `WiringFinding(unwired_callable)` (SC-010)
- Finding references the specific `step_runner=None` no-op pattern that motivated this release
- Validation report documents finding details and confirms real-code detection
- Report archived at D-0023/evidence.md

**Validation:**
- Manual check: retrospective analysis output reviewed for SC-010 compliance
- Evidence: validation report produced at D-0023/evidence.md

**Dependencies:** T04.01 (fixture test must pass first to confirm analyzer works)
**Rollback:** Delete D-0023/evidence.md

---

### T04.04 -- Run Performance Benchmark

| Field | Value |
|---|---|
| Roadmap Item IDs | R-040 |
| Why | Performance validation ensures the AST-only analysis gate completes within the p95 < 5s threshold on a representative 50-file package, preventing sprint loop slowdown. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | performance (p95 latency threshold), latency |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0024 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0024/evidence.md`

**Deliverables:**
1. Performance benchmark report confirming p95 < 5s on 50-file package (NFR-001, SC-009)

**Steps:**
1. **[PLANNING]** Identify or create a 50-file Python package benchmark fixture
2. **[PLANNING]** Review NFR-001 and SC-009 performance threshold: p95 < 5s
3. **[EXECUTION]** Run full wiring analysis pipeline against 50-file benchmark fixture
4. **[EXECUTION]** Measure wall-clock time across multiple runs (minimum 10 iterations) to compute p95
5. **[VERIFICATION]** Verify p95 < 5s threshold met; if not, identify bottlenecks for optimization
6. **[COMPLETION]** Record benchmark results to D-0024/evidence.md

**Acceptance Criteria:**
- Benchmark run against 50-file package completes with p95 < 5s (SC-009)
- Multiple iterations measured (minimum 10) for statistical validity
- Results include p50, p95, and max timings
- Report archived at D-0024/evidence.md

**Validation:**
- Manual check: benchmark timing data reviewed against SC-009 threshold
- Evidence: benchmark report produced at D-0024/evidence.md

**Dependencies:** T01.05 (analysis engine must be complete)
**Rollback:** Delete D-0024/evidence.md

---

### Checkpoint: End of Phase 4

**Purpose:** Final code quality gate before merge — verify all success criteria, coverage, performance, and retroactive detection.
**Checkpoint Report Path:** `.dev/releases/current/v3.2_fidelity-refactor___/checkpoints/CP-P04-END.md`
**Verification:**
- Full success-criteria review: SC-001 through SC-015 satisfied or explicitly dispositioned
- Coverage >= 90% on `wiring_gate.py` (NFR-003)
- Retrospective detection of the original no-op bug succeeds (SC-010)
**Exit Criteria:**
- All 4 tasks (T04.01-T04.04) completed with deliverables D-0021 through D-0024 produced
- Performance benchmark p95 < 5s confirmed (SC-009)
- NFR-006 verified: diff inspection proves `pipeline/models.py`, `pipeline/gates.py`, `pipeline/trailing_gate.py` unchanged
