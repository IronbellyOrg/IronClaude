---
spec_source: merged-spec.md
complexity_score: 0.78
primary_persona: architect
---

## 1. Executive summary

This roadmap delivers a deterministic, AST-based wiring verification capability across the roadmap, sprint, and audit subsystems without violating existing pipeline contracts or dependency layering. The implementation must detect three failure classes—unwired optional callable injections, orphan provider modules, and broken dispatch registries—then emit a gate-valid report that supports phased rollout from shadow to soft and full enforcement.

From an architectural perspective, the primary challenge is not raw implementation size; it is controlled integration breadth under strict constraints. The roadmap therefore prioritizes:

1. **Stable analysis core first**
   - Build the wiring data model, AST analyzers, report emitter, and semantic checks before touching orchestration surfaces.

2. **Contract-safe integration second**
   - Add the roadmap step, sprint hook, and audit extensions only after the analysis/report artifacts prove compliant with existing gate infrastructure.

3. **Operational rollout third**
   - Use shadow-mode evidence to calibrate false-positive behavior before enabling any blocking semantics.

4. **Risk containment throughout**
   - Preserve zero pipeline substrate changes, additive-only agent extensions, and deterministic execution guarantees.

## 2. Phased implementation plan with milestones

### Phase 0 — Architecture alignment and decision closure

**Objective:** Eliminate ambiguity before code changes begin.

#### Key actions
1. Confirm unresolved specification decisions:
   - `audit_artifacts_used` discovery and counting rules
   - `files_skipped` semantics
   - whitelist strictness runtime boundary
   - whether `SprintConfig.source_dir` already exists
   - comparator/consolidator extension scope
   - rollout ownership for `grace_period`
   - merge sequencing for concurrent `roadmap/gates.py` work

2. Lock architectural rules into implementation checklist:
   - no changes to `pipeline/*`
   - no LLM or subprocess usage in wiring analysis
   - artifact-based enforcement only
   - duplicate `_FRONTMATTER_RE` privately in `audit/wiring_gate.py`

3. Define phase-exit acceptance criteria:
   - decisions recorded
   - impacted files identified
   - test strategy mapped to FR/NFR and success criteria

#### Deliverables
- Architecture decision log for open questions
- File-level implementation map
- Test matrix traceability draft

#### Milestone
- **M0: Spec ambiguities resolved and architecture frozen**

#### Timeline estimate
- **0.5-1 phase-day**

---

### Phase 1 — Core domain models and analysis engine

**Objective:** Build the deterministic wiring analysis substrate.

#### Key actions
1. Implement core dataclasses:
   - `WiringFinding`
   - `WiringReport`
   - `WiringConfig`

2. Implement AST analysis primitives:
   - unwired optional callable detection
   - orphan module detection
   - registry verification detection

3. Add config and suppression handling:
   - provider directory configuration
   - registry pattern configuration
   - exclusion rules
   - `wiring_whitelist.yaml` loading and validation behavior by rollout phase

4. Implement severity classification:
   - critical
   - major
   - info

5. Add graceful degradation behavior:
   - SyntaxError-safe file analysis
   - skip/continue on malformed source where required

#### Architectural notes
- Keep analysis logic isolated in `audit/*` or equivalent consumer-side layer.
- Do not couple AST logic to roadmap or sprint orchestration.
- Treat false-positive reduction as a first-class design concern, especially for alias/re-export patterns.

#### Deliverables
- Working analysis engine
- Config loading and whitelist handling
- Severity and blocking semantics support

#### Milestone
- **M1: Analysis engine detects all three finding classes from fixtures**

#### Timeline estimate
- **2-3 phase-days**

---

### Phase 2 — ToolOrchestrator AST plugin integration

**Objective:** Populate reusable file-level analysis data without breaking dependency boundaries.

#### Key actions
1. Implement `ast_analyze_file()` plugin for `ToolOrchestrator`.
2. Populate `FileAnalysis` fields:
   - `references`
   - `imports`
   - `exports`
   - metadata: `has_dispatch_registry`, `injectable_callables`
