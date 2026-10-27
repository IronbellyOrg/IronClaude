# Phase 11 -- Verification and Release Readiness

Prove the implementation satisfies all 14 explicit success criteria and recoverability expectations. Run automated tests, sample runs, and produce the release readiness checklist.

---

### T11.01 -- Unit Test Suite: Error Paths, Gates, Status, TurnLedger, Exit Codes

| Field | Value |
|---|---|
| Roadmap Item IDs | R-067 |
| Why | Unit tests for all 5 error paths, 12 gates, _determine_status(), TurnLedger budget, and exit codes provide the automated proof that the core invariants hold |
| Effort | XL |
| Risk | Low |
| Risk Drivers | None |
| Tier | STRICT |
| Confidence | [█████████░] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent quality-engineer 60s |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0063 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0063/evidence.md`

**Deliverables:**
- Passing unit test suite covering: all 5 validation error paths (NAME_COLLISION, OUTPUT_NOT_WRITABLE, AMBIGUOUS_PATH, INVALID_PATH, DERIVATION_FAILED), all 12 gates G-000–G-011 with passing and failing inputs, `_determine_status()` exhaustively (5 file-state matrix cases), `TurnLedger` budget tracking and exhaustion, exit code mapping (SC-014: exit 124 → TIMEOUT)

**Steps:**
1. **[PLANNING]** Enumerate all pre-existing test files in `tests/cli_portify/` that target these areas
2. **[EXECUTION]** For each of 5 error codes: ensure at least one test triggers the error via appropriate input
3. **[EXECUTION]** For each of 12 gates: ensure passing test (valid artifact) and failing test (invalid artifact) both exist and pass
4. **[EXECUTION]** For `_determine_status()`: test all 5 file-state matrix cases (absent file, stale file, empty file, fresh no marker, fresh with marker)
5. **[EXECUTION]** For TurnLedger: test `can_launch()` returns False when budget=0; test `record_turn()` decrements budget; test exhaustion → HALTED outcome
6. **[EXECUTION]** For exit codes: mock subprocess exit 124 → TIMEOUT (SC-014); mock exit 1 → ERROR; mock exit 0 → _determine_status() called
7. **[EXECUTION]** Run `uv run pytest tests/cli_portify/ -k "error_path or gates or determine_status or turn_ledger or exit_code" -v`
8. **[COMPLETION]** Document coverage in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0063/evidence.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "error_path or gate_ or determine_status or turn_ledger or exit_124" -v` exits 0
- All 5 error codes have triggering test cases
- All 12 gates have ≥2 test cases each (passing + failing)
- `_determine_status()` test matrix covers all 5 file-state cases
- SC-014: exit 124 → TIMEOUT verified by automated test

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -v --tb=short` — zero failures; coverage report produced
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0063/evidence.md` produced with test count

**Dependencies:** All Phase 2–10 implementations complete
**Rollback:** Remove failing tests; do not merge until all pass

---

### T11.02 -- Integration Test Suite: Dry-Run, Resume, Signal, Gate Retry

