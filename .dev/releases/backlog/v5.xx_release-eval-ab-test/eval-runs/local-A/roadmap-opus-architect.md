---
spec_source: "eval-spec.md"
complexity_score: 0.45
primary_persona: architect
---

# Roadmap: Pipeline Progress Reporting for Unified Audit Gating

## Executive Summary

This roadmap covers the implementation of a structured progress reporting subsystem for the `superclaude roadmap` CLI pipeline. The feature adds a `progress.json` output file that records per-step execution metadata (status, timing, gate verdicts, step-specific diagnostics) using atomic writes for crash safety. The integration surface is narrow: one new module (`progress.py`), three modified modules (`executor.py`, `commands.py`, `gates.py`), and two cross-module read points (`convergence.py`, `wiring_gate.py`). Complexity is MEDIUM (0.45) — the core callback-and-write pattern is straightforward, but deviation sub-reporting and wiring integration require careful data-model design.

**Key architectural decisions**:
- Callback-based, not observer-based — no threads, no file watchers
- Atomic JSON writes via `os.replace()` — crash-safe by construction
- Sequential callback invocation even for parallel steps — no concurrency in the writer
- `progress.py` depends on `models.py` and `gates.py`, never the reverse

## Phase 1: Foundation — Data Models & Atomic Writer

**Goal**: Establish the `StepProgress` / `PipelineProgress` data models and the crash-safe file writer in `progress.py`.

### Tasks
1. Design `StepProgress` dataclass with fields: `step_id`, `status`, `duration_ms`, `gate_verdict`, `output_file`, `metadata` (dict)
2. Design `PipelineProgress` container holding `list[StepProgress]` with `to_json()` serialization
3. Implement atomic write function: serialize to JSON → write to temp file → `os.replace()` to target path
4. Validate zero import-time side effects (NFR-003) — no module-level I/O
5. Unit test: round-trip serialization, atomic write under simulated interruption

### Milestone
`progress.py` exists, imports cleanly with no side effects, and can serialize/write a `PipelineProgress` atomically.

### Requirements Covered
FR-001, FR-002, FR-010, NFR-002, NFR-003

### Estimated Effort
1–2 days

---

## Phase 2: CLI Integration & Executor Callback

**Goal**: Wire `--progress-file` into the CLI and hook the progress writer into `execute_pipeline()` via its existing `on_step_complete` callback.

### Tasks
1. Add `--progress-file` as `click.Path` option to `run` command in `commands.py`, defaulting to `{output_dir}/progress.json`
2. Add path validation: parent directory must exist; fail fast before pipeline starts (FR-005)
3. Implement `on_step_complete` callback that builds a `StepProgress` entry from `StepResult` and appends it to the running `PipelineProgress`
4. Thread the callback through `execute_roadmap()` → `execute_pipeline()` — no signature changes to `execute_pipeline` itself; use the existing callback slot (NFR-004)
5. Handle overwrite-on-fresh-run semantics (FR-005): initialize empty `PipelineProgress` at pipeline start

### Milestone
A full pipeline run produces a valid `progress.json` with one entry per step, all core fields populated.

### Requirements Covered
FR-001, FR-003, FR-004, FR-005, NFR-001, NFR-004, SC-001, SC-005

### Estimated Effort
1–2 days

---

## Phase 3: Gate Summary & Dry-Run Table

**Goal**: Add the `summary()` method to gate constants and implement the `--dry-run` Markdown table output.

### Tasks
1. Add `summary()` method to `GateCriteria` — returns tier, required fields count, semantic checks count (NFR-005: purely additive)
2. Verify backward compatibility: no existing gate constant interfaces change, no call-site modifications
3. Implement dry-run table renderer: iterate `ALL_GATES` (including `WIRING_GATE`), output Markdown table with columns: Step, Gate Tier, Required Fields, Semantic Checks
4. Mark conditional steps (remediate, certify) explicitly in the table output
5. Integration test: `--dry-run` output contains all 13 gate entries

### Milestone
`--dry-run` outputs a complete gate summary table. `summary()` is available on all gate constants.

### Requirements Covered
FR-006, NFR-005, SC-003

### Estimated Effort
0.5–1 day

---

## Phase 4: Parallel Step Timing & Special-Step Metadata

**Goal**: Ensure parallel steps report accurate independent timing, and enrich progress entries for remediation, certification, and wiring verification steps.

### Tasks
1. Verify parallel step timing: `generate-A` and `generate-B` entries must have independent `duration_ms` values derived from their respective `StepResult.started_at` / `finished_at` — confirm the existing `execute_pipeline()` parallel runner already provides per-step timing (FR-003, SC-004)
2. Implement remediation metadata: when remediation executes, populate `metadata.trigger_reason` and `metadata.finding_count` (FR-008)
3. Implement certification cross-reference: certification entry's `metadata` must reference the remediation step it validates (FR-008)
4. Implement wiring verification metadata: populate `metadata.unwired_count`, `metadata.orphan_count`, `metadata.blocking_count`, `metadata.rollout_mode` from `WiringReport` (FR-009). Gate verdict must reflect `WIRING_GATE` semantic check results.

### Milestone
All special-step progress entries contain their required metadata fields. Parallel step timings are independently accurate.

### Requirements Covered
FR-003, FR-008, FR-009, SC-004

### Estimated Effort
1–2 days

---

## Phase 5: Convergence Sub-Reporting

**Goal**: Capture deviation analysis iterations as sub-entries within the spec-fidelity step's progress record.

### Prerequisites
- **OQ-001 must be resolved** before implementation: the JSON schema for deviation sub-entries needs a design decision. Recommended default: `metadata.convergence_iterations: list[{pass_number, structural_high_count, semantic_high_count, regression_detected}]` mirroring `ConvergenceResult` fields.