3. Handle parse failures deterministically by returning empty analysis objects.
4. Validate whether T06 cut criteria can be met before T08 begins.

#### Architectural notes
- This phase is a leverage point: it improves reuse across audit logic and reduces duplicated scanning paths.
- Because this item has explicit defer criteria, it should be isolated behind a clean boundary so v2.1 deferral does not destabilize the main rollout.

#### Deliverables
- AST plugin implementation
- Plugin-backed test fixtures
- Go/no-go recommendation against T06 cut criteria

#### Milestone
- **M2: FileAnalysis is populated correctly and remains contract-safe**

#### Timeline estimate
- **1-1.5 phase-days**

---

### Phase 3 — Report generation and gate contract compliance

**Objective:** Emit an artifact that can be validated by existing gate machinery with zero substrate changes.

#### Key actions
1. Implement report emitter with:
   - exact 17 required frontmatter fields
   - exact Markdown section order
   - YAML-safe serialization using `yaml.safe_dump()` for string values

2. Implement private helper:
   - `_extract_frontmatter_values()`

3. Define `WIRING_GATE`:
   - required fields
   - enforcement tier
   - semantic checks

4. Implement semantic checks:
   - `_analysis_complete_true`
   - `_recognized_rollout_mode`
   - `_finding_counts_consistent`
   - `_severity_summary_consistent`
   - `_zero_blocking_findings_for_mode`

5. Validate mode-aware blocking logic:
   - shadow = 0
   - soft = critical only
   - full = critical + major

#### Architectural notes
- This phase is the contract boundary between analysis and enforcement.
- The report must encode policy clearly enough that gate behavior is artifact-driven, not repo-state-driven.

#### Deliverables
- Gate-valid report emitter
- Gate definition and semantic checks
- Unit tests for frontmatter invariants and mode logic

#### Milestone
- **M3: `gate_passed()` validates a compliant wiring report without pipeline changes**

#### Timeline estimate
- **1.5-2 phase-days**

---

### Phase 4 — Roadmap pipeline integration

**Objective:** Add wiring verification as a deterministic post-merge roadmap step.

#### Key actions
1. Add `build_wiring_verification_prompt()` returning empty string.
2. Add `wiring-verification` step in `_build_steps()`:
   - after `spec-fidelity`
   - before `remediate`
   - `GateMode.TRAILING`
   - `retry_limit=0`
   - `timeout_seconds=60`

3. Update executor special-case path:
   - `step.id == "wiring-verification"` runs deterministic analysis + report emission

4. Update step ordering:
   - `_get_all_step_ids()`

5. Register gate:
   - add `WIRING_GATE` to `ALL_GATES`

#### Architectural notes
- This phase must preserve static gate wiring and avoid dynamic registry behavior.
- Special-casing the step is acceptable because the spec explicitly defines it as non-LLM.

#### Deliverables
- End-to-end roadmap pipeline wiring step
- Valid generated report artifact in roadmap runs

#### Milestone
- **M4: Roadmap pipeline executes wiring verification as a non-LLM trailing gate step**

#### Timeline estimate
- **1-1.5 phase-days**

---

### Phase 5 — Sprint integration and rollout controls

**Objective:** Apply the same analysis to sprint execution with mode-aware behavior.

#### Key actions
1. Add `wiring_gate_mode` to `SprintConfig`.
2. Implement sprint post-task hook behavior:
   - shadow: log only
   - soft: warn
   - full: affect `gate_passed()` and remediation path

3. Add pre-activation operator safeguards:
   - provider directory zero-match warning
   - whitelist validation escalation by mode
   - performance guardrails

4. Confirm `source_dir` contract and wire target directory correctly.

#### Architectural notes
- Sprint integration is operationally sensitive because it affects developer workflow directly.
- Keep enforcement behavior explicit and observable; avoid silent state changes.

