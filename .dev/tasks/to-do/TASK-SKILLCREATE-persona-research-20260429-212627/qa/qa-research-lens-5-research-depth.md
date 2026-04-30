# QA Report — Research Depth Lens (Phase 3, Lens 5 of 6)

**Topic:** sc-persona-research-protocol skill creation
**Date:** 2026-04-30
**Phase:** skillcreate-research-depth
**Lens:** Research Depth ONLY
**Depth Tier:** Deep
**Fix authorization:** false (REPORT ONLY)
**Status:** Complete

---

## Overall Verdict: FAIL

**Rationale:** Research is mostly deep — line ranges, [CODE-VERIFIED] tags, and explicit cross-reference disagreement tables exist. However, several findings have shallow areas masked by the overall thoroughness. Adversarial scrutiny found 7 substantive depth gaps (2 Critical, 5 Important) that would not survive a tier-appropriate Deep review.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Section classification evidence depth — line-by-line comparison | PARTIAL FAIL | Shallow areas in S26 & S29 classification rationale; see F-1, F-2 |
| 2 | Boilerplate boundary precision (exact line ranges) | PARTIAL FAIL | tech-research has line ranges; skill-creator boundaries are mixed; task-builder boundaries show only line ranges, no within-line column specificity; see F-3 |
| 3 | Domain variable extraction completeness — all 10 D-fields with evidence | FAIL | D7 (`personares-{...}` lens names) and D8 (validation rules) listed in research-notes table without [CODE-VERIFIED] tags; not back-checked against spec line refs; see F-4 |
| 4 | Cross-reference depth (5 ref skills cross-validated) | PARTIAL PASS | 12-section-classification.md DOES include explicit disagreement table. However, several "SUBSTITUTE" rows from references were never read line-by-line — see F-5 |
| 5 | Anomaly documentation with line refs | PASS | tech-research file 02 lines 173-179, skill-creator file 03 lines 222-228 document anomalies with line refs |
| 6 | Tier-appropriate depth (Deep tier exhaustive cross-validation) | FAIL | Multiple shortcuts taken — see F-6, F-7 |

---

## Findings

### F-1 (IMPORTANT) — S26 classification rationale skips line-by-line comparison
**Location:** `12-section-classification.md` line 98 (S26 row), line 156 (caveat #2)
**Issue:** S26 (Content Rules) is classified SUBSTITUTE without row-by-row comparison. Reference analyses claim "first 6 universal rows + 5 domain-specific rows" but no enumeration which rows are which.
**Fix:** Read tech-research lines 1219-1242 AND skill-creator lines 1401-1424 verbatim, list each row's left-column verbatim, mark each as IDENTICAL/DIVERGENT/SKILL-CREATOR-ONLY.

### F-2 (IMPORTANT) — S29 classification depends on a contradiction not resolved
**Location:** `12-section-classification.md` line 101 (S29 row), line 138 (disagreement table)
**Issue:** S29 has THREE conflicting reference classifications. Resolution rationale asserts universality without demonstration.
**Fix:** Read tech-research lines 1301-1322, skill-creator lines 1495-1522, task-builder lines 1568-1591 side-by-side; produce a 3-column table.

### F-3 (IMPORTANT) — Boilerplate boundaries given as section-level only for prd & tdd
**Location:** `05-reference-prd.md` lines 86-119; `06-reference-tdd.md` lines 36-105
**Issue:** Hedge language ("appear to be COPY") not verified.
**Fix:** Diff prd/tdd/tech-research character-by-character for the relevant ranges.

### F-4 (CRITICAL) — Domain variables D7 and D8 lack [CODE-VERIFIED] tags
**Location:** `research-notes.md` lines 162-163 (D7, D8 rows)
**Issue:** D7 lens names and D8 validation rules are research-author inventions mapped to spec FRs without byte-level verification.
**Fix:** Read spec §10.1 and FR-6/FR-7/FR-22/FR-2 verbatim, quote disclaimer string and constraint phrasing, tag each D8 entry with exact spec line range.

### F-5 (IMPORTANT) — Reference SUBSTITUTE classifications not all line-checked
**Location:** `12-section-classification.md` lines 73-101
**Issue:** Several SUBSTITUTE rows cite line ranges only from tech-research. For Deep tier with 5 references, every SUBSTITUTE call should cite line ranges from at least 3 of 5 references.
**Fix:** Append `(skill-creator Lxxx-yyy, prd Lxxx-yyy, tdd Lxxx-yyy)` line ranges to each SUBSTITUTE row.

### F-6 (CRITICAL) — Tier-inappropriate shortcut: prd and tdd analyses truncated
**Location:** `05-reference-prd.md` (sections 1-5 detailed only), `06-reference-tdd.md` (truncated at S10)
**Issue:** prd modularizes — many canonical sections are absent or in refs/. Each canonical S1-S29 needs explicit PRESENT/ABSENT/EMBEDDED tag. Without this, "5-ref agreement" claim is overstated.
**Fix:** Each canonical section row should have a definitive marker for ALL 29 sections.

### F-7 (IMPORTANT) — task-builder mapped despite being explicitly non-29-section
**Location:** `04-reference-task-builder.md` lines 14-15, 56, 118
**Issue:** task-builder is Stage-A-only orchestrator; cannot validate canonical Stage-B sections (e.g., S19). "All 5 refs agree" claim for COPY sections is overstated.
**Fix:** Footnote which sections task-builder cannot validate; recompute "N of 5 refs agree" denominators.

---

## Summary

- Checks passed: 1 / 6 (anomaly documentation)
- Checks partial: 3 / 6 (classification evidence, boilerplate boundaries, cross-validation)
- Checks failed: 2 / 6 (D-field completeness, tier-appropriate depth)
- CRITICAL findings: 2 (F-4, F-6)
- IMPORTANT findings: 5 (F-1, F-2, F-3, F-5, F-7)
- MINOR findings: 0

**Adversarial assessment:** Found 7 shallow findings. The research has the *appearance* of Deep-tier rigor but Deep-tier *behavior* requires every classification to be backed by actual side-by-side line-level diffing across 5 references.

---

## Recommendations for the fix agent

1. **F-4 (CRITICAL):** Re-verify D7 and D8 against actual spec content with [CODE-VERIFIED] tags.
2. **F-6 (CRITICAL):** Extend prd and tdd reference analyses to cover ALL 29 canonical sections with PRESENT/ABSENT/EMBEDDED tags.
3. **F-7 (IMPORTANT):** Footnote in `12-section-classification.md` which sections task-builder cannot validate.
4. **F-1 / F-2 (IMPORTANT):** Produce side-by-side row-level diffs for S26 and S29.
5. **F-3 (IMPORTANT):** Convert "appear to be COPY" hedge language in 06-reference-tdd.md to verified line ranges.
6. **F-5 (IMPORTANT):** Add 3+ reference line ranges to each SUBSTITUTE row in 12-section-classification.md.

## QA Complete
