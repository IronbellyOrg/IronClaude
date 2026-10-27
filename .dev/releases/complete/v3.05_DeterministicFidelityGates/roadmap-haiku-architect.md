---
spec_source: "deterministic-fidelity-gate-requirements.md"
complexity_score: 0.88
primary_persona: architect
---

# 1. Executive summary

This roadmap delivers a deterministic fidelity-gating architecture that replaces monolithic comparison with a hybrid model:

1. **Deterministic structural validation first**
   - Implement FR-2, FR-5, FR-1, and FR-3 as the new system backbone.
   - Target ≥70% of findings through anchored structural rules per SC-4.

2. **Semantic judgment only where structurally necessary**
   - Constrain FR-4, FR-4.1, and FR-4.2 to residual checks only.
   - Gate semantic HIGH findings through deterministic adversarial validation.

3. **Persistent convergence across runs**
   - Extend FR-6, FR-7, FR-7.1, FR-8, and FR-10 to make the registry authoritative in convergence mode.
   - Enforce ≤3 runs per NFR-2 and SC-2.

4. **Safe remediation with bounded blast radius**
   - Implement FR-9 and FR-9.1 with patch-level diff guards and regeneration opt-in.
   - Preserve backward compatibility under NFR-7 and SC-5.

## Architectural priorities

1. **Critical path first**: FR-2 → FR-1 → FR-4 → FR-7.
2. **Strict mode isolation**:
   - Legacy mode remains byte-identical to baseline `f4d9035`.
   - Convergence mode is fully gated by `convergence_enabled: bool = False`.
3. **Determinism before intelligence**:
   - Structural findings must satisfy NFR-1 before semantic enhancements are trusted.
4. **State authority discipline**:
   - In convergence mode, `DeviationRegistry` is the sole pass/fail authority.
   - `SPEC_FIDELITY_GATE` must not be invoked in convergence mode.
5. **Operational safety**:
   - No file changes >30% without `--allow-regeneration`.
   - No git worktrees for FR-8 temp isolation.

---

# 2. Phased implementation plan with milestones

## Phase 0 — Baseline verification and architecture lock
**Objective:** Confirm existing surfaces, freeze interfaces, and remove ambiguity before implementation.

### Scope
1. Validate baseline against architectural constraints:
   - `f4d9035` legacy behavior reference
   - `convergence_enabled` default false
   - step 8-only scope for convergence logic
2. Confirm current code ownership and module disposition:
   - `spec_parser.py` create
   - `convergence.py`, `semantic_layer.py`, `remediate_executor.py`, CLI/config/model surfaces modify
   - `fidelity.py` delete per architectural constraint 12
3. Lock canonical APIs:
   - `SEVERITY_RULES` + `get_severity()`
   - stable finding ID tuple
   - `RunMetadata`
   - `RegressionResult`
   - `RemediationPatch`

### Milestones
- **M0.1**: Interface contract approved for FR-7/FR-8 integration.
- **M0.2**: Legacy/convergence dispatch strategy documented and verified.
- **M0.3**: Acceptance-test matrix mapped to SC-1 through SC-6.

### Requirements covered
- FR-7.1
- NFR-7
- Architectural Constraints 4, 5, 6, 7, 11, 12

### Timeline estimate
- **2-3 days**

---

## Phase 1 — Parsing and sectional document model
**Objective:** Build the deterministic document understanding layer that all downstream logic depends on.

### Scope
1. Implement **FR-2: Spec & Roadmap Parser**
   - YAML frontmatter extraction
   - section-keyed table extraction
   - fenced code block extraction with language capture
   - requirement ID family extraction:
     - `FR-\d+\.\d+`
     - `NFR-\d+\.\d+`
     - `SC-\d+`
     - `G-\d+`
     - `D\d+`
   - Python signature extraction
   - manifest file path extraction
   - `Literal[...]` enum extraction
   - numeric threshold extraction
   - `ParseWarning` accumulation and surfacing
