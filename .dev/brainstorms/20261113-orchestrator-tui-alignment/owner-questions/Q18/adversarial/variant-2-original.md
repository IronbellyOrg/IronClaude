# Proposal B: yes; state now that a TUIBBS screen is planned and open the channel design

## Answer

Yes. The owner states that a TUIBBS screen is planned, which is one of the two triggers for CO-04, so the design of the snapshot copy channel starts now: transport, identity envelope, age rule and re-sanitising, before any code.

## What happens next if the owner picks it

- The ledger records "Q18: yes; TUIBBS screen planned" with the date.
- CO-04 opens as a design item (merged-requirements.md line 356). Its design names: how the snapshot leaves the Coder workspace for the separate SSH host (transport); who and which workspace a copy came from (identity envelope; today `scope` is only `object` or `"UNKNOWN"`, ADJ line 306); how old a copy may be before it is shown as stale (age rule, which needs Q22's number); and re-sanitising the strings on the TUIBBS side.
- Q22 (what age makes a snapshot stale) becomes needed now rather than later.
- The Coder#477 reply (CO-01) says a read-only, identity-tagged, aged copy of the observer snapshot is planned and that nothing can be sent into a workspace (ADJ line 306, the "designed for a copy" reading).
- The contract note's "single host" line gains a sentence that copies to the TUIBBS host are read-only and identity-tagged.

## What it unlocks

- The snapshot was shaped for exactly this reader (ADJ glossary line 91); this puts that design to use.
- Gives Coder#477 a concrete, read-only purpose if it is kept or narrowed (Q3), instead of an unclear one.
- Settles the transport early, so the TUIBBS screen and the observer do not each invent their own.

## What it costs or risks

- Crosses a host boundary that every other item stays inside (merged-requirements.md line 145, out of scope until later). The snapshot holds worker rows and Orca strings and is written with mode 0600 on purpose (ADJ line 244); copying it off the workspace widens who can read it.
- Contradicts the owner's own recorded stance, "Background, not deciding" (ADJ line 306), unless the owner now changes it.
- No TUIBBS document mentions Coder or Orca (round2-rebuttal-V5.md line 20), so the receiving side is undesigned.
- Pulls Q22 and an authentication design forward; the spec says no transport is chosen until Q4, Q18 and real authentication behaviour are settled (line 375).

## What stays unresolved

- Which transport (copy, pull, push) and which credentials.
- Whether the TUIBBS screen itself gets built.
