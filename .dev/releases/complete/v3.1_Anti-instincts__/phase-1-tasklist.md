# Phase 1 -- Core Detection Modules & Architecture Decisions

Resolve blocking open questions on day 1, then implement all four detection modules as standalone pure-function libraries with comprehensive tests. No pipeline integration yet. All four modules are internally parallelizable. Milestone M1: all modules pass unit tests against the cli-portify regression case with combined latency < 1s.

---

### T01.01 -- Resolve Day-1 Architecture Decisions

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001 |
| Why | OQ-003, OQ-004, OQ-005, and OQ-010 directly affect pass/fail correctness of all detection modules; resolving them before coding prevents rework. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0001, D-0002 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0001/spec.md`
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0002/notes.md`

**Deliverables:**
1. Architecture Decision Record documenting resolutions for OQ-003 (`# obligation-exempt` per-line scope), OQ-004 (separate `medium_severity_obligations` frontmatter field excluded from gate blocking), OQ-005 (defense-in-depth: both D-03/D-04 gates evaluate independently), OQ-009 (global pattern matching in Phase 1; contract-specific matching deferred), OQ-010 (heading presence check added to structural audit)
2. Merge coordination plan confirming no conflict with parallel `WIRING_GATE` work in `gates.py`

**Steps:**
1. **[PLANNING]** Read roadmap sections 1.0, OQ-003, OQ-004, OQ-005, OQ-009, OQ-010 and identify each decision's downstream impact on module APIs
2. **[PLANNING]** Check current state of `src/superclaude/cli/roadmap/gates.py` for WIRING_GATE definitions that may conflict
3. **[EXECUTION]** Document OQ-003 resolution: `# obligation-exempt` applies per-line on the scaffold term's line
4. **[EXECUTION]** Document OQ-004 resolution: MEDIUM severity obligations stored in separate frontmatter field, excluded from STRICT gate blocking
5. **[EXECUTION]** Document OQ-005 resolution: defense-in-depth, both gates evaluate independently per NFR-010
6. **[EXECUTION]** Document OQ-009 resolution: Phase 1 uses global pattern matching; contract-specific matching deferred to future iteration
7. **[EXECUTION]** Document OQ-010 resolution: `## Integration Wiring Tasks` heading presence check added as structural audit indicator
8. **[COMPLETION]** Write Architecture Decision Record to `D-0001/spec.md` and merge coordination plan to `D-0002/notes.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0001/spec.md` exists with resolutions for all five OQs (OQ-003, OQ-004, OQ-005, OQ-009, OQ-010)
- Each OQ resolution specifies the exact API impact on the corresponding detection module
- Merge coordination plan identifies additive-only insertion strategy for `gates.py`
- All decisions are traceable to roadmap section 1.0 recommended resolutions

**Validation:**
- Manual check: each OQ resolution matches the roadmap's recommended resolution column
- Evidence: Architecture Decision Record artifact produced at D-0001/spec.md

**Dependencies:** None
**Rollback:** TBD
**Notes:** This task must complete before T01.02-T01.05 begin; it resolves semantic ambiguities that affect module behavior.

---

### T01.02 -- Implement Obligation Scanner `obligation_scanner.py`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-002 |
| Why | The obligation scanner detects "scaffold-without-discharge" patterns using deterministic regex, forming the primary detection module for undischarged obligations. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | system-wide regex engine, breaking-change detection patterns |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0003/spec.md`

**Deliverables:**
1. `src/superclaude/cli/roadmap/obligation_scanner.py` — pure-Python module implementing FR-MOD1.1 through FR-MOD1.8: compiled regex vocabulary for 11 scaffold terms, phase-section parser with H2/H3 fallback, cross-phase discharge search with verb-anchored patterns, 60-char component context extraction (backtick-priority, capitalized-fallback), dual-condition discharge matching, `ObligationReport` and `Obligation` dataclasses, `# obligation-exempt` comment parsing, code-block severity demotion to MEDIUM

