# Base Selection Report

Variants: V1 = reviewer-1 card (analyzer, sonnet); V2 = reviewer-2 card (qa, haiku->glm-5.3); V3 = reviewer-3 card (refactorer, opus). Evaluator: debate-orchestrator. The inputs are YAML reviewer cards, so "sections" are top-level YAML keys and "claims" are the finding claims, the verdict and the self-audit.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 | V2 | V3 |
|--------|--------|----|----|----|
| requirement_coverage | 0.30 | 0.15 (spec sections cited or named: 7, 13, 20 = 3/20) | 0.50 (4, 6, 7, 8, 11, 13, 14, 15, 16, 20 = 10/20) | 0.10 (16, 20 = 2/20) |
| internal_consistency | 0.25 | 1.00 (0 intra-card contradictions / 6 claims) | 1.00 (0 / 7; the self-audit "each maps to a task" covers section 15/16 rows, Q-3 covers section 20, so there is no intra-card conflict) | 1.00 (0 / 9) |
| specificity_ratio | 0.15 | 1.00 (0 vague-term hits) | 1.00 (0) | 1.00 (0) |
| dependency_completeness | 0.15 | 1.00 (internal refs "A-1 and A-2" resolve) | 1.00 (no internal refs) | 1.00 (no internal refs) |
| section_coverage | 0.15 | 0.875 (7/8 top-level keys) | 1.00 (8/8; adds `resolved_model`) | 0.875 (7/8) |
| **quant_score** | | **0.7263** | **0.8500** | **0.7113** |

Computation: spec sections were mapped from the `source.md:N` line citations (lines 76-77 -> section 4; 132 -> 6; 148-159 -> 7; 192-210 -> 8; 282 -> 11; 321 -> 13; 327-342 -> 14; 391 and 400 -> 16; 465-475 -> 20) plus "section N" mentions. Vague-term and key counts come from a deterministic grep over the card files.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

### Completeness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Covers all explicit requirements | NOT MET | Missed A-001 (token) and U-003 | NOT MET | Missed C-001 and A-001 | NOT MET | Missed C-002 and A-001 |
| Edge cases / failure scenarios | MET | A-2 blocked-task halt; A-4 token-set shell | MET | Q-3 closed or assigned-elsewhere ACs | MET | S-1 halt; S-5 stale master |
| Dependencies / prerequisites | MET | A-2 Task 16 depends on 14 and 15 | MET (after re-eval) | Q-2 "Wave 1 precondition" git fetch | MET | S-1; S-2 session started after Task 13 |
| Success / completion criteria | MET | A-1 recommends a per-criterion artifact | MET | Q-3 recommends a pending-AC artifact | MET | S-3 concrete hunk-range check |
| Out-of-scope items | NOT MET | No scope reasoning | MET | Q-1: INF-054 is an authorized exclusion (plan:24) | MET | S-7 Constraints scope (plan:20) |
| **Subtotal** | **3/5** | | **4/5** | | **4/5** | |

### Correctness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| No factual errors | NOT MET | A-1 "items 1-6 have no task" is false for AC 5 (plan:49, plan:215-224); conceded in Round 2 | NOT MET | verdict PASS and self-audit "no ... security risk" are false (C-001, A-001); conceded | MET | S-1..S-7 facts hold; S-4's label is wrong but its facts are true (test_how_we_work_routing_table.py:19, :144) |
| Feasible approaches | MET | Recommendations are executable | MET | Recommendations are executable | MET | Recommendations are executable |
| Consistent terminology | MET | Categories used accurately | NOT MET | Q-4 "weak-match" for a missing requirement (source.md:132) | NOT MET | S-4 "false-claim" for a spec-inherited wording (source.md:391) |
| No internal contradictions | MET | None | MET | None (see IC) | MET | None |
| Claims supported by evidence | MET | file:line on every finding | MET | file:line on every finding | MET | file:line on every finding |
| **Subtotal** | **4/5** | | **3/5** | | **4/5** | |

