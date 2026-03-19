---
spec_source: "eval-spec.md"
complexity_score: 0.45
primary_persona: architect
---

# 1. Executive Summary

This roadmap delivers a **crash-safe, additive progress reporting capability** for `superclaude roadmap run` with minimal architectural disruption and strong validation coverage. The work is medium complexity because the core implementation is straightforward, but correctness depends on careful integration across the roadmap executor, convergence loop, gate summaries, and wiring verification.

From an architect perspective, the priorities are:

1. **Preserve existing pipeline behavior** while adding observability.
2. **Guarantee file integrity** through atomic JSON writes.
3. **Contain scope** to the mandated integration surface, especially the single new module constraint.
4. **Resolve specification ambiguities early** so the implementation remains deterministic and testable.
5. **Prove behavior with real CLI-driven evals**, not isolated unit-only validation.

The roadmap is structured into six phases: requirements closure, architecture/data model design, core implementation, special-case integration, validation/performance hardening, and release readiness.

---

# 2. Phased Implementation Plan with Milestones

## Phase 1 — Requirements Closure and Architectural Alignment

### Objectives
1. Eliminate open ambiguities that would otherwise create rework.
2. Confirm architectural constraints before code changes begin.
3. Lock the acceptance contract for progress reporting and dry-run output.

### Key Actions
1. Confirm the exact JSON schema for:
   - deviation-analysis sub-entries
   - remediation metadata
   - certification linkage to remediation
   - step-level metadata conventions
2. Resolve contradictory behavior for:
   - fresh run overwrite semantics
   - `--resume` handling of existing progress
3. Define remediation trigger semantics precisely:
   - whether “significant findings” means HIGH severity only
   - whether finding counts include all findings or only blocking findings
4. Confirm dry-run table scope:
   - full step list
   - conditional step labeling
   - semantic check representation format

### Deliverables
- Approved progress schema definition
- Resolved behavior notes for overwrite vs resume
- Acceptance mapping from FR/NFR/SC to implementation points

### Milestone
- **M1: Spec ambiguities closed and implementation contract frozen**

### Timeline Estimate
- **0.5-1 day**

---

## Phase 2 — Progress Architecture and Data Model Design

### Objectives
1. Design a clean, additive progress subsystem within the single-file constraint.
2. Ensure module boundaries remain compliant with dependency direction rules.
3. Keep import behavior side-effect free.

### Key Actions
1. Create `src/superclaude/cli/roadmap/progress.py` containing:
   - `StepProgress`
   - `PipelineProgress`
   - serialization helpers
   - atomic write implementation
   - progress update orchestration
2. Define a normalized entry structure for all steps:
   - `step_id`
   - `status`
   - `duration_ms`
   - `gate_verdict`
   - `output_file`
   - optional metadata container
3. Design special-step metadata extensions for:
   - convergence iterations
   - remediation execution
   - certification linkage
   - wiring verification counts and rollout mode
4. Define overwrite lifecycle:
   - initialize fresh in-memory state
   - first completed step creates file
   - all subsequent writes replace atomically
5. Add gate summary representation as an additive interface in `gates.py`

### Architectural Decisions
- Use **in-memory aggregation plus atomic replace**, not incremental append.
- Treat the progress writer as a **pure callback sink**, not a pipeline controller.
- Keep special-case logic **localized to progress serialization**, not spread across executor internals.

### Deliverables
- `progress.py` design finalized
- Data model schema aligned to eval expectations
- Gate summary contract defined

### Milestone
- **M2: Progress subsystem design approved**

### Timeline Estimate
- **0.5-1 day**

---

## Phase 3 — Core CLI and Executor Integration

### Objectives
1. Wire progress reporting into the main roadmap pipeline without changing execution semantics.
2. Provide configurable progress-file path handling.
3. Support valid JSON creation from the first completed step onward.

### Key Actions
1. Add `--progress-file` to `src/superclaude/cli/roadmap/commands.py`:
   - `click.Path`
   - default `{output_dir}/progress.json`
   - parent directory validation before pipeline start
2. Update `src/superclaude/cli/roadmap/executor.py` to:
   - construct progress reporter
   - invoke post-step callback after each completed step
   - pass step result data without changing step signatures globally
