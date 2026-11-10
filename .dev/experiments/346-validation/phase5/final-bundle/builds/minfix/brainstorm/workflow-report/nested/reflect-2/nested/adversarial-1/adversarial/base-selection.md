# Base Selection

## Quantitative Scoring (50% weight)

Source requirements for RC = the 13 included content findings C-001..C-013 established in the debate (A-001 folds into C-001, A-002 into C-002; X-002 excluded). SR and SC computed by script (concrete = file/line/number tokens, vague = hedge words; sections = H2/H3 count).

| Metric | Weight | V1 | V2 | V3 | Computation |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.538 | 0.154 | 0.385 | V1: C-001, C-004, C-005, C-006, C-007, C-012, C-013 (7/13); V2: C-002, C-003 (2/13); V3: C-001, C-008, C-009, C-010, C-011 (5/13) |
| Internal consistency (IC) | 0.25 | 1.000 | 1.000 | 0.800 | V3: R3-F3 describes an AC that cannot pass yet grades it minor against the shared rule (1 of 5 claims) |
| Specificity ratio (SR) | 0.15 | 1.000 | 1.000 | 0.983 | concrete/vague: V1 75/0, V2 28/0, V3 59/1 |
| Dependency completeness (DC) | 0.15 | 1.000 | 1.000 | 1.000 | every finding-id and file:line reference resolves |
| Section coverage (SC) | 0.15 | 1.000 | 0.750 | 1.000 | sections 4 / 3 / 4 |
| **quant_score** | | **0.862** | **0.709** | **0.763** | |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Full CEV tables: scoring-pass1.md (order V1, V2, V3) and scoring-pass2.md (order V3, V2, V1).

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 3/5 | 3/5 | 3/5 |
| Correctness | 4/5 | 5/5 | 4/5 |
| Structure | 5/5 | 4/5 | 5/5 |
| Clarity | 4/5 | 4/5 | 4/5 |
| Risk Coverage | 5/5 | 4/5 | 4/5 |
| Invariant & Edge Case Coverage | 5/5 | 3/5 | 4/5 |
| **Total** | **26/30 (0.867)** | **23/30 (0.767)** | **24/30 (0.800)** |

### Edge Case Floor Check

All three variants score at least 1/5 on Invariant & Edge Case Coverage (5, 3, 4): all eligible.

## Position-Bias Mitigation

| Metric | Value |
|---|---|
| Criterion-variant pairs | 90 |
| Disagreements between pass 1 and pass 2 | 0 |
| Verdicts changed by re-evaluation | 0 |

## Combined Scoring

| Variant | quant × 0.5 | qual × 0.5 | Final |
|---|---|---|---|
| V1 (reviewer-1, sonnet/analyzer) | 0.431 | 0.433 | **0.864** |
| V3 (reviewer-3, opus/refactorer) | 0.381 | 0.400 | 0.781 |
| V2 (reviewer-2, haiku/qa) | 0.354 | 0.383 | 0.738 |

Margin V1 over V3: 0.083 (8.3%), above the 5% tiebreaker trigger; tiebreaker not applied.

## Selected Base: Variant 1 (reviewer-1, sonnet/analyzer)

- **Selection rationale:** highest requirement coverage (7 of 13 agreed findings), highest risk and invariant coverage (5/5 each in both passes), and it found the CI-breaking C-001 (debate: S-001 won by V1 unanimously).
- **Strengths to preserve:** R1-F1 (C-001 evidence), R1-F2 (500-line arithmetic), R1-F3..F5, the narrowed R1-F6 (40-character rule), R1-F7 (with the Round 2 column-0 evidence), the self-audit.
- **Strengths to incorporate:** V2 R2-F1 (C-002, blocking, with the owner-decision-sentence channel from plan:117); V2 R2-F2 reframed per V3 as a declared necessary deviation (C-003/X-001); V3 R3-F1 decisive set-edit fix (C-001); V3 R3-F3 upgraded to blocking (C-009) with the INV-005 grep-exclusion fix; V3 R3-F2 (narrowed), R3-F4, R3-F5; Round 2.5 amendments INV-001 (rewrite plan:119), INV-003 (INF-032 blocking), INV-002 (in-paragraph placement), INV-004 (second exit 2).
- **To drop:** X-002 (test_model_alias_policy.py) and the skill-path half of R1-F6.
