# Proposal C: The owner is the #539 author; agents may prepare, only the owner commits and pushes

## Answer

The owner personally is the #539 author. An agent session in this checkout may prepare and test the SW-02 and SW-03 changes and leave them uncommitted. The owner reviews them, commits named paths and pushes by hand, so no session ever holds push authority on #539.

## What happens next if the owner picks it

- The ledger records "#539 author = the owner; agent role = prepare and test only".
- After Q1's ruling, an agent session in this checkout makes the SW-02 change and runs `uv run pytest tests/sweep/`, then stops and reports. The same happens for SW-03. It does not stage, commit, push or resolve threads.
- The owner reads the diff, stages named paths only (`git add -- <paths>`), commits and pushes, and resolves the Augment thread personally. No `GRANT(<item>,push)` or `GRANT(SW-03,thread-resolve)` row is needed, because the owner acts directly.
- The owner refreshes the merge ref and merges (SW-05). `/sc:pr-submit` is not used on #539 (Q28's default).

## What it unlocks

- Removes push authority from agents on the PR that carries the INV-008 security finding. The spec already says no tool may design or push an INV-008 fix (6.3), and this applies the same caution to the hand push.
- Needs no grant rows for SW-02, SW-03 or SW-05 pushes, and no question about which session owns the checkout.
- The owner sees every line before it reaches GitHub, which the worker contract asks for anyway before publishing unseen changes (`WORKER-CONTRACT.md:244`).

## What it costs or risks

- Every push on the critical path waits on the owner's own time, in a program where "Owner latency is the real schedule" (line 523). SW-05 blocks most later work.
- The owner must run git by hand with named-path staging in a checkout full of untracked program files. A mistaken `git add .` would carry them into #539 (A-005).
- Pushes made by the owner directly do not appear in the grant table, so the ledger must record them separately to keep the audit trail complete.
- The preparing agent session still has to be identified (or launched), so part of the "which session" question remains.

## What stays unresolved

- Which agent session prepares the changes (the existing checkout session or a new one).
- Whether the owner wants the same arrangement for later program PRs (this covers #539 only).
