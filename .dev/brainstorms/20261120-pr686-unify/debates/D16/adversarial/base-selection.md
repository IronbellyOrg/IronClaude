# Base Selection: D16 prevention package

Scope note: this scores the two position papers as documents. It does not decide the question; the verdict applies the owner's weighting rule on top. Evaluator: one orchestrator, hand counts (no script was run), so every figure below is approximate. Source requirements (R1 to R12): R1 to R9 = the nine items of FULL-REPORT section 11; R10 = names the lightest version that would have prevented the incident; R11 = gives costs; R12 = names which items only the repository admin can enable.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 (OURS) | Variant 2 (CLAY) | Computation |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.917 | 0.750 | OURS states a position on R1 to R9, R11, R12 (11 of 12); no R10. CLAY states a position on R1 to R4, R6, R8 to R11 (9 of 12); R5 (decision log), R7 (cooling period) and R12 (admin-only items) not stated |
| Internal consistency (IC) | 0.25 | 0.955 | 0.900 | OURS: 1 contradiction in about 22 scorable claims (calls the items "cheap-and-enforced" while its risk list admits a queue). CLAY: 2 in about 20 (the mis-cited CONTRIBUTING.md:77-79 passage, found in Round 1; item 3 "merged by someone other than the author" against its own "gates change the working mode", X-003) |
| Specificity ratio (SR) | 0.15 | 0.93 | 0.93 | Both give numbers, paths, logins, issue and PR numbers; both carry a few vague phrases ("a short path list", "within a day") |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | Internal references resolve in both |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | Six H2 sections each |
| **quant_score** | | **0.953** | **0.890** | (RC x 0.30) + (IC x 0.25) + (SR x 0.15) + (DC x 0.15) + (SC x 0.15) |

## Qualitative Scoring (50% weight) - Additive Binary Rubric

CEV = claim, evidence, verdict. MET only with a citation; no citation means NOT MET.

### Completeness
| # | Criterion | V1 (OURS) | V2 (CLAY) |
|---|---|---|---|
| 1 | Covers all explicit requirements | MET (R1 to R9, cost, admin; `variant-1-original.md` Claim and Cost) | NOT MET (no stance on decision log, cooling period, admin-only items; `variant-2-original.md`) |
| 2 | Edge cases and failure scenarios | MET (Risk: queue, shared login, rot, noisy stop) | MET (Risk: no enforcement, silence, invisible owner work) |
| 3 | Dependencies and prerequisites | NOT MET (no prerequisite of Clay accepting the roles text; A-003) | NOT MET (same) |
| 4 | Success or completion criteria | NOT MET (no way to tell it worked) | NOT MET |
| 5 | What is out of scope | NOT MET (no out-of-scope statement) | MET (What it gets right: "does not claim to detect what no check can see") |
| | Subtotal | 2 | 2 |

