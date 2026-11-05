# Evidence Validation Report (round 2; returned by evidence-validator, persisted on receipt)
**Timestamp**: 2026-11-04T15:42:30Z — Total 8, Verified 6, Dropped 0, Passed through 2 — **Suggested report status**: success
## Verified citations
:153, :120, :196, :219, :267, :326 of src/superclaude/hooks/scripts/block-bare-python.sh — all exact.
## Passed-through
7 trace-probe.out lines 1-8; 8 tier1-observation.md lines 16-22.
## Structural assertions
| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| A1 | no | — | — | calibrated 0.92; captured trace |
| A2 | skipped | — | — | input absent: diff_path |
| A3 | no | — | — | no timestamp line in the draft |
| A4 | no | — | — | hc0 decisions not_applicable |
| A5 | skipped | — | — | input absent: candidate-fixes.md |
| A6 | no | — | — | no reference-context cell |
| A7 | no | — | — | RUN-SITE resolved |
| A8 | no | — | — | not CI |
| A9 | skipped | — | — | no reference arm |
| A10 | no | — | — | capability-verdict n/a |
## Notes
Mechanism 2 also rests on endword lines 94-96 (skn cleared only when a word is open). Quoted "[[" variant observed in bash only (disclosed).
