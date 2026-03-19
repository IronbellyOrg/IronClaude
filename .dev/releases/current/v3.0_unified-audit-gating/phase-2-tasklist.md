# Phase 2 -- Core Analysis Engine

Build the standalone wiring analyzer that detects unwired injectable callables, orphan modules, and broken dispatch registries using deterministic AST analysis. This phase produces the core analysis engine with no pipeline integration, validated by unit tests achieving the milestone of `run_wiring_analysis()` returning correct `WiringReport` for all three detection types.

### T02.01 -- Define WiringConfig Dataclass with Registry Patterns and Whitelist Loading in cli/audit/wiring_config.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004, R-009 |
| Why | The analysis engine requires configuration for registry patterns, provider directories, and whitelist-based suppression before any analyzer can execute |
| Effort | M |
| Risk | Medium |
| Risk Drivers | audit, compliance (whitelist strictness per rollout_mode) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0002, D-0047 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0002/spec.md
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0047/spec.md

**Deliverables:**
- `WiringConfig` dataclass in `src/superclaude/cli/audit/wiring_config.py` with fields for `provider_dir_names`, `exclude_patterns`, `registry_patterns`, `whitelist_path`, and `rollout_mode`
- `DEFAULT_REGISTRY_PATTERNS` constant with regex patterns for dispatch registry detection per section 4.2.1
- Whitelist loading function that reads `wiring_whitelist.yaml` and returns suppression entries
- `wiring_whitelist.yaml` template file at `src/superclaude/cli/audit/wiring_whitelist.yaml`

**Steps:**
1. **[PLANNING]** Read `pipeline/models.py` to understand existing `GateCriteria`, `GateMode` contracts that WiringConfig must align with
2. **[PLANNING]** Verify `src/superclaude/cli/audit/` directory exists; create if needed
3. **[EXECUTION]** Define `WiringConfig` dataclass with typed fields per section 4.2.1 and section 5.2.1
4. **[EXECUTION]** Define `DEFAULT_REGISTRY_PATTERNS` as a tuple of compiled regex patterns for registry file detection
5. **[EXECUTION]** Implement `load_whitelist(path: Path) -> list[WhitelistEntry]` function that parses YAML and returns typed suppression entries
6. **[EXECUTION]** Create `wiring_whitelist.yaml` with documented schema and example entries
7. **[VERIFICATION]** Run `uv run pytest tests/audit/test_wiring_gate.py -v` to validate dataclass instantiation and whitelist loading
8. **[COMPLETION]** Document WiringConfig field semantics in module docstring

**Acceptance Criteria:**
- `from superclaude.cli.audit.wiring_config import WiringConfig, DEFAULT_REGISTRY_PATTERNS, load_whitelist` imports successfully without errors
- `WiringConfig` dataclass accepts `provider_dir_names`, `exclude_patterns`, `registry_patterns`, `whitelist_path`, and `rollout_mode` with type-checked defaults
- `load_whitelist()` returns an empty list for a nonexistent path and a populated list for a valid YAML file
- `wiring_whitelist.yaml` exists at `src/superclaude/cli/audit/wiring_whitelist.yaml` with documented schema

**Validation:**
- `uv run pytest tests/audit/ -k "wiring_config" -v` exits 0
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0002/spec.md

**Dependencies:** T01.01 (OQ-3 determines whitelist strictness per rollout_mode)
**Rollback:** Delete `src/superclaude/cli/audit/wiring_config.py` and `wiring_whitelist.yaml`
**Notes:** Roadmap task 1.5 (whitelist loading + suppression) is merged into this task per roadmap note "(included in 1.1a)".

---

### T02.02 -- Define WiringFinding and WiringReport Dataclasses in cli/audit/wiring_gate.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Why | All three analyzers need structured output types to produce findings and aggregate them into a report for gate evaluation |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0003/spec.md

**Deliverables:**
- `WiringFinding` dataclass in `src/superclaude/cli/audit/wiring_gate.py` with fields for finding type (unwired/orphan/registry), severity (critical/major/minor), file path, symbol name, evidence text, and suppressed flag
- `WiringReport` dataclass aggregating findings with metadata (scan timestamp, file count, config summary, rollout_mode)

**Steps:**
1. **[PLANNING]** Review section 5.1 of merged-spec for WiringFinding and WiringReport field requirements
2. **[PLANNING]** Check that `WiringConfig` from T02.01 is available for type references
3. **[EXECUTION]** Define `WiringFinding` dataclass with `finding_type: Literal["unwired", "orphan", "registry"]`, `severity: Literal["critical", "major", "minor"]`, `file_path: Path`, `symbol_name: str`, `evidence: str`, `suppressed: bool`
4. **[EXECUTION]** Define `WiringReport` dataclass with `findings: list[WiringFinding]`, `files_scanned: int`, `files_skipped: int`, `scan_duration_seconds: float`, `config: WiringConfig`, `rollout_mode: str`
5. **[VERIFICATION]** Instantiate both dataclasses with test data and verify field access
6. **[COMPLETION]** Add type annotations and module-level docstring

