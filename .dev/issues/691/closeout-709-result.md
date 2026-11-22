```yaml
closeout:
  pr: 709
  status: partial
  verdict: MERGED
  merged_by: ironbelly
  merge_commit: 5e48b98
  match: same
  pr_links_issue: refs
  issue:
    number: 691
    status: settled
    detail: left_open
    note: posted
    handback: remaining
    remaining_file: /tmp/sc-closeout-IronbellyOrg__IronClaude__709.Tudab4/done-verdict.md
    remaining: ["Part B: a live claim leaves the file in place (no pull request yet)"]
    handback_text: "The issue is not done and stays open with one note of what remains. The orchestrator takes the rest from here; by hand, run `/sc:issue --plan 691` and start a worker on what remains."
  entry:
    key: IronbellyOrg__IronClaude__691
    status: already_final
    detail: issue_open
  task:
    id: null
    status: escalated
    detail: no_orca_run
    dispatch: null
  escalations: ["task: No Orca Run is bound to this session, so the worker's task was not looked at. Settle it from the coordinator's session."]
  stop: null
```

Unusual:
- The task (task_a18573aefd1e) for dispatch ctx_fd07c38a1446 was NOT set to completed: settle.sh task printed `TASK escalated why=no_orca_run` (no Orca Run bound to this session). Not retried, because it is not a usage mistake. A session that holds the Run must settle it.
- The entry item was `already_final how=issue_open`, so the report command was not run (the issue stayed open).
- The evidence step printed truncated=yes (PR 514 file list cut); no verdict depended on the cut part.
- One marked note was posted on issue 691 by this run. Nothing else was written; git status shows only the pre-existing untracked .dev/reflect/pre-planIssue691Part-20261120204445/.
- The temporary directory /tmp/sc-closeout-IronbellyOrg__IronClaude__709.Tudab4 was left in place (it holds the verdict file the hand-back points to).
