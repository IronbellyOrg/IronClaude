# Base Selection (Q01, who writes a per-issue grant row)

Scoring was done by two independent scorer agents (pass 1 forward order V1 then V2, agent ab3d83fc6c1568a4a; pass 2 reverse order V2 then V1, agent a91c164e94ad9a7f8), then reconciled by the orchestrator. Both agents verified cited facts against the master snapshot. The quantitative layer is estimated by hand (counts of claims are judgment counts), not scripted.

## Quantitative Scoring (50% weight)

Source requirements used for RC (from the Q01 topic block): R-1 which record governs a per-issue grant row; R-2 cleanup-design approval (issue 687); R-3 `--apply` grants; R-4 engages `answer-check`.

| Metric | Weight | V1 pass 1 | V1 pass 2 | V1 used (mean) | V2 pass 1 | V2 pass 2 | V2 used (mean) |
|---|---|---|---|---|---|---|---|
| RC requirement coverage | 0.30 | 0.75 (3/4) | 0.75 (3/4) | 0.75 | 1.00 (4/4) | 1.00 (4/4) | 1.00 |
| IC internal consistency | 0.25 | 1.00 (0/22) | 1.00 (0/28) | 1.00 | 0.95 (1/20) | 0.97 (1/32) | 0.96 |
| SR specificity ratio | 0.15 | 0.93 | 0.87 | 0.90 | 0.94 | 0.91 | 0.925 |
| DC dependency completeness | 0.15 | 0.75 | 0.70 | 0.725 | 0.78 | 0.75 | 0.765 |
| SC section coverage | 0.15 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| **quant_score** | | 0.877 | 0.861 | **0.869** | 0.946 | 0.943 | **0.944** |

Notes both passes agree on: V1 never mentions the cleanup design or issue 687 (R-2 missing) and reaches the validator only as "D:694". V2's one unreconciled contradiction: its Claim says a merge is released by a typed answer while its Mechanism puts `pr.merge` on the standing list (its own costs section admits D04 rejected this).

## Qualitative Scoring (50% weight): additive binary rubric

CEV = claim, evidence, verdict. "Final" is the verdict after disagreement resolution (below). P1 and P2 are the two pass verdicts. M = MET, N = NOT MET.

### Completeness (5)
| ID | V1 P1/P2/Final | V1 evidence | V2 P1/P2/Final | V2 evidence |
|---|---|---|---|---|
| C1 all explicit requirements | N/N/N | cleanup design (issue 687) absent | M/M/M | fact 8: D13 `--apply` and cleanup design |
| C2 edge cases, failures | M/M/M | "executor-invented approval ... refused" | M/M/M | `E-NO-GRANT` covers only own verbs; fail closed |
| C3 dependencies, prerequisites | M/M/M | "validator is only designed ... PR B is not built" | M/M/M | "all PR B and are not built (D:1020)" |
| C4 completion criteria | N/N/N | none found | N/N/N | none found |
| C5 out of scope | N/N/N | none found | N/N/N | none found |

### Correctness (5)
| ID | V1 P1/P2/Final | V1 evidence | V2 P1/P2/Final | V2 evidence |
|---|---|---|---|---|
| K1 no factual error | N/N/N | fact 7 "finds only" omits `orchestrator.md:116` (verified by the orchestrator: a case-insensitive search of master `docs` and `src` finds "grant row" at `orchestrator.md:116` too) | M/M/M | D:116, 688, 694, 696, 1020 and `repos.py:295` verified |
| K2 feasible | M/M/M | chat go, agent records in ledger | M/M/M | standing list plus `answer-check` (design) |
| K3 terminology | M/M/M | "grant row", "owner" used consistently | M/N/N | "Master's `grants` file" misplaces it: `repos.yaml` lives in the orchestrator repo (D:859, D:866) |
| K4 no internal contradiction | M/M/M | claim and mechanism agree; line 57 conflict named as a risk | N/N/N | claim says merge by typed answer; mechanism lists `pr.merge` as standing |
| K5 claims supported | M/M/M | nine cited facts with lines | M/M/M | eight cited facts with D: lines |

### Structure (5)
| ID | V1 P1/P2/Final | V2 P1/P2/Final | Evidence (both) |
|---|---|---|---|
| T1 order | M/M/M | M/M/M | Claim, Mechanism, Facts, Costs, Risks, Strengths |
| T2 hierarchy | M/M/M | M/M/M | six flat H2 |
| T3 separation | M/M/M | M/M/M | costs, risks, strengths separate |
| T4 navigation | M/M/M | M/M/M | "Abbreviations:" line and D:nnn references |
| T5 conventions | M/M/M | M/M/M | claim, mechanism, 8-9 facts, costs, risks, strengths |

### Clarity (5)
| ID | V1 P1/P2/Final | V1 evidence | V2 P1/P2/Final | V2 evidence |
|---|---|---|---|---|
| L1 unambiguous language | M/M/M | "owner says the go in chat, agent records" | M/N/M | "Nobody writes a file; the script refuses ..." (pass 2 judged whether it answers the question, which is not what L1 tests) |
| L2 concrete | M/M/M | lines, dates, commit `bfabf1d63` | M/M/M | D: lines, verb names, key format |
| L3 clear purpose | M/M/M | each H2 one purpose | M/M/M | each H2 one purpose |
| L4 terms defined | N/N/N | "D04 verdict", "PR B", "D2" undefined | N/N/N | "D04", "D13", "U37", "WC-17" undefined |
| L5 actionable next steps | M/M/M | "line 57 needs a one-line correction" | M/N/N | only a quoted "parameterise the owner identity"; no clear next step |

