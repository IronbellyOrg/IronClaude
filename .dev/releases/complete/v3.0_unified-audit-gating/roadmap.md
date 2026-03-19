---
spec_source: merged-spec.md
complexity_score: 0.78
adversarial: true
---

# Unified Audit Gating — Final Merged Roadmap

## Executive Summary

This roadmap delivers a **static wiring verification gate** for the SuperClaude pipeline that detects three classes of integration defects — unwired injectable callables, orphan modules, and broken dispatch registries — using deterministic AST analysis. The system integrates into the roadmap pipeline as a post-merge step, extends the sprint executor with a mode-aware hook, and enriches the cleanup-audit agent suite with wiring-aware behavioral rules.

**Key architectural constraints**:
- Zero modifications to the `pipeline/*` substrate. All new code consumes existing contracts (`GateCriteria`, `SemanticCheck`, `Step`, `GateMode`) without altering them.
- Every enforcement decision must be explainable from report frontmatter and evidence sections alone (design for auditability).

**Rollout strategy**: Three-phase shadow → soft → full enforcement with statistical FPR calibration gates between phases.

**Scope**: 8 goals (G-001–G-008), 14 success criteria (SC-001–SC-014), ~480-580 LOC production code, ~420-560 LOC test code, touching 3 subsystems (roadmap, sprint, audit) plus 5 agent specs.

**Phase structure**: 6 primary phases with structural sub-phases where the debate identified substantive separation value (sprint/roadmap integration, validation/activation). A compressed decision checkpoint precedes implementation.

---

## Phased Implementation Plan

### Phase 0 — Decision Checkpoint (2-4 hours, not a full phase)

**Goal**: Commit to answers for all open questions before code begins. Not a process gate — a documented 2-4 hour review producing a decision log.

**Decisions to resolve**:

| # | Question | Proposed Default | Source |
|---|----------|-----------------|--------|
| OQ-1 | How are `audit_artifacts_used` located/counted? | Glob for `*-audit-report.yaml` in output dir | Opus |
| OQ-2 | Are `exclude_patterns` matches counted in `files_skipped`? | Yes, for visibility | Opus |
| OQ-3 | Is whitelist strictness derived from `rollout_mode`? | shadow → WARNING; soft/full → `WiringConfigError` | Opus |
| OQ-4 | Does `SprintConfig.source_dir` already exist? | Verify before Phase 3a | Opus |
| OQ-5 | Comparator/consolidator extension scope? | Additive wiring sections only, no restructure | Haiku |
| OQ-6 | Rollout ownership for `grace_period`? | Single accountable owner for shadow metrics and activation | Haiku |
| OQ-7 | Merge sequencing with concurrent PRs? | Complete Phases 1-2 before touching shared files | Both |

**Deliverable**: Architecture decision log recording committed answers.

**Exit criterion**: All 7 questions have committed answers with rationale.

---

### Phase 1 — Core Analysis Engine (Sprint 1)

**Goal**: Standalone wiring analyzer producing structured findings, no pipeline integration yet.

**Milestone M1**: `run_wiring_analysis()` returns correct `WiringReport` for all three detection types against test fixtures.

| Task | Files | Requirements | Est. LOC |
|------|-------|-------------|----------|
| 1.1a Define `WiringConfig` dataclass, `DEFAULT_REGISTRY_PATTERNS`, whitelist loading | `cli/audit/wiring_config.py` | §4.2.1, §5.2.1 | 50-70 |
| 1.1b Define `WiringFinding`, `WiringReport` dataclasses | `cli/audit/wiring_gate.py` | §5.1 | 40-60 |
| 1.2 Implement unwired callable analysis | `cli/audit/wiring_gate.py` | §5.2.1, G-001 | 80-100 |
| 1.3 Implement orphan module analysis | `cli/audit/wiring_gate.py` | §5.2.2, G-002 | 70-90 |
| 1.4 Implement registry analysis | `cli/audit/wiring_gate.py` | §5.2.3, G-003 | 60-80 |
| 1.5 Implement whitelist loading + suppression | `cli/audit/wiring_config.py` | §5.2.1 whitelist | (included in 1.1a) |
| 1.6 Implement `ast_analyze_file()` utility | `cli/audit/wiring_analyzer.py` | §5.3, G-008 | 40-50 |
| 1.7 Unit tests for all three analyzers + whitelist | `tests/audit/` | §10.1, §10.3, SC-001–SC-003, SC-007 | 200-250 |