### Tasks
1. Resolve OQ-001: define deviation sub-entry schema (recommend aligning with `ConvergenceResult` fields from `convergence.py`)
2. Hook into the convergence loop in the spec-fidelity step to capture per-iteration data
3. Populate `metadata.convergence_iterations` and `metadata.convergence_pass_count` on the spec-fidelity progress entry (FR-007)
4. Test: multi-iteration convergence run produces correctly nested sub-entries

### Milestone
Spec-fidelity progress entries contain per-iteration convergence data.

### Requirements Covered
FR-007

### Estimated Effort
1–1.5 days

---

## Phase 6: Validation & Performance

**Goal**: Verify all success criteria, measure write latency, and confirm crash safety.

### Tasks
1. **SC-001**: End-to-end test — full pipeline run → parse `progress.json` → assert all fields present per step
2. **SC-002**: Crash-safety test — kill pipeline mid-step → parse `progress.json` → must be valid JSON
3. **SC-004**: Parallel timing test — verify `generate-A` and `generate-B` have distinct, accurate `duration_ms`
4. **SC-005**: Custom path test — `--progress-file /tmp/custom.json` writes to specified path
5. **SC-006**: Performance test — measure per-step write overhead; assert < 50ms
6. **SC-007**: Import test — `import superclaude.cli.roadmap.progress` → no file I/O side effects
7. Resolve OQ-002 if blocking acceptance tests for FR-008 (define "significant findings" threshold — recommend: HIGH severity, aligning with `_high_severity_count_zero` semantic check already in `gates.py`)

### Milestone
All 7 success criteria pass. Performance budget met.

### Requirements Covered
SC-001 through SC-007, NFR-001

### Estimated Effort
1–2 days

---

## Risk Assessment & Mitigation

| Risk | Severity | Mitigation | Phase |
|------|----------|------------|-------|
| **RISK-001**: Progress writes add latency | Low | Atomic write is < 50ms; pipeline steps take minutes. NFR-001 test in Phase 6 enforces this. | 6 |
| **RISK-002**: Parallel steps corrupt progress file | Medium | Already mitigated by architecture: `on_step_complete` is invoked sequentially even for parallel steps. No concurrent writes. | 2 |
| **RISK-003**: `summary()` breaks gate constants | High | Method is purely additive. Phase 3 includes backward-compat verification. No existing signatures change. | 3 |
| **RISK-004**: Undefined deviation sub-entry schema | Medium | OQ-001 must be resolved before Phase 5. Default schema proposed based on `ConvergenceResult`. | 5 |
| **OQ-004**: Overwrite vs. resume contradiction | Medium | Treat as two distinct modes: fresh run overwrites, `--resume` appends. Requires spec clarification before Phase 2 path validation. | 2 |

## Resource Requirements & Dependencies

### Internal Dependencies (by phase)
- **Phase 1**: `models.py` (read `StepResult` shape from `pipeline/models.py`), `gates.py` (import for type references)
- **Phase 2**: `executor.py` (callback slot in `execute_pipeline`), `commands.py` (Click option registration)
- **Phase 3**: `gates.py` (`GateCriteria` class, `ALL_GATES` list)
- **Phase 4**: `wiring_gate.py` (`WiringReport`, `WIRING_GATE`), `executor.py` (remediation step metadata access)
- **Phase 5**: `convergence.py` (`DeviationRegistry`, `ConvergenceResult`)

### External Dependencies
- Python stdlib only: `json`, `os`, `tempfile`, `time`, `dataclasses`
- No new third-party packages required

### Pre-Implementation Decisions Required
1. **OQ-001** (blocks Phase 5): Deviation sub-entry JSON schema
2. **OQ-002** (blocks Phase 6 acceptance): "Significant findings" threshold definition
3. **OQ-004** (blocks Phase 2 edge case): Overwrite vs. resume behavior reconciliation
4. **OQ-005** (informational): Metadata key conventions — recommend documenting but not enforcing schema constraints on the open dict

## Success Criteria Validation Matrix

| Criterion | Validated In | Method |
|-----------|-------------|--------|
| SC-001: Complete progress.json | Phase 6 | End-to-end pipeline run + JSON parse |
| SC-002: Crash-safe JSON | Phase 6 | Kill-and-parse test |
| SC-003: Dry-run gate table | Phase 3 | `--dry-run` output assertion |
| SC-004: Independent parallel timing | Phase 6 | Timing delta comparison |
| SC-005: Custom progress path | Phase 6 | `--progress-file` path test |
| SC-006: < 50ms write overhead | Phase 6 | Timing measurement with/without progress |
| SC-007: No import side effects | Phase 6 | Import + I/O monitoring |

## Timeline Summary

| Phase | Duration | Dependencies | Cumulative |
|-------|----------|-------------|------------|
| 1: Data Models & Writer | 1–2 days | None | Days 1–2 |
| 2: CLI & Executor Wiring | 1–2 days | Phase 1, OQ-004 | Days 3–4 |
| 3: Gate Summary & Dry-Run | 0.5–1 day | Phase 1 | Days 4–5 |
| 4: Special-Step Metadata | 1–2 days | Phase 2 | Days 5–7 |
| 5: Convergence Sub-Reporting | 1–1.5 days | Phase 4, OQ-001 | Days 7–8 |
| 6: Validation & Performance | 1–2 days | All phases | Days 8–10 |

**Total estimated duration**: 6–10 working days, depending on open question resolution speed and testing depth.

**Critical path**: Phase 1 → Phase 2 → Phase 4 → Phase 5 → Phase 6. Phase 3 can run in parallel with Phase 2.
