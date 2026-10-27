# Phase 6 -- Specification Pipeline

Implement Phase 2 design and spec generation with second user review checkpoint. Produces step-graph, models-gates, prompts-executor specs, then assembles them into a unified `portify-spec.md`.

---

### T06.01 -- Implement step-graph-design Prompt Builder and Step

| Field | Value |
|---|---|
| Roadmap Item IDs | R-042 |
| Why | The step graph specification defines the execution DAG for the generated CLI; it feeds the spec assembly step and must be complete before portify-spec.md can be generated |
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
| Deliverable IDs | D-0038 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0038/spec.md`

**Deliverables:**
- `prompts.py` `build_step_graph_design_prompt()` builder; step execution producing `workdir/step-graph-spec.md` with EXIT_RECOMMENDATION marker (FR-020)

**Steps:**
1. **[PLANNING]** Review roadmap FR-020: step-graph-design → step-graph-spec.md
2. **[EXECUTION]** Implement `build_step_graph_design_prompt(config, analysis_report_content) -> str` in `prompts.py`
3. **[EXECUTION]** Prompt instructs Claude to design the step execution graph from the analysis report
4. **[EXECUTION]** Implement `execute_step_graph_design(config, workdir, process) -> PortifyStepResult`
5. **[EXECUTION]** Write output to `workdir/step-graph-spec.md`; apply G-005 gate; retry once on PASS_NO_SIGNAL
6. **[EXECUTION]** Enforce 600s timeout (via STEP_REGISTRY entry)
7. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "step_graph" -v`
8. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0038/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "step_graph"` exits 0
- `build_step_graph_design_prompt()` references analysis report content
- Mock execution writes `step-graph-spec.md` with EXIT_RECOMMENDATION marker in workdir
- G-005 gate passes on output with marker; fails on output without marker

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "step_graph" -v` — G-005 gate integration confirmed
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0038/spec.md` produced

**Dependencies:** T04.01 (G-005 gate), T05.02 (analysis-report.md input)
**Rollback:** Remove step-graph-design step from registry; revert `prompts.py`

---

### T06.02 -- Implement models-gates-design Prompt Builder and Step

| Field | Value |
|---|---|
| Roadmap Item IDs | R-043 |
| Why | The models-gates spec defines the data model and gate logic for the generated CLI; it must be produced before spec assembly |
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
| Deliverable IDs | D-0039 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0039/spec.md`

**Deliverables:**
- `prompts.py` `build_models_gates_design_prompt()` builder; step execution producing `workdir/models-gates-spec.md` (FR-021)

**Steps:**
1. **[PLANNING]** Review roadmap FR-021: models-gates-design → models-gates-spec.md
2. **[EXECUTION]** Implement `build_models_gates_design_prompt(config, step_graph_content) -> str` in `prompts.py`
3. **[EXECUTION]** Implement `execute_models_gates_design(config, workdir, process) -> PortifyStepResult`
4. **[EXECUTION]** Write output to `workdir/models-gates-spec.md`; apply G-006 gate; enforce 600s timeout
5. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "models_gates" -v`
6. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0039/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "models_gates"` exits 0
- `build_models_gates_design_prompt()` references step graph content
- G-006 (return type pattern check) applied on output
- 600s timeout set in STEP_REGISTRY for this step

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "models_gates" -v` passes
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0039/spec.md` produced

**Dependencies:** T04.01 (G-006 gate), T06.01 (step-graph-spec.md input)
**Rollback:** Remove models-gates-design step; revert `prompts.py`

---

### T06.03 -- Implement prompts-executor-design Prompt Builder and Step

