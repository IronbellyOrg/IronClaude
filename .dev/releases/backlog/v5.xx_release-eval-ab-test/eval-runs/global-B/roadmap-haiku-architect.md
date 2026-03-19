---
spec_source: extraction.md
complexity_score: 0.45
primary_persona: architect
---

# 1. Executive summary

This roadmap delivers a moderate-scope enhancement to the `superclaude roadmap run` pipeline by adding crash-safe progress reporting, dry-run gate visibility, and richer auditability around deviation analysis, remediation, and wiring verification.

From an architect perspective, the work is attractive because it has:
1. A constrained blast radius: one new module plus a small number of integrations.
2. Clear extension points: existing post-step callback, existing CLI surface, and additive gate metadata.
3. A manageable risk profile: most uncertainty is not implementation complexity, but specification ambiguity.

The recommended strategy is to implement this as a thin reporting layer with strict separation from gate enforcement logic. The roadmap should preserve current execution semantics, avoid concurrency expansion, and treat the progress file as a durable system-of-record artifact.

## Architectural priorities

1. **Protect pipeline correctness first**
   - Progress reporting must never alter execution order or gate behavior.
   - Existing gate validation logic remains unchanged.

2. **Guarantee artifact integrity**
   - Progress JSON must remain valid after every write.
   - Atomic rewrite semantics are mandatory.

3. **Resolve spec ambiguities early**
   - Deviation sub-entry schema
   - Remediation trigger threshold
   - `--resume` vs overwrite semantics
   - `completed` field meaning
   - Metadata placement contract

4. **Keep the design additive**
   - New `progress.py`
   - Additive CLI option
   - Additive `summary()` support on gates
   - Callback wiring only, no new background observers or streaming paths

# 2. Phased implementation plan with milestones

## Phase 0 — Specification alignment and contract freeze

### Objective
Remove the known ambiguities before code integration hardens around assumptions.

### Milestone M1 — Reporting contract definition
1. Define the JSON schema for:
   - `PipelineProgress`
   - `StepProgress`
   - deviation analysis sub-entries
   - remediation linkage
   - wiring metadata
2. Decide whether extended fields live:
   - directly on step entries, or
   - under `metadata`
3. Define `completed` semantics:
   - `false` until pipeline terminal step finishes
   - `true` only after planned pipeline completion
4. Define `--resume` precedence over overwrite behavior.

### Deliverables
- Frozen progress JSON contract
- Resolution log for all identified gaps
- Acceptance examples for normal, resumed, remediated, and crashed runs

### Exit criteria
- No blocking ambiguity remains
- Test expectations map to a single data contract

---

## Phase 1 — Core progress infrastructure

### Objective
Build the durable reporting foundation before any CLI or executor wiring.

### Milestone M2 — Datamodel and writer implementation
1. Create `src/superclaude/cli/roadmap/progress.py`.
2. Implement:
   - `StepProgress` dataclass
   - `PipelineProgress` dataclass
3. Implement serialization for wrapped JSON output.
4. Implement crash-safe persistence via:
   - temp file write
   - `os.replace()`
5. Ensure zero I/O at import time.

### Deliverables
- `progress.py`
- serialization helpers
- atomic writer implementation

### Dependencies
- Depends on M1 schema decisions

### Exit criteria
- Valid JSON emitted after each write
- No import-time side effects
- Atomic writes verified in isolation

---

## Phase 2 — CLI and gate-summary enablement

### Objective
Expose reporting to users and enrich dry-run output without touching gate enforcement logic.

### Milestone M3 — CLI progress-file option
1. Add `--progress-file` to `superclaude roadmap run`.
2. Set default to `{output_dir}/progress.json`.
3. Validate parent directory before pipeline start.
4. Define startup behavior:
   - overwrite on fresh run
   - append/preserve on `--resume`

### Milestone M4 — Gate summary support for dry-run
1. Add additive `summary()` method to gate constants in `gates.py`.
2. Produce dry-run Markdown table with:
   - Step
   - Gate Tier
   - Required Fields
   - Semantic Checks
3. Include conditional steps:
   - remediate
   - certify
4. Mark conditional execution explicitly.

### Deliverables
- Updated CLI interface
- Updated dry-run reporting
- Additive gate summary API

### Dependencies
- M3 depends on M1 resume semantics
- M4 depends on gate summary contract decisions from M1

### Exit criteria
- CLI validates pathing before execution
- Dry-run output is complete and deterministic
- No gate validation behavior changed

---

## Phase 3 — Executor integration and step-level reporting

### Objective
Wire reporting into pipeline execution using the existing sequential callback path.

### Milestone M5 — Post-step callback integration
1. Connect progress reporter to `execute_pipeline()` callback mechanism.
2. Ensure each completed step emits:
   - `step_id`
   - `status`
   - `duration_ms`
   - `gate_verdict`
   - `output_file`
