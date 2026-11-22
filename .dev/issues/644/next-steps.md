/model claude-gw-tier2

# Next steps for #644

Plan boundary: before step 1

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: the agent it launches does (up to the plan boundary at the default level), or you do after `--pipeline none`.

1. `/sc:task "Create the file ob-442/T3.txt holding the single line: ob-442 T3. Touch nothing else. Context: @.dev/issues/644/issue-summary.md"`
   - Input: `@.dev/issues/644/issue-summary.md`
2. Check the result: `git status --short` shows only `ob-442/T3.txt` as new, and `cat ob-442/T3.txt` prints exactly `ob-442 T3`. There is no related test to run. Close the issue without merging anything (the issue says so).

- Effort estimate: 0.1 hours
- Default row not used: Feature, simple (the change is one new one-line file, below the guide's hard limit, so a written plan adds nothing).
