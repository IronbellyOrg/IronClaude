# Phase 2 -- Foundation Data Model and Gates

Establish the type system, gate definitions, and semantic check functions in `models.py` and `gates.py` that all subsequent phases depend on. This phase modifies the `Finding` dataclass, renames `parse_frontmatter()`, implements 9+ semantic check functions, and defines/modifies 4 gate definitions.

### T02.01 -- Add deviation_class Field to Finding Dataclass in models.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-017, R-018, R-019, R-020 |
| Why | Finding must carry deviation classification for downstream routing; default ensures backward compatibility |
| Effort | M |
| Risk | Medium |
| Risk Drivers | schema, model, breaking |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0010 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0010/spec.md`

**Deliverables:**
1. Modified `Finding` dataclass in `models.py` with `deviation_class` field, `VALID_DEVIATION_CLASSES` frozenset, and `__post_init__` validation

**Steps:**
1. **[PLANNING]** Read current `Finding` dataclass definition in `src/superclaude/cli/sprint/models.py`
2. **[PLANNING]** Identify all existing `Finding` constructors across codebase to verify backward compatibility
3. **[EXECUTION]** Add `deviation_class: str = "UNCLASSIFIED"` field to `Finding` dataclass
4. **[EXECUTION]** Add `VALID_DEVIATION_CLASSES` frozenset: `{"SLIP", "INTENTIONAL", "AMBIGUOUS", "PRE_APPROVED", "UNCLASSIFIED"}`
5. **[EXECUTION]** Add `__post_init__` validation that raises `ValueError` if `deviation_class` not in `VALID_DEVIATION_CLASSES`
6. **[VERIFICATION]** Run `uv run pytest tests/sprint/test_models.py -v` to verify backward compatibility and new validation
7. **[VERIFICATION]** Run `uv run pytest tests/sprint/ -v` to confirm all existing `Finding` constructors across the codebase still work with default `deviation_class`
8. **[COMPLETION]** Document changes in `D-0010/spec.md`

**Acceptance Criteria:**
- `Finding("test", deviation_class="SLIP")` constructs successfully
- `Finding("test", deviation_class="INVALID")` raises `ValueError`
- `Finding("test")` defaults to `"UNCLASSIFIED"` — all existing constructors remain compatible
- `VALID_DEVIATION_CLASSES` contains exactly 5 values: SLIP, INTENTIONAL, AMBIGUOUS, PRE_APPROVED, UNCLASSIFIED

**Validation:**
- `uv run pytest tests/sprint/test_models.py -v` exits 0 with all tests passing
- Evidence: linkable artifact produced at `D-0010/spec.md`

**Dependencies:** T01.08 (Phase 1 exit)
**Rollback:** Revert `models.py` changes; single-file modification

---

### T02.02 -- Rename _parse_frontmatter() to parse_frontmatter() in gates.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-021 |
| Why | Downstream phases import parse_frontmatter() as public API; rename must happen first as all phases build on it |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0011 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0011/evidence.md`

**Deliverables:**
1. Renamed function `parse_frontmatter()` in `gates.py` with all callers updated across codebase

**Steps:**
1. **[PLANNING]** Grep all callers of `_parse_frontmatter` across the codebase
2. **[PLANNING]** Identify all import statements referencing `_parse_frontmatter`
3. **[EXECUTION]** Rename `_parse_frontmatter()` to `parse_frontmatter()` in `gates.py`
4. **[EXECUTION]** Update all callers and imports to use `parse_frontmatter()`
5. **[EXECUTION]** Commit as single atomic commit per NFR-021
6. **[VERIFICATION]** Grep confirms no remaining `_parse_frontmatter` references; `uv run pytest tests/sprint/ -v` exits 0
7. **[COMPLETION]** Document rename scope in `D-0011/evidence.md`

