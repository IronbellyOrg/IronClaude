# Base Selection Report

Variants: V1 = reviewer-1 card (sonnet:analyzer); V2 = reviewer-2 card (haiku->glm-5.3:qa); V3 = reviewer-3 card (opus:refactorer). Evaluator: debate-orchestrator (quantitative layer) and two independent evaluator agents (qualitative Pass 1 forward and Pass 2 reverse; full CEV tables in `.work/qual-pass1.md` and `.work/qual-pass2.md`). The inputs are YAML reviewer cards: "sections" are top-level YAML keys, and "claims" are finding claims, the verdict and the self-audit.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 | V2 | V3 |
|--------|--------|----|----|----|
| requirement_coverage | 0.30 | 0.20 (spec sections cited: 7, 12, 13, 19 = 4/20) | 0.50 (4, 7, 8, 12, 13, 14, 15, 16, 17, 20 = 10/20) | 0.15 (13, 14, 20 = 3/20) |
| internal_consistency | 0.25 | 1.00 (0 intra-card contradictions / 8 claims) | 1.00 (0 / 6) | 1.00 (0 / 14) |
| specificity_ratio | 0.15 | 1.00 (0 vague-term hits) | 1.00 (0) | 1.00 (0) |
| dependency_completeness | 0.15 | 1.00 ("blocking A-1" resolves) | 1.00 (no internal refs) | 1.00 ("S-1 and S-2" resolve) |
| section_coverage | 0.15 | 0.889 (8/9 top-level keys) | 1.000 (9/9) | 0.778 (7/9) |
| **quant_score** | | **0.7433** | **0.8500** | **0.7117** |

Computation: spec sections from `source.md:N` citations mapped to the H2 ranges (H2 lines 11, 20, 42, 57, 81, 112, 137, 182, 221, 240, 272, 284, 316, 323, 344, 384, 402, 410, 444, 465), plus explicit "section N" mentions. Vague-term counts, key counts and citation counts come from one deterministic grep over the variant copies (V1 22 citations, V2 14, V3 41). Internal consistency measures intra-card contradiction only; factual errors refuted in the debate are scored under Correctness 1.

## Qualitative Scoring (50% weight) — Additive Binary Rubric (final verdicts after position-bias resolution)

CEV evidence for every cell is in `.work/qual-pass1.md` (order V1, V2, V3) and `.work/qual-pass2.md` (order V3, V2, V1). Cells re-evaluated by the orchestrator are marked (R).

### Completeness
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 Covers all explicit requirements | NOT MET (missed A-002..A-007) | NOT MET (missed C-001 and A-002..A-007) | NOT MET (missed C-001 and A-002..A-007) |
| 2 Edge cases / failure scenarios | MET (A-1 escaped write; A-4 exported variables) | NOT MET | MET (S-2 halt paths; S-8 `__pycache__`) |
| 3 Dependencies / prerequisites | MET (A-2 Task 14 prerequisite) | NOT MET | MET (S-3 dependency metadata) |
| 4 Success / completion criteria | MET | MET | MET |
| 5 Out-of-scope items | NOT MET | MET (Q-1 deferred PR step) | NOT MET |
| **Subtotal** | **3/5** | **2/5** | **3/5** |

### Correctness
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 No factual errors | NOT MET (A-1 "public comments on someone else's repo": escaped write lands on origin; conceded round2-v1) | NOT MET (PASS self-audit misses C-001; conceded round2-v2) | NOT MET (S-2 "resume cannot work" false; conceded round1-v3 Concessions 1) |
| 2 Feasible recommendations | MET | MET | MET |
| 3 Terminology / categories accurate | NOT MET (A-1 `blocking`/`safety-risk`, conceded minor) | NOT MET (R): Q-2/Q-3 deviation labels conceded (round2-v2.md:17) | NOT MET (S-1 `cross-task-contradiction`, S-1/S-2 `blocking`, conceded) |
| 4 No internal contradictions | MET | MET | NOT MET (self_audit "FAIL rests on S-1 and S-2" vs S-2 evidence including ledger.md:161 Row S, which supports resume) |
| 5 Claims cited | MET | MET | MET |
| **Subtotal** | **3/5** | **3/5** | **2/5** |