### Structure (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Logical ordering | MET | verdict, findings (blocking first), audit | MET | verdict, findings, audit | MET | verdict, findings (blocking first), audit |
| Consistent hierarchy | MET | uniform finding schema | MET | uniform | MET | uniform |
| Separation of concerns | NOT MET | A-4 bundles three unrelated items; conceded | MET | one topic per finding | MET | one topic per finding |
| Navigation aids | MET | finding IDs A-1..A-4 | MET | Q-1..Q-5 | MET | S-1..S-7 |
| Artifact conventions | MET | reviewer-card schema | MET | schema plus `resolved_model` | MET | schema |
| **Subtotal** | **4/5** | | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|
| Unambiguous language | MET | MET | MET | 0 vague-term hits in each |
| Concrete | MET | MET | MET | named files, commands, IDs |
| One-sentence purpose per finding | MET | MET | MET | each claim is one sentence |
| Terms defined on first use | NOT MET | NOT MET | NOT MET | "T1 R-1" (V1), "INF-013" (V2), "E-HALT-QA" (V3) and "AC" are undefined |
| Actionable next steps | MET | MET | MET | `recommendation` on every finding |
| **Subtotal** | **4/5** | **4/5** | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| >=3 risks with probability and impact | NOT MET | no probability given | NOT MET | none | NOT MET | none |
| Mitigation per risk | MET | recommendation on each | MET | recommendation on each | MET | recommendation on each |
| Failure modes / recovery | MET | A-2 halt and reorder | NOT MET | none | MET | S-1 halt; S-2 stop and resume |
| External dependency failure | MET | A-2 tier unserved, token missing | NOT MET | none | MET | S-1, S-2 served-model evidence |
| Monitoring / validation mechanism | MET | A-1 static assertions plus artifact | MET | Q-3 pending-AC artifact | MET | S-2 named evidence source |
| **Subtotal** | **4/5** | | **2/5** | | **4/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Collection boundaries | NOT MET | none | NOT MET | none | NOT MET | none |
| State interactions across boundaries | MET | A-2 blocked state halts later tasks | NOT MET | none | MET | S-1; S-2 agents loaded at session start |
| Guard condition gaps | MET | A-4 unset token not forced | MET | Q-4 spawn guard missing from refs | MET | S-6 ASCII/live-reference guard |
| Count divergence | NOT MET | none | NOT MET | none | NOT MET | none |
| Interaction effects | MET | A-2 Tasks 14/15 with 16; A-4 Task 11 with earlier tasks | NOT MET | none | MET | S-3 Tasks 9/10 with 11; S-1 |
| **Subtotal** | **3/5** | | **1/5** | | **3/5** | |

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 3/5 | 4/5 | 4/5 |
| Correctness | 4/5 | 3/5 | 4/5 |
| Structure | 4/5 | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 2/5 | 4/5 |
| Invariant & Edge Case | 3/5 | 1/5 | 3/5 |
| **qual_score** | **22/30 = 0.733** | **19/30 = 0.633** | **24/30 = 0.800** |

### Edge Case Floor Check

| Variant | Invariant & Edge score | Eligible (>= 1/5) |
|---|---|---|
| V1 | 3/5 | yes |
| V2 | 1/5 | yes |
| V3 | 3/5 | yes |

## Position-Bias Mitigation

Pass 1 used input order (V1, V2, V3); Pass 2 used reverse order (V3, V2, V1).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| Completeness: dependencies/prerequisites | V2 | NOT MET | MET | DISAGREE | MET: Q-2 explicitly recommends adding the Wave 1 fetch as a precondition (variant-2 Q-2) |
| Correctness: no factual errors | V1 | NOT MET | MET | DISAGREE | NOT MET: A-1's literal claim is false for AC 5 (plan:49, :215-224), and V1 conceded this in Round 2 |
| Correctness: consistent terminology | V3 | NOT MET | NOT MET | AGREE | NOT MET |

All other criterion-variant pairs agreed between passes.
Disagreements re-evaluated: 2
Final verdicts changed (versus Pass 1): 1 (V2 dependencies -> MET)

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate points won |
|---|---|---|---|---|
| V1 (sonnet:analyzer) | 0.3631 | 0.3667 | **0.7298** | 3.0 |
| V2 (haiku->glm-5.3:qa) | 0.4250 | 0.3167 | **0.7417** | 3.0 |
| V3 (opus:refactorer) | 0.3556 | 0.4000 | **0.7556** | 4.0 |

**Margin**: 1.4% between V3 and V2 (below the 5% threshold)
**Tiebreaker applied**: Yes, level 1 (debate performance). V3 won 4.0 diff points against 3.0 for V2 (debate-transcript.md, "Points won"). That margin is above 5%, so the tie is settled at level 1.

## Selected Base: Variant 3 (opus:refactorer)

### Selection Rationale
V3 has the highest combined score and wins the tiebreaker. Its blocking finding S-1 (C-001) survived the debate unanimously as blocking. It also has the most minor findings that hold up when re-read: S-2 through S-7 were all kept, two of them with corrected labels. Its correctness errors are category mislabels (S-4), not false facts. Its structure gives one finding per topic, which is the shape the merged verdict needs. It must take in V1's and V2's section-20 work, the A-001 security blocker that all three cards missed, and the invariant-probe amendments.

### Strengths to Preserve from Base
1. S-1 as the blocking ordering finding, recommending that the full-suite/lint/sync task run before the two smoke checks (plan:228).
2. S-2, S-3, S-5, S-6 and S-7 as minor findings with their concrete fixes (hunk-range check, `origin/master` grep, scope and worktree removal).
3. S-4 as a minor finding, relabelled from false-claim to spec-inherited (source.md:391).

### Strengths to Incorporate from Non-Base Variants
1. From V1 A-1 and V2 Q-3 (narrowed, minor): section 20 ACs 1-4 and 6 are never run or recorded as pending. Also V1's static `--repo` assertion idea (A-002).
2. From V1 A-3 and V2 Q-2 (minor): the `git fetch origin` rule, plus the read-only-git conflict (A-004, from the calibration and the debate).
3. From V1 A-4 (split): U-001, the Task 2 environment not being forced.
4. From V2 Q-4 (minor, relabelled missing-requirement): the never-pass-`model` rule in every ref (all five, per INV-006).
5. From V2 Q-1: matrix bookkeeping (minor).
6. Debate-surfaced (calibration of reviewer-3, A-001): the Task 15 token-exposure blocker.
7. Invariant probe: INV-001 and INV-002 amend the C-001 fix; INV-003 and INV-004 amend the A-001 fix; INV-005, INV-007, INV-008, INV-009 and INV-010 become minors.
