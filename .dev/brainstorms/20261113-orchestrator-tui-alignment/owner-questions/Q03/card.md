# What to do with the Coder workspace-listener issue (Coder#477)

## Question in one sentence
Should the Coder issue #477 ("Workspace listener, monitor registration and secure prompt routing for every Coder workspace") be kept as written, narrowed to read-only workspace status, or closed?

## Why you are being asked
The issue sits in a different repository (IronbellyOrg/Coder), and its central idea, sending prompts into workspaces, no longer matches how the issue watcher was built. A reply is drafted and waiting. Nothing in IronClaude is blocked by it, but the reply also settles one sentence in the planned rewrite of issue #423.

## Background you need
- The issue watcher (IronClaude #331) was built as a poller inside each workspace. Your design chose no listener, no inbound port and no address list. #477 was written to serve that watcher.
- Any route that can start a session in a workspace starts it with permission checks off on the standard image. That is the main risk of keeping prompt routing.
- `superclaude observe` (the read-only worker dashboard, IronClaude #409) sees only this host. Seeing other workspaces is a planned later release; a TUIBBS screen (your separate TUI platform) is a possible later reader.
- On 2026-11-13 you commented on #477: "Ensure this aligns with Orchestrator and TUI Panel."
- Three replies are drafted: narrow, keep, close.

## Your options
1. **Narrow to read-only status and identity, with no prompt routing.**
   - If you pick this: the issue is rewritten so an outside reader can see which of your workspaces exist, whether each runs, and each one's status record. Nothing can be sent in. Some placeholders (for example how old a record may be before it counts as stale) are filled first.
   - Upside: answers your alignment comment; removes the risky send route; keeps the real gap on record.
   - Downside: the reply is not ready to paste yet; it designs for readers that do not exist yet; in practice it replaces the issue's problem statement.
2. **Close as superseded, with two reopen conditions.**
   - If you pick this: a ready closing comment says when to reopen (a watcher-design revisit, or a remote or TUIBBS reader that needs other workspaces). One link placeholder in it must be fixed first.
   - Upside: fewest decisions now; honest that nothing waits on it.
   - Downside: may not match your comment of yesterday; the gap is easy to forget once closed.
3. **Keep the listener and prompt routing, with strict guards.**
   - If you pick this: you reopen your watcher design choice; the issue waits for a signed-grant format that does not exist yet.
   - Upside: a path for one place to ask another workspace to act.
   - Downside: the largest attack surface; contradicts the built watcher; cannot be built yet.

## What the debate found
- Two of three advocates recommended narrowing; the third recommended closing, but only if you confirm single-host and no TUIBBS screen soon.
- All three ranked "keep" last.
- The closing text, called ready to post, still contains a link placeholder.
- Closing changes the issue's state, so the posting permission must say so.

## Recommendation and confidence
Option 1 (narrow), 55 percent. Close instead if you say the dashboard stays single-host for good and no TUIBBS or remote reader is planned. This matches the spec's recommended answer.

## If you do not answer
Nothing is posted on #477; the reply is recorded as skipped and the next issue edit in the sequence goes ahead.

## What this answer does not authorize
Posting the reply itself (that needs its own permission row naming each write, including a close); any work in the Coder repository; any route that sends prompts into a workspace.

## How to answer
Type, for example: "Q3: option 1, narrow" (or "Q3: option 2, close; single-host for good" / "Q3: option 3, keep").
