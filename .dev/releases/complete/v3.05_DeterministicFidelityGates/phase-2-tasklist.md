# Phase 2 -- Structural Checkers & Severity Engine

Build the five deterministic checkers and their severity rule tables. After this phase, ~70% of fidelity checks are deterministic. Exit when SC-1 is proven: identical inputs produce byte-identical findings (Gate B).

### T02.01 -- Define Checker Callable Interface and Registry

| Field | Value |
|---|---|
| Roadmap Item IDs | R-024 |
| Why | Checkers must conform to a uniform interface for the pipeline to dispatch them. The registry maps dimension names to checker callables. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | cross-cutting (all 5 checkers depend on this interface) |
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
- `TASKLIST_ROOT/artifacts/D-0012/spec.md`

**Deliverables:**
1. Checker callable interface `(spec_path, roadmap_path) -> List[Finding]` defined in `structural_checkers.py`; registry dict mapping dimension names to checker callables; checkers receive only relevant `SpecSection` objects per dimension-to-section mapping

**Steps:**
1. **[PLANNING]** Review FR-1 acceptance criteria for checker interface requirements
2. **[PLANNING]** Confirm dimension-to-section mapping from T01.04 is available
3. **[EXECUTION]** Define checker callable type alias in `structural_checkers.py`
4. **[EXECUTION]** Implement checker registry: `CHECKER_REGISTRY: dict[str, Callable]` mapping 5 dimension names
5. **[EXECUTION]** Implement section routing: each checker receives only its relevant `SpecSection` objects
6. **[VERIFICATION]** Verify registry maps all 5 dimensions; each callable matches the interface
7. **[COMPLETION]** Document interface contract in `TASKLIST_ROOT/artifacts/D-0012/spec.md`

**Acceptance Criteria:**
- `structural_checkers.py` defines checker callable type: `(spec_path, roadmap_path) -> List[Finding]`
- `CHECKER_REGISTRY` dict maps all 5 dimension names (signatures, data_models, gates, cli, nfrs) to callables
- Each checker receives only the sections relevant to its dimension via the mapping from T01.04
- Registry is importable and all entries are callable

**Validation:**
- `uv run pytest tests/roadmap/test_structural_checkers.py::test_registry -v` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0012/spec.md` documents interface contract

**Dependencies:** T01.04, T01.05
**Rollback:** TBD

---

### T02.02 -- Implement Signatures and Data Models Checkers (FR-1)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-025, R-026 |
| Why | Signatures checker has highest structural % (80%) and catches phantom ID/missing function bugs. Data Models checker (85%) catches missing files and path prefix mismatches. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | cross-cutting (checkers feed registry and convergence), dependency (requires parser output) |
| Tier | STRICT |
| Confidence | [████████░░] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0013 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0013/spec.md`

**Deliverables:**
1. Signatures checker: compares function signatures from spec code blocks against roadmap; uses machine keys `phantom_id`, `function_missing`, `param_arity_mismatch`, `param_type_mismatch`. Data Models checker: compares file manifest tables, dataclass fields, enum literals; uses machine keys `file_missing`, `path_prefix_mismatch`, `enum_uncovered`, `field_missing`

**Steps:**
1. **[PLANNING]** Identify spec sections feeding each checker (FR sections for Signatures, Sec 4.x for Data Models)
2. **[PLANNING]** List all machine keys and severity rules for both checkers
3. **[EXECUTION]** Implement Signatures checker: extract function sigs from spec, compare against roadmap references, produce typed findings
4. **[EXECUTION]** Implement Data Models checker: extract file manifest, dataclass fields, enum literals, compare against roadmap tasks
5. **[EXECUTION]** Ensure both checkers use `get_severity()` for severity assignment (never LLM)
6. **[VERIFICATION]** Run both checkers on real spec sections; verify findings have correct machine keys and severities
7. **[COMPLETION]** Document checker behavior in `TASKLIST_ROOT/artifacts/D-0013/spec.md`

**Acceptance Criteria:**
- Signatures checker produces findings with machine keys `phantom_id`, `function_missing`, `param_arity_mismatch`, `param_type_mismatch`
- Data Models checker produces findings with machine keys `file_missing`, `path_prefix_mismatch`, `enum_uncovered`, `field_missing`
- Both checkers assign severity via `get_severity()` lookup, never LLM
- Each finding includes: dimension, rule_id, severity, spec_quote, roadmap_quote_or_MISSING, location

**Validation:**
- `uv run pytest tests/roadmap/test_structural_checkers.py -v -k "signatures or data_models"` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0013/spec.md` documents checker outputs

**Dependencies:** T02.01, T01.02
**Rollback:** TBD

---

### T02.03 -- Implement Gates, CLI Options, and NFRs Checkers (FR-1)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-027, R-028, R-029 |
| Why | Gates (65%), CLI (75%), and NFRs (55%) checkers complete the 5-dimension deterministic layer. Together with Signatures and Data Models, they cover ~70% of fidelity checks. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | cross-cutting (3 checkers, shared interface), dependency (requires parser and severity rules) |
| Tier | STRICT |
| Confidence | [████████░░] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0014 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0014/spec.md`

**Deliverables:**
1. Gates checker (machine keys: `frontmatter_field_missing`, `step_param_missing`, `ordering_violated`, `semantic_check_missing`), CLI Options checker (machine keys: `mode_uncovered`, `default_mismatch`), NFRs checker (machine keys: `threshold_contradicted`, `security_missing`, `dep_direction_violated`, `coverage_mismatch`, `dep_rule_missing`)

