# Base Selection (Step 3)

Variants: V1 = OURS (`variant-1-original.md`), V2 = CLAY (`variant-2-original.md`). Scoring was done by the orchestrator (the debate-orchestrator role); the quantitative counts are sampled estimates, not machine counts (stated openly, as in the earlier R5 debate record), and both evaluation passes were run by the same orchestrator one after the other, so the position-bias check is weaker than with two independent evaluators.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 | V2 | Computation note |
|--------|--------|----|----|------------------|
| Requirement coverage (RC) | 0.30 | 1.00 | 0.83 | Source requirements = the six items in the D03 question: revert/keep/restore; "never ran live"; the three old protections; owner branch dependence; PRs 584 and 591 history; decision 6. V2 has no "restore parts" branch (5 of 6). |
| Internal consistency (IC) | 0.25 | 1.00 | 0.97 | V2 fact 1 says "never ran live" while fact 3 cites FU-1 record j (a live record): 1 conflict in about 30 claims. |
| Specificity ratio (SR) | 0.15 | 0.95 | 0.93 | Sample of 20 sentences each: concrete numbers, file:line, named entities against vague phrases. |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | Internal references ("fact N", section names) all resolve in both. |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 6 H2 sections each. |
| **quant_score** | | **0.9925** | **0.9310** | RC x0.30 + IC x0.25 + SR x0.15 + DC x0.15 + SC x0.15 |

## Qualitative Scoring (50% weight): additive binary rubric (30 criteria, CEV)

Format per criterion: MET only with a specific evidence citation; otherwise NOT MET. Evidence is a short pointer into the variant file.

### Completeness
| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| 1 | Covers all explicit requirements | MET (Claim, facts 1 to 9 cover the six items) | NOT MET (no "restore parts" branch; searched Claim, Mechanism) |
| 2 | Edge cases and failure scenarios | MET (Risks: D01 reversal, L-1, PR 686 clash) | MET (Risks: unreviewed plan, reversed decisions) |
| 3 | Dependencies and prerequisites | MET (Mechanism 1 and 2: imports, 3 files) | MET (Mechanism 2, fact 6: removal order) |
| 4 | Success or completion criteria | NOT MET (no stated done-test for the revert) | NOT MET |
| 5 | Out of scope stated | MET ("that is topic D01, not this one") | NOT MET |
| Subtotal | | 4 | 2 |

### Correctness
| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| 1 | No factual errors | NOT MET (fact 7 "53 changed files" is stale; fault-finder INV-008: 223 status entries) | NOT MET (fact 2 calls a question "the ruling"; concession in Round 2) |
| 2 | Feasible approach | MET (Mechanism 1 to 3; INV-009, INV-010 confirm the revert applies) | MET (design order, fact 6) |
| 3 | Consistent terminology | MET | MET |
| 4 | No internal contradictions | MET | NOT MET (facts 1 and 3, see IC) |
| 5 | Claims supported | MET (every fact has a path or PR) | NOT MET (fact 7 "one winner per cycle" does not cover per-issue adoption; conceded) |
| Subtotal | | 4 | 2 |

