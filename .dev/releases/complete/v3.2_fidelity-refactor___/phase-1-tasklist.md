# Phase 1 -- Core Analysis Engine

Implement the three wiring analysis functions (unwired callables, orphan modules, unwired registries) and their supporting data models as self-contained, testable units in `src/superclaude/cli/audit/wiring_gate.py` and `audit/wiring_config.py`, with zero integration dependencies. Validate with 14+ unit tests covering all finding types, parse degradation, and whitelist behavior.

---

### T01.01 -- Implement Data Models and Config

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001, R-002, R-003, R-004 |
| Why | The analysis engine requires WiringFinding, WiringReport, and WiringConfig dataclasses plus a whitelist schema loader before any analyzer can be built. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | schema, database (dataclass modeling), compliance (whitelist conformance) |
| Tier | STRICT |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0001, D-0002 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0001/spec.md`
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0002/spec.md`

**Deliverables:**
1. `WiringFinding` and `WiringReport` dataclasses in `src/superclaude/cli/audit/wiring_gate.py` with `to_dict()` round-trip and computed properties
2. `WiringConfig` dataclass and whitelist YAML schema loader in `src/superclaude/cli/audit/wiring_config.py` with malformed-entry skip + WARNING behavior (NFR-008)

**Steps:**
1. **[PLANNING]** Read FR: T01, Goal-1c, Goal-1d, NFR-008 requirements from roadmap; identify field lists for each dataclass
2. **[PLANNING]** Confirm no existing `audit/` directory conflicts; plan file structure for `wiring_gate.py` and `wiring_config.py`
3. **[EXECUTION]** Implement `WiringFinding` dataclass with `finding_type`, `file_path`, `symbol_name`, `detail` fields and `to_dict()` method
4. **[EXECUTION]** Implement `WiringReport` dataclass with computed properties (finding counts by type, `analysis_complete`, `files_skipped`)
5. **[EXECUTION]** Implement `WiringConfig` dataclass with `provider_dir_names`, `registry_patterns`, whitelist path fields and default values
6. **[EXECUTION]** Implement whitelist YAML schema loader: valid entries loaded, malformed entries skipped with `logging.warning()`, `whitelist_entries_applied` count tracked
7. **[VERIFICATION]** Verify `WiringFinding.to_dict()` round-trips; `WiringReport` computed properties return correct counts; whitelist loads valid YAML and skips malformed entries
8. **[COMPLETION]** Record implementation details to D-0001/spec.md and D-0002/spec.md

**Acceptance Criteria:**
- File `src/superclaude/cli/audit/wiring_gate.py` exists with `WiringFinding` and `WiringReport` dataclasses where `WiringFinding.to_dict()` round-trips correctly
- File `src/superclaude/cli/audit/wiring_config.py` exists with `WiringConfig` dataclass and whitelist loader that skips malformed entries with WARNING
- `WiringReport` computed properties return correct finding counts grouped by `finding_type`
- `whitelist_entries_applied` count is tracked in report frontmatter data (Goal-4a)
- `WiringConfig` provides conservative default `provider_dir_names`: `steps/`, `handlers/`, `validators/`, `checks/` (R6 mitigation)

**Validation:**
- `uv run pytest tests/audit/test_wiring_gate.py -k "dataclass or config or whitelist" -v`
- Evidence: linkable artifact produced at D-0001/spec.md and D-0002/spec.md

**Dependencies:** None
**Rollback:** Delete `src/superclaude/cli/audit/wiring_gate.py` and `src/superclaude/cli/audit/wiring_config.py`

---

