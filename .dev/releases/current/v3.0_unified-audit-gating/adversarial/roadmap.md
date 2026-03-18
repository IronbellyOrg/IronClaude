---
spec_source: .dev/releases/current/v3.0_unified-audit-gating/adversarial/merged-spec.md
complexity_score: 0.82
adversarial: true
---

# Wiring Verification Gate v3.0 — Merged Project Roadmap

## Executive Summary

This roadmap delivers a deterministic AST-based wiring verification gate that detects unwired callable injections, orphan modules, and broken dispatch registries across the SuperClaude pipeline infrastructure. The system operates as a consumer of the existing gate substrate (`SemanticCheck`, `GateCriteria`, `gate_passed()`) with zero modifications to upstream interfaces.

**Scope**: 7 new files, 7 modified files, 5 agent behavioral extensions. ~500 lines production code, ~400 lines test code.

**Key architectural decision**: The wiring step is a deterministic Python analysis (not LLM synthesis), special-cased in the roadmap executor. This ensures reproducibility, enables pipeline resume, and keeps execution under 5 seconds.

**Rollout strategy**: Three-phase promotion — shadow → soft → full — with quantitative promotion gates (FPR/TPR thresholds) preventing premature enforcement. Shadow mode is the primary v3.0 deliverable. Soft and full enforcement are promotion decisions made after shadow calibration — they are not implementation tasks for this release.

**Architectural priorities**:
1. Stable architecture first — preserve substrate signatures and import boundaries.
2. Deterministic deployability — build the analyzer as pure Python with reproducible output.
3. Calibration before enforcement — use measured false-positive/true-positive data before soft/full promotion.
4. Testing and observability throughout — ≥90% coverage on core modules.

**Public API contract**:
- `run_wiring_analysis(target_dir, config?) -> WiringReport`
- `emit_report(report, output_path, enforcement_mode)`
- `ast_analyze_file(file_path, content) -> FileAnalysis`

---

## Phased Implementation Plan

### Phase 0: Architecture Confirmation

**Objective**: Confirm architectural seams and resolve blocking open questions before committing to file layouts and API shapes. Timeboxed to 0.5–1 session maximum. Does not delay Phase 1 if answers are immediately available.

**Confirmation checklist**:
1. Verify `ToolOrchestrator.__init__()` analyzer injection seam — determines whether T06 proceeds or is cut.
2. Confirm definitive `provider_dir_names` defaults by auditing actual directory names in the codebase.
3. Confirm current roadmap step ordering around `spec-fidelity` and `remediate`.
4. Confirm sprint enforcement control points and `SprintGatePolicy` interaction.
5. Assign whitelist governance owner and promotion review owner.

**Exit criteria**:
- M0.1: All 5 confirmation items resolved or assigned to owners with deadlines.
- M0.2: `provider_dir_names` default set confirmed (recommended: `{"steps", "handlers", "validators", "checks"}` with config override).
- M0.3: T06 go/no-go decision made based on `ToolOrchestrator` seam inspection.

### Phase 1: Core Analysis Engine (T01–T04)

**Objective**: Build the deterministic wiring analysis and report emission layer. No pipeline integration yet.

| Task | Description | Files | Dependencies |
|------|-------------|-------|-------------|
| T01 | `WiringConfig` dataclass + whitelist loader with strict validation | `audit/wiring_config.py` (CREATE) | Phase 0 |
| T02 | `WiringFinding` + `WiringReport` dataclasses with derived `total_findings` and `blocking_for_mode()` | `audit/wiring_gate.py` (CREATE) | Phase 0 |
| T03 | Core analysis: `run_wiring_analysis()` — AST parsing, callable detection, orphan detection, registry detection, severity classification | `audit/wiring_gate.py` (EXTEND) | T01, T02 |
| T04 | `emit_report()` — YAML frontmatter (15 fields via `yaml.safe_dump()`) + Markdown report with 7 body sections: (1) Summary, (2) Unwired Optional Callable Injections, (3) Orphan Modules/Symbols, (4) Unregistered Dispatch Entries, (5) Suppressions and Dynamic Retention, (6) Recommended Remediation, (7) Evidence and Limitations | `audit/wiring_gate.py` (EXTEND) | T02, T03 |

