# Phase 3 -- Pipeline Fixes + Reachability Gate

Ship the three production code changes (0-files-analyzed fix, impl-vs-spec fidelity checker, reachability gate interface) and validate them with targeted tests. Production changes are constrained to FR-5.1, FR-5.2, and FR-4.3 only.

---

### T03.01 -- Add 0-files-analyzed assertion guard to wiring_gate.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-039 |
| Why | If `files_analyzed == 0` and source dir is non-empty, the wiring gate silently passes; this must return FAIL with `failure_reason` (FR-5.1) |
| Effort | S |
| Risk | Medium |
| Risk Drivers | breaking change (new failure condition) |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0038 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0038/spec.md`
- `TASKLIST_ROOT/artifacts/D-0038/evidence.md`

**Deliverables:**
- Modified `src/superclaude/cli/audit/wiring_gate.py` — `run_wiring_analysis()` with 0-files guard: if `files_analyzed == 0` AND source dir non-empty -> return FAIL with `failure_reason`

**Steps:**
1. **[PLANNING]** Read `src/superclaude/cli/audit/wiring_gate.py` to locate `run_wiring_analysis()` and understand current return path
2. **[PLANNING]** Investigate the 3 pre-existing test failures per OQ-7; determine if any are related to this code path
3. **[EXECUTION]** Add assertion guard: after analysis completes, check `files_analyzed == 0` AND source dir contains files -> return FAIL with `failure_reason = "0 files analyzed in non-empty source directory"`
4. **[EXECUTION]** Implement as additive failure condition (new early return) per R-5 mitigation; do not modify existing logic paths
5. **[VERIFICATION]** Sub-agent verification: existing tests still pass; new guard triggers on synthetic empty-analysis scenario
6. **[COMPLETION]** Record which pre-existing failures (if any) are resolved by this fix

**Acceptance Criteria:**
- `run_wiring_analysis()` in `wiring_gate.py` returns FAIL with `failure_reason` when `files_analyzed == 0` and source dir is non-empty
- Change is additive (new early return path); existing return paths unmodified per R-5 mitigation
- No new regressions beyond intended behavior change
- Change documented in function docstring

**Validation:**
- `uv run pytest tests/v3.3/ tests/roadmap/ -v` (full v3.3 + roadmap suites)
- Evidence: diff showing additive guard, not modified existing logic

**Dependencies:** Phase 2 complete (tests exist to validate)
**Rollback:** Remove the additive guard; existing logic paths remain unchanged
**Notes:** Per R-5, investigate 3 pre-existing failures before patching. If 2 are wiring-pipeline related, this fix may resolve them.

---

### T03.02 -- Implement impl-vs-spec fidelity checker module

| Field | Value |
|---|---|
| Roadmap Item IDs | R-040 |
| Why | Reads spec FRs, searches codebase for function/class name evidence, reports implementation gaps (FR-5.2) |
| Effort | L |
| Risk | High |
| Risk Drivers | cross-cutting scope (codebase search), breaking change potential (new checker in pipeline) |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0039 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0039/spec.md`
- `TASKLIST_ROOT/artifacts/D-0039/evidence.md`

**Deliverables:**
- New `src/superclaude/cli/roadmap/fidelity_checker.py` — reads spec FRs, searches codebase for function/class name evidence, reports gaps; starts with exact name matching per OQ-2

