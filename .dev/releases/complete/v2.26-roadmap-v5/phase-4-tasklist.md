# Phase 4 -- Resume Logic and Recovery

Implement resume freshness detection, remediation budget enforcement, and retire the spec-patch auto-resume cycle. This is the highest regression-risk phase per the roadmap. Modifies `executor.py` for freshness checks, budget enforcement, terminal halt, and spec-patch retirement.

### T04.01 -- Implement _check_annotate_deviations_freshness() in executor.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-055, R-056 |
| Why | FR-071: stale spec-deviations.md must never be reused; freshness check compares roadmap_hash and resets downstream gates on mismatch |
| Effort | L |
| Risk | High |
| Risk Drivers | Security (hash validation), data (state corruption), system-wide (resume flow) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0029 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0029/spec.md`

**Deliverables:**
1. `_check_annotate_deviations_freshness()` function in `executor.py`: compares `roadmap_hash` in `spec-deviations.md` against current SHA-256 of `roadmap.md`, fail-closed on missing file/field/read error, re-adds `annotate-deviations` to execution queue on mismatch, resets gate-pass state for `spec-fidelity` and `deviation-analysis` (FR-084)
2. Integration of freshness check into `_apply_resume()` before skipping `annotate-deviations` (FR-071)

**Steps:**
1. **[PLANNING]** Read `_apply_resume()` logic in `executor.py` to identify integration point
2. **[PLANNING]** Review all 9 test cases from SC-8 in the roadmap
3. **[EXECUTION]** Implement `_check_annotate_deviations_freshness()`: read `spec-deviations.md` frontmatter, extract `roadmap_hash`, compare against `hashlib.sha256(roadmap_content).hexdigest()`
4. **[EXECUTION]** Implement fail-closed behavior: missing file -> False, missing field -> False, read error -> False; log specific failure reason for each case
5. **[EXECUTION]** On False: re-add `annotate-deviations` to execution queue; reset `spec-fidelity` and `deviation-analysis` gate-pass state
6. **[EXECUTION]** Integrate freshness check into `_apply_resume()` before skipping `annotate-deviations`
7. **[VERIFICATION]** Run all 9 SC-8 test cases: matching hash, mismatched hash, missing file, missing field, read error, empty file, corrupt frontmatter, missing roadmap.md, None hash
8. **[COMPLETION]** Document implementation and test results in `D-0029/spec.md`

**Acceptance Criteria:**
- `_check_annotate_deviations_freshness()` passes all 9 SC-8 test cases
- Freshness failure reason logged explicitly before returning False (not just "failed")
- Mismatch triggers re-run of `annotate-deviations` + resets `spec-fidelity` and `deviation-analysis` gate-pass state
- `uv run pytest tests/sprint/test_executor.py -v -k "freshness"` exits 0 with all 9 test cases passing

**Validation:**
- `uv run pytest tests/sprint/test_executor.py -v -k "freshness"` exits 0 with 9 test cases
- Evidence: linkable artifact produced at `D-0029/spec.md`

**Dependencies:** T03.07 (roadmap_hash injection must exist), T03.11 (Phase 3 exit)
**Rollback:** Remove freshness check function and _apply_resume() integration

---

### T04.02 -- Add remediation_attempts Counter to .roadmap-state.json

| Field | Value |
|---|---|
| Roadmap Item IDs | R-057, R-063 |
| Why | FR-039: remediation budget requires persistent counter; existing state files without field must default to 0 gracefully |
| Effort | M |
| Risk | Medium |
| Risk Drivers | Schema (state file), migration (backward compatibility) |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0030 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0030/spec.md`

**Deliverables:**
1. `remediation_attempts` field added to `.roadmap-state.json` schema with default value 0 and backward compatibility for existing state files

**Steps:**
1. **[PLANNING]** Read current `.roadmap-state.json` schema and serialization/deserialization logic
2. **[PLANNING]** Identify all state file readers to update for backward compatibility
3. **[EXECUTION]** Add `remediation_attempts` field to state schema with default 0
4. **[EXECUTION]** Ensure existing `.roadmap-state.json` without `remediation_attempts` defaults to 0 gracefully
5. **[VERIFICATION]** Test: new state file has `remediation_attempts: 0`; old state file without field reads as 0
6. **[VERIFICATION]** Test: `remediation_attempts` persists across save/load cycles
7. **[COMPLETION]** Document schema change in `D-0030/spec.md`

**Acceptance Criteria:**
- New `.roadmap-state.json` files include `remediation_attempts` field
- Existing state files without `remediation_attempts` default to 0 without error
- Field persists across save/load cycles with correct integer value
- Note: coercion of `remediation_attempts` to int on read is completed in T04.05; T04.02 is not independently shippable without T04.05 coercion hardening
- `uv run pytest tests/sprint/test_executor.py -v -k "state"` exits 0

