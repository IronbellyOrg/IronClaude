# Proposal A: narrow Coder#477 to read-only workspace status and identity, with no prompt routing

## Answer

Narrow Coder#477: rewrite it as "Read-only workspace status and identity for the Orchestrator observer (no prompt routing)", so a read-only observer outside a workspace can see which of the owner's Coder workspaces exist, whether each runs, and each one's status record, and nothing can be sent to a workspace through it.

## What happens next if the owner picks it

1. The owner answers Q4 (what "TUI Panel" means) and Q22 (the age after which a record is stale), or lets text A keep "owner decides" for the age.
2. CO-02 completes text A's placeholders: the age, the owner-token route marked UNVERIFIED or removed, and the record named "observe snapshot v1" exactly as the contract note names it.
3. CO-01: the single issue editor posts text A on Coder#477 with a one-line Q4 answer, after the #450 edits and before the #409 pass, under `GRANT(CO-01,issue-write)`, after re-reading `updatedAt`.
4. CO-03 (deferred, in the Coder repo): implementation only after text A is posted, with each of the nine checklist items tested and a written read-permission model.

## What it unlocks

- Keeps the one real need the issue carries: the observer reads one host's Orca only and cannot see another workspace (ADJ Part 6.3 text A problem statement).
- Removes the dangerous part: no prompt, command or session-start route, so no remote path can start a permission-free session (checklist item 9).
- Gives the owner's 2026-11-13 comment ("Ensure this aligns with Orchestrator and TUI Panel") a concrete answer: aligned as a read-only source for the observer.
- The #423 rewrite can settle its "if #477 is kept" clause.

## What it costs or risks

- Text A is not paste-ready: three open items (age placeholder, UNVERIFIED owner-token route, naming match) must be filled first (ADJ line 606).
- It commits the Coder repo to a design whose consumers (observer release R4 remote fleet, a TUIBBS screen) do not exist yet; it may sit unbuilt.
- A later Coder change could add a send route without the checklist (merged-requirements residual risk for CO-01).
- The Coder-repo paths rest on one review only ("per V3").

## What stays unresolved

- When, if ever, a reader needs another workspace's status (R4 or TUIBBS timing).
- The read-permission model across workspaces.
