ebf8633471ff532365c6e1f73aed2f2ec554f729
## family=dev-tasks-staging (F1.1)
defect form: the report describes the staging step as a plain `git add .dev/tasks` and calls the superseded package "left unstaged" without stating who decided the exclusion or how it was done.
search: grep -n -F -e "git add .dev/tasks" -e "left unstaged" -- .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/p0-static-report.md
before:
.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/p0-static-report.md:17:| AC-C4 | PASS: on the index after `git add .dev/tasks`, the check prints nothing (empty file); nothing under `.claude/` is staged | `./artifacts/ac-c4-index.txt` |
.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/p0-static-report.md:33:- `.dev/tasks`: this package, ... The superseded package `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/` is not part of this commit and is left unstaged.
coupled sites: none outside the report. What actually ran (shell history of this run): `git add .dev/tasks` was run twice (once before the AC-C4 check, once after the report was written), each time followed at once by `git restore --staged .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950`. That restore is an explicit constraint of the coordinator's dispatch brief for this run ("Right after that add, run git restore --staged .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950 so the superseded package stays unstaged"; "Do not edit, delete, move or stage the superseded package"). Staging that package, the reviewer's first fix option, would break that constraint, so the fix takes the reviewer's second option: record the exclusion as the coordinator's decision and describe the staging step exactly.
after:
after: 17:| AC-C4 | PASS: on the index after `git add .dev/tasks` and the coordinator-directed `git restore --staged` of the superseded package (see the commit list below), the check prints nothing (e
after: 33:- `.dev/tasks`: this package, `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/` (moved to `.dev/tasks/done/` when the archive runs), with its `progress.md` and `artifacts/`. Stagi
