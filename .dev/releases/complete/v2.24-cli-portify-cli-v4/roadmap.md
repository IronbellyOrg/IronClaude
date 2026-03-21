---
spec_source: "portify-release-spec.md"
complexity_score: 0.85
adversarial: true
---

# CLI Portify Pipeline — Merged Roadmap

## 1. Executive Summary

This roadmap delivers a high-complexity CLI portification pipeline (`cli-portify`) that converts inference-driven SuperClaude workflows into deterministic, synchronous Python CLI pipelines. The implementation combines pure-programmatic steps, Claude-assisted generation, subprocess-based skill reuse, convergence logic, TUI/CLI integration, gate enforcement, and resumable failure handling under strict architectural constraints.

The release is governed by four dominant architectural concerns:

1. **Deterministic orchestration** — Python controls sequencing, convergence, retries, gating, status, and resume behavior. Claude output is constrained, observable, and subordinate to Python-controlled execution.
2. **Strict separation of responsibilities** — Pure-programmatic steps own path resolution, discovery, validation, and flow control. Claude-assisted steps own content generation only.
3. **Safe reuse of existing framework capabilities** — The implementation extends `pipeline` and `sprint` base types rather than forking behavior. `/sc:brainstorm` and `/sc:spec-panel` are reused via subprocess, not reimplemented.
4. **Production-grade quality gates** — STRICT validation is required across core content-producing steps. Success depends on convergence, score thresholds, structural validity, failure-path completeness, and additive-only modification behavior.

**Tradeoff Priority Framework** — When implementation conflicts arise, resolve in this order:

1. Deterministic runner control
2. STRICT gate integrity
3. Base-module immutability
4. Skill reuse with safe fallbacks
5. Operational resilience (resume/contracts/monitoring)

**Delivery Strategy**: 7-milestone sequential dependency chain with 3 parallel work streams overlaid. 3 governance gates at high-value decision points. Real eval-driven validation anchored by self-portification meta-test.

**Estimated Duration**: 24–30 working days.

---

## 2. Phased Implementation Plan

### Milestone 1: Architecture Baseline and Scope Lock

**Goal**: Establish the final implementation contract, resolve critical open questions, and de-risk core assumptions before coding begins.

**Primary Outcomes**
- Lock 18-module additive architecture under `cli_portify/`.
- Confirm extension points into `pipeline.models`, `pipeline.gates`, `pipeline.process`, `sprint.models`, and `sprint.process`.
- Define resume state machine across all failure paths.
- Design and document a specific, testable additive-only enforcement mechanism for NFR-008.

**Requirements Addressed**
- NFR-003, NFR-005, NFR-006, NFR-007, NFR-010
- FR-PORTIFY-CLI.4f (executor ownership design)

**Key Work Items**
1. Define the target package/module structure for `cli_portify/`.
2. Formalize inheritance model: `PortifyConfig` → `PipelineConfig`, `PortifyStepResult` → `StepResult`, `PortifyProcess` → `ClaudeProcess`.
3. Define executor vs subprocess responsibility boundaries.
4. Freeze CLI surface: `run`, `--dry-run`, `--skip-review`, `--resume`, `--start`.
5. Freeze synchronous-only rule: no `async def`, no `await`.
6. Confirm zero changes to `pipeline/` or `sprint/`.
7. Design resume-state decision table covering all failure paths.
8. Design and document the additive-only enforcement mechanism (structural comparison, section hashing, or equivalent). This must be a specific, testable design — not deferred to implementation.
9. Add static checks to prevent `async def` or `await` in `cli_portify/`.
10. Define NDJSON signal vocabulary.

**Milestone Deliverables**
- Architecture decision record for `cli_portify/`
- CLI surface definition
- Step contract matrix
- Resume-state decision table
- Additive-only enforcement design document

**Exit Criteria**
- Open Question 9 (CLI surface) resolved.
- Open Questions 1, 2, 3 (resume semantics, signal vocabulary) resolved at design level.
- Architectural constraints mapped to concrete modules.
- Additive-only enforcement mechanism designed and documented.

**Timeline**: 2–3 days

#### Governance Gate 1 (Lightweight)
Approve architecture contract, CLI surface, resume state machine design, and additive-only enforcement design before code scales.

---

### Milestone 2: Programmatic Foundation — Config, Discovery, Models, Contracts

