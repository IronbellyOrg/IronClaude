# Task 1 spec-compliance review

## Earlier blocking findings

None supplied.

## Acceptance criteria

T1.AC1 met — docs/designs/issue-watcher.md:3 removes the obsolete phrase; an independent whole-file, case-insensitive search returned no matches. The saved no-match evidence is .dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/artifacts/t1-status-search.log:2-4.

T1.AC2 met — docs/designs/issue-watcher.md:3 names both PRs, states never run live, disabled shipping default and no installed schedule, and directs the owner to FU-1 in section 14.1 of the named setup document. Neither old task command remains on that line. The linked destination exists at docs/designs/issue-watcher-setup.md:578-587.

T1.AC3 met — .dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/artifacts/t1-status-search.log:5-7 records the required search and its empty result. Independent whole-file searches for the required alternatives and broader implementation/status language confirmed there are no remaining hits requiring correction.

T1.AC4 met — .dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/artifacts/t1-status-search.log:8 reports 935 lines before and after. Independently counted the start-snapshot blob and current document with `wc -l`: both are 935. The product diff contains exactly one removed status line and one replacement line.

## Findings

None.

## Self-audit

- Read the full design and independently searched the whole file for both the required phrases and broader implementation/status wording. Distinguished historical assumptions and descriptions of the design document itself from claims that the watcher remains unbuilt; preserved the required mocks-only scope wording.
- Verified every required status clause, the relative link's destination and FU-1 section heading, the saved empty-search evidence, and both line counts rather than accepting the implementer's report.
- Checked local merge history: 4c93b6c73 implements the poller in #447; ce6608258 carries its #448 follow-up. Checked the disabled source default and unchanged setup example. The compared product paths show only the one-line design replacement, with no source, setup, fixture, test or project configuration changes.
- Made no external service calls, live watcher runs, scheduler changes or product edits. Did not read other retry files. Did not run tests for this prose-only replacement; never-run-live and no-schedule status are reviewed against the task's stated baseline, not independently established by probing production state.
