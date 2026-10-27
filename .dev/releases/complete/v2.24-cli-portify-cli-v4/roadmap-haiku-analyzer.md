---
spec_source: "portify-release-spec.md"
complexity_score: 0.85
primary_persona: analyzer
---

# 1. Executive Summary

This roadmap delivers a new `cli-portify` pipeline that converts inference-driven SuperClaude workflows into deterministic, programmatic CLI pipelines while preserving existing framework boundaries and enforcing quality gates. The implementation is high complexity because it combines pure-programmatic steps, Claude-assisted generation, subprocess-based skill reuse, convergence logic, TUI/CLI integration, gate enforcement, and resumable failure handling under strict architectural constraints.

From an analyzer perspective, the primary delivery concern is not feature breadth but control integrity:

- `FR-PORTIFY-CLI.1` through `FR-PORTIFY-CLI.7` form a strictly ordered dependency chain.
- The highest-risk areas are subprocess skill reuse, convergence-state correctness, machine-readable artifact validation, and additive-only modification guarantees.
- `NFR-005`, `NFR-006`, `NFR-007`, `NFR-008`, and `NFR-009` are architectural guardrails and should be treated as release blockers, not polish items.
- The roadmap should favor early validation of irreversible assumptions:
  1. base-type extension strategy,
  2. synchronous execution model,
  3. subprocess `@path` access,
  4. skill availability and fallback behavior,
  5. convergence marker parsing.

## Strategic Objectives

1. Build a working `cli-portify` command path that satisfies all seven functional requirements.
2. Enforce deterministic, Python-owned flow control regardless of Claude output variability.
3. Reuse `/sc:brainstorm` and `/sc:spec-panel` without duplicating their logic.
4. Produce verifiable artifacts and contracts for success, dry-run, partial, and failure outcomes.
5. Preserve repository stability by keeping implementation additive and avoiding changes to `pipeline/` and `sprint/`.

## Recommended Delivery Strategy

1. Implement the pipeline in four phases aligned to dependency and risk.
2. Front-load foundational and gate semantics before Claude-assisted steps.
3. Treat end-to-end execution against a real workflow as the primary validation mechanism.
4. Gate Phase 3 and Phase 4 with artifact contract checks before moving forward.
5. Use analyzer-driven checkpoints after each phase to validate assumptions against the extraction requirements.

---

# 2. Phased Implementation Plan with Milestones

## Phase 0 — Foundation and Architecture Lock

### Goals
Establish the implementation skeleton and de-risk core architectural constraints before building step logic.

### Scope
- Define module structure consistent with the accepted 18-module architecture.
- Establish inheritance model for:
  - `PortifyConfig` → `PipelineConfig`
  - `PortifyStepResult` → `StepResult`
  - `PortifyProcess` → `ClaudeProcess`
- Register Click command entrypoint in `main.py`.
- Define shared models, gate criteria shells, monitor/reporting scaffolding, and contract defaults.

### Requirements addressed
- `NFR-003`
- `NFR-004`
- `NFR-005`
- `NFR-006`
- `NFR-007`
- `NFR-009`
- Architectural Constraints 1-12

### Key actions
1. Create the additive module layout under `cli_portify/`.
2. Define common data models and enums, including convergence state.
3. Establish valid state-transition logic for resumability and terminal outcomes.
4. Create contract-emission utilities with fully populated defaults on failure.
5. Add static checks to prevent `async def` or `await` in `cli_portify/`.
6. Add git-diff validation coverage for `pipeline/` and `sprint/`.

### Analyzer concerns
- Locking architecture now avoids midstream redesign when `FR-PORTIFY-CLI.7` introduces convergence complexity.
- Contract completeness must be implemented early because all later failure paths depend on it.
- CLI surface must include unresolved open-question items such as `--resume` and `--start` before tests codify the wrong interface.

### Milestone M0
**Architecture baseline approved**
- Module scaffold exists.
- Base-type extension verified.
- No forbidden edits to `pipeline/` or `sprint/`.
- CLI group is registered but may contain stubbed step wiring.

### Timeline estimate
- **2-3 days**

---

## Phase 1 — Deterministic Core Pipeline Steps

### Goals
Implement the pure-programmatic steps first to establish reliable inputs for all Claude-assisted stages.

### Scope
- `FR-PORTIFY-CLI.1: validate-config`
- `FR-PORTIFY-CLI.2: discover-components`