**Steps:**
1. **[PLANNING]** Load T01.01 decision record for OQ-003 (exempt syntax) and OQ-004 (MEDIUM severity) resolutions
2. **[PLANNING]** Review FR-MOD1.1-1.8 requirements; confirm no external dependencies beyond Python `re` and `dataclasses`
3. **[EXECUTION]** Define `Obligation` and `ObligationReport` dataclasses with fields: term, component, phase, severity, discharged, exempt (FR-MOD1.6)
4. **[EXECUTION]** Implement compiled regex vocabulary for 11 scaffold terms (FR-MOD1.1) and phase-section parser splitting on H2/H3 headings with fallback (FR-MOD1.2)
5. **[EXECUTION]** Implement cross-phase discharge search with verb-anchored patterns (FR-MOD1.3), 60-char component context extraction (FR-MOD1.4), dual-condition discharge matching (FR-MOD1.5)
6. **[EXECUTION]** Implement `# obligation-exempt` comment parsing (FR-MOD1.7) and code-block severity demotion to MEDIUM (FR-MOD1.8)
7. **[VERIFICATION]** Run `uv run pytest tests/roadmap/test_obligation_scanner.py -v` to validate all FR-MOD1 requirements
8. **[COMPLETION]** Record implementation evidence to D-0003/spec.md

**Acceptance Criteria:**
- `src/superclaude/cli/roadmap/obligation_scanner.py` exists with all 8 FR-MOD1 sub-requirements implemented as pure functions
- Module uses only `re` and `dataclasses` from stdlib; no LLM calls per NFR-001
- `ObligationReport` dataclass exposes `undischarged_count` property returning count of obligations where `discharged=False` and `severity != MEDIUM`
- All functions are stateless: no module-level mutable state, no file I/O within scanner functions

**Validation:**
- `uv run pytest tests/roadmap/test_obligation_scanner.py -v` exits 0
- Evidence: test output log and module source archived to D-0003/spec.md

**Dependencies:** T01.01
**Rollback:** Delete `src/superclaude/cli/roadmap/obligation_scanner.py`
**Notes:** Parallelizable with T01.03, T01.04, T01.05 after T01.01 completes.

---

### T01.03 -- Implement Integration Contract Extractor `integration_contracts.py`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | The contract extractor detects dispatch patterns and verifies wiring task coverage, catching missing integration points like `PROGRAMMATIC_RUNNERS`. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | system-wide regex engine, breaking-change detection patterns |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0004/spec.md`

**Deliverables:**
1. `src/superclaude/cli/roadmap/integration_contracts.py` — pure-Python module implementing FR-MOD2.1 through FR-MOD2.6: 7-category dispatch pattern scanner with compiled regexes, context capture (3 lines) with mechanism classification and sequential ID assignment and deduplication, verb-anchored wiring task coverage check, named mechanism identifier matching (UPPER_SNAKE_CASE, PascalCase), wiring-task-specific coverage semantics, `IntegrationAuditResult` dataclass with `all_covered` property

**Steps:**
1. **[PLANNING]** Review FR-MOD2.1-2.6 requirements; note OQ-009 deferral (contract-specific matching deferred to later)
2. **[PLANNING]** Identify the 7 dispatch pattern categories from spec
3. **[EXECUTION]** Implement compiled regexes for 7-category dispatch pattern scanner (FR-MOD2.1)
4. **[EXECUTION]** Implement context capture (3 lines), mechanism classification, sequential ID assignment, deduplication (FR-MOD2.2)
5. **[EXECUTION]** Implement verb-anchored wiring task coverage check (FR-MOD2.3) and named mechanism identifier matching for UPPER_SNAKE_CASE and PascalCase (FR-MOD2.4)
6. **[EXECUTION]** Implement wiring-task-specific coverage semantics (FR-MOD2.5) and define `IntegrationAuditResult` dataclass with `all_covered` property (FR-MOD2.6)
7. **[VERIFICATION]** Run `uv run pytest tests/roadmap/test_integration_contracts.py -v` to validate all FR-MOD2 requirements
8. **[COMPLETION]** Record implementation evidence to D-0004/spec.md