**Acceptance Criteria:**
- `from superclaude.cli.audit.wiring_gate import WiringFinding, WiringReport` imports successfully
- `WiringFinding` enforces `finding_type` as one of "unwired", "orphan", "registry" via type annotation
- `WiringReport.findings` is a list of `WiringFinding` instances with correct aggregation semantics
- Both dataclasses are serializable to dict via `dataclasses.asdict()`

**Validation:**
- `uv run pytest tests/audit/ -k "wiring_finding or wiring_report" -v` exits 0
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0003/spec.md

**Dependencies:** T02.01
**Rollback:** Remove WiringFinding and WiringReport classes from wiring_gate.py

---

### T02.03 -- Implement Unwired Callable Analyzer in cli/audit/wiring_gate.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | G-001 requires detection of injectable callables (Optional[Callable] parameters) that are never wired in the codebase |
| Effort | M |
| Risk | Medium |
| Risk Drivers | audit (wiring analysis), compliance (G-001 success criterion) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0004/spec.md

**Deliverables:**
- `analyze_unwired_callables(config: WiringConfig, source_dir: Path) -> list[WiringFinding]` function that uses AST to find `Optional[Callable]` parameters and checks whether they are wired anywhere in the scanned files

**Steps:**
1. **[PLANNING]** Read section 5.2.1 for the unwired callable detection algorithm and whitelist suppression rules
2. **[PLANNING]** Identify test fixtures needed: Python files with both wired and unwired Optional[Callable] parameters
3. **[EXECUTION]** Implement AST visitor that collects function parameters typed as `Optional[Callable]` across all scanned files
4. **[EXECUTION]** Implement cross-reference check: for each callable parameter, search for call sites that pass a concrete callable value
5. **[EXECUTION]** Apply whitelist suppression: mark findings as `suppressed=True` when matching whitelist entries
6. **[EXECUTION]** Handle `SyntaxError` gracefully per R2: log, skip file, continue with empty analysis
7. **[VERIFICATION]** Run `uv run pytest tests/audit/test_wiring_gate.py -k "unwired" -v` to validate detection against fixtures (SC-001)
8. **[COMPLETION]** Document algorithm in function docstring with reference to section 5.2.1

**Acceptance Criteria:**
- `analyze_unwired_callables()` detects at least 1 unwired callable finding from a test fixture containing an `Optional[Callable]` parameter with no call-site wiring (SC-001)
- Whitelisted entries produce findings with `suppressed=True` and are excluded from gate-blocking counts
- Files with `SyntaxError` produce a log warning and do not crash the analyzer
- Function returns `list[WiringFinding]` with `finding_type="unwired"` for all detected instances

**Validation:**
- `uv run pytest tests/audit/test_wiring_gate.py -k "unwired" -v` exits 0 with at least 1 test passing
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0004/spec.md

**Dependencies:** T02.01, T02.02
**Rollback:** Remove `analyze_unwired_callables()` function from wiring_gate.py

---

### T02.04 -- Implement Orphan Module Analyzer in cli/audit/wiring_gate.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007 |
| Why | G-002 requires detection of modules in provider directories that are not imported or referenced by any other module in the codebase |
| Effort | M |
| Risk | Medium |
| Risk Drivers | audit (wiring analysis), compliance (G-002 success criterion) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0005 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0005/spec.md

**Deliverables:**
- `analyze_orphan_modules(config: WiringConfig, source_dir: Path) -> list[WiringFinding]` function that identifies Python modules in configured `provider_dir_names` directories that are not imported by any other module

**Steps:**
1. **[PLANNING]** Read section 5.2.2 for the orphan module detection algorithm and dual evidence rule
2. **[PLANNING]** Identify test fixtures: provider directories with both imported and orphaned modules
3. **[EXECUTION]** Scan `provider_dir_names` directories for Python files, collecting module paths
4. **[EXECUTION]** Build import graph using AST: for each scanned file, extract `import` and `from ... import` statements
5. **[EXECUTION]** Flag modules with zero inbound imports from outside their own directory as orphan candidates
6. **[EXECUTION]** Apply `exclude_patterns` filtering and whitelist suppression
7. **[VERIFICATION]** Run `uv run pytest tests/audit/test_wiring_gate.py -k "orphan" -v` to validate detection against fixtures (SC-002)
8. **[COMPLETION]** Document the dual evidence rule behavior in docstring (full rule requires Phase 7 plugin)

