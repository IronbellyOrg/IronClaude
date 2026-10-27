---
spec_source: .dev/releases/current/v3.0_unified-audit-gating/adversarial/merged-spec.md
complexity_score: 0.82
primary_persona: architect
---

# 1. Executive summary

This roadmap delivers a deterministic Python-only wiring verification capability for the v3.0 unified audit gating pipeline. The initiative adds static analysis for three failure classes — unwired optional callable injections, orphan provider modules, and unregistered dispatch registry entries — then integrates those findings into roadmap and sprint execution without breaking existing gate substrate contracts.

From an architectural perspective, the primary challenge is not raw implementation size but integration discipline. The solution touches roadmap execution, sprint enforcement, gate evaluation, audit tooling, ToolOrchestrator analysis, and agent behavioral extensions while preserving strict layering and deterministic resume behavior. The roadmap therefore prioritizes:

1. **Stable architecture first**
   - Preserve substrate signatures and import boundaries.
   - Separate analysis, report emission, and enforcement into distinct layers.

2. **Deterministic deployability second**
   - Build the analyzer as pure Python with reproducible output.
   - Ensure artifact-based gate evaluation and retry-free execution.

3. **Calibration before enforcement third**
   - Start in shadow mode with trailing behavior.
   - Use measured false-positive/true-positive data before soft/full promotion.

4. **Testing and observability throughout**
   - Achieve ≥90% coverage on the new core modules.
   - Validate functional correctness, performance, and rollout safety before promotion.

## Target outcomes

- Deterministic `run_wiring_analysis()` public API implemented.
- Report generation compliant with `GateCriteria` and 15-field frontmatter.
- Wiring verification integrated into roadmap execution as a deterministic step.
- Sprint post-task wiring checks enabled with mode-aware behavior.
- Audit agents extended additively for wiring-aware detection and validation.
- Shadow rollout producing trustworthy calibration data for later enforcement.

---

# 2. Phased implementation plan with milestones

## Phase 0 — Architecture confirmation and activation readiness

### Objectives
Establish the implementation contract before code changes to avoid rework across multiple subsystems.

### Key work
1. Confirm architectural seams and unresolved assumptions:
   - Verify `ToolOrchestrator.__init__()` analyzer injection seam.
   - Confirm definitive `provider_dir_names` defaults or ownership.
   - Confirm current roadmap step ordering around `spec-fidelity` and `remediate`.
   - Confirm sprint enforcement control points and `SprintGatePolicy` interaction.
   - Confirm rollout ownership for whitelist governance and grace period.

2. Define canonical module boundaries:
   - `audit/` owns deterministic wiring analysis and gate artifact helpers.
   - `roadmap/` owns step integration and prompt placeholder.
   - `sprint/` owns post-task hook behavior only.
   - `pipeline/` remains substrate-only and must not gain reverse imports.

3. Lock acceptance contract:
   - Public APIs:
     - `run_wiring_analysis(target_dir, config?) -> WiringReport`
     - `emit_report(report, output_path, enforcement_mode)`
     - `ast_analyze_file(file_path, content) -> FileAnalysis`
   - Rollout default:
     - `wiring_gate_mode = "shadow"`
   - Initial execution mode:
     - roadmap step uses `GateMode.TRAILING`, `retry_limit=0`

### Milestones
- M0.1: Architecture decisions recorded.
- M0.2: Open questions assigned to owners.
- M0.3: Activation checklist criteria defined.

### Timeline estimate
- **0.5-1 phase-unit**

---

## Phase 1 — Core data model and deterministic analysis engine

### Objectives
Build the analysis foundation before any pipeline integration.

### Key work
1. Implement core models:
   - `WiringFinding`
   - `WiringReport`
   - `WiringConfig`
   - Derived `total_findings`
   - Mode-aware `blocking_for_mode()`

2. Implement AST-based analyzers:
   - Constructor scan for `Optional[Callable]` / `Callable | None` defaulted to `None`
   - Cross-file call-site detection for explicit keyword injection
   - Provider directory discovery by configured names and heuristic fallback
   - Orphan module analysis with exclusions
   - Registry dictionary detection using configured/default patterns
   - Severity classification for:
     - unresolved registry entry
     - registry unused
     - explicit `None` mapping

3. Build graceful degradation behavior:
   - Parse errors logged and counted, not fatal
   - Deterministic ordering of files/findings
   - Explicit exclusion of unsupported dynamic patterns (`**kwargs`, `getattr`, `importlib`)

