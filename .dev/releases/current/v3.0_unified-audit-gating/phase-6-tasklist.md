# Phase 6 -- Audit Agent Extensions

Enrich the cleanup-audit agent suite with wiring-aware behavioral rules. All extensions are strictly additive: no existing tools changed, no existing rules removed. This phase achieves milestone M4: audit pipeline produces wiring path information in analyzer profiles and validates wiring claims.

### T06.01 -- Extend Audit-Scanner with REVIEW:wiring Signal in agents/audit-scanner.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-031 |
| Why | SC-011 requires the audit scanner to classify files with wiring indicators (injectable callables, registry patterns) using a new REVIEW:wiring signal |
| Effort | S |
| Risk | Medium |
| Risk Drivers | audit (agent behavioral spec change), compliance (SC-011, section 6.2) |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0027 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0027/spec.md

**Deliverables:**
- Updated `src/superclaude/agents/audit-scanner.md` with `REVIEW:wiring` classification signal for files containing `Optional[Callable]` parameters, registry patterns, or provider directory indicators

**Steps:**
1. **[PLANNING]** Read `src/superclaude/agents/audit-scanner.md` to understand existing classification signals and rule structure
2. **[PLANNING]** Read section 6.2 for REVIEW:wiring signal specification
3. **[EXECUTION]** Add `REVIEW:wiring` signal definition to the scanner's classification rules section
4. **[EXECUTION]** Define trigger conditions: file contains `Optional[Callable]`, matches registry patterns, or resides in provider directories
5. **[EXECUTION]** Ensure addition is strictly additive: no existing signals modified or removed per section 6.1
6. **[VERIFICATION]** Review diff to confirm only additive changes
7. **[COMPLETION]** Run `make sync-dev` to propagate changes to `.claude/agents/`

**Acceptance Criteria:**
- `REVIEW:wiring` signal is defined in `audit-scanner.md` with clear trigger conditions
- No existing classification signals are modified or removed (section 6.1 additive constraint)
- Scanner can classify `wiring_config.py`, `wiring_gate.py`, and `wiring_analyzer.py` as `REVIEW:wiring` candidates
- File diff shows only additions, no deletions of existing content

**Validation:**
- Manual check: diff of `audit-scanner.md` shows only additive changes with REVIEW:wiring signal defined
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0027/spec.md

**Dependencies:** Phase 2 (core engine provides wiring context for signal definition)
**Rollback:** Revert `audit-scanner.md` to pre-modification state

---

### T06.02 -- Extend Audit-Analyzer with 9th Field and Finding Types in agents/audit-analyzer.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-032 |
| Why | SC-012 requires the audit analyzer to produce 9-field per-file profiles (adding Wiring as the 9th field) with wiring-specific finding types |
| Effort | S |
| Risk | Medium |
| Risk Drivers | audit (agent behavioral spec change), compliance (SC-012, section 6.3) |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0028 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0028/spec.md

**Deliverables:**
- Updated `src/superclaude/agents/audit-analyzer.md` with 9th profile field "Wiring" and wiring-specific finding types (unwired-callable, orphan-module, broken-registry)

**Steps:**
1. **[PLANNING]** Read `src/superclaude/agents/audit-analyzer.md` to understand existing 8-field profile structure
2. **[PLANNING]** Read section 6.3 for 9th field specification and finding type definitions
3. **[EXECUTION]** Add "Wiring" as the 9th mandatory field in the per-file profile template
4. **[EXECUTION]** Define wiring-specific finding types: unwired-callable, orphan-module, broken-registry with severity mappings
5. **[EXECUTION]** Add instructions for populating the Wiring field from `run_wiring_analysis()` output
6. **[VERIFICATION]** Review diff to confirm only additive changes to the profile structure
7. **[COMPLETION]** Run `make sync-dev` to propagate changes to `.claude/agents/`

**Acceptance Criteria:**
- Audit analyzer profile template contains 9 fields with "Wiring" as the 9th field (SC-012)
- Three wiring finding types are defined: unwired-callable, orphan-module, broken-registry
- No existing 8 fields are modified or removed (section 6.1 additive constraint)
- Profile template instructions reference `run_wiring_analysis()` for data population

**Validation:**
- Manual check: diff of `audit-analyzer.md` shows 9th field addition with no existing field changes
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0028/spec.md

**Dependencies:** Phase 2 (core engine defines finding types)
**Rollback:** Revert `audit-analyzer.md` to pre-modification state

---

