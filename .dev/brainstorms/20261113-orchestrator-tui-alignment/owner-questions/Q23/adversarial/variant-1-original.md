# Proposal A: historical: a reclaimable worker has finished, so hide it with the other finished workers

## Answer

`reclaimable` is historical. The observer adds it to the states it hides from the default view (with `released` and `retained`), and the contract note's mapping table says "reclaimable: historical (finished, resources not yet released)".

## What happens next if the owner picks it

1. The contract note draft (XC-05) writes the mapping row: "reclaimable = historical in both programs; shown with Orca's word in detail views".
2. A small observer change adds `"reclaimable"` to `HISTORICAL_STATES` (`src/superclaude/cli/observe/view.py:35`), with a test that a reclaimable row is hidden by default and shown with the `h` key. It ships in its own small PR or inside the guard-flip PR (OB-06), opened by the PR session.
3. OB-06 prerequisite (e) is met by the note draft or the observer spec carrying the row.
4. The sweep needs no code change: it already reads finished state from Orca's `outcome` (`classify.py:98,114-115`), and its "safe to close" stays "could not determine" for reclaimable rows (`classify.py:479-481`).

## What it unlocks

- A default observer view that shows working workers, not finished ones: at the probe there were 27 reclaimable rows and 0 active (INV-023), so today the default view can be filled entirely with finished workers.
- One meaning of "historical" in both programs for this state.
- The observer's guard-flip PR can cite a final row, not a provisional one.

## What it costs or risks

- Orca's exact meaning of `reclaimable` is not documented in any file read (UNVERIFIED). If a reclaimable worker still holds a terminal or worktree that a person must release, hiding it removes a cue to clean up.
- A code change to the built observer, with a test, for a word whose meaning was inferred.
- The sweep's "historical" means "older than its 6 h window" and its "settled" comes from `outcome`, so "historical" still does not mean exactly the same thing in both programs; the note must say so.

## What stays unresolved

- Orca's own definition of `reclaimable`, and whether `release_pending` and `release_unknown` (listed in `worker-list --help`, behaviour UNVERIFIED) need the same treatment.
