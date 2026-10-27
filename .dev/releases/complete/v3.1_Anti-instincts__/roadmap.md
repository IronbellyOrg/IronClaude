---
spec_source: "anti-instincts-gate-unified.md"
complexity_score: 0.72
adversarial: true
---

# v3.1 Anti-Instinct Gate — Final Merged Roadmap

## Executive Summary

This release adds a deterministic, zero-LLM anti-instinct gating layer to the SuperClaude roadmap and sprint pipelines. Four pure-Python detection modules — obligation scanner, integration contract extractor, fingerprint coverage checker, and spec structural auditor — catch the class of "scaffold-without-discharge" bugs that LLM-on-LLM review structurally misses. The gate slots between `merge` and `test-strategy` in the existing pipeline, is additive-only to shared files, and ships with `gate_rollout_mode=off`, where the gate still evaluates but the result is ignored until shadow validation confirms accuracy.

**Scope**: 35 functional requirements (FR-MOD1–4, FR-GATE, FR-EXEC, FR-PROMPT, FR-SPRINT) and 10 non-functional requirements (NFR-001–011, excluding NFR-003) across 12 new files and 5 modified files (~1,200 LOC). HIGH complexity (0.72) driven by dual execution context (standalone roadmap vs sprint-invoked) and three independent regex engines.

**Key architectural decisions**:
- All detection is deterministic Python. No LLM calls. Non-negotiable per NFR-001.
- `off` means gate fires but result is not submitted to sprint infrastructure (backward-compatible). Shadow mode adds metrics recording.
- D-03/D-04 coexistence: defense-in-depth (both gates evaluate independently per NFR-010).
- Prompt changes are probability reducers, not enforcement. Deterministic checks are authoritative.

**Delivery structure**: 4 build phases with 3 explicit validation checkpoints (A: implementation readiness, B: rollout readiness, C: enforcement readiness). Day-based estimates for build phases; sprint-based for observation.

---

## Phase 1: Core Detection Modules & Architecture Decisions

**Goal**: Resolve blocking open questions on day 1, then implement all four detection modules as standalone pure-function libraries with comprehensive tests. No pipeline integration yet.

**Milestone M1**: All four modules pass unit tests against the cli-portify regression case. Combined latency < 1s.

### 1.0 Day-1 Architecture Decisions

Before writing module code, resolve and document the following:

| OQ | Decision | Recommended Resolution |
|----|----------|----------------------|
| OQ-003 | `# obligation-exempt` syntax | Per-line scope on the scaffold term's line |
| OQ-004 | MEDIUM severity vs STRICT gate | Separate `medium_severity_obligations` frontmatter field, excluded from gate blocking |
| OQ-005 | D-03/D-04 coexistence | Defense-in-depth: both gates evaluate independently. Document overlap in operator guide. |
| OQ-010 | `## Integration Wiring Tasks` validation | Add heading presence check to merge gate or as structural audit indicator |

Confirm merge coordination plan with any parallel work on `WIRING_GATE` in `gates.py`.

### 1.1 Obligation Scanner (`obligation_scanner.py`)

- Implement compiled regex vocabulary for 11 scaffold terms (FR-MOD1.1)
- Implement phase-section parser splitting on H2/H3 headings with fallback (FR-MOD1.2)
- Implement cross-phase discharge search with verb-anchored patterns (FR-MOD1.3)
- Implement 60-char component context extraction: backtick-priority, capitalized-fallback (FR-MOD1.4)
- Implement dual-condition discharge matching (term + component name) (FR-MOD1.5)
- Define `ObligationReport` and `Obligation` dataclasses (FR-MOD1.6)
- Implement `# obligation-exempt` comment parsing per OQ-003 resolution (FR-MOD1.7)
- Implement code-block severity demotion to MEDIUM per OQ-004 resolution (FR-MOD1.8)

### 1.2 Integration Contract Extractor (`integration_contracts.py`)

