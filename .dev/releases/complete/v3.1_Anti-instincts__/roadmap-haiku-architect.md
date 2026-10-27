---
spec_source: "anti-instincts-gate-unified.md"
complexity_score: 0.72
primary_persona: architect
---

# 1. Executive summary

This roadmap delivers a deterministic anti-instinct validation layer for the roadmap and sprint pipelines to catch a specific failure mode: plans that mention scaffolding, dispatch mechanisms, or code fingerprints without ever wiring them into executable reality. Architecturally, the implementation should remain additive, stateless, pure-Python, and rollout-gated.

## Primary architectural objective
Build a new `anti-instinct` gate and supporting deterministic analyzers that:
1. Detect undischarged scaffolding obligations.
2. Detect uncovered integration contracts.
3. Measure roadmap coverage of code-level fingerprints.
4. Add a structural extraction audit as a warning-only upstream safeguard.

## Scope summary
- **Functional scope**: 23 requirements across roadmap analysis modules, executor integration, prompt strengthening, gate definition, and sprint rollout wiring.
- **Non-functional scope**: 11 constraints with high emphasis on determinism, latency, statelessness, backward compatibility, and rollout safety.
- **Detected domains**: backend, pipeline-infrastructure, testing, prompt-engineering, sprint-economics.
- **Risk posture**: high but controlled, because the feature spans two execution contexts and several shared pipeline modules, while remaining deterministic and additive.

## Architectural priorities
1. **Preserve pipeline invariants first**
   - `NFR-001`, `NFR-004`, `NFR-008`, `NFR-009`, `NFR-010`
2. **Ship safely behind rollout controls**
   - `FR-SPRINT.1`, `NFR-006`, `NFR-007`
3. **Place the gate in the correct execution topology**
   - `FR-EXEC.1`, `FR-EXEC.2`, `FR-EXEC.4`, `FR-GATE.3`
4. **Calibrate heuristics before enforcement expansion**
   - `FR-MOD4.3`, `NFR-011`

## Delivery recommendation
Implement in **six phases** with two explicit promotion checkpoints:
- **Checkpoint A**: deterministic module correctness and latency proof.
- **Checkpoint B**: shadow-mode evidence for sprint rollout readiness.

This sequence minimizes merge conflicts, protects `master` behavior, and isolates the highest-risk interfaces before broader enablement.

---

# 2. Phased implementation plan with milestones

## Phase 0 — Architecture lock and dependency coordination
**Goal**: remove ambiguity before code changes in shared files.

### Requirements addressed
- `NFR-008`
- `NFR-009`
- `NFR-010`
- Open questions `OQ-003`, `OQ-004`, `OQ-005`, `OQ-006`, `OQ-009`, `OQ-010`

### Work items
1. Confirm and document the following architectural decisions before implementation:
   - Exact `# obligation-exempt` parsing semantics for `FR-MOD1.7`
   - Severity behavior for code-block scaffold detections under `FR-MOD1.8` vs `FR-GATE.2`
   - Coexistence policy for D-03/D-04 overlap per architectural constraint 8
   - Structural audit graduation mechanism for `FR-MOD4.3`
   - Contract-specific vs generic coverage matching for `OQ-009`
   - Whether prompt-required wiring section is downstream-validated for `OQ-010`
2. Freeze integration points in shared files:
   - `src/superclaude/cli/roadmap/gates.py`
   - `src/superclaude/cli/roadmap/executor.py`
   - `src/superclaude/cli/roadmap/prompts.py`
   - `src/superclaude/cli/sprint/models.py`
   - `src/superclaude/cli/sprint/executor.py`
3. Establish merge coordination plan with any parallel work on `WIRING_GATE`.

### Milestone
- **M0**: Architecture decision record approved for unresolved behaviors and file-touch coordination.

### Timeline estimate
- **0.5-1 day**

---

## Phase 1 — Deterministic analyzer module implementation
**Goal**: build the pure functions first, independent of pipeline wiring.

