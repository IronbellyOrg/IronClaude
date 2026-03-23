---
base_variant: A
variant_scores: 'A:81 B:74'
---

# Scoring Criteria

Derived from the debate's five primary dispute axes (D1, D2, D4, D5, D8/D9) and convergence assessment:

1. **Implementability** — Can an engineer start coding from this roadmap without ambiguity? (weight: 25%)
2. **Spec Fidelity** — Does every requirement/SC have a clear, traceable home? (weight: 20%)
3. **Risk Mitigation Quality** — Are the highest risks (R6, R7) concretely addressed with actionable steps? (weight: 20%)
4. **Phase Granularity Fit** — Is the phase structure appropriate for ~800-1100 LOC, single-implementer scope? (weight: 20%)
5. **Actionability of Open Questions** — Does the roadmap give the implementer concrete decisions vs. deferring to a process? (weight: 15%)

---

# Per-Criterion Scores

| Criterion | Variant A (Opus) | Variant B (Haiku) | Notes |
|-----------|-----------------|-------------------|-------|
| **Implementability** (25%) | **88** | 70 | A provides LOC estimates per item, concrete file paths, and inline test counts. B assumes role separation (4 engineering roles) that doesn't match the solo-implementer reality. B's Phase 0 blocks all coding on a decision session. |
| **Spec Fidelity** (20%) | **85** | **85** | Tie. Both map all 15 SCs. A provides an explicit SC→Phase→Test-Type table. B embeds SC references inline per phase. Both achieve full coverage. |
| **Risk Mitigation** (20%) | 78 | **82** | B's Phase 6 rollout milestones (M12-M14) directly address R6 validation in production — the debate's strongest Haiku argument. A's R6 mitigation relies on SC-011 warning + Phase 4 retrospective, which is weaker for the highest-severity risk. |
| **Phase Granularity** (20%) | **85** | 68 | A's 4-phase structure is right-sized. As A argued in Round 2: phase transitions for a solo implementer reviewing their own work are ceremony. B's 7 phases create 6 transition boundaries; Phase 0 and Phase 6 add calendar time without proportional engineering value for the v1.0 scope. |
| **Open Question Actionability** (15%) | **82** | 65 | A provides 10 numbered recommendations with specific stances (approve/defer/block). B absorbs all into Phase 0 without individual recommendations — the implementer gets a process, not answers. Debate Round 1/D9 validates this: A's recommendations are immediately usable. |

---

# Overall Scores

| Variant | Weighted Score | Justification |
|---------|---------------|---------------|
| **A (Opus)** | **81** | Superior implementability, right-sized granularity, actionable open-question treatment. The roadmap can be handed to an engineer who starts Phase 1 today. Weakness: rollout validation is underspecified. |
| **B (Haiku)** | **74** | Stronger rollout risk mitigation and validation checkpoints per phase. Weakness: over-engineered for scope (assumes 4 roles, 7 phases for ~1000 LOC), Phase 0 delays delivery without proportional risk reduction, open questions lack concrete recommendations. |

---

# Base Variant Selection Rationale

**Variant A** is the base because:

1. **Actionable now** — An implementer can begin Phase 1 immediately using A's inline recommendations for open questions. B requires a separate decision session before any code is written.

2. **Right-sized structure** — The debate established this is ~800-1100 LOC with a single-implementer profile. A's 4-phase model maps to natural engineering milestones. B's 7-phase model optimizes for a multi-person team that doesn't exist.

3. **Superior traceability** — A's SC validation map (Section: Success Criteria Validation Map) is a single table mapping all 15 SCs to phases, test types, and gates. This is immediately auditable.

4. **Concrete detail** — LOC estimates per milestone item, test counts per phase, file-level modification tracking. B is more narrative and less tabular.

---

# Improvements to Incorporate from Variant B

The following B elements should be merged into the A base:

1. **Rollout validation milestones (B's Phase 6, M12-M14)** — Add as a "Phase 5: Rollout Validation" appendix or post-merge checklist. B's argument that R6 can only be fully validated during rollout is correct (debate D5, Round 2). Include the three concrete milestones: shadow baseline collection, soft-mode readiness criteria, blocking-mode authorization gates. Frame as engineering validation, not operational runbook.

2. **Per-phase validation checkpoints (B's Section 5 "Validation checkpoints by phase")** — Add exit criteria after each of A's 4 phases. B's structure of "After Phase N, verify X" is lightweight and catches problems earlier than A's consolidation-in-Phase-4 approach. This addresses B's valid rebuttal in D4 Round 2.

3. **Explicit Phase 2 prerequisites from open questions** — B correctly argues that Opus's "2.0 [BLOCKER] Validate SprintGatePolicy constructor" is effectively spec closure happening mid-implementation (debate D2, Round 2 rebuttal). Promote OQ-2 (budget constants) and OQ-6 (SprintGatePolicy) to explicit Phase 2 entry prerequisites with a "resolve before starting Phase 2" gate, rather than inline blockers.

4. **`analysis_complete` degraded-state as observability event** — B's R2 recommendation ("treat degraded analysis as an observability event, not a silent skip") is more precise than A's treatment. Incorporate this language into A's Milestone 1.2 constraints.

5. **Coordination strategy for `roadmap/gates.py`** — B's dependency handling strategy section is more explicit about cross-branch coordination mechanics. Merge B's "sequence edits carefully" guidance into A's Phase 3 Milestone 3.2 coordination note.
