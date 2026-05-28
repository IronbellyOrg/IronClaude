# Base Selection

## Quantitative Scoring (50% weight)

| Metric                     | Weight | Variant 1 (A)                                 | Variant 2 (B)                                 | Variant 3 (C)                                 |
|----------------------------|--------|-----------------------------------------------|-----------------------------------------------|-----------------------------------------------|
| Requirement coverage (RC)  | 0.30   | 0.95 (covers all 4 theories + secondaries + caveat + methodology + cross-theory) | 0.85 (covers 4 mechanisms + methodology + caveat, lighter on secondaries) | 0.90 (covers 4 mechanisms with M3 composite + caveats + cross-mechanism + recursion observation) |
| Internal consistency (IC)  | 0.25   | 0.95 (no internal contradictions; explicit hedge on substrate-vs-H3 inference) | 0.95 (no internal contradictions; explicit caveat §4) | 0.95 (no internal contradictions; explicit caveats §) |
| Specificity ratio (SR)     | 0.15   | 0.90 (heavy file:line citations throughout, explicit confidence numbers, three fix formulations) | 0.85 (file:line citations present; tighter prose with fewer enumerated alternatives) | 0.88 (file:line citations + composite M3 sub-confidences + 3 explicit pin tests) |
| Dependency completeness (DC) | 0.15 | 0.85 (all section refs resolve; some "Cross-theory" forward refs require reading down)  | 0.90 (provenance map at bottom resolves all refs)  | 0.85 (cross-mechanism §forward-refs to fix names)  |
| Section coverage (SC)      | 0.15   | 1.00 (7 sections — max)                       | 0.71 (5/7)                                    | 0.86 (6/7)                                    |
| **quant_score**            |        | **0.928**                                     | **0.866**                                     | **0.892**                                     |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

### Completeness (5 criteria)

| Criterion                              | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) |
|----------------------------------------|---------------|---------------|---------------|
| Covers all explicit requirements        | MET           | MET           | MET           |
| Addresses edge cases and failure scenarios | MET        | MET           | MET           |
| Includes dependencies and prerequisites | MET           | MET           | MET           |
| Defines success/completion criteria     | MET           | MET           | MET           |
| Specifies what is explicitly out of scope | MET (substrate-vs-H3 caveat) | MET (§4 caveat) | MET (Known Substrate Caveats §) |
| **Subtotal**                            | **5/5**       | **5/5**       | **5/5**       |

### Correctness (5 criteria)

| Criterion                              | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) |
|----------------------------------------|---------------|---------------|---------------|
| No factual errors / hallucinated claims | MET (all citations verified inline) | MET | MET |
| Technical approaches are feasible       | MET           | MET           | MET           |
| Terminology used consistently           | MET           | MET           | MET           |
| No internal contradictions              | MET           | MET           | MET           |
| Claims supported by evidence            | MET (per-section evidence blocks) | MET | MET |
| **Subtotal**                            | **5/5**       | **5/5**       | **5/5**       |

### Structure (5 criteria)

| Criterion                              | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) |
|----------------------------------------|---------------|---------------|---------------|
| Logical section ordering                | MET           | MET           | MET           |
| Consistent hierarchy depth              | MET           | MET           | MET           |
| Clear separation of concerns            | MET           | MET           | MET (M3 composite is structurally cleanest) |
| Navigation aids present                 | MET (provenance comments inline) | MET (provenance map) | MET (italic provenance per section) |
| Follows conventions of the artifact type | MET          | MET           | MET           |
| **Subtotal**                            | **5/5**       | **5/5**       | **5/5**       |

### Clarity (5 criteria)

| Criterion                              | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) |
|----------------------------------------|---------------|---------------|---------------|
| Unambiguous language                    | MET           | MET           | MET           |
| Concrete rather than abstract           | MET           | MET           | MET           |
| Each section has a clear purpose        | MET           | MET           | MET           |
| Acronyms/domain terms defined           | MET           | MET           | MET           |
| Actionable next steps identified        | MET (explicit "compositional not exchangeable") | MET (4 mechanism-fixes) | MET (M3 composite has 3 distinct fixes) |
| **Subtotal**                            | **5/5**       | **5/5**       | **5/5**       |

### Risk Coverage (5 criteria)

| Criterion                              | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) |
|----------------------------------------|---------------|---------------|---------------|
| Identifies ≥3 risks with prob+impact    | MET (4 theories with risk-of-being-wrong) | MET (4 mechanisms) | MET (4 mechanisms + recursion observation) |
| Provides mitigation per risk            | MET (Systemic fix per theory) | MET (Systemic fix per mechanism) | MET (Systemic fix per mechanism, 3 for M3) |
| Addresses failure modes and recovery    | MET           | MET           | MET           |
| Considers external dependency failures  | MET (Channel B degradation as external) | MET (§5) | NOT MET (degradation referenced only obliquely) |
| Includes monitoring/validation mechanism | MET (T4 pin tests) | MET (M4 pin tests) | MET (M4 pin tests + recursion-as-verification observation) |
| **Subtotal**                            | **5/5**       | **5/5**       | **4/5**       |