### Requirements addressed
#### Obligation scanner
- `FR-MOD1.1`
- `FR-MOD1.2`
- `FR-MOD1.3`
- `FR-MOD1.4`
- `FR-MOD1.5`
- `FR-MOD1.6`
- `FR-MOD1.7`
- `FR-MOD1.8`

#### Integration contracts
- `FR-MOD2.1`
- `FR-MOD2.2`
- `FR-MOD2.3`
- `FR-MOD2.4`
- `FR-MOD2.5`
- `FR-MOD2.6`

#### Fingerprints
- `FR-MOD3.1`
- `FR-MOD3.2`
- `FR-MOD3.3`
- `FR-MOD3.4`

#### Structural audit
- `FR-MOD4.1`
- `FR-MOD4.2`
- `FR-MOD4.3`

#### Non-functional constraints
- `NFR-001`
- `NFR-002`
- `NFR-004`

### Work items
1. Implement new pure-Python modules in `src/superclaude/cli/roadmap/`:
   - `obligation_scanner.py`
   - `integration_contracts.py`
   - `fingerprint.py`
   - `spec_structural_audit.py`
2. Define dataclasses and results with no I/O:
   - `ObligationReport` and `Obligation` for `FR-MOD1.6`
   - `IntegrationAuditResult` for `FR-MOD2.6`
3. Build compiled regex sets and normalize matching behavior.
4. Ensure all module APIs follow content-in/result-out semantics only.
5. Add targeted unit tests for:
   - positive detections
   - negative detections
   - deduplication
   - phase parsing fallbacks
   - edge cases around missing component context
   - exemption behavior
   - code-block severity handling
6. Measure combined execution latency against `NFR-002` and `SC-006`.

### Architect guidance
- Keep analyzer modules isolated from executor concerns.
- Do not leak rollout or ledger behavior into analyzer code.
- Favor deterministic explainability over aggressive heuristic recall.

### Milestone
- **M1**: All four analyzers pass unit tests and combined runtime remains below `NFR-002` / `SC-006`.

### Timeline estimate
- **2-3 days**

---

## Phase 2 — Roadmap gate and executor integration
**Goal**: wire deterministic analyzers into the roadmap pipeline at the correct control points.

### Requirements addressed
#### Gate definition
- `FR-GATE.1`
- `FR-GATE.2`
- `FR-GATE.3`

#### Executor wiring
- `FR-EXEC.1`
- `FR-EXEC.2`
- `FR-EXEC.3`
- `FR-EXEC.4`

#### Non-functional constraints
- `NFR-005`
- `NFR-009`
- `NFR-010`

### Work items
1. Define `ANTI_INSTINCT_GATE` in `src/superclaude/cli/roadmap/gates.py` per `FR-GATE.1`.
2. Implement semantic checks:
   - `no_undischarged_obligations`
   - `integration_contracts_covered`
   - `fingerprint_coverage_sufficient`
3. Insert `("anti-instinct", ANTI_INSTINCT_GATE)` into `ALL_GATES` between merge and test-strategy per `FR-GATE.3`.
4. Add `_run_structural_audit()` after extract gate pass and before generate steps per `FR-EXEC.1`.
5. Add anti-instinct `Step` between merge and test-strategy:
   - `timeout_seconds=30`
   - `retry_limit=0`
   - `gate_scope=GateScope.TASK`
6. Implement `_run_anti_instinct_audit()` to:
   - read spec + merged roadmap
   - execute the three audits
   - emit `anti-instinct-audit.md` with required frontmatter and details
7. Extend `_get_all_step_ids()` in correct order.

### Architect guidance
- Preserve `gate_passed()` signature exactly per `NFR-009`.
- Enforce strict pass/fail semantics only for the three semantic checks.
- Keep structural audit warning-only during this phase.

### Milestone
- **M2**: Roadmap pipeline executes new anti-instinct step in correct position and writes a valid `anti-instinct-audit.md`.

### Timeline estimate
- **1.5-2 days**

---

## Phase 3 — Prompt hardening for upstream plan quality
**Goal**: reduce false negatives by improving roadmap generation before deterministic checks evaluate output.

