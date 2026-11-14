# Proposal B: No. Workers never commit; the PR session commits

## Answer

No. Supervised workers in this program leave their changes uncommitted and unstaged, and the PR session (the top-level session that later opens the pull request for that worktree) stages and commits named paths, after the coordinator has shown the person any change they have not seen.

## What happens next if the owner picks it

- The ledger records Q32 = no, with the date. The grant table never holds a `GRANT(<item>,commit)` row for a worker in this program.
- Every worker brief says the worker leaves its changes uncommitted (spec line 1070 brief rule; `WORKER-CONTRACT.md:42` "Outside that grant a worker never runs `git add` ... never commits").
- After the coordinator admits the worker's `worker_done` and the worker's session has ended, the PR session gets exclusive use of the worktree, the coordinator shows the person the uncommitted change, and the PR session stages named paths plus `.dev/tasks` and commits with `git commit --only -- <paths>`, never `--no-verify` (spec 6.4 rule 14; `WORKER-CONTRACT.md:245` describes the same steps for the coordinator).

## What it unlocks

- One commit path for every program PR: the same session that pushes also commits, so what is pushed is exactly what that session committed and checked.
- No owner wording to collect, and no question of whether a standing sentence meets WC-9's "word for word ... for that Task".
- The person reviews the diff once, before the commit, rather than reviewing worker commits before the push (`WORKER-CONTRACT.md:244`).
- Matches the default, so nothing changes if the owner never answers.

## What it costs or risks

- Between `worker_done` and the PR session's commit, the change exists only as uncommitted files in the worktree. Removing or cleaning that worktree, or a stray checkout in it, would lose it. The spec does not measure how long that gap is (UNVERIFIED).
- No commit id to cite in the worker's `worker_done` body; the coordinator inspects the change with `git status` and `git diff` rather than a fixed revision.
- All commit work and any pre-commit hook failure (this repo runs a `verify-sync` hook) lands on the PR session, which adds to the work INV-001 already loads onto the PR route.

## What stays unresolved

- How long uncommitted work may wait between a worker's end and its PR session (not specified).
- Whether this "no" should hold for later programs too (it covers this program only).