2. Implement **FR-5: Sectional/Chunked Comparison**
   - `SpecSection` dataclass
   - `split_into_sections(content: str) -> list[SpecSection]`
   - frontmatter and preamble special sections
   - deterministic section mapping

### Architect emphasis
- Parser must degrade safely rather than fail hard.
- Section model must be stable enough to support deterministic quoting and location references used later in findings and registry IDs.

### Milestones
- **M1.1**: Real-spec parse succeeds on `deterministic-fidelity-gate-requirements.md`.
- **M1.2**: Section splitting produces deterministic heading paths and line ranges.
- **M1.3**: Parse warnings surfaced without blocking partial output.

### Requirements covered
- FR-2
- FR-5
- NFR-1
- NFR-6

### Timeline estimate
- **5-7 days**

---

## Phase 2 — Structural checker framework and anchored severity
**Objective:** Replace monolithic fidelity judgment with parallel deterministic structural analysis.

### Scope
1. Implement **FR-1: Decomposed Structural Checkers (5 Dimensions)**
   - Signatures
   - Data Models
   - Gates
   - CLI Options
   - NFRs
2. Implement **FR-3: Anchored Severity Rules**
   - canonical `SEVERITY_RULES: dict[tuple[str, str], str]`
   - `get_severity()`
   - unknown combinations raise `KeyError`
3. Add checker registry and parallel execution with no shared mutable state.
4. Standardize finding schema:
   - `dimension`
   - `rule_id`
   - `severity`
   - `spec_quote`
   - `roadmap_quote_or_MISSING`
   - `location`
   - `mismatch_type`

### Architect emphasis
- This phase is the foundation for SC-1 and SC-4.
- Deterministic findings must be byte-stable across repeated runs before semantic work proceeds.
- Quote extraction and location fidelity must be precise because they later anchor registry identity and remediation.

### Milestones
- **M2.1**: All five checkers callable independently as `(spec_path, roadmap_path) → List[Finding]`.
- **M2.2**: Parallel checker execution verified under NFR-4.
- **M2.3**: Repeated runs on same inputs produce identical structural findings per SC-1.

### Requirements covered
- FR-1
- FR-3
- NFR-1
- NFR-4
- SC-1
- SC-4

### Timeline estimate
- **6-8 days**

---

## Phase 3 — Deviation registry and run memory
**Objective:** Establish persistent state, cross-run identity, and authoritative convergence data.

### Scope
1. Extend **FR-6: Deviation Registry**
   - JSON registry in release output directory
   - stable finding IDs from `(dimension, rule_id, spec_location, mismatch_type)`
   - `source_layer`
   - run metadata
   - reset on `spec_hash` change
   - compatibility for pre-v3.05 registries
2. Implement **FR-10: Run-to-Run Memory**
   - `first_seen_run`
   - `last_seen_run`
   - prior findings summary for semantic prompts
   - ledger snapshot in run metadata for convergence mode

### Architect emphasis
- Registry schema is the core long-lived contract; it must be version-tolerant.
- Stable ID design should be validated against collision and over-specificity risk before convergence logic depends on it.

### Milestones
- **M3.1**: Registry persists and reloads findings with stable identities.
- **M3.2**: FIXED findings transition correctly across runs.
- **M3.3**: Pre-v3.05 registries load with backward-compatible defaults.

### Requirements covered
- FR-6
- FR-10
- NFR-6
- SC-3

### Timeline estimate
- **4-5 days**

---

## Phase 4 — Residual semantic layer and adversarial validation
**Objective:** Reintroduce LLM judgment only for residual semantic gaps, under strict budget and validation control.

### Scope
1. Implement **FR-4: Residual Semantic Layer with Adversarial Validation**
   - semantic checks receive only uncovered dimensions/aspects
   - chunked inputs only
   - structural findings passed as context
   - `source_layer="semantic"`