- Implement 7-category dispatch pattern scanner with compiled regexes (FR-MOD2.1)
- Implement context capture (3 lines), mechanism classification, sequential ID assignment, deduplication (FR-MOD2.2)
- Implement verb-anchored wiring task coverage check (FR-MOD2.3)
- Implement named mechanism identifier matching (UPPER_SNAKE_CASE, PascalCase) (FR-MOD2.4)
- Enforce wiring-task-specific coverage semantics (FR-MOD2.5)
- Define `IntegrationAuditResult` dataclass with `all_covered` property (FR-MOD2.6)
- Phase 1 ships with global pattern matching per spec; contract-specific matching deferred (OQ-009)

### 1.3 Fingerprint Extraction (`fingerprint.py`)

- Implement three-source extraction: backtick identifiers (≥4 chars), code-block `def`/`class`, ALL_CAPS constants (FR-MOD3.1)
- Implement `_EXCLUDED_CONSTANTS` frozenset filtering, aligned with 4-char regex minimum (FR-MOD3.1, OQ-011)
- Implement deduplication by text value (FR-MOD3.2)
- Implement case-insensitive roadmap coverage check returning 4-tuple (FR-MOD3.3)
- Implement threshold gate logic (default 0.7) with empty-fingerprint passthrough (FR-MOD3.4)
- Extensibility deferred to Phase 2 (OQ-001)

### 1.4 Spec Structural Audit (`spec_structural_audit.py`)

- Implement 7 structural indicator counters (FR-MOD4.1)
- Implement ratio comparison against `total_requirements` frontmatter (FR-MOD4.2)
- Warning-only enforcement, no pipeline blocking (FR-MOD4.3)
- Transition to STRICT is manual configuration after shadow-mode metrics confirm threshold adequacy (OQ-006, NFR-011)

### 1.5 Unit Tests for All Modules

- `test_obligation_scanner.py`: scaffold detection, discharge matching, exempt comments, code-block severity, cli-portify regression (SC-002)
- `test_integration_contracts.py`: 7-category detection, wiring coverage, deduplication, cli-portify regression (SC-003)
- `test_fingerprint.py`: three-source extraction, deduplication, coverage ratio, threshold boundary, cli-portify regression (SC-004)
- `test_spec_structural_audit.py`: all 7 indicators, ratio comparison, warning-only behavior (SC-005)
- All tests use real content fixtures, no mocks (per project eval philosophy)
- **Parallelization note**: unit tests can be developed alongside module coding — these are independent work streams

### 1.5.1 Validation Gate (Checkpoint A: Implementation Readiness)

- SC-001 through SC-005 pass
- SC-006 (latency <1s) verified via timing assertions
- SC-007 (backward compat) verified by running full existing test suite
- No signature or statelessness violations

**Timeline estimate**: 2–3 days

---

## Phase 2: Gate Definition, Executor Wiring & Prompt Hardening

**Goal**: Wire the four modules into the roadmap pipeline as the `anti-instinct` gate step, including prompt modifications to improve upstream plan quality. No sprint integration yet.

**Milestone M2**: `anti-instinct` step executes between `merge` and `test-strategy` in standalone roadmap mode. Prompts instruct explicit integration wiring.

### 2.1 Gate Definition in `roadmap/gates.py`

- Define `ANTI_INSTINCT_GATE` as `GateCriteria` with required frontmatter: `undischarged_obligations` (int), `uncovered_contracts` (int), `fingerprint_coverage` (float), `min_lines=10`, and `gate_scope=GateScope.TASK` (FR-GATE.1)
- Implement three semantic checks (FR-GATE.2):
  - `_no_undischarged_obligations`: parse from frontmatter, assert == 0
  - `_integration_contracts_covered`: parse from frontmatter, assert == 0
  - `_fingerprint_coverage_check`: parse from frontmatter, assert >= 0.7
- Set `enforcement_tier="STRICT"` per NFR-005
- Insert `("anti-instinct", ANTI_INSTINCT_GATE)` into `ALL_GATES` between `merge` and `test-strategy` (FR-GATE.3)
- **Constraint**: `gate_passed()` signature unchanged (NFR-009)
- **Coordinate**: Additive-only insertion; verify no merge conflict with WIRING_GATE definition

### 2.2 Executor Integration in `roadmap/executor.py`

