# Base Selection: D13 position papers

Scoring inputs: both variants, the diff analysis and the debate transcript. Note: the quantitative layer was estimated by hand from the texts (the skill's formulas, no script), and the qualitative layer was scored by two independent evaluator agents (pass 1 in input order, pass 2 in reverse order). The scores measure how complete and well made each paper is as a document. They do not decide the question; the question is decided in VERDICT.md under the owner's weighting rule.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 (OURS) | Variant 2 (CLAY) | Computation |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.875 | 1.000 | 8 topics: closeout, cleanup, PR log, sc:close, hourly sweep, adoption as coordinator steps, complementary-or-duplicate answer, costs and risks. Variant 1 gives no explicit adoption answer for the PR log (7 of 8). Variant 2 covers 8 of 8. |
| Internal consistency (IC) | 0.25 | 1.000 | 1.000 | No intra-variant contradiction found in either (claims about 25 each) |
| Specificity ratio (SR) | 0.15 | 0.95 | 0.95 | Hand estimate: both are dense in numbers, line references and PR numbers; vague wording is rare |
| Dependency completeness (DC) | 0.15 | 1.000 | 1.000 | Internal references (fact numbers, sections) resolve in both |
| Section coverage (SC) | 0.15 | 1.000 | 1.000 | Six H2 sections each |
| **quant_score** | | **0.955** | **0.9925** | |

## Qualitative Scoring (50% weight): additive binary rubric

Final verdicts after position-bias handling (see below). Evidence per criterion is in the two evaluator tables (kept in the evaluator reports; summarised here per dimension).

| Dimension | Variant 1 | Variant 2 | Main reason |
|---|---|---|---|
| Completeness (5) | 3 | 5 | Variant 1 gives no per-piece complementary-or-duplicate answer (C1) and no out-of-scope statement (C5); Variant 2 states "never deletes anything" and lists scope limits |
| Correctness (5) | 4 | 4 | Both mix "orchestrator" and "coordinator" without defining them as one role (R3 not met for both) |
| Structure (5) | 5 | 5 | Same six-section layout |
| Clarity (5) | 3 | 4 | Variant 1's core claim ("must be read under 339's scope") is vague (L1); both use unexplained terms (L4 not met for both) |
| Risk coverage (5) | 0 | 3 | Both list only two risks with no ratings or mitigations (K1, K2); Variant 2 describes fail-closed behaviour, the shared landed check and the dry run (K3 to K5) |
| Invariant and edge case (5) | 4 | 5 | Variant 2 has the 53 versus 26 worktree count gap and the shared landed check; Variant 1 has the open-issue worktrees and the closeout-is-not-sc:close scope gap, but no state interaction analysis (E2) |
| **Total (30)** | **19** | **26** | qual_score 0.633 and 0.867 |

Edge case floor: both variants score at least 1 of 5, so both are eligible.

## Position-Bias Mitigation

| Variant | Pass 1 total | Pass 2 total | Criteria that disagreed | Resolution |
|---|---|---|---|---|
| Variant 1 | 19 | 17 | C4 (0 then 1), R3 (0 then 1), R4 (1 then 0), T3 (1 then 0), L4 (1 then 0), E4 (1 then 0) | Re-evaluated by the orchestrator with both pieces of evidence: C4 MET (fact 3 states the done-condition for 339), R3 NOT MET (terms mixed, equivalence unstated; A-001), R4 MET (the risk is stated as a risk, and the "must not land" rule is paired with a stated cost), T3 MET (repetition of quotes, not mixed concerns), L4 NOT MET (Orca and WC-16 not defined; same standard as Variant 2), E4 MET (scope mismatch: closeout is not the sc:close 339 describes) |
| Variant 2 | 26 | 27 | R3 (0 then 1) | Re-evaluated: NOT MET, same standard as Variant 1 |

Disagreements found: 7. Verdicts changed from at least one pass by the re-evaluation: 7 of 7 took one pass's side, none was new. The re-evaluation was made by the orchestrating session, not by a third evaluator (the skill allows a re-evaluation prompt; no third agent was used).

## Combined Scoring

| Variant | quant (x0.50) | qual (x0.50) | Final |
|---|---|---|---|
| Variant 1 (OURS) | 0.4775 | 0.3167 | **0.794** |
| Variant 2 (CLAY) | 0.4963 | 0.4333 | **0.930** |

Margin: 13.6 points. The tiebreaker (5% band) was not needed.

## Selected Base: Variant 2 (CLAY)

**Selection rationale.** Variant 2 is the more complete and better-evidenced document: it answers the question for every piece, states what each tool will not do, and describes how removal fails safe. Variant 1 is weaker as a document because it gives no per-piece answer, no out-of-scope statement and no description of how its preferred coordinator-owned removal would be validated.

**Limit of this result.** Choosing Variant 2 as the base for the merge does not mean the contested rule wins. Under the owner's weighting rule, Variant 1's accountable-owner position and the owner's 339 wording must be merged in (X-001, C-002), and the debate converged on HYBRID. The refactoring plan reflects that.

**Strengths to preserve from the base:** the per-tool mechanisms; the nine rules; the shared landed check; closeout's three settled items and its never-deletes limit; the PR log's independence.

**Strengths to incorporate from Variant 1:** the owner's 339 duty text (2026-11-05 comment, 2026-11-17 status review); WC-16 running `/sc:sweep` on every coordinator wake; the accountable-coordinator requirement; the open-approval gap on the wave 8 chain; the risk that a defect in a coordinator's checks destroys unpushed work.
