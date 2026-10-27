# Phase 5 -- Validation and Release

Run the full test suite, verify all success criteria (SC-001 through SC-007), execute lint/format/sync checks, update documentation, and validate release gate criteria. This phase produces no new code -- it validates and polishes the work from Phases 1-4.

---

### T05.01 -- Run Full Test Suite (14 Unit + 8 Integration)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-048 |
| Why | The complete test suite must pass with 14 unit tests and 8 integration tests covering all preflight functionality before any release gate criteria can be checked. |
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
| Deliverable IDs | D-0029 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0029/evidence.md

**Deliverables:**
- Full test suite passing: `uv run pytest tests/cli/sprint/test_preflight.py -v` exits 0 with 14 unit tests and 8 integration tests

**Steps:**
1. **[PLANNING]** Review the test file to confirm expected test count (14 unit + 8 integration)
2. **[PLANNING]** Check for any skipped or xfail markers that might mask failures
3. **[EXECUTION]** Run `uv run pytest tests/cli/sprint/test_preflight.py -v --tb=long`
4. **[EXECUTION]** Run `uv run pytest tests/ -v --tb=short` to check for regressions across the full suite
5. **[VERIFICATION]** Confirm 22 tests pass with 0 failures, 0 errors, 0 skipped
6. **[COMPLETION]** Record test counts and any notable results in evidence

