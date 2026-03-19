---
complexity_class: HIGH
validation_philosophy: continuous-parallel
validation_milestones: 9
work_milestones: 9
interleave_ratio: "1:1"
major_issue_policy: stop-and-fix
spec_source: merged-spec.md
generated: "2026-03-19T01:59:39.414373+00:00"
generator: superclaude-roadmap-executor
---

# Unified Audit Gating — Test Strategy

## Issue Classification

| Severity | Action | Gate Impact |
|----------|--------|-------------|
| CRITICAL | Stop-and-fix immediately | Blocks current phase |
| MAJOR | Stop-and-fix before next phase | Blocks next phase |
| MINOR | Track and fix in next sprint | No gate impact |
| COSMETIC | Backlog | No gate impact |

---

## 1. Validation Milestones Mapped to Roadmap Phases

| Validation Milestone | Roadmap Phase | Gate Description | Blocking Criteria |
|---------------------|---------------|------------------|-------------------|
| **VM-0** | Phase 0 — Decision Checkpoint | Decision completeness gate | All 7 open questions resolved with rationale documented |
| **VM-1** | Phase 1 — Core Analysis Engine | Analyzer correctness gate | SC-001–003 pass; whitelist works; SyntaxError handled; <2s for 50-file fixture |
| **VM-2** | Phase 2 — Report & Gate Definition | Report conformance gate | 17 frontmatter fields present; `gate_passed()` evaluates WIRING_GATE; mode semantics correct; 90% coverage |
| **VM-3a** | Phase 3a — Roadmap Integration | Pipeline integration gate | Step ordering correct; shadow gate non-blocking; no layering violations |
| **VM-3b** | Phase 3b — Sprint Integration | Sprint hook gate | Shadow/soft/full semantics honored; no performance regression |
| **VM-4** | Phase 4 — Agent Extensions | Agent regression gate | All extensions additive; 9-field profiles correct; no regression in prior outputs |
| **VM-5** | Phase 5 — ToolOrchestrator Plugin | Plugin correctness gate (conditional) | `FileAnalysis.references` populated; dual evidence rule functional |
| **VM-6a** | Phase 6a — Shadow Calibration | Statistical readiness gate | FPR < 15%, TPR > 50%, p95 < 5s, ≥2 release cycles data |
| **VM-6b** | Phase 6b — Activation | Operational stability gate | FPR < 5%, TPR > 80%, whitelist stable 5+ sprints |

---

## 2. Test Categories

### 2.1 Unit Tests (target: ≥20)