- Add `_run_structural_audit()` hook after EXTRACT_GATE pass, before generate steps — warning-only (FR-EXEC.1)
- Add `anti-instinct` step to `_build_steps()` between `merge` and `test-strategy` with `timeout_seconds=30`, `retry_limit=0`, `gate=ANTI_INSTINCT_GATE`, `gate_scope=GateScope.TASK` (FR-EXEC.2)
- Implement `_run_anti_instinct_audit()`: read spec + merged roadmap, invoke all three modules, write `anti-instinct-audit.md` with YAML frontmatter + markdown report (FR-EXEC.3)
- Add explicit executor import/update bundle for sprint-side integration artifacts, including `TrailingGateResult`, `DeferredRemediationLog`, and maintenance of `"anti-instinct"` in `_get_all_step_ids()` between `"merge"` and `"test-strategy"` (FR-EXEC.4)
- **Constraint**: Anti-instinct step is non-LLM; executor runs the audit function directly

### 2.3 Prompt Modifications in `roadmap/prompts.py`

- Add `INTEGRATION_ENUMERATION_BLOCK` to `build_generate_prompt()` before `_OUTPUT_FORMAT_BLOCK` (FR-PROMPT.1)
  - Block instructs LLM to enumerate integration points with named artifacts, wired components, owning phase, cross-reference section
- Add `INTEGRATION_WIRING_DIMENSION` as dimension 6 to `build_spec_fidelity_prompt()` after dimension 5 (FR-PROMPT.2)
  - Dimension instructs LLM to verify wiring tasks for dispatch tables, registries, DI points
- **Note**: Prompt changes are probability reducers. Deterministic modules remain the source of truth.

### 2.4 Integration Tests

- End-to-end roadmap pipeline run with anti-instinct gate active
- Verify gate blocks on known-bad roadmap (cli-portify regression)
- Verify gate passes on known-good roadmap
- Verify structural audit emits warning without blocking
- Verify `anti-instinct-audit.md` output format and frontmatter correctness

### 2.4.1 Validation Gate

- Full roadmap pipeline completes with anti-instinct gate
- SC-001 regression passes end-to-end
- SC-006 latency confirmed
- SC-007 no existing test breakage

**Timeline estimate**: 2–3 days

---

## Phase 3: Sprint Integration & Rollout Mode

**Goal**: Wire the anti-instinct gate into the sprint executor with rollout mode control and TurnLedger integration.

**Milestone M3**: Sprint executor supports `gate_rollout_mode` for anti-instinct with shadow metrics recording.

### 3.1 Sprint Config Extension

- Add `gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "off"` to `SprintConfig` (FR-SPRINT.1)
- Default to `"off"` per NFR-006 — no behavioral change because the gate result is ignored until rollout advances beyond `off`

### 3.2 Sprint Executor Wiring

- Wrap anti-instinct gate result in `TrailingGateResult(passed, evaluation_ms, gate_name)` and submit to `_all_gate_results` (FR-SPRINT.2)
- Implement rollout mode behavior matrix (FR-SPRINT.3):

| Mode | Gate Evaluation | Metrics Recording | Task Behavior |
|------|----------------|-------------------|---------------|
| `off` | Yes (result ignored) | None | No change |
| `shadow` | Yes | `ShadowGateMetrics.record()` | No change |
| `soft` | Yes | `ShadowGateMetrics.record()` | Credit on pass; remediation + `BUDGET_EXHAUSTED` on fail |
| `full` | Yes | `ShadowGateMetrics.record()` | Credit on pass; remediation + `BUDGET_EXHAUSTED` on fail; `TaskResult.status = FAIL` on fail |

- On PASS (soft/full): `ledger.credit(int(upstream_merge_turns * ledger.reimbursement_rate))` (FR-SPRINT.3)
- On FAIL (soft): append to `remediation_log`, exit with `BUDGET_EXHAUSTED` (retry_limit=0) (FR-SPRINT.3)
- On FAIL (full): same as soft plus `TaskResult.status = FAIL` (FR-SPRINT.3)
- Call `ShadowGateMetrics.record(passed, evaluation_ms)` in shadow/soft/full modes (FR-SPRINT.4)
- Feed anti-instinct trailing-gate results into sprint KPI aggregation via `build_kpi_report()` / `GateKPIReport` in sprint context (FR-SPRINT.4)
- Guard ALL TurnLedger calls with `if ledger is not None` (FR-SPRINT.5, NFR-007)

