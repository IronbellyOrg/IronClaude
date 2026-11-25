# Base Selection Report

Limitations: one evaluator scored both variants and also authored them. The reverse-order second pass was not run by an independent evaluator; see Position-Bias Mitigation. Inputs: the two variants, `diff-analysis.md`, `debate-transcript.md`.

## Quantitative Scoring (50% weight)

Source requirements (from the user's request, section-level matching): (1) where sub-agents are spawned, (2) where a refactor would land, (3) pros and cons, (4) a worth-it recommendation.

| Metric | Weight | Variant A (keep Task) | Variant B (Orca orchestrator) |
|--------|--------|-----------------------|-------------------------------|
| requirement_coverage | 0.30 | 0.75 (3 of 4 clear; spawn map relies on the opportunity map) | 0.70 (cons only appear as mitigations) |
| internal_consistency | 0.25 | 1.00 (0 contradictions in ~14 claims) | 0.86 (X-001 and X-002 in ~14 claims) |
| specificity_ratio | 0.15 | 0.88 (14 concrete, 2 vague) | 0.67 (8 concrete, 4 vague) |
| dependency_completeness | 0.15 | 1.00 (external refs excluded) | 1.00 (external refs excluded) |
| section_coverage | 0.15 | 1.00 (3 H2) | 1.00 (3 H2) |
| **quant_score** | | **0.907** | **0.826** |

## Qualitative Scoring (50% weight): Additive Binary Rubric

Every MET cites evidence from the variant; no evidence means NOT MET.

### Completeness (5)
| Criterion | A | Evidence | B | Evidence |
|-----------|---|----------|---|----------|
| Covers all explicit requirements | MET | Case points 1-6 plus "What to do instead" | MET | Claim, case, mitigation |
| Edge cases and failures | MET | Point 4: Orca receipt is not proof of work | MET | Fallback when `orca --version` fails |
| Dependencies and prerequisites | MET | Point 3: Orca may be absent elsewhere | MET | Orca worktree and CLI check |
| Success criteria | NOT MET | none stated | NOT MET | none stated |
| Out of scope | NOT MET | none stated | MET | "No change to scoring, merge or return contract" |
| **Subtotal** | **3/5** | | **4/5** | |

### Correctness (5)
| Criterion | A | Evidence | B | Evidence |
|-----------|---|----------|---|----------|
| No factual errors | MET | Thresholds and "5-wave" defect verified | NOT MET | X-001: retry claim is false |
| Feasible with constraints | MET | Keeps Task fan-out (WC-7) | NOT MET | In-skill `worker-start` violates WC-8 |
| Terminology consistent | MET | S1-S5 used consistently | MET | same |
| No internal contradictions | MET | none found | NOT MET | X-002: point 2 vs point 6 |
| Claims supported | MET | file:line citations | NOT MET | no repo citations (S-001) |
| **Subtotal** | **5/5** | | **1/5** | |

### Structure (5)
| Criterion | A | B |
|-----------|---|---|
| Logical ordering | MET | MET |
| Consistent hierarchy | MET | MET |
| Separation of concerns | MET | MET |
| Navigation aids | MET (file refs) | NOT MET |
| Artifact-type conventions | MET | MET |
| **Subtotal** | **5/5** | **4/5** |

### Clarity (5)
| Criterion | A | B |
|-----------|---|---|
| Unambiguous language | MET | NOT MET ("coarser telemetry") |
| Concrete over abstract | MET | NOT MET ("full tools") |
| Clear section purpose | MET | MET |
| Terms defined on first use | NOT MET (S2-S5 undefined) | NOT MET (S1-S3 undefined) |
| Actionable next steps | MET | MET |
| **Subtotal** | **4/5** | **2/5** |

### Risk Coverage (5)
| Criterion | A | B |
|-----------|---|---|
| 3+ risks with probability and impact | NOT MET | NOT MET |
| Mitigation per risk | NOT MET | MET (mitigation section) |
| Failure modes and recovery | NOT MET (names risk, no recovery) | MET (fallback, verify on disk) |
| External dependency failures | MET (Orca absent) | MET |
| Monitoring or validation mechanism | NOT MET | MET (verify file on disk) |
| **Subtotal** | **1/5** | **4/5** |

### Invariant & Edge Case Coverage (5)
| Criterion | A | B |
|-----------|---|---|
| Collection boundaries | NOT MET | NOT MET |
| State across component boundaries | MET (kill rule needs Task usage report) | MET (parent state vs files) |
| Guard condition gaps | MET (threshold mismatch) | MET (verify file, not signal) |
| Count divergence | MET ("5-wave" vs six steps) | NOT MET |
| Interaction effects | MET (shared skill callers) | NOT MET |
| **Subtotal** | **4/5** | **2/5** |

Edge Case Floor Check: A 4/5 and B 2/5 both meet the 1/5 floor; both eligible.

### Qualitative Summary
| Dimension | A | B |
|-----------|---|---|
| Completeness | 3/5 | 4/5 |
| Correctness | 5/5 | 1/5 |
| Structure | 5/5 | 4/5 |
| Clarity | 4/5 | 2/5 |
| Risk Coverage | 1/5 | 4/5 |
| Invariant & Edge Case | 4/5 | 2/5 |
| **qual_score** | **22/30 = 0.733** | **17/30 = 0.567** |

## Position-Bias Mitigation

Pass 1 (A then B) is the table above. Pass 2 (B then A) was re-read against the same evidence by the same evaluator, not independently. Verdict changes on re-read: 0. Disagreements re-evaluated: 0. This is a known weakness: an independent second pass was not run, and the result may carry the evaluator's own bias because it also wrote both variants.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (keep Task) | 0.454 | 0.367 | **0.820** | not needed |
| B (Orca orchestrator) | 0.413 | 0.283 | **0.696** | not needed |

**Margin**: 12.4 points (above the 5% threshold)
**Tiebreaker applied**: No

## Selected Base: Variant A (keep Task sub-agents)

### Selection Rationale
A wins on correctness (5/5 against 1/5): B's retry claim is false, its context benefit does not follow from its own staging plan, and its core mechanism violates WC-8 and WC-13. Margin 0.124.

### Strengths to Preserve from Base
1. Task fan-out stays inside the commands (WC-7).
2. Evidence-cited reasoning (file:line).
3. Verified spec defects: token thresholds (`SKILL.md:238-239` against `refs/agent-spec-builder.md`) and "5-wave" against six steps.
4. `sc-bare-review` as the no-Orca route to other model families.

### Strengths to Incorporate from Non-Base Variants
1. From B (C-006, C-007, C-008): the observability, isolation and resume goals, delivered at the coordinator layer (one `/sc:brainstorm --unattended` worker per Task), not inside the skills.
2. From B (U-004): verify the result file on disk, citing WC-4.
3. From the debate (A-001, A-004): the unit to spawn is the whole command; nothing in the skills calls Orca.
4. From the debate (A-003): measure worker cold-start time and cost before committing.
