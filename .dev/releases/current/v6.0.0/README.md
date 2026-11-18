# v6.0.0 release records

These files record the IronClaude 6.0.0 cleanup and release, run by the `ic6-orchestrator` session for Clay (GitHub `clayphi`). The plan is IronClaude issue 571. They live on branch `clayphi/release-6.0.0` and are committed and pushed after every merge and every wave, so nothing is lost if a worktree goes away (the 5.0.0 records were lost that way, see `../v5.0.0/README.md`).

| File or folder | What it holds |
|---|---|
| `RELEASE-READINESS.md` | Baseline, every pull request with its state and link, waves, dependencies, finished worktrees, and the gate results (G1 to G9) once the release PR is green. |
| `DECISIONS.md` | Each decision, who made it and when. |
| `PROCESS-LOG.md` | One entry per step the orchestrator takes, with times, what went well, what got in the way, and what should change. Also the "Out of scope, for later" list. |
| `RETROSPECTIVE.md` | Written after the tag: what we did, what worked, a draft release template and workflow, and proposed changes to the release procedure and skills. Proposals only. |
| `prompts/` | The prompt file each agent was given, one per pull request. |
| `launches/` | The JSON reply of each `orca worktree create`, which holds the agent's terminal handle. |