**Goal**: Implement the deterministic base layer that all Claude-assisted work depends on.

**Primary Outcomes**
- `validate-config` and `discover-components` fully functional and fast.
- Shared data models, result contracts, logging schema, and failure defaults established.

**Requirements Addressed**
- FR-PORTIFY-CLI.1a–1f
- FR-PORTIFY-CLI.2a–2f
- NFR-004, NFR-009

**Key Work Items**
1. Implement workflow path resolution and `SKILL.md` presence checks.
2. Implement deterministic CLI-name derivation: `sc-` prefix stripping, `-protocol` suffix stripping, kebab/snake conversion, hard failure on derivation ambiguity.
3. Validate output directory parent existence and writability.
4. Detect name collisions with non-portified modules.
5. Emit `validate-config-result.json`.
6. Implement component inventory discovery: `SKILL.md`, `refs/`, `rules/`, `templates/`, `scripts/`, command-file lookup across both command roots.
7. Add accurate line counting with documented handling for the 1MB cap inconsistency (Open Question #6).
8. Emit `component-inventory.md` with required frontmatter.
9. Establish return-contract defaults for success, failure, partial, and dry-run outcomes.
10. Define failure code catalog.
11. Ensure all gate functions conform to `tuple[bool, str]`.

**Exit Criteria**
- FR-PORTIFY-CLI.1 and FR-PORTIFY-CLI.2 acceptance criteria pass.
- Performance constraints (NFR-004) measured and passing.
- Failure-path defaults populated on all tested outcomes.
- File discovery is deterministic and shell-independent.

**Timeline**: 3–4 days

---

### Milestone 3: Analysis and Pipeline Design Layer

**Goal**: Implement the first two Claude-assisted steps with deterministic gate enforcement around nondeterministic output.

**Primary Outcomes**
- Workflow analysis output generated, bounded, and validated.
- Pipeline design output fully maps steps, gates, prompts, and execution model.
- Review gate and dry-run semantics proven.

**Requirements Addressed**
- FR-PORTIFY-CLI.3a–3f
- FR-PORTIFY-CLI.4a–4h
- NFR-005, NFR-006

**Key Work Items**
1. Build prompt/input assembly using `@path` references only.
2. Implement `analyze-workflow` subprocess execution via `PortifyProcess`.
3. Validate `portify-analysis.md` structure: Source Components, Step Graph, Gates Summary, Data Flow Diagram, Classification Summary.
4. Enforce line-count ceiling (400 lines) and structural checks.
5. Implement `design-pipeline` subprocess execution.
6. Validate that all steps have mappings, gate definitions, and execution model specification.
7. Ensure pure-programmatic steps contain actual Python implementation, not design prose (FR-PORTIFY-CLI.4d).
8. Implement user review halt point after design.
9. Ensure `--dry-run` exits here with a complete dry-run contract.
10. Implement resume path for M3 failures as designed in M1.

**Exit Criteria**
- STRICT tier passes for both `portify-analysis.md` and `portify-spec.md`.
- `--dry-run` halts after design review exactly as required.
- Deterministic runner remains source of truth for state.
- Review gate TUI interaction works correctly.

**Timeline**: 4–5 days

---

### Milestone 4: Spec Synthesis and Brainstorm Integration

**Goal**: Produce the release spec with zero placeholders and enrich it with structured gap analysis.

**Primary Outcomes**
- Release spec generated with zero `{{SC_PLACEHOLDER:*}}` markers.
- Brainstorm skill reused safely with fallback and structural validation.
- Additive-only modification behavior preserved.

**Requirements Addressed**
- FR-PORTIFY-CLI.5a–5g
- FR-PORTIFY-CLI.6a–6j
- NFR-008, NFR-010

**Key Work Items**
1. Implement `synthesize-spec` prompt builder and output parser.
2. Add placeholder detection and retry logic with specific remaining placeholder names.
3. Enforce exact 7 FR count and logical step consolidation mapping.
4. Validate required conditional sections (4.3, 4.5, 5, 8.3, 9).
5. Pre-flight check `/sc:brainstorm` availability.
6. If available, invoke `/sc:brainstorm` via subprocess; otherwise execute inline fallback with explicit warning.
7. Implement Section 12 (Brainstorm Gap Analysis) append semantics.
8. Enforce structural validity: findings table with Gap ID column, or literal zero-gap summary text (FR-PORTIFY-CLI.6i).
9. Route findings as `[INCORPORATED]` or `[OPEN]` (routed to Section 11).
10. Implement resume path for M4 failures as designed in M1.
11. Measure and report phase timing for NFR-001.

**Exit Criteria**
- Zero `{{SC_PLACEHOLDER:*}}` in synthesized spec.
- STANDARD/STRICT gates pass where required.
- Section 12 is structurally valid (not heading-only).
- No destructive rewrite behavior introduced.
- Fallback path produces warning in artifacts and return contract.

**Timeline**: 4–5 days

---

### Milestone 5: Panel Review, Convergence Engine, and Quality Gates

**Goal**: Build the most critical control loop: iterative expert review with bounded convergence, quality thresholds, and downstream readiness enforcement.

**Primary Outcomes**
- Expert panel loop with max-3 iterations, convergence predicate, timeout control, budget guard, and downstream readiness gate.
- Machine-readable convergence outputs produced and enforced.

**Requirements Addressed**
- FR-PORTIFY-CLI.7a–7n
- NFR-001, NFR-002, NFR-005, NFR-008, NFR-010, NFR-011

**Key Work Items**
1. Pre-flight check `/sc:spec-panel` availability; implement fallback prompt path with warning.
2. Implement dual-mode iteration execution: focus pass + critique pass in single subprocess boundary.
3. Implement convergence state model and iteration counter (max 3).
4. Implement independent per-iteration timeout (default 300s).
5. Integrate TurnLedger budget guard before each launch.
6. Parse and validate: `CONVERGENCE_STATUS`, `UNADDRESSED_CRITICALS`, `QUALITY_OVERALL`.
7. Compute quality scores: clarity, completeness, testability, consistency; `overall = mean(...)`.
8. Implement additive-only enforcement using the mechanism designed in M1.
9. Implement terminal state handling: CONVERGED, ESCALATED.
10. Enforce downstream-ready gate: `overall >= 7.0`.
11. Add review gate at end of panel phase.
12. Emit `panel-report.md`.
13. Implement resume path for M5 failures.
14. Measure and report phase timing for NFR-002.

**Exit Criteria**
- Boundary check: `7.0` passes, `6.9` fails.
- Zero unaddressed CRITICAL findings on converged path.
- ESCALATED path valid and observable.
- Additive-only enforcement active and tested.
- Review gate behavior works interactively.

**Timeline**: 5–6 days

#### Governance Gate 2 (Heavyweight)
Approve convergence engine behavior, additive-only enforcement in practice, quality thresholds, and resume semantics before release-hardening investment.

---

### Milestone 6: Monitoring, Resume Integration, UX, and Failure Recovery

**Goal**: Consolidate operational concerns into a coherent, validated layer across all exit paths.

**Primary Outcomes**
- Monitoring, diagnostics, signal extraction, review pauses, and contract completeness behave consistently across all exit paths.
- Resume logic (designed in M1, implemented incrementally in M3–M5) is validated as a coherent whole.

**Requirements Addressed**
- NFR-005, NFR-006, NFR-009, NFR-011

**Key Work Items**
1. Implement monitor and diagnostic collector.
2. Finalize NDJSON signal vocabulary implementation.
3. Validate review pause interaction on stderr across all gate points.
4. Validate resume semantics cohesively across all failure paths:
   - Synthesize-spec failure recovery
   - Panel review restart
   - Partial spec existence handling
5. Validate `resume_command()` output consistency.
6. Ensure every exit path emits a complete return contract.
7. Validate `--skip-review` bypass behavior end-to-end.
8. Normalize warning vs failure classification.

**Exit Criteria**
- Open Questions 1, 2, 3, 8 validated in implementation (designed in M1).
- Partial and resumed runs are reproducible.
- Review gating behaves as specified across all gate points.
- Every exit path emits a structurally complete contract.

**Timeline**: 3–4 days

---

### Milestone 7: Validation, Real Evals, and Release Hardening

**Goal**: Convert implementation confidence into release confidence using real pipeline execution, adversarial failure-path coverage, and architectural compliance checks.

**Requirements Addressed**
- Success Criteria 1–12
- NFR-003, NFR-007, NFR-009, NFR-010

**Key Work Items**

Validation must follow this ordering:

#### Layer 1: Static and Deterministic Tests
1. Static checks: no `async def`/`await` in `cli_portify/`.
2. Diff checks: no modifications to `pipeline/` or `sprint/`.
3. Gate function signature compliance: `tuple[bool, str]`.

#### Layer 2: Artifact Structural Tests
4. Unit tests for gate functions, score arithmetic, convergence predicate, resume command generation, failure contract completeness.
5. Malformed artifact rejection tests (STRICT gate enforcement).

#### Layer 3: Review and Fallback Tests
6. Integration tests for review-gate accept/reject/non-interactive behavior.
7. Skill fallback behavior tests (brainstorm and spec-panel unavailability).
8. `--dry-run` halt verification.

#### Layer 4: End-to-End Pipeline Runs
9. Full pipeline execution on a real skill target.
10. Resumed execution path test.
11. Timing advisory validation for NFR-001 and NFR-002.
12. Confirm all reports are runner-authored from observed data only (no Claude self-reporting).

#### Layer 5: Self-Portification (Final Confidence Check)
13. `superclaude cli-portify run src/superclaude/skills/sc-cli-portify-protocol/`
14. Verify source workflow files remain unmodified (read-only guard).
15. Verify generated artifacts land in isolated target directory.

**Validation Rules**
- Prefer artifact inspection over subprocess stdout interpretation.
- Require every failure path to emit enough data for independent diagnosis.
- Reject ambiguous "looks successful" outcomes unless supported by exit codes, artifacts, gates, or contract fields.

**Exit Criteria**
- Success Criteria 1–12 satisfied or explicitly escalated with rationale.
- No architectural constraint violations remain.
- Real artifact-producing runs are reproducible.

**Timeline**: 4–5 days

#### Governance Gate 3 (Final Release Gate)
Require passing real eval evidence, self-portification meta-test evidence, and architecture guard evidence before release.

---

## 3. Parallel Work Streams

Although milestone execution follows a sequential dependency chain, implementation work can be partially parallelized across three named streams:

| Stream | Work Items | Can Start | Dependencies |
|---|---|---|---|
| **A — Core Implementation** | Models, process wrapper, executor scaffolding, deterministic steps, Claude-assisted steps | M1 | Sequential per FR chain |
| **B — Validation Harness** | Unit tests for gates, static checks, contract validators, diff-based compliance | M2 | Zero dependency on Claude-assisted steps |
| **C — Review & Diagnostics** | Monitor/report generator, TUI behavior, signal vocabulary implementation | M2 | Failure taxonomy from M1; full validation deferred to M6 |

Stream B has zero dependency on Claude-assisted step implementation and can run continuously from M2 onward. Stream C requires the failure taxonomy and signal vocabulary designed in M1 but can begin implementation during M2.

---

## 4. Risk Assessment and Mitigation Strategies

### High-Priority Risks

#### Risk 1: Large context windows in Steps 5–7 cause Claude output truncation
- **Affected**: FR-PORTIFY-CLI.5a, 5b, 6b, 7f
- **Mitigations**:
  1. Enforce `@path` references only — never inline large artifacts.
  2. Keep upstream artifacts concise and machine-structured.
  3. Add strict structural post-checks after every Claude-assisted step.
  4. Fail fast on incomplete frontmatter or missing terminal sections.

#### Risk 2: Convergence loop exhausts budget before 3 iterations
- **Affected**: FR-PORTIFY-CLI.7b, 7h, 7n
- **Mitigations**:
  1. TurnLedger budget check before each launch.
  2. Per-iteration budget estimate from prior token/runtime patterns.
  3. Explicit ESCALATED terminal state (not ambiguous failure).
  4. Contract reflects partial completion clearly.

#### Risk 3: `/sc:brainstorm` and `/sc:spec-panel` fail to produce machine-readable markers
- **Affected**: FR-PORTIFY-CLI.6c, 6f, 7g
- **Mitigations**:
  1. Prepend strict output-shape instructions in subprocess prompts.
  2. Parse structurally first, semantically second.
  3. Fall back to structural heuristics only when markers absent.
  4. Emit warnings and downgrade confidence on fallback parsing.
  5. Cover marker-missing scenarios in integration tests.

#### Risk 4: Sequential execution yields long wall-clock time
- **Affected**: NFR-001, NFR-002
- **Mitigations**:
  1. Keep pure-programmatic steps efficient.
  2. Avoid unnecessary artifact inflation between steps.
  3. Report advisory timing overruns rather than misclassifying as semantic failures.
  4. Instrument phase timing from start of implementation.

#### Risk 5: Self-portification circularity
- **Affected**: Success Criterion 12
- **Mitigations**:
  1. Treat source workflow files as read-only during execution.
  2. Write generated outputs to isolated target directories.
  3. Add meta-test guards against source mutation.

### Medium-Priority Risks

#### Risk 6: Subprocess skill invocation fails if commands not installed
- **Affected**: FR-PORTIFY-CLI.6j, 7l
- **Mitigations**:
  1. Check `claude` binary at pipeline start.
  2. Check skill availability before relevant step.
  3. Explicit warning-backed fallback path.
  4. Record fallback usage in artifacts and return contract.

#### Risk 7: Subprocess cannot read `@path` files outside working directory
- **Affected**: FR-PORTIFY-CLI.3a, 4a, 5a, 6a, 7a
- **Mitigations**:
  1. `PortifyProcess` passes `--add-dir` for both work directory and workflow path.
  2. Early smoke test for file accessibility before full pipeline execution.
  3. Actionable path diagnostics on failure.

#### Risk 8: User review gates lack programmatic interaction mechanism
- **Affected**: FR-PORTIFY-CLI.4h, 7k; NFR-011
- **Mitigations**:
  1. Implement stderr prompt behavior once in shared review-gate handler.
  2. `--skip-review` bypass path.
  3. Cover `y`, `n`, and non-interactive scenarios in tests.

#### Risk 9: Panel review convergence uses wrong mode mapping across iterations
- **Affected**: FR-PORTIFY-CLI.7m
- **Mitigations**:
  1. Encode dual-mode (focus + critique) iteration contract explicitly in executor.
  2. Test iteration behavior independently.
  3. Freeze prompt contract for focus + critique sequencing.

### Residual Risk Management
- Maintain unresolved-issues register linked to Section 11/12 handling.
- Treat unresolved medium-impact open questions as schedule threats, not documentation debt.
- Treat low-impact inconsistencies as documentation blockers only unless they affect gates.

---

## 5. Resource Requirements and Dependencies

### Engineering Resources

| Role | Responsibility |
|---|---|
| Primary backend/CLI engineer | Executor, config models, process integration, step orchestration, convergence engine |
| Quality engineer / test owner | Unit, integration, E2E, meta-test coverage; validation harness (Stream B) |
| Architectural reviewer | Gate semantics, failure classification, artifact validation, NFR compliance, open-question closure |

### Technical Dependencies

#### Internal Package Dependencies (consume, never modify)
1. `pipeline.models` — base-type extension
2. `pipeline.gates` — gate validation engine reuse
3. `pipeline.process` — subprocess behavior inheritance
4. `sprint.models` — TurnLedger budget management
5. `sprint.process` — signal handling, graceful shutdown

#### External/Runtime Dependencies
6. `/sc:brainstorm` — required by FR-PORTIFY-CLI.6a; pre-flight validated with fallback
7. `/sc:spec-panel` — required by FR-PORTIFY-CLI.7a; pre-flight validated with fallback
8. `claude` binary — required for all Claude-assisted steps; validated before M3

#### Python Library Dependencies
- `click>=8.0.0`
- `rich>=13.0.0`
- `pyyaml`
- Python `>=3.10`

### Environment Requirements
- Subprocess invocation with path references and `--add-dir` support
- Interactive stderr review prompts
- CI environment supporting static analysis, integration tests, E2E pipeline execution, and artifact inspection

---

## 6. Success Criteria and Validation Approach

### Release Gates

| Gate | Validates | Checks |
|---|---|---|
| **A — Deterministic Core Integrity** | FR-PORTIFY-CLI.1, 2; NFR-006 | Config resolution deterministic; discovery reproducible; Python controls sequencing |
| **B — Artifact Structural Quality** | FR-PORTIFY-CLI.3f, 4g, 5f, 6h, 7j | All artifacts pass tiered gates; required sections/frontmatter exist; markers parseable |
| **C — Review and Convergence Integrity** | FR-PORTIFY-CLI.4h, 7b, 7c, 7h, 7k; NFR-011 | Review pauses correct; convergence predicate enforced; ESCALATED works; USER_REJECTED halts |
| **D — Nonfunctional Compliance** | NFR-001–010 | Timing advisories; no async; gate signatures; base packages untouched; additive-only; failure contracts complete; skill reuse real |

### Success Criteria Matrix

| # | Criterion | Validation Type | Priority |
|---|---|---|---|
| 1 | Full pipeline execution completes | Real integration test | Blocker |
| 2 | Dry-run halts correctly | Integration test with `--dry-run` | Blocker |
| 3 | STRICT gates enforce quality | Malformed artifact test | Blocker |
| 4 | Convergence loop terminates | Unit + integration | Blocker |
| 5 | Downstream readiness gate exact | Boundary test (7.0 true, 6.9 false) | Blocker |
| 6 | Quality scores arithmetic correct | Unit test with known means | Blocker |
| 7 | Zero placeholders (SC-003) | Semantic gate | Blocker |
| 8 | Return contract complete on every path | Unit coverage across outcome types | Blocker |
| 9 | Resume command generation correct | Unit tests | High |
| 10 | No base module changes | CI diff check | Blocker |
| 11 | Synchronous-only implementation | Static analysis | Blocker |
| 12 | Self-portification succeeds | E2E meta-test | Blocker |

---

## 7. Requirement Traceability

### Functional Requirements → Milestones
| Requirement | Milestone |
|---|---|
| FR-PORTIFY-CLI.1a–1f | M2 |
| FR-PORTIFY-CLI.2a–2f | M2 |
| FR-PORTIFY-CLI.3a–3f | M3 |
| FR-PORTIFY-CLI.4a–4h | M3 |
| FR-PORTIFY-CLI.5a–5g | M4 |
| FR-PORTIFY-CLI.6a–6j | M4 |
| FR-PORTIFY-CLI.7a–7n | M5 |

### Non-Functional Requirements → Milestones
| Requirement | Milestones |
|---|---|
| NFR-001, NFR-002 | M5, M7 |
| NFR-003 | M1, M2, M7 |
| NFR-004 | M2 |
| NFR-005, NFR-006 | M1, M3, M5, M6, M7 |
| NFR-007 | M1, M7 |
| NFR-008 | M1 (design), M4, M5 |
| NFR-009 | M2, M6, M7 |
| NFR-010 | M1, M4, M5, M7 |
| NFR-011 | M5, M6 |

---

## 8. Timeline Summary

| Milestone | Scope | Duration | Governance Gate |
|---|---|---:|---|
| M1 | Architecture baseline, scope lock, enforcement design | 2–3 days | Gate 1 (lightweight) |
| M2 | Programmatic foundation: config, discovery, models | 3–4 days | — |
| M3 | Analysis and pipeline design (Claude-assisted) | 4–5 days | — |
| M4 | Spec synthesis and brainstorm integration | 4–5 days | — |
| M5 | Panel review, convergence engine, quality gates | 5–6 days | Gate 2 (heavyweight) |
| M6 | Monitoring, resume integration, UX, failure recovery | 3–4 days | — |
| M7 | Validation, real evals, release hardening | 4–5 days | Gate 3 (final release) |
| **Total** | | **24–30 days** | |

### Critical Path
The critical path follows the sequential FR dependency chain: FR-PORTIFY-CLI.1 → 2 → 3 → 4 → 5 → 6 → 7. Parallel streams B and C reduce total duration by ~3–5 days compared to fully serial execution.

### Schedule Risks
1. Skill fallback underspecification can slip M4 and M5.
2. If additive-only enforcement design is weak in M1, M5 may require redesign.
3. If E2E tests are deferred past M7, defects cluster in the final week.
4. Unresolved medium-impact open questions are schedule threats, not documentation debt.

---

## 9. Immediate Next Actions

1. Lock M1 scope: module boundaries, CLI surface, resume state machine, additive-only enforcement design.
2. Resolve highest-impact open questions during M1: resume semantics, `--resume`/`--start` CLI flags, NDJSON signal vocabulary.
3. Implement FR-PORTIFY-CLI.1 and FR-PORTIFY-CLI.2 with performance instrumentation.
4. Begin Stream B (validation harness) in parallel with M2.
5. Build gate-validation utilities before writing prompts for FR-PORTIFY-CLI.3 and FR-PORTIFY-CLI.4.
6. Reserve final release confidence for real artifact-producing E2E runs, especially Success Criterion 12.
