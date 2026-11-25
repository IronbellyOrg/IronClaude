/model claude-gw-tier2

# Next steps for #593

Plan boundary: before step 1

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: the agent it launches does (up to the plan boundary at the default level), or you do after `--pipeline none`.

1. Create `ob-442/T1.txt` holding the single line `ob-442 T1` (Write tool; or `/sc:task "Create ob-442/T1.txt holding the single line ob-442 T1"`)
   - Input: `@.dev/issues/593/issue-summary.md`
2. Read `ob-442/T1.txt` and run `git status --short` to confirm it is the only change (manual check; there is no related test)
   - Touch nothing else, and do not merge anything: the issue says to close without merging.

- Effort estimate: 0.25 hours
- Default row not used: Feature, simple (brainstorm, workflow, implement) because one new one-line file is within the direct-change limit and needs no written plan.
