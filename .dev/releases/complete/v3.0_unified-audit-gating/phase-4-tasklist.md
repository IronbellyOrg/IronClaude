# Phase 4 -- Roadmap Pipeline Integration

Wire the wiring verification gate into the roadmap pipeline as a post-merge step running in shadow mode. This phase achieves milestone M3a: end-to-end roadmap pipeline executes the wiring-verification step and emits a report without blocking.

### T04.01 -- Add build_wiring_verification_prompt() Stub to roadmap/prompts.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-020 |
| Why | Section 5.7 Step 2 requires a prompt builder function for the wiring-verification pipeline step |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0017 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0017/spec.md

**Deliverables:**
- `build_wiring_verification_prompt(merge_file: Path, spec_source: str) -> str` function in `src/superclaude/cli/roadmap/prompts.py` that returns a prompt string for the wiring-verification step

**Steps:**
1. **[PLANNING]** Read `src/superclaude/cli/roadmap/prompts.py` to understand existing prompt builder patterns
2. **[PLANNING]** Read section 5.7 Step 2 for prompt content requirements
3. **[EXECUTION]** Add `build_wiring_verification_prompt()` function following existing prompt builder conventions in the file
4. **[EXECUTION]** Function accepts `merge_file: Path` and `spec_source: str`, returns formatted prompt string
5. **[VERIFICATION]** Verify function is importable and returns non-empty string for valid inputs
6. **[COMPLETION]** Document function purpose with reference to section 5.7

**Acceptance Criteria:**
- `from superclaude.cli.roadmap.prompts import build_wiring_verification_prompt` imports successfully
- Function returns a non-empty string when called with valid `Path` and `str` arguments
- Function signature matches `(merge_file: Path, spec_source: str) -> str` exactly
- No imports from `pipeline/*` in the function (NFR-007)

**Validation:**
- `uv run pytest tests/ -k "wiring_verification_prompt" -v` exits 0
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0017/spec.md

**Dependencies:** Phase 3 complete (report format defined)
**Rollback:** Remove `build_wiring_verification_prompt()` from prompts.py

---

### T04.02 -- Add Wiring-Verification Step to _build_steps() and Update _get_all_step_ids() in roadmap/executor.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-021 |
| Why | The wiring-verification step must be positioned after spec-fidelity and before remediate in the pipeline step sequence per section 5.7 Steps 4-5 (INV-003) |
| Effort | M |
| Risk | Medium |
| Risk Drivers | pipeline (step ordering), multi-file (executor modifications) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0018, D-0048 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0018/spec.md
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0048/spec.md

**Deliverables:**
- New `Step` entry in `_build_steps()` for `"wiring-verification"` with `timeout_seconds=60`, `retry_limit=0`, `inputs=[merge_file, spec_fidelity_file]`, `gate_mode=GateMode.TRAILING`
- Updated `_get_all_step_ids()` to include `"wiring-verification"` after `"spec-fidelity"` and before `"remediate"`

**Steps:**
1. **[PLANNING]** Read `src/superclaude/cli/roadmap/executor.py` to locate `_build_steps()` and `_get_all_step_ids()` functions
2. **[PLANNING]** Identify the existing step ordering to find insertion point between spec-fidelity and remediate
3. **[EXECUTION]** Add `Step(id="wiring-verification", timeout_seconds=60, retry_limit=0, inputs=[merge_file, spec_fidelity_file], gate_mode=GateMode.TRAILING)` to `_build_steps()` after the spec-fidelity step
4. **[EXECUTION]** Update `_get_all_step_ids()` to include `"wiring-verification"` in the correct position
5. **[EXECUTION]** Set `gate_mode=GateMode.TRAILING` explicitly to prevent R8 risk (resolve_gate_mode override)
6. **[VERIFICATION]** Assert `_get_all_step_ids()` returns wiring-verification between spec-fidelity and remediate
7. **[COMPLETION]** Document step parameters with reference to section 5.7

**Acceptance Criteria:**
- `_get_all_step_ids()` returns a list where `"wiring-verification"` appears immediately after `"spec-fidelity"` and before `"remediate"`
- The wiring-verification `Step` has `timeout_seconds=60`, `retry_limit=0`, and `gate_mode=GateMode.TRAILING`
- `Step` inputs include both `merge_file` and `spec_fidelity_file`
- No signature changes to existing pipeline substrate functions (section 3.1)