**Acceptance Criteria:**
- `src/superclaude/cli/roadmap/integration_contracts.py` exists with all 6 FR-MOD2 sub-requirements implemented as pure functions
- Module uses only `re` and `dataclasses` from stdlib; no LLM calls per NFR-001
- `IntegrationAuditResult.all_covered` returns `True` only when `uncovered_contracts == 0`
- Global pattern matching used per spec; contract-specific matching explicitly not implemented (OQ-009 deferred)

**Validation:**
- `uv run pytest tests/roadmap/test_integration_contracts.py -v` exits 0
- Evidence: test output log and module source archived to D-0004/spec.md

**Dependencies:** T01.01
**Rollback:** Delete `src/superclaude/cli/roadmap/integration_contracts.py`
**Notes:** Parallelizable with T01.02, T01.04, T01.05 after T01.01 completes.

---

### T01.04 -- Implement Fingerprint Extraction `fingerprint.py`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Why | Fingerprint extraction catches missing code identifiers in roadmap output by comparing spec-derived identifiers against roadmap content, providing the third detection dimension. |
| Effort | M |
| Risk | Low |
| Risk Drivers | performance (coverage ratio computation) |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0005 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0005/spec.md`

**Deliverables:**
1. `src/superclaude/cli/roadmap/fingerprint.py` — pure-Python module implementing FR-MOD3.1 through FR-MOD3.4: three-source extraction (backtick identifiers >= 4 chars, code-block `def`/`class`, ALL_CAPS constants), `_EXCLUDED_CONSTANTS` frozenset filtering aligned with 4-char regex minimum, deduplication by text value, case-insensitive roadmap coverage check returning 4-tuple, threshold gate logic (default 0.7) with empty-fingerprint passthrough

**Steps:**
1. **[PLANNING]** Review FR-MOD3.1-3.4 requirements; note OQ-001 deferral (extensibility deferred to Phase 2) and OQ-011 (`_EXCLUDED_CONSTANTS`)
2. **[PLANNING]** Confirm threshold default (0.7) and empty-fingerprint passthrough behavior
3. **[EXECUTION]** Implement three-source extraction: backtick identifiers (>= 4 chars), code-block `def`/`class` names, ALL_CAPS constants (FR-MOD3.1)
4. **[EXECUTION]** Implement `_EXCLUDED_CONSTANTS` frozenset and deduplication by text value (FR-MOD3.1, FR-MOD3.2)
5. **[EXECUTION]** Implement case-insensitive roadmap coverage check returning 4-tuple (total, found, missing, ratio) (FR-MOD3.3)
6. **[EXECUTION]** Implement threshold gate logic with default 0.7 and empty-fingerprint passthrough (FR-MOD3.4)
7. **[VERIFICATION]** Run `uv run pytest tests/roadmap/test_fingerprint.py -v` to validate all FR-MOD3 requirements
8. **[COMPLETION]** Record implementation evidence to D-0005/spec.md

**Acceptance Criteria:**
- `src/superclaude/cli/roadmap/fingerprint.py` exists with all 4 FR-MOD3 sub-requirements implemented as pure functions
- Coverage check returns exact 4-tuple `(total, found, missing_list, ratio)` with case-insensitive matching
- Threshold gate returns pass when `ratio >= 0.7` or when fingerprint set is empty (passthrough)
- `_EXCLUDED_CONSTANTS` frozenset filters common non-semantic ALL_CAPS terms aligned with 4-char minimum

**Validation:**
- `uv run pytest tests/roadmap/test_fingerprint.py -v` exits 0
- Evidence: test output log and module source archived to D-0005/spec.md

**Dependencies:** T01.01
**Rollback:** Delete `src/superclaude/cli/roadmap/fingerprint.py`
**Notes:** Parallelizable with T01.02, T01.03, T01.05 after T01.01 completes.

---

### T01.05 -- Implement Spec Structural Audit `spec_structural_audit.py`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Why | The structural auditor provides early warning of under-specified specs by counting structural indicators and comparing ratios, operating in warning-only mode. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0006 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0006/spec.md`

