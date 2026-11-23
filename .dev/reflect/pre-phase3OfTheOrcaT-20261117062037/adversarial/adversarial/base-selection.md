# Base Selection

Variants: V1 analyzer (sonnet), V2 qa (haiku), V3 refactorer (opus). Inputs: variant-N-original.md, debate-transcript.md (final rulings), scoring-pass-1.md, scoring-pass-2.md.

## Quantitative Scoring (50% weight)

Source requirement set for RC: the 10 plan defects that survived the debate at MEDIUM or higher (C-001, C-002, C-003, C-004, C-005, C-006, C-009, C-011, C-012, C-013). IC counts claims the debate refuted as factual errors. SR, DC and SC are equal for all three cards (every finding names a file:line; every reference resolves; every card has findings, uncovered requirements and a checked section).

| Metric | Weight | V1 | V2 | V3 | Computation |
|---|---|---|---|---|---|
| RC requirement coverage | 0.30 | 0.60 | 0.40 | 0.90 | V1 raised 6 of 10 (C-001 to C-006), V2 raised 4 (C-001, C-002, C-003, C-009), V3 raised 9 (all but C-009) |
| IC internal consistency | 0.25 | 1.00 | 1.00 | 0.83 | V3 had 2 refuted factual claims of 12 findings (INF-009 "only a constraint"; register line 33 "exists only after execution"); V1 and V2 none |
| SR specificity | 0.15 | 1.00 | 1.00 | 1.00 | every claim cites a file:line or id |
| DC dependency completeness | 0.15 | 1.00 | 1.00 | 1.00 | internal references resolve |
| SC section coverage | 0.15 | 1.00 | 1.00 | 1.00 | three sections each |
| **quant_score** | | **0.880** | **0.820** | **0.9275** | RC*0.30 + IC*0.25 + SR*0.15 + DC*0.15 + SC*0.15 |

## Qualitative Scoring (50% weight)

Two independent passes (scoring-pass-1.md forward order, scoring-pass-2.md reverse order) on the 30-criterion rubric, interpreted for a reviewer card.

| Variant | Pass 1 | Pass 2 | Disagreements | Final (30) | qual_score |
|---|---|---|---|---|---|
| V1 | 28 | 28 | Completeness 4 vs 5 (task ordering and prerequisites not stated: NOT MET); Correctness 5 vs 4 (F6 cites export.py:75-86, the record writer, for a snapshot claim: NOT MET) | 27 | 0.900 |
| V2 | 26 | 26 | Completeness 5 vs 4 (misses six ruled MEDIUM points: NOT MET); Invariant/edge 4 vs 5 (no count-divergence figure: NOT MET) | 25 | 0.833 |
| V3 | 26 | 24 | Structure 5 vs 4 (pass 2 read a condensed copy of the card that dropped the plan_says and reality fields; the card as returned has them: MET); Risk coverage 5 vs 4 (no external-failure case: NOT MET) | 25 | 0.833 |

Disagreement resolution: each differing criterion was re-evaluated against the card text and the final debate rulings; the re-evaluated verdict is final.

### Edge-case floor
V1 5/5, V2 4/5, V3 4/5 on the Invariant and Edge Case dimension (final): all eligible (floor is 1/5).

## Combined Scoring

| Variant | 0.5 x quant | 0.5 x qual | variant_score |
|---|---|---|---|
| V1 | 0.440 | 0.450 | **0.890** |
| V3 | 0.464 | 0.417 | **0.880** |
| V2 | 0.410 | 0.417 | **0.827** |

Margin V1 over V3: 0.010 (1.1%), inside the 5% tiebreaker band.

## Tiebreaker
- Level 1, debate performance (points where the variant's own Round 1 severity equalled the final ruling, of 15 C points): V1 14 (missed C-002), V3 14 (missed C-007), V2 11. V1 and V3 tie.
- Level 2, correctness criteria met: V1 4 of 5, V3 3 of 5. V1 wins.

## Selected Base: Variant 1 (analyzer, sonnet)

Rationale: highest combined score; tiebreaker won on correctness criteria; the only card that traces the render height budget, the typed join and the first-selection gate, and the only one that measures the footer growth (107 to about 121 characters). Strengths to preserve: F1 (the `--once` Collector site), F2, F4, F5, F7 and the `checked` list of confirmed-correct items. Strengths to incorporate from the other cards: V2's byte-for-byte link-off check and desk assertions (C-009), V3's architecture-drift, builder-reuse and stale-spec findings (C-011, C-012, C-013), V2's narrower Task 6 fix. Regrade V1's F3 (keys line) and F6 (snapshot check) from MEDIUM to BLOCKING per the final rulings.