### Requirements addressed
- `FR-PROMPT.1`
- `FR-PROMPT.2`

### Work items
1. Add `INTEGRATION_ENUMERATION_BLOCK` before `_OUTPUT_FORMAT_BLOCK` in `build_generate_prompt()` per `FR-PROMPT.1`.
2. Add `INTEGRATION_WIRING_DIMENSION` as the 6th spec fidelity comparison dimension per `FR-PROMPT.2`.
3. Update prompt-related tests to ensure:
   - ordering is correct
   - wording explicitly requires named wiring tasks
   - integration enumeration is preserved in output contract
4. Validate whether prompt-required structure is actually enforced downstream; if not, document residual exposure from `OQ-010`.

### Architect guidance
- Treat prompt changes as probability reducers, not primary enforcement.
- Deterministic modules remain the source of truth.
- Keep prompt changes tightly scoped to explicit wiring enumeration.

### Milestone
- **M3**: Prompt outputs consistently instruct explicit integration wiring and fidelity comparison includes integration coverage.

### Timeline estimate
- **0.5-1 day**

---

## Phase 4 — Sprint executor and rollout-mode integration
**Goal**: integrate the new gate into sprint economics and trailing-gate accounting without changing default behavior.

### Requirements addressed
- `FR-SPRINT.1`
- `FR-SPRINT.2`
- `FR-SPRINT.3`
- `FR-SPRINT.4`
- `FR-SPRINT.5`

#### Non-functional constraints
- `NFR-006`
- `NFR-007`
- `NFR-008`
- `NFR-010`

### Work items
1. Add `gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "off"` to `SprintConfig` per `FR-SPRINT.1`.
2. Ensure sprint-side gate results are wrapped in `TrailingGateResult` and added to `_all_gate_results`.
3. Implement rollout behavior matrix:
   1. **off**
      - gate evaluated if required for metrics policy, but no behavior change
   2. **shadow**
      - `ShadowGateMetrics.record(passed, evaluation_ms)` always
      - no task failure
   3. **soft**
      - pass reimbursement credit if ledger exists
      - fail adds remediation and exits `BUDGET_EXHAUSTED`
   4. **full**
      - same as soft plus `TaskResult.status = FAIL`
4. Guard all ledger operations with `if ledger is not None` per `FR-SPRINT.5`.
5. Add sprint integration tests for all rollout modes and ledger-none paths.

### Architect guidance
- Default remains `"off"` until shadow evidence satisfies `NFR-006`.
- Do not introduce stateful cross-run registries.
- Keep anti-instinct and wiring-integrity evaluation independent.

### Milestone
- **M4**: Sprint path supports all rollout modes with no behavior change in default config and no regressions in standalone roadmap mode.

### Timeline estimate
- **1.5-2 days**

---

## Phase 5 — End-to-end validation, regression coverage, and calibration
**Goal**: prove the feature works on the motivating failure mode and is safe to promote.

### Requirements addressed
#### Success criteria validation
- `SC-001`
- `SC-002`
- `SC-003`
- `SC-004`
- `SC-005`
- `SC-006`
- `SC-007`
- `SC-008`
- `SC-009`

#### Non-functional calibration
- `NFR-011`

### Work items
1. Create end-to-end regression coverage against the cli-portify failure case:
   - `SC-001`
   - `SC-002`
   - `SC-003`
   - `SC-004`
2. Validate structural audit warning behavior and threshold logic for `SC-005`.
3. Run full existing test suite to prove `SC-007`.
4. Run performance sampling to confirm `SC-006`.
5. Execute at least 5 shadow-mode sprint runs and record:
   - pass rate
   - evaluation latency
   - false-positive review notes
6. Validate no merge conflict or coordination breakage with TurnLedger/WIRING_GATE integration for `SC-009`.
7. Review threshold performance:
   - fingerprint threshold `0.7`
   - structural threshold `0.5`

### Promotion gate
Advance from `off` to `shadow` only after:
1. All end-to-end regression tests pass.
2. No existing tests break.
3. Latency target is met.

