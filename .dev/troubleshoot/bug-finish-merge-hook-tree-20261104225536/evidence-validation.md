# Evidence Validation Report

**Report under validation**: .dev/troubleshoot/bug-finish-merge-hook-tree-20261104225536/REPORT.md.draft
**Validator**: evidence-validator (persisted by the parent on receipt; condensed)
**Total citations**: 11
**Verified**: 10
**Dropped**: 0
**Passed through (command, no reexec)**: 1 (the test "fails on 62121669" claim; corroborated by probe-c4.out:2-5 and the parent's negative-witness run in audit.log)
**Suggested report status**: success

## Verified citations
| # | Location | Verdict |
|---|---|---|
| 1-3 | probe-c4.out:2 (`exit: 0`), :3-4 (trees differ), :5 (`changed by hook`) | verified |
| 4 | refs/conflict-mechanical.md:124 tree_dirty row | verified (fix-side documentation, not defect evidence) |
| 5-6 | finish-merge.sh:274 VALIDATED_TREE; :296-298 HEAD^{tree} comparison and fail tree_dirty | verified |
| 7-8 | one `git commit -F` (:278), no --no-verify; write-tree failure -> tree_dirty before the commit | verified |
| 9-10 | conflict-mechanical.md:114 step 9 text; :294 merge_preflight_dirty row | verified |
| 11 | test_conflict_scripts.py:989, :1015 | verified |

## Dropped citations
None.

## Notes
- The pre-fix Summary rests on the probe output (the working copy holds the fix).
- Line numbers as of validation; later CI-driven edits (marker_widths) shifted lines in finish-merge.sh by about 15.