**Acceptance Criteria:**
- `parse_frontmatter()` is public in `gates.py`; all callers updated
- Grep for `_parse_frontmatter` across codebase returns zero results
- Full test suite passes after rename
- Single atomic commit contains all rename changes

**Validation:**
- `uv run pytest tests/sprint/ -v` exits 0 with all tests passing
- Evidence: linkable artifact produced at `D-0011/evidence.md`

**Dependencies:** T01.08 (Phase 1 exit)
**Rollback:** Revert the single atomic rename commit

---

### T02.03 -- Implement _parse_routing_list() With Regex Validation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-022, R-023 |
| Why | Routing list parsing is critical infrastructure for deviation-analysis gate checks; invalid tokens must be excluded with logging |
| Effort | M |
| Risk | Medium |
| Risk Drivers | Cross-cutting scope (parsing used by multiple gates) |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0012 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0012/spec.md`

**Deliverables:**
1. `_parse_routing_list()` function at module placement decided in T01.06, with regex validation (`^DEV-\d+$`), WARNING logging for non-conforming tokens, and cross-check against `total_analyzed`

**Steps:**
1. **[PLANNING]** Confirm module placement from T01.06 decision (remediate.py or parsing.py)
2. **[PLANNING]** Review integer-parsing requirements: distinct log messages for missing/malformed/failing values (FR-080)
3. **[EXECUTION]** Implement `_parse_routing_list()`: split on `,`, strip whitespace, validate against `re.compile(r'^DEV-\d+$')`
4. **[EXECUTION]** Add WARNING log and exclusion for non-conforming tokens
5. **[EXECUTION]** Add cross-check: `len(returned_tokens)` against `total_analyzed`
6. **[EXECUTION]** Add distinct log messages for missing vs malformed vs failing integer values
7. **[VERIFICATION]** Run unit tests for empty string, whitespace, invalid IDs, valid IDs, mixed input
8. **[COMPLETION]** Document implementation in `D-0012/spec.md`

**Acceptance Criteria:**
- `_parse_routing_list("DEV-001, DEV-002")` returns `["DEV-001", "DEV-002"]`
- `_parse_routing_list("")` returns empty list
- `_parse_routing_list("DEV-001, INVALID, DEV-002")` returns `["DEV-001", "DEV-002"]` with WARNING log
- Integer-parsing produces distinct log messages for missing, malformed, and failing values

**Validation:**
- `uv run pytest tests/sprint/test_remediate.py -v -k "parse_routing"` exits 0
- Evidence: linkable artifact produced at `D-0012/spec.md`

**Dependencies:** T01.06 (module placement decision)
**Rollback:** Revert function addition; no downstream consumers yet

---

### T02.04 -- Implement 9 Semantic Check Functions in gates.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-024, R-025, R-026, R-027, R-028, R-029, R-030, R-031, R-032 |
| Why | Gate infrastructure requires 9+ semantic check functions; all must be fail-closed per NFR-016 |
| Effort | L |
| Risk | Medium |
| Risk Drivers | Multi-file, system-wide (gate infrastructure), security (fail-closed) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0013 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0013/spec.md`

**Deliverables:**
1. Nine semantic check functions in `gates.py`: `_certified_is_true`, `_validation_complete_true`, `_no_ambiguous_deviations`, `_routing_consistent_with_slip_count`, `_pre_approved_not_in_fix_roadmap`, `_slip_count_matches_routing`, `_total_annotated_consistent`, `_total_analyzed_consistent`, `_routing_ids_valid` — all fail-closed

