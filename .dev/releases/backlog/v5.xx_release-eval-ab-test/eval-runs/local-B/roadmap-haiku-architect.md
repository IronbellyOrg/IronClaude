---
spec_source: "eval-spec.md"
complexity_score: 0.45
primary_persona: architect
---

# 1. Executive Summary

This roadmap delivers progress reporting and dry-run gate visibility for the `superclaude roadmap run` pipeline with minimal architectural disruption. The work is medium complexity because it spans several integration points, introduces one new module, and must preserve crash safety, CLI ergonomics, and gate compatibility without changing core validation behavior.

## Architectural priorities
1. Preserve existing pipeline control flow and callback sequencing.
2. Isolate all new progress logic in `src/superclaude/cli/roadmap/progress.py`.
3. Treat atomic JSON persistence as a hard reliability requirement, not an enhancement.
4. Keep gate changes additive-only via `summary()` support.
5. Resolve seeded ambiguities before implementation crosses fidelity gates.

## Expected outcomes
- A valid `progress.json` written after each completed step.
- A configurable `--progress-file` CLI option with safe validation and sensible defaulting.
- Dry-run output that exposes gate expectations in a deterministic Markdown table.
- Coverage for convergence, remediation, and wiring-specific reporting.
- Benchmarked proof that observability additions do not materially slow execution.

# 2. Phased Implementation Plan with Milestones

## Phase 0 — Specification Closure and Architectural Alignment
**Goal:** Eliminate blockers before code changes.

### Work
1. Confirm resolution path for blocking ambiguities:
   - Deviation sub-entry schema.
   - Remediation trigger threshold for “significant findings.”
   - Resume behavior vs overwrite behavior.
2. Freeze the progress JSON shape:
   - Top-level pipeline structure.
   - Step entry shape.
   - Conditional-step representation.
   - Convergence sub-report representation.
3. Confirm dry-run table contract for all gate definitions.

### Deliverables
- Approved schema decision for progress entries.
- Written decision on remediation threshold.
- Explicit rule for overwrite vs resume.
- Final acceptance checklist mapped to SC-001 through SC-009.

### Milestone
- **M0:** Spec-fidelity approval to implement.

### Timeline estimate
- **0.5 day**

---

## Phase 1 — Progress Reporting Foundation
**Goal:** Build the isolated persistence layer in `progress.py`.

### Work
1. Implement progress data model:
   - `StepProgress`
   - `PipelineProgress`
2. Implement serialization helpers with stable JSON output.
3. Implement atomic writer:
   - Write temp file.
   - Flush/close.
   - Replace with `os.replace()`.
4. Ensure zero import-time I/O.
5. Define overwrite-on-start behavior unless explicit resume exception is approved.

### Architectural notes
- This phase must remain self-contained.
- No observer threads, background writers, or async file coordination.
- Design for sequential callback invocation assumption from executor.

### Deliverables
- `src/superclaude/cli/roadmap/progress.py`
- Unit coverage for serialization and atomic write behavior

### Milestone
- **M1:** Crash-safe progress writer operational in isolation.

### Timeline estimate
- **1 day**

---

## Phase 2 — Pipeline Integration
**Goal:** Connect progress reporting to execution flow without refactoring executor semantics.

### Work
1. Extend pipeline execution integration in:
   - `src/superclaude/cli/roadmap/executor.py`
2. Hook progress writes into step completion callback.
3. Map each completed step to required fields:
   - `step_id`
   - `status`
   - `duration_ms`
   - `gate_verdict`
   - `output_file`
4. Ensure parallel generate steps emit independent entries with correct timing.
5. Add convergence reporting:
   - Record iteration/pass count.
   - Add deviation-analysis sub-entries per agreed schema.
6. Add remediation reporting:
   - `trigger_reason`
   - `finding_count`
   - certification linkage to remediation validation
7. Add wiring verification enrichment:
   - `unwired_count`
   - `orphan_count`
   - `blocking_count`
   - `rollout_mode`

### Architectural notes
- Integration must extend `StepResult` usage, not bypass it.
- Callback order is the guardrail against corruption; do not introduce alternative concurrency paths.

### Deliverables
- Executor integration complete
- Progress output populated across normal, parallel, conditional, and convergence scenarios

### Milestone
- **M2:** End-to-end progress entries emitted for all relevant step types.

### Timeline estimate
- **1.5 days**

