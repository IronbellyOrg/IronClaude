# Phase 5 -- Analysis Pipeline

Implement Phase 1 artifact generation and first user review checkpoint. Produces `protocol-map.md` and `portify-analysis-report.md` via Claude subprocess invocations, then pauses for user review before continuing.

**Requires**: Phase 3 observability baseline complete, Phase 4 gate system complete.

---

### T05.01 -- Implement protocol-mapping Prompt Builder and Step Execution

| Field | Value |
|---|---|
| Roadmap Item IDs | R-037 |
| Why | The protocol map is the first Claude-generated artifact; it drives all downstream analysis steps and must have valid YAML frontmatter and an EXIT_RECOMMENDATION marker to pass G-002 |
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
| Deliverable IDs | D-0033 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0033/spec.md`

**Deliverables:**
- `src/superclaude/cli/cli_portify/prompts.py` `build_protocol_mapping_prompt()` builder; analysis step function executing Claude subprocess and writing `protocol-map.md` with required YAML frontmatter (FR-013); EXIT_RECOMMENDATION enforced (FR-014)

**Steps:**
1. **[PLANNING]** Load existing `prompts.py` content; identify which builders already exist
2. **[PLANNING]** Review roadmap FR-013/FR-014: protocol-map.md requires YAML frontmatter + EXIT_RECOMMENDATION marker
3. **[EXECUTION]** Implement `build_protocol_mapping_prompt(config: PortifyConfig, inventory: list[ComponentEntry]) -> str` in `prompts.py`
4. **[EXECUTION]** Prompt must instruct Claude to output `EXIT_RECOMMENDATION: CONTINUE` at end of result file
5. **[EXECUTION]** Implement `execute_protocol_mapping_step(config, workdir, process) -> PortifyStepResult` in executor
6. **[EXECUTION]** Run Claude via `PortifyProcess`; write output to `workdir/protocol-map.md`
7. **[EXECUTION]** Apply G-002 gate after step; if fail → retry once (PASS_NO_SIGNAL path)
8. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "protocol_mapping or protocol_map" -v`
9. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0033/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "protocol_mapping"` exits 0
- `build_protocol_mapping_prompt()` returns non-empty string containing component inventory reference
- Mock Claude execution produces `protocol-map.md` with YAML frontmatter in workdir
- G-002 gate passes on properly structured `protocol-map.md` (SC-003)

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "protocol_mapping" -v` — G-002 gate integration confirmed
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0033/spec.md` produced

**Dependencies:** T04.01 (G-002 gate), T03.04 (executor), T02.07 (component inventory)
**Rollback:** Remove protocol-mapping step from step registry; revert `prompts.py` changes

---

### T05.02 -- Implement analysis-synthesis Prompt Builder and Step Execution

| Field | Value |
|---|---|
| Roadmap Item IDs | R-038 |
| Why | The analysis report synthesizes all component data into actionable recommendations; it must contain all 7 required sections to pass G-003 |
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
| Deliverable IDs | D-0034 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0034/spec.md`

**Deliverables:**
- `prompts.py` `build_analysis_synthesis_prompt()` builder; step execution producing `portify-analysis-report.md` with Source Components, Step Graph, Parallel Groups, Gates Summary, Data Flow, Classifications, Recommendations sections (FR-016); EXIT_RECOMMENDATION enforced (FR-017)

**Steps:**
1. **[PLANNING]** Review roadmap FR-016/FR-017: 7 required sections + EXIT_RECOMMENDATION
2. **[EXECUTION]** Implement `build_analysis_synthesis_prompt(config, inventory, protocol_map_content) -> str` in `prompts.py`
3. **[EXECUTION]** Prompt must explicitly list all 7 required section names so Claude includes them
4. **[EXECUTION]** Implement `execute_analysis_synthesis_step(config, workdir, process) -> PortifyStepResult`
5. **[EXECUTION]** Write output to `workdir/portify-analysis-report.md`
6. **[EXECUTION]** Apply G-003 gate; retry once on PASS_NO_SIGNAL
7. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "analysis_synthesis or analysis_report" -v`
8. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0034/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "analysis_synthesis"` exits 0
- `build_analysis_synthesis_prompt()` includes all 7 section names in prompt text
- G-003 gate passes on properly structured `portify-analysis-report.md` (SC-004)
- G-003 fails correctly when any of the 7 sections is missing

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "analysis_report" -v` — G-003 gate integration confirmed
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0034/spec.md` produced

**Dependencies:** T04.01 (G-003 gate), T05.01 (protocol-map.md input)
**Rollback:** Remove analysis-synthesis step; revert `prompts.py` changes

---

### T05.03 -- Enforce 600s Timeout on Analysis Steps

