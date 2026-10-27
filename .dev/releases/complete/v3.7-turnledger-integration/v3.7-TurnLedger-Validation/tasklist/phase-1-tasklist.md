# Phase 1 -- Foundation

Build the two cross-cutting infrastructure pieces that all subsequent phases depend on: the JSONL audit trail system (FR-7) and the AST-based reachability analyzer (FR-4). The audit trail fixture is the hard dependency for Phase 2; the reachability analyzer is required for Phase 3.

---

### T01.01 -- Implement JSONL audit record writer

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001 |
| Why | All subsequent test phases require audit records; the writer is the foundational component of the audit trail infrastructure (FR-7.1) |
| Effort | M |
| Risk | Medium |
| Risk Drivers | audit, schema |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0001 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0001/spec.md`
- `TASKLIST_ROOT/artifacts/D-0001/evidence.md`

**Deliverables:**
- `tests/audit-trail/audit_writer.py` — JSONL audit record writer with 10-field schema: `test_id`, `spec_ref`, `timestamp`, `assertion_type`, `inputs`, `observed`, `expected`, `verdict`, `evidence`, `duration_ms` (auto-computed from test start/end)

**Steps:**
1. **[PLANNING]** Read FR-7.1 requirements and identify the 10-field schema contract
2. **[PLANNING]** Check existing `tests/audit-trail/` directory structure; confirm no prior `audit_writer.py` exists
3. **[EXECUTION]** Create `tests/audit-trail/audit_writer.py` with `AuditWriter` class: `__init__(output_path)`, `record(**fields)` method, auto-computed `duration_ms` from test start/end timestamps
4. **[EXECUTION]** Implement JSONL line-per-record output using stdlib `json` module; one `record()` call = one JSON line appended
5. **[EXECUTION]** Add schema validation: reject records missing any of the 10 required fields; raise `ValueError` with field name
6. **[VERIFICATION]** Run `uv run pytest tests/audit-trail/test_audit_writer.py -v` to validate writer produces valid JSONL with all 10 fields
7. **[COMPLETION]** Verify JSONL output is parseable by `json.loads()` line-by-line; record evidence

**Acceptance Criteria:**
- `tests/audit-trail/audit_writer.py` exists and `AuditWriter.record()` produces valid JSONL lines with all 10 schema fields present
- No external dependencies beyond stdlib `json`; no `mock.patch` usage
- Given identical inputs, `record()` produces identical JSONL output (deterministic except for `timestamp` and `duration_ms`)
- Schema fields documented in module docstring with types and constraints

**Validation:**
- `uv run pytest tests/audit-trail/test_audit_writer.py -v`
- Evidence: JSONL sample output file in `TASKLIST_ROOT/evidence/`

**Dependencies:** None
**Rollback:** Delete `tests/audit-trail/audit_writer.py`
**Notes:** Design assumption per roadmap: tests run sequentially within a session; no write locking needed.

---

### T01.02 -- Implement session-scoped audit_trail pytest fixture

| Field | Value |
|---|---|
| Roadmap Item IDs | R-002 |
| Why | All E2E tests in Phases 2-4 use this fixture to emit JSONL audit records (FR-7.3) |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0002 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0002/spec.md`
- `TASKLIST_ROOT/artifacts/D-0002/evidence.md`

**Deliverables:**
- `tests/v3.3/conftest.py` — session-scoped `audit_trail` fixture that opens JSONL in `results_dir`, provides `record()` method, auto-flushes after each test
- `tests/roadmap/conftest.py` — registers `audit_trail` fixture for `tests/roadmap/` test suite per roadmap integration point

**Steps:**
1. **[PLANNING]** Read T01.01 deliverable (`audit_writer.py`) API surface to understand `AuditWriter` interface
2. **[PLANNING]** Confirm `tests/v3.3/conftest.py` is the target location per roadmap integration point specification
3. **[EXECUTION]** Create `tests/v3.3/conftest.py` with `@pytest.fixture(scope="session")` named `audit_trail`
4. **[EXECUTION]** Fixture instantiates `AuditWriter(output_path=results_dir / "audit.jsonl")`, yields `record()` method, auto-flushes on teardown
5. **[EXECUTION]** Register fixture also at `tests/roadmap/conftest.py` per roadmap integration point
6. **[VERIFICATION]** Run `uv run pytest tests/v3.3/ -v --co` to verify fixture is discoverable
7. **[COMPLETION]** Document fixture scope and usage pattern in conftest.py docstring

