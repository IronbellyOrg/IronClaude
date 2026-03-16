# Phase 1 -- Data Model and Parsing

Establish all data structures and parsing extensions required for the preflight execution mode. This phase adds the `execution_mode`, `command`, and `classifier` fields to existing dataclasses, extends parsers to extract them from tasklist files, adds the `PREFLIGHT_PASS` status, and validates python-mode tasks at parse time. All changes are in `src/superclaude/cli/sprint/`.

---

### T01.01 -- Add `execution_mode` Field to `Phase` Dataclass

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001 |
| Why | The `Phase` dataclass needs an `execution_mode` field to distinguish claude, python, and skip phases at the data model level. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0001 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0001/evidence.md

**Deliverables:**
- `Phase.execution_mode: str = "claude"` field added to the `Phase` dataclass in the config/model file

**Steps:**
1. **[PLANNING]** Read the `Phase` dataclass definition in `src/superclaude/cli/sprint/` to identify the exact file and class location
2. **[PLANNING]** Confirm no existing `execution_mode` field or similar attribute exists
3. **[EXECUTION]** Add `execution_mode: str = "claude"` field to the `Phase` dataclass with default value `"claude"`
4. **[EXECUTION]** Verify the field is a plain string with no type validation at the dataclass level (validation happens in `discover_phases()`)
5. **[VERIFICATION]** Run `uv run pytest tests/` to confirm no regressions from the new field
6. **[COMPLETION]** Record the exact file path and line number of the change in evidence

**Acceptance Criteria:**
- `Phase` dataclass has an `execution_mode` attribute that defaults to `"claude"` when not specified
- Existing code that constructs `Phase` objects without `execution_mode` continues to work unchanged
- `Phase(execution_mode="python")` and `Phase(execution_mode="skip")` are accepted without error
- Change is confined to a single dataclass definition in `src/superclaude/cli/sprint/`

**Validation:**
- `uv run pytest tests/ -v --tb=short` exits 0 with no test failures
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0001/evidence.md

**Dependencies:** None
**Rollback:** Remove the `execution_mode` field from the dataclass
**Notes:** Default value "claude" ensures backward compatibility with all existing Phase instantiations.

---

### T01.02 -- Extend `discover_phases()` to Read Execution Mode Column

| Field | Value |
|---|---|
| Roadmap Item IDs | R-002 |
| Why | The phase discovery function must parse the `Execution Mode` column from `tasklist-index.md` to populate `Phase.execution_mode`, with validation for allowed values and case-insensitive normalization. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STRICT |
| Confidence | [████████░-] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0002, D-0003 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0002/evidence.md
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0002/spec.md

**Deliverables:**
- `discover_phases()` reads the `Execution Mode` column from the tasklist-index.md table
- Case-insensitive normalization to lowercase; `click.ClickException` raised on unrecognized values; default to `"claude"` when column is absent

**Steps:**
1. **[PLANNING]** Read the `discover_phases()` function in `src/superclaude/cli/sprint/` to understand current parsing logic
2. **[PLANNING]** Identify where the markdown table is parsed and how columns are extracted
3. **[EXECUTION]** Add column detection for `Execution Mode` in the table header parsing
4. **[EXECUTION]** Extract the value per phase row, normalize to lowercase via `.strip().lower()`
5. **[EXECUTION]** Validate against allowed set `{"claude", "python", "skip"}`; raise `click.ClickException(f"Unknown execution mode '{value}' for phase {phase_name}. Allowed: claude, python, skip")` on mismatch
6. **[EXECUTION]** Default to `"claude"` when the `Execution Mode` column is not present in the table
7. **[VERIFICATION]** Run `uv run pytest tests/ -v` and verify column-present and column-absent scenarios work
8. **[COMPLETION]** Document the parsing logic and validation behavior in evidence

**Acceptance Criteria:**
- `discover_phases()` correctly reads `Execution Mode` column values and populates `Phase.execution_mode`
- `click.ClickException` is raised with an actionable message when an unrecognized mode like `"invalid"` is provided
- When `Execution Mode` column is absent from the table, all phases default to `execution_mode="claude"`
- Case variations like `"Python"`, `"SKIP"`, `"Claude"` are normalized to lowercase

**Validation:**
- `uv run pytest tests/ -v --tb=short` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0002/evidence.md

**Dependencies:** T01.01
**Rollback:** Revert the column-reading logic in `discover_phases()`; Phase objects revert to default "claude"

---

