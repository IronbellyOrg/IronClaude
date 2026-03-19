---
spec_source: merged-spec.md
complexity_score: 0.78
primary_persona: architect
---

# Unified Audit Gating — Wiring Verification Roadmap

## 1. Executive Summary

This roadmap delivers a **static wiring verification gate** for the SuperClaude pipeline that detects three classes of integration defects — unwired injectable callables, orphan modules, and broken dispatch registries — using deterministic AST analysis. The system integrates into the roadmap pipeline as a post-merge step, extends the sprint executor with a mode-aware hook, and enriches the cleanup-audit agent suite with wiring-aware behavioral rules.

**Key architectural constraint**: Zero modifications to the `pipeline/*` substrate. All new code consumes existing contracts (`GateCriteria`, `SemanticCheck`, `Step`, `GateMode`) without altering them.

**Rollout strategy**: Three-phase shadow → soft → full enforcement with statistical FPR calibration gates between phases.

**Scope**: ~52 requirements, ~500 LOC production code, ~400 LOC test code, touching 3 subsystems (roadmap, sprint, audit) plus 5 agent specs.

---

## 2. Phased Implementation Plan

### Phase 1 — Core Analysis Engine (Sprint 1)

**Goal**: Standalone wiring analyzer producing structured findings, no pipeline integration yet.

**Milestone**: `run_wiring_analysis()` returns correct `WiringReport` for all three detection types against test fixtures.

| Task | Files | Requirements | Est. LOC |
|------|-------|-------------|----------|
| 1.1 Define `WiringFinding`, `WiringReport`, `WiringConfig` dataclasses | `audit/wiring_gate.py` | FR-009, FR-010, FR-011 | 60-80 |
| 1.2 Implement unwired callable analysis | `audit/wiring_analyzer.py` | FR-012, FR-014 | 80-100 |
| 1.3 Implement orphan module analysis | `audit/wiring_analyzer.py` | FR-015, FR-016, FR-017 | 70-90 |
| 1.4 Implement registry analysis | `audit/wiring_analyzer.py` | FR-018, FR-019 | 60-80 |
| 1.5 Implement whitelist loading + suppression | `audit/wiring_analyzer.py` | FR-013 | 30-40 |
| 1.6 Implement `ast_analyze_file()` utility | `audit/wiring_analyzer.py` | FR-020, FR-021 | 40-50 |
| 1.7 Unit tests for all three analyzers + whitelist | `tests/audit/` | NFR-003, NFR-004, SC-001–SC-003, SC-007 | 200-250 |

**Validation checkpoint**:
- All 3 detection types produce correct findings against known fixtures
- Whitelist suppression works; `SyntaxError` handled gracefully
- Performance: < 2s for 50-file fixture (NFR-001)

---

### Phase 2 — Report Emission & Gate Definition (Sprint 2)

**Goal**: Structured YAML+Markdown report that passes `gate_passed()` validation. Gate criteria defined but not yet wired into pipeline.

**Milestone**: `gate_passed(WIRING_GATE, report_content)` returns `True` for well-formed shadow-mode reports.

| Task | Files | Requirements | Est. LOC |
|------|-------|-------------|----------|
| 2.1 Implement report emitter (frontmatter + 7 Markdown sections) | `audit/wiring_gate.py` | FR-004, FR-022, FR-023, NFR-005 | 80-100 |
| 2.2 Implement `_extract_frontmatter_values()` helper | `audit/wiring_gate.py` | FR-024 | 15 |
| 2.3 Define `WIRING_GATE` as `GateCriteria` | `audit/wiring_gate.py` | FR-025 | 20-30 |
| 2.4 Implement 5 semantic check functions | `audit/wiring_gate.py` | FR-026, FR-027, FR-028 | 40-50 |
| 2.5 Implement `blocking_for_mode()` logic | `audit/wiring_gate.py` | FR-010, FR-028 | 15-20 |
| 2.6 Unit tests for report + gate + semantic checks | `tests/audit/` | SC-004, SC-014, NFR-003 | 100-130 |