#### Deliverables
- Sprint hook implementation
- Mode-aware operator messaging
- Integration tests for task status behavior

#### Milestone
- **M5: Sprint execution honors shadow/soft/full semantics without regressions**

#### Timeline estimate
- **1-1.5 phase-days**

---

### Phase 6 — Cleanup-audit agent extensions

**Objective:** Extend audit capabilities additively to incorporate wiring evidence.

#### Key actions
1. Extend `audit-scanner`:
   - emit `REVIEW:wiring` classification

2. Extend `audit-analyzer`:
   - add 9th mandatory field: Wiring path
   - support `UNWIRED_DECLARATION`
   - support `BROKEN_REGISTRATION`

3. Extend `audit-validator`:
   - add Wiring Claim Verification check
   - critical fail if DELETE is recommended for files with live wiring paths

4. Clarify and implement additive behavior for:
   - `audit-comparator`
   - `audit-consolidator`

#### Architectural notes
- Do not create new audit agent types.
- Extensions must be strictly additive and non-breaking.

#### Deliverables
- Updated agent specs
- Agent tests covering new wiring behavior
- Consolidated audit compatibility review

#### Milestone
- **M6: Cleanup-audit pipeline incorporates wiring-aware signals without altering existing audit behavior**

#### Timeline estimate
- **1-2 phase-days**

---

### Phase 7 — Validation, benchmarking, and rollout readiness

**Objective:** Prove correctness, performance, and calibration readiness.

#### Key actions
1. Build test suite:
   - minimum 20 unit tests
   - minimum 3 integration tests
   - benchmark coverage for <5s/50 files

2. Achieve coverage targets:
   - >=90% on `wiring_gate.py`
   - >=90% on `wiring_analyzer.py`

3. Run retrospective validation:
   - known cli-portify no-op bug fixture
   - alias/re-export noise characterization
   - provider-dir sanity checks

4. Collect shadow-mode quality metrics:
   - false positive rate
   - true positive rate
   - p95 runtime
   - whitelist churn stability across sprints

5. Prepare activation recommendation:
   - remain shadow, advance to soft, or defer

#### Deliverables
- Full test evidence bundle
- Benchmark results
- Shadow-mode readiness report

#### Milestone
- **M7: System is validated for shadow deployment and objectively assessed for soft-mode readiness**

#### Timeline estimate
- **2-3 phase-days plus shadow observation period**

---

### Phase 8 — Rollout progression and operational hardening

**Objective:** Move safely from shadow to soft and, later, full enforcement.

#### Key actions
1. Shadow mode rollout:
   - enable in roadmap pipeline
   - enable in sprint hook
   - observe for minimum 2 release cycles

2. Soft mode activation gate:
   - FPR < 15%
   - TPR > 50%
   - p95 < 5s
   - noise floor separation for unwired-callable detection

3. Full mode activation gate:
   - FPR < 5%
   - TPR > 80%
   - whitelist stable for 5+ sprints

4. Schedule v2.1 improvements if blocked by alias noise:
   - import alias pre-pass
   - re-export chain handling
   - additional dynamic-retention evidence heuristics

#### Deliverables
- Rollout scorecard
- Phase advancement decision record
- Deferred enhancement plan if needed

#### Milestone
- **M8: Enforcement level advanced only on measured operational evidence**

#### Timeline estimate
- **Shadow: 2 release cycles minimum**
- **Soft-to-full: dependent on observed quality metrics**

## 3. Risk assessment and mitigation strategies

### High-priority architectural risks

1. **R1 — False positives from intentional Optional[Callable] seams**
   - **Impact:** Undermines trust in gate output and blocks safe rollout.
   - **Mitigation:**
     - whitelist support from initial release
     - shadow-first rollout
     - explicit severity/info classification for intentional optional seams
     - collect alias/re-export false-positive patterns as structured evidence

