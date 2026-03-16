# Phase 4 -- Sprint Integration

Integrate the preflight executor into the sprint orchestration loop, implement skip mode, merge results, and validate that mixed-mode sprints work correctly end-to-end. All changes are in `src/superclaude/cli/sprint/process.py` with integration tests covering the full sprint lifecycle.

---

### T04.01 -- Integrate `execute_preflight_phases()` into `execute_sprint()`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-037, R-038 |
| Why | The preflight executor must be called in `execute_sprint()` before the main phase loop, and the main loop must skip phases where `execution_mode == "python"` since they are already handled by preflight. Single insertion point ensures minimal blast radius. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | Cross-cutting scope (orchestration), breaking change risk (R-060) |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0023, D-0040 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0023/evidence.md
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0023/spec.md

**Deliverables:**
- `execute_preflight_phases(config)` call added to `execute_sprint()` in `src/superclaude/cli/sprint/process.py` before the main phase loop
- Main loop skip condition: `if phase.execution_mode == "python": continue` (already handled by preflight)

**Steps:**
1. **[PLANNING]** Read `execute_sprint()` in `src/superclaude/cli/sprint/process.py` to identify the exact insertion point before the main loop
2. **[PLANNING]** Identify how `PhaseResult` objects are collected in the current loop
3. **[EXECUTION]** Add `preflight_results = execute_preflight_phases(config)` call before the main phase loop
4. **[EXECUTION]** Add skip condition in the main loop: `if phase.execution_mode == "python": continue`
5. **[EXECUTION]** Import `execute_preflight_phases` from `preflight` module
6. **[VERIFICATION]** Verify that removing the single `execute_preflight_phases()` call line reverts to all-Claude behavior
7. **[VERIFICATION]** Run `uv run pytest tests/ -v` to confirm no regressions
8. **[COMPLETION]** Record the exact insertion point (file, line number) in evidence

**Acceptance Criteria:**
- `execute_preflight_phases(config)` is called exactly once in `execute_sprint()`, before the main phase loop
- Phases with `execution_mode == "python"` are skipped in the main loop
- Removing the `execute_preflight_phases(config)` call (single line) reverts to all-Claude behavior
- No changes to the Claude-mode execution code path

**Validation:**
- `uv run pytest tests/ -v --tb=short` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0023/evidence.md

**Dependencies:** T03.01, T03.03
**Rollback:** Remove the `execute_preflight_phases(config)` call and the skip condition (single-line rollback per R-051)

---

### T04.02 -- Implement Skip Mode with `PhaseStatus.SKIPPED`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-039 |
| Why | Phases with `execution_mode == "skip"` must be skipped entirely with `PhaseStatus.SKIPPED` status, no subprocess launched, providing a way to exclude phases from execution without removing them from the tasklist. |
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
| Deliverable IDs | D-0024 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0024/evidence.md

**Deliverables:**
- Skip mode: phases with `execution_mode == "skip"` produce `PhaseStatus.SKIPPED` with no subprocess or Claude execution

**Steps:**
1. **[PLANNING]** Read the main phase loop in `execute_sprint()` to identify where skip logic should be added
2. **[PLANNING]** Confirm `PhaseStatus.SKIPPED` already exists in the enum (or add if needed)
3. **[EXECUTION]** Add skip condition: `if phase.execution_mode == "skip"`: create a `PhaseResult` with `PhaseStatus.SKIPPED` and continue
4. **[EXECUTION]** Ensure no subprocess is launched and no `ClaudeProcess` is instantiated for skip-mode phases
5. **[VERIFICATION]** Test with a skip-mode phase: assert `PhaseStatus.SKIPPED` returned and no side effects
6. **[COMPLETION]** Record skip logic placement in evidence

**Acceptance Criteria:**
- Phases with `execution_mode == "skip"` produce `PhaseResult` with `PhaseStatus.SKIPPED`
- No subprocess is launched for skip-mode phases
- No `ClaudeProcess` is instantiated for skip-mode phases
- Skip-mode PhaseResult object is created with correct status and returned from the skip handler