2. Implement **FR-4.1: Lightweight Debate Protocol**
   - `validate_semantic_high()`
   - prosecutor/defender parallelism
   - deterministic Python judge
   - YAML debate output
   - registry updates with verdict and transcript
3. Implement **FR-4.2: Prompt Budget Enforcement**
   - 30,720-byte total budget
   - proportional allocation
   - deterministic truncation order and markers

### Architect emphasis
- Semantic layer must be explicitly subordinate to the structural layer.
- Budget enforcement is not merely performance optimization; it is a correctness and operational predictability requirement under NFR-3.
- Debate must validate severity, not re-open broad interpretation.

### Milestones
- **M4.1**: Semantic prompt builder respects 30KB budget with deterministic truncation.
- **M4.2**: HIGH semantic findings trigger debate and verdict persistence.
- **M4.3**: MEDIUM/LOW semantic findings bypass debate cleanly.

### Requirements covered
- FR-4
- FR-4.1
- FR-4.2
- NFR-3
- SC-4
- SC-6

### Timeline estimate
- **5-7 days**

---

## Phase 5 — Convergence engine and regression validation
**Objective:** Operationalize convergence as a bounded, budgeted, stateful control loop.

### Scope
1. Implement **FR-7: Convergence Gate**
   - `execute_fidelity_with_convergence()`
   - `handle_regression()`
   - registry-based pass/fail
   - TurnLedger integration
   - step 8-only execution
   - strict mutual exclusion from legacy path
2. Implement **FR-7.1: FR-7/FR-8 Interface Contract**
   - `RegressionResult`
   - debit behavior and separation of responsibilities
3. Implement **FR-8: Regression Detection & Parallel Validation**
   - trigger only on structural HIGH increase
   - 3 parallel isolated temp-directory agents
   - consolidation, deduplication, severity ordering
   - adversarial debate for HIGH severity after consolidation
   - guaranteed cleanup

### Architect emphasis
- This phase carries the highest operational coupling risk.
- The dispatch boundary between legacy and convergence mode must be exhaustively tested.
- Budget accounting must remain externally observable and internally non-overlapping.

### Milestones
- **M5.1**: Run 2 monotonic structural check enforced.
- **M5.2**: Regression detection launches 3-agent validation successfully.
- **M5.3**: Pipeline halts or passes within ≤3 runs per SC-2.
- **M5.4**: Legacy path remains byte-identical with `convergence_enabled=false`.

### Requirements covered
- FR-7
- FR-7.1
- FR-8
- NFR-2
- NFR-7
- SC-2
- SC-5

### Timeline estimate
- **6-8 days**

---

## Phase 6 — Edit-only remediation and safety controls
**Objective:** Make remediation precise, bounded, and safe under per-patch governance.

### Scope
1. Implement **FR-9: Edit-Only Remediation with Diff-Size Guard**
   - `RemediationPatch` dataclass
   - structured patch output
   - primary ClaudeProcess applicator
   - deterministic fallback applicator
   - per-patch diff-size guard
   - partial rejection support
   - sequential same-file patch application
   - per-file rollback
   - post-execution coherence check
2. Implement **FR-9.1: `--allow-regeneration` Flag**
   - Click `is_flag=True`
   - `RoadmapConfig.allow_regeneration: bool = False`
   - warning path for oversized patches when enabled

### Architect emphasis
- Blast-radius containment is the central design concern here.
- Patch-level evaluation is superior to file-level evaluation because it preserves local valid remediation while rejecting high-risk edits.
- Cross-file coherence must be verified after partial acceptance to avoid silent inconsistency.

### Milestones
- **M6.1**: Oversized patches rejected by default at 30%.
- **M6.2**: `--allow-regeneration` changes behavior only for oversized patches and emits warnings.
- **M6.3**: Valid patches continue applying even when sibling patches are rejected.

### Requirements covered
- FR-9
- FR-9.1
- NFR-5
- SC-3

### Timeline estimate
- **4-6 days**

