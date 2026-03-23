---
base_variant: "A (Opus-Architect)"
variant_scores: "A:81 B:76"
---

# Base Selection: v3.1 Anti-Instinct Gate Roadmap

## 1. Scoring Criteria (Derived from Debate)

The debate surfaced seven evaluation dimensions:

| # | Criterion | Weight | Rationale |
|---|-----------|--------|-----------|
| C1 | **Structural clarity & implementability** | 20% | Solo implementer needs unambiguous build sequence |
| C2 | **Phase granularity (right-sized)** | 15% | Debate points D-01/D-02 — ceremony vs. risk reduction |
| C3 | **Timeline precision & honesty** | 10% | D-03 — units must communicate scope clearly |
| C4 | **Technical correctness** | 20% | Module specs, gate semantics, wiring accuracy |
| C5 | **Risk management** | 15% | Identified risks, mitigations, merge coordination |
| C6 | **Validation coverage** | 10% | Testing strategy completeness and traceability |
| C7 | **Operational safety** | 10% | Rollout mode semantics, backward compat, off=off |

## 2. Per-Criterion Scores

### C1: Structural Clarity & Implementability (weight: 20%)

| | A (Opus) | B (Haiku) |
|---|----------|-----------|
| Score | **88** | 78 |

**A**: 4 phases, each with clear goal/milestone/validation gate. Work items are concrete and requirement-tagged. An implementer can start coding from Phase 1.1 immediately.

**B**: 6 phases + Phase 0. More sections (resource requirements, architect recommendations) add documentation value but dilute actionability. Phase 5 and 6 split what is logically one observation period.

### C2: Phase Granularity (weight: 15%)

| | A (Opus) | B (Haiku) |
|---|----------|-----------|
| Score | **82** | 72 |

**A**: 4 phases maps cleanly to the build sequence. The debate convergence (section "Areas of Partial Convergence" #7) explicitly recommends resolving OQ-005/OQ-010 as day-1 tasks within Phase 1 rather than a separate phase — matching A's structure.

**B**: Phase 0 was the central debate point. B's own rebuttal couldn't overcome the convergence recommendation against it. Phase 3 (prompt-only, 0.5-1 day) and Phase 5/6 split add phases without proportionate value.

### C3: Timeline Precision (weight: 10%)

| | A (Opus) | B (Haiku) |
|---|----------|-----------|
| Score | 62 | **82** |

**A**: Sprint-based estimates with undefined sprint length. Debate convergence explicitly sided with day-based estimates for build phases. "6-10 sprints" total range is too wide.

**B**: Day-based estimates (8-12 working days for build). Clear, actionable, forces scope scrutiny. Opus conceded this point in Round 2.

### C4: Technical Correctness (weight: 20%)

| | A (Opus) | B (Haiku) |
|---|----------|-----------|
| Score | **85** | 83 |

Both are technically near-identical on module specs, dataclasses, file structure, and gate semantics (debate convergence area #1). A edges ahead with more specific implementation detail per work item (e.g., explicit regex compilation notes, dual-condition discharge matching specifics in 1.1). B's requirement coverage matrix is a useful addition but doesn't change correctness.

### C5: Risk Management (weight: 15%)

| | A (Opus) | B (Haiku) |
|---|----------|-----------|
| Score | **82** | 78 |

**A**: Tabular risk assessment with phase mapping, clear HIGH/MEDIUM/LOW tiers, explicit mitigations. Includes merge conflict risk with WIRING_GATE.

**B**: Similar risk identification but narrative format is harder to scan. Adds resource/staffing section (3-role breakdown) which is informative but somewhat theoretical for a solo-implementer project.

### C6: Validation Coverage (weight: 10%)

| | A (Opus) | B (Haiku) |
|---|----------|-----------|
| Score | 75 | **88** |

**B**: Cross-cutting taxonomy (A: unit, B: integration, C: sprint-mode, D: regression, E: non-functional) with three explicit checkpoints (A/B/C). The debate convergence (#12) explicitly recommends adopting B's taxonomy. Requirement coverage matrix provides full traceability.

**A**: Phase-aligned testing is simpler but misses the coverage analysis dimension. No explicit checkpoints beyond per-phase validation gates.

### C7: Operational Safety (weight: 10%)

| | A (Opus) | B (Haiku) |
|---|----------|-----------|
| Score | **85** | 72 |

**A**: `off` means zero computation — simpler, safer, more debuggable. Debate convergence (#11) explicitly recommends Opus's strict `off` semantics.

**B**: `off` with conditional metrics evaluation blurs semantics. B conceded this is "a judgment call, not a structural disagreement" in Round 2. The hidden dependency on metrics infrastructure in `off` mode is a legitimate concern A raised.

## 3. Overall Scores

| Criterion | Weight | A (Opus) | B (Haiku) |
|-----------|--------|----------|-----------|
| C1: Structural clarity | 20% | 88 | 78 |
| C2: Phase granularity | 15% | 82 | 72 |
| C3: Timeline precision | 10% | 62 | 82 |
| C4: Technical correctness | 20% | 85 | 83 |
| C5: Risk management | 15% | 82 | 78 |
| C6: Validation coverage | 10% | 75 | 88 |
| C7: Operational safety | 10% | 85 | 72 |
| **Weighted total** | | **81.2** | **78.0** |

**A wins on structure, granularity, correctness, risk, and operational safety. B wins on timeline precision and validation coverage.** The debate's own synthesis recommendation aligns with A-as-base: "use Opus's 4-phase structure with Haiku's additions."

## 4. Base Variant Selection Rationale

**Variant A (Opus-Architect)** is the base because:

1. **The debate convergence explicitly recommends it** — "merged roadmap should use Opus's 4-phase structure" (synthesis recommendation).
2. **Higher implementability** — 4 clean phases with per-section work items that can be executed directly.
3. **Correct `off` semantics** — the debate resolved this dispute in A's favor.
4. **No Phase 0 ceremony** — convergence agreed to fold OQ resolution into Phase 1 day-1, matching A's approach.

## 5. Specific Improvements to Incorporate from B (Haiku)

These are the elements the merge must pull from B, per debate convergence:

| # | Element from B | Where to integrate | Debate reference |
|---|---------------|-------------------|-----------------|
| 1 | **Day-based timeline estimates** for build phases (keep sprint-based for Phase 4 observation) | Replace A's sprint estimates in Phases 1-3 | Convergence #8; A conceded in Round 2 |
| 2 | **Cross-cutting validation taxonomy** (A: unit, B: integration, C: sprint-mode, D: regression, E: non-functional) | Add as documentation overlay to A's phase-aligned testing sections | Convergence #12 |
| 3 | **Three explicit checkpoints** (A: implementation readiness, B: rollout readiness, C: enforcement readiness) | Add as a new section after validation approach | B Phase 5 promotion gate |
| 4 | **Requirement coverage matrix** | Append to A's resource requirements section | B section 6 bottom |
| 5 | **Resource/staffing section** (3 roles: pipeline engineer, QA, architecture reviewer) | Add to A's resource requirements | B section 4 |
| 6 | **Resolve OQ-005 and OQ-010 as day-1 tasks** in Phase 1 | Add explicit work items to Phase 1 opening | Convergence #7 |
| 7 | **Parallelization note**: unit tests alongside module coding is safe | Add to Phase 1 as implementation guidance | Convergence #10; both agreed |
| 8 | **Architect recommendations** (B's 5 numbered recommendations) | Add as closing section — concise, actionable | B section bottom |
