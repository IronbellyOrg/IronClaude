# Proposal C: no coordinator yet; the owner keeps the ledger by hand

## Answer

Do not name a coordinator home now: XC-09 does not start, the owner keeps the decision ledger by hand outside the repository, and no program file is written on any branch until the first-wave owner rulings (INV-008 and the #539 author) have landed and Orca is confirmed reachable.

## What happens next if the owner picks it

1. XC-10 part (3) records "held: Q26 default" with the date.
2. The owner records answers (Q1, Q33 and the rest) in their own notes; SW-01's ruling is the owner's reply on the Codex thread of PR #539 only, which never waited for the ledger (`refactor-plan.md:91`).
3. Work that needs no coordinator proceeds: SW-01 to SW-05 on PR #539 by its author, the GitHub-only edits under their grants, and items marked "ledger only" (kept by the owner).
4. Q26 is asked again when the first worker-dispatched item (edge 119) is next, with the then-current state of the main checkout and of Orca.

## What it unlocks

- Nothing new; it avoids committing to a home before the facts that affect it (Orca reachability, whether the docs branch is finished, whether `--agent` counts as person-opened) are settled.
- No branch switch in the main checkout and no new worktree.

## What it costs or risks

- Every dispatched item (SW-07, SW-08, SW-10, SW-14, OB-05 to OB-07, WA-01, WA-03, XC-05 to XC-07, V2-03, V2-05) waits.
- The ledger kept by hand is not in the repository, so the grant table (6.8) that every outward action needs exists only in the owner's notes; agents cannot read it from disk, so every grant must be restated in each session.
- It conflicts in spirit with the always-staged `.dev/tasks/` practice for program state.

## What stays unresolved

- Everything Q26 asks; it is only deferred.
