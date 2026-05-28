# Base Selection

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (analyzer) | V2 (architect) | V3 (qa) |
|--------|--------|---------------|----------------|---------|
| Requirement coverage (M1+M2+M3a closure named) | 0.30 | 0.95 | 0.95 | 0.95 |
| Internal consistency (gates, formulas, caps) | 0.25 | 0.95 | 0.90 | 0.95 |
| Specificity (concrete diff sketches, file:line, formula) | 0.15 | 0.95 | 0.95 | 0.85 |
| Dependency completeness (cross-references between changes) | 0.15 | 0.90 | 0.85 | 0.95 |
| Section coverage (Coverage matrix, counter-args, migration) | 0.15 | 1.00 | 1.00 | 1.00 |
| **Quant subtotal** | | **0.940** | **0.928** | **0.937** |

## Qualitative Scoring (50% weight) — 30-criterion rubric

| Dimension | V1 | V2 | V3 |
|-----------|----|----|----|
| Completeness (5) | 5/5 | 5/5 | 5/5 |
| Correctness (5) | 5/5 | 4/5 (M3c masking claim overstates strength — V2 own-acknowledged) | 5/5 |
| Structure (5) | 5/5 | 4/5 (schema-v2.0 redesign blurs the v1.5 vs v2.0 ship boundary) | 4/5 (Change 6 pytest-hookup is half in/out of brainstorm scope) |
| Clarity (5) | 5/5 | 5/5 | 5/5 |
| Risk coverage (5) | 4/5 (under-named M4 regression risk) | 4/5 (under-named migration cost) | 5/5 (names migration, regression, anchoring) |
| Invariant/edge-case (5) | 4/5 | 5/5 (typed-evidence table catches more edge cases) | 5/5 (pin tests ARE the edge cases) |
| **Qual subtotal** | **28/30 = 0.933** | **27/30 = 0.900** | **29/30 = 0.967** |

## Combined Scoring

| Variant | Quant×0.50 | Qual×0.50 | **Final** | Rank |
|---------|------------|-----------|-----------|------|
| V1 opus:analyzer | 0.470 | 0.467 | **0.937** | 2 (margin 0.015 from V3) |
| V2 sonnet:architect | 0.464 | 0.450 | **0.914** | 3 |
| V3 haiku:qa | 0.469 | 0.484 | **0.952** | **1** |

## Tiebreaker (V3 vs V1 within 5%)

- Level 1 (debate performance): V3 wins on 4 diff points (U-003, C-004, C-005, X-002); V1 wins on 8 (S-002, S-003, C-001, C-003, X-001, U-002, partial C-002). V1 wins level 1.
- Level 2 (correctness criteria): tie (5/5 each).
- Level 3 (input order): V1 (variant-1) wins.

**Tiebreaker resolution**: V1 wins level 1 by debate performance, BUT V1's own Round 2/3 final concedes the merged shape adopts V3's Changes 4+5 (SKILL.md scope + pin-test corpus). The debate-resolution is: **base = V1's structural choices, augmented with V3's defense-in-depth changes (4+5) and V2's optional kind-tagging enhancement (U-001)**.

## Selected Base: V1 (opus:analyzer) — merged with V3's Changes 4+5 + V2's optional U-001

**Selection rationale**:
- V1 wins on structural choices (additive schema, no version bump, minimal migration cost).
- V1's Round 2 concession explicitly absorbs V3's Changes 4+5 — meaning the merged base already includes the pin-test corpus and SKILL.md scope correction.
- V2's typed evidence table is adopted as an *optional* enhancement to the card template (not mandatory in v1.5; mandatory in deferred v2.0).
- V3 wins on defense-in-depth — its Changes 4+5 are the only proposal-level deliverables that close M4.
- The merged base is: 3 core file changes (V1's shape) + 2 defense-in-depth changes (V3's 4+5) + 1 optional schema enhancement (V2's U-001) = 5 in-scope changes for the brainstorm proposal.

**Strengths to preserve from V1**:
- Three-file core (rubric + card + calibrator) with surgical, additive diffs
- Coverage matrix structure
- "What I am explicitly NOT changing" section (V1's distinctive contribution to scope discipline)
- Counter-arguments rejection prose

**Strengths to incorporate**:
- From V3: Change 4 (confidence-check/SKILL.md scope correction), Change 5 (calibrator-eval-cases.md pin-test corpus with 6 fixtures + 5 property tests), property test P5 added to M3c partial closure
- From V2: optional `kind` field in the card template's Evidence section (the typed-evidence table presented as a *recommended* shape, not mandatory)
- From V2: explicit note that mandatory `verdict_direction` + reject-malformed cards is the v2.0 evolution, deferred behind v1.5's safe defaults

**Edge case floor check**: All three variants score ≥1/5 on Invariant/edge-case coverage — floor satisfied.
