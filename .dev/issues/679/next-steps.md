/model claude-gw-tier2

# Next steps for #679

Plan boundary: before step 1

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: the agent it launches does (up to the plan boundary at the default level), or you do after `--pipeline none`.

1. Make the edit directly with Write, or run `/sc:task "Create ob-442/T4.txt holding the single line: ob-442 T4. Touch nothing else."`
   - Input: `@.dev/issues/679/issue-summary.md`
2. Check the result: Read `ob-442/T4.txt` and confirm it holds exactly the line `ob-442 T4`, then run `git status` to confirm no other file changed (documented manual verification; there is no related test).

- Effort estimate: 0.1 hours
- Default row not used: feature, simple (the guide's hard limit is not reached by one new one-line file, so a written plan only adds overhead).
