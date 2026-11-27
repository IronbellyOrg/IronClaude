# Calibration of reviewer-1 card (blind calibrator, opus alias)

Calibrated C = 0.82 (Citation grounding 0.85, Coverage completeness 0.85, Deviation-classification clarity 0.75, Risk surface coverage 0.90, Recommendation actionability 0.75). Below the 0.85 floor. The card carries no self-reported confidence.

Rows 1 to 4 (all graded Blocking) verified TRUE by the calibrator:
- Row 1: `tests/recommend/test_routing_refresh.py:101-107` and `:495-496` resolve a `-protocol` activation to `skills/<name>/SKILL.md` and assert it exists; Task 19 (plan 232, depends only on Task 3 at 230) sets S23 to `sc:git-protocol`; Task 20 creates that file and depends on Task 19 (plan 240). Fixture today: `routing_refresh_cases.json:325` `{"sc:git": "self-contained"}`.
- Row 2: plan 29 versus plan 60, 172, 193, 334; implement `SKILL.md:106`, `refs/qa.md:52,61`; design 319.
- Row 3: plan 292 says "Delete", plan 295 checks `git ls-files`; `git ls-files` lists the index (the 21-file count is UNVERIFIED).
- Row 4: design 290-291, 355; REQ:551, 576, 580; plan 149, 156.
Rows 5, 7 to 13, 15 (git CLI claim UNVERIFIED), 16: true. Row 6: true, but citation DESIGN:134 is wrong (the text is at DESIGN:333 and 523). Row 14: partly false (DESIGN:192 does list `hooks_path`).

Other failed citations: summary count "Regression 2 (rows 1 and 3)" does not match the table (row 5 is also labelled Regression). UNVERIFIED by Read alone: row 3 file count and tracking; row 10 branch-deletion hits in `tests/worktree_cleanup/*`, `tests/hooks/test_launch_level_guard.py`, `scripts/worktree_cleanup_PROVENANCE.md`; row 12 whether `origin/integration` resolves; row 15 which git verbs accept `--ignore-submodules`; that FR-024 to FR-029, FR-083 to FR-089, FR-119 have no definition.