### T01.03 -- Add `command` Field to `TaskEntry` and Extend `parse_tasklist()`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003, R-004 |
| Why | `TaskEntry` needs a `command` field to store the executable command string, and `parse_tasklist()` must extract `**Command:**` fields from task markdown, preserving pipes, redirects, and quoted arguments verbatim. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | Command quoting/escaping (R-058) |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0004, D-0005 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0004/evidence.md
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0004/spec.md

**Deliverables:**
- `TaskEntry.command: str = ""` field added to the `TaskEntry` dataclass
- `parse_tasklist()` extracts `**Command:**` field values, strips backtick delimiters, preserves pipes/redirects/quoted arguments verbatim

**Steps:**
1. **[PLANNING]** Read the `TaskEntry` dataclass and `parse_tasklist()` function to understand current structure
2. **[PLANNING]** Identify how existing fields like description are extracted from task markdown
3. **[EXECUTION]** Add `command: str = ""` field to the `TaskEntry` dataclass
4. **[EXECUTION]** In `parse_tasklist()`, add extraction logic for lines matching `**Command:**` pattern
5. **[EXECUTION]** Strip surrounding backtick delimiters (`` ` ``) from the extracted command string
6. **[EXECUTION]** Preserve all shell metacharacters (pipes `|`, redirects `>`, quoted arguments) verbatim in the string
7. **[VERIFICATION]** Test with command strings containing pipes (`cmd1 | cmd2`), redirects (`cmd > file`), and quotes (`cmd "arg with spaces"`)
8. **[COMPLETION]** Record test results and edge cases in evidence

**Acceptance Criteria:**
- `TaskEntry` dataclass has a `command` attribute defaulting to `""` when no `**Command:**` field is present
- `parse_tasklist()` correctly extracts `**Command:** \`echo hello\`` as `"echo hello"` (backticks stripped)
- Command `uv run pytest tests/ | grep PASS > results.txt` is preserved verbatim after extraction
- Existing task entries without `**Command:**` fields parse identically to pre-change behavior

**Validation:**
- `uv run pytest tests/ -v --tb=short` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0004/evidence.md

**Dependencies:** None
**Rollback:** Remove the `command` field and extraction logic
**Notes:** Shell metacharacters are preserved textually but not shell-expanded under `shell=False` at execution time (per R-058).

---

### T01.04 -- Add `classifier` Field to `TaskEntry`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Why | `TaskEntry` needs a `classifier` field to store the classifier name from `| Classifier |` metadata in task markdown, enabling per-task classification routing at execution time. |
| Effort | XS |
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
| Deliverable IDs | D-0006 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0006/evidence.md

**Deliverables:**
- `TaskEntry.classifier: str = ""` field for `| Classifier |` metadata extraction from task markdown

**Steps:**
1. **[PLANNING]** Read the `TaskEntry` dataclass to confirm the field does not already exist
2. **[PLANNING]** Identify the metadata extraction pattern used by `parse_tasklist()` for table-row fields
3. **[EXECUTION]** Add `classifier: str = ""` field to the `TaskEntry` dataclass
4. **[EXECUTION]** In `parse_tasklist()`, add extraction for `| Classifier |` table row, stripping whitespace
5. **[VERIFICATION]** Run `uv run pytest tests/ -v` to confirm no regressions
6. **[COMPLETION]** Record the change location in evidence

**Acceptance Criteria:**
- `TaskEntry` dataclass has a `classifier` attribute defaulting to `""` when no `| Classifier |` row is present
- `parse_tasklist()` extracts `| Classifier | empirical_gate_v1 |` as `"empirical_gate_v1"`
- Existing task entries without `| Classifier |` rows parse identically to pre-change behavior
- Change is confined to the dataclass definition and `parse_tasklist()` function

**Validation:**
- `uv run pytest tests/ -v --tb=short` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0006/evidence.md

**Dependencies:** None
**Rollback:** Remove the `classifier` field and extraction logic

---

### T01.05 -- Add `PhaseStatus.PREFLIGHT_PASS` Enum Value

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | A new `PREFLIGHT_PASS` status is needed to distinguish phases completed by preflight execution from phases completed by Claude, ensuring correct status reporting and TUI display. |
| Effort | XS |
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
| Deliverable IDs | D-0007 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0007/evidence.md

**Deliverables:**
- `PhaseStatus.PREFLIGHT_PASS = "preflight_pass"` added to the `PhaseStatus` enum with `is_success` returning `True` and `is_failure` returning `False`

**Steps:**
1. **[PLANNING]** Read the `PhaseStatus` enum to understand existing values and `is_success`/`is_failure` logic
2. **[PLANNING]** Confirm the enum uses string values and identify how success/failure classification works
3. **[EXECUTION]** Add `PREFLIGHT_PASS = "preflight_pass"` to the `PhaseStatus` enum
4. **[EXECUTION]** Ensure `is_success` returns `True` and `is_failure` returns `False` for `PREFLIGHT_PASS`
5. **[VERIFICATION]** Run `uv run pytest tests/ -v` and assert `PhaseStatus.PREFLIGHT_PASS.is_success is True`
6. **[COMPLETION]** Record the enum location and logic in evidence

**Acceptance Criteria:**
- `PhaseStatus.PREFLIGHT_PASS` exists with value `"preflight_pass"`
- `PhaseStatus.PREFLIGHT_PASS.is_success` returns `True`
- `PhaseStatus.PREFLIGHT_PASS.is_failure` returns `False`
- Existing `PhaseStatus` values and their `is_success`/`is_failure` behavior are unchanged

**Validation:**
- `uv run pytest tests/ -v --tb=short` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0007/evidence.md

**Dependencies:** None
**Rollback:** Remove the `PREFLIGHT_PASS` enum member

---

### Checkpoint: Phase 1 / Tasks T01.01-T01.05

**Purpose:** Verify all data model additions (execution_mode, command, classifier fields and PREFLIGHT_PASS status) are in place before proceeding to validation and test tasks.
**Checkpoint Report Path:** .dev/releases/current/v2.25.5-PreFlightExecutor/checkpoints/CP-P01-T01-T05.md
**Verification:**
- All three new dataclass fields (`execution_mode`, `command`, `classifier`) exist with correct defaults
- `discover_phases()` reads `Execution Mode` column with case normalization and validation
- `PhaseStatus.PREFLIGHT_PASS` is present with correct `is_success`/`is_failure` behavior
**Exit Criteria:**
- `uv run pytest tests/ -v` exits 0 with no regressions
- All five tasks have evidence artifacts written
- No modifications to existing test files required

---

### T01.06 -- Add Validation for Python-Mode Tasks with Empty Commands

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007 |
| Why | Python-mode phases require every task to have a command. Missing commands should fail fast at parse time with actionable errors instead of producing subprocess tracebacks at execution time. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STRICT |
| Confidence | [████████░-] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0008, D-0036 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0008/evidence.md
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0008/spec.md

**Deliverables:**
- Validation logic: if `execution_mode == "python"` and any task has `command == ""`, raise `click.ClickException(f"Task {task_id} in python-mode phase has no command")`
- Actionable error message format that identifies the specific task and phase

**Steps:**
1. **[PLANNING]** Identify where phase/task validation occurs in the parse pipeline (after `discover_phases()` and `parse_tasklist()`)
2. **[PLANNING]** Determine whether validation belongs in `parse_tasklist()` or in a separate validation pass
3. **[EXECUTION]** Add validation logic that iterates tasks in python-mode phases and checks for empty `command` fields
4. **[EXECUTION]** Raise `click.ClickException(f"Task {task_id} in python-mode phase has no command")` on first empty command found
5. **[EXECUTION]** Ensure validation runs at parse time, not at execution time
6. **[VERIFICATION]** Test with a python-mode phase containing a task with empty command; verify ClickException is raised
7. **[VERIFICATION]** Test with a python-mode phase where all tasks have commands; verify no exception
8. **[COMPLETION]** Record validation placement and error message format in evidence

**Acceptance Criteria:**
- `click.ClickException` is raised with message `"Task {task_id} in python-mode phase has no command"` when a python-mode task has `command == ""`
- Validation occurs at parse time, before `execute_preflight_phases()` is called
- Claude-mode phases with empty commands do not trigger this validation
- Skip-mode phases with empty commands do not trigger this validation

**Validation:**
- `uv run pytest tests/ -v --tb=short` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0008/evidence.md

**Dependencies:** T01.01, T01.02, T01.03
**Rollback:** Remove the validation logic; empty commands in python-mode phases will fail at subprocess execution instead

---

### T01.07 -- Unit Tests for Phase Modes, TaskEntry Fields, and PhaseStatus

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008, R-009, R-010, R-011, R-012 |
| Why | Unit tests validate the new dataclass fields, enum value, and validation logic added in T01.01-T01.06, providing regression coverage for the data model layer. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0009 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0009/evidence.md

**Deliverables:**
- Unit tests in `tests/cli/sprint/test_preflight.py` covering: `Phase` with all three execution modes; `TaskEntry.command` extraction (empty, simple, pipes, quotes); `TaskEntry.classifier` extraction; `PhaseStatus.PREFLIGHT_PASS` behavior; missing-command validation in python-mode phases

**Steps:**
1. **[PLANNING]** Review the test patterns in `tests/cli/sprint/` to match existing conventions
2. **[PLANNING]** Plan test cases: 3 execution modes, 4 command variants, classifier extraction, PREFLIGHT_PASS checks, validation error
3. **[EXECUTION]** Create `tests/cli/sprint/test_preflight.py` if it does not exist
4. **[EXECUTION]** Apply `@pytest.mark.unit` to all unit test functions in this task
5. **[EXECUTION]** Write `test_phase_execution_mode_default()` asserting default is `"claude"`
5. **[EXECUTION]** Write `test_phase_execution_mode_python()` and `test_phase_execution_mode_skip()`
6. **[EXECUTION]** Write `test_task_entry_command_empty()`, `test_task_entry_command_simple()`, `test_task_entry_command_pipes()`, `test_task_entry_command_quotes()`
7. **[EXECUTION]** Write `test_task_entry_classifier_extraction()`, `test_phase_status_preflight_pass()`, `test_python_mode_empty_command_validation()`
8. **[COMPLETION]** Run `uv run pytest tests/cli/sprint/test_preflight.py -v` and record results

**Acceptance Criteria:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v -m unit` exits 0 with all unit tests passing
- Test file covers all 5 roadmap test items (R-008 through R-012)
- Each test function has a descriptive name matching the tested behavior
- No test relies on external services or file system state beyond fixtures

**Validation:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0009/evidence.md

**Dependencies:** T01.01, T01.02, T01.03, T01.04, T01.05, T01.06
**Rollback:** Delete the test file; no production code affected

---

### T01.08 -- Round-Trip Integration Test for Execution Mode Column

| Field | Value |
|---|---|
| Roadmap Item IDs | R-013 |
| Why | A round-trip test writes a `tasklist-index.md` with the `Execution Mode` column, parses it with `discover_phases()`, and verifies the extracted modes match, validating the complete parse pipeline. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [████████░-] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0010 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0010/evidence.md

**Deliverables:**
- Round-trip integration test: write a `tasklist-index.md` with `Execution Mode` column containing `python`, `claude`, `skip` values, parse with `discover_phases()`, verify extracted `Phase.execution_mode` values match

**Steps:**
1. **[PLANNING]** Review the `tasklist-index.md` table format expected by `discover_phases()`
2. **[PLANNING]** Plan a temp file fixture with mixed execution modes
3. **[EXECUTION]** Apply `@pytest.mark.integration` to the round-trip test function
4. **[EXECUTION]** Write test that creates a temporary `tasklist-index.md` with 3 phases: python, claude, skip
4. **[EXECUTION]** Call `discover_phases()` on the temp file
5. **[EXECUTION]** Assert `phases[0].execution_mode == "python"`, `phases[1].execution_mode == "claude"`, `phases[2].execution_mode == "skip"`
6. **[VERIFICATION]** Also test with `Execution Mode` column absent; verify all default to `"claude"`
7. **[COMPLETION]** Record test results in evidence

**Acceptance Criteria:**
- `uv run pytest tests/cli/sprint/test_preflight.py::test_round_trip_execution_mode -v` exits 0
- Test writes a temporary file, parses it, and verifies all three execution mode values round-trip correctly
- Test also validates the absent-column default behavior
- No persistent files left after test completes (uses `tmp_path` fixture)

**Validation:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v -m integration` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0010/evidence.md

**Dependencies:** T01.02
**Rollback:** Delete the test function; no production code affected

---

### Checkpoint: End of Phase 1

**Purpose:** Gate for Phase 2 and Phase 3: confirm all data model extensions, parsing changes, and validation logic are complete and tested.
**Checkpoint Report Path:** .dev/releases/current/v2.25.5-PreFlightExecutor/checkpoints/CP-P01-END.md
**Verification:**
- All 8 tasks (T01.01-T01.08) have status completed with evidence artifacts
- `uv run pytest tests/cli/sprint/test_preflight.py -v` exits 0 with all Phase 1 tests passing
- `Phase`, `TaskEntry`, and `PhaseStatus` dataclass/enum changes are in place with correct defaults
**Exit Criteria:**
- No regressions in existing test suite: `uv run pytest tests/ -v` exits 0
- All new fields have default values that preserve backward compatibility
- Validation logic for python-mode empty commands is confirmed working
