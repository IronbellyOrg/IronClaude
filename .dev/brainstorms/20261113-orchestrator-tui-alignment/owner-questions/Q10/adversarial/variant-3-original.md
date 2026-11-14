# Proposal C: the observer's alone for now; correct the sweep's two sentences now

## Answer

For now only the observer may read questions with `check --all --types question`; the sweep keeps `check` outside its allow-list, and its two report sentences are corrected after PR #539 merges to state only what is established.

## What happens next if the owner picks it

- The ledger records "Q10: observer's alone for now, date"; `check` stays forbidden for the sweep (NFR-014; `probes.py:49-60`).
- SW-07 (wave W3, after the #539 merge) replaces the text at `report.py:199,534` with exactly: "This command reads no messages. A plain `check` consumes them. Whether `check --all --types question` consumes on a live Run is not established." and updates the tests that pin those strings in the same PR (`merged-requirements.md:196`).
- The question may be reopened by the owner after the observer's consumption evidence exists; nothing is scheduled for that.

## What it unlocks

- SW-07 can proceed in W3 with a fixed text; the sweep stops claiming a fact that is unproven (ADJ X-016, 61 percent, unproven both ways).
- Keeps the sweep's owner-signed allow-list unchanged, and keeps the two programs separate (one reader of questions).
- Matches the spec's default, so answering costs nothing beyond recording it.

## What it costs or risks

- "For now" leaves the long-term answer open; the question can come back.
- The corrected sentence says "not established", which itself becomes stale once OB-03 produces a result, so a second wording change may follow.
- A coordinator that has only the sweep open still sees no pending questions; it must open the observer (whose questions read is itself switched off until Q6 and its tests).

## What stays unresolved

Whether the sweep should ever read questions once consumption is measured; whether the observer's read is safe (Q6).