**Steps:**
1. **[PLANNING]** Identify spec sections for each checker (FR-7/FR-8 for Gates, Sec 5.1 for CLI, Sec 6 for NFRs)
2. **[PLANNING]** List all machine keys and severity rules for all 3 checkers
3. **[EXECUTION]** Implement Gates checker: verify gate definitions, thresholds, step ordering
4. **[EXECUTION]** Implement CLI Options checker: compare Click options, flags, defaults
5. **[EXECUTION]** Implement NFRs checker: verify numeric thresholds, security primitives, dependency rules
6. **[VERIFICATION]** Run all 3 checkers on real spec sections; verify correct machine keys and no shared mutable state
7. **[COMPLETION]** Document checker behavior in `TASKLIST_ROOT/artifacts/D-0014/spec.md`

**Acceptance Criteria:**
- All 3 checkers produce findings with their specified machine keys
- All checkers assign severity via `get_severity()` lookup
- Checkers share no mutable state (can run in parallel without interference)
- Each finding includes dimension, rule_id, severity, spec_quote, roadmap_quote_or_MISSING, location

**Validation:**
- `uv run pytest tests/roadmap/test_structural_checkers.py -v -k "gates or cli or nfrs"` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0014/spec.md` documents all 3 checker outputs

**Dependencies:** T02.01, T01.02
**Rollback:** TBD

---

### T02.04 -- Implement Complete Severity Rule Table (FR-3)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-030 |
| Why | All 19 canonical rules must be implemented with deterministic severity assignment. Unknown mismatch types must raise `KeyError` to force explicit rule addition. |
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
| Deliverable IDs | D-0015 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0015/evidence.md`

**Deliverables:**
1. All 19 canonical severity rules in `SEVERITY_RULES` dict verified: 7 HIGH rules, 12 MEDIUM rules across 5 dimensions

**Steps:**
1. **[PLANNING]** Cross-reference spec FR-3 table against `SEVERITY_RULES` dict from T01.05
2. **[EXECUTION]** Verify all 19 rules present with correct severity assignments
3. **[EXECUTION]** Test `get_severity()` returns correct severity for each of the 19 rules
4. **[EXECUTION]** Test `get_severity()` raises `KeyError` for unknown `(dimension, mismatch_type)` combos
5. **[VERIFICATION]** `uv run pytest tests/roadmap/test_structural_checkers.py::test_severity_rules -v` exits 0
6. **[COMPLETION]** Document rule coverage in `TASKLIST_ROOT/artifacts/D-0015/evidence.md`

**Acceptance Criteria:**
- `SEVERITY_RULES` contains exactly 19 entries matching spec FR-3 table
- `get_severity()` returns correct severity for all 19 canonical rules
- `get_severity()` raises `KeyError` for `("signatures", "unknown_key")`
- Rule table is extensible (adding a new tuple entry does not require checker logic changes)

**Validation:**
- `uv run pytest tests/roadmap/test_structural_checkers.py::test_severity_rules -v` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0015/evidence.md` lists all 19 rules with severities

**Dependencies:** T01.05
**Rollback:** TBD

---

### Checkpoint: Phase 2 / Tasks T02.01-T02.04

**Purpose:** Verify all 5 checkers produce correct findings before determinism proof.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-T01-T04.md`
**Verification:**
- All 5 checkers registered and callable via registry
- Severity rules cover all 19 canonical mismatch types
- Checkers produce findings with correct machine keys and severity
**Exit Criteria:**
- All checker unit tests pass on real spec sections
- No shared mutable state between checkers
- `get_severity()` raises `KeyError` on unknown combinations

---

### T02.05 -- Verify Determinism: SC-1 Proof (Gate B)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-031 |
| Why | SC-1 requires identical inputs to produce byte-identical structural findings. This is the core determinism guarantee of the entire architecture. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | cross-cutting (system-wide determinism property) |
| Tier | STANDARD |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0016 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0016/evidence.md`

**Deliverables:**
1. Determinism proof: two runs of all 5 checkers on identical inputs produce byte-identical findings (SC-1, NFR-1, NFR-4)

**Steps:**
1. **[PLANNING]** Prepare fixed spec + roadmap inputs for determinism test
2. **[EXECUTION]** Run all 5 checkers on the fixed inputs, serialize output
3. **[EXECUTION]** Run all 5 checkers again on the same inputs, serialize output
4. **[EXECUTION]** Diff both outputs; verify zero differences
5. **[EXECUTION]** Run checkers in parallel to verify no interference (NFR-4)
6. **[VERIFICATION]** Confirm byte-identical output across runs and parallel execution
7. **[COMPLETION]** Write determinism proof to `TASKLIST_ROOT/artifacts/D-0016/evidence.md`

**Acceptance Criteria:**
- Two sequential runs on identical inputs produce byte-identical serialized findings
- Parallel execution of all 5 checkers produces identical output to sequential execution
- No shared mutable state detected across checker runs (NFR-4)
- Determinism proof document includes diff output showing zero differences

**Validation:**
- `uv run pytest tests/roadmap/test_structural_checkers.py::test_determinism -v` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0016/evidence.md` with diff output

**Dependencies:** T02.02, T02.03, T02.04
**Rollback:** TBD

---

### Checkpoint: End of Phase 2

**Purpose:** Gate B -- Structural Determinism Certified. SC-1 proven before registry and semantic layer development.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-END.md`
**Verification:**
- All 5 checkers pass unit tests with real spec sections
- Checkers execute in parallel without interference (NFR-4)
- Determinism verified: two runs on identical input produce byte-identical findings (SC-1)
**Exit Criteria:**
- Severity rules cover all 19 canonical mismatch types
- SC-1 determinism proof documented with diff output
- All Phase 2 tasks completed with passing validation
