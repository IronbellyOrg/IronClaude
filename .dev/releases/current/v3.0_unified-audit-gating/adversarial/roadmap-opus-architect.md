---
spec_source: .dev/releases/current/v3.0_unified-audit-gating/adversarial/merged-spec.md
complexity_score: 0.82
primary_persona: architect
---

# Wiring Verification Gate v3.0 — Project Roadmap

## 1. Executive Summary

This roadmap delivers a deterministic AST-based wiring verification gate that detects unwired callable injections, orphan modules, and broken dispatch registries across the SuperClaude pipeline infrastructure. The system operates as a consumer of the existing gate substrate (`SemanticCheck`, `GateCriteria`, `gate_passed()`) with zero modifications to upstream interfaces.

**Scope**: 7 new files, 7 modified files, 5 agent behavioral extensions. ~500 lines production code, ~400 lines test code.

**Key architectural decision**: The wiring step is a deterministic Python analysis (not LLM synthesis), special-cased in the roadmap executor. This ensures reproducibility, enables pipeline resume, and keeps execution under 5 seconds.

**Rollout strategy**: Three-phase promotion — shadow → soft → full — with quantitative promotion gates (FPR/TPR thresholds) preventing premature enforcement.

---

## 2. Phased Implementation Plan

### Phase 1: Core Analysis Engine (Tasks T01–T04)

**Objective**: Build the deterministic wiring analysis and report emission layer. No pipeline integration yet.

| Task | Description | Files | Dependencies |
|------|-------------|-------|-------------|
| T01 | `WiringConfig` dataclass + whitelist loader | `audit/wiring_config.py` (CREATE) | None |
| T02 | `WiringFinding` + `WiringReport` dataclasses | `audit/wiring_gate.py` (CREATE) | T01 |
| T03 | Core analysis: `run_wiring_analysis()` — AST parsing, callable detection, orphan detection, registry detection | `audit/wiring_gate.py` (EXTEND) | T01, T02 |
| T04 | `emit_report()` — YAML frontmatter + Markdown report generation with `yaml.safe_dump()` | `audit/wiring_gate.py` (EXTEND) | T02, T03 |

**Milestone M1**: `run_wiring_analysis()` returns correct `WiringReport` for test fixtures. `emit_report()` produces valid YAML+Markdown.

**Parallelism**: T01 and T02 can proceed concurrently (Wave 1). T03 and T04 are sequential on T02.

### Phase 2: Gate Definition + Semantic Checks (Tasks T05–T06)

**Objective**: Wire the analysis into the gate substrate via `WIRING_GATE` and implement all 5 semantic checks.

| Task | Description | Files | Dependencies |
|------|-------------|-------|-------------|
| T05 | `WIRING_GATE` constant + 5 semantic check functions + `_extract_frontmatter_values()` helper | `audit/wiring_gate.py` (EXTEND) | T04 |
| T06 | `ast_analyze_file()` ToolOrchestrator plugin (CUT-ELIGIBLE: defer to v3.1 if not complete before T08) | `audit/wiring_analyzer.py` (CREATE) | T03 |

**Milestone M2**: `gate_passed(report_path, WIRING_GATE)` returns correct `(bool, str|None)` for valid and invalid reports. All 5 semantic checks pass independently.

**Critical constraint**: Semantic check functions must be pure `Callable[[str], bool]` — no I/O, no side effects.

### Phase 3: Pipeline Integration (Tasks T07–T09)

**Objective**: Integrate into roadmap pipeline and sprint executor. Deploy in shadow mode.

| Task | Description | Files | Dependencies |
|------|-------------|-------|-------------|
| T07 | Add `WIRING_GATE` to `ALL_GATES` + `build_wiring_verification_prompt()` stub | `roadmap/gates.py` (MODIFY), `roadmap/prompts.py` (MODIFY) | T05 |
| T08 | Add wiring-verification as Step 9 in `_build_steps()` + special-case in `roadmap_run_step()` + update `_get_all_step_ids()` | `roadmap/executor.py` (MODIFY) | T05, T07 |
| T09 | Add `wiring_gate_mode` to `SprintConfig` + post-task analysis hook | `sprint/executor.py` (MODIFY), `sprint/models.py` (MODIFY) | T03, T05 |

**Milestone M3**: Full roadmap pipeline completes with wiring-verification step in shadow mode (TRAILING). Sprint executor logs wiring findings without affecting task status.

**Critical path**: T08 is the highest-risk task — touches the roadmap executor hot path and must handle deterministic-step special-casing correctly.

### Phase 4: Agent Extensions (Tasks T10–T12)

**Objective**: Extend cleanup-audit agents with wiring-aware capabilities. Additive-only changes.