**Steps:**
1. **[PLANNING]** Review each semantic check's specification from roadmap (FR-026 through FR-086)
2. **[PLANNING]** Identify existing SemanticCheck pattern in `gates.py` to match
3. **[EXECUTION]** Implement `_certified_is_true()` (FR-028): returns True only when `certified: true` present
4. **[EXECUTION]** Implement `_validation_complete_true()` (FR-053), `_no_ambiguous_deviations()` (FR-026), `_routing_consistent_with_slip_count()` (FR-056)
5. **[EXECUTION]** Implement `_pre_approved_not_in_fix_roadmap()` (FR-079), `_slip_count_matches_routing()` (FR-081), `_total_annotated_consistent()` (FR-085)
6. **[EXECUTION]** Implement `_total_analyzed_consistent()` (FR-086), `_routing_ids_valid()` (FR-074)
7. **[VERIFICATION]** Run unit tests for all 9 functions with boundary inputs: valid, invalid, missing, malformed cases
8. **[COMPLETION]** Document all semantic check signatures and fail-closed behavior in `D-0013/spec.md`

**Acceptance Criteria:**
- All 9 semantic check functions exist in `gates.py` with fail-closed behavior (missing/malformed input returns False)
- Each function has unit tests covering valid, invalid, missing, malformed, and failing-value inputs -- with distinct log messages verified for each failure mode
- `_pre_approved_not_in_fix_roadmap()` implementation matches OQ-A resolution from T01.01
- `uv run pytest tests/sprint/test_gates_data.py -v` exits 0 with all boundary tests passing

**Validation:**
- `uv run pytest tests/sprint/test_gates_data.py -v` exits 0 with all tests passing
- Evidence: linkable artifact produced at `D-0013/spec.md`

**Dependencies:** T02.02 (parse_frontmatter public), T02.03 (_parse_routing_list available)
**Rollback:** Revert semantic check additions to `gates.py`

---

### Checkpoint: Phase 2 / Tasks 1-5

**Purpose:** Verify data model changes and core semantic check functions are implemented and tested.
**Checkpoint Report Path:** `.dev/releases/current/v2.26-roadmap-v5/checkpoints/CP-P02-T01-T05.md`
**Verification:**
- `Finding` dataclass accepts `deviation_class` with validation
- `parse_frontmatter()` is public; all callers updated
- All 9 semantic check functions pass boundary-input unit tests
**Exit Criteria:**
- `uv run pytest tests/sprint/test_models.py tests/sprint/test_gates_data.py -v` exits 0
- No remaining `_parse_frontmatter` references in codebase
- D-0010 through D-0013 artifacts exist and are non-empty

---

### T02.05 -- Define ANNOTATE_DEVIATIONS_GATE and DEVIATION_ANALYSIS_GATE

