# Base Selection: Q9 owner-answer proposals

Scored by the orchestrating session (not an advocate). Variant 1 = A, 2 = B, 3 = C.

## Quantitative Scoring (50% weight)

Requirement set (question.md): R1 NFR-001 kept now; R2 SW-11 handled with a clear status; R3 the first named reader defines fields first (ADJ A-001); R4 keeps the Q17 and V2-04 links workable; R5 nothing changes inside PR #539; R6 one owner for storage rules.

| Metric | Weight | A | B | C | Computation note |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.83 | 0.83 | 0.50 | A misses R6 (per-caller rules); B misses R3; C misses R3, R4, R6 |
| Internal consistency (IC) | 0.25 | 1.00 | 0.90 | 0.95 | B: "tests should pass unchanged" conflicts with appending after the `Report complete` footer (`test_cli_contract.py:1476`); C: "never stored by callers" against its own admission it cannot be enforced |
| Specificity ratio (SR) | 0.15 | 0.90 | 0.90 | 0.90 | Estimated |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 | All references resolve |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | Five of five |
| **quant_score** | | **0.934** | **0.909** | **0.823** | |

## Qualitative Scoring (50% weight): Additive Binary Rubric (condensed CEV)

| Dimension | A | B | C | Evidence (short) |
|---|---|---|---|---|
| Completeness | 5 | 4 | 3 | B: no reader named; C: closes v2 and Q17 paths |
| Correctness | 5 | 3 | 4 | B: footer test conflict and an unguarded fence (sanitizer has no backtick rule, `report.py:569-599`); C: "never" against ADJ A-001 |
| Structure | 4 | 4 | 4 | Same template |
| Clarity | 4 | 4 | 4 | |
| Risk | 4 | 3 | 3 | A names divergent caller storage and deferral; B and C miss the durability gap of gitignored reports |
| Invariant and edge cases | 3 | 3 | 3 | A: trigger and fallback order; B: copy drift, sanitizing; C: unenforceable caller rule |
| **Total of 30** | **25** | **22** | **21** | |
| **qual_score** | **0.833** | **0.733** | **0.700** | |

Edge-case floor: all eligible.

## Position-Bias Mitigation

Pass 1 order A, B, C; pass 2 order C, B, A. One disagreement: B, Completeness "edge cases" (pass 1: 1, two copies drifting; pass 2: 0, misses the footer). Re-evaluated: 1 (drift is a real edge case; the footer miss is scored under Correctness). Verdicts changed: 0.

## Combined Scoring

| Variant | quant x 0.5 | qual x 0.5 | Score |
|---|---|---|---|
| A | 0.467 | 0.417 | 0.884 |
| B | 0.455 | 0.367 | 0.821 |
| C | 0.411 | 0.350 | 0.761 |

Margin A over B: 0.063 (more than 5%); tiebreaker not applied.

## Selected Base: Variant 1 (proposal A)

- Selection rationale: highest combined score, won 6 of 10 points, chosen by all three advocates.
- Strengths to preserve: nothing stored now; SW-11 deferred with a named-reader trigger; caller capture first.
- Strengths to incorporate: from B, the embedded-in-report form as the preferred stored option ahead of relaxing NFR-001, corrected (before the footer, backtick-safe fence, copy-match test); from C, a contract-note sentence now that the JSON is stdout-only until the trigger fires; from the shared-assumption responses, the durability and host caveats.
