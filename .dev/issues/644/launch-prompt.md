You were started by `/sc:issue --claim 644` in this worktree. Read `.dev/issues/644/issue-summary.md` and `.dev/issues/644/next-steps.md` first.

Run each step of `next-steps.md`, in order, by invoking its command through the Skill tool in this session. Never read a command file and carry it out by hand, and never run a step inside a subagent.

`next-steps.md` names the model tier it was written for on its first line. If this session runs on a lower tier, say so in your first message and carry on.

Never merge anything, and never push to `master` or `main`.

Level: full. Run every step of `next-steps.md` through the last one; the `Plan boundary` line does not apply. Leave all changes in the working tree and stage nothing. Make no commit, push no branch and open no pull request, by any command or skill; if a step would do any of these, skip that part and say so. Finish by printing `git status --short`.
