# Coverage matrix (UC-1, Step 1B.0)

Spec: `.dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/source.md`
Tasklist: `.dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/TASK-WF-rollOutTheIssueW-20261109-000305.md` (5 tasks, 4 phases)

## Pass 1 (ID_REGEX `\b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b`)

parsed_count: 0 (the spec labels follow-ups as FU-1 / FU-2, which the regex does not match).

## Pass 2 (inferred rows)

| id | quote (verbatim) | citation | matched task | match_method | source |
|---|---|---|---|---|---|
| INF-001 | "replace the _assumed_shape fixtures with captured real gh and Orca output after the owner-run live test (FU-1)" | source.md:7 | Task 5 | containment | inferred |
| INF-002 | "fix the stale status line ... in docs/designs/issue-watcher.md" | source.md:7 | Task 1 | containment | inferred |
| INF-003 | "fix ... the 59-name reason table in docs/designs/issue-watcher.md" | source.md:7 | Task 2 | containment | inferred |
| INF-004 | "prepare the shadow-run, lock, restart and cron steps (FU-2) as owner-run checklist items" | source.md:7 | Task 4 | containment | inferred |
| INF-005 | "keep enabled false until the owner flips it" | source.md:7 | Constraints (plan line 20); Task 4 AC 3 | containment | inferred |
| INF-006 | "is written up as `docs/designs/issue-watcher-live-test.md` (FU-1)" | source.md:22 | owner-run (plan line 28); Task 5 precondition | containment | inferred |
| INF-007 | "then the six-field cron entry `0 */5 * * * *` (FU-2)" | source.md:22 | Task 4 (8.7) | containment | inferred |
| INF-008 | "Watcher test suite; must still pass after the fixture swap" | source.md:32 | Task 5 AC 3 | containment | inferred |
| INF-009 | "a reviewed 24-hour shadow run, the two-process lock test and the state-directory restart test, after which `enabled` becomes `true`" | source.md:22 | Task 4 (checklist) + owner-run lines 30-33 | containment | inferred |
| INF-010 | "FU-2 also covers a persisted `state_dir` if `$HOME` is not persistent" | source.md:42 | Task 4 (8.7) | containment | inferred |

inferred_count: 10, parsed_count: 0, union: 10, unmapped_union: 0
coverage_pct: null (parsed-only, no parsed rows)
coverage_pct_union: 1.00
S_dev_density (union): 0.00
coverage_degraded: parsed-sparse (inferred 10 > parsed 0; Step 1B.2b forbids the Tier-1 stop)