**Acceptance Criteria:**
- `analyze_orphan_modules()` detects at least 1 orphan module finding from a test fixture with an unimported provider module (SC-002)
- Modules with valid inbound imports are not flagged as orphans
- `exclude_patterns` correctly filters out matched files from analysis per OQ-2 decision
- Function returns `list[WiringFinding]` with `finding_type="orphan"` for all detected instances

**Validation:**
- `uv run pytest tests/audit/test_wiring_gate.py -k "orphan" -v` exits 0 with at least 1 test passing
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0005/spec.md

**Dependencies:** T02.01, T02.02
**Rollback:** Remove `analyze_orphan_modules()` function from wiring_gate.py

---

### Checkpoint: Phase 2 / Tasks T02.01-T02.04

**Purpose:** Verify core dataclasses and first two analyzers are functional before proceeding to registry analysis.
**Checkpoint Report Path:** .dev/releases/current/v3.0_unified-audit-gating/checkpoints/CP-P02-T01-T04.md
**Verification:**
- WiringConfig, WiringFinding, WiringReport dataclasses instantiate correctly with type-checked fields
- Unwired callable analyzer detects known fixtures (SC-001)
- Orphan module analyzer detects known fixtures (SC-002)
**Exit Criteria:**
- `uv run pytest tests/audit/ -k "wiring_config or wiring_finding or unwired or orphan" -v` exits 0
- No import errors when loading `superclaude.cli.audit.wiring_config` and `superclaude.cli.audit.wiring_gate`
- Whitelist suppression produces `suppressed=True` findings for matched entries

---

### T02.05 -- Implement Registry Analyzer in cli/audit/wiring_gate.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008 |
| Why | G-003 requires detection of broken dispatch registries where registered handler keys reference nonexistent callables or modules |
| Effort | M |
| Risk | Medium |
| Risk Drivers | audit (wiring analysis), compliance (G-003 success criterion) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0006 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0006/spec.md

**Deliverables:**
- `analyze_registries(config: WiringConfig, source_dir: Path) -> list[WiringFinding]` function that detects broken dispatch registry entries using `DEFAULT_REGISTRY_PATTERNS` to locate registry files and AST to verify referenced callables exist

**Steps:**
1. **[PLANNING]** Read section 5.2.3 for registry analysis algorithm and pattern matching rules
2. **[PLANNING]** Create test fixtures: registry files with both valid and broken handler references
3. **[EXECUTION]** Scan source directory for files matching `DEFAULT_REGISTRY_PATTERNS` regex patterns
4. **[EXECUTION]** Parse registry files using AST to extract key-to-callable mappings (dict literals, decorator registrations)
5. **[EXECUTION]** For each registered callable reference, verify the target exists via import resolution or AST symbol lookup
6. **[EXECUTION]** Generate `WiringFinding` with `finding_type="registry"` for broken references
7. **[VERIFICATION]** Run `uv run pytest tests/audit/test_wiring_gate.py -k "registry" -v` to validate detection against fixtures (SC-003)
8. **[COMPLETION]** Document registry pattern matching approach in function docstring

**Acceptance Criteria:**
- `analyze_registries()` detects at least 1 broken registry finding from a test fixture with a handler referencing a nonexistent callable (SC-003)
- Valid registry entries with resolvable callables are not flagged
- Registry files matched by `DEFAULT_REGISTRY_PATTERNS` are correctly identified
- Function returns `list[WiringFinding]` with `finding_type="registry"` for all detected instances

**Validation:**
- `uv run pytest tests/audit/test_wiring_gate.py -k "registry" -v` exits 0 with at least 1 test passing
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0006/spec.md

**Dependencies:** T02.01, T02.02
**Rollback:** Remove `analyze_registries()` function from wiring_gate.py

---

### T02.06 -- Implement ast_analyze_file() Utility in cli/audit/wiring_analyzer.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-010 |
| Why | G-008 requires a shared AST analysis utility that produces FileAnalysis objects for use by all three analyzers and the future ToolOrchestrator plugin |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0007 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0007/spec.md

**Deliverables:**
- `ast_analyze_file(file_path: Path) -> FileAnalysis` function in `src/superclaude/cli/audit/wiring_analyzer.py` that parses a Python file and returns structured analysis including imports, callable definitions, and class hierarchies

**Steps:**
1. **[PLANNING]** Read section 5.3 for ast_analyze_file() specification and `FileAnalysis` type from `cli/audit/tool_orchestrator.py`
2. **[PLANNING]** Identify the `FileAnalysis` type structure from the existing `ToolOrchestrator` contract
3. **[EXECUTION]** Implement `ast_analyze_file()` using Python `ast` module to parse the file and populate `FileAnalysis` fields (imports, definitions, references)
4. **[EXECUTION]** Handle `SyntaxError` gracefully: return empty `FileAnalysis` with error metadata per R2 mitigation
5. **[EXECUTION]** Implement efficient caching: avoid re-parsing files already analyzed in the same run
6. **[VERIFICATION]** Run `uv run pytest tests/audit/test_wiring_analyzer.py -v` to validate against test fixtures
7. **[COMPLETION]** Document return type and error handling in function docstring