4. Implement whitelist handling:
   - YAML load and validation
   - Phase-aware malformed-entry behavior:
     - warning in Phase 1
     - `WiringConfigError` in Phase 2+

### Architectural recommendations
- Keep cross-file resolution conservative and explicit; do not attempt speculative alias inference in v3.0.
- Sort all file traversal and emitted findings to guarantee reproducibility.
- Keep analysis pure and side-effect-light so benchmark and resume semantics stay stable.

### Milestones
- M1.1: Data classes and config complete.
- M1.2: Optional callable analysis complete.
- M1.3: Orphan analysis complete with dual-evidence rule hooks.
- M1.4: Registry analysis complete.
- M1.5: Public API returns stable `WiringReport`.

### Timeline estimate
- **2-3 phase-units**

---

## Phase 2 — Report emission and gate validation layer

### Objectives
Convert analysis results into a strict artifact that existing gate infrastructure can evaluate unchanged.

### Key work
1. Implement report emission:
   - YAML frontmatter with all 15 required fields
   - Safe serialization for all string-valued frontmatter via `yaml.safe_dump()`
   - Required body sections in exact order:
     1. Summary
     2. Unwired Optional Callable Injections
     3. Orphan Modules/Symbols
     4. Unregistered Dispatch Entries
     5. Suppressions and Dynamic Retention
     6. Recommended Remediation
     7. Evidence and Limitations

2. Implement gate definition:
   - `WIRING_GATE` as `GateCriteria`
   - Required semantic checks:
     - analysis complete true
     - recognized rollout mode
     - finding counts consistent
     - severity summary consistent
     - zero blocking findings for mode

3. Implement private frontmatter extraction helper in `audit/wiring_gate.py`
   - Duplicate `_FRONTMATTER_RE`
   - Do not import it from `pipeline/gates.py`

4. Ensure blocking count behavior:
   - shadow = 0
   - soft = critical
   - full = critical + major

### Architectural recommendations
- Treat the report artifact as the enforcement boundary.
- Avoid any gate logic that re-reads repository state during validation.
- Keep semantic checks pure to preserve portability and testability.

### Milestones
- M2.1: Valid report artifact generation complete.
- M2.2: `WIRING_GATE` accepted by existing `gate_passed()` with no substrate modification.
- M2.3: Shadow/full behavior validated by tests.

### Timeline estimate
- **1-1.5 phase-units**

---

## Phase 3 — Roadmap pipeline integration

### Objectives
Integrate wiring verification into roadmap execution as a deterministic, resume-safe step.

### Key work
1. Update roadmap sequencing:
   - Add `wiring-verification` after `spec-fidelity`
   - Before `remediate`
   - Update `_get_all_step_ids()`

2. Update step construction:
   - Insert step in `_build_steps()`
   - `retry_limit=0`
   - `gate_mode=GateMode.TRAILING`

3. Update executor behavior:
   - Special-case `step.id == "wiring-verification"` in `roadmap_run_step()`
   - Run deterministic analysis rather than LLM generation

4. Update prompt layer:
   - Add `build_wiring_verification_prompt()` returning empty string

5. Register gate:
   - Include `WIRING_GATE` in `ALL_GATES`

### Architectural recommendations
- Keep wiring verification as a first-class deterministic step, not a disguised prompt step.
- Preserve resume semantics by deriving outputs entirely from source inputs and config.
- Avoid hidden coupling between step execution and gate evaluation.

### Milestones
- M3.1: Step ordering updated.
- M3.2: Deterministic execution path implemented.
- M3.3: Trailing shadow behavior verified in roadmap flow.

### Timeline estimate
- **1-1.5 phase-units**

---

## Phase 4 — Sprint integration and post-task enforcement

### Objectives
Extend wiring verification into sprint workflows with low-latency AST-only analysis.

### Key work
1. Extend `SprintConfig`:
   - add `wiring_gate_mode: Literal["off", "shadow", "soft", "full"]`
   - default `"shadow"`

2. Implement post-task hook:
   - Run after task classification
   - Emit per-task report
   - Mode behavior:
     - shadow: log only
     - soft: warn
     - full: gate

3. Enforce performance target:
   - AST-only
   - no subprocess
   - target <2s

4. Confirm governance compatibility:
   - no local override mechanism
   - lifecycle governance remains authoritative

### Architectural recommendations
- Share core analysis logic between roadmap and sprint; only orchestration should differ.
- Keep sprint integration thin to minimize latency and rollout risk.
- Emit per-task artifacts for traceability and later calibration.

