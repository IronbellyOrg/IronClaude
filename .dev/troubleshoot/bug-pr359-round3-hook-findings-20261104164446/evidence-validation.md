# Evidence Validation Report (round 3; returned by evidence-validator, persisted on receipt)
**Timestamp**: 2026-11-04T16:52:41Z — Total 8, Verified 6, Dropped 0, Passed through 2 — **Suggested report status**: success
## Verified citations
:218, :219, :130, :206, :340, :336 of src/superclaude/hooks/scripts/block-bare-python.sh — exact; ordering :218 -> :219 -> :130 holds.
## Passed-through
6 trace-probe.out; 7 tier1-observation.md lines 14-24.
## Structural assertions
| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| A1 | no | — | — | tokens in trace-probe.out with provenance; 0.92 |
| A2 | skipped | — | — | input absent: diff_path |
| A3 | no | — | — | no timestamp line in draft |
| A4 | no | — | — | hc0 decisions not_applicable |
| A5 | no | — | — | first clause skipped (candidate-fixes.md absent); second clause no |
| A6 | no | — | — | reference literals `2` |
| A7 | no | — | — | RUN-SITE concrete |
| A8 | no | — | — | not CI |
| A9 | no | — | — | reference literals match captured hook_exit=2 |
| A10 | no | — | — | capability-verdict n/a |
