---
total_diff_points: 12
shared_assumptions_count: 14
---

# Comparative Diff Analysis: Opus-Architect vs Haiku-Architect Roadmaps

## 1. Shared Assumptions and Agreements

Both variants agree on:

1. **Complexity score**: 0.78 (HIGH)
2. **NFR-006 is non-negotiable**: zero modifications to `pipeline/models.py`, `pipeline/gates.py`, `pipeline/trailing_gate.py`
3. **AST-only analysis** using Python `ast` module, no dynamic dispatch resolution
4. **Three analyzer types**: unwired callables, orphan modules, unwired registries
5. **Phased rollout model**: shadow → soft → blocking
6. **Floor-to-zero credit semantics** (`credit_wiring(1, 0.8) == 0`) as by-design behavior requiring explicit tests
7. **Whitelist as first-class citizen** shipped in Phase 1, not deferred
8. **R6 (provider_dir_names mismatch)** as highest rollout risk
9. **Retrospective validation (T11)** is mandatory — must detect original `step_runner=None` no-op bug
10. **`roadmap/gates.py` coordination** needed with Anti-Instincts / Unified Audit Gating
11. **Per-file try/except** for AST parse error graceful degradation (NFR-002)
12. **Total LOC estimates** roughly comparable (~800-1100 LOC)
13. **All 15 success criteria** must be mapped and validated
14. **Import alias resolution** deferred to v1.1

---

## 2. Divergence Points

### D1 — Phase Structure (4 vs 7 phases)

- **Opus**: 4 phases — Core Engine → Sprint Integration → KPI/Reconciliation → Integration Testing
- **Haiku**: 7 phases (0-6) — Spec Closure → Analysis → Report/Gate → Sprint Integration → Fidelity → Tests → Rollout

**Impact**: Haiku's Phase 0 (spec closure) and Phase 6 (controlled rollout) are explicit phases that Opus handles as inline blockers and post-merge concerns respectively. Haiku's granularity makes dependencies clearer but adds coordination overhead. Opus's consolidation is more actionable for a single implementer.

### D2 — Specification Closure as Explicit Phase

- **Opus**: Treats open questions as inline recommendations within a closing section; no separate phase
- **Haiku**: Dedicates Phase 0 (1-2 days) as a gating milestone before any code begins

**Impact**: Haiku's approach prevents implementation starting with unresolved ambiguity but adds calendar time. Opus assumes an experienced implementer can resolve questions during Phase 2 implementation. For a team with multiple contributors, Haiku's approach is safer; for a solo implementer, Opus's is more efficient.

### D3 — Report/Gate as Separate Phase vs Embedded in Phase 1

- **Opus**: Report emission and gate definition are Milestone 1.3 within Phase 1
- **Haiku**: Dedicates Phase 2 (2 days) solely to report and gate conformance

**Impact**: Opus treats report generation as tightly coupled to analysis (same file, same phase). Haiku separates concerns for clearer exit criteria. The practical difference is minimal since both deliver the same artifacts before sprint integration.

### D4 — Testing Strategy Placement

- **Opus**: Unit tests embedded within each phase (Milestone 1.4 for Phase 1, Milestone 2.3 for Phase 2); integration tests in Phase 4
- **Haiku**: All testing consolidated in Phase 5 (3-4 days), after all feature phases complete

**Impact**: Opus's approach catches regressions earlier and follows test-alongside-code practice. Haiku's consolidation risks late discovery of integration issues but allows the test engineer to work from stable, complete code. Opus's approach is stronger for CI-driven workflows.

### D5 — Rollout as Explicit Phase vs Implicit

- **Opus**: No rollout phase; ends at Phase 4 (integration testing + retrospective)
- **Haiku**: Phase 6 explicitly models shadow → soft → blocking promotion with measurable criteria

**Impact**: Haiku correctly identifies that rollout is an engineering concern requiring telemetry review and evidence-based promotion decisions. Opus's roadmap ends at "code complete + validated" and leaves rollout as an operational concern. For production safety, Haiku's explicit rollout phase is materially stronger.

### D6 — Engineering Role Decomposition

- **Opus**: No role assignments; implicitly assumes single implementer or undifferentiated team
- **Haiku**: Explicitly names 4 roles — backend/static-analysis engineer, pipeline/sprint integration engineer, quality engineer, release architect/reviewer

**Impact**: Haiku's role decomposition enables parallel work streams and clearer ownership. Opus's single-track approach is simpler but limits parallelism. For a team > 1, Haiku provides actionable staffing guidance.

### D7 — Parallelism Recommendations