| ID | Test | Phase | Requirements | Priority |
|----|------|-------|-------------|----------|
| UT-01 | Unwired callable detection on fixture with `Optional[Callable]=None` never provided | 1 | FR-001, FR-012, SC-001 | P0 |
| UT-02 | Unwired callable — callable IS provided at call site → no finding | 1 | FR-012 | P0 |
| UT-03 | Orphan module detection on fixture with zero importers | 1 | FR-002, FR-015, SC-002 | P0 |
| UT-04 | Orphan exclusion: `__init__.py`, `conftest.py`, `test_*.py` not flagged | 1 | FR-016 | P0 |
| UT-05 | Registry detection — unresolvable function reference | 1 | FR-003, FR-018, SC-003 | P0 |
| UT-06 | Registry classification — three detection types correctly assigned | 1 | FR-019 | P1 |
| UT-07 | Whitelist suppression — matching entries excluded, count incremented | 1 | FR-013, SC-007 | P0 |
| UT-08 | Whitelist malformed entry — WARNING logged (shadow mode) | 1 | FR-013 | P1 |
| UT-09 | `ast_analyze_file()` — SyntaxError returns empty `FileAnalysis` | 1 | FR-021 | P0 |
| UT-10 | `ast_analyze_file()` — valid file populates imports/exports/metadata | 1 | FR-020 | P1 |
| UT-11 | Severity assignment — critical/major/info correctly mapped | 1 | FR-014 | P0 |
| UT-12 | Report frontmatter contains all 17 required fields | 2 | FR-022, SC-004 | P0 |
| UT-13 | Report body contains 7 sections in correct order | 2 | FR-023 | P1 |
| UT-14 | `_extract_frontmatter_values()` parses frontmatter correctly | 2 | FR-024 | P0 |
| UT-15 | `_analysis_complete_true` semantic check | 2 | FR-026 | P1 |
| UT-16 | `_recognized_rollout_mode` semantic check | 2 | FR-026 | P1 |
| UT-17 | `_finding_counts_consistent` semantic check | 2 | FR-026 | P0 |
| UT-18 | `_severity_summary_consistent` semantic check | 2 | FR-026 | P0 |
| UT-19 | `_zero_blocking_findings_for_mode` — shadow always True | 2 | FR-027, SC-014 | P0 |
| UT-20 | `_zero_blocking_findings_for_mode` — full blocks on findings | 2 | FR-027, SC-014 | P0 |
| UT-21 | `blocking_findings` computation per rollout mode | 2 | FR-028 | P0 |
| UT-22 | `WIRING_GATE` GateCriteria well-formed (tier, min_lines, fields, checks) | 2 | FR-025 | P1 |
| UT-23 | YAML safe_dump used for string frontmatter values | 2 | NFR-005 | P1 |
| UT-24 | ToolOrchestrator plugin — references populated for import-bearing files | 5 | FR-008, SC-013 | P1 |
| UT-25 | Dual evidence rule — orphan requires both AST + no audit justification | 5 | FR-017 | P1 |

### 2.2 Integration Tests (target: ≥3)

| ID | Test | Phase | Requirements | Priority |
|----|------|-------|-------------|----------|
| IT-01 | Unmodified `gate_passed()` evaluates `WIRING_GATE` correctly | 2–3a | SC-005, NFR-006 | P0 |
| IT-02 | Roadmap pipeline executes wiring-verification step end-to-end in shadow | 3a | FR-006, FR-030, FR-031 | P0 |
| IT-03 | Sprint task status unchanged with shadow-mode wiring findings | 3b | FR-035, SC-006 | P0 |
| IT-04 | Sprint soft mode warns on critical findings | 3b | FR-035 | P0 |
| IT-05 | Sprint full mode blocks on critical+major findings | 3b | FR-035 | P0 |
| IT-06 | Pre-activation zero-match warning with misconfigured `provider_dir_names` | 3b | SC-010 | P1 |

### 2.3 End-to-End Tests

| ID | Test | Phase | Purpose |
|----|------|-------|---------|
| E2E-01 | Full roadmap pipeline with wiring step → report emitted → gate evaluated | 3a | Validates complete pipeline path |
| E2E-02 | Sprint execution loop with wiring hook in each mode | 3b | Validates sprint integration path |
| E2E-03 | Audit pipeline produces 9-field profiles with Wiring path on test repo | 4 | Validates agent extension path |

### 2.4 Acceptance / Validation Tests

| ID | Test | Phase | Method |
|----|------|-------|--------|
| AT-01 | Retrospective: analyzer detects known `step_runner` bug in cli-portify | 6a | SC-009 — manual run, documented evidence |
| AT-02 | Shadow FPR/TPR/p95 within thresholds | 6a | Statistical analysis of shadow data |
| AT-03 | Alias noise floor characterization | 6a | Documented analysis separating signal from re-export noise |
| AT-04 | Soft-mode stability over 5+ sprints | 6b | Operational monitoring evidence |

### 2.5 Static Verification Tests

| ID | Check | Phase | Method |
|----|-------|-------|--------|
| SV-01 | No signature changes to pipeline substrate | All | `grep` for changed signatures in `pipeline/*.py` (NFR-006) |
| SV-02 | No `pipeline/*` imports from `roadmap/*`, `audit/*`, `sprint/*` | All | Import graph analysis (NFR-007) |
| SV-03 | Agent extensions are additive only — no rules removed, no tools changed | 4 | Diff analysis against prior agent specs (NFR-013) |

