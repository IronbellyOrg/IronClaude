# Phase 3 -- Preflight Executor Core

Implement the core preflight executor that runs commands via `subprocess.run()`, produces evidence artifacts and phase result files, and verifies compatibility with the existing `_determine_phase_status()` parser. This phase depends on both Phase 1 (data model) and Phase 2 (classifier registry). All new code is in `src/superclaude/cli/sprint/preflight.py`.

---

### T03.01 -- Create `preflight.py` with `execute_preflight_phases()`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-025, R-026 |
| Why | The core preflight executor filters python-mode phases, parses their tasks, executes commands via `subprocess.run(shell=False, capture_output=True, timeout=120)`, captures results, and applies classifiers. This is the central function of the feature. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | Performance (subprocess execution), cross-cutting scope (touches parsing + execution + classification) |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0015, D-0016, D-0037 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0015/evidence.md
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0015/spec.md
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0015/notes.md

**Deliverables:**
- `src/superclaude/cli/sprint/preflight.py` with `execute_preflight_phases(config) -> list[PhaseResult]`
- Phase filtering (`execution_mode == "python"`), task iteration, `subprocess.run(shell=False, capture_output=True, timeout=120)` execution
- Command tokenization via `shlex.split()`, stdout/stderr/exit_code/duration capture, classifier application via `run_classifier()`

**Steps:**
1. **[PLANNING]** Read `PhaseResult`, `TaskResult`, and config structures to understand return types and input contract
2. **[PLANNING]** Read `run_classifier()` in `classifiers.py` to understand classifier invocation interface
3. **[EXECUTION]** Create `src/superclaude/cli/sprint/preflight.py`
4. **[EXECUTION]** Implement `execute_preflight_phases(config) -> list[PhaseResult]`:
   - Filter `config.active_phases` where `phase.execution_mode == "python"`
   - For each phase: call `parse_tasklist()` to get tasks
   - For each task: `shlex.split(task.command)`, `subprocess.run(cmd, shell=False, capture_output=True, timeout=120, cwd=config.working_dir)`
   - Capture `stdout.decode()`, `stderr.decode()`, `returncode`, wall-clock `time.monotonic()` duration
   - Apply `run_classifier(task.classifier, exit_code, stdout, stderr)`
   - Build `TaskResult` per task, `PhaseResult` per phase with `PhaseStatus.PREFLIGHT_PASS` or failure
5. **[EXECUTION]** Handle `subprocess.TimeoutExpired`: set exit_code to -1, classification to `"timeout"`
6. **[VERIFICATION]** Test with `echo hello` command: verify stdout captured, exit_code 0, classification "pass"
7. **[VERIFICATION]** Test with `false` command: verify exit_code 1, classification "fail"
8. **[COMPLETION]** Record function signature, error handling, and subprocess configuration in evidence

**Acceptance Criteria:**
- `execute_preflight_phases(config)` returns `list[PhaseResult]` for all python-mode phases
- Each task is executed via `subprocess.run(shell=False, capture_output=True, timeout=120)`
- Commands are tokenized with `shlex.split()` before execution
- `subprocess.TimeoutExpired` is handled gracefully with exit_code -1 and `"timeout"` classification

