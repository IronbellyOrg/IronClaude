You were started by `/sc:issue --claim 712` in this worktree. Read `.dev/issues/712/issue-summary.md` and `.dev/issues/712/next-steps.md` first.

Run each step of `next-steps.md`, in order, by invoking its command through the Skill tool in this session. Never read a command file and carry it out by hand, and never run a step inside a subagent.

`next-steps.md` names the model tier it was written for on its first line. If this session runs on a lower tier, say so in your first message and carry on.

Never merge anything, and never push to `master` or `main`.

Only the coordinator writes to an issue, a label or a Project. You never post an issue comment, never change an issue, a label or a Project field, and never run the coordinator's completion step; you report only through your result file (the last step below).

Level: worktree. Follow the steps of `next-steps.md` up to the line `Plan boundary: after step <K>` (the number after `after step` is the last step you may run before a human approves). If the line reads `Plan boundary: before step 1`, there is nothing to run yet. Do not run `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`.

When the plan exists, print its path and the words `Waiting for approval`, then wait. A human approves only by running the printed implement command in this session, a prompt whose first line starts `/sc:implement`, `/sc:task` or `/task`. After that, run the remaining steps, still with no commit, no push and no `/sc:pr-submit`.

Last step, after every other step, whatever the outcome: write `.dev/issues/712/result.md` with exactly these three lines and nothing else:

```text
outcome: succeeded
artifacts: <repo-relative paths, comma separated, or empty>
pull_request: <the number, or none>
```

Use `failed`, `blocked` or `partial` in place of `succeeded` when that is the truth. The coordinator reads this file and does everything on GitHub itself.
