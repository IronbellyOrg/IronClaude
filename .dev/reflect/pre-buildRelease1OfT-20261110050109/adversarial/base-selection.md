# Base Selection

Scored by the debate-orchestrator (judge). Both position-bias passes were run by the orchestrator itself, not by separate evaluator agents; this is recorded as a degradation in the return contract.

## Quantitative Scoring (50% weight)

Adaptations for review cards (YAML findings lists, not prose documents): the "source requirements" are the 12 plan units (Constraints + Tasks 1-11), matched against each card's `task` fields; a "section" is one finding; an "internal reference" is one `evidence_file_line` citation, resolved when the cited line supports the claim it is attached to (re-read by the orchestrator).

| Metric | Weight | Variant 1 (R1) | Variant 2 (QA) | Computation |
|--------|--------|----------------|----------------|-------------|
| Requirement coverage (RC) | 0.30 | 0.750 | 0.667 | V1 touches Constraints, Tasks 2, 5, 6, 7, 8, 9, 10, 11 (9/12). V2 touches Tasks 1, 3, 5, 6, 7, 8, 9, 11 (8/12). |
| Internal consistency (IC) | 0.25 | 1.000 | 1.000 | No finding in either card contradicts another finding in the same card. |
| Specificity ratio (SR) | 0.15 | 1.000 | 1.000 | Every finding names a task, quotes a token and cites file:line. |
| Dependency completeness (DC) | 0.15 | 1.000 | 0.976 | V1: 19/19 citations support their claims. V2: 41/42; plan:118 (cited by QA-04) contradicts QA-04's "last good snapshot is kept" half. |
| Section coverage (SC) | 0.15 | 0.583 | 1.000 | 7/12 vs 12/12 findings. |
| **quant_score** | | **0.863** | **0.896** | (RC×0.30)+(IC×0.25)+(SR×0.15)+(DC×0.15)+(SC×0.15) |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

CEV format compressed to one row per criterion: verdict per variant with the evidence.

### Completeness (5 criteria)

| # | Criterion | V1 | V2 | Evidence |
|---|-----------|----|----|----------|
| 1 | Covers all explicit requirements | NOT MET | NOT MET | Both missed T16 and the T22 view texts (debate, Round 2). |
| 2 | Edge cases and failure scenarios | MET | MET | V1: R1-01 overrun, R1-03 failed cycles. V2: QA-04 shape failure, QA-05. |
| 3 | Dependencies and prerequisites | MET | NOT MET | V1: R1-05 (Task 5 needs Task 4). V2: no dependency finding. |
| 4 | Success/completion criteria | MET | MET | Every finding has a `suggested_fix` stating the criterion to add. |
| 5 | Explicit out of scope | NOT MET | MET | V2: QA-02, QA-07, QA-10 test "not excluded by the plan" and QA-10 offers an exclusion. V1: no scope statement. |

### Correctness (5 criteria)

| # | Criterion | V1 | V2 | Evidence |
|---|-----------|----|----|----------|
| 1 | No factual errors | MET | NOT MET | V2: QA-04 says no criterion keeps the last good snapshot (plan:118 does); QA-08 lists NOT AVAILABLE (plan:182 asserts it); QA-11 says no task builds STALE/FAILED cells (plan:126 lists them). V1: R1-06's severity was too low, but no claim is factually false. |
| 2 | Feasible fixes | MET | MET | V1's R1-04 fix offers "narrow the constraint" as an alternative to suppression; all V2 fixes are feasible. |
| 3 | Consistent terminology | MET | MET | Both use plan and SPEC tokens verbatim. |
| 4 | No internal contradictions | MET | MET | IC = 1.0 for both. |
| 5 | Claims supported by evidence | MET | NOT MET | V2's QA-04 cites plan:118, which refutes part of its claim. |

### Structure (5 criteria)

| # | Criterion | V1 | V2 | Evidence |
|---|-----------|----|----|----------|
| 1 | Logical ordering | MET | MET | Both list blocking findings before minor ones. |
| 2 | Consistent hierarchy | MET | MET | Flat list of uniform records. |
| 3 | Separation of concerns | MET | MET | One defect per finding (merging needed only across cards). |
| 4 | Navigation aids | MET | MET | Stable ids and `task` fields. |
| 5 | Artifact conventions | MET | MET | Both follow the reviewer-card schema (id, severity, task, claim, evidence, fix). |

### Clarity (5 criteria)

