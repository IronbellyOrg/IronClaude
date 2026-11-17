# Base Selection (Step 3)

## Quantitative Scoring (50% weight)
Deterministic metrics from card text:

| Metric | Weight | V1 | V2 | V3 |
|--------|--------|----|----|----|
| Requirement coverage (INF rows touched/assigned) | 0.30 | 1.00 (3/3 observed) | 1.00 (2/2 observed) | 1.00 (1/1 observed) |
| Internal consistency (1 - contradictions/claims) | 0.25 | 1.00 (0 internal contradictions) | 1.00 | 1.00 (self-corrected F2 severity; not a contradiction) |
| Specificity ratio (concrete/citable claims) | 0.15 | 0.85 (5/5 findings with file:line) | 0.40 (coverage note, no defect claims) | 0.95 (4/4 findings with file:line incl. Makefile) |
| Dependency completeness (citations resolve) | 0.15 | 0.90 (10/11 citations valid; 1 flagged quote-mismatch) | 0.55 (6 citations, 4 flagged quote-mismatches) | 1.00 (6/6 citations valid, 0 flagged) |
| Section coverage (H2 sections / max) | 0.15 | 1.00 (4/4) | 0.50 (2/4) | 1.00 (4/4) |
| **quant_score** | | **0.96** | **0.76** | **0.99** |

Citation-flag data from panel/precheck.json (23 checked, 5 flagged): V1 1 flag (tasklist:61 quote), V2 4 flags (source:5, tasklist:37, :77, :79), V3 0 flags.

## Qualitative Scoring (50% weight) — 30-criterion binary rubric (CEV summarized)

| Dimension | V1 | V2 | V3 | Deciding evidence |
|-----------|----|----|----|-------------------|
| Completeness (5) | 4 | 3 | 5 | V3 covers distribution + preservation + fixture + self-location + immutability checks; V1 misses mirror mechanism; V2 covers only spec-vs-plan |
| Correctness (5) | 4 | 4 | 5 | V1's F4 circularity claim withdrawn in debate (correctness hit); V2 zero-defect stance partially conceded; V3 all claims survived debate |
| Structure (5) | 4 | 3 | 5 | V3's "What I checked" negative-evidence section; V2 lacks matrix |
| Clarity (5) | 4 | 4 | 5 | All cards cite lines; V3 names mechanisms (sync-dev, merge-by-command-identity) |
| Risk coverage (5) | 3 | 3 | 4 | V1 missed distribution risk; V2 missed staging ambiguity; V3 flagged both but missed constraint-AC gap |
| Invariant & edge case (5) | 2 | 1 | 3 | V3: interim window, foundation scoping, plugin mirror; V1: undefined outcomes; V2: none |
| **qual_score (x/30)** | **21/30 = 0.70** | **18/30 = 0.60** | **27/30 = 0.90** |

Edge-case floor (>=1/5): all three eligible (V1 2/5, V2 1/5, V3 3/5).

## Position-Bias Mitigation
Dual pass (input order V1,V2,V3 then reverse V3,V2,V1) applied over the CEV criteria. Passes agreed on 28/30 per-variant criterion verdicts; 2 disagreements (V1 risk-coverage in reverse pass scored 4 then re-evaluated to 3 on the "missed distribution risk" evidence; V3 completeness 4 vs 5 resolved to 5 on the fixture-check evidence). Final table uses agreed/re-evaluated verdicts.

## Combined Scoring

| Variant | quant | qual | combined |
|---------|-------|------|----------|
| V1 | 0.96 | 0.70 | **0.83** |
| V2 | 0.76 | 0.60 | **0.68** |
| V3 | 0.99 | 0.90 | **0.945** |

Tiebreaker: not needed (margin V3-V1 = 0.115 > 0.05).

## Selected Base: Variant 3 (refactorer lens, opus class)
Selection rationale: highest citation validity (0 flags), most complete affirmative verification ("What I checked"), all four findings survived adversarial pressure with calibrated severities, and the debate's corrected consensus (C-001 MEDIUM, U-001 LOW-MEDIUM) rests on V3's mechanism analysis.
Strengths to preserve: all four findings with their debate-corrected severities; the negative-evidence section.
Strengths to incorporate: V1's U-005 (constraint without AC) and U-004 (bash-only limit unsourced) and U-006 (undefined pass criteria, LOW) — the three points V1 won; V2's X-001 resolution (updatedInput "official" = outside contract, residual LOW) as the standing answer on that point.
