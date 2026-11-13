# Base Selection

## Quantitative Scoring (50% weight)
Source requirements = the nine content diff points C-001..C-009 (the only shared yardstick for three audit cards); computed by the orchestrator, deterministic.

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 |
|---|---|---|---|---|
| Requirement coverage (RC): points reported / 9 | 0.30 | 5/9 = 0.556 | 2/9 = 0.222 | 4/9 = 0.444 |
| Internal consistency (IC): 1 - claims overturned in debate / claims | 0.25 | 1 - 2/7 = 0.714 | 1.000 | 1 - 2/8 = 0.750 |
| Specificity ratio (SR) | 0.15 | 0.95 | 0.90 | 0.95 |
| Dependency completeness (DC): resolved refs | 0.15 | 0.90 | 0.90 | 0.95 |
| Section coverage (SC): H2 headings / max | 0.15 | 1.00 | 1.00 | 1.00 |
| quant_score | | 0.7735 | 0.7370 | 0.7555 |

Overturned claims: V1 "dependencies consistent" and "no missed defects" (conceded, Round 2); V3 "must invent" and MAJOR severity of the cycle-id gap (conceded, Round 2).

## Qualitative Scoring (50% weight): 30-criterion rubric, dual pass
Pass 1 (order 1, 2, 3) and pass 2 (order 3, 2, 1) were run by two independent scorer agents (sonnet class); both scored from the cards only, without opening the spec or plan, so Correctness 2 and 5 rest on each card's own citations (limitation recorded).

| Variant | Pass 1 total | Pass 2 total | Mean | qual_score (mean / 30) |
|---|---|---|---|---|
| 1 | 22 | 22 | 22.0 | 0.7333 |
| 2 | 18 | 17 | 17.5 | 0.5833 |
| 3 | 22 | 22 | 22.0 | 0.7333 |

Per-dimension disagreements between the passes (kept, not re-adjudicated criterion by criterion): V1 Correctness 4/5, Invariant 3/2; V2 Completeness 2/3, Correctness 5/4, Invariant 2/1; V3 Risk 2/3, Invariant 3/2. Totals agree within 1 point, so the mean is used.
Edge Case Floor Check: every variant scored at least 1/5 on Invariant & Edge Case Coverage in both passes; all eligible as base.

## Position-Bias Mitigation
Dual pass done (above). Disagreements found: 7 dimension-level pairs; no total changed by more than 1.

## Combined Scoring
| Variant | 0.5 x quant | 0.5 x qual | variant_score |
|---|---|---|---|
| 1 | 0.3868 | 0.3667 | 0.7534 |
| 2 | 0.3685 | 0.2917 | 0.6602 |
| 3 | 0.3778 | 0.3667 | 0.7444 |

Margin V1 over V3: 0.009 (< 0.05), so the tiebreaker applies.
- Level 1, diff points won in Round 1 and 2: V1 5 (C-001, C-003, C-004, C-005, C-006), V3 5 (C-002, C-008, C-009, X-001, X-002), V2 1 (C-007). Tie.
- Level 2, correctness criteria MET (mean of both passes): V3 5.0, V1 4.5. V3 wins.

## Selected Base: Variant 3 (refactorer card, opus class)
Tiebreaker level 2 applied (margin 0.9%). 
- Strengths to preserve: the section 10 authoring-rule checks (C-008, C-009) and the cycle-id equality finding with its dependency on held_cycle_published (C-002).
- Strengths to incorporate: V1's more precise C-001 (GuardAction has no re-enter member; plan 73 requires action/reason/cause assertions; rebuttal of the "SKILL re-enters" reading) and V1's C-003, C-004, C-005, C-006; V2's C-007 (writer-side event contract); the fault-finder's INV-001, INV-003, INV-004, INV-005, INV-006 and the engage-row ordering quirk.