3. Confirm parallel steps produce independent entries while callback writes remain sequential.
4. Create progress file only on first completed step.

### Deliverables
- Executor-to-progress integration
- step completion reporting
- sequential callback safety verification

### Dependencies
- Depends on M2 infrastructure
- Depends on M3 CLI setup

### Exit criteria
- Parallel generate steps are reported correctly
- No concurrent file corruption
- Step completion order is faithfully represented

---

## Phase 4 — Domain-specific reporting enrichment

### Objective
Capture the higher-value auditability features once the base path is stable.

### Milestone M6 — Deviation and remediation reporting
1. Capture each deviation-analysis iteration as a sub-report.
2. Record convergence loop pass count.
3. When remediation executes, include:
   - `trigger_reason`
   - `finding_count`
4. Ensure remediation entry is written only when remediation actually runs.
5. Make certification reference the remediation instance it validates.

### Milestone M7 — Wiring verification reporting
1. Include wiring metadata in wiring step entry:
   - `unwired_count`
   - `orphan_count`
   - `blocking_count`
   - `rollout_mode`
2. Ensure gate verdict reflects wiring semantic-check outcomes.

### Deliverables
- deviation sub-reporting
- remediation linkage
- wiring gate reporting enrichment

### Dependencies
- Strongly depends on M1 schema decisions
- Depends on M5 execution callback wiring

### Exit criteria
- All required enriched fields are present when applicable
- Conditional entries appear only when executed
- Wiring verdict and metadata are traceable in progress output

---

## Phase 5 — Validation, performance, and hardening

### Objective
Prove the design meets integrity, latency, and compatibility expectations.

### Milestone M8 — Verification and non-functional hardening
1. Validate write latency remains under 50ms per step.
2. Validate crash safety under interruption scenarios.
3. Validate resume behavior against existing progress state.
4. Validate dry-run table completeness.
5. Validate no regression in existing roadmap pipeline behavior.
6. Validate backward compatibility of gate APIs.

### Deliverables
- targeted validation suite
- performance comparison results
- compatibility sign-off

### Dependencies
- Depends on all prior milestones

### Exit criteria
- All functional and non-functional requirements pass
- No unresolved contract ambiguity remains
- Solution is ready for release gating

# 3. Risk assessment and mitigation strategies

## Risk register

### R-001 — Schema ambiguity causes rework
**Risk:** Undefined structure for deviation sub-entries and metadata placement leads to implementation churn and brittle tests.

**Impact:** High  
**Likelihood:** High

**Mitigations**
1. Freeze schema in Phase 0 before code changes.
2. Create concrete JSON examples for:
   - normal run
   - resumed run
   - remediated run
   - crash mid-pipeline
3. Use acceptance fixtures derived from those examples.

---

### R-002 — Resume behavior conflicts with overwrite semantics
**Risk:** Fresh-run overwrite and `--resume` append semantics are inconsistent.

**Impact:** High  
**Likelihood:** Medium

**Mitigations**
1. Explicitly define precedence: `--resume` overrides overwrite behavior.
2. Validate this at CLI argument handling boundary.
3. Add dedicated tests for:
   - existing file + fresh run
   - existing file + `--resume`
   - missing file + `--resume`

---

### R-003 — Reporting layer corrupts or delays pipeline execution
**Risk:** Callback integration introduces ordering issues or excessive write latency.

**Impact:** High  
**Likelihood:** Medium

**Mitigations**
1. Keep reporting synchronous and callback-bound only.
2. Avoid any new threading or async behavior.
3. Benchmark write overhead per step.
4. Keep data model lean and serialization deterministic.

---

### R-004 — Crash-safety implementation is only nominal
**Risk:** JSON becomes partially written or invalid under interruption.

**Impact:** High  
**Likelihood:** Medium

**Mitigations**
1. Use temp-file + `os.replace()` only.
2. Validate crash scenarios with interruption-style tests.
3. Avoid append-based JSON mutation.

---

### R-005 — Gate summary addition accidentally alters validation code paths
**Risk:** Adding `summary()` creates coupling with existing gate logic.

**Impact:** Medium  
**Likelihood:** Low

**Mitigations**
1. Keep `summary()` purely additive and read-only.
2. Avoid changing existing gate method signatures.
3. Add compatibility tests around current gate usage.

---

### R-006 — Conditional-step reporting becomes semantically inconsistent
**Risk:** remediate/certify reporting appears when steps are skipped or lacks linkage.

**Impact:** Medium  
**Likelihood:** Medium

**Mitigations**
1. Define conditional-step write rules explicitly.
2. Require explicit references between certification and remediation when both exist.
3. Test skipped vs executed branches separately.

# 4. Resource requirements and dependencies

## Engineering resources

