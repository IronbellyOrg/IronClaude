# QA Report: Internal-Consistency Lens, Instance b

**Topic:** one unified central Review Panel (shared core plus thin modules) from E1, E2 and E3 (run 2, report only)
**Date:** 2026-11-14
**Phase:** report-validation (Gate 3, structural lens 2 of 5, instance b)
**Report:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/RESEARCH-REPORT-review-panel-unification-run2.md`
**Range reviewed:** lines 2115 to 5057 (Sections 6 to 10, Appendix A pointer, Appendix B); lines 1 to 2114 used by Grep only for cross-reference resolution
**Grading:** grading override in `qa/grading-override.md` applies
**Fix authorization:** false (report only)
**Status:** Complete

---

## Progress log (appended as each part is read)

### Part 1: Section 6 (lines 2115 to 3541) read in full

Checked and found consistent (arithmetic recomputed from the report's own numbers):

| Check | Result |
|---|---|
| 6.3 loss figures: 92 = 56+18+14+3+1; 49 = 24+14+10+1; 88 and 48 length lines; per-model list 30+33+14+7+7+1 = 92 | agree |
| 6.6 conflict classes 13+4+4+15 = 36; 6.12.3 split 14 decided + 22 routed = 36 (9 CL-X + 13 CL-C routed, CL-X11 counted decided) | agree |
| 6.12.10 summary: rows 16+22+36+31+41+15+28 = 189; decided 10+21+14+25+21+15+28 = 134; routed 6+1+22+6+20+0+0 = 55; row counts of Tables A, B, D, F, G recounted from the tables (16, 22, 31, 15, 28); Table E CO-1..CO-41 = 41 | agree |
| 6.12.9 slots C-01..C-15 and 6.12.9.1 outcomes: 15 of 15; base-selection margins recomputed for all 15 (for example C-01 0.8760 - 0.8515 = 2.45; C-08 0.8969 - 0.8956 = 0.13); tiebreaker present exactly where the margin is below 5 percent; unresolved-point counts (28-24, 26-21, 37-32, 44-40) agree | agree |
| 6.12.9 routing-coverage paragraph against the Conflict IDs column and the Decision column of Tables A to G | agree |
| "Adjudicated winners by axis" HIGH-invariant counts against 6.12.9.1 (C-02 three, C-03 two, C-05 seven, C-08 thirteen, C-14 twelve, C-13 two) | agree |
| 6.12.8 table OQ-1..OQ-25 = 25 rows; 6.12.10 says OQ-1..OQ-25 | agree |
| DOC-1..DOC-13 = 13 and the 13 GQ ids listed; RX-1..RX-15 = 15 | agree |

Findings so far (graded under the override; full table in the Findings section):

- P1-1 minor: Section 6 text 2166 and 2393 still say "six of the eight pins" although RX-8 (3394) and LG-4 (3287) correct it to "8 of the 9 pins" and the Corrected-claims header says the corrected form is used above.
- P1-2 (pending check of Sections 7 to 9): two different lists in Section 6 both use ids OQ-1..OQ-n with different meanings (lines 3059 to 3075 and 3430 to 3456).
- P1-3 minor: adjudicated-winners table row 6.11 labels both C-10 and C-11 with the slug `rfqa-first-step-and-readonly-scope`; C-10 is `pr-review-wire-format-and-slot` (3473).

### Part 2: Section 7 lines 3544 to 3634 read (7.0.1, F-1..F-6, 11-axis rationale, A-3..A-9)

Checked and found consistent: the 15 rows of the 7.0.1 combination table cover C-01..C-15 once each; 11 axes in the rationale table; A-3..A-20 = 18 rows and the 12 + 6 split of "differ" and "confirm" = 18; HIGH-invariant counts and convergence figures in rows A-3 to A-9 agree with 6.12.9.1.

### Part 3: Section 7 lines 3635 to 4208 read (A-10..A-20, 7.1, 7.2, adjudication register, contradiction list, 7.3)

Checked and found consistent:

| Check | Result |
|---|---|
| Choices table: 18 rows A-3..A-20 map to 15 slots (A-15/A-16 on C-01, A-4/A-9 on C-02, A-11/A-20 on X-14); the register table at 3829 to 3848 and the "Slot coverage" line (3850) agree | agree |
| 7.3 slot legend: HIGH 60, MEDIUM 161, LOW 23, total 244; sums recomputed (60 = 1+3+2+0+7+4+1+13+0+5+6+2+2+12+2; 161; 23); table rows counted with Grep: 60 HIGH, 161 MEDIUM, 23 LOW, 244 total; per-slot row counts (16, 16, 12, 17, 12, 20, 16, 20, 13, 14, 16, 14, 16, 25, 17) equal the legend's H+M+L for every slot; "addressed" counts (9, 6, 5, 3, 3, 6, 3, 2, 13, 6, 2, 2, 4, 4, 3) plus listed rows equal the debates' invariant totals | agree |
| 7.3 "Where addressed" question ids against Section 9.10 Q-41..Q-88: every HIGH and MEDIUM invariant is in exactly one Q row (checked slot by slot, for example Q-50 = C-02 INV-005..011, 013, 014, 018; Q-86 = 13 X-14 MEDIUM rows; Q-44 = C-08 INV-020, X-14 INV-021, INV-026) | agree |
| Register of r17 in 7.1: 64+46+2+59 = 171; owners 75+29+2+2+14+36+2+11 = 171; Section 1 "75 core, 29 reflect, 4 tasklist and spec" | agree |
| 7.0.1 tensions CT-1..CT-6 against Q-41..Q-46 in 9.10 | agree |
| Rules-check slug lengths (at most 40 characters) for all 15 slugs | agree |

### Part 4: Section 8 lines 4209 to 4647 read (8.1, 8.2 a to e, Open Questions OQ1..OQ24)

Checked and found consistent:

| Check | Result |
|---|---|
| 8.1.0 table: every row total (886, 868, 1,685, 955, 796, 589, 171) and every column total (948, 278, 340, 69, 45, 53, 1,365, 467, 416, 1,969) recomputed; grand total 5,950; 5,779 + 171 = 5,950; DROP reasons 1,753+126+86+4 = 1,969; 118+43 = 161 | agree |
| 8.1.2 line ranges: each group length = rows + 4 (heading, blank, header, separator) for all ten groups; heading lines checked with Grep on `synth-08-value-inventory.md` (45, 997, 1279, 1623, 1696, 1745, 1802, 3171, 3642, 4062); file has 5,950 `VL-`/`DR-` rows (Grep count), 6,127 lines and 2,024,775 bytes (`wc`), as the report states | agree |
| 8.1.1 moved-row counts 9+28+30+2+1 = 70; P3-014 table (214 = 28+2+184; 124 = 30+0+94; 23 = 9+3+11); exchange-layer list 20 + 29 = 49; sum of reason groups 49+7+3+3+4+4 = 70; 184+94 = 278 | agree (but see finding 5) |
| 8.2: C15..C29 = 15 rows; G17..G27 = 11 debate gates; D1..D26; AE-1..AE-15; (e) rf-* call-site split 23+12+4+5 = 44 over 8 files | agree |
| 8.2 G7 ratios 8/13 = 0.615 and 3/39 = 0.077 and 6.8 / G-17 reflect exit codes 0/10/11/2 | agree |

### Part 5: Sections 9 and 10, Appendix A pointer and Appendix B (lines 4648 to 5057) read

Checked and found consistent: gaps log 555 = 243+187+67+58 and 192+363 = 555 (Grep on `gaps-and-questions.md`: 555 rows, 363 `logged-open`); 363 = 185+124+49+5 and 185 = 143+42; Q-38..Q-93 = 56 rows; 221 = 60+161; Evidence Trail: 24 codebase files, 12 scope slices, 4 web files, 10 synthesis files; QA table 42 rows, second table 25 rows, 42+25 = 67; Appendix A pointer figures equal 8.1.2 and the file itself.

---

## Overall Verdict: PASS

Zero findings are blocking under `qa/grading-override.md`. Twelve findings are recorded, all `(minor under grading override)`. For each one I asked whether the recommendation, a value-inventory destination, a conflict-log outcome or a number the recommendation rests on would change if it stays as it is; in every case the correct fact or the correct destination is stated elsewhere in the report (or in Appendix A) and no decision is affected.

## Items Reviewed

| # | Check (lens item) | Result | Evidence |
|---|---|---|---|
| 1 | (a) conflict ids, slot ids and slugs in 6.12.9, 6.12.9.1, "Adjudicated winners by axis", 7.0.1, choices table, register, 7.3, Evidence Trail | PASS with note | 15 slugs and 15 slots agree everywhere; one mislabel (finding 4) |
| 2 | (a) Q-ids cited in 6.x, 7.x and 8.2 against 9.10 | PASS with note | Q-38..Q-93 exist; CT-1..CT-6 map to Q-41..Q-46; two loose cites (finding 11) |
| 3 | (a) OQ, X, C identifier families | PASS with note | collisions between lists (finding 3) |
| 4 | (b) 6.12.10 summary: rows, decided, routed, per table | PASS | 189 = 16+22+36+31+41+15+28; 134; 55; each table recounted from its rows |
| 5 | (b) 15 debates, 244 invariant rows, HIGH 60 / MEDIUM 161 / LOW 23 | PASS | Grep counts and per-slot sums (Parts 3 and 5) |
| 6 | (b) value inventory 5,950 rows and its reconciliation line | PASS | row and column totals recomputed; file verified with Grep and `wc` |
| 7 | (b) defect register 171 rows and owner split | PASS with note | totals agree; family table places 94 of 171 rows (finding 8) |
| 8 | (b) evidence-trail file counts (24 + 12 + 4 + 10; QA 42 + 25 = 67) | PASS | Part 5 |
| 9 | (b) gaps log 555 / 363 / 192 | PASS | Grep on `gaps-and-questions.md` |
| 10 | (b) numeric claims repeated across sections (92/49/88/48; 36 conflicts; 65 vs 38; 36 tests; 110 + 27 names) | PASS with note | agree except the pin count (finding 1), template count (finding 7), pr_submit test count (finding 9), EVAL bucket (finding 10) |
| 11 | (c) cross-references inside range b (6.8.c, 6.12.10, 7.0.1, 7.3, 8.1.4 limit 3b, Section 9.10, synth-09 C29, G17..G27) | PASS | each target exists with the stated content |
| 12 | (d) recommended design (7, 7.1) against 6.12 conflict outcomes and 8.2 constraints | PASS with note | no contradiction in a decision; two status mismatches in tags and carried open-question text (findings 2 and 6) |
| 13 | (d) Section 2 / Section 4 against range b (spot checks by Grep and Read of 4.1, 4.3, G-01, G-17, G-18) | PASS with note | 4.1: 148 = 24+93+31 and the 24 Critical rows listed; G-18 repeats the stale pin count (finding 1) |

## Summary

- Checks passed: 13 / 13 (7 with notes)
- Checks failed: 0
- Blocking findings (under the grading override): 0
- Minor findings (notes, `(minor under grading override)`): 12
- Issues fixed in-place: 0 (fix authorization false; the report was not modified)

## Issues Found

| # | Severity (information label) | Section | Finding | Evidence | Proposed Fix |
|---|---|---|---|---|---|
| 1 | IMPORTANT label, minor under grading override | 6.1, 6.4 (and 4, G-18) | Stale pin count. 6.1 Option A Risk says "six of eight pins read in R03 section 2" and 6.4 Option 2 Effort says "six of the eight pins read assert the defect behaviour"; Section 4 G-18 says "6 of 8 read tests". The conflict log corrects this to "8 of the 9 pins" (RX-8, line 3394; LG-4, line 3287), and the header of "Corrected claims" says the corrected form is used above. No decision rests on it (the effort and risk ratings are unchanged by 6 or 8). | lines 2166, 2393, 1230 against 3287, 3394 | Use "8 of the 9 pins read" at 2166, 2393 and 1230, or add the row to "Corrected claims". |
| 2 | MINOR | 2.x, 6.1, 6.2, 6.12 CO-1, 7 axes 1 and 2, 7.1, 8.2 D9, OQ14, Appendix B | One fact is described in two ways and tagged four ways. Most places say a v2 citation-only finding "crashes the v1 ledger path (KeyError 'anchor')" (tag [CODE-VERIFIED by execution] at G-01 line 1213, REPRODUCED at line 3612); axis 1 of 7 and C-01 say the line "is rejected at findings.py:104 before it can reach annotate"; CO-1 says "no code path from v2 findings to the ledger"; 8.2 D9 and OQ14 tag the KeyError reproduction [CARRIED] and "carried from research/01 and 17". Appendix B (line 5044) reconciles it (the KeyError occurs only when a v2-validated finding reaches `annotate` directly) but nothing in 6.1, 6.2 or 7 points to that. The decision (thin contract; citation-only findings stay out of the v1 ledger path) is the same under both readings. | lines 1213, 2154, 2165, 3306, 3488, 3611, 3612, 3641, 3857, 4467, 4636, 5044 | In 6.1 and 6.2 add "when a v2-validated finding is passed to `annotate` directly; a v1 parse rejects it earlier"; align the tags. |
| 3 | MINOR | 6.x, 6.12, 7, 8.2, 4.3 | Identifier families reused with different meanings. OQ-1..OQ-15 (lines 3059 to 3075, "raised by the options analysis"), OQ-1..OQ-25 (3430 to 3456, "unverified residue") and OQ1..OQ24 (4623 to 4646, 8.2 open questions) are three unrelated lists (for example OQ-9 is the PR panel cost in the first and the approval of T-1..T-10 in the second; OQ-18 in 7 and G24 means the second list). X-13, X-14, X-15 are contradiction rows in 4.3 (lines 1419 to 1421) and debate slots in 6.12, 7 and 9. C-1..C-19 in the Section 7 contradiction list (3856 to 3874) reuse the R01 conflict ids C-1..C-12 and look like slot ids C-01..C-15. Each list is labelled locally, so no decision is misread. | lines listed | Prefix the families (for example `OQ-6a`, `OQ-6b`, `OQ-8`; `CX-` for the 4.3 and Section 7 contradiction rows). |
| 4 | MINOR | "Adjudicated winners by axis" (6.11 row) | The row for 6.11 names the debate as "C-10 and C-11 `rfqa-first-step-and-readonly-scope`". That slug belongs to C-11 only; C-10 is `pr-review-wire-format-and-slot` (6.12.9 line 3473; 6.2 row of the same table uses it correctly). The row's content covers both debates. | line 3017 against 3473, 3474 | Write "C-10 `pr-review-wire-format-and-slot` and C-11 `rfqa-first-step-and-readonly-scope`". |
| 5 | MINOR | 8.1.3 (P3-014, P3-011) | The P3-014 list "Rows that moved to CORE, by reason" ends with "Other single-row moves (4): VL-20-067, VL-23-267, VL-23-479, VL-24-181" and the 70 are counted as moved to CORE; 8.1.1 says VL-24-181 moved from CORE to MODULE-reflect, and Appendix A line 1255 shows destination MODULE-reflect (inside the MODULE-reflect group 997 to 1278). The destination in Appendix A is the correct one; only the narrative list is wrong (69 rows moved to CORE, 1 between modules). Also the P3-011 `_REF_TOKEN` row names VL-19-562 and VL-23-105 in its "What was done" cell but not in its "Rows involved" cell. | lines 4248, 4287, 4352; `synth-08-value-inventory.md:1255` | Move VL-24-181 out of the "moved to CORE" list (or retitle it "moved to CORE or between modules"); add the two ids to "Rows involved". |
| 6 | MINOR | 8.2 Open Questions | OQ8 asks "Which convergence threshold is intended, 0.75 or 0.80?" and OQ9 lists "five further skill-versus-code vocabulary conflicts without a decision" (single-vendor posture, `t2_model_class_diversity`, `contract_version`, `merge_method`). 6.8.c, 6.12.4 CV-1..CV-5, the note after the choices table in 7 and Q-08 in Section 9 classify the threshold (0.80) and the single-vendor posture (degrade) as decided by the code and CV-3..CV-5 as DECIDED-BY-EVIDENCE; only the skill prose is left to reconcile. Section 8.2 is the input for a later plan, so a reader who stops at 8.2 would treat decided items as open. | lines 4630, 4631 against 2757, 3288 to 3292, 3648, 4668 | State in OQ8 and OQ9 that the code decides the threshold and the vendor posture and that the open part is the skill prose and the missing decision record. |
| 7 | MINOR | 8.2 (c) D11 and (e) Core | "The nine `data/*.json` templates" (D11) and "`data/*.json` (nine templates)" (e). G8 (line 4432) says nine files (8 `review-panel.*.json` plus `review-tiers.default.json`); FX-9 says "All 8 packaged templates"; D11's own evidence cell says "24 hits over 8 templates". | lines 4468, 4524 against 3206, 4432 | Write "nine data files (eight templates plus the tier file)". |
| 8 | MINOR | 7.1 defect-family table | The register header gives owners CORE 75, MODULE-tasklist 2, MODULE-spec 2, but the family rows place only 63 CORE rows (8+11+11+5+10+6+10+2), 1 tasklist row (DR-007) and 1 spec row (DR-026): 12 CORE, 1 tasklist and 1 spec row are not in any family (94 of 171 rows are placed: 63 CORE + 29 reflect + 2 others; the last row lumps HARNESS 14, EVAL 36, OPS 2, DROP 11 without ids). Every register row still has a destination in Appendix A, so a later plan does not lose them. | lines 3741 to 3756 | Add a line "14 owned rows (12 CORE) are carried only in Appendix A" or list them. |
| 9 | MINOR | 7.2.1 vs 8.2 G14 | Test-file count for `tests/pr_submit/`: 7.2.1 says "50 files, 47 `test_*.py`"; G14 and (e) say "50 test files plus `conftest.py` and `__init__.py`" (which reads as 52). At HEAD `tests/pr_submit/` holds 47 `test_*.py` and 49 `.py` files (Bash `ls`). | lines 3772, 3779, 4438, 4552 | Use "47 test files (49 `.py` with `conftest.py` and `__init__.py`)". |
| 10 | MINOR | 9.7 Q-32 | "the EVAL bucket is large (285)": 285 matches neither the EVAL destination total in 8.1.0 (1,365) nor Ledger 20's EVAL count (284). Probably a pre-fix figure from the gaps log; no decision uses it. | line 4722 against 4227 to 4234 | Say "1,365 (8.1.0)" or cite the ledger and its count. |
| 11 | MINOR | choices table A-12, A-17 | Row A-12 ends "2 HIGH invariants open (Q-87, Q-89)" and A-17 "6 HIGH invariants open (Q-72 to Q-74, Q-91)". Section 9.10 (line 4743) classes Q-89..Q-93 as owner decisions that are not invariants, and 7.3 maps the X-15 HIGH rows to Q-87 and the C-11 HIGH rows to Q-72..Q-74 only. | lines 3638, 3643 against 4181 to 4203, 4743 | Write "(Q-87; owner decision Q-89)" and "(Q-72 to Q-74; owner decision Q-91)". |
| 12 | MINOR | 7 "Rationale: the 11 decision axes" intro | The sentence "Where a debate overturned the earlier default (axes 1, 2, 4, 5, 8), the cell says so" omits axis 9 (its cell says "CHANGES the earlier default of a kernel `verify-run`") and axis 4 is worded "CHANGES ... in three places"; the choices table counts 12 rows that differ in whole or part (A-3..A-8, A-10, A-11, A-15, A-16, A-17, A-20). | lines 3607, 3614, 3619, 3625 | Reword to "overturned or changed (axes 1, 2, 3, 4, 5, 8, 9, 11)". |

All twelve: (minor under grading override).

## Actions Taken

None. fix_authorization was false; the report and every other file were left unmodified. Read-only checks run: Grep counts on the report, on `synthesis/synth-08-value-inventory.md` and on `gaps-and-questions.md`; `wc -l -c` on the inventory; `ls` counts for `tests/pr_submit/`; Glob of `tests/pr_submit/`.

## Recommendations

- Proceed: no blocking finding, so the gate for this instance and lens is PASS.
- Notes for the follow-up list (grading override): findings 1 to 12 above, each `(minor under grading override)`.
- Outside the report (not a finding of this lens): `qa/report-size-and-partition.md` line 10 says `synth-08-value-inventory.md` has 6,121 lines; the file has 6,127 lines (the report states 6,127 correctly).
- Cross-range note: Section 2.9 (line 1101) says "21 conflicts are logged (CF-01 to CF-21)" while Section 1 says twelve registered conflicts (R01 C-1..C-12) and 6.12.10 counts 189 rows; these are different sets (R01 registry, the overlap-matrix list, the conflict log) and each count is internally correct, but the report never says how the three relate. Instance a owns Section 2.9; not graded here.

## Confidence

Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

Scope limits (not UNVERIFIABLE for this lens, listed for honesty): this lens checks internal agreement, not truth against code; the per-row bodies of Appendix A (5,950 rows) were checked only by count, by heading and line ranges and by one row read (VL-24-181), not row by row; Section 5 and Section 2 figures outside range b were checked only where range b repeats them.

**Tool engagement:** Read: ~40 | Grep: ~42 | Glob: 1 | Bash: 2 (counts approximate; each call targeted a specific check above). Read + Grep + Glob (about 83) exceeds the 13 checklist items. No web research was performed (no Tavily or web calls).

## QA Complete

**Status: Complete**
