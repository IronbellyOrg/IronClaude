---
spec_source: extraction.md
complexity_score: 0.45
primary_persona: architect
---

# 1. Executive Summary

This roadmap delivers a moderate-scope enhancement to the `superclaude roadmap run` pipeline by adding durable progress reporting, dry-run gate transparency, and richer conditional-step observability without changing gate enforcement behavior.

From an architecture perspective, the safest implementation is to:
1. Introduce a dedicated `progress.py` module with atomic single-file JSON persistence.
2. Reuse the existing `execute_pipeline()` callback path for all progress events.
3. Keep the data contract extensible through `StepProgress.metadata` rather than widening the core schema repeatedly.
4. Isolate CLI parsing, progress persistence, dry-run rendering, and executor wiring into separate responsibilities to avoid circular dependencies and regression risk.

The main architectural risk is not implementation complexity; it is requirements ambiguity around sub-entry schema, remediation trigger semantics, and `--resume` overwrite behavior. These must be resolved early to prevent rework in both the data model and acceptance tests.

## Strategic Outcome

At completion, the roadmap pipeline should provide:
- Crash-safe `progress.json` state after every step write.
- Deterministic reporting for normal, parallel, and conditional pipeline steps.
- Inline dry-run Markdown visibility into gate tiers and semantic checks.
- Resume-aware progress handling with clear overwrite vs append semantics.
- Testable observability with minimal blast radius to the existing pipeline.

---

# 2. Phased Implementation Plan with Milestones

## Phase 0 — Specification Clarification and Contract Freeze

### Objective
Resolve blocking ambiguities before implementation begins.

### Milestones
1. **M1 — Progress Contract Decisions**
   - Define deviation iteration sub-entry schema.
   - Define where sub-entries live:
     - preferred: `StepProgress.metadata.deviation_iterations[]`
     - alternative: separate top-level list.
   - Define certification-to-remediation reference field.
   - Define required metadata key names for:
     - remediation
     - wiring
     - convergence loop
     - certification linkage

2. **M2 — Behavioral Clarifications**
   - Resolve `--resume` semantics:
     - fresh run overwrites
     - resumed run appends/preserves
   - Resolve “significant findings” threshold:
     - HIGH only
     - or HIGH + MEDIUM

### Deliverables
- Approved progress JSON schema.
- Approved conditional-step semantics matrix.
- Acceptance note for `--resume` behavior.

### Exit Criteria
- No unresolved blockers from Section 5 of the extraction.
- Test assertions can be written deterministically.

### Architect Notes
This phase is mandatory. Skipping it risks redesigning the progress model mid-sprint.

---

## Phase 1 — Core Progress Data Model and Persistence Foundation

### Objective
Create the progress subsystem with strong correctness guarantees before wiring it into execution.

### Milestones
1. **M3 — Data Model Definition**
   - Implement `PipelineProgress` with:
     - `spec_file`
     - `started_at`
     - `steps`
     - `completed`
   - Implement `StepProgress` with:
     - `step_id`
     - `status`
     - `duration_ms`
     - `gate_verdict`
     - `output_file`
     - `metadata`

2. **M4 — Atomic Persistence Layer**
   - Create progress writer in `progress.py`.
   - Use write-to-temp + `os.replace()`.
   - Ensure file remains valid JSON after every write.
   - Overwrite existing file on fresh initialization.
   - Support load-and-append path for `--resume`.

3. **M5 — Serialization and Import Safety**
   - Add deterministic serialization helpers.
   - Ensure zero I/O on import.
   - Keep persistence instantiation explicit at runtime only.

### Deliverables
- `progress.py`
- Data model serialization tests
- Atomic write tests
- Import-side-effect regression test

### Exit Criteria
- Progress file can be created, rewritten, and resumed safely.
- Write latency path is instrumented and meets target design expectations.

### Architect Notes
This phase establishes the contract boundary. Everything else should depend on this module, not duplicate file-writing behavior elsewhere.

---

## Phase 2 — CLI and Dry-Run Reporting Integration

### Objective
Expose the feature through the CLI and enrich dry-run output without touching gate enforcement code.

### Milestones
1. **M6 — CLI Option Integration**
   - Add `--progress-file` to `superclaude roadmap run`.
   - Default to `{output_dir}/progress.json`.
   - Validate parent directory before pipeline start.
   - Preserve special `--resume` handling if enabled.

