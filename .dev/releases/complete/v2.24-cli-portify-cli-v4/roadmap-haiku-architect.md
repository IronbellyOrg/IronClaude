---
spec_source: "portify-release-spec.md"
complexity_score: 0.85
primary_persona: architect
---

## 1. Executive Summary

This roadmap delivers a high-complexity CLI portification pipeline for `sc-cli-portify`, transforming an inference-heavy workflow into a deterministic, synchronous Python execution path with strict gate enforcement, reusable skill integration, and end-to-end validation.

Architecturally, the release is defined by four dominant concerns:

1. **Deterministic orchestration**
   - Python must control sequencing, convergence, retries, gating, status, and resume behavior.
   - This is driven by FR-PORTIFY-CLI.4f, FR-PORTIFY-CLI.7b, NFR-005, and NFR-006.

2. **Strict separation of responsibilities**
   - Pure-programmatic steps own path resolution, discovery, validation, and flow control.
   - Claude-assisted steps own content generation only.
   - This split is central to FR-PORTIFY-CLI.1, FR-PORTIFY-CLI.2, FR-PORTIFY-CLI.3, FR-PORTIFY-CLI.4, and the architectural constraints.

3. **Safe reuse of existing framework capabilities**
   - The implementation must extend existing pipeline and sprint base types rather than fork behavior.
   - `/sc:brainstorm` and `/sc:spec-panel` must be reused rather than reimplemented per FR-PORTIFY-CLI.6a and FR-PORTIFY-CLI.7a.

4. **Production-grade quality gates**
   - STRICT validation is required across the core content-producing steps.
   - Success depends not only on artifact generation, but on convergence, score thresholds, structural validity, failure-path completeness, and additive-only modification behavior.

Given the **HIGH** complexity classification and multi-domain scope (`backend`, `cli`, `devops`, `testing`), the roadmap prioritizes:
- early architecture stabilization,
- explicit contract design,
- isolated step-by-step implementation,
- failure-path and resume correctness,
- real pipeline validation rather than shallow unit-only assurance.

## 2. Phased Implementation Plan with Milestones

### Milestone 1. Architecture Baseline and Scope Lock
**Goal:** Establish the final implementation contract before coding begins.

**Primary outcomes**
- Lock 18-module additive architecture.
- Confirm extension points into `pipeline.models`, `pipeline.gates`, `pipeline.process`, `sprint.models`, and `sprint.process`.
- Resolve open CLI contract gaps before implementation drift begins.

**Requirements addressed**
- FR-PORTIFY-CLI.4f
- NFR-003
- NFR-006
- NFR-007
- NFR-010

**Key work items**
1. Define the target package/module structure for `cli_portify/`.
2. Formalize inheritance model:
   - `PortifyConfig extends PipelineConfig`
   - `PortifyStepResult extends StepResult`
   - `PortifyProcess extends ClaudeProcess`
3. Define executor responsibilities vs subprocess responsibilities.
4. Add explicit CLI surface for:
   - `run`
   - `--dry-run`
   - `--skip-review`
   - `--resume`
   - `--start`
5. Freeze the synchronous-only rule:
   - no `async def`
   - no `await`
6. Confirm no changes will be made under `pipeline/` or `sprint/`.

**Milestone deliverables**
- Architecture decision record for `cli_portify/`
- CLI surface definition
- Step contract matrix
- Resume-state decision table

**Exit criteria**
- Open Question 9 resolved.
- Architectural constraints mapped to concrete modules.
- No unresolved ambiguity on flow ownership.

**Timeline estimate**
- **2-3 days**

---

### Milestone 2. Programmatic Foundation: Config, Discovery, Models, Contracts
**Goal:** Implement the deterministic base layer that all Claude-assisted work depends on.

**Primary outcomes**
- `validate-config` and `discover-components` fully functional and fast.
- Shared data models, result contracts, logging schema, and failure defaults established.

**Requirements addressed**
- FR-PORTIFY-CLI.1a
- FR-PORTIFY-CLI.1b
- FR-PORTIFY-CLI.1c
- FR-PORTIFY-CLI.1d
- FR-PORTIFY-CLI.1e
- FR-PORTIFY-CLI.1f
- FR-PORTIFY-CLI.2a
- FR-PORTIFY-CLI.2b
- FR-PORTIFY-CLI.2c
- FR-PORTIFY-CLI.2d
- FR-PORTIFY-CLI.2e
- FR-PORTIFY-CLI.2f
- NFR-004
- NFR-009

