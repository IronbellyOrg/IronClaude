<!--
Template of `launch-prompt.md` (claim Wave 5). Four blocks, each opened by a marker
line of the form `block:<name>` inside an HTML comment. `orca_worktree.py prompt`
keeps `common` plus the level block (`worktree` or `full`), plus `submit` when
`--submit` was passed, drops every other block and every marker line, and replaces
`<N>` with the issue number and `<R>` with the origin repository (`owner/repo`).
Text before the first marker is dropped. Code, not the
model, assembles the file, so a block cannot be paraphrased away.
-->

<!-- block:common -->
You were started by `/sc:issue --claim <N>` in this worktree. Read `.dev/issues/<N>/issue-summary.md` and `.dev/issues/<N>/next-steps.md` first.

Run each step of `next-steps.md`, in order, by invoking its command through the Skill tool in this session. Never read a command file and carry it out by hand, and never run a step inside a subagent.

`next-steps.md` names the model tier it was written for on its first line. If this session runs on a lower tier, say so in your first message and carry on.

Never merge anything, and never push to `master` or `main`.

<!-- block:worktree -->
Level: worktree. Follow the steps of `next-steps.md` up to the line `Plan boundary: after step <K>` (the number after `after step` is the last step you may run before a human approves). If the line reads `Plan boundary: before step 1`, there is nothing to run yet. Do not run `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`.

When the plan exists, print its path and the words `Waiting for approval`, then wait. A human approves by replying `approved` in this session or by running the printed implement command. After that, run the remaining steps, still with no commit, no push and no `/sc:pr-submit`.

<!-- block:full -->
Level: full. Run every step of `next-steps.md` through the last one; the `Plan boundary` line does not apply. Leave all changes in the working tree and stage nothing. Make no commit, push no branch and open no pull request, by any command or skill; if a step would do any of these, skip that part and say so. Finish by printing `git status --short`.

<!-- block:submit -->
The owner asked for the commit and push by passing `--submit`. This replaces the no-commit, no-push and nothing-staged rule of the level block above, for the following steps only. After the last step:

1. Check that no pull request is already open or merged for this branch: `gh pr list --repo <R> --head <branch> --state all`. If one exists, stop and report it; do not commit or push.
2. Commit with `git commit` and a conventional-commit message. Stage `.dev/tasks` and the files you changed; never anything under `.claude/` and never `.dev/issues/`.
3. Push the current feature branch with `git push origin <branch>`, never `master` or `main`.
4. Run `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."` through the Skill tool. Never merge.
