# Scout report

- Mode: claim
- Repo: IronbellyOrg/IronClaude
- Written by: issue-worker-t3

## Claim

- Issue: #450
- url: https://github.com/IronbellyOrg/IronClaude/issues/450
- is_pull_request: false
- State: OPEN
- Assignees: ironbelly
- Current login: ironbelly
- Earlier claim comment ID: none
- Earlier accuracy-check comment ID: none
- Created at: 2026-11-08T07:03:49Z

### Merged pull requests since creation

- Result truncated at the 200 limit: no (15 results, including eight before creation on the same calendar date).
- Changed-file locations below are abbreviated; full returned paths are in `/home/coder/.claude/projects/-home-coder-workspaces-IronClaude/1779a921-dc86-44c8-867c-d5e117eb8e31/tool-results/be2muad7g.txt`. The `gh` files field returned 100 files for #458, so that PR's file list may itself be incomplete.

| PR | Title | Merged at | Changed files |
|---|---|---|---|
| #459 | docs(designs): describe the tab-title shim check in the claim pipeline design | 2026-11-08T23:46:23Z | docs/designs/sc-issue-claim-pipeline-flag.md |
| #458 | fix(mcp): accept the LiteLLM proxy tool names alongside the direct names (#454) | 2026-11-08T23:44:55Z | .dev/tasks/… (100 returned; possibly incomplete) |
| #457 | test(hooks): assert the launch-level guard speed limit on every run, including xdist workers (#440) | 2026-11-08T22:41:10Z | .dev/tasks/…, tests/hooks/… |
| #455 | fix(issue): accept the ccsession session name in the tab title as the shim check | 2026-11-08T20:07:12Z | src/superclaude/…, tests/skills/… |
| #453 | fix(tests): pick ccsession shim ports clear of the stand-in gateway's shim window (#443) | 2026-11-08T13:47:59Z | .dev/tasks/…, tests/unit/… |
| #451 | docs(dev): record the issue-watcher brainstorm, task outcome and reflect patterns (#331) | 2026-11-08T07:32:03Z | .dev/brainstorms/20261107-064825-github-issue-watcher/…, .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/…, docs/memory/reflect/deviation-patterns-issue-331-github-issue-watcher.md |
| #449 | feat(orca): require an agent on every worktree create | 2026-11-08T07:05:30Z | .dev/tasks/…, CLAUDE.md, docs/designs/…, docs/user-guide/…, plugins/superclaude/…, src/superclaude/…, tests/cli/…, tests/core/…, tests/hooks/…, tests/skills/…, tests/unit/… |

### Commits on the default branch since creation

Full `git log --name-only` output is in `/home/coder/.claude/projects/-home-coder-workspaces-IronClaude/1779a921-dc86-44c8-867c-d5e117eb8e31/tool-results/bsdrk5h0c.txt`; directory summaries below are abbreviated. Git commit paths may be more complete than the PR API's capped files field.

| Commit | Changed files |
|---|---|
| 933cf3a4f (#459) | docs/designs/sc-issue-claim-pipeline-flag.md |
| ed6074c47 (#458) | See full git log above; MCP proxy names and associated files |
| 085afc8d1 (#457) | .dev/tasks/…, tests/hooks/… |
| 2c8109b30 (#455) | src/superclaude/…, tests/skills/… |
| 0423fe5f1 (#453) | .dev/tasks/…, tests/unit/… |
| 5dc29d23b (#451) | .dev/brainstorms/20261107-064825-github-issue-watcher/…, .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/…, docs/memory/reflect/deviation-patterns-issue-331-github-issue-watcher.md |
| 24d79b7fa (#449) | .dev/tasks/…, CLAUDE.md, docs/designs/…, docs/user-guide/…, plugins/superclaude/…, src/superclaude/…, tests/… |

### First guesses

- Complexity: complex: rollout requires an owner-run live test, a 24-hour shadow run, concurrency and restart checks, and scheduling.
- Type: feature: the issue requests rollout and activation of an existing watcher rather than a standalone bug fix.