### 2.6 Benchmark Tests

| ID | Test | Phase | Threshold |
|----|------|-------|-----------|
| BM-01 | 50-file analysis completes within budget | 1 | < 2s target, < 5s hard limit (NFR-001, SC-008) |
| BM-02 | Sprint hook latency impact | 3b | No measurable regression on task execution path |

---

## 3. Test-Implementation Interleaving Strategy

### Ratio Justification

**Complexity class**: HIGH (0.78 score) → **1:1 interleave ratio**

Every implementation phase has a paired validation milestone. This is justified by:

1. **Integration breadth**: 3 subsystems + 5 agent specs. Defects compound across boundaries if not caught immediately.
2. **Constraint density**: Zero-change pipeline contract, layering rules, frontmatter invariants. Each constraint is a potential silent violation.
3. **Rollout irreversibility**: Shadow → soft → full progression depends on clean data from prior phases. A false-positive bug in Phase 1 corrupts Phase 6a calibration data.
4. **Agent behavioral risk**: LLM-interpreted spec changes have emergent effects that only surface through end-to-end agent testing.

### Interleaving Schedule

```
Phase 0 (implement) → VM-0 (validate decisions)
Phase 1 (implement) → VM-1 (validate analyzers)
Phase 2 (implement) → VM-2 (validate report + gate)
Phase 3a (implement) → VM-3a (validate roadmap integration)
Phase 3b (implement) → VM-3b (validate sprint integration)
Phase 4 (implement) → VM-4 (validate agent extensions)
Phase 5 (implement) → VM-5 (validate plugin) [conditional]
Phase 6a (observe) → VM-6a (validate statistical readiness)
Phase 6b (activate) → VM-6b (validate operational stability)
```

**Rule**: No phase may begin until the prior phase's validation milestone passes with zero CRITICAL and zero MAJOR issues.

---

## 4. Risk-Based Test Prioritization

### Tier 0 — Must pass before ANY code ships to shadow

These tests guard against the highest-severity risks and the hardest-to-fix-later defects:

| Tests | Risk Mitigated |
|-------|---------------|
| UT-01 through UT-05 (core detection) | R1: False positives undermine trust |
| UT-07 (whitelist suppression) | R1: No escape hatch for intentional optionals |
| UT-09 (SyntaxError handling) | R2: Unhandled parse errors crash pipeline |
| UT-12, UT-14 (frontmatter completeness) | Corrupt reports produce meaningless shadow data |
| UT-19, UT-20, UT-21 (mode semantics) | R8: Shadow mode blocks unexpectedly |
| IT-01 (unmodified gate_passed) | NFR-006: Pipeline substrate integrity |
| SV-01, SV-02 (static layering) | NFR-006, NFR-007: Architectural violations |
| BM-01 (performance) | R4: Sprint performance degradation |

### Tier 1 — Must pass before soft-mode activation

| Tests | Risk Mitigated |
|-------|---------------|
| IT-02, IT-03 (pipeline + sprint integration) | Integration defects masked by shadow pass-through |
| IT-04, IT-05 (soft/full mode behavior) | Enforcement semantics incorrect when mode changes |
| IT-06 (zero-match warning) | R5: Misconfigured provider_dir_names silently succeeds |
| E2E-01, E2E-02 (end-to-end paths) | Cross-subsystem interaction failures |
| AT-01 (retrospective detection) | Validates real-world detection capability |
| AT-02 (FPR/TPR thresholds) | R3, R6: Insufficient or noisy data |

### Tier 2 — Must pass before full-mode activation

| Tests | Risk Mitigated |
|-------|---------------|
| E2E-03 (audit pipeline) | R7: Agent regression |
| SV-03 (additive-only check) | R7: Spec changes remove existing behavior |
| AT-03 (alias noise floor) | R6: FPR inseparable from noise |
| AT-04 (soft-mode stability) | Premature full activation |

---

## 5. Acceptance Criteria per Milestone

