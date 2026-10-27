# Phase 3 -- Execution Engine

**Goal**: Implement the runtime modules that drive the PRD pipeline: NDJSON monitoring, Claude subprocess management, execution logging, failure diagnostics, TUI dashboard, and the main executor loop. The executor is the integration point that depends on all Phase 1 and Phase 2 modules.

**Files**: `monitor.py`, `process.py`, `logging_.py`, `diagnostics.py`, `tui.py`, `executor.py` + corresponding tests

**Dependencies**: Phase 1 (models, gates, inventory, filtering), Phase 2 (prompts, config), `pipeline.process` (base ClaudeProcess)

---

## T03.01: Implement monitor.py

**Effort**: S | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Critical Path Override**: No
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: Preferred: Sequential, Context7
**Sub-Agent Delegation**: None

**Deliverable**: D-0013 u2014 `src/superclaude/cli/prd/monitor.py`
**Roadmap Items**: R-022, R-035

**Steps**:
1. **[PLANNING]** Review PrdMonitorState fields from models.py
2. **[PLANNING]** Review sprint module's monitor.py for NDJSON parsing patterns
3. **[EXECUTION]** Implement `PrdMonitor` class with `parse_line(line: str) -> None` updating PrdMonitorState
4. **[EXECUTION]** Implement PRD-specific signal detection: research file completion (`research/NN-*.md` created), QA verdict extraction, fix cycle counter, synthesis completion signals
5. **[EXECUTION]** Implement stall detection: `check_stall(threshold_seconds: float) -> bool` comparing last_event_time to current time [NFR-PRD.5]
6. **[EXECUTION]** Implement `get_state() -> PrdMonitorState` for TUI consumption. NOTE: monitor depends only on models.py; it does NOT import executor types [GAP-002]
7. **[VERIFICATION]** Verify monitor parses synthetic NDJSON lines correctly and updates state
8. **[COMPLETION]** Record signal count in evidence

**Acceptance Criteria**:
- [ ] Parses NDJSON stdout lines and updates PrdMonitorState fields
- [ ] Detects stall condition when no events received within stall_timeout [NFR-PRD.5]
- [ ] No imports from executor.py or tui.py (prevents circular dependency) [GAP-002]
- [ ] Extracts QA verdict, fix cycle count, and agent completion signals from output

**Validation**:
- `uv run python -c "from superclaude.cli.prd.monitor import PrdMonitor; m = PrdMonitor(); print(m.get_state())"`
- Evidence: PrdMonitor importable, get_state returns PrdMonitorState instance

**Risk Drivers**: None

---

## T03.02: Implement process.py

**Effort**: M | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Critical Path Override**: No
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: Preferred: Sequential, Context7
**Sub-Agent Delegation**: None

**Deliverable**: D-0014 u2014 `src/superclaude/cli/prd/process.py`
**Roadmap Items**: R-023, R-038, R-041

**Steps**:
1. **[PLANNING]** Read `src/superclaude/cli/pipeline/process.py` to understand base `ClaudeProcess` interface
2. **[PLANNING]** Review Section 5.3 (Phase Contracts) for per-step `allowed_refs` scoping
3. **[EXECUTION]** Implement `PrdClaudeProcess` extending `ClaudeProcess` with PRD-specific prompt construction
4. **[EXECUTION]** Implement `--file` arg construction: each subprocess receives only refs files permitted for its phase [GAP-003]. Files >50KB passed as `--file` args; files <50KB inlined in prompt
5. **[EXECUTION]** Implement subprocess timeout enforcement via `subprocess.Popen` with external watchdog timer: (1) SIGTERM on timeout, (2) 5s grace, (3) SIGKILL if still alive [NFR-PRD.13/F-004]
6. **[EXECUTION]** Implement launch resilience: retry up to 2 times with exponential backoff (5s, 15s) on transient failures [NFR-PRD.12/GAP-011]
7. **[VERIFICATION]** Verify PrdClaudeProcess constructs correct `--file` args for stage_a_builder vs stage_b_research
8. **[COMPLETION]** Record subprocess argument patterns in evidence

**Acceptance Criteria**:
- [ ] PrdClaudeProcess extends ClaudeProcess with phase-aware `--file` arg scoping [GAP-003]
- [ ] Subprocess timeout enforced via Popen watchdog (SIGTERM -> 5s -> SIGKILL) [NFR-PRD.13/F-004]
- [ ] Launch retry with exponential backoff on transient failures (rate limiting, API unavailability) [NFR-PRD.12/GAP-011]
- [ ] Non-transient failures (invalid args, permission denied) fail immediately without retry

**Validation**:
- `uv run python -c "from superclaude.cli.prd.process import PrdClaudeProcess"`
- Evidence: PrdClaudeProcess importable, extends ClaudeProcess base class