2. **R5 — Misconfigured provider directories**
   - **Impact:** Orphan analysis becomes useless or misleading.
   - **Mitigation:**
     - first-run sanity warning if configured directories produce zero matches
     - pre-activation checklist
     - integration test for zero-match warning path
     - operator-visible configuration summary in report/log output

3. **R6 — Alias and re-export noise**
   - **Impact:** Inflates FPR enough to invalidate soft/full activation.
   - **Mitigation:**
     - explicitly treat as known limitation
     - calibrate against measured noise floor
     - block activation if unwired-callable FPR cannot be separated from noise
     - isolate v2.1 alias pre-pass as an enhancement seam

4. **R7 — Audit agent regression from extensions**
   - **Impact:** Existing cleanup-audit workflows degrade.
   - **Mitigation:**
     - additive-only changes
     - no removal of existing rules
     - regression tests for prior audit outputs
     - staged validation of scanner, analyzer, validator independently

### Medium-priority operational risks

5. **R3 — Insufficient shadow data for calibration**
   - **Mitigation:**
     - require minimum 2-release shadow period
     - track structured FPR/TPR evidence
     - do not compress observation period to meet schedule pressure

6. **R4 — Sprint performance regression**
   - **Mitigation:**
     - AST-only deterministic analysis
     - benchmark on 50-file fixture
     - instrument runtime by phase
     - short-circuit on excluded/skipped files

7. **R8 — Gate mode resolution conflicts with trailing shadow intent**
   - **Mitigation:**
     - set explicit step `gate_mode`
     - semantic check always passes shadow mode
     - integration tests for shadow/non-blocking behavior

### Low-priority but important correctness risks

8. **R2 — SyntaxError and complex AST patterns**
   - **Mitigation:**
     - parse-fail-safe behavior
     - skipped-file accounting
     - Evidence and Limitations section in report

## 4. Resource requirements and dependencies

### Engineering roles

1. **Architect/lead engineer**
   - Owns design decisions, layering enforcement, rollout criteria, and cross-subsystem sequencing.

2. **Backend/Python implementation engineer**
   - Implements AST analyzers, report emitter, and integrations.

3. **QA/test engineer**
   - Builds fixtures, coverage, benchmark tests, and rollout validation evidence.

4. **Audit workflow owner**
   - Reviews additive agent behavior changes and validates no regression in cleanup-audit flows.

### Technical dependencies

1. Existing pipeline contracts:
   - `pipeline/models.py`
   - `pipeline/gates.py`
   - `pipeline/trailing_gate.py`

2. Existing orchestration surfaces:
   - `roadmap/executor.py`
   - `roadmap/gates.py`
   - `roadmap/prompts.py`
   - `sprint/executor.py`
   - `sprint/models.py`
   - `audit/tool_orchestrator.py`

3. Standard library/runtime dependencies:
   - `ast`
   - `re`
   - `yaml.safe_dump()`

4. Optional operational artifact:
   - `wiring_whitelist.yaml`

5. Agent-spec dependencies:
   - scanner
   - analyzer
   - validator
   - comparator
   - consolidator

### Coordination dependencies

1. **Concurrent modification coordination**
   - `roadmap/gates.py` merge sequencing must be agreed early to avoid rebasing churn.

2. **Rollout ownership**
   - one owner must be accountable for shadow metrics and activation decisions.

3. **Spec clarification owners**
   - unresolved fields like `audit_artifacts_used` and comparator/consolidator behavior need explicit decisions before implementation finalization.

## 5. Success criteria and validation approach

### Functional validation

1. **Detection coverage**
   - Validate each core finding class with dedicated fixtures:
     - unwired optional callable
     - orphan provider module
     - broken registry entry

2. **Gate contract compliance**
   - Confirm well-formed report passes existing gate evaluation unchanged.

3. **Mode-aware behavior**
   - Prove:
     - shadow passes regardless of findings
     - soft blocks only critical findings
     - full blocks critical + major findings

4. **Whitelist behavior**
   - Confirm suppressions reduce active findings and increment `whitelist_entries_applied`.

### Non-functional validation