### VM-0 — Decision Checkpoint
- [ ] All 7 open questions (OQ-1 through OQ-7) have committed answers
- [ ] Each answer includes rationale and source
- [ ] Decision log committed to repository
- **Gate**: Proceed only when all 7 answered. Missing answers = MAJOR.

### VM-1 — Core Analysis Engine
- [ ] UT-01 through UT-11 pass (all analyzer unit tests)
- [ ] Whitelist suppression increments `whitelist_entries_applied`
- [ ] `SyntaxError` produces empty `FileAnalysis`, no crash
- [ ] BM-01: < 2s for 50-file fixture (< 5s hard limit)
- [ ] `WiringFinding`, `WiringReport`, `WiringConfig` dataclasses match FR-009–011
- **Gate**: All P0 unit tests green. Performance within budget. Coverage ≥ 80% on analyzer.

### VM-2 — Report & Gate Definition
- [ ] UT-12 through UT-23 pass (all report + gate unit tests)
- [ ] Report frontmatter: exactly 17 fields present
- [ ] `gate_passed(WIRING_GATE, report)` returns True for well-formed shadow report
- [ ] Mode semantics: shadow always passes; soft blocks on critical; full blocks on critical+major
- [ ] Coverage ≥ 90% on `wiring_gate.py` and `wiring_analyzer.py` (NFR-003)
- [ ] ≥ 20 unit tests total (NFR-004)
- **Gate**: Coverage target met. All semantic checks verified. YAML injection prevention confirmed.

### VM-3a — Roadmap Integration
- [ ] IT-02 passes: wiring-verification step executes in pipeline
- [ ] `_get_all_step_ids()` returns wiring-verification between spec-fidelity and remediate
- [ ] SV-01: No pipeline substrate signature changes
- [ ] SV-02: No layering violations (`pipeline/*` imports clean)
- [ ] Shadow gate does not block pipeline completion
- **Gate**: End-to-end pipeline runs with wiring step. Zero layering violations.

### VM-3b — Sprint Integration
- [ ] IT-03: Shadow mode — task status unchanged with findings
- [ ] IT-04: Soft mode — warning emitted on critical findings
- [ ] IT-05: Full mode — blocked on critical+major findings
- [ ] IT-06: Zero-match warning emitted for misconfigured dirs
- [ ] BM-02: No measurable performance regression on task path
- [ ] ≥ 3 integration tests total (NFR-004)
- **Gate**: All three modes behave correctly. Performance neutral.

### VM-4 — Agent Extensions
- [ ] SV-03: All extensions additive — diff shows no removals
- [ ] Scanner classifies wiring-indicator files as `REVIEW:wiring`
- [ ] Analyzer produces 9-field profiles with Wiring path (chain or "MISSING")
- [ ] Validator flags DELETE on files with live wiring paths as critical fail
- [ ] Comparator includes cross-file wiring consistency check
- [ ] Consolidator includes Wiring Health section
- [ ] No regression in existing audit output quality (compare against baseline)
- **Gate**: All 5 agents extended. Regression test against prior outputs passes.

### VM-5 — ToolOrchestrator Plugin (conditional)
- [ ] UT-24: `FileAnalysis.references` populated for import-bearing files
- [ ] UT-25: Dual evidence rule functional
- [ ] Plugin integrates without modifying `ToolOrchestrator` contract
- **Gate**: Plugin works or is deferred per NFR-012 cut criteria.

### VM-6a — Shadow Calibration
- [ ] AT-01: Retrospective detects known `step_runner` defect
- [ ] AT-02: FPR < 15%, TPR > 50%, p95 < 5s
- [ ] AT-03: Alias noise floor characterized and separable from signal
- [ ] Shadow data from ≥ 2 release cycles
- [ ] `measured_FPR + 2σ < 15%` (NFR-014)
- [ ] Readiness report produced with explicit go/no-go recommendation
- **Gate**: Statistical thresholds met OR shadow period extended. No activation on marginal data.