| Task | Description | Files | Dependencies |
|------|-------------|-------|-------------|
| T10 | Extend audit-scanner with `REVIEW:wiring` classification signal | Agent behavioral rules (MODIFY) | T03 |
| T11 | Extend audit-analyzer with 9th mandatory field "Wiring path" | Agent behavioral rules (MODIFY) | T10 |
| T12 | Extend audit-validator with Check 5: Wiring Claim Verification | Agent behavioral rules (MODIFY) | T11 |

**Milestone M4**: Cleanup-audit produces wiring-aware profiles. No existing agent rules removed or tools changed.

### Phase 5: Testing + Validation (Tasks T13–T15)

**Objective**: Achieve ≥90% coverage on core modules, validate all 14 success criteria.

| Task | Description | Dependencies |
|------|-------------|-------------|
| T13 | Unit tests: 20+ tests covering all detection types, semantic checks, whitelist, mode-aware enforcement, edge cases (AST parse failures, empty dirs) | T01–T05 |
| T14 | Integration tests: 3+ tests — full pipeline run with shadow gate, sprint post-task hook, gate_passed() with WIRING_GATE | T07–T09 |
| T15 | Pre-activation checklist: sanity check (>50 files → >0 findings), `provider_dir_names` validation | T03, T08 |

**Milestone M5**: 90% coverage on `wiring_gate.py` and `wiring_analyzer.py`. All SC-001 through SC-014 pass. Pre-activation checklist green.

**Parallelism**: T13 can start as soon as Phase 1 completes. T14 requires Phase 3.

### Phase 6: Shadow Deployment + Calibration (Post-implementation)

**Objective**: Collect shadow data for FPR/TPR calibration. No enforcement.

| Activity | Threshold | Duration |
|----------|-----------|----------|
| Shadow data collection | Minimum 2 releases | Ongoing |
| FPR measurement | Baseline established | After shadow window |
| Soft promotion decision | FPR < 15%, TPR > 50%, p95 < 5s | After shadow window |
| Full promotion decision | FPR < 5%, TPR > 80%, whitelist stable 5+ sprints | After soft window |

---

## 3. Risk Assessment and Mitigation

### High Priority

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **RISK-005**: `provider_dir_names` misconfiguration → missed/false findings | HIGH | Pre-activation sanity check: >50 files must produce >0 findings. Rollback if zero findings on known-unwired codebase. Resolve Open Question #1 before T01. |
| **RISK-001**: False positives from intentional `Optional[Callable]` hooks | MEDIUM | Whitelist mechanism in T01. Shadow calibration before any enforcement. |
| **RISK-006**: Import re-export aliases → 30-70% FPR | MEDIUM | Document as known limitation. Measure FPR noise floor during shadow. Alias pre-pass deferred to v3.1. Shadow mode acceptable with high FPR — it's observational only. |

### Medium Priority

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **RISK-007**: Agent behavioral extension regression | MEDIUM | Additive-only changes (NFR-016). No existing rules removed. Test with existing audit fixtures before merging. |
| **RISK-003**: Insufficient shadow data for calibration | MEDIUM | Enforce minimum 2-release shadow period. Do not shortcut promotion. |
| **RISK-004**: Sprint performance impact | LOW | AST-only analysis, no subprocesses. NFR-002 target: < 2s. Benchmark in T13. |

### Low Priority

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **RISK-002**: AST parse errors on complex patterns | LOW | Graceful degradation — log, skip, count in `files_skipped`. |
| **RISK-008**: `resolve_gate_mode()` overrides shadow intent | LOW | Explicit `gate_mode=GateMode.TRAILING` on Step construction. |

### Architectural Risk: Merge Coordination (Open Question #5)

The `roadmap/gates.py` modification overlaps with Anti-Instincts (v3.1) and other v3.x branches. **Recommendation**: Sequence v3.0 merge first — it touches fewer lines in `gates.py` (one import + one list append). Rebase v3.1 after v3.0 lands on integration.

---

## 4. Resource Requirements and Dependencies

### Internal Dependencies (Must Exist, No Changes)

All 14 dependencies (DEP-001 through DEP-014) are existing symbols. The spec has verified line-number references. Key risk: if any upstream refactoring moves these symbols before v3.0 merges, imports will break.

**Mitigation**: Pin to current `integration` branch state. Run import verification as part of T15.

### Open Questions Requiring Resolution Before Implementation

| Priority | Question | Blocks | Recommended Resolution |
|----------|----------|--------|----------------------|
| **P0** | #1: Definitive `provider_dir_names` set | T01 | Audit actual directory names in codebase; default to `{"steps", "handlers", "validators", "checks"}` with config override |
| **P0** | #7: Does `ToolOrchestrator.__init__()` accept `analyzer` param? | T06 | Inspect `audit/tool_orchestrator.py` before T06. If seam doesn't exist, T06 becomes a v3.1 deferral (already marked CUT-ELIGIBLE) |
| **P1** | #5: Merge conflict coordination with v3.x branches | T07–T08 | Merge v3.0 first, rebase others |
| **P1** | #6: 30-70% FPR acceptable for shadow? | Phase 6 | Yes — shadow is observational. Measure and document. |
| **P2** | #2–4, #8–10 | Phase 6 | Resolve during shadow calibration with real data |

