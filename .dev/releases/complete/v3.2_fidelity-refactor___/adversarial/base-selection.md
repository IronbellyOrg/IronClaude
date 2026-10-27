# Base Selection: Spec-Fidelity Resolution

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (Amend Spec) | Variant B (Amend Roadmap) | Variant C (Regenerate) |
|--------|--------|------------------------|---------------------------|------------------------|
| Requirement Coverage (resolves all 3 HIGHs) | 0.30 | 1.00 (all 3) | 1.00 (all 3) | 0.33 (probabilistic) |
| Internal Consistency | 0.25 | 1.00 (no contradictions) | 0.75 (whitelist gap acknowledged) | 0.50 (may re-introduce) |
| Specificity Ratio | 0.15 | 1.00 (3 specific edits named) | 0.80 (edits identified but cascade unclear) | 0.20 (no specific actions) |
| Dependency Completeness | 0.15 | 1.00 (spec→roadmap pipeline clear) | 0.70 (cascade effects unresolved) | 0.30 (depends on LLM output) |
| Approach Coverage | 0.15 | 1.00 | 0.80 | 0.50 |
| **Quant Score** | | **0.97** | **0.82** | **0.37** |

## Qualitative Scoring (50% weight) — Quick Rubric (10 criteria)

| Criterion | A | B | C |
|-----------|---|---|---|
| Addresses all 3 HIGH deviations | MET | MET | NOT MET |
| Deterministic outcome | MET | MET | NOT MET |
| Evidence-based rationale | MET | MET | NOT MET |
| Low cascade risk | MET | NOT MET | NOT MET |
| Preserves roadmap quality | MET | NOT MET | NOT MET |
| Resolves MEDIUM deviations as side effect | MET | NOT MET | NOT MET |
| Actionable without rework | MET | MET | MET |
| Validated by spec-fidelity report itself | MET | NOT MET | NOT MET |
| Sustainable process precedent | NOT MET | MET | NOT MET |
| Time-efficient | MET | NOT MET | MET |
| **Qual Score** | **0.90** | **0.50** | **0.30** |

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | Combined | Rank |
|---------|---------------|--------------|----------|------|
| **A: Amend Spec** | 0.485 | 0.450 | **0.935** | **1st** |
| B: Amend Roadmap | 0.410 | 0.250 | 0.660 | 2nd |
| C: Regenerate | 0.185 | 0.150 | 0.335 | 3rd |

## Tiebreaker
Not required. Margin between 1st and 2nd: 27.5% (well above 5% threshold).

## Selected Base: Variant A (Amend Spec)

**Selection Rationale**: Variant A wins decisively across all scoring dimensions. It is deterministic, targets the root cause (spec underspecification), and is validated by the spec-fidelity report's own assessment. The roadmap's OQ resolutions respond to the spec's own Open Questions section — making this an amendment, not an override.

**Strengths to Preserve**:
- 3 targeted spec edits with zero ambiguity
- Resolves MEDIUM deviations (DEV-004 through DEV-008) as cascade effect
- Maintains roadmap quality (better observability, complete FPR mitigation, pragmatic v1.0 scoping)

**Process Note on Variant B's Valid Concern**: Variant B raised a legitimate process point about spec authority. The mitigating factor is that the spec contained an explicit Open Questions section inviting resolution. The roadmap answered those questions. Amending the spec to incorporate those answers is the correct process — the spec should evolve, not be frozen when it explicitly asked for input.