**Deliverables:**
1. `src/superclaude/cli/roadmap/spec_structural_audit.py` — pure-Python module implementing FR-MOD4.1 through FR-MOD4.3: 7 structural indicator counters, ratio comparison against `total_requirements` frontmatter, warning-only enforcement with no pipeline blocking

**Steps:**
1. **[PLANNING]** Review FR-MOD4.1-4.3 requirements; note OQ-006 deferral (STRICT transition manual after shadow metrics) and NFR-011
2. **[PLANNING]** Identify the 7 structural indicators from spec
3. **[EXECUTION]** Implement 7 structural indicator counters (FR-MOD4.1)
4. **[EXECUTION]** Implement ratio comparison against `total_requirements` frontmatter with default threshold 0.5 (FR-MOD4.2)
5. **[EXECUTION]** Ensure warning-only enforcement: function returns result but never raises exceptions or blocks pipeline (FR-MOD4.3)
6. **[VERIFICATION]** Run `uv run pytest tests/roadmap/test_spec_structural_audit.py -v`
7. **[COMPLETION]** Record implementation evidence to D-0006/spec.md

**Acceptance Criteria:**
- `src/superclaude/cli/roadmap/spec_structural_audit.py` exists with all 3 FR-MOD4 sub-requirements implemented
- Module counts exactly 7 structural indicators as defined in the spec
- Warning-only mode: function returns audit result object but never raises or blocks
- Ratio comparison uses `total_requirements` frontmatter value as denominator

**Validation:**
- `uv run pytest tests/roadmap/test_spec_structural_audit.py -v` exits 0
- Evidence: test output log archived to D-0006/spec.md

**Dependencies:** T01.01
**Rollback:** Delete `src/superclaude/cli/roadmap/spec_structural_audit.py`

---

### Checkpoint: Phase 1 / Tasks T01.01-T01.05

**Purpose:** Verify all four detection modules are implemented and functionally correct before writing unit tests.
**Checkpoint Report Path:** `.dev/releases/current/v3.1_Anti-instincts__/checkpoints/CP-P01-T01-T05.md`
**Verification:**
- All four module files exist in `src/superclaude/cli/roadmap/`
- Each module uses only stdlib dependencies (re, dataclasses); no LLM calls
- Each module's public functions are stateless (no module-level mutable state)
**Exit Criteria:**
- T01.01 decision record documents all five OQ resolutions (OQ-003, OQ-004, OQ-005, OQ-009, OQ-010)
- T01.02-T01.05 modules compile without errors
- No import-time side effects in any module

---

### T01.06 -- Write `test_obligation_scanner.py` Unit Tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | Unit tests validate the obligation scanner against scaffold detection, discharge matching, exempt comments, code-block severity demotion, and the cli-portify regression case (SC-002). |
| Effort | S |
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
| Deliverable IDs | D-0007 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0007/evidence.md`

**Deliverables:**
1. `tests/roadmap/test_obligation_scanner.py` — unit tests covering: scaffold term detection for all 11 terms, cross-phase discharge matching, `# obligation-exempt` comment parsing, code-block severity demotion to MEDIUM, cli-portify regression case (SC-002: detects "mocked steps" without discharge). All tests use real content fixtures, no mocks.

**Steps:**
1. **[PLANNING]** Read `obligation_scanner.py` public API to identify testable functions
2. **[PLANNING]** Prepare real content fixtures from cli-portify regression case
3. **[EXECUTION]** Write tests for scaffold term detection across all 11 vocabulary terms
4. **[EXECUTION]** Write tests for discharge matching, exempt comment parsing, severity demotion
5. **[EXECUTION]** Write cli-portify regression test (SC-002): verify scanner detects "mocked steps" without discharge at >= 85% confidence
6. **[VERIFICATION]** Run `uv run pytest tests/roadmap/test_obligation_scanner.py -v`
7. **[COMPLETION]** Record test results to D-0007/evidence.md