**Milestone M1**: `run_wiring_analysis()` returns correct `WiringReport` for test fixtures. `emit_report()` produces valid YAML+Markdown with all 7 body sections.

**Parallelism**: T01 ∥ T02 (config and data models are independent). T03 and T04 are sequential on T02.

**Architectural notes**:
- Keep cross-file resolution conservative and explicit; do not attempt speculative alias inference in v3.0.
- Sort all file traversal and emitted findings to guarantee reproducibility.
- Graceful degradation on AST parse errors — log, skip, count in `files_skipped`.

### Phase 2: Gate Definition and Semantic Checks (T05–T06)

**Objective**: Wire the analysis into the gate substrate via `WIRING_GATE` and implement all 5 semantic checks.

| Task | Description | Files | Dependencies |
|------|-------------|-------|-------------|
| T05 | `WIRING_GATE` constant + 5 semantic check functions + `_extract_frontmatter_values()` helper (duplicate `_FRONTMATTER_RE` — intentional layering constraint per NFR-007) | `audit/wiring_gate.py` (EXTEND) | T04 |
| T06 | `ast_analyze_file()` ToolOrchestrator plugin — populates `FileAnalysis.references`, `has_dispatch_registry`, `injectable_callables` (CUT-ELIGIBLE: defer to v3.1 if Phase 0 reveals no analyzer injection seam or if not complete before T08) | `audit/wiring_analyzer.py` (CREATE) | T03, Phase 0 |

**Milestone M2**: `gate_passed(report_path, WIRING_GATE)` returns correct `(bool, str|None)` for valid and invalid reports. All 5 semantic checks pass independently.

**Critical constraint**: Semantic check functions must be pure `Callable[[str], bool]` — no I/O, no side effects.

**5 required semantic checks**:
1. Analysis complete (`analysis_complete: true`)
2. Recognized rollout mode
3. Finding counts consistent
4. Severity summary consistent
5. Zero blocking findings for mode

**Blocking count behavior by mode**: shadow = 0 blocking, soft = critical only, full = critical + major.

### Phase 3: Roadmap Pipeline Integration (T07–T08)

**Objective**: Integrate wiring verification into roadmap execution as a deterministic, resume-safe step deployed in shadow mode.

| Task | Description | Files | Dependencies |
|------|-------------|-------|-------------|
| T07 | Add `WIRING_GATE` to `ALL_GATES` + `build_wiring_verification_prompt()` returning empty string | `roadmap/gates.py` (MODIFY), `roadmap/prompts.py` (MODIFY) | T05 |
| T08 | Add wiring-verification as step after `spec-fidelity` and before `remediate` in `_build_steps()` + special-case in `roadmap_run_step()` for deterministic execution + update `_get_all_step_ids()` | `roadmap/executor.py` (MODIFY) | T05, T07 |

**Milestone M3**: Full roadmap pipeline completes with wiring-verification step in shadow mode (TRAILING).

**Step construction requirements**: `retry_limit=0`, `gate_mode=GateMode.TRAILING`.

**Critical path note**: T08 is the highest-risk task — touches the roadmap executor hot path and must handle deterministic-step special-casing correctly. Keep wiring verification as a first-class deterministic step, not a disguised prompt step.

**Multi-implementer note**: In multi-session scenarios, Phase 4 (sprint integration) can begin once Phase 1 stabilizes, running in parallel with Phase 3.

### Phase 4: Sprint Integration (T09)

**Objective**: Extend wiring verification into sprint workflows with low-latency AST-only analysis.

| Task | Description | Files | Dependencies |
|------|-------------|-------|-------------|
| T09 | Add `wiring_gate_mode: Literal["off", "shadow", "soft", "full"]` (default `"shadow"`) to `SprintConfig` + post-task analysis hook with mode-aware behavior (shadow: log only, soft: warn, full: gate) | `sprint/executor.py` (MODIFY), `sprint/models.py` (MODIFY) | T03, T05 |

