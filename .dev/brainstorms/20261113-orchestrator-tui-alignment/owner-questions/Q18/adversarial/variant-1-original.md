# Proposal A: not yet; open the channel only at observer release 4 or when a TUIBBS screen is planned

## Answer

No copy channel now. The channel (CO-04) opens only when the observer reaches its release 4 (the remote fleet) or the owner states that a TUIBBS screen is planned; until then the observer stays single-host.

## What happens next if the owner picks it

- The ledger records "Q18: not before R4 or a TUIBBS statement" with the date.
- The Coder#477 reply (CO-01) states that no channel to the TUIBBS host exists or is planned yet (merged-requirements.md line 353, "the channel per Q18").
- CO-04 stays deferred with its two triggers written in (line 356). When a trigger fires, CO-04's design must name four things before any code: a transport, an identity envelope, an age rule (Q22) and a re-sanitising step (ADJ line 306).
- The contract note keeps "single owner, single OS user, single host" (line 453).

## What it unlocks

- CO-01 can be posted with a settled channel sentence.
- Keeps every current item on one host, matching the spec's out-of-scope list (line 145) and the owner's own "background, not deciding" record (ADJ line 306).
- Leaves the snapshot's TUIBBS-ready shape in place, so a later channel needs no change to the observer's file.

## What it costs or risks

- If the owner does want a TUIBBS screen soon, the four missing pieces (transport, identity, age, re-sanitising) are designed later rather than now.
- "Or an owner statement" relies on the owner remembering to say it; nothing prompts it except Q4 (line 1177).
- Coder#477's text may need a second edit when the channel opens.

## What stays unresolved

- Whether a TUIBBS screen will ever exist.
- The transport and identity design.