**Validation checkpoint**:
- All 3 detection types produce correct findings against known fixtures
- Whitelist suppression works; `SyntaxError` handled gracefully
- Performance: < 5s for 50-file fixture (SC-008); aspirational < 2s per R4 sprint target

---

### Phase 2 — Report Emission & Gate Definition (Sprint 2)

**Goal**: Structured YAML+Markdown report that passes `gate_passed()` validation. Gate criteria defined but not yet wired into pipeline.

**Milestone M2**: `gate_passed(report_path, WIRING_GATE)` returns `(True, None)` for well-formed shadow-mode reports.

| Task | Files | Requirements | Est. LOC |
|------|-------|-------------|----------|
| 2.1 Implement report emitter (frontmatter + 7 Markdown sections); use `yaml.safe_dump()` for string fields per §5.4 | `cli/audit/wiring_gate.py` | §5.4, §5.4.1, G-004 | 80-100 |
| 2.2 Implement `_extract_frontmatter_values()` helper (duplicate `_FRONTMATTER_RE` per §5.5, preserve NFR-007 layering) | `cli/audit/wiring_gate.py` | §5.5 | 15 |
| 2.3 Define `WIRING_GATE` as `GateCriteria` (16 required frontmatter fields) | `cli/audit/wiring_gate.py` | §5.6 | 20-30 |
| 2.4 Implement 5 semantic check functions | `cli/audit/wiring_gate.py` | §5.6 semantic_checks | 40-50 |
| 2.5 Implement `blocking_for_mode()` logic | `cli/audit/wiring_gate.py` | §5.1, §5.6 mode-aware enforcement | 15-20 |
| 2.6 Unit tests for report + gate + semantic checks | `tests/audit/` | SC-004, SC-014, §10.1 (4 tests for emit_report+gate), §10.3 (≥90% coverage) | 100-130 |

**Validation checkpoint**:
- Report frontmatter contains all 16 required fields per §5.6
- `gate_passed()` (unmodified) correctly evaluates `WIRING_GATE`
- Mode-aware semantics: shadow always passes; soft blocks on critical; full blocks on critical+major
- 90% coverage on `wiring_gate.py` and `wiring_analyzer.py`

---

### Phase 3a — Roadmap Pipeline Integration (Sprint 3)

**Goal**: Wiring verification runs as a pipeline step in shadow mode.

**Milestone M3a**: End-to-end roadmap pipeline executes wiring-verification step and emits report without blocking.

| Task | Files | Requirements | Est. LOC |
|------|-------|-------------|----------|
| 3a.1 Add `build_wiring_verification_prompt(merge_file: Path, spec_source: str) -> str` stub | `roadmap/prompts.py` | §5.7 Step 2 | 5 |
| 3a.2 Add wiring-verification `Step` to `_build_steps()` with `timeout_seconds=60`, `retry_limit=0`, `inputs=[merge_file, spec_fidelity_file]`, `gate_mode=GateMode.TRAILING`; also update `_get_all_step_ids()` to include `"wiring-verification"` after `"spec-fidelity"` and before `"remediate"` per §5.7 Step 5 (INV-003) | `roadmap/executor.py` | §5.7 Steps 4-5 | 15-20 |
| 3a.3 Special-case `roadmap_run_step()` for wiring-verification: call `run_wiring_analysis()`, `emit_report()`, return `StepStatus.PASS` unconditionally (gate evaluation is separate) per §5.7.1 | `roadmap/executor.py` | §5.7.1, G-006 | 20-30 |
| 3a.4 Register `WIRING_GATE` in `ALL_GATES` | `roadmap/gates.py` | §5.7 Step 5 | 3 |
| 3a.5 Integration tests for roadmap pipeline (include resume behavior validation per §5.7.2) | `tests/integration/` | SC-005, §10.2 (≥3 integration tests) | 40-50 |