**Milestone M4**: Sprint executor logs wiring findings without affecting task status in shadow mode. Per-task artifacts emitted for traceability.

**Performance target**: AST-only analysis, no subprocesses, target < 2s per task.

**Note**: In single-implementer scenarios, T09 can be combined with Phase 3 work since the context is warm from T07–T08. The separation enables cleaner milestone tracking and parallelism when multiple sessions are available.

### Phase 5: Agent Extensions (T10–T12)

**Objective**: Extend cleanup-audit agents with wiring-aware capabilities. Additive-only changes — no existing rules removed or tools changed.

| Task | Description | Files | Dependencies |
|------|-------------|-------|-------------|
| T10 | Extend audit-scanner with `REVIEW:wiring` classification signal | Agent behavioral rules (MODIFY) | T03 |
| T11 | Extend audit-analyzer with 9th mandatory field "Wiring path" | Agent behavioral rules (MODIFY) | T10 |
| T12 | Extend audit-validator with Check 5: Wiring Claim Verification | Agent behavioral rules (MODIFY) | T11 |

**Milestone M5**: Cleanup-audit produces wiring-aware profiles. Test with existing audit fixtures before merging.

**Deferral option**: Can be deferred to a follow-up PR if scope pressure demands it. The wiring gate functions independently of agent awareness.

### Phase 6: Testing, Validation, and Shadow Calibration (T13–T15)

**Objective**: Achieve ≥90% coverage on core modules, validate all 14 success criteria, and collect shadow data for promotion decisions.

| Task | Description | Dependencies |
|------|-------------|-------------|
| T13 | Unit tests: 20+ tests covering all detection types, semantic checks, whitelist, mode-aware enforcement, edge cases (AST parse failures, empty dirs). Fixtures 50–80 LOC each. | T01–T05 |
| T14 | Integration tests: 3+ tests — full pipeline run with shadow gate, sprint post-task hook, `gate_passed()` with `WIRING_GATE` | T07–T09 |
| T15 | Pre-activation checklist: sanity check (>50 files → >0 findings), `provider_dir_names` validation, retrospective validation against known cli-portify no-op defect class | T03, T08 |

**Milestone M6**: 90% coverage on `wiring_gate.py` and `wiring_analyzer.py` (if T06 not cut). All SC-001 through SC-014 pass. Pre-activation checklist green.

**Parallelism**: T13 can start as soon as Phase 1 completes and run alongside Phases 2–5. T14 requires Phase 4 completion.

**Shadow calibration** (post-implementation, ongoing):

| Activity | Threshold | Duration |
|----------|-----------|----------|
| Shadow data collection | Minimum 2 releases | Ongoing |
| FPR measurement | Baseline established | After shadow window |
| Soft promotion decision | FPR < 15%, TPR > 50%, p95 < 5s | After shadow window |
| Full promotion decision | FPR < 5%, TPR > 80%, whitelist stable 5+ sprints | After soft window |

---

## Risk Assessment

Risks are organized using a four-layer model (Prevent → Detect → Contain → Recover) as a completeness check, then detailed in an actionable flat table.

**Risk handling layers**: (1) **Prevent** via strict layering, deterministic analysis, and bounded scope. (2) **Detect** via integration tests, benchmark suite, and first-run sanity warnings. (3) **Contain** via shadow rollout, trailing mode, and additive-only agent changes. (4) **Recover** via rollback to shadow/off, deferral of ToolOrchestrator work to v3.1, and preservation of existing gate substrate.

### High Priority

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **RISK-005**: `provider_dir_names` misconfiguration → missed/false findings | HIGH | Pre-activation sanity check: >50 files must produce >0 findings. Rollback if zero findings on known-unwired codebase. Resolve in Phase 0 before T01. |
| **RISK-001**: False positives from intentional `Optional[Callable]` hooks | MEDIUM | Whitelist mechanism in T01. Shadow calibration before any enforcement. |
| **RISK-006**: Import re-export aliases → 30–70% FPR | MEDIUM | Document as known limitation. Measure FPR noise floor during shadow. Alias pre-pass deferred to v3.1. Shadow mode acceptable with high FPR — it's observational only. |

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

