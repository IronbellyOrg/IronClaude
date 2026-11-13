persona: refactorer
model_class: opus
model: claude-gw-tier1a

## Findings block

```findings-v2
{"id":"F1","severity":"MAJOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"The tasklist's byte-exact early-section text names `summary.md`, omits the Write-block sentence, and adds the 'does not apply' clause, so it no longer matches the agent files or test constants (which use `issue-summary.md`); executing it byte-for-byte would fail the pinned tests.","citations":[{"role":"plan","path":".dev/tasks/done/TASK-WF-fixTheScIssueWor-20261104-162205/TASK-WF-fixTheScIssueWor-20261104-162205.md","line_start":26,"line_end":26,"quote":"(`scout.md`, `accuracy-check.md`, `summary.md`, the reports under `analysis/`"},{"role":"plan","path":".dev/tasks/done/TASK-WF-fixTheScIssueWor-20261104-162205/TASK-WF-fixTheScIssueWor-20261104-162205.md","line_start":22,"line_end":22,"quote":"Exact early section (byte-identical in all three agent files"},{"role":"plan","path":"tests/skills/test_issue_worker_agents.py","line_start":228,"line_end":228,"quote":"`issue-summary.md`, the reports under `analysis/` such as "}]}
{"id":"F2","severity":"MINOR","blocking":false,"category":"unpassable-check","lens":"reflect-pre","claim":"Task 1 requires new tests written before edits with a recorded red run, but its list of required paragraph file names includes `summary.md` while the on-disk test requires `issue-summary.md`; the tasklist's own AC cannot be met by the tests that exist on disk today.","citations":[{"role":"plan","path":".dev/tasks/done/TASK-WF-fixTheScIssueWor-20261104-162205/TASK-WF-fixTheScIssueWor-20261104-162205.md","line_start":45,"line_end":45,"quote":"any of the files `scout.md`, `accuracy-check.md`, `summary.md`, `analysis/`"},{"role":"plan","path":"tests/skills/test_issue_worker_agents.py","line_start":253,"line_end":253,"quote":"issue-summary.md"}]}
{"id":"F3","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"The tasklist adds a SKILL.md spawn-rule paragraph the spec does not list; the tasklist justifies the addition inline and the line is present on disk, so this is an authorized expansion.","citations":[{"role":"spec","path":".dev/tasks/done/TASK-WF-fixTheScIssueWor-20261104-162205/source.md","line_start":1,"line_end":1,"quote":"Files: src/superclaude/agents/issue-worker-t1.md, issue-worker-t2.md, issue-worker-t3.md, tests/skills/test_issue_worker_agents.py"},{"role":"plan","path":".dev/tasks/done/TASK-WF-fixTheScIssueWor-20261104-162205/TASK-WF-fixTheScIssueWor-20261104-162205.md","line_start":20,"line_end":20,"quote":"(judged needed: the spawn prompt is the instruction nearest the worker's action"}]}
{"id":"F4","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"The early-section paragraph is byte-identical across three agent files and repeated in the test constants: five copies total, so any rename (as summary.md to issue-summary.md already did) must touch every copy. Inherited from the spec's design, not a tasklist defect.","citations":[{"role":"plan","path":".dev/tasks/done/TASK-WF-fixTheScIssueWor-20261104-162205/TASK-WF-fixTheScIssueWor-20261104-162205.md","line_start":22,"line_end":22,"quote":"byte-identical in all three agent files"},{"role":"spec","path":".dev/tasks/done/TASK-WF-fixTheScIssueWor-20261104-162205/source.md","line_start":1,"line_end":1,"quote":"add to each issue-worker-t*.md Rules section a rule"}]}
```

```yaml
calibration:
  per_finding:
    F1: 0.85
    F2: 0.75
    F3: 0.7
    F4: 0.6
```
