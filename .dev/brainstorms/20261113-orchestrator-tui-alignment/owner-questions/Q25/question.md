# Q25: who runs `/sc:pr-submit --monitor 3` for each program PR?

## The question, verbatim

Spec row (merged-requirements.md section 3, line 552): "Who runs `/sc:pr-submit --monitor 3` for each program PR? (new, R25-INV-001)"

`/sc:pr-submit --monitor 3` is the project's mandatory way to open a PR on the fork `IronbellyOrg/IronClaude`: it opens the PR, then runs an attended poll loop for the Augment and Codex reviews and fixes, pushes, replies to and resolves confirmed findings (`~/.claude/skills/sc-pr-submit-protocol/SKILL.md:3,19`; project CLAUDE.md).

## Spec's recommended answer

"An owner-designated top-level PR session per PR, launched by the coordinator with `orca agent launch` in the item's worktree after the worker's `worker_done` is admitted and its session has ended, closed when the PR merges (that Orca permits a second, sequential agent launch in a `worker-start` worktree is UNVERIFIED; the owner confirms). Alternative: a top-level agent per PR item created with `worktree create --agent` and no worker (V2 Round 3)" (merged-requirements.md line 552).

## Default if unanswered

"No PR is opened; the change stays uncommitted in its worktree; the lane is held" (line 552).

## What it gates

Every program item that ends in a PR (line 552): SW-07 and SW-08 (post-merge sweep wording and small pinned fixes), SW-10 (machine-started label), SW-14 (conditional restore of the sweep's `working` class), OB-06 (the observer's guard-flip PR), OB-07 (the observer's routing row), WA-01 and WA-03 (issue watcher claim level and runbook), XC-07 (the contract note with its test and links). Each also needs its own `GRANT(<item>,pr-submit)` row in the ledger. Wave needed by: W1. Not authorized by Q25: a merge (line 576).

## Facts the question depends on

| Fact | Source |
|---|---|
| `/sc:pr-submit` is on the worker contract's never-as-worker list "while the answer to decision D3 keeps it off workers" | `src/superclaude/core/WORKER-CONTRACT.md:23` |
| WC-9: no outward action from a worker (push, PR, GitHub post); the only git write a brief may authorize is an end-of-Task local commit, by a quoted user instruction | `WORKER-CONTRACT.md:41-42` |
| WC-13: a worker never calls `worker-start`, `dispatch`, `task-create`, `worktree create --agent` or `agent launch` | `WORKER-CONTRACT.md:62` |
| "PRs go only through `/sc:pr-submit --monitor 3`, run in an ordinary top-level session as decision D3 states, never as a worker" | `WORKER-CONTRACT.md:243` |
| "Before any push that would publish worker commits the person has not seen, the coordinator shows them to the person and pushes only on the person's go" | `WORKER-CONTRACT.md:244` |
| The pr-submit skill "MUST run in the main orchestrating session" and is an attended, in-session poll loop | `~/.claude/skills/sc-pr-submit-protocol/SKILL.md:19,43,47` |
| The coordinator never runs `/sc:pr-submit` itself, because its poll loop would block the coordinator's watch duty (WC-16) | merged-requirements.md line 962 (6.3 Coordinator row), line 975 (6.4 rule 2) |
| A worktree gets its agent from `worker-start` (a supervised worker) or from `orca worktree create --agent` (a top-level agent), never both; one worktree never holds two live agents | merged-requirements.md line 951 |
| PR session role: runs `/sc:pr-submit --monitor 3` for one PR in the item's worktree, writes bounded by its grant row, closes when the PR merges; never runs while the worker's session is live; never merges | merged-requirements.md line 964 |
| Whether Orca allows a second, sequential `agent launch` in a worktree first created by `worker-start` is UNVERIFIED | merged-requirements.md lines 552, 964 |
| By default a worker leaves changes uncommitted; the PR session stages and commits named paths with exclusive use of the worktree (Q32 governs worker commits) | merged-requirements.md line 987 (6.4 rule 14), line 559 |
| The Round 3 alternative (V2): every PR item done by a top-level agent in its own Orca worktree created with `worktree create --agent`; `worker-start` workers only for report-only items; advocate confidence 85 | `.dev/brainstorms/20261113-orchestrator-tui-alignment/adversarial/adversarial/round3-invariants-V2.md:53` |
| Invariant R25-INV-001 (HIGH): addressed by rule; the PR actor model | merged-requirements.md line 1309 |
| PRs target only the fork; every `gh` call names `--repo IronbellyOrg/IronClaude`; a PR URL on `SuperClaude-Org` stops the session | project CLAUDE.md; merged-requirements.md line 975 |
