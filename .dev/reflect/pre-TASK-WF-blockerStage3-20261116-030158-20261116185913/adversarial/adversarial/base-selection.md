# Base Selection

## Quantitative Scoring (50% weight)

Computed by script (`uv run python`, text-mechanical, deterministic; run twice gives the same numbers). The metric proxies are crude for review cards: RC is keyword evidence for each of the 9 checks the reviewers were given, IC counts one hand-coded contradiction per card (Variant 1: table grade MEDIUM against text "Blocking: yes"; Variant 2: the F10 premise that the plan names lines 389 and 476), SR is concrete-versus-vague indicators, DC is resolved `F<n>` cross references, SC is H2 section count against the maximum.

| Metric | Weight | Variant 1 (haiku analyzer) | Variant 2 (opus qa) |
|--------|--------|----------------------------|---------------------|
| Requirement coverage (RC) | 0.30 | 1.000 | 1.000 |
| Internal consistency (IC) | 0.25 | 0.938 | 0.955 |
| Specificity ratio (SR) | 0.15 | 1.000 | 1.000 |
| Dependency completeness (DC) | 0.15 | 1.000 | 1.000 |
| Section coverage (SC) | 0.15 | 1.000 (7 H2) | 0.571 (4 H2) |
| **quant_score** | | **0.9844** | **0.9244** |

The quantitative gap comes only from section count (Variant 2 follows the brief's four-section answer format on purpose). RC saturates because both cards touch all 9 checks by keyword; it does not measure depth.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Two independent judges (opus class, a different class from both advocates; general-purpose, read-only) scored the 30 criteria in opposite orders.

| Dimension | V1 pass 1 | V1 pass 2 | V2 pass 1 | V2 pass 2 |
|-----------|-----------|-----------|-----------|-----------|
| Completeness (5) | 4 | 4 | 5 | 5 |
| Correctness (5) | 3 | 2 | 4 | 3 |
| Structure (5) | 5 | 4 | 5 | 5 |
| Clarity (5) | 4 | 3 | 4 | 4 |
| Risk Coverage (5) | 3 | 3 | 5 | 5 |
| Invariant & Edge Case (5) | 2 | 3 | 5 | 5 |
| **Total (30)** | 21 | 19 | 28 | 27 |

### Qualitative Summary (position-bias mitigation)

Disagreements between the two passes: Variant 1: C1, C4, K1, S5, L1, E5 (6); Variant 2: K3 (1). Each was re-evaluated by the orchestrator against the cards and the debate, the re-evaluation being final:
- V1 C1 (covers all explicit checks): NOT MET. It never checks the plan against the spec.
- V1 C4 (completion state for each earlier finding): MET. It states fixed or fixed in text for each of F1 to F3 and F4 to F16 with a citation.
- V1 K1 (no factual errors): MET. Its two findings and its correction of T1 observation O4 are true on the live files.
- V1 S5 (follows the format the brief asked for): NOT MET. The brief asked for four sections "only"; the card adds a deviation table, an adherence summary and a notes section.
- V1 L1 (unambiguous): NOT MET. The table grades both findings MEDIUM while the text says "Blocking: yes".
- V1 E5 (interaction effects): MET. It tests the digest insertion against the zero-count greps and checks stage 4 consumption, one-sidedly.
- V2 K3 (terminology): MET. Blocking and minor are used as defined; the reuse of F1 to F10 beside the earlier-finding labels is a reading hazard, not an inaccuracy.

Final qualitative totals: Variant 1 = 20 of 30 (0.667); Variant 2 = 28 of 30 (0.933). Disagreements found 7, verdicts changed 4.

### Edge Case Floor Check

Variant 1 scores 3 of 5 on Invariant & Edge Case Coverage in the re-evaluated total (E1, E2, E5 MET; E3, E4 NOT MET) and Variant 2 scores 5 of 5. Both clear the 1/5 floor.

## Position-Bias Mitigation

Dual pass as above; agreement on 53 of 60 criterion-variant verdicts (88 percent). Disagreements re-evaluated with both passes' evidence; no further appeal.

## Combined Scoring

| Variant | 0.50 x quant | 0.50 x qual | variant_score |
|---------|--------------|-------------|---------------|
| Variant 1 | 0.4922 | 0.3333 | **0.8255** |
| Variant 2 | 0.4622 | 0.4667 | **0.9289** |

Margin: 10.3 points (more than the 5 percent tiebreaker band); no tiebreaker applied.

## Selected Base: Variant 2 (reviewer-2, qa persona, opus class; `variant-2-original.md`)

Selection rationale: Variant 2 found both debate-confirmed new blocking defects that Variant 1 missed in whole or in part (the unequal-panel threshold artifact, C-003, and the Task 6 fix-pass route, C-007, which the invariant probe raised to blocking as INV-001), and it covers the cross-stage, test and spec checks the brief asked for. Variant 1's quantitative edge is a section-count artifact.

Strengths to preserve from the base: the earlier-findings table, the panel-size arithmetic, the vacuous-grep observation, the unedited label-floor lines, the stage 4 coupling and the "Checked and sound" list.

Strengths to incorporate from Variant 1: the R1b outcome-word hole (C-002, blocking, found by Variant 1 alone), the `verify` against `verify-citations` slip (C-004), and the cross-stage agreement list.

Corrections to apply to the base when merging: grade the fix-pass route (V2 F5) blocking (INV-001); grade V2 F2 and F3 non-blocking as the debate settled; drop the F7 matrix finding (it reviews the orchestrator's artifact, not the plan) and the F10 premise that lines 389 and 476 are named in Task 7's body (no such line number appears in the plan); label the earlier-finding references so they do not collide with the new numbering.
