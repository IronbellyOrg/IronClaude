# Which session publishes each pull request?

## Question in one sentence
For each of the program's nine code changes, which session should open the pull request and run the review-and-fix tool `/sc:pr-submit --monitor 3` on your fork?

## Why you are being asked
Nine work items end in a PR, and none can be published until this is answered. The rules already forbid two candidates. A supervised worker may not push or open PRs. The coordinator may not run the tool, because its waiting loop would block the coordinator's own watch duty.

## Background you need
- A supervised worker is an agent started under the worker contract. It builds and tests one change, then reports "done" (`worker_done`) for the coordinator to accept.
- `/sc:pr-submit --monitor 3` opens the PR on `IronbellyOrg/IronClaude` and waits for two automatic reviewers. It then fixes, pushes, replies to and resolves their confirmed findings without asking.
- Orca is the app that runs agents. Nobody has checked whether Orca lets a second agent start in a worktree after its worker has finished.
- The worker contract requires that you see unseen changes before they are pushed.

## Your options

### 1. Worker builds, then a separate PR session publishes (recommended)
- If you pick this: after a worker's result is accepted and its session has ended, the coordinator starts a PR session in the same worktree. That session shows you the diff, waits for your go, then commits and runs the tool. Before the first item, someone checks that Orca allows this. If Orca does not, option 3's route is used, with a deadline check.
- Upside: the code is built under worker supervision; no session of yours per PR.
- Downside: rests on an unchecked Orca behaviour; two agents per change; the publishing session did not write the code.

### 2. You open each PR session yourself
- If you pick this: the coordinator tells you when a change is ready; you open a Claude session in that worktree and run the tool there.
- Upside: you give the instruction to publish yourself, every time.
- Downside: nine sessions you must open and attend; PRs wait whenever you are away.

### 3. One agent per change builds it and publishes it, with no worker
- If you pick this: the coordinator creates one worktree and agent per change; that agent builds, shows you the diff, and runs the tool.
- Upside: simplest; no unchecked Orca behaviour; the author answers its own reviews.
- Downside: loses worker supervision; an agent that stalls before opening its PR is not noticed automatically.

## What the debate found
- The advocates split three ways on the overall answer, though most single points had a clear majority.
- All agreed option 2 best guarantees you see each diff, option 3 is simplest, and option 1 alone keeps supervision without costing your time.
- All found a rule gap: the worker contract gives commits to the coordinator, but the plan gives them to the PR session. One sentence in decision D3, plus a grant row listing every write, closes it.

## Recommendation and confidence
Option 1 with option 3 as its fallback, about 55 percent. This is a close call.

## If you do not answer
No PR is opened. Each change stays uncommitted in its worktree, and its lane is held.

## What this answer does not authorize
It does not authorize any merge, and no PR is opened without its own permission row. It allows nothing on any repository other than `IronbellyOrg/IronClaude`, and no `/sc:pr-submit` on PR #539, which question Q28 governs.

## How to answer
Type: "Q25: option 1" (or "Q25: option 2", "Q25: option 3").
