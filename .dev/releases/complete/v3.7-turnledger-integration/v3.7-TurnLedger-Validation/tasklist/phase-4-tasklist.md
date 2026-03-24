# Phase 4 -- Regression Validation + Final Audit

Full regression sweep, audit trail verification, and documentation. This phase validates the release gate: zero regressions, complete audit trail, and all 12 success criteria green.

---

### T04.01 -- Run full test suite regression validation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-046 |
| Why | Confirm >= 4894 passed, <= 3 pre-existing failures, 0 new regressions across the entire test suite (NFR-3, SC-4) |
| Effort | M |
| Risk | Medium |
| Risk Drivers | regression risk across full suite |
| Tier | EXEMPT |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0045 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0045/spec.md`
- `TASKLIST_ROOT/artifacts/D-0045/evidence.md`

**Deliverables:**
- Full test suite run report: total passed, total failed, pre-existing vs new failures identified

**Steps:**
1. **[PLANNING]** Establish baseline: run `uv run pytest` to capture current pass/fail counts
2. **[PLANNING]** Document the <= 3 pre-existing failures by name and reason (per OQ-7)
3. **[EXECUTION]** Run `uv run pytest --tb=short` across entire test suite
4. **[EXECUTION]** Compare results against baseline: identify any new failures
5. **[VERIFICATION]** Assert >= 4894 passed, <= 3 pre-existing failures, 0 new regressions
6. **[COMPLETION]** Record full results in evidence with pass/fail breakdown

**Acceptance Criteria:**
- `uv run pytest` reports >= 4894 passed tests
- <= 3 pre-existing failures (documented with names and reasons)
- 0 new regressions introduced by v3.3 changes
- Results recorded in evidence artifact

**Validation:**
- `uv run pytest --tb=short` (full suite)
- Evidence: test output summary with counts

**Dependencies:** All Phase 1-3 tasks
**Rollback:** N/A (validation only)

---

### T04.02 -- Run grep-audit for mock.patch on gate functions or orchestration logic

| Field | Value |
|---|---|
| Roadmap Item IDs | R-047 |
| Why | Confirm no `mock.patch` usage on gate functions or orchestration logic across all v3.3 test files (NFR-1) |
| Effort | S |
| Risk | Low |
| Risk Drivers | audit |
| Tier | EXEMPT |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0046 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0046/spec.md`

**Deliverables:**
- Grep-audit report confirming zero `mock.patch` on gate functions or orchestration logic (including `execute_phase_tasks()`, `_run_checkers()`, `_subprocess_factory` wiring paths) across all v3.3 test files

**Steps:**
1. **[PLANNING]** Define search patterns: `mock.patch`, `@patch`, `patch(` targeting gate function names and orchestration module paths
2. **[EXECUTION]** Run grep across `tests/v3.3/` for `mock.patch` patterns targeting gate/orchestration modules
3. **[EXECUTION]** Run grep across `tests/roadmap/` for same patterns in files modified by v3.3
4. **[VERIFICATION]** Assert zero matches for prohibited mock patterns
5. **[COMPLETION]** Record grep results as evidence

**Acceptance Criteria:**
- Zero `mock.patch` usage on gate functions or orchestration logic in `tests/v3.3/` files
- Zero `mock.patch` usage on gate functions or orchestration logic in v3.3-modified `tests/roadmap/` files
- Grep patterns and results documented in evidence
- Only allowed injection point is `_subprocess_factory`

**Validation:**
- Manual check: grep output shows zero prohibited matches
- Evidence: grep command output

**Dependencies:** All Phase 2-3 tasks
**Rollback:** N/A (audit only)

---

### T04.03 -- Review JSONL audit trail: confirm third-party verifiability properties

| Field | Value |
|---|---|
| Roadmap Item IDs | R-048 |
| Why | Confirm JSONL audit trail meets 4 third-party verifiability properties per FR-7.2: real timestamps, spec-traced, runtime observations, explicit verdicts (SC-12) |
| Effort | S |
| Risk | Low |
| Risk Drivers | audit |
| Tier | EXEMPT |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0047 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0047/spec.md`

**Deliverables:**
- Manual review report: JSONL audit trail verifiability assessment against FR-7.2 properties (real timestamps, spec-traced, runtime observations, explicit verdicts)

**Steps:**
1. **[PLANNING]** Collect JSONL output from full test suite run (T04.01)
2. **[EXECUTION]** Verify property 1: all records have real ISO-8601 timestamps (not mocked/hardcoded)
3. **[EXECUTION]** Verify property 2: all records have `spec_ref` tracing to FR-/SC- identifiers
4. **[EXECUTION]** Verify property 3: `observed` fields contain runtime data (not template/placeholder)
5. **[EXECUTION]** Verify property 4: `verdict` fields are explicit PASS/FAIL/SKIP (no empty/null)
6. **[VERIFICATION]** Document any records failing any property
7. **[COMPLETION]** Record review findings in evidence

**Acceptance Criteria:**
- All JSONL records reviewed against 4 verifiability properties
- All records have real timestamps, spec traces, runtime observations, and explicit verdicts
- Review findings documented with specific examples of compliance
- Any exceptions documented and justified

**Validation:**
- Manual check: JSONL records pass 4-property verification
- Evidence: review report with sample records

**Dependencies:** T04.01
**Rollback:** N/A (review only)

---

### T04.04 -- Validate wiring manifest completeness

| Field | Value |
|---|---|
| Roadmap Item IDs | R-049 |
| Why | Verify every known wiring point from FR-1 has a manifest entry (NFR-5) |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0048 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0048/spec.md`