**Validation:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v -k "preflight and not evidence"` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0015/evidence.md

**Dependencies:** T01.01, T01.02, T01.03, T01.05, T01.06, T02.01, T02.02, T02.03
**Rollback:** Delete `src/superclaude/cli/sprint/preflight.py`

---

### T03.02 -- Implement Evidence Artifact Writing

| Field | Value |
|---|---|
| Roadmap Item IDs | R-027 |
| Why | Each preflight task must produce an evidence artifact file containing the command, exit code, stdout, stderr, duration, and classification for traceability and debugging. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [████████--] 82% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0017, D-0038 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0017/evidence.md
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0017/spec.md

**Deliverables:**
- Evidence artifact files written per task to `artifacts/<task_id>/evidence.md` containing: command, exit code, stdout (truncated 10KB), stderr (truncated 2KB), duration, classification
- Directory creation via `mkdir(parents=True, exist_ok=True)` for artifact paths

**Steps:**
1. **[PLANNING]** Review the artifact directory structure and how task IDs map to paths
2. **[PLANNING]** Design the evidence file markdown format: command, exit_code, stdout, stderr, duration, classification
3. **[EXECUTION]** Add `_write_evidence(task_id, command, exit_code, stdout, stderr, duration, classification, artifacts_dir)` to `preflight.py`
4. **[EXECUTION]** Truncate stdout at 10KB and stderr at 2KB with `[truncated at N bytes]` marker
5. **[EXECUTION]** Create `artifacts/<task_id>/` via `Path.mkdir(parents=True, exist_ok=True)`
6. **[EXECUTION]** Write `evidence.md` with all fields in a structured markdown format
7. **[VERIFICATION]** Test with 15KB stdout: verify truncation to 10KB with marker
8. **[COMPLETION]** Record evidence file format and truncation behavior in evidence

**Acceptance Criteria:**
- Evidence file at `artifacts/<task_id>/evidence.md` contains command, exit_code, stdout, stderr, duration, and classification
- stdout exceeding 10KB is truncated with `[truncated at 10240 bytes]` marker appended
- stderr exceeding 2KB is truncated with `[truncated at 2048 bytes]` marker appended
- `mkdir(parents=True, exist_ok=True)` is used for directory creation (no errors on existing dirs)

**Validation:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v -k evidence` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0017/evidence.md

**Dependencies:** T03.01
**Rollback:** Remove `_write_evidence()` function; evidence files are not produced

---

### T03.03 -- Implement Phase Result File Generation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-028 |
| Why | Preflight must produce `phase-N-result.md` files using `AggregatedPhaseReport.to_markdown()` with YAML frontmatter including `source: preflight` and `EXIT_RECOMMENDATION`, ensuring zero parser changes in `_determine_phase_status()`. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | Data format compatibility (R-056), breaking change risk if format diverges |
| Tier | STRICT |
| Confidence | [████████░-] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0018, D-0039 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0018/evidence.md
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0018/spec.md

**Deliverables:**
- Phase result file written to `phase-N-result.md` via `AggregatedPhaseReport.to_markdown()` for each preflight phase
- YAML frontmatter includes `source: preflight` and `EXIT_RECOMMENDATION: CONTINUE` or `HALT`

**Steps:**
1. **[PLANNING]** Read `AggregatedPhaseReport` class and its `to_markdown()` method to understand the output format
2. **[PLANNING]** Read `_determine_phase_status()` to understand what fields it parses from result files
3. **[EXECUTION]** After all tasks in a phase complete, build an `AggregatedPhaseReport` from `TaskResult` objects
4. **[EXECUTION]** Call `report.to_markdown()` to generate the result file content
5. **[EXECUTION]** Inject `source: preflight` into the YAML frontmatter
6. **[EXECUTION]** Set `EXIT_RECOMMENDATION` to `CONTINUE` if all tasks passed, `HALT` if any failed
7. **[VERIFICATION]** Parse the generated file with `_determine_phase_status()` and verify it returns the expected status
8. **[COMPLETION]** Record the frontmatter fields and format compatibility in evidence

**Acceptance Criteria:**
- Phase result file is written to `phase-N-result.md` using `AggregatedPhaseReport.to_markdown()` (no custom format generation, filename matches `_determine_phase_status()` file lookup convention)
- YAML frontmatter includes `source: preflight` field
- `EXIT_RECOMMENDATION` is `CONTINUE` when all tasks pass, `HALT` when any task fails
- Generated file is parseable by `_determine_phase_status()` with no modifications to that function