### Requirements addressed

#### `FR-PORTIFY-CLI.1`
- `FR-PORTIFY-CLI.1a`
- `FR-PORTIFY-CLI.1b`
- `FR-PORTIFY-CLI.1c`
- `FR-PORTIFY-CLI.1d`
- `FR-PORTIFY-CLI.1e`
- `FR-PORTIFY-CLI.1f`

#### `FR-PORTIFY-CLI.2`
- `FR-PORTIFY-CLI.2a`
- `FR-PORTIFY-CLI.2b`
- `FR-PORTIFY-CLI.2c`
- `FR-PORTIFY-CLI.2d`
- `FR-PORTIFY-CLI.2e`
- `FR-PORTIFY-CLI.2f`

### Key actions
1. Implement workflow path resolution and `SKILL.md` presence checks.
2. Implement CLI name derivation logic with:
   - `sc-` prefix stripping,
   - `-protocol` suffix stripping,
   - kebab/snake conversion,
   - hard failure on derivation ambiguity.
3. Validate output directory parent existence and writability.
4. Detect name collisions with non-portified modules.
5. Write `validate-config-result.json`.
6. Discover all relevant workflow assets:
   - `SKILL.md`
   - `refs/`
   - `rules/`
   - `templates/`
   - `scripts/`
7. Locate matching command files in both:
   - `src/superclaude/commands/`
   - `.claude/commands/sc/`
8. Count lines for each discovered component.
9. Write `component-inventory.md` with required frontmatter.

### Analyzer concerns
- `FR-PORTIFY-CLI.1f` and `FR-PORTIFY-CLI.2f` should be treated as real performance gates because they precede all expensive work.
- File discovery behavior must be deterministic and testable; avoid shell-dependent traversal.
- Line-counting cap inconsistency from open question #6 should be resolved explicitly during implementation.

### Milestone M1
**Deterministic input pipeline complete**
- Pure-programmatic steps run without Claude.
- Both artifacts are emitted.
- Performance constraints are measured and pass.

### Timeline estimate
- **3-4 days**

---

## Phase 2 — Analysis and Design Artifacts

### Goals
Build the first Claude-assisted stages that translate discovered components into a machine-actionable pipeline design.

### Scope
- `FR-PORTIFY-CLI.3: analyze-workflow`
- `FR-PORTIFY-CLI.4: design-pipeline`

### Requirements addressed

#### `FR-PORTIFY-CLI.3`
- `FR-PORTIFY-CLI.3a`
- `FR-PORTIFY-CLI.3b`
- `FR-PORTIFY-CLI.3c`
- `FR-PORTIFY-CLI.3d`
- `FR-PORTIFY-CLI.3e`
- `FR-PORTIFY-CLI.3f`

#### `FR-PORTIFY-CLI.4`
- `FR-PORTIFY-CLI.4a`
- `FR-PORTIFY-CLI.4b`
- `FR-PORTIFY-CLI.4c`
- `FR-PORTIFY-CLI.4d`
- `FR-PORTIFY-CLI.4e`
- `FR-PORTIFY-CLI.4f`
- `FR-PORTIFY-CLI.4g`
- `FR-PORTIFY-CLI.4h`

### Key actions
1. Implement `PortifyProcess` artifact-passing pattern using `@path` references.
2. Build prompt assembly for workflow analysis using only discovered artifacts and machine-readable instructions.
3. Generate `portify-analysis.md` with:
   - required frontmatter,
   - Source Components,
   - Step Graph,
   - Gates Summary,
   - Data Flow Diagram,
   - Classification Summary.
4. Enforce:
   - step classification completeness,
   - data flow arrow notation,
   - line-count ceiling under 400,
   - STRICT-tier validation.
5. Use the analysis artifact to generate `portify-spec.md`.
6. Ensure every pipeline step has:
   - mapping,
   - gate definition,
   - pure-programmatic Python implementation where required,
   - prompt builder spec for Claude-assisted steps,
   - synchronous threading model,
   - review gate behavior,
   - `--dry-run` stop point.

### Analyzer concerns
- This phase is where nondeterminism first enters; gate validation must reject structurally plausible but incomplete Claude output.
- `FR-PORTIFY-CLI.4d` is critical: pure-programmatic steps must contain actual Python implementation, not design prose.
- `FR-PORTIFY-CLI.4h` introduces human review control; TUI pause semantics should be proven now, not deferred.