**Acceptance Criteria:**
- `tests/roadmap/test_obligation_scanner.py` exists with tests covering all 5 functional areas listed above
- All tests use real content fixtures; zero mock objects
- SC-002 regression test explicitly asserts detection of "mocked steps" without discharge
- `uv run pytest tests/roadmap/test_obligation_scanner.py -v` exits 0 with all tests passing

**Validation:**
- `uv run pytest tests/roadmap/test_obligation_scanner.py -v` exits 0
- Evidence: test output log archived to D-0007/evidence.md

**Dependencies:** T01.02
**Rollback:** Delete `tests/roadmap/test_obligation_scanner.py`

---

### T01.07 -- Write `test_integration_contracts.py` Unit Tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | Unit tests validate the integration contract extractor against 7-category detection, wiring coverage, deduplication, and the cli-portify regression case (SC-003). |
| Effort | S |
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
| Deliverable IDs | D-0008 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0008/evidence.md`

**Deliverables:**
1. `tests/roadmap/test_integration_contracts.py` — unit tests covering: 7-category dispatch pattern detection, wiring task coverage check, mechanism deduplication, cli-portify regression case (SC-003: detects `PROGRAMMATIC_RUNNERS` without wiring task at >= 90% confidence). All tests use real content fixtures, no mocks.

**Steps:**
1. **[PLANNING]** Read `integration_contracts.py` public API to identify testable functions
2. **[PLANNING]** Prepare real content fixtures including cli-portify case with `PROGRAMMATIC_RUNNERS`
3. **[EXECUTION]** Write tests for each of the 7 dispatch pattern categories
4. **[EXECUTION]** Write tests for wiring coverage, deduplication, and named mechanism matching
5. **[EXECUTION]** Write cli-portify regression test (SC-003): verify extractor detects `PROGRAMMATIC_RUNNERS` without wiring task
6. **[VERIFICATION]** Run `uv run pytest tests/roadmap/test_integration_contracts.py -v`
7. **[COMPLETION]** Record test results to D-0008/evidence.md

**Acceptance Criteria:**
- `tests/roadmap/test_integration_contracts.py` exists with tests covering all 4 functional areas listed above
- All tests use real content fixtures; zero mock objects
- SC-003 regression test explicitly asserts detection of `PROGRAMMATIC_RUNNERS` without wiring task
- `uv run pytest tests/roadmap/test_integration_contracts.py -v` exits 0 with all tests passing

**Validation:**
- `uv run pytest tests/roadmap/test_integration_contracts.py -v` exits 0
- Evidence: test output log archived to D-0008/evidence.md

**Dependencies:** T01.03
**Rollback:** Delete `tests/roadmap/test_integration_contracts.py`

---

### T01.08 -- Write `test_fingerprint.py` Unit Tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | Unit tests validate fingerprint extraction against three-source extraction, deduplication, coverage ratio, threshold boundary, and the cli-portify regression case (SC-004). |
| Effort | S |
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
| Deliverable IDs | D-0009 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0009/evidence.md`

**Deliverables:**
1. `tests/roadmap/test_fingerprint.py` — unit tests covering: three-source extraction (backtick, def/class, ALL_CAPS), deduplication by text value, coverage ratio computation, threshold boundary (0.7 pass/fail edge), empty-fingerprint passthrough, cli-portify regression case (SC-004: detects missing `_run_programmatic_step`, `PROGRAMMATIC_RUNNERS`, `test_programmatic_step_routing` at >= 95% confidence). All tests use real content fixtures, no mocks.