| Field | Value |
|---|---|
| Roadmap Item IDs | R-044 |
| Why | The prompts-executor spec defines how the generated CLI's own prompt builders and executor work; it completes the three input specs needed for pipeline-spec-assembly |
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
| Deliverable IDs | D-0040 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0040/spec.md`

**Deliverables:**
- `prompts.py` `build_prompts_executor_design_prompt()` builder; step execution producing `workdir/prompts-executor-spec.md` (FR-022)

**Steps:**
1. **[PLANNING]** Review roadmap FR-022: prompts-executor-design → prompts-executor-spec.md
2. **[EXECUTION]** Implement `build_prompts_executor_design_prompt(config, step_graph_content, models_gates_content) -> str`
3. **[EXECUTION]** Implement `execute_prompts_executor_design(config, workdir, process) -> PortifyStepResult`
4. **[EXECUTION]** Write output to `workdir/prompts-executor-spec.md`; apply G-007 gate; enforce 600s timeout
5. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "prompts_executor" -v`
6. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0040/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "prompts_executor"` exits 0
- Output written to `prompts-executor-spec.md` in workdir
- G-007 (EXIT_RECOMMENDATION marker) applied and enforced
- 600s timeout set

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "prompts_executor" -v` passes
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0040/spec.md` produced

**Dependencies:** T04.01 (G-007 gate), T06.01, T06.02
**Rollback:** Remove step; revert `prompts.py`

---

### T06.04 -- Implement pipeline-spec-assembly Step

| Field | Value |
|---|---|
| Roadmap Item IDs | R-045 |
| Why | The spec assembly step produces the unified `portify-spec.md` that all downstream phases depend on; programmatic pre-assembly ensures deduplication before Claude synthesis |
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
| Deliverable IDs | D-0041 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0041/spec.md`

**Deliverables:**
- `executor.py` pipeline-spec-assembly step: programmatic concatenation + deduplication of 3 input specs, then Claude synthesis → `workdir/portify-spec.md` passing G-008 (step-count consistency) (FR-023, SC-005)

**Steps:**
1. **[PLANNING]** Review roadmap FR-023/SC-005: programmatic pre-assembly then Claude synthesis; G-008 requires step_mapping count consistency
2. **[EXECUTION]** Implement `assemble_specs_programmatic(step_graph, models_gates, prompts_executor) -> str`: concatenate with section headers; deduplicate repeated sections
3. **[EXECUTION]** Implement `build_spec_assembly_prompt(assembled_content) -> str` in `prompts.py`
4. **[EXECUTION]** Execute Claude synthesis; write to `workdir/portify-spec.md`
5. **[EXECUTION]** Apply G-008: verify EXIT_RECOMMENDATION present AND step_mapping count matches declared steps
6. **[EXECUTION]** Enforce 600s timeout
7. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "spec_assembly or portify_spec" -v`
8. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0041/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "spec_assembly"` exits 0
- Programmatic pre-assembly produces deduplicated content before Claude call
- G-008 gate passes on `portify-spec.md` with consistent step_mapping count (SC-005)
- G-008 gate fails when step_mapping count mismatches declared steps

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "portify_spec" -v` — G-008 step-count consistency verified
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0041/spec.md` produced

**Dependencies:** T04.01 (G-008 gate), T06.01, T06.02, T06.03
**Rollback:** Remove spec-assembly step; revert programmatic assembler

---

### T06.05 -- Verify 600s Timeout and Per-Gate Enforcement on All Phase 2 Claude Steps