### 3.3 Sprint Integration Tests

- Test rollout mode matrix: all 4 modes × pass/fail scenarios
- Test None-safe ledger guards (standalone mode without TurnLedger)
- Test ShadowGateMetrics recording across modes
- Verify no interaction with existing `wiring_gate_mode` behavior
- Verify anti-instinct and wiring-integrity evaluate independently (NFR-010)

### 3.3.1 Validation Gate (Checkpoint B: Rollout Readiness)

- Sprint pipeline runs with `gate_rollout_mode=shadow`
- SC-008 baseline established (metrics recording confirmed)
- SC-009 no merge conflicts
- Audit outputs explain failures clearly

**Timeline estimate**: 2–3 days

---

## Phase 4: Shadow Validation & Graduation

**Goal**: Run shadow mode across real sprint executions to calibrate thresholds and validate accuracy before enabling enforcement.

**Milestone M4**: `ShadowGateMetrics.pass_rate >= 0.90` over 5+ sprints. Graduation decision documented.

### 4.1 Shadow Mode Activation

- Set `gate_rollout_mode=shadow` in test sprint configurations
- Run anti-instinct gate in parallel with existing gates across 5+ real sprint runs
- Record all `ShadowGateMetrics` data points

### 4.2 Threshold Calibration

- Analyze fingerprint coverage threshold (0.7) against real data (NFR-011)
- Analyze structural audit threshold (0.5) against real data (NFR-011)
- Adjust thresholds if false positive/negative rates exceed acceptable bounds
- Document calibration results and threshold rationale

### 4.3 Open Question Resolution

- OQ-002: Validate 60-char context window against diverse roadmaps; adjust if needed
- OQ-008: Assess multi-component false negatives; expand context extraction if needed
- OQ-007: Verify TurnLedger design.md sections are finalized; reconcile any gaps

### 4.4 Graduation Criteria (Checkpoint C: Enforcement Readiness)

Advance from `off` → `shadow` after Checkpoint B passes.

Advance from `shadow` → `soft` only after:
1. `ShadowGateMetrics.pass_rate >= 0.90` over 5+ sprints (NFR-006, SC-008)
2. False-positive rate is operationally acceptable
3. All false negatives documented with vocabulary/pattern expansion plan
4. Enforcement-related open questions resolved

Advance from `soft` → `full` after additional validation cycle confirms economics and failure semantics are acceptable.

**Rollout sequence**: `off` (ship default) → `shadow` (first adoption) → `soft` (after metrics) → `full` (after stable soft evidence)

**Timeline estimate**: 1–2 sprints (calendar-bound by the 5-sprint shadow validation requirement)

---

## Risk Assessment & Mitigation

### HIGH Risks

| Risk | Description | Mitigation | Phase |
|------|-------------|------------|-------|
| A-002 | Unparseable natural language defeats regex | Prompt constraints (FR-PROMPT.1/2) + fingerprint catch-all + phase parsing fallback | 2, 4 |
| A-009 | Mention-equals-coverage false passes | Verb-anchored patterns + ratio thresholds + named mechanism matching + adversarial tests | 1, 4 |
| A-008 | Unvalidated thresholds | Ship `off` default; warning-only structural audit; shadow calibration before enforcement | 3, 4 |

### MEDIUM Risks

| Risk | Description | Mitigation | Phase |
|------|-------------|------------|-------|
| A-004 | Non-vocabulary scaffold terms | Expandable vocabulary + `# obligation-exempt` escape hatch + shadow miss tracking | 1 |
| A-011 | TurnLedger not instantiated before gate fires | None-safe guards on all ledger calls (FR-SPRINT.5) | 3 |
| A-014 | SprintGatePolicy not instantiated | None-safe guards; explicit mode-matrix tests | 3 |
| D-03/D-04 | Overlap with Unified Audit Gating | Defense-in-depth; both evaluate independently (NFR-010). Document overlap. | 3 |
| Merge conflict | Both anti-instinct and WIRING_GATE modify `gates.py` | Additive-only changes; coordinate timing; rebase before merge | 2 |

