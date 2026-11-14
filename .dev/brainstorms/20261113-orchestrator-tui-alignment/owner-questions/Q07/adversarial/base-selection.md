# Base Selection: Q7 owner-answer proposals

Scored by the orchestrating session (not an advocate). Variant 1 = A, 2 = B, 3 = C.

## Quantitative Scoring (50% weight)

Requirement set (from question.md): R1 the OB-01 files saved; R2 the pass record saved before any cleaning; R3 owner authorship of the pass record; R4 the "named archive" alternative (merged-requirements.md:249); R5 nothing cleaned before saving; R6 OB-06 prerequisite (d) as written.

| Metric | Weight | A | B | C | Computation note |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.83 | 0.67 | 0.17 | A misses R2 (pass record only in the switch-on PR); B misses R4 and changes R6; C meets only R5 |
| Internal consistency (IC) | 0.25 | 0.92 | 1.00 | 1.00 | A: "after OB-01 is recorded, the sibling may be cleaned" conflicts with the pass record still being only in the sibling until OB-06 |
| Specificity ratio (SR) | 0.15 | 0.85 | 0.90 | 0.90 | Estimated: A leaves the commit route and "the 2026-11-12 record" unspecified |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 | All references resolve |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | Five of five |
| **quant_score** | | **0.907** | **0.885** | **0.736** | |

## Qualitative Scoring (50% weight): Additive Binary Rubric (condensed CEV)

| Dimension | A | B | C | Evidence (short) |
|---|---|---|---|---|
| Completeness (both question parts; edge cases; dependencies; completion criteria; out of scope) | 4 | 5 | 3 | A misses the pass-record gap edge case; C answers neither part and has no completion criterion |
| Correctness (facts; feasible; terms; no contradiction; supported) | 4 | 4 | 5 | A internal conflict as IC; B feasible only after an owner ruling on agent commits and a spec rewording |
| Structure (ordering; hierarchy; separation; navigation; convention) | 4 | 4 | 4 | Same template; no navigation aids |
| Clarity (unambiguous; concrete; purpose; terms; next steps) | 4 | 5 | 5 | A: "the 2026-11-12 record" is ambiguous (decision record or pass record) |
| Risk (3+ risks; mitigation; recovery; external deps; detection) | 3 | 5 | 2 | B: byte check, merge verified, two-versions risk; C: freeze is an instruction, no recovery |
| Invariant and edge cases (file set; cross-item state; guard; count; interaction) | 2 | 4 | 3 | B: OB-06 (d) interaction and byte-check guard; C: OB-08 interaction and full inventory |
| **Total of 30** | **21** | **27** | **22** | |
| **qual_score** | **0.700** | **0.900** | **0.733** | |

Edge-case floor: A 2, B 4, C 3; all eligible.

## Position-Bias Mitigation

Pass 1 order A, B, C; pass 2 order C, B, A. One disagreement: C, Clarity "next steps" (pass 1: 1, "re-ask when the switch-on is scheduled"; pass 2: 0, no date). Re-evaluated: 1 (the trigger is stated even if undated). Verdicts changed: 0.

## Combined Scoring

| Variant | quant x 0.5 | qual x 0.5 | Score |
|---|---|---|---|
| A | 0.453 | 0.350 | 0.803 |
| B | 0.443 | 0.450 | 0.893 |
| C | 0.368 | 0.367 | 0.735 |

Margin B over A: 0.090 (more than 5%); tiebreaker not applied.

## Selected Base: Variant 2 (proposal B)

- Selection rationale: highest combined score, won 5 of 10 debate points (A won 4), and chosen as the lead of the combination by 2 of 3 advocates.
- Strengths to preserve: save every sibling-only record, the pass record included, now and independent of the switch-on; byte comparison; clean only after the merge is verified.
- Strengths to incorporate: from A, the owner re-reads each file before confirming authorship (C-004, A-001), the named-archive alternative (A-002), and the owner as default committer (X-001, won by A); from C, a dated "do not clean" ledger entry today with the full inventory, held until the merge is verified (C-005 partial; U-003).