### T01.02 -- Implement analyze_unwired_callables

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Why | Detects injectable callables that are declared but never wired into dispatch — the primary defect class that caused the cli-portify no-op bug. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | security (callable injection analysis), performance (AST parsing) |
| Tier | STRICT |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0003/spec.md`

**Deliverables:**
1. `analyze_unwired_callables()` function in `src/superclaude/cli/audit/wiring_gate.py` using AST-only analysis with whitelist suppression per Goal-1c

**Steps:**
1. **[PLANNING]** Read FR: Goal-1a, Goal-1b, Goal-1c requirements; identify callable detection patterns using Python `ast` module
2. **[PLANNING]** Confirm Architectural Constraint 1 (AST-only) and Constraint 2 (no dynamic dispatch — exclude `**kwargs`, `getattr`, `importlib`)
3. **[EXECUTION]** Implement AST visitor to detect callable declarations (`def`, `class`) in target package
4. **[EXECUTION]** Implement dispatch wiring detection — scan for references to declared callables in registration sites
5. **[EXECUTION]** Apply whitelist suppression during analysis per Goal-1c; track `whitelist_entries_applied` count
6. **[EXECUTION]** Wrap each `ast.parse()` in try/except per NFR-002; emit structured warning with file path, parse reason, and files-skipped count on failure
7. **[VERIFICATION]** Verify function detects unwired callables in test fixtures and applies whitelist suppression correctly
8. **[COMPLETION]** Record implementation details to D-0003/spec.md

**Acceptance Criteria:**
- `analyze_unwired_callables()` exists in `src/superclaude/cli/audit/wiring_gate.py` and returns `list[WiringFinding]` with `finding_type='unwired_callable'`
- Function uses only Python `ast` module for analysis (Constraint 1); excludes `**kwargs`, `getattr`, `importlib` patterns (Constraint 2)
- Whitelist entries suppress findings and increment `whitelist_entries_applied` count (Goal-1c)
- Parse errors emit structured warning with file path, parse reason, and files-skipped count (NFR-002); `analysis_complete` reflects whether all files parsed successfully; `files_skipped: N` propagated to report frontmatter

**Validation:**
- `uv run pytest tests/audit/test_wiring_gate.py -k "unwired_callable" -v`
- Evidence: linkable artifact produced at D-0003/spec.md

**Dependencies:** T01.01
**Rollback:** Remove `analyze_unwired_callables()` from `wiring_gate.py`

---

### T01.03 -- Implement analyze_orphan_modules

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | Detects provider modules that exist in configured directories but are never imported or referenced, indicating dead or disconnected code. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | performance (AST parsing across directories), cross-cutting scope |
| Tier | STRICT |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0004/spec.md`

**Deliverables:**
1. `analyze_orphan_modules()` function in `src/superclaude/cli/audit/wiring_gate.py` scanning configured `provider_dir_names` for unreferenced modules

**Steps:**
1. **[PLANNING]** Read FR: Goal-2a, Goal-2b, Goal-2c, Goal-2d requirements; identify provider directory scanning patterns
2. **[PLANNING]** Review default `provider_dir_names` list (`steps/`, `handlers/`, `validators/`, `checks/`) and R6 risk mitigation (zero-findings SC-011 warning)
3. **[EXECUTION]** Implement directory scanner for configured `provider_dir_names` to enumerate Python modules
4. **[EXECUTION]** Implement import reference scanner using AST to detect which provider modules are referenced from non-provider code
5. **[EXECUTION]** Apply whitelist suppression (OQ-9: extended to orphan findings); emit SC-011 warning on zero findings
6. **[VERIFICATION]** Verify function detects orphan modules in test fixtures and emits SC-011 warning when no findings produced
7. **[COMPLETION]** Record implementation details to D-0004/spec.md

**Acceptance Criteria:**
- `analyze_orphan_modules()` exists in `src/superclaude/cli/audit/wiring_gate.py` and returns `list[WiringFinding]` with `finding_type='orphan_module'`
- Function scans only directories matching `provider_dir_names` from `WiringConfig` (Goal-2a)
- Zero-findings condition emits explicit SC-011 warning to prevent silent misconfiguration (R6 mitigation)
- Whitelist suppression applies to orphan findings per OQ-9 resolution

**Validation:**
- `uv run pytest tests/audit/test_wiring_gate.py -k "orphan_module" -v`
- Evidence: linkable artifact produced at D-0004/spec.md

**Dependencies:** T01.01
**Rollback:** Remove `analyze_orphan_modules()` from `wiring_gate.py`

---

