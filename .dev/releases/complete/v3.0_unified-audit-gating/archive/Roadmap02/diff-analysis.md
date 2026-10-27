

---
total_diff_points: 12
shared_assumptions_count: 14
---

## 1. Shared Assumptions and Agreements

Both variants align on these foundational points:

1. **Complexity score**: 0.92 / HIGH — both treat this as architecturally significant
2. **Scope boundary**: v1.2.1 = milestone + release scope only; task-scope deferred to v1.3
3. **Phase structure**: Phase 0 (defects/governance) → Foundation → Integration → Rollout promotion
4. **P0-A defects**: `run_portify()` step_runner fix and `validate_portify_config()` enforcement are hard prerequisites
5. **Dead code retirement**: Both retire `_apply_resume_after_spec_patch()` and `_find_qualifying_deviation_files()`
6. **Canonical terms**: Same 6 terms defined (`AuditLease`, `audit_lease_timeout`, `max_turns`, `Critical Path Override`, `audit_gate_required`, `audit_attempts`)
7. **`AuditGateResult` naming**: Both introduce a new dataclass to avoid collision with existing `GateResult`
8. **Silent Success Detector**: Same signal suite (S1/S2/S3), same composite formula, same band thresholds
9. **Smoke Test Gate G-012**: Same check hierarchy (timing/artifact/content), same failure routing
10. **D-03/D-04 fidelity checks**: Deterministic findings override LLM severity in both
11. **Lease model**: Same fields, same heartbeat formula (`≤ timeout/3`), same timeout behavior
12. **Rollout sequence**: Shadow → Soft → Full with KPI gates at each transition
13. **Override rules**: Hard-fail never overridable at release scope; soft-fail overridable at task/milestone
14. **Required roles**: Both identify the same role gaps (Reliability Owner, Policy Owner, Tasklist Owner, Program Manager)

---

## 2. Divergence Points

### D-01: Phase Count and Boundary Placement

- **Opus**: 5 phases (P0–P4). Smoke Test Gate G-012 is in **Phase 1** alongside Silent Success and D-03/D-04. TUI is a separate **Phase 3** (Enforcement).
- **Haiku**: 5 phases (P0–P4). Smoke Test Gate G-012 is deferred to **Phase 2** alongside lease/retry integration. TUI is also in Phase 2.
- **Impact**: Opus front-loads all three behavioral gates before any integration work, enabling earlier standalone validation. Haiku couples G-012 with the infrastructure it needs (lease model, executor wiring), reducing rework risk but delaying smoke gate availability.

### D-02: TUI Placement

- **Opus**: TUI is isolated in Phase 3 (Enforcement), after integration is complete.
- **Haiku**: TUI is bundled into Phase 2 alongside gate integration.
- **Impact**: Opus allows operator experience design to benefit from integration learnings. Haiku enables earlier operator feedback but risks TUI rework if integration surfaces unexpected state shapes.

### D-03: Timeline Estimates

- **Opus**: Phase durations given as day ranges (P0: 3–5d, P1: 10–14d, P2: 10–14d, P3: 7–10d, P4: 14–21d). No overall estimate.
- **Haiku**: Phase durations in week ranges (P0: 1–2w, P1: 2–3w, P2: 3–4w, P3: 2–4w, P4: 2–3w). Overall: 10–16 weeks.
- **Impact**: Haiku's estimates are more conservative and realistic for a 0.92-complexity program. Opus's day-level precision implies tighter control but may underestimate integration friction. Haiku explicitly names schedule drivers.

### D-04: Module Placement Recommendations

- **Opus**: Explicit architect recommendation — `silent_success.py` and `audit_lease.py` under `cli/pipeline/`, `smoke_gate.py` under `cli/cli_portify/`, `fidelity_inventory.py` under `cli/roadmap/`.
- **Haiku**: Mentions `silent_success.py` implementation but does not prescribe directory placement.
- **Impact**: Opus provides actionable file-level guidance that reduces ambiguity during implementation. Haiku leaves this to implementers.

### D-05: New File Inventory

- **Opus**: Enumerates exactly 7 new source files and 7 new test files with estimated line counts.
- **Haiku**: Lists workstreams and components but does not provide a file manifest.
- **Impact**: Opus is immediately actionable for sprint planning and code review scoping. Haiku requires a follow-up decomposition step.

### D-06: `reimbursement_rate` Handling

- **Opus**: Lists as "Blocker 6" with binary decision: wire as turn-recovery credit OR remove. Must resolve before Phase 2 GO.
- **Haiku**: Frames as an architect decision to make "immediately" — remove or productize.
- **Impact**: Substantively identical, but Opus ties it to a specific gate (Phase 2 GO) while Haiku treats it as pre-program governance.

### D-07: Shadow Mode Observation Window