### Milestone M2
**Analysis-to-design chain verified**
- `portify-analysis.md` and `portify-spec.md` are emitted and pass STRICT gates.
- `--dry-run` halts after design review as required.
- Prompt contracts are stable enough for downstream synthesis.

### Timeline estimate
- **4-5 days**

---

## Phase 3 — Spec Synthesis and Gap Expansion

### Goals
Generate the release spec, eliminate placeholder leakage, and augment it with structured gap analysis.

### Scope
- `FR-PORTIFY-CLI.5: synthesize-spec`
- `FR-PORTIFY-CLI.6: brainstorm-gaps`

### Requirements addressed

#### `FR-PORTIFY-CLI.5`
- `FR-PORTIFY-CLI.5a`
- `FR-PORTIFY-CLI.5b`
- `FR-PORTIFY-CLI.5c`
- `FR-PORTIFY-CLI.5d`
- `FR-PORTIFY-CLI.5e`
- `FR-PORTIFY-CLI.5f`
- `FR-PORTIFY-CLI.5g`

#### `FR-PORTIFY-CLI.6`
- `FR-PORTIFY-CLI.6a`
- `FR-PORTIFY-CLI.6b`
- `FR-PORTIFY-CLI.6c`
- `FR-PORTIFY-CLI.6d`
- `FR-PORTIFY-CLI.6e`
- `FR-PORTIFY-CLI.6f`
- `FR-PORTIFY-CLI.6g`
- `FR-PORTIFY-CLI.6h`
- `FR-PORTIFY-CLI.6i`
- `FR-PORTIFY-CLI.6j`

### Key actions
1. Implement spec synthesis prompt templates that instantiate the release spec structure from `portify-spec.md`.
2. Enforce placeholder elimination with semantic checks for `{{SC_PLACEHOLDER:*}}`.
3. Validate that exactly seven functional requirements are present in the synthesized spec and aligned to pipeline-step coverage.
4. Ensure required conditional sections are included:
   - 4.3
   - 4.5
   - 5
   - 8.3
   - 9
5. Implement retry-on-failure logic that includes specific missing placeholder names.
6. Pre-flight check `/sc:brainstorm` availability.
7. If available, invoke `/sc:brainstorm`; otherwise execute inline fallback with warning.
8. Append Section 12 Brainstorm Gap Analysis in the required structured format.
9. Route findings as:
   - `[INCORPORATED]` when integrated,
   - `[OPEN]` when unresolved and routed to Section 11.
10. Validate zero-gap behavior and structural sufficiency of Section 12.

### Analyzer concerns
- `FR-PORTIFY-CLI.5b` and `FR-PORTIFY-CLI.5g` directly address a common high-severity failure mode: incomplete machine-authored specs that look finished.
- `FR-PORTIFY-CLI.6i` is especially important because a heading-only section creates false confidence.
- This phase should also resolve open questions around section consistency and CLI surface drift before panel review amplifies those defects.

### Milestone M3
**Release spec generated and enriched**
- `portify-release-spec.md` exists with zero placeholders.
- Section 12 is structurally valid.
- Phase timing for `NFR-001` is measured and reported.

### Timeline estimate
- **4-5 days**

---

## Phase 4 — Panel Review, Convergence, and Release Readiness

### Goals
Run the expert review loop, converge or escalate cleanly, and produce downstream-ready artifacts with enforced quality thresholds.

### Scope
- `FR-PORTIFY-CLI.7: panel-review`

### Requirements addressed
- `FR-PORTIFY-CLI.7a`
- `FR-PORTIFY-CLI.7b`
- `FR-PORTIFY-CLI.7c`
- `FR-PORTIFY-CLI.7d`
- `FR-PORTIFY-CLI.7e`
- `FR-PORTIFY-CLI.7f`
- `FR-PORTIFY-CLI.7g`
- `FR-PORTIFY-CLI.7h`
- `FR-PORTIFY-CLI.7i`
- `FR-PORTIFY-CLI.7j`
- `FR-PORTIFY-CLI.7k`
- `FR-PORTIFY-CLI.7l`
- `FR-PORTIFY-CLI.7m`
- `FR-PORTIFY-CLI.7n`

### Key actions
1. Pre-flight check `/sc:spec-panel` availability.
2. If unavailable, invoke inline expert-panel fallback with explicit warning.
3. Implement executor-owned convergence loop with:
   - iteration counter,
   - max 3 cap,
   - independent per-iteration timeout,
   - TurnLedger pre-launch guard.