### Risk Coverage (5)
| ID | V1 P1/P2/Final | V1 evidence | V2 P1/P2/Final | V2 evidence |
|---|---|---|---|---|
| R1 three risks with probability and impact | N/N/N | three risks, no probability or impact | N/N/N | four risks, no probability or impact |
| R2 mitigation per risk | N/N/N | none found | N/N/N | none found |
| R3 failure modes and recovery | N/N/N | refusal only, no recovery | M/N/N | fail closed, no recovery (resolved to match V1) |
| R4 external dependencies | M/M/M | "No script checks the recorded row today ... PR B not built" | M/M/M | "Until then there is no check at all" |
| R5 monitoring or validation | N/M/M | "A row an agent writes without the owner's own chat confirmation ... is refused" | M/M/M | "every grant use is logged" |

### Invariant and Edge Case Coverage (5)
| ID | V1 P1/P2/Final | V1 evidence | V2 P1/P2/Final | V2 evidence |
|---|---|---|---|---|
| E1 collection boundaries | N/N/N | none found | M/M/M | missing `grants` key read as an empty list |
| E2 state interactions | M/M/M | line 57 vs chat rule vs tech-ref twin | M/M/M | `E-NO-GRANT` covers two of six entries |
| E3 guard-condition gaps | M/M/M | "chat message does not prove who typed it" | M/M/M | "cannot tell the owner from another session" |
| E4 count divergence | N/N/N | none found | N/N/N | none found |
| E5 interaction effects | M/M/M | merged text and chat rule disagree today | M/M/M | `grants` file inside orchestrator write reach |

### Qualitative Summary
| Dimension | V1 | V2 |
|---|---|---|
| Completeness | 2 | 3 |
| Correctness | 4 | 3 |
| Structure | 5 | 5 |
| Clarity | 4 | 3 |
| Risk Coverage | 2 | 2 |
| Invariant & Edge Case | 3 | 4 |
| **Total / 30** | **20** | **20** |
| qual_score | 0.667 | 0.667 |

### Edge Case Floor Check
V1: 3 of 5 (eligible as base). V2: 4 of 5 (eligible).

## Position-Bias Mitigation

Dual pass ran in opposite orders. Pass totals: V1 19 and 20; V2 23 and 19. Disagreements found: 5 criterion-variant pairs (V1 R5; V2 K3, L1, L5, R3). Re-evaluated by the orchestrator with both pieces of evidence in view; final verdicts: V1 R5 MET (pass 2); V2 K3 NOT MET (pass 2); V2 L1 MET (pass 1); V2 L5 NOT MET (pass 2); V2 R3 NOT MET (pass 2, and consistent with V1 R3 where both passes agreed). Verdicts that differ from pass 1: 4. Verdicts that differ from pass 2: 1. Each scorer was more generous to the variant it scored second: V2 scored 23 when second and 19 when first; V1 scored 20 when second and 19 when first. That is the position bias the dual pass exists to catch. The four V2 pairs where the passes split (K3, L1, L5, R3) account for the whole 4-point swing.

## Combined Scoring

| Variant | quant (0.50) | qual (0.50) | Combined |
|---|---|---|---|
| V1 (OURS) | 0.869 | 0.667 | 0.768 |
| V2 (CLAY) | 0.944 | 0.667 | 0.805 |

Margin: 0.037 (3.7%), under the 5% threshold. Tiebreaker applied.

Tiebreaker level 1 (debate performance, points won in the scoring matrix): V1 won 3 points (C-005, X-001, X-002); V2 won 0 outright (C-001 and A-001 and A-002 ended as hybrid or agreement; five points unresolved). V1 wins at level 1; levels 2 and 3 not needed. (Had level 2 been reached, correctness counts are 4 for V1 and 3 for V2, the same direction.)

## Selected Base: Variant 1 (OURS, `variant-1-original.md`)

Selection rationale: the combined score favours V2 by 3.7 points, which is inside the tie band, and the qualitative layer is tied at 20 of 30. Debate points decide it: V1 won three points, V2 none outright. The weighting rule of this run (OURS wins ties and wins unless CLAY shows a clear, evidenced benefit) points the same way.

Strengths to preserve from the base: the owner-record provenance chain (Decision 8, the 2026-11-17 chat rule, PR 585 provenance, owner-answers line 285); master line 241 as the already-built chat route; the per-action refusal of standing merge and close; the Ruling-line precedent.

Strengths to incorporate from the non-base variant (V2):
1. `answer-check` source, entry and freshness tests, with the owner identity parameterised (debate points C-001, C-003, A-003).
2. Question-key binding for a go (`merge_safety:<PR>:<head sha>` style), which gives the go an end when the head moves (A-003).
3. Fail-closed default and a log of each grant used (C-006).
4. Cover the cleanup-design approval and `--apply` explicitly (V1 missed requirement R-2).
5. The point that the per-issue row has no reader in master since PR 682, and that the old row's writes are covered by standing low-stakes grants (C-002, A-002).

Corrections to apply to the base: fact 7 of V1 must add `docs/designs/orchestrator.md:116` to the "grant row" hits; "contract lines 241 and 245 refuse bulk standing grants" must say what they literally say (an outward action needs the user's instruction naming it; no pre-authorization waives a push) and attribute the "no standing merge and close" conclusion to the D04 verdict.