Advance from `shadow` to `soft/full` only after:
1. `ShadowGateMetrics.pass_rate >= 0.90` over 5+ sprint runs per `NFR-006` / `SC-008`.
2. False-positive rate is operationally acceptable.
3. Open questions affecting enforcement semantics are resolved.

### Milestone
- **M5**: Evidence package supports rollout promotion decision.

### Timeline estimate
- **2-3 days plus shadow-run observation window**

---

## Phase 6 — Rollout and operational hardening
**Goal**: safely promote the feature from dormant to enforced behavior.

### Requirements addressed
- `NFR-006`
- `NFR-011`

### Work items
1. Enable `shadow` in controlled environments first.
2. Review pass-rate, false-positive incidents, and remediation cost.
3. If evidence supports, promote to `soft`.
4. Promote to `full` only after sprint stakeholders confirm economics and failure semantics are acceptable.
5. Capture unresolved Phase 2 follow-ups from open questions.

### Rollout recommendation
1. **off** → immediate ship default
2. **shadow** → first real adoption mode
3. **soft** → only after acceptable shadow metrics
4. **full** → only after stable shadow/soft evidence

### Milestone
- **M6**: Controlled production-grade enforcement with documented thresholds and rollback path.

### Timeline estimate
- **1-2 sprints of observation after implementation**

---

# 3. Risk assessment and mitigation strategies

## High-priority risks

### 1. A-002 — Unparseable natural-language roadmap text
**Impact**: false negatives in obligation and contract checks.  
**Affected requirements**: `FR-MOD1.2`, `FR-MOD1.3`, `FR-MOD2.3`, `FR-PROMPT.1`, `FR-PROMPT.2`

**Mitigation**
1. Strengthen output structure through `FR-PROMPT.1` and `FR-PROMPT.2`.
2. Keep phase parsing fallback from `FR-MOD1.2`.
3. Rely on fingerprint coverage (`FR-MOD3.3`) as an orthogonal signal.
4. Include end-to-end regression for cli-portify case (`SC-001` to `SC-004`).

**Architect recommendation**
- Make output structure more machine-readable before broadening regex complexity.

---

### 2. A-009 — Mention-equals-coverage false passes
**Impact**: gate passes without real wiring tasks.  
**Affected requirements**: `FR-MOD2.3`, `FR-MOD2.5`, `FR-PROMPT.1`, `SC-003`

**Mitigation**
1. Keep verb-anchored wiring-task patterns strict.
2. Prefer contract-specific matching if feasible after Phase 1 evidence.
3. Use named mechanism identifier checks from `FR-MOD2.4`.
4. Add adversarial tests where component implementation is mentioned but wiring is absent.

**Architect recommendation**
- Favor slightly higher false negatives in early rollout over permissive false positives.

---

### 3. A-008 — Uncalibrated thresholds
**Impact**: unstable enforcement and poor promotion decisions.  
**Affected requirements**: `FR-MOD3.4`, `FR-MOD4.2`, `FR-MOD4.3`, `NFR-011`, `SC-008`

**Mitigation**
1. Ship with sprint rollout default `"off"` per `FR-SPRINT.1` and `NFR-006`.
2. Keep structural audit warning-only in Phase 1.
3. Run shadow-mode calibration before any strict rollout promotion.
4. Preserve threshold values as configurable internals only if needed after evidence, not before.

**Architect recommendation**
- Treat thresholds as operational policy knobs backed by evidence, not theoretical constants.

---

## Medium-priority risks

### 4. A-004 — Missing scaffold vocabulary
**Mitigation**
- Expand vocabulary only after test evidence.
- Use component context extraction and exemption mechanism.
- Track misses from real shadow runs.

### 5. A-011 / A-014 — Sprint wiring incomplete
**Mitigation**
- Implement `FR-SPRINT.5` None-safe guards first.
- Add explicit mode-matrix tests.
- Verify `SprintGatePolicy` / executor integration during Phase 4.

### 6. D-03/D-04 overlap
**Mitigation**
- Resolve coexistence policy in Phase 0.
- Document whether anti-instinct is conditional or defense-in-depth.
- Prevent duplicate operator signals.