### VM-6b — Activation & Hardening
- [ ] FPR < 5%, TPR > 80%
- [ ] Whitelist stable for 5+ sprints
- [ ] No material audit regressions during soft-mode period
- [ ] AT-04: Operational stability confirmed
- **Gate**: Full enforcement activated only on measured evidence. Regression = rollback to soft.

---

## 6. Quality Gates Between Phases

### Gate Structure

Each gate follows the same protocol:

```
1. Run all tests for the completed phase
2. Run static verification (SV-01, SV-02) — always
3. Run coverage check — Phases 1+ require ≥ 90% on touched files
4. Classify any failures by severity
5. Apply issue policy:
   - CRITICAL → stop-and-fix immediately, re-run gate
   - MAJOR → stop-and-fix before next phase begins
   - MINOR → log in backlog, proceed
   - COSMETIC → log in backlog, proceed
6. Document gate result in phase completion record
```

### Gate Definitions

| Gate | Between | Must Pass | Blocks On |
|------|---------|-----------|-----------|
| **G0→1** | Decision → Core Engine | VM-0 all criteria | Any unanswered question |
| **G1→2** | Core Engine → Report | VM-1 all criteria | Any P0 unit test failure; performance budget exceeded |
| **G2→3a** | Report → Roadmap Integration | VM-2 all criteria | Coverage < 90%; mode semantics incorrect |
| **G3a→3b** | Roadmap → Sprint Integration | VM-3a all criteria | Layering violation; pipeline regression |
| **G3b→6a** | Sprint → Shadow Calibration | VM-3b all criteria | Any mode behavior incorrect; performance regression |
| **G4→merge** | Agent Extensions → Merge | VM-4 all criteria | Any agent regression; non-additive change |
| **G5→merge** | Plugin → Merge | VM-5 all criteria OR cut decision | Plugin breaks contract (CRITICAL) |
| **G6a→6b** | Shadow → Activation | VM-6a all criteria | FPR/TPR thresholds not met; insufficient data |
| **G6b→done** | Activation → Complete | VM-6b all criteria | Regression during soft-mode operation |

### Parallel Gate Considerations

Phases 3a, 3b, and 4 have parallel execution windows:

- **Phase 4** may begin after Phase 1 completes (needs analyzer context)
- **Phase 4** gate (VM-4) is independent of VM-3a/VM-3b
- **Phase 3b** must wait for VM-3a to pass
- All three must pass their respective gates before shadow calibration begins

```
G1→2 ──→ G2→3a ──→ G3a→3b ──→ G3b→6a ──→ G6a→6b
              │                      ↑
              └──→ G4→merge ─────────┘ (must merge before 6a)
```

### Regression Policy

After any gate passes, subsequent phases must not break prior gate criteria. If a later phase introduces a regression detected by a prior phase's tests:

1. Classify the regression (CRITICAL/MAJOR/MINOR)
2. CRITICAL/MAJOR: Stop current phase, fix regression, re-run both gates
3. MINOR: Fix in current phase, re-run prior gate before proceeding

### Test Fixture Requirements

| Fixture | Purpose | Phase |
|---------|---------|-------|
| `fixtures/unwired_callable.py` | Class with `Optional[Callable]=None` never provided | 1 |
| `fixtures/wired_callable.py` | Class with callable properly provided (negative case) | 1 |
| `fixtures/orphan_module.py` | Module in provider dir with zero importers | 1 |
| `fixtures/valid_module.py` | Module with active import chain (negative case) | 1 |
| `fixtures/broken_registry.py` | Registry dict with unresolvable function ref | 1 |
| `fixtures/valid_registry.py` | Registry with all entries resolvable (negative case) | 1 |
| `fixtures/syntax_error.py` | Intentionally malformed Python file | 1 |
| `fixtures/whitelist.yaml` | Suppression config with valid + malformed entries | 1 |
| `fixtures/50_file_benchmark/` | 50 Python files for performance testing | 1 |
| `fixtures/golden_report.yaml` | Known-good report for regression comparison | 2 |
| `fixtures/audit_baseline/` | Prior audit outputs for agent regression testing | 4 |
