# Base Selection Report

## Quantitative Scoring (50% weight)

Method: specificity ratio computed by a throwaway script (concrete = numbers, `:line` refs, backticked tokens, named tools; vague = appropriate/as needed/properly/adequate/should consider/might/various/etc./best practices/likely/possibly/may) over non-comment lines of `variant-N-original.md`. Section coverage = top-level YAML keys (`grep -c -E '^[a-z0-9_]+:'`; the first script run used `[a-z_]` and missed `t1_findings_disputed`, corrected and re-counted). Requirement coverage = plan tasks (8) touched by at least one finding (the source has no requirement ids; section-level topic matching). Internal consistency = 1 - contradictions / (findings + T1 disputes + resolution rows), contradictions taken from the debate (V1's D-001 "resolved: yes" beside R1-1, conceded in round2-v1.md); both qualitative passes found no internal contradiction in V2 or V3. Dependency completeness: every internal finding-id reference resolves; T1 ids are external and excluded.

| Metric | Weight | Variant 1 (sonnet:analyzer) | Variant 2 (haiku-slot:qa) | Variant 3 (opus:refactorer) |
|--------|--------|-----------|-----------|-----------|
| requirement_coverage | 0.30 | 0.375 (Tasks 2, 3, 4) | 0.375 (Tasks 1, 2, 8) | 0.500 (Tasks 2, 4, 6, 8) |
| internal_consistency | 0.25 | 0.955 (1 of 22) | 1.000 (0 of 4) | 1.000 (0 of 11) |
| specificity_ratio | 0.15 | 0.995 (183 concrete, 1 vague) | 0.978 (88, 2) | 0.994 (164, 1) |
| dependency_completeness | 0.15 | 1.000 | 1.000 | 1.000 |
| section_coverage | 0.15 | 0.889 (8 of 9) | 1.000 (9 of 9) | 0.778 (7 of 9) |
| **quant_score** | | **0.784** | **0.809** | **0.816** |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Two independent read-only passes with full Claim-Evidence-Verdict tables: `qualitative-pass1.md` (order 1, 2, 3) and `qualitative-pass2.md` (order 3, 2, 1). Per-criterion evidence is in those files. Six disagreements were re-evaluated by a third agent (opus) whose verdict is final (below).

### Qualitative Summary (final, after disagreement resolution)
| Dimension | Variant 1 | Variant 2 | Variant 3 |
|-----------|-----------|-----------|-----------|
| Completeness | 5/5 | 4/5 | 3/5 |
| Correctness | 4/5 (K4 not met) | 4/5 (K1 not met: R2-F3 premise refuted) | 2/5 (K1, K3, K5 not met) |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 3/5 (L1, L4 not met) | 3/5 (L3, L4 not met) | 3/5 (L3, L4 not met) |
| Risk Coverage | 5/5 | 5/5 | 5/5 |
| Invariant & Edge Case | 4/5 (E1 not met) | 4/5 (E1 not met) | 5/5 |
| **Total** | **26/30 = 0.867** | **25/30 = 0.833** | **23/30 = 0.767** |

### Edge Case Floor Check
All three variants score 4/5 or 5/5 on Invariant & Edge Case Coverage (>= 1/5): all eligible as base.

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| L1 | 1 | MET | NOT MET | DISAGREE | NOT MET (D-002 "resolved: yes" vs note "R1-4, R1-5 remain"; hedged R1-1/R1-2 headlines) |
| K4 | 2 | MET | NOT MET | DISAGREE | MET ("REFUTED" is an orchestrator annotation, not the reviewer's own statement) |
| K5 | 2 | MET | NOT MET | DISAGREE | MET (R2-F3 claims only that the plan has no check; plan:44 and eval_runner.py:138 support it) |
| L3 | 2 | MET | NOT MET | DISAGREE | NOT MET (R2-F1 and R2-F2 headlines each make two claims) |
| R3 | 2 | MET | NOT MET | DISAGREE | MET (recovery steps in R2-F1, R2-F2, R2-F3) |
| L3 | 3 | MET | NOT MET | DISAGREE | NOT MET (R3-F2, R3-F3, R3-F4 headlines bundle 2-3 claims) |

Disagreements re-evaluated: 6. Final verdicts changed vs pass 1: 3; vs pass 2: 3.
Arithmetic correction: pass 2 reported Variant 1 = 24/30; its own verdicts sum to 26/30 (recorded in qualitative-pass2.md).

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker (diff points won of 12 S/C/X) |
|---------|---------------|--------------|-----------------|-------------------|
| 1 (sonnet:analyzer) | 0.392 | 0.433 | **0.825** | 4.5 |
| 2 (haiku-slot:qa) | 0.405 | 0.417 | **0.821** | 0 |
| 3 (opus:refactorer) | 0.408 | 0.383 | **0.791** | 7.5 |

Wins counted from the debate-transcript scoring matrix; split points (S-003, C-001 content vs label, C-004 merge) count 0.5 to each side.

**Margin**: Variant 1 over Variant 2 = 0.004 (0.5%), below the 5% threshold.
**Tiebreaker applied**: Yes, level 1 (debate performance): Variant 1 won 4.5 diff points, Variant 2 won 0. Variant 3 is 0.034 behind Variant 1 and is not part of the top-two tie.

## Selected Base: Variant 1 (reviewer-1, sonnet:analyzer)

### Selection Rationale
Highest combined score (0.825) and the tiebreaker winner over Variant 2. It is the only card with a 14-row D-001..D-014 coverage table (C1 met in both passes), the only card with an explicit out-of-scope statement (C5: R1-6), and it has no refuted premise and no mislabelled finding. All three advocates chose it as the S-001 base by the end of Round 2 (round2-v3.md moved from V2 to V1).

### Strengths to Preserve from Base
1. `deviations_resolution` table (D-001..D-014 with plan locations), amended where the debate conceded the D-001 cell.
2. R1-1 (import crash; drift label agreed by all), R1-3 (Orca link-flag strength mismatch, plan:88 vs :111), R1-4 (CLAUDE.md:70), R1-5 (section-limited whole-word grep), R1-6 (pr-submit fallbacks out of scope).
3. T1 disputes of F1 and F3.

### Strengths to Incorporate from Non-Base Variants
1. From Variant 3: R3-F3 failure-path design (MasterCheckoutError, rmdir before try/finally, try/finally around `yield` only, narrow catch) replacing R1-2's weaker recommendation and raising it to medium (C-002, X-004).
2. From Variant 3: R3-F2 plus R3-F9 (main() wiring, global-setup path, exit code) merged with Variant 2's R2-F2 and V1's round-2 eval_runner.py:294-295 guard note (C-003, X-005).
3. From Variant 3: R3-F4 CLAUDE.md:50 placeholder conflict (scripts half dropped), merged with R1-4/R1-5 (C-004).
4. From Variant 2: R2-F1 Task 8 rerun artifact (medium, uncontested).
5. From Variant 2: Search A/B reproduction note (U-005).
6. From Variant 3: R3-F5 (`git diff HEAD`) as low hardening per round2-v3.md evidence; R3-F6, R3-F7, R3-F8 as low.
7. From Variant 3: dispute of T1 S1 (Task 2 not executable as written).
8. From Variant 2: R2-F3 as a low completeness note with the refuted-premise annotation.
