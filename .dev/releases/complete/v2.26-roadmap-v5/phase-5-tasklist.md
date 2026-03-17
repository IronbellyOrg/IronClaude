# Phase 5 -- Negative Validation and Verification

Validate that only actionable slips are remediated and that all required refusal behaviors are verified with evidence. This phase treats negative validation as the primary correctness boundary — block release on evidence, not implementation confidence.

### T05.01 -- Verify Refuse Bogus Intentional Claims

| Field | Value |
|---|---|
| Roadmap Item IDs | R-069 |
| Why | INTENTIONAL_IMPROVEMENT without valid D-XX + round citation must be rejected and promoted to HIGH severity in spec-fidelity |
| Effort | M |
| Risk | Medium |
| Risk Drivers | Security (anti-laundering enforcement) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0037 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0037/evidence.md`

**Deliverables:**
1. Test evidence: INTENTIONAL_IMPROVEMENT annotation without valid D-XX + round citation is rejected; promoted to HIGH severity in spec-fidelity

**Steps:**
1. **[PLANNING]** Identify test fixtures needed: bogus intentional claims without valid citations
2. **[PLANNING]** Identify code path: annotate-deviations -> spec-fidelity -> HIGH promotion
3. **[EXECUTION]** Create test fixture: deviation annotated as INTENTIONAL_IMPROVEMENT without D-XX citation
4. **[EXECUTION]** Execute test: verify spec-fidelity promotes invalid annotation to HIGH severity
5. **[EXECUTION]** Execute test: verify the rejection is logged with specific reason
6. **[VERIFICATION]** Confirm negative test passes: bogus claims are rejected, not silently approved
7. **[COMPLETION]** Document test evidence in `D-0037/evidence.md`

**Acceptance Criteria:**
- Test fixture with bogus INTENTIONAL_IMPROVEMENT (no D-XX citation) causes HIGH severity in spec-fidelity output
- Invalid annotation rejection is logged with the specific missing citation
- Silent approval of bogus claims is impossible (fail-closed)
- Test fixture with D-XX present but missing round citation also causes HIGH severity in spec-fidelity output
- `uv run pytest tests/sprint/ -v -k "bogus_intentional or anti_laundering"` exits 0

**Validation:**
- `uv run pytest tests/sprint/ -v -k "bogus_intentional or anti_laundering"` exits 0
- Evidence: linkable artifact produced at `D-0037/evidence.md`

**Dependencies:** T04.08 (Phase 4 exit)
**Rollback:** TBD (test/verification task; no production code changes)

---

### T05.02 -- Verify Refuse Stale Deviation Artifacts

| Field | Value |
|---|---|
| Roadmap Item IDs | R-070 |
| Why | spec-deviations.md with roadmap_hash mismatch must never be reused; annotate-deviations must rerun |
| Effort | M |
| Risk | Medium |
| Risk Drivers | Security (stale data), data (hash mismatch) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0038 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0038/evidence.md`

**Deliverables:**
1. Test evidence: stale `spec-deviations.md` (roadmap_hash mismatch) triggers re-run of annotate-deviations

**Steps:**
1. **[PLANNING]** Create test fixture: spec-deviations.md with stale roadmap_hash
2. **[PLANNING]** Identify expected behavior: freshness check fails, annotate-deviations re-queued
3. **[EXECUTION]** Execute test with modified roadmap.md content (changed hash)
4. **[EXECUTION]** Verify annotate-deviations is re-added to execution queue
5. **[EXECUTION]** Verify spec-fidelity and deviation-analysis gate-pass states are reset
6. **[VERIFICATION]** Confirm stale artifact is never used for downstream processing
7. **[COMPLETION]** Document test evidence in `D-0038/evidence.md`

**Acceptance Criteria:**
- Stale `spec-deviations.md` (hash mismatch) triggers annotate-deviations re-run
- Downstream gates (`spec-fidelity`, `deviation-analysis`) reset on stale detection
- Stale artifact is never passed to downstream steps
- `uv run pytest tests/sprint/test_executor.py -v -k "stale or freshness"` exits 0

