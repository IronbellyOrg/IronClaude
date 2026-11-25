# Base Selection

Scores are computed by hand by the orchestrating session (no script). Pass 2 was run by the same evaluator, not an independent one; see Position-Bias Mitigation.

## Quantitative Scoring (50% weight)

The source has no formal requirement IDs, so RC uses topic matching on the five things the topic asks for: first push and PR; fix-round push; push after revert or rebase; merge; one testable rule that names SEC and FR rows.

| Metric | Weight | Variant 1 | Variant 2 | Computation |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.90 | 0.80 | V1 treats four classes by name, has no named SEC and FR rows or one-sentence rule (4.5 of 5); V2 treats revert and rebase only by assertion (4 of 5) |
| Internal consistency (IC) | 0.25 | 0.96 | 0.96 | 1 - 1/25 each: V1 has X-001 (intra); V2 has X-002 (its ADD1 claim against WC:23 and WC:244) |
| Specificity ratio (SR) | 0.15 | 0.85 | 0.85 | File and line citations, caps, numbers; vague phrases rare in both |
| Dependency completeness (DC) | 0.15 | 0.95 | 0.95 | Internal references (notation lines, SEC rows) resolve; both cite one unresolved item (R25 row in an unpushed file) |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | Six H2 sections each |

quant_score: Variant 1 = 0.27 + 0.24 + 0.1275 + 0.1425 + 0.15 = **0.930**. Variant 2 = 0.24 + 0.24 + 0.1275 + 0.1425 + 0.15 = **0.900**.

## Qualitative Scoring (50% weight): additive binary rubric

CEV for each criterion is summarized as the verdict plus the evidence or the reason for NOT MET (a MET needs a citation).

### Completeness
| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | Covers all explicit requirements | MET (four push classes, Mechanism 2, "What it costs") | NOT MET (revert and rebase only asserted, "Claim") |
| 2 | Edge cases and failure scenarios | MET (PR 368, script push) | MET (head move, rebase "What it risks") |
| 3 | Dependencies and prerequisites | MET (WC:245, R25, SEC-01) | MET (ADD1, WC:245) |
| 4 | Success or completion criteria | NOT MET (no testable one-sentence rule) | NOT MET (same) |
| 5 | Out of scope stated | NOT MET | NOT MET |
Subtotal: V1 3, V2 2.

### Correctness
| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | No factual errors | MET (sha claim flagged honestly, Risks bullet 3) | NOT MET (Mechanism 1 depends on ADD1, rejected by D06 item 5 and contrary to WC:244) |
| 2 | Feasible with constraints | NOT MET (a sha-bound per-fix go cannot exist, own Risks bullet 2) | MET (run-level go fits `--monitor 3`) |
| 3 | Terminology consistent | MET | MET |
| 4 | No internal contradictions | NOT MET (X-001) | MET |
| 5 | Evidence supports claims | MET (WC:245 quote, PR 368 note) | MET (SKILL.md:342-348, pr-submit.md:121) |
Subtotal: V1 3, V2 4.

### Structure
| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | Logical ordering | MET | MET |
| 2 | Consistent hierarchy | MET | MET |
| 3 | Separation of concerns | MET | MET |
| 4 | Navigation aids | NOT MET | NOT MET |
| 5 | Follows convention (brief's position paper format) | MET | MET |
Subtotal: V1 4, V2 4.

### Clarity
| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | Unambiguous | MET | MET |
| 2 | Concrete | MET | MET |
| 3 | Section purpose clear | MET | MET |
| 4 | Terms defined on first use | NOT MET (R25, DQ7 not glossed) | NOT MET (ADD1, DQ7 not glossed) |
| 5 | Decision points identified | MET (Risks name what must be said plainly) | MET |
Subtotal: V1 4, V2 4.

### Risk Coverage
| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | At least 3 risks with probability and impact | NOT MET (no probabilities) | NOT MET |
| 2 | Mitigation for each | NOT MET (Risks bullets name no mitigation) | NOT MET |
| 3 | Failure modes and recovery | MET (PR 368) | MET (PR 368 as counterexample) |
| 4 | External dependency failure | MET (unprotected master, no GitHub brake) | MET (script push, DQ7) |
| 5 | Monitoring or detection | NOT MET | NOT MET |
Subtotal: V1 2, V2 2.

### Invariant and Edge Case Coverage
| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | Collection boundaries (here: zero, one, many rounds) | NOT MET | NOT MET |
| 2 | State interactions across components | MET (head move voids the go) | MET (no end event, PR state) |
| 3 | Guard condition gaps | MET (worker script push, SEC-13) | MET (same) |
| 4 | Count divergence | MET (5-round cap as cost) | MET (`push_count <= max_rounds + 1`) |
| 5 | Interaction effects | MET (push go vs merge go) | NOT MET (does not say how the push go interacts with the merge go beyond "merge is where the brake is spent") |
Subtotal: V1 4, V2 3.

### Qualitative Summary
V1 = 3 + 3 + 4 + 4 + 2 + 4 = 20 of 30 = **0.667**. V2 = 2 + 4 + 4 + 4 + 2 + 3 = 19 of 30 = **0.633**.

### Edge Case Floor Check
V1 4/5 and V2 3/5, both at or above 1/5: both eligible.

## Position-Bias Mitigation

Pass 1 evaluated V1 then V2; pass 2 evaluated V2 then V1, by the same evaluator, so it is not an independent check. No verdict changed between passes (disagreements found: 0, verdicts changed: 0). This is a limit of this run, recorded in the verdict's Unverified list.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | Combined |
|---|---|---|---|
| Variant 1 (OURS) | 0.465 | 0.3335 | **0.7985** |
| Variant 2 (CLAY) | 0.450 | 0.3165 | **0.7665** |

Margin: 3.2 points, under 5%, so the tiebreaker applies.

Tiebreaker level 1 (debate points won in the Round 1 scoring matrix): Variant 1 won C-003, C-005, C-006, C-007, X-002, X-003, S-001 (7); Variant 2 won none outright; Hybrid points C-001, C-002, C-004, C-008, X-001 (5) go to the merge plan. Variant 1 wins at level 1. The owner's weighting rule (OURS wins ties) points the same way.

## Selected Base: Variant 1 (OURS, `position-OURS.md`)

**Rationale.** Higher combined score (0.7985 against 0.7665), more debate points won (7 against 0), and the weighting rule. Both advocates agree the answer is a hybrid in which the owner's per-publication rule stays and the typed run line carries the fix-round pushes.

**Strengths to preserve.** Per-class go for first push, revert, rebase and merge; push go and merge go never cover each other; PR 368 as the reason a go must end; honesty note that sha-bound push is OURS extended and not recorded in D06 or Q01; WC:245's "no earlier pre-authorization".

**Strengths to incorporate from Variant 2.** U-005 (a sha cannot be bound for an unwritten fix commit); U-006 (`/sc:pr-submit`'s mechanical fence at the push: one fix commit per cycle, `push_range_mismatch`, fast-forward only, no default-branch push, `push_count <= max_rounds + 1`); U-007 (merge-time controls as the downstream catch); U-008 (a pre-commit per-issue go is an "earlier pre-authorization", so the R25 amendment must be worded to avoid that); the C-002 benefit (fix rounds covered by the typed run line).