4. Ensure each iteration includes both:
   - focus pass,
   - critique pass
   in one subprocess.
5. Parse and validate:
   - `CONVERGENCE_STATUS`
   - `UNADDRESSED_CRITICALS`
   - `QUALITY_OVERALL`
6. Compute and validate quality scores:
   - clarity
   - completeness
   - testability
   - consistency
   - overall mean
7. Enforce convergence predicate:
   - zero CRITICAL findings not marked `[INCORPORATED]` or `[DISMISSED]`
8. Emit `panel-report.md`.
9. Enforce downstream-ready gate at `overall >= 7.0`.
10. Pause for user review unless `--skip-review`.

### Analyzer concerns
- This is the highest operational risk phase because multiple failure modes overlap:
  - marker absence,
  - budget exhaustion,
  - additive-only enforcement,
  - timeout handling,
  - resume semantics,
  - score arithmetic.
- The executor must remain the source of truth at all times per `NFR-005`.
- Additive-only enforcement from `NFR-008` should use structural comparison or section hashing rather than trusting model behavior.

### Milestone M4
**Converged or escalated review complete**
- `panel-report.md` emitted.
- Final spec reaches CONVERGED or ESCALATED terminal state.
- Review gate behavior works interactively.
- Phase timing for `NFR-002` is measured and reported.

### Timeline estimate
- **4-6 days**

---

## Phase 5 — Validation, Hardening, and Meta-Test Closure

### Goals
Convert implementation confidence into release confidence using real pipeline execution and adversarial failure-path coverage.

### Scope
Cross-cutting validation of all FRs and NFRs, including end-to-end and self-portification tests.

### Requirements addressed
- Success Criteria 1-12
- `NFR-001` through `NFR-011`

### Key actions
1. Build unit tests for:
   - gate signatures,
   - score arithmetic,
   - convergence predicate,
   - resume command generation,
   - failure contract completeness.
2. Build integration tests for:
   - full pipeline execution,
   - malformed artifact rejection,
   - `--dry-run`,
   - skill unavailability fallback,
   - review-gate accept/reject behavior.
3. Build static checks for:
   - no `async def` / `await`,
   - no base-module edits.
4. Run E2E portification on a real skill.
5. Run self-portification meta-test:
   - `superclaude cli-portify run src/superclaude/skills/sc-cli-portify-protocol/`
6. Verify runner-authored truth:
   - no status inference from Claude self-reporting.
7. Validate failure, partial, dry-run, and success contract emission.

### Analyzer concerns
- Based on project memory, real evals must take precedence over narrow unit-only validation.
- Success Criteria #1 and #12 are the real confidence anchors; anything less leaves the pipeline unproven.
- Failure-path completeness is as important as happy-path execution due to the number of review, timeout, and gate branches.

### Milestone M5
**Release-ready validation complete**
- All success criteria are demonstrated.
- Real artifact-producing runs are reproducible.
- Known open questions are either resolved or explicitly documented as accepted residuals.

### Timeline estimate
- **3-5 days**

---

# 3. Risk Assessment and Mitigation Strategies

The extraction identifies 9 risks. The roadmap below converts each into concrete controls.

## High-priority risks

### Risk 1: Large context windows in Steps 5-7 cause Claude output truncation
- **Mapped source**: Risk Inventory #1
- **Affected requirements**:
  - `FR-PORTIFY-CLI.5a`
  - `FR-PORTIFY-CLI.5b`
  - `FR-PORTIFY-CLI.6b`
  - `FR-PORTIFY-CLI.7f`
- **Mitigations**:
  1. Always use `@path` file references, never inline large artifacts.
  2. Keep upstream artifacts concise and machine-structured.
  3. Add post-generation structural gates to detect truncation symptoms.
  4. Fail fast on incomplete frontmatter or missing terminal sections.

### Risk 2: Convergence loop exhausts budget before 3 iterations
- **Mapped source**: Risk Inventory #2
- **Affected requirements**:
  - `FR-PORTIFY-CLI.7b`
  - `FR-PORTIFY-CLI.7h`
  - `FR-PORTIFY-CLI.7n`
- **Mitigations**:
  1. Perform TurnLedger budget check before each launch.
  2. Estimate remaining budget from prior iteration token and runtime patterns.
  3. Use explicit ESCALATED terminal state instead of ambiguous failure.
  4. Ensure contract reflects partial completion clearly.