**Validation:**
- `uv run pytest tests/sprint/test_executor.py -v -k "stale or freshness"` exits 0
- Evidence: linkable artifact produced at `D-0038/evidence.md`

**Dependencies:** T04.01 (freshness check implemented)
**Rollback:** TBD (test/verification task)

---

### T05.03 -- Verify Refuse Ambiguous Continuation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-071 |
| Why | ambiguous_count > 0 must cause STRICT gate failure; pipeline halts with operator instructions for manual reclassification |
| Effort | M |
| Risk | Medium |
| Risk Drivers | Security (ambiguity enforcement) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0039 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0039/evidence.md`

**Deliverables:**
1. Test evidence: `ambiguous_count > 0` causes DEVIATION_ANALYSIS_GATE failure and pipeline halt with reclassification instructions

**Steps:**
1. **[PLANNING]** Create test fixture: deviation-analysis.md with `ambiguous_count: 1`
2. **[PLANNING]** Identify DEVIATION_ANALYSIS_GATE check: `_no_ambiguous_deviations()`
3. **[EXECUTION]** Execute test: verify STRICT gate failure when ambiguous_count > 0
4. **[EXECUTION]** Verify pipeline halts (does not continue past deviation-analysis)
5. **[EXECUTION]** Verify operator instructions for manual reclassification are output
6. **[VERIFICATION]** Confirm ambiguous deviations cannot silently pass through pipeline
7. **[COMPLETION]** Document test evidence in `D-0039/evidence.md`

**Acceptance Criteria:**
- `ambiguous_count > 0` causes `_no_ambiguous_deviations()` to return False
- DEVIATION_ANALYSIS_GATE (STRICT) fails, halting pipeline
- Operator receives instructions for manual reclassification
- `uv run pytest tests/sprint/ -v -k "ambiguous"` exits 0

**Validation:**
- `uv run pytest tests/sprint/ -v -k "ambiguous"` exits 0
- Evidence: linkable artifact produced at `D-0039/evidence.md`

**Dependencies:** T02.04 (_no_ambiguous_deviations implemented), T04.08 (Phase 4 exit)
**Rollback:** TBD (test/verification task)

---

### T05.04 -- Verify Refuse False Certification

| Field | Value |
|---|---|
| Roadmap Item IDs | R-072 |
| Why | certified: false must cause CERTIFY_GATE failure; pipeline does not advance past certification |
| Effort | M |
| Risk | Medium |
| Risk Drivers | Security (certification enforcement) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0040 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0040/evidence.md`

**Deliverables:**
1. Test evidence: `certified: false` causes CERTIFY_GATE failure with true/false/missing/malformed unit tests for `_certified_is_true()`

**Steps:**
1. **[PLANNING]** Identify `_certified_is_true()` function and CERTIFY_GATE check
2. **[PLANNING]** Prepare test cases: true, false, missing, malformed
3. **[EXECUTION]** Execute unit tests for `_certified_is_true()` with all 4 input variants
4. **[EXECUTION]** Execute integration test: certified: false causes CERTIFY_GATE failure
5. **[EXECUTION]** Verify pipeline does not advance past certification on failure
6. **[VERIFICATION]** Confirm SC-5 verified with explicit true/false/missing/malformed test results
7. **[COMPLETION]** Document test evidence in `D-0040/evidence.md`

**Acceptance Criteria:**
- `_certified_is_true()` returns True only for `certified: true`; returns False for false/missing/malformed
- `CERTIFY_GATE` fails when `certified: false`, blocking pipeline advancement
- SC-5 verified with all 4 input variants tested
- `uv run pytest tests/sprint/ -v -k "certified"` exits 0

**Validation:**
- `uv run pytest tests/sprint/ -v -k "certified"` exits 0
- Evidence: linkable artifact produced at `D-0040/evidence.md`

**Dependencies:** T02.04 (_certified_is_true implemented), T02.06 (CERTIFY_GATE modified)
**Rollback:** TBD (test/verification task)

---

### T05.05 -- Verify Refuse Third Remediation Attempt