**Acceptance Criteria:**
- `tests/v3.3/conftest.py` exists with session-scoped `audit_trail` fixture that provides a `record()` method
- Fixture auto-flushes JSONL output after each test; no data loss on test failure
- Fixture is importable and discoverable by pytest in both `tests/v3.3/` and `tests/roadmap/` directories
- Fixture docstring documents scope, output path, and `record()` method signature

**Validation:**
- `uv run pytest tests/v3.3/ -v --co` (fixture collection check)
- Evidence: conftest.py file with fixture implementation

**Dependencies:** T01.01
**Rollback:** Delete `tests/v3.3/conftest.py` and `tests/roadmap/conftest.py`

---

### T01.03 -- Implement session-end summary report generation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | Session-end summary provides aggregate pass/fail/coverage statistics for audit trail (FR-7.3) |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0003/spec.md`

**Deliverables:**
- Summary report generation logic in `audit_trail` fixture teardown: emits total/passed/failed/wiring coverage at session end

**Steps:**
1. **[PLANNING]** Identify where summary generation hooks into `audit_trail` fixture teardown
2. **[PLANNING]** Define summary output fields: total tests, passed, failed, wiring coverage percentage
3. **[EXECUTION]** Add summary generation to `audit_trail` fixture's session teardown: parse JSONL, count verdicts, compute wiring coverage
4. **[EXECUTION]** Write summary as final JSONL record with `assertion_type: "session_summary"` or as separate summary file
5. **[VERIFICATION]** Run a minimal test session and verify summary output contains all 4 fields with correct counts
6. **[COMPLETION]** Record summary output format in fixture docstring

**Acceptance Criteria:**
- Session-end summary includes total/passed/failed counts and wiring coverage percentage
- Summary is generated automatically during fixture teardown without manual invocation
- Summary output is deterministic given the same test results
- Summary format documented in `tests/v3.3/conftest.py` docstring

**Validation:**
- Manual check: run `uv run pytest tests/v3.3/ -v` and verify summary appears in output or summary file
- Evidence: sample summary output

**Dependencies:** T01.02
**Rollback:** Remove summary generation from fixture teardown

---

### T01.04 -- Implement JSONL verifiability property tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Why | Proves audit trail meets 4 third-party verifiability properties required by FR-7.2 |
| Effort | S |
| Risk | Low |
| Risk Drivers | audit |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0004/spec.md`

**Deliverables:**
- Verification tests in `tests/audit-trail/test_audit_writer.py` confirming 4 properties: real timestamps, spec-traced records, runtime observations, explicit verdicts

**Steps:**
1. **[PLANNING]** Enumerate the 4 third-party verifiability properties from FR-7.2
2. **[PLANNING]** Design one test per property targeting `AuditWriter` output
3. **[EXECUTION]** Write test `test_real_timestamps`: verify `timestamp` field is ISO-8601 and within reasonable bounds of `datetime.now()`
4. **[EXECUTION]** Write test `test_spec_traced`: verify `spec_ref` field is non-empty and matches `FR-*` or `SC-*` pattern
5. **[EXECUTION]** Write test `test_runtime_observations`: verify `observed` field contains runtime data (not hardcoded)
6. **[EXECUTION]** Write test `test_explicit_verdict`: verify `verdict` field is one of `PASS`, `FAIL`, `SKIP`
7. **[VERIFICATION]** Run `uv run pytest tests/audit-trail/test_audit_writer.py -v`
8. **[COMPLETION]** Emit audit records for each test using `audit_trail` fixture

**Acceptance Criteria:**
- 4 tests exist in `tests/audit-trail/test_audit_writer.py`, one per verifiability property
- All 4 tests exercise real `AuditWriter` output (no mocks on writer internals)
- Tests are deterministic and do not depend on wall-clock timing beyond reasonable bounds
- Each test emits a JSONL audit record via `audit_trail` fixture

**Validation:**
- `uv run pytest tests/audit-trail/test_audit_writer.py -v`
- Evidence: test output log showing 4 passing tests

**Dependencies:** T01.01, T01.02
**Rollback:** Remove verifiability tests from test file

---

### Checkpoint: Phase 1 / Tasks T01.01-T01.04

**Purpose:** Verify audit trail infrastructure (FR-7) is functional before proceeding to reachability analyzer and Phase 2.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P01-T01-T04.md`
**Verification:**
- `AuditWriter` produces valid JSONL with all 10 schema fields
- `audit_trail` fixture is session-scoped and discoverable in both `tests/v3.3/` and `tests/roadmap/`
- All 4 verifiability property tests pass

