# Base Selection: Q6 owner-answer proposals

Scored by the orchestrating session (not an advocate). Variant 1 = A, 2 = B, 3 = C.

## Quantitative Scoring (50% weight)

Requirement set (from question.md "What it gates" and the dependencies of those items): OB-03, OB-04, OB-05, OB-06, Q24, Q30.

| Metric | Weight | A | B | C | Computation note |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 1.00 | 0.67 | 1.00 | B names OB-03 to OB-06 but not Q24 or Q30 |
| Internal consistency (IC) | 0.25 | 0.92 | 1.00 | 1.00 | A: its re-open trigger "release 3 is opened" cannot fire while OB-06 is parked (OB-09 is blocked by OB-06, merged-requirements.md:257), 1 conflict in about 12 claims |
| Specificity ratio (SR) | 0.15 | 0.90 | 0.85 | 0.90 | Estimated by counting statements that name an item, file line or number against statements that do not; B carries one UNVERIFIED mechanism |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 | Every internal reference resolves to the spec |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | Five of five sections each |
| **quant_score** | | **0.965** | **0.878** | **0.985** | |

## Qualitative Scoring (50% weight): Additive Binary Rubric

Claim-Evidence-Verdict, condensed: 1 = MET with the cited evidence, 0 = NOT MET.

| Dimension and criterion | A | B | C | Evidence (short) |
|---|---|---|---|---|
| Completeness 1: covers both parts of the question (scope, flip timing) | 0 | 1 | 1 | A answers neither scope nor flip, defers both |
| Completeness 2: edge and failure cases | 1 | 1 | 1 | A: Orca unreachable; B: test fails, PR closed; C: stop rule `:1000` |
| Completeness 3: dependencies | 1 | 0 | 1 | B omits Q24, Q30 |
| Completeness 4: completion criteria | 0 | 1 | 1 | A's trigger cannot fire (circular) |
| Completeness 5: out of scope stated | 1 | 1 | 1 | "What stays unresolved" in all |
| Correctness 1: no factual errors | 1 | 1 | 1 | Spot-checked against spec lines; none found |
| Correctness 2: feasible under constraints | 0 | 0 | 1 | A: circular trigger; B: W1 PR violates OB-06 blockers `:254` |
| Correctness 3: consistent terms | 1 | 1 | 1 | |
| Correctness 4: no internal contradictions | 0 | 1 | 1 | A as IC |
| Correctness 5: claims supported | 1 | 1 | 1 | All cite spec or ADJ |
| Structure 1 to 5 (ordering, hierarchy, separation, navigation, convention) | 4 | 4 | 4 | Same template; no navigation aids (criterion 4 not met by any) |
| Clarity 1: unambiguous | 1 | 0 | 1 | B: "held by this terminal" undefined |
| Clarity 2: concrete | 1 | 1 | 1 | |
| Clarity 3: section purpose clear | 1 | 1 | 1 | |
| Clarity 4: terms defined | 1 | 1 | 1 | |
| Clarity 5: next steps clear | 1 | 1 | 1 | |
| Risk 1: at least 3 risks | 1 | 1 | 1 | |
| Risk 2: mitigation per risk | 0 | 1 | 1 | A names evidence loss without mitigation |
| Risk 3: failure and recovery | 0 | 1 | 1 | B: close PR; C: stop rules |
| Risk 4: external dependency failure | 1 | 1 | 1 | Orca reachability in all |
| Risk 5: detection mechanism | 0 | 1 | 1 | B and C: OB-05 build check |
| Invariant 1: collection boundaries (zero holder Runs, 28 of 53) | 0 | 1 | 0 | B cites 28 of 53 Runs without holder |
| Invariant 2: state across components (guard global boolean) | 1 | 1 | 1 | |
| Invariant 3: guard gaps (`check_run_id` syntax only) | 0 | 1 | 1 | B cites INV-003; C enforces with a test |
| Invariant 4: count divergence | 0 | 0 | 0 | Not applicable to any |
| Invariant 5: interaction effects | 1 | 0 | 1 | A: Q7 interaction; C: OB-04 result feeds scope; B none |
| **Total of 30** | **19** | **24** | **27** | |
| **qual_score** | **0.633** | **0.800** | **0.900** | |

Edge-case floor (at least 1 of 5 invariant criteria): A 2, B 3, C 3. All eligible.

## Position-Bias Mitigation

Pass 1 in order A, B, C; pass 2 in order C, B, A. Disagreements: one (B, Invariant 5: pass 1 gave 1 for "closed unmerged if OB-03 fails", pass 2 gave 0 because that is a failure rule, not an interaction). Re-evaluated with both: 0 (final). Verdicts changed: 1.

## Combined Scoring

| Variant | quant x 0.5 | qual x 0.5 | Score |
|---|---|---|---|
| A | 0.483 | 0.317 | 0.800 |
| B | 0.439 | 0.400 | 0.839 |
| C | 0.493 | 0.450 | 0.943 |

Margin C over B: 0.104 (more than 5%); tiebreaker not applied.

## Selected Base: Variant 3 (proposal C)

- Selection rationale: highest combined score, won 7 of 10 debate points, and chosen by all three advocates in their overall verdicts.
- Strengths to preserve: evidence before scope; W1 test, W2 flip; stop rules at merged-requirements.md:1000-1001; a scope test written against a known sentence.
- Strengths to incorporate: from B, the observation that "this Run only" names an old Run nobody watches, so the realistic W2 choice is "any Run my terminal holds" or no flip (debate C-002, X-001; conceded by C's advocate, concession 1); from A, the explicit fallback that if live Orca, Q24 or Q30 stay unavailable the owner records a dated park rather than an open lane (C-005, won by A), with a trigger that is not circular (A's concession 1).