### T01.04 -- Implement analyze_unwired_registries

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007 |
| Why | Detects dispatch registries (dicts/lists mapping names to callables) where entries reference non-existent or mistyped callable names. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STRICT |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0005 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0005/spec.md`

**Deliverables:**
1. `analyze_unwired_registries()` function in `src/superclaude/cli/audit/wiring_gate.py` using configurable `registry_patterns` to detect broken dispatch entries

**Steps:**
1. **[PLANNING]** Read FR: Goal-3a, Goal-3b requirements; identify registry pattern matching approach
2. **[PLANNING]** Review configurable `registry_patterns` from `WiringConfig` and R5 risk mitigation (log zero-registry warning)
3. **[EXECUTION]** Implement AST-based registry detection using `registry_patterns` configuration
4. **[EXECUTION]** Implement cross-reference validation between registry entries and available callable definitions
5. **[EXECUTION]** Apply whitelist suppression per OQ-9; emit warning on zero registries found (R5 mitigation)
6. **[VERIFICATION]** Verify function detects broken registry entries in test fixtures
7. **[COMPLETION]** Record implementation details to D-0005/spec.md

**Acceptance Criteria:**
- `analyze_unwired_registries()` exists in `src/superclaude/cli/audit/wiring_gate.py` and returns `list[WiringFinding]` with `finding_type='unwired_registry'`
- Function uses configurable `registry_patterns` from `WiringConfig` (Goal-3a)
- Whitelist suppression applies to registry findings per OQ-9 resolution
- Zero-registry condition emits warning (R5 mitigation)

**Validation:**
- `uv run pytest tests/audit/test_wiring_gate.py -k "unwired_registry" -v`
- Evidence: linkable artifact produced at D-0005/spec.md

**Dependencies:** T01.01
**Rollback:** Remove `analyze_unwired_registries()` from `wiring_gate.py`

---

### T01.05 -- Implement Report Emission and Gate Definition

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008, R-009, R-010 |
| Why | The report emission function serializes analysis results into frontmatter-conformant output, and the gate definition enables integration with the existing audit pipeline evaluation framework. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | compliance (GateCriteria schema conformance), schema (frontmatter serialization) |
| Tier | STRICT |
| Confidence | [█████████░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0006, D-0007 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0006/spec.md`
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0007/spec.md`

**Deliverables:**
1. `emit_report()` function in `src/superclaude/cli/audit/wiring_gate.py` producing 11 required frontmatter fields via `yaml.safe_dump()` (Goal-4a, Goal-4b, Goal-4c, Goal-4d, NFR-005)
2. `WIRING_GATE` constant and 5 semantic check functions with `(content: str) -> bool` signature in `src/superclaude/cli/audit/wiring_gate.py` (FR: T05, Constraint 6)

**Steps:**
1. **[PLANNING]** Read FR: Goal-4a through Goal-4d, NFR-005, FR: T05, Constraint 6 requirements; enumerate the 11 required frontmatter fields
2. **[PLANNING]** Confirm `GateCriteria` schema from `pipeline/models.py` (NFR-006: read-only, no modifications)
3. **[EXECUTION]** Implement `emit_report()` with `yaml.safe_dump()` serialization for all string frontmatter fields; include `whitelist_entries_applied`, `files_skipped`, `analysis_complete` fields
4. **[EXECUTION]** Implement `WIRING_GATE` constant matching `GateCriteria` schema with 5 `SemanticCheck` entries
5. **[EXECUTION]** Implement 5 semantic check functions each with `(content: str) -> bool` signature per Constraint 6
6. **[VERIFICATION]** Verify `emit_report()` output matches `GateCriteria` schema; all 5 semantic checks return correct booleans for valid/invalid inputs
7. **[COMPLETION]** Record implementation details to D-0006/spec.md and D-0007/spec.md

**Acceptance Criteria:**
- `emit_report()` in `src/superclaude/cli/audit/wiring_gate.py` produces output with exactly 11 frontmatter fields serialized via `yaml.safe_dump()` (NFR-005)
- `WIRING_GATE` constant in `src/superclaude/cli/audit/wiring_gate.py` matches `GateCriteria` schema from `pipeline/models.py`
- All 5 semantic check functions follow `(content: str) -> bool` signature (Constraint 6)
- Zero modifications to `pipeline/models.py` or `pipeline/gates.py` (NFR-006)

**Validation:**
- `uv run pytest tests/audit/test_wiring_gate.py -k "report or gate or semantic" -v`
- Evidence: linkable artifact produced at D-0006/spec.md and D-0007/spec.md

**Dependencies:** T01.01, T01.02, T01.03, T01.04
**Rollback:** Remove `emit_report()`, `WIRING_GATE`, and semantic check functions from `wiring_gate.py`

---

### Checkpoint: Phase 1 / Tasks T01.01-T01.05

**Purpose:** Verify all core analysis components are implemented before writing unit tests.
**Checkpoint Report Path:** `.dev/releases/current/v3.2_fidelity-refactor___/checkpoints/CP-P01-T01-T05.md`
**Verification:**
- All analysis functions (`analyze_unwired_callables`, `analyze_orphan_modules`, `analyze_unwired_registries`) exist and are callable
- `emit_report()` produces valid frontmatter; `WIRING_GATE` constant and 5 semantic checks defined
- Data models (`WiringFinding`, `WiringReport`, `WiringConfig`) and whitelist loader are functional
**Exit Criteria:**
- All 5 tasks (T01.01-T01.05) completed with deliverables D-0001 through D-0007 produced
- AST-only analysis verified (no subprocess calls, no dynamic dispatch resolution)
- Parse degradation path verified: bad file logged with structured warning, skipped, analysis continues

---

### T01.06 -- Write Unwired Callable and Orphan Module Tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011, R-012 |
| Why | Unit tests validate that unwired callable and orphan module analyzers correctly detect defects and handle edge cases including whitelist suppression and parse errors. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0008 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0008/evidence.md`