1. **Performance**
   - < 5 seconds for 50 files
   - capture p95 runtime during shadow rollout

2. **Determinism**
   - no subprocesses
   - no LLM path
   - repeatable outputs for same repository state

3. **Coverage**
   - >=90% for target modules
   - minimum test count thresholds met

4. **Layering compliance**
   - verify no forbidden imports introduced
   - review import graph for `pipeline/*` isolation

### Operational validation

1. **Retrospective known-bug detection**
   - detect cli-portify executor no-op issue

2. **Pre-activation safety checks**
   - warning on zero provider-dir matches
   - operator visibility for malformed whitelist behavior by mode

3. **Audit extension quality**
   - scanner emits `REVIEW:wiring`
   - analyzer emits 9-field profile with Wiring path
   - validator blocks unsafe DELETE recommendations

### Exit criteria by rollout stage

1. **Shadow ready**
   - all core functional tests green
   - gate-valid report emitted
   - benchmark target met
   - roadmap and sprint integration stable

2. **Soft ready**
   - FPR < 15%
   - TPR > 50%
   - p95 < 5s
   - shadow data sufficient
   - alias noise separable from signal

3. **Full ready**
   - FPR < 5%
   - TPR > 80%
   - whitelist stable for 5+ sprints
   - no material audit regressions

## 6. Timeline estimates per phase

| Phase | Name | Estimate | Exit milestone |
|---|---|---:|---|
| 0 | Architecture alignment and decision closure | 0.5-1 phase-day | M0 |
| 1 | Core domain models and analysis engine | 2-3 phase-days | M1 |
| 2 | ToolOrchestrator AST plugin integration | 1-1.5 phase-days | M2 |
| 3 | Report generation and gate compliance | 1.5-2 phase-days | M3 |
| 4 | Roadmap pipeline integration | 1-1.5 phase-days | M4 |
| 5 | Sprint integration and rollout controls | 1-1.5 phase-days | M5 |
| 6 | Cleanup-audit agent extensions | 1-2 phase-days | M6 |
| 7 | Validation, benchmarking, rollout readiness | 2-3 phase-days | M7 |
| 8 | Rollout progression and hardening | 2 release cycles minimum for shadow, then metrics-driven | M8 |

### Aggregate implementation estimate
1. **Build-to-shadow-ready engineering effort**
   - approximately **9.5-15.5 phase-days**

2. **Shadow observation window**
   - **minimum 2 release cycles**

3. **Soft/full activation**
   - **metrics-gated, not schedule-gated**

## Recommended architectural priorities

1. **Prioritize correctness over breadth**
   - Ship the core analyzer and gate-valid report before deeper ToolOrchestrator optimization if schedule pressure emerges.

2. **Protect the dependency boundaries aggressively**
   - The layering rule is a structural asset; violating it would create more long-term cost than deferring secondary enhancements.

3. **Treat rollout as part of the architecture, not postscript**
   - Shadow telemetry and false-positive calibration are essential system components, not operational extras.

4. **Design for auditability**
   - Every enforcement decision should be explainable from report frontmatter and evidence sections alone.

5. **Use explicit deferral if T06 slips**
   - The ToolOrchestrator AST plugin is valuable, but the roadmap should not jeopardize the primary gate rollout if the cut criterion triggers.

## Final milestone sequence

1. **M0** — Spec ambiguities resolved and architecture frozen  
2. **M1** — Analysis engine detects all required finding classes  
3. **M2** — FileAnalysis AST plugin integrated or explicitly deferred  
4. **M3** — Gate-valid report emitted and validated by existing gate machinery  
5. **M4** — Roadmap pipeline step operational  
6. **M5** — Sprint hook operational with shadow/soft/full behavior  
7. **M6** — Cleanup-audit extensions operational and additive  
8. **M7** — Tests, coverage, benchmarks, and retrospective validations complete  
9. **M8** — Shadow rollout complete; evidence-based decision on soft/full enforcement