### T06.03 -- Extend Audit-Validator with Check 5 in agents/audit-validator.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-033 |
| Why | Section 6.4 requires the audit validator to perform a new Check 5 that catches DELETE recommendations on files with live wiring connections |
| Effort | S |
| Risk | Low |
| Risk Drivers | audit (agent behavioral spec change) |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0029 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0029/spec.md

**Deliverables:**
- Updated `src/superclaude/agents/audit-validator.md` with Check 5: "Validate that files recommended for DELETE do not have live wiring connections (inbound imports, registry references, injectable callables)"

**Steps:**
1. **[PLANNING]** Read `src/superclaude/agents/audit-validator.md` to understand existing check structure (Checks 1-4)
2. **[PLANNING]** Read section 6.4 for Check 5 specification
3. **[EXECUTION]** Add Check 5 definition with clear validation logic: if a file is recommended for DELETE, verify it has no live wiring connections
4. **[EXECUTION]** Define "live wiring connections" as: inbound imports from other modules, registry key references, or injectable callable consumers
5. **[VERIFICATION]** Review diff to confirm Check 5 is additive and Checks 1-4 are unchanged
6. **[COMPLETION]** Run `make sync-dev` to propagate changes to `.claude/agents/`

**Acceptance Criteria:**
- Check 5 is defined in `audit-validator.md` with clear validation criteria for DELETE recommendations
- Checks 1-4 are unmodified (section 6.1 additive constraint)
- Check 5 references wiring analysis output to determine live connections
- Validator catches DELETE recommendations on files with live wiring (prevents accidental removal of wired modules)

**Validation:**
- Manual check: diff of `audit-validator.md` shows only Check 5 addition with Checks 1-4 unchanged
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0029/spec.md

**Dependencies:** Phase 2 (core engine for wiring analysis context)
**Rollback:** Revert `audit-validator.md` to pre-modification state

---

### T06.04 -- Extend Audit-Comparator with Cross-File Wiring Check in agents/audit-comparator.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-034 |
| Why | G-007 requires the comparator to detect cross-file wiring inconsistencies during audit comparison passes |
| Effort | S |
| Risk | Medium |
| Risk Drivers | audit (agent behavioral spec change), compliance (G-007, section 6.1) |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0030 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0030/spec.md

**Deliverables:**
- Updated `src/superclaude/agents/audit-comparator.md` with cross-file wiring consistency check: verify that wiring claims in analyzer profiles are consistent across files (e.g., if file A claims to wire callable X, file X should show as wired)

**Steps:**
1. **[PLANNING]** Read `src/superclaude/agents/audit-comparator.md` to understand existing comparison checks
2. **[PLANNING]** Read section 6.1 for additive extension scope (OQ-5 decision: additive wiring sections only, no restructure)
3. **[EXECUTION]** Add wiring consistency check section: compare Wiring fields across file profiles for cross-referential integrity
4. **[EXECUTION]** Define inconsistency types: orphan claims (file says wired but no consumer found), phantom consumers (consumer references nonexistent provider)
5. **[VERIFICATION]** Review diff to confirm only additive changes per OQ-5 decision
6. **[COMPLETION]** Run `make sync-dev` to propagate changes to `.claude/agents/`

**Acceptance Criteria:**
- Cross-file wiring check is defined in `audit-comparator.md` as an additive section
- Check detects orphan claims and phantom consumers across file profiles
- Existing comparison checks are not modified or removed (section 6.1, OQ-5 additive-only scope)
- Check references the Wiring field added to analyzer profiles in T06.02

**Validation:**
- Manual check: diff of `audit-comparator.md` shows only additive wiring section
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0030/spec.md

**Dependencies:** T06.02 (analyzer 9th field defines data source)
**Rollback:** Revert `audit-comparator.md` to pre-modification state

---

### T06.05 -- Extend Audit-Consolidator with Wiring Health Section in agents/audit-consolidator.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-035 |
| Why | G-007 requires the consolidator to produce a Wiring Health summary section in final audit reports |
| Effort | S |
| Risk | Low |
| Risk Drivers | audit (agent behavioral spec change) |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0031 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0031/spec.md

**Deliverables:**
- Updated `src/superclaude/agents/audit-consolidator.md` with a "Wiring Health" section template for final audit reports, summarizing wiring findings aggregated across all analyzed files

**Steps:**
1. **[PLANNING]** Read `src/superclaude/agents/audit-consolidator.md` to understand existing report sections
2. **[PLANNING]** Read section 6.1 for consolidator extension scope (OQ-5: additive only)
3. **[EXECUTION]** Add "Wiring Health" section template with summary metrics: total wiring findings by type, suppressed count, health score
4. **[EXECUTION]** Define aggregation rules: collect Wiring fields from all analyzer profiles, merge with wiring gate report data
5. **[VERIFICATION]** Review diff to confirm only additive section addition
6. **[COMPLETION]** Run `make sync-dev` to propagate changes to `.claude/agents/`