**Steps:**
1. **[PLANNING]** Read `fingerprint.py` public API to identify testable functions
2. **[PLANNING]** Prepare real content fixtures including cli-portify case with known missing identifiers
3. **[EXECUTION]** Write tests for three-source extraction, deduplication, and `_EXCLUDED_CONSTANTS` filtering
4. **[EXECUTION]** Write tests for coverage ratio computation and threshold boundary at 0.7
5. **[EXECUTION]** Write cli-portify regression test (SC-004): verify fingerprint checker detects missing `_run_programmatic_step`, `PROGRAMMATIC_RUNNERS`, `test_programmatic_step_routing`
6. **[VERIFICATION]** Run `uv run pytest tests/roadmap/test_fingerprint.py -v`
7. **[COMPLETION]** Record test results to D-0009/evidence.md

**Acceptance Criteria:**
- `tests/roadmap/test_fingerprint.py` exists with tests covering all 6 functional areas listed above
- All tests use real content fixtures; zero mock objects
- SC-004 regression test explicitly asserts detection of all three missing identifiers
- `uv run pytest tests/roadmap/test_fingerprint.py -v` exits 0 with all tests passing

**Validation:**
- `uv run pytest tests/roadmap/test_fingerprint.py -v` exits 0
- Evidence: test output log archived to D-0009/evidence.md

**Dependencies:** T01.04
**Rollback:** Delete `tests/roadmap/test_fingerprint.py`

---

### T01.09 -- Write `test_spec_structural_audit.py` Unit Tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | Unit tests validate the structural auditor against all 7 indicators, ratio comparison, and warning-only behavior (SC-005). |
| Effort | S |
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
| Deliverable IDs | D-0010 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v3.1_Anti-instincts__/artifacts/D-0010/evidence.md`

**Deliverables:**
1. `tests/roadmap/test_spec_structural_audit.py` — unit tests covering: all 7 structural indicator counters, ratio comparison against `total_requirements` frontmatter, warning-only behavior (function returns result without raising/blocking), SC-005 regression (flags extraction inadequacy when ratio < 0.5). All tests use real content fixtures, no mocks.

**Steps:**
1. **[PLANNING]** Read `spec_structural_audit.py` public API to identify testable functions
2. **[PLANNING]** Prepare real content fixtures with known indicator counts and ratios
3. **[EXECUTION]** Write tests for each of the 7 structural indicator counters
4. **[EXECUTION]** Write tests for ratio comparison (pass at >= 0.5, flag at < 0.5) and warning-only behavior
5. **[EXECUTION]** Write SC-005 regression test: verify auditor flags extraction inadequacy when ratio < 0.5
6. **[VERIFICATION]** Run `uv run pytest tests/roadmap/test_spec_structural_audit.py -v`
7. **[COMPLETION]** Record test results to D-0010/evidence.md

**Acceptance Criteria:**
- `tests/roadmap/test_spec_structural_audit.py` exists with tests covering all 4 functional areas listed above
- All tests use real content fixtures; zero mock objects
- Warning-only behavior test confirms function returns result object without blocking the pipeline (FR-MOD4.3)
- `uv run pytest tests/roadmap/test_spec_structural_audit.py -v` exits 0 with all tests passing

**Validation:**
- `uv run pytest tests/roadmap/test_spec_structural_audit.py -v` exits 0
- Evidence: test output log archived to D-0010/evidence.md

**Dependencies:** T01.05
**Rollback:** Delete `tests/roadmap/test_spec_structural_audit.py`

---

### Checkpoint: End of Phase 1

**Purpose:** Validate implementation readiness (Checkpoint A): all modules and tests pass, latency < 1s, no existing test breakage, no signature or statelessness violations.
**Checkpoint Report Path:** `.dev/releases/current/v3.1_Anti-instincts__/checkpoints/CP-P01-END.md`
**Verification:**
- `uv run pytest tests/roadmap/ -v` exits 0 with all new tests passing (SC-001 through SC-005)
- Combined execution of all four modules on cli-portify regression case completes in < 1s (SC-006)
- `uv run pytest` (full existing test suite) exits 0 with zero regressions (SC-007)
**Exit Criteria:**
- All 9 tasks (T01.01-T01.09) completed with deliverables D-0001 through D-0010 produced
- No module contains LLM calls, module-level mutable state, or file I/O in scanner functions
- All four OQ resolutions documented and reflected in module implementations