- **Opus**: Architect recommendation: "minimum 2-week shadow observation window" — stated as non-negotiable.
- **Haiku**: Identifies shadow window length as a schedule driver but does not prescribe a minimum.
- **Impact**: Opus provides a concrete guardrail. Haiku is more flexible but risks insufficient observation under schedule pressure.

### D-08: Deviation Analysis Placement

- **Opus**: Deviation analysis wiring is Phase 1 (section 1.6), treated as part of the foundation.
- **Haiku**: Also Phase 1 (workstream 4), aligned.
- **Impact**: No practical divergence — both agree this is foundational. Included for completeness since Opus gives it a dedicated subsection while Haiku embeds it in a workstream.

### D-09: Document Structure and Readability

- **Opus**: Uses numbered subsections (0.1–0.4, 1.1–1.6, etc.) with inline FR/NFR/SC traceability codes throughout. Go/no-go criteria as checklists per phase.
- **Haiku**: Uses narrative workstream descriptions with milestone labels (M0.1, M1.1, etc.). Validation strategy organized by concern type (Foundation, Integration, Reliability, Governance, Rollout).
- **Impact**: Opus is optimized for requirement traceability and sprint-level task extraction. Haiku is optimized for architectural communication and stakeholder alignment.

### D-10: Risk Table Granularity

- **Opus**: 12 risks (4 HIGH, 6 MEDIUM, 2 LOW) with owner column and specific mitigations.
- **Haiku**: 12 risks (5 high, 5 medium, 2 governance) with narrative mitigations, no explicit owner assignment in the risk table.
- **Impact**: Opus is more actionable for risk tracking. Haiku's governance-risk category is a useful framing absent from Opus.

### D-11: Success Criteria Organization

- **Opus**: Full SC-001 through SC-016 validation matrix with phase mapping and test method per criterion.
- **Haiku**: Groups success criteria by concern domain (build correctness, determinism, structural readiness, operational policy) with recommended test suite types.
- **Impact**: Opus enables direct test-to-requirement traceability. Haiku provides better conceptual grouping for test strategy design.

### D-12: Sequencing Guardrails

- **Opus**: Guardrails embedded in go/no-go checklists per phase.
- **Haiku**: Four explicit sequencing guardrails stated as rules at the end of the timeline section (e.g., "Do not start Phase 2 until P0-A fixes are verified").
- **Impact**: Haiku's standalone guardrails are easier to enforce as policy. Opus's embedded checklists are more granular but require reading each phase to extract the constraints.

---

## 3. Areas Where One Variant Is Clearly Stronger

### Opus is stronger in:
- **Implementation specificity**: File manifest with line estimates, module placement recommendations, exact regex pattern names — directly usable for sprint planning
- **Requirement traceability**: Every subsection maps to FR/NFR/SC codes, making audit and compliance straightforward
- **Naming collision awareness**: Explicitly calls out the `GateResult` duplication as a "canary" for broader naming audit
- **Go/no-go granularity**: Per-phase checklists with specific test names

### Haiku is stronger in:
- **Strategic framing**: Architectural priorities numbered 1–5 provide clear decision-making hierarchy
- **Timeline realism**: Week-level estimates with named schedule drivers and an overall program range (10–16 weeks)
- **Validation strategy organization**: Concern-based grouping (Foundation/Integration/Reliability/Governance/Rollout) is more useful for test planning
- **Governance risk treatment**: Explicitly categorizes scope creep and unowned blockers as governance risks, not just technical risks
- **Sequencing guardrails**: Standalone rules are easier to enforce as program policy

---

## 4. Areas Requiring Debate to Resolve

1. **G-012 phase placement (D-01)**: Should the smoke gate be built standalone in Phase 1 (Opus) or integrated alongside its infrastructure in Phase 2 (Haiku)? Opus enables earlier unit testing but may require rework when wiring. Haiku reduces rework but delays validation.

2. **TUI timing (D-02)**: Should TUI work wait until after integration (Opus/Phase 3) or ship alongside it (Haiku/Phase 2)? Depends on whether operator feedback is needed during integration or whether integration stability is needed for TUI design.

3. **Shadow window minimum (D-07)**: Should the 2-week minimum be a hard constraint (Opus) or left to Reliability Owner discretion (Haiku)? Opus is safer but may conflict with delivery pressure.

4. **Document format for downstream consumption (D-09)**: The team should decide whether FR/NFR inline tracing (Opus) or concern-based validation grouping (Haiku) better serves their sprint planning and QA processes. A merged approach — Opus's traceability with Haiku's validation strategy organization — may be optimal.

5. **Timeline granularity (D-03)**: Day-level estimates (Opus) vs. week-level with schedule drivers (Haiku). For a 0.92-complexity program spanning 10+ weeks, week-level with explicit uncertainty drivers is likely more honest, but day-level may be needed for sprint commitments within phases.
