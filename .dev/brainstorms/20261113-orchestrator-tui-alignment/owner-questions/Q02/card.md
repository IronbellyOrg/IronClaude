# How far the issue watcher's automatic claim goes, and whether its first test may run without permission checks

## Question in one sentence
Should the issue watcher's automatic claim stop after assigning and commenting (`--pipeline none`) or also open a worktree with a second agent (the default), and do you accept in writing that its first live test session runs with permission checks off?

## Why you are being asked
The watcher is built but has never run live. Its first live test (called FU-1), the small code change that sets the claim level, and edits to the rollout issue #450 all wait for this answer. Accepting a security risk in writing is yours alone.

## Background you need
- The watcher polls for approved issues and starts a Claude session that runs `/sc:issue --claim <N>`. It passes nothing else, so today the claim runs at its default level.
- Default level: assign the issue, post two comments, write summary files, then create a worktree and start a second agent that stops at a plan for a person. `--pipeline none` stops after the comments.
- Your own watcher design says the claim stops at the summary file ("claim-only"). The default contradicts it; reviewers judged that an accident.
- On this host every launched Claude session runs with permission checks off. The session reads the issue's text, which anyone who can edit the issue controls.
- The claim command's own gate says no claim at any level runs on a real issue until a hook check called "OB-H1 item 5" passes; it is recorded as not yet run.

## Your options
1. **Claim-only, and accept permission checks off for the one test issue.**
   - If you pick this: a small watcher change adds `--pipeline none`; the test waits until the hook check passes, you record a separate live-test permission, Orca is reachable and the watcher worktree has a named owner; then one test runs and is recorded.
   - Upside: matches your design; one session per approval, no extra worktrees; the test settles facts nothing else can.
   - Downside: that one session still reads untrusted text with checks off. Your acceptance covers whatever it does on that issue, not only the intended writes. One possible write (a ClickUp script) may not be reversible.
2. **Claim-only, but do not accept permission checks off yet.**
   - If you pick this: the same small change; the live test waits until a session can run with checks on, or until you accept later.
   - Upside: no session runs with checks off on your say-so.
   - Downside: nothing downstream starts; a session with checks on may stall with nobody to approve prompts.
3. **Keep the default (claim, worktree and second agent).**
   - If you pick this: no code change; your design document is amended; the test waits for all of the claim command's hook checks; your acceptance covers two sessions.
   - Upside: each approval yields a ready plan.
   - Downside: two sessions with checks off per approval, unowned worktrees and agents (up to 6 sessions a day), and it reverses your own recorded decision.

## What the debate found
- All three advocates, including those for options 2 and 3, recommended option 1 when asked to be neutral.
- The default level was judged an accident against your own "claim-only" decision.
- Every option also needs a separate live-test permission row, a reachable Orca and an owner for the watcher worktree; none of the drafts said so.
- The hook check "OB-H1 item 5" binds even the claim-only level and is recorded as not yet run.

## Recommendation and confidence
Option 1, 72 percent, with the acceptance worded to cover whatever the one session does on the test issue. Writing the test issue's text yourself lowers the risk. This matches the spec's recommended answer, plus the preconditions above.

## If you do not answer
The small watcher change and the live test do not start, and the first edit to #450 is left out of the edit set and recorded as skipped.

## What this answer does not authorize
Any later, non-test issue running with checks off; the live test itself without its separate live-test permission row; any merge; any handoff from the watcher to an orchestrator (not built).

## How to answer
Type, for example: "Q2: option 1, accepted for the test issue only" (or "Q2: option 2" / "Q2: option 3, accepted for both sessions on the test issue").
