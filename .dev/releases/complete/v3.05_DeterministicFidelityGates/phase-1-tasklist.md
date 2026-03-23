# Phase 1 -- Foundation: Parser, Data Model & Interface Verification

Establish the parsing infrastructure and data models that every downstream component depends on. Verify interface contracts for cross-phase dependencies. After this phase, the parser produces structured output from real specs, section splitting works, and all data model extensions are backward-compatible. Exit when FR-2 + FR-5 pass real-spec validation (Gate A).

### T01.01 -- Verify Interface Contracts for TurnLedger, Registry, and FR-7.1

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001, R-002, R-003, R-004, R-005, R-006 |
| Why | All downstream phases depend on TurnLedger API, DeviationRegistry surface, and convergence config. Verifying these interfaces first prevents cascading rework. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | cross-cutting (system-wide interface verification), dependency (blocked on API stability) |
| Tier | STRICT |
| Confidence | [████████░░] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0001 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0001/evidence.md`

**Deliverables:**
1. Interface verification report documenting TurnLedger API (`debit()`, `credit()`, `can_launch()`, `can_remediate()`, `reimbursement_rate`), DeviationRegistry surface (`convergence.py:50-225`), `convergence_enabled` default, `fidelity.py` import status, `handle_regression()` signature, and SC-1 through SC-6 acceptance-test mapping

**Steps:**
1. **[PLANNING]** Read `superclaude/cli/sprint/models.py` TurnLedger class (~lines 488-525) and confirm method signatures
2. **[PLANNING]** Read `convergence.py:50-225` and document DeviationRegistry public methods
3. **[EXECUTION]** Verify `convergence_enabled` defaults to `false` in `models.py:107` and is scoped to step 8
4. **[EXECUTION]** Run `uv run python -c "from superclaude.cli.roadmap.fidelity import *"` to confirm `fidelity.py` has zero imports
5. **[EXECUTION]** Lock `handle_regression() -> RegressionResult` callable signature in an interface document
6. **[EXECUTION]** Map each SC-1 through SC-6 to specific spec sections and validation commands
7. **[VERIFICATION]** Verify all 6 interface checks documented with source-code line references
8. **[COMPLETION]** Write interface verification report to `TASKLIST_ROOT/artifacts/D-0001/evidence.md`

**Acceptance Criteria:**
- `TASKLIST_ROOT/artifacts/D-0001/evidence.md` exists and documents all 6 interface verification results with line-number references
- TurnLedger API surface matches spec Section 1.3: `debit()`, `credit()`, `can_launch()`, `can_remediate()`, `reimbursement_rate`
- No unexpected API changes that would require spec amendment
- SC-1 through SC-6 each mapped to a concrete validation command or manual check

**Validation:**
- Manual check: each interface item verified against source code at specific line numbers
- Evidence: `TASKLIST_ROOT/artifacts/D-0001/evidence.md` produced with verification results

**Dependencies:** None
**Rollback:** TBD
**Notes:** Verification-only task; no code changes. Critical path entry point for the entire release.

---

### T01.02 -- Implement Spec & Roadmap Parser (FR-2)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007, R-008, R-009, R-010, R-011, R-012, R-013, R-014, R-015 |
| Why | FR-2 is the critical path entry. Every structural checker depends on parsed spec data. Parser robustness against real-world specs is not optional. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | dependency (FR-1, FR-4, FR-5, FR-7 all depend on FR-2), cross-cutting (parser feeds all checkers) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0002, D-0003 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0002/spec.md`
- `TASKLIST_ROOT/artifacts/D-0003/evidence.md`

**Deliverables:**
1. `src/superclaude/cli/roadmap/spec_parser.py` with YAML frontmatter extraction (graceful degradation via `ParseWarning`), markdown table extraction keyed by heading path, fenced code block extraction with language annotation, requirement ID regex extraction (`FR-\d+\.\d+`, `NFR-\d+\.\d+`, `SC-\d+`, `G-\d+`, `D\d+`)
2. Function signature extraction from fenced Python blocks, `Literal[...]` enum value extraction, numeric threshold expression extraction (`< 5s`, `>= 90%`, `minimum 20`), file path extraction from manifest tables (Sec 4.1, 4.2, 4.3)