**Acceptance Criteria:**
- `ast_analyze_file()` returns a `FileAnalysis` object with populated `imports`, `definitions`, and `references` fields for valid Python files
- `SyntaxError` in input files returns an empty `FileAnalysis` without raising an exception
- Function processes a 500-line Python file in under 100ms
- No imports from `pipeline/*` in `wiring_analyzer.py` (NFR-007 compliance)

**Validation:**
- `uv run pytest tests/audit/test_wiring_analyzer.py -v` exits 0
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0007/spec.md

**Dependencies:** T02.01 (WiringConfig for configuration context)
**Rollback:** Delete `src/superclaude/cli/audit/wiring_analyzer.py`

---

### T02.07 -- Implement Unit Test Suite for Analyzers and Whitelist in tests/audit/

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011, R-012 |
| Why | SC-001 through SC-003 and SC-007 require validated test evidence, and section 10.1 mandates >=20 unit tests with section 10.3 requiring >=90% coverage |
| Effort | M |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0008, D-0009 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0008/evidence.md
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0009/evidence.md

**Deliverables:**
- `tests/audit/test_wiring_gate.py` with >=15 unit tests covering all three analyzers (unwired SC-001, orphan SC-002, registry SC-003) and whitelist suppression (SC-007)
- `tests/audit/test_wiring_analyzer.py` with >=5 unit tests for `ast_analyze_file()` utility
- `tests/audit/fixtures/` directory with Python test fixture files for each detection type
- Performance benchmark test validating <5s execution for 50-file fixture (SC-008)

**Steps:**
1. **[PLANNING]** Review SC-001 through SC-003, SC-007, SC-008, and section 10.1/10.3 test requirements
2. **[PLANNING]** Design fixture files: valid wiring, unwired callables, orphan modules, broken registries, whitelist-suppressed entries
3. **[EXECUTION]** Create `tests/audit/fixtures/` directory with at least 4 Python fixture files
4. **[EXECUTION]** Write test_wiring_gate.py with tests for: unwired detection (>=3), orphan detection (>=3), registry detection (>=3), whitelist suppression (>=3), SyntaxError handling (>=2), edge cases (>=1)
5. **[EXECUTION]** Write test_wiring_analyzer.py with tests for: valid file analysis (>=2), SyntaxError handling (>=1), empty file (>=1), import extraction (>=1)
6. **[EXECUTION]** Write performance benchmark test generating 50 fixture files and asserting <5s completion
7. **[VERIFICATION]** Run `uv run pytest tests/audit/ -v --cov=superclaude.cli.audit` and verify >=20 tests pass with >=90% coverage
8. **[COMPLETION]** Record coverage report in evidence artifact

**Acceptance Criteria:**
- `uv run pytest tests/audit/ -v` exits 0 with >=20 unit tests passing
- `uv run pytest tests/audit/ --cov=superclaude.cli.audit` shows >=90% coverage on `wiring_gate.py` and `wiring_analyzer.py`
- Performance benchmark test confirms <5s for 50-file fixture (SC-008)
- Fixture directory `tests/audit/fixtures/` contains at least 4 Python files with documented purpose

**Validation:**
- `uv run pytest tests/audit/ -v --cov=superclaude.cli.audit` exits 0 with >=20 tests and >=90% coverage
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0008/evidence.md

**Dependencies:** T02.01, T02.02, T02.03, T02.04, T02.05, T02.06
**Rollback:** Delete test files and fixtures directory

---

### Checkpoint: End of Phase 2

**Purpose:** Validate milestone M1: run_wiring_analysis() returns correct WiringReport for all three detection types.
**Checkpoint Report Path:** .dev/releases/current/v3.0_unified-audit-gating/checkpoints/CP-P02-END.md
**Verification:**
- All 3 detection types (unwired, orphan, registry) produce correct findings against test fixtures (SC-001, SC-002, SC-003)
- Whitelist suppression works correctly (SC-007) and SyntaxError is handled gracefully (R2)
- Performance benchmark passes: <5s for 50-file fixture (SC-008)
**Exit Criteria:**
- `uv run pytest tests/audit/ -v` exits 0 with >=20 tests passing
- Coverage >=90% on wiring_gate.py and wiring_analyzer.py
- No imports from `pipeline/*` in any new `cli/audit/` files (NFR-007)