**Validation:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v -k result_file` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0018/evidence.md

**Dependencies:** T03.01
**Rollback:** Remove result file generation; preflight phases produce no result files
**Notes:** This is the highest-risk boundary (RISK-001). Result format is treated as a locked contract.

---

### T03.04 -- Verify `_determine_phase_status()` Compatibility

| Field | Value |
|---|---|
| Roadmap Item IDs | R-029 |
| Why | The existing `_determine_phase_status()` function must parse preflight-generated result files identically to Claude-generated ones. This is the critical compatibility check that prevents false halts or broken sprint completion. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | Data format compatibility (R-056), breaking change if format diverges |
| Tier | STRICT |
| Confidence | [████████░-] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0019 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0019/evidence.md

**Deliverables:**
- Verification that `_determine_phase_status()` parses preflight-generated result files correctly with no code modifications

**Steps:**
1. **[PLANNING]** Read `_determine_phase_status()` to catalog all fields it extracts from result files
2. **[PLANNING]** Generate a sample preflight result file using T03.03 logic
3. **[EXECUTION]** Pass the preflight-generated result file to `_determine_phase_status()`
4. **[EXECUTION]** Assert the returned status matches expectations (CONTINUE -> success, HALT -> failure)
5. **[EXECUTION]** Compare with a Claude-generated result file to confirm identical parsing behavior
6. **[VERIFICATION]** Create a minimal Claude-origin result file sample and compare `_determine_phase_status()` output with the preflight-generated file from Step 4
7. **[COMPLETION]** Document all parsed fields and their values in evidence

**Acceptance Criteria:**
- `_determine_phase_status()` returns correct status for a preflight-generated result file with `EXIT_RECOMMENDATION: CONTINUE`
- `_determine_phase_status()` returns correct status for a preflight-generated result file with `EXIT_RECOMMENDATION: HALT`
- No modifications to `_determine_phase_status()` are required
- Parsing behavior is identical for preflight-origin and Claude-origin result files

**Validation:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v -k compatibility` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0019/evidence.md

**Dependencies:** T03.03
**Rollback:** Not applicable (verification-only task; no code changes)
**Notes:** If compatibility issues appear, block release per RISK-001 contingency. Do not patch `_determine_phase_status()` as a shortcut.

---

### Checkpoint: Phase 3 / Tasks T03.01-T03.04

**Purpose:** Verify the core preflight executor, evidence writing, result file generation, and compatibility with `_determine_phase_status()` are all working before proceeding to integration tests.
**Checkpoint Report Path:** .dev/releases/current/v2.25.5-PreFlightExecutor/checkpoints/CP-P03-T01-T04.md
**Verification:**
- `execute_preflight_phases()` successfully executes `echo hello` and returns `PhaseResult` with `PREFLIGHT_PASS`
- Evidence artifacts are written with correct structure and truncation
- `_determine_phase_status()` parses preflight result files with no modifications
**Exit Criteria:**
- All four tasks (T03.01-T03.04) have evidence artifacts
- Subprocess execution, evidence writing, and result file generation are operational
- Compatibility with existing result parser is confirmed

---

### T03.05 -- Integration Tests for Preflight Execution and Timeout

| Field | Value |
|---|---|
| Roadmap Item IDs | R-030, R-031 |
| Why | Integration tests validate that the preflight executor correctly runs commands and captures output, and that the timeout mechanism triggers after the configured duration. |
| Effort | S |
| Risk | Low |
| Risk Drivers | Performance (timeout behavior) |
| Tier | STANDARD |
| Confidence | [████████--] 82% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0020 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0020/evidence.md

**Deliverables:**
- Integration test: preflight executes `echo hello` and captures stdout `"hello\n"`, exit_code 0, classification `"pass"`
- Integration test: command exceeding timeout triggers `subprocess.TimeoutExpired` handling with exit_code -1

**Steps:**
1. **[PLANNING]** Design test fixtures with real subprocess execution (no mocking for integration tests)
2. **[PLANNING]** Plan timeout test with `sleep 5` and a 1-second timeout override
3. **[EXECUTION]** Write `test_preflight_echo_hello()` that runs `echo hello` and asserts captured output
4. **[EXECUTION]** Write `test_preflight_timeout()` that runs `sleep 5` with timeout=1 and asserts graceful handling
5. **[VERIFICATION]** Run both tests and verify they pass reliably
6. **[COMPLETION]** Record test configurations and results in evidence

**Acceptance Criteria:**
- `test_preflight_echo_hello` passes: stdout contains `"hello"`, exit_code is 0, classification is `"pass"`
- `test_preflight_timeout` passes: timeout triggers, exit_code is -1, classification is `"timeout"`
- Tests use real subprocess execution, not mocks
- Tests marked with `@pytest.mark.integration`