| Field | Value |
|---|---|
| Roadmap Item IDs | R-073 |
| Why | Budget exhaustion after 2 attempts must trigger terminal halt with sys.exit(1); SC-6 verification |
| Effort | M |
| Risk | Medium |
| Risk Drivers | System-wide (exit behavior) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0041 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0041/evidence.md`

**Deliverables:**
1. Test evidence: third remediation attempt triggers terminal halt with `sys.exit(1)` and stderr content assertions (SC-6)

**Steps:**
1. **[PLANNING]** Create test fixture: state file with `remediation_attempts: 2`
2. **[PLANNING]** Identify expected behavior: budget exhaustion -> terminal halt -> sys.exit(1)
3. **[EXECUTION]** Execute integration test with mock failing certify
4. **[EXECUTION]** Verify `_print_terminal_halt()` called with correct parameters
5. **[EXECUTION]** Verify stderr contains attempt count, failing findings, manual-fix instructions
6. **[VERIFICATION]** Confirm SC-6: terminal halt after 2 failed remediations with stderr detail assertions
7. **[COMPLETION]** Document test evidence in `D-0041/evidence.md`

**Acceptance Criteria:**
- Third `--resume` attempt triggers `_print_terminal_halt()` and `sys.exit(1)`
- Stderr output includes: attempt count, remaining failing finding count, per-finding details, manual-fix instructions with certification report path and resume command
- SC-6 verified with failing-certify integration test including stderr assertion
- `uv run pytest tests/sprint/test_executor.py -v -k "terminal_halt or budget"` exits 0

**Validation:**
- `uv run pytest tests/sprint/test_executor.py -v -k "terminal_halt or budget"` exits 0
- Evidence: linkable artifact produced at `D-0041/evidence.md`

**Dependencies:** T04.03 (_check_remediation_budget), T04.04 (_print_terminal_halt)
**Rollback:** TBD (test/verification task)

---

### Checkpoint: Phase 5 / Tasks 1-5

**Purpose:** Verify all 5 refusal behaviors are verified with explicit test evidence.
**Checkpoint Report Path:** `.dev/releases/current/v2.26-roadmap-v5/checkpoints/CP-P05-T01-T05.md`
**Verification:**
- Bogus intentional claims rejected with HIGH severity
- Stale deviation artifacts trigger re-run
- Ambiguous continuation causes STRICT gate failure
**Exit Criteria:**
- D-0037 through D-0041 evidence artifacts exist and are non-empty
- All 5 refusal negative tests pass
- No refusal behavior has a silent-pass code path

---

### T05.06 -- Verify Certify Behavior Alignment

| Field | Value |
|---|---|
| Roadmap Item IDs | R-074 |
| Why | Ensure _certified_is_true() blocks certification on certified: false and manual-fix recovery path works |
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
| Deliverable IDs | D-0042 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0042/evidence.md`

**Deliverables:**
1. Verification that manual-fix recovery path works after repeated certification failure

**Steps:**
1. **[PLANNING]** Review certify-block-then-recover scenario
2. **[PLANNING]** Identify manual-fix recovery code path
3. **[EXECUTION]** Test: certification fails, manual fix applied, resume succeeds
4. **[EXECUTION]** Verify recovery path does not bypass any gate checks
5. **[VERIFICATION]** Confirm manual-fix recovery produces successful certification
6. **[COMPLETION]** Document verification in `D-0042/evidence.md`

**Acceptance Criteria:**
- `_certified_is_true()` blocks on `certified: false` (verified in T05.04)
- Manual-fix recovery path works: fix applied -> resume -> certification succeeds
- Recovery does not bypass gate checks
- `uv run pytest tests/sprint/ -v -k "certif"` exits 0

**Validation:**
- `uv run pytest tests/sprint/ -v -k "certif"` exits 0
- Evidence: linkable artifact produced at `D-0042/evidence.md`

**Dependencies:** T05.04 (certification refusal verified)
**Rollback:** TBD (verification task)

---

