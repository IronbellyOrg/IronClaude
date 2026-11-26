# Base Selection Report

Variants are the two reviewer cards. Variant A = variant-1-original.md (haiku:analyzer). Variant B = variant-2-original.md (opus:qa). Source requirements for requirement_coverage = the 19 requirement-bearing statements of `source.md` listed below. Calibration (C 0.61 and C 0.85) is context only and is not a score input. The metrics below were counted by the orchestrator by hand from the card text (the protocol's "deterministic" layer, applied to prose cards); counts are stated so a reader can redo them.

Source requirements used (SPEC line): R1 add scenario regression tests (11, 43); R2 recorded quick, standard and deep runs with actual question/post counts (11); R3 response application shown (11); R4 addition retention shown (11); R5 preserved user flags shown (11); R6 required verification gates (11); R7 re-check the closed state, no reopening or claim writes (11); R8 secret exception stated as a qualification (11); R9 exercise the worker depth paths (20); R10 keep existing tests, add genuinely exercised cases (23); R11 preserve claim posting, staged recommendation and plan-approval boundary (26); R12 runs load the revised skill, not a stale copy (27); R13 revisit the estimate if interception is unavailable, no self-testing second copy (35); R14 the seven named scenarios (43); R15 GitHub writes intercepted, no live test issue without asking the lead (43); R16 say so with file and line when a criterion is already delivered (43); R17 base branch integration, `Refs #834` unless all delivered (43); R18 start from origin/integration in this worktree (43); R19 do only what 852 left undone (43).

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (haiku:analyzer) | Variant B (opus:qa) |
|--------|--------|----------------------------|---------------------|
| requirement_coverage | 0.30 | 0.368 (7 of 19: R1, R2, R7, R10, R13, R14, R19) | 0.947 (18 of 19; R4 only via "additions-only") |
| internal_consistency | 0.25 | 0.867 (2 contradictions in about 15 claims: "Blocking" label with MEDIUM severity in rows 2 and 3) | 0.981 (1 contradiction in about 54 claims: row 9 against the rule text) |
| specificity_ratio | 0.15 | 0.90 (hand count, about 30 concrete to 3 vague) | 0.95 (hand count, about 150 concrete to 8 vague) |
| dependency_completeness | 0.15 | 0.625 (5 of 8; "Units 1, 14 and 15" is not defined in the card) | 0.545 (12 of 22; "card C12", "card C9" and the INF-nnn rows are not defined in the card) |
| section_coverage | 0.15 | 1.00 (3 of 3 H2) | 1.00 (3 of 3 H2) |
| **quant_score** | | **0.706** | **0.903** |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Verdict form: MET (1) or NOT MET (0), with the CEV evidence in brief.

### Completeness (5)
| Criterion | A | Evidence | B | Evidence |
|---|---|---|---|---|
| Covers all explicit requirements | NOT MET | 7 of 19 (V1:19-21) | MET | 18 of 19 (V2:20-37, 41-43) |
| Edge cases and failure scenarios | NOT MET | none | MET | hung-run scenario, secret case (V2:21, 25, 37) |
| Dependencies and prerequisites | NOT MET (pass 2) | restates "Task 5 depends on Task 4" only (V1:20) | MET | ordering rows 10, 11 (V2:29-30) |
| Success/completion criteria | NOT MET | none | MET | "can each acceptance check pass or fail" (V2:53-58) |
| Out-of-scope stated | MET | V1:37 (nothing run) | MET | V2:68 |
| **Subtotal** | **1/5** | | **5/5** | |

### Correctness (5)
| Criterion | A | Evidence | B | Evidence |
|---|---|---|---|---|
| No factual errors or hallucinated claims | NOT MET | "Regression" for a pre-execution gap; "already closed" placed at PLAN:24 (it is at PLAN:195) | NOT MET | row 9 against CREATE:86; row 14 gives line 82 for a rule at line 84 |
| Feasible approaches | NOT MET | proposes none | MET | fixes given per row (V2:66) |
| Terminology consistent | MET | V1 uses Blocking/Missing consistently in prose | MET | V2 consistent |
| No internal contradictions | NOT MET | Blocking label with MEDIUM severity (V1:20-21) | MET | V2 counts agree (16 Drift, 1, 1) |
| Claims supported by evidence | MET | file:line on each row | MET | file:line on each row |
| **Subtotal** | **2/5** | | **4/5** | |

### Structure (5)
Both MET on all five (ordered sections, consistent hierarchy, separation of deviations, summary and notes, cross-references through the path legend, the card form). **A 5/5, B 5/5.**

### Clarity (5)
| Criterion | A | B |
|---|---|---|
| Unambiguous language | MET | MET |
| Concrete | MET | MET |
| Clear section purpose | MET | MET |
| Terms defined on first use | MET | NOT MET (AC4, INF-007, C9 not defined in the card) |
| Actionable next steps | NOT MET (no fix named) | MET (V2:66) |
| **Subtotal** | **4/5** | **4/5** |

### Risk Coverage (5)
| Criterion | A | B |
|---|---|---|
| At least 3 risks with probability and impact | NOT MET | NOT MET (impacts stated, probabilities not) |
| Mitigation per risk | NOT MET | MET |
| Failure modes and recovery | NOT MET | MET |
| External dependencies and their failure | NOT MET | MET (print-mode question tool, user config, V2:68) |
| Monitoring or validation mechanism | NOT MET | MET (expected post count, secret check, V2:66) |
| **Subtotal** | **0/5** | **4/5** |

### Invariant & Edge Case Coverage (5)
| Criterion | A | B |
|---|---|---|
| Collection boundaries (empty, single, max) | MET (empty, mixed, multiple notes, V1:19) | MET (V2:23, 34-36) |
| State interactions across component boundaries | NOT MET | MET (installed vs `src/` copy, staged artifacts, V2:25, 33) |
| Guard condition gaps | NOT MET | MET (V2:21-22, 25) |
| Count divergence | NOT MET | MET (17-test count, V2:55) |
| Interaction effects | NOT MET | MET (ordering of Tasks 9, 10, 11, V2:29-30) |
| **Subtotal** | **1/5** | **5/5** |

### Qualitative Summary
| Dimension | A | B |
|---|---|---|
| Completeness | 1/5 | 5/5 |
| Correctness | 2/5 | 4/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 0/5 | 4/5 |
| Invariant & Edge Case Coverage | 1/5 | 5/5 |
| **qual_score** | **13/30 = 0.433** | **27/30 = 0.900** |

### Edge Case Floor Check
Both variants score at least 1/5 on Invariant & Edge Case Coverage (A 1/5, B 5/5): both eligible.

## Position-Bias Mitigation

Pass 1 evaluated A then B; pass 2 evaluated B then A, both by the orchestrator in one sitting (so this mitigates order effects only, not evaluator bias).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Completeness: dependencies and prerequisites | A | MET | NOT MET | DISAGREE | NOT MET (the card restates the plan's dependency; it analyses none) |
| Clarity: terms defined on first use | B | NOT MET | NOT MET | AGREE | NOT MET |

Disagreements re-evaluated: 1. Final verdicts changed: 1 (A Completeness 2/5 to 1/5; A's qual_score 14/30 to 13/30).

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (haiku:analyzer) | 0.353 | 0.217 | **0.570** | n/a |
| B (opus:qa) | 0.452 | 0.450 | **0.902** | n/a |

**Margin**: 33.2 points (far above the 5% threshold). **Tiebreaker applied**: No.

## Selected Base: Variant B (opus:qa), reviewer-2-card

### Selection Rationale
Variant B covers 18 of the 19 source requirements against 7, has no more than one internal contradiction against two, and carries the invariant and risk coverage Variant A lacks. The debate agreed: after Round 2 both advocates graded the shared points the same way, and the Round 2.5 fault-finder confirmed that the substance of V2's rows holds while adjusting grades.

### Strengths to Preserve from Base
1. A per-row evidence column with plan and spec line citations and the affected action for each blocking row.
2. The testability pass (which acceptance checks can fail) and the coverage-matrix audit as source for row ordering.
3. The safety row kept open as unverified rather than dismissed.

### Strengths to Incorporate from Non-Base Variants
1. From Variant A, finding 1: the observation that PLAN:81's admission does not supply the missing executable coverage (U-006), folded into M-01.
2. From Variant A, finding 3: the closed-state re-check as a separate row (graded Medium), and the note that SPEC:32-33 links do not resolve, folded into M-04.
3. From Variant A, finding 2: the Missing-label reading of the absent estimate revisit, adopted as the merged grade of M-02.