2. **M7 — Gate Summary Capability**
   - Add additive `summary()` method to gate constants.
   - Preserve existing signatures and enforcement behavior.
   - Standardize return structure for dry-run table generation.

3. **M8 — Dry-Run Markdown Table**
   - Render inline table with:
     - Step
     - Gate Tier
     - Required Fields
     - Semantic Checks
   - Include conditional steps:
     - remediate
     - certify
   - Explicitly mark them as conditional.

### Deliverables
- CLI parsing changes
- Gate summary interface
- Dry-run report renderer

### Exit Criteria
- `--dry-run` produces complete and readable gate summary output.
- `--progress-file` path validation fails early and clearly.

### Architect Notes
This phase should proceed partly in parallel:
- CLI option work
- gate `summary()` work
Then converge in dry-run rendering.

---

## Phase 3 — Executor Wiring and Step-Level Progress Reporting

### Objective
Connect the progress subsystem to the existing execution flow through the approved callback mechanism.

### Milestones
1. **M9 — Executor Callback Wiring**
   - Integrate progress writes through existing `execute_pipeline()` callback.
   - Guarantee sequential callback invocation is preserved.
   - Avoid threads, watchers, locks, or async additions.

2. **M10 — Standard Step Reporting**
   - Emit entry after every completed step with:
     - `step_id`
     - `status`
     - `duration_ms`
     - `gate_verdict`
     - `output_file`
   - Create progress file on first step completion.

3. **M11 — Parallel Step Handling**
   - Ensure `generate-A` and `generate-B` emit independent entries.
   - Preserve correct timing attribution.
   - Validate no write corruption despite parallel execution upstream.

### Deliverables
- Executor integration changes
- Standard and parallel-step reporting tests
- Sequential callback safety verification

### Exit Criteria
- All non-conditional steps appear correctly in `progress.json`.
- Parallel branches are represented independently and validly.

### Architect Notes
The architecture relies on serialized callback execution as the concurrency boundary. Do not leak persistence concerns into parallel worker logic.

---

## Phase 4 — Conditional and Nested Reporting Enhancements

### Objective
Add richer progress detail for convergence loops, remediation, certification, and wiring verification.

### Milestones
1. **M12 — Deviation Analysis Sub-Reporting**
   - Record each convergence-loop iteration as a nested sub-entry.
   - Record total pass count.
   - Keep nesting within the approved `metadata` contract unless Phase 0 decides otherwise.

2. **M13 — Remediation Trigger Reporting**
   - Write remediation entry only when remediation executes.
   - Include:
     - `trigger_reason`
     - `finding_count`

3. **M14 — Certification Linkage**
   - Add explicit reference from certification step to the remediation instance it validates.

4. **M15 — Wiring Verification Metadata**
   - Add wiring progress metadata:
     - `unwired_count`
     - `orphan_count`
     - `blocking_count`
     - `rollout_mode`
   - Ensure gate verdict reflects `WIRING_GATE` semantic result accurately.

### Deliverables
- Extended metadata schema usage
- Conditional-step integration tests
- Nested reporting tests
- Wiring metadata verification tests

### Exit Criteria
- Conditional and loop-driven behavior is fully observable in the progress file.
- Certification/remediation lineage is traceable.

### Architect Notes
This is the most schema-sensitive phase. It should not begin until Phase 0 decisions are complete.

---

## Phase 5 — Validation, Performance, and Release Hardening

### Objective
Prove correctness, backward compatibility, and operational fitness.

### Milestones
1. **M16 — Functional Validation**
   - Validate all FRs and implicit FRs against real CLI pipeline runs.
   - Include `--resume` scenario coverage.

2. **M17 — Performance and Crash-Safety Validation**
   - Measure per-write latency target:
     - `< 50ms` per step
   - Verify valid JSON after interruption scenarios.

3. **M18 — Release Readiness Review**
   - Confirm no gate enforcement logic changed.
   - Confirm no import-time I/O.
   - Confirm single-file output behavior.
   - Confirm additive compatibility of `summary()`.

### Deliverables
- Real eval coverage
- Performance evidence
- Release-readiness checklist
- Final acceptance report

### Exit Criteria
- All required evals pass.
- No regression in existing pipeline behavior.
- Feature is releaseable behind normal CLI usage without hidden migration steps.