- **Opus**: Notes Phase 3 (KPI/reconciliation) can run parallel with Phase 4 (integration tests); Phase 1 is "highly parallelizable internally"
- **Haiku**: Notes Phase 3 and Phase 4 can overlap "only if ownership is split and merge coordination is explicit"; more cautious

**Impact**: Opus is more aggressive about parallelism, which could accelerate delivery but requires implicit coordination. Haiku's guardrail is appropriate for teams where merge conflicts are a real risk.

### D8 — Timeline Estimates

- **Opus**: No explicit timeline estimates (deliberate omission per some project conventions)
- **Haiku**: Explicit day estimates per phase totaling ~13-20 engineering days + 2 release cycles for rollout

**Impact**: Haiku provides actionable planning data. Opus leaves timeline to the implementer. Whether this is a strength or weakness depends on project norms — Opus may be following the "avoid giving time estimates" instruction.

### D9 — Open Question Treatment Depth

- **Opus**: 10 numbered open questions with specific architect recommendations (approve/defer/block)
- **Haiku**: Same questions absorbed into Phase 0 closure requirements without individual recommendations

**Impact**: Opus's per-question recommendations are immediately actionable — an implementer can start Phase 1 with clear decisions. Haiku requires a separate decision-making session before work begins. Opus is stronger here for implementation velocity.

### D10 — Validation Checkpoint Granularity

- **Opus**: Acceptance criteria listed per milestone
- **Haiku**: Explicit "Validation checkpoints by phase" section (Section 5) with cumulative criteria per phase boundary

**Impact**: Haiku's checkpoint model is better for gate-review workflows where a reviewer needs to approve phase transitions. Opus's per-milestone criteria are more useful for the implementer doing continuous validation.

### D11 — `--skip-wiring-gate` CLI Flag

- **Opus**: Recommends deferring to Phase 2 rollout — "shadow mode already provides non-interference"
- **Haiku**: Lists as an open question to resolve in Phase 0 — no explicit recommendation

**Impact**: Minor. Opus's reasoning is sound — shadow mode makes the flag redundant for v1.0.

### D12 — Provider Heuristic ("3+ files with common prefix")

- **Opus**: Explicitly recommends excluding from v1.0 scope — "unspecified and untested"
- **Haiku**: Lists as Phase 0 decision item — "whether provider heuristic in `Goal-2a` is active scope or deferred"

**Impact**: Opus takes a clear position; Haiku defers the decision. Opus's recommendation to exclude is well-reasoned given the complexity and testing burden.

---

## 3. Areas Where One Variant Is Clearly Stronger

### Opus Strengths
- **Open question resolution**: Actionable per-question recommendations with rationale — implementer can start immediately
- **Test-alongside-code**: Unit tests embedded in feature phases catches issues earlier
- **LOC estimates per item**: Granular sizing at the task level aids sprint planning
- **Requirement traceability table**: SC-ID → Phase → Test Type → Gate mapping is a complete verification matrix
- **Critical path clarity**: Single clear statement — Phase 1 → 2 → 4, with Phase 3 parallel

### Haiku Strengths
- **Rollout as engineering phase**: Phase 6 with measurable promotion criteria is production-grade thinking Opus omits entirely
- **Spec closure gate**: Phase 0 prevents wasted work on ambiguous requirements
- **Role decomposition**: Enables team-scale execution and ownership clarity
- **Validation checkpoints**: Cumulative phase-boundary review model suits gate-review governance
- **Risk-to-requirement traceability**: Each risk explicitly lists affected requirements

---

## 4. Areas Requiring Debate to Resolve

1. **Should spec closure be a blocking phase or inline?** Opus assumes an experienced implementer can resolve questions during implementation; Haiku insists on upfront closure. The right answer depends on team size and implementer experience.

2. **Should rollout be in-scope for the roadmap?** Opus treats it as post-merge operational concern; Haiku models it as Phase 6 with explicit criteria. If this roadmap drives a tasklist, rollout phases need to be included or explicitly excluded.

3. **Testing placement — alongside or consolidated?** Opus embeds tests per phase; Haiku consolidates. The hybrid approach (unit tests per phase, integration tests consolidated) may be optimal — which is closer to Opus's actual structure.

4. **Timeline estimates — include or omit?** Project conventions may prohibit time estimates (Opus follows this). If stakeholders need delivery projections, Haiku's estimates are necessary. This is a governance question, not a technical one.

5. **Parallelism posture — aggressive or guarded?** Depends on team size and merge-conflict history in `roadmap/gates.py`. If the Anti-Instincts work is active, Haiku's caution is warranted.