**Validation:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v -k skip` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0024/evidence.md

**Dependencies:** T01.01, T01.05, T04.01
**Rollback:** Remove the skip condition; skip-mode phases will be treated as Claude-mode

---

### T04.03 -- Merge Preflight Results with Main Loop Results

| Field | Value |
|---|---|
| Roadmap Item IDs | R-040 |
| Why | The final sprint outcome must combine preflight `PhaseResult` objects with main loop results in the correct phase order, ensuring the sprint summary and exit logic see all phases. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | Cross-cutting scope (result aggregation affects sprint exit logic) |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0025, D-0041 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0025/evidence.md
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0025/spec.md

**Deliverables:**
- Combined `PhaseResult` list merging preflight results and main loop results in phase order
- Phase ordering preserved: preflight results inserted at their original phase indices

**Steps:**
1. **[PLANNING]** Read how `PhaseResult` objects are collected and used for sprint outcome/exit logic
2. **[PLANNING]** Design merge strategy that preserves original phase ordering from config
3. **[EXECUTION]** After main loop completes, merge `preflight_results` and `main_loop_results` into a single ordered list
4. **[EXECUTION]** Ensure phase ordering matches the original `config.active_phases` order
5. **[VERIFICATION]** Test with 3 phases (python, claude, skip): verify combined result list has 3 entries in correct order
6. **[COMPLETION]** Record merge strategy and ordering guarantees in evidence

**Acceptance Criteria:**
- Combined result list contains one `PhaseResult` per phase in the original phase order defined by the sprint config
- Preflight results (python-mode) appear at their original phase indices
- Main loop results (claude-mode) appear at their original phase indices
- Skip-mode results appear at their original phase indices

**Validation:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v -k merge` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0025/evidence.md

**Dependencies:** T04.01, T04.02
**Rollback:** Remove merge logic; only main loop results are used (preflight results discarded)

---

### T04.04 -- Verify Logger and TUI Handle New Statuses

| Field | Value |
|---|---|
| Roadmap Item IDs | R-041 |
| Why | The sprint logger and TUI display must handle `PREFLIGHT_PASS` and `SKIPPED` statuses without errors, displaying them correctly in progress output and final summaries. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
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
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0026/evidence.md

**Deliverables:**
- Logger and TUI correctly display `PREFLIGHT_PASS` and `SKIPPED` statuses without errors or unhandled exceptions

**Steps:**
1. **[PLANNING]** Read the logger and TUI code to identify where `PhaseStatus` values are rendered
2. **[PLANNING]** Identify any switch/match statements or string formatting that might break on new status values
3. **[EXECUTION]** Test logger output with `PhaseStatus.PREFLIGHT_PASS` and `PhaseStatus.SKIPPED`
4. **[EXECUTION]** Fix any unhandled status errors in display logic (if found)
5. **[VERIFICATION]** Run a mock sprint with mixed statuses and verify clean output
6. **[COMPLETION]** Record display behavior for new statuses in evidence

**Acceptance Criteria:**
- Logger does not raise exceptions when encountering `PREFLIGHT_PASS` or `SKIPPED` statuses
- TUI displays `PREFLIGHT_PASS` and `SKIPPED` with appropriate formatting
- Sprint summary includes all three status types (pass, preflight_pass, skipped) in its output
- No unhandled `KeyError` or `ValueError` from status rendering

**Validation:**
- `uv run pytest tests/ -v --tb=short` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0026/evidence.md

**Dependencies:** T01.05, T04.01, T04.02, T04.03
**Rollback:** Revert any display logic changes

---

### Checkpoint: Phase 4 / Tasks T04.01-T04.04

**Purpose:** Verify sprint integration, skip mode, result merging, and status display are all working before proceeding to comprehensive integration tests.
**Checkpoint Report Path:** .dev/releases/current/v2.25.5-PreFlightExecutor/checkpoints/CP-P04-T01-T04.md
**Verification:**
- `execute_sprint()` calls `execute_preflight_phases()` before the main loop
- Skip-mode phases produce `SKIPPED` status with no execution
- Combined result list preserves phase ordering
**Exit Criteria:**
- All four tasks (T04.01-T04.04) have evidence artifacts
- Mixed-mode sprint (python + claude + skip) produces correct combined results
- Logger and TUI handle all status types without errors

---

### T04.05 -- Integration Tests for Mixed-Mode Sprint Execution

| Field | Value |
|---|---|
| Roadmap Item IDs | R-042, R-043, R-044, R-045 |
| Why | Comprehensive integration tests validate the complete sprint lifecycle with mixed execution modes, rollback behavior, skip mode, and zero ClaudeProcess instantiation for python-mode phases. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | Cross-cutting scope (end-to-end), performance (subprocess execution) |
| Tier | STRICT |
| Confidence | [████████░-] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0027, D-0042 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0027/evidence.md
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0027/spec.md