### Milestones
- M4.1: Sprint config updated.
- M4.2: Post-task hook implemented.
- M4.3: Shadow/soft/full sprint behaviors validated.

### Timeline estimate
- **1-1.5 phase-units**

---

## Phase 5 — ToolOrchestrator and agent extensions

### Objectives
Propagate wiring intelligence into the audit ecosystem without destabilizing existing agents.

### Key work
1. ToolOrchestrator extension:
   - Implement `ast_analyze_file()`
   - Populate:
     - `FileAnalysis.references`
     - `has_dispatch_registry`
     - `injectable_callables`

2. Agent extensions:
   - audit-scanner: add `REVIEW:wiring`
   - audit-analyzer: add 9th mandatory field `Wiring path`
   - audit-validator: add Check 5 for Wiring Claim Verification

3. Preserve additive-only change discipline:
   - no existing tools removed
   - no behavior regressions in prior analysis modes

### Architectural recommendations
- Treat ToolOrchestrator integration as a secondary dependency; defer if it threatens core rollout.
- Use the spec’s cut criterion: if this work lags, push it to v3.1 rather than blocking core gate delivery.
- Keep agent changes schema-compatible where possible.

### Milestones
- M5.1: `ast_analyze_file()` implemented.
- M5.2: scanner/analyzer/validator extensions complete.
- M5.3: additive-only regression tests pass.

### Timeline estimate
- **1-2 phase-units**
- Can partially overlap with Phase 4 if seams are stable.

---

## Phase 6 — Test hardening, performance qualification, and rollout calibration

### Objectives
Validate correctness, safety, and promotion readiness before enforcement escalation.

### Key work
1. Unit tests
   - Minimum 20 unit tests
   - Coverage ≥90% on `wiring_gate.py` and `wiring_analyzer.py`
   - Fixtures 50-80 LOC

2. Integration tests
   - Minimum 3 integration tests
   - Validate:
     - roadmap shadow step behavior
     - sprint shadow behavior
     - gate processing via existing `gate_passed()`

3. Performance and determinism validation
   - <5s for 50 files
   - <2s sprint post-task
   - same inputs => same outputs

4. Retrospective validation
   - Ensure analyzer catches known cli-portify no-op class of defect

5. Rollout calibration
   - Run shadow for minimum two release cycles
   - Measure:
     - FPR
     - TPR
     - p95 runtime
     - whitelist churn
   - Promote only when thresholds are met

### Milestones
- M6.1: Coverage and test count targets met.
- M6.2: Benchmark thresholds met.
- M6.3: Shadow calibration report produced.
- M6.4: Promotion recommendation issued.

### Timeline estimate
- **2 phase-units** for initial qualification
- **2 release cycles** for shadow calibration before soft promotion

---

# 3. Risk assessment and mitigation strategies

## Highest-priority risks

### 1. Provider directory misconfiguration
- **Risk**: High likelihood, high impact.
- **Why it matters**: Incorrect provider scope invalidates orphan detection and reduces trust in the system.
- **Mitigation**:
  - Mandatory pre-activation checklist.
  - Require confirmation of configured directories against real repository structure.
  - First-run sanity rule: if analysis covers >50 files and returns zero findings, emit warning and halt promotion.
- **Architect recommendation**:
  - Treat this as a release gate for enabling anything beyond shadow mode.

### 2. False positives from aliasing and re-exports
- **Risk**: High likelihood, medium impact.
- **Why it matters**: Excessive noise can erode confidence and stall rollout.
- **Mitigation**:
  - Keep v3.0 conservative and deterministic.
  - Document limitations in every report.
  - Use shadow calibration to quantify baseline noise.
  - Plan alias pre-pass improvement for v3.1 if FPR threatens promotion criteria.
- **Architect recommendation**:
  - Do not expand scope into complex alias resolution unless shadow data proves it necessary.

### 3. Integration regression across roadmap/sprint/gates
- **Risk**: Medium likelihood, high impact.
- **Why it matters**: This work crosses several execution paths and could destabilize release workflows.
- **Mitigation**:
  - Preserve existing public signatures.
  - Keep step integration special-cased and deterministic.
  - Ensure all new enforcement flows are artifact-based.
- **Architect recommendation**:
  - Add integration tests before enabling soft mode, not after.