**Deliverables:**
1. 9 unit tests in `tests/audit/test_wiring_gate.py` covering unwired callable detection (4 tests: basic detection, whitelist suppression, parse error handling, no false positives on wired callables) and orphan module detection (5 tests: basic orphan, multi-directory scan, import reference exclusion, zero-findings SC-011 warning, whitelist suppression)

**Steps:**
1. **[PLANNING]** Review T01.02 and T01.03 implementations; identify boundary conditions for each analyzer
2. **[PLANNING]** Plan test fixtures: minimal Python files with known unwired callables and orphan modules
3. **[EXECUTION]** Write 4 unwired callable tests: basic detection, whitelist suppression, parse error graceful degradation, wired-callable no-false-positive
4. **[EXECUTION]** Write 5 orphan module tests: basic orphan detection, multi-directory scan, import reference exclusion, SC-011 zero-findings warning, whitelist suppression
5. **[EXECUTION]** Assert all `finding_type` values match expected strings ('unwired_callable', 'orphan_module')
6. **[VERIFICATION]** `uv run pytest tests/audit/test_wiring_gate.py -k "unwired_callable or orphan_module" -v` exits 0 with all 9 tests passing
7. **[COMPLETION]** Record test results to D-0008/evidence.md

**Acceptance Criteria:**
- `tests/audit/test_wiring_gate.py` exists with 9 tests covering unwired callable (4) and orphan module (5) analyzers
- All `finding_type` values asserted in tests match roadmap-specified strings
- Parse error handling test verifies structured warning emission and continued analysis (NFR-002)
- `uv run pytest tests/audit/test_wiring_gate.py -k "unwired_callable or orphan_module" -v` exits 0

**Validation:**
- `uv run pytest tests/audit/test_wiring_gate.py -k "unwired_callable or orphan_module" -v`
- Evidence: test output log archived to D-0008/evidence.md

**Dependencies:** T01.02, T01.03
**Rollback:** Delete unwired callable and orphan module test functions from `tests/audit/test_wiring_gate.py`

---