| Field | Value |
|---|---|
| Roadmap Item IDs | R-068 |
| Why | Integration tests verify the full pipeline machinery — not just individual units — behaving correctly across real step boundaries and state transitions |
| Effort | XL |
| Risk | Low |
| Risk Drivers | None |
| Tier | STRICT |
| Confidence | [█████████░] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent quality-engineer 60s |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0064 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0064/evidence.md`

**Deliverables:**
- Passing integration test suite covering: dry-run against real skill directory (no SYNTHESIS artifacts), resume across both review boundaries (phase1-approval + phase2-approval), SIGINT handling (INTERRUPTED + return-contract), gate failure + retry (missing EXIT_RECOMMENDATION → PASS_NO_SIGNAL → retry fires)

**Steps:**
1. **[PLANNING]** Identify a real skill directory in `src/superclaude/skills/` to use as integration test target
2. **[EXECUTION]** Implement `test_dry_run_real_skill()`: run with `--dry-run` against real skill; assert no `portify-release-spec.md` produced; assert `portify-config.yaml` and `component-inventory.yaml` produced (SC-012)
3. **[EXECUTION]** Implement `test_resume_phase1()`: run to phase1 pause; write `status: approved`; resume; assert Phase 2 steps skip Phase 1 re-execution (SC-007)
4. **[EXECUTION]** Implement `test_resume_phase2()`: run to phase2 pause; write `status: completed`; resume; assert Phase 3+ steps executed
5. **[EXECUTION]** Implement `test_sigint_handling()`: mock SIGINT mid-step; assert INTERRUPTED outcome; assert `return-contract.yaml` written with `outcome: INTERRUPTED`
6. **[EXECUTION]** Implement `test_gate_retry()`: mock Claude output missing EXIT_RECOMMENDATION; assert PASS_NO_SIGNAL status → retry triggered; second attempt succeeds → PASS
7. **[EXECUTION]** Run `uv run pytest tests/cli_portify/integration/ -v`
8. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0064/evidence.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/integration/ -v` exits 0
- Dry-run test produces zero SYNTHESIS artifacts (SC-012)
- Resume test confirms completed steps are not re-executed (SC-007)
- SIGINT test confirms `return-contract.yaml` contains `outcome: INTERRUPTED` (SC-011)
- Gate retry test confirms PASS_NO_SIGNAL → retry → PASS flow

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/integration/ -v --tb=short` exits 0
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0064/evidence.md` produced

**Dependencies:** T10.01 (commands), T10.03 (main.py registration), all Phase 3–9 implementations
**Rollback:** Remove failing integration tests; investigate root cause before retrying

---

### T11.03 -- Edge Case Tests: Ambiguous, Collision, Budget, Escalated, >120KB

| Field | Value |
|---|---|
| Roadmap Item IDs | R-069 |
| Why | Edge cases represent the highest-risk failure modes; automated tests ensure they produce correct errors and state rather than silent corruption |
| Effort | L |
| Risk | Low |
| Risk Drivers | None |
| Tier | STRICT |
| Confidence | [█████████░] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent quality-engineer 60s |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0065 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0065/evidence.md`

**Deliverables:**
- Passing edge case tests: AMBIGUOUS_PATH (multiple skill matches), NAME_COLLISION (non-portified module), budget exhaustion mid-pipeline (HALTED + return-contract), convergence ESCALATED path (downstream_ready=false + panel-report.md), template >120KB raises CONTENT_TOO_LARGE

**Steps:**
1. **[EXECUTION]** Implement `test_ambiguous_skill()`: provide workflow name matching 2 skills; assert AMBIGUOUS_PATH with candidate list
2. **[EXECUTION]** Implement `test_name_collision_non_portified()`: target output dir with existing non-portified module; assert NAME_COLLISION before any file written
3. **[EXECUTION]** Implement `test_budget_exhaustion()`: set max_turns=1; run multi-step pipeline; assert HALTED outcome; assert `return-contract.yaml` has `outcome: HALTED` and non-zero `suggested_resume_budget`
4. **[EXECUTION]** Implement `test_convergence_escalated()`: mock 3 iterations all with unaddressed CRITICALs; assert ESCALATED state; assert `downstream_ready = False`; assert `panel-report.md` exists
5. **[EXECUTION]** Implement `test_template_too_large()`: mock template content of 121 * 1024 bytes; assert `PortifyValidationError(failure_type=CONTENT_TOO_LARGE)` raised (amended from original >50KB --file test)
6. **[EXECUTION]** Run `uv run pytest tests/cli_portify/ -k "edge_case or ambiguous or collision or budget_exhaustion or escalated or content_too_large" -v`
7. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0065/evidence.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "edge_case"` exits 0
- AMBIGUOUS_PATH error includes candidate skill paths in message
- NAME_COLLISION error raised before any file is written to output dir
- HALTED outcome has `suggested_resume_budget > 0` in return-contract.yaml
- ESCALATED path has `downstream_ready = False` and `panel-report.md` in workdir
- Template >120KB raises `CONTENT_TOO_LARGE` (not `--file` call)

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "content_too_large" -v` — confirms amended >120KB behavior (not original >50KB --file test)
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0065/evidence.md` produced