3. Ensure overwrite semantics for existing progress file on fresh run.
4. Capture accurate per-step durations, including parallel-generated steps reported independently.
5. Guarantee sequential callback invocation remains the only write path.

### Deliverables
- CLI option functional
- Executor callback integration complete
- Default and custom progress-file paths operational

### Milestone
- **M3: Base progress reporting works for standard steps**

### Timeline Estimate
- **1-1.5 days**

---

## Phase 4 — Special-Case Step Support and Dry-Run Visibility

### Objectives
1. Complete support for the steps with additional semantic requirements.
2. Expose roadmap gate requirements clearly during dry-run.
3. Preserve backward compatibility in gate infrastructure.

### Key Actions
1. Integrate convergence loop reporting via `src/superclaude/cli/roadmap/convergence.py`:
   - record each deviation-analysis iteration
   - include pass/iteration count
   - align nesting format with the resolved schema
2. Implement remediation progress capture:
   - only emit remediate entry when remediation actually executes
   - include `trigger_reason`
   - include `finding_count`
3. Implement certification linkage:
   - certification step references remediation artifact or step instance it validates
4. Implement wiring verification enrichment using `src/superclaude/cli/audit/wiring_gate.py`:
   - `unwired_count`
   - `orphan_count`
   - `blocking_count`
   - `rollout_mode`
   - gate verdict sourced from wiring semantic result
5. Add additive `summary()` support in `src/superclaude/cli/roadmap/gates.py`
6. Extend dry-run output to a Markdown table with:
   - Step
   - Gate Tier
   - Required Fields
   - Semantic Checks
   - conditional labeling for remediate/certify

### Deliverables
- Convergence sub-entry reporting
- Remediation/certification metadata
- Wiring verification reporting
- Full dry-run gate table

### Milestone
- **M4: All special-case requirements implemented**

### Timeline Estimate
- **1-1.5 days**

---

## Phase 5 — Validation, Performance, and Failure-Safety Hardening

### Objectives
1. Prove the implementation satisfies functional and nonfunctional requirements.
2. Verify crash-safety and import cleanliness.
3. Confirm additive behavior with no regressions to existing roadmap pipeline behavior.

### Key Actions
1. Add or update tests covering:
   - default progress-file behavior
   - custom progress-file path
   - overwrite behavior
   - valid JSON after every write
   - independent timings for `generate-A` and `generate-B`
   - dry-run Markdown table correctness
   - remediation/certification conditional behavior
   - wiring verification metadata
   - convergence iteration capture
2. Add crash-interruption validation:
   - simulate interrupted write path
   - verify JSON remains parseable
3. Add import-side-effect validation:
   - import `superclaude.cli.roadmap.progress`
   - confirm zero file I/O at import time
4. Add performance validation:
   - compare step execution with and without progress reporting
   - confirm per-step overhead remains under 50ms
5. Run real eval-style CLI tests to satisfy project preference for pipeline-level validation

### Deliverables
- Passing targeted test suite
- Performance evidence
- Crash-safety evidence
- Regression confidence for pipeline behavior

### Milestone
- **M5: Validation evidence complete and requirements demonstrably met**

### Timeline Estimate
- **1-2 days**

---

## Phase 6 — Release Readiness and Adoption

### Objectives
1. Finalize rollout with minimal operational risk.
2. Ensure development copies and source-of-truth remain synchronized.
3. Establish confidence for downstream users and future maintenance.

### Key Actions
1. Verify source-of-truth changes are in `src/superclaude/` first.
2. Run `make sync-dev` and `make verify-sync`.
3. Run focused regression suite plus full relevant roadmap/audit tests.
4. Validate sample run output artifacts for maintainability and operator clarity.
5. Confirm no unintended API or CLI regressions.
6. Document any resolved schema conventions implicitly through tests and artifact examples.

### Deliverables
- Synced source and dev copies
- Verified implementation readiness
- Stable artifact behavior for future evaluations

### Milestone
- **M6: Feature ready for merge and downstream use**

### Timeline Estimate
- **0.5 day**

---

# 3. Risk Assessment and Mitigation Strategies

## Risk 1 — Progress reporting slows pipeline execution
**Severity:** Low

