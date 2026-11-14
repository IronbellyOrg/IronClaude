# Base Selection Report: Q16

Performed by: the orchestrating session (group 4 worker), inline, as the debate-orchestrator role. Variant 1 = proposal-A (promise nothing yet), Variant 2 = proposal-B (one trust design), Variant 3 = proposal-C (one vocabulary and one audit record).

## Quantitative Scoring (50% weight)

Source "requirements" for requirement coverage = the 8 work items Q16 gates (XC-08, OB-08 decision 6, V2-01, CO-03, SW-12, V2-03, V2-04, OB-09; question.md "What it gates").

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 0.88 (7 of 8; no CO-03) | 0.38 (3 of 8: OB-08, V2-01, SW-12) | 0.75 (6 of 8; no V2-03, CO-03) |
| internal_consistency | 0.25 | 0.92 ("promise nothing" yet keeps a one-design sentence: 1 contradiction in about 12 claims) | 1.00 | 1.00 |
| specificity_ratio | 0.15 | 0.85 | 0.80 | 0.85 |
| dependency_completeness | 0.15 | 0.90 (re-ask trigger depends on SW-12, which is blocked by XC-08) | 1.00 | 1.00 |
| section_coverage | 0.15 | 1.00 (5 of 5) | 1.00 | 1.00 |
| **quant_score** | | **0.907** | **0.784** | **0.903** |

## Qualitative Scoring (50% weight): Additive Binary Rubric (CEV, condensed)

| Dimension / criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|
| Completeness 1: covers the gated items | MET | NOT MET | MET | V2 omits XC-08, V2-03, V2-04, OB-09, CO-03; V3 covers them through XC-08 |
| Completeness 2: edge cases and failures | MET | MET | MET | V1 "returns at a worse time"; V2 "fits one consumer badly"; V3 "drift apart beneath shared words" |
| Completeness 3: dependencies | MET | MET | MET | All name SW-12 Phase 4 |
| Completeness 4: completion criteria | MET | MET | MET | All state the ledger record and the issue text outcome |
| Completeness 5: out of scope stated | NOT MET | NOT MET | MET | V3: "It does not authorize relay" |
| Correctness 1: no factual errors | MET | MET | MET | V1 and V3 had one off-row line citation each (corrected after Round 1); facts were right |
| Correctness 2: feasible under stated constraints | NOT MET | NOT MET | MET | V1 re-ask trigger is circular (merged-requirements lines 201, 830); V2 is out of scope per line 146 |
| Correctness 3: consistent terminology | MET | MET | MET | Note: "grant" also names ledger rows GRANT(item, action) (advocate 3) |
| Correctness 4: no internal contradiction | NOT MET | MET | MET | V1 keeps "Decide one design, not two." while "promising nothing" |
| Correctness 5: claims supported | MET | MET | MET | All cite merged-requirements, ADJ, diff-analysis |
| Structure 1 to 5 | 5 MET | 5 MET | 5 MET | Identical five-section layout, ordered, cross-referenced |
| Clarity 1: unambiguous | MET | MET | MET | |
| Clarity 2: concrete | MET | MET | MET | |
| Clarity 3: clear purpose per section | MET | MET | MET | |
| Clarity 4: ids glossed on first use | NOT MET | NOT MET | NOT MET | XC-01 or XC-08 used without gloss in each |
| Clarity 5: next steps clear | MET | MET | MET | |
| Risk 1: three or more risks with probability and impact | NOT MET | NOT MET | NOT MET | No per-risk probability |
| Risk 2: mitigation per risk | NOT MET | NOT MET | NOT MET | V3's drift risk has no guard |
| Risk 3: failure and recovery | MET | MET | NOT MET | V1 "extra round of issue edits"; V2 "three issue texts must change"; V3 none |
| Risk 4: external dependencies | MET | MET | MET | SW-12 Phase 4 deferred and unbuilt |
| Risk 5: monitoring or validation | NOT MET | NOT MET | MET | V3: OB-09 audits every answer path in the vocabulary |
| Invariant 1: consumer-set boundaries (empty, one, more) | NOT MET | NOT MET | NOT MET | None covers the watcher (A-001) |
| Invariant 2: state across component boundaries | MET | MET | MET | V1 #409 vs #423 readers; V2 threat models; V3 per-consumer mechanism |
| Invariant 3: guard gaps | NOT MET | NOT MET | MET | V3 relay limit (line 574) |
| Invariant 4: count divergence | NOT MET | NOT MET | NOT MET | Not applicable to a policy answer |
| Invariant 5: interaction effects | NOT MET | MET | MET | V2 translation layer for relay; V3 equal words hiding unequal protection |

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 4/5 | 3/5 | 5/5 |
| Correctness | 3/5 | 4/5 | 5/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 | 4/5 |
| Risk Coverage | 2/5 | 2/5 | 2/5 |
| Invariant and Edge Case | 1/5 | 2/5 | 3/5 |
| **qual_score** | **19/30 = 0.633** | **20/30 = 0.667** | **24/30 = 0.800** |

### Edge Case Floor Check
All three score at least 1/5; all eligible.

## Position-Bias Mitigation

Single evaluator, two passes (order 1, 2, 3 then 3, 2, 1). The passes disagreed on Correctness 1 for V1 and V3 (an off-row line citation). Re-evaluated: a wrong line number with a correct fact is a citation slip, not a factual error; final MET for both.
Disagreements re-evaluated: 2. Final verdicts changed: 0 relative to pass 1.

## Combined Scoring

| Variant | Quant x 0.50 | Qual x 0.50 | Final Score |
|---|---|---|---|
| V1 (proposal-A) | 0.453 | 0.317 | 0.770 |
| V2 (proposal-B) | 0.392 | 0.333 | 0.725 |
| V3 (proposal-C) | 0.451 | 0.400 | **0.851** |

Margin: 8.1 points over V1 (above the 5 point threshold). Tiebreaker applied: no. Debate points won: V3 11 of 14, V1 2, V2 1.

## Selected Base: Variant 3 (proposal-C, one vocabulary and one audit record)

### Selection Rationale
Highest combined score and unanimous Round 1 verdict (3 of 3 advocates, 65 to 70 percent). It is the only option the spec places in reach (merged-requirements line 146), the only branch XC-08 writes out in full (line 456), and it routes poisoned content to an existing control (V2-04, line 401).

### Strengths to Preserve from Base
1. Separate mechanisms per threat model, shared words and audit shape only.
2. The decision 6 rewrite and the "promise the vocabulary, not a design" clause for #423 and Coder#477.
3. The stated limit: the vocabulary does not authorize relay.

### Strengths to Incorporate from Non-Base Variants
1. From V1 (U-001): a re-ask checkpoint; the owner re-confirms the narrow promise when SW-12 Phase 4 opens.
2. From V2 (U-002): a single owner for the vocabulary and audit format, and a written bar on a second vocabulary.
3. From advocates 2 and 3: when the vocabulary is defined, each term states what it actually enforces in each program, so equal words do not hide unequal protection; audit records are untrusted input to every reader.
