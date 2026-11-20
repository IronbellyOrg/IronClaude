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

Only the coordinator writes to an issue, a label or a Project. You never post an issue comment, never change an issue, a label or a Project field, and never run the coordinator's completion step; you report only through your result file (the last step below).

<!-- block:worktree -->
Level: worktree. Follow the steps of `next-steps.md` up to the line `Plan boundary: after step <K>` (the number after `after step` is the last step you may run before a human approves). If the line reads `Plan boundary: before step 1`, there is nothing to run yet. Do not run `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`.

When the plan exists, print its path and the words `Waiting for approval`, then wait. A human approves only by running the printed implement command in this session, a prompt whose first line starts `/sc:implement`, `/sc:task` or `/task`. After that, run the remaining steps, still with no commit, no push and no `/sc:pr-submit`.

<!-- block:full -->
Level: full. Run every step of `next-steps.md` through the last one; the `Plan boundary` line does not apply. Leave all changes in the working tree and stage nothing. Make no commit, push no branch and open no pull request, by any command or skill; if a step would do any of these, skip that part and say so. Finish by printing `git status --short`.

<!-- block:submit -->
The owner asked for the commit and push by passing `--submit`. This replaces the no-commit, no-push and nothing-staged rule of the level block above, for the following steps only. After the last step:

1. Check that no pull request is already open or merged for this branch: `gh pr list --repo <R> --head <branch> --state all`. If one exists, stop and report it; do not commit or push.
2. Commit with `git commit` and a conventional-commit message. Stage `.dev/tasks` and the files you changed; never anything under `.claude/` and never `.dev/issues/`.
3. Push the current feature branch with `git push origin <branch>`, never `master` or `main`.
4. Run `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."` through the Skill tool. Never merge.

<!-- block:research -->
Stage: research. Step 1 of `next-steps.md` is `/sc:research` on `.dev/issues/<N>/issue-summary.md`. Keep its report under `.dev/issues/<N>/`.

<!-- block:spec -->
Stage: spec. Step 1 of `next-steps.md` is `/sc:design` when `issue-summary.md` has the line `spec-route: design`, otherwise `/sc:brainstorm`, followed by `/sc:design` for an issue of high complexity or scope.

<!-- block:plan -->
Stage: plan. Step 1 of `next-steps.md` is `/sc:workflow` on `.dev/issues/<N>/issue-summary.md`. Stop at the tasklist package it writes; never run `/sc:implement` or `/task` for this stage.

<!-- block:debugworktree -->
Stage: debug. Step 1 of `next-steps.md` is `/sc:troubleshoot` on `.dev/issues/<N>/issue-summary.md`, run without `--fix`. Report the cause and the next steps it proposes, then stop.

<!-- block:debugfull -->
Stage: debug. Step 1 of `next-steps.md` is `/sc:troubleshoot` on `.dev/issues/<N>/issue-summary.md`, run with `--fix`. It leaves a remediation tasklist package; never apply a code change by hand.

<!-- block:result -->
Last step, after every other step, whatever the outcome: write `.dev/issues/<N>/result.md` with exactly these three lines and nothing else:

```text
outcome: succeeded
artifacts: <repo-relative paths, comma separated, or empty>
pull_request: <the number, or none>
```

Use `failed`, `blocked` or `partial` in place of `succeeded` when that is the truth. The coordinator reads this file and does everything on GitHub itself.