**Exit Criteria:**
- `uv run pytest tests/audit-trail/ tests/v3.3/ -v` exits 0
- JSONL output file exists and is parseable line-by-line
- Summary report generation produces correct aggregate counts

---

### T01.05 -- Define wiring manifest YAML schema

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Why | The manifest schema defines the contract for entry points and reachable targets that the AST analyzer validates against (FR-4.1) |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0005 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0005/spec.md`

**Deliverables:**
- Wiring manifest YAML schema with `entry_points` section listing callable entry points and `required_reachable` section listing target symbols with spec references

**Steps:**
1. **[PLANNING]** Review FR-4.1 requirements for manifest schema structure
2. **[PLANNING]** Identify required sections: `entry_points`, `required_reachable`
3. **[EXECUTION]** Define YAML schema: `entry_points` as list of `{module, function, spec_ref}` entries; `required_reachable` as list of `{symbol, module, spec_refs}` entries
4. **[EXECUTION]** Document schema in manifest file header comments
5. **[VERIFICATION]** Validate schema is parseable by PyYAML; verify required fields are present
6. **[COMPLETION]** Record schema definition as evidence

**Acceptance Criteria:**
- YAML schema defines `entry_points` and `required_reachable` sections with documented field contracts
- Schema is parseable by stdlib/PyYAML without errors
- Each `required_reachable` entry includes at least one `spec_ref` for traceability
- Schema documented with inline YAML comments

**Validation:**
- Manual check: YAML schema loads without error via `yaml.safe_load()`
- Evidence: schema definition file

**Dependencies:** None
**Rollback:** Delete schema definition

---

### T01.06 -- Implement AST call-chain analyzer module

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006, R-007 |
| Why | The AST analyzer is the core engine for reachability evaluation (FR-4.2); it must resolve cross-module imports and handle lazy imports. Documented limitations are required by NFR-6. |
| Effort | L |
| Risk | High |
| Risk Drivers | cross-cutting scope (cross-module), performance (AST parsing) |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0006 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0006/spec.md`
- `TASKLIST_ROOT/artifacts/D-0006/evidence.md`

**Deliverables:**
- `src/superclaude/cli/audit/reachability.py` — AST call-chain analyzer: `ast.parse()` -> call graph construction -> BFS/DFS reachability; cross-module import resolution; lazy import handling; documented limitations in module docstring (dynamic dispatch false negatives, `TYPE_CHECKING` exclusions, function-scope lazy imports included)

**Steps:**
1. **[PLANNING]** Analyze target code paths in `executor.py` to understand call graph shape and cross-module import patterns
2. **[PLANNING]** Identify known lazy import patterns in target codebase; review R-1 risk mitigation strategy (function-scope import extraction first)
3. **[EXECUTION]** Create `src/superclaude/cli/audit/reachability.py` with `ReachabilityAnalyzer` class: `__init__(manifest_path)`, `analyze(source_root) -> ReachabilityReport`
4. **[EXECUTION]** Implement `ast.parse()` -> `ast.NodeVisitor` subclass to build call graph; handle `ast.Import`, `ast.ImportFrom`, `ast.Call` nodes
5. **[EXECUTION]** Add cross-module import resolution: resolve `from X import Y` to file paths; handle relative imports
6. **[EXECUTION]** Add function-scope lazy import detection: walk `ast.FunctionDef` bodies for nested `import` statements
7. **[EXECUTION]** Document limitations in module docstring per NFR-6: dynamic dispatch (`getattr`, `**kwargs`) produces false negatives; `TYPE_CHECKING` conditionals excluded; lazy imports inside functions included
8. **[VERIFICATION]** Sub-agent verification: analyzer resolves at least one representative lazy-import case from target code paths (per R-1 exit criteria)
9. **[COMPLETION]** Record analysis of known limitations and edge cases

**Acceptance Criteria:**
- `src/superclaude/cli/audit/reachability.py` exists with `ReachabilityAnalyzer` class exposing `analyze()` method that returns structured `ReachabilityReport`
- Cross-module import resolution handles `from X import Y` and relative imports without crashing on missing modules
- Module docstring documents all 3 limitation categories per NFR-6: dynamic dispatch, TYPE_CHECKING, lazy imports
- Analyzer correctly resolves at least one representative lazy-import case from target code paths (per R-1 exit criteria)

**Validation:**
- `uv run pytest tests/v3.3/test_reachability_eval.py -v` (after T01.08)
- Evidence: analysis report for executor.py entry points

