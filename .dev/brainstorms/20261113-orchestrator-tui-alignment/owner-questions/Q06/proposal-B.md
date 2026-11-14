# Proposal B: give the scope now, "any Run my terminal holds", and build the flip in parallel with the tests

## Answer

The pass covers any Run the terminal running the observer holds (not only `run_93bfa00cae2b`); do not flip before the seeded test, but write the scope sentence now so the flip pull request can be built and tested in parallel and lands as soon as the seeded test, the live-layout attempt and the build pin pass.

## What happens next if the owner picks it

- The owner's sentence "any Run my terminal holds" goes into the ledger now, with its date.
- OB-06 (the flip pull request) starts in its own worktree in wave W1 instead of W2: the code enforces "held by this terminal" (a test refuses a Run the terminal does not hold), so the global boolean no longer reads any syntactically valid `--run <id>` (ADJ INV-003).
- OB-03 (seeded test) and OB-04 (live-layout attempt) run as planned; the flip PR stays unmerged until both records and the build pin (OB-05) are linked. If OB-03 shows consumption, the PR is closed unmerged.

## What it unlocks

- The panel becomes useful for the Runs people actually work with: only the holder terminal can read a Run's questions anyway (Q-1 failed, ADJ INV-024), so "any Run my terminal holds" matches the only access path Orca gives.
- Saves one round of owner latency: no second question after the test.
- The pinned old Run `run_93bfa00cae2b` (an old "Claim issue 375" Run) gives no practical use; this answer avoids a flip that works only for a Run nobody watches.

## What it costs or risks

- The owner commits to a wide scope before knowing whether the read consumes on a live Run; a live coordinator Run has `--wait` listeners and an acknowledge cycle the throwaway Run lacks, so a seeded pass is necessary, not sufficient (ADJ line 174; `merged-requirements.md:1156`).
- "Held by this terminal" must be determined by the observer without `run-use`; whether a read verb reports the holder reliably is not established here (UNVERIFIED), and 28 of 53 Runs have no holder (ADJ INV-024).
- Building OB-06 before OB-03 may be wasted work if the test fails.
- The only debate recommendation to widen scope (V5 D5(ii)) was withdrawn (ADJ line 814), so this answer has no debate verdict behind it.

## What stays unresolved

Consumption on a live coordinator Run beyond the one disposable Run OB-04 reads; how the code detects "held by this terminal".