### LOW Risks

| Risk | Description | Mitigation | Phase |
|------|-------------|------------|-------|
| A-001 | No requirement IDs in extraction | Fingerprints work without IDs | 1 |
| A-007 | SemanticCheck single-file limitation | Executor-level workaround; model extension deferred | 2 |
| A-010 | Correlated LLM tendencies | N/A — all checks are deterministic | 1 |
| A-012 | Incorrect default for `gate_rollout_mode` | Explicit `"off"` in code | 3 |
| A-013 | Single reimbursement rate insufficient | Sufficient for v3.1; extensibility noted | 3 |

---

## Resource Requirements & Dependencies

### Engineering Resources

| Role | Responsibility |
|------|---------------|
| 1 backend/pipeline engineer | Analyzers, gate wiring, sprint integration |
| 1 QA-focused engineer (or shared ownership) | Unit tests, integration tests, regression harness, latency verification |
| 1 architecture reviewer | Shared-file coordination, rollout readiness, threshold promotion approval |

### New Files (12)

| File | Module | Phase |
|------|--------|-------|
| `src/superclaude/cli/roadmap/obligation_scanner.py` | FR-MOD1 | 1 |
| `src/superclaude/cli/roadmap/integration_contracts.py` | FR-MOD2 | 1 |
| `src/superclaude/cli/roadmap/fingerprint.py` | FR-MOD3 | 1 |
| `src/superclaude/cli/roadmap/spec_structural_audit.py` | FR-MOD4 | 1 |
| `tests/roadmap/test_obligation_scanner.py` | Tests | 1 |
| `tests/roadmap/test_integration_contracts.py` | Tests | 1 |
| `tests/roadmap/test_fingerprint.py` | Tests | 1 |
| `tests/roadmap/test_spec_structural_audit.py` | Tests | 1 |
| `tests/roadmap/test_anti_instinct_integration.py` | Tests | 2 |
| `tests/sprint/test_anti_instinct_sprint.py` | Tests | 3 |
| `tests/sprint/test_shadow_mode.py` | Tests (shadow mode integration) | 3 |
| `tests/pipeline/test_full_flow.py` | Tests (full flow + reimbursement path) | 3 |

### Modified Files (5)

| File | Changes | Phase | Conflict Risk |
|------|---------|-------|---------------|
| `src/superclaude/cli/roadmap/gates.py` | Add `ANTI_INSTINCT_GATE`, insert into `ALL_GATES` | 2 | MEDIUM (WIRING_GATE) |
| `src/superclaude/cli/roadmap/executor.py` | Add step, audit function, structural audit hook | 2 | LOW |
| `src/superclaude/cli/roadmap/prompts.py` | Add 2 prompt blocks | 2 | LOW |
| `src/superclaude/cli/sprint/models.py` | Add `gate_rollout_mode` field | 3 | LOW |
| `src/superclaude/cli/sprint/executor.py` | Add gate evaluation, rollout logic, ledger guards | 3 | MEDIUM (TurnLedger) |

### External Dependencies

- Python `re` (stdlib) — core regex engine
- Python `dataclasses` (stdlib) — data structures
- Python `yaml` — frontmatter parsing (already used by executor)
- No new third-party dependencies

### Requirement Coverage Matrix

| Requirement Group | Requirements | Phase |
|-------------------|-------------|-------|
| Core modules | FR-MOD1.1–1.8, FR-MOD2.1–2.6, FR-MOD3.1–3.4, FR-MOD4.1–4.3 | 1 |
| Gate and executor | FR-GATE.1–3, FR-EXEC.1–4 | 2 |
| Prompt path | FR-PROMPT.1–2 | 2 |
| Sprint path | FR-SPRINT.1–5 | 3 |
| Architectural invariants | NFR-001, NFR-004, NFR-008, NFR-009, NFR-010 | All |
| Latency | NFR-002 | 1, 2 |
| Enforcement & rollout | NFR-005, NFR-006, NFR-007, NFR-011 | 2, 3, 4 |