### T05.07 -- Verify Roadmap Diff for SLIP-Only Remediation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-075 |
| Why | SC-4: remediation must modify only SLIP-routed elements; no INTENTIONAL or PRE_APPROVED content modified |
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
| Deliverable IDs | D-0043 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0043/evidence.md`

**Deliverables:**
1. Before/after roadmap diff evidence showing changed sections map exclusively to SLIP-classified deviation IDs; no INTENTIONAL or PRE_APPROVED content modified

**Steps:**
1. **[PLANNING]** Identify test fixture with mixed deviations: SLIP + INTENTIONAL + PRE_APPROVED
2. **[PLANNING]** Plan diff comparison strategy
3. **[EXECUTION]** Run remediation on fixture with mixed deviation types
4. **[EXECUTION]** Generate before/after diff of `roadmap.md`
5. **[EXECUTION]** Verify changed sections map exclusively to SLIP-classified IDs
6. **[EXECUTION]** Verify no INTENTIONAL or PRE_APPROVED item content is modified
7. **[VERIFICATION]** Confirm SC-4 with diff-based evidence (not just test pass)
8. **[COMPLETION]** Document diff evidence in `D-0043/evidence.md`

**Acceptance Criteria:**
- Before/after roadmap diff shows changes only in SLIP-routed sections
- No INTENTIONAL or PRE_APPROVED content modified in diff
- SC-4 verified with before/after roadmap diff (not just test pass)
- Changed sections traceable to specific SLIP deviation IDs

**Validation:**
- Manual check: Before/after diff reviewed showing SLIP-only changes
- Evidence: linkable artifact produced at `D-0043/evidence.md`

**Dependencies:** T03.10 (remediation with deviation-class awareness)
**Rollback:** TBD (verification task)

---

### T05.08 -- Validate Phase 5 Exit Criteria

| Field | Value |
|---|---|
| Roadmap Item IDs | R-076 |
| Why | Gate check: all 5 refusal behaviors verified with explicit test or artifact reference; no prohibited file modifications |
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
| Deliverable IDs | D-0044 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0044/evidence.md`

**Deliverables:**
1. Phase 5 exit criteria checklist with all 5 criteria verified

**Steps:**
1. **[PLANNING]** Load Phase 4 (roadmap) exit criteria from roadmap (5 checkboxes)
2. **[PLANNING]** Gather evidence from T05.01-T05.07
3. **[EXECUTION]** Verify all 5 refusal behaviors have explicit test or artifact reference
4. **[EXECUTION]** Verify SC-4 with before/after roadmap diff
5. **[EXECUTION]** Verify no prohibited file modifications in generic pipeline layer
6. **[VERIFICATION]** Cross-check each criterion against evidence artifacts
7. **[COMPLETION]** Write exit criteria verification to `D-0044/evidence.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0044/evidence.md` exists with all 5 exit criteria checked
- All 5 refusal behaviors verified with explicit test or artifact reference
- SC-4 verified with before/after roadmap diff (not just test pass)
- SC-5 verified with explicit true/false/missing/malformed unit tests for `_certified_is_true()`
- SC-6 verified with failing-certify integration test including stderr assertion
- No prohibited file modifications in generic pipeline layer

**Validation:**
- Manual check: All 5 Phase 4 (roadmap) exit criteria verified with evidence references
- Evidence: linkable artifact produced at `D-0044/evidence.md`

**Dependencies:** T05.07
**Rollback:** TBD (validation task)

---

### Checkpoint: End of Phase 5

**Purpose:** Confirm all negative validation is complete; Phase 6 (Integration Testing) can begin.
**Checkpoint Report Path:** `.dev/releases/current/v2.26-roadmap-v5/checkpoints/CP-P05-END.md`
**Verification:**
- All 5 refusal behaviors verified with explicit test evidence
- SC-4 roadmap diff shows SLIP-only remediation
- No prohibited file modifications in generic pipeline layer
**Exit Criteria:**
- D-0037 through D-0044 evidence artifacts exist and are non-empty
- All Phase 4 (roadmap) exit criteria verified in D-0044
- `uv run pytest tests/sprint/ -v` exits 0 with no regressions