---

## Phase 3 — CLI and Dry-Run Visibility
**Goal:** Surface the feature through the public command contract.

### Work
1. Extend `src/superclaude/cli/roadmap/commands.py`:
   - Add `--progress-file PATH`
   - Validate parent directory exists before pipeline starts
   - Default to `{output_dir}/progress.json`
2. Extend `src/superclaude/cli/roadmap/gates.py`:
   - Add additive `summary()` method
   - Preserve all current interfaces
3. Render Markdown dry-run table including:
   - Step
   - Gate Tier
   - Required Fields
   - Semantic Checks
4. Ensure conditional steps are listed and clearly marked.

### Architectural notes
- CLI validation should fail fast before expensive pipeline work starts.
- `summary()` must be purely additive and side-effect free.

### Deliverables
- Updated roadmap CLI contract
- Dry-run gate summary table
- Gate metadata accessible programmatically

### Milestone
- **M3:** CLI feature complete and dry-run contract visible.

### Timeline estimate
- **1 day**

---

## Phase 4 — Validation, Performance, and Reliability Hardening
**Goal:** Prove the implementation satisfies functional and nonfunctional requirements.

### Work
1. Add tests for:
   - First-write creation behavior
   - Valid JSON after every write
   - Custom/default progress file path behavior
   - Directory validation failure
   - Parallel step reporting correctness
   - Convergence sub-entry reporting
   - Remediation conditional reporting
   - Wiring verification metadata
   - Dry-run table completeness
   - No import-time side effects
2. Benchmark write overhead against `< 50ms` target.
3. Simulate interruption/crash during write to prove JSON validity.
4. Validate additive-only gate extension behavior.
5. Run real CLI-driven eval coverage, not gate-only unit abstractions.

### Deliverables
- Automated test evidence for SC-001 through SC-009
- Benchmark results
- Crash-safety verification notes

### Milestone
- **M4:** Validation complete with evidence-backed acceptance.

### Timeline estimate
- **1 day**

---

## Phase 5 — Release Readiness and Rollout
**Goal:** Ship safely with low regression risk.

### Work
1. Confirm no regression in existing roadmap execution paths.
2. Run sync workflow if source/distributable artifacts require it.
3. Verify developer-facing copies and source-of-truth consistency.
4. Prepare release notes focused on:
   - new progress reporting
   - dry-run visibility
   - operational expectations
5. Validate on representative roadmap runs.

### Deliverables
- Release-ready implementation
- Final verification report
- Sync confirmation for `src/superclaude/` to `.claude/` if applicable

### Milestone
- **M5:** Ready for merge and downstream use.

### Timeline estimate
- **0.5 day**

# 3. Risk Assessment and Mitigation Strategies

## Risk 1 — Progress writes degrade pipeline performance
**Severity:** Low

### Mitigation
- Use small, bounded JSON payloads.
- Perform atomic replace only on step completion.
- Benchmark explicitly against the `< 50ms` requirement.
- Reject unnecessary formatting or excessive metadata expansion.

## Risk 2 — Parallel step completion corrupts progress state
**Severity:** Medium

### Mitigation
- Depend on sequential `on_step_complete` invocation contract.
- Centralize all writes in one callback pathway.
- Avoid background workers, shared mutable writer threads, or async flush logic.
- Add tests specifically for parallel generate-A / generate-B behavior.

## Risk 3 — `summary()` change breaks existing gate behavior
**Severity:** High

### Mitigation
- Keep `summary()` additive-only.
- Do not alter constructor, field semantics, or existing method signatures.
- Add regression tests for existing gate usage patterns.
- Review all call sites in `gates.py` consumers before merge.

## Risk 4 — Seeded ambiguities become implementation defects
**Severity:** Medium

### Mitigation
- Treat OQ-001 and OQ-002 as implementation blockers.
- Record chosen interpretations explicitly before coding dependent paths.
- Gate Phase 2 integration on Phase 0 closure.
- If unresolved, implement only unambiguous core behavior and stop before fidelity-sensitive features.

## Risk 5 — Resume semantics conflict with overwrite requirement
**Severity:** Medium

### Mitigation
- Establish a single rule for standard run vs resumed run.
- Encode that rule in CLI tests.
- Avoid hidden implicit behavior based on file existence alone.

# 4. Resource Requirements and Dependencies