**Validation checkpoint**:
- `_get_all_step_ids()` returns wiring-verification between spec-fidelity and remediate
- Pipeline runs end-to-end with shadow gate (no blocking)
- No imports from `pipeline/*` into `roadmap/*` or `audit/*` violating layering (NFR-007)

---

### Phase 3b — Sprint Integration (Sprint 3, after 3a validates)

**Goal**: Sprint executor applies wiring analysis with mode-aware behavior, validated independently from roadmap integration.

**Milestone M3b**: Sprint execution honors shadow/soft/full semantics without regressions.

**Rationale for separation**: The debate (D3 rebuttal) established that integration bugs in the sprint hot path — exceptions, latency, state corruption — are not mitigated by shadow mode's finding-level pass-through. Sprint integration affects every task execution; roadmap integration runs once per release. Independent validation reduces the chance of a sprint-blocking regression masked by roadmap test coverage.

| Task | Files | Requirements | Est. LOC |
|------|-------|-------------|----------|
| 3b.1 Add `wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"` to `SprintConfig` | `sprint/models.py` | §5.8 | 5 |
| 3b.2 Implement sprint post-task wiring hook | `sprint/executor.py` | §5.8, G-005 | 30-40 |
| 3b.3 Pre-activation safeguards (>50 files must produce >0 findings per §7; zero-match warning, whitelist validation) | `sprint/executor.py` | SC-010, §7 Phase 1 checklist | 15-20 |
| 3b.4 Integration tests for sprint hook (test off/shadow/soft/full modes) | `tests/integration/` | SC-006 | 30-50 |

**Validation checkpoint**:
- Sprint hook logs findings without affecting task status (shadow)
- Sprint hook warns on critical findings (soft)
- Sprint hook blocks on critical+major findings (full)
- No performance regression on task execution path

---

### Phase 4 — Audit Agent Extensions (Sprint 3-4, parallelizable with Phase 3a/3b)

**Goal**: Cleanup-audit agents enriched with wiring-aware rules.

**Milestone M4**: Audit pipeline produces wiring path information in analyzer profiles and validates wiring claims.

| Task | Files | Requirements | Est. LOC |
|------|-------|-------------|----------|
| 4.1 Extend audit-scanner with `REVIEW:wiring` signal | `agents/audit-scanner.md` | §6.2, SC-011 | Behavioral spec |
| 4.2 Extend audit-analyzer with 9th field + finding types | `agents/audit-analyzer.md` | §6.3, SC-012 | Behavioral spec |
| 4.3 Extend audit-validator with Check 5 | `agents/audit-validator.md` | §6.4 | Behavioral spec |
| 4.4 Extend audit-comparator with cross-file wiring check | `agents/audit-comparator.md` | §6.1, G-007 | Behavioral spec |
| 4.5 Extend audit-consolidator with Wiring Health section | `agents/audit-consolidator.md` | §6.1, G-007 | Behavioral spec |
| 4.6 Agent regression tests | `tests/audit/` | SC-011, SC-012 | Behavioral validation |

