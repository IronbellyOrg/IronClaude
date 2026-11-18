# Base selection (step 3): reviewer-card comparison

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 pass 1 | V2 pass 1 | V1 pass 2 | V2 pass 2 |
|---|---|---|---|---|---|
| RC requirement coverage (12 consensus items) | 0.30 | 0.667 | 0.833 | 0.667 | 0.833 |
| IC internal consistency | 0.25 | 1.00 | 0.95 | 1.00 | 0.94 |
| SR specificity | 0.15 | 0.71 | 0.79 | 0.66 | 0.83 |
| DC dependency completeness | 0.15 | 1.00 | 1.00 | 1.00 | 1.00 |
| SC section coverage | 0.15 | 1.00 | 1.00 | 1.00 | 1.00 |
| quant | | 0.857 | 0.906 | 0.849 | 0.910 |

## Qualitative Scoring (50% weight): 30-criterion binary rubric

| Pass | V1 met /30 | V2 met /30 | Note |
|---|---|---|---|
| 1 (order V1, V2) | 28 (0.933) | 26 (0.867) | V2 loses Correctness 1 and 4 |
| 2 (order V2, V1) | 28 (0.933) | 26 (0.867) | same subtotals; the per-criterion detail differs in Completeness 4 (both variants: not met in pass 1, met in pass 2) and in Clarity (V1: pass 1 met 1,2,3,5, pass 2 met 1,3,5; V2: pass 1 met 1,2,3,5, pass 2 met 1,2,5) |

Per-criterion evidence: `debate/scoring-pass1.md`, `debate/scoring-pass2.md`.

## Position-Bias Mitigation

Two independent sonnet-class evaluators (agents af7f9560b210a719f and aca830f6025f4cd00), the second in reverse order. Subtotals agree (28 and 26), but three criterion verdicts disagree between the passes, and the orchestrator resolved each by re-reading the card text against the criterion (a re-evaluation with both passes' notes in view; the evaluators were not re-run): Completeness 4, "defines the success or fix check for each finding": MET for both variants, because every finding carries a Fix line (this adds one point to each variant in pass 1); Clarity 2 for V1, "concrete rather than abstract": NOT MET, because its fixes ("add an explicit, scoped refresh", "control or explicitly override") name no command or check; Clarity 3 for V2, "each finding has one clear purpose": NOT MET, because its F2 bundles the pass rule, the advisory class and the same-reviewers point. Resolved totals: V1 28, V2 26, the same as both passes, so the combined scores and the tiebreak result are unchanged.

## Combined Scoring

| Variant | Pass 1 | Pass 2 | Mean |
|---|---|---|---|
| V1 (reviewer 1, analyzer, haiku) | 0.895 | 0.891 | 0.893 |
| V2 (reviewer 2, qa, opus) | 0.887 | 0.888 | 0.8875 |

Margin 0.0055 (inside the 5 percent band), so the tiebreaker applies. Level 1, debate performance (points won where both advocates agree or the opposing advocate conceded): V2 6, V1 4 (both passes). V2 is the base.

Edge-case floor: both variants meet 5/5 on the last dimension; neither is ineligible.

## Selected Base: Variant 2 (reviewer-2 card, qa persona, opus class)

- Selection rationale: it carries 10 of the 12 consensus items, including the four only it raised (U-003 to U-006); the debate gave it more points; its fixes are the more specific ones.
- Strengths to preserve: the cross-package and baseline findings (U-003, U-004), the stale-numbering and registry-grep findings, the "Checked and sound" mapping to the prior review's recommendations.
- Strengths to incorporate from Variant 1: U-001 (the installed output style is never refreshed; narrowed to naming the release, refresh and install-check steps), U-002 (the owner summary wrongly defers RT1 and RT3), the softer wording of C-001 and the "do not rewrite evidence" clause, the matched-reviewer-configuration point of C-002, the advisory-result handling of C-003.
- Drop or lower: V2 F9 (wrong about Task 4), V2 F2's interval and tolerance demand, V2 F1's "fails every time", V1's blocking grade for the inventory path (C-004 minor).
- Added from the invariant probe: INV-001, INV-002, INV-003 (into F1, F3), INV-004, INV-010 (into F5), INV-006 and INV-014 (into F4), INV-013 (into F7), INV-007, INV-008, INV-009 (new non-blocking findings).
