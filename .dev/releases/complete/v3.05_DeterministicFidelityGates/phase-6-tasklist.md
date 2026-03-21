# Phase 6 -- Remediation & Integration

Implement structured patch remediation, wire all components together, delete dead code, and verify all success criteria end-to-end. Exit when FR-9, FR-9.1, SC-3 pass (Gate E) and all SC-1 through SC-6 pass on real artifacts (Gate F).

### T06.01 -- Extend remediate_executor.py with Structured Patches and Diff-Size Guard (FR-9)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-049 |
| Why | Remediation must produce structured patches in MorphLLM-compatible format with per-patch diff-size guard at 30%. Partial rejection and per-file rollback replace the all-or-nothing approach. |
| Effort | L |
| Risk | High |
| Risk Drivers | breaking (diff threshold change 50->30%), data (patch schema), cross-cutting (feeds convergence loop) |
| Tier | STRICT |
| Confidence | [█████████░] 92% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0038, D-0039, D-0048 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0038/spec.md`
- `TASKLIST_ROOT/artifacts/D-0039/spec.md`
- `TASKLIST_ROOT/artifacts/D-0048/spec.md`

**Deliverables:**
1. Extended `remediate_executor.py` with `RemediationPatch` dataclass (target_file, finding_id, original_code, instruction, update_snippet, rationale); per-patch diff-size guard rejecting if `changed_lines / patch_original_lines > 30%`; `_DIFF_SIZE_THRESHOLD_PCT` changed from 50 to 30; `_check_diff_size()` retired and replaced by per-patch evaluation; partial rejection (valid patches applied even when others rejected); per-file rollback; sequential patch application per file
2. `fallback_apply()` deterministic text replacement using `original_code` as anchor (minimum 5 lines or 200 chars); used when ClaudeProcess fails
3. `check_morphllm_available()` probes MCP runtime; returns bool; future migration prep (not blocking for v3.05)

**Steps:**
1. **[PLANNING]** Review existing `remediate_executor.py` (563 lines): identify `_check_diff_size()`, `_handle_failure()`, `_DIFF_SIZE_THRESHOLD_PCT`
2. **[EXECUTION]** Define `RemediationPatch` dataclass with MorphLLM-compatible JSON schema
3. **[EXECUTION]** Change `_DIFF_SIZE_THRESHOLD_PCT` from 50 to 30; replace `_check_diff_size()` with per-patch evaluation
4. **[EXECUTION]** Implement partial rejection: valid patches applied even when others rejected; rejected patches logged with reason
5. **[EXECUTION]** Implement per-file rollback replacing all-or-nothing `_handle_failure()`; post-execution cross-file coherence check
6. **[EXECUTION]** Implement `fallback_apply()` with minimum anchor of 5 lines or 200 chars
7. **[EXECUTION]** Implement `check_morphllm_available()` MCP runtime probe
8. **[VERIFICATION]** Test per-patch guard, partial rejection, per-file rollback, fallback applicator
9. **[COMPLETION]** Document remediation changes in `TASKLIST_ROOT/artifacts/D-0038/spec.md`

**Acceptance Criteria:**
- `RemediationPatch` dataclass includes target_file, finding_id, original_code, instruction, update_snippet, rationale
- Per-patch diff-size guard: `changed_lines / patch_original_lines > 0.30` triggers rejection
- Partial rejection: valid patches applied even when others for same file rejected
- `fallback_apply()` uses `original_code` anchor (min 5 lines or 200 chars) for deterministic replacement
- Post-execution cross-file coherence check evaluates rollback of successful files when related files fail; existing snapshot/restore mechanism (create_snapshots/restore_from_snapshots/cleanup_snapshots) retained

**Validation:**
- `uv run pytest tests/roadmap/test_remediate_executor.py -v` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0038/spec.md` documents remediation changes

**Dependencies:** T03.01
**Rollback:** TBD

---

