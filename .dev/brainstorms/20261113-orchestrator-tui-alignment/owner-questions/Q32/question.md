# Q32: May supervised workers make one local commit at the end of their Task?

## The question (verbatim from the spec row)

Source: `merged-requirements.md` section 3, row Q32 (line 559).

> May supervised workers make one end-of-Task local commit? If yes, give the sentence to quote (new, R25-INV-015)

## The spec's recommended answer

> No; the PR session commits

## Default if unanswered

> Same as recommended: workers leave changes uncommitted; the PR session commits named paths

## What it gates

> `GRANT(<item>,commit)` rows only; asked only when the first code-changing worker is dispatched

In plain words: Q32 starts no work item and blocks none. It decides whether the grant table in the decision ledger (work item XC-01, the program's on-disk record of owner answers; the grant table is a list of one-row permissions, each written `GRANT(<item>,<action>)`, spec section 6.8) may ever hold a "commit" row for a worker. Dependency graph edge 101 (line 748): "Recorded only; they gate no item (Q32 governs `GRANT(<item>,commit)` rows)". Wave: W1 (the first working wave). It is asked only when the first code-changing worker is dispatched (line 523).

## Facts the question depends on

1. **The worker contract's only allowed git write.** `src/superclaude/core/WORKER-CONTRACT.md:41-42` (rule WC-9): a supervised worker (an agent session started by Orca's `worker-start` to do one Task and report with `worker_done`) may make "the worker session's end-of-Task local commit, made only when (1) the brief quotes, word for word, the user's instruction naming a local commit for that Task, (2) the worker runs alone in its own child worktree created by Orca (WC-11), and (3) the command has exited with `worker_status: succeeded`." It then stages named paths plus `.dev/tasks`, commits with `git commit --only -- <paths>`, never `--no-verify`, never pushes, and puts the commit id in its `worker_done` body. Outside that grant a worker "never runs `git add` ... never commits".
2. **One grant per Task.** `WORKER-CONTRACT.md:244`: "A commit grant covers one Task and ends at that Task's `worker_done`." Same line: before any push that would publish worker commits the person has not seen, the coordinator shows them to the person and pushes only on the person's go.
3. **Who commits otherwise.** `WORKER-CONTRACT.md:245`: the coordinator commits in a worktree only when no worker runs there, stages explicit paths plus `.dev/tasks`, never `--no-verify`. The spec moves this job to the PR session (an ordinary top-level session that runs `/sc:pr-submit --monitor 3` for one PR after the worker's session has ended, Q25): spec section 6.4 rule 14 (line 987), "the PR session (6.3) stages and commits named paths with exclusive use of the worktree, after the coordinator has shown the person any change they have not seen".
4. **Why this was asked.** Probe finding INV-015 (`adversarial/adversarial/invariant-probe.md:23`): "No variant or R2 asks the owner for per-Task commit wording, so either workers leave every change uncommitted (and the coordinator commits, adding to INV-001's load) or briefs lack the quote and the commit is refused."
5. **The PR session commits anyway.** Spec line 1050: a `pr-submit` grant row lists "local fix commits ... in the worktree" among the tool's writes.
6. **How many workers it touches.** The items that end in a program PR (Q25's gate list, line 552): SW-07, SW-08, SW-10, SW-14, OB-06, OB-07, WA-01, WA-03, XC-07, so up to nine code-changing worker Tasks. SW-02, SW-03 and SW-05 are done by the #539 author, a top-level session, not a worker (section 6.3).
7. **Child worktree condition.** WC-11 (`WORKER-CONTRACT.md:47`): "A worker gets its own child worktree (section 4) when its brief grants local commits". The spec gives every worker its own `worker-start` worktree (section 6.2). Whether a `worker-start` worktree counts as the "child worktree created by Orca" WC-9 names is UNVERIFIED (my reading: likely yes).
8. **Whether one standing sentence can serve every Task.** WC-9 asks for "the user's instruction naming a local commit for that Task". Whether one sentence with the Task id filled in by the coordinator meets "word for word" is not stated in the contract: UNVERIFIED.
9. **Hooks.** This repository runs a pre-commit `verify-sync` hook (project CLAUDE.md, "ABSOLUTE RULE: Never Stage or Commit `.claude/` Contents"); a commit by any session runs it, and WC-9 forbids `--no-verify`.
