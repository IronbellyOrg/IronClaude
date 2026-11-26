# Merge log (base: variant 3, plan: refactor-plan.md)

Inputs read: `base-selection.md`, `refactor-plan.md`, `variant-3-original.md` (base), `variant-1-original.md`, `variant-2-original.md`, `diff-analysis.md`. Output: `merged-output.md`. Grades and labels were copied from `refactor-plan.md`; none was changed. `V1`, `V2`, `V3` = the three variant cards. Merged-row ids M-01 to M-16 follow the plan's table; "first-review M-xx" means the prior-blocker ids.

## Applied changes

Prior-blocker table
1. Took the base table (V3) for first-review M-01 to M-09 and M-11 and added V1 and V2 evidence lines to each (V1: base-commit comparison for M-03, Check 9 for M-02, `_SITE` match for M-07; V2: line ranges) without removing any V3 citation.
2. First-review M-10: changed the status from "resolved" (V3, V1) to "regressed" (V2, X-001 settled for V2); kept V3 and V1 line cites for the T-04 and T-21 pieces that are present; pointed the regression at row M-01 and the leftover FR-109 cases at row M-09.
3. Kept the status line "ten resolved, one regressed".

Deviation rows
4. M-01: added from V2 (R2-01), text and evidence as V2 wrote them; V1 row 1 contributed the "bare abandon" example and the "no override recorded" point; V1's Medium grade not used (X-002).
5. M-02: kept from V3 row 1.
6. M-03: kept from V3 row 2; merged the advisory gap 1 (git-lfs, `check-attr` suggestion, UNVERIFIED runners) into it (C-003 and C-017 are one row).
7. M-04: kept from V3 row 3.
8. M-05: kept from V3 row 4; added a `(line differs between reviewers)` note on where the T-16 override is recorded (PLAN:29 in V3, PLAN:20 in V1 and V2).
9. M-06: kept from V3 row 5.
10. M-07: added from V1 row 2.
11. M-08: kept from V3 row 8; added V1 row 3 detail (the reject-`add`-without-index case, Tasks 13 to 15 dependence, PLAN:174).
12. M-09: added from V1 row 4.
13. M-10: added from V1 row 5.
14. M-11: added from V1 row 6; the "Medium:" prefix of the V1 text was left out because the plan's grade is Note.
15. M-12: added from V1 row 7; the "Medium:" prefix was left out because the plan's grade is Note.
16. M-13: kept from V3 row 6; added V1 row 8 and its PLAN:31 cite, marked `(line differs between reviewers)` against V3's PLAN:40.
17. M-14: kept from V3 row 7.
18. M-15: kept from V3 row 9.
19. M-16: added from V2 (NFR-013 gap, carried forward from first-review M-27); category written as "Gap", V2's own word, because V2 gave no taxonomy category.

Other sections
20. Coverage note: took the 17 / 8 / 1 lists from V2 and kept V2's remark that the inactive count is 17, not 16 (FR-037).
21. Counts line printed exactly as `blocking 2, label_high 2, medium 8, note 6`.
22. `follow-up candidates`: one line for each of M-03 to M-10.
23. Short names `PLAN`, `DESIGN`, `REQ` defined at the top and used instead of the cards' `P`, `D`, `R`, `source.md` and `merged-requirements.md`; line numbers unchanged.
24. Provenance table added after the rows (source variant and source row per row).
25. Row renumbering: V3's "row 1" to "row 9" became M-02, M-03, M-04, M-05, M-06, M-13 (row 6), M-14 (row 7), M-08 (row 8), M-15 (row 9); the cross-references inside V3 and V1 text ("Row 1 is a new gap", "row 4", "row 5", "row 7") were rewritten to the merged ids M-02, M-05, M-10, M-12.
26. Added `(line differs between reviewers)` marks in the prior-blocker table where V1 and V3 cite different lines for the same claim: first-review M-06 (`test_task_workspace_lifecycle.py`) and first-review M-08 (`archive_workspace.py`).
27. Cross-reference added in first-review M-08: the pattern count on `archive_workspace.py` lines 44-67 is disputed (V1 cites those lines for "the nine"; V3 says they hold eleven), pointing to row M-14. Both cites kept; no line was changed.