| Field | Value |
|---|---|
| Roadmap Item IDs | R-039 |
| Why | Claude subprocess analysis steps can stall indefinitely; 600s is the hard backstop to prevent pipeline hangs on Steps 2 and 3 |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STRICT |
| Confidence | [█████████░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent quality-engineer 60s |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0035 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0035/evidence.md`

**Deliverables:**
- 600s timeout enforced on protocol-mapping step and analysis-synthesis step via `PortifyStep.timeout_s = 600` in STEP_REGISTRY (NFR-001)

**Steps:**
1. **[PLANNING]** Review roadmap NFR-001: 600s timeout for both analysis steps
2. **[EXECUTION]** Confirm `timeout_s = 600` set in STEP_REGISTRY for `protocol-mapping` and `analysis-synthesis` step entries
3. **[EXECUTION]** Verify executor passes `timeout_s` to `PortifyProcess` subprocess via `--max-turns` equivalent or process kill timer
4. **[EXECUTION]** Confirm exit code 124 classification (T03.07) fires correctly when timeout reached
5. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "analysis_timeout or timeout_600" -v` — mock 601s execution
6. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0035/evidence.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "timeout_600"` exits 0
- Protocol-mapping step `timeout_s` = 600 confirmed in STEP_REGISTRY
- Analysis-synthesis step `timeout_s` = 600 confirmed in STEP_REGISTRY
- Mocked 601s subprocess triggers TIMEOUT classification

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "analysis_timeout" -v` — timeout boundary verified
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0035/evidence.md` produced

**Dependencies:** T03.07 (exit 124 → TIMEOUT), T05.01 (protocol-mapping step), T05.02 (analysis-synthesis step)
**Rollback:** Remove timeout enforcement; steps revert to unbounded execution

---

### T05.04 -- Implement user-review-p1 Gate and phase1-approval.yaml

| Field | Value |
|---|---|
| Roadmap Item IDs | R-040 |
| Why | The first user review checkpoint ensures human approval before the more expensive specification pipeline begins; skipping it risks generating specs from flawed analysis |
| Effort | M |
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
| Deliverable IDs | D-0036 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0036/spec.md`

**Deliverables:**
- `executor.py` `execute_user_review_p1()`: writes `workdir/phase1-approval.yaml` with `status: pending`; prints resume instructions to stdout; exits cleanly with code 0 (FR-018, SC-006)

**Steps:**
1. **[PLANNING]** Review roadmap FR-018/SC-006: write pending YAML, print resume instructions, exit cleanly
2. **[EXECUTION]** Implement `execute_user_review_p1(config, workdir) -> None` in `executor.py`
3. **[EXECUTION]** Write `workdir/phase1-approval.yaml`:
   ```yaml
   status: pending
   workflow: <cli_name>
   review_artifacts:
     - protocol-map.md
     - portify-analysis-report.md
   instructions: "Review artifacts above. Set status to 'approved' to continue."
   ```
4. **[EXECUTION]** Print resume command to stdout: `"Review complete? Run: superclaude cli-portify run <workflow> --resume phase2"`
5. **[EXECUTION]** Call `sys.exit(0)` — clean exit, not an error
6. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "user_review_p1 or phase1_approval" -v`
7. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0036/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "phase1_approval"` exits 0 (SC-006)
- `execute_user_review_p1()` writes `phase1-approval.yaml` with `status: pending`
- Resume instructions printed to stdout before exit
- Exit code is 0 (not an error condition)

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "user_review_p1" -v` — pending YAML output and clean exit verified
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0036/spec.md` produced

**Dependencies:** T05.02 (analysis complete before review gate), T04.01 (G-004 gate for approval status)
**Rollback:** Remove `execute_user_review_p1()` from step registry

---

### T05.05 -- Implement --resume Logic with YAML Parse + Schema Validation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-041 |
| Why | Resume must validate the approval YAML structurally — raw string matching on `status: approved` fails on malformed YAML, comments, and whitespace variants |
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
| Deliverable IDs | D-0037 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0037/spec.md`

**Deliverables:**
- `executor.py` `_validate_phase1_approval(workdir: Path) -> None`: YAML parse + schema validation requiring `status: approved`; raises `PortifyValidationError` on malformed YAML, missing status, or non-approved status (FR-019)

**Steps:**
1. **[PLANNING]** Review roadmap FR-019 and Risk 8: YAML parse + schema validation; not raw string match
2. **[EXECUTION]** Implement `_validate_phase1_approval(workdir: Path) -> None` in `executor.py`
3. **[EXECUTION]** Read `workdir/phase1-approval.yaml`; parse with `yaml.safe_load()`
4. **[EXECUTION]** Validate schema: `status` field must exist and equal `"approved"`
5. **[EXECUTION]** Raise `PortifyValidationError(failure_type=INVALID_PATH, message="phase1-approval.yaml: status must be 'approved'")` on any failure
6. **[EXECUTION]** Call `_validate_phase1_approval()` at start of `--resume` execution before any step runs
7. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "phase1_approval or resume_validation" -v`
8. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0037/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "resume_validation"` exits 0 (SC-007)
- Malformed YAML in `phase1-approval.yaml` raises `PortifyValidationError`
- `status: pending` raises `PortifyValidationError`
- `status: approved` passes validation; resume proceeds
- Status in YAML comment (not actual field) raises `PortifyValidationError` (not raw string matched)

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "phase1_approval" -v` — all 4 validation cases pass
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0037/spec.md` produced

**Dependencies:** T05.04 (phase1-approval.yaml writer), T03.04 (resume executor)
**Rollback:** Remove `_validate_phase1_approval()` call from resume path

---

### Checkpoint: End of Phase 5

**Purpose:** Verify analysis pipeline produces valid artifacts, review gate pauses correctly, and resume validates approval before Phase 6 specification pipeline begins.
**Checkpoint Report Path:** `.dev/releases/current/v2.25-cli-portify-cli/checkpoints/CP-P05-END.md`

**Verification:**
- `uv run pytest tests/cli_portify/ -k "protocol_mapping or analysis_synthesis or phase1_approval or resume_validation" -v` exits 0
- SC-003 (G-002 passes on protocol-map.md) and SC-004 (G-003 passes on analysis-report.md) verified
- SC-006 (review gate writes pending approval) and SC-007 (resume skips completed steps) verified

**Exit Criteria:**
- All 5 Phase 5 tasks complete with D-0033 through D-0037 artifacts
- Milestone M4: Phase 1 completes reliably; review gate pauses; resume validates status:approved
- Zero blocking issues for Phase 6 specification pipeline