**Validation:**
- `uv run pytest tests/ -k "step_ids" -v` exits 0 with wiring-verification in correct position
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0018/spec.md

**Dependencies:** T04.01 (prompt builder), Phase 3 complete (gate definition)
**Rollback:** Remove wiring-verification Step from `_build_steps()` and revert `_get_all_step_ids()`

---

### T04.03 -- Special-Case roadmap_run_step() for Wiring-Verification in roadmap/executor.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-022 |
| Why | Section 5.7.1 requires the wiring-verification step to call run_wiring_analysis() and emit_report() directly, returning StepStatus.PASS unconditionally since gate evaluation is handled separately by the trailing gate runner |
| Effort | M |
| Risk | Medium |
| Risk Drivers | pipeline (step execution), multi-file (cross-module calls) |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0019 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0019/spec.md

**Deliverables:**
- Special-case branch in `roadmap_run_step()` for `step.id == "wiring-verification"` that calls `run_wiring_analysis()` from `cli/audit/wiring_gate.py`, calls `emit_report()`, and returns `StepStatus.PASS` unconditionally per section 5.7.1

**Steps:**
1. **[PLANNING]** Read `roadmap_run_step()` in `src/superclaude/cli/roadmap/executor.py` to understand the existing step dispatch pattern
2. **[PLANNING]** Verify `run_wiring_analysis` and `emit_report` are importable from `cli/audit/wiring_gate`
3. **[EXECUTION]** Add `elif step.id == "wiring-verification":` branch to `roadmap_run_step()`
4. **[EXECUTION]** In the branch: construct `WiringConfig` from step inputs, call `run_wiring_analysis(config, source_dir)`, call `emit_report(report, output_path)`, return `StepStatus.PASS`
5. **[EXECUTION]** Ensure the import path is `from superclaude.cli.audit.wiring_gate import run_wiring_analysis, emit_report` (not from pipeline)
6. **[VERIFICATION]** Run integration test that exercises the wiring-verification step end-to-end
7. **[COMPLETION]** Document the unconditional PASS return with reference to section 5.7.1

**Acceptance Criteria:**
- `roadmap_run_step()` handles `step.id == "wiring-verification"` without raising exceptions
- The step calls `run_wiring_analysis()` and `emit_report()` from `cli/audit/wiring_gate`
- Step always returns `StepStatus.PASS` regardless of findings (gate evaluation is separate per section 5.7.1)
- Import path does not cross the NFR-007 boundary (no pipeline imports into audit code)

**Validation:**
- `uv run pytest tests/integration/ -k "wiring_verification_step" -v` exits 0
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0019/spec.md

**Dependencies:** T04.02 (Step definition), T02.03-T02.05 (analyzers), T03.01 (emit_report)
**Rollback:** Remove the wiring-verification branch from `roadmap_run_step()`

---

### T04.04 -- Register WIRING_GATE in ALL_GATES in roadmap/gates.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-023 |
| Why | The trailing gate runner needs WIRING_GATE registered in ALL_GATES to evaluate it during pipeline execution per section 5.7 Step 5 |
| Effort | XS |
| Risk | Medium |
| Risk Drivers | pipeline (shared modification point), merge conflicts (R-009 concurrent PR risk) |
| Tier | STRICT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0020 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0020/spec.md

**Deliverables:**
- `WIRING_GATE` entry added to `ALL_GATES` dict/list in `src/superclaude/cli/roadmap/gates.py`

**Steps:**
1. **[PLANNING]** Read `src/superclaude/cli/roadmap/gates.py` to understand `ALL_GATES` structure and existing gate registrations
2. **[PLANNING]** Coordinate merge window: this modifies a shared file per R-009 risk mitigation
3. **[EXECUTION]** Import `WIRING_GATE` from `superclaude.cli.audit.wiring_gate` and add to `ALL_GATES`
4. **[VERIFICATION]** Verify `WIRING_GATE` appears in `ALL_GATES` and `gate_passed()` can look it up
5. **[COMPLETION]** Add comment noting this was added as part of v3.0 unified audit gating

