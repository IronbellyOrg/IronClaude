/model claude-gw-tier1b (use claude-gw-tier2 when tier1b is not in your /model list)

# Next steps for #611

Plan boundary: after step 3

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: the agent it launches does (up to the plan boundary at level `worktree`, to the last step at level `full`), or you do after `--pipeline none`.

1. `/sc:brainstorm "Jev preflight step 2: compare Jev against the keyword table on about 30 labelled prompts @.dev/issues/611/issue-summary.md" --blind`
   - Input: `@.dev/issues/611/issue-summary.md`
2. `/sc:design <brainstorm dir>/merged-requirements.md --type architecture --format spec`
3. `/sc:workflow <design doc> --depth standard --handoff none`
4. `/sc:implement <plan path printed by step 3>`

- Effort estimate: 10 hours
