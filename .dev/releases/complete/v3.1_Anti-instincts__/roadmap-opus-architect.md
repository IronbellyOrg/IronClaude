---
spec_source: "anti-instincts-gate-unified.md"
complexity_score: 0.72
primary_persona: architect
---

# v3.1 Anti-Instinct Gate — Project Roadmap

## Executive Summary

This release adds a deterministic, zero-LLM anti-instinct gating layer to the SuperClaude roadmap and sprint pipelines. Four pure-Python detection modules — obligation scanner, integration contract extractor, fingerprint coverage checker, and spec structural auditor — catch the class of "scaffold-without-discharge" bugs that LLM-on-LLM review structurally misses. The gate slots between `merge` and `test-strategy` in the existing pipeline, is additive-only to shared files, and ships with `gate_rollout_mode=off` to ensure zero behavioral change until shadow validation confirms accuracy.

**Scope**: 34 requirements (23 functional, 11 non-functional) across 10 new files and 5 modified files (~1,200 LOC total). HIGH complexity (0.72) driven by dual execution context (standalone roadmap vs sprint-invoked) and three independent regex engines.

**Key architectural decision**: All detection is deterministic Python. No LLM calls. This is non-negotiable per NFR-001.

---

## Phase 1: Core Detection Modules (Pure Python)

**Goal**: Implement all four detection modules as standalone, pure-function libraries with comprehensive tests. No pipeline integration yet.

**Milestone**: All four modules pass unit tests against the cli-portify regression case.

### 1.1 Obligation Scanner (`obligation_scanner.py`)

- Implement compiled regex vocabulary for 11 scaffold terms (FR-MOD1.1)
- Implement phase-section parser splitting on H2/H3 headings with fallback (FR-MOD1.2)
- Implement cross-phase discharge search with verb-anchored patterns (FR-MOD1.3)
- Implement 60-char component context extraction: backtick-priority, capitalized-fallback (FR-MOD1.4)
- Implement dual-condition discharge matching (term + component name) (FR-MOD1.5)
- Define `ObligationReport` and `Obligation` dataclasses (FR-MOD1.6)
- Implement `# obligation-exempt` comment parsing (per-line scope) (FR-MOD1.7)
- Implement code-block severity demotion to MEDIUM (FR-MOD1.8)
- **Decision required (OQ-003)**: Define exact `# obligation-exempt` syntax before implementation — recommend per-line scope on the scaffold term's line
- **Decision required (OQ-004)**: Define MEDIUM severity semantics — recommend adding `medium_severity_obligations` count to frontmatter, excluded from gate-blocking `undischarged_obligations`

### 1.2 Integration Contract Extractor (`integration_contracts.py`)

- Implement 7-category dispatch pattern scanner with compiled regexes (FR-MOD2.1)
- Implement context capture (3 lines), mechanism classification, sequential ID assignment, deduplication (FR-MOD2.2)
- Implement verb-anchored wiring task coverage check (FR-MOD2.3)
- Implement named mechanism identifier matching (UPPER_SNAKE_CASE, PascalCase) (FR-MOD2.4)
- Enforce wiring-task-specific coverage semantics (FR-MOD2.5)
- Define `IntegrationAuditResult` dataclass with `all_covered` property (FR-MOD2.6)
- **Decision required (OQ-009)**: Recommend contract-specific coverage matching in Phase 2; Phase 1 ships with global pattern matching per spec

### 1.3 Fingerprint Extraction (`fingerprint.py`)

- Implement three-source extraction: backtick identifiers (≥4 chars), code-block `def`/`class`, ALL_CAPS constants (FR-MOD3.1)
- Implement `_EXCLUDED_CONSTANTS` frozenset filtering (FR-MOD3.1)
- Implement deduplication by text value (FR-MOD3.2)
- Implement case-insensitive roadmap coverage check returning 4-tuple (FR-MOD3.3)
- Implement threshold gate logic (default 0.7) with empty-fingerprint passthrough (FR-MOD3.4)
- **Note (OQ-011)**: Align `_EXCLUDED_CONSTANTS` entries with the 4-char regex minimum; remove 3-char entries that can never match
- **Note (OQ-001)**: Keep hardcoded for Phase 1; extensibility deferred to Phase 2