### Architect Notes
Given prior project feedback, validation must exercise the actual CLI pipeline and artifact generation rather than relying on narrow unit-only coverage.

---

# 3. Risk Assessment and Mitigation Strategies

## High-Priority Risks

1. **Schema ambiguity causes rework**
   - Risk:
     - Undefined deviation sub-entry structure
     - Undefined certification reference mechanism
     - Unclear metadata contract
   - Impact:
     - Data model churn
     - Test churn
     - downstream consumer confusion
   - Mitigation:
     - Freeze JSON schema in Phase 0
     - Add representative fixture examples before coding
     - Treat schema changes after Phase 1 as change-controlled

2. **`--resume` semantics create destructive behavior**
   - Risk:
     - overwrite vs append contradiction leads to loss of existing progress
   - Impact:
     - broken resumability
     - inaccurate audit trail
   - Mitigation:
     - Explicitly split behavior:
       - fresh run overwrites
       - `--resume` preserves and appends
     - Add dedicated acceptance tests for both flows

3. **Parallel execution corrupts progress file**
   - Risk:
     - concurrent writes or non-deterministic callback invocation
   - Impact:
     - invalid JSON
     - missing or duplicated step entries
   - Mitigation:
     - Centralize all writes behind one callback path
     - Preserve sequential invocation invariant
     - Test generate-A/generate-B under realistic execution

4. **Performance regression from full-file atomic rewrites**
   - Risk:
     - repeated atomic rewrites exceed `<50ms` target
   - Impact:
     - slower pipeline
   - Mitigation:
     - Keep payload compact
     - Avoid expensive reformatting or redundant serialization
     - Measure early with realistic step counts

## Medium-Priority Risks

5. **Backward compatibility break in gate objects**
   - Risk:
     - `summary()` implementation changes existing interfaces or assumptions
   - Mitigation:
     - Add only additive method
     - No signature changes
     - Regression tests against existing gate use paths

6. **Conditional-step reporting drifts from actual execution logic**
   - Risk:
     - remediation/certification entries appear when not executed
   - Mitigation:
     - Emit progress only from actual execution points
     - Never infer execution from planning state alone

7. **Hidden circular dependency across modules**
   - Risk:
     - `commands.py → executor.py → progress.py → models.py/gates.py` direction gets violated
   - Mitigation:
     - Keep `progress.py` free of command-layer imports
     - Treat dependency direction as an architectural rule checked in code review

## Low-Priority Risks

8. **Progress file growth over many resumes**
   - Mitigation:
     - Accept as known limitation for this release
     - Document as future enhancement, not current scope

---

# 4. Resource Requirements and Dependencies

## Engineering Roles

1. **Primary backend/CLI engineer**
   - Owns data model, persistence layer, CLI integration, executor wiring.

2. **QA / evaluation engineer**
   - Owns real pipeline validation, crash-safety checks, and resume behavior coverage.

3. **Architecture reviewer**
   - Confirms dependency direction, scope discipline, and no gate-enforcement drift.

## Code Dependencies

1. Existing `execute_pipeline()` callback mechanism
2. Existing roadmap CLI command parsing path
3. Existing gate constants and semantic check definitions
4. Existing dry-run output flow
5. Existing `--resume` pipeline behavior, if present elsewhere in command flow

## Technical Dependencies

1. Filesystem support for atomic replace via `os.replace()`
2. Stable JSON serialization behavior
3. Reliable step timing measurement around callback integration
4. Test harness capable of validating actual artifact output

## External/Decision Dependencies

1. Product/spec decision on deviation sub-entry schema
2. Product/spec decision on “significant findings” threshold
3. Product/spec decision on certification reference field
4. Product/spec decision on `--resume` overwrite exception

## Recommended Work Sequencing

1. Contract decisions
2. Progress foundation
3. CLI and gate summary in parallel
4. Executor wiring
5. Nested/conditional reporting
6. Full validation

This sequencing minimizes rework and preserves the stated implementation-order constraint in the extraction.

---

# 5. Success Criteria and Validation Approach

## Success Criteria

1. **Progress persistence correctness**
   - `progress.json` exists after first completed step.
   - File remains valid JSON after every write.
   - Fresh run overwrites prior file unless `--resume` is active.
   - Resume run preserves prior entries and appends new ones.