| # | Criterion | V1 | V2 | Evidence |
|---|-----------|----|----|----------|
| 1 | Unambiguous language | MET | MET | No hedging words in either card. |
| 2 | Concrete | MET | MET | Exact tokens and line numbers. |
| 3 | Each section has a clear purpose | MET | MET | One-sentence claims. |
| 4 | Terms defined on first use | NOT MET | NOT MET | Both use T-numbers, SNAP and SPEC section numbers without definitions. |
| 5 | Actionable next steps | MET | MET | Suggested fixes throughout. |

### Risk Coverage (5 criteria)

| # | Criterion | V1 | V2 | Evidence |
|---|-----------|----|----|----------|
| 1 | ≥3 risks with probability and impact | NOT MET | NOT MET | Neither states probability. |
| 2 | Mitigation per risk | MET | MET | Suggested fixes. |
| 3 | Failure modes and recovery | MET | MET | V1: R1-03 failure publication. V2: QA-04 FAILED (shape). |
| 4 | External dependency failure | MET | MET | V1: R1-02 Orca discovery probe. V2: QA-05 slow Orca calls. |
| 5 | Monitoring/validation mechanism | MET | MET | Both propose tests for every gap. |

### Invariant & Edge Case Coverage (5 criteria)

| # | Criterion | V1 | V2 | Evidence |
|---|-----------|----|----|----------|
| 1 | Collection boundaries | MET | MET | V1: R1-06 empty. V2: QA-02 empty, QA-03 empty page. |
| 2 | State interactions across components | MET | MET | V1: R1-03 collector state vs snapshot file. V2: QA-11 STALE state into the view. |
| 3 | Guard condition gaps | MET | MET | V1: R1-02 runner boundary. V2: QA-04 shape guard. |
| 4 | Count divergence | MET | MET | V1: R1-07 `reported T (page k)`. V2: QA-03 mismatch / changed during read. |
| 5 | Interaction effects | MET | MET | V1: R1-02 discovery vs T36. V2: QA-05 five calls x timeout. |

### Qualitative Summary

| Dimension | V1 | V2 |
|-----------|----|----|
| Completeness | 3 | 3 |
| Correctness | 5 | 3 |
| Structure | 5 | 5 |
| Clarity | 4 | 4 |
| Risk Coverage | 4 | 4 |
| Invariant & Edge Case | 5 | 5 |
| **Total** | **26/30 = 0.867** | **24/30 = 0.800** |

### Edge Case Floor Check

Both variants score 5/5 (floor 1/5): both eligible.

## Position-Bias Mitigation

| Pass | Order | V1 total | V2 total |
|------|-------|----------|----------|
| 1 | V1, V2 | 26 | 24 |
| 2 | V2, V1 | 26 | 24 |

Disagreements found: 0. Verdicts changed: 0. Caveat: both passes were run by the same evaluator (the orchestrator), so this mitigation is weaker than the protocol intends.

## Combined Scoring

| Variant | Quant (×0.5) | Qual (×0.5) | Final |
|---------|--------------|-------------|-------|
| V1 (haiku:analyzer card) | 0.431 | 0.433 | **0.865** |
| V2 (opus:qa card) | 0.448 | 0.400 | **0.848** |

Margin: 0.017 (1.7%), inside the 5% tie band, so the tiebreaker applies.

- Level 1, debate performance (scoring matrix): V2 won 4 points (S-001, C-001, C-002, X-001), V1 won 2 (S-002, X-002). The gap is larger than 5%, so Level 1 decides.
- Tiebreaker applied: Yes (Level 1).

## Selected Base: Variant 2 (reviewer-2 card, opus:qa)

**Selection rationale.** The two cards scored within 2% of each other. V2 won more debate points and covers more of the plan's acceptance tests (12 findings across Tasks 1, 3, 5-9 and 11), so it is the better skeleton for a de-duplicated findings list. V1's higher correctness score is reflected by importing all four of its unique design findings and by narrowing the V2 findings that the debate showed to be partly wrong.

**Strengths to preserve from the base.** QA-01 (four-kind contract gate), QA-02 (T33, blocking), QA-05's T5 citation, QA-09 (inspector caps line), and the minor coverage findings QA-07, QA-10, with QA-03, QA-04, QA-08, QA-11 and QA-12 kept in narrowed form.

**Strengths to incorporate from Variant 1.** R1-02 (discovery probe outside the runner seam), R1-03 (snapshot written only on success), R1-04 (constraint overreach, as minor), R1-05 (missing dependency), and R1-01's and R1-07's citations merged into the matching V2 findings.
