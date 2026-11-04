# Coverage matrix (UC-1)

Spec: `.dev/tasks/to-do/TASK-WF-fixTheScIssueWor-20261104-162205/source.md` (1 line).
Tasklist: `.dev/tasks/to-do/TASK-WF-fixTheScIssueWor-20261104-162205/TASK-WF-fixTheScIssueWor-20261104-162205.md` (3 tasks).

Pass 1 (ID_REGEX `R-|REQ-|SPEC-|T-`): 0 parsed IDs. Pass 2 (inference): 5 rows.
parsed_count = 0, inferred_count = 5 → `coverage_degraded: parsed-sparse` (Step 1B.2b).

| Requirement | Source | Verbatim quote (source.md:1) | Matched tasks | Method |
|---|---|---|---|---|
| INF-001 | inferred | "add to each issue-worker-t*.md Rules section a rule that the files they write under .dev/issues/ are input files for the orchestrator's next tool calls (gh --body-file posts, /sc:recommend), not report files" | Task 2 | containment |
| INF-002 | inferred | "so the general harness note against writing report .md files does not apply to them" | Task 2 | containment |
| INF-003 | inferred | "and returning the content as text instead is a failure (E-WORKER-NO-OUTPUT)." | Task 2 | containment |
| INF-004 | inferred | "Add a regression test in tests/skills/test_issue_worker_agents.py that every issue-worker agent file carries that rule." | Task 1 | containment |
| INF-005 | inferred | "Files: src/superclaude/agents/issue-worker-t1.md, issue-worker-t2.md, issue-worker-t3.md, tests/skills/test_issue_worker_agents.py" | Task 1, Task 2 | containment |

coverage_pct (parsed-only): null (parsed_total = 0)
coverage_pct_union: 1.0000 (5/5)
unmapped_requirements: []
unmapped_requirements_union: []
S_dev_density: 0.00
S_scope (UC-1 task count): 3
S_domains: 2 (code/docs agent prompts + tests)