**Acceptance Criteria:**
- "Wiring Health" section is defined in `audit-consolidator.md` as an additive report section
- Section template includes wiring finding counts by type (unwired, orphan, registry) and suppressed count
- Existing report sections are not modified or removed (section 6.1, OQ-5)
- Section references data from analyzer Wiring fields and wiring gate reports

**Validation:**
- Manual check: diff of `audit-consolidator.md` shows only additive Wiring Health section
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0031/spec.md

**Dependencies:** T06.02 (analyzer 9th field), T06.04 (comparator wiring data)
**Rollback:** Revert `audit-consolidator.md` to pre-modification state

---

### Checkpoint: Phase 6 / Tasks T06.01-T06.05

**Purpose:** Verify all 5 agent extensions are strictly additive before running regression tests.
**Checkpoint Report Path:** .dev/releases/current/v3.0_unified-audit-gating/checkpoints/CP-P06-T01-T05.md
**Verification:**
- All 5 agent spec diffs show only additions, no deletions of existing content
- Scanner defines REVIEW:wiring signal, Analyzer has 9th field, Validator has Check 5
- Comparator has cross-file wiring check, Consolidator has Wiring Health section
**Exit Criteria:**
- `make sync-dev` completes without errors for all 5 modified agent specs
- All diffs are additive-only per section 6.1 constraint
- Agent spec files pass basic markdown linting

---

### T06.06 -- Implement Agent Regression Tests with Prior-Output Comparison in tests/audit/

| Field | Value |
|---|---|
| Roadmap Item IDs | R-036, R-037 |
| Why | R7 mitigation requires staged independent validation per agent with regression tests against prior outputs to detect emergent LLM behavioral effects from spec changes |
| Effort | M |
| Risk | Medium |
| Risk Drivers | audit (regression risk R7), compliance (SC-011, SC-012) |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0032 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0032/evidence.md

**Deliverables:**
- Regression test suite in `tests/audit/` that validates each agent extension independently against prior audit outputs, confirming no regression in existing audit functionality

**Steps:**
1. **[PLANNING]** Capture baseline audit outputs from each agent before extensions were applied (or use existing test fixtures)
2. **[PLANNING]** Design regression test strategy per Haiku's staged validation approach (R7 mitigation)
3. **[EXECUTION]** Write tests validating scanner correctly classifies wiring-indicator files as REVIEW:wiring (SC-011)
4. **[EXECUTION]** Write tests validating analyzer produces complete 9-field profiles with Wiring path populated (SC-012)
5. **[EXECUTION]** Write tests validating validator catches DELETE recommendations on files with live wiring
6. **[EXECUTION]** Write tests validating comparator detects cross-file wiring inconsistencies
7. **[VERIFICATION]** Run `uv run pytest tests/audit/ -k "agent_regression" -v` and verify all regression tests pass
8. **[COMPLETION]** Record regression test results and baseline comparison in evidence artifact

**Acceptance Criteria:**
- `uv run pytest tests/audit/ -k "agent_regression" -v` exits 0 with regression tests for all 5 agents passing
- Scanner classifies wiring-indicator files correctly (SC-011)
- Analyzer produces complete 9-field profiles with Wiring path (SC-012)
- Validator catches DELETE recommendations on files with live wiring
- No regression in existing audit output quality compared to baseline

**Validation:**
- `uv run pytest tests/audit/ -k "agent_regression" -v` exits 0
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0032/evidence.md

**Dependencies:** T06.01, T06.02, T06.03, T06.04, T06.05
**Rollback:** Delete regression test files

---

### Checkpoint: End of Phase 6

**Purpose:** Validate milestone M4: audit pipeline produces wiring path information in analyzer profiles and validates wiring claims.
**Checkpoint Report Path:** .dev/releases/current/v3.0_unified-audit-gating/checkpoints/CP-P06-END.md
**Verification:**
- All 5 agent extensions are strictly additive (section 6.1: no tools changed, no rules removed)
- Scanner classifies wiring-indicator files correctly (SC-011)
- Analyzer produces complete 9-field profiles with Wiring path (SC-012)
**Exit Criteria:**
- Regression tests pass for all 5 agents confirming no behavioral degradation
- Validator catches DELETE recommendations on files with live wiring
- `make sync-dev` and `make verify-sync` both pass after all agent modifications
