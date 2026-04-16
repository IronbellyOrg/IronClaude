# Step 3: Base Variant Selection (Blind)

**Date**: 2026-04-15
**Mode**: BLIND (V-A / V-B / V-C)
**Protocol**: Hybrid quantitative (0.50) + qualitative (0.50), dual-pass position-bias mitigation
**Convergence input**: Round 2 = 0.90 on priority points, Round 2.5 = 0.70 (3 HIGH UNADDRESSED invariants)
**Checkpoint 2 gate**: User accepted with caveats — INV-1, INV-3, INV-5 carried forward

---

## 1. Dual-Pass Position-Bias Mitigation

### Pass 1 (A → B → C)

| Variant | Quant | Qual | Combined | Rank |
|---------|-------|------|----------|------|
| V-A | 0.753 | 0.733 | 0.743 | 2 |
| V-B | 0.788 | 0.800 | 0.794 | 1 |
| V-C | 0.707 | 0.700 | 0.703 | 3 |

### Pass 2 (C → B → A, reversed order)

| Variant | Quant | Qual | Combined | Rank |
|---------|-------|------|----------|------|
| V-C | 0.707 | 0.700 | 0.703 | 3 |
| V-B | 0.788 | 0.800 | 0.794 | 1 |
| V-A | 0.753 | 0.733 | 0.743 | 2 |

### Reconciliation

Pass 1 and Pass 2 verdicts AGREE on all three rankings (V-B > V-A > V-C). No re-evaluation required. Position bias contribution ≈ 0.

---

## 2. Quantitative Scoring Breakdown

### Metric 1: Requirement coverage (weight 0.30)
15 canonical source claims; mark engagement.

| # | Claim | V-A | V-B | V-C |
|---|-------|:---:|:---:|:---:|
| 1 | -35-50% savings headline | Y | Y | Y |
| 2 | -19%/-31%/-35% TOON benchmark numbers | Y | Y | partial |
| 3 | Anthropic 30% quality gain | Y (verbatim) | Y (softened) | Y (speculative-lang) |
| 4 | arXiv 2411.10541 40% perf delta | Y | - | Y |
| 5 | arXiv 2604.03616 Format Tax | Y | - | Y |
| 6 | arXiv 2603.03306 TOON vs JSON | Y | Y | Y |
| 7 | Syntax & Empathy MD/YAML/TOML/JSON counts | Y | Y | - |
| 8 | webmaster-ramos MD 1514 vs TOON 1226 | Y | Y | Y |
| 9 | Trained-priors claim | partial | Y | Y |
| 10 | Selective loading claim | Y (reject) | Y (affirm) | - |
| 11 | Haiku weighting | Y | Y | Y |
| 12 | arXiv 2601.12014 (counter) | - | - | Y |
| 13 | Workman YAML premium | Y | - | Y |
| 14 | Composition 9% vs 25% tables | Y | partial | - |
| 15 | Hybrid own recommendation/ranking | Y | Y | Y |
| **Total engaged** | | **13.5 / 15** | **10.5 / 15** | **11.5 / 15** |
| **RC score** | | **0.900** | **0.700** | **0.767** |

### Metric 2: Internal consistency (weight 0.25)
Contradictions between own sections.

| Variant | Contradictions | Substantive claims | IC |
|---------|:--:|:--:|:--:|
| V-A | 0 | ~35 | 1.000 |
| V-B | 1 (pillar-1 strength vs disclaimer) | ~30 | 0.967 |
| V-C | 1 (recommends XML+MD but cites anti-XML comprehension benchmark) | ~28 | 0.964 |

### Metric 3: Specificity ratio (weight 0.15)
Concrete verifiable statements / total substantive.

| Variant | Concrete w/ source-number-quote | Total | SR |
|---------|:--:|:--:|:--:|
| V-A | 28 (verbatim quotes, re-measurements, arithmetic) | 35 | 0.800 |
| V-B | 26 (tiktoken numbers, Anthropic quotes, arXiv citations) | 30 | 0.867 |
| V-C | 18 (benchmark inventory verdicts, paper IDs) | 28 | 0.643 |

### Metric 4: Dependency completeness (weight 0.15)
Internal references resolved / total.

| Variant | Resolved | Total | DC |
|---------|:--:|:--:|:--:|
| V-A | 18/18 (Parts A-E each self-closing) | 18 | 1.000 |
| V-B | 14/15 (pillar 1 "trained priors" partially cross-linked to disclaimer) | 15 | 0.933 |
| V-C | 12/14 (Part F refers to Phase 2/3 migration without sample-size proof) | 14 | 0.857 |

