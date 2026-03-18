# Base Selection: Solution C Design Specs

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (Integration) | Variant B (Provenance) | Variant C (Sanitize) |
|--------|--------|------------------------|----------------------|---------------------|
| Requirement Coverage (RC) | 0.30 | 0.95 — covers both fixes, tests, rollback, sync | 0.65 — covers provenance fix + diagnostics fix only | 0.60 — covers sanitize fix only |
| Internal Consistency (IC) | 0.25 | 0.95 — no internal contradictions | 1.00 — no contradictions | 0.90 — recommends "minimal fix" but presents 3 alternatives creating some confusion |
| Specificity Ratio (SR) | 0.15 | 0.85 — specific line numbers, file paths, test IDs | 0.90 — specific line numbers, full code, charset rationale | 0.92 — specific line numbers, full function, byte counts in edge cases |
| Dependency Completeness (DC) | 0.15 | 0.90 — all cross-references resolve | 0.85 — Part 1 reference is external | 0.80 — Part 2 reference is external |
| Section Coverage (SC) | 0.15 | 1.00 — 6 sections (max) | 1.00 — 7 sections (max tied) | 0.86 — 6 sections |

**Quant scores**:
- Variant A: (0.95×0.30) + (0.95×0.25) + (0.85×0.15) + (0.90×0.15) + (1.00×0.15) = 0.285 + 0.2375 + 0.1275 + 0.135 + 0.15 = **0.935**
- Variant B: (0.65×0.30) + (1.00×0.25) + (0.90×0.15) + (0.85×0.15) + (1.00×0.15) = 0.195 + 0.25 + 0.135 + 0.1275 + 0.15 = **0.8575**
- Variant C: (0.60×0.30) + (0.90×0.25) + (0.92×0.15) + (0.80×0.15) + (0.86×0.15) = 0.18 + 0.225 + 0.138 + 0.12 + 0.129 = **0.792**

## Qualitative Scoring (50% weight) — Additive Binary Rubric

### Completeness (5 criteria)

| Criterion | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| Covers all explicit requirements | MET — both fixes + tests | NOT MET — only Part 2 | NOT MET — only Part 1 |
| Addresses edge cases and failure scenarios | MET — rollback section | MET — 9 edge cases + false positive | MET — 9 edge cases |
| Includes dependencies and prerequisites | MET — ordering analysis | NOT MET — defers to Part 1 | NOT MET — defers to Part 2 |
| Defines success/completion criteria | MET — verification section | MET — test plan | MET — test plan |
| Specifies what is explicitly out of scope | NOT MET | NOT MET | MET — "Part 2 is defense-in-depth" |
| **Subtotal** | **4/5** | **2/5** | **3/5** |

### Correctness (5 criteria)

| Criterion | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| No factual errors | MET | MET | MET |
| Technical approaches feasible | MET | MET | MET |
| Terminology consistent | MET | MET | MET |
| No internal contradictions | MET | MET | NOT MET — presents 3 versions, final recommendation unclear |
| Claims supported by evidence | MET — line numbers cited | MET — line numbers + code | MET — line numbers + code |
| **Subtotal** | **5/5** | **5/5** | **4/5** |

### Structure (5 criteria)

| Criterion | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| Logical section ordering | MET | MET | MET |
| Consistent hierarchy depth | MET | MET | NOT MET — nested alternatives create confusion |
| Clear separation of concerns | MET | MET | MET |
| Navigation aids present | MET — checklist serves as TOC | NOT MET | NOT MET |
| Follows artifact type conventions | MET | MET | MET |
| **Subtotal** | **5/5** | **4/5** | **3/5** |

### Clarity (5 criteria)

