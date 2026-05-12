# Base Selection: Roadmap Compression Strategy

## Quantitative Scoring (50% weight)

| Metric | Weight | Position A | Position B | Position C |
|--------|--------|-----------|-----------|------------|
| Requirement Coverage (RC) | 0.30 | 0.85 (covers independence, compression, ID preservation) | 0.40 (fails independence, minimal compression) | 0.90 (covers all stated requirements) |
| Internal Consistency (IC) | 0.25 | 1.00 (no contradictions) | 0.60 (pre-comparison contradicts independence req) | 0.90 (vocabulary issue is acknowledged) |
| Specificity Ratio (SR) | 0.15 | 0.90 (concrete compression ratios, field lists) | 0.70 (vague "depends on overlap") | 0.85 (concrete ratios, specific examples) |
| Dependency Completeness (DC) | 0.15 | 0.95 (self-contained) | 0.50 (depends on other file) | 0.90 (self-contained with vocabulary caveat) |
| Section Coverage (SC) | 0.15 | 0.85 (covers all sections) | 0.70 (missing non-table handling) | 1.00 (most complete coverage) |

**Quantitative scores:**
- Position A: (0.85u00d70.30) + (1.00u00d70.25) + (0.90u00d70.15) + (0.95u00d70.15) + (0.85u00d70.15) = 0.255 + 0.250 + 0.135 + 0.143 + 0.128 = **0.911**
- Position B: (0.40u00d70.30) + (0.60u00d70.25) + (0.70u00d70.15) + (0.50u00d70.15) + (0.70u00d70.15) = 0.120 + 0.150 + 0.105 + 0.075 + 0.105 = **0.555**
- Position C: (0.90u00d70.30) + (0.90u00d70.25) + (0.85u00d70.15) + (0.90u00d70.15) + (1.00u00d70.15) = 0.270 + 0.225 + 0.128 + 0.135 + 0.150 = **0.908**

## Qualitative Scoring (50% weight) u2014 30-Criterion Rubric

### Completeness (5 criteria)
| Criterion | A | C | Evidence |
|-----------|---|---|----------|
| Covers all explicit requirements | MET | MET | Both handle independence, compression, ID preservation |
| Addresses edge cases | NOT MET | MET | C addresses vocabulary drift; A ignores AC loss impact |
| Includes dependencies | MET | MET | Both preserve dep chains |
| Defines success criteria | MET | MET | Both define compression targets |
| Specifies out of scope | NOT MET | MET | C explicitly scopes vocabulary dictionary |
| **Subtotal** | **3/5** | **5/5** | |

### Correctness (5 criteria)
| Criterion | A | C | Evidence |
|-----------|---|---|----------|
| No factual errors | MET | MET | Both compression ratio estimates verifiable |
| Technical approaches feasible | MET | MET | Both implementable with standard tools |
| Terminology consistent | MET | MET | Both use consistent naming |
| No internal contradictions | MET | MET | Neither contradicts itself |
| Claims supported by evidence | MET | MET | Both cite specific file sizes, task counts |
| **Subtotal** | **5/5** | **5/5** | |

### Structure (5 criteria)
| Criterion | A | C | Evidence |
|-----------|---|---|----------|
| Logical ordering | MET | MET | Both follow extract-transform-output |
| Consistent hierarchy | MET | MET | Clean document structure |
| Clear separation of concerns | MET | MET | Task data vs metadata clearly separated |
| Navigation aids | NOT MET | MET | C has clearer section labels (META/INTEGRATION/TASKS) |
| Follows artifact conventions | MET | MET | Both follow compression strategy conventions |
| **Subtotal** | **4/5** | **5/5** | |

### Clarity (5 criteria)
| Criterion | A | C | Evidence |
|-----------|---|---|----------|
| Unambiguous language | MET | MET | Both use concrete terms |
| Concrete rather than abstract | MET | MET | Both provide specific examples |
| Clear purpose per section | MET | MET | Both well-organized |
| Terms defined | MET | MET | AC_TAGS, deps explained |
| Actionable next steps | MET | MET | Both can be directly implemented |
| **Subtotal** | **5/5** | **5/5** | |