## Dropped items

- C-014 (V1 row 9, the 15-line growth budget of `SKILL.md` across Tasks 26 and 30 is tight): dropped, not a defect by majority (`refactor-plan.md`). V1's UNVERIFIED remark on it is not carried.
- C-019 (V2's 26-id disposition): not a finding; carried only as the coverage note, not as a row.
- V1's paragraph on first-review M-12 to M-24 and the UNVERIFIED lists of V1, V2 and V3: outside the required form of the merged output, not carried, except that V1's link of its test-first row to first-review M-20 and V3's carried-forward remark on first-review M-33 appear in the provenance and row text. UNVERIFIED marks that sit inside a row's own text are kept.
- V3's "Adherence summary", "Notes" and "Reviewer recommendation" sections: not carried (replaced by the counts line and the follow-up list).

## Changes not being made

- V1's "No Blocking defect found" verdict is rejected (X-002 settled for V2). V1's Medium grade for the Task 28 rule is not used.
- V2's Blocking grade for C-004, C-005, C-006 and C-010 is rejected: no named decision, acceptance check or quoted number changes if the text is corrected. The V2 card read for this merge has no row for those ids; the position is taken from `refactor-plan.md` as written. Merged rows M-04, M-05, M-06, M-10 keep the plan's Medium grade.
- V1 and V3 status "first-review M-10 resolved" is replaced by "regressed" (X-001 settled for V2).
- No grade was raised or lowered against `refactor-plan.md`. For M-05 and M-08 the advocate votes were split (M-05: Note, Blocking, Medium; M-08: Note, Medium, Medium); the plan's grade (Medium) is used as written.
- No citation was corrected or added. `base-selection.md` says four plan line numbers in the base drifted (K5, a form defect); the plan says to keep every citation as the cards wrote it, so those cites are unchanged and left to the evidence validator.

## Escalations

None. Every planned change could be applied as written.

## Final re-scan for contradictions inside merged-output.md

Checks run on the finished file, with their results.

- Row grades by pattern match on the 16 table rows: Blocking (Decision) with label HIGH = 2 (M-01, M-02), Medium = 8 (M-03 to M-10), Note = 6 (M-11 to M-16). This matches the counts line `blocking 2, label_high 2, medium 8, note 6` and `refactor-plan.md`. No row carries a grade other than the plan's.
- Prior-blocker table: ten rows read "resolved" (first-review M-05 reads "resolved (in its named scope)") and one row (M-10) reads "regressed". This matches the heading and the counts paragraph.
- Row M-01 (blocking) and the first-review M-10 row (regressed) point at each other; no row calls first-review M-10 resolved. The V3 and V1 "resolved" wording survives only as "the T-04 and T-21 pieces are present", which does not contradict the regression.
- No row text states a grade other than its grade column (the leading "Medium:", "Note:" and "Blocking (Decision):" prefixes of the cards were removed; a search for them in the file finds none in the table rows).
- References between rows resolve: first-review M-05 to M-02; M-07 to M-05; M-08 to M-14; M-09 to M-10; M-10 to M-01 and M-09; M-11 to M-12; M-16 to coverage gap NFR-013. The coverage note says "17 inactive, 8 covered, 1 gap" and lists 6+7+1+2+1 = 17, 7 + NFR-015 = 8, and NFR-013 = 1, so 26.
- Line-number conflicts: four spots are marked `(line differs between reviewers)`: first-review M-06, first-review M-08, row M-05 (PLAN:29 against PLAN:20), row M-13 (PLAN:31 against PLAN:40). The V1 and V3 claims about `archive_workspace.py` lines 44-67 (nine against eleven patterns) are kept side by side and cross-referenced between first-review M-08 and row M-14; neither is dropped. No two kept statements say opposite things about the same row.
- Typography: no em dash or en dash in `merged-output.md` or this file; the file has no leftover stub marker.
- Not checked here: whether each cited line still says what the card claims (the evidence validator does this); four plan line numbers in the base may have drifted (K5), unchanged by rule.