### T06.02 -- Implement --allow-regeneration Flag (FR-9.1)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-050 |
| Why | Explicit user consent for patches exceeding diff-size threshold. Binary flag prevents accidental over-permitting. |
| Effort | S |
| Risk | Low |
| Risk Drivers | none matched |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0040 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0040/evidence.md`

**Deliverables:**
1. `--allow-regeneration` Click `is_flag=True` option on `run` command; `allow_regeneration: bool = False` on `RoadmapConfig`; with flag: exceeding patches applied with WARNING (includes patch ID, actual ratio, threshold); without flag: exceeding patches rejected (FAILED)

**Steps:**
1. **[PLANNING]** Review existing `--allow-regeneration` CLI flag in `commands.py:89-94` (pre-existing)
2. **[EXECUTION]** Verify flag wires through to `RoadmapConfig.allow_regeneration`
3. **[EXECUTION]** Implement guard in remediation: check `config.allow_regeneration` when patch exceeds threshold
4. **[EXECUTION]** With flag: log WARNING including patch ID, actual ratio, threshold; proceed with application
5. **[VERIFICATION]** Test both paths: flag present -> WARNING + apply; flag absent -> reject (FAILED)
6. **[COMPLETION]** Document flag behavior in `TASKLIST_ROOT/artifacts/D-0040/evidence.md`

**Acceptance Criteria:**
- `--allow-regeneration` is a Click `is_flag=True` option on the `run` command (pre-existing in commands.py)
- Config field `allow_regeneration` defaults to `False`
- Without flag: patches exceeding 30% threshold rejected with FAILED status
- With flag: patches exceeding 30% threshold applied with WARNING log (patch ID, ratio, threshold)

**Validation:**
- `uv run pytest tests/roadmap/test_remediate_executor.py -v -k "allow_regeneration"` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0040/evidence.md` documents flag behavior

**Dependencies:** T06.01
**Rollback:** TBD

---

### T06.03 -- Wire Pipeline Integration: Step 8 End-to-End (FR-7)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-051 |
| Why | All components must be wired together within step 8: structural checkers -> semantic layer -> convergence engine -> remediation. Steps 1-7 and step 9 must be unaffected. |
| Effort | M |
| Risk | High |
| Risk Drivers | cross-cutting (pipeline integration), breaking (step ordering) |
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
- `TASKLIST_ROOT/artifacts/D-0041/spec.md`

**Deliverables:**
1. Step 8 pipeline wiring: `execute_fidelity_with_convergence()` calls structural checkers, then semantic layer, then convergence evaluation, then `execute_remediation()` between runs; steps 1-7 and step 9 verified unaffected; wiring-verification bypass preserved

**Steps:**
1. **[PLANNING]** Map all component call chains within step 8
2. **[EXECUTION]** Wire structural checkers -> semantic layer -> registry update -> convergence gate evaluation
3. **[EXECUTION]** Wire convergence loop to call `execute_remediation()` between runs
4. **[EXECUTION]** Verify steps 1-7 produce identical output with convergence enabled
5. **[EXECUTION]** Verify step 9 receives `spec_fidelity_file` (decorative in convergence mode)
6. **[VERIFICATION]** Run full pipeline end-to-end in convergence mode; verify step ordering
7. **[COMPLETION]** Document integration in `TASKLIST_ROOT/artifacts/D-0041/spec.md`

**Acceptance Criteria:**
- Structural checkers -> semantic layer -> convergence engine -> remediation wired within step 8
- `execute_fidelity_with_convergence()` calls `execute_remediation()` between runs
- Steps 1-7 and step 9 are unaffected by `convergence_enabled=true` (NFR-7)
- Wiring-verification bypass preserved in convergence mode

**Validation:**
- `uv run pytest tests/roadmap/ -v` exits 0 (full roadmap test suite)
- Evidence: `TASKLIST_ROOT/artifacts/D-0041/spec.md` documents pipeline integration

**Dependencies:** T05.02, T05.03, T06.01
**Rollback:** TBD

---

### T06.04 -- Delete fidelity.py Dead Code

| Field | Value |
|---|---|
| Roadmap Item IDs | R-052 |
| Why | `fidelity.py` is 66 lines of dead code with zero imports. Removing it reduces confusion and maintenance burden. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | none matched |
| Tier | STANDARD |
| Confidence | [███████░░░] 78% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: none |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0042 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0042/evidence.md`

**Deliverables:**
1. `fidelity.py` deleted from `src/superclaude/cli/roadmap/`; zero remaining references confirmed via codebase grep

**Steps:**
1. **[PLANNING]** Confirm `fidelity.py` has zero imports (verified in T01.01)
2. **[EXECUTION]** Delete `src/superclaude/cli/roadmap/fidelity.py`
3. **[EXECUTION]** Grep entire codebase for references to `fidelity` module
4. **[VERIFICATION]** `uv run pytest` (full suite) passes after deletion
5. **[COMPLETION]** Document deletion in `TASKLIST_ROOT/artifacts/D-0042/evidence.md`

**Acceptance Criteria:**
- `src/superclaude/cli/roadmap/fidelity.py` no longer exists on disk
- Grep for `from.*fidelity import` and `import.*fidelity` returns zero results
- `uv run pytest` (full suite) passes after deletion
- No remaining references to the deleted module anywhere in codebase

**Validation:**
- `uv run pytest` exits 0 (full suite after deletion)
- Evidence: `TASKLIST_ROOT/artifacts/D-0042/evidence.md` documents grep results

**Dependencies:** None (can be done anytime; zero imports confirmed)
**Rollback:** `git checkout src/superclaude/cli/roadmap/fidelity.py`

---

### Checkpoint: Phase 6 / Tasks T06.01-T06.04

**Purpose:** Verify remediation and pipeline integration before end-to-end success criteria verification.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P06-T01-T04.md`
**Verification:**
- Remediation produces valid `RemediationPatch` objects with diff-size guard enforced
- `--allow-regeneration` overrides guard with warning
- Pipeline wiring complete: structural -> semantic -> convergence -> remediation
**Exit Criteria:**
- `fidelity.py` deleted with zero remaining references
- Steps 1-7 and step 9 unaffected by convergence mode
- Per-file rollback works correctly on test scenarios

