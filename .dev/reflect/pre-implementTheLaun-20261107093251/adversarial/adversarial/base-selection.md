# Base Selection

## Quantitative Scoring (50% weight)

Computed by the orchestrator from the card text and the consensus list M-01 to M-15 (requirement set for RC). The metrics are approximate, because the "requirements" are consensus findings, not labeled ids.

| Metric | Weight | V1 | V2 | V3 |
|---|---|---|---|---|
| Requirement coverage (consensus items covered / 15) | 0.30 | 0.73 (11/15) | 0.40 (6/15) | 0.63 (9.5/15) |
| Internal consistency (1 - contradictions/claims) | 0.25 | 0.81 | 0.78 | 0.82 |
| Specificity ratio | 0.15 | 0.85 | 0.88 | 0.92 |
| Dependency completeness (references that resolve) | 0.15 | 0.85 | 0.85 | 0.95 |
| Section coverage (sections / 6) | 0.15 | 0.67 | 0.67 | 1.00 |
| **quant_score** | | **0.777** | **0.675** | **0.825** |

## Qualitative Scoring (50% weight): 30-criterion binary rubric, two independent passes

Pass 1 (order V1, V2, V3; sonnet): V1 24, V2 24, V3 27. Pass 2 (order V3, V2, V1; opus): V3 28, V2 25, V1 23.

### Position-bias reconciliation (disagreeing criteria, re-evaluated by the orchestrator with both pieces of evidence)

| Criterion | Variant | Pass 1 | Pass 2 | Final | Reason |
|---|---|---|---|---|---|
| K3 consistent terminology | V1 | MET | NOT MET | NOT MET | "LOW-MEDIUM" is not on the severity scale it uses elsewhere. |
| S5 follows output format | V1 | MET | NOT MET | NOT MET | Adds a Fix column, a hybrid category and a nonstandard severity to the agent's table. |
| E1 collection boundaries | V1 | NOT MET | MET | NOT MET | "Baseline moves once a store exists" is a state shift, not a collection boundary. |
| R5 detection mechanism | V2 | NOT MET | MET | MET | Proposes acceptance cases that detect present-but-ineffective registrations. |
| L5 actionable steps | V2 | NOT MET | MET | MET | Finding 1 gives alternatives and the report ends with a recommended action. |
| E1 collection boundaries | V2 | MET | NOT MET | NOT MET | "Empty parsed-id list" is a confirmed T1 claim, not a boundary finding. |
| C4 how a fix is verified | V3 | NOT MET | MET | MET | Fix 1 requires listing every re-baselined test. |

Disagreements found: 7. Verdicts changed from either pass: 7 (all resolved as shown).

### Totals

| Dimension (5 each) | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 4 | 4 | 5 |
| Correctness | 4 | 5 | 5 |
| Structure | 4 | 5 | 5 |
| Clarity | 2 | 4 | 4 |
| Risk coverage | 5 | 4 | 5 |
| Invariant and edge-case coverage | 3 | 3 | 4 |
| **Total / 30** | **22** | **25** | **28** |
| **qual_score** | **0.733** | **0.833** | **0.933** |

### Edge Case Floor Check

All three variants score at least 3 of 5 on invariant and edge-case coverage; all eligible as base.

## Combined Scoring

| Variant | 0.50 x quant | 0.50 x qual | Combined |
|---|---|---|---|
| V1 | 0.389 | 0.367 | 0.755 |
| V2 | 0.338 | 0.417 | 0.754 |
| V3 | 0.413 | 0.467 | **0.879** |

Margin of the top variant over the runner-up: 12.4 points; no tiebreaker applied (V1 and V2 differ by 0.1 point, which does not affect the base).

## Selected Base: Variant 3 (reviewer 3, refactorer card, opus-class)

Selection rationale: highest combined score, the only card that traced the plan against the existing tests with line numbers (12 "launched" asserts, TOW:1011 stub, check-order effect on la3), best clarity and risk coverage.
Strengths to preserve: the verified test-fallout analysis, the one-line fix list, the "checked and correct" list, the advisory notes.
Strengths to incorporate from non-base variants: V2's matcher-ineffective registration cases, adapter runtime prerequisites, coverage-matrix gap, T-MSG-4 to T-MSG-6, F1-F8 unresolvable, ownership negative cases; V1's gate-has-no-consumer finding, Task 12 dependency, IR-3, issue.md, superclaude.* forms, --pipeline none test limit, sessions/<sid> source; the invariant-probe findings INV-001 to INV-010.
