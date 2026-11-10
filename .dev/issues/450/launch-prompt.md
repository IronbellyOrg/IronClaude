You were started by `/sc:issue --claim 450` in this worktree. Read `.dev/issues/450/issue-summary.md` and `.dev/issues/450/next-steps.md` first.

Run each step of `next-steps.md`, in order, by invoking its command through the Skill tool in this session. Never read a command file and carry it out by hand, and never run a step inside a subagent.

`next-steps.md` names the model tier it was written for on its first line. If this session runs on a lower tier, say so in your first message and carry on.

Never merge anything, and never push to `master` or `main`.

Level: worktree. Follow the steps of `next-steps.md` up to the line `Plan boundary: after step <K>` (the number after `after step` is the last step you may run before a human approves). If the line reads `Plan boundary: before step 1`, there is nothing to run yet. Do not run `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`.

When the plan exists, print its path and the words `Waiting for approval`, then wait. A human approves by replying `approved` in this session or by running the printed implement command. After that, run the remaining steps, still with no commit, no push and no `/sc:pr-submit`.
