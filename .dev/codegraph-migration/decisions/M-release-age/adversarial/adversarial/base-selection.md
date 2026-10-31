# Base Selection: M-b minimum release age

Source requirements used for scoring (from context.md and the --focus list):
R1 state a minimum age; R2 state what is picked when the newest release is too young; R3 fit with the user's two-week rule; R4 exposure to pulled or quickly patched releases; R5 lag on security fixes; R6 offline testability.

## Quantitative Scoring (50% weight)

Computation notes (deterministic, from variant text only):
- RC: keyword match per requirement. R1 {age, minimum, days}; R2 {young, younger}; R3 {two-week, 14 days}; R4 {pulled, re-tag, quick, same-day, patch}; R5 {lag, security, fastest}; R6 {test, offline}.
  - A: R1, R4, R5 = 3/6
  - B: all six = 6/6
  - C: R1 to R5 = 5/6
- IC: claims counted per variant.
  - A: 6 claims, 1 contradiction ("fixes days later" against its own same-day example) = 0.833.
  - B: 9 claims, 1 contradiction (X-002: "the eligible release is the settled one" against its own 1.7.0 and 1.7.1 example) = 0.889.
  - C: 8 claims, 0 contradictions = 1.0.
- SR: no variant uses a listed vague indicator, so all score 1.0.
- DC: no variant has internal cross-references, so DC defaults to 1.0 for all.
- SC: no variant has H2 sections, so top-level bullets are the proxy (A 3, B 4, C 3).

| Metric | Weight | A | B | C |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.500 | 1.000 | 0.833 |
| Internal consistency (IC) | 0.25 | 0.833 | 0.889 | 1.000 |
| Specificity ratio (SR) | 0.15 | 1.000 | 1.000 | 1.000 |
| Dependency completeness (DC) | 0.15 | 1.000 | 1.000 | 1.000 |
| Section coverage (SC) | 0.15 | 0.750 | 1.000 | 0.750 |
| **Quant score** | | **0.771** | **0.972** | **0.913** |

## Qualitative Scoring (50% weight): Additive Binary Rubric

Pass 1 evaluated A, B, C in that order; Pass 2 evaluated C, B, A. Both passes were independent agents using the Claim-Evidence-Verdict format. Their per-criterion evidence is summarized here, and full tables are in the agent returns recorded in this pipeline run.

### Dimension subtotals (final, after disagreement resolution)

| Dimension | A | B | C |
|---|---|---|---|
| Completeness | 3 | 3 | 4 |
| Correctness | 3 | 4 | 5 |
| Structure | 4 | 4 | 4 |
| Clarity | 4 | 3 | 4 |
| Risk coverage | 2 | 3 | 1 |
| Invariant and edge case | 2 | 3 | 3 |
| **Total (of 30)** | **18** | **20** | **21** |
| **Qual score** | **0.600** | **0.667** | **0.700** |

Key evidence:
- B: "non-draft, non-prerelease" (Inv-3); "the run summary says which newer release is waiting" (Risk-5); "overrides it for a manual run (for example a security fix)" (Risk-2, Risk-3); "the monitor may still bump" is hedged (Clar-1 not met); bullet 2 mixes the rule with reporting (Clar-3 not met).
- C: "(no fallback to an older eligible release)" (Comp-5); "do nothing this run" (Inv-1); no mitigation for "can block bumping indefinitely" (Risk-2, Risk-3 not met).
- A: "a pulled or re-tagged release can already be in an open PR" (Risk-4; only A covers upstream deletion or re-tagging); "the proof and the human merge are the safety net" is unsupported against context (Corr-5 not met).

### Edge Case Floor Check

| Variant | Invariant and edge case score | Eligible as base |
|---|---|---|
| A | 2/5 | Yes |
| B | 3/5 | Yes |
| C | 3/5 | Yes |

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Resolution reason |
|---|---|---|---|---|---|---|
| Corr-5 | A | 1 | 0 | No | 0 | The central "safety net" claim has no support in the text and contradicts context.md (proof does not test semantics); A's advocate conceded it. |
| Clar-4 | A | 0 | 1 | No | 0 | "the proof" and "pin" are used undefined; same standard applied to all variants. |
| Comp-1 | B | 1 | 0 | No | 0 | R6 asks for offline testability; "one more date comparison to test" does not address offline. Pass 1 itself called it thin. |
| Corr-4 | B | 1 | 1 | Yes | 0 | Override by cross-validation: the criterion is defined as cross-validated with the IC metric, and IC found X-002, which B's advocate conceded. Logged as the one deviation from "use the agreed verdict". |
| Clar-4 | C | 1 | 0 | No | 0 | "at least 7 days old" never says what the age is measured from. B gets the point for "published at least 14 days before the run". |
| Risk-1 | C | 1 | 0 | No | 1 | C names three risks (two-week divergence, fast-train blocking, same-day re-releases). The same-day risk was counted for A in both passes, so it is counted here for consistency. |

- Disagreements found: 5 (plus 1 cross-validation override)
- Verdicts changed from at least one pass: 6

## Combined Scoring

| Variant | Quant x 0.50 | Qual x 0.50 | Combined |
|---|---|---|---|
| A | 0.385 | 0.300 | **0.685** |
| B | 0.486 | 0.333 | **0.819** |
| C | 0.456 | 0.350 | **0.806** |

- The B to C margin is 0.013, under 0.05, so the tiebreaker applies.
- Tiebreaker level 1 is debate performance, counted as points won in the Step 2 scoring matrix. B won 6 points outright (S-001, C-001, C-003, C-004, C-005, A-003) and shared X-001. C won 2 points (C-002, X-002) and shared X-001. Merge-only points (A-001, A-002, A-004, A-005, A-006) count for neither. B leads 6.5 to 2.5.
- Tiebreaker applied: yes, at level 1. Level 2 was not needed.

## Selected Base: Variant 2 (Option B, 14 days, newest eligible)

**Selection rationale.** B is the only option that meets the user's two-week rule (C-001, unanimous). It is also the only one with a security-fix path (C-003) and a waiting report (C-005). It reads the full filtered release list rather than the maintainer-set latest flag (C-004, A-003). It won the debate tiebreaker 6.5 to 2.5.

**Strengths to preserve (B):**
- `MIN_AGE_DAYS = 14` as one constant.
- The non-draft, non-prerelease filter over the full release list.
- The `workflow_dispatch` input `min_age_days`.
- The run summary naming the waiting release and its eligibility date.

**Strengths to incorporate:**
- From C (C-002, X-002, U-003): no fallback. When the newest candidate is too young, do nothing. This removes B's internal contradiction. In the replay it avoided every already-patched release.
- From C and A (debate): a stall warning in the run summary. This answers the starvation risk that no fallback creates.
- From A (Risk-4): name the pulled or re-tagged release case explicitly, and say how the rule behaves.
- From the shared assumptions (unanimous or majority): use `published_at`; order by semver; inclusive exact-seconds boundary; a pure function testable offline; the candidate set split by major line according to M-a.
