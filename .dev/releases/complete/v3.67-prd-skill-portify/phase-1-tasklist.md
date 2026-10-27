# Phase 1 -- Core Models + Gates

**Goal**: Implement the foundational domain types, gate criteria, file discovery utilities, and data filtering functions. These modules have zero cross-dependencies within the PRD package and form the base layer that all other modules import.

**Files**: `models.py`, `gates.py`, `inventory.py`, `filtering.py` + corresponding unit tests

**Dependencies**: `src/superclaude/cli/pipeline/models.py` (base types)

---

## T01.01: Confirm batch tier classification for implementation tasks

**Type**: Clarification Task
**Effort**: XS | **Risk**: Low | **Tier**: EXEMPT | **Confidence**: [#####-----] 50%
**Requires Confirmation**: Yes
**Verification Method**: Skip verification
**MCP Tools**: None required
**Sub-Agent Delegation**: None

**Deliverable**: D-0001 u2014 Tier classification confirmation document

**Context**: All 26 implementation tasks score below 0.70 tier classification confidence because the keyword algorithm is calibrated for short user prompts, not detailed spec items. The `model` keyword triggers STRICT for `models.py` (Python dataclasses, not database migrations). The `pipeline` keyword inflates effort scores for execution-adjacent tasks. This task confirms or overrides the computed tiers before implementation begins.

**Steps**:
1. **[PLANNING]** Review computed tier assignments in the Traceability Matrix
2. **[PLANNING]** Identify any misclassified tasks where keyword-triggered tier differs from actual risk
3. **[EXECUTION]** Confirm STRICT for T01.02 (models.py) and T03.06 (executor.py) as critical pipeline components
4. **[EXECUTION]** Confirm STANDARD for all other implementation tasks
5. **[EXECUTION]** Confirm LIGHT for T04.02 (__init__.py) and EXEMPT for T05.01 (open items)
6. **[VERIFICATION]** Record confirmed tiers with override justifications
7. **[COMPLETION]** Update task metadata if any tiers changed

**Acceptance Criteria**:
- [ ] All 26 implementation task tiers reviewed and confirmed or overridden
- [ ] Override justifications documented for any tier changes
- [ ] No implementation task left with unconfirmed tier
- [ ] Confirmation document written to D-0001 artifact path

**Validation**:
- Manual check: all tasks in phases 1-5 have confirmed tier assignments
- Evidence: D-0001 notes.md produced with tier confirmation table

**Risk Drivers**: None (clarification task)
**Notes**: Batch clarification per Rule 4.6. Confidence < 0.70 is systemic (keyword mismatch), not per-task ambiguity.

---

## T01.02: Implement models.py

**Effort**: M | **Risk**: Low | **Tier**: STRICT | **Confidence**: [####------] 40%
**Requires Confirmation**: Yes (covered by T01.01)
**Critical Path Override**: No
**Verification Method**: Sub-agent (quality-engineer) | Token Budget: 3-5K | Timeout: 60s
**MCP Tools**: Required: Sequential, Serena | Preferred: Context7
**Sub-Agent Delegation**: Recommended (STRICT tier)

**Deliverable**: D-0002 u2014 `src/superclaude/cli/prd/models.py`
**Roadmap Items**: R-016, R-031

**Steps**:
1. **[PLANNING]** Read `src/superclaude/cli/pipeline/models.py` to understand base `PipelineConfig`, `Step`, `StepResult` interfaces
2. **[PLANNING]** Review Section 4.5 (Data Models) of release spec for complete type definitions
3. **[EXECUTION]** Create `src/superclaude/cli/prd/models.py` with `PrdConfig` extending `PipelineConfig` (19 fields)
4. **[EXECUTION]** Implement `PrdStepStatus` enum with 12 states: PENDING, RUNNING, PASS, PASS_NO_SIGNAL, PASS_NO_REPORT, INCOMPLETE, HALT, TIMEOUT, ERROR, SKIPPED, QA_FAIL, QA_FAIL_EXHAUSTED, VALIDATION_FAIL
5. **[EXECUTION]** Implement `PrdStepResult` extending `StepResult` with execution telemetry fields (exit_code, output_bytes, artifacts_produced, qa_verdict)
6. **[EXECUTION]** Implement `PrdPipelineResult` with aggregate pipeline state, resume_command(), suggested_resume_budget
7. **[EXECUTION]** Implement `PrdMonitorState` with NDJSON signal fields and `ExistingWorkState` enum (NO_EXISTING, RESUME_STAGE_A, RESUME_STAGE_B, ALREADY_COMPLETE)
8. **[VERIFICATION]** Verify zero `async def` or `await` (NFR-PRD.1); verify all dataclasses are importable
9. **[COMPLETION]** Record line count and type count in evidence

**Acceptance Criteria**:
- [ ] All 6 types defined: PrdConfig, PrdStepStatus, PrdStepResult, PrdPipelineResult, PrdMonitorState, ExistingWorkState
- [ ] PrdStepStatus has is_terminal, is_success, is_failure, needs_fix_cycle properties
- [ ] PrdPipelineResult.resume_command() generates correct CLI invocation
- [ ] Module imports successfully with no circular dependencies

**Validation**:
- `uv run python -c "from superclaude.cli.prd.models import PrdConfig, PrdStepStatus, PrdStepResult, PrdPipelineResult, PrdMonitorState, ExistingWorkState"`
- Evidence: module file exists with >= 80 lines, all types importable

**Risk Drivers**: None
**Notes**: Tier conflict: model (STRICT) vs implement (STANDARD) -> resolved to STRICT by priority rule. The `model` keyword matches the Data category but this is a Python dataclass file, not a database migration. STRICT is still appropriate as this is the foundational type system.

---

## T01.03: Implement gates.py

**Effort**: S | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Critical Path Override**: No
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: Preferred: Sequential, Context7
**Sub-Agent Delegation**: None

**Deliverable**: D-0003 u2014 `src/superclaude/cli/prd/gates.py`
**Roadmap Items**: R-017, R-032, R-053

**Steps**:
1. **[PLANNING]** Read `src/superclaude/cli/pipeline/gates.py` to understand `GateCriteria`, `gate_passed()` interface
2. **[PLANNING]** Review Section 5.2 (Gate Criteria table) for all 18 gate definitions
3. **[EXECUTION]** Define `GATE_CRITERIA` dict mapping step IDs to `GateCriteria` instances (tier, required_frontmatter, min_lines)
4. **[EXECUTION]** Implement reusable layer: `_check_verdict_field()`, `_check_no_placeholders()` returning `bool | str`
5. **[EXECUTION]** Implement PRD-specific layer: `_check_parsed_request_fields()`, `_check_research_notes_sections()`, `_check_suggested_phases_detail()`, `_check_task_phases_present()`, `_check_b2_self_contained()`, `_check_parallel_instructions()`, `_check_prd_template_sections()`, `_check_qa_verdict()`
6. **[EXECUTION]** Wrap all semantic checks in try/except: exceptions return `(False, "check '{name}' crashed: {error}")` [F-005]
7. **[VERIFICATION]** Verify all `_check_*` functions match `Callable[[str], bool | str]` signature (NFR-PRD.2)
8. **[COMPLETION]** Record function count and gate count in evidence

**Acceptance Criteria**:
- [ ] 10 semantic check functions defined, each returning `bool | str` (True for pass, error string for fail)
- [ ] Two-layer organization: reusable checks + PRD-specific checks [F-001]
- [ ] All checks wrapped in try/except with crash-safe error messages [F-005]
- [ ] Gate criteria table matches Section 5.2 (18 step->gate mappings)

**Validation**:
- `uv run python -c "from superclaude.cli.prd.gates import GATE_CRITERIA; print(len(GATE_CRITERIA))"`
- Evidence: 18 gate criteria entries, 10 semantic check functions

**Risk Drivers**: None

---

## T01.04: Implement inventory.py

**Effort**: S | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Critical Path Override**: No
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: Preferred: Sequential, Context7
**Sub-Agent Delegation**: None

**Deliverable**: D-0004 u2014 `src/superclaude/cli/prd/inventory.py`
**Roadmap Items**: R-018, R-001, R-006

**Steps**:
1. **[PLANNING]** Review FR-PRD.1 (Existing Work Detection) acceptance criteria
2. **[PLANNING]** Review FR-PRD.6 (Template Triage) acceptance criteria
3. **[EXECUTION]** Implement `check_existing_work(config: PrdConfig) -> ExistingWorkState` with 4-state detection: NO_EXISTING, RESUME_STAGE_A, RESUME_STAGE_B, ALREADY_COMPLETE
4. **[EXECUTION]** Implement product name matching with short-name guard: names < 3 chars require frontmatter `product_name` match instead of full-content substring [F-008]
5. **[EXECUTION]** Implement `discover_research_files(task_dir: Path) -> list[Path]` scanning `research/*.md`
6. **[EXECUTION]** Implement `discover_synth_files(task_dir: Path) -> list[Path]` scanning `synthesis/synth-*.md`
7. **[EXECUTION]** Implement `select_template(prd_scope: str) -> int` returning 2 for creation, 1 for update
8. **[EXECUTION]** Implement `create_task_dirs(task_dir: Path) -> None` creating research/, synthesis/, qa/, reviews/, results/ subdirectories
9. **[VERIFICATION]** Verify all functions are pure (no side effects except create_task_dirs)
10. **[COMPLETION]** Record function count in evidence

**Acceptance Criteria**:
- [ ] `check_existing_work` detects all 4 states correctly by scanning `.dev/tasks/to-do/TASK-PRD-*/`
- [ ] Short product name matching (< 3 chars) uses frontmatter field, not substring [F-008]
- [ ] `discover_research_files` returns only completed files (skips incomplete markers)
- [ ] `create_task_dirs` creates all 5 required subdirectories

**Validation**:
- `uv run python -c "from superclaude.cli.prd.inventory import check_existing_work, discover_research_files, discover_synth_files, select_template, create_task_dirs"`
- Evidence: 5 functions importable, select_template("product") returns 2

**Risk Drivers**: None

---

## T01.05: Implement filtering.py

**Effort**: S | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Critical Path Override**: No
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: Preferred: Sequential, Context7
**Sub-Agent Delegation**: None

**Deliverable**: D-0005 u2014 `src/superclaude/cli/prd/filtering.py`
**Roadmap Items**: R-019, R-011, R-013

**Steps**:
1. **[PLANNING]** Review FR-PRD.11 (partition + merge) and FR-PRD.13 (synthesis QA partition) acceptance criteria
2. **[PLANNING]** Review `refs/synthesis-mapping.md` for the 9-entry section mapping table
3. **[EXECUTION]** Implement `partition_files(files: list[Path], threshold: int) -> list[list[Path]]` with single-partition below threshold, even-split above
4. **[EXECUTION]** Implement `compile_gaps(research_dir: Path) -> list[dict]` extracting and deduplicating gaps from research files
5. **[EXECUTION]** Implement `merge_qa_partition_reports(reports: list[dict]) -> dict` with pessimistic merge: overall FAIL if ANY partition FAIL [GAP-005]
6. **[EXECUTION]** Implement `load_synthesis_mapping(refs_dir: Path) -> list[dict]` returning 9 entries with section assignments [F-002]
7. **[EXECUTION]** Implement `_filter_research_for_sections(research_files: list[Path], mapping_entry: dict) -> list[Path]` matching research files to synthesis section inputs
8. **[VERIFICATION]** Verify partition_files([], 6) returns empty list (zero-file boundary case)
9. **[COMPLETION]** Record function count in evidence

**Acceptance Criteria**:
- [ ] `partition_files` returns single partition when count <= threshold, splits evenly above
- [ ] `merge_qa_partition_reports` uses pessimistic merge (FAIL if ANY partition FAIL) [GAP-005]
- [ ] `load_synthesis_mapping` returns exactly 9 entries from refs/synthesis-mapping.md [F-002]
- [ ] Zero-file edge case handled: empty input returns empty results

**Validation**:
- `uv run python -c "from superclaude.cli.prd.filtering import partition_files; print(partition_files(list(range(8)), 6))"`
- Evidence: partition_files correctly splits 8 items with threshold 6 into 2 partitions

**Risk Drivers**: None

---

### Checkpoint: Phase 1 / Tasks T01.01u2013T01.05

**Purpose**: Verify all foundational modules compile and are independently importable before writing tests.

**Verification**:
- [ ] All 4 source files exist under `src/superclaude/cli/prd/`: models.py, gates.py, inventory.py, filtering.py
- [ ] `uv run python -c "from superclaude.cli.prd import models, gates, inventory, filtering"` succeeds
- [ ] No circular imports between the 4 modules

**Exit Criteria**:
- [ ] All 4 modules importable with zero errors
- [ ] models.py exports all 6 domain types
- [ ] gates.py exports GATE_CRITERIA dict with 18 entries

---

## T01.06: Write unit tests for models.py

**Effort**: XS | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: None required
**Sub-Agent Delegation**: None

**Deliverable**: D-0006 u2014 `tests/cli/prd/test_models.py`
**Roadmap Items**: R-048

**Steps**:
1. **[PLANNING]** Review Section 8.1 test plan for models.py tests (3 tests specified)
2. **[PLANNING]** Check existing test patterns in `tests/cli/` for conventions
3. **[EXECUTION]** Implement `test_prd_config_derived_paths`: verify research_dir, synthesis_dir, qa_dir resolve correctly from base paths
4. **[EXECUTION]** Implement `test_prd_step_status_properties`: verify is_terminal, is_success, is_failure, needs_fix_cycle for each status value
5. **[EXECUTION]** Implement `test_prd_pipeline_result_resume_command`: verify correct CLI string on halt
6. **[VERIFICATION]** Run `uv run pytest tests/cli/prd/test_models.py -v` and verify all 3 tests pass
7. **[COMPLETION]** Record pass count in evidence

**Acceptance Criteria**:
- [ ] 3 test functions implemented matching Section 8.1 specification
- [ ] All tests pass with `uv run pytest tests/cli/prd/test_models.py -v`
- [ ] Tests cover all PrdStepStatus enum values for property correctness
- [ ] Test file follows existing `tests/cli/` conventions

**Validation**:
- `uv run pytest tests/cli/prd/test_models.py -v --tb=short`
- Evidence: 3 tests passed, 0 failures

**Risk Drivers**: None

---

## T01.07: Write unit tests for gates.py

**Effort**: XS | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: None required
**Sub-Agent Delegation**: None

**Deliverable**: D-0007 u2014 `tests/cli/prd/test_gates.py`
**Roadmap Items**: R-046

**Steps**:
1. **[PLANNING]** Review Section 8.1 test plan for gates.py tests (8 tests specified)
2. **[PLANNING]** Prepare test fixtures: valid/invalid JSON, research notes with/without sections
3. **[EXECUTION]** Implement 8 test functions: test_check_parsed_request_fields_valid, test_check_parsed_request_fields_missing, test_check_research_notes_sections, test_check_verdict_field, test_check_b2_self_contained, test_check_parallel_instructions, test_check_prd_template_sections, test_check_no_placeholders
4. **[EXECUTION]** Each test verifies both pass (returns True) and fail (returns error string) paths
5. **[VERIFICATION]** Run `uv run pytest tests/cli/prd/test_gates.py -v` and verify all 8 tests pass
6. **[COMPLETION]** Record pass count in evidence

**Acceptance Criteria**:
- [ ] 8 test functions implemented matching Section 8.1 specification
- [ ] All tests pass with `uv run pytest tests/cli/prd/test_gates.py -v`
- [ ] Both pass and fail paths tested for each check function
- [ ] Gate exception wrapping tested (check that crashed checks return error string, not exception)

**Validation**:
- `uv run pytest tests/cli/prd/test_gates.py -v --tb=short`
- Evidence: 8 tests passed, 0 failures

**Risk Drivers**: None

---

## T01.08: Write unit tests for inventory.py

**Effort**: XS | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: None required
**Sub-Agent Delegation**: None

**Deliverable**: D-0008 u2014 `tests/cli/prd/test_inventory.py`
**Roadmap Items**: R-044

**Steps**:
1. **[PLANNING]** Review Section 8.1 test plan for inventory.py tests (5 tests specified)
2. **[PLANNING]** Prepare test fixtures using tmp_path for directory structures
3. **[EXECUTION]** Implement `test_check_existing_work_no_existing`: empty dir returns NO_EXISTING
4. **[EXECUTION]** Implement `test_check_existing_work_resume_stage_b`: existing task file with unchecked items
5. **[EXECUTION]** Implement `test_select_template`: returns 2 for creation, 1 for update
6. **[EXECUTION]** Implement `test_discover_research_files`: finds completed research files, skips incomplete
7. **[EXECUTION]** Implement `test_discover_synth_files`: finds synth files matching `synth-*.md` pattern
8. **[VERIFICATION]** Run `uv run pytest tests/cli/prd/test_inventory.py -v` and verify all 5 tests pass
9. **[COMPLETION]** Record pass count in evidence

**Acceptance Criteria**:
- [ ] 5 test functions implemented matching Section 8.1 specification
- [ ] All tests pass with `uv run pytest tests/cli/prd/test_inventory.py -v`
- [ ] Tests use tmp_path fixtures for file system isolation
- [ ] Short product name matching (< 3 chars) edge case tested

**Validation**:
- `uv run pytest tests/cli/prd/test_inventory.py -v --tb=short`
- Evidence: 5 tests passed, 0 failures

**Risk Drivers**: None

---

## T01.09: Write unit tests for filtering.py

**Effort**: XS | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: None required
**Sub-Agent Delegation**: None

**Deliverable**: D-0009 u2014 `tests/cli/prd/test_filtering.py`
**Roadmap Items**: R-045

**Steps**:
1. **[PLANNING]** Review Section 8.1 test plan for filtering.py tests (4 tests specified)
2. **[PLANNING]** Prepare test fixtures for partition scenarios and research file content
3. **[EXECUTION]** Implement `test_partition_files_below_threshold`: returns single partition when count <= threshold
4. **[EXECUTION]** Implement `test_partition_files_above_threshold`: splits into correct partition count
5. **[EXECUTION]** Implement `test_merge_qa_partition_reports`: merges reports, pessimistic verdict (FAIL if ANY FAIL)
6. **[EXECUTION]** Implement `test_compile_gaps`: extracts and deduplicates gaps from research files
7. **[VERIFICATION]** Run `uv run pytest tests/cli/prd/test_filtering.py -v` and verify all 4 tests pass
8. **[COMPLETION]** Record pass count in evidence

**Acceptance Criteria**:
- [ ] 4 test functions implemented matching Section 8.1 specification
- [ ] All tests pass with `uv run pytest tests/cli/prd/test_filtering.py -v`
- [ ] Pessimistic merge strategy explicitly tested (mixed PASS/FAIL partitions -> FAIL)
- [ ] Zero-file partition edge case tested (empty input -> empty result)

**Validation**:
- `uv run pytest tests/cli/prd/test_filtering.py -v --tb=short`
- Evidence: 4 tests passed, 0 failures

**Risk Drivers**: None

---

### Checkpoint: End of Phase 1

**Purpose**: Verify all Phase 1 modules and tests are complete and passing before moving to Prompts + Config.

**Verification**:
- [ ] All 4 source files exist and are importable: models.py, gates.py, inventory.py, filtering.py
- [ ] All 4 test files exist and pass: test_models.py, test_gates.py, test_inventory.py, test_filtering.py
- [ ] `uv run pytest tests/cli/prd/ -v` shows 20 tests passed (3+8+5+4)

**Exit Criteria**:
- [ ] 20/20 unit tests passing
- [ ] No import errors across Phase 1 modules
- [ ] Tier classification confirmed (T01.01 complete)
