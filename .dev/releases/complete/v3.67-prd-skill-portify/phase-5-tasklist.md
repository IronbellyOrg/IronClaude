# Phase 5 -- Validation + E2E

**Goal**: Resolve pre-implementation open items, write E2E test scenarios, and run final integration validation across the complete pipeline.

**Files**: Open Items document, E2E test suite, validation report

**Dependencies**: Phases 1-4 (complete PRD CLI module)

---

## T05.01: Resolve pre-implementation Open Items

**Type**: Clarification Task
**Effort**: XS | **Risk**: Low | **Tier**: EXEMPT | **Confidence**: [######----] 55%
**Requires Confirmation**: No
**Verification Method**: Skip verification
**MCP Tools**: None required
**Sub-Agent Delegation**: None

**Deliverable**: D-0025 u2014 Open Items resolution document
**Roadmap Items**: R-056

**Steps**:
1. **[PLANNING]** Review Section 11 (Open Items) for OI-001 and OI-002 (pre-implementation targets)
2. **[PLANNING]** Gather context from spec sections referenced by each open item
3. **[EXECUTION]** Resolve OI-001: decide whether `--scope product|feature` is explicit flag or inferred from parsing. Recommendation: infer from parsing (matches current skill behavior). Record decision.
4. **[EXECUTION]** Resolve OI-002: define maximum acceptable wall-clock time for heavyweight PRD run. Recommendation: 45 minutes based on 10+ agents with 600s timeout each plus fix cycles. Record decision.
5. **[EXECUTION]** Document resolution rationale for OI-001 and OI-002
6. **[VERIFICATION]** Review remaining OI-003 through OI-011 and confirm they are correctly marked as "During implementation" targets
7. **[COMPLETION]** Write resolution document to D-0025 artifact path

**Acceptance Criteria**:
- [ ] OI-001 resolved with documented decision and rationale
- [ ] OI-002 resolved with specific timeout value and justification
- [ ] Decisions recorded in writing with impact analysis
- [ ] OI-003 through OI-011 confirmed as implementation-time items

**Validation**:
- Manual check: resolution document exists at D-0025 artifact path
- Evidence: 2 open items resolved with decisions documented

**Risk Drivers**: None

---

## T05.02: Write E2E test suite

**Effort**: M | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Critical Path Override**: No
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: None required
**Sub-Agent Delegation**: None

**Deliverable**: D-0026 u2014 E2E test suite (5 scenarios)
**Roadmap Items**: R-051

**Steps**:
1. **[PLANNING]** Review Section 8.3 test plan for 5 E2E test scenarios
2. **[PLANNING]** Design E2E test infrastructure: mock Claude subprocess responses, tmp_path working directories
3. **[EXECUTION]** Implement Scenario 1: Full PRD creation (standard tier) u2014 complete pipeline from request to PRD output, 800-1500 lines expected
4. **[EXECUTION]** Implement Scenario 2: Lightweight PRD u2014 shorter pipeline with 2-3 research agents, 0-1 web agents
5. **[EXECUTION]** Implement Scenario 3: Resume from halted step u2014 skip completed steps, resume from specified agent ID
6. **[EXECUTION]** Implement Scenario 4: Existing work detection u2014 run twice with same product, second detects existing work
7. **[EXECUTION]** Implement Scenario 5: Budget exhaustion u2014 `--max-turns 50` causes halt with resume command and suggested budget
8. **[VERIFICATION]** Run full E2E suite with mocked subprocess responses
9. **[COMPLETION]** Record scenario pass count and execution time in evidence

**Acceptance Criteria**:
- [ ] 5 E2E test scenarios implemented matching Section 8.3 specification
- [ ] Tests use mocked Claude subprocess responses (no real API calls)
- [ ] Each scenario validates end-to-end data flow from CLI input to output artifacts
- [ ] Resume scenario verifies step-skipping and per-agent resume behavior

**Validation**:
- `uv run pytest tests/cli/prd/test_e2e.py -v --tb=short`
- Evidence: 5 E2E scenarios passed, 0 failures

**Risk Drivers**: end-to-end (+1)

---

## T05.03: Full pipeline integration validation

**Effort**: S | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Critical Path Override**: No
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: Preferred: Sequential
**Sub-Agent Delegation**: Recommended (final validation)

**Deliverable**: D-0027 u2014 Final validation report
**Roadmap Items**: R-055

**Steps**:
1. **[PLANNING]** Compile complete test run: all unit + integration + E2E tests
2. **[PLANNING]** Review risk mitigations from Section 7 against implementation
3. **[EXECUTION]** Run full test suite: `uv run pytest tests/cli/prd/ -v --tb=short`
4. **[EXECUTION]** Verify coverage across all 14 source files in `src/superclaude/cli/prd/`
5. **[EXECUTION]** Verify all 9 risk mitigations from Section 7 are addressed by implementation
6. **[EXECUTION]** Run `superclaude prd run "validation test" --dry-run` to verify CLI end-to-end
7. **[VERIFICATION]** Compile final validation report with test counts, coverage, risk verification
8. **[COMPLETION]** Write validation report to D-0027 artifact path

**Acceptance Criteria**:
- [ ] Full test suite passes: `uv run pytest tests/cli/prd/ -v` shows 0 failures
- [ ] All 14 source files have at least 1 test covering their primary function
- [ ] All 9 risk mitigations from Section 7 verified as addressed in implementation
- [ ] Validation report documents: test count, pass rate, coverage summary, risk checklist

**Validation**:
- `uv run pytest tests/cli/prd/ -v --tb=short --co | wc -l` (count test items)
- Evidence: validation report at D-0027 with full test results and risk checklist

**Risk Drivers**: None

---

### Checkpoint: End of Phase 5

**Purpose**: Final quality gate before declaring the PRD CLI pipeline implementation complete.

**Verification**:
- [ ] Full test suite: `uv run pytest tests/cli/prd/ -v` shows 44+ tests passed, 0 failures
- [ ] CLI subcommand functional: `superclaude prd --help` displays correctly
- [ ] Open Items OI-001 and OI-002 resolved

**Exit Criteria**:
- [ ] All 44+ tests passing (unit: 24, integration: 9, E2E: 5, CLI smoke: 1, + validation)
- [ ] 14 source files + 1 modified file complete
- [ ] Validation report written with risk checklist verified
- [ ] Pipeline ready for first real PRD generation run