### Risk 3: `/sc:brainstorm` and `/sc:spec-panel` fail to produce machine-readable markers
- **Mapped source**: Risk Inventory #3
- **Affected requirements**:
  - `FR-PORTIFY-CLI.6c`
  - `FR-PORTIFY-CLI.6f`
  - `FR-PORTIFY-CLI.7g`
- **Mitigations**:
  1. Prepend strict output-shape instructions in subprocess prompts.
  2. Parse structurally first, semantically second.
  3. Fall back to structural heuristics only when markers are absent.
  4. Emit warnings and downgrade confidence on fallback parsing.
  5. Cover marker-missing scenarios in integration tests.

### Risk 4: Sequential execution yields long wall-clock time
- **Mapped source**: Risk Inventory #4
- **Affected requirements**:
  - `NFR-001`
  - `NFR-002`
- **Mitigations**:
  1. Keep pure-programmatic steps efficient.
  2. Avoid unnecessary artifact inflation between steps.
  3. Report advisory timing overruns rather than misclassifying them as semantic failures.
  4. Instrument phase timing from the start of implementation.

### Risk 5: Self-portification circularity
- **Mapped source**: Risk Inventory #5
- **Affected requirements**:
  - Success Criterion #12
- **Mitigations**:
  1. Keep source workflow files read-only during execution.
  2. Write generated outputs to isolated target directories.
  3. Add meta-test guards against source mutation.
  4. Validate no accidental writes into source workflow tree.

### Risk 6: Subprocess skill invocation fails if commands not installed
- **Mapped source**: Risk Inventory #6
- **Affected requirements**:
  - `FR-PORTIFY-CLI.6j`
  - `FR-PORTIFY-CLI.7l`
- **Mitigations**:
  1. Check `claude` binary at pipeline start.
  2. Check skill availability before the relevant step.
  3. Provide explicit warning-backed fallback path.
  4. Record fallback usage in artifacts and return contract.

### Risk 7: Subprocess cannot read `@path` files outside working directory scope
- **Mapped source**: Risk Inventory #7
- **Affected requirements**:
  - `FR-PORTIFY-CLI.3a`
  - `FR-PORTIFY-CLI.4a`
  - `FR-PORTIFY-CLI.5a`
  - `FR-PORTIFY-CLI.6a`
  - `FR-PORTIFY-CLI.7a`
- **Mitigations**:
  1. Pass `--add-dir` for both work directory and workflow path.
  2. Verify file accessibility with an early smoke test before full pipeline execution.
  3. Fail with actionable path diagnostics, not generic subprocess errors.

### Risk 8: User review gates lack programmatic interaction mechanism
- **Mapped source**: Risk Inventory #8
- **Affected requirements**:
  - `FR-PORTIFY-CLI.4h`
  - `FR-PORTIFY-CLI.7k`
  - `NFR-011`
- **Mitigations**:
  1. Implement stderr prompt behavior exactly once in shared review-gate handling.
  2. Add `--skip-review` bypass path.
  3. Cover `y`, `n`, and non-interactive scenarios in manual/integration tests.

### Risk 9: Panel review convergence prompt uses wrong mode mapping across iterations
- **Mapped source**: Risk Inventory #9
- **Affected requirements**:
  - `FR-PORTIFY-CLI.7m`
- **Mitigations**:
  1. Encode iteration prompt contract explicitly.
  2. Run both focus and critique modes in one subprocess every iteration.
  3. Validate output contains both expected sections before accepting iteration results.

## Residual-risk management

1. Maintain an explicit unresolved-issues register linked to Section 11 / Section 12 handling.
2. Treat open questions with medium impact as must-resolve before M5:
   - Resume from Phase 3 failure
   - NDJSON signal vocabulary
   - Resume from Phase 4
   - `--resume` and `--start` CLI flags
3. Treat low-impact inconsistencies as documentation blockers, not functional blockers, unless they affect gates.

---

# 4. Resource Requirements and Dependencies

## Team roles

Given the complexity profile and domains detected (`backend`, `cli`, `devops`, `testing`), the recommended resource plan is:

1. **Primary backend/CLI engineer**
   - Owns executor, config models, process integration, step orchestration.
2. **Quality engineer / test owner**
   - Owns unit, integration, E2E, and meta-test coverage.
