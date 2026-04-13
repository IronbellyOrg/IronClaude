---
base_variant: "roadmap-opus-architect"
variant_scores: "A:82 B:68"
---

## 1. Scoring Criteria (Derived from Debate)

The debate surfaced four contested dimensions plus several implicit quality factors. Scoring uses 7 criteria weighted by relevance to the spec's constraints (0.45 complexity, solo implementer, content fidelity task):

| # | Criterion | Weight | Source |
|---|-----------|--------|--------|
| C1 | Executability — can an implementer/agent follow without re-interpretation | 20% | D3 (granularity debate) |
| C2 | Safety — risk of content loss or silent error propagation | 20% | D2 (verification ordering) |
| C3 | Efficiency — minimal overhead for a 0.45-complexity solo task | 15% | D1 (Phase 0), D4 (effort) |
| C4 | Traceability — FR/NFR coverage visible per step | 15% | D3 (requirement IDs) |
| C5 | Pipeline compatibility — consumable by sc:tasklist and sprint CLI | 10% | D4 (effort units) |
| C6 | Completeness — all spec requirements addressed | 10% | Both variants claim full coverage |
| C7 | Integration clarity — wiring/dispatch mechanisms explicit | 10% | Convergence point 5 |

---

## 2. Per-Criterion Scores

### C1: Executability (weight 20%)

| Aspect | Variant A (Opus) | Variant B (Haiku) |
|--------|-----------------|------------------|
| Step granularity | 47 steps with sub-steps, line numbers, exact counts | ~20 actions, abstract targets ("400-500 lines") |
| Ambiguity | Near-zero — each step specifies input, action, verification | Moderate — "Trim SKILL.md to behavioral protocol only" requires judgment |
| Agent-readiness | High — checklistable by automated executor | Low — requires content understanding to interpret |

**Score**: A: 90, B: 60

The debate's convergence section acknowledged: "automated agent → Opus; experienced human → Haiku." Given that this roadmap feeds into `sc:tasklist` for potential agent execution, Opus's granularity is the correct default.

### C2: Safety (weight 20%)

| Aspect | Variant A (Opus) | Variant B (Haiku) |
|--------|-----------------|------------------|
| Verification ordering | Dedicated Phase 1 blocking gate before any edits | Integrated into Phase 2 alongside edits |
| Per-step checks | Every step has explicit verification column | Phase-level milestones only |
| Rollback | Explicit git checkout command documented | Implicit (assumes git knowledge) |

**Score**: A: 88, B: 62

Opus's verify-first approach directly addresses the debate's central safety concern: the v1 implementation left refs in an unknown fidelity state. Haiku's "quick diff at Phase 2 start" is reasonable but loses the isolation benefit. The debate convergence recommended Opus's ordering.

### C3: Efficiency (weight 15%)

| Aspect | Variant A (Opus) | Variant B (Haiku) |
|--------|-----------------|------------------|
| Phase count | 4 phases (no Phase 0) | 5 phases (includes Phase 0 baseline) |
| Overhead | Dedicated verification phase (30-45 min) but no governance ceremony | Phase 0 governance + acceptance matrix creation |
| Total effort | 3.25-4.75 hours (concrete) | 3 Sprint Slots (abstract) |

**Score**: A: 80, B: 65

Phase 0 was identified in the debate as "ceremony without substance" for a solo executor on a 0.45-complexity task. Haiku's acceptance matrix duplicates Opus's Phase 4 success criteria table. Opus's verification phase has concrete output (confirmed refs); Haiku's Phase 0 produces documentation artifacts.

### C4: Traceability (weight 15%)

| Aspect | Variant A (Opus) | Variant B (Haiku) |
|--------|-----------------|------------------|
| FR mapping | Per-step "Requirements Addressed" column in every phase table | Phase-level "Owned requirements" lists |
| Coverage visibility | Can verify any FR is addressed by scanning step tables | Must read action descriptions to confirm coverage |
| Gap detection | Missing FR would be visible as absent from step tables | Missing FR could hide inside vague action descriptions |

**Score**: A: 78, B: 75

Both provide FR traceability, but at different resolutions. Haiku's phase-level requirement lists are cleaner to scan; Opus's per-step mapping is more auditable. Close score — Haiku's approach is actually slightly more readable, but Opus's is more verifiable.

### C5: Pipeline Compatibility (weight 10%)

| Aspect | Variant A (Opus) | Variant B (Haiku) |
|--------|-----------------|------------------|
| Effort units | Hours only | Sprint Slots only |
| Frontmatter | Complete (total_phases, milestones, effort, critical_path) | Minimal (spec_source, complexity, persona) |
| Pipeline consumption | Needs Sprint Slot conversion | Native Sprint Slots but no hour guidance |

**Score**: A: 70, B: 72

Slight edge to Haiku on native pipeline units, but Opus has richer frontmatter. The debate convergence recommended including both formats. Neither variant does this — both lose points.

### C6: Completeness (weight 10%)