### 7. Merge conflict with `WIRING_GATE`
**Mitigation**
- Sequence edits in `roadmap/gates.py`.
- Keep changes additive and localized.
- Rebase/coordinate before merging shared-file work.

---

## Low-priority risks
- `A-001`, `A-007`, `A-010`, `A-012`, `A-013`, Phase 2 debt accumulation

**Mitigation posture**
1. Address through tests and documentation, not new architecture.
2. Avoid premature abstractions.
3. Track unresolved items for post-rollout review.

---

# 4. Resource requirements and dependencies

## Engineering resources

### Core implementation
1. **1 backend/pipeline engineer**
   - roadmap analyzers
   - gate wiring
   - sprint integration
2. **1 QA-focused engineer or shared test ownership**
   - unit tests
   - integration tests
   - regression harness
   - latency verification
3. **1 architecture reviewer**
   - shared-file coordination
   - rollout readiness
   - threshold promotion approval

## Required code dependencies
1. `src/superclaude/cli/roadmap/gates.py`
2. `src/superclaude/cli/roadmap/executor.py`
3. `src/superclaude/cli/roadmap/prompts.py`
4. `src/superclaude/cli/sprint/models.py`
5. `src/superclaude/cli/sprint/executor.py`
6. `src/superclaude/cli/sprint/kpi.py`
7. Python `re`
8. Python `dataclasses`
9. Python `yaml`
10. `MERGE_GATE`
11. `SPEC_FIDELITY_GATE`
12. `WIRING_GATE`

## Tooling and validation dependencies
1. UV-based test execution
2. Existing roadmap pipeline test harness
3. Existing sprint executor tests
4. Regression fixture for cli-portify failure case
5. Shadow-run environment for sprint metrics collection

## Artifact expectations
1. **New source files**: approximately 10
2. **Modified source files**: approximately 5
3. **New tests**: approximately 6 files
4. **Audit artifact**: `anti-instinct-audit.md`

## Critical architectural constraints to enforce during implementation
1. `NFR-001`: no LLM calls added
2. `NFR-004`: pure functions except executor I/O
3. `NFR-008`: maintain stateless pipeline
4. `NFR-009`: preserve `gate_passed()` signature
5. `NFR-010`: independent evaluation with wiring gate

---

# 5. Success criteria and validation approach

## Success criteria mapping

### Functional correctness
1. `SC-001` — all three semantic checks pass on the motivating regression case
2. `SC-002` — obligation scanner catches undischarged mocked steps
3. `SC-003` — integration contract extractor catches `PROGRAMMATIC_RUNNERS` without wiring task
4. `SC-004` — fingerprint coverage detects missing `_run_programmatic_step`, `PROGRAMMATIC_RUNNERS`, `test_programmatic_step_routing`
5. `SC-005` — structural audit flags inadequate extraction ratio

### Operational safety
6. `SC-006` — total latency under 1 second
7. `SC-007` — no existing tests break
8. `SC-008` — shadow pass rate at or above 0.90 over 5+ runs
9. `SC-009` — zero merge conflicts with TurnLedger integration

## Validation strategy

### A. Unit validation
Validate each analyzer independently against focused fixtures:
1. scaffold term detection and discharge matching
2. phase parsing variants
3. contract extraction categories
4. fingerprint source extraction and exclusion rules
5. structural audit counting and threshold behavior

### B. Integration validation
Validate roadmap pipeline behavior:
1. anti-instinct step position
2. frontmatter parsing for semantic checks
3. audit artifact generation
4. step IDs and gate registration order

### C. Sprint-mode validation
Validate mode-specific behavior:
1. `off`
2. `shadow`
3. `soft`
4. `full`
5. ledger present/absent
6. reimbursement and remediation semantics

### D. Regression validation
Run real regression fixtures for the original cli-portify failure mode.

### E. Non-functional validation
1. latency benchmarks for analyzers
2. full test suite pass for backward compatibility
3. proof of no new stateful coupling

## Validation checkpoints

