# Proposal B: keep both programs separate, joined by one short written contract note

## Answer

Keep the observer and the sweep as two separate programs with no runtime link in version 1, and write one short contract note between them: which file each publishes, what their shared words mean, which Orca commands each may call, and how their rows would be matched. Neither program reads the other and neither gains a file or key.

## What happens next if the owner picks it

1. XC-05: the note `docs/designs/observe-sweep-contract.md` is drafted on a master-based branch (not in the PR #539 checkout), with the registry of contracts, units, versioning rule ("consumers ignore unknown keys"), mapping table of shared words, verb lists per caller, binary resolution, and "candidate join basis" (not "join key") until the real-id comparison is done.
2. XC-06: one test compares the note's verb lists, schema versions, join basis and shared words with the two programs' constants and fails if either changes without the note.
3. XC-07: after PR #539 merges and the real-id comparison (XC-04), the note, the test and links from the sweep design and the observer spec merge in one PR opened by the PR session.
4. A shared parser is revisited after #539 merges; Q9 and Q17 stay at "not now".

## What it unlocks

- Ends the confusion of two files both called "v1", three vocabularies and two Orca allow-lists that disagree on one command (ADJ Part 1.1).
- Three other planned texts (the Coder#477 status record, the v2 field list, the #409 mapping table) depend on the note (ADJ Part 2.3).
- No code change in either program; no change to the sweep's one-report-per-run rule.

## What it costs or risks

- The person still sees two views that can classify the same session differently; the note documents the difference, it does not remove it.
- The test compares words and constants, not behaviour; "stale" can mean 45 seconds in one program and 6 hours in the other and still pass (`merged-requirements.md:1160`).
- The note and its test cannot land before PR #539 merges.
- The #409 body's "one shared set of facts" proposal is set aside for version 1.

## What stays unresolved

- Whether an observer panel for sweep facts is ever wanted (Q17) and how the sweep JSON would be kept (Q9).
- Whether the candidate join basis holds on real ids (XC-04).