**Steps:**
1. **[PLANNING]** Create `src/superclaude/cli/roadmap/spec_parser.py`; define module docstring and public API
2. **[PLANNING]** Identify all extraction targets from spec FR-2 acceptance criteria
3. **[EXECUTION]** Implement YAML frontmatter extraction with `ParseWarning` on malformed input
4. **[EXECUTION]** Implement markdown table extraction, code block extraction, requirement ID regex, function signature extraction, `Literal[...]` extraction, threshold extraction, and file path extraction
5. **[EXECUTION]** Implement graceful degradation: irregular tables, missing language tags, malformed YAML all produce `ParseWarning` with partial results
6. **[VERIFICATION]** Run `uv run pytest tests/roadmap/test_spec_parser.py -v` (tests created in T01.06)
7. **[COMPLETION]** Document parser API in `TASKLIST_ROOT/artifacts/D-0002/spec.md`

**Acceptance Criteria:**
- `src/superclaude/cli/roadmap/spec_parser.py` exists and exports all extraction functions listed in FR-2
- Parser returns structured objects (not raw text) for each extraction type
- Malformed YAML frontmatter returns partial parse + `ParseWarning` (not crash)
- `ParseWarning` list collected per parse call and surfaced to caller

**Validation:**
- `uv run pytest tests/roadmap/test_spec_parser.py -v` exits 0 with all tests passing
- Evidence: parser validated against `deterministic-fidelity-gate-requirements.md` (real spec, not synthetic)

**Dependencies:** None
**Rollback:** TBD
**Notes:** Risk #1 (spec parser robustness) is highest severity. Validate against real spec early.

---

### T01.03 -- Validate Parser Against Real Spec

| Field | Value |
|---|---|
| Roadmap Item IDs | R-016 |
| Why | Roadmap explicitly requires validation against the real spec, not just synthetic fixtures. This catches real-world format deviations. |
| Effort | S |
| Risk | Low |
| Risk Drivers | none matched |
| Tier | STANDARD |
| Confidence | [████████░░] 82% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0004/evidence.md`

**Deliverables:**
1. Parser validation report: real spec produces structured output with zero crashes and populated `ParseWarning` list

**Steps:**
1. **[PLANNING]** Identify the real spec path: `deterministic-fidelity-gate-requirements.md`
2. **[PLANNING]** List expected extraction outputs (IDs, signatures, tables, thresholds)
3. **[EXECUTION]** Run parser against real spec and capture all outputs
4. **[EXECUTION]** Verify each extraction type produces non-empty results
5. **[EXECUTION]** Verify `ParseWarning` list is populated for any irregular content
6. **[VERIFICATION]** Confirm zero crashes and all expected data extracted
7. **[COMPLETION]** Write validation evidence to `TASKLIST_ROOT/artifacts/D-0004/evidence.md`

**Acceptance Criteria:**
- Parser produces structured output from `deterministic-fidelity-gate-requirements.md` with zero crashes
- `ParseWarning` list correctly populated for any malformed inputs in the real spec
- All FR-2 extraction types return non-empty results on the real spec
- Evidence document lists each extraction type and its result count

**Validation:**
- `uv run pytest tests/roadmap/test_spec_parser.py::test_real_spec_validation -v` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0004/evidence.md` produced

**Dependencies:** T01.02
**Rollback:** TBD

---

