# Who is responsible for the issue watcher's sessions? (Q20)

## Question in one sentence
Who owns the agent in the issue watcher's working folder, and may that folder collect up to 6 new Claude sessions a day that no coordinator session looks after?

## Why you are being asked
The watcher's first live test, the setup step that creates its folder, and one planned edit to issue #450 (the watcher rollout issue) all wait on this answer. Without it the watcher cannot be tested or switched on.

## Background you need
- The issue watcher is a background process: when an issue is approved, it starts a Claude session that claims the issue. It is not part of the coordinator's managed work.
- Every session starts in one shared Orca working folder (a "worktree"). Orca's rule: whoever creates a worktree with an agent owns that agent.
- It starts at most 6 sessions in 24 hours (a value fixed in code, meant for you to confirm after a trial run). Nothing closes these sessions; the setup guide says to close them yourself in Orca.
- The sessions read issue text that anyone who can comment can write. On this host they run with permission checks off (a separate question, Q2).
- The coordinator session's duty ends when its own batch of work is done; it can only see these sessions as rows it "could not determine".

## Your options

### 1. A person you name owns it; sessions stay person-reviewed (recommended)
- If you pick this: that person creates the folder and owns its agent; up to the confirmed cap (default 6) of sessions a day are allowed, never coordinator-owned. The one-session live test runs now. Before the schedule is switched on, you write down who closes sessions and when, how often the person checks, and who covers when they are away.
- Upside: matches how the watcher was designed; keeps outsider-written text away from the coordinator.
- Downside: relies on that person actually looking and closing sessions by hand.

### 2. Decide nothing yet
- If you pick this: no folder, no live test, no schedule; asked again together with a cleanup rule.
- Upside: no unattended sessions at all.
- Downside: the watcher stalls, and the cleanup rule needs the live test's results anyway.

### 3. The coordinator session owns it and reviews the sessions
- If you pick this: the coordinator creates the folder and lists watcher sessions in its regular checks; a person still closes them.
- Upside: something already running keeps an eye on them.
- Downside: the coordinator stops when its own work ends, cannot really see these sessions, and would be exposed to outsider-written text.

## What the debate found
- All three debaters, including those arguing for options 2 and 3, judged option 1 best (60 to 70 percent).
- Option 2's caution belongs before switching the schedule on, not before a one-session test; that was added to option 1.
- The 6-a-day cap is yours to confirm or lower (a small code change).

## Recommendation and confidence
Option 1, 70 percent.

## If you do not answer
The same as option 2: the setup step and the #450 edit are left out, and the watcher's live test does not run.

## What this answer does not authorize
It does not authorize the live test itself (that also needs the claim-level answer and your written acceptance of the session's permission mode, Q2), switching on the schedule, or any coordinator adopting watcher sessions.

## How to answer
Type: "Q20: option 1, owner is <name>" (or "Q20: option 2" or "Q20: option 3").
