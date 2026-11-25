/model claude-gw-tier2

# Next steps for #595

Plan boundary: after step 2

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: the agent it launches does (up to the plan boundary at the default level), or you do after `--pipeline none`.

1. `/sc:task "Create the file ob-442/T3.txt containing the single line: ob-442 T3. Change nothing else."`
   - Input: `@.dev/issues/595/issue-summary.md`
2. Read `ob-442/T3.txt` back and run `git status --short`; confirm that only `ob-442/T3.txt` changed. No related test exists for a text file.

- Effort estimate: 0.1 hours
- Default row not used: Feature, simple (brainstorm, workflow, implement). `/sc:recommend` chose the level-2 small-change route: one new file, one edit, under the five-edit limit.
