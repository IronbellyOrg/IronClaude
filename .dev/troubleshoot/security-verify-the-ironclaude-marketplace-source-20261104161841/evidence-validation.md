# Evidence Validation Report

**Report under validation**: REPORT.md.draft
**Timestamp**: 2026-11-04T16:31:01Z
**Total citations**: 4 | **Verified**: 2 | **Dropped**: 0 | **Passed through**: 2
**Suggested report status**: success
**Provenance**: evidence-validator agent; persisted by the parent on receipt (condensed)

## Verified citations

| # | Location | Verdict |
|---|---|---|
| 1 | src/superclaude/cli/install_user_setup.py:332 (+ :336-337) | verified |
| 2 | src/superclaude/cli/install_user_setup.py:371 (+ :372) | verified |

Passed through: repro (tier1-observation.md:6-11) and real-CLI probe (tier1-observation.md:22-25; behaviour-definitions.md row 2) both match.

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| A1 | no | — | — | no enum token; max calibrated 0.92 |
| A2 | skipped | — | — | input absent: diff_path |
| A3 | no | — | — | Date within mtime + 5 min |
| A4 | no | — | — | not_applicable is in the contract set |
| A5 | no | — | — | consensus backed by two runtime_repro cards |
| A6 | no | — | — | no Reference-context rows |
| A7 | no | — | — | RUN-SITE concrete |
| A8 | no | — | — | same-shell, not CI |
| A9 | no | — | — | no reference-arm comparison |
| A10 | no | — | — | usable-capture-routes: 1 |

## Notes (dispositions applied in step 3.25)

- Evidence 4 covers a foreign directory source only: Diagnosis qualified.
- Update-failure path observed only for add: Grounding Gaps line added.