**Key work items**
1. Implement workflow path resolution and validation.
2. Implement deterministic CLI-name derivation logic.
3. Implement output path validation and writability checks.
4. Implement non-portified collision detection.
5. Emit `validate-config-result.json`.
6. Implement component inventory discovery:
   - `SKILL.md`
   - `refs/`
   - `rules/`
   - `templates/`
   - `scripts/`
   - command-file lookup across both command roots
7. Add accurate line counting with documented handling for the 1MB cap inconsistency.
8. Emit `component-inventory.md` with required frontmatter.
9. Establish return-contract defaults for success, failure, partial, and dry-run outcomes.

**Architect notes**
- This milestone must be complete before any prompt engineering work. If the deterministic layer is weak, downstream Claude-assisted steps will be hard to validate.
- Failure taxonomy should be finalized here, not retrofitted later.

**Milestone deliverables**
- Core models
- Config validator
- Component discovery implementation
- Contract emission logic
- Failure code catalog

**Exit criteria**
- FR-PORTIFY-CLI.1 and FR-PORTIFY-CLI.2 acceptance criteria pass.
- All gate functions conform to `tuple[bool, str]`.
- Failure-path defaults are populated on all tested outcomes.

**Timeline estimate**
- **3-4 days**

---

### Milestone 3. Analysis and Pipeline Design Layer
**Goal:** Implement the first two Claude-assisted steps with deterministic gate enforcement around them.

**Primary outcomes**
- Workflow analysis output is generated, bounded, and validated.
- Pipeline design output fully maps steps, gates, prompts, and execution model.

**Requirements addressed**
- FR-PORTIFY-CLI.3a
- FR-PORTIFY-CLI.3b
- FR-PORTIFY-CLI.3c
- FR-PORTIFY-CLI.3d
- FR-PORTIFY-CLI.3e
- FR-PORTIFY-CLI.3f
- FR-PORTIFY-CLI.4a
- FR-PORTIFY-CLI.4b
- FR-PORTIFY-CLI.4c
- FR-PORTIFY-CLI.4d
- FR-PORTIFY-CLI.4e
- FR-PORTIFY-CLI.4f
- FR-PORTIFY-CLI.4g
- FR-PORTIFY-CLI.4h
- NFR-005
- NFR-006

**Key work items**
1. Build prompt/input assembly using `@path` references only.
2. Implement `analyze-workflow` subprocess execution.
3. Validate `portify-analysis.md` structure:
   - Source Components
   - Step Graph
   - Gates Summary
   - Data Flow Diagram
   - Classification Summary
4. Enforce line-count ceiling and structural checks.
5. Implement `design-pipeline` subprocess execution.
6. Validate that all steps have mappings and gates.
7. Ensure pure-programmatic steps contain actual Python implementation.
8. Implement user review halt point after design.
9. Ensure `--dry-run` exits here with a complete dry-run contract.

**Architect notes**
- This milestone converts conceptual workflow into enforceable execution architecture.
- Review gate placement here is correct because it is the last point before spec synthesis cost expands.

**Milestone deliverables**
- Prompt builders for Steps 3 and 4
- Strict gate definitions for analysis/design artifacts
- Review-gate TUI interaction
- Dry-run path

**Exit criteria**
- STRICT tier passes for both steps.
- `--dry-run` halts after design exactly as required.
- Deterministic runner remains the source of truth for state.

**Timeline estimate**
- **4-5 days**

---

### Milestone 4. Spec Synthesis and Brainstorm Integration
**Goal:** Produce the release spec and enrich it with structured gap analysis without weakening determinism.

**Primary outcomes**
- Release spec generated with zero placeholders.
- Brainstorm skill reused safely, with fallback and structural validation.

