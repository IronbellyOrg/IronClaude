# Base Selection

## Quantitative Scoring (50% weight)

| Metric (weight) | V1 | V2 | V4 | V5 |
|-----------------|----|----|----|----|
| Requirement coverage RC (0.30) — SC1–SC7 + OQ1–6 | 0.95 | 0.90 | 0.95 | 0.90 |
| Internal consistency IC (0.25) | 0.80 (X-001 self-contradiction: counted class vs §17.7) | 0.95 | 0.98 | 0.95 |
| Specificity SR (0.15) | 0.90 | 0.95 | 0.92 | 0.95 |
| Dependency completeness DC (0.15) | 0.92 | 0.88 | 0.95 | 0.85 |
| Section coverage SC (0.15) | 1.0 | 1.0 | 1.0 | 0.95 |
| **quant_score** | **0.896** | **0.918** | **0.957** | **0.913** |

## Qualitative Scoring (50% weight) — 30-criterion CEV (dimension subtotals /5)

| Dimension | V1 | V2 | V4 | V5 |
|-----------|----|----|----|----|
| Completeness | 5 | 4 | 5 | 5 |
| Correctness | 3 (§10.8 counted bin contradicts §17.7 — CLAIM: "5th category"; EVIDENCE: §17.7 L1742 rejects it; VERDICT: NOT MET ×2) | 5 | 5 | 5 |
| Structure | 5 | 4 | 5 | 4 |
| Clarity | 4 | 5 | 5 | 5 |
| Risk Coverage | 4 | 4 | 5 | 4 |
| Invariant & Edge-Case Coverage | 3 | 4 | 5 (overlap/confidence split, auggie-down→advisory cap, modifier-not-class) | 5 (7-exclusion list, two-floor, confusion matrix) |
| **/30** | **24** | **26** | **30** | **28** |
| **qual_score** | **0.80** | **0.867** | **1.00** | **0.933** |

Edge-case floor (≥1/5 on Invariant dimension): all variants pass (V1=3, V2=4, V4=5, V5=5).

## Position-Bias Mitigation
Dual-pass (input order A–D, then reverse). Both passes agree V4 ranks first; the only disagreement was V2 vs V5 for #2 — re-evaluated: V5 edges V2 on FP-precision + §17.7-sanctioned Grounding-Gaps routing, V2 edges V5 on falsifiable proof. Treated as a near-tie (#2/#3), both fully grafted, so the ordering is immaterial to the merge.

## Combined Scoring

| Variant | quant×0.50 | qual×0.50 | **combined** | rank |
|---------|-----------|-----------|--------------|------|
| **V4** opus gate-placement | 0.479 | 0.500 | **0.979** | **1 (BASE)** |
| V5 sonnet/gpt-5.5 precision | 0.457 | 0.467 | 0.923 | 2 |
| V2 opus analyzer | 0.459 | 0.433 | 0.892 | 3 |
| V1 opus architect | 0.448 | 0.400 | 0.848 | 4 |

Margin V4→V5 = 5.6% (>5% → no tiebreaker needed; V4 wins outright).

## Selected Base: Variant 4 (opus:architect, gate-placement)

**Selection rationale.** The load-bearing axis of this design is *taxonomy + gate correctness* — the hardest thing to get right and the thing that determines whether the feature is conforming and trusted. V4 alone:
- Got X-001 right *and cited the actual constraint* (§17.7 → modifier-not-class), independently confirmed.
- Adds zero new gate machinery (maps to Drift/Regression by evidence; rides unmodified §14.5.2 cond-4 + §5.3 rule-3).
- Separates `overlap` (similarity) from `confidence` (meaningfulness) → the clean 3-signal L3 block bar.
- ADVISORY-BLOCKING-PREVIEW makes the eventual post-stage block predictable.
- auggie-down degrades to advisory-L2 (a weaker substrate may never block a build).

**Strengths to preserve (V4):** the L0–L4 ladder; finding-modifier mapping; high-bar-to-block/low-bar-to-advise asymmetry; mechanical NFR downgrade; pre/post structural table.

**Strengths to incorporate (graft):**
- **V2:** the 6-facet Capability Fingerprint as the rigorous definition of `overlap`; the worked Ω=0.88 ground-truth proof; the re-Read live-citation evidence discipline (§2.2); the "spec-conformant + name-divergent = invisible to existing gates" root-cause framing.
- **V5:** the per-dimension floors (C_cap≥0.80 ∧ C_shape≥0.70) on top of S_reuse≥0.82; the explicit 7-item exclusion list + confusion matrix; routing maybe-related/insufficient-grounding to **§10.6 Grounding Gaps** (§17.7-sanctioned).
- **V1:** the shared, versioned `refs/reuse-audit.md` sub-spec as the single source both protocols reference; the named extension points — **minus** the §10.8-counted-category and the §14.5.2 cond-4b new gate condition (both X-001 defects).

**Changes NOT made (rejected with rationale):**
- V1 `deviation_count_by_class.reuse_miss` + cond-4b → REJECTED (§17.7).
- V5 "pre-stage can hard-block a design" → REJECTED (3/4 + design-doc has nothing to gate); kept as advisory-strong.
- V1 ×1.1 advisory→blocking bridge multiplier → DEFERRED (INV-003: no guaranteed cross-invocation channel; post re-detects independently anyway). Optional future enhancement.