### Merge Coordination (Open Question #5)

The `roadmap/gates.py` modification overlaps with Anti-Instincts (v3.1) and other v3.x branches. **Recommendation**: Sequence v3.0 merge first — it touches fewer lines in `gates.py` (one import + one list append). Rebase v3.1 after v3.0 lands on integration.

---

## Resource Requirements and Dependencies

### Internal Dependencies (Must Exist, No Changes)

All 14 dependencies (DEP-001 through DEP-014) are existing symbols verified with line-number references. Key risk: if upstream refactoring moves these symbols before v3.0 merges, imports will break.

**Mitigation**: Pin to current `integration` branch state. Run import verification as part of T15.

### Open Questions Requiring Resolution

| Priority | Question | Blocks | Resolution |
|----------|----------|--------|------------|
| **P0** | #1: Definitive `provider_dir_names` set | T01 | Audit actual directory names; default to `{"steps", "handlers", "validators", "checks"}` with config override |
| **P0** | #7: Does `ToolOrchestrator.__init__()` accept `analyzer` param? | T06 | Inspect `audit/tool_orchestrator.py` in Phase 0. If seam absent, T06 deferred to v3.1 (CUT-ELIGIBLE) |
| **P1** | #5: Merge conflict coordination with v3.x branches | T07–T08 | Merge v3.0 first, rebase others |
| **P1** | #6: 30–70% FPR acceptable for shadow? | Phase 6 | Yes — shadow is observational. Measure and document. |
| **P2** | #2–4, #8–10 | Phase 6 | Resolve during shadow calibration with real data |

### Compute and Tooling Requirements

- Python `ast` module (stdlib — no external dependencies)
- `yaml.safe_dump()` for frontmatter emission (PyYAML already in dependency tree)
- Test fixtures: 50–80 LOC each (NFR-012), synthetic Python files with known wiring patterns

---

## Success Criteria and Validation Approach

### Automated Validation (CI-Enforceable)

| Criterion | Test Type | Phase |
|-----------|----------|-------|
| SC-001: Detect `Optional[Callable]=None` never provided | Unit | Phase 6 |
| SC-002: Detect orphan modules | Unit | Phase 6 |
| SC-003: Detect unresolvable registry entries | Unit | Phase 6 |
| SC-004: Report conforms to `GateCriteria` | Unit | Phase 6 |
| SC-005: `gate_passed()` evaluates `WIRING_GATE` unmodified | Integration | Phase 6 |
| SC-007: Whitelist exclusion + suppression count | Unit | Phase 6 |
| SC-008: < 5s for 50 files | Benchmark | Phase 6 |
| SC-013: ToolOrchestrator AST plugin populates references | Unit | Phase 6 (if T06 not cut) |
| SC-014: Mode-aware enforcement correctness | Unit | Phase 6 |

### Manual and Observational Validation

| Criterion | Method | Phase |
|-----------|--------|-------|
| SC-006: Shadow mode doesn't affect task status | Integration test + manual sprint run | Phase 6 |
| SC-009: Catches cli-portify executor no-op bug | Retrospective on known fixtures | Phase 6 |
| SC-010: Pre-activation zero-match warning | Integration test | Phase 6 |
| SC-011: audit-scanner `REVIEW:wiring` | Agent test with audit fixtures | Phase 6 |
| SC-012: audit-analyzer 9-field profile | Agent test | Phase 6 |

### Coverage Gate

- `wiring_gate.py`: ≥ 90% line coverage
- `wiring_analyzer.py`: ≥ 90% line coverage (if T06 not cut)
- Minimum 20 unit tests + 3 integration tests

### Promotion Gates

**Soft promotion** requires all: FPR < 15%, TPR > 50%, p95 < 5s, shadow data for ≥ 2 release cycles, `provider_dir_names` validated, zero unresolved governance questions.

**Full promotion** requires all: FPR < 5%, TPR > 80%, whitelist stable 5+ sprints, sprint latency acceptable, no unresolved substrate or layering regressions.

---

## Timeline Estimates