**Requirements addressed**
- FR-PORTIFY-CLI.5a
- FR-PORTIFY-CLI.5b
- FR-PORTIFY-CLI.5c
- FR-PORTIFY-CLI.5d
- FR-PORTIFY-CLI.5e
- FR-PORTIFY-CLI.5f
- FR-PORTIFY-CLI.5g
- FR-PORTIFY-CLI.6a
- FR-PORTIFY-CLI.6b
- FR-PORTIFY-CLI.6c
- FR-PORTIFY-CLI.6d
- FR-PORTIFY-CLI.6e
- FR-PORTIFY-CLI.6f
- FR-PORTIFY-CLI.6g
- FR-PORTIFY-CLI.6h
- FR-PORTIFY-CLI.6i
- FR-PORTIFY-CLI.6j
- NFR-008
- NFR-010

**Key work items**
1. Implement `synthesize-spec` prompt builder and output parser.
2. Add placeholder detection and retry logic with specific remaining placeholder names.
3. Enforce exact FR count and logical step consolidation mapping.
4. Validate required conditional sections.
5. Implement pre-flight skill availability check for `/sc:brainstorm`.
6. Add fallback inline multi-persona prompt with warning path.
7. Implement Section 12 append semantics.
8. Enforce structural validity:
   - findings table with Gap ID column, or
   - literal zero-gap summary text
9. Route unresolved items into Section 11 with `[OPEN]`.
10. Mark incorporated items as `[INCORPORATED]`.
11. Preserve additive-only modification behavior.

**Architect notes**
- This is the first stage where content volume and context pressure materially increase.
- Artifact parsing must be robust to partial/verbose skill output.

**Milestone deliverables**
- Synthesized `portify-release-spec.md`
- Brainstorm integration module
- Placeholder retry handler
- Structural validators for Section 12

**Exit criteria**
- Zero `{{SC_PLACEHOLDER:*}}`
- STANDARD/STRICT gates pass where required
- No destructive rewrite behavior introduced

**Timeline estimate**
- **4-5 days**

---

### Milestone 5. Panel Review, Convergence Engine, and Quality Gates
**Goal:** Build the most critical control loop in the system: iterative expert review with bounded convergence.

**Primary outcomes**
- Expert panel loop implemented with max-3 iterations, convergence predicate, timeout control, and downstream readiness gate.
- Machine-readable convergence outputs produced and trusted.

**Requirements addressed**
- FR-PORTIFY-CLI.7a
- FR-PORTIFY-CLI.7b
- FR-PORTIFY-CLI.7c
- FR-PORTIFY-CLI.7d
- FR-PORTIFY-CLI.7e
- FR-PORTIFY-CLI.7f
- FR-PORTIFY-CLI.7g
- FR-PORTIFY-CLI.7h
- FR-PORTIFY-CLI.7i
- FR-PORTIFY-CLI.7j
- FR-PORTIFY-CLI.7k
- FR-PORTIFY-CLI.7l
- FR-PORTIFY-CLI.7m
- FR-PORTIFY-CLI.7n
- NFR-001
- NFR-002
- NFR-005
- NFR-008
- NFR-010
- NFR-011

**Key work items**
1. Implement `/sc:spec-panel` pre-flight check and fallback prompt path.
2. Implement dual-mode iteration execution:
   - focus pass
   - critique pass
   - single subprocess boundary
3. Implement convergence state model and iteration counter.
4. Implement independent iteration timeout with default 300s.
5. Integrate TurnLedger budget guard before each launch.
6. Parse and validate:
   - `CONVERGENCE_STATUS`
   - `UNADDRESSED_CRITICALS`
   - `QUALITY_OVERALL`
7. Compute and validate quality scores:
   - clarity
   - completeness
   - testability
   - consistency
   - `overall = mean(...)`
8. Implement terminal state handling:
   - CONVERGED
   - ESCALATED
9. Add review gate at end of panel phase.
10. Emit `panel-report.md`.

**Architect notes**
- This milestone is the highest-risk part of the release.
- Convergence logic, additive-only behavior, and quality thresholds are the principal architectural differentiators of the feature.

**Milestone deliverables**
- Convergence engine
- Panel review step
- Score calculator and validators
- `panel-report.md`
- User escalation path

**Exit criteria**
- Boundary check for `overall >= 7.0` passes.
- No unaddressed CRITICAL findings on converged path.
- ESCALATED path remains valid and observable.

**Timeline estimate**
- **5-6 days**

---