### Structure
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 Logical ordering | MET (blocking first) | MET (R): Q-1..Q-4 follow plan order (plan:25, :92, :129, :254) | MET (blocking first) |
| 2 Consistent schema | MET | MET | NOT MET (mixed block and flow findings) |
| 3 One topic per finding | NOT MET (A-3 bundles four claims) | MET | NOT MET (S-2 multi-branch; S-6 two topics) |
| 4 Navigation aids | MET | MET | MET |
| 5 Card conventions | MET | MET | MET |
| **Subtotal** | **4/5** | **5/5** | **3/5** |

### Clarity
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 Unambiguous language | MET | MET | NOT MET (S-2 "or ..." alternatives; S-7 "[INFERRED]") |
| 2 Concrete | MET | MET | MET |
| 3 One-sentence summary per finding | NOT MET (A-3) | MET | MET (R): S-2 reduces to "Task 15's stop-and-resume does not fit /sc:implement's semantics" |
| 4 Terms defined on first use | NOT MET | NOT MET | NOT MET |
| 5 Actionable next steps | MET | MET | MET |
| **Subtotal** | **3/5** | **4/5** | **3/5** |

### Risk Coverage
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 At least 3 risks with impact | MET | NOT MET | MET |
| 2 Mitigation for each | MET | MET | MET |
| 3 Failure modes and recovery | MET | NOT MET | MET |
| 4 External dependencies and failures | MET (R): GitHub (A-1), ClickUp (A-3, A-4, A-6), executor (A-2); the criterion does not require all four | NOT MET | MET (GitHub, ClickUp, gateway S-7, executor S-2) |
| 5 Validation mechanism | MET | MET | MET |
| **Subtotal** | **5/5** | **2/5** | **5/5** |

### Invariant & Edge Case Coverage
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 Collection boundaries | MET (A-6 non-positive page cap) | NOT MET | NOT MET |
| 2 State interactions across components | MET (A-4 env state into tests) | NOT MET | MET (S-2 ledger state) |
| 3 Guard-condition gaps | MET (A-1 Wave 0 guard) | NOT MET | MET (S-1 fork-safety scan) |
| 4 Count divergence | MET (A-4 two of four variables cleared) | NOT MET (R): "all nine STOP codes" asserts a match; no divergence scenario | NOT MET (R): S-3 is a dependency-set mismatch, S-8 a collection-membership issue; neither is a count or range divergence |
| 5 Interaction effects | MET (A-5 Task 6 prose vs Task 7 scan) | NOT MET | MET (S-1) |
| **Subtotal** | **5/5** | **0/5** | **3/5** |

### Qualitative Summary
| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 3/5 | 2/5 | 3/5 |
| Correctness | 3/5 | 3/5 | 2/5 |
| Structure | 4/5 | 5/5 | 3/5 |
| Clarity | 3/5 | 4/5 | 3/5 |
| Risk Coverage | 5/5 | 2/5 | 5/5 |
| Invariant & Edge Case | 5/5 | 0/5 | 3/5 |
| **qual_score** | **23/30 = 0.7667** | **16/30 = 0.5333** | **19/30 = 0.6333** |