| Field | Value |
|---|---|
| Roadmap Item IDs | R-046 |
| Why | All 4 Phase 2 Claude steps must have consistent EXIT_RECOMMENDATION enforcement and 600s timeout; missing enforcement on any step creates an undetectable quality gap |
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
| Deliverable IDs | D-0042 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0042/evidence.md`

**Deliverables:**
- Audit confirming all 4 Phase 2 steps (step-graph, models-gates, prompts-executor, spec-assembly) have `timeout_s = 600` in STEP_REGISTRY; EXIT_RECOMMENDATION enforced on G-005/G-007/G-008 steps; G-006 enforces return-type pattern (not EXIT_RECOMMENDATION) (FR-024, NFR-001)

**Steps:**
1. **[PLANNING]** List all 4 Phase 2 Claude steps from STEP_REGISTRY
2. **[EXECUTION]** Assert each has `timeout_s = 600` in STEP_REGISTRY
3. **[EXECUTION]** Assert each has a gate (G-005, G-006, G-007, G-008) applied in executor
4. **[EXECUTION]** Confirm each gate checks EXIT_RECOMMENDATION marker (G-005, G-007, G-008 do; G-006 checks return type pattern)
5. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "phase2_timeout or phase2_exit_rec" -v`
6. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0042/evidence.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "phase2_timeout"` exits 0
- All 4 Phase 2 steps have `timeout_s = 600` confirmed
- EXIT_RECOMMENDATION enforcement confirmed on steps with G-005, G-007, G-008
- No Phase 2 step allows continuation without gate passing

**Validation:**
- Manual check: audit output in `D-0042/evidence.md` lists all 4 steps with timeout and gate confirmed
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0042/evidence.md` produced

**Dependencies:** T06.01, T06.02, T06.03, T06.04
**Rollback:** N/A (audit only; no production code changes)

---

### T06.06 -- Implement user-review-p2 Gate and phase2-approval.yaml Validation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-047 |
| Why | Phase 2 review validates the full specification before the expensive release spec synthesis and panel review; a flawed spec here propagates to all downstream artifacts |
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
| Deliverable IDs | D-0043 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0043/spec.md`

**Deliverables:**
- `executor.py` `execute_user_review_p2()`: validates `status: completed`, all blocking gates passed, `step_mapping` has entries; writes `workdir/phase2-approval.yaml`; YAML parse + schema validation on resume (FR-025, FR-026)

**Steps:**
1. **[PLANNING]** Review roadmap FR-025/FR-026: status:completed (not approved), blocking gates passed, step_mapping entries
2. **[EXECUTION]** Implement `execute_user_review_p2(config, workdir, step_results) -> None`
3. **[EXECUTION]** Validate all blocking gates (G-005, G-006, G-007, G-008) passed before writing approval YAML
4. **[EXECUTION]** Validate `portify-spec.md` has non-empty `step_mapping` section
5. **[EXECUTION]** Write `workdir/phase2-approval.yaml` with `status: completed`
6. **[EXECUTION]** Implement `_validate_phase2_approval(workdir) -> None`: YAML parse; require `status: completed`; raise `PortifyValidationError` otherwise
7. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "user_review_p2 or phase2_approval" -v`
8. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0043/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "phase2_approval"` exits 0
- `execute_user_review_p2()` writes `phase2-approval.yaml` with `status: completed`
- Resume with `status: pending` raises `PortifyValidationError`
- Empty `step_mapping` in `portify-spec.md` blocks approval emission
- All blocking gates must pass before approval YAML is written

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "user_review_p2" -v` — all validation cases pass
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0043/spec.md` produced

**Dependencies:** T06.04 (portify-spec.md with step_mapping), T04.01 (G-005–G-008 gates)
**Rollback:** Remove `execute_user_review_p2()` from step registry

---

### Checkpoint: End of Phase 6

**Purpose:** Verify the complete specification pipeline produces a valid `portify-spec.md` passing G-008, and that the second review gate functions correctly before release spec synthesis begins.
**Checkpoint Report Path:** `.dev/releases/current/v2.25-cli-portify-cli/checkpoints/CP-P06-END.md`

**Verification:**
- `uv run pytest tests/cli_portify/ -k "step_graph or models_gates or prompts_executor or spec_assembly or phase2_approval" -v` exits 0
- SC-005 (G-008 passes on portify-spec.md) verified
- SC-006 (review gate writes pending/completed YAML) and SC-007 (resume skips completed steps) verified for Phase 2

**Exit Criteria:**
- All 6 Phase 6 tasks complete with D-0038 through D-0043 artifacts
- Milestone M5: Phase 2 produces valid unified spec passing G-008; user-review-p2 validates and blocks correctly
- SC-005, SC-006, SC-007 all passing