**Dependencies:** All Phase 2–9 implementations; T07.04 (CONTENT_TOO_LARGE error)
**Rollback:** Remove failing edge case tests; do not merge until all pass

---

### T11.04 -- Run uv run pytest; Validate All 14 Success Criteria SC-001–SC-014

| Field | Value |
|---|---|
| Roadmap Item IDs | R-070 |
| Why | SC-001–SC-014 are the contractual acceptance criteria for the release; all must pass by automated test before merge |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution 30s |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0066 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0066/evidence.md`

**Deliverables:**
- `uv run pytest` exits 0 with all tests passing; SC-001–SC-014 validation report at `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0066/evidence.md`

**Steps:**
1. **[PLANNING]** List all 14 SC criteria and their phase/test mappings from roadmap SC-to-Phase matrix
2. **[EXECUTION]** Run `uv run pytest -v --tb=short 2>&1 | tee /tmp/portify-pytest.txt`
3. **[EXECUTION]** Confirm zero failures across all test files
4. **[EXECUTION]** For each SC: note the specific test(s) that validate it and whether it passes
5. **[EXECUTION]** Produce SC validation table: SC-001 through SC-014, each with status PASS/FAIL and test reference
6. **[COMPLETION]** Write validation table to `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0066/evidence.md`

**Acceptance Criteria:**
- `uv run pytest` exits 0 (zero failures, zero errors)
- Validation table in D-0066 has 14 rows, one per SC, each with PASS status and specific test reference — validated against the roadmap SC-to-Phase matrix:
  - SC-001: Step 0 ≤30s, `portify-config.yaml` valid (workflow_path, cli_name, output_dir)
  - SC-002: Step 1 ≤60s, `component-inventory.yaml` with ≥1 component
  - SC-003: G-002 passes on `protocol-map.md`
  - SC-004: G-003 passes on `portify-analysis-report.md`
  - SC-005: G-008 passes on `portify-spec.md` (step_mapping count consistent)
  - SC-006: Review gates write phase approval YAML with `status: pending`
  - SC-007: Resume skips steps already in PASS/PASS_NO_REPORT status
  - SC-008: G-010 passes on `portify-release-spec.md` (zero placeholders, Section 12 present)
  - SC-009: Convergence CONVERGED within 3 iterations with zero unaddressed CRITICALs
  - SC-010: Quality score overall ≥7.0 → `downstream_ready = true`
  - SC-011: `return-contract.yaml` emitted on success, failure, dry-run, interrupted paths
  - SC-012: `--dry-run` limits execution to PREREQUISITES, ANALYSIS, USER_REVIEW, SPECIFICATION
  - SC-013: Exit codes correct (0=success/interrupted, 1=failure)
  - SC-014: Exit code 124 → `PortifyStatus.TIMEOUT` classification
- No regressions in `tests/sprint/` or other existing test suites (confirmed by full run)
- Validation report produced at D-0066 path

**Validation:**
- Manual check: `uv run pytest -v --tb=short` — output shows 0 failures; SC table written
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0066/evidence.md` produced with SC-001–SC-014 PASS status

**Dependencies:** T11.01, T11.02, T11.03 (all test suites complete)
**Rollback:** Investigate failing tests; do not mark this task complete until all pass

---

### T11.05 -- Perform 5 Sample Runs

| Field | Value |
|---|---|
| Roadmap Item IDs | R-071 |
| Why | Automated tests cover unit/integration scenarios; sample runs against real workflow inputs verify the end-to-end user experience before release |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution 30s |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0067 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0067/evidence.md`

**Deliverables:**
- 5 sample run results documenting observed behavior for: (1) valid workflow dry-run, (2) ambiguous workflow name, (3) insufficient turn budget (HALTED), (4) interrupted execution (SIGINT), (5) escalation case (3 iterations, ESCALATED)

**Steps:**
1. **[EXECUTION]** Run 1 — valid workflow dry-run: `superclaude cli-portify run sc-roadmap-protocol --dry-run`; verify clean exit, portify-config.yaml and component-inventory.yaml produced, no Claude calls
2. **[EXECUTION]** Run 2 — ambiguous workflow: provide a name matching multiple skills; verify AMBIGUOUS_PATH error with candidate list
3. **[EXECUTION]** Run 3 — insufficient budget: set `--max-turns 1` on full workflow; verify HALTED outcome with resume command in return-contract.yaml
4. **[EXECUTION]** Run 4 — interrupted: Ctrl-C mid-step; verify INTERRUPTED outcome, return-contract.yaml written, workdir intact
5. **[EXECUTION]** Run 5 — escalation: mock 3 iterations with persistent unaddressed CRITICALs; verify ESCALATED, `panel-report.md` present, `downstream_ready = false`
6. **[COMPLETION]** Document all 5 run outcomes in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0067/evidence.md`