### T01.04 -- Implement Sectional Splitting and Dimension Mapping (FR-5)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-017, R-018, R-019, R-020 |
| Why | Structural checkers require sectional input. Full-document inline comparison causes attention degradation (failure mode #3). |
| Effort | M |
| Risk | Low |
| Risk Drivers | none matched |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0005, D-0006 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0005/spec.md`
- `TASKLIST_ROOT/artifacts/D-0006/spec.md`

**Deliverables:**
1. `SpecSection` dataclass with `heading`, `heading_path`, `level`, `content`, `start_line`, `end_line`; `split_into_sections()` in `spec_parser.py` with frontmatter (level=0) and preamble handling
2. Dimension-to-section mapping table for checker routing (Signatures->FR sections, Data Models->Sec 4.x, Gates->FR-7/FR-8, CLI->Sec 5.1, NFRs->Sec 6)

**Steps:**
1. **[PLANNING]** Define `SpecSection` dataclass fields per FR-5 specification
2. **[PLANNING]** Plan heading-level splitting algorithm (split on `^#{1,6} `)
3. **[EXECUTION]** Implement `split_into_sections()` in `spec_parser.py`
4. **[EXECUTION]** Handle YAML frontmatter as special section (level=0, heading="frontmatter") and preamble content (level=0)
5. **[EXECUTION]** Define dimension-to-section mapping as a deterministic dict
6. **[VERIFICATION]** Verify round-trip: split -> reassemble matches original content
7. **[COMPLETION]** Document section splitter API and mapping in `TASKLIST_ROOT/artifacts/D-0005/spec.md`

**Acceptance Criteria:**
- `SpecSection` dataclass defined in `spec_parser.py` with all 6 specified fields
- `split_into_sections()` correctly splits real spec into sections with proper heading_path and level
- Round-trip test passes: split content reassembled matches original byte-for-byte
- Dimension-to-section mapping covers all 5 checker dimensions per roadmap table

**Validation:**
- `uv run pytest tests/roadmap/test_spec_parser.py::test_section_splitting -v` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0005/spec.md` documents section splitter behavior

**Dependencies:** T01.02
**Rollback:** TBD

---

### Checkpoint: Phase 1 / Tasks T01.01-T01.04

**Purpose:** Verify parser infrastructure and interface contracts are stable before data model extensions.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P01-T01-T04.md`
**Verification:**
- Parser produces structured output from real spec with zero crashes
- Interface verification report confirms all 6 API surfaces match expectations
- Section splitter round-trips correctly on real spec content
**Exit Criteria:**
- T01.01 through T01.04 all completed with passing validation
- No blocking issues identified in interface verification
- Parser handles all FR-2 extraction types

---

### T01.05 -- Define Data Model Extensions (FR-3, FR-6 partial)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-021, R-022, R-023 |
| Why | Finding dataclass, severity rules, and supporting types must be defined before checkers can produce typed findings. Backward compatibility with existing serialized data is required. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | schema (model extension), breaking (backward compat requirement) |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0007, D-0008, D-0009 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0007/spec.md`
- `TASKLIST_ROOT/artifacts/D-0008/spec.md`
- `TASKLIST_ROOT/artifacts/D-0009/spec.md`

**Deliverables:**
1. Extended `Finding` dataclass in `models.py` with `rule_id: str = ""`, `spec_quote: str = ""`, `roadmap_quote: str = ""` (all defaulted)
2. `SEVERITY_RULES: dict[tuple[str, str], str]` with all 19 canonical rules and `get_severity()` raising `KeyError` on unknown combos
3. `ParseWarning`, `RunMetadata`, `RegressionResult`, `RemediationPatch` dataclass definitions

**Steps:**
1. **[PLANNING]** Review existing `Finding` dataclass in `models.py` for current fields
2. **[PLANNING]** Enumerate all 19 canonical severity rules from spec FR-3 table
3. **[EXECUTION]** Extend `Finding` with `rule_id`, `spec_quote`, `roadmap_quote` (all with defaults)
4. **[EXECUTION]** Implement `SEVERITY_RULES` dict and `get_severity()` in `structural_checkers.py`
5. **[EXECUTION]** Define `ParseWarning`, `RunMetadata`, `RegressionResult`, `RemediationPatch` dataclasses
6. **[VERIFICATION]** Verify existing serialized Finding data still loads (backward compat test)
7. **[COMPLETION]** Document all new types in `TASKLIST_ROOT/artifacts/D-0007/spec.md`

**Acceptance Criteria:**
- `Finding` dataclass in `models.py` includes `rule_id`, `spec_quote`, `roadmap_quote` with string defaults
- `SEVERITY_RULES` dict contains all 19 `(dimension, mismatch_type) -> severity` mappings from spec FR-3
- `get_severity("signatures", "unknown_key")` raises `KeyError`
- Existing serialized `Finding` objects load without error (backward compatibility verified)

**Validation:**
- `uv run pytest tests/roadmap/test_models.py -v` exits 0 with all existing + new tests passing
- Evidence: `TASKLIST_ROOT/artifacts/D-0007/spec.md` documents extended Finding fields

**Dependencies:** None (models defined independently)
**Rollback:** TBD
**Notes:** Critical Path Override: Yes -- models affect data integrity across all phases.

---

### T01.06 -- Create Unit Tests for Parser and Section Splitter

| Field | Value |
|---|---|
| Roadmap Item IDs | R-016 |
| Why | Parser is critical path (Risk #1). Tests must validate against real spec content, not only synthetic fixtures. |
| Effort | M |
| Risk | Low |
| Risk Drivers | none matched |
| Tier | STANDARD |
| Confidence | [████████░░] 82% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0010 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0010/evidence.md`

**Deliverables:**
1. `tests/roadmap/test_spec_parser.py` covering all FR-2 extraction types validated against real spec content; includes section splitting round-trip test

**Steps:**
1. **[PLANNING]** List all FR-2 extraction functions to test
2. **[PLANNING]** Identify test fixtures from real spec content
3. **[EXECUTION]** Write tests for YAML frontmatter, table, code block, ID, signature, Literal, threshold, and file path extraction
4. **[EXECUTION]** Write section splitting tests: heading levels, frontmatter section, preamble, round-trip
5. **[EXECUTION]** Write real-spec validation test using `deterministic-fidelity-gate-requirements.md`
6. **[VERIFICATION]** `uv run pytest tests/roadmap/test_spec_parser.py -v` exits 0
7. **[COMPLETION]** Document test coverage in `TASKLIST_ROOT/artifacts/D-0010/evidence.md`

**Acceptance Criteria:**
- `tests/roadmap/test_spec_parser.py` exists and covers all FR-2 extraction types
- At least one test uses real spec content (`deterministic-fidelity-gate-requirements.md`)
- Section splitting round-trip test passes
- `ParseWarning` entries produced and correctly populated for malformed YAML, irregular tables, and missing language tags
- `uv run pytest tests/roadmap/test_spec_parser.py -v` exits 0 with all tests passing

**Validation:**
- `uv run pytest tests/roadmap/test_spec_parser.py -v` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0010/evidence.md` lists test names and results

**Dependencies:** T01.02, T01.04
**Rollback:** TBD

---

### T01.07 -- Gate A: Implementation Readiness Verification

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | Roadmap defines Gate A: "Parser Certified." SC-007 backward compat and all exit criteria must be verified before Phase 2. |
| Effort | S |
| Risk | Low |
| Risk Drivers | none matched |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0011 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0011/evidence.md`

**Deliverables:**
1. Gate A verification: all Phase 1 exit criteria confirmed (parser validated, data models backward-compatible, interfaces verified)

**Steps:**
1. **[PLANNING]** Compile Phase 1 exit criteria from roadmap
2. **[EXECUTION]** Run `uv run pytest tests/roadmap/ -v` to confirm all Phase 1 tests pass
3. **[EXECUTION]** Run `uv run pytest` (full suite) to confirm SC-007 backward compat
4. **[EXECUTION]** Verify SpecSection round-trip and ParseWarning population
5. **[VERIFICATION]** Confirm all exit criteria met
6. **[COMPLETION]** Write Gate A verification report to `TASKLIST_ROOT/artifacts/D-0011/evidence.md`

**Acceptance Criteria:**
- `uv run pytest tests/roadmap/ -v` exits 0 with all new tests passing
- `uv run pytest` (full suite) exits 0 confirming no existing test breakage (SC-007)
- Data model extensions are backward-compatible (existing serialized data loads)
- Gate A verification report documents all checks with pass/fail status

**Validation:**
- `uv run pytest` exits 0 (full suite, no breakage)
- Evidence: `TASKLIST_ROOT/artifacts/D-0011/evidence.md` produced

**Dependencies:** T01.01, T01.02, T01.03, T01.04, T01.05, T01.06
**Rollback:** TBD

---

### Checkpoint: End of Phase 1

**Purpose:** Gate A -- Parser Certified. Confirm FR-2 + FR-5 pass real-spec validation before structural checker development begins.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P01-END.md`
**Verification:**
- Parser produces structured output from real spec with zero crashes
- All data model extensions are backward-compatible with existing serialized data
- Full test suite passes with zero regressions (SC-007)
**Exit Criteria:**
- Interface verification complete; no surprises in TurnLedger or registry APIs
- `SpecSection` round-trips correctly
- All Phase 1 tasks completed with passing validation
