---
total_diff_points: 12
shared_assumptions_count: 14
---

# Comparative Analysis: Opus-Architect vs Haiku-Architect Roadmaps

## 1. Shared Assumptions and Agreements

1. **Spec source and complexity**: Both derive from `anti-instincts-gate-unified.md` at complexity 0.72
2. **Four core modules**: obligation scanner, integration contracts, fingerprint extraction, spec structural audit — identical scope
3. **Pure Python, zero LLM**: NFR-001 is non-negotiable in both
4. **File locations**: Same 10 new files, same 5 modified files, same directory structure
5. **Gate position**: `anti-instinct` between `merge` and `test-strategy`
6. **Rollout mode enum**: `off | shadow | soft | full` with `off` default
7. **Dataclass definitions**: `ObligationReport`, `Obligation`, `IntegrationAuditResult` — identical
8. **Gate semantics**: Three semantic checks (undischarged obligations == 0, uncovered contracts == 0, fingerprint coverage >= 0.7)
9. **Shadow validation**: 5+ sprints, pass rate >= 0.90 before promotion
10. **Backward compatibility**: Preserve `gate_passed()` signature, no existing test breakage
11. **TurnLedger None-safety**: Both require `if ledger is not None` guards
12. **Success criteria**: SC-001 through SC-009 identically referenced
13. **No new third-party dependencies**: stdlib only (re, dataclasses, yaml)
14. **Defense-in-depth recommendation**: Both lean toward D-03/D-04 coexistence (Option B)

## 2. Divergence Points

### D-01: Phase Count and Granularity
- **Opus**: 4 phases (Core Modules → Gate Wiring → Sprint Integration → Shadow Validation)
- **Haiku**: 6 phases (adds Phase 0: Architecture Lock + separates Phase 3: Prompt Hardening + Phase 6: Rollout)
- **Impact**: Haiku's Phase 0 forces explicit decision resolution before code; Opus embeds decisions as inline "Decision required" notes. Haiku's separation of prompts (Phase 3) from gate wiring (Phase 2) allows independent review. Opus bundles prompts into Phase 2, creating a larger atomic unit.

### D-02: Architecture Decision Record (Phase 0)
- **Opus**: No explicit pre-implementation phase; open questions noted inline with recommended resolutions
- **Haiku**: Dedicates Phase 0 (0.5–1 day) to locking all architectural decisions, freezing integration points, and establishing merge coordination
- **Impact**: Haiku reduces implementation rework risk but adds calendar time. Opus moves faster but risks mid-implementation decision churn on OQ-003/004/005/009/010.

### D-03: Timeline Units
- **Opus**: Estimates in "sprints" (6–10 sprints total)
- **Haiku**: Estimates in "working days" (8–12 days for build, 1–2 sprints for rollout observation)
- **Impact**: Opus's sprint-based estimates are ambiguous (sprint length undefined). Haiku's day-based estimates are more actionable for planning but may underestimate if sprint overhead exists.

### D-04: Prompt Changes Placement
- **Opus**: Prompt modifications in Phase 2 (bundled with gate/executor wiring)
- **Haiku**: Prompt modifications isolated in Phase 3 (after gate wiring, before sprint integration)
- **Impact**: Haiku treats prompts as a separate concern with independent validation. Opus treats them as part of the wiring phase, which is more efficient but harder to review independently.

### D-05: Parallelization Assessment
- **Opus**: "No parallelism between phases. Phase 1 modules are internally parallelizable."
- **Haiku**: Identifies cross-phase parallelization: Phase 1 analyzers can overlap with Phase 3 prompt changes; unit tests parallel with module coding; sprint tests can begin once API shape frozen
- **Impact**: Haiku's parallelization opportunities could compress the calendar timeline by 1–2 days. Opus's stricter sequencing is more conservative but potentially slower.

### D-06: Rollout Phase Explicitness
- **Opus**: Phase 4 covers shadow validation and graduation as a single phase
- **Haiku**: Splits into Phase 5 (validation/calibration) and Phase 6 (controlled rollout) with explicit promotion gates (Checkpoint A/B/C)
- **Impact**: Haiku's three named checkpoints (A: implementation readiness, B: rollout readiness, C: enforcement readiness) provide clearer go/no-go decision points. Opus's graduation criteria are present but less formally structured.