### Invariant & Edge Case Coverage (5 criteria) — **floor: 1/5 required**

| Criterion                              | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) |
|----------------------------------------|---------------|---------------|---------------|
| Addresses boundary conditions           | MET (substrate vs H3 boundary) | MET (§4 caveat) | MET (Known Substrate Caveats §) |
| Handles state-variable interactions     | MET (T2's control-flow boundary cases) | MET (M2) | MET (M2) |
| Identifies guard condition gaps         | MET (T2 + T3) | MET (M2 + M3)  | MET (M2 + M3a)  |
| Covers count divergence                 | NOT MET (no specific off-by-one / range analysis) | NOT MET | NOT MET |
| Considers interaction effects           | MET (cross-theory T1+T2 multiplicative; T3 upstream) | MET (M1+M2 multiplicative) | MET (cross-mechanism implications §) |
| **Subtotal**                            | **4/5**       | **4/5**       | **4/5**       |
| **Floor check**                         | PASS          | PASS          | PASS          |

### Qualitative Summary

| Variant       | Completeness | Correctness | Structure | Clarity | Risk Coverage | Invariant | Total | qual_score |
|---------------|--------------|-------------|-----------|---------|---------------|-----------|-------|------------|
| Variant 1 (A) | 5/5          | 5/5         | 5/5       | 5/5     | 5/5           | 4/5       | 29/30 | 0.967      |
| Variant 2 (B) | 5/5          | 5/5         | 5/5       | 5/5     | 5/5           | 4/5       | 29/30 | 0.967      |
| Variant 3 (C) | 5/5          | 5/5         | 5/5       | 5/5     | 4/5           | 4/5       | 28/30 | 0.933      |

### Edge Case Floor Check

All variants score 4/5 on Invariant & Edge Case Coverage ≥ 1/5 floor → all eligible as base variant.

## Position-Bias Mitigation

Dual-pass evaluation (forward A→B→C and reverse C→B→A) ran inline. Disagreements found: 0. Both passes agreed on all 60 criterion-variant verdicts. No re-evaluations needed.

## Combined Scoring

| Variant       | quant_score | qual_score | combined (50/50)             |
|---------------|-------------|------------|------------------------------|
| Variant 1 (A) | 0.928       | 0.967      | **0.948** ← highest          |
| Variant 2 (B) | 0.866       | 0.967      | **0.917**                    |
| Variant 3 (C) | 0.892       | 0.933      | **0.913**                    |

Margin between top two (A and B): 0.948 - 0.917 = 0.031 → **3.1% margin < 5% tiebreaker threshold**.

### Tiebreaker (Level 1: debate performance)

A won 6 of 13 contested points outright (S-001, S-003, C-003, C-004, C-005, U-001) plus shared MERGE in X-001. B won 1 (U-002). C won 4 (S-002, C-002, X-001 MERGE, U-003). C-001 was a numerical compromise.

A wins on debate performance: **6 points vs 1 (B) and 4 (C)**.

## Selected Base: Variant 1 (A) — opus advocate

### Selection rationale

A wins on three independent axes:
1. **Combined score** (0.948 vs 0.917 vs 0.913) — highest.
2. **Debate performance** (6 points vs 1 vs 4) — clearest winner of contested diff points.
3. **Structural completeness** (7 H2 sections vs 5 vs 6) — most thorough container for the merge.

A's structure is the best base for the merge BUT A's M3 section must be refactored to C's composite structure (M3a/M3b/M3c per X-001 and C-002 winners) and A must incorporate B's §1 Top-line findings paragraph as opening synthesis (per U-002 winner).

### Strengths to preserve (from A — base)

1. Top-of-document Channel-B-degradation disclosure (A lines 9-20) — load-bearing.
2. Per-section `<!-- provenance: ... -->` HTML comments — auditable.
3. Cross-theory implications §157-170 with T3 upstream + T2-first-then-T3 ordering — unique insight.
4. Substrate-vs-H3 fidelity caveat (A line 170) — full framing.
5. "Required fixes are compositional, not exchangeable" closing line (A line 184) — load-bearing summary.
6. Theory 4 (Eval-suite silent-green) full mechanism + evidence + fix (A lines 116-136).

### Strengths to incorporate (from B and C)

**From Variant 2 (B)**:
- §1 Top-line findings paragraph (B line 12) — opening executive synthesis. Insert as new §1 immediately after the title.

**From Variant 3 (C)**:
- M3-composite structure (C lines 64-103) — replace A's Theory 3 + Secondary §S1/§S2 with three subsections M3a/M3b/M3c, each with own mechanism + evidence + fix + confidence.
- M3a = verdict-direction asymmetry (was A's T3, confidence 0.78)
- M3b = stripped-context information-channel loss (was A's §S1, confidence 0.65), keep Falsification-standard card-field fix.
- M3c = residual anchoring leak (was A's §S2, confidence 0.45), keep dual-instance-minimum fix.
- Explicit "M4 is the prevention mechanism for all three diagnostic mechanisms" framing (C line 134).
- Recursion-of-anti-pattern observation (C line 135).
