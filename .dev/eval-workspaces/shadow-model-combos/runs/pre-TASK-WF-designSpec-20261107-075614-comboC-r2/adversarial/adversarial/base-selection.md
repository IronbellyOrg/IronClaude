# Base Selection

Scorer: the reflect orchestrator (inline; `debate-orchestrator` role). Honest limits: the 30-criterion rubric was applied once per variant by one evaluator; the reverse-order second pass was a recheck by the same evaluator, not an independent agent (see Position-Bias Mitigation). Scores are judgments, not measurements.

## Quantitative Scoring (50% weight)

Source "requirements" for RC = the 20 content diff points C-001 to C-020 (a variant covers a point when one of its findings addresses it). IC = 1 - (overstated, withdrawn or narrowed claims / claims), taken from the Round 2 concessions. SR from the share of findings carrying line cites and quotes. DC = internal references that resolve (all three about 0.95). SC = sections / max sections.

| Metric (weight) | V1 | V2 | V3 |
|---|---|---|---|
| RC (0.30) | 7/20 = 0.35 | 12/20 = 0.60 | 8/20 = 0.40 |
| IC (0.25) | 1 - 3/7 = 0.57 | 1 - 4/12 = 0.67 | 1 - 4/8 = 0.50 |
| SR (0.15) | 0.85 | 0.88 | 0.90 |
| DC (0.15) | 0.95 | 0.95 | 0.95 |
| SC (0.15) | 4/5 = 0.80 | 5/5 = 1.00 | 4/5 = 0.80 |
| **quant_score** | **0.6375** | **0.7720** | **0.6425** |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Dimension subtotals (each criterion MET only with a citable line; the per-criterion CEV rows are summarised by the evidence column).

| Dimension | V1 | V2 | V3 | Evidence (examples) |
|---|---|---|---|---|
| Completeness (5) | 3 | 4 | 3 | V2 covers 12 distinct gaps incl. resume inputs; V1 and V3 miss several (Round 1 concessions) |
| Correctness (5) | 3 | 3 | 3 | each has 3 to 4 findings narrowed in Round 2 (V1 F1, F4, F5; V2 F9, F11, F4; V3 F4, F1, F8) |
| Structure (5) | 4 | 4 | 4 | all use Checked/Held/Refuted/New plus a findings-v2 block |
| Clarity (5) | 3 | 4 | 4 | V1 states no fixes; V2 F5 names a fix; V3 names exact edits |
| Risk Coverage (5) | 3 | 4 | 2 | V3 raises 7 MINOR hygiene items and no state-mechanics risk |
| Invariant & Edge Case Coverage (5) | 3 | 3 | 1 | V3 meets only 1 (it flags undefined Phase values) |
| **Total / 30** | **19** | **22** | **17** |  |
| **qual_score** | **0.633** | **0.733** | **0.567** |  |

### Edge Case Floor Check
Floor 1/5: V1 3/5 eligible, V2 3/5 eligible, V3 1/5 eligible (meets the floor exactly).

## Position-Bias Mitigation
Pass 1 in input order (V1, V2, V3); pass 2 re-scored in reverse order (V3, V2, V1) by the same evaluator. No dimension subtotal changed. Disagreements found: 0; verdicts changed: 0. Weakness: same evaluator, so this does not test evaluator bias.

## Combined Scoring
| Variant | 0.50 x quant | 0.50 x qual | Final |
|---|---|---|---|
| V1 (reviewer-1, analyzer, sonnet) | 0.3188 | 0.3167 | **0.6354** |
| V2 (reviewer-2, qa, haiku) | 0.3860 | 0.3667 | **0.7527** |
| V3 (reviewer-3, refactorer, opus) | 0.3213 | 0.2833 | **0.6046** |

Margin V2 over V1: 11.7 points; no tiebreaker applied.

## Selected Base: Variant 2 (reviewer-2 card, qa persona, claude-haiku-5-5)

Selection rationale: V2 raised the most distinct defects (12 of the 20 content points, plus the one design-level hole C-010) and won 10 of 30 points outright (S-001, C-001, C-002, C-003, C-008, C-009, C-010, C-019, X-001, X-002) with 3 of 3 agreement on C-003, C-008, C-009, C-010. Its Round 2 concessions bring its blocking flags from 4 to 2, which matches its evidence.

Strengths to preserve: findings-v2 block with quotes; C-010 resume-input finding; C-008 autoMergeRequest; C-009 Wave 3 test; C-019 fold list.

Strengths to incorporate: V1 C-004, C-005, C-017, C-018 (plus the sharper C-002/C-003 framing of V1 F2 and F3); V3 C-006 (as MINOR spec-origin), C-007, C-011 to C-016.

Dissent: the advocate for V3 and the advocate for V1 each rank their own variant lower than V2 for deciding readiness; V2's own advocate ranks V2 first. The result does not depend on self-ranking.
