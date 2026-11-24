# Evidence Validation Report

**Report under validation**: ./REPORT.md
**Timestamp**: 2026-11-23T20:58:12Z (supplied receipt time, not validation execution time)
**Total citations**: 21 (12 quote rows and 9 other citation occurrences)
**Verified**: 21
**Dropped**: 0
**Suggested report status**: success on citations alone. The plan verdict remains FAIL.
**Passed through (command, no reexec)**: 0. Commands are proposed future work, not observed runs.

## Verified citations

Independent evidence-validator re-Read actual source. All twelve inferred requirement quotes match verbatim substrings at `../../source.md:1`; each counted separately, not collapsed into one citation. Literal results match coverage-matrix row for row: INF-003 through INF-008 match tasks, the other six do not. Coverage remains 6/12, not revised upward.

| # | Citation | Verdict |
|---|---|---|
| 1 | INF-001 scope quote | verified |
| 2 | INF-002 historical-preservation quote | verified |
| 3 | INF-003 two-description/field quote | verified |
| 4 | INF-004 failing-then-passing quote | verified |
| 5 | INF-005 public captures quote | verified |
| 6 | INF-006 rejection quote | verified |
| 7 | INF-007 independent review quote | verified |
| 8 | INF-008 behavioral prohibitions quote | verified |
| 9 | INF-009 isolation quote | verified |
| 10 | INF-010 counters quote | verified |
| 11 | INF-011 prohibited actions quote, governed by preceding Do not | verified |
| 12 | INF-012 plan-only quote | verified |
| 13 | adversarial/merged-review.md, summary trace | verified, full trace exists |
| 14 | coverage-matrix.md, coverage receipt | verified, 4 tasks/0 parsed/12 inferred/6 matches |
| 15 | package plan:76-84 | verified, Task 4 and exact two quoted fragments |
| 16 | installed workflow template:15 | verified, stand-alone rule exact |
| 17 | installed executor qa.md:9-31 | verified, brief/diff and required-read citation rule |

| 18 | package plan:47-66, F2 | verified: sibling-symbol reference at 47, diagnostic-disposition at 54, validate-help-green at 66 |
| 19 | package plan:36-50, F3 | verified: normalization at 36/50 does not distinguish collapsing/removing |
| 20 | historical validate-lenses-help.txt:7-17 via five-parent relative path | verified: target intact at 7; other tokens split at 12-13/16-17 |
| 21 | package plan path, Recommendation R-001 | verified: file exists, Task 4 at 72-84 |

Full tail recovered without a new review; counts unchanged. Validator independently checked F1: Task 4 and Constraints do not name three commands or four earlier baseline/red paths, while Task 2 does. Template 15/qa 9 support the input boundary. No re-grading performed. Merged review and verdict agree on 1 Blocking, 5 Medium, 3 Notes; report matches, including unnumbered F4 Note. Convergence matches 0.9166666667.

## Dropped citations

None. Zero drops is the observed independent result, not an assumed zero. The report's plan verdict remains FAIL.

## Passed-through citations

None. Proposed future `uv run superclaude swarm ...` commands are recommendations, not command/output citations or executed checks. `allow_command_reexec: false` throughout.

## Notes

- Citation-only validation; assertions_path absent, structural assertions skipped rather than silently passed.
- All 21 occurrences were re-Read, including 12 quotes and 3 path-only references. Full validation exceeded the small-citation threshold because the validator counted related file links as citations too; no sampling/extrapolation was substituted.
- Literal-match rows independently cross-checked against coverage receipt, 6/12. No requirement rows dropped, so union denominator/density unchanged.
- Validator did not independently audit uncited calibration values (0.68/0.81), density, codegraph time or snapshot hash. Those are receipts supplied by calibration/coverage/snapshot artifacts, not new product proof. Main separately rechecked the 19-file hash unchanged.
- Source-width and codegraph claims in the intermediate merged card were outside the final report's own citation count. Validator did not claim checking them; source-width was directly Read by main/merger, and graph readiness has its own receipt.
- Product/docs paths appearing only inside cited plan text were not counted as separate REPORT citations. No upstream pattern flagged.
- Original receipt was truncated at row 18; bounded resend recovered rows 18-21 and limitations, with no new review or changed counts. Draft header finalized only after that recovery.
