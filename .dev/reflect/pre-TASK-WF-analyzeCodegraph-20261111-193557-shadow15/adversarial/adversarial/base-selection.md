# Base Selection — shadow15 reflect-pre findings merge

## Quantitative Scoring (50% weight)

Computed from the variant cards as artifacts. Source requirements = the 7 spec R-IDs + 6 §2.4 interface rules the audit could cite (13 referenceable items); internal references = the cards' refs/citation links.

| Metric | Weight | V1 (analyzer/sonnet) | V2 (qa/haiku) | V3 (refactorer/opus) |
|--------|--------|----------------------|----------------|----------------------|
| Requirement coverage (RC) | 0.30 | 0.62 (8/13: R1,R2,R3,R4,R5,R7 partly, §2.2, §2.4-1) | 0.77 (10/13: R2,R3,R5,R7, §2.4-3, §2.4-6, §2.5, §4 cap, §2.2) | 0.46 (6/13: guide-rule stratum — R4/R7 indirectly via INF refs) |
| Internal consistency (IC) | 0.25 | 0.67 (1 of 3 claims contradicted by evidence: F2) | 0.75 (1 of 4 partially: F1 matrix clause + F2 return-contract clause = 1 full contradiction equivalent) | 0.33 (2 of 3 refuted: F2; F3 halved by post-#513 text) |
| Specificity ratio (SR) | 0.15 | 0.85 | 0.80 | 0.75 |
| Dependency completeness (DC) | 0.15 | 0.95 (all citations resolve) | 0.95 | 0.85 (INF-ID refs require t1-card indirection; both resolve) |
| Section coverage (SC) | 0.15 | 0.75 | 1.00 (max findings block + calibration) | 0.75 |

Formula: `quant_score = (RC×0.30) + (IC×0.25) + (SR×0.15) + (DC×0.15) + (SC×0.15)`

- V1: 0.62×0.30 + 0.67×0.25 + 0.85×0.15 + 0.95×0.15 + 0.75×0.15 = 0.186 + 0.1675 + 0.1275 + 0.1425 + 0.1125 = **0.736**
- V2: 0.77×0.30 + 0.75×0.25 + 0.80×0.15 + 0.95×0.15 + 1.00×0.15 = 0.231 + 0.1875 + 0.12 + 0.1425 + 0.15 = **0.831**
- V3: 0.46×0.30 + 0.33×0.25 + 0.75×0.15 + 0.85×0.15 + 0.75×0.15 = 0.138 + 0.0825 + 0.1125 + 0.1275 + 0.1125 = **0.573**

## Qualitative Scoring (50% weight) — Additive Binary Rubric (30 criteria, CEV)

Compact CEV: one line per dimension per variant (met-count with the decisive evidence). Dual-pass position-bias mitigation ran as order-swap re-check; zero verdict disagreements, so no re-evaluation entries.

### Completeness (5)
- V1 3/5 — MET: edge/failure scenarios via AC-gap family; dependencies/prereqs clear; scope implicit. NOT MET: success criteria (no falsifiability angle), explicit out-of-scope statement.
- V2 4/5 — MET: failure scenarios (escape clauses), success criteria (what would make each AC fail), dependencies, coverage breadth incl. §2.5/§4. NOT MET: explicit out-of-scope.
- V3 2/5 — MET: dependency (guide↔command coupling), scope (shipped-artifact stratum). NOT MET: requirements coverage, edge/failure scenarios, success criteria.

### Correctness (5)
- V1 3/5 — F1/F3 verified true; F2 false (misattribution). MET: 1,3,4,5 minus one for the factual error → 3/5 with criteria 1 and 5 split.
- V2 4/5 — F3/F4 true and verified; F1 matrix clause false; F2 return-contract clause overstated. Terminology consistent; claims evidence-backed.
- V3 1/5 — F1 true and verified; F2 false (misattribution); F3 half-true (post-#513 text inflates the density claim). Only criterion 4 (no internal contradiction) survives cleanly.

### Structure (5)
- V1 5/5 — findings-v2 schema clean, refs anchored, citations well-formed.
- V2 5/5 — same, plus the fullest calibration block.
- V3 4/5 — INF-ID indirection slightly weakens navigation (S-004).

### Clarity (5)
- V1 4/5 — concrete and unambiguous; F2's "mild unplanned elaboration" hid the temporal assumption.
- V2 4/5 — concrete; F2's four-clause bundle hurt single-claim verifiability.
- V3 4/5 — concrete; F3's "about six rules" is uncounted.

### Risk Coverage (5)
- V1 2/5 — identifies drift risk (ungated clauses); no mitigation, no monitoring.
- V2 3/5 — identifies process risk (unpassable checks) with what-would-fail reasoning; no mitigation strategies.
- V3 2/5 — identifies guide-drift channel; no probability/impact framing.

### Invariant & Edge Case Coverage (5)
- V1 2/5 — boundary conditions of the constraint/AC relationship; no state/interaction analysis.
- V2 4/5 — escape-clause boundary cases (the AC analog of empty-collection handling); count/coverage edges; the only falsifiability-boundary audit.
- V3 1/5 — the density/line-count boundary only.

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|-----------|----|----|----|
| Completeness | 3 | 4 | 2 |
| Correctness | 3 | 4 | 1 |
| Structure | 5 | 5 | 4 |
| Clarity | 4 | 4 | 4 |
| Risk Coverage | 2 | 3 | 2 |
| Invariant & Edge Case | 2 | 4 | 1 |
| **Total** | **19/30 = 0.633** | **24/30 = 0.800** | **14/30 = 0.467** |

### Edge Case Floor Check
- V1 2/5 — eligible. V2 4/5 — eligible. V3 1/5 — eligible (floor is <1/5; V3 exactly meets it).

## Combined Scoring

`variant_score = (0.50 × quant) + (0.50 × qual)`

| Variant | Quant | Qual | Combined |
|---------|-------|------|----------|
| V2 (qa/haiku) | 0.831 | 0.800 | **0.816** |
| V1 (analyzer/sonnet) | 0.736 | 0.633 | **0.685** |
| V3 (refactorer/opus) | 0.573 | 0.467 | **0.520** |

Margin V2→V1: 0.131 (13.1 points) — exceeds the 5% tiebreaker band; no tiebreaker applied.

## Selected Base: Variant 2 (qa / haiku / claude-haiku-5-5)

Selection rationale: V2 wins both layers outright — highest requirement coverage (the only card reaching the falsifiability stratum AND §2.5/§4 residues), highest correctness after adjudication (2 of its 4 claims survive whole, 1 survives re-scoped, only 1 clause fell to evidence), and the strongest invariant/edge-case dimension, which is what this debate's L3 diff points were made of. Notably, the lowest-model-class card out-scored both larger models on correctness — its two refuted clauses were vantage/overreach errors, while V1 and V3 each lost a whole finding to the HEAD=execution-output assumption (A-001) that V2's plan-text-only citation habit partly avoided.

Strengths to preserve from V2 (base): F3/F4 falsifiability pair verbatim (highest-confidence findings of the debate); the unpassable-check category; per-finding calibration block.

Strengths to incorporate from non-base variants:
- V1-F1 (R7 symbolsOnly ban ungated) — merge as the lead instance of the constraint-without-AC family (C-001 winner; V1 stated it first and tightest).
- V1-F3 (R2 access:mcp gate ungated) — merge as third family instance (C-005 winner).
- V2-F2 residue (25-line cap ungated) and re-scoped V2-F1 (§2.4 items 3/6 AC-level gap) fold into the same family as sub-clauses.
- V3-F1 (guide verb-list duplication) — keep as the sole shipped-artifact finding, with its guide citation (C-006 winner).
- V3-F3 at reduced scope (Leads-bullet density attributable to 7764bb623 text only) — MINOR, lowest confidence.
- Provenance discipline from V3: cite the execution commit hash alongside HEAD line numbers where the two differ.
