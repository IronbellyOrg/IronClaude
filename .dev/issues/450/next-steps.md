/model claude-gw-tier1a

# Next steps for #450

Plan boundary: after step 2

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: the agent it launches does (up to the plan boundary at the default level), or you do after `--pipeline none`.

1. `/sc:workflow "Roll out the issue watcher (issue #450, follow-up to #331): replace the _assumed_shape fixtures with captured real gh and Orca output after the owner-run live test (FU-1), fix the stale status line and the 59-name reason table in docs/designs/issue-watcher.md, prepare the shadow-run, lock, restart and cron steps (FU-2) as owner-run checklist items, keep enabled false until the owner flips it. Spec and runbook: docs/designs/issue-watcher.md, docs/designs/issue-watcher-setup.md. Code: src/superclaude/cli/issue_watch/, tests/issue_watch/" --depth standard --handoff none`
   - Input: `@.dev/issues/450/issue-summary.md`
2. Read the actual printed plan `.dev/tasks/to-do/<id>/<id>.md` and its advisory check result.
3. Only when execution is requested: `/sc:implement <the plan path printed by step 1>`

- Effort estimate: 20 hours
- Default row not used: Feature, complex (the issue already fixes the requirements and the design and runbook exist, so a brainstorm and a new design add nothing; `/sc:recommend` chose the `simple-plan` row).
- The live test, the 24-hour shadow run, the lock and restart tests and the cron install need the owner's own gh login and Orca: no agent runs them.