**Deliverables:**
- Integration test: sprint with mixed `python`/`claude`/`skip` phases produces correct combined results
- Integration test: removing `execute_preflight_phases()` call reverts to all-Claude behavior
- Integration test: `skip` phases produce `SKIPPED` status with no subprocess launched
- Integration test: zero `ClaudeProcess` instantiation for python-mode phases

**Steps:**
1. **[PLANNING]** Design a test tasklist with 3 phases: python (echo hello), claude (mock), skip
2. **[PLANNING]** Plan assertions for each execution mode's expected behavior
3. **[EXECUTION]** Write `test_mixed_mode_sprint()` with python + claude + skip phases
4. **[EXECUTION]** Write `test_rollback_removes_preflight()` patching out the preflight call
5. **[EXECUTION]** Write `test_skip_no_subprocess()` asserting no subprocess launched for skip phases
6. **[EXECUTION]** Write `test_python_no_claude_process()` asserting `ClaudeProcess` is not instantiated for python phases
7. **[VERIFICATION]** Run all integration tests and verify they pass
8. **[COMPLETION]** Record test configurations and assertions in evidence

**Acceptance Criteria:**
- `test_mixed_mode_sprint` passes: combined results contain PREFLIGHT_PASS, mock-claude-pass, and SKIPPED in order
- `test_rollback_removes_preflight` passes: without preflight call, all phases are treated as claude-mode
- `test_skip_no_subprocess` passes: skip phases produce SKIPPED with zero subprocess calls
- `test_python_no_claude_process` passes: python phases do not instantiate `ClaudeProcess`

**Validation:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v -m integration` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0027/evidence.md

**Dependencies:** T04.01, T04.02, T04.03, T04.04
**Rollback:** Delete the test functions

---

### T04.06 -- Regression Test for All-Claude Tasklist Behavior

| Field | Value |
|---|---|
| Roadmap Item IDs | R-046 |
| Why | A regression test confirms that an all-Claude tasklist (no python/skip phases) behaves identically to pre-feature behavior, ensuring the preflight feature has zero impact on existing workflows. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | Breaking change risk (R-060), system-wide regression |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | No |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0028 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0028/evidence.md

**Deliverables:**
- Regression test: all-Claude tasklist (no python/skip phases) produces identical behavior to pre-feature baseline

**Steps:**
1. **[PLANNING]** Identify a representative all-Claude tasklist from existing tests or fixtures
2. **[PLANNING]** Define "identical behavior" metrics: same phase statuses, same result file count, no preflight calls
3. **[EXECUTION]** Write `test_all_claude_regression()` that runs a sprint with only claude-mode phases
4. **[EXECUTION]** Assert `execute_preflight_phases()` returns an empty list (no python phases to run)
5. **[EXECUTION]** Assert all phases go through the main Claude loop as before
6. **[VERIFICATION]** Compare output with a pre-feature baseline run
7. **[COMPLETION]** Record regression test results in evidence

**Acceptance Criteria:**
- `test_all_claude_regression` passes: all-Claude tasklist executes through the main loop only
- `execute_preflight_phases()` returns empty list when no python-mode phases exist
- No behavioral change observed compared to pre-feature execution
- Existing test suite passes without modifications: `uv run pytest tests/ -v`

**Validation:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v -k regression` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0028/evidence.md

**Dependencies:** T04.01
**Rollback:** Delete the test function

---

### Checkpoint: End of Phase 4

**Purpose:** Gate for Phase 5: confirm end-to-end sprint integration with mixed modes, regression safety, and comprehensive integration test coverage.
**Checkpoint Report Path:** .dev/releases/current/v2.25.5-PreFlightExecutor/checkpoints/CP-P04-END.md
**Verification:**
- Mixed-mode sprint (python + claude + skip) produces correct combined results
- All-Claude regression test confirms zero behavioral change for existing workflows
- Zero `ClaudeProcess` instantiation for python-mode phases verified
**Exit Criteria:**
- All 6 tasks (T04.01-T04.06) have evidence artifacts
- Integration tests for mixed-mode, rollback, skip, and regression all pass
- Single-line rollback property confirmed (remove `execute_preflight_phases()` call)
