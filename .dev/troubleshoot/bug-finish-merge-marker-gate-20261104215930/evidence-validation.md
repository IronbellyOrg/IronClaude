# Evidence Validation Report
(persisted on receipt from the evidence-validator agent; condensed)
**Total citations**: 8 | **Verified**: 8 | **Dropped**: 0 | **Passed through**: 0
**Suggested report status**: success

## Verified citations
finish-merge.sh:208, :246, :249; conflict-mechanical.md:76; probe-finish.out:2, :4, :9; source.md:817-818 — all verified at the cited lines.

## Dropped citations
None.

## Structural assertions
| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| A1 | no | — | — | no enum asserted as observed; calibrated 1.00 |
| A2 | skipped | — | — | input absent: diff_path (fix diff not yet written) |
| A3 | no | — | — | no timestamp lines in the draft |
| A4 | no | — | — | no pipeline_hardening_verdict field |
| A5 | no (clause 1 skipped) | — | — | evidence class runtime_repro; candidate-fixes.md absent (Tier 1) |
| A6 | no | — | — | no Reference-context value |
| A7 | no | — | — | RUN-SITE concrete; zero producer rows |
| A8 | no | — | — | OBSERVE-VIA same-shell; not a CI job |
| A9 | no | — | — | no reference literal |
| A10 | no | — | — | usable-capture-routes 1 |

## Notes
- probe-finish.out:4 "(A1 case passed)" means the gate passed falsely; wording clarified in the final report.
