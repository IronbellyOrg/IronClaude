# Proposal C: its own state, shown with Orca's word, until its meaning is known

## Answer

`reclaimable` is its own state: neither program calls it live or historical. Readers show Orca's word `reclaimable` as it is, and the contract note records that its side of the line is undecided until Orca's meaning is confirmed.

## What happens next if the owner picks it

1. The contract note draft (XC-05) writes the mapping row ADJ already drafted: "the note decides which side of 'historical' `reclaimable` is (Q23); until then show Orca's word `reclaimable` and do not call it live or historical" (ADJ line 258), with "Q23 answered: its own state" and the date.
2. No code change now. The observer keeps reclaimable rows in its default view (`view.py:35`), but no text calls them live; the sweep keeps "could not determine" for safe-to-close (`classify.py:479-481`).
3. OB-06 prerequisite (e) is met by the row in the note draft or the observer spec.
4. The question is reopened when Orca's meaning is recorded, for example by adding one line to the shared read-only capture (XC-03): the help text or a detail read of one reclaimable worker.

## What it unlocks

- OB-06 and XC-05 proceed now without deciding a meaning nobody has confirmed (Orca's definition is UNVERIFIED in every file read).
- No code change and no wrong claim: a person sees the exact word Orca uses.
- Leaves both later choices open (hide it as historical, or keep it as awaiting release) at no cost.

## What it costs or risks

- The observer's default view is unchanged, so it can still be filled with finished workers (27 reclaimable, 0 active at the probe, INV-023); "its own state" names the problem without fixing it.
- "Its own state" is a non-answer to a reader who asks "is this worker still running?"; the meaning is deferred, not settled.
- A provisional row needs someone to revisit it; without a trigger it can stay provisional indefinitely.

## What stays unresolved

- Which side of "historical" `reclaimable` belongs on, and Orca's own definition.