### Architectural Concern
Observability features often expand over time and can quietly degrade performance if write paths are not tightly bounded.

### Mitigation
1. Keep writes strictly atomic and local-file only.
2. Serialize from in-memory model, not repeated deep reconstruction.
3. Measure overhead in validation and enforce `< 50ms` per step.
4. Avoid additional background workers, locks, or polling mechanisms.

### Contingency
- If overhead approaches threshold, optimize serialization scope before changing architecture.

---

## Risk 2 — Parallel step handling corrupts progress state
**Severity:** Medium

### Architectural Concern
Parallel execution often introduces accidental shared-state races even if the spec states callbacks are sequential.

### Mitigation
1. Treat `execute_pipeline()` callback order as the sole serialization boundary.
2. Ensure the progress writer has no independent concurrency logic.
3. Add explicit tests proving independent entries and correct timings for `generate-A` and `generate-B`.

### Contingency
- If callback order assumptions prove weaker than expected, centralize callback dispatch rather than introducing file locks.

---

## Risk 3 — Additive gate summary change breaks compatibility
**Severity:** High

### Architectural Concern
`gates.py` likely participates in multiple flows; even small interface changes can ripple into dry-run and validation behavior.

### Mitigation
1. Make `summary()` purely additive.
2. Do not alter existing gate constant semantics or signatures.
3. Validate existing consumers remain untouched.
4. Use regression tests against dry-run and existing pipeline paths.

### Contingency
- If backward compatibility becomes fragile, move formatting logic outward and keep gates exposing raw data only.

---

## Risk 4 — Undefined deviation schema causes implementation churn
**Severity:** Medium

### Architectural Concern
This is the highest design ambiguity and can infect both data models and tests.

### Mitigation
1. Resolve schema before implementation begins.
2. Prefer a compact, deterministic nested structure.
3. Ensure iteration entries are machine-verifiable and not free-form text blobs.

### Contingency
- If no clarification is available, document and adopt a minimal schema with explicit versioned test assertions.

---

## Risk 5 — Resume behavior contradiction causes artifact inconsistency
**Severity:** Medium

### Architectural Concern
Overwrite vs append semantics affect user expectations, test design, and crash recovery.

### Mitigation
1. Resolve as a first-phase decision.
2. Separate semantics by mode if necessary:
   - fresh run: overwrite
   - resume: merge/append
3. Encode behavior in acceptance tests, not informal assumptions.

### Contingency
- If unresolved, block release rather than ship ambiguous behavior.

---

# 4. Resource Requirements and Dependencies

## Engineering Resources

### Primary Roles
1. **Architect/Lead engineer**
   - Owns schema decisions
   - Guards architectural constraints
   - Approves compatibility strategy
2. **Backend/CLI engineer**
   - Implements progress models and executor wiring
   - Adds CLI option handling
3. **QA/test engineer**
   - Builds real CLI validation coverage
   - Confirms crash-safety, timing, and artifact integrity

### Recommended Staffing
- **1 primary implementer**
- **1 reviewer with roadmap pipeline context**
- **1 validation pass focused on real eval behavior**

---

## Technical Dependencies

1. `src/superclaude/cli/roadmap/executor.py`
   - callback integration point
   - step completion lifecycle
2. `src/superclaude/cli/roadmap/commands.py`
   - `--progress-file` CLI registration and validation
3. `src/superclaude/cli/roadmap/gates.py`
   - additive `summary()` support
4. `src/superclaude/cli/roadmap/models.py`
   - alignment with `StepResult`
5. `src/superclaude/cli/roadmap/convergence.py`
   - deviation iteration reporting
6. `src/superclaude/cli/audit/wiring_gate.py`
   - wiring verification metadata and verdict context
7. Python stdlib `json`
   - deterministic serialization
8. Python stdlib `os.replace()`
   - crash-safe atomic replace

---

## Environmental and Process Dependencies

1. **UV-based execution**
   - all tests and validation must run with `uv`
2. **Source-of-truth sync discipline**
   - edit `src/superclaude/` first
   - then `make sync-dev`
   - then `make verify-sync`
3. **Real CLI eval validation**
   - required by project memory and acceptance expectations

---

# 5. Success Criteria and Validation Approach