### Milestone 6. Monitoring, Resume Semantics, UX, and Failure Recovery
**Goal:** Make the pipeline operationally usable and resilient.

**Primary outcomes**
- Monitoring, diagnostics, review pauses, signal extraction, resume flow, and contract completeness behave consistently across all exit paths.

**Requirements addressed**
- NFR-005
- NFR-006
- NFR-009
- NFR-011

**Key work items**
1. Implement monitor and diagnostic collector.
2. Define NDJSON signal vocabulary.
3. Implement review pause interaction on stderr.
4. Implement resume semantics for:
   - synthesize-spec failure
   - Phase 4 restart
   - partial spec existence
5. Implement `resume_command()` output consistency.
6. Ensure every exit path emits a complete contract.
7. Validate `--skip-review` bypass behavior.
8. Normalize warning vs failure classification.

**Architect notes**
- Operational correctness is a release requirement, not polish.
- Resume behavior should be deterministic and explicit, never inferred by Claude output.

**Milestone deliverables**
- Monitor/diagnostics module
- Resume-state logic
- Review-gate handler
- Completed failure classification/reporting

**Exit criteria**
- Open Questions 1, 2, 3, and 8 resolved in implementation.
- Partial and resumed runs are reproducible.
- Review gating behaves as specified.

**Timeline estimate**
- **3-4 days**

---

### Milestone 7. Validation, Real Evals, and Release Hardening
**Goal:** Prove the system works against real artifacts and enforce non-regression.

**Primary outcomes**
- Real pipeline evals pass.
- Meta-portification path is validated.
- CI-ready checks guard architecture constraints.

**Requirements addressed**
- Success Criteria 1-12
- NFR-003
- NFR-007
- NFR-009
- NFR-010

**Key work items**
1. Build unit coverage for:
   - gate functions
   - arithmetic checks
   - failure default completeness
   - resume command generation
2. Build integration coverage for:
   - strict gate failures
   - dry-run halt
   - review gates
   - skill fallback behavior
3. Build end-to-end runs on a real skill.
4. Add self-portification meta-test:
   - `superclaude cli-portify run src/superclaude/skills/sc-cli-portify-protocol/`
5. Add static checks for:
   - no `async def`
   - no `await`
   - no diffs in `pipeline/` and `sprint/`
6. Validate timing advisories for Phase 3 and Phase 4.
7. Confirm reports are runner-authored from observed data only.

**Architect notes**
- Based on project memory, validation should favor **real evals over isolated mock-only confidence**.
- The meta-test is especially important because it exercises the system on its own complexity boundary.

**Milestone deliverables**
- Real eval suite
- Integration tests
- Static architecture guards
- Release readiness report

**Exit criteria**
- Success Criteria 1-12 satisfied or explicitly escalated with rationale.
- No architectural constraint violations remain.

**Timeline estimate**
- **4-5 days**

---

## 3. Risk Assessment and Mitigation Strategies

### High-priority risks

1. **Risk 1: Large context windows in Steps 5-7 cause output truncation**
   - **Impact:** Broken specs, incomplete panel outputs, invalid convergence parsing.
   - **Mitigation:**
     - Enforce `@path` references only.
     - Keep prompts minimal and artifact-oriented.
     - Add strict structural post-checks after every Claude-assisted step.
     - Fail fast if machine-readable blocks are incomplete.

2. **Risk 3: `/sc:brainstorm` and `/sc:spec-panel` do not emit expected machine-readable markers**
   - **Impact:** Convergence and routing logic become ambiguous.
   - **Mitigation:**
     - Pre-flight skill checks.
     - Structural fallback parsing.
     - Inline fallback prompt paths.
     - Clear warning emission when degraded mode is used.

3. **Risk 6: Subprocess invocation fails if commands are not installed**
   - **Impact:** Claude-assisted steps unusable.
   - **Mitigation:**
     - Validate `claude` binary at startup.
     - Validate skill availability before step execution.
     - Fail in Phase 0/1 instead of mid-pipeline.

4. **Risk 7: Subprocess cannot read `@path` references**
   - **Impact:** Claude steps fail despite valid orchestration.
   - **Mitigation:**
     - Ensure `PortifyProcess` passes required `--add-dir` locations.
     - Add an early integration smoke test for path visibility.
     - Treat path-access failure as a classified pre-flight defect.