**Validation:**
- `uv run pytest tests/sprint/test_executor.py -v -k "state"` exits 0
- Evidence: linkable artifact produced at `D-0030/spec.md`

**Dependencies:** T03.11 (Phase 3 exit)
**Rollback:** Remove `remediation_attempts` from state schema

---

### T04.03 -- Implement _check_remediation_budget() in executor.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-058, R-060 |
| Why | FR-040/FR-041: max 2 remediation attempts; budget exhaustion triggers terminal halt; must not call sys.exit(1) directly (Constraint #12) |
| Effort | M |
| Risk | Medium |
| Risk Drivers | System-wide (exit behavior), security (budget enforcement) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0031 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0031/spec.md`

**Deliverables:**
1. `_check_remediation_budget()` function in `executor.py`: coerces `remediation_attempts` to int (FR-072, WARNING on failure, treat as 0), max 2 attempts (configurable via `max_attempts`), calls `_print_terminal_halt()` on exhaustion and returns False, does NOT call `sys.exit(1)` directly
2. Caller logic: on third `--resume` attempt (budget exhausted), caller calls `sys.exit(1)` (FR-044)

**Steps:**
1. **[PLANNING]** Review Constraint #12 from roadmap: callers own exit
2. **[PLANNING]** Review coercion requirements from FR-072
3. **[EXECUTION]** Implement `_check_remediation_budget()` with `max_attempts` parameter (default 2)
4. **[EXECUTION]** Add coercion: non-integer `remediation_attempts` logged as WARNING, treated as 0
5. **[EXECUTION]** On budget exhaustion: call `_print_terminal_halt()` and return False
6. **[EXECUTION]** Implement caller logic: on False return from budget check, call `sys.exit(1)`
7. **[VERIFICATION]** Test: attempts 1 and 2 return True; attempt 3 returns False and calls _print_terminal_halt()
8. **[COMPLETION]** Document implementation in `D-0031/spec.md`

**Acceptance Criteria:**
- `_check_remediation_budget()` caps at 2 attempts; third attempt triggers terminal halt
- Non-integer `remediation_attempts` treated as 0 with WARNING log
- Function returns False on budget exhaustion (does NOT call sys.exit directly)
- Caller invokes `sys.exit(1)` when budget check returns False
- Configurable `max_attempts` verified: `max_attempts=1` triggers halt on second attempt; `max_attempts=3` allows third attempt

**Validation:**
- `uv run pytest tests/sprint/test_executor.py -v -k "budget"` exits 0
- Evidence: linkable artifact produced at `D-0031/spec.md`

**Dependencies:** T04.02 (remediation_attempts counter exists)
**Rollback:** Remove `_check_remediation_budget()` and caller logic

---

### T04.04 -- Implement _print_terminal_halt() in executor.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-059 |
| Why | FR-042: terminal halt message must output to stderr with attempt count, failing findings, per-finding details, and manual-fix instructions |
| Effort | M |
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
| Deliverable IDs | D-0032 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0032/spec.md`

**Deliverables:**
1. `_print_terminal_halt()` function in `executor.py`: outputs to stderr with attempt count, remaining failing finding count, per-finding details, manual-fix instructions with certification report path and resume command. Function signature and output structure must accommodate FR-077 dual-budget-exhaustion note (implemented in T04.07)

**Steps:**
1. **[PLANNING]** Review FR-042 requirements for stderr content
2. **[PLANNING]** Identify certification report path and resume command format
3. **[EXECUTION]** Implement `_print_terminal_halt()` outputting to stderr
4. **[EXECUTION]** Include: attempt count, remaining failing finding count, per-finding details
5. **[EXECUTION]** Include: manual-fix instructions with certification report path and resume command
6. **[VERIFICATION]** Stderr content assertions in unit tests (not just implementation check)
7. **[COMPLETION]** Document implementation in `D-0032/spec.md`

**Acceptance Criteria:**
- `_print_terminal_halt()` writes to stderr (not stdout)
- Output includes: attempt count, remaining failing finding count, per-finding details
- Output includes: manual-fix instructions with certification report path and resume command
- Stderr content verified by unit test assertions

**Validation:**
- `uv run pytest tests/sprint/test_executor.py -v -k "terminal_halt"` exits 0 with stderr assertions
- Evidence: linkable artifact produced at `D-0032/spec.md`

**Dependencies:** T04.03 (_check_remediation_budget calls this function)
**Rollback:** Remove `_print_terminal_halt()` function

---

### T04.05 -- Implement Atomic State Writes and Coercion

| Field | Value |
|---|---|
| Roadmap Item IDs | R-061, R-062 |
| Why | NFR-022: .roadmap-state.json must use atomic writes; NFR-017: _save_state() must coerce existing_attempts to int before incrementing |
| Effort | M |
| Risk | Medium |
| Risk Drivers | Data (state corruption), schema (coercion) |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0033 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0033/spec.md`

**Deliverables:**
1. Atomic state writes for `.roadmap-state.json` using `.tmp` + `os.replace()` pattern (NFR-022)
2. `_save_state()` coerces `existing_attempts` to `int` before incrementing (NFR-017)

**Steps:**
1. **[PLANNING]** Read current `_save_state()` implementation
2. **[PLANNING]** Review atomic write pattern requirements
3. **[EXECUTION]** Modify `.roadmap-state.json` writes to use `.tmp` + `os.replace()` pattern
4. **[EXECUTION]** Add int coercion for `existing_attempts` in `_save_state()` before incrementing
5. **[VERIFICATION]** Test: atomic write creates `.tmp` file then replaces
6. **[VERIFICATION]** Test: string "2" coerced to int 2 before increment; non-numeric treated as 0 with WARNING
7. **[COMPLETION]** Document implementation in `D-0033/spec.md`

**Acceptance Criteria:**
- `.roadmap-state.json` writes use `.tmp` + `os.replace()` pattern (no partial write risk)
- `_save_state()` coerces string attempt values to int before incrementing
- Non-numeric coercion failure logged as WARNING and treated as 0
- `uv run pytest tests/sprint/test_executor.py -v -k "state"` exits 0

**Validation:**
- `uv run pytest tests/sprint/test_executor.py -v -k "state"` exits 0
- Evidence: linkable artifact produced at `D-0033/spec.md`

**Dependencies:** T04.02 (remediation_attempts field exists)
**Rollback:** Revert atomic write and coercion changes in `_save_state()`

---

### Checkpoint: Phase 4 / Tasks 1-5

**Purpose:** Verify freshness detection, budget enforcement, terminal halt, and atomic writes are implemented.
**Checkpoint Report Path:** `.dev/releases/current/v2.26-roadmap-v5/checkpoints/CP-P04-T01-T05.md`
**Verification:**
- `_check_annotate_deviations_freshness()` passes all 9 SC-8 test cases
- `_check_remediation_budget()` caps at 2 attempts correctly
- `_print_terminal_halt()` stderr content verified by unit tests
**Exit Criteria:**
- `uv run pytest tests/sprint/test_executor.py -v` exits 0
- D-0029 through D-0033 artifacts exist and are non-empty
- No state corruption detected in save/load cycle tests

---

### T04.06 -- Retire _apply_resume_after_spec_patch() as Dormant

| Field | Value |
|---|---|
| Roadmap Item IDs | R-064, R-065, R-066 |
| Why | FR-059: spec-patch cycle retired from active execution; NFR-019: retained as functionally dormant; FR-076: independent counters preserved |
| Effort | S |
| Risk | Medium |
| Risk Drivers | Breaking change (behavior removal) |
| Tier | STANDARD |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0034 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0034/evidence.md`

**Deliverables:**
1. `_apply_resume_after_spec_patch()` retired from active execution (FR-059) but retained as functionally dormant code (NFR-019); spec-patch and remediation budgets remain independent counters (FR-076)

**Steps:**
1. **[PLANNING]** Read `_apply_resume_after_spec_patch()` and `_spec_patch_cycle_count` in executor.py
2. **[PLANNING]** Identify all call sites that invoke spec-patch resume flow
3. **[EXECUTION]** Remove active invocations of `_apply_resume_after_spec_patch()` from normal v2.26 execution flow
4. **[EXECUTION]** Retain function definition and `_spec_patch_cycle_count` as dormant code (do not delete)
5. **[EXECUTION]** Verify spec-patch and remediation budget counters remain independent
6. **[VERIFICATION]** Confirm `_apply_resume_after_spec_patch()` is never invoked in normal v2.26 execution
7. **[COMPLETION]** Document retirement in `D-0034/evidence.md`

**Acceptance Criteria:**
- `_apply_resume_after_spec_patch()` code retained in `executor.py` but never invoked in normal v2.26 flow
- `_spec_patch_cycle_count` retained as dormant
- Spec-patch and remediation budgets are independent counters (not shared)
- `uv run pytest tests/sprint/ -v` exits 0 confirming no regressions

**Validation:**
- `uv run pytest tests/sprint/ -v` exits 0
- Evidence: linkable artifact produced at `D-0034/evidence.md`

**Dependencies:** T04.03 (new budget mechanism replaces old cycle)
**Rollback:** Re-enable spec-patch resume invocations

---

### T04.07 -- Add FR-077 Dual-Budget-Exhaustion Placeholder

| Field | Value |
|---|---|
| Roadmap Item IDs | R-067 |
| Why | FR-077: when both spec-patch and remediation budgets exhausted, _print_terminal_halt() must include note about both; mechanism deferred to v2.26 |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | LIGHT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0035 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0035/notes.md`

**Deliverables:**
1. Placeholder note in `_print_terminal_halt()` for dual-budget-exhaustion scenario, with v2.26 deferral comment

**Steps:**
1. **[PLANNING]** Review FR-077 and OQ-J resolution from T01.04
2. **[PLANNING]** Identify where in `_print_terminal_halt()` to add dual-budget note
3. **[EXECUTION]** Add conditional note in `_print_terminal_halt()` when both budgets exhausted
4. **[EXECUTION]** Add code comment referencing v2.26 deferral for full mechanism
5. **[VERIFICATION]** Quick check: dual-budget note appears in terminal halt output when both exhausted
6. **[COMPLETION]** Document placeholder in `D-0035/notes.md`

**Acceptance Criteria:**
- `_print_terminal_halt()` includes dual-budget note when both mechanisms exhausted
- Code comment references v2.26 for full dual-budget mechanism
- No functional dual-budget enforcement logic implemented (placeholder only)
- Placeholder does not interfere with normal single-budget terminal halt

**Validation:**
- Manual check: Dual-budget note visible in terminal halt output for dual-exhaustion scenario
- Evidence: linkable artifact produced at `D-0035/notes.md`

**Dependencies:** T04.04 (_print_terminal_halt exists), T04.06 (spec-patch budget context)
**Rollback:** Remove dual-budget note from `_print_terminal_halt()`

---

### T04.08 -- Validate Phase 4 Exit Criteria

| Field | Value |
|---|---|
| Roadmap Item IDs | R-068 |
| Why | Gate check: all Phase 3 (roadmap) exit criteria verified before proceeding to Phase 5 |
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
| Deliverable IDs | D-0036 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0036/evidence.md`

**Deliverables:**
1. Phase 4 exit criteria checklist with all 10 criteria verified

**Steps:**
1. **[PLANNING]** Load Phase 3 (roadmap) exit criteria from roadmap (10 checkboxes)
2. **[PLANNING]** Gather test results and artifact evidence from T04.01-T04.07
3. **[EXECUTION]** Verify freshness check passes all 9 SC-8 test cases
4. **[EXECUTION]** Verify remediation budget caps at 2 with terminal halt on third attempt
5. **[EXECUTION]** Verify resume behavior across: fresh resume, stale hash, exhausted budget, malformed state
6. **[VERIFICATION]** Run `uv run pytest tests/sprint/ -v` to confirm full test suite passes
7. **[COMPLETION]** Write exit criteria verification to `D-0036/evidence.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0036/evidence.md` exists with all 10 exit criteria checked
- Integration tests for `deviations_to_findings()` completed against stable budget mechanism
- Resume behavior verified across 4 scenarios: fresh, stale hash, exhausted budget, malformed state
- `_print_terminal_halt()` stderr content covered by assertion-based unit tests (roadmap Phase 3 exit criterion)
- `_apply_resume_after_spec_patch()` retained but unreachable from normal v2.26 execution paths (roadmap Phase 3 exit criterion)
- Non-integer `remediation_attempts` coercion to 0 with WARNING verified (roadmap Phase 3 exit criterion)
- Phase 5 is unblocked

**Validation:**
- `uv run pytest tests/sprint/ -v` exits 0 with all tests passing
- Evidence: linkable artifact produced at `D-0036/evidence.md`

**Dependencies:** T04.07
**Rollback:** TBD (validation task; no code changes)

---

### Checkpoint: End of Phase 4

**Purpose:** Confirm all resume logic, recovery mechanisms, and spec-patch retirement are complete; Phase 5 (Negative Validation) can begin.
**Checkpoint Report Path:** `.dev/releases/current/v2.26-roadmap-v5/checkpoints/CP-P04-END.md`
**Verification:**
- `_check_annotate_deviations_freshness()` passes all 9 SC-8 test cases
- Remediation budget caps at 2 attempts; third triggers terminal halt with stderr assertions
- `_apply_resume_after_spec_patch()` retained but never invoked in normal v2.26 flow
**Exit Criteria:**
- `uv run pytest tests/sprint/ -v` exits 0 with no regressions
- All 10 Phase 3 (roadmap) exit criteria verified in D-0036
- D-0029 through D-0036 artifacts exist and are non-empty