**Dependencies:** T01.05
**Rollback:** Delete `src/superclaude/cli/audit/reachability.py`
**Notes:** Highest technical risk item (R-1). Start with allowlist of known FR->function mappings per architect recommendation.

---

### T01.07 -- Populate initial wiring manifest YAML

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008 |
| Why | The manifest must be populated with executor.py entry points to serve as the reachability analyzer's input (FR-4.1) |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0007 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0007/spec.md`

**Deliverables:**
- `tests/v3.3/wiring_manifest.yaml` — populated wiring manifest for executor.py entry points using the schema from T01.05

**Steps:**
1. **[PLANNING]** Read executor.py to identify callable entry points and required reachable symbols
2. **[PLANNING]** Cross-reference FR-1 sub-requirements to identify all wiring points that need manifest entries
3. **[EXECUTION]** Create `tests/v3.3/wiring_manifest.yaml` with `entry_points` populated from executor.py public API and `required_reachable` populated from FR-1 wiring targets
4. **[VERIFICATION]** Quick sanity check: YAML loads without error; all `entry_points` reference real module paths
5. **[COMPLETION]** Verify manifest covers all FR-1 wiring points

**Acceptance Criteria:**
- `tests/v3.3/wiring_manifest.yaml` exists and is valid YAML parseable by `yaml.safe_load()`
- `entry_points` section lists executor.py callable entry points with module paths
- `required_reachable` section lists target symbols with spec references (FR-1.x)
- Manifest follows schema defined in T01.05

**Validation:**
- Manual check: `yaml.safe_load()` succeeds; entry_points are non-empty
- Evidence: populated manifest file

**Dependencies:** T01.05
**Rollback:** Delete `tests/v3.3/wiring_manifest.yaml`

---

### T01.08 -- Write AST analyzer unit tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009 |
| Why | Unit tests validate the AST analyzer in isolation before it is integrated into the reachability gate (FR-4.4) |
| Effort | M |
| Risk | Medium |
| Risk Drivers | cross-cutting scope (cross-module resolution) |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0008 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0008/spec.md`
- `TASKLIST_ROOT/artifacts/D-0008/evidence.md`

**Deliverables:**
- `tests/v3.3/test_reachability_eval.py` — unit tests for AST analyzer covering: known-good reachability (positive), known-bad unreachability (negative), cross-module import resolution, lazy import detection

**Steps:**
1. **[PLANNING]** Identify test cases from R-1 exit criteria: known-good reachability, known-bad unreachability, lazy import resolution
2. **[PLANNING]** Design test fixtures with synthetic Python modules for controlled AST analysis
3. **[EXECUTION]** Write `test_known_good_reachability`: analyzer returns REACHABLE for directly called functions
4. **[EXECUTION]** Write `test_known_bad_unreachability`: analyzer returns UNREACHABLE for dead code paths
5. **[EXECUTION]** Write `test_cross_module_resolution`: analyzer follows `from X import Y` across module boundaries
6. **[EXECUTION]** Write `test_lazy_import_detection`: analyzer detects imports inside function bodies
7. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_reachability_eval.py -v`
8. **[COMPLETION]** All tests emit JSONL audit records via `audit_trail` fixture

**Acceptance Criteria:**
- `tests/v3.3/test_reachability_eval.py` exists with tests covering known-good, known-bad, cross-module, and lazy-import cases
- All tests exercise `ReachabilityAnalyzer` directly (no mocks on analyzer internals)
- Tests use synthetic Python module fixtures for deterministic AST analysis
- All tests emit JSONL audit records via `audit_trail` fixture per REQ-078

**Validation:**
- `uv run pytest tests/v3.3/test_reachability_eval.py -v`
- Evidence: test output log showing all cases pass

**Dependencies:** T01.06, T01.07, T01.02
**Rollback:** Delete `tests/v3.3/test_reachability_eval.py`

---

### Checkpoint: End of Phase 1

**Purpose:** Confirm both infrastructure pieces (audit trail + AST reachability analyzer) are functional and tested before Phase 2 test authoring begins.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P01-END.md`
**Verification:**
- Audit trail fixture produces valid JSONL; all 4 verifiability property tests pass
- AST analyzer resolves cross-module imports and detects reachability for known-good and known-bad cases
- Wiring manifest schema committed and populated with executor.py entry points

**Exit Criteria:**
- `uv run pytest tests/audit-trail/ tests/v3.3/test_reachability_eval.py -v` exits 0
- `tests/v3.3/wiring_manifest.yaml` is valid YAML with non-empty `entry_points` and `required_reachable` sections
- Analyzer contract documented per NFR-6 with 3 limitation categories in module docstring