### 1.4 Spec Structural Audit (`spec_structural_audit.py`)

- Implement 7 structural indicator counters (FR-MOD4.1)
- Implement ratio comparison against `total_requirements` frontmatter (FR-MOD4.2)
- Phase 1: warning-only enforcement, no pipeline blocking (FR-MOD4.3)
- **Note (OQ-006)**: Transition to STRICT is manual configuration, triggered after shadow-mode metrics confirm threshold adequacy per NFR-011

### 1.5 Unit Tests for All Modules

- `test_obligation_scanner.py`: scaffold detection, discharge matching, exempt comments, code-block severity, cli-portify regression (validates SC-002)
- `test_integration_contracts.py`: 7-category detection, wiring coverage, deduplication, cli-portify regression (validates SC-003)
- `test_fingerprint.py`: three-source extraction, deduplication, coverage ratio, threshold boundary, cli-portify regression (validates SC-004)
- `test_spec_structural_audit.py`: all 7 indicators, ratio comparison, warning-only behavior (validates SC-005)
- All tests use real content fixtures, no mocks (per project eval philosophy)

**Validation gate**: SC-001 through SC-005 pass. SC-006 (latency <1s) verified via timing assertions. SC-007 (backward compat) verified by running full existing test suite.

---

## Phase 2: Gate Definition & Executor Wiring

**Goal**: Wire the four modules into the roadmap pipeline as the `anti-instinct` gate step. No sprint integration yet.

**Milestone**: `anti-instinct` step executes between `merge` and `test-strategy` in standalone roadmap mode.

### 2.1 Gate Definition in `roadmap/gates.py`

- Define `ANTI_INSTINCT_GATE` as `GateCriteria` with required frontmatter: `undischarged_obligations` (int), `uncovered_contracts` (int), `fingerprint_coverage` (float) (FR-GATE.1)
- Implement three semantic checks (FR-GATE.2):
  - `_no_undischarged_obligations`: parse `undischarged_obligations` from frontmatter, assert == 0
  - `_integration_contracts_covered`: parse `uncovered_contracts` from frontmatter, assert == 0
  - `_fingerprint_coverage_sufficient`: parse `fingerprint_coverage` from frontmatter, assert >= 0.7