1. **Primary architect/maintainer**
   - Owns schema decisions
   - Confirms integration boundaries
   - Reviews backward compatibility

2. **Python implementation engineer**
   - Implements dataclasses, serialization, CLI wiring, executor callback integration

3. **QA/validation support**
   - Builds crash-safety, resume, and latency validation coverage
   - Confirms dry-run output contract

## Technical dependencies

1. Existing `execute_pipeline()` post-step callback mechanism
2. Existing CLI command surface for `superclaude roadmap run`
3. Existing gate constants in `gates.py`
4. Existing wiring gate configuration and semantic-check outputs
5. Existing convergence/spec-fidelity loop signals for deviation/remediation

## Architectural dependencies

1. `commands.py → executor.py → progress.py`
2. `progress.py → models.py, gates.py`
3. `executor.py → audit/wiring_gate.py`

## Environmental requirements

1. UV-based Python workflow
2. Existing test harness for roadmap pipeline
3. Real eval-style validation where feasible, not only isolated unit assertions

# 5. Success criteria and validation approach

## Success criteria

### Functional success
1. Progress file is created on first completed step.
2. File remains valid JSON after every write.
3. Every completed step records required base fields.
4. Parallel generate steps are represented independently and accurately.
5. `--progress-file` works with default and custom paths.
6. Dry-run emits a complete Markdown gate summary including conditional steps.
7. Deviation-analysis iterations are captured with pass-count visibility.
8. Remediation reporting appears only when remediation runs.
9. Certification references the remediation it validates.
10. Wiring step includes all required wiring metadata.
11. `--resume` preserves prior entries and appends correctly.

### Non-functional success
1. Progress write overhead stays below 50ms per step.
2. Atomic write behavior survives crash/interruption scenarios.
3. `progress.py` has no import side effects.
4. Existing gate behavior remains unchanged.
5. Callback sequencing prevents file corruption.

## Validation approach

### Validation stream 1 — Contract validation
1. Validate generated JSON against the agreed schema.
2. Use golden examples for:
   - fresh run
   - resumed run
   - remediated run
   - wiring-failure run
   - interrupted run

### Validation stream 2 — Integration validation
1. Exercise `superclaude roadmap run` with:
   - default progress path
   - custom progress path
   - `--dry-run`
   - `--resume`
2. Confirm end-to-end artifact correctness.

### Validation stream 3 — Failure-mode validation
1. Simulate interruption between steps.
2. Confirm file remains parseable JSON.
3. Confirm `completed` remains `false` for interrupted runs.

### Validation stream 4 — Performance validation
1. Measure step duration deltas with and without reporting.
2. Confirm overhead stays within NFR target.

### Validation stream 5 — Compatibility validation
1. Verify additive `summary()` does not affect existing gate consumers.
2. Verify no signature changes in existing gate logic.
3. Verify no unintended behavior changes in executor path.

# 6. Timeline estimates per phase

Given the moderate complexity and limited blast radius, the work should be planned as a short, dependency-aware sequence rather than a broad parallel effort.

## Estimated phase breakdown

1. **Phase 0 — Specification alignment and contract freeze**
   - Estimate: **0.5-1 day**
   - Critical because it removes the highest rework risk

2. **Phase 1 — Core progress infrastructure**
   - Estimate: **1 day**
   - Can proceed quickly once schema is frozen

3. **Phase 2 — CLI and gate-summary enablement**
   - Estimate: **0.5-1 day**
   - Two parallelizable tracks:
     - CLI option
     - gate `summary()` support

4. **Phase 3 — Executor integration and step-level reporting**
   - Estimate: **0.5-1 day**
   - Sequential dependency on Phases 1 and 2

5. **Phase 4 — Domain-specific reporting enrichment**
   - Estimate: **1 day**
   - Higher uncertainty due to convergence/remediation semantics

6. **Phase 5 — Validation, performance, and hardening**
   - Estimate: **1 day**
   - Includes crash-safety and resume verification

## Total estimate
- **Best case:** 4.5 days
- **Expected:** 5-6 days
- **With ambiguity-driven rework:** 6-7 days

## Milestone sequencing summary

1. **M1** — Contract freeze
2. **M2** — `progress.py` foundation
3. **M3 + M4** — CLI and dry-run/gate summary in parallel
4. **M5** — executor callback wiring
5. **M6 + M7** — deviation/remediation and wiring enrichment
6. **M8** — validation and release readiness

## Recommended go/no-go checkpoints

1. **Checkpoint A after M1**
   - Proceed only if schema ambiguities are resolved

2. **Checkpoint B after M5**
   - Proceed only if base reporting is correct and stable

3. **Checkpoint C after M8**
   - Release only if crash safety, resume semantics, and latency targets are met

This roadmap keeps the implementation architecturally narrow, preserves existing pipeline behavior, and front-loads ambiguity resolution so the team does not pay integration costs twice.
