# Base Selection

## Quantitative Scoring (50% weight)

| Metric | Weight | qwen3.6-plus | glm-5.2 | Notes |
|--------|--------|--------------|---------|-------|
| Requirement coverage (RC) | 0.30 | 0.80 | 0.85 | glm covers more distinct audit dimensions (C2/I1/I4) |
| Internal consistency (IC) | 0.25 | 0.90 | 0.70 | glm's C3 over-reach ("fabricated") + truncation lower consistency |
| Specificity (SR) | 0.15 | 0.85 | 0.85 | Both cite file:line/section evidence |
| Dependency completeness (DC) | 0.15 | 0.90 | 0.60 | **glm truncated at M1** — dangling MINOR section, no synthesis |
| Section coverage (SC) | 0.15 | 1.00 | 0.70 | qwen has 5 complete sections; glm's tail is cut |
| **quant_score** | | **0.869** | **0.750** | |

`quant = RC·.30 + IC·.25 + SR·.15 + DC·.15 + SC·.15`
- qwen: .240+.225+.128+.135+.150 = **0.878** → normalized **0.87**
- glm: .255+.175+.128+.090+.105 = **0.753** → **0.75**

## Qualitative Scoring (50% weight) — 30-criterion additive binary rubric

| Dimension (5 ea.) | qwen | glm |
|-------------------|------|-----|
| Completeness | 4 | 3 (truncated; but +unique C2/I1/I4) |
| Correctness | 4 | 3 (C3 fabrication claim NOT MET; A-001 premise NOT MET) |
| Structure | 5 | 3 (truncated tail, orphaned MINOR heading) |
| Clarity | 4 | 4 |
| Risk coverage | 3 | 4 (verification-skip + scope-creep raise real risk) |
| Invariant & edge-case | 3 | 3 |
| **Total /30** | **23** | **20** |

- qwen qual = 23/30 = **0.77**
- glm qual = 20/30 = **0.67**

**Edge-case floor (1/5):** qwen 3/5, glm 3/5 — both eligible.

## Position-Bias Mitigation
Dual-pass (forward qwen→glm, reverse glm→qwen) agreed on ranking in both passes. No disagreement requiring re-evaluation. qwen ranks first in both orders.

## Combined Scoring

| Variant | quant×.50 | qual×.50 | **Combined** |
|---------|-----------|----------|--------------|
| qwen3.6-plus | 0.435 | 0.385 | **0.820** |
| glm-5.2 | 0.375 | 0.335 | **0.710** |

Margin: **11.0%** (> 5% → no tiebreaker needed).

## Selected Base: Variant 1 (qwen3.6-plus)

**Selection rationale:** qwen wins on completeness (glm is truncated at M1 — a truncated base structurally loses content), structural integrity, internal consistency, and provides a reusable scaffold (suspect-source table + adversarial-scoring weights). It is the better *chassis* to merge into.

**Critical caveat — the base is NOT the more insightful review.** glm's three highest-value catches (C2 verification-skip, I1 aienv scope, I4 xpass) are all CONFIRMED real and all ABSENT from qwen. The merge's job is therefore **graft-heavy**: qwen scaffold + glm's confirmed unique findings + adversarial corrections. Base selection ≠ "qwen was right"; it means "qwen is the cleaner container."

**Strengths to preserve (from base):** complete section structure, graded severity scale, suspect-source table, adversarial-scoring weights, honest "unverified" labeling of additive-only.

**Strengths to incorporate (from glm + adjudication):**
- glm C2 → new finding **AUD-2** (verification-round skip, CONFIRMED).
- glm I1 → **AUD-4** (aienv.py scope drift, CONFIRMED).
- glm I4 → **AUD-6** (xpass follow-up).
- glm I2 `test_cli_smoke.py` sharpening → fold into **AUD-3**.
- Adjudicator A-001/A-002 → **downgrade** qwen Finding 1 / glm C1 to MINOR reconciliation (**AUD-1**).
- Verified 0-diff → **resolve** qwen Finding 4 as SATISFIED.
- Reject qwen Finding 2 "violation" framing; adopt glm I5 WARN.
- Downgrade glm C3 to LOW field-semantics note.
