outcome: applied-not-effective

path taken: run. The one `repo.update` call (upstream null) was sent once and reported success, and the stored upstream now reads null. The projectId in `orca worktree current --json` still reads github:superclaude-org/superclaude_framework, both right after the call (2026-11-26T12:13:09Z) and about 27 seconds later (2026-11-26T12:13:36Z). By the outcome rule the override did not take effect on the project id. Raw readings are in ./artifacts/t2-after.txt: upstream null, projectId github:superclaude-org/superclaude_framework, worktrees preserved: yes (32 of 32).

What this does not show (unverified): whether the project id is only recomputed when Orca restarts or when its worktree records are rebuilt. The agent did not restart Orca and did not open the repo's Settings panel, so the id may still change after either, and the stored null may also be replaced when the Settings panel is opened (the panel asks GitHub again for a repo with a GitHub avatar icon). Durability across a restart and after opening that panel is unverified.

Owner checks (the two checks the owner should make): restart Orca and open the repo's Settings panel, then read the two states again with `orca repo show --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json` and `orca worktree current --json`.

Orca was not restarted and the repo's Settings panel was not opened.

Rollback: send the same `repo.update` call with `updates: { upstream: { owner: 'SuperClaude-Org', repo: 'SuperClaude_Framework' } }`. The previous record is kept in `~/.config/orca/profiles/local-default/orca-data.json.sqlite-export.1.json`.

The decided fallback is to change Orca (so the fork's own git remote wins over the stored upstream). The second state change that also replaces the repo icon (step B of the REPORT.md Proposed Fix) is not run and needs the owner's approval.

The tracked source files are unchanged by this task.