### 4. Performance regression in sprint workflow
- **Risk**: Medium likelihood, low-medium impact.
- **Why it matters**: Sprint hook latency directly affects developer experience.
- **Mitigation**:
  - Reuse AST parse outputs where possible.
  - No subprocess execution.
  - Benchmark on representative repositories early.
- **Architect recommendation**:
  - Make sprint latency a non-negotiable acceptance criterion.

### 5. Rollout ambiguity and governance gaps
- **Risk**: Medium likelihood, medium impact.
- **Why it matters**: Whitelist ownership, grace period, and promotion criteria affect operational trust.
- **Mitigation**:
  - Assign owners for whitelist approval and calibration review.
  - Publish explicit promotion checklist.
  - Define shadow window and review cadence before promotion.
- **Architect recommendation**:
  - Governance decisions must be made in Phase 0, not deferred to rollout time.

## Secondary risks

- AST parse failures on complex files
- Merge conflicts with adjacent v3.x release streams
- Agent extension regressions
- Severity misclassification edge cases

## Risk handling model

1. **Prevent**
   - strict layering
   - deterministic analysis
   - bounded scope

2. **Detect**
   - integration tests
   - benchmark suite
   - first-run sanity warning

3. **Contain**
   - shadow rollout
   - trailing mode
   - additive agent changes

4. **Recover**
   - rollback to shadow/off
   - defer ToolOrchestrator work to v3.1 if needed
   - preserve existing gate substrate untouched

---

# 4. Resource requirements and dependencies

## Engineering resources

### Core implementation
1. **Backend/static analysis engineer**
   - AST traversal
   - cross-file resolution
   - report emission
   - config/whitelist handling

2. **Pipeline/architecture engineer**
   - roadmap executor integration
   - sprint executor integration
   - gate wiring and layering enforcement

3. **QA/quality engineer**
   - fixture design
   - unit/integration/performance test coverage
   - determinism validation

4. **Agent/tooling engineer**
   - ToolOrchestrator extension
   - audit agent behavior additions

## Dependency plan

### Critical internal dependencies
1. `pipeline/models.py`
   - `SemanticCheck`
   - `GateCriteria`
   - `Step`
   - `GateMode`

2. `pipeline/gates.py`
   - `gate_passed()`
   - semantic validation contract

3. `pipeline/trailing_gate.py`
   - `TrailingGateRunner`
   - `DeferredRemediationLog`
   - `resolve_gate_mode()`

4. `roadmap/executor.py`
   - `_build_steps()`
   - deterministic step execution path

5. `sprint/executor.py`
   - `SprintGatePolicy`
   - post-task hook integration point

6. `audit/tool_orchestrator.py`
   - `ToolOrchestrator`
   - `FileAnalysis`

### External/runtime dependencies
- Python standard library:
  - `ast`
  - `re`
- YAML serialization library already used by project patterns

## Dependency sequencing

### Must complete before roadmap/sprint integration
- Core models
- Deterministic analysis engine
- Report emitter
- `WIRING_GATE`

### Can run in parallel after core analyzer stabilizes
- Roadmap step integration
- Sprint hook integration
- Test suite authoring

### Can be deferred if necessary
- ToolOrchestrator analyzer seam
- Agent extensions

## Operational dependencies

1. Confirmed `provider_dir_names`
2. Whitelist governance owner
3. Promotion review owner
4. Merge coordination plan for v3.x branches
5. Shadow telemetry collection process

---

# 5. Success criteria and validation approach

## Success criteria mapping

### Functional validation
1. Detect unwired optional callable injections on fixtures with **100% expected detection**
2. Detect orphan modules in provider directories with **100% expected detection**
3. Detect unresolved dispatch registry entries with **100% expected detection**
4. Produce valid report artifacts accepted by existing `gate_passed()` without modifying substrate
5. Apply whitelist suppressions correctly and always emit `whitelist_entries_applied`

### Integration validation
6. Roadmap shadow mode must not fail execution solely due to findings
7. Sprint shadow mode must not change task status
8. Full mode must block on configured blocking findings
9. Wiring verification step must be resume-safe and deterministic
10. Agent extensions must remain additive and non-breaking

### Quality and performance validation
11. `wiring_gate.py` and `wiring_analyzer.py` coverage ≥90%
12. Minimum 20 unit tests and 3 integration tests
13. p95 runtime <5s for 50 files
14. Sprint hook runtime <2s

## Validation approach

### Test pyramid

