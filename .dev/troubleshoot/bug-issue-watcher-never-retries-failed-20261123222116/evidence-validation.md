# Evidence Validation Report
(persisted by the orchestrator from the evidence-validator agent's returned report; timestamp 2026-11-23T22:26:58Z)

Report under validation: REPORT.md.draft. Total citations 12 (Evidence items 1-8), verified 12, dropped 0, command claim passed through 1 (`grep -rn "first_run(" src tests`, not re-executed; the validator verified the `src` half independently). Suggested report status: partial.

## Structural assertions
| id | fired | flag | consequence |
|---|---|---|---|
| A1 | no | - | no categorical run value claimed; observation_paths empty |
| A2 | skipped | - | input absent: diff_path |
| A3 | no | - | draft Date within mtime + 5 min |
| A4 | yes (conservative) | verdict_not_in_contract | partial; Pipeline Hardening Closure says "HC0 not run" with no verdict token |
| A5 | yes | consensus_on_unobserved | partial; consensus rests on static evidence only (all three calibrations: static_defect / source_static) |
| A6 | skipped | - | no probe rows |
| A7 | no | - | one producer row; RUN-SITE resolved |
| A8 | no | - | no failing CI arm |
| A9 | skipped | - | no reference-arm value |
| A10 | no | - | no blocked capability verdict |

Notes: status merged monotonically to partial; no citation dropped. Unverified by the validator: "test files only" half of the call-site grep; the `world.config` no-report characterisation of test_dispatch.py:421-426.
