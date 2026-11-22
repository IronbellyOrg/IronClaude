/model claude-gw-tier2

# Next steps for #643

Plan boundary: before step 1

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: the agent it launches does (up to the plan boundary at the default level), or you do after `--pipeline none`.

1. `/sc:implement "Create the single file ob-442/T2.txt containing exactly the one line `ob-442 T2`. Touch nothing else. Source: @.dev/issues/643/issue-summary.md"`
   - Input: `@.dev/issues/643/issue-summary.md`
2. Check the recorded verification: `ob-442/T2.txt` exists and holds exactly `ob-442 T2`. No related test applies.

- Effort estimate: 0.25 hours
- Default row not used: Feature, simple (the brainstorm, workflow, implement chain), because the whole job is one new file with one known line, which fits the guide's small-change level and needs no written plan.
- Close the issue without merging anything, as it asks.
