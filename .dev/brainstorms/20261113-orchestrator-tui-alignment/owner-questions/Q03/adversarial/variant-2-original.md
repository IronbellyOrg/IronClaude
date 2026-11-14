# Proposal B: keep Coder#477's listener and prompt routing, rewritten with strict guards

## Answer

Keep Coder#477 as a listener that can receive a fixed set of requests (for the watcher, only `claim` plus one integer issue number), and rewrite its acceptance criteria with text B's guards: signed, expiring, one-use grants; separate read and request credentials; rate caps; audit; and the owner's written acceptance of every started session's permission mode. This means revisiting the watcher's chosen design (no listener).

## What happens next if the owner picks it

1. The owner states that the watcher's design decision D1 option A (a poller inside each workspace, no listener) is being revisited (`docs/designs/issue-watcher.md:39`), and why.
2. CO-01 posts text B, which replaces the problem statement and acceptance criteria; it is not paste-ready until the grant format of #339 exists (ADJ line 606), so the route stays disabled until then.
3. The Coder-repo implementation waits for the #339 grant format, the nine-item checklist and a recorded permission-mode acceptance.

## What it unlocks

- A path for one workspace or a central place to ask another workspace to act, which a single poller per workspace cannot give.
- Keeps the owner's original feature idea intact rather than shrinking it.
- Lines up with a future "orchestrator of orchestrators" if the owner wants one (#339 version 2), without promising it exists.

## What it costs or risks

- It contradicts the built watcher (ADJ E-12) and the debate's verdict ("keep as written is the least defensible", ADJ line 605).
- Every accepted request starts a session with permission checks off on the stock image (checklist item 9); a remote route to that is the largest attack surface of the three options.
- It is blocked on the #339 grant format, which does not exist; the issue would stay open and unbuildable.
- The rewrite is the longest and needs the most owner decisions.

## What stays unresolved

- The grant format and trust design (#339, Q16).
- Who may send requests, and how a stopped workspace is handled (a listener cannot start a stopped workspace).
