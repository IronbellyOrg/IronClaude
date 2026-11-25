# Wave 1.5 Branch A (release-doc lookup), persisted by the parent on receipt

Returned by troubleshoot-analyst (lens: documentation branch A). Line numbers inside it come from Grep output and were not re-read by the worker; unverified until Wave 5 validation.

```json
{
  "release_slug": "v5.0.0 (current)",
  "artifact_paths": [
    "/home/coder/workspaces/IronClaude/.dev/releases/current/v5.0.0/post-release/scan/DE2-claude-surface.md",
    "/home/coder/workspaces/IronClaude/.dev/releases/current/v5.0.0/post-release/CONSOLIDATED-PLAN.md"
  ],
  "summary": "No PRD, TDD, spec or roadmap in .dev/releases/current/ or complete/ scopes ccsession list_sessions or session-list performance. The only v5.0.0 hits are post-release documentation scans. DE2-claude-surface.md line 136 records `--ask [<hint>]` behaviour (prints the list and question on the terminal, exit 1 on timeout, exit 130 on Ctrl+C). CONSOLIDATED-PLAN.md line 62 lists the `ccsession-lists` surface (--list, --here, --here --all, --rm, --ask). These constrain only the CLI contract (exit codes, stdout/stderr split, flag set), not speed, so a fix to the listing cost must keep that contract.",
  "confidence": 0.7
}
```

Repo task records returned with it (data, not release docs):

- /home/coder/workspaces/IronClaude/.dev/issues/315/accuracy-check.md lines 16-19: plain `ccsession` never asks by itself; `--ask` is the only listing path on the launch route for Orca and Coder; ccsession-orca defaults CCSESSION_ASK_TIMEOUT to 30 seconds.
- /home/coder/workspaces/IronClaude/.dev/tasks/done/TASK-WF-fixIssue389Ironb-20261105-174606/TASK-WF-fixIssue389Ironb-20261105-174606.md line 21: output of `--ask`, `--auto-name`, `--list`, `--rm` and captured `models.py` prints must stay on standard output because the shell captures them (a listing change must not move streams).
- /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-WF-fixGitHubIssue31-20261105-031410/TASK-WF-fixGitHubIssue31-20261105-031410.md lines 34, 59, 61, 107: `--ask` contract (30 s default limit, exit 1 on timeout, exit 3 for oversized/tab/multi-line input, `*` still lists); whether that task finished is unverified.
- Worker limitation: older checkout line numbers appear in those records.