**Validation approach** (adopted from Haiku's staged strategy): Validate each agent extension independently with regression tests against prior audit outputs before combining. This addresses the emergent behavioral risk of LLM-interpreted spec changes (R7) while maintaining the MEDIUM severity rating.

**Validation checkpoint**:
- All extensions are strictly additive (§6.1: no tools changed, no rules removed)
- Scanner classifies wiring-indicator files correctly
- Analyzer produces complete 9-field profiles with Wiring path
- Validator catches DELETE recommendations on files with live wiring
- No regression in existing audit output quality

---

### Phase 5 — ToolOrchestrator Plugin (Sprint 4, conditional)

**Goal**: AST analyzer plugin for `ToolOrchestrator` injection seam.

**Milestone M5**: `FileAnalysis.references` populated for files with imports.

**Cut criteria (§5.3.1)**: If not complete before Phase 6a begins, defer to v2.1. Late placement is the conservative-correct choice — it ships a working gate regardless of plugin outcome (debate §9 convergence). The plugin improves data quality for orphan detection (§5.2.2 dual evidence rule) but is not on the critical path.

| Task | Files | Requirements | Est. LOC |
|------|-------|-------------|----------|
| 5.1 Implement AST plugin for `ToolOrchestrator` | `cli/audit/wiring_analyzer.py` | §5.3, G-008 | 40-50 |
| 5.2 Wire dual evidence rule using plugin output | `cli/audit/wiring_analyzer.py` | §5.2.2 evidence rule | 15-20 |
| 5.3 Unit tests for plugin integration | `tests/audit/` | SC-013, §10.1 (3 tests for ast_analyze_file) | 30-40 |

---

### Phase 6a — Shadow Calibration & Readiness Assessment (Sprint 5+)

**Goal**: Collect shadow data, compute statistical readiness for soft-mode activation.

**Milestone M6a**: Statistical evidence supports or blocks soft-mode activation, documented in a readiness report.

**Rationale for separation from activation**: The debate (D5) established that combining readiness assessment with activation creates incentive to rationalize marginal data. "Are we ready?" and "activate it" are structurally distinct decisions requiring different rigor.

| Task | Description | Requirements |
|------|-------------|-------------|
| 6a.1 Run shadow mode across 2+ release cycles | Collect findings data | §7 Phase 2 criteria |
| 6a.2 Compute FPR, TPR, p95 latency from shadow data | Statistical analysis | §7 Phase 2, SC-008 |
| 6a.3 Run retrospective validation (cli-portify known-bug fixture) | Confirm detection of known defect | SC-009 |
| 6a.4 Characterize alias/re-export noise floor | Determine if signal separable from noise | R6 mitigation |
| 6a.5 Validate `measured_FPR + 2σ < 15%` threshold | Calibration gate | §7 Phase 2 FPR calibration |
| 6a.6 Produce readiness report with explicit recommendation | Shadow → soft, or extend shadow | Decision record |

**Exit criteria for readiness**:
- FPR < 15%, TPR > 50%, p95 < 5s
- Alias noise separable from signal
- Shadow data from ≥2 release cycles
- Readiness report reviewed and signed off

---

### Phase 6b — Activation & Operational Hardening (Post-readiness)

**Goal**: Progress from soft to full enforcement based on measured evidence.

**Milestone M6b**: Enforcement level advanced only on measured operational evidence.

| Task | Description | Requirements |
|------|-------------|-------------|
| 6b.1 Activate soft mode if 6a criteria met | Config change | §7 Phase 2 |
| 6b.2 Monitor soft mode for 5+ sprints | Stability tracking | §7 Phase 3 |
| 6b.3 Validate full-mode criteria: FPR < 5%, TPR > 80% | Statistical gate | §7 Phase 3 |
| 6b.4 Activate full mode if criteria met | Config change | §7 Phase 3 |
| 6b.5 Schedule v2.1 improvements if blocked by alias noise | Import alias pre-pass, re-export chain handling | R6 deferred |

---

## Risk Assessment & Mitigation

### High Severity

| Risk | Impact | Mitigation | Phase |
|------|--------|------------|-------|
| **R1**: False positives from intentional `Optional[Callable]` | Gate blocks legitimate code; undermines trust | Whitelist mechanism (Phase 1); shadow calibration (Phase 6a); alias pre-pass deferred to v2.1 | 1, 6a |
| **R5**: `provider_dir_names` misconfiguration | Orphan analysis scans wrong dirs, produces misleading results | Pre-activation sanity check: >50 files must produce >0 findings (SC-010); integration test; operator-visible config summary in report | 1, 3b |
| **R6**: Re-export aliases cause 30-70% FPR | Shadow data unusable for calibration; blocks soft activation | Document noise floor; v2.1 alias pre-pass; if FPR cannot separate from noise, block Phase 6b activation (§7 Phase 2 FPR calibration) | 6a |

### Medium Severity

| Risk | Impact | Mitigation | Phase |
|------|--------|------------|-------|
| **R3**: Insufficient shadow data | Cannot calibrate for soft mode | Minimum 2-release shadow period; extend if data insufficient; do not compress observation period to meet schedule pressure | 6a |
| **R4**: Sprint performance degradation | Developer experience impact | AST-only analysis; <2s target; <5s hard budget; benchmark tests; short-circuit on excluded/skipped files | 1, 3b |
| **R7**: Agent spec regression | Existing audit functionality breaks via emergent LLM behavioral effects | Strictly additive extensions; no tools changed, no rules removed (§6.1); staged independent validation per agent with regression tests against prior outputs | 4 |
| **R9**: Merge conflicts with concurrent PRs | Integration delays | Sequence: complete Phases 1-2 before touching shared files (`roadmap/gates.py`); coordinate merge window | 3a |

### Low Severity

| Risk | Impact | Mitigation | Phase |
|------|--------|------------|-------|
| **R8**: `resolve_gate_mode()` overrides shadow TRAILING | Shadow mode blocks unexpectedly | Explicit `gate_mode=GateMode.TRAILING` on Step; shadow semantic checks always return True | 2, 3a |
| **R2**: AST parsing failures on complex patterns | Missed findings | Graceful degradation: log, skip, continue; empty `FileAnalysis` returned; Evidence and Limitations section in report | 1 |

---

## Resource Requirements & Dependencies

### Engineering Roles (reference model from Haiku, applicable even for single implementer)

| Role | Responsibility |
|------|---------------|
| Architect/lead | Design decisions, layering enforcement, rollout criteria, cross-subsystem sequencing |
| Backend/Python engineer | AST analyzers, report emitter, pipeline and sprint integrations |
| QA/test engineer | Fixtures, coverage, benchmark tests, rollout validation evidence |
| Audit workflow owner | Review additive agent behavior changes, validate no regression in cleanup-audit flows |

### External Dependencies (no changes required)

- Python `ast`, `re`, `yaml` stdlib modules
- `pipeline/models.py`: `SemanticCheck`, `GateCriteria`, `Step`, `GateMode`
- `pipeline/gates.py`: `gate_passed()`
- `pipeline/trailing_gate.py`: `TrailingGateRunner`, `DeferredRemediationLog`, `resolve_gate_mode()`
- `cli/audit/tool_orchestrator.py`: `ToolOrchestrator`, `FileAnalysis`

### Internal Dependencies (modifications required)

- `roadmap/executor.py`: `_build_steps()`, `_get_all_step_ids()`, `roadmap_run_step()`
- `roadmap/gates.py`: `ALL_GATES`
- `roadmap/prompts.py`: new prompt builder
- `sprint/executor.py`: post-task hook
- `sprint/models.py`: `SprintConfig` field addition
- 5 audit agent behavioral specs

### New Files

| File | Purpose |
|------|---------|
| `src/superclaude/cli/audit/wiring_gate.py` | Core analysis + gate definition + report emitter (280-320 LOC) |
| `src/superclaude/cli/audit/wiring_config.py` | Config, patterns, whitelist (50-70 LOC) |
| `src/superclaude/cli/audit/wiring_analyzer.py` | AST analyzer plugin for ToolOrchestrator (140-180 LOC) |
| `src/superclaude/cli/audit/wiring_whitelist.yaml` | Optional suppression config |
| `tests/audit/test_wiring_gate.py` | Unit tests (240-300 LOC) |
| `tests/audit/test_wiring_analyzer.py` | AST analyzer tests (80-100 LOC) |
| `tests/audit/test_wiring_integration.py` | Integration tests (50-80 LOC) |
| `tests/audit/fixtures/` | Python test fixtures (50-80 LOC) |

### Merge Coordination

- `roadmap/gates.py` is a shared modification point with concurrent PRs
- **Required sequence**: Phases 1-2 (no shared files) → coordinate merge window → Phase 3a (shared files)

---

## Success Criteria & Validation Approach

### Automated Validation (CI-enforceable)

| Criterion | Test Type | Pass Condition |
|-----------|-----------|----------------|
| SC-001–003 | Unit | Each analyzer detects ≥1 finding from known fixture |
| SC-004 | Unit | `gate_passed(report_path, WIRING_GATE)` returns `(True, None)` |
| SC-005 | Integration | Unmodified `gate_passed()` processes WIRING_GATE |
| SC-006 | Integration | Sprint task status unchanged with shadow findings |
| SC-007 | Unit | `whitelist_entries_applied > 0` when whitelist matches |
| SC-008 | Benchmark | < 5s for 50 Python files |
| SC-014 | Unit | Shadow passes; full blocks on findings |
| §10.3 | Coverage | ≥ 90% on `wiring_gate.py` + `wiring_analyzer.py` |
| §10.1/§10.2 | Count | ≥ 20 unit + 3 integration tests |
| §3.1 | Static | No signature changes to pipeline substrate (grep verification) |
| NFR-007 (§3.2) | Static | No `pipeline/*` imports from `roadmap/*`, `audit/*`, `sprint/*` |

### Manual / Observational Validation

| Criterion | Method |
|-----------|--------|
| SC-009 | Retrospective: run analyzer on cli-portify executor, confirm `step_runner` detected |
| SC-010 | Run with misconfigured `provider_dir_names`, verify WARNING emitted |
| SC-011–012 | Run audit pipeline on test repo, inspect agent output for 9-field profiles with Wiring path |
| SC-013 | Conditional on Phase 5 completion |

### Exit Criteria by Rollout Stage

| Stage | Criteria |
|-------|----------|
| **Shadow ready** | All core functional tests green; gate-valid report emitted; benchmark target met; roadmap and sprint integration stable |
| **Soft ready** | FPR < 15%; TPR > 50%; p95 < 5s; shadow data from ≥2 releases; alias noise separable from signal |
| **Full ready** | FPR < 5%; TPR > 80%; whitelist stable for 5+ sprints; no material audit regressions |

---

## Timeline Estimates

| Phase | Sprint | Duration | Dependencies | Parallelizable |
|-------|--------|----------|-------------|----------------|
| **0 — Decision Checkpoint** | Pre-Sprint 1 | 2-4 hours | None | — |
| **1 — Core Engine** | Sprint 1 | 3-4 days | Phase 0 | — |
| **2 — Report & Gate** | Sprint 2 | 2-3 days | Phase 1 | — |
| **3a — Roadmap Integration** | Sprint 3 | 1.5-2 days | Phase 2 | Yes, with Phase 4 |
| **3b — Sprint Integration** | Sprint 3 | 1-1.5 days | Phase 3a validated | After 3a |
| **4 — Agent Extensions** | Sprint 3-4 | 2 days | Phase 1 (for context) | Yes, with Phase 3a |
| **5 — ToolOrchestrator Plugin** | Sprint 4 | 1-2 days | Phase 1 | Cut if late |
| **6a — Shadow Calibration** | Sprint 5+ | 2+ release cycles | Phase 3b | Ongoing |
| **6b — Activation** | Post-6a | Metrics-gated | Phase 6a criteria met | — |

**Total implementation time**: ~13-17 days of active development across 4 sprints.
**Total to soft-mode activation**: 2+ release cycles after shadow deployment.
**Total to full enforcement**: 5+ sprints of stable soft-mode operation after soft activation.

### Dependency Graph

```
Phase 0 ──→ Phase 1 ──→ Phase 2 ──→ Phase 3a ──→ Phase 3b ──→ Phase 6a ──→ Phase 6b
                │                       ↑ (parallel)
                │                    Phase 4
                │
                └──→ Phase 5 (conditional, cut if late)
```