- Set `enforcement_tier="STRICT"` per NFR-005
- Insert `("anti-instinct", ANTI_INSTINCT_GATE)` into `ALL_GATES` between `merge` and `test-strategy` (FR-GATE.3)
- **Constraint**: `gate_passed()` signature in `pipeline/gates.py` remains unchanged (NFR-009)
- **Coordinate**: Additive-only insertion; verify no merge conflict with WIRING_GATE definition (Risk #8)

### 2.2 Executor Integration in `roadmap/executor.py`

- Add `_run_structural_audit()` hook after EXTRACT_GATE pass, before generate steps — warning-only (FR-EXEC.1)
- Add `anti-instinct` step to `_build_steps()` between `merge` and `test-strategy` with `timeout_seconds=30`, `retry_limit=0`, `gate=ANTI_INSTINCT_GATE`, `gate_scope=GateScope.TASK` (FR-EXEC.2)
- Implement `_run_anti_instinct_audit()`: read spec + merged roadmap, invoke all three modules, write `anti-instinct-audit.md` with YAML frontmatter + markdown report (FR-EXEC.3)
- Add `"anti-instinct"` to `_get_all_step_ids()` between `"merge"` and `"test-strategy"` (FR-EXEC.4)
- **Constraint**: Anti-instinct step is non-LLM; executor runs the audit function directly rather than dispatching to an LLM agent

### 2.3 Prompt Modifications in `roadmap/prompts.py`

- Add `INTEGRATION_ENUMERATION_BLOCK` to `build_generate_prompt()` before `_OUTPUT_FORMAT_BLOCK` (FR-PROMPT.1)
  - Block instructs LLM to enumerate integration points with named artifacts, wired components, owning phase, cross-reference section
- Add `INTEGRATION_WIRING_DIMENSION` as dimension 6 to `build_spec_fidelity_prompt()` after dimension 5 (FR-PROMPT.2)
  - Dimension instructs LLM to verify wiring tasks for dispatch tables, registries, DI points
- **Decision required (OQ-010)**: Recommend adding a downstream validator that checks for `## Integration Wiring Tasks` heading in merged output; without this, the prompt instruction has no enforcement

### 2.4 Integration Tests

- End-to-end roadmap pipeline run with anti-instinct gate active
- Verify gate blocks on known-bad roadmap (cli-portify regression)
- Verify gate passes on known-good roadmap
- Verify structural audit emits warning without blocking
- Verify `anti-instinct-audit.md` output format and frontmatter correctness

**Validation gate**: Full roadmap pipeline completes with anti-instinct gate. SC-001 regression passes end-to-end. SC-006 latency confirmed. SC-007 no existing test breakage.

---

## Phase 3: Sprint Integration & Rollout Mode

**Goal**: Wire the anti-instinct gate into the sprint executor with rollout mode control and TurnLedger integration.

**Milestone**: Sprint executor supports `gate_rollout_mode` for anti-instinct with shadow metrics recording.

### 3.1 Sprint Config Extension

- Add `gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "off"` to `SprintConfig` (FR-SPRINT.1)
  - Note: existing `wiring_gate_mode` follows same pattern; maintain consistency
- Default to `"off"` per NFR-006 — no behavioral change until shadow validation

### 3.2 Sprint Executor Wiring

- Wrap anti-instinct gate result in `TrailingGateResult(step_id, passed, evaluation_ms)` and submit to `_all_gate_results` (FR-SPRINT.2)
- Implement rollout mode behavior matrix (FR-SPRINT.3):
  - `off`: no gate evaluation
  - `shadow`: evaluate and record metrics only
  - `soft`: evaluate, record, credit on pass, remediate on fail (no task failure)
  - `full`: evaluate, record, credit on pass, fail task on fail
- On PASS (soft/full): `ledger.credit(int(upstream_merge_turns * ledger.reimbursement_rate))` (FR-SPRINT.3)
- On FAIL: append to `remediation_log`, exit with `BUDGET_EXHAUSTED` (retry_limit=0) (FR-SPRINT.3)
- On FAIL + full: set `TaskResult.status = FAIL` (FR-SPRINT.3)
- Call `ShadowGateMetrics.record(passed, evaluation_ms)` in ALL modes (FR-SPRINT.4)
- Guard ALL TurnLedger calls with `if ledger is not None` (FR-SPRINT.5, NFR-007)

### 3.3 D-03/D-04 Coexistence Decision

- **Decision required (OQ-005)**: Resolve coexistence strategy before sprint integration
  - **Option A**: Conditional activation — disable D-03/D-04 overlap modules when anti-instinct gate is active
  - **Option B**: Defense-in-depth — both run independently, accept redundancy
  - **Recommendation**: Option B (defense-in-depth) for Phase 1. Both gates evaluate independently per NFR-010. Document overlap in operator guide. Consolidate in Phase 2 if metrics show redundancy.

### 3.4 Sprint Integration Tests

- Test rollout mode matrix: all 4 modes × pass/fail scenarios
- Test None-safe ledger guards (standalone mode without TurnLedger)
- Test ShadowGateMetrics recording across modes
- Verify no interaction with existing `wiring_gate_mode` behavior

**Validation gate**: Sprint pipeline runs with `gate_rollout_mode=shadow`. SC-008 baseline established (metrics recording confirmed). SC-009 no merge conflicts.

---

## Phase 4: Shadow Validation & Graduation

**Goal**: Run shadow mode across real sprint executions to calibrate thresholds and validate accuracy before enabling enforcement.

**Milestone**: `ShadowGateMetrics.pass_rate >= 0.90` over 5+ sprints.

### 4.1 Shadow Mode Activation

- Set `gate_rollout_mode=shadow` in test sprint configurations
- Run anti-instinct gate in parallel with existing gates across 5+ real sprint runs
- Record all `ShadowGateMetrics` data points

### 4.2 Threshold Calibration

- Analyze fingerprint coverage threshold (0.7) against real data (NFR-011)
- Analyze structural audit threshold (0.5) against real data (NFR-011)
- Adjust thresholds if false positive/negative rates exceed acceptable bounds
- Document calibration results and threshold rationale

### 4.3 Graduation Criteria

- `ShadowGateMetrics.pass_rate >= 0.90` over 5+ sprints (NFR-006)
- Zero false positives on known-good roadmaps
- All false negatives documented with vocabulary/pattern expansion plan
- Graduate to `soft` mode, then `full` after additional validation cycle

### 4.4 Open Question Resolution

- OQ-002: Validate 60-char context window against diverse roadmaps; adjust if needed
- OQ-008: Assess multi-component false negatives; expand context extraction if needed
- OQ-007: Verify TurnLedger design.md sections are finalized; reconcile any gaps

**Validation gate**: SC-008 fully met. Graduation decision documented.

---

## Risk Assessment & Mitigation

### HIGH Risks

| Risk | Description | Mitigation | Phase |
|------|-------------|------------|-------|
| A-002 | Unparseable natural language defeats regex | Prompt constraints (FR-PROMPT.1, FR-PROMPT.2) + fingerprint catch-all | 2, 4 |
| A-009 | Mention-equals-coverage false passes | Verb-anchored patterns + ratio thresholds + combined checks | 1, 4 |
| A-008 | Unvalidated thresholds | Shadow mode before enforcement; `gate_rollout_mode=off` default | 3, 4 |

### MEDIUM Risks

| Risk | Description | Mitigation | Phase |
|------|-------------|------------|-------|
| A-004 | Non-vocabulary scaffold terms | Expandable vocabulary + `# obligation-exempt` escape hatch | 1 |
| A-011 | TurnLedger not instantiated before gate fires | None-safe guards on all ledger calls (FR-SPRINT.5) | 3 |
| A-014 | SprintGatePolicy not instantiated | Cross-cutting concern; None-safe guards | 3 |
| D-03/D-04 | Overlap with Unified Audit Gating | Defense-in-depth (Option B); consolidate in Phase 2 | 3 |
| Merge conflict | Both anti-instinct and WIRING_GATE modify `gates.py` | Additive-only changes; coordinate timing | 2 |

### LOW Risks

| Risk | Description | Mitigation | Phase |
|------|-------------|------------|-------|
| A-001 | No requirement IDs in extraction | Fingerprints work without IDs | 1 |
| A-007 | SemanticCheck single-file limitation | Executor-level workaround; Phase 2 model extension | 2 |
| A-010 | Correlated LLM tendencies | N/A — all Phase 1 checks are deterministic | 1 |
| A-012 | Incorrect default for `gate_rollout_mode` | Explicit `"off"` in code | 3 |
| A-013 | Single reimbursement rate insufficient | Sufficient for v3.1; extensibility noted | 3 |
| Phase 2 debt | Deferred items never adopted | Explicit adoption conditions per item | 4 |

---

## Resource Requirements & Dependencies

### New Files (10)

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

### Modified Files (5)

| File | Changes | Phase | Conflict Risk |
|------|---------|-------|---------------|
| `src/superclaude/cli/roadmap/gates.py` | Add `ANTI_INSTINCT_GATE`, insert into `ALL_GATES` | 2 | MEDIUM (WIRING_GATE) |
| `src/superclaude/cli/roadmap/executor.py` | Add step, audit function, structural audit hook | 2 | LOW |
| `src/superclaude/cli/roadmap/prompts.py` | Add 2 prompt blocks | 2 | LOW |
| `src/superclaude/cli/sprint/models.py` | Add `gate_rollout_mode` field | 3 | LOW |
| `src/superclaude/cli/sprint/executor.py` | Add gate evaluation, rollout logic, ledger guards | 3 | MEDIUM (TurnLedger) |

### External Dependencies

- Python `re` module (stdlib) — core regex engine
- Python `dataclasses` module (stdlib) — data structures
- Python `yaml` module — frontmatter parsing (already used by executor)
- No new third-party dependencies

---

## Success Criteria & Validation Approach

| Criterion | Validation Method | Phase |
|-----------|-------------------|-------|
| SC-001: Three semantic checks pass on cli-portify regression | End-to-end pipeline test with known-good input | 2 |
| SC-002: Obligation scanner detects "mocked steps" without discharge (85% confidence) | Unit test with cli-portify roadmap fixture | 1 |
| SC-003: Contract extractor detects `PROGRAMMATIC_RUNNERS` without wiring task (90% confidence) | Unit test with cli-portify roadmap fixture | 1 |
| SC-004: Fingerprint checker detects missing `_run_programmatic_step`, `PROGRAMMATIC_RUNNERS`, `test_programmatic_step_routing` (95% confidence) | Unit test with cli-portify roadmap fixture | 1 |
| SC-005: Structural audit flags extraction inadequacy (ratio < 0.5) | Unit test with crafted spec/extraction mismatch | 1 |
| SC-006: Combined latency < 1s | Timing assertions in integration tests | 2 |
| SC-007: Zero existing test breakage | Full `make test` in every phase | 1, 2, 3 |
| SC-008: Shadow pass rate ≥ 0.90 over 5+ sprints | Shadow mode metrics accumulation | 4 |
| SC-009: Zero merge conflicts with TurnLedger | File change coordination; verified at PR time | 2, 3 |

---

## Timeline Estimates

| Phase | Description | Estimated Effort | Dependencies |
|-------|-------------|------------------|--------------|
| **Phase 1** | Core detection modules + unit tests | 2–3 sprints | None — fully independent |
| **Phase 2** | Gate definition + executor wiring + prompts + integration tests | 1–2 sprints | Phase 1 complete; coordinate with WIRING_GATE timing |
| **Phase 3** | Sprint integration + rollout mode | 1–2 sprints | Phase 2 complete; OQ-005 decision (D-03/D-04 coexistence) |
| **Phase 4** | Shadow validation + threshold calibration + graduation | 2–3 sprints (calendar time for 5+ sprint runs) | Phase 3 complete |

**Total**: 6–10 sprints, with Phase 4 being calendar-bound by the 5-sprint shadow validation requirement.

### Critical Path

```
Phase 1 (modules) → Phase 2 (wiring) → Phase 3 (sprint) → Phase 4 (shadow)
```

No parallelism between phases. Phase 1 modules are internally parallelizable (all four modules are independent). Phase 2 and Phase 3 each have internal sequential dependencies (gate definition before executor wiring; config before executor logic).

### Open Questions Requiring Pre-Implementation Decisions

| OQ | Question | Blocks | Recommended Resolution |
|----|----------|--------|----------------------|
| OQ-003 | `# obligation-exempt` syntax | Phase 1.1 | Per-line scope on scaffold term line |
| OQ-004 | MEDIUM severity vs STRICT gate | Phase 1.1 | Separate `medium_severity_obligations` frontmatter field, excluded from gate blocking |
| OQ-005 | D-03/D-04 coexistence | Phase 3.3 | Defense-in-depth; both run independently |
| OQ-010 | `## Integration Wiring Tasks` validation | Phase 2.3 | Add heading presence check to merge gate or as structural audit indicator |
