# Base Selection

Inputs: `variant-1-opus-architect.md` (V1, 537 lines), `variant-2-sonnet-analyzer.md` (V2, 691 lines), `variant-3-haiku-backend.md` (V3, 637 lines). Scoring passes: `debate/score-pass1-forward.md` (V1, V2, V3 order; quantitative and qualitative) and `debate/score-pass2-reverse.md` (V3, V2, V1 order; qualitative only). Evidence for every verdict is in those two files.

## Quantitative Scoring (50% weight)

Deterministic metrics from pass 1 (numerator over denominator; the sampling method for IC and SR is stated in `debate/score-pass1-forward.md`: 30 falsifiable claims and 40 substantive statements per variant).

| Metric | Weight | V1 | V2 | V3 |
|---|---|---|---|---|
| RC requirement coverage (19 source requirements) | 0.30 | 18/19 = 0.947 | 18/19 = 0.947 | 18/19 = 0.947 |
| IC internal consistency | 0.25 | 28/30 = 0.933 | 28/30 = 0.933 | 30/30 = 1.000 |
| SR specificity ratio | 0.15 | 35/37 = 0.946 | 38/38 = 1.000 | 25/35 = 0.714 |
| DC dependency completeness | 0.15 | 89/89 = 1.000 | 135/136 = 0.993 | 4/4 = 1.000 |
| SC section coverage (H2 sections) | 0.15 | 16/18 = 0.889 | 18/18 = 1.000 | 14/18 = 0.778 |
| **quant_score** | | **0.943** | **0.966** | **0.908** |

Caveat recorded: V3's DC of 4 of 4 rests on only four internal cross-references (it uses almost none), so its perfect DC is weak evidence.

## Qualitative Scoring (50% weight): additive binary rubric

Final verdict per criterion = the agreed verdict of the two passes, or, where they disagreed, the re-evaluated verdict (see Position-Bias Mitigation). Cells show pass 1 / pass 2 / final.

### Completeness (5 criteria)

| Criterion | V1 (P1/P2/final) | V2 (P1/P2/final) | V3 (P1/P2/final) |
|---|---|---|---|
| completeness.1 | NOT MET / MET / **MET** | NOT MET / NOT MET / **NOT MET** | NOT MET / NOT MET / **NOT MET** |
| completeness.2 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |
| completeness.3 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |
| completeness.4 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |
| completeness.5 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |

### Correctness (5 criteria)

| Criterion | V1 (P1/P2/final) | V2 (P1/P2/final) | V3 (P1/P2/final) |
|---|---|---|---|
| correctness.1 | NOT MET / NOT MET / **NOT MET** | NOT MET / NOT MET / **NOT MET** | MET / MET / **MET** |
| correctness.2 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |
| correctness.3 | MET / MET / **MET** | NOT MET / MET / **NOT MET** | MET / MET / **MET** |
| correctness.4 | NOT MET / MET / **NOT MET** | NOT MET / MET / **NOT MET** | MET / MET / **MET** |
| correctness.5 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |

### Structure (5 criteria)

| Criterion | V1 (P1/P2/final) | V2 (P1/P2/final) | V3 (P1/P2/final) |
|---|---|---|---|
| structure.1 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |
| structure.2 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |
| structure.3 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |
| structure.4 | MET / MET / **MET** | MET / MET / **MET** | NOT MET / NOT MET / **NOT MET** |
| structure.5 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |

### Clarity (5 criteria)

| Criterion | V1 (P1/P2/final) | V2 (P1/P2/final) | V3 (P1/P2/final) |
|---|---|---|---|
| clarity.1 | MET / MET / **MET** | MET / MET / **MET** | NOT MET / MET / **NOT MET** |
| clarity.2 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |
| clarity.3 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |
| clarity.4 | NOT MET / NOT MET / **NOT MET** | NOT MET / MET / **NOT MET** | NOT MET / NOT MET / **NOT MET** |
| clarity.5 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |

### Risk Coverage (5 criteria)

| Criterion | V1 (P1/P2/final) | V2 (P1/P2/final) | V3 (P1/P2/final) |
|---|---|---|---|
| risk.1 | MET / MET / **MET** | NOT MET / NOT MET / **NOT MET** | NOT MET / NOT MET / **NOT MET** |
| risk.2 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |
| risk.3 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |
| risk.4 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |
| risk.5 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |

### Invariant and Edge Case Coverage (5 criteria)

| Criterion | V1 (P1/P2/final) | V2 (P1/P2/final) | V3 (P1/P2/final) |
|---|---|---|---|
| invariant.1 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |
| invariant.2 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |
| invariant.3 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |
| invariant.4 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |
| invariant.5 | MET / MET / **MET** | MET / MET / **MET** | MET / MET / **MET** |

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 5/5 | 4/5 | 4/5 |
| Correctness | 3/5 | 2/5 | 5/5 |
| Structure | 5/5 | 5/5 | 4/5 |
| Clarity | 4/5 | 4/5 | 3/5 |
| Risk Coverage | 5/5 | 4/5 | 4/5 |
| Invariant and Edge Case Coverage | 5/5 | 5/5 | 5/5 |
| **Total** | **27/30** | **24/30** | **25/30** |

### Edge Case Floor Check

All three variants score 5 of 5 on Invariant and Edge Case Coverage in both passes, so none is ineligible as base (floor: at least 1 of 5).

## Position-Bias Mitigation

Dual pass: pass 1 evaluated V1, V2, V3; pass 2 (independent, forbidden to read pass 1) evaluated V3, V2, V1. Pass totals before reconciliation: pass 1 V1 26, V2 24, V3 25; pass 2 V1 28, V2 27, V3 26 (pass 2 is more lenient on every variant, a consistent offset rather than an order effect in favour of one variant).

