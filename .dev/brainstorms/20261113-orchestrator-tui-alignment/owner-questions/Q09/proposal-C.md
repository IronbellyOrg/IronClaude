# Proposal C: neither, as a standing rule: the sweep JSON is never stored by the sweep or its callers

## Answer

No: the sweep's JSON stays a one-time answer printed to the caller and is never stored; SW-11 is closed as "will not do", and any later reader works from the dated Markdown report or asks for its own status source.

## What happens next if the owner picks it

- The ledger records "Q9: neither, date"; SW-11 is removed from wave W5 and its row in the #534 follow-up table (SW-06) is closed with that reason.
- NFR-001, its design line and its two pinned tests stay exactly as they are, now as a settled rule rather than a Phase 1 limit.
- The contract note (XC-05) states that sweep report JSON v1 is a stdout-only reply with no stored form.
- If v2 (#423) or a Coder#477 status record later wants stored facts, that is a new owner question, not a revival of SW-11.

## What it unlocks

- Removes one open decision and one deferred work item from the program for good.
- Keeps the observer and the sweep separate (ADJ X-013, X-017: no observer reader of the sweep JSON), so nobody builds against a stored sweep file.
- Avoids a store with no named reader, owner, retention or file mode (v2's own rewrite requires all four, `merged-requirements.md:401`).

## What it costs or risks

- If v2 or a status record does need sweep facts, the answer has to be reopened, and the closure may have to be explained.
- Readers of past sweeps must parse Markdown, which is not a stable machine format.
- Q17 (observer showing sweep facts) effectively becomes "no" as well, since there would be nothing stored to read.
- Callers may still save stdout on their own; "never stored by callers" is an instruction, not something the sweep can enforce.

## What stays unresolved

Where a future v2 would get sweep facts if it needs them.
