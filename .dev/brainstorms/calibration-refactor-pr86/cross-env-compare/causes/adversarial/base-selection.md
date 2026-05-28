# Base Selection — Cross-Environment Causes Merge

## Hybrid Scoring (per SKILL.md §Step 3)

### Quantitative Layer (50% weight)

| Metric | Weight | V1 (pr86) | V2 (T4) | Notes |
|--------|--------|-----------|---------|-------|
| Requirement coverage | 0.30 | 0.85 | 0.70 | Both cover the core question "why did calibration fail?"; V1 covers more mechanism breadth. |
| Internal consistency | 0.25 | 0.95 | 0.95 | Both internally consistent; no contradictions within each document. |
| Specificity ratio (concrete/substantive) | 0.15 | 0.90 | 0.85 | V1 has more verbatim file:line citations; V2 has the irrefutable `ls` evidence. |
| Dependency completeness (internal refs) | 0.15 | 0.92 | 0.85 | V1's cross-mechanism implications resolve all internal references; V2 has open INV-002. |
| Section coverage (relative to max) | 0.15 | 1.00 | 0.55 | V1 has all sections V2 has, plus M4 + cross-mechanism + synthesis addendum. |

**V1 quant_score** = 0.85×0.30 + 0.95×0.25 + 0.90×0.15 + 0.92×0.15 + 1.00×0.15 = 0.255 + 0.2375 + 0.135 + 0.138 + 0.15 = **0.9155**

**V2 quant_score** = 0.70×0.30 + 0.95×0.25 + 0.85×0.15 + 0.85×0.15 + 0.55×0.15 = 0.21 + 0.2375 + 0.1275 + 0.1275 + 0.0825 = **0.785**

### Qualitative Layer (50% weight — 30-criterion rubric)

| Dimension | V1 | V2 | Comments |
|-----------|----|----|----------|
| Completeness (5 criteria) | 5/5 | 3/5 | V1 covers M1/M2/M3a/M3b/M3c/M4 + sequencing + recursion-of-pattern. V2 misses M4 and M3b/M3c. |
| Correctness (5 criteria) | 4/5 | 5/5 | V2 has the irrefutable empirical-disk verification; V1 has one substrate-blind-spot (assumed calibrator ran). |
| Structure (5 criteria) | 5/5 | 4/5 | V1's mechanism-decomposition is structurally richer; V2's layer-taxonomy is cleaner but flatter. |
| Clarity (5 criteria) | 4/5 | 5/5 | V2 is terser and easier to scan; V1's depth requires more reader effort. |
| Risk Coverage (5 criteria) | 4/5 | 4/5 | V1 covers M4 regression risk + multiplicative compounding; V2 covers INV-002 partial-calibration + agent-mismatch. Different gaps. |
| Invariant & Edge Case Coverage (5 criteria) | 4/5 | 3/5 | V1 explicitly addresses Channel-B-degradation, fix-sequencing, substrate-vs-H3 fidelity. V2 surfaces INV-002 + INV-003 + agent-domain edge cases but fewer overall. |

**V1 qual_score** = 26/30 = **0.867**
**V2 qual_score** = 24/30 = **0.800**

### Combined Scoring

- **V1 total**: 0.50 × 0.9155 + 0.50 × 0.867 = 0.4578 + 0.4335 = **0.8913**
- **V2 total**: 0.50 × 0.785 + 0.50 × 0.800 = 0.3925 + 0.400 = **0.7925**

### Edge-Case Floor Check

Both variants score 4/5 (V1) and 3/5 (V2) on Invariant & Edge Case Coverage. Both clear the 1/5 threshold. Floor not triggered.

### Position-Bias Mitigation

Pass 1 (V1, V2 order): V1=0.8913, V2=0.7925 → V1 wins
Pass 2 (V2, V1 order): V1=0.8913, V2=0.7925 → V1 wins (scores are positional-invariant; rubric is content-based, not order-dependent)
**Agreement**: V1 is the base.

### Tiebreaker Protocol

Top two variants differ by 0.8913 - 0.7925 = 0.0988 = **9.88%** — outside the 5% tiebreaker window. **No tiebreaker needed**.

---

## Base Selection: V1 (pr86-substrate run)

**Rationale**: V1 wins on completeness (covers M4 + M3b/M3c + cross-mechanism analysis) and section coverage (1.00 vs 0.55), and is only slightly behind on correctness (4/5 vs 5/5 due to the implicit-calibrator-ran assumption).

**Critical caveat**: V1's win does NOT mean V2's unique contributions are discarded. The merge MUST incorporate:
- V2's calibrator-non-execution cause (C-004 / V2-#1) as a new top cause
- V2's agent-domain mismatch (V2-#5) as a new top cause
- V2's INV-002 partial-calibration open invariant
- V2's layer-taxonomy framing as an annotative axis on V1's mechanisms
- V2's explicit naming of A-α (right-layer assumption) as a stated shared assumption

The substrate-divergence in X-001 means the merged output must be **substrate-aware** — explicitly tagging which causes apply on pr86-shaped substrates (calibrator ran, math broken) vs T4-shaped substrates (calibrator absent, enforcement broken) vs both.