**Validation checkpoint**:
- Report frontmatter contains all 17 required fields
- `gate_passed()` (unmodified) correctly evaluates `WIRING_GATE`
- Mode-aware semantics: shadow always passes; soft blocks on critical; full blocks on critical+major
- 90% coverage on `wiring_gate.py` and `wiring_analyzer.py`

---

### Phase 3 — Pipeline Integration (Sprint 3)

**Goal**: Wiring verification runs as a pipeline step in shadow mode. Sprint hook active.

**Milestone**: End-to-end roadmap pipeline executes wiring-verification step and emits report without blocking.

| Task | Files | Requirements | Est. LOC |
|------|-------|-------------|----------|
| 3.1 Add `build_wiring_verification_prompt()` stub | `roadmap/prompts.py` | FR-029 | 5 |
| 3.2 Add wiring-verification `Step` to `_build_steps()` | `roadmap/executor.py` | FR-030, FR-032 | 15-20 |
| 3.3 Special-case executor for wiring-verification step | `roadmap/executor.py` | FR-031, NFR-011 | 20-30 |
| 3.4 Register `WIRING_GATE` in `ALL_GATES` | `roadmap/gates.py` | FR-033 | 3 |
| 3.5 Add `wiring_gate_mode` to `SprintConfig` | `sprint/models.py` | FR-034 | 5 |
| 3.6 Implement sprint post-task wiring hook | `sprint/executor.py` | FR-035 | 30-40 |
| 3.7 Integration tests (pipeline + sprint) | `tests/integration/` | SC-005, SC-006, NFR-004 | 70-100 |

**Validation checkpoint**:
- `_get_all_step_ids()` returns wiring-verification between spec-fidelity and remediate
- Pipeline runs end-to-end with shadow gate (no blocking)
- Sprint hook logs findings without affecting task status
- No imports from `pipeline/*` into `roadmap/*` or `audit/*` violating layering (NFR-007)

---

### Phase 4 — Audit Agent Extensions (Sprint 3-4, parallelizable with Phase 3)

**Goal**: Cleanup-audit agents enriched with wiring-aware rules.

**Milestone**: Audit pipeline produces wiring path information in analyzer profiles and validates wiring claims.

| Task | Files | Requirements | Est. LOC |
|------|-------|-------------|----------|
| 4.1 Extend audit-scanner with `REVIEW:wiring` signal | `agents/audit-scanner.md` | FR-036, SC-011 | Behavioral spec |
| 4.2 Extend audit-analyzer with 9th field + finding types | `agents/audit-analyzer.md` | FR-037, SC-012 | Behavioral spec |
| 4.3 Extend audit-validator with Check 5 | `agents/audit-validator.md` | FR-038 | Behavioral spec |
| 4.4 Extend audit-comparator with cross-file wiring check | `agents/audit-comparator.md` | FR-007 | Behavioral spec |
| 4.5 Extend audit-consolidator with Wiring Health section | `agents/audit-consolidator.md` | FR-007 | Behavioral spec |
| 4.6 Agent integration tests | `tests/audit/` | SC-011, SC-012, NFR-013 | Behavioral validation |

**Validation checkpoint**:
- All extensions are strictly additive (NFR-013)
- Scanner classifies wiring-indicator files correctly
- Analyzer produces complete 9-field profiles with Wiring path
- Validator catches DELETE recommendations on files with live wiring

---

### Phase 5 — ToolOrchestrator Plugin (Sprint 4, conditional)

**Goal**: AST analyzer plugin for `ToolOrchestrator` injection seam.

**Milestone**: `FileAnalysis.references` populated for files with imports.

**Cut criteria (NFR-012)**: If not complete before Sprint 5 (Phase 6) begins, defer to v2.1.

| Task | Files | Requirements | Est. LOC |
|------|-------|-------------|----------|
| 5.1 Implement AST plugin for `ToolOrchestrator` | `audit/wiring_analyzer.py` | FR-008, FR-020 | 40-50 |
| 5.2 Wire dual evidence rule using plugin output | `audit/wiring_analyzer.py` | FR-017 | 15-20 |
| 5.3 Unit tests for plugin integration | `tests/audit/` | SC-013 | 30-40 |

