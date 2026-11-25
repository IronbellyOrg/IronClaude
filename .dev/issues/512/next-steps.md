/model claude-gw-tier1a

# Next steps for #512

Plan boundary: after step 2

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: you do after `--pipeline none`. Run them from a worktree based on `origin/master` (this checkout is far behind).

1. `/sc:workflow "Apply the nine MCP edits E1-E9 of GitHub issue 512 exactly as specified in @.dev/issues/512/issue-summary.md and the issue body; correct the audit bookkeeping noted in @.dev/issues/512/accuracy-check.md first; include the pinned tests and sync-dev" --depth standard --handoff none`
   - Input: `@.dev/issues/512/issue-summary.md`
2. Read the plan path it prints (`.dev/tasks/to-do/<id>/<id>.md`) and its advisory check result.
3. `/sc:implement <the exact plan path printed by step 1>`

- Effort estimate: 12 hours
- Default row not used: Feature, complex (brainstorm, design, workflow --depth deep, implement): the issue already holds exact edit specs E1-E9, and #504 followed the workflow-then-implement route.