---

### T06.05 -- SC-1 End-to-End: Deterministic Structural Findings

| Field | Value |
|---|---|
| Roadmap Item IDs | R-053 |
| Why | SC-1 is the core determinism guarantee. Must be verified end-to-end on real artifacts, not just unit-level. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | cross-cutting (system-wide determinism property) |
| Tier | STRICT |
| Confidence | [████████░░] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0043 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0043/evidence.md`

**Deliverables:**
1. SC-1 E2E proof: run same spec+roadmap twice through full pipeline in convergence mode; diff structural findings -> zero differences

**Steps:**
1. **[PLANNING]** Prepare real spec + roadmap pair for determinism test
2. **[EXECUTION]** Run full pipeline in convergence mode on the pair, capture structural findings
3. **[EXECUTION]** Run full pipeline again on identical inputs, capture structural findings
4. **[EXECUTION]** Diff both outputs: verify byte-identical structural findings
5. **[VERIFICATION]** SC-1 passes: zero differences in structural findings
6. **[COMPLETION]** Write SC-1 proof to `TASKLIST_ROOT/artifacts/D-0043/evidence.md`

**Acceptance Criteria:**
- Two sequential pipeline runs on identical inputs produce byte-identical structural findings
- Diff output shows zero differences (included in evidence document)
- NFR-1 (determinism) verified at E2E level, not just unit level
- Evidence document includes full diff command and output

**Validation:**
- Manual check: `diff` command on two outputs shows zero differences
- Evidence: `TASKLIST_ROOT/artifacts/D-0043/evidence.md` with diff output

**Dependencies:** T06.03
**Rollback:** TBD

---

### T06.06 -- SC-2, SC-3, SC-5 End-to-End Verification

| Field | Value |
|---|---|
| Roadmap Item IDs | R-053 |
| Why | Convergence budget (SC-2), edit preservation (SC-3), and legacy backward compat (SC-5) must all pass on real artifacts for release. |
| Effort | L |
| Risk | High |
| Risk Drivers | cross-cutting (3 success criteria), dependency (requires full pipeline) |
| Tier | STRICT |
| Confidence | [████████░░] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0044 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0044/evidence.md`

**Deliverables:**
1. SC-2: pipeline terminates within <=3 runs or halts with diagnostic; TurnLedger never negative at halt. SC-3: run remediation, verify FIXED findings remain FIXED in subsequent run. SC-5: legacy mode (`convergence_enabled=false`) on baseline spec produces byte-identical output to commit `f4d9035`

**Steps:**
1. **[PLANNING]** Design test scenarios for each SC criterion
2. **[EXECUTION]** SC-2: run convergence on test cases; verify <=3 runs; verify ledger state at halt
3. **[EXECUTION]** SC-3: seed findings, run remediation, run again; verify FIXED findings stay FIXED
4. **[EXECUTION]** SC-5: run legacy mode on baseline spec; diff against commit `f4d9035` output
5. **[VERIFICATION]** All 3 criteria pass
6. **[COMPLETION]** Write E2E results to `TASKLIST_ROOT/artifacts/D-0044/evidence.md`

**Acceptance Criteria:**
- SC-2: convergence terminates within <=3 runs on all test cases; TurnLedger budget never negative at halt
- SC-3: FIXED findings remain FIXED after remediation in subsequent pipeline run
- SC-5: legacy mode output byte-identical to commit `f4d9035` output
- Evidence document covers all 3 criteria with specific test results

**Validation:**
- `uv run pytest tests/roadmap/ -v -k "sc2 or sc3 or sc5 or legacy_compat"` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0044/evidence.md` documents all 3 SC results

**Dependencies:** T06.03, T06.01
**Rollback:** TBD

---

### T06.07 -- SC-4 and SC-6 End-to-End Verification

| Field | Value |
|---|---|
| Roadmap Item IDs | R-053 |
| Why | SC-4 (>=70% structural) and SC-6 (no prompt >30,720 bytes) must be verified on real artifacts. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | performance (prompt size) |
| Tier | STANDARD |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0045 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0045/evidence.md`

