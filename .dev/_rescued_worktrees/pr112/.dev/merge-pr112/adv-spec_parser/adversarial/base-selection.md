# Base Selection

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (hybrid) | V2 (ours) | V3 (theirs) |
|--------|--------|-------------|-----------|-------------|
| Requirement coverage (MD-family feature implemented) | 0.30 | 1.00 | 1.00 | 1.00 |
| Internal consistency (no contradictory paths) | 0.25 | 1.00 | 1.00 | 1.00 |
| Specificity (concrete, deterministic logic) | 0.15 | 1.00 | 1.00 | 1.00 |
| Dependency completeness (no dangling refs) | 0.15 | 1.00 | 1.00 | 1.00 |
| Section coverage | 0.15 | 1.00 | 1.00 | 1.00 |
| **quant_score** | | **1.00** | **1.00** | **1.00** |

(All three implement the feature; quant layer does not separate them — the separation is qualitative.)

## Qualitative Scoring (50% weight)

### Correctness (decisive dimension)
| Criterion | V1 | V2 | V3 | Evidence |
|-----------|----|----|----|----------|
| Span-aware dedup preserves legitimate standalone D | MET | **NOT MET** | MET | V2 value-global dedup drops standalone `D01` (fails master test); V1/V3 empirically PASS |
| No internal contradictions | MET | MET | MET | — |
| Passes incoming master test suite (`test_md_family_does_not_collapse_bare_d`) | MET | **NOT MET** | MET | Empirical run: V1 PASS both MD tests |

### Structure / SoT compliance (Contract #8)
| Criterion | V1 | V2 | V3 | Evidence |
|-----------|----|----|----|----------|
| Zero duplicate regex literals vs contracts SoT | MET | NOT MET (1: `_MD_TRAILING_D_RE`) | **NOT MET (6 hardcoded)** | V3 duplicates all 6 family bodies → silent-drift risk |
| Pattern table tracks `ID_PATTERNS` changes automatically | MET | MET | NOT MET | V3 hardcoded table will not follow SoT edits |

### Invariant & Edge Case Coverage
| Criterion | V1 | V2 | V3 | Evidence |
|-----------|----|----|----|----------|
| Empty text → `{}` | MET | MET | MET | md_spans=[], findall=[] |
| MD-only (no standalone D) → no phantom D key | MET | MET | MET | `if ids` drops empty D; verified `{'MD': ['M1-D01']}` |
| Pure-spec D (no MD) → unchanged base behavior | MET | MET | MET | md_spans empty → `else` findall path |
| Edge-case floor (≥1/5) | PASS | PASS | PASS | — |

## Position-Bias Mitigation
Forward (V1,V2,V3) and reverse (V3,V2,V1) evaluation agree: V1 wins on the Correctness + Contract #8
criteria in both passes. No disagreements requiring re-evaluation.

## Combined Scoring

| Variant | quant (0.50) | qual (0.50) | Combined | Rank |
|---------|--------------|-------------|----------|------|
| V1 (hybrid)  | 0.500 | best (correct + 0 dup literals) | **highest** | 1 |
| V3 (theirs)  | 0.500 | correct dedup BUT 6 dup literals | 2nd | 2 |
| V2 (ours)    | 0.500 | WRONG dedup (fails master test) | 3rd | 3 |

Margin V1 vs V3 > 5% (V3 carries a full SoT regression on 6 literals + would itself need re-merging to
adopt the contracts table). No tiebreaker needed.

## Selected Base: Variant 1 (proposed_hybrid)

**Selection rationale:** V1 is the only variant that is simultaneously (a) correct on the bare-D dedup
(passes the incoming master test that V2 fails), and (b) fully Contract #8-compliant (zero duplicate
regex literals, vs V2's one and V3's six). It is a genuine hybrid — ours' SoT-sourced table + theirs'
span-aware dedup — not a concatenation; it removes ours' now-redundant `_MD_TRAILING_D_RE`.

**Strengths to preserve:** contracts-sourced pattern dict; explicit `_REQUIREMENT_PATTERNS["MD"]` lookup;
span-aware containment dedup.

**Strengths to incorporate:** none beyond V1 (V1 already unions the best of V2 and V3).
