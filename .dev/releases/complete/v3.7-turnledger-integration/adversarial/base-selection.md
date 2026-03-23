# Base Selection: Validation Report Comparison

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (GPT) | Variant B (Sonnet) |
|--------|--------|-----------------|-------------------|
| Requirement Coverage (RC) | 0.30 | 0.85 — covers FR-1 through FR-7 + SC + NFR; 15 gap findings map to spec FRs | 0.92 — covers same FRs with finer granularity; 21 findings + cascade to SC criteria |
| Internal Consistency (IC) | 0.25 | 0.95 — no internal contradictions detected within variant | 0.93 — minor: GAP-M004 reclassifies FR-7.1 to MEDIUM while acknowledging the roadmap "explicitly says 9-field" |
| Specificity Ratio (SR) | 0.15 | 0.78 — recommended corrections cite spec lines but some lack exact language | 0.88 — recommended corrections include exact replacement text (e.g., GAP-H006 full rewrite) |
| Dependency Completeness (DC) | 0.15 | 0.90 — internal references (spec lines, roadmap lines) resolve correctly | 0.95 — internal references resolve; cascade references (H008→H001,H002,H003) create strong traceability chain |
| Section Coverage (SC) | 0.15 | 0.78 — 7 sections (Executive Summary, Verdict, Coverage, Gap Registry, Cross-Cutting, Integration, Agent Index) | 1.00 — 9 sections (adds Validation Ledger Delta, richer Agent Index table) — normalized max |

| | Variant A (GPT) | Variant B (Sonnet) |
|---|---|---|
| **Quant Score** | (0.85×0.30)+(0.95×0.25)+(0.78×0.15)+(0.90×0.15)+(0.78×0.15) = 0.255+0.238+0.117+0.135+0.117 = **0.862** | (0.92×0.30)+(0.93×0.25)+(0.88×0.15)+(0.95×0.15)+(1.00×0.15) = 0.276+0.233+0.132+0.143+0.150 = **0.934** |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

### Completeness (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Covers all explicit requirements from source input | MET — all spec FRs addressed | MET — all spec FRs addressed with finer decomposition |
| 2 | Addresses edge cases and failure scenarios | NOT MET — no cascade analysis | MET — cascade to SC-1/SC-8 shows failure path |
| 3 | Includes dependencies and prerequisites | MET — dependency ordering implicit | MET — Phase dependency chain explicit |
| 4 | Defines success/completion criteria | MET — verdict criteria table present | MET — verdict criteria table present |
| 5 | Specifies what is explicitly out of scope | NOT MET — no scope exclusion statement | NOT MET — no scope exclusion statement |
| | **Subtotal** | **3/5** | **4/5** |

### Correctness (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | No factual errors or hallucinated claims | MET — all citations verified against source files | MET — all citations verified against source files |
| 2 | Technical approaches are feasible | MET — recommended corrections are implementable | MET — recommended corrections are implementable and more specific |
| 3 | Terminology used consistently | MET — consistent throughout | MET — consistent throughout |
| 4 | No internal contradictions | MET — none detected | MET — GAP-M004 has minor tension but not a contradiction |
| 5 | Claims supported by evidence | MET — spec/roadmap line citations present | MET — spec/roadmap line citations present throughout |
| | **Subtotal** | **5/5** | **5/5** |

### Structure (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Logical section ordering | MET — executive → verdict → coverage → gaps → cross-cutting → integration → agents | MET — same logical flow with additions |
| 2 | Consistent hierarchy depth | MET — consistent H2/H3 usage | MET — consistent H2/H3/H4 usage |
| 3 | Clear separation of concerns | MET — each section is distinct | MET — finer domain separation |
| 4 | Navigation aids present | NOT MET — no cross-references within gap entries | MET — cascade references (H008→H001,H002,H003) and agent cross-references |
| 5 | Follows conventions of the artifact type | MET — standard validation report structure | MET — standard validation report structure with enhancements |
| | **Subtotal** | **4/5** | **5/5** |

### Clarity (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Unambiguous language | MET — clear throughout | MET — clear throughout |
| 2 | Concrete rather than abstract | MET — specific line citations | MET — specific line citations + exact replacement text |
| 3 | Each section has clear purpose | MET | MET |
| 4 | Acronyms and domain terms defined on first use | NOT MET — FR, SC, NFR used without definition | NOT MET — same issue |
| 5 | Actionable next steps clearly identified | MET — "Recommended correction" per gap | MET — "Recommended correction" per gap with more specific language |
| | **Subtotal** | **4/5** | **4/5** |