5. **Risk 9: Wrong mode mapping across panel-review iterations**
   - **Impact:** False convergence, repeated critique loops, inconsistent quality scoring.
   - **Mitigation:**
     - Encode dual-mode iteration explicitly in executor logic.
     - Test iteration behavior independently.
     - Freeze prompt contract for focus + critique sequencing.

### Medium-priority risks

6. **Risk 2: Convergence loop exhausts budget before 3 iterations**
   - **Mitigation:**
     - TurnLedger pre-launch checks.
     - Per-iteration budget estimate.
     - Explicit ESCALATED state.

7. **Risk 5: Self-portification circularity**
   - **Mitigation:**
     - Treat source skill files as read-only.
     - Emit generated artifacts into separate target directories only.

8. **Risk 8: User review gates lack robust interaction mechanism**
   - **Mitigation:**
     - Implement stderr prompt contract early.
     - Ensure `--skip-review` works reliably.
     - Cover manual interaction path in integration validation.

### Structural mitigation strategy by phase

- **Early phases:** eliminate ambiguity and environment risk.
- **Middle phases:** validate artifact structure and additive-only editing.
- **Late phases:** validate resume, convergence, and real end-to-end behavior.

## 4. Resource Requirements and Dependencies

### Engineering resources

1. **Primary implementation owner**
   - Strong Python CLI and orchestration experience.
   - Comfortable with Click, Rich, YAML/JSONL, subprocess management, and deterministic runner design.

2. **Architectural reviewer**
   - Verifies extension-vs-reimplementation discipline.
   - Focus on NFR-003, NFR-006, NFR-007, and NFR-005.

3. **QA/validation owner**
   - Builds real evals, integration tests, and architecture guards.
   - Ensures success criteria and timing advisories are validated.

### Technical dependencies to plan around

1. `pipeline.models`
2. `pipeline.gates`
3. `pipeline.process`
4. `sprint.models`
5. `sprint.process`
6. `/sc:brainstorm`
7. `/sc:spec-panel`
8. `claude` binary

### Dependency handling plan

- **Internal package dependencies**
  - Lock interface expectations before coding.
  - Avoid base-package modifications per NFR-007.
  - Add contract tests around inherited behavior.

- **External skill dependencies**
  - Add pre-flight detection.
  - Add fallback prompt modes.
  - Emit warnings when fallback mode is used.

- **System dependency**
  - Validate `claude` binary availability before any Claude-assisted step.
  - Fail early with explicit diagnosis.

### Additional supporting requirements

- `click>=8.0.0`
- `rich>=13.0.0`
- `pyyaml`
- Python `>=3.10`

## 5. Success Criteria and Validation Approach

### Success criteria mapping

1. **Pipeline execution succeeds end-to-end**
   - Validate Success Criterion 1 with a real skill target.

2. **Dry-run halts at the correct boundary**
   - Validate Success Criterion 2 with `--dry-run`.

3. **STRICT gates halt malformed outputs**
   - Validate Success Criterion 3 with intentional bad artifacts.

4. **Convergence loop behaves correctly**
   - Validate Success Criterion 4 across converged and escalated paths.

5. **Downstream readiness threshold is exact**
   - Validate Success Criterion 5 for `7.0` and `6.9`.

6. **Quality arithmetic is exact**
   - Validate Success Criterion 6 using fixed-value score tests.

7. **No placeholders remain**
   - Validate Success Criterion 7 structurally.

8. **Return contract is complete on every path**
   - Validate Success Criterion 8 with per-outcome tests.

9. **Resume command generation is correct**
   - Validate Success Criterion 9 with resumable failure cases.

10. **No base module changes**
   - Validate Success Criterion 10 via diff checks.

11. **Synchronous-only implementation**
   - Validate Success Criterion 11 with static analysis.

12. **Self-portification works**
   - Validate Success Criterion 12 with E2E meta-test.

### Validation layers

1. **Unit validation**
   - Gate functions
   - score arithmetic
   - contract completion
   - derivation logic
   - resume logic

2. **Integration validation**
   - step-to-step artifact flow
   - subprocess invocation
   - review gates
   - fallback modes
   - monitoring/diagnostics