**Acceptance Criteria:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v` exits 0 with 14 unit tests passing
- `uv run pytest tests/cli/sprint/test_preflight.py -v -m integration` exits 0 with 8 integration tests passing
- `uv run pytest tests/ -v` exits 0 with no regressions in the existing test suite
- No tests skipped or marked xfail without documented reason

**Validation:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0029/evidence.md

**Dependencies:** T01.07, T01.08, T02.04, T03.05, T03.06, T03.07, T04.05, T04.06
**Rollback:** Not applicable (validation-only task)

---

### T05.02 -- Verify SC-001: Performance Criterion

| Field | Value |
|---|---|
| Roadmap Item IDs | R-049 |
| Why | SC-001 requires python-mode phases to complete in <30s with zero API tokens consumed, validating the core value proposition of eliminating token waste on deterministic tasks. |
| Effort | S |
| Risk | Low |
| Risk Drivers | Performance (latency) |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0030 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0030/evidence.md

**Deliverables:**
- SC-001 verified: python-mode phase with 5 EXEMPT-tier tasks completes in <30s with zero API token consumption

**Steps:**
1. **[PLANNING]** Design a benchmark tasklist with 5 EXEMPT-tier python-mode tasks (e.g., `echo` commands)
2. **[PLANNING]** Identify how to measure wall-clock time and confirm zero token usage
3. **[EXECUTION]** Run the benchmark tasklist through `execute_preflight_phases()`
4. **[EXECUTION]** Measure wall-clock duration with `time.monotonic()`
5. **[EXECUTION]** Assert no API calls were made (no `ClaudeProcess` instantiation, no HTTP requests)
6. **[VERIFICATION]** Confirm duration < 30s and token count == 0
7. **[COMPLETION]** Record benchmark results (duration, task count, token count) in evidence

**Acceptance Criteria:**
- 5 EXEMPT-tier python-mode tasks complete in <30s wall-clock time
- Zero API tokens consumed during preflight execution
- No `ClaudeProcess` instantiated during the benchmark
- Benchmark results are reproducible (run 3 times, all under 30s)

**Validation:**
- Manual check: benchmark duration < 30s and token count == 0 verified by test output
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0030/evidence.md

**Dependencies:** T03.01, T04.01
**Rollback:** Not applicable (validation-only task)

---

### T05.03 -- Verify SC-002: Nested Claude Without Deadlock

| Field | Value |
|---|---|
| Roadmap Item IDs | R-050 |
| Why | SC-002 validates that `subprocess.run()` with `capture_output=True` can execute nested `claude --print -p "hello"` without deadlock from pipe buffer exhaustion, with the 120s timeout as backstop. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | Performance (deadlock risk), cross-cutting (nested subprocess) |
| Tier | STANDARD |
| Confidence | [████████--] 82% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0031 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0031/evidence.md

**Deliverables:**
- SC-002 verified: nested `claude --print -p "hello"` executes without deadlock, produces output, and completes within timeout

**Steps:**
1. **[PLANNING]** Review the deadlock risk: `capture_output=True` uses pipes that could fill if output is large
2. **[PLANNING]** Confirm `claude --print` is available in the execution environment
3. **[EXECUTION]** Run a preflight task with command `claude --print -p "hello"`
4. **[EXECUTION]** Assert the command completes without hanging (within 120s timeout)
5. **[EXECUTION]** Assert stdout contains a response
6. **[VERIFICATION]** Confirm no deadlock: command completes within the 120s timeout
7. **[COMPLETION]** Record execution time and output in evidence

**Acceptance Criteria:**
- `claude --print -p "hello"` executes successfully via `subprocess.run()` with `capture_output=True`
- Command completes without deadlock within the 120s timeout
- stdout contains a non-empty response
- No pipe buffer exhaustion observed

**Validation:**
- Manual check: nested `claude --print` completes without hanging, verified by test output
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0031/evidence.md

**Dependencies:** T03.01
**Rollback:** Not applicable (validation-only task)
**Notes:** Per R-061, large output from nested Claude could theoretically fill pipe buffers. The 120s timeout is the backstop.

---

### T05.04 -- Verify SC-007: Single-Line Rollback

| Field | Value |
|---|---|
| Roadmap Item IDs | R-051 |
| Why | SC-007 validates the single-line rollback property: removing the `execute_preflight_phases()` call from `execute_sprint()` reverts to all-Claude behavior with the existing test suite passing unchanged. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | No |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0032 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0032/evidence.md

**Deliverables:**
- SC-007 verified: removing `execute_preflight_phases(config)` call line and running existing test suite passes

**Steps:**
1. **[PLANNING]** Identify the exact line in `execute_sprint()` that calls `execute_preflight_phases()`
2. **[PLANNING]** Plan a temporary patch to comment out the line
3. **[EXECUTION]** Comment out the `execute_preflight_phases(config)` call
4. **[EXECUTION]** Run `uv run pytest tests/ -v --ignore=tests/cli/sprint/test_preflight.py` (existing tests, excluding preflight-specific tests)
5. **[EXECUTION]** Verify all existing tests pass with no modifications
6. **[EXECUTION]** Restore the `execute_preflight_phases(config)` call
7. **[VERIFICATION]** Confirm the rollback is exactly one line (comment/uncomment)
8. **[COMPLETION]** Record the rollback line and test results in evidence

**Acceptance Criteria:**
- Commenting out a single line (`execute_preflight_phases(config)`) reverts to all-Claude behavior
- Existing test suite (excluding preflight-specific tests) passes with the line removed
- No other code changes required for rollback
- Rollback line restored after verification

**Validation:**
- Manual check: single-line rollback demonstrated and test suite passes without preflight call
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0032/evidence.md

**Dependencies:** T04.01
**Rollback:** Not applicable (verification-only task)

---

### Checkpoint: Phase 5 / Tasks T05.01-T05.04

**Purpose:** Verify all success criteria (SC-001, SC-002, SC-007) and full test suite before proceeding to lint/sync and release gate.
**Checkpoint Report Path:** .dev/releases/current/v2.25.5-PreFlightExecutor/checkpoints/CP-P05-T01-T04.md
**Verification:**
- Full test suite passes: 14 unit + 8 integration tests
- SC-001: <30s, zero tokens for python-mode phase
- SC-002: nested `claude --print` works without deadlock
**Exit Criteria:**
- All four tasks (T05.01-T05.04) have evidence artifacts
- All three success criteria verified
- Single-line rollback demonstrated

---

### T05.05 -- Run Lint, Format, Sync-Dev, Verify-Sync

| Field | Value |
|---|---|
| Roadmap Item IDs | R-052, R-053 |
| Why | Code quality gates must pass before release: linting catches style issues, formatting ensures consistency, and sync-dev/verify-sync confirms source-of-truth alignment between `src/` and `.claude/`. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | LIGHT |
| Confidence | [████████░-] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0033 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0033/evidence.md

**Deliverables:**
- `make lint`, `make format`, `make sync-dev`, and `make verify-sync` all exit 0

**Steps:**
1. **[PLANNING]** Confirm all new files (`classifiers.py`, `preflight.py`, `test_preflight.py`) are included in lint/format scope
2. **[EXECUTION]** Run `make lint` and fix any issues
3. **[EXECUTION]** Run `make format` and commit any formatting changes
4. **[EXECUTION]** Run `make sync-dev` to copy `src/superclaude/` to `.claude/`
5. **[EXECUTION]** Run `make verify-sync` to confirm alignment
6. **[VERIFICATION]** All four commands exit 0
7. **[COMPLETION]** Record command outputs in evidence

**Acceptance Criteria:**
- `make lint` exits 0 with no linting errors
- `make format` exits 0 (may produce formatting changes)
- `make sync-dev` exits 0 with files synced
- `make verify-sync` exits 0 confirming `src/` and `.claude/` are aligned

**Validation:**
- `make lint && make format && make sync-dev && make verify-sync` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0033/evidence.md

**Dependencies:** T05.01
**Rollback:** Fix lint/format issues and re-run

---

### T05.06 -- Update Execution Log and Documentation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-054 |
| Why | The execution log and relevant documentation must be updated to reflect the completed preflight executor feature, its configuration options, and usage instructions. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0034 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0034/evidence.md

**Deliverables:**
- Updated execution log at `.dev/releases/current/v2.25.5-PreFlightExecutor/execution-log.md` with task completion records

**Steps:**
1. **[PLANNING]** Review the execution log template from the tasklist index
2. **[PLANNING]** Gather completion timestamps and results from all phases
3. **[EXECUTION]** Update `execution-log.md` with entries for all completed tasks
4. **[EXECUTION]** Update any relevant sprint documentation with preflight executor usage notes
5. **[VERIFICATION]** Confirm execution log entries are complete and accurate
6. **[COMPLETION]** Record documentation updates in evidence

**Acceptance Criteria:**
- `execution-log.md` contains entries for all 33 tasks with timestamps, results, and evidence paths
- Documentation reflects the new `Execution Mode` column and preflight behavior
- No references to unimplemented features or TODO items
- All evidence paths in the log are valid relative to TASKLIST_ROOT

**Validation:**
- Manual check: execution log entries are complete and consistent with task results
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0034/evidence.md

**Dependencies:** T05.01, T05.05
**Rollback:** Revert documentation changes

---

### T05.07 -- Release Gate Validation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-055 |
| Why | The release gate checklist ensures all criteria are met before merge: compatibility tests pass, performance is within threshold, rollback is demonstrated, and no regression is observed in all-Claude tasklists. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | Cross-cutting scope (release decision), breaking change risk |
| Tier | STRICT |
| Confidence | [████████░-] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0035, D-0043 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0035/evidence.md
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0035/spec.md (D-0043)

**Deliverables:**
- Release gate checklist: all compatibility tests pass, performance <30s for 5 EXEMPT-tier tasks, rollback demonstrated, no regression in all-Claude tasklists
- No regression confirmed in all-Claude tasklists

**Steps:**
1. **[PLANNING]** Review all success criteria (SC-001 through SC-008) from the roadmap
2. **[PLANNING]** Gather evidence from T05.01 through T05.06
3. **[EXECUTION]** Verify SC-001: performance <30s, zero tokens (from T05.02 evidence)
4. **[EXECUTION]** Verify SC-002: nested claude works (from T05.03 evidence)
5. **[EXECUTION]** Verify SC-003: parser compatibility (from T03.04 evidence)
6. **[EXECUTION]** Verify SC-004: 14 unit tests pass (from T05.01 evidence)
7. **[EXECUTION]** Verify SC-005: 8 integration tests pass (from T05.01 evidence)
8. **[EXECUTION]** Verify SC-006: skip mode works (from T04.02 evidence)
9. **[EXECUTION]** Verify SC-007: single-line rollback (from T05.04 evidence)
10. **[EXECUTION]** Verify SC-008: evidence artifacts complete (from T03.06 evidence)
11. **[VERIFICATION]** Confirm all 8 criteria met; create release gate checklist artifact
12. **[COMPLETION]** Record final release decision and evidence references

**Acceptance Criteria:**
- All 8 success criteria (SC-001 through SC-008) verified with evidence references
- `uv run pytest tests/ -v` exits 0 with no regressions
- `make lint && make format && make sync-dev && make verify-sync` exits 0
- Release gate checklist artifact exists at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0035/evidence.md

**Validation:**
- `uv run pytest tests/ -v` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0035/evidence.md

**Dependencies:** T05.01, T05.02, T05.03, T05.04, T05.05, T05.06
**Rollback:** Not applicable (validation-only task)

---

### Checkpoint: End of Phase 5

**Purpose:** Final gate: confirm all success criteria met, code quality validated, documentation complete, and release gate checklist approved.
**Checkpoint Report Path:** .dev/releases/current/v2.25.5-PreFlightExecutor/checkpoints/CP-P05-END.md
**Verification:**
- Full test suite passes: 14 unit + 8 integration + existing tests with zero regressions
- All 8 success criteria (SC-001 through SC-008) verified with evidence
- `make lint && make format && make sync-dev && make verify-sync` all exit 0
**Exit Criteria:**
- All 7 tasks (T05.01-T05.07) have evidence artifacts
- Release gate checklist approved with all criteria met
- No open issues or unresolved blockers