**Deliverables:**
1. SC-4: >=70% findings from structural rules (verified on real spec). SC-6: no semantic prompt exceeds 30,720 bytes (assert before every LLM call). NFR-4: checkers share no mutable state (parallel execution test). NFR-7: steps 1-7 unchanged integration test.

**Steps:**
1. **[EXECUTION]** SC-4: run full pipeline, count structural vs total findings, verify ratio >= 0.70
2. **[EXECUTION]** SC-6: instrument semantic layer to log prompt sizes; verify all <= 30,720 bytes
3. **[EXECUTION]** NFR-4: run checkers in parallel; verify no shared state interference
4. **[EXECUTION]** NFR-7: run pipeline with `convergence_enabled=false`; verify steps 1-7 unchanged
5. **[VERIFICATION]** All criteria pass
6. **[COMPLETION]** Write results to `TASKLIST_ROOT/artifacts/D-0045/evidence.md`

**Acceptance Criteria:**
- SC-4: structural findings account for >= 70% of total findings on real spec
- SC-6: no semantic prompt exceeds 30,720 bytes (assertion fires before every LLM call)
- NFR-4: parallel checker execution produces identical output to sequential
- NFR-7: steps 1-7 produce identical output with `convergence_enabled=true` vs `false`

**Validation:**
- `uv run pytest tests/roadmap/ -v -k "sc4 or sc6 or nfr4 or nfr7"` exits 0
- Evidence: `TASKLIST_ROOT/artifacts/D-0045/evidence.md` documents all SC/NFR results

**Dependencies:** T06.03
**Rollback:** TBD

---

### T06.08 -- Document Open Question Resolutions (OQ-1, OQ-3, OQ-4, OQ-5, OQ-5b, OQ-6)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-053 |
| Why | Roadmap requires all open questions documented with decisions by end of Phase 6. |
| Effort | M |
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
| Deliverable IDs | D-0046 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0046/notes.md`

**Deliverables:**
1. OQ-1: FR-4.1 rubric threshold (0.15) calibration documented. OQ-3: ParseWarning handling decision (log-and-continue vs block) documented. OQ-4: TurnLedger constant calibration (CHECKER_COST, REMEDIATION_COST, etc.) rationale documented. OQ-5: Agent failure criteria for FR-8 regression validation documented. OQ-5b: FR-4.1 threshold calibration basis documented. OQ-6: Cross-file coherence check scope for FR-9 documented.

**Steps:**
1. **[PLANNING]** Compile all open questions from roadmap Section "Open-Question Risks"
2. **[EXECUTION]** OQ-1: analyze rubric threshold against real semantic findings; document calibration
3. **[EXECUTION]** OQ-2: decide ParseWarning policy (log-and-continue vs block); document
4. **[EXECUTION]** OQ-3: define agent failure criteria for FR-8 regression validation; document
5. **[EXECUTION]** OQ-4: document TurnLedger constant calibration (CHECKER_COST, REMEDIATION_COST, etc.)
6. **[EXECUTION]** OQ-5: define cross-file coherence check scope for FR-9; document
7. **[VERIFICATION]** All 5 OQs documented with clear decisions
8. **[COMPLETION]** Write decisions to `TASKLIST_ROOT/artifacts/D-0046/notes.md`

**Acceptance Criteria:**
- `TASKLIST_ROOT/artifacts/D-0046/notes.md` exists and documents all 6 open questions (OQ-1, OQ-3, OQ-4, OQ-5, OQ-5b, OQ-6) with decisions
- Each OQ entry includes: question, decision, rationale, affected requirement
- Decisions are concrete (not "TBD" or "to be determined")
- FR-4.1 threshold calibration includes data from real semantic findings if available

**Validation:**
- Manual check: all 6 OQs (OQ-1, OQ-3, OQ-4, OQ-5, OQ-5b, OQ-6) documented with non-TBD decisions
- Evidence: `TASKLIST_ROOT/artifacts/D-0046/notes.md` produced

**Dependencies:** T06.05, T06.06
**Rollback:** TBD

---

### Checkpoint: End of Phase 6

**Purpose:** Gate E (Remediation Safety Certified) + Gate F (Release Readiness). All SC-1 through SC-6 pass on real artifacts.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P06-END.md`
**Verification:**
- All 6 success criteria (SC-1 through SC-6) pass on real artifacts
- All 7 non-functional requirements (NFR-1 through NFR-7) verified
- Remediation produces valid patches with diff-size guard enforced
**Exit Criteria:**
- `--allow-regeneration` overrides guard with warning (FR-9.1)
- Legacy mode regression test passes (SC-5)
- No orphaned temp directories, no git worktree artifacts