3. **End-to-end validation**
   - real workflow portification
   - dry-run path
   - resumed execution path
   - self-portification

4. **Static architecture validation**
   - zero async
   - no forbidden module edits
   - type signature compliance

### Architect emphasis

The release should not be declared complete just because files are generated. It is complete only when:
- the runner owns truth,
- gates are trustworthy,
- quality thresholds are enforced,
- resume and failure semantics are deterministic,
- and a real pipeline run proves the architecture under production-like conditions.

## 6. Timeline Estimates per Phase

| Phase | Scope | Estimated Duration |
|---|---|---:|
| Milestone 1 | Architecture baseline and scope lock | 2-3 days |
| Milestone 2 | Programmatic foundation | 3-4 days |
| Milestone 3 | Analysis and pipeline design | 4-5 days |
| Milestone 4 | Spec synthesis and brainstorm integration | 4-5 days |
| Milestone 5 | Panel review and convergence engine | 5-6 days |
| Milestone 6 | Monitoring, resume, UX, failure recovery | 3-4 days |
| Milestone 7 | Validation, real evals, release hardening | 4-5 days |

### Overall roadmap estimate
- **Total:** **25-32 working days**

### Suggested milestone dependency chain

1. **M1 → M2**
   - No implementation should begin before the CLI and architecture contract are locked.

2. **M2 → M3**
   - Claude-assisted analysis depends on deterministic artifact foundations.

3. **M3 → M4**
   - Spec synthesis depends on validated analysis/design outputs.

4. **M4 → M5**
   - Panel review depends on a valid synthesized spec and structured brainstorm results.

5. **M5 → M6**
   - Resume and monitoring logic should target the final convergence behavior, not an interim design.

6. **M6 → M7**
   - Final validation must cover the complete operational pipeline.

## Requirement Traceability Summary

### Functional requirements covered by roadmap phases
- **FR-PORTIFY-CLI.1a - FR-PORTIFY-CLI.1f** → Milestone 2
- **FR-PORTIFY-CLI.2a - FR-PORTIFY-CLI.2f** → Milestone 2
- **FR-PORTIFY-CLI.3a - FR-PORTIFY-CLI.3f** → Milestone 3
- **FR-PORTIFY-CLI.4a - FR-PORTIFY-CLI.4h** → Milestone 3
- **FR-PORTIFY-CLI.5a - FR-PORTIFY-CLI.5g** → Milestone 4
- **FR-PORTIFY-CLI.6a - FR-PORTIFY-CLI.6j** → Milestone 4
- **FR-PORTIFY-CLI.7a - FR-PORTIFY-CLI.7n** → Milestone 5

### Non-functional requirements covered by roadmap phases
- **NFR-001, NFR-002** → Milestones 5 and 7
- **NFR-003** → Milestones 1, 2, and 7
- **NFR-004** → Milestone 2
- **NFR-005, NFR-006** → Milestones 1, 3, 5, 6, and 7
- **NFR-007** → Milestones 1 and 7
- **NFR-008** → Milestones 4 and 5
- **NFR-009** → Milestones 2, 6, and 7
- **NFR-010** → Milestones 1, 4, 5, and 7
- **NFR-011** → Milestones 5 and 6

## Recommended Release Governance

1. **Gate after Milestone 1**
   - Approve architecture and CLI contract before code scales.

2. **Gate after Milestone 3**
   - Approve deterministic runner behavior and dry-run semantics before synthesis work.

3. **Gate after Milestone 5**
   - Approve convergence engine before release-hardening investment.

4. **Final release gate after Milestone 7**
   - Require passing real eval evidence, meta-test evidence, and architecture guard evidence.

## Final Architect Recommendation

Implement this release as a **control-plane-first system**, not as a prompt-generation feature. The highest-value architectural choice is to keep Claude output constrained, observable, and subordinate to Python-controlled execution. If tradeoffs are required during implementation, preserve the following in order:

1. **Deterministic runner control**
2. **STRICT gate integrity**
3. **Base-module immutability**
4. **Skill reuse with safe fallbacks**
5. **Operational resilience via resume/contracts/monitoring**

That priority order best aligns the roadmap with the extracted requirements, identified risks, and long-term maintainability of the SuperClaude CLI platform.