### Correctness
| # | Criterion | V1 (OURS) | V2 (CLAY) |
|---|---|---|---|
| 1 | No factual errors or hallucinated claims | MET (all ten facts re-checked in Round 1 and Round 2; "silence blocks" is unproven, see INV-007, but is stated as a mechanism not a measured fact) | NOT MET (fact 2 cites CONTRIBUTING.md:77-79 as team governance; it is a rot-budget CI disclaimer, confirmed by both advocates) |
| 2 | Approaches feasible within stated constraints | MET (rulesets are free: public repo, plan `free`) | MET |
| 3 | Terminology consistent | MET | MET |
| 4 | No internal contradictions | MET | NOT MET (X-003) |
| 5 | Claims supported by evidence | MET (each fact cited) | NOT MET (the claim that one paragraph "would have prevented it" is unsupported: PR 681's body already said "the owner reviews and merges" and it was self-merged; INV-026) |
| | Subtotal | 5 | 2 |

### Structure
| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | Logical section order | MET | MET |
| 2 | Consistent hierarchy | MET | MET |
| 3 | Separation of concerns | MET | MET |
| 4 | Navigation aids | NOT MET | NOT MET |
| 5 | Follows the position-paper convention of the brief | MET | MET |
| | Subtotal | 4 | 4 |

### Clarity
| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | Unambiguous language | MET | MET |
| 2 | Concrete rather than abstract | MET | MET |
| 3 | Each section has one purpose | MET | MET |
| 4 | Terms defined on first use | MET | MET |
| 5 | Actionable next steps or decision points | NOT MET (a list of nine items with no order) | MET (four sentences, one template line, one issue to finish) |
| | Subtotal | 4 | 5 |

### Risk Coverage
| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | At least 3 risks with probability and impact | NOT MET (four risks, no probability) | NOT MET (same) |
| 2 | Mitigation for each risk | NOT MET | NOT MET |
| 3 | Failure modes and recovery | NOT MET | NOT MET |
| 4 | External dependencies and their failure | MET (shared login, Risk bullet 2) | MET (fact 5) |
| 5 | Monitoring or validation mechanism | NOT MET | NOT MET |
| | Subtotal | 1 | 1 |

### Invariant and Edge Case Coverage
| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | Collection boundaries (empty, single, maximum) | NOT MET | NOT MET |
| 2 | State across component boundaries | NOT MET | NOT MET |
| 3 | Guard condition gaps | MET (a required reviewer behind the shared login proves little) | MET (fact 5) |
| 4 | Count divergence | NOT MET | NOT MET |
| 5 | Interaction effects | MET (path-limited review versus work in flight) | MET (fact 8, same interaction) |
| | Subtotal | 2 | 2 |

Edge-case floor (needs 1 of 5): V1 2, V2 2. Both eligible.

### Qualitative Summary
| Dimension | V1 | V2 |
|---|---|---|
| Completeness | 2 | 2 |
| Correctness | 5 | 2 |
| Structure | 4 | 4 |
| Clarity | 4 | 5 |
| Risk Coverage | 1 | 1 |
| Invariant and Edge Case | 2 | 2 |
| **Total / 30** | **18** | **16** |
| **qual_score** | **0.600** | **0.533** |

## Position-Bias Mitigation

Pass 1 evaluated V1 then V2; pass 2 evaluated V2 then V1, both by the same evaluator, so this is a weak form of the mitigation (not independent agents). Disagreements found: 1 criterion-variant pair (Correctness 1 for V1: pass 2 first marked NOT MET because "CODEOWNERS makes silence block" was unproven). Re-evaluated with both pieces of evidence: the sentence is a stated mechanism backed by GitHub's documentation that a pull request touching owned content "must be approved by that code owner", so the verdict stayed MET; the unproven part (an author who is himself a listed owner, 0 approvals) is recorded as INV-007 instead. Verdicts changed: 0.

## Combined Scoring

| Variant | quant (x 0.50) | qual (x 0.50) | Final |
|---|---|---|---|
| V1 (OURS) | 0.953 | 0.600 | **0.777** |
| V2 (CLAY) | 0.890 | 0.533 | **0.711** |

Margin: 0.066 (6.6 percent), above the 5 percent tiebreaker band. No tiebreaker applied. (Debate record for reference, from the scoring matrix: OURS wins 4 diff points, CLAY wins 5, 13 are agreed hybrids or neutral.)

## Selected Base: Variant 1 (OURS)

**Rationale.** V1 scores higher on the quantitative layer (coverage of the nine items, the admin-only list, costs) and on Correctness (5 against 2). V2 scores higher on Clarity (an actionable order) and is the only paper that names what it leaves out.

**Strengths to preserve from V1.** The three-layer idea (words, visibility, enforcement); the server-side control that makes silence block; the decision log; the admission that the gate creates a queue.

**Strengths to incorporate from V2** (all of them were adopted by the OURS advocate in Round 2 or confirmed by evidence): the one-sentence silence rule ("silence is never a yes"); drop `/sc:overlap`, stop-on-overlap, the 24 hour timer and the in-flight table; publishing beats searching (three of the four missed items were unpushed or in another repository); the 30 day deletion sentence; root `CLAUDE.md` rather than CONTRIBUTING.md as the carrier; the admin bypass for the owner's own emergency PRs (PR 662, a 3 minute revert); no named deputy who has never acted (`IB-JonathanB`); a direct hold on open PRs that no path list reaches (PR 690).

**Caveat.** The base score rates the documents. It does not decide the question; the weighting rule does (OURS wins unless CLAY shows a clear evidenced benefit; a separable CLAY benefit is adopted as a hybrid).
