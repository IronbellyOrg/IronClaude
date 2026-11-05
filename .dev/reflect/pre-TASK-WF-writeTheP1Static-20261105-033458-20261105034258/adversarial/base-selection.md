# Base Selection (hybrid scoring)

Variants: V1 = reviewer 1 card (analyzer, sonnet), V2 = reviewer 2 card (qa, haiku), V3 = reviewer 3 card (refactorer, opus). Scoring was done by the orchestrator inline (not a separate scorer agent); the basis of each number is stated so it can be re-derived. The invariant probe (Round 2.5) is not a variant; it feeds the refactor plan.

## Quantitative layer (weight 0.50)

Merged final findings used as the requirement set (16): M-01 graph/impact skill gaps, M-02 graph init refusal order, M-03 init-lite pass-through and dry-run, M-04 Task 15 path-list, M-05 Task 14 nested rule, M-06 regex copy, M-07 boundaries wording, M-08 drop cleanup-audit test, M-09 D-P1-1, M-10 lint WARN counting, M-11 adversarial `-i`/`-o`, M-12 workflow refs `--output` rule, M-13 invariant-2 decision, M-14 plugin inventory, M-15 business-panel trailing spaces, M-16 stale WORKER-CONTRACT.md table.

| Metric | Weight | V1 | V2 | V3 | Basis |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.625 (10/16) | 0.375 (6/16) | 0.5625 (9/16) | merged findings each card raised |
| Internal consistency (IC) | 0.25 | 0.77 | 0.86 | 0.80 | 1 - (wrong or retracted claims / findings): V1 3/13 (R1-01 impact sub-claim, R1-06, R1-09), V2 1/7 (R2-01), V3 2/10 (R3-06 count, t1_ref note) |
| Specificity (SR) | 0.15 | 0.85 | 0.85 | 0.88 | calibrator citation-grounding score |
| Dependency completeness (DC) | 0.15 | 0.92 | 1.00 | 1.00 | references in the card that resolve to real plan or spec lines (V1 R1-09 unresolved) |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | all three cards carry findings plus self-audit |

quant: V1 = 0.7955, V2 = 0.7550, V3 = 0.8008.

## Qualitative layer (weight 0.50)

30-criterion additive rubric, Claim-Evidence-Verdict per criterion, two passes.

| Dimension (5 each) | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 3 | 3 | 4 |
| Correctness | 3 | 4 | 4 |
| Structure | 4 | 4 | 4 |
| Clarity | 4 | 3 | 4 |
| Risk coverage | 4 | 2 | 4 |
| Invariant and edge-case coverage | 4 | 1 | 3 |
| Total | 22 | 17 | 23 |

Edge-case floor (1/5): all three pass (V2 at exactly 1).
Pass 1 (input order V1, V2, V3) and pass 2 (reverse) agree on every dimension total; no re-evaluation needed. qual: V1 = 0.733, V2 = 0.567, V3 = 0.767.

## Combined

| Variant | Quant | Qual | Combined |
|---|---|---|---|
| V1 | 0.7955 | 0.733 | 0.764 |
| V2 | 0.7550 | 0.567 | 0.661 |
| V3 | 0.8008 | 0.767 | 0.784 |

V3 leads V1 by 0.020 (inside the 5 percent band), so the tiebreaker applies.

## Tiebreaker

Level 1, debate performance (points won in the per-point table): V3 wins C-002, C-005, C-006, C-007, X-001, X-002, X-003 (7); V1 wins C-001 (substance), C-008, X-005, X-006 (4). V3 is base.

## Selected base: V3 (reviewer 3 card)

Weaknesses of V3 that the refactor plan repairs from other sources: no closed-flag-table finding (V1 R1-01), no graph init ordering (V1 R1-13), no `-i`/`-o` (V1 R1-10), no trailing-space check (V2 + calibrator), no invariant-2 decision (V2 R2-06), no plugin inventory (V2 R2-07), no D-P1-1 finding (V1 R1-07 / V2 R2-05), and the six probe items INV-1 to INV-6.