### Compute/Tooling Requirements

- Python `ast` module (stdlib — no external dependencies)
- `yaml.safe_dump()` for frontmatter emission (PyYAML already in dependency tree)
- Test fixtures: 50-80 LOC each (NFR-012), synthetic Python files with known wiring patterns

---

## 5. Success Criteria and Validation Approach

### Automated Validation (CI-Enforceable)

| Criterion | Test Type | Phase |
|-----------|----------|-------|
| SC-001: Detect `Optional[Callable]=None` never provided | Unit | Phase 5 |
| SC-002: Detect orphan modules | Unit | Phase 5 |
| SC-003: Detect unresolvable registry entries | Unit | Phase 5 |
| SC-004: Report conforms to `GateCriteria` | Unit | Phase 5 |
| SC-005: `gate_passed()` evaluates `WIRING_GATE` unmodified | Integration | Phase 5 |
| SC-007: Whitelist exclusion + suppression count | Unit | Phase 5 |
| SC-008: < 5s for 50 files | Benchmark | Phase 5 |
| SC-013: ToolOrchestrator AST plugin populates references | Unit | Phase 5 (if T06 not cut) |
| SC-014: Mode-aware enforcement correctness | Unit | Phase 5 |

### Manual/Observational Validation

| Criterion | Method | Phase |
|-----------|--------|-------|
| SC-006: Shadow mode doesn't affect task status | Integration test + manual sprint run | Phase 5–6 |
| SC-009: Catches cli-portify executor no-op bug | Retrospective on known fixtures | Phase 5 |
| SC-010: Pre-activation zero-match warning | Integration test | Phase 5 |
| SC-011: audit-scanner `REVIEW:wiring` | Agent test with audit fixtures | Phase 5 |
| SC-012: audit-analyzer 9-field profile | Agent test | Phase 5 |

### Coverage Gate

- `wiring_gate.py`: ≥ 90% line coverage
- `wiring_analyzer.py`: ≥ 90% line coverage (if T06 not cut)
- Minimum 20 unit tests + 3 integration tests

---

## 6. Timeline Estimates

| Phase | Tasks | Estimated Effort | Cumulative |
|-------|-------|-----------------|-----------|
| Phase 1: Core Analysis | T01–T04 | 2–3 sessions | 2–3 sessions |
| Phase 2: Gate Definition | T05–T06 | 1–2 sessions | 3–5 sessions |
| Phase 3: Pipeline Integration | T07–T09 | 2–3 sessions | 5–8 sessions |
| Phase 4: Agent Extensions | T10–T12 | 1–2 sessions | 6–10 sessions |
| Phase 5: Testing | T13–T15 | 2–3 sessions | 8–13 sessions |
| Phase 6: Shadow Calibration | Observational | 2+ release cycles | Ongoing |

**Critical path**: T01 → T02 → T03 → T05 → T08 (core analysis → gate definition → pipeline integration)

**Parallelizable work**:
- T01 ∥ T02 (config and data models are independent)
- T06 ∥ T07 (ToolOrchestrator plugin and gates.py modification are independent)
- T10–T12 ∥ T13 (agent extensions and unit tests are independent)
- T13 starts after Phase 1, runs alongside Phases 2–4

### Cut Decisions

- **T06 (ToolOrchestrator AST plugin)**: CUT-ELIGIBLE. Defer to v3.1 if not complete before T08 begins. Core wiring analysis does not depend on it.
- **Phase 4 (Agent Extensions)**: Can be deferred to a follow-up PR if scope pressure demands it. Wiring gate functions independently of agent awareness.

---

## 7. Architectural Recommendations

1. **Implement T01–T04 as a self-contained module first**. The analysis engine should be fully testable in isolation before any pipeline wiring. This de-risks Phase 3 significantly.

2. **Resolve Open Question #7 early**. Inspect `ToolOrchestrator.__init__()` before planning T06. If the `analyzer` injection seam doesn't exist, cut T06 immediately — it's already CUT-ELIGIBLE and deferring it simplifies the release.

3. **Frontmatter regex duplication is intentional**. Do not refactor `_FRONTMATTER_RE` into a shared module. The duplication preserves the layering constraint (NFR-007) and is explicitly called out in Section 5.5.

4. **Shadow mode is the primary deliverable**. The wiring gate in shadow/TRAILING mode is the v3.0 ship requirement. Soft and full enforcement are promotion decisions made after shadow calibration — they are not implementation tasks for this release.

5. **Sequence the v3.0 merge before v3.1 (Anti-Instincts)**. v3.0 touches `roadmap/gates.py` minimally (one import, one list append). Landing it first gives v3.1 a clean rebase target.