---

## Phase 7 — Integration hardening, backward-compatibility certification, and release readiness
**Objective:** Validate the full architecture against real artifacts and certify release readiness.

### Scope
1. Integration validation across backend, cli, testing, pipeline-orchestration, and nlp-integration domains.
2. Real-artifact testing with actual CLI pipeline flows.
3. Backward-compatibility certification against `f4d9035`.
4. Operational cleanup:
   - delete dead `fidelity.py`
   - sync distributable/dev copies if relevant
   - final release diagnostics and handoff notes

### Validation focus
1. Determinism runs for SC-1.
2. Budget and halt behavior for SC-2.
3. Registry persistence behavior for SC-3.
4. Severity source distribution for SC-4.
5. Legacy byte-identity for SC-5.
6. Prompt-size assertions for SC-6.

### Milestones
- **M7.1**: All success criteria pass against real release artifacts.
- **M7.2**: No regression in steps 1-7 or step 9.
- **M7.3**: Release package ready for branch-based integration.

### Requirements covered
- SC-1
- SC-2
- SC-3
- SC-4
- SC-5
- SC-6
- NFR-1 through NFR-7

### Timeline estimate
- **4-5 days**

---

# 3. Risk assessment and mitigation strategies

## High-priority risks

### 1. Spec parser robustness
- **Mapped risk:** Risk 1
- **Affected requirements:** FR-2, FR-5, FR-1, FR-4, FR-7
- **Impact:** Critical-path failure cascades through the entire architecture.
- **Mitigation:**
  1. Validate parser on the real `deterministic-fidelity-gate-requirements.md` before downstream implementation sign-off.
  2. Treat `ParseWarning` as first-class surfaced output.
  3. Build deterministic fallback behavior for malformed YAML, irregular tables, and missing language tags.
- **Architect recommendation:** Make parser certification the exit criterion for Phase 1.

### 2. Dual budget system overlap
- **Mapped risk:** Risk 5
- **Affected requirements:** FR-7, FR-7.1, NFR-7, SC-5
- **Impact:** Double charging, invalid halts, and broken legacy compatibility.
- **Mitigation:**
  1. Single dispatch gate on `convergence_enabled`.
  2. Prohibit TurnLedger construction outside convergence path.
  3. Add integration tests proving legacy branch does not import/reference TurnLedger.
- **Architect recommendation:** Treat mutual exclusion as a release blocker.

## Medium-priority risks

### 3. Stable finding ID collisions
- **Mapped risk:** Risk 2
- **Affected requirements:** FR-6, FR-10, SC-3
- **Impact:** False new/fixed findings undermine convergence memory.
- **Mitigation:**
  1. Test ID stability on real deviation sets.
  2. Verify collision resistance and sensitivity tradeoff.
  3. Keep tuple inputs human-auditable for debugging.
- **Architect recommendation:** Add a registry schema review checkpoint at M3.1.

### 4. Debate rubric calibration
- **Mapped risk:** Risk 4
- **Affected requirements:** FR-4.1, SC-4
- **Impact:** Over- or under-confirmation of semantic HIGH severity.
- **Mitigation:**
  1. Keep deterministic judge and conservative tiebreak.
  2. Log rubric scores and verdict margins for auditability.
  3. Make threshold constants explicitly tunable without protocol rewrite.
- **Architect recommendation:** Ship with conservative defaults; tune only after real corpus evidence.

### 5. Temp directory cleanup leaks
- **Mapped risk:** Risk 3
- **Affected requirements:** FR-8
- **Impact:** Disk leakage and operational instability across repeated runs.
- **Mitigation:**
  1. `try/finally` cleanup.
  2. `atexit` fallback.
  3. Prefix-identifiable temp directories and failure logging.
- **Architect recommendation:** Include failure-injection tests for cleanup paths.

## Low-priority risks