| Aspect | Variant A (Opus) | Variant B (Haiku) |
|--------|-----------------|------------------|
| All FRs addressed | Yes — every FR-PRD-R appears in step tables | Yes — every FR-PRD-R appears in phase ownership |
| All NFRs addressed | Yes — NFR-PRD-R.1-5 covered in Phase 4 | Yes — NFR-PRD-R.1-5 referenced |
| Risk coverage | 9 risks, identical to spec | 9 risks, identical to spec |
| Integration points | 5 named artifacts with embedded table | 5 named artifacts with standalone list |
| Developer Guide reference | Implicit (constraints enforced) | Explicit (listed as dependency #8) |

**Score**: A: 82, B: 80

Near-parity. Haiku's explicit Developer Guide dependency is a minor advantage noted in the debate convergence. Opus's integration table is more accessible during execution.

### C7: Integration Clarity (weight 10%)

| Aspect | Variant A (Opus) | Variant B (Haiku) |
|--------|-----------------|------------------|
| Wiring table format | Embedded 5-column table with owning/consuming phases | Numbered list with cross-reference annotations |
| Mechanism types | Explicitly named (file-load directive, cross-reference path table, Skill invocation, delegation) | Implied through descriptions |
| Consuming phase visibility | Explicit column | Cross-Reference field |

**Score**: A: 85, B: 72

Opus's embedded table with explicit mechanism types and owning/consuming phase columns is directly more useful during execution. The debate convergence agreed on this point.

---

## 3. Overall Scores

| Criterion | Weight | Variant A | Variant B | A Weighted | B Weighted |
|-----------|--------|-----------|-----------|------------|------------|
| C1 Executability | 20% | 90 | 60 | 18.0 | 12.0 |
| C2 Safety | 20% | 88 | 62 | 17.6 | 12.4 |
| C3 Efficiency | 15% | 80 | 65 | 12.0 | 9.75 |
| C4 Traceability | 15% | 78 | 75 | 11.7 | 11.25 |
| C5 Pipeline compat | 10% | 70 | 72 | 7.0 | 7.2 |
| C6 Completeness | 10% | 82 | 80 | 8.2 | 8.0 |
| C7 Integration | 10% | 85 | 72 | 8.5 | 7.2 |
| **Total** | | | | **83.0** | **67.8** |

**Rounded: A: 82, B: 68**

### Justification

Variant A (Opus) wins decisively on the two highest-weighted criteria — executability and safety — which together account for 40% of the score. The 47-step granularity with per-step verification and the dedicated verify-first phase directly address the primary risk identified by both variants and the debate: content fidelity in a decomposition task. Variant B's strengths (pipeline-native units, Developer Guide reference, cleaner requirement grouping) are real but lower-impact, and all are easy to incorporate into Variant A as additions.

---

## 4. Base Variant Selection Rationale

**Selected base: Variant A (roadmap-opus-architect)**

Three decisive factors:

1. **The debate's own convergence recommends it.** The synthesis section explicitly recommended Opus's phase ordering, 47-step granularity as primary plan, embedded integration table, and rollback command — 4 of 5 structural recommendations favor Opus as base.

2. **The task's risk profile favors over-specification.** This is a content fidelity refactoring where the primary failure mode is "missing something." Opus's 47 steps with per-step verification directly counter this risk. Haiku's 20-action flexibility is valuable for experienced humans but introduces interpretation risk for agent executors.

3. **Merge direction is asymmetric.** Adding Haiku's elements (Sprint Slot equivalences, Developer Guide dependency, FR/NFR phase-level groupings) to Opus is additive. Reaching Opus's step-level detail from Haiku's structure would require rewriting the entire plan.

---

## 5. Specific Improvements from Variant B to Incorporate in Merge

| # | Element from Variant B | Where to Add in Variant A | Rationale |
|---|----------------------|--------------------------|-----------|
| 1 | **Sprint Slot equivalences** alongside hours in Phase timeline (Section 6) | Add "Sprint Slot" column to timeline table | Debate convergence: "include both effort formats" |
| 2 | **Developer Guide as explicit dependency** (Haiku dependency #8) | Add row to Section 4 External Dependencies table | Minimal cost, better audit trail per debate |
| 3 | **Phase-level FR/NFR ownership lists** (Haiku's "Owned requirements" headers) | Add as opening annotation to each Opus phase section | Improves scanability without replacing per-step mapping |
| 4 | **"Move, don't improve" rule** (Haiku Risk #4 mitigation phrasing) | Replace Opus R4 mitigation text with this crisper formulation | More memorable and actionable as a working rule |
| 5 | **Phase 0 as optional annotation** for team/review contexts | Add note after Section 1 Executive Summary | Debate convergence: "skip for solo, note as option for teams" |
| 6 | **Stage B Delegation Contract** as named integration artifact (Haiku integration point #4) | Add 6th row to Opus's integration table | Opus omits this pre-existing but relevant wiring point |
