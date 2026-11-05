# Base Selection

Detail files: `score-pass1.md` (forward order, quantitative layer, all 30 criteria) and `score-pass2.md` (reverse order, independent). Both scoring agents ran on claude-opus-5-5.

## Quantitative Scoring (50% weight)

| Metric (weight) | V1 | V2 | V3 |
|---|---|---|---|
| RC requirement coverage (0.30) | 0.769 (10/13) | 0.846 (11/13) | 0.846 (11/13) |
| IC internal consistency (0.25) | 0.957 (1 contradiction in 23 claims) | 1.000 | 1.000 |
| SR specificity (0.15) | 0.923 | 1.000 | 1.000 |
| DC dependency completeness (0.15) | 0.889 (16/18) | 1.000 | 1.000 |
| SC section coverage (0.15) | 1.000 | 1.000 | 1.000 |
| quant | 0.892 | 0.954 | 0.954 |

Note on DC for V1: one unresolved reference ("see t1 grounding") was added to the persisted card by the orchestrator, not by the reviewer; the other is R1-6 (refuted). Scoring was left as the scorer computed it.

## Qualitative Scoring (50% weight) - 30-criterion additive binary rubric

Both passes cite evidence per criterion in the detail files. Position-bias mitigation: pass 1 evaluated V1, V2, V3; pass 2 evaluated V3, V2, V1 independently.

| Dimension (5 criteria each) | V1 pass1 / pass2 / final | V2 pass1 / pass2 / final | V3 pass1 / pass2 / final |
|---|---|---|---|
| Completeness | 5 / 5 / 5 | 4 / 4 / 4 | 5 / 5 / 5 |
| Correctness | 3 / 3 / 3 | 5 / 5 / 5 | 5 / 5 / 5 |
| Structure | 5 / 5 / 5 | 5 / 5 / 5 | 4 / 4 / 4 |
| Clarity | 3 / 5 / 4 | 4 / 4 / 4 | 4 / 4 / 4 |
| Risk coverage | 3 / 3 / 3 | 3 / 3 / 3 | 3 / 3 / 3 |
| Invariant and edge-case | 4 / 4 / 3 | 4 / 3 / 3 | 5 / 5 / 5 |
| Total of 30 | 23 / 25 / 24 | 25 / 24 / 24 | 26 / 26 / 26 |

### Position-bias disagreements (re-evaluated; the re-evaluation verdict is final)

| Criterion | Variant | Pass 1 | Pass 2 | Final | Reason |
|---|---|---|---|---|---|
| L1 unambiguous language | V1 | NOT MET | MET | MET | Hedges are rare; findings name exact variables and values (R1-1) |
| L4 terms defined on first use | V1 | NOT MET | MET | MET | The reviewer's own terms are defined (legacy T1Model slots, defaults.sh:63-65); the dangling "t1 grounding" text was added by the orchestrator |
| E1 collection boundaries | V1 | MET | NOT MET | NOT MET | R1-10 is about scan scope, not an empty or single-element case |
| E1 collection boundaries | V2 | MET | NOT MET | NOT MET | R2-3 is about scan scope, not an empty or single-element case |

Disagreements found: 4 criterion-variant pairs (V1 three, V2 one, V3 none). Verdicts changed from pass 1: 4 (V1 L1, V1 L4, V1 E1, V2 E1). Pass 2 also scored V1 E4 MET (equal mirror line counts) against pass 1 NOT MET; the orchestrator kept NOT MET (a line count is not a count-divergence analysis), so that pair is counted as a fifth disagreement, resolved to pass 1.

Edge-case floor: V1 3/5, V2 3/5, V3 5/5; none below 1/5, all eligible.

## Combined Scoring

| Variant | quant | qual (final) | Combined |
|---|---|---|---|
| V1 | 0.892 | 24/30 = 0.800 | 0.846 |
| V2 | 0.954 | 24/30 = 0.800 | 0.877 |
| V3 | 0.954 | 26/30 = 0.867 | 0.910 |

Margin V3 over V2: 0.033 (3.3%), inside the 5% tiebreaker band. Tiebreaker level 1, debate performance (diff points won outright, `debate-transcript.md`): V3 8, V1 4, V2 3. V3 wins at level 1. Correctness count is 5 for both V2 and V3 and was not needed.

## Selected Base: Variant 3 (reviewer-3 card, refactorer, claude-opus-5-5)

- Selection rationale: highest combined score (0.910), most debate points won (8 of 19), the only variant whose findings tie both interaction blockers to cited plan lines, and the only one with zero self-contradictions and zero pass disagreements.
- Strengths to preserve: R3-1, R3-2 with concrete fixes; the Task 9 anchor corrections (shell variable versus exported variable, `CCSESSION_EXT_PROFILE`); the "Verified correct" list.
- Strengths to incorporate from non-base variants: V2's R2-1 (blocking, unsatisfiable Task 3 check) and R2-4, R2-5; V1's R1-2 (D12 pins the old model), R1-1 (primary ladder activation), R1-3, R1-4, R1-8, and V1's U-001 legacy-slot note.
- Weaknesses of the base to fix in the merge: R3-9 bundles about seven nits (split into separate minor items); R3-8 Task 8 "accurate" and "scope creep" stated together (keep as a note); the claim that Task 8 names no module is correct (plan line 116 says "search tests/ for count_model_aliases").
