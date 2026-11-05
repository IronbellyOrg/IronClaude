# Evidence Validation Report (returned by evidence-validator, persisted on receipt)

**Report under validation**: REPORT.md.draft
**Timestamp**: 2026-11-04T15:20:40Z
**Total citations**: 8 (5 file:line, 3 command+output) — Verified 5, Dropped 0, Passed through 3
**Suggested report status**: success

## Verified citations
| # | Location | Verdict |
|---|---|---|
| 1 | src/superclaude/hooks/scripts/block-bare-python.sh:206 | verified (ansi branch of qchar) |
| 2a | src/superclaude/hooks/scripts/block-bare-python.sh:98 | verified |
| 2b | src/superclaude/hooks/scripts/block-bare-python.sh:101 | verified; argopt 234-239 short options only |
| 3 | src/superclaude/hooks/scripts/block-bare-python.sh:191 | verified; :190 guarded by need[o] |
| 5a | src/superclaude/hooks/scripts/block-bare-python.sh:275 | verified |

## Passed-through (no reexec)
4 trace-probe.out lines 2,4,6,7; 5b probe-baseline.out (symptom rows 2-4, 7-12 exit 0; =~ row 16 exit 2); 6 tier1-observation.md lines 41,42,45.

## Structural assertions
| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| A1 | no | — | — | tokens in trace-probe.out with provenance; confidence 0.92 |
| A2 | skipped | — | — | input absent: diff_path |
| A3 | no | — | — | Date before mtime, not T00:00:00Z |
| A4 | no | — | — | closure prose maps to not_applicable (hc0-boundary-scan.md) |
| A5 | skipped | — | — | input absent: candidate-fixes.md; calibration clause evaluated: no |
| A6 | no | — | — | no reference-context cell; D1 first_instrumented_run true |
| A7 | no | — | — | RUN-SITE resolved |
| A8 | no | — | — | not a CI job |
| A9 | skipped | — | — | no reference-arm capture |
| A10 | no | — | — | capability-verdict n/a |

## Notes
Precision: Evidence 5 should say "symptom rows" (control rows 5, 13, 14, 17 exit 2). Minor outside the draft: calibration note's comment lines are 10 and 11, not 10 and 12.