3. **Analyzer/reviewer**
   - Owns gate semantics, failure classification, artifact validation, and open-question closure.
4. **Optional devops/tooling support**
   - Assists with CI wiring, environment pre-flight checks, and reproducible execution.

## Dependency plan

The extraction identifies 8 core dependencies.

### Internal dependencies
1. `pipeline.models`
   - Needed for base-type extension.
   - Must be consumed, not modified.
2. `pipeline.gates`
   - Needed for gate validation engine reuse.
3. `pipeline.process`
   - Needed for subprocess behavior inheritance.
4. `sprint.models`
   - Needed for `TurnLedger` budget management.
5. `sprint.process`
   - Needed for signal handling and graceful shutdown.

### External/runtime dependencies
6. `/sc:brainstorm`
   - Required by `FR-PORTIFY-CLI.6a`
   - Must be pre-flight validated; fallback available.
7. `/sc:spec-panel`
   - Required by `FR-PORTIFY-CLI.7a`
   - Must be pre-flight validated; fallback available.
8. `claude` binary
   - Required for all Claude-assisted steps
   - Must be validated before Phase 2 begins.

### Python library dependencies
- `click>=8.0.0`
- `rich>=13.0.0`
- `pyyaml`

## Environment requirements

1. Python 3.10+ features must be available.
2. CLI execution environment must support:
   - subprocess invocation,
   - path references,
   - interactive stderr review prompts.
3. CI environment must support:
   - static analysis,
   - integration tests,
   - end-to-end pipeline execution,
   - artifact inspection.

## Resource loading considerations

1. Claude-assisted phases should be budgeted separately from deterministic phases.
2. Phase 3 and Phase 4 are the most resource-intensive due to:
   - artifact size,
   - retries,
   - convergence loop,
   - skill invocation.
3. Monitoring and logging should be implemented early to keep diagnosis cost low when failures occur.

---

# 5. Success Criteria and Validation Approach

The extraction provides 12 measurable success criteria. The roadmap below aligns each to validation type and release gate.

## Primary release gates

### Gate A — Deterministic Core Integrity
Validated by:
- `FR-PORTIFY-CLI.1`
- `FR-PORTIFY-CLI.2`
- `NFR-006`

Checks:
1. Config resolution is deterministic.
2. Discovery output is complete and reproducible.
3. Python, not Claude, controls sequencing.

### Gate B — Artifact Structural Quality
Validated by:
- `FR-PORTIFY-CLI.3f`
- `FR-PORTIFY-CLI.4g`
- `FR-PORTIFY-CLI.5f`
- `FR-PORTIFY-CLI.6h`
- `FR-PORTIFY-CLI.7j`

Checks:
1. All generated artifacts pass tiered gate validation.
2. Required sections and frontmatter exist.
3. Machine-readable markers are parseable.

### Gate C — Review and Convergence Integrity
Validated by:
- `FR-PORTIFY-CLI.4h`
- `FR-PORTIFY-CLI.7b`
- `FR-PORTIFY-CLI.7c`
- `FR-PORTIFY-CLI.7h`
- `FR-PORTIFY-CLI.7k`
- `NFR-011`

Checks:
1. Review pauses behave correctly.
2. Convergence predicate is enforced correctly.
3. ESCALATED state works when needed.
4. Human rejection halts with `USER_REJECTED`.

### Gate D — Nonfunctional Compliance
Validated by:
- `NFR-001`
- `NFR-002`
- `NFR-003`
- `NFR-004`
- `NFR-005`
- `NFR-007`
- `NFR-008`
- `NFR-009`
- `NFR-010`

Checks:
1. Timing advisories measured.
2. No async code appears.
3. Gate signatures are correct.
4. Base packages remain untouched.
5. Panel review is additive-only.
6. Failure contracts are complete.
7. Skill reuse is real, not simulated.

## Validation matrix against success criteria

1. **Success Criterion 1 — Full pipeline execution completes**
   - Validation: real integration test
   - Release priority: blocker

2. **Success Criterion 2 — Dry-run halts correctly**
   - Validation: integration test with `--dry-run`
   - Release priority: blocker

3. **Success Criterion 3 — STRICT gates enforce quality**
   - Validation: malformed artifact test
   - Release priority: blocker

4. **Success Criterion 4 — Convergence loop terminates**
   - Validation: unit + integration
   - Release priority: blocker