| Criterion | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| Unambiguous language | MET | MET | NOT MET — "Recommendation: minimal fix" but simplified version shown first |
| Concrete rather than abstract | MET | MET | MET |
| Each section has clear purpose | MET | MET | MET |
| Acronyms/terms defined on first use | MET | MET | MET |
| Actionable next steps identified | MET — 4-phase checklist | MET — 6-step sequence | MET — 4-step checklist |
| **Subtotal** | **5/5** | **5/5** | **4/5** |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| Identifies ≥3 risks | MET — rollback scenarios | NOT MET — risk section is 1 paragraph | NOT MET — no rollback |
| Mitigation for each risk | MET — per-fix rollback | NOT MET | NOT MET |
| Failure modes and recovery | MET — full rollback plan | NOT MET | NOT MET |
| External dependency failures | NOT MET | NOT MET | NOT MET |
| Monitoring/validation for risk detection | MET — _log.info calls documented | NOT MET | MET — _log.info in function |
| **Subtotal** | **4/5** | **0/5** | **1/5** |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| Boundary conditions for collections | MET — empty file, no frontmatter | MET — empty file, empty frontmatter | MET — 9 edge cases |
| State variable interactions | MET — ordering analysis (sanitize before inject) | NOT MET | MET — impact analysis |
| Guard condition gaps | NOT MET — doesn't catch idempotency | MET — idempotency guards | NOT MET |
| Count divergence scenarios | MET — preamble_bytes return values | MET — byte counts | MET — byte counts in table |
| Interaction effects | MET — E2E test for sanitize+inject | NOT MET | MET — integration test |
| **Subtotal** | **4/5** | **3/5** | **4/5** |

### Qualitative Summary

| Dimension | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| Completeness | 4 | 2 | 3 |
| Correctness | 5 | 5 | 4 |
| Structure | 5 | 4 | 3 |
| Clarity | 5 | 5 | 4 |
| Risk Coverage | 4 | 0 | 1 |
| Invariant & Edge Case | 4 | 3 | 4 |
| **Total** | **27/30** | **19/30** | **19/30** |

**Qual scores**: A = 0.900, B = 0.633, C = 0.633

### Edge Case Floor Check
- Variant A: 4/5 — ELIGIBLE
- Variant B: 3/5 — ELIGIBLE
- Variant C: 4/5 — ELIGIBLE

## Combined Scoring

| Variant | Quant (50%) | Qual (50%) | Combined |
|---------|-------------|------------|----------|
| **Variant A** | 0.935 × 0.50 = 0.468 | 0.900 × 0.50 = 0.450 | **0.918** |
| Variant B | 0.858 × 0.50 = 0.429 | 0.633 × 0.50 = 0.317 | **0.745** |
| Variant C | 0.792 × 0.50 = 0.396 | 0.633 × 0.50 = 0.317 | **0.713** |

**Margin**: A leads B by 17.3% — no tiebreaker needed.

## Selected Base: Variant A (Integration Plan)

**Selection rationale**: Variant A scores highest on both quantitative (0.935) and qualitative (0.900) axes. It is the only variant that covers the full Solution C scope: both fixes, their ordering, testing, verification, rollback, and deployment. Its primary gaps (idempotency, lstrip charset) are additive improvements from B that can be cleanly incorporated.

**Strengths to preserve**:
- Complete integration sequence with ordering guarantees
- 12-test regression plan with E2E coverage
- Per-fix rollback plan with independence analysis
- 4-phase implementation checklist
- Named existing regression tests

**Strengths to incorporate from Variant B**:
- Idempotency guards for `_inject_provenance_fields` (Section 3) — HIGH priority
- Explicit `.lstrip("\n\r\t ")` charset with rationale (Section 2.3) — HIGH priority
- `_inject_pipeline_diagnostics` idempotency (Section 5.2 tests) — MEDIUM priority
- False positive analysis for substring matching — LOW priority

**Strengths to incorporate from Variant C**:
- Full `_sanitize_output` function body (minimal fix version, Section 2) — HIGH priority
- 9-entry edge case table with byte counts (Section 3) — MEDIUM priority
- Impact analysis on other pipeline steps (Section 4) — MEDIUM priority