| Field | Value |
|---|---|
| Roadmap Item IDs | R-033, R-034 |
| Why | Two new gates required for the deviation-aware pipeline; ANNOTATE is STANDARD tier, DEVIATION_ANALYSIS is STRICT tier with 6 ordered semantic checks |
| Effort | M |
| Risk | Medium |
| Risk Drivers | Multi-file, system-wide (gate infrastructure) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0014 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0014/spec.md`

**Deliverables:**
1. `ANNOTATE_DEVIATIONS_GATE` (STANDARD tier, required fields include `roadmap_hash`, check: `_total_annotated_consistent`) and `DEVIATION_ANALYSIS_GATE` (STRICT tier, 6 semantic checks in specified order) defined in `gates.py`

**Steps:**
1. **[PLANNING]** Review existing gate definition pattern in `gates.py` (GateCriteria usage)
2. **[PLANNING]** Confirm required fields and semantic check ordering from roadmap
3. **[EXECUTION]** Define `ANNOTATE_DEVIATIONS_GATE` — STANDARD tier, required fields include `roadmap_hash`, check: `_total_annotated_consistent`
4. **[EXECUTION]** Define `DEVIATION_ANALYSIS_GATE` — STRICT tier, 6 semantic checks in order: `no_ambiguous_deviations`, `validation_complete_true`, `routing_consistent_with_slip_count`, `pre_approved_not_in_fix_roadmap`, `slip_count_matches_routing`, `total_analyzed_consistent`
5. **[VERIFICATION]** Verify DEVIATION_ANALYSIS_GATE semantic check *order*, not just existence
6. **[VERIFICATION]** Run targeted gate tests confirming both gates validate correctly
7. **[COMPLETION]** Document gate definitions in `D-0014/spec.md`

**Acceptance Criteria:**
- `ANNOTATE_DEVIATIONS_GATE` defined as STANDARD tier with `roadmap_hash` in required fields
- `DEVIATION_ANALYSIS_GATE` defined as STRICT tier with exactly 6 semantic checks in the specified order
- Unit test asserts the ordered list/tuple of semantic check references in `DEVIATION_ANALYSIS_GATE`, not merely that all 6 checks are present
- `ANNOTATE_DEVIATIONS_GATE` required fields list is complete per FR-013 and FR-070, not limited to `roadmap_hash` alone
- Gate definitions follow existing GateCriteria pattern in `gates.py`
- `uv run pytest tests/sprint/ -v -k "gate"` exits 0 with gate definition tests passing

**Validation:**
- `uv run pytest tests/sprint/ -v -k "gate"` exits 0 with all tests passing
- Evidence: linkable artifact produced at `D-0014/spec.md`

**Dependencies:** T02.04 (semantic check functions must exist)
**Rollback:** Remove gate constant definitions from `gates.py`

---

### T02.06 -- Modify SPEC_FIDELITY_GATE and CERTIFY_GATE

| Field | Value |
|---|---|
| Roadmap Item IDs | R-035, R-036 |
| Why | SPEC_FIDELITY_GATE must be downgraded STRICT->STANDARD with deprecated checks removed; CERTIFY_GATE must include certified_true check |
| Effort | M |
| Risk | Medium |
| Risk Drivers | Breaking change (gate tier downgrade), system-wide |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0015 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0015/spec.md`

**Deliverables:**
1. Modified `SPEC_FIDELITY_GATE` (downgraded to STANDARD, deprecated checks removed with docstrings) and `CERTIFY_GATE` (appended `certified_true` semantic check) in `gates.py`

**Steps:**
1. **[PLANNING]** Read current `SPEC_FIDELITY_GATE` and `CERTIFY_GATE` definitions
2. **[PLANNING]** Identify `high_severity_count_zero` and `tasklist_ready_consistent` checks to remove
3. **[EXECUTION]** Downgrade `SPEC_FIDELITY_GATE` from STRICT to STANDARD
4. **[EXECUTION]** Remove `high_severity_count_zero` and `tasklist_ready_consistent` from active checks; add `[DEPRECATED v2.26]` docstrings
5. **[EXECUTION]** Append `certified_true` semantic check to `CERTIFY_GATE`
6. **[VERIFICATION]** Run full test suite to confirm STANDARD downgrade is a relaxation and doesn't break existing tests
7. **[COMPLETION]** Document modifications in `D-0015/spec.md`

**Acceptance Criteria:**
- `SPEC_FIDELITY_GATE` tier is STANDARD (not STRICT)
- All deprecated semantic check functions (including but not limited to `high_severity_count_zero` and `tasklist_ready_consistent`) have `[DEPRECATED v2.26]` docstrings; complete list of deprecated functions documented explicitly
- `CERTIFY_GATE` includes `certified_true` check
- `uv run pytest -v` exits 0 confirming full test suite passes (STANDARD downgrade is relaxation, confirm no regressions)

**Validation:**
- `uv run pytest tests/sprint/ -v` exits 0 with all tests passing
- Evidence: linkable artifact produced at `D-0015/spec.md`

**Dependencies:** T02.04 (_certified_is_true function must exist)
**Rollback:** Revert gate modifications; restore STRICT tier and removed checks

---

### T02.07 -- Update ALL_GATES Registry and Retain Deprecated Checks