#### Unit tests
- Data class derivations
- Optional callable extraction
- Call-site resolution
- Provider directory heuristics
- Orphan classification dual-evidence behavior
- Registry detection/classification
- Frontmatter emission correctness
- Semantic check purity and correctness
- Mode-aware blocking calculation

#### Integration tests
- `WIRING_GATE` evaluated by existing gate engine
- Roadmap step inserted and executed deterministically
- Sprint hook honors off/shadow/soft/full semantics

#### Benchmark tests
- 50-file representative benchmark
- p95 runtime measurement
- repeated-run determinism checks

#### Retrospective/fixture tests
- Known cli-portify defect fixture must produce at least one finding

### Promotion gates

#### Promote to soft only if all are true
- FPR <15%
- TPR >50%
- p95 <5s
- shadow data collected for at least 2 release cycles
- provider directory config validated
- zero unresolved rollout-governance questions

#### Promote to full only if all are true
- FPR <5%
- TPR >80%
- whitelist stable for 5+ sprints
- sprint latency acceptable
- no unresolved substrate or layering regressions

---

# 6. Timeline estimates per phase

## Recommended timeline model

Because the dominant risk is coordination and calibration, the roadmap should be treated as **implementation phases plus rollout phases**, not only coding phases.

### Phase timeline summary

1. **Phase 0 — Architecture confirmation**
   - Estimate: **0.5-1 phase-unit**
   - Exit criteria:
     - unresolved seam owners assigned
     - provider directory approach confirmed
     - rollout governance clarified

2. **Phase 1 — Core deterministic analyzer**
   - Estimate: **2-3 phase-units**
   - Exit criteria:
     - public API implemented
     - core findings produced deterministically
     - whitelist and parse-failure handling complete

3. **Phase 2 — Report emission and gate validation**
   - Estimate: **1-1.5 phase-units**
   - Exit criteria:
     - valid artifact emission
     - `WIRING_GATE` operational through existing gate engine

4. **Phase 3 — Roadmap integration**
   - Estimate: **1-1.5 phase-units**
   - Exit criteria:
     - new step added
     - deterministic execution path working
     - trailing shadow mode verified

5. **Phase 4 — Sprint integration**
   - Estimate: **1-1.5 phase-units**
   - Exit criteria:
     - post-task analysis enabled
     - <2s target demonstrated

6. **Phase 5 — ToolOrchestrator and agent extensions**
   - Estimate: **1-2 phase-units**
   - Exit criteria:
     - analyzer metadata extension complete
     - agent changes additive and tested
   - Note:
     - may be deferred to v3.1 if it endangers core delivery

7. **Phase 6 — Test hardening and rollout calibration**
   - Initial qualification: **2 phase-units**
   - Shadow observation: **minimum 2 release cycles**
   - Exit criteria:
     - test and coverage thresholds met
     - performance thresholds met
     - promotion metrics achieved

## Overall schedule recommendation

### Delivery strategy
1. **Implementation tranche**
   - Complete Phases 0-4 first to establish core value.
2. **Optional extension tranche**
   - Complete Phase 5 only if seams are low-risk and schedule allows.
3. **Operational readiness tranche**
   - Complete Phase 6 before any soft/full enforcement decision.

### Critical path
- Phase 0 -> Phase 1 -> Phase 2 -> Phase 3 -> Phase 6
- Phase 4 can begin once Phase 1 is stable
- Phase 5 is off critical path by design

### Architect recommendation on scope control
- **v3.0 must prioritize deterministic analyzer + report + roadmap integration + shadow rollout**
- **v3.1 should absorb alias-resolution improvements or deferred ToolOrchestrator work if calibration shows need**

---

# Recommended implementation order

1. Finalize Phase 0 decisions and owners.
2. Implement core models and analyzer.
3. Implement report emitter and `WIRING_GATE`.
4. Add roadmap deterministic step and register gate.
5. Build tests and benchmarks immediately after core integration.
6. Add sprint hook once analyzer performance is validated.
7. Add ToolOrchestrator and agent extensions only if they do not jeopardize rollout quality.
8. Run shadow for two release cycles and decide on soft promotion using measured evidence.

# Final architect recommendation

This initiative should be managed as a **controlled architecture rollout**, not just a feature build. The right success condition for v3.0 is **trusted shadow visibility with stable integration**, not aggressive enforcement. If the team preserves strict layering, keeps analysis deterministic, and uses shadow telemetry to calibrate before promotion, the wiring gate can become a reliable quality control mechanism without destabilizing the broader audit and roadmap pipeline.