| Phase | Tasks | Estimated Effort | Cumulative |
|-------|-------|-----------------|-----------|
| Phase 0: Architecture Confirmation | — | 0.5–1 session | 0.5–1 session |
| Phase 1: Core Analysis | T01–T04 | 2–3 sessions | 2.5–4 sessions |
| Phase 2: Gate Definition | T05–T06 | 1–2 sessions | 3.5–6 sessions |
| Phase 3: Roadmap Integration | T07–T08 | 1–2 sessions | 4.5–8 sessions |
| Phase 4: Sprint Integration | T09 | 1 session | 5.5–9 sessions |
| Phase 5: Agent Extensions | T10–T12 | 1–2 sessions | 6.5–11 sessions |
| Phase 6: Testing + Calibration | T13–T15 | 2–3 sessions | 8.5–14 sessions |
| Shadow Observation | — | 2+ release cycles | Ongoing |

### Critical Paths

**Task-level**: T01 → T02 → T03 → T05 → T07 → T08 (core analysis → gate definition → pipeline integration)

**Phase-level**: Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 6. Phase 4 can begin once Phase 1 stabilizes. Phase 5 is off the critical path by design.

### Parallelizable Work

- T01 ∥ T02 (config and data models are independent)
- T06 ∥ T07 (ToolOrchestrator plugin and gates.py modification are independent)
- T10–T12 ∥ T13 (agent extensions and unit tests are independent)
- T13 starts after Phase 1 completes, runs alongside Phases 2–5

### Cut Decisions

- **T06 (ToolOrchestrator AST plugin)**: CUT-ELIGIBLE. Defer to v3.1 if Phase 0 reveals no injection seam or if not complete before T08 begins. Core wiring analysis does not depend on it.
- **Phase 5 (Agent Extensions)**: Can be deferred to a follow-up PR if scope pressure demands it. Wiring gate functions independently of agent awareness.

### Delivery Strategy

1. **Core tranche**: Phases 0–4 to establish core value (deterministic analyzer + report + roadmap/sprint integration in shadow).
2. **Extension tranche**: Phase 5 only if seams are low-risk and schedule allows.
3. **Operational readiness tranche**: Phase 6 before any soft/full enforcement decision.

---

## Deployment Readiness Prerequisites

The following operational dependencies must be resolved before enforcement promotion. They are not implementation tasks but are on the critical path to value delivery.

1. **`provider_dir_names` confirmation**: Definitive set validated against actual repository structure (resolve in Phase 0).
2. **Whitelist governance owner**: Assigned individual responsible for approving whitelist additions and reviewing suppressions.
3. **Promotion review owner**: Assigned individual responsible for evaluating shadow calibration data and authorizing soft/full promotion.
4. **Merge coordination plan**: v3.0 merges to integration before v3.1 (Anti-Instincts) and other v3.x branches to minimize conflict surface.
5. **Shadow telemetry process**: Defined collection and review cadence for FPR/TPR metrics during shadow observation window.

---

## Architectural Recommendations

1. **Implement T01–T04 as a self-contained module first**. The analysis engine should be fully testable in isolation before any pipeline wiring. This de-risks Phase 3 significantly.

2. **Resolve Open Question #7 early**. Inspect `ToolOrchestrator.__init__()` in Phase 0. If the `analyzer` injection seam doesn't exist, cut T06 immediately — it's already CUT-ELIGIBLE and deferring it simplifies the release.

3. **Frontmatter regex duplication is intentional**. Do not refactor `_FRONTMATTER_RE` into a shared module. The duplication preserves the layering constraint (NFR-007).

4. **Shadow mode is the primary deliverable**. The wiring gate in shadow/TRAILING mode is the v3.0 ship requirement. This initiative should be managed as a controlled architecture rollout, not just a feature build. The right success condition is trusted shadow visibility with stable integration, not aggressive enforcement.

5. **Sequence the v3.0 merge before v3.1 (Anti-Instincts)**. v3.0 touches `roadmap/gates.py` minimally (one import, one list append). Landing it first gives v3.1 a clean rebase target.

6. **Share core analysis logic between roadmap and sprint**. Only orchestration should differ — the analyzer is the same. Keep sprint integration thin to minimize latency and rollout risk.