**Acceptance Criteria:**
- `WIRING_GATE` is present in `ALL_GATES` and discoverable by `gate_passed()` (SC-005)
- Import is from `superclaude.cli.audit.wiring_gate`, not duplicated inline
- No other entries in `ALL_GATES` are modified or removed
- File passes linting with `ruff check src/superclaude/cli/roadmap/gates.py`

**Validation:**
- `uv run pytest tests/ -k "all_gates" -v` exits 0 with WIRING_GATE discoverable
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0020/spec.md

**Dependencies:** T03.03 (WIRING_GATE definition)
**Rollback:** Remove WIRING_GATE import and entry from gates.py
**Notes:** This is a shared modification point with concurrent PRs. Merge window coordination required per R-009 mitigation.

---

### T04.05 -- Implement Integration Tests for Roadmap Pipeline with Resume Behavior Validation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-024, R-025 |
| Why | SC-005 requires integration proof that unmodified gate_passed() processes WIRING_GATE, and section 10.2 mandates >=3 integration tests including resume behavior per section 5.7.2 |
| Effort | M |
| Risk | Medium |
| Risk Drivers | pipeline (integration testing), multi-file (cross-subsystem) |
| Tier | STANDARD |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0021, D-0022 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0021/evidence.md
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0022/evidence.md

**Deliverables:**
- `tests/integration/test_wiring_pipeline.py` with >=3 integration tests: (1) end-to-end pipeline with shadow gate, (2) gate_passed() processes WIRING_GATE correctly (SC-005), (3) resume behavior after wiring-verification step per section 5.7.2
- Resume behavior validation: pipeline resumes correctly when interrupted after wiring-verification step

**Steps:**
1. **[PLANNING]** Review SC-005, section 10.2, and section 5.7.2 resume behavior requirements
2. **[PLANNING]** Design test scenarios: full pipeline run, gate evaluation, interrupted resume
3. **[EXECUTION]** Write test 1: end-to-end pipeline executes wiring-verification step, emits report, does not block in shadow mode
4. **[EXECUTION]** Write test 2: `gate_passed(report_path, WIRING_GATE)` returns `(True, None)` for well-formed shadow report (SC-005)
5. **[EXECUTION]** Write test 3: simulate pipeline interruption after wiring-verification, resume from checkpoint, verify step is not re-executed per section 5.7.2
6. **[EXECUTION]** Verify no `pipeline/*` imports from `roadmap/*` or `audit/*` (NFR-007 static check)
7. **[VERIFICATION]** Run `uv run pytest tests/integration/test_wiring_pipeline.py -v` and verify all 3 tests pass
8. **[COMPLETION]** Record test results in evidence artifact

**Acceptance Criteria:**
- `uv run pytest tests/integration/test_wiring_pipeline.py -v` exits 0 with >=3 tests passing
- End-to-end pipeline runs with shadow gate without blocking on any findings
- `gate_passed()` (unmodified from pipeline) correctly evaluates WIRING_GATE (SC-005)
- Resume behavior validated: interrupted pipeline does not re-execute completed wiring-verification step

**Validation:**
- `uv run pytest tests/integration/test_wiring_pipeline.py -v` exits 0 with >=3 tests passing
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0021/evidence.md

**Dependencies:** T04.01, T04.02, T04.03, T04.04
**Rollback:** Delete `tests/integration/test_wiring_pipeline.py`

---

### Checkpoint: End of Phase 4

**Purpose:** Validate milestone M3a: end-to-end roadmap pipeline executes wiring-verification step and emits report without blocking.
**Checkpoint Report Path:** .dev/releases/current/v3.0_unified-audit-gating/checkpoints/CP-P04-END.md
**Verification:**
- `_get_all_step_ids()` returns wiring-verification between spec-fidelity and remediate
- Pipeline runs end-to-end with shadow gate without blocking
- No imports from `pipeline/*` into `roadmap/*` or `audit/*` violating layering (NFR-007)
**Exit Criteria:**
- `uv run pytest tests/integration/test_wiring_pipeline.py -v` exits 0 with >=3 integration tests passing
- `gate_passed(report_path, WIRING_GATE)` returns `(True, None)` for shadow-mode reports (SC-005)
- Static check confirms no NFR-007 violations across all new and modified files
