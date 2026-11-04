# T1 reflection card (UC-1, pre-execution, check round 2)

- Spec: `.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md` (476 lines, unchanged since round 1)
- Tasklist: `.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md` (version 2: 6 phases, 17 tasks), revised after round 1 (`.dev/reflect/pre-TASK-WF-scIssueCommand-20261104-064713-20261104070955/REPORT.md`, merged verdict FAIL with blocking F-01 ordering and F-02 token handling)
- Card author: inline orchestrator

## Coverage section

- Pass 1: 0 parsed IDs. Pass 2: the same 67 quote-pinned rows as round 1 (spec unchanged); 0 dropped.
- Containment match on the revised plan: 60 of 67; `coverage_pct_union = 0.8955`; `S_dev_density = 0.1045`; `coverage_degraded: parsed-sparse` (Tier-1 stop forbidden).
- Semantic read of the 7 string-unmapped rows:
  - INF-013 (source.md:215, labels never created): covered by plan Task 5 create.md bullet ("never created (B7)").
  - INF-020 (source.md:314, one manual smoke claim against a test task): covered by Task 16 (ClickUp smoke claim); matcher miss after the task was reworded.
  - INF-054 (source.md:408, PR via /sc:pr-submit): authorized exclusion in Constraints.
  - INF-058, INF-059, INF-062 (source.md:468, 469, 472: AC 2, 3, 6): recorded by Task 17 as run or pending with exact commands; not executed without user approval.
  - INF-061 (source.md:471, AC 5 skipped comment): the no-token path is executed by Task 2; the comment wording is pending in Task 17.

## Deviation / risk section

How the revision addresses each round 1 finding:

- F-01 (blocking, ordering): the suite/lint/sync/staging task is now Task 14, depending on Task 13 only; the smoke checks are Tasks 15 and 16 after it, with truthful run/unavailable/pending outcomes instead of "reported as blocked"; Task 15 tells the executor to stop and resume in a new session; each smoke task stages its artifact; Task 16 re-runs tests, sync and lint after any fixture or script change.
- F-02 (blocking, security): Constraints add a secrets rule; Task 16 never asks for or inlines the token, needs the user to pre-export it, compares key paths only and never copies live values; Task 2's no-token check uses `env -u CLICKUP_API_TOKEN -u CLICKUP_WORKSPACE_ID` and every test clears both variables.
- F-03: new Task 17 records section 20 items 1-9 as run or pending; item 4 (stops before any write) is run.
- F-04: Task 7 adds the fork-safety scan (`--repo` on every `gh issue|pr|label` line; no `{owner}/{repo}`), Task 3's test adds it for worker bodies.
- F-05: Task 5 claim.md carries `git fetch origin` and `git log --since`; Task 3 body and test carry the fetch-only rule.
- F-06: Task 11 uses `git diff -U0 -- <guide>` with hunks inside 4.1-4.4.
- F-07: Task 10 states the ASCII and live-reference rules.
- F-09: all five refs carry the spawn rule; Task 7 checks every ref.
- F-10: Task 15 names external evidence sources and rejects self-report.
- F-11: Task 7 reads source command files only, noted as a deliberate narrowing.
- F-12: Task 13 compares against `origin/master` after `git fetch origin`.
- F-13: Constraints allow `./artifacts/`, `.dev/issues/smoke/` and the temporary worktree; Task 14 removes the worktree.
- F-15: claim.md adds `--limit 200` to the merged-PR query and records truncation.
- F-16: Task 2 documents the first page and invalid `CLICKUP_MAX_PAGES` behaviour and tests both.
- F-17: Task 7's scan skips `__pycache__` and non-UTF-8 files; Task 13 uses `grep -rIn`.
- F-18: one line-count rule (`len(text.splitlines())`) in Task 6 and Task 7.

Remaining risks:

- R-1: Task 17 item 4 runs `/sc:issue --claim` against a third-party URL (`octocat/Hello-World`); it depends on Wave 0 stopping before any `gh` call, which is what the spec orders (source.md:142-144) but is only as safe as the implemented SKILL.md.
- R-2: Task 15 and Task 16 may legitimately end pending; the plan's Goal now says so.

## Structural section

- 6 phases, 17 tasks numbered contiguously; every `Depends on` names a lower task; no checkbox or numbered lines; no absolute or to-do-prefixed paths.

## Self-reported confidence

0.85 (not used by the rubric).
