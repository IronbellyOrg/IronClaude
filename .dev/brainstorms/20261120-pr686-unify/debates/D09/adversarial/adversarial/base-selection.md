# Base Selection (Step 3)

Scope note: base selection scores the two papers as documents (completeness, correctness of cited facts, structure, clarity, risk coverage, edge cases). It does not decide who wins the question; the verdict applies the owner's weighting rule to the debate outcome. The merged output uses the selected base and folds in the other paper's strengths.

## Quantitative Scoring (50% weight)

The source has no formal requirement IDs, so requirement coverage uses topic matching on six parts of the question: (1) is the hold a clear benefit, (2) the rule change, (3) which writes, (4) by whom, (5) the plan request, (6) the lease comment. Scores for IC come from contradictions found in the diff analysis and the evaluators (C9, C8). SR counts vague indicators (grep: 0 in both papers). DC: no internal cross-references are unresolved in either paper. SC: both papers have 7 H2 sections.

| Metric | Weight | Variant 1 (OURS) | Variant 2 (CLAY) |
|--------|--------|------------------|------------------|
| RC requirement coverage | 0.30 | 0.833 (5/6; lease comment not covered) | 1.000 (6/6) |
| IC internal consistency | 0.25 | 0.933 (1 contradiction / about 15 claims: human gate answers readiness, yet `plan_check` "fills a gap") | 0.875 (2 / about 16: "add or remove one label" against three calls incl. create; "stateless-ish" against the new `holds` map) |
| SR specificity | 0.15 | 1.000 (0 vague, 85 concrete tokens) | 1.000 (0 vague, 100 concrete tokens) |
| DC dependency completeness | 0.15 | 1.000 | 1.000 |
| SC section coverage | 0.15 | 1.000 (7 of 7) | 1.000 (7 of 7) |
| **quant_score** | | **0.9333** | **0.9688** |

## Qualitative Scoring (50% weight): additive binary rubric (30 criteria)

Two independent evaluators ran. Pass 1 order: Variant 1 then 2. Pass 2 order: Variant 2 then 1. Evidence per criterion is in the evaluators' returns, kept in the debate record; the table below gives the final verdicts (M = MET, N = NOT MET) and the pass results.

| Criterion | V1 pass 1 | V1 pass 2 | V1 final | V2 pass 1 | V2 pass 2 | V2 final |
|-----------|-----------|-----------|----------|-----------|-----------|----------|
| C1 covers all parts of the question | M | M | M | M | M | M |
| C2 edge cases and failures | M | M | M | M | M | M |
| C3 dependencies | M | M | M | M | M | M |
| C4 success criteria | N | N | N | N | N | N |
| C5 out of scope | N | M | M | M | M | M |
| C6 no factual errors | M | N | N | M | M | M |
| C7 feasibility | M | M | M | M | M | M |
| C8 consistent terminology | M | N | N | M | N | N |
| C9 no internal contradictions | N | N | N | N | N | N |
| C10 claims supported | M | M | M | M | M | M |
| C11 logical ordering | M | M | M | M | M | M |
| C12 consistent hierarchy | M | M | M | M | M | M |
| C13 separation of concerns | M | M | M | M | M | M |
| C14 navigation and cross-references | M | M | M | M | M | M |
| C15 conventions | M | M | M | M | M | M |
| C16 unambiguous | M | M | M | M | M | M |
| C17 concrete | M | M | M | M | M | M |
| C18 clear purpose per section | M | M | M | M | M | M |
| C19 terms defined | N | N | N | N | N | N |
| C20 actionable next steps | M | M | M | M | M | M |
| C21 risks with likelihood and impact | N | N | N | N | N | N |
| C22 mitigation per risk | N | M | M | N | N | N |
| C23 failure modes and recovery | M | M | M | M | M | M |
| C24 external dependencies | M | M | M | M | M | M |
| C25 monitoring or validation | M | M | M | M | M | M |
| C26 collection boundaries | N | N | N | N | M | M |
| C27 state interactions | M | M | M | M | M | M |
| C28 guard condition gaps | M | M | M | M | M | M |
| C29 count divergence | N | N | N | M | M | M |
| C30 interaction effects | M | M | M | M | M | M |

### Dimension subtotals (final)

| Dimension | Variant 1 | Variant 2 |
|-----------|-----------|-----------|
| Completeness | 4/5 | 4/5 |
| Correctness | 2/5 | 3/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 3/5 |
| Invariant and Edge Case Coverage | 3/5 | 5/5 |
| **Total** | **22/30 = 0.733** | **24/30 = 0.800** |

### Edge Case Floor Check

Both variants score at least 1/5 on Invariant and Edge Case Coverage (3/5 and 5/5). Both eligible.

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| C5 | V1 | N | M | disagree | M (moderator: the Concession states what OURS does not accept; weak but present) |
| C6 | V1 | M | N | disagree | N (moderator verified: OURS says a `holds` store "with four states"; design 4.11 point 6, `orchestrator.md:486`, gives `state` two values and `plan_request` five) |
| C8 | V1 | M | N | disagree | N (coordinator and orchestrator are mixed; this is the naming topic D08) |
| C22 | V1 | N | M | disagree | M (the one listed risk has the mitigation "keep the human gate") |
| C8 | V2 | M | N | disagree | N (same mix: "The coordinator runs `/sc:issue --plan`" against "orchestrator" elsewhere) |
| C26 | V2 | N | M | disagree | M ("present once and not empty", the 17-issue baseline) |

Disagreements found: 6 of 60 criterion-variant pairs. The moderator re-evaluation (the two passes were run unattended with no third evaluator) took the Pass 2 verdict in all six pairs, so the final differs from Pass 1 in six pairs and from Pass 2 in none. Totals are the same under either pass (V1 22, V2 24).

## Combined Scoring

| Variant | quant (x0.50) | qual (x0.50) | Final score |
|---------|---------------|--------------|-------------|
| Variant 1 (OURS) | 0.4667 | 0.3667 | **0.8333** |
| Variant 2 (CLAY) | 0.4844 | 0.4000 | **0.8844** |

Margin: 0.0511 (5.1 percent), above the 0.05 tiebreaker band. Tiebreaker applied: No (by a hair; had it applied, level 1 debate performance gives the points tallied in the debate record as a near tie, level 2 correctness count favours Variant 2 with 3 against 2).

## Selected Base: Variant 2 (CLAY paper)

- **Selection rationale.** Higher combined score: broader coverage of the question (it covers the plan request and the lease comment), better edge-case and budget coverage (C26, C29), and fewer factual errors (OURS has a verified miscount).
- **Strengths to preserve.** The exact write boundary (add or remove one label, no comment), the grant switch and dry-run shadow run, the `hold:backlog` person-only stop, the hand-removed-stays-removed rule, the switch-on baseline.
- **Strengths to incorporate from Variant 1 (OURS).**
  1. The least-privilege chain (workers never write, completion writes need a grant row, R24) as the rule that governs every other write.
  2. The honest concession that the plan check is separable and read-only, and the proposal to ship `plan_check` plus `held_incomplete` first.
  3. The risk of an unattended poll writing wrongly, with the mitigation "the label write is off until a test passes".
  4. NG-2 and D2 as the baseline rules to amend, with D2 left unchanged.
- **Base weaknesses to fix from debate and probe.** One write described as three (create is moved to init); "stateless-ish" wording; `plan_check` treats `<...>` template placeholders as filled (INV-004); the off state warns every cycle (INV-003); the human-gate statement names the wrong tree (INV-002); the body read changes a second owner rule (INV-007).