**Acceptance Criteria:**
- All 5 sample run scenarios produce expected outcomes (no unexpected exceptions)
- Run 1: `portify-config.yaml` exists; no SYNTHESIS artifacts produced
- Run 3: `return-contract.yaml` has `outcome: HALTED` and `suggested_resume_budget > 0`
- Run 4: `return-contract.yaml` has `outcome: INTERRUPTED`; workdir preserved for resume
- Run 5: `downstream_ready = false`; `panel-report.md` exists in workdir

**Validation:**
- Manual check: observed behavior matches expected outcomes for all 5 runs
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0067/evidence.md` produced with run results

**Dependencies:** T10.03 (main.py registration for CLI invocability), T11.04 (full test suite passing)
**Rollback:** Investigate unexpected behavior before declaring release readiness

---

### T11.06 -- Confirm Logs, Workdir Behavior, and Produce Release Readiness Checklist

| Field | Value |
|---|---|
| Roadmap Item IDs | R-072 |
| Why | The release readiness checklist is the final sign-off document; it confirms all acceptance criteria, risks mitigated, and operational requirements met before merge |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution 30s |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0068 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0068/spec.md`

**Deliverables:**
- Confirmation that logs are workdir-scoped (no source-tree writes); workdir retained post-run; release readiness checklist at D-0068 with all SC-001–SC-014 PASS, all risks mitigated, main.py integration verified

**Steps:**
1. **[EXECUTION]** Confirm `execution-log.jsonl` and `execution-log.md` written to workdir only (not to `src/`)
2. **[EXECUTION]** Confirm `portify-release-spec.md`, `panel-report.md`, `return-contract.yaml` all written to workdir only
3. **[EXECUTION]** Confirm no source-tree writes during execution (check git status after sample run)
4. **[EXECUTION]** Confirm workdir retained after run (OQ-014 policy: retain by default)
5. **[EXECUTION]** Produce release readiness checklist covering: SC-001–SC-014 all PASS, Risks 1–13 mitigated, no `--file` calls in codebase, main.py registration working, sprint test suite 713+ passing
6. **[COMPLETION]** Write checklist to `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0068/spec.md`

**Acceptance Criteria:**
- `git status src/` shows no new files after a full pipeline run (no source-tree artifact writes)
- `workdir/execution-log.jsonl` exists and contains events after a run
- Workdir directory retained at `.dev/portify-workdir/<cli_name>/` after pipeline completes
- Release readiness checklist at D-0068 has all items checked with evidence references

**Validation:**
- Manual check: `git status src/` is clean after sample run; workdir present with logs
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0068/spec.md` produced with checklist

**Dependencies:** T11.04 (SC validation), T11.05 (sample runs)
**Rollback:** N/A (documentation; no code changes)

---

### Checkpoint: End of Phase 11

**Purpose:** Final verification that all 14 success criteria pass, all edge cases are covered, and the implementation is ready for merge.
**Checkpoint Report Path:** `.dev/releases/current/v2.25-cli-portify-cli/checkpoints/CP-P11-END.md`

**Verification:**
- `uv run pytest -v --tb=short` exits 0 with zero failures across entire test suite
- D-0066 validation report shows SC-001–SC-014 all PASS
- D-0068 release readiness checklist is complete with all items checked

**Exit Criteria:**
- All 6 Phase 11 tasks complete with D-0063 through D-0068 artifacts
- Milestone M10: all 14 success criteria validated by automated tests; implementation ready for merge
- `superclaude cli-portify run` is invokable, resumable, and produces correct artifacts on valid and invalid inputs