**Deliverables:**
- Manifest completeness report: every FR-1 wiring point has a corresponding manifest entry

**Steps:**
1. **[PLANNING]** Enumerate all FR-1 wiring points from spec (FR-1.1 through FR-1.21)
2. **[EXECUTION]** Cross-reference each FR-1 wiring point against `tests/v3.3/wiring_manifest.yaml` entries
3. **[EXECUTION]** Identify any missing manifest entries
4. **[VERIFICATION]** Assert all FR-1 wiring points have manifest entries
5. **[COMPLETION]** Record completeness report

**Acceptance Criteria:**
- Every FR-1 wiring point (FR-1.1 through FR-1.21) has at least one manifest entry
- Manifest entries reference correct module paths and function names
- Any gaps identified and documented
- Completeness percentage reported

**Validation:**
- Manual check: FR-1 -> manifest entry cross-reference table complete
- Evidence: completeness report

**Dependencies:** T01.07, Phase 2 complete
**Rollback:** N/A (validation only)

---

### T04.05 -- Generate final wiring-verification artifact

| Field | Value |
|---|---|
| Roadmap Item IDs | R-050 |
| Why | Final wiring-verification artifact for release evidence package (FR-6.1 T14) |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0049 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0049/spec.md`

**Deliverables:**
- Final wiring-verification artifact in `docs/generated/` reflecting complete v3.3 validation results

**Steps:**
1. **[PLANNING]** Collect all validation results from Phases 1-3
2. **[EXECUTION]** Generate final artifact incorporating: test results, reachability analysis, fidelity checker output, audit trail summary
3. **[EXECUTION]** Ensure artifact is self-contained and reviewable without tribal knowledge
4. **[VERIFICATION]** Review artifact for completeness
5. **[COMPLETION]** Record artifact path

**Acceptance Criteria:**
- Final artifact exists in `docs/generated/`
- Artifact incorporates test results, reachability analysis, fidelity checker output, and audit trail summary
- Artifact is self-contained and reviewable without tribal knowledge
- Artifact reflects complete v3.3 validation state

**Validation:**
- Manual check: artifact exists, is non-empty, and covers all validation domains
- Evidence: artifact file path

**Dependencies:** T04.01 through T04.04
**Rollback:** N/A (artifact generation)

---

### Checkpoint: Phase 4 / Tasks T04.01-T04.05

**Purpose:** Verify all validation and audit tasks complete before final documentation.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P04-T01-T05.md`
**Verification:**
- Full suite >= 4894 passed, <= 3 pre-existing, 0 new regressions
- Zero mock.patch on gate functions in v3.3 tests
- JSONL audit trail passes 4-property verification

**Exit Criteria:**
- SC-4 (regression baseline) validated
- SC-12 (audit trail verifiable) validated
- Wiring manifest 100% complete for FR-1 wiring points

---

### T04.06 -- Update solutions_learned.jsonl with v3.3 patterns

| Field | Value |
|---|---|
| Roadmap Item IDs | R-051 |
| Why | Capture v3.3 development patterns and solutions for cross-session learning |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0050 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0050/spec.md`

**Deliverables:**
- Updated `docs/memory/solutions_learned.jsonl` with v3.3 patterns: audit trail infrastructure, AST reachability analysis, fidelity checking, budget exhaustion handling

**Steps:**
1. **[PLANNING]** Identify key patterns and solutions from v3.3 development
2. **[EXECUTION]** Append v3.3 entries to `docs/memory/solutions_learned.jsonl`: audit trail JSONL pattern, AST reachability analysis approach, fidelity checker exact-match strategy, budget exhaustion graceful handling
3. **[VERIFICATION]** Verify JSONL is valid (parseable line-by-line)
4. **[COMPLETION]** Record entry count

**Acceptance Criteria:**
- `docs/memory/solutions_learned.jsonl` updated with v3.3 pattern entries
- Entries cover: audit trail, AST reachability, fidelity checking, budget exhaustion
- JSONL is valid and parseable
- Entries include context and rationale (not just pattern names)

**Validation:**
- Manual check: JSONL file parseable with new v3.3 entries
- Evidence: entry count before and after

**Dependencies:** T04.05
**Rollback:** Remove v3.3 entries from JSONL

---

### Checkpoint: End of Phase 4

**Purpose:** Release gate — confirm zero regressions, complete audit trail, all 12 success criteria green, and evidence package reviewable without tribal knowledge.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P04-END.md`
**Verification:**
- Full suite >= 4894 passed, <= 3 pre-existing, 0 new regressions (SC-4)
- All 12 success criteria (SC-1 through SC-12) validated with evidence
- Evidence package is self-contained and third-party reviewable

**Exit Criteria:**
- All success criteria pass: SC-1 (>=20 wiring tests), SC-2 (4/4 paths), SC-3 (8+ modes), SC-4 (regression baseline), SC-5 (KPI values), SC-6 (4/4 budget), SC-7 (eval catches bad), SC-8 (QA gaps), SC-9 (reachability gate), SC-10 (0-files FAIL), SC-11 (fidelity gap), SC-12 (audit verifiable)
- Wiring-verification artifact generated in `docs/generated/`
- `solutions_learned.jsonl` updated with v3.3 patterns
