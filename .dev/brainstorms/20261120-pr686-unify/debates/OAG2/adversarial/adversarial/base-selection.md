# Base Selection: OAG2

## Quantitative Scoring (50% weight)

Computed by the orchestrator. Specificity ratio and section counts come from a deterministic script (`uv run python -I`, regex counts of numbers, backticked identifiers, file and id references against a fixed list of vague words); the other metrics are counted by reading.

| Metric | Weight | Variant 1 (OURS) | Variant 2 (CLAY) | Computation |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 1.0000 | 1.0000 | 9 requirements: 3 sub-questions (OA-9, OA-17a, OA-17b) plus the 6 paper parts of the brief; each paper covers all 9 (V1 has 9 facts, V2 has 8, both inside the 5 to 10 range) |
| Internal consistency (IC) | 0.25 | 1.0000 | 0.9643 | V1: 0 contradictions in about 30 claims. V2: 1 in about 28 (cost line says the observer keeps the sweep's eight classes, while its mechanism says the observer reads Orca on its own cycle as today) |
| Specificity ratio (SR) | 0.15 | 0.9932 | 1.0000 | V1: 145 concrete, 1 vague; V2: 119 concrete, 0 vague |
| Dependency completeness (DC) | 0.15 | 1.0000 | 1.0000 | Internal cross-references ("facts 4 and 5", "fact 1", "fact 7") all resolve; no unresolved ones |
| Section coverage (SC) | 0.15 | 1.0000 | 1.0000 | 6 H2 sections each |
| **Quantitative score** | | **0.9990** | **0.9911** | 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC |

## Qualitative Scoring (50% weight): Additive Binary Rubric

Pass 1 (forward order, V1 then V2) by the orchestrator. Pass 2 (reverse order, V2 then V1) by an independent subagent that was told not to read any other file of this run; its full evidence table is in `base-selection-pass2.md`. P1 and P2 are the two passes; Final is the verdict after the disagreement rule below. Evidence is a short pointer into the variant; the pass-2 file has its own quotes.

| Criterion | V1 evidence (pass 1) | V1 P1 | V1 P2 | V1 Final | V2 evidence (pass 1) | V2 P1 | V2 P2 | V2 Final |
|---|---|---|---|---|---|---|---|---|
| C1 all requirements | Claims 1 to 3 | MET | MET | MET | Claims 1 to 3 | MET | MET | MET |
| C2 edge cases | Risk bullets: staleness, window, root, entry fields | MET | MET | MET | Facts 1, 5, 7 | MET | MET | MET |
| C3 dependencies | Contract note, S5, window rule | MET | MET | MET | Shared question id, WC-16 edit | MET | MET | MET |
| C4 success criteria | No done-condition or test stated | NOT MET | NOT MET | NOT MET | None | NOT MET | NOT MET | NOT MET |
| C5 out of scope | Fact 8 "needs a design that does not exist yet" | NOT MET | MET | MET | None | NOT MET | NOT MET | NOT MET |
| K1 no factual errors | Spot checks match | MET | MET | MET | Cost line says the observer keeps the sweep's eight classes; `observe/*.py` has no sweep reference | NOT MET | MET | NOT MET |
| K2 feasible | Second link on an existing atomic path | MET | MET | MET | Titles-only is feasible | MET | MET | MET |
| K3 terminology | Consistent | MET | MET | MET | Consistent | MET | MET | MET |
| K4 no contradictions | Window mitigation explained | MET | MET | MET | Cost line against Mechanism | NOT MET | NOT MET | NOT MET |
| K5 claims supported | Facts 1 to 9 | MET | MET | MET | Facts 1 to 8, UNVERIFIED flagged | MET | MET | MET |
| S1 ordering | Claim, Mechanism, Facts, Cost, Risk, Gets right | MET | MET | MET | Same | MET | MET | MET |
| S2 hierarchy | All H2 | MET | MET | MET | All H2 | MET | MET | MET |
| S3 separation | Distinct sections | MET | MET | MET | Distinct sections | MET | MET | MET |
| S4 navigation | Numbered claims and facts | MET | MET | MET | Numbered, cross-referenced | MET | MET | MET |
| S5 conventions | All parts present | MET | MET | MET | All parts present | MET | MET | MET |
| L1 unambiguous | Concrete verbs | MET | MET | MET | No hedge phrases | MET | MET | MET |
| L2 concrete | File:line, numbers | MET | MET | MET | File:line, numbers | MET | MET | MET |
| L3 section purpose | One job each | MET | MET | MET | One job each | MET | MET | MET |
| L4 terms defined | OA-9, D11, R4, S5, "JSON v1" undefined | NOT MET | NOT MET | NOT MET | OA-9, D11, D07, WC-16 undefined | NOT MET | NOT MET | NOT MET |
| L5 next steps | "The spec must say who passes which `--window`" | MET | MET | MET | Shared question id before the observer ships | MET | MET | MET |
| R1 3+ risks with probability and impact | Four risks, no probabilities | NOT MET | NOT MET | NOT MET | Two risks, no probabilities | NOT MET | NOT MET | NOT MET |
| R2 mitigations | Each risk has a rule or display | MET | MET | MET | None given | NOT MET | NOT MET | NOT MET |
| R3 failure modes and recovery | "missing or old file is its own state" | MET | MET | MET | None | NOT MET | NOT MET | NOT MET |
| R4 external dependency failure | "could not read" state; read not tested live (UNVERIFIED) | NOT MET | MET | MET | More Orca reads only | NOT MET | NOT MET | NOT MET |
| R5 monitoring or validation | `observed_at` and age | MET | MET | MET | None | NOT MET | NOT MET | NOT MET |
| I1 collection boundaries | "empty folder, zero rows, could not read" | MET | MET | MET | A string length, not a collection | NOT MET | NOT MET | NOT MET |
| I2 cross-component state | File hand-off; panel's own Orca call | MET | MET | MET | Ledger against report "Needs you" | MET | MET | MET |
| I3 guard condition gaps | Entry field list needed | MET | MET | MET | Sanitizer no markup guard, no field list | MET | MET | MET |
| I4 count divergence | None | NOT MET | NOT MET | NOT MET | None | NOT MET | NOT MET | NOT MET |
| I5 interaction effects | 90 s sweep against 15 s cycle; window with shared file | NOT MET | MET | MET | Window with one root; 90 s against 15 s | MET | MET | MET |

Dimension subtotals (Final): V1: Completeness 4, Correctness 5, Structure 5, Clarity 4, Risk Coverage 4, Invariant and Edge Case 4 = 26 of 30. V2: Completeness 3, Correctness 3, Structure 5, Clarity 4, Risk Coverage 0, Invariant and Edge Case 3 = 18 of 30.

Pass totals: pass 1: V1 23, V2 18. Pass 2: V1 26, V2 19.

Edge case floor (at least 1 of 5 on Invariant and Edge Case Coverage): V1 4 of 5 pass, V2 3 of 5 pass. Both eligible.

Note on Risk Coverage: V2 scores 0 of 5 partly because the brief asked papers to state risks but not mitigations, recovery or monitoring; V1 happened to include them. This is a quality-of-document score, not a measure of which side is right on the question.

## Position-Bias Mitigation

Disagreements found: 4 criterion-variant pairs (V1 C5, V1 R4, V1 I5, V2 K1). Verdicts changed: pass 1 verdict replaced in 3 (V1 C5, R4, I5 became MET) and pass 2 verdict replaced in 1 (V2 K1 became NOT MET).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Why |
|---|---|---|---|---|---|---|
| C5 out of scope | V1 | NOT MET | MET | No | MET | Fact 8 says ending the exception now "needs a design that does not exist yet" and the claim says the exception stays "until a shared questions block exists": an explicit exclusion, if a weak one |
| R4 external dependency failure | V1 | NOT MET | MET | No | MET | The "could not read" state is the Orca-read failure case, and the questions read is flagged "not tested live (UNVERIFIED)" |
| I5 interaction effects | V1 | NOT MET | MET | No | MET | Fact 2 sets the 90 s sweep budget against the 15 s cycle; the risk bullet combines the producer window with the shared file |
| K1 no factual errors | V2 | NOT MET | MET | No | NOT MET | Pass 2 placed the cost-line error under K4 only. V2's own advocate conceded the cost line "is wrong as worded: the observer does not have the eight classes"; a claim shown false under K1 is NOT MET. (One small mis-cite, `report.py:569-599` for the 200-character cut, which is at `report.py:24`, was not counted.) |

The same overclaim appears in both papers ("a sweep per observer cycle cannot fit"; the 90 s figure is a cap, not a measurement, A-003). It is treated as qualified by both advocates and is not scored against either side.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | Combined |
|---|---|---|---|
| Variant 1 (OURS) | 0.9990 gives 0.4995 | 26/30 = 0.8667 gives 0.4333 | **0.9328** |
| Variant 2 (CLAY) | 0.9911 gives 0.4955 | 18/30 = 0.6000 gives 0.3000 | 0.7955 |

Margin: 13.7 points. The 5-point tiebreaker rule is not triggered. Tiebreaker applied: No.

## Selected Base

### Selected Base: Variant 1 (OURS position paper)

Selection rationale: Variant 1 has the higher combined score (0.9328 against 0.7955) and the higher qualitative score (26 of 30 against 18 of 30). The difference comes from risk coverage (4 against 0), one factual slip in Variant 2 (K1) and one internal contradiction (K4). This rates the paper as a document. It does not decide the question; the question is decided in the merged recommendation by the weighting rule (the owner's line wins unless Clay shows a clear, evidenced, separable benefit).

Strengths to preserve from the base: one shared sweep file written on the existing atomic path; the 90 s against 15 s budget argument; WC-16 untouched; the observer shows `observed_at` and age with missing or old as its own state; the three observer states kept distinct; the labelled questions exception; "recommend nothing" on the sweep and "navigation only" on the observer.

Strengths to incorporate from Variant 2: a reader selection rule and the window shown on screen (C-003); the pair-suffix rule is an orchestrator and Variant 1 advocate addition; an entry-field allowlist and a cap (C-007, C-008); the handled-versus-open limit on the questions label (C-010); a follow-up item for one shared question id (C-009); the multi-root rule (C-004); the "views not on record" disclaimer (S-002).