Verdict pairs compared: 90. Agreement: 84. Disagreements found: 6 (6.7 percent). Verdicts changed by re-evaluation: 6 (each disagreement resolves to one side, so one pass's verdict is changed).

Re-evaluation was done by the orchestrator comparing both passes' written evidence, not by a fresh agent (stated so that the reader can weigh it). Rule used: prefer the verdict whose evidence names a concrete, checkable text; a keyword Grep that only shows absence of hedge words does not outweigh a named ambiguous phrase; apply the same standard to every variant.

| Criterion | Variant | Pass 1 | Pass 2 | Final | Reason |
|---|---|---|---|---|---|
| completeness.1 | V1 | NOT MET | MET | MET | Pass 1 penalised V1 for the false "81 files" count and for line numbers labelled "not re-read". Both are correctness problems already counted under correctness.1 (NOT MET); every required section and open question is answered in V1 (5.5, 9.1, D1, D2, D8). |
| correctness.3 | V2 | NOT MET | MET | NOT MET | Pass 1 names a concrete clash: "R2" defined as the run-2 folder in section 0 and reused as a risk id in section 14, and "D" used for a classifier question and for decision ids. |
| correctness.4 | V1 | NOT MET | MET | NOT MET | Pass 1 names two clashes (section 3 NOTE example versus the table-shape rule; risk R4 versus the section 5.2 endorsement of the sketch's wrong() step); the diff analysis found the same class of defect (V1 endorses a monotonicity claim the sketch fails across UNSET). |
| correctness.4 | V2 | NOT MET | MET | NOT MET | Pass 1 names "consumer-unknown is a non-blocking Medium" (4.2) against "UNSET means send to a person" (7.3), and "nine paths below" against 8 rows; V2's own advocate conceded the first. |
| clarity.1 | V3 | NOT MET | MET | NOT MET | Pass 2 used a keyword Grep that cannot see "called Medium where useful"; that phrase leaves when it applies undefined, the same kind of vagueness as "as appropriate". |
| clarity.4 | V2 | NOT MET | MET | NOT MET | Pass 1 names "MDTM templates" and "WC-2", "WC-4" used without definition; the same standard already marks V1 NOT MET for undefined "DNSP" and "MDTM" in both passes. |

## Combined Scoring

| Variant | quant (x0.50) | qual (x0.50) | Final score |
|---|---|---|---|
| V1 (opus architect) | 0.943 -> 0.471 | 27/30 = 0.900 -> 0.450 | **0.921** |
| V2 (sonnet analyzer) | 0.966 -> 0.483 | 24/30 = 0.800 -> 0.400 | **0.883** |
| V3 (haiku backend) | 0.908 -> 0.454 | 25/30 = 0.833 -> 0.417 | **0.871** |

Ranking by score: V1, V2, V3. Margin V1 over V2: 0.038 (3.8 percent), under the 5 percent threshold, so the tiebreaker protocol applies. V1 over V3: 0.050, not within the tiebreak band.

### Tiebreaker (top two within 5 percent: V1 and V2)

- Level 1, debate performance: points won in the Round 2 scoring matrix (47 non-assumption points; the 14 shared-assumption points record ACCEPT, REJECT or QUALIFY, not a variant): V1 9, V2 19, V3 19. V2 won 19 against V1's 9, a gap well over 5 percent, so level 1 decides for V2. Levels 2 and 3 are not needed.
- Result: Tiebreaker applied: yes (level 1). The numeric leader (V1) loses the base position to V2 on debate performance; this is stated openly because the margin is 3.8 percent and the final spec takes V1's and V3's winning points through the refactoring plan anyway.

## Selected Base: Variant 2 (sonnet:analyzer)

Selection rationale: highest quantitative score (0.966), full section coverage (18 of 18), the only variant that explains why the rule over-blocks with evidence (six causes; the wording is one), and the winner of the most diff points together with V3. It has known defects that the merge must fix: an "UNSET means send to a person" claim that is false for the safety and decision questions, "R2" used for two meanings, a test-module count of 8 (the union is at least 10), the claim that "highest severity wins" sits in task-builder and tech-research (it sits in tech-reference, task, and more lines), and undefined terms (MDTM, WC-n).

Strengths to preserve from V2: the six-cause root-cause analysis; the named-consumer counterfactual test with 8 or more worked examples; the measured guardrails (blind audit with a no-rule auditor, seeded-defect recall test, Wilson-interval revert triggers); the evidence discipline (live checks list); the six-question classifier with the classifier as a measurement and consistency tool.

Strengths to incorporate from non-base variants (full list in `refactor-plan.md`):

- From V1: the delegate-only skill folder as the home of the shared rule (the only location that gets installed copy, project `.claude/` copy and drift check); the registry of carriers and the registry-driven drift test; the versioned inline digest plus pointer; the extension contracts (new gate, judge, scale or deliverable kind is one row); the explicit inventory of other severity scales and how each maps; staged rollout by named file sets.
- From V3: the follow-up ledger as a data contract (stable finding identity, repeat-safe imports, explicit states, atomic writes), the one-issue batch filing bound to the user's approved selection with crash reconciliation, fork-only targeting, the fail-safe rule that a missing decisive answer never authorises a downgrade, bounded fallback judge chain and privacy controls.
- From the invariant probe: the 9 HIGH items (INV-001, 007, 008, 009, 015, 023, 026, 027, 034) become explicit requirements or owner decisions.