### Risk Coverage (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Identifies at least 3 risks with assessment | MET — 7 HIGH, 6 MEDIUM, 2 LOW with impact statements | MET — 9 HIGH, 5 MEDIUM, 2 LOW with impact statements |
| 2 | Provides mitigation strategy per risk | MET — "Recommended correction" per gap | MET — "Recommended correction" per gap |
| 3 | Addresses failure modes and recovery | NOT MET — no failure mode analysis | MET — cascade analysis shows SC-1/SC-8 failure modes |
| 4 | Considers external dependencies | NOT MET — no dependency failure analysis | NOT MET — no external dependency analysis |
| 5 | Includes monitoring or validation mechanism | NOT MET — no re-validation mechanism | MET — Validation Ledger Delta provides run-over-run monitoring |
| | **Subtotal** | **2/5** | **4/5** |

### Invariant & Edge Case Coverage (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Addresses boundary conditions for collections | NOT MET — requirement count disagreement not addressed | NOT MET — same |
| 2 | Handles state variable interactions across boundaries | NOT MET | MET — cascade analysis shows state interaction between FR-6 gaps and SC criteria |
| 3 | Identifies guard condition gaps | MET — FR-7.3 flush semantics is a guard condition gap | MET — FR-7.3 + FR-5.2 positive case |
| 4 | Covers count divergence scenarios | MET — GAP-H007 boundary/count | NOT MET — subsumed into cascade, not standalone |
| 5 | Considers interaction effects | NOT MET — no interaction analysis | MET — H008/H009 show interaction between gap closures and success criteria |
| | **Subtotal** | **2/5** | **3/5** |

**Edge Case Floor Check**: Both variants score ≥1/5 — both eligible.

### Qualitative Summary

| Dimension | Variant A (GPT) | Variant B (Sonnet) |
|-----------|-----------------|-------------------|
| Completeness | 3/5 | 4/5 |
| Correctness | 5/5 | 5/5 |
| Structure | 4/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 2/5 | 4/5 |
| Invariant & Edge Case | 2/5 | 3/5 |
| **TOTAL** | **20/30 = 0.667** | **25/30 = 0.833** |

## Position-Bias Mitigation

| Dimension | Pass 1 (A→B) | Pass 2 (B→A) | Agreement | Final |
|-----------|-------------|-------------|-----------|-------|
| Completeness | A:3, B:4 | A:3, B:4 | Yes | A:3, B:4 |
| Correctness | A:5, B:5 | A:5, B:5 | Yes | A:5, B:5 |
| Structure | A:4, B:5 | A:4, B:5 | Yes | A:4, B:5 |
| Clarity | A:4, B:4 | A:4, B:4 | Yes | A:4, B:4 |
| Risk Coverage | A:2, B:4 | A:2, B:4 | Yes | A:2, B:4 |
| Invariant | A:2, B:3 | A:2, B:3 | Yes | A:2, B:3 |

Disagreements found: 0. No re-evaluation needed.

## Combined Scoring

| Component | Weight | Variant A (GPT) | Variant B (Sonnet) |
|-----------|--------|-----------------|-------------------|
| Quantitative | 0.50 | 0.862 | 0.934 |
| Qualitative | 0.50 | 0.667 | 0.833 |
| **Combined** | **1.00** | **0.765** | **0.884** |

**Margin**: 11.9% (exceeds 5% tiebreaker threshold — no tiebreaker needed)

## Selected Base: Variant B (Sonnet Validation Report)

**Selection Rationale**: Variant B (Sonnet) wins decisively on both quantitative (0.934 vs 0.862) and qualitative (0.833 vs 0.667) layers. The margin of 11.9% exceeds the 5% tiebreaker threshold. Key differentiators:

**Strengths to Preserve from Base (Variant B)**:
- 7-domain decomposition providing granular coverage visibility
- Cascade analysis connecting individual gaps to success criteria (H008→SC-1, H009→SC-8)
- Validation Ledger Delta for temporal tracking
- More specific recommended corrections with exact replacement text
- Richer agent report index with findings columns

**Strengths to Incorporate from Variant A (GPT)**:
1. FR-7.1 severity: Reclassify GAP-M004 back to HIGH — the "9-field schema" text is a textual contradiction regardless of auto-computation
2. GAP-H007 boundary/count: Add as standalone finding — the 13-vs-62 requirement scoping disconnect is independently valuable
3. Adversarial pass status: Add process metadata confirming fresh re-read
