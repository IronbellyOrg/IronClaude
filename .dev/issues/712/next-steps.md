/model claude-gw-tier2

# Next steps for #712

Plan boundary: before step 1

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: the agent it launches does (up to the plan boundary at level `worktree`, to the last step at level `full`), or you do after `--pipeline none`.

1. Write `ob-442/T1.txt` (at the worktree root) holding the single line `ob-442 T1`, with the Write tool.
   - Input: `@.dev/issues/712/issue-summary.md`
2. Read `ob-442/T1.txt` and run `git status --short`: the file holds exactly that one line and nothing else changed. Do not commit, push or merge.

- Effort estimate: 0.25 hours
- Default row not used: Feature, simple (/sc:workflow then /sc:implement) (a one-file, one-edit change is level 2 of the routing guide; a written plan would cost more than the change).
