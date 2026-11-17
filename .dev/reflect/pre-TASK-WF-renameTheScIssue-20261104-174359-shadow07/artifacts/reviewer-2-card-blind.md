
# Reviewer 2 card (qa, reflect-pre)

## Analysis

**Coverage matrix versus the spec.** The five inferred rows (INF-001 to INF-005) cover the spec's main requirements. Two spans have no row of their own:
- The developer and user guide rows. The spec lists them among the places the rename must reach. The plan resolves them as "no /sc:issue row exists, so no edit" (Task 4, plan:91), checked only by a recorded read. The matrix folds this into INF-001, so the one place the plan declines to apply the rename has no separate row. This is non-blocking. The guide hits are unrelated and Task 4 records the check.
- The spec's closing "Files: as listed in scope". The scope list is not a matrix row, so nothing checks that the plan's file list equals it.

**Acceptance criteria.**
- T1.AC3 (plan:51) says grep for `summary\.md` must print "only `issue-summary.md` occurrences". As literally written that is self-contradictory, because `issue-summary.md` contains the substring `summary.md`. The pattern matches every line, and "only" is satisfiable only through an unstated `grep -v issue-summary` or a `(^|[^-])summary\.md` pattern. Task 2 (plan:56) and Task 4 (plan:94) use the same phrasing. A reader cannot tell what a pass looks like.
- T1.AC2 (plan:50) says the template is "otherwise unchanged apart from the analysis-name wording". It names no verifier. A diff against `artifacts/pre/template-summary.md` would work, but the criterion does not say to run it.
- T1.AC4 (plan:52) is sound. `tests/skills/test_issue_protocol.py:137` globs `refs/*.md`, `templates/*.md` and `scripts/*.py`, and `:95` defines the path regex used for the inventory. So the two-way inventory does see `templates/issue-summary.md` through SKILL.md. No finding.
- T3.AC2 (plan:76) is the red-check, and it is weaker than it reads. It is an ad-hoc `uv run python` import from a test module, with "exit code recorded" and no stated expected value, so a pass is not defined. The pinned test `test_checks_flag_pre_fix_text` (tests/skills/test_issue_worker_agents.py:493-501) already does the same proof deterministically, so the ad-hoc step adds little. The red-check also compares only names, not paths.
- The spec asks that "no reference to the old `<D>/summary.md` path remains". The deterministic test scans only worker-instruction texts, `issue.md` and `templates/*.md`. The design doc is checked only by a one-off grep (Task 4), which is not a regression test. This is intentional, since the dated note must keep the old name, but the plan does not say so.

**Test spec versus the code on disk** (`tests/skills/test_issue_worker_agents.py:333-501`). All specified tests exist and pin what the plan demands:
- The probe set (`test_harness_regex_matches_probe`, :440) matches the plan's probe list, with extra cases added.
- `test_worker_written_names_avoid_harness_block` (:459) scans the three agents, SKILL.md, all refs and the `## Outputs` table rows. It asserts that the Outputs table yields names, and that `analysis/analyze-<scope>.md` is present in SKILL.md, `refs/claim.md` and the t1 and t2 agent files.
- `test_old_summary_path_is_gone` (:482) covers templates and also the whole `issue.md`, which is stronger than the plan. It checks that `templates/issue-summary.md` exists and `templates/summary.md` is absent.
- `test_checks_flag_pre_fix_text` (:493) asserts exact lists, which is stronger than the plan's "yields a name".
- `written_md_names` (:370) behaves as specified.
- I found no defect against the spec.

## Findings block

```findings-v2
{"id":"F1","severity":"MINOR","blocking":false,"category":"ambiguous-acceptance-criterion","lens":"reflect-pre","claim":"T1.AC3 literal grep for summary\\.md cannot print 'only issue-summary.md occurrences' because issue-summary.md contains the substring, so the criterion has no stated pass condition (same phrasing in T2 and T4 ACs).","citations":[{"role":"plan","path":".dev/tasks/done/TASK-WF-renameTheScIssue-20261104-174359/TASK-WF-renameTheScIssue-20261104-174359.md","line_start":51,"line_end":51,"quote":"`grep -rn 'summary\\.md' src/superclaude/skills/sc-issue-protocol` prints only `issue-summary.md` occurrences"}]}
{"id":"F2","severity":"MINOR","blocking":false,"category":"verifier-weaker-than-claimed","lens":"reflect-pre","claim":"The T3 red-check is an ad-hoc python import with no expected exit code and no stated pass value; it duplicates the pinned test_checks_flag_pre_fix_text and so adds little proof.","citations":[{"role":"plan","path":".dev/tasks/done/TASK-WF-renameTheScIssue-20261104-174359/TASK-WF-renameTheScIssue-20261104-174359.md","line_start":76,"line_end":76,"quote":"reports `summary.md` as a blocked name and `<D>/summary.md` as an old path, exit code recorded"},{"role":"repo","path":"tests/skills/test_issue_worker_agents.py","line_start":493,"line_end":501,"quote":"def test_checks_flag_pre_fix_text(tmp_path):"}]}
{"id":"F3","severity":"MINOR","blocking":false,"category":"unmeasurable-criterion","lens":"reflect-pre","claim":"T1.AC2 asserts the template is 'otherwise unchanged' but names no verifier such as a diff against the saved pre-fix copy.","citations":[{"role":"plan","path":".dev/tasks/done/TASK-WF-renameTheScIssue-20261104-174359/TASK-WF-renameTheScIssue-20261104-174359.md","line_start":50,"line_end":50,"quote":"the template content is otherwise unchanged apart from the analysis-name wording"}]}
{"id":"F4","severity":"MINOR","blocking":false,"category":"coverage-gap","lens":"reflect-pre","claim":"The spec's requirement that no old <D>/summary.md reference remains is pinned deterministically only for worker texts and templates; the design doc is checked by one-off grep, and the matrix has no separate row for the guide-row requirement that the plan resolves as no-edit.","citations":[{"role":"spec","path":".dev/tasks/done/TASK-WF-renameTheScIssue-20261104-174359/source.md","line_start":1,"line_end":1,"quote":"the design doc, and the developer and user guide rows"},{"role":"plan","path":".dev/tasks/done/TASK-WF-renameTheScIssue-20261104-174359/TASK-WF-renameTheScIssue-20261104-174359.md","line_start":91,"line_end":91,"quote":"so neither guide is edited; record this check."}]}
```

reviewer_model_self_report: claude-gw-tier1b[1m]
