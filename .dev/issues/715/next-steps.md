/model claude-gw-tier2

# Next steps for #715

Plan boundary: before step 1

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: the agent it launches does (up to the plan boundary at level `worktree`, to the last step at level `full`), or you do after `--pipeline none`.

1. Write `ob-442/T4.txt` holding the single line `ob-442 T4` (native Write tool; no other file is touched).
   - Input: `@.dev/issues/715/issue-summary.md`
2. Read the file back and run `git status --short` to confirm it is the only change. Do not merge anything.

- Effort estimate: 0.25 hours
- Default row not used: Feature, simple (`/sc:workflow` then `/sc:implement`): one new one-line file is a level 2 direct change, and a written plan costs more than it saves.
