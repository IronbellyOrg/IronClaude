# Base selection (condensed scoring)

The protocol's full scoring (five script metrics, a 30-criterion rubric, a dual forward and reverse pass) was not run. The artifacts being compared are three position papers on one decision, not three versions of one document, and a dual pass by the same Sonnet session that orchestrated the debate would not be independent. This is recorded in `return-contract.yaml` (`status: partial`, `fallback_mode: true`). The selection below is a documented count of the debate's own scoring matrix.

## Points won (from `debate-transcript.md`, scoring matrix; majority of three advocates)
| Variant | Points won outright | Points shared or "all agree" |
|---|---|---|
| V1 Haiku defender | C-007, X-003, X-001 (with V3) | C-001 (with V3), C-003, C-006, A-001 to A-005 as groups |
| V2 Sonnet prosecutor | none outright (its BD-1 was withdrawn in round 1; its contingent reword text U-001 was not adopted) | X-001 is a point V2 lost (its claim was false) |
| V3 Sonnet architect | S-001, C-002, C-004, C-005, C-008, C-009, X-002 (7), plus C-001 and X-001 with V1 | C-003, C-006, A-001 to A-005 |

## Quantitative layer (what could be computed without a model)
- Requirement coverage (each variant against the five verdict criteria: unfair, unmeasurable, misleading, REQ-05, REQ-23): V1 covers REQ-05 and REQ-23 and the "misleading" criterion partly; V2 covers all five (it raised the registration gap); V3 covers all five and adds the cost table. Not scored as a number.
- Internal consistency: V2's paper contains a stated tension (position "text unchanged" versus section 5 "contingent reword") and a false factual claim (frozen hash); V3's paper contains one false claim (`config/freeze.json` "unchanged") and a wrong recommendation (b) found by the probe (corrections items 3 and 5); V1's paper contains no false factual claim found by the corrections.
- No numeric scores are given, because a score computed by the orchestrator over three position papers it had briefed would not be independent evidence.

## Selected base: V3 (Sonnet architect)
Reason: it won the most points, kept the options table that shows what each alternative breaks (REQ-05, the RL byte copy, REQ-23, the one PROBLEM-row instruction), and gave the only concrete reading rule. Strengths to keep: the options table, the exact upper bound and "never harmless" wording, the limit that the count may not change a gate. Strengths to incorporate from the others: V1's point that a reword breaks a stated requirement and that shared text is not shared runs; V2's route list R-E to R-I and the sentence that the count is descriptive only. Corrections to apply to the base: its sentence (b) is wrong as written (corrections item 5).

Tiebreaker: not needed (V3 leads by more than five points of the matrix).
