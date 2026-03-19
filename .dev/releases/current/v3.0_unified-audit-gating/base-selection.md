---
base_variant: "A (Opus)"
variant_scores: "A:81 B:76"
---

## 1. Scoring Criteria (Derived from Debate)

| # | Criterion | Weight | Source |
|---|-----------|--------|--------|
| C1 | Critical path protection — schedule risk minimization | 20% | D2 (ToolOrchestrator timing), D3 (bundling) |
| C2 | Specification fidelity — requirement coverage completeness | 15% | D6 (LOC/traceability), convergence §1-2 |
| C3 | Integration risk management — blast radius control | 15% | D3 (sprint hot path), D4/D5 (validation) |
| C4 | Actionability — downstream consumability (tasklist, sprint CLI) | 15% | D6 (LOC estimates vs narrative) |
| C5 | Phase sequencing correctness — dependency ordering | 10% | D1 (Phase 0), D2 (plugin timing) |
| C6 | Rollout safety — shadow/soft/full transition rigor | 10% | D4/D5 (validation separation), convergence §3 |
| C7 | Risk assessment calibration — severity accuracy | 10% | D12 (R7 level), risk tables |
| C8 | Scope discipline — avoids unnecessary overhead | 5% | D1 (Phase 0 cost), D7 (phase count) |

## 2. Per-Criterion Scores

| Criterion | A (Opus) | B (Haiku) | Rationale |
|-----------|----------|-----------|-----------|
| **C1: Critical path protection** | 90 | 70 | Opus's late ToolOrchestrator placement (Phase 5, conditional) keeps the critical path clear. Haiku's Phase 2 placement risks blocking Phases 3-6 on a plugin spike. The debate's convergence assessment (§9) confirms this is "the most consequential unresolved disagreement" and Opus's position is the safer default. |
| **C2: Spec fidelity** | 80 | 82 | Haiku identifies two additional open questions (comparator/consolidator scope, rollout ownership) that Opus missed. Both cover the 52 requirements, but Haiku's Phase 0 decision log provides marginally better traceability. |
| **C3: Integration risk** | 75 | 85 | Haiku's separation of sprint (Phase 5) from roadmap (Phase 4) integration is substantive. The debate (D3 rebuttal) correctly notes integration bugs in the sprint hot path aren't mitigated by shadow mode. Opus bundles them, creating a larger blast radius per merge. |
| **C4: Actionability** | 90 | 68 | Opus provides per-task file paths, LOC estimates, and requirement traceability — directly convertible to sprint tasklists. Haiku uses narrative descriptions requiring a translation step. For this project's CLI pipeline (`superclaude sprint run`), Opus's format is materially superior. |
| **C5: Phase sequencing** | 78 | 75 | Both have sound core sequencing. Opus's omission of Phase 0 is debatable but defensible (proposed answers are provided inline). Haiku's early ToolOrchestrator creates a dependency that the debate shows is unnecessary for minimum viability. |
| **C6: Rollout safety** | 72 | 85 | Haiku's separation of validation (Phase 7) from rollout (Phase 8) enforces deliberation between measurement and activation. The debate point about "psychological pressure" in combined phases (D5) is legitimate. Opus combines these into Phase 6 with less structural separation. |
| **C7: Risk calibration** | 82 | 78 | Opus's MEDIUM for R7 with strictly-additive mitigation is pragmatically correct. Haiku's HIGH rating for agent regression is theoretically sound but empirically unvalidated. The convergence assessment (§12) recommends Haiku's mitigation with Opus's rating — favoring Opus's calibration. |
| **C8: Scope discipline** | 85 | 70 | Opus's 6 phases vs Haiku's 9 reduces coordination overhead. The debate (D7) identifies this as team-size dependent, but for this project (likely single/small implementer per CLAUDE.md patterns), fewer phases is more efficient. |

## 3. Overall Scores

| Variant | Weighted Score | Strengths | Weaknesses |
|---------|---------------|-----------|------------|
| **A (Opus)** | **81** | Actionable task format, protected critical path, lean phase structure, accurate risk calibration | Bundles sprint/roadmap integration, combined validation+rollout, skips explicit decision closure |
| **B (Haiku)** | **76** | Superior integration risk separation, rollout deliberation, broader open-question coverage | Early ToolOrchestrator creates schedule risk, narrative format less actionable, 9 phases adds overhead for likely team size |

## 4. Base Variant Selection Rationale

**Variant A (Opus)** is selected as the base for three reasons:

1. **Actionability**: The task-level format with file paths, LOC estimates, and requirement traceability is directly consumable by the project's sprint CLI pipeline. This is the roadmap's primary downstream consumer, and Opus's format eliminates a translation step.

2. **Critical path safety**: The ToolOrchestrator decision is the highest-impact divergence (debate §9). Opus's late/conditional placement is the conservative-correct choice — it ships a working gate regardless of plugin outcome.

3. **Phase efficiency**: 6 phases vs 9 reduces merge windows and coordination overhead. The project's development model (evident from CLAUDE.md) favors leaner structures.

## 5. Specific Improvements to Incorporate from Variant B (Haiku)

### Must incorporate:

1. **Separate sprint from roadmap integration** (Haiku Phases 4-5 → split Opus Phase 3 into 3a/3b). The debate's D3 rebuttal about integration bugs in the sprint hot path not being mitigated by shadow mode is substantive. Sprint integration should validate independently before merging.

2. **Add lightweight decision closure step** (Haiku Phase 0 → compressed to 2-4 hours as the convergence assessment suggests). Include Haiku's two additional open questions (comparator/consolidator scope, rollout ownership for `grace_period`). Not a full phase, but a documented pre-implementation checkpoint.

3. **Separate rollout readiness from activation** (Haiku Phases 7-8 → expand Opus Phase 6 into 6a: calibration/readiness assessment, 6b: activation). The deliberation enforcement argument from D5 is valid — "are we ready?" and "activate it" should be structurally distinct steps.

4. **Adopt Haiku's staged agent validation approach for R7** — implement independent validation of each agent extension with regression tests against prior audit outputs, while keeping Opus's MEDIUM severity rating.

### Consider incorporating:

5. **Haiku's 4-role resource model** (architect, backend engineer, QA, audit workflow owner) as a reference for review assignments, even if a single implementer does the work.

6. **Haiku's explicit "design for auditability" principle** — every enforcement decision explainable from report frontmatter alone. This is a valuable architectural constraint not explicitly stated in Opus.