### Risk Coverage (5 criteria)
| Criterion | A | C | Evidence |
|-----------|---|---|----------|
| Identifies 3+ risks | MET | MET | A: AC loss, LLM dependency, dual format. C: vocabulary, lower compression, domain specificity |
| Mitigation per risk | NOT MET | MET | A concedes AC loss without mitigation; C proposes controlled vocabulary |
| Failure modes addressed | NOT MET | MET | C addresses tag normalization failure; A doesn't address what happens if LLM can't reconstruct AC |
| External dependency scenarios | MET | MET | Both address deef's nature |
| Monitoring/validation mechanism | NOT MET | MET | C can validate tags against vocabulary; A has no validation |
| **Subtotal** | **2/5** | **5/5** | |

### Invariant & Edge Case Coverage (5 criteria)
| Criterion | A | C | Evidence |
|-----------|---|---|----------|
| Collection boundary conditions | NOT MET | MET | C handles empty AC (tag: `none`); A just drops it |
| State variable interactions | NOT MET | MET | C handles ID type mismatches (JTBD etc.) with source_id |
| Guard condition gaps | NOT MET | MET | C validates tag format; A has no validation |
| Count divergence | MET | MET | Both handle different row counts |
| Interaction effects | NOT MET | NOT MET | Neither fully addresses combined compression + diff interaction |
| **Subtotal** | **1/5** | **4/5** | |

### Qualitative Summary
| Dimension | Position A | Position C |
|-----------|-----------|------------|
| Completeness | 3/5 | 5/5 |
| Correctness | 5/5 | 5/5 |
| Structure | 4/5 | 5/5 |
| Clarity | 5/5 | 5/5 |
| Risk Coverage | 2/5 | 5/5 |
| Edge Cases | 1/5 | 4/5 |
| **Total** | **20/30** | **29/30** |

**Qualitative scores:** A = 0.667, B = (eliminated), C = 0.967

### Edge Case Floor Check
- Position A: 1/5 u2014 PASSES floor (threshold: 1/5)
- Position C: 4/5 u2014 PASSES

## Combined Scoring

| Position | Quant (50%) | Qual (50%) | Combined | Rank |
|----------|-------------|------------|----------|------|
| A | 0.456 (0.911u00d70.50) | 0.334 (0.667u00d70.50) | **0.789** | 2nd |
| B | 0.278 (0.555u00d70.50) | N/A (eliminated) | **eliminated** | 3rd |
| C | 0.454 (0.908u00d70.50) | 0.484 (0.967u00d70.50) | **0.938** | 1st |

**Margin: C leads A by 14.9 percentage points. No tiebreaker required.**

## Selected Base: Position C (Normalized Table Format)

**Selection rationale:** Position C wins decisively on the qualitative rubric (29/30 vs 20/30) while nearly matching Position A on quantitative metrics (0.908 vs 0.911). The 10% compression disadvantage (65-70% vs 75-80%) is more than compensated by:

1. **AC preservation via keyword tags** u2014 the single most important differentiator for LLM-based merge decisions
2. **Standard diff compatibility** u2014 TSV works with any line-based diff tool
3. **Risk mitigation completeness** u2014 C addresses its own vocabulary problem with a bounded solution

**Strengths to preserve from base (C):**
- TSV schema normalization with fixed columns
- AC keyword tag extraction with controlled vocabulary
- Metadata header for non-table content
- Integration points as structured rows

**Strengths to incorporate from Position A:**
- YAML/JSON machine-readable output format (instead of TSV) for programmatic consumption
- One-line prose summaries for narrative sections (supplement metadata header)
- Critical path notation as a single compressed line
- Explicit phase field per task (rather than phase as grouping)

**From Position B (constructive contribution):**
- Post-compression hash fingerprinting as an optional enhancement layer