---

## Success Criteria & Validation Approach

### Success Criteria

| Criterion | Validation Method | Phase |
|-----------|-------------------|-------|
| SC-001 | Three semantic checks pass on cli-portify regression (end-to-end) | 2 |
| SC-002 | Obligation scanner detects "mocked steps" without discharge (85% confidence) | 1 |
| SC-003 | Contract extractor detects `PROGRAMMATIC_RUNNERS` without wiring task (90% confidence) | 1 |
| SC-004 | Fingerprint checker detects missing `_run_programmatic_step`, `PROGRAMMATIC_RUNNERS`, `test_programmatic_step_routing` (95% confidence) | 1 |
| SC-005 | Structural audit flags extraction inadequacy (ratio < 0.5) | 1 |
| SC-006 | Combined latency < 1s | 1, 2 |
| SC-007 | Zero existing test breakage | 1, 2, 3 |
| SC-008 | Shadow pass rate ≥ 0.90 over 5+ sprints | 4 |
| SC-009 | Zero merge conflicts with TurnLedger | 2, 3 |

### Cross-Cutting Validation Taxonomy

| Category | Scope | Phases |
|----------|-------|--------|
| **A: Unit** | Each analyzer independently against focused fixtures | 1 |
| **B: Integration** | Pipeline step position, frontmatter parsing, audit artifact generation, gate registration order | 2 |
| **C: Sprint-mode** | All 4 rollout modes × pass/fail, ledger present/absent, reimbursement/remediation semantics | 3 |
| **D: Regression** | cli-portify failure case end-to-end | 1, 2 |
| **E: Non-functional** | Latency benchmarks, full test suite backward compat, statelessness proof | 1, 2, 3 |

### Validation Checkpoints

| Checkpoint | Gate | Criteria |
|------------|------|----------|
| **A: Implementation Readiness** | End of Phase 1 | All new tests green, existing tests green, SC-006 satisfied, no signature/statelessness violations |
| **B: Rollout Readiness** | End of Phase 3 | cli-portify regression proven, shadow metrics collection functioning, audit outputs explain failures clearly |
| **C: Enforcement Readiness** | During Phase 4 | SC-008 satisfied, false positives reviewed, enforcement-related OQs closed |

---

## Timeline Estimates

| Phase | Description | Estimate | Dependencies |
|-------|-------------|----------|--------------|
| **Phase 1** | Core detection modules + architecture decisions + unit tests | 2–3 days | None — fully independent |
| **Phase 2** | Gate definition + executor wiring + prompts + integration tests | 2–3 days | Phase 1 complete; coordinate with WIRING_GATE |
| **Phase 3** | Sprint integration + rollout mode | 2–3 days | Phase 2 complete |
| **Phase 4** | Shadow validation + threshold calibration + graduation | 1–2 sprints | Phase 3 complete |

**Total build time**: 6–9 working days. **Total to enforcement confidence**: 1–2 additional sprints of shadow observation.

### Critical Path

```
Phase 1 (modules + decisions) → Phase 2 (wiring + prompts) → Phase 3 (sprint) → Phase 4 (shadow)
```

No cross-phase parallelism. Phase 1 modules are internally parallelizable (all four modules are independent). Unit tests can be developed alongside module coding within Phase 1.

---

## Architect Recommendations

1. **Build and prove analyzers first.** Shared pipeline edits should come only after deterministic behavior is trusted.

2. **Resolve semantic ambiguity before strict enforcement.** OQ-003, OQ-004, OQ-005, OQ-009, and OQ-010 directly affect pass/fail correctness — resolve on day 1 of Phase 1.

3. **Treat prompt changes as support, not enforcement.** The anti-instinct feature succeeds only if deterministic checks remain authoritative.

4. **Protect shared-file stability.** `gates.py`, `executor.py`, and sprint executor/model changes are the highest coordination-risk edits. Keep changes additive and localized.

5. **Use shadow-mode evidence as the promotion gate.** Required by both architecture and sprint economics. Do not skip to enforcement without data.