### Checkpoint A — implementation readiness
Must pass before merging core feature work:
1. all new tests green
2. existing tests green
3. `SC-006` satisfied
4. no signature or statelessness violations

### Checkpoint B — rollout readiness
Must pass before promoting from `off`:
1. cli-portify regression proven
2. shadow metrics collection functioning
3. audit outputs explain failures clearly

### Checkpoint C — enforcement readiness
Must pass before promoting to `soft` or `full`:
1. `SC-008` satisfied
2. false positives reviewed
3. unresolved enforcement-related open questions closed

---

# 6. Timeline estimates per phase

## Summary timeline
1. **Phase 0 — Architecture lock and coordination**
   - **0.5-1 day**
2. **Phase 1 — Deterministic analyzer modules**
   - **2-3 days**
3. **Phase 2 — Roadmap gate and executor integration**
   - **1.5-2 days**
4. **Phase 3 — Prompt hardening**
   - **0.5-1 day**
5. **Phase 4 — Sprint integration and rollout modes**
   - **1.5-2 days**
6. **Phase 5 — Validation and calibration**
   - **2-3 days plus shadow-run observation**
7. **Phase 6 — Controlled rollout**
   - **1-2 sprints of observation**

## Total implementation estimate
- **Build-ready code and tests**: approximately **8-12 working days**
- **Operational rollout to enforcement confidence**: approximately **1-2 additional sprints**, depending on shadow-mode evidence

## Critical path
1. Phase 0 decisions
2. Phase 1 analyzers
3. Phase 2 gate/executor wiring
4. Phase 4 sprint rollout integration
5. Phase 5 shadow calibration evidence

## Parallelization opportunities
1. Phase 1 analyzer implementation and Phase 3 prompt changes can partially overlap.
2. Unit tests for analyzers can be developed in parallel with module coding.
3. Sprint-mode tests can begin once rollout API shape is frozen in Phase 4.

## Recommended milestone sequence
1. **M0** — architecture decisions locked
2. **M1** — analyzers complete and fast
3. **M2** — roadmap pipeline wired
4. **M3** — prompts hardened
5. **M4** — sprint integration complete
6. **M5** — validation evidence complete
7. **M6** — staged rollout approved

---

# Requirement coverage matrix

## Core modules
- `FR-MOD1.1` to `FR-MOD1.8` — Phase 1
- `FR-MOD2.1` to `FR-MOD2.6` — Phase 1
- `FR-MOD3.1` to `FR-MOD3.4` — Phase 1
- `FR-MOD4.1` to `FR-MOD4.3` — Phase 1, enforced operationally in Phase 5/6

## Gate and executor
- `FR-GATE.1` to `FR-GATE.3` — Phase 2
- `FR-EXEC.1` to `FR-EXEC.4` — Phase 2

## Prompt path
- `FR-PROMPT.1` to `FR-PROMPT.2` — Phase 3

## Sprint path
- `FR-SPRINT.1` to `FR-SPRINT.5` — Phase 4

## Key non-functional controls
- `NFR-001`, `NFR-004`, `NFR-008`, `NFR-009`, `NFR-010` — architectural invariants across all phases
- `NFR-002` — proven in Phase 1 and rechecked in Phase 5
- `NFR-005`, `NFR-006`, `NFR-007`, `NFR-011` — operationalized in Phases 2, 4, 5, and 6

---

# Architect recommendations

1. **Do not start with executor wiring.**  
   Build and prove the analyzers first; shared pipeline edits should come only after deterministic behavior is trusted.

2. **Resolve semantic ambiguity before strict enforcement.**  
   `OQ-003`, `OQ-004`, `OQ-005`, `OQ-009`, and `OQ-010` directly affect pass/fail correctness and should not remain implicit.

3. **Treat prompt changes as support, not enforcement.**  
   The anti-instinct feature succeeds only if deterministic checks remain authoritative.

4. **Protect shared-file stability.**  
   `gates.py`, `executor.py`, and sprint executor/model changes are the highest coordination-risk edits.

5. **Use shadow-mode evidence as the promotion gate.**  
   This is required by both the architecture and the economics of deterministic gate rollout.