### 6. Cross-module import fragility
- **Mapped risk:** Risk 6
- **Affected requirements:** FR-7
- **Impact:** Limited future migration cost.
- **Mitigation:**
  1. Conditional import in convergence mode only.
  2. Keep import boundary isolated in one dispatch surface.
- **Architect recommendation:** Document as known migration debt, not current blocker.

## Open-question risks requiring explicit decision
1. **ParseWarning severity policy**
   - Needed to finalize FR-2 operational behavior.
2. **Agent failure definition in FR-8**
   - Needed to operationalize regression validation failure handling.
3. **Cross-file coherence check scope in FR-9**
   - Needed to size remediation verification.
4. **TurnLedger constant calibration**
   - Needed to reduce budget-tuning churn post-release.
5. **FR-4.1 threshold calibration**
   - Needed for confidence in semantic HIGH adjudication.

---

# 4. Resource requirements and dependencies

## Team / capability requirements

### Core engineering capabilities
1. **Backend/Pipeline engineer**
   - FR-2, FR-5, FR-6, FR-7, FR-7.1
2. **CLI / integration engineer**
   - FR-7, FR-9.1, config and command wiring
3. **LLM workflow engineer**
   - FR-4, FR-4.1, FR-4.2, FR-9
4. **QA / validation engineer**
   - SC-1 through SC-6 validation, backward-compatibility certification

## Dependency plan

### External/code dependencies identified
1. **TurnLedger** (`superclaude.cli.sprint.models`)
   - Required for FR-7, FR-7.1, FR-10
   - Constraint: consume as-is; do not modify
2. **DeviationRegistry** (`convergence.py:50-225`)
   - Extend rather than replace
3. **ClaudeProcess**
   - Required for FR-4.1, FR-8, FR-9
4. **RoadmapConfig**
   - Extend with/confirm `allow_regeneration` and `convergence_enabled`
5. **Finding dataclass**
   - Extend for rule/quote compatibility
6. **MorphLLM MCP**
   - Optional/future; probe only in v3.05
7. **Click CLI**
   - Required for FR-9.1 flag surface
8. **YAML parser**
   - Required for FR-2 and FR-4.1 debate serialization

## Environment and workflow constraints
1. **UV-only execution**
   - All implementation and validation via `uv run`
2. **Feature branch workflow**
   - Do not commit directly to `master`
3. **Source-of-truth discipline**
   - `src/superclaude/` canonical
4. **No git worktrees in FR-8**
   - temp directories only
5. **Real-artifact validation**
   - Aligns with project memory: use actual CLI pipeline outputs, not only unit-level gates

## Recommended staffing model
1. **Wave 1**
   - Parser/section model
   - structural checker framework
2. **Wave 2**
   - registry/memory
   - semantic/debate layer
3. **Wave 3**
   - convergence/regression
   - remediation/CLI
4. **Wave 4**
   - integration hardening and release certification

---

# 5. Success criteria and validation approach

## Success criteria traceability

### SC-1: Deterministic structural findings
- **Validation**
  1. Run the same spec+roadmap pair twice.
  2. Diff structural outputs byte-for-byte.
- **Primary requirement support**
  - FR-1
  - FR-2
  - FR-3
  - FR-5
  - NFR-1

### SC-2: Convergence within budget
- **Validation**
  1. Exercise convergence mode through up to 3 runs.
  2. Verify halt/pass behavior and non-negative budget handling.
- **Primary requirement support**
  - FR-6
  - FR-7
  - FR-7.1
  - FR-8
  - NFR-2

### SC-3: Edit preservation
- **Validation**
  1. Apply remediation.
  2. Re-run pipeline.
  3. Confirm previously fixed findings do not reappear as ACTIVE.
- **Primary requirement support**
  - FR-6
  - FR-9
  - FR-10

### SC-4: Severity anchoring
- **Validation**
  1. Measure percentage of findings whose severity comes from FR-3 machine-key rules.
  2. Verify all semantic HIGHs have debate verdicts.