**Risk Drivers**: None

---

## T03.03: Implement logging_.py

**Effort**: XS | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [###-------] 25%
**Requires Confirmation**: Yes (covered by T01.01)
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: None required
**Sub-Agent Delegation**: None

**Deliverable**: D-0015 u2014 `src/superclaude/cli/prd/logging_.py`
**Roadmap Items**: R-024, R-042

**Steps**:
1. **[PLANNING]** Review sprint module's logging patterns for JSONL + Markdown dual logging
2. **[PLANNING]** Review NFR-PRD.10 for logging requirements
3. **[EXECUTION]** Implement `PrdLogger` class with `log_step_start(step_id, step_name)`, `log_step_complete(step_id, result)`, `log_gate_result(step_id, passed, message)`
4. **[EXECUTION]** Write JSONL entries to `{task_dir}/execution-log.jsonl` (machine-readable)
5. **[EXECUTION]** Write Markdown entries to `{task_dir}/execution-log.md` (human-readable)
6. **[VERIFICATION]** Verify dual logging produces both files with correct entry counts
7. **[COMPLETION]** Record log format in evidence

**Acceptance Criteria**:
- [ ] JSONL log entries include timestamp, step_id, event_type, duration_seconds, exit_code
- [ ] Markdown log entries are human-readable with step name, status emoji, duration
- [ ] Both log files written per step execution
- [ ] Log files are append-only (support resume without overwriting)

**Validation**:
- `uv run python -c "from superclaude.cli.prd.logging_ import PrdLogger"`
- Evidence: PrdLogger importable, dual file output verified

**Risk Drivers**: None

---

## T03.04: Implement diagnostics.py

**Effort**: S | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: Preferred: Sequential
**Sub-Agent Delegation**: None

**Deliverable**: D-0016 u2014 `src/superclaude/cli/prd/diagnostics.py`
**Roadmap Items**: R-025, R-036

**Steps**:
1. **[PLANNING]** Review sprint diagnostics module for DiagnosticCollector and FailureClassifier patterns
2. **[PLANNING]** Review NFR-PRD.6 for resume granularity requirements
3. **[EXECUTION]** Implement `DiagnosticCollector` aggregating step results, gate failures, fix cycle history
4. **[EXECUTION]** Implement `FailureClassifier` categorizing failures: TIMEOUT, QA_FAIL, BUDGET_EXHAUSTED, CRASH, GATE_FAIL
5. **[EXECUTION]** Implement `ReportGenerator` producing diagnostic summary with resume command
6. **[EXECUTION]** Implement resume output generation: `generate_resume_command(pipeline_result) -> str` with step-level and per-agent granularity [NFR-PRD.6/GAP-007]
7. **[VERIFICATION]** Verify resume command generation for mid-parallel-group failure case
8. **[COMPLETION]** Record failure categories in evidence

**Acceptance Criteria**:
- [ ] DiagnosticCollector aggregates all step results into structured diagnostic report
- [ ] FailureClassifier maps PrdStepStatus values to user-facing failure categories
- [ ] Resume command includes step ID and suggested budget for mid-run failures [NFR-PRD.6]
- [ ] Per-agent resume: parallel group failure generates command for specific failed agent [GAP-007]

**Validation**:
- `uv run python -c "from superclaude.cli.prd.diagnostics import DiagnosticCollector, FailureClassifier, ReportGenerator"`
- Evidence: 3 classes importable

**Risk Drivers**: None

---

## T03.05: Implement tui.py

**Effort**: XS | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [###-------] 25%
**Requires Confirmation**: Yes (covered by T01.01)
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: None required
**Sub-Agent Delegation**: None

**Deliverable**: D-0017 u2014 `src/superclaude/cli/prd/tui.py`
**Roadmap Items**: R-026

**Steps**:
1. **[PLANNING]** Review sprint module's tui.py for Rich live dashboard patterns
2. **[PLANNING]** Review PrdMonitorState fields for TUI data sources
3. **[EXECUTION]** Implement `PrdTUI` class using Rich Live display with step progress table
4. **[EXECUTION]** Display columns: Step ID, Step Name, Status, Duration, Agent Count, QA Verdict
5. **[EXECUTION]** Implement gate state machine visualization: PENDING -> RUNNING -> PASS/FAIL
6. **[EXECUTION]** Implement fix cycle display: show current fix cycle number and remaining budget
7. **[VERIFICATION]** Verify TUI renders without errors for synthetic PrdMonitorState
8. **[COMPLETION]** Record column layout in evidence

**Acceptance Criteria**:
- [ ] Rich Live display shows step progress table with status, duration, agent count
- [ ] Gate state machine visualized as PENDING -> RUNNING -> PASS/FAIL with color coding
- [ ] Fix cycle counter displayed for QA steps
- [ ] TUI gracefully degrades when terminal is not interactive (e.g., CI/CD)

**Validation**:
- `uv run python -c "from superclaude.cli.prd.tui import PrdTUI"`
- Evidence: PrdTUI importable, renders synthetic state without crash

**Risk Drivers**: None

---

### Checkpoint: Phase 3 / Tasks T03.01u2013T03.05

**Purpose**: Verify all support modules compile before implementing the main executor which depends on all of them.

**Verification**:
- [ ] All 5 source files exist: monitor.py, process.py, logging_.py, diagnostics.py, tui.py
- [ ] All modules importable: `uv run python -c "from superclaude.cli.prd import monitor, process, logging_, diagnostics, tui"`
- [ ] No circular imports between Phase 3 modules or back to Phase 1/2 modules

**Exit Criteria**:
- [ ] 5 modules importable with zero errors
- [ ] monitor.py has no executor/tui imports (GAP-002 verified)
- [ ] process.py extends ClaudeProcess successfully

---

## T03.06: Implement executor.py

**Effort**: L | **Risk**: Low | **Tier**: STRICT | **Confidence**: [######----] 55%
**Requires Confirmation**: Yes (covered by T01.01)
**Critical Path Override**: No
**Verification Method**: Sub-agent (quality-engineer) | Token Budget: 3-5K | Timeout: 60s
**MCP Tools**: Required: Sequential, Serena | Preferred: Context7
**Sub-Agent Delegation**: Required (STRICT tier + integration point)

**Deliverable**: D-0018 u2014 `src/superclaude/cli/prd/executor.py`
**Roadmap Items**: R-027, R-002u2013R-015, R-033u2013R-037, R-040, R-054, R-057

**Steps**:
1. **[PLANNING]** Read sprint executor.py for synchronous supervisor loop pattern
2. **[PLANNING]** Review all 15 FRs for step implementation requirements
3. **[EXECUTION]** Implement `PrdExecutor` class with main execution loop: `run(config: PrdConfig) -> PrdPipelineResult`
4. **[EXECUTION]** Implement sequential step dispatch for Steps 1-9 (Stage A), dynamic step generation for Steps 10-14, and final step 15
5. **[EXECUTION]** Implement parallel dispatch via `ThreadPoolExecutor` with `max_workers=min(len(steps), 10)` [NFR-PRD.7]. Zero-step guard: empty step list returns empty results immediately
6. **[EXECUTION]** Implement fix cycle loop for Steps 11 and 13b: QA FAIL -> parse failures -> spawn gap-fillers -> re-QA. Max cycles from config (3 research, 2 synthesis). Budget deducted from main TurnLedger [F-006]
7. **[EXECUTION]** Implement status classification with sentinel detection: `^EXIT_RECOMMENDATION:` anchored regex with `re.MULTILINE`, skip matches inside fenced code blocks [NFR-PRD.3/F-007]
8. **[EXECUTION]** Implement TurnLedger budget guards before every subprocess launch [NFR-PRD.4]. Budget exhaustion mid-fix-cycle produces `QA_FAIL_EXHAUSTED` with partial results in resume state
9. **[EXECUTION]** Implement signal-aware shutdown: SIGINT/SIGTERM -> graceful state preservation -> resume state written [NFR-PRD.9]
10. **[EXECUTION]** Implement context injection: append `## Prior Step Results` section with verbose summaries of direct deps, terse summaries of transitive deps [NFR-PRD.11/GAP-004]
11. **[VERIFICATION]** Verify executor runs dry-run mode (config validation only, no subprocess launches)
12. **[COMPLETION]** Record step count, parallel group count, fix cycle configuration in evidence

**Acceptance Criteria**:
- [ ] Main execution loop implements all 15 pipeline steps with correct ordering and dependencies
- [ ] Sentinel detection uses `^EXIT_RECOMMENDATION:` anchored regex, skips code blocks [F-007]
- [ ] Fix cycle budget from main TurnLedger, halts with QA_FAIL_EXHAUSTED on exhaustion [F-006]
- [ ] Signal-aware shutdown preserves state for resume [NFR-PRD.9]

**Validation**:
- `uv run python -c "from superclaude.cli.prd.executor import PrdExecutor"`
- Evidence: PrdExecutor importable, dry-run mode exits cleanly

**Risk Drivers**: None
**Notes**: This is the largest and most complex module. It integrates all Phase 1, 2, and 3 modules. Implement last after all dependencies are stable.

---

## T03.07: Write unit tests for executor.py

**Effort**: XS | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: None required
**Sub-Agent Delegation**: None

**Deliverable**: D-0019 u2014 `tests/cli/prd/test_executor.py`
**Roadmap Items**: R-047

**Steps**:
1. **[PLANNING]** Review Section 8.1 test plan for executor.py tests (5 tests specified)
2. **[PLANNING]** Prepare mocks for ClaudeProcess to avoid launching real subprocesses
3. **[EXECUTION]** Implement `test_determine_status_pass`: EXIT_RECOMMENDATION: CONTINUE -> PASS
4. **[EXECUTION]** Implement `test_determine_status_halt`: EXIT_RECOMMENDATION: HALT -> HALT
5. **[EXECUTION]** Implement `test_determine_status_qa_fail`: verdict: FAIL -> QA_FAIL
6. **[EXECUTION]** Implement `test_determine_status_timeout`: exit code 124 -> TIMEOUT
7. **[EXECUTION]** Implement `test_sentinel_not_matched_in_code_block`: EXIT_RECOMMENDATION inside code block is ignored [F-007]
8. **[VERIFICATION]** Run `uv run pytest tests/cli/prd/test_executor.py -v` and verify all 5 tests pass
9. **[COMPLETION]** Record pass count in evidence

**Acceptance Criteria**:
- [ ] 5 test functions implemented matching Section 8.1 specification
- [ ] All tests pass with `uv run pytest tests/cli/prd/test_executor.py -v`
- [ ] Sentinel code block exclusion explicitly tested [F-007]
- [ ] Tests use mocked ClaudeProcess (no real subprocess launches in unit tests)

**Validation**:
- `uv run pytest tests/cli/prd/test_executor.py -v --tb=short`
- Evidence: 5 tests passed, 0 failures

**Risk Drivers**: None

---

## T03.08: Write integration tests

**Effort**: M | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: None required
**Sub-Agent Delegation**: None

**Deliverable**: D-0020 u2014 Integration test suite (9 tests)
**Roadmap Items**: R-050

**Steps**:
1. **[PLANNING]** Review Section 8.2 test plan for all 9 integration tests
2. **[PLANNING]** Design test fixtures: mock directory structures, pre-populated research files, budget configs
3. **[EXECUTION]** Implement `test_prd_pipeline_dry_run`: config construction and validation without execution
4. **[EXECUTION]** Implement `test_prd_pipeline_check_existing_integration`: full existing work detection against real directory
5. **[EXECUTION]** Implement `test_prd_pipeline_budget_exhaustion`: pipeline halts when TurnLedger reports insufficient budget
6. **[EXECUTION]** Implement `test_prd_pipeline_signal_shutdown`: SIGINT triggers graceful shutdown with resume state
7. **[EXECUTION]** Implement `test_prd_pipeline_gate_enforcement`: STRICT gate failures halt pipeline
8. **[EXECUTION]** Implement `test_prd_pipeline_fix_cycle_flow`: QA FAIL -> gap-fill -> re-QA -> PASS flow
9. **[EXECUTION]** Implement `test_prd_pipeline_parallel_execution`: ThreadPoolExecutor runs N agents concurrently
10. **[EXECUTION]** Implement `test_build_investigation_steps_standard_tier`: dynamic step generation correct count [F-012]
11. **[EXECUTION]** Implement `test_build_investigation_steps_heavyweight_tier`: heavyweight produces correct count [F-012]
12. **[VERIFICATION]** Run `uv run pytest tests/cli/prd/test_integration.py -v` and verify all 9 tests pass
13. **[COMPLETION]** Record pass count and execution time in evidence

**Acceptance Criteria**:
- [ ] 9 integration test functions implemented matching Section 8.2 specification
- [ ] All tests pass with `uv run pytest tests/cli/prd/test_integration.py -v`
- [ ] Dynamic step generation tests cover standard and heavyweight tiers [F-012]
- [ ] Budget exhaustion test verifies resume command is generated on halt

**Validation**:
- `uv run pytest tests/cli/prd/test_integration.py -v --tb=short`
- Evidence: 9 tests passed, 0 failures

**Risk Drivers**: None

---

### Checkpoint: End of Phase 3

**Purpose**: Verify the complete execution engine is functional before CLI integration.

**Verification**:
- [ ] All 6 source files exist and are importable: monitor.py, process.py, logging_.py, diagnostics.py, tui.py, executor.py
- [ ] All unit tests pass: `uv run pytest tests/cli/prd/test_executor.py -v`
- [ ] All integration tests pass: `uv run pytest tests/cli/prd/test_integration.py -v`

**Exit Criteria**:
- [ ] 38/38 cumulative tests passing (Phase 1: 20 + Phase 2: 4 + Phase 3: 14)
- [ ] PrdExecutor dry-run mode completes without errors
- [ ] No circular imports across the entire `src/superclaude/cli/prd/` package
