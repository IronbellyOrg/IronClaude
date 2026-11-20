# Reflect report (pre-execution): TASK-WF-implementDocsDes-20261120-005507

- Mode: pre (UC-1). Spec: `.dev/tasks/to-do/TASK-WF-implementDocsDes-20261120-005507/source.md`. Plan: `.dev/tasks/to-do/TASK-WF-implementDocsDes-20261120-005507/TASK-WF-implementDocsDes-20261120-005507.md` (sha256 d4c233ed...).
- Tier reached: 2. Why: the source has no requirement ids (parsed 0, inferred 5), so `coverage_degraded: parsed-sparse` forbids a Tier 1 stop.
- Reviewers: three `reflect-reviewer` agents (sonnet analyzer, haiku qa, opus refactorer). All three verdict: **not-ready**.
- Status: **partial**. Stages NOT run (loud): blind calibration of the three cards, the `sc-adversarial-protocol` merge, and the evidence-validator gate. The findings below are a hand-deduplicated union of the three cards, not a calibrated merge; no citation was independently re-Read by a validator. Treat the severity labels as reviewer-stated.
- Coverage (inferred rows INF-001 to INF-005): all five map to tasks (union coverage 1.0); the plan's defects are in execution detail, not missing requirements.

## Blocking findings (union, with who found them)

| # | Where | Finding | Found by |
|---|---|---|---|
| B1 | Task 8 | `plugins/superclaude/commands/workflow.md` must stay byte-identical to the src command (`tests/commands/test_workflow_command.py:102-103`); the plan edits only the src file and never runs `tests/commands`. | all three |
| B2 | Task 2 | `tests/cli/reflect/test_shadow_skill_contract.py` has two tests that compare the reflect SKILL.md with git HEAD and allow edits only in sections 3.1, 4.3a, 5.4, 9.2; editing 9.1 and 9.4 fails them. The plan names only the heading pin. | analyzer |
| B3 | Task 4 | `archive --superseded-by <new-id>` records the new id before `place` picks it; a collision suffix makes the archived contract name an id that never exists. | all three |
| B4 | Tasks 4, 5 | The repaired copy sits in a `/tmp` directory with the old slug, so it fails the Wave 3 rule that `slug` equals its directory name. | qa, refactorer |
| B5 | Task 13 | The acceptance grep is wrong: `TASK-WF-blockerStage4-20261116-030206` has no `return-contract.yaml` at all, and the replacement `...20261117-170451` and `specScRecommendR` are what the grep returns. | all three |
| B6 | Task 6 | The workflow skill has no Task/Agent tool and bans "Task fan-out" (`SKILL.md:4,107`), yet the reviser and re-review are sub-agents. | refactorer |
| B7 | Wave 5 / Tasks 6, 7 | Nothing says Wave 5 writes the contract into the final placed package, or that `report_path` and the printed plan path name it (it could write into an archived package). | refactorer |
| B8 | Task 4 | No subcommand writes `superseded_by`, `review_verdict`, `open_blockers`; Tasks 9 and 10 read them. | refactorer |
| B9 | Task 4 | `place` drops the design's `## Revision N` section in `source.md` and the `artifacts/` audit trail (diff, prior findings, old-plan copy, revision log). | analyzer (Medium), refactorer |
| B10 | Tasks 4, 13 | `--superseded-by` is required, but six of the seven contracts name no replacement id; the move cannot run as written. | analyzer, refactorer |
| B11 | Task 2 | `panel_lint` accepting only 1.9.0 makes `scripts/reflect_shadow_exit.py` fail its 14 recorded 1.8.0 shadow runs; the plan does not choose between accepting both versions or exempting check L1. | refactorer |
| B12 | Task 6 | Plugin skill mirror: the plan mirrors the new ref and script only "if the mirror carries" them, but the mirror has no `scripts/`, so its own `diff -rq` criterion fails. | analyzer, refactorer |

## Medium and Notes (follow-up candidates, never block)

- `restore` does not undo the `SUPERSEDED` line or the minimal contract that `archive` wrote (analyzer, refactorer).
- `remediate.py` must be stdlib-only and must not re-serialize archived YAML (installed skills run under `uv run --no-project`) (refactorer).
- Task 7 rewrites text pinned by `tests/commands/test_workflow_command.py:151,158` (analyzer).
- Task 9 should also add `E-MANAGED-REVIEW-FAIL` to the STOP list in `sc-implement-protocol/refs/qa.md:285` (analyzer).
- Reflect `SKILL.md:311` ("contract 1.8.0 is unchanged") is missing from Task 1's list; panel mapping of `medium` and `note` is undefined; `route()` order of `forced` and `regenerated_already` is undefined; Task 10 also depends on Task 7; where `--finding-counts` come from on re-review and `--revise` is unstated; `argument-hint` lines need the new flags.

## Checked and fine

The routing rule and thresholds match design section 3; `rename_noreplace` is loadable by file path; the workflow contract "1.1" pins are all kept; every 1.8.0 consumer in src, tests, scripts and plugins is named in Task 1 or 2 (except line 311); no file references the seven migrated package ids.

## Verdict

not-ready (three of three reviewers). 12 blocking findings, all with a concrete fix. Per the workflow rule this review is advisory: the plan was not edited.
