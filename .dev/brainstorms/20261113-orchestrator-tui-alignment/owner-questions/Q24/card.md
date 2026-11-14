# Who should make the live Orca checks?

## Question in one sentence
Which session (or person) should run three live checks against Orca: a read-only capture of a few unknown fields, a one-time comparison of worker ids between the dashboard and the sweep report, and a test that writes throwaway messages?

## Why you are being asked
Without a named runner, none of the three runs. That blocks the gate check for Orchestrator v2 (issue #423) and the dashboard's PR that turns on its questions panel. The review suggested "the 409 session, in one sitting". The debate found two problems with that.

## Background you need
- Orca is the local app that runs agent workers. The dashboard is `superclaude observe`. The sweep is the coordinator's read-only report (PR #539, not merged yet).
- "The 409 session" is the agent that built the dashboard, in worktree `issue-409-mvp`. That worktree is on an unmerged branch and holds unpushed commits and records that must not be lost. Nobody has checked whether that session is still alive.
- The comparison must run the sweep on merged (master) code, so it can only happen after PR #539 merges. That makes it a second sitting, two waves after the first.
- The message-writing test needs its own separate permission.

## Your options

### 1. A fresh session on master, made for this job (recommended)
- If you pick this: the coordinator creates a new Orca worktree from master with its own agent. That agent runs the capture now and the comparison after the merge. It may ask the 409 session questions but does not use it to run anything. You run the message-writing test yourself unless you name someone else.
- Upside: certain to exist; on the right code; cannot touch the 409 worktree's unsaved work.
- Downside: one more worktree to create and clean up; the new agent starts without dashboard history.

### 2. The 409 session (the review's suggestion)
- If you pick this: the coordinator checks that the session is alive and that its terminal is not bound to a Run, then it runs all three, each under its own permission.
- Upside: it knows the dashboard and has run similar checks safely before.
- Downside: if it has ended, nothing runs; its branch is not master; its unsaved work is at risk.

### 3. You run them by hand
- If you pick this: an agent writes step-by-step procedures, and you run each check at a plain terminal.
- Upside: no agent makes live Orca calls.
- Downside: three sittings of your time; hand-typed commands drift more easily.

## What the debate found
- 2 of 3 advocates chose option 1; 8 of 10 points agreed. Who runs the message test, and whether agents should make live calls at all, stayed open.
- A past failure only blocked reading another Run's mailbox, not listing its workers. The first step of the capture should confirm this.

## Recommendation and confidence
Option 1, about 65 percent.

## If you do not answer
None of the three checks runs. The Orchestrator v2 gate check cannot pass, and the dashboard's questions panel stays off.

## What this answer does not authorize
It does not grant any permission row. Each check still needs its own row in the ledger. The message-writing test needs its own write permission. No `run-use`, no merge, and no message to a live coordinator.

## How to answer
Type: "Q24: option 1" (or "Q24: option 2", "Q24: option 3"). With option 1, you can add "and I run the message test" or name a runner for it.
