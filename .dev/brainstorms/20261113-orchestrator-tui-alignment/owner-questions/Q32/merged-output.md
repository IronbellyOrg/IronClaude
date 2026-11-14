<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (proposal-B) -->
<!-- Merge date: 2026-11-14 -->

<!-- Source: Base (original) -->
# Proposal B: No. Workers never commit; the PR session commits

<!-- Source: Base (original) -->
## Answer

No. Supervised workers in this program leave their changes uncommitted and unstaged, and the PR session (the top-level session that later opens the pull request for that worktree) stages and commits named paths, after the coordinator has shown the person any change they have not seen.

<!-- Source: Base (original, modified) with Change #4 and Change #1 -->
## What happens next if the owner picks it

- The ledger records Q32 = no, with the date. The grant table never holds a `GRANT(<item>,commit)` row for a worker in this program.
<!-- Source: Base (original, modified) with Change #4 -->
- Every worker brief says the worker leaves its changes uncommitted (spec line 1070 brief rule; `WORKER-CONTRACT.md:44` "Outside that grant a worker never runs `git add` ... never commits").
- After the coordinator admits the worker's `worker_done` and the worker's session has ended, the PR session gets exclusive use of the worktree, the coordinator shows the person the uncommitted change, and the PR session stages named paths plus `.dev/tasks` and commits with `git commit --only -- <paths>`, never `--no-verify` (spec 6.4 rule 14; `WORKER-CONTRACT.md:245` describes the same steps for the coordinator).
<!-- Source: Variant 2 advocate concession (A-002) with Change #1 -->
- The coordinator does not remove, clean or reuse a worker's worktree until its PR session has committed the change; this guard is not yet written in the spec as a general rule, so it is recorded in the ledger with Q32's answer.

<!-- Source: Base (original) -->
## What it unlocks

- One commit path for every program PR: the same session that pushes also commits, so what is pushed is exactly what that session committed and checked.
- No owner wording to collect, and no question of whether a standing sentence meets WC-9's "word for word ... for that Task".
- The person reviews the diff once, before the commit, rather than reviewing worker commits before the push (`WORKER-CONTRACT.md:244`).
- Matches the default, so nothing changes if the owner never answers.

<!-- Source: Base (original, modified) with Change #1 -->
## What it costs or risks

- Between `worker_done` and the PR session's commit, the change exists only as uncommitted files in the worktree. Removing or cleaning that worktree, or a stray checkout in it, would lose it. The spec does not measure how long that gap is (UNVERIFIED). The guard under "What happens next if the owner picks it" bounds this risk until the spec states it as a general rule.
<!-- Source: Base (original) -->
- No commit id to cite in the worker's `worker_done` body; the coordinator inspects the change with `git status` and `git diff` rather than a fixed revision.
- All commit work and any pre-commit hook failure (this repo runs a `verify-sync` hook) lands on the PR session, which adds to the work INV-001 already loads onto the PR route.

<!-- Source: Base (original, modified) with Change #2 and Change #3 -->
## What stays unresolved

- How long uncommitted work may wait between a worker's end and its PR session (not specified).
- Whether this "no" should hold for later programs too (it covers this program only).
<!-- Source: Variant 1 with Change #2 -->
- If the owner later wants a checkpoint commit for one specific Task, that Task can get its own owner sentence and grant, which meets WC-9 strictly.
<!-- Source: Variant 3 with Change #3 -->
- If the owner prefers yes after all, a sentence naming all nine work items (SW-07, SW-08, SW-10, SW-14, OB-06, OB-07, WA-01, WA-03, XC-07) lets each brief quote it unchanged; whether that meets WC-9's 'for that Task' is UNVERIFIED.
