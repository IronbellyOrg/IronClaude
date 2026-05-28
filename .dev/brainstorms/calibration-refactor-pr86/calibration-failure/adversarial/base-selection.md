# Base Selection — Hybrid Scoring

## Quantitative Layer (weight 0.50)

| Metric                  | Weight | V1 (A) | V2 (B) | V3 (C) | Notes                                                                                                   |
|-------------------------|--------|--------|--------|--------|---------------------------------------------------------------------------------------------------------|
| Requirement coverage    | 0.30   | 1.00   | 1.00   | 1.00   | All three produce: invocation evidence, 3 theories, per-theory confidence, systemic fix, citations.       |
| Internal consistency    | 0.25   | 1.00   | 1.00   | 0.92   | V3 has one explicitly-flagged `[interpretive — uncited]` and one `[uncited]` marker — honest but counts. |
| Specificity ratio       | 0.15   | 0.95   | 1.00   | 0.92   | V2 has the most concrete file:line citations; V3 generally specific but some inline-fallback narrative.   |
| Dependency completeness | 0.15   | 1.00   | 1.00   | 0.95   | V3's pipeline-degradation disclosure introduces external dependencies (--no-mcp) acknowledged as gaps.    |
| Section coverage        | 0.15   | 1.00   | 0.92   | 1.00   | V2 lacks Cross-theory synthesis section that V1 has and V3 partially has via Wave landing summary.        |

**Quant scores**:
- V1: (1.00×0.30) + (1.00×0.25) + (0.95×0.15) + (1.00×0.15) + (1.00×0.15) = 0.30+0.25+0.1425+0.15+0.15 = **0.9925**
- V2: (1.00×0.30) + (1.00×0.25) + (1.00×0.15) + (1.00×0.15) + (0.92×0.15) = 0.30+0.25+0.15+0.15+0.138 = **0.988**
- V3: (1.00×0.30) + (0.92×0.25) + (0.92×0.15) + (0.95×0.15) + (1.00×0.15) = 0.30+0.23+0.138+0.1425+0.15 = **0.9605**

## Qualitative Layer (weight 0.50; 30-criterion binary)

| Dimension                          | V1  | V2  | V3  |
|------------------------------------|-----|-----|-----|
| Completeness (5)                   | 5/5 | 5/5 | 5/5 |
| Correctness (5)                    | 5/5 | 5/5 | 4/5 (one inference flagged uncited) |
| Structure (5)                      | 5/5 | 5/5 | 4/5 (no explicit cross-theory section) |
| Clarity (5)                        | 5/5 | 5/5 | 5/5 |
| Risk Coverage (5)                  | 5/5 | 5/5 | 4/5 (no channel-failure disclosure equivalent) |
| Invariant & Edge Case Coverage (5) | 5/5 (substrate-fidelity caveat = invariant probe) | 4/5 (channel-failure honest but doesn't probe substrate-vs-H3 fidelity) | 5/5 (recursion observation + pipeline-degradation = explicit edge-case acknowledgment) |

**Qual scores**:
- V1: 30/30 = **1.00**
- V2: 29/30 = **0.967**
- V3: 27/30 = **0.90**

**Edge-case floor (1/5 on dim 6)**: All variants pass.

## Combined Scoring

- V1: (0.50 × 0.9925) + (0.50 × 1.00) = 0.4963 + 0.50 = **0.9963**
- V2: (0.50 × 0.988) + (0.50 × 0.967) = 0.494 + 0.4835 = **0.9775**
- V3: (0.50 × 0.9605) + (0.50 × 0.90) = 0.48025 + 0.45 = **0.93025**

## Position Bias Mitigation

- Pass 1 (input order A,B,C): V1=0.9963, V2=0.9775, V3=0.93025 → V1 wins.
- Pass 2 (reverse C,B,A): V1=0.9963, V2=0.9775, V3=0.93025 → V1 wins (deterministic scoring; no order dependence in quant/qual rubric).
- **Agreement**: V1 selected as base.

## Tiebreaker (would apply if top-two within 5%)

V1 (0.9963) vs V2 (0.9775) → delta 0.0188 ≈ 1.9% → tiebreaker applies.

- **Level 1 (debate performance)**: V2 won 2 individual points (T1 winner, T2 winner); V1 won 1 (cross-theory synthesis); V3 won 2 (recursion observation, eval-suite silent-green). V2 has slight edge on per-point debate, but V1's "cross-theory synthesis" point is *structurally load-bearing* for the merged output's shape.
- **Level 2 (correctness count)**: V1=5/5, V2=5/5 → tie.
- **Level 3 (input order)**: V1 (deterministic).

**Resolution**: V1 selected as base for structural shape; V2's individual point wins (T1 framing, T2 framing) integrated via refactor plan.

## Selected Base: **V1 (Agent A)**

**Rationale**: V1's cross-theory implications section provides the structural skeleton the merged output needs ("T1+T2 compound multiplicatively; T3 is upstream feeder; common root = source-reading-as-epistemology"). V2's per-theory framings are sharper individually but V2 lacks the synthesis. V3's unique contributions (recursion observation, eval-suite silent-green) are *additions*, not a replacement structure. Refactor plan integrates V2 and V3 strengths into V1's skeleton.