### T01.07 -- Write Registry, Report, and Gate Tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-013, R-014 |
| Why | Unit tests validate registry analysis correctness and report/gate evaluation compatibility with the existing pipeline framework. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0009 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0009/evidence.md`

**Deliverables:**
1. 5 unit tests in `tests/audit/test_wiring_gate.py` covering unwired registry detection (2 tests: broken entry detection, zero-registry warning) and report+gate evaluation (3 tests: frontmatter field count/serialization, gate pass on clean report, gate fail on invalid report)

**Steps:**
1. **[PLANNING]** Review T01.04 and T01.05 implementations; identify report schema and gate evaluation edge cases
2. **[PLANNING]** Plan test fixtures for registry patterns and report content
3. **[EXECUTION]** Write 2 unwired registry tests: broken dispatch entry detection, zero-registry warning emission
4. **[EXECUTION]** Write 3 report+gate tests: frontmatter 11-field completeness via `yaml.safe_dump()`, gate pass on clean report, gate fail on invalid/missing frontmatter
5. **[VERIFICATION]** `uv run pytest tests/audit/test_wiring_gate.py -k "registry or report or gate" -v` exits 0 with all 5 tests passing
6. **[COMPLETION]** Record test results to D-0009/evidence.md

**Acceptance Criteria:**
- `tests/audit/test_wiring_gate.py` contains 5 additional tests covering registry (2) and report+gate (3)
- Report test verifies exactly 11 frontmatter fields are present and serialized via `yaml.safe_dump()`
- Gate evaluation tests verify deterministic pass/fail behavior using `gate_passed()` from `pipeline/gates.py`
- `uv run pytest tests/audit/test_wiring_gate.py -k "registry or report or gate" -v` exits 0

**Validation:**
- `uv run pytest tests/audit/test_wiring_gate.py -k "registry or report or gate" -v`
- Evidence: test output log archived to D-0009/evidence.md

**Dependencies:** T01.04, T01.05
**Rollback:** Delete registry and report/gate test functions from `tests/audit/test_wiring_gate.py`

---

### T01.08 -- Create Test Fixtures

| Field | Value |
|---|---|
| Roadmap Item IDs | R-015 |
| Why | Shared test fixtures provide realistic Python source files and configurations used across all unit tests in Milestone 1.4. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0010 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.2_fidelity-refactor___/artifacts/D-0010/evidence.md`

**Deliverables:**
1. Test fixture files in `tests/audit/fixtures/` including sample Python packages with known wiring defects, valid whitelist YAML, and malformed whitelist YAML

**Steps:**
1. **[PLANNING]** Identify fixture requirements from T01.06 and T01.07 test plans
2. **[PLANNING]** Design minimal Python package structures that exercise all three analyzer code paths
3. **[EXECUTION]** Create fixture package with unwired callables (declared but not dispatched)
4. **[EXECUTION]** Create fixture with orphan provider modules in `steps/` and `handlers/` directories
5. **[EXECUTION]** Create fixture with broken dispatch registry entries and valid/malformed whitelist YAML files
6. **[VERIFICATION]** Verify all fixtures are importable/parseable by test runner; `uv run pytest tests/audit/ --collect-only` shows all tests collected
7. **[COMPLETION]** Record fixture inventory to D-0010/evidence.md

**Acceptance Criteria:**
- Directory `tests/audit/fixtures/` exists with fixture files covering all three finding types
- Fixtures include both valid and malformed whitelist YAML files for config loader testing
- `uv run pytest tests/audit/ --collect-only` successfully collects all test cases using these fixtures
- No fixture files contain executable side effects (pure data/source files only)

**Validation:**
- `uv run pytest tests/audit/ --collect-only` exits 0 with expected test count
- Evidence: fixture inventory documented at D-0010/evidence.md

**Dependencies:** T01.06, T01.07
**Rollback:** Delete `tests/audit/fixtures/` directory

**Notes:** Fixtures should be created alongside or after test functions, as test requirements drive fixture design. Listed last in phase for logical grouping but may be developed concurrently with T01.06/T01.07.

---

### Checkpoint: End of Phase 1

**Purpose:** Gate for Phase 2 entry — verify all Phase 1 deliverables are complete and analysis engine is functional.
**Checkpoint Report Path:** `.dev/releases/current/v3.2_fidelity-refactor___/checkpoints/CP-P01-END.md`
**Verification:**
- All three analyzer functions pass with correct finding types in unit tests
- Parse degradation verified: bad file logged, skipped, analysis continues (NFR-002)
- Whitelist behavior stable — suppression count reported in frontmatter (Goal-1c, Goal-4a)
**Exit Criteria:**
- 14+ unit tests passing with all `finding_type` values asserted (SC-001 through SC-005, SC-007 validated)
- Gate passes clean report; gate fails invalid report deterministically
- Coverage >= 90% line coverage on `wiring_gate.py` (NFR-003)
