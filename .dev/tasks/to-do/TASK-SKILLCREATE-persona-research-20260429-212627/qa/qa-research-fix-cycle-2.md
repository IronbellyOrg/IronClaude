# QA Report — Research Gate Fix Cycle 2

**Topic:** sc-persona-research-protocol skill creation
**Date:** 2026-04-30
**Phase:** fix-cycle
**Fix cycle:** 2
**Fix authorization:** true

---

## Scope

Address the single regression finding from cycle 1 verification (N-1):
count rollup arithmetic in the Canonical RF 29-Section Cross-Mapping
appendices in `research/05-reference-prd.md` and `research/06-reference-tdd.md`.

Source verifier report: `qa/qa-research-verify-1-evidence-quality.md`

---

## Overall Verdict: PASS

The single regression finding (N-1) is resolved. Both appendix rollups now sum to 29 and accurately reflect the row counts in their respective tables.

## Recount Methodology

For each appendix, I read the full 29-row mapping table and tallied each marker (PRESENT / EMBEDDED / ABSENT) by enumerating the rows assigned to each category.

### File 1 — `research/05-reference-prd.md` (lines 463-491)

**Independent recount:**
- PRESENT (18): S1, S3, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, S18, S19, S28
- EMBEDDED (7): S2, S20, S21, S22, S23, S24, S25
- ABSENT (4): S4, S26, S27, S29
- Sum: 18 + 7 + 4 = **29** ✓

**Verifier expected counts:** 18 / 7 / 4 — matches recount.

### File 2 — `research/06-reference-tdd.md` (lines 413-441)

**Independent recount:**
- PRESENT (15): S1, S3, S5, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, S18, S19
- EMBEDDED (9): S2, S7, S20, S21, S22, S23, S24, S25, S28
- ABSENT (5): S4, S6, S26, S27, S29
- Sum: 15 + 9 + 5 = **29** ✓

**Verifier expected counts:** 15 / 9 / 5 — matches recount.

---

## Issues Fixed

| # | File | Line | Original | Corrected |
|---|------|------|----------|-----------|
| 1 | `research/05-reference-prd.md` | 493 | `**Roll-up vs canonical 29:** PRESENT 19 / EMBEDDED 7 / ABSENT 3.` | `**Roll-up vs canonical 29:** PRESENT 18 / EMBEDDED 7 / ABSENT 4.` |
| 2 | `research/05-reference-prd.md` | 494 | "...The 7 EMBEDDED-in-refs sections (S20, S22, S23, S24, S25 in prd) and the 3 ABSENT canonical sections (S4, S26, S27, S29)..." | "...The 7 EMBEDDED-in-refs sections (S2, S20, S21, S22, S23, S24, S25 in prd) and the 4 ABSENT canonical sections (S4, S26, S27, S29)..." |
| 3 | `research/06-reference-tdd.md` | 443 | `**Roll-up vs canonical 29:** PRESENT 14 / EMBEDDED 11 / ABSENT 4.` | `**Roll-up vs canonical 29:** PRESENT 15 / EMBEDDED 9 / ABSENT 5.` |
| 4 | `research/06-reference-tdd.md` | 444 | "...The 11 EMBEDDED-in-refs sections in tdd indicate... the equivalent S20/S22/S23/S24/S25/S28 sections must be GENERATEd..." | "...The 9 EMBEDDED-in-refs sections in tdd (S2, S7, S20, S21, S22, S23, S24, S25, S28) indicate... the equivalent S20/S21/S22/S23/S24/S25/S28 sections must be GENERATEd..." |

### Note on Implication Sentence Edits

In the prd file, the original Implication sentence enumerated only "S20, S22, S23, S24, S25" as the EMBEDDED set (5 items, not 7). Since the rollup count is 7, the corrected enumeration adds S2 (S2 is marked EMBEDDED on line 464) and S21 (S21 is marked EMBEDDED on line 483) to bring the enumerated set into agreement with the count.

In the tdd file, the original Implication sentence cited "S20/S22/S23/S24/S25/S28" (6 items). The corrected enumeration now lists all 9 EMBEDDED items in the parenthetical, and updates the GENERATE-target list to include S21 (which was missing from the original list of items to be GENERATEd in monolithic form).

## Post-Fix Verification

Re-read both files at the corrected lines:

- `05-reference-prd.md` line 493: `**Roll-up vs canonical 29:** PRESENT 18 / EMBEDDED 7 / ABSENT 4.` → 18 + 7 + 4 = **29** ✓
- `06-reference-tdd.md` line 443: `**Roll-up vs canonical 29:** PRESENT 15 / EMBEDDED 9 / ABSENT 5.` → 15 + 9 + 5 = **29** ✓

## Confidence

- **Verified:** 2/2 file rollups recounted from source rows | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100%
- **Tool engagement:** Read: 4 | Edit: 2 | Write: 1
- Each Read targeted the specific appendix/rollup line being verified. Each Edit targeted the specific count string being corrected.

## Actions Taken

1. Read prd appendix (lines 450-509) — enumerated 29 markers, confirmed 18/7/4.
2. Read tdd appendix (lines 400-447) — enumerated 29 markers, confirmed 15/9/5.
3. Edited prd line 493-494 rollup + Implication sentence.
4. Edited tdd line 443-444 rollup + Implication sentence.
5. Re-read both files at corrected lines to verify the edits applied and the math now sums to 29.

## Recommendations

The N-1 regression is closed. No further fixes required for this finding. Cycle 2 verification can confirm and proceed.

## QA Complete

