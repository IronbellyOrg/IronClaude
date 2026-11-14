# Proposal A: accept now with caveats, fix in a tracked follow-up with a hard trigger

## Answer

(a) Accept the risk for PR #539 now (the F3 option: caveat every "read-only" claim and record a written acceptance), and at the same time order a fix (neutralise or refuse, method left to the PR author) as a tracked follow-up that must land before a named trigger: before the one real-id comparison (XC-04) runs, before any unattended or scheduled sweep, and before a second user or host is added. (b) The acceptance and the follow-up both cover every channel measured on 2026-11-13 (fsmonitor, clean and process filters, `include.path`/`includeIf`, per-worktree config, `GIT_*`/`GIT_CONFIG_*` variables).

## What happens next if the owner picks it

1. The owner posts the ruling on the Codex security thread on PR #539 (SW-01), naming the premise it relies on (single owner, single host, every session already runs with permission checks off: ADJ E-11) and the full channel list.
2. The #539 author adds a caveat to every "read-only" or "changes nothing" statement in #539's files: at least 16 locations, not four (probe INV-011), keeping the mirror byte-equal.
3. A row in the #534 follow-up table records the fix with its owner and its trigger.
4. PR #539 merges once the other thread and CI are clear (SW-03, SW-04, SW-05).
5. A second, small PR later implements the fix with the probe experiment as its regression test, and removes the caveats it made true again.

## What it unlocks

- The #539 merge is not held for a fix design that touches the owner-signed allow-list and three pinned tests (INV-009) and the shared path list (INV-039).
- Everything behind the merge (post-merge wording fixes, contract-note links, routing row) can start sooner.
- The fix gets its own focused review instead of riding inside a 1003-file PR (ADJ E-08).

## What it costs or risks

- Two passes over the same 16-plus texts: caveat now, un-caveat later.
- The one real-id comparison (XC-04) must still wait for the follow-up fix, because the spec forbids running the unfixed sweep for it (`merged-requirements.md`, XC-04 row (4)). So the slowest downstream lane gains nothing.
- An acceptance is reversible only before merge (SW-01 row); after merge the hole is on master until the follow-up lands.
- Follow-ups with a trigger can slip; the trigger is a promise in a table, not a mechanical gate.

## What stays unresolved

- Which fix method the follow-up uses (neutralise or refuse) and who writes it.
- Whether the trigger list is complete; a future change (a second host, a shared workspace) could arrive without anyone checking the #534 row.