### Edge Case Floor Check
| Variant | Invariant & Edge Case | Eligible as base |
|---|---|---|
| V1 | 5/5 | Yes |
| V2 | 0/5 | No (below the 1/5 floor) |
| V3 | 3/5 | Yes |

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| Correctness 3 | V2 | MET | NOT MET | DISAGREE | NOT MET: V2 conceded its Q-2/Q-3 deviation labels (round2-v2.md:17) |
| Structure 1 | V2 | MET | NOT MET | DISAGREE | MET: findings follow plan line order 25, 92, 129, 254 |
| Clarity 3 | V3 | NOT MET | MET | DISAGREE | MET: S-2 reduces to one sentence |
| Risk 4 | V1 | MET | NOT MET | DISAGREE | MET: three external dependencies analysed with failures; the criterion does not require all four |
| Invariant 4 | V2 | NOT MET | MET | DISAGREE | NOT MET: a count match is asserted, no divergence scenario |
| Invariant 4 | V3 | MET | NOT MET | DISAGREE | NOT MET: S-3 and S-8 are set-membership issues, not count or range divergence |

Disagreements re-evaluated: 6 (of 90 criterion-variant pairs). Final verdicts that differ from Pass 1: 3 (V2 Correctness 3, V3 Clarity 3, V3 Invariant 4). Final verdicts that differ from Pass 2: 3 (V2 Structure 1, V1 Risk 4, V2 Invariant 4).
Pass totals: Pass 1 V1 23, V2 17, V3 19; Pass 2 V1 22, V2 16, V3 19; final V1 23, V2 16, V3 19.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---|---|---|---|---|
| V1 (sonnet:analyzer) | 0.3717 | 0.3833 | **0.7550** | n/a |
| V2 (haiku->glm-5.3:qa) | 0.4250 | 0.2667 | **0.6917** (ineligible: edge-case floor) | n/a |
| V3 (opus:refactorer) | 0.3558 | 0.3167 | **0.6725** | n/a |

**Margin**: 6.3 points (V1 over V2, above the 5% threshold); V1 over the next eligible variant V3 by 8.3 points.
**Tiebreaker applied**: No.
Debate points won (scoring matrix, for reference): V1 5 (C-001, C-002, C-004, C-005, X-002), V2 3 (C-006, X-001, A-006), V3 2 (C-003, C-007), new shared-assumption findings 5 (A-002, A-003, A-004, A-005, A-007), none/rejected 4 (S-001, S-002, A-001, A-008).

## Selected Base: Variant 1 (reviewer-1, sonnet:analyzer)

### Selection Rationale
V1 has the highest combined score and full Invariant & Edge Case and Risk Coverage. It also holds the finding the debate ranked first, C-001 (A-1): the Task 17 live item-4 run is exempted from approval on the strength of untested behaviour. All three advocates endorsed V1's fix direction, as amended in Round 2. V1 is the only card that checked the round-1 fixes (`round1_fix_check`). Its weaknesses are an overstated severity and target on A-1 (conceded) and a bundled A-3; the merge corrects both.

### Strengths to Preserve from Base
1. A-1 as the lead finding, rewritten as minor, top priority, with the Round 2 fix (non-existent-target URL, an origin_repo.py URL check with a Task 6 AC, real-output evidence, a target-based plan:26 exemption).
2. A-2 (Task 15 two exits, "after Task 14"), A-3/A-4/A-6 ClickUp hygiene findings, A-5 scan scoping.
3. `round1_fix_check: {F-01: fixed, F-02: fixed}`.

### Strengths to Incorporate from Non-Base Variants
1. V3 S-1 (C-003 winner): the section 14 table and write list in SKILL.md lack `--repo`, merged with V1 A-5.
2. V3 S-3 (C-007 winner), S-4 (merged into C-005), S-5, S-6 (merged into C-004), S-7, S-8, S-9, S-10, S-12 as minor; S-11 dropped (withdrawn by V3).
3. V2 Q-4 (C-006 winner, strengthened: the executor prompts only on its closed list, so "approval at that moment" needs an explicit ask step); Q-1, Q-2, Q-3 as authorized expansions or notes.
4. V2's X-001 verdict: PASS with notes.
5. Shared-assumption findings A-002..A-007 (new, minor).