### Structure
| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| 1 | Logical order | MET | MET |
| 2 | Consistent depth | MET | MET |
| 3 | Separation of concerns | MET | MET |
| 4 | Navigation aids | NOT MET (no contents list or cross-links) | NOT MET |
| 5 | Follows artifact conventions | MET (brief's position-paper layout) | MET |
| Subtotal | | 4 | 4 |

### Clarity
| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| 1 | Unambiguous language | MET | MET |
| 2 | Concrete rather than abstract | MET (git revert, file names) | MET (design line numbers) |
| 3 | Each section has one purpose | MET | MET |
| 4 | Terms defined at first use | NOT MET (R18, FU-1, G2 not glossed) | NOT MET |
| 5 | Actionable next steps | MET (Mechanism list) | NOT MET (no next step beyond "keep") |
| Subtotal | | 4 | 3 |

### Risk Coverage
| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| 1 | 3 or more risks with probability and impact | NOT MET (3 risks, no probability) | NOT MET |
| 2 | Mitigation per risk | NOT MET (one of three has one) | NOT MET |
| 3 | Failure modes and recovery | MET ("the revert can itself be reverted") | NOT MET |
| 4 | External dependencies | MET (PR 686 symbol dependency) | MET (PR B unbuilt) |
| 5 | Monitoring or validation | NOT MET | NOT MET |
| Subtotal | | 2 | 1 |

### Invariant and Edge Case Coverage
| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| 1 | Collection boundaries | NOT MET | NOT MET |
| 2 | State variable interactions across components | MET (kill between `worker-start` and `adopt-mark`, fact 4) | MET (write-ahead `intent`/`done`, Mechanism 4) |
| 3 | Guard condition gaps | MET (fact 9, guard comment disagreement) | MET (fact 5, rule 2 kept) |
| 4 | Count divergence | NOT MET | NOT MET |
| 5 | Interaction effects | MET (PR 686 vs package, Risks 3) | MET (fact 6) |
| Subtotal | | 3 | 3 |

### Qualitative Summary
| Dimension | V1 | V2 |
|-----------|----|----|
| Completeness | 4 | 2 |
| Correctness | 4 | 2 |
| Structure | 4 | 4 |
| Clarity | 4 | 3 |
| Risk coverage | 2 | 1 |
| Invariant and edge | 3 | 3 |
| **Total / 30** | **21** | **15** |
| **qual_score** | **0.700** | **0.500** |

### Edge Case Floor Check
Floor is 1 of 5. V1 scores 3 and V2 scores 3: both eligible as base.

## Position-Bias Mitigation

Pass 1 evaluated V1 then V2; pass 2 evaluated V2 then V1 (reverse order), each time scoring all 30 criteria without looking at the other pass.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Completeness 1 | V2 | NOT MET | MET (pass 2 read "revert or keep" as the question) | No | NOT MET (re-evaluated: the question names "RESTORE parts" and V2 never considers it) |
| Correctness 1 | V1 | NOT MET | MET (pass 2 accepted the figure as cited from E-pr682.md line 67) | No | NOT MET (re-evaluated: fault-finder INV-008 shows 223 entries, so the figure is stale) |

Disagreements found: 2. Verdicts changed by re-evaluation: 0 (both returned to the pass 1 verdict).

## Combined Scoring

| Variant | quant (x0.50) | qual (x0.50) | Final score |
|---------|---------------|--------------|-------------|
| V1 (OURS) | 0.4963 | 0.3500 | **0.8463** |
| V2 (CLAY) | 0.4655 | 0.2500 | 0.7155 |

Margin: 13.1 percentage points. The tiebreaker (needs a margin under 5 points) was not applied.

## Selected Base: Variant 1 (OURS)

**Selection rationale.** V1 wins on combined score (0.846 against 0.716) and on the debate: both advocates ended with V1 as winner on 15 of 18 diff points (V2 won only S-001 as a tie, C-005 and C-010), and the advocates' own final lists agree on 16 of 18. The weighting rule given by the owner (OURS wins unless CLAY shows a clear evidenced benefit) is met: the only separable CLAY benefits are small (see below), and the one CLAY benefit that was claimed as new (the F14 contract bullet) turned out to be a relocation of a sentence already in WC-17 at `01e7a9e23^`.

**Strengths to preserve from V1.** Executable revert mechanics with a verified small overlap; the named old tests that pin the protections; the FU-1 live record; the owner-branch dependence; the dangling-text inventory.

**Strengths to incorporate from V2** (all separable from the contested rule):
1. The standalone "ask and send carry no `--to`" contract bullet and its test assertion (U-007; INV-002 says a bare revert loses it).
2. The creation-time plan sections of `/sc:issue --create` stay as an extra layer (U-006), not a replacement for approval.
3. The removal order and the file-by-file removal plan of the design (U-005, C-005) as the sequencing input, strengthened by INV-001.
4. The PR B test rows (`orchestrator.md:1108-1112`) as the stated bar for any replacement protection (U-008).
5. The honest cost statement: the gate costs latency, a coordinator and a grant row per issue (C-010, Q36), and the same-login limit shown by FU-1 record j (U-009).
