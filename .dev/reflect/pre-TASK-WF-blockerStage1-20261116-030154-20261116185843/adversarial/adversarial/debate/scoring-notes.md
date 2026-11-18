# Scoring notes (inputs to base-selection.md)

## Quantitative layer (script output `debate/quant-scores.json`; computed by the orchestrator, deterministic)

RC = share of the 26 review duties the card touches (F1-F9, M-F1-M-F10, and seven brief checks: numbering, dependencies, later-task falsification, missing paths, brief decisions, stage 2 contradiction, exit tests) by keyword presence. IC = 1 - contradictions/claims (manual: V1 0 of 25; V2 1 of 18, "blocking: yes" against its own MEDIUM row; V3 1 of 19, a finding it says "fails" PLAN:238 is graded non-blocking). SR = concrete indicators (line refs, backticked names, numbers) over concrete plus vague words; it saturates at 1.0 for all three, so it does not separate them. DC = internal references that resolve inside the card (V3 cites T1-F1, T1-F4, T1-F5 that are not defined in the card). SC = H2 section count over the maximum (V2 has 7).

| Variant | RC (0.30) | IC (0.25) | SR (0.15) | DC (0.15) | SC (0.15) | quant |
|---|---|---|---|---|---|---|
| 1 | 0.962 | 1.000 | 1.000 | 1.000 | 0.857 | 0.9671 |
| 2 | 0.885 | 0.944 | 1.000 | 1.000 | 1.000 | 0.9515 |
| 3 | 0.962 | 0.947 | 1.000 | 0.667 | 0.571 | 0.8610 |

## Qualitative layer, two blind scorer passes (sonnet class; pass 1 forward order, pass 2 reverse order)

| Variant | Pass 1 | Pass 2 | Disagreeing criteria (pass 1 / pass 2) |
|---|---|---|---|
| 1 | 26 | 25 | C1 (0/1), K1 (1/0), K3 (1/0) |
| 2 | 22 | 22 | R3 (0/1), E4 (1/0) |
| 3 | 28 | 28 | L4 (0/1), E1 (1/0) |

Re-evaluation of each disagreement (orchestrator, with both passes' evidence; the final verdict is final):
- V1 C1: NOT MET (0). The card never checks the brief's decisions or the later-task-falsification duty by name; it checks earlier findings, numbering, dependencies, paths, the stage 2 plan and the spec rows.
- V1 K1: MET (1). Of four line cites the second scorer called stale, PLAN:149, PLAN:190 and PLAN:232 are the `Depends on` lines of Tasks 9, 12 and 15 (correct); PLAN:122 is the Task 7 `Depends on` line where the F4 text sits at PLAN:124, a moved line on a true claim.
- V1 K3: MET (1). Ids are used consistently inside the card (all `R3-Fk`); the orchestrator note records the slip.
- V2 R3: MET (1). The card names the failure mode (a contract-valid row resolves to UNSET) and the repair fixture.
- V2 E4: MET (1). It checks counts (16 tasks, eleven exit tests mapped).
- V3 L4: NOT MET (0). T1-F1, T1-F4 and T1-F5 are cited but never defined in the card.
- V3 E1: MET (1). It covers the "origin that matches no key" case.

Final qualitative totals: V1 26/30 = 0.8667; V2 23/30 = 0.7667; V3 28/30 = 0.9333.
Edge-case floor (dimension E, at least 1/5): V1 5, V2 4, V3 5: all variants eligible.

## Combined score (0.50 quant + 0.50 qual)

V1 0.9169; V3 0.8972; V2 0.8591. The top two are 2.2 percent apart, inside the 5 percent band, so the tiebreaker applies (level 1: debate points won).