2. **Coverage of execution states**
   - Standard steps report required fields.
   - Parallel steps report distinct entries with correct durations.
   - Conditional steps report only when executed.
   - Deviation iterations are visible and countable.
   - Certification references its remediation target.
   - Wiring metadata is complete and accurate.

3. **Dry-run transparency**
   - Markdown table is emitted for `--dry-run`.
   - All steps, including conditional ones, are listed.
   - Gate tiers, required fields, and semantic checks are complete.

4. **Non-functional compliance**
   - Atomic writes use temp file + `os.replace()`.
   - Per-step write cost remains below 50ms.
   - `progress.py` performs no import-time I/O.
   - Output remains single-file JSON.

5. **Architectural integrity**
   - No modifications to `pipeline/gates.py` enforcement behavior.
   - No new concurrency model introduced.
   - No circular imports introduced.

## Validation Approach

1. **Real pipeline evals**
   - Run the actual CLI pipeline end-to-end.
   - Verify generated artifacts as third-party verifiable outputs.

2. **Contract tests**
   - Validate JSON schema and required fields.
   - Verify metadata structures for:
     - deviation iterations
     - remediation
     - certification
     - wiring

3. **Behavioral scenario tests**
   - Fresh run
   - Resume run
   - Dry run
   - Parallel branch execution
   - Remediation path
   - Certification path
   - Wiring failure/pass cases

4. **Resilience tests**
   - Simulate interruption between writes.
   - Confirm resulting file is always parseable JSON.

5. **Performance checks**
   - Compare step durations with and without progress writes.
   - Record worst-case write latency.

6. **Regression checks**
   - Confirm existing gate enforcement results are unchanged.
   - Confirm imports do not create files.
   - Confirm existing CLI behavior remains intact when defaults are used.

---

# 6. Timeline Estimates per Phase

Given the extraction’s stated single-sprint scope, the roadmap fits into one implementation sprint with front-loaded clarification.

## Phase Estimates

1. **Phase 0 — Specification Clarification and Contract Freeze**
   - Estimate: 0.5 day
   - Output:
     - schema decisions
     - resolved acceptance semantics

2. **Phase 1 — Core Progress Data Model and Persistence Foundation**
   - Estimate: 1 day
   - Output:
     - `progress.py`
     - data model and atomic write foundation

3. **Phase 2 — CLI and Dry-Run Reporting Integration**
   - Estimate: 0.5-1 day
   - Output:
     - `--progress-file`
     - gate `summary()`
     - dry-run table

4. **Phase 3 — Executor Wiring and Step-Level Progress Reporting**
   - Estimate: 0.5-1 day
   - Output:
     - callback integration
     - standard and parallel-step reporting

5. **Phase 4 — Conditional and Nested Reporting Enhancements**
   - Estimate: 1 day
   - Output:
     - deviation loop sub-reporting
     - remediation/certification linkage
     - wiring metadata

6. **Phase 5 — Validation, Performance, and Release Hardening**
   - Estimate: 1 day
   - Output:
     - real eval evidence
     - crash/performance validation
     - release readiness review

## Total Estimate
- **Overall:** 4.5-5.5 engineering days
- **Delivery shape:** single sprint, provided Phase 0 ambiguities are resolved immediately

## Critical Path

1. Clarify ambiguous schema and resume semantics
2. Build progress model/persistence layer
3. Wire executor callback
4. Add nested/conditional reporting
5. Validate with real CLI evals

## Parallelization Opportunities

1. **Phase 2 parallel track**
   - Engineer A: CLI `--progress-file`
   - Engineer B: gate `summary()` + dry-run renderer

2. **Phase 5 parallel track**
   - Engineer A: functional evals
   - Engineer B: performance + crash-safety checks

## Timeline Risk Adjusters

Schedule expands if:
- schema decisions are delayed,
- `--resume` behavior is disputed,
- or downstream consumers require a stricter progress schema than currently implied.

---

# Recommended Milestone Summary

1. **M1-M2** — Resolve schema and semantic ambiguities
2. **M3-M5** — Build crash-safe progress foundation
3. **M6-M8** — Expose CLI and dry-run visibility
4. **M9-M11** — Integrate executor callback reporting
5. **M12-M15** — Add conditional and nested observability
6. **M16-M18** — Validate against real pipeline runs and release criteria

This is the architecturally conservative path: minimal blast radius, explicit contracts first, and validation anchored in the real pipeline rather than isolated helper tests.