**Steps:**
1. **[PLANNING]** Define matching contract in docstring per architect recommendation for R-3 mitigation: exact function-name or class-name match as minimum evidence
2. **[PLANNING]** Design allowlist of known FR->function mappings as starting point per architect recommendation
3. **[EXECUTION]** Create `src/superclaude/cli/roadmap/fidelity_checker.py` with `FidelityChecker` class
4. **[EXECUTION]** Implement FR extraction: parse spec for `FR-X.Y` patterns, extract associated function/class names
5. **[EXECUTION]** Implement codebase search: exact function-name and class-name matching via `ast.parse()` or string search
6. **[EXECUTION]** Implement gap reporting: for each FR, report whether evidence found; fail-open on ambiguous matches (log warning, don't block) per R-3 mitigation
7. **[VERIFICATION]** Sub-agent verification: checker passes known-good synthetic cases and flags known-bad synthetic cases
8. **[COMPLETION]** Document matching contract in module docstring

**Acceptance Criteria:**
- `src/superclaude/cli/roadmap/fidelity_checker.py` exists with `FidelityChecker` class
- Exact function-name and class-name matching per OQ-2 (no NLP/fuzzy matching)
- Fail-open on ambiguous matches per R-3 mitigation (log warning, don't block)
- Matching contract documented in module docstring

**Validation:**
- `uv run pytest tests/v3.3/ -k "fidelity" -v` (after T03.07)
- Evidence: checker output on synthetic positive and negative cases

**Dependencies:** Phase 1B (AST infrastructure)
**Rollback:** Delete `src/superclaude/cli/roadmap/fidelity_checker.py`
**Notes:** R-3 is the highest-friction risk. Start with allowlist of known FR->function mappings per architect recommendation.

---

### T03.03 -- Wire fidelity_checker into _run_checkers() registry

| Field | Value |
|---|---|
| Roadmap Item IDs | R-041 |
| Why | The fidelity checker must be integrated into the convergence pipeline's checker dispatch table alongside structural and semantic checkers (FR-5.2) |
| Effort | M |
| Risk | Medium |
| Risk Drivers | breaking change (new checker in existing pipeline), cross-cutting |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0040 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0040/spec.md`
- `TASKLIST_ROOT/artifacts/D-0040/evidence.md`

**Deliverables:**
- Modified `src/superclaude/cli/roadmap/executor.py` — `_run_checkers()` registry updated to include `fidelity_checker` alongside structural and semantic layers

**Steps:**
1. **[PLANNING]** Read `src/superclaude/cli/roadmap/executor.py` to understand `_run_checkers()` dispatch table structure and ordering
2. **[PLANNING]** Verify checker output shape and failure aggregation contract to ensure fidelity checker is compatible
3. **[EXECUTION]** Add `fidelity_checker` to `_run_checkers()` registry; preserve ordering of existing structural and semantic checkers
4. **[EXECUTION]** Ensure fidelity checker output conforms to existing checker output shape for failure aggregation
5. **[VERIFICATION]** Sub-agent verification: structural and semantic checkers still function; fidelity checker invoked in correct order
6. **[COMPLETION]** Record integration point and ordering in evidence

**Acceptance Criteria:**
- `_run_checkers()` in `executor.py` invokes `fidelity_checker` alongside structural and semantic checkers
- Existing checker ordering preserved; fidelity checker integrated alongside structural and semantic layers per roadmap 3A.3; ordering relative to existing checkers determined by integration contract review
- Checker output shape compatible with failure aggregation per the existing structural/semantic checker output contract in `_run_checkers()`
- No regressions in structural or semantic checker behavior

**Validation:**
- `uv run pytest tests/roadmap/ -v` (convergence pipeline tests)
- Evidence: diff showing registry addition

**Dependencies:** T03.02
**Rollback:** Remove fidelity_checker from `_run_checkers()` registry

---

### T03.04 -- Add GateCriteria-compatible reachability interface

| Field | Value |
|---|---|
| Roadmap Item IDs | R-042 |
| Why | The reachability analyzer needs a GateCriteria-compatible interface to integrate as a pipeline gate producing structured PASS/FAIL reports (FR-4.3) |
| Effort | M |
| Risk | Medium |
| Risk Drivers | cross-cutting (gate infrastructure integration) |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0041 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0041/spec.md`
- `TASKLIST_ROOT/artifacts/D-0041/evidence.md`

**Deliverables:**
- Extended `src/superclaude/cli/audit/reachability.py` — `GateCriteria`-compatible interface: reads manifest, runs AST analysis, produces structured PASS/FAIL report

**Steps:**
1. **[PLANNING]** Read `GateCriteria` interface from `pipeline/models.py` to understand required contract
2. **[PLANNING]** Design adapter: `ReachabilityAnalyzer` -> `GateCriteria` output shape
3. **[EXECUTION]** Add `GateCriteria`-compatible method to `ReachabilityAnalyzer`: reads manifest, runs analysis, produces structured report with PASS/FAIL and failure details
4. **[EXECUTION]** Integrate with existing gate infrastructure; ensure report format matches other gate outputs
5. **[VERIFICATION]** Sub-agent verification: gate produces PASS for fully-reachable manifest and FAIL for manifest with unreachable symbols
6. **[COMPLETION]** Record integration interface in evidence

**Acceptance Criteria:**
- `reachability.py` exposes `GateCriteria`-compatible interface producing structured PASS/FAIL reports
- Interface reads wiring manifest and runs AST analysis end-to-end
- PASS/FAIL report includes failure details (which symbols unreachable, from which entry points)
- Report format compatible with existing gate infrastructure

**Validation:**
- `uv run pytest tests/v3.3/test_reachability_eval.py -v` (extended with gate interface tests)
- Evidence: PASS and FAIL report samples

**Dependencies:** T01.06 (AST analyzer), T01.07 (manifest)
**Rollback:** Remove GateCriteria interface from reachability module

---

### Checkpoint: Phase 3 / Tasks T03.01-T03.04

**Purpose:** Verify all 3 production code changes are shipped and integrated before validation tests.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P03-T01-T04.md`
**Verification:**
- 0-files guard added to `wiring_gate.py` as additive change
- Fidelity checker created and wired into `_run_checkers()`
- Reachability gate has `GateCriteria`-compatible interface

**Exit Criteria:**
- `uv run pytest tests/roadmap/ -v` exits 0 (no regressions from production changes)
- All 3 new/modified production files exist at expected paths
- Fidelity checker uses exact name matching (no fuzzy/NLP)

---

### T03.05 -- Write 0-files-analyzed -> FAIL validation test

| Field | Value |
|---|---|
| Roadmap Item IDs | R-043 |
| Why | Validate the 0-files-analyzed fix: non-empty dir with 0 files analyzed must return FAIL, not silent PASS (FR-5.1, SC-10) |
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
| Deliverable IDs | D-0042 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0042/spec.md`

**Deliverables:**
- 1 test validating 0-files-analyzed on non-empty dir returns FAIL with `failure_reason`

**Steps:**
1. **[PLANNING]** Design test scenario: non-empty source directory but analysis produces 0 files_analyzed
2. **[EXECUTION]** Write `test_zero_files_analyzed_returns_fail`: set up non-empty dir, configure analysis to produce 0 files result, assert FAIL return with `failure_reason` field
3. **[VERIFICATION]** Run `uv run pytest tests/v3.3/ -k "zero_files" -v`
4. **[COMPLETION]** Emit audit record with spec_ref FR-5.1, SC-10

**Acceptance Criteria:**
- Test confirms `run_wiring_analysis()` returns FAIL when `files_analyzed == 0` on non-empty dir
- `failure_reason` field is present and descriptive
- Test uses real `run_wiring_analysis()` (no mocks on gate)
- Test emits JSONL audit record

**Validation:**
- `uv run pytest tests/v3.3/ -k "zero_files" -v`
- Evidence: test output showing FAIL result

**Dependencies:** T03.01
**Rollback:** Remove test

---

### T03.06 -- Write broken wiring detection regression test

| Field | Value |
|---|---|
| Roadmap Item IDs | R-044 |
| Why | Regression test: intentionally remove `run_post_phase_wiring_hook()` call and verify gate detects the gap referencing v3.2-T02 (FR-4.4, SC-7, SC-9) |
| Effort | M |
| Risk | Medium |
| Risk Drivers | cross-cutting (modifies code temporarily for regression detection) |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0043 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0043/spec.md`
- `TASKLIST_ROOT/artifacts/D-0043/evidence.md`

**Deliverables:**
- 1 regression test: temporarily removes `run_post_phase_wiring_hook()` call, runs reachability gate, asserts gap detected

**Steps:**
1. **[PLANNING]** Identify the `run_post_phase_wiring_hook()` call site to temporarily remove for regression testing
2. **[PLANNING]** Design test: use a synthetic/copied module with the call removed (do not modify production code in test)
3. **[EXECUTION]** Write `test_broken_wiring_detected`: create synthetic module missing the hook call, run reachability gate against it, assert FAIL with gap referencing the missing wiring
4. **[VERIFICATION]** Run `uv run pytest tests/v3.3/ -k "broken_wiring" -v`
5. **[COMPLETION]** Emit audit record with spec_ref FR-4.4, SC-7, SC-9

**Acceptance Criteria:**
- Test intentionally breaks wiring (using synthetic module, not production code modification)
- Reachability gate detects the gap and reports it in structured output
- Gate output references the specific missing wiring point
- Test emits JSONL audit record

**Validation:**
- `uv run pytest tests/v3.3/ -k "broken_wiring" -v`
- Evidence: gate FAIL output showing detected gap

**Dependencies:** T03.04 (GateCriteria interface)
**Rollback:** Remove regression test

---

### T03.07 -- Write impl-vs-spec checker positive + negative tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-045 |
| Why | Validate fidelity checker with both positive (finds existing impl) and negative (flags gap in synthetic test) cases (FR-5.2, SC-11) |
| Effort | M |
| Risk | Medium |
| Risk Drivers | cross-cutting (codebase search in test) |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0044 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0044/spec.md`
- `TASKLIST_ROOT/artifacts/D-0044/evidence.md`

**Deliverables:**
- 2 tests: (a) positive case — checker finds existing implementation evidence for known FR; (b) negative case — checker flags gap in synthetic test with missing implementation (per R-3 mitigation: use synthetic fixtures to control test conditions)

**Steps:**
1. **[PLANNING]** Identify a known-good FR->function mapping for positive test and design a synthetic missing mapping for negative test
2. **[EXECUTION]** Write `test_fidelity_checker_positive`: checker finds implementation evidence for known existing function
3. **[EXECUTION]** Write `test_fidelity_checker_negative`: checker flags gap for synthetic FR with no matching implementation
4. **[VERIFICATION]** Run `uv run pytest tests/v3.3/ -k "fidelity_checker" -v`
5. **[COMPLETION]** Emit audit records with spec_ref FR-5.2, SC-11

**Acceptance Criteria:**
- Positive test: checker reports evidence found for known existing implementation
- Negative test: checker reports gap for synthetic FR with missing implementation
- Tests use real `FidelityChecker` (no mocks on checker internals)
- Both tests emit JSONL audit records

**Validation:**
- `uv run pytest tests/v3.3/ -k "fidelity_checker" -v`
- Evidence: checker output for both positive and negative cases

**Dependencies:** T03.02 (fidelity checker)
**Rollback:** Remove checker tests

---

### Checkpoint: End of Phase 3

**Purpose:** Confirm all production fixes shipped, reachability gate catches broken wiring, fidelity checker detects gaps, and all new gates integrate into existing infrastructure.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P03-END.md`
**Verification:**
- 0-files guard returns FAIL on non-empty dir with 0 analyzed (SC-10)
- Reachability gate detects intentionally broken wiring (SC-7, SC-9)
- Fidelity checker finds known-good and flags known-bad (SC-11)

**Exit Criteria:**
- `uv run pytest tests/v3.3/ tests/roadmap/ -v` exits 0 with all Phase 3 tests passing
- SC-7, SC-9, SC-10, SC-11 validated
- No regressions from production code changes (existing test count stable)