- **Primary requirement support**
  - FR-3
  - FR-4
  - FR-4.1

### SC-5: Legacy backward compatibility
- **Validation**
  1. Run with `convergence_enabled=false`.
  2. Compare outputs to pre-v3.05 baseline behavior at `f4d9035`.
- **Primary requirement support**
  - FR-7
  - NFR-7

### SC-6: Prompt size compliance
- **Validation**
  1. Assert prompt byte size before LLM calls.
  2. Force truncation path and verify markers/ordering.
- **Primary requirement support**
  - FR-4.2
  - NFR-3

## Validation strategy by test layer

### 1. Unit validation
- Parser extraction functions
- section splitting
- severity mapping
- stable ID computation
- prompt budgeting
- diff-size guard

### 2. Integration validation
- checker suite parallelism
- registry persistence across runs
- convergence loop dispatch
- regression validation orchestration
- remediation pipeline application

### 3. End-to-end validation
- Actual CLI pipeline execution through step 8
- legacy and convergence mode comparison
- real artifact generation and verification

### 4. Non-functional validation
- determinism repeatability
- prompt byte bounds
- shared-state independence
- cleanup guarantees
- backward-compatibility diffing

## Requirement-ID preservation guidance
In all artifacts and reports:
1. Preserve exact IDs including:
   - FR-4.1
   - FR-4.2
   - FR-7.1
   - FR-9.1
   - NFR-1 through NFR-7
   - SC-1 through SC-6
2. Do not alias or renumber IDs in code comments, registry records, or reports.

---

# 6. Timeline estimates per phase

## Recommended schedule

1. **Phase 0 — Baseline verification and architecture lock**
   - **2-3 days**

2. **Phase 1 — Parsing and sectional document model**
   - **5-7 days**

3. **Phase 2 — Structural checker framework and anchored severity**
   - **6-8 days**

4. **Phase 3 — Deviation registry and run memory**
   - **4-5 days**

5. **Phase 4 — Residual semantic layer and adversarial validation**
   - **5-7 days**

6. **Phase 5 — Convergence engine and regression validation**
   - **6-8 days**

7. **Phase 6 — Edit-only remediation and safety controls**
   - **4-6 days**

8. **Phase 7 — Integration hardening and release readiness**
   - **4-5 days**

## Total estimate
- **Core delivery:** 36-49 working days

## Critical-path timeline
The architecturally constrained path remains:

1. **FR-2**
2. **FR-5**
3. **FR-1**
4. **FR-3**
5. **FR-6**
6. **FR-4**
7. **FR-4.1 / FR-4.2**
8. **FR-7 / FR-7.1**
9. **FR-8**
10. **FR-9 / FR-9.1**
11. **FR-10**
12. **SC-1 through SC-6 certification**

## Recommended milestone gates
1. **Gate A — Parser certified**
   - Exit when FR-2 + FR-5 pass real-spec validation.
2. **Gate B — Structural determinism certified**
   - Exit when SC-1 is proven.
3. **Gate C — Registry and semantic layer certified**
   - Exit when FR-6, FR-10, FR-4, FR-4.1, FR-4.2 are integrated.
4. **Gate D — Convergence certified**
   - Exit when SC-2 and SC-5 pass.
5. **Gate E — Remediation safety certified**
   - Exit when FR-9, FR-9.1, and SC-3 pass.
6. **Gate F — Release readiness**
   - Exit when all SC-1 through SC-6 pass on real artifacts.

# Final architect recommendation

Prioritize delivery in three architectural increments:

1. **Deterministic core**: FR-2, FR-5, FR-1, FR-3
2. **Stateful control loop**: FR-6, FR-10, FR-7, FR-7.1, FR-8
3. **Residual intelligence and safe repair**: FR-4, FR-4.1, FR-4.2, FR-9, FR-9.1

This sequence minimizes systemic risk, preserves backward compatibility, and creates measurable checkpoints against SC-1 through SC-6 before release.