## Engineering resources
1. **Primary backend/CLI engineer**
   - Implement progress module
   - Wire executor and command changes
2. **QA/validation support**
   - Real CLI execution validation
   - Crash-safety and latency measurement
3. **Architect/reviewer**
   - Approve schema and ambiguity resolutions
   - Review additive gate changes

## Code dependencies
1. `src/superclaude/cli/roadmap/executor.py`
   - callback integration
   - step construction and lifecycle
2. `src/superclaude/cli/roadmap/commands.py`
   - CLI option registration and validation
3. `src/superclaude/cli/roadmap/models.py`
   - `StepResult` compatibility
4. `src/superclaude/cli/roadmap/gates.py`
   - dry-run summaries
5. `src/superclaude/cli/roadmap/convergence.py`
   - deviation iteration reporting
6. `src/superclaude/cli/audit/wiring_gate.py`
   - wiring verdict and metadata

## External/runtime dependencies
1. Python `os`
   - atomic replace
2. Python `json`
   - serialization
3. Existing Click framework
   - CLI option support
4. UV-based execution environment
   - all runs and tests via `uv run`

## Architectural constraints to honor
1. Only one new file: `src/superclaude/cli/roadmap/progress.py`
2. No change to gate validation logic behavior
3. No new third-party packages
4. Python 3.10+ compatible typing and dataclasses only

# 5. Success Criteria and Validation Approach

## Success criteria
1. `progress.json` is created on first completed step.
2. File remains valid JSON after every write.
3. Every step entry includes required fields.
4. Custom `--progress-file` path works and validates parent existence.
5. Default path resolves to `{output_dir}/progress.json`.
6. Dry-run prints complete Markdown gate summary table.
7. Wiring verification entries include required metrics.
8. Write overhead stays below 50ms per step.
9. Importing progress module causes zero filesystem I/O.

## Validation approach

### Functional validation
1. Run CLI-driven tests for standard execution.
2. Run CLI-driven tests for `--dry-run`.
3. Run scenarios including:
   - parallel generation
   - convergence loop
   - remediation triggered
   - remediation not triggered
   - wiring gate outcomes

### Reliability validation
1. Validate atomic writes by simulating interruption between temp write and replace.
2. Confirm final file is always parseable JSON.
3. Verify overwrite behavior is deterministic.

### Compatibility validation
1. Confirm no existing gate consumers break after `summary()` addition.
2. Confirm no executor flow regressions.
3. Confirm no import side effects in new module.

### Performance validation
1. Benchmark step completion with and without progress writes.
2. Record max and average overhead.
3. Fail validation if writes exceed target budget.

### Acceptance evidence
- Test results mapped to SC-001 through SC-009
- Sample progress file outputs
- Dry-run output snapshot
- Benchmark log
- Regression test pass on affected roadmap suite

# 6. Timeline Estimates per Phase

| Phase | Name | Duration | Exit Condition |
|---|---|---:|---|
| 0 | Specification Closure and Architectural Alignment | 0.5 day | Blocking ambiguities resolved |
| 1 | Progress Reporting Foundation | 1 day | Atomic progress writer complete |
| 2 | Pipeline Integration | 1.5 days | End-to-end step reporting works |
| 3 | CLI and Dry-Run Visibility | 1 day | CLI option and gate table complete |
| 4 | Validation, Performance, and Reliability Hardening | 1 day | Success criteria proven with evidence |
| 5 | Release Readiness and Rollout | 0.5 day | Merge-ready implementation |

## Total estimated implementation window
- **5.5 engineering days**

## Recommended sequencing notes
1. Do not start convergence/remediation reporting until schema ambiguity is closed.
2. Do not merge `summary()` changes without regression proof.
3. Do not treat unit-only validation as sufficient; final acceptance should use real CLI pipeline execution.

# Recommended Milestone Order

1. **M0** — Spec decisions approved
2. **M1** — Atomic writer complete
3. **M2** — Executor-integrated progress reporting complete
4. **M3** — CLI and dry-run contract complete
5. **M4** — Evidence-backed validation complete
6. **M5** — Release-ready and safe to merge

# Architect Recommendation

The safest and fastest path is a constrained additive implementation: isolate persistence in one module, integrate only through the existing callback contract, and block fidelity-sensitive work until ambiguity decisions are explicit. This preserves system stability while still delivering meaningful observability and operator clarity.