---

### Phase 6 — Shadow Calibration & Rollout Preparation (Sprint 5+)

**Goal**: Collect shadow data, calibrate FPR/TPR, prepare soft-mode activation.

**Milestone**: Statistical evidence supports Phase 2 (soft mode) activation criteria.

| Task | Description | Requirements |
|------|-------------|-------------|
| 6.1 Run shadow mode across 2+ release cycles | Collect findings data | NFR-008 |
| 6.2 Compute FPR, TPR, p95 latency from shadow data | Statistical analysis | NFR-008, NFR-014 |
| 6.3 Validate `measured_FPR + 2σ < 15%` threshold | Calibration gate | NFR-014 |
| 6.4 Activate soft mode if criteria met | Config change | NFR-008 |
| 6.5 Monitor soft mode for 5+ sprints | Stability tracking | NFR-009 |
| 6.6 Activate full mode if criteria met | Config change | NFR-009 |

---

## 3. Risk Assessment & Mitigation

| Risk | Severity | Impact | Mitigation | Phase Affected |
|------|----------|--------|------------|----------------|
| **R1**: False positives from intentional `Optional[Callable]` | HIGH | Gate blocks legitimate code | Whitelist mechanism (Phase 1); shadow calibration (Phase 6); alias pre-pass deferred to v2.1 | 1, 6 |
| **R5**: `provider_dir_names` misconfiguration | HIGH | Orphan analysis scans wrong dirs | Pre-activation sanity check: >50 files must produce >0 findings (SC-010); integration test | 1, 3 |
| **R6**: Re-export aliases cause 30-70% FPR | HIGH | Shadow data unusable for calibration | Document noise floor; v2.1 alias pre-pass; if FPR cannot separate from noise, block Phase 2 activation (NFR-014) | 6 |
| **R3**: Insufficient shadow data | MEDIUM | Cannot calibrate for soft mode | Minimum 2-release shadow period; extend if data insufficient | 6 |
| **R4**: Sprint performance degradation | MEDIUM | Developer experience impact | AST-only analysis; <2s target; <5s hard budget; benchmark tests | 1, 3 |
| **R7**: Agent spec regression | MEDIUM | Existing audit functionality breaks | Strictly additive extensions; no tools changed, no rules removed (NFR-013) | 4 |
| **R8**: `resolve_gate_mode()` overrides shadow TRAILING | LOW | Shadow mode blocks unexpectedly | Explicit `gate_mode=GateMode.TRAILING` on Step; shadow semantic checks always return True | 2, 3 |
| **R2**: AST parsing failures on complex patterns | LOW | Missed findings | Graceful degradation: log, skip, continue; empty `FileAnalysis` returned | 1 |
| **R9** (new): Merge conflicts with concurrent PRs | MEDIUM | Integration delays | Sequence: complete Phase 1-2 before touching shared files (`roadmap/gates.py`); coordinate with Anti-Instincts PR | 3 |

---

## 4. Resource Requirements & Dependencies

### External Dependencies (no changes required)
- Python `ast`, `re`, `yaml` stdlib modules
- `pipeline/models.py`: `SemanticCheck`, `GateCriteria`, `Step`, `GateMode`
- `pipeline/gates.py`: `gate_passed()`
- `pipeline/trailing_gate.py`: `TrailingGateRunner`, `DeferredRemediationLog`, `resolve_gate_mode()`
- `audit/tool_orchestrator.py`: `ToolOrchestrator`, `FileAnalysis`

### Internal Dependencies (modifications required)
- `roadmap/executor.py`: `_build_steps()`, `_get_all_step_ids()`, `roadmap_run_step()`
- `roadmap/gates.py`: `ALL_GATES`
- `roadmap/prompts.py`: new prompt builder
- `sprint/executor.py`: post-task hook
- `sprint/models.py`: `SprintConfig` field addition
- 5 audit agent behavioral specs