**Validation:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v -k "echo or timeout"` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0020/evidence.md

**Dependencies:** T03.01
**Rollback:** Delete the test functions

---

### T03.06 -- Integration Tests for Evidence and Result File Structure

| Field | Value |
|---|---|
| Roadmap Item IDs | R-032, R-033 |
| Why | Integration tests validate that evidence files contain the required structure (command, exit_code, stdout, stderr, duration, classification) and that result files are parseable by `_determine_phase_status()`. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | Data format compatibility (R-056) |
| Tier | STANDARD |
| Confidence | [████████--] 82% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0021 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0021/evidence.md

**Deliverables:**
- Integration test: evidence file written with correct structure (command, exit_code, stdout, stderr, duration, classification fields present)
- Integration test: result file generated by preflight is parseable by `_determine_phase_status()` and returns expected status

**Steps:**
1. **[PLANNING]** Define expected evidence file structure as a fixture
2. **[PLANNING]** Identify the exact fields `_determine_phase_status()` requires in result files
3. **[EXECUTION]** Write `test_evidence_file_structure()` that runs a preflight task and reads the evidence file
4. **[EXECUTION]** Assert all required fields (command, exit_code, stdout, stderr, duration, classification) are present
5. **[EXECUTION]** Write `test_result_file_parseable()` that generates a result file and passes it to `_determine_phase_status()`
6. **[VERIFICATION]** Run both tests and verify they pass
7. **[COMPLETION]** Record file formats and parsed fields in evidence

**Acceptance Criteria:**
- Evidence file contains all 6 required fields: command, exit_code, stdout, stderr, duration, classification
- Result file generated by preflight is successfully parsed by `_determine_phase_status()`
- `_determine_phase_status()` returns the expected status (success for all-pass, failure for any-fail)
- Tests use temporary directories and leave no persistent files

**Validation:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v -k "evidence_structure or result_parseable"` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0021/evidence.md

**Dependencies:** T03.02, T03.03, T03.04
**Rollback:** Delete the test functions

---

### T03.07 -- Unit Tests for Truncation and Compatibility Fixture

| Field | Value |
|---|---|
| Roadmap Item IDs | R-034, R-035 |
| Why | Unit tests validate stdout/stderr truncation at 10KB/2KB limits, and a compatibility fixture confirms that both preflight-origin and Claude-origin result files parse identically through `_determine_phase_status()`. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [████████░-] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | No |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0022 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0022/evidence.md

**Deliverables:**
- Unit test: stdout truncation at 10KB produces output ending with `[truncated at 10240 bytes]`
- Unit test: stderr truncation at 2KB produces output ending with `[truncated at 2048 bytes]`
- Compatibility fixture: preflight-origin and Claude-origin result files produce identical `_determine_phase_status()` output

**Steps:**
1. **[PLANNING]** Review truncation logic in `_write_evidence()` (T03.02)
2. **[PLANNING]** Design compatibility fixture with pre-built result file samples
3. **[EXECUTION]** Write `test_stdout_truncation_10kb()` with 15KB input, assert output is 10KB + marker
4. **[EXECUTION]** Write `test_stderr_truncation_2kb()` with 5KB input, assert output is 2KB + marker
5. **[EXECUTION]** Write `test_result_file_compatibility()` comparing preflight and Claude result file parsing
6. **[VERIFICATION]** Run all tests and verify compatibility fixture passes
7. **[COMPLETION]** Record truncation thresholds and compatibility results in evidence

**Acceptance Criteria:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v -k "truncation or compatibility"` exits 0
- Truncation tests verify exact byte limits (10240 for stdout, 2048 for stderr)
- Compatibility fixture proves `_determine_phase_status()` returns identical results for both file origins
- No modifications to `_determine_phase_status()` needed

**Validation:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v -k "truncation or compatibility"` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0022/evidence.md

**Dependencies:** T03.02, T03.03, T03.04
**Rollback:** Delete the test functions and fixture

---

### Checkpoint: End of Phase 3

**Purpose:** Gate for Phase 4: confirm the preflight executor core is complete with all evidence artifacts, result file generation, and comprehensive test coverage.
**Checkpoint Report Path:** .dev/releases/current/v2.25.5-PreFlightExecutor/checkpoints/CP-P03-END.md
**Verification:**
- `execute_preflight_phases()` runs commands, captures output, applies classifiers, and produces PhaseResult objects
- Evidence artifacts and result files are generated with correct structure
- `_determine_phase_status()` compatibility is confirmed via shared fixture
**Exit Criteria:**
- All 7 tasks (T03.01-T03.07) have evidence artifacts
- Integration tests for execution, timeout, evidence, and result parsing all pass
- Compatibility fixture validates format contract between preflight and Claude origins