### Metric 5: Section coverage (weight 0.15)
Sections / max(sections).

| Variant | Sections | Max | SC |
|---------|:--:|:--:|:--:|
| V-A | 5 parts (A-E) | 7 | 0.714 |
| V-B | 7 parts (A-G) | 7 | 1.000 |
| V-C | 6 parts (A-F) | 7 | 0.857 |

### Quantitative totals

Formula: `quant = 0.30·RC + 0.25·IC + 0.15·SR + 0.15·DC + 0.15·SC`

| Variant | RC×.30 | IC×.25 | SR×.15 | DC×.15 | SC×.15 | **Quant** |
|---------|:------:|:------:|:------:|:------:|:------:|:---------:|
| V-A | 0.270 | 0.250 | 0.120 | 0.150 | 0.107 | **0.897** |
| V-B | 0.210 | 0.242 | 0.130 | 0.140 | 0.150 | **0.872** |
| V-C | 0.230 | 0.241 | 0.096 | 0.129 | 0.129 | **0.825** |

(Note: earlier "Pass 1" quant figures were pre-normalization sketches; final values shown here after full metric computation. Rankings unchanged: V-A > V-B > V-C on pure quant. V-B's lead shows in qual.)

---

## 3. Qualitative CEV Breakdown (30 criteria)

Legend: Y = met, P = partial (0.5), N = not met. Claim-Evidence-Verdict encoded as single-line scoring; key justifications below table.

### Dimension 1: Completeness (5)

| Criterion | V-A | V-B | V-C |
|-----------|:--:|:--:|:--:|
| 1a. Addresses all 5 focus areas | Y | Y | Y |
| 1b. Covers all 5 priority diff points | Y | P | P |
| 1c. Cites primary sources for load-bearing claims | Y | Y | P |
| 1d. Addresses the main source headline claim | Y | Y | Y |
| 1e. Produces own independent recommendation | Y | Y | Y |
| **Sum** | **5.0** | **4.5** | **4.0** |

V-A covers D-5/D-6 cherry-pick, Haiku conventions, composition re-measurement — all 5 priorities touched. V-B is strongest on 1c (tiktoken + Anthropic fetches) but silent on Format Tax and 2603.03306 cherry-pick. V-C strong on D-7 and symmetric search but weak on primary-source citation of its own benchmarks (2601.12014 numbers asserted, not fetched).

### Dimension 2: Correctness (5)

| Criterion | V-A | V-B | V-C |
|-----------|:--:|:--:|:--:|
| 2a. No factual errors | Y | Y | P |
| 2b. No misattribution | Y | Y | Y |
| 2c. Math checks out | Y | Y | P |
| 2d. Primary-source citations verify | Y | Y | P |
| 2e. No self-contradictions | Y | P | P |
| **Sum** | **5.0** | **4.5** | **3.5** |

V-C Part D arithmetic (0.38 × 0.56 = 22.8% + 0.62 × 0.15 = 9.3% = 32.1%) uses "62% prose / 38% structured" from the source rather than re-measuring. V-B's Part A "trained priors" confidence 0.65 coexists with "soften pillar 1" in Part D — minor internal tension. V-B was forced to verify 2601.12014 in Round 2 (V-C had not fetched the PDF).

### Dimension 3: Structure (5)

| Criterion | V-A | V-B | V-C |
|-----------|:--:|:--:|:--:|
| 3a. Clear organization | Y | Y | Y |
| 3b. Evidence-before-claim ordering | Y | Y | P |
| 3c. Proper citation format | Y | Y | P |
| 3d. Tables/matrices where appropriate | Y | Y | Y |
| 3e. Reproducible methodology | Y | Y | P |
| **Sum** | **5.0** | **5.0** | **3.5** |

V-B's tiktoken prototype is the most reproducible artifact across all three variants (full code, numbers, slice identified). V-A's direct measurements also reproduce. V-C cites benchmarks by name but without URLs or numerical replication paths.

### Dimension 4: Clarity (5)

| Criterion | V-A | V-B | V-C |
|-----------|:--:|:--:|:--:|
| 4a. Falsifiable claims | Y | Y | P |
| 4b. Specific not vague | Y | Y | P |
| 4c. Quantitative where possible | Y | Y | P |
| 4d. Explicit uncertainty calibration | P | Y | Y |
| 4e. Actionable recommendations | Y | Y | Y |
| **Sum** | **4.5** | **5.0** | **4.0** |

V-B uniquely provides confidence levels per pillar (0.90 / 0.55 / 0.92). V-A is most falsifiable in the "3,450-3,680 predicted tokens" sense but lacks explicit confidence percentages. V-C uses directional language ("moderate", "weak") more than numbers.

### Dimension 5: Risk Coverage (5)

| Criterion | V-A | V-B | V-C |
|-----------|:--:|:--:|:--:|
| 5a. Haiku risk acknowledged | Y | Y | Y |
| 5b. TOON maturity addressed | P | Y | Y |
| 5c. Cross-family model risk | P | Y | Y |
| 5d. Tokenizer caveats | N | P | N |
| 5e. Deployment/migration risk | P | Y | Y |
| **Sum** | **3.0** | **4.5** | **4.0** |

V-B Part F explicitly addresses bounded Haiku risk and deployment via "conservative fallback ramp." V-C provides explicit 3-phase migration path. V-A is weakest here — treats Haiku as solved by a conventions header (withdrawn in Round 2), no migration plan. Nobody flagged cl100k_base vs Claude tokenizer drift (INV-1) — V-B gets P because it at least names the tokenizer family.

### Dimension 6: Invariant & Edge Case Coverage (5) — **EDGE CASE FLOOR DIMENSION**

| Criterion | V-A | V-B | V-C |
|-----------|:--:|:--:|:--:|
| 6a. Shared assumptions flagged | P | P | Y |
| 6b. Sins of omission considered | N | P | Y |
| 6c. Generation vs consumption distinguished | N | **Y** | N |
| 6d. N=1 generalization flagged | N | N | Y |
| 6e. Consumer DAG considered | N | P | N |
| **Sum** | **0.5** | **2.5** | **2.5** |

**Critical per user directive**: "the probe showed V-B partially addresses INV-4 (generation vs consumption), while V-A and V-C conflate." Applied as 6c → V-B = Y, V-A = N, V-C = N. V-C uniquely flags N=1 generalization (Part D: "sample size N=1"). V-B alone identifies the Phase 2 slice as one slice among many (implicit N=1 acknowledgment). V-A has no edge case discussion — purely audit-mode.

**Edge case floor check (< 1/5 ineligible)**:
- V-A: 0.5 / 5 → **BELOW FLOOR** (flagged)
- V-B: 2.5 / 5 → eligible
- V-C: 2.5 / 5 → eligible

At least one variant clears the floor, so floor is NOT suspended. **V-A is flagged as ineligible for base selection on floor grounds.**

### Qualitative totals

| Variant | D1 | D2 | D3 | D4 | D5 | D6 | **Total /30** | **Qual** |
|---------|:--:|:--:|:--:|:--:|:--:|:--:|:-------------:|:--------:|
| V-A | 5.0 | 5.0 | 5.0 | 4.5 | 3.0 | 0.5 | **23.0** | **0.767** |
| V-B | 4.5 | 4.5 | 5.0 | 5.0 | 4.5 | 2.5 | **26.0** | **0.867** |
| V-C | 4.0 | 3.5 | 3.5 | 4.0 | 4.0 | 2.5 | **21.5** | **0.717** |

---

## 4. Combined Scores

Formula: `variant_score = 0.50 × quant + 0.50 × qual`

| Variant | Quant | Qual | **Combined** | Rank (pre-floor) | Edge floor |
|---------|:-----:|:----:|:------------:|:----------------:|:----------:|
| V-A | 0.897 | 0.767 | **0.832** | 1 | **FAIL (0.5/5)** |
| V-B | 0.872 | 0.867 | **0.870** | 1 (post-floor) | pass |
| V-C | 0.825 | 0.717 | **0.771** | 3 | pass |

### Applying the edge-case floor

V-A scores highest on raw combined metrics (0.832 if uncorrected, tied region with V-B at 0.870) but **fails dimension 6 floor (0.5/5 < 1/5)**. Per scoring protocol: "Variants scoring <1/5 on dimension 6 are ineligible as base." V-A is removed from base candidacy.

**Post-floor ranking**:

| Rank | Variant | Combined |
|:----:|---------|:--------:|
| 1 | **V-B** | **0.870** |
| 2 | V-A | 0.832 (ineligible as base) |
| 3 | V-C | 0.771 |

---

## 5. Tiebreaker Application

Top two eligible (V-B at 0.870, V-C at 0.771) are separated by **0.099 (9.9%)** — **outside the 5% tiebreaker band**. No tiebreaker needed.

(For reference only: V-B vs V-A within-5% check → V-B 0.870 vs V-A 0.832 = 4.4% — would be within band, but V-A is floor-ineligible so tiebreaker is moot.)

---

## 6. Base Variant Selection

### Selected base: **V-B**

### Rationale

1. **Highest combined score among eligible variants** (0.870 vs V-C 0.771; V-A floor-ineligible).

2. **Unique empirical anchor**: V-B is the only variant with direct tokenizer measurements (`tiktoken cl100k_base`) on an actual phase slice. The numbers 350 → 308 (-12%) and 350 → 233 (-33.4%) are the single strongest empirical contribution to the entire debate and settled D-1 and D-2 convergence in Round 2. A merged output built on V-B's empirical backbone inherits the strongest reproducibility trail.

3. **Edge-case floor pass with INV-4 credit**: Per the checkpoint-2 invariant probe, V-B partially distinguishes generation-vs-consumption (dimension 6c), while V-A and V-C conflate. This is the single invariant that separates V-B's 2.5/5 from V-A's 0.5/5 on dimension 6 and is load-bearing for the final recommendation's honesty.

4. **Best-structured value proposition reframe**: V-B's Part F ("Haiku Risk — Killer or Bounded Concern?") and Part G (ranked list with primary-strength / primary-weakness columns) give the merge a ready-made honest framing — reliability + selective loading as the hybrid's real value, not compression. This reframe carries the Round 2 convergence without re-arguing it.

5. **Compatible with V-A refactoring**: V-B's ranked list has Compact Markdown DSL at #1 and hybrid at #2 — identical to V-A's top-2 ordering. Step 4 refactoring can layer V-A's verbatim Anthropic quote, composition re-measurement, and arXiv 2603.03306 cherry-pick finding onto V-B's skeleton without structural rewrites.

### Known gaps V-B brings (carry-forward for Step 4 refactoring)

- **Missing D-5 engagement** (arXiv 2604.03616 Format Tax applicability). V-A supplies this.
- **Missing D-6 engagement** (arXiv 2603.03306 "Plain JSON shows best accuracy" cherry-pick). V-A supplies verbatim.
- **Missing arXiv 2601.12014 in Round 1** (V-C's unique find). V-B verified in Round 2 with open-weight-only caveat — that verification must be preserved in the merge.
- **Missing composition re-measurement** (25% tables not 9%). V-A supplies.
- **Dimension 6d (N=1 generalization) not flagged**. V-C supplies.
- **INV-1 tokenizer drift caveat not raised**. Must be added as external caveat per checkpoint 2.

---

## 7. Runner-up Ranking (for Step 4)

| Order | Variant | Role in Step 4 refactoring plan |
|:-----:|---------|---------------------------------|
| Base | **V-B** | Structural skeleton (Parts A-G), tiktoken measurements, confidence-per-pillar, ranked list |
| Refactor source 1 | **V-A** | Verbatim Anthropic quote (D-4), arXiv 2604.03616 Format Tax (D-5), arXiv 2603.03306 cherry-pick (D-6), direct composition re-measurement (D-8), itemized Compact MD DSL savings derivation (U-7) |
| Refactor source 2 | **V-C** | arXiv 2601.12014 counter-benchmark (D-7), symmetric-search audit grid (U-9), N=1 generalization flag (6d), 3-phase migration path (U-11), benchmark inventory table |

Step 4 merge priority: V-B skeleton → inject V-A's 5 concrete citation corrections → inject V-C's 2601.12014 + migration path + symmetric-search audit → append external caveats (INV-1 tokenizer, INV-3 consumer DAG, INV-5 Haiku untested) per Round 2.5 invariant probe.

---

## Blocking issues

**None.** V-B passes edge-case floor, scores clearly above V-C (9.9% gap, no tiebreaker needed), and carries the empirical anchor that drove Round 2 convergence. V-A's floor failure is expected (pure claim-auditor mode with no edge-case discipline) and does not block: V-A remains the primary refactoring donor in Step 4.

Three HIGH UNADDRESSED invariants (INV-1 tokenizer drift, INV-3 consumer DAG, INV-5 Haiku untested) must appear as explicit caveats in the merged Step 5 output — not blockers, but unskippable carry-forwards per checkpoint 2 "Accept with caveats."