### D-07: Resource Requirements
- **Opus**: No explicit resource/staffing section
- **Haiku**: Explicitly calls for 3 roles: 1 backend/pipeline engineer, 1 QA engineer, 1 architecture reviewer
- **Impact**: Haiku provides actionable staffing guidance. Opus assumes resourcing is implicit.

### D-08: Sprint Rollout `off` Mode Semantics
- **Opus**: `off` = "no gate evaluation"
- **Haiku**: `off` = "gate evaluated if required for metrics policy, but no behavior change"
- **Impact**: Subtle but significant. Haiku's interpretation allows metrics collection even in `off` mode, which could accelerate shadow validation data collection. Opus's strict `off` means no computation at all.

### D-09: Validation Strategy Structure
- **Opus**: Tests organized by phase (unit tests in Phase 1, integration in Phase 2, sprint in Phase 3)
- **Haiku**: Tests organized by validation type (A: unit, B: integration, C: sprint-mode, D: regression, E: non-functional) cutting across phases
- **Impact**: Haiku's cross-cutting validation taxonomy is more useful for test planning and coverage analysis. Opus's phase-aligned testing is simpler to execute sequentially.

### D-10: Architect Recommendations
- **Opus**: Embedded throughout as constraints and notes
- **Haiku**: Consolidated in a dedicated section (Section 6) with 5 numbered recommendations plus per-phase guidance blocks
- **Impact**: Haiku's explicit architect guidance is more discoverable and reviewable. Opus's inline approach keeps guidance closer to relevant context.

### D-11: Requirement Coverage Matrix
- **Opus**: No explicit coverage matrix; requirements referenced inline
- **Haiku**: Includes a dedicated requirement-to-phase coverage matrix (Section 7)
- **Impact**: Haiku's matrix enables quick verification that all 34 requirements are addressed. Opus requires reading the full document to confirm coverage.

### D-12: Dependency Enumeration
- **Opus**: Lists new/modified files with conflict risk ratings per file
- **Haiku**: Lists all code dependencies including upstream gates (`MERGE_GATE`, `SPEC_FIDELITY_GATE`, `WIRING_GATE`) and tooling dependencies (UV, test harness, regression fixtures)
- **Impact**: Haiku's broader dependency enumeration catches integration risks Opus doesn't surface (e.g., `kpi.py` dependency, existing gate interactions).

## 3. Areas Where One Variant Is Clearly Stronger

### Opus strengths:
- **Inline decision tracking**: Open questions appear exactly where they affect implementation, with concrete recommended resolutions — easier for an implementer to act on
- **Conflict risk ratings**: Per-file conflict risk (LOW/MEDIUM) on modified files is actionable
- **Conciseness**: ~40% shorter; higher signal density for an experienced implementer

### Haiku strengths:
- **Phase 0 architecture lock**: Forcing decision resolution before code prevents mid-implementation pivots — clearly superior for team coordination
- **Checkpoint framework**: Three named promotion gates (A/B/C) with explicit criteria are more rigorous than Opus's single graduation section
- **Cross-cutting validation taxonomy**: Test strategy organized by type rather than phase catches gaps more reliably
- **Resource and staffing section**: Opus omits this entirely
- **Requirement coverage matrix**: Enables quick audit of spec coverage completeness
- **Parallelization analysis**: Identifies real opportunities Opus explicitly rules out
- **Broader dependency graph**: Catches `kpi.py` and upstream gate dependencies Opus misses

## 4. Areas Requiring Debate to Resolve

1. **Phase 0 necessity**: Is a formal architecture decision record worth 0.5–1 day, or can OQs be resolved inline during Phase 1? Depends on team size and coordination overhead.

2. **`off` mode semantics (D-08)**: Should `off` mean zero computation or passive metrics collection? This affects how quickly shadow data accumulates and whether `off` is truly zero-cost.

3. **Prompt changes bundling (D-04)**: Should prompt modifications be reviewed independently (Haiku) or shipped atomically with gate wiring (Opus)? Depends on whether prompt changes need separate stakeholder review.

4. **Cross-phase parallelism (D-05)**: Is Phase 1 + Phase 3 overlap safe given that prompt changes could affect what the analyzers need to detect? The dependency is indirect but real.

5. **Timeline units (D-03)**: The estimates need reconciliation. Opus's "6–10 sprints" vs Haiku's "8–12 days + 1–2 sprints observation" suggest fundamentally different scope interpretations unless Opus sprints are 1-day sprints.