5. **Success Criterion 5 — Downstream readiness gate**
   - Validation: boundary test (`7.0` true, `6.9` false)
   - Release priority: blocker

6. **Success Criterion 6 — Quality scores arithmetic**
   - Validation: unit test with known means
   - Release priority: blocker

7. **Success Criterion 7 — Zero placeholders (SC-003)**
   - Validation: semantic gate
   - Release priority: blocker

8. **Success Criterion 8 — Return contract completeness**
   - Validation: unit coverage across outcome types
   - Release priority: blocker

9. **Success Criterion 9 — Resume command generation**
   - Validation: unit tests
   - Release priority: high

10. **Success Criterion 10 — No base module changes**
    - Validation: CI diff check
    - Release priority: blocker

11. **Success Criterion 11 — Synchronous execution**
    - Validation: static analysis
    - Release priority: blocker

12. **Success Criterion 12 — Self-portification**
    - Validation: end-to-end meta-test
    - Release priority: blocker

## Recommended validation order

1. Static and deterministic tests first.
2. Artifact structural tests second.
3. Review-gate and fallback tests third.
4. End-to-end real pipeline runs fourth.
5. Self-portification last, as the final confidence check.

## Analyzer-specific recommendations

1. Prefer artifact inspection over subprocess stdout interpretation.
2. Require every failure path to emit enough data for independent diagnosis.
3. Reject ambiguous “looks successful” outcomes unless supported by:
   - exit codes,
   - artifacts,
   - gates,
   - contract fields.

---

# 6. Timeline Estimates per Phase

## Summary timeline

| Phase | Name | Duration | Exit Milestone |
|---|---|---:|---|
| Phase 0 | Foundation and Architecture Lock | 2-3 days | M0 |
| Phase 1 | Deterministic Core Pipeline Steps | 3-4 days | M1 |
| Phase 2 | Analysis and Design Artifacts | 4-5 days | M2 |
| Phase 3 | Spec Synthesis and Gap Expansion | 4-5 days | M3 |
| Phase 4 | Panel Review, Convergence, and Release Readiness | 4-6 days | M4 |
| Phase 5 | Validation, Hardening, and Meta-Test Closure | 3-5 days | M5 |

## Total estimated range
- **20-28 working days**

## Critical path

The critical path is strictly sequential due to requirement dependencies:

1. `FR-PORTIFY-CLI.1`
2. `FR-PORTIFY-CLI.2`
3. `FR-PORTIFY-CLI.3`
4. `FR-PORTIFY-CLI.4`
5. `FR-PORTIFY-CLI.5`
6. `FR-PORTIFY-CLI.6`
7. `FR-PORTIFY-CLI.7`

## Parallelizable work

Although step execution is sequential, implementation work can be partially parallelized:

### Parallel stream A — Core implementation
- models
- process wrapper
- executor scaffolding
- deterministic steps

### Parallel stream B — Validation harness
- unit tests for gates
- static checks
- contract validation utilities
- diff-based compliance checks

### Parallel stream C — Review and diagnostics
- monitor/report generator
- TUI behavior
- signal vocabulary
- failure classifier

## Schedule risks affecting timeline

1. If skill fallback behavior is underspecified, Phase 3 and Phase 4 can slip.
2. If resume semantics are not resolved early, Phase 4 and Phase 5 rework is likely.
3. If additive-only enforcement is implemented late, panel review may require redesign.
4. If end-to-end tests are deferred, defects will cluster in the final week.

## Timeline control recommendations

1. Do not start Phase 3 until Phase 2 artifacts consistently pass STRICT gates.
2. Do not start self-portification until:
   - fallback logic,
   - convergence logic,
   - contract completeness
   are already verified.
3. Treat any unresolved medium-impact open question as a schedule threat, not documentation debt.

---

# Recommended Immediate Next Actions

1. Lock Phase 0 scope and module boundaries, including the accepted 18-module structure.
2. Resolve the highest-impact open questions before Phase 2:
   - resume semantics,
   - CLI surface for `--resume` and `--start`,
   - signal vocabulary.
3. Implement `FR-PORTIFY-CLI.1` and `FR-PORTIFY-CLI.2` with performance instrumentation first.
4. Build gate-validation utilities before writing prompts for `FR-PORTIFY-CLI.3` and `FR-PORTIFY-CLI.4`.
5. Reserve final release confidence for real artifact-producing E2E runs, especially Success Criterion #12.
