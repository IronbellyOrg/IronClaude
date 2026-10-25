# Base Selection

Scored inline by the orchestrator (no separate debate-orchestrator agent was spawned; recorded as a degradation). Variant 1 = reviewer-1 card; Variant 2 = reviewer-2 card.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 | Variant 2 | Computation |
|--------|--------|-----------|-----------|-------------|
| Requirement coverage (RC) | 0.30 | 0.833 | 1.000 | Section-level topic matching over source.md sections Fix 1, Fix 2, Fix 3, Fix 4, Quality rules, Noticed. V1 has no Fix 3 finding; V2 touches all six (R2-7 covers the Codecov `<decided file input>`). |
| Internal consistency (IC) | 0.25 | 1.000 | 0.941 | V1: 0 contradictions in 19 claims (12 findings + 7 row verdicts). V2: 1 in 17 (INF-045 "partial" with `where: null`). |
| Specificity ratio (SR) | 0.15 | 1.000 | 1.000 | Script count over `claim:` fields: V1 60 concrete / 0 vague; V2 24 / 0. |
| Dependency completeness (DC) | 0.15 | 1.000 | 1.000 | All card_ref values (C1-C6) resolve in t1-card.md. |
| Section coverage (SC) | 0.15 | 1.000 | 1.000 | Both carry findings, unmapped_row_verdicts, overall_verdict, self_confidence, self_audit. |
| **quant_score** | | **0.950** | **0.935** | |

## Qualitative Scoring (50% weight) — Additive Binary Rubric (CEV)

| Dimension | V1 | V2 | Decisive evidence |
|-----------|----|----|-------------------|
| Completeness | 4/5 | 4/5 | V1 NOT MET c1 (missed Task 8, R2-4); V2 NOT MET c1 (missed Task 5 warning and Task 6 unchanged body, R1-1/R1-5). Both MET edge cases, dependencies, success criteria, out-of-scope. |
| Correctness | 4/5 | 3/5 | V1 NOT MET c1 (R1-12 .venv/uv.lock claims wrong, .gitignore:56, :215). V2 NOT MET c1 (R2-1 overstated, R2-3 contradicts source.md:35) and c4 (INF-045 partial/null). |
| Structure | 5/5 | 5/5 | Both follow the brief's YAML schema with card_ref cross-references. |
| Clarity | 4/5 | 4/5 | Both NOT MET c4 (abbreviations such as BRE, INF, CON undefined). |
| Risk coverage | 4/5 | 3/5 | Both MET c1-c3 (severity + confidence per finding, mitigation per finding, false-fail modes). V1 MET c4 (gh/git identity, R1-6); V2 NOT MET c4. Both NOT MET c5 (no monitoring). |
| Invariant & edge case | 5/5 | 3/5 | V1: deleted paths (R1-12), state file (R1-5), guard gaps (R1-1), line counts (R1-2), two-dot/three-dot interaction (R1-7). V2: guard gap (R2-4), counts (R2-4/R2-6), cross-task state (R2-7); NOT MET collections and interaction. |
| **qual_score** | **26/30 = 0.867** | **22/30 = 0.733** | |

Edge-case floor: both ≥ 1/5, both eligible.

## Position-Bias Mitigation
Pass 1 (V1 then V2) and pass 2 (V2 then V1) were applied by the same orchestrator; verdicts agreed on all 60 criterion-variant pairs. Disagreements found: 0; verdicts changed: 0. Recorded as a single-evaluator dual pass (weaker than independent passes).

## Combined Scoring

| Variant | Quant ×0.5 | Qual ×0.5 | Final |
|---------|-----------|-----------|-------|
| Variant 1 | 0.475 | 0.433 | **0.908** |
| Variant 2 | 0.468 | 0.367 | 0.834 |

Margin 7.4% (> 5%); tiebreaker not applied. Debate points won: V1 7, V2 2, tie/qualify 8.

## Selected Base: Variant 1 (sonnet:analyzer, reviewer-1 card)
- Selection rationale: higher correctness and invariant coverage; owns the two highest-cost false passes (R1-1, R1-5) and the false-fail render hazard (R1-7).
- Strengths to preserve: R1-1, R1-4, R1-5, R1-6, R1-7, R1-9, R1-10, R1-11, R1-8 (artifact home for INF-045).
- Strengths to incorporate from Variant 2: R2-4 (Task 8 acceptance), R2-7 (`<decided file input>` placeholder), R2-5 (explicit dependency repoints), overall verdict not_ready (consensus X-001), INF-041 partial, R2-6 false-pass direction; R2-9/R2-10 as reflect-artifact corrections only.