## Success Criteria

1. **Progress artifact completeness**
   - Every executed step creates exactly one corresponding progress entry.
2. **Valid JSON after every write**
   - File remains parseable after interruption or crash.
3. **CLI path correctness**
   - Default and custom `--progress-file` paths both work as specified.
4. **Parallel step timing accuracy**
   - `generate-A` and `generate-B` report independent durations.
5. **Dry-run completeness**
   - Markdown table includes all required and conditional steps.
6. **Special-step fidelity**
   - convergence, remediation, certification, and wiring verification all produce required metadata.
7. **No import-time side effects**
   - `progress.py` performs no I/O on import.
8. **Backward compatibility**
   - existing roadmap pipeline behavior remains unchanged aside from additive progress output.
9. **Performance target met**
   - progress reporting overhead remains below 50ms per step.

---

## Validation Approach

### A. Functional Validation
1. Run full roadmap pipeline with default settings.
2. Run full roadmap pipeline with `--progress-file /custom/path.json`.
3. Validate final JSON structure and per-step field population.
4. Verify conditional steps appear only when executed.

### B. Failure-Safety Validation
1. Simulate interruption during write cycle.
2. Parse resulting `progress.json`.
3. Confirm no partial JSON or truncation is observable.

### C. Dry-Run Validation
1. Execute `--dry-run`.
2. Compare Markdown table output against expected gate inventory.
3. Verify conditional steps are explicitly marked.

### D. Performance Validation
1. Benchmark representative steps with reporting disabled vs enabled.
2. Measure per-step delta.
3. Fail validation if average or worst-case overhead exceeds threshold.

### E. Compatibility Validation
1. Run existing roadmap test suite.
2. Run focused audit/wiring tests where integration crosses boundaries.
3. Confirm additive gate summary does not break legacy flows.

### F. Real Eval Validation
1. Prefer CLI-driven end-to-end tests over isolated unit-only proof.
2. Preserve third-party verifiability through artifact inspection.

---

# 6. Timeline Estimates per Phase

## Summary Timeline

1. **Phase 1 — Requirements Closure and Architectural Alignment**
   - **0.5-1 day**

2. **Phase 2 — Progress Architecture and Data Model Design**
   - **0.5-1 day**

3. **Phase 3 — Core CLI and Executor Integration**
   - **1-1.5 days**

4. **Phase 4 — Special-Case Step Support and Dry-Run Visibility**
   - **1-1.5 days**

5. **Phase 5 — Validation, Performance, and Failure-Safety Hardening**
   - **1-2 days**

6. **Phase 6 — Release Readiness and Adoption**
   - **0.5 day**

## Total Estimated Range
- **4.5-7.5 working days**

## Critical Path
1. Resolve open questions
2. Finalize progress schema
3. Implement executor/CLI integration
4. Complete convergence/remediation/wiring special cases
5. Validate crash-safety and performance
6. Sync and release

## Timeline Notes
- The schedule is dominated not by coding volume, but by **ambiguity resolution and evidence gathering**.
- If open questions are resolved immediately, the lower bound is realistic.
- If resume semantics or deviation schema remain unclear, Phase 1 becomes the gating factor for the entire roadmap.

---

# Recommended Implementation Priorities

1. **Resolve OQ-001 and OQ-004 first**  
   These affect data model shape and overwrite semantics, which are foundational.

2. **Implement the base progress writer before special cases**  
   Establish a stable core path for normal steps first.

3. **Treat dry-run and gate summary as contract work, not presentation work**  
   These outputs are part of the validation surface.

4. **Validate via real pipeline execution early**  
   Avoid discovering artifact-shape mismatches late in the cycle.

5. **Protect backward compatibility aggressively**  
   This feature is additive; any behavioral regression should block rollout.

---

# Final Architectural Recommendation

Proceed with a **single-module, callback-driven progress subsystem** centered in `src/superclaude/cli/roadmap/progress.py`, using **in-memory state plus atomic JSON replacement** as the core persistence strategy. This best satisfies the explicit constraints, minimizes blast radius, and preserves future maintainability. The only meaningful blockers are the unresolved schema and resume semantics; those should be treated as pre-implementation decisions, not deferred coding details.