| Field | Value |
|---|---|
| Roadmap Item IDs | R-037, R-038 |
| Why | ALL_GATES registry must include both new gate entries; deprecated semantic check functions must be retained with docstrings |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0016 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0016/evidence.md`

**Deliverables:**
1. Updated `ALL_GATES` registry in `gates.py` with both new gate entries; deprecated semantic check functions retained with `[DEPRECATED v2.26]` docstrings

**Steps:**
1. **[PLANNING]** Read current `ALL_GATES` registry definition
2. **[PLANNING]** Identify deprecated semantic check functions to retain
3. **[EXECUTION]** Add `ANNOTATE_DEVIATIONS_GATE` and `DEVIATION_ANALYSIS_GATE` to `ALL_GATES` registry
4. **[EXECUTION]** Add `[DEPRECATED v2.26]` docstrings to deprecated semantic check functions (do not delete)
5. **[VERIFICATION]** Confirm `ALL_GATES` contains all expected gate entries; deprecated functions still importable
6. **[COMPLETION]** Document registry update in `D-0016/evidence.md`

**Acceptance Criteria:**
- `ALL_GATES` registry contains both `ANNOTATE_DEVIATIONS_GATE` and `DEVIATION_ANALYSIS_GATE`
- Deprecated semantic check functions exist with `[DEPRECATED v2.26]` docstrings
- No deprecated function deleted
- `uv run pytest tests/sprint/ -v -k "gate"` exits 0

**Validation:**
- `uv run pytest tests/sprint/ -v -k "gate"` exits 0 with all tests passing
- Evidence: linkable artifact produced at `D-0016/evidence.md`

**Dependencies:** T02.05, T02.06 (gates must be defined before registering)
**Rollback:** Remove new gate entries from ALL_GATES; remove deprecation docstrings

---

### T02.08 -- Validate Phase 2 Exit Criteria

| Field | Value |
|---|---|
| Roadmap Item IDs | R-039 |
| Why | Gate check: all Phase 1 (roadmap) exit criteria verified before proceeding to Phase 3 |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0017 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0017/evidence.md`

**Deliverables:**
1. Phase 2 exit criteria checklist with all 11 criteria verified

**Steps:**
1. **[PLANNING]** Load Phase 1 (roadmap) exit criteria from roadmap (12 checkboxes)
2. **[PLANNING]** Gather test results and artifact evidence from T02.01-T02.07
3. **[EXECUTION]** Verify each of the 11 exit criteria with specific test output or artifact reference
4. **[EXECUTION]** Confirm `DEVIATION_ANALYSIS_GATE` semantic check order verified (not just existence)
5. **[EXECUTION]** Confirm Phase 0 OQ-A resolved and gate implementation matches chosen option
6. **[VERIFICATION]** Run `uv run pytest tests/sprint/ -v` to confirm full test suite passes
7. **[COMPLETION]** Write exit criteria verification to `D-0017/evidence.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0017/evidence.md` exists with all 11 exit criteria checked
- Each criterion references specific test output or artifact
- Full test suite passes: `uv run pytest tests/sprint/ -v` exits 0
- Phase 3 is unblocked

**Validation:**
- `uv run pytest tests/sprint/ -v` exits 0 with all tests passing
- Evidence: linkable artifact produced at `D-0017/evidence.md`

**Dependencies:** T02.07
**Rollback:** TBD (validation task; no code changes)

---

### Checkpoint: End of Phase 2

**Purpose:** Confirm all data model, parsing, and gate infrastructure is in place for pipeline step wiring in Phase 3.
**Checkpoint Report Path:** `.dev/releases/current/v2.26-roadmap-v5/checkpoints/CP-P02-END.md`
**Verification:**
- `Finding` dataclass with `deviation_class` backward-compatible
- All 9+ semantic check functions pass unit tests with boundary inputs
- Both new gates defined; existing gates modified; ALL_GATES updated
**Exit Criteria:**
- `uv run pytest tests/sprint/ -v` exits 0 with no regressions
- All 12 Phase 1 (roadmap) exit criteria verified in D-0017
- D-0010 through D-0017 artifacts exist and are non-empty