### New Files
- `src/superclaude/audit/wiring_gate.py` — gate criteria, report emitter, frontmatter helper
- `src/superclaude/audit/wiring_analyzer.py` — three analysis algorithms, AST utility, whitelist
- `wiring_whitelist.yaml` — optional suppression config
- `tests/audit/test_wiring_analyzer.py`
- `tests/audit/test_wiring_gate.py`
- `tests/integration/test_wiring_pipeline.py`

### Merge Coordination
- `roadmap/gates.py` is a shared modification point with Anti-Instincts and Unified Audit Gating PRs
- **Recommended sequence**: Phase 1-2 (no shared files) → coordinate merge window → Phase 3 (shared files)

---

## 5. Success Criteria & Validation Approach

### Automated Validation (CI-enforceable)

| Criterion | Test Type | Pass Condition |
|-----------|-----------|----------------|
| SC-001–003 | Unit | Each analyzer detects ≥1 finding from known fixture |
| SC-004 | Unit | `gate_passed(WIRING_GATE, report)` returns True |
| SC-005 | Integration | Unmodified `gate_passed()` processes WIRING_GATE |
| SC-006 | Integration | Sprint task status unchanged with shadow findings |
| SC-007 | Unit | `whitelist_entries_applied > 0` when whitelist matches |
| SC-008 | Benchmark | < 5s for 50 Python files |
| SC-014 | Unit | Shadow passes; full blocks on findings |
| NFR-003 | Coverage | ≥ 90% on `wiring_gate.py` + `wiring_analyzer.py` |
| NFR-004 | Count | ≥ 20 unit + 3 integration tests |
| NFR-006 | Static | No signature changes to pipeline substrate (grep verification) |
| NFR-007 | Static | No `pipeline/*` imports from `roadmap/*`, `audit/*`, `sprint/*` |

### Manual / Observational Validation

| Criterion | Method |
|-----------|--------|
| SC-009 | Retrospective: run analyzer on cli-portify executor, confirm `step_runner` detected |
| SC-010 | Run with misconfigured `provider_dir_names`, verify WARNING emitted |
| SC-011–012 | Run audit pipeline on test repo, inspect agent output |
| SC-013 | Conditional on Phase 5 completion |

---

## 6. Timeline Estimates

| Phase | Sprint | Duration | Dependencies | Parallelizable |
|-------|--------|----------|-------------|----------------|
| **1 — Core Engine** | Sprint 1 | 3-4 days | None | — |
| **2 — Report & Gate** | Sprint 2 | 2-3 days | Phase 1 | — |
| **3 — Pipeline Integration** | Sprint 3 | 2-3 days | Phase 2 | Yes, with Phase 4 |
| **4 — Agent Extensions** | Sprint 3-4 | 2 days | Phase 1 (for context) | Yes, with Phase 3 |
| **5 — ToolOrchestrator Plugin** | Sprint 4 | 1-2 days | Phase 1 | Cut if late |
| **6 — Shadow Calibration** | Sprint 5+ | 2+ release cycles | Phase 3 | Ongoing |

**Total implementation time**: ~12-16 days of active development across 4 sprints.
**Total to soft-mode activation**: 2+ release cycles after shadow deployment.
**Total to full enforcement**: 5+ sprints of stable soft-mode operation after soft activation.

---

## 7. Open Questions Requiring Resolution Before Implementation

These must be resolved before or during Phase 1-2 to avoid rework:

1. **OQ-1** (blocks Phase 2): How are `audit_artifacts_used` located and counted at runtime? Propose: glob for `*-audit-report.yaml` in output dir, count matched files.
2. **OQ-2** (blocks Phase 1): Are `exclude_patterns` matches counted in `files_skipped`? Propose: yes, to provide visibility.
3. **OQ-3** (blocks Phase 6): Is whitelist strictness derived from `rollout_mode`? Propose: `shadow` → WARNING, `soft`/`full` → `WiringConfigError`.
4. **OQ-4** (blocks Phase 3): Does `SprintConfig.source_dir` already exist? Verify before implementation.
5. **OQ-9** (blocks Phase 3): Merge sequencing with concurrent PRs — establish coordination plan.
