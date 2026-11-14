<!-- Provenance: produced by /sc:adversarial -->
<!-- Base: Variant 1 (proposal-A) -->
<!-- Merge date: 2026-11-14 -->
<!-- Plan: adversarial/refactor-plan.md (5 changes, all applied); log: adversarial/merge-log.md -->

# Proposal A: narrow Coder#477 to read-only workspace status and identity, with no prompt routing

## Answer
<!-- Source: Base (Variant 1, proposal-A); appended sentence from Variant 3 Answer and reopen conditions, plan Change 1 (debate X-001, X-003, A-003) -->

Narrow Coder#477: rewrite it as "Read-only workspace status and identity for the Orchestrator observer (no prompt routing)", so a read-only observer outside a workspace can see which of the owner's Coder workspaces exist, whether each runs, and each one's status record, and nothing can be sent to a workspace through it.

Close is the right answer instead if the owner states that single-host is lasting and that no TUIBBS screen or remote reader is planned: then Coder#477 is closed as superseded with text C and its two reopen conditions (ADJ line 283; Q18 at `merged-requirements.md:545`).

## What happens next if the owner picks it
<!-- Source: Base (Variant 1, proposal-A); step 2 clause from plan Change 4 (V3 advocate; spec CO-03 (5)); step 3 grant wording and fallback note from plan Change 3 (Variant 3 advocate concession 3 and A-002 response) -->

1. The owner answers Q4 (what "TUI Panel" means) and Q22 (the age after which a record is stale), or lets text A keep "owner decides" for the age.
2. CO-02 completes text A's placeholders: the age, the owner-token route marked UNVERIFIED or removed, and the record named "observe snapshot v1" exactly as the contract note names it. It also reconciles text A's statement that the read route "writes nothing" with text A's requirement of an audit line per read, as CO-03 (5) already asks.
3. CO-01: the single issue editor posts text A on Coder#477 with a one-line Q4 answer, after the #450 edits and before the #409 pass, under `GRANT(CO-01,issue-write)`, after re-reading `updatedAt`. Each write gets its own grant row that names it (XC-02 (4)); whether the `issue-write` action covers a state change is UNVERIFIED.
4. CO-03 (deferred, in the Coder repo): implementation only after text A is posted, with each of the nine checklist items tested and a written read-permission model.

Fallback note (if the owner picks close under the condition in the Answer): text C is not fully paste-ready. It holds the placeholder "[link to the comment holding option A]" (ADJ line 661), so it must be reworded or text A posted first, and the grant row must name the close as a state change.

## What it unlocks
<!-- Source: Base (Variant 1, proposal-A), unchanged -->

- Keeps the one real need the issue carries: the observer reads one host's Orca only and cannot see another workspace (ADJ Part 6.3 text A problem statement).
- Removes the dangerous part: no prompt, command or session-start route, so no remote path can start a permission-free session (checklist item 9).
- Gives the owner's 2026-11-13 comment ("Ensure this aligns with Orchestrator and TUI Panel") a concrete answer: aligned as a read-only source for the observer.
- The #423 rewrite can settle its "if #477 is kept" clause.

## What it costs or risks
<!-- Source: Base (Variant 1, proposal-A); last bullet from plan Change 2 (debate A-001; V1 advocate concession) -->

- Text A is not paste-ready: three open items (age placeholder, UNVERIFIED owner-token route, naming match) must be filled first (ADJ line 606).
- It commits the Coder repo to a design whose consumers (observer release R4 remote fleet, a TUIBBS screen) do not exist yet; it may sit unbuilt.
- A later Coder change could add a send route without the checklist (merged-requirements residual risk for CO-01).
- The Coder-repo paths rest on one review only ("per V3").
- Narrowing in effect replaces the problem statement: the issue's written body serves only the watcher, so text A is a new problem under the old issue number (debate A-001).

## What stays unresolved
<!-- Source: Base (Variant 1, proposal-A); last bullet from plan Change 5 (Variant 2, U-002, preserved in ADJ Part 6.3) -->

- When, if ever, a reader needs another workspace's status (R4 or TUIBBS timing).
- The read-permission model across workspaces.
- Text B's guards stay on record: if the owner ever revisits the watcher's design decision D1 (`docs/designs/issue-watcher.md:39`), text B in ADJ Part 6.3 (signed, expiring, one-use grants; separate read and request credentials; rate caps; audit; and the owner's written acceptance of every started session's permission mode) is the guarded routing text to start from. Nothing is lost by not keeping routing now.
