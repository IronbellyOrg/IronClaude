# Evidence Validation Report

**Report under validation**: REPORT.md.draft (this directory)
**Timestamp**: 2026-11-04T15:39:52Z
**Total citations**: 6 | **Verified**: 5 | **Dropped**: 0 | **Passed through (command, no reexec)**: 1
**Suggested report status**: success
**Provenance**: evidence-validator agent; persisted by the parent on receipt (condensed)

## Verified citations

| # | Location | Verdict |
|---|---|---|
| 1 | src/superclaude/cli/install_user_setup.py:175-177 | verified |
| 2 | src/superclaude/cli/user_settings_defaults.json:36 | verified |
| 3 | src/superclaude/cli/install_user_setup.py:297 | verified |
| 4 | src/superclaude/cli/install_user_setup.py:10 | verified |
| 5 | docs/getting-started/installation.md:398 | verified (sentence ends :399) |

Passed through: `timeout 120 uv run python /tmp/t14c-repro/repro.py`; quoted output matches tier1-observation.md:5-9.

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| A1 | no | — | — | calibrated 1.00; token observed in tier1-observation.md:7-8 |
| A2 | skipped | — | — | input absent: diff_path; tasklist has no pending rows |
| A3 | no | — | — | Date equals now_iso |
| A4 | no | — | — | pipeline_hardening_applicable=false, no verdict token |
| A5 | no | — | — | evidence class runtime_repro |
| A6 | no | — | — | no Reference-context rows |
| A7 | no | — | — | RUN-SITE concrete |
| A8 | no | — | — | same-shell, not CI |
| A9 | no | — | — | no reference expectation |
| A10 | no | — | — | usable-capture-routes: 1 |

## Notes (dispositions applied by the parent in step 3.25)

- producers.md and execution-locus.md cited :174 for the statement at :177: corrected.
- "is then installed" went beyond Evidence 4 (only the `wanted` selection was observed): wording changed to "selected for install" and a Grounding Gaps line added.
- Added explicit `pipeline_hardening_verdict: not_applicable`.
