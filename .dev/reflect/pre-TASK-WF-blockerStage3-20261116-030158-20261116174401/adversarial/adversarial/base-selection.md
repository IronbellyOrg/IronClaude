# Base selection

Two independent scoring passes by sonnet-class reflect-reviewer agents (the judge class differs from both debaters, haiku and opus): pass 1 evaluated Variant 1 then Variant 2 (agent ad6f2b0ae78c7053d), pass 2 evaluated Variant 2 then Variant 1 (agent ac769198a6d2eb27e). Source requirements for the requirement-coverage metric: 10 items (the 7 first-review blocking findings, the new-defect check, the plan-against-spec check, the blocking-or-minor grading).

## Quantitative scoring (50 percent)

| Metric | Weight | V1 pass 1 | V1 pass 2 | V1 mean | V2 pass 1 | V2 pass 2 | V2 mean |
|---|---|---|---|---|---|---|---|
| RC requirement coverage | 0.30 | 0.95 | 0.95 | 0.95 | 1.00 | 1.00 | 1.00 |
| IC internal consistency | 0.25 | 0.97 | 0.95 | 0.96 | 0.93 | 0.96 | 0.945 |
| SR specificity | 0.15 | 0.90 | 0.88 | 0.89 | 0.93 | 0.93 | 0.93 |
| DC dependency completeness | 0.15 | 0.97 | 0.97 | 0.97 | 0.92 | 0.96 | 0.94 |
| SC section coverage | 0.15 | 0.57 | 0.57 | 0.57 | 1.00 | 1.00 | 1.00 |
| quant score | | 0.894 | 0.886 | 0.890 | 0.960 | 0.974 | 0.967 |

## Qualitative scoring (50 percent): 30 binary criteria with a cited-evidence line each (per-criterion lines are in the two scorer hand-backs; summary)

| Dimension | V1 pass 1 | V1 pass 2 | V2 pass 1 | V2 pass 2 |
|---|---|---|---|---|
| Completeness (5) | 4 | 4 | 5 | 5 |
| Correctness (5) | 5 | 3 | 3 | 4 |
| Structure (5) | 5 | 5 | 3 | 4 |
| Clarity (5) | 5 | 5 | 4 | 4 |
| Risk coverage (5) | 4 | 4 | 4 | 4 |
| Invariant and edge case coverage (5) | 5 | 4 | 5 | 5 |
| Total of 30 | 28 | 25 | 24 | 26 |
| qual score | 0.933 | 0.833 | 0.800 | 0.867 |

Edge-case floor check (at least 1 of 5 on invariant and edge cases): V1 4 or 5, V2 5 of 5. Both eligible.

## Position-bias mitigation

Pass 1 picked Variant 1 (combined 0.914 against 0.880); pass 2 picked Variant 2 (0.920 against 0.860). The passes disagree on the pick and on criteria: for Variant 1 Correctness.1 (pass 1 MET, pass 2 NOT MET: the gate "appears only in the acceptance criterion at PLAN:128"), Correctness.5 (the pass-2 NOT MET rests on "Tasks 10 and 11 name the corresponding replacements", refuted for the zero-trust scorer and conceded in the debate) and Invariant.4; for Variant 2 Correctness.1 (pass 1 NOT MET on `rf-qa.md:389`) and Structure.2 (pass 1 NOT MET: F9 has no Consequence line). Orchestrator re-evaluation with the debate evidence: V1 Correctness.1 MET (PLAN:20 states a constraint, not a check inside Task 5; the claim is accurate for the Task 5 body); V1 Correctness.5 NOT MET (conceded); V1 Invariant.4 MET (F3 targets the "at least 2 of the 3" threshold under an exclusion); V2 Correctness.1 MET (`rf-qa.md:389` is a count-CRITICAL-and-IMPORTANT-as-blocking line as SPEC:853 and PLAN:140 describe it, not a mislabel); V2 Structure.2 NOT MET (F9 has no Consequence line); the first-review F3 "fixed" and the F9 end-point claim stay NOT MET (conceded in the debate). Net after re-evaluation: V1 27 of 30 (0.900), V2 25 of 30 (0.833).

## Combined scoring

| Variant | quant (mean of passes) | qual (after re-evaluation) | Combined |
|---|---|---|---|
| V1 (reviewer-1, analyzer, haiku) | 0.890 | 0.900 | 0.895 |
| V2 (reviewer-2, qa, opus) | 0.967 | 0.833 | 0.900 |

Margin 0.005 (0.6 percent): inside the 5 percent band, so the tiebreaker runs. Level 1 (debate performance, points won in the final Round 2 tables, three shared assumptions excluded): V2 won 11 to 12, V1 won 4 to 7 (the tables disagree on X-001, U-001, U-006). Variant 2 wins on debate performance. Correctness criteria MET (level 2, not reached): V1 3 to 5, V2 3 to 4.

## Selected Base: Variant 2 (reviewer-2 card, qa persona, opus class)

Rationale: the combined scores are within the 5 percent band (V1 0.895, V2 0.900), so the level 1 tiebreaker (debate points won) decides; full coverage of the 10 source requirements; 10 findings against 4. Margin small and pass-dependent; recorded as such.

Strengths to preserve: the first-review disposition lines; the residual-contradiction finding (rule 8, "When in doubt, fail it"); the test re-pin findings (zero-trust scorer, hash description, pinned quota sentence); M6 baseline; README ledger fields; L5 sentence.

Strengths to incorporate from Variant 1: F3 (controlling variant for the recall lines), F1 (gate checked after the edit; upgraded to blocking by the debate and the invariant probe), F4 (stale plugin-mirror sentence in Task 12); the "partly fixed" reading of first-review F3; the Category field is not carried (debate S-001 favoured it only weakly: it is information, not a grade).
