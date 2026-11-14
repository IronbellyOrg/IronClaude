<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (proposal-A) -->
<!-- Merge date: 2026-11-14 -->

<!-- Source: Base (original) -->
# Proposal A: not yet; open the channel only at observer release 4 or when a TUIBBS screen is planned

<!-- Source: Base (original) -->
## Answer

No copy channel now. The channel (CO-04) opens only when the observer reaches its release 4 (the remote fleet) or the owner states that a TUIBBS screen is planned; until then the observer stays single-host.

<!-- Source: Base (original, modified); reason: four bullets extended or reworded per Changes #1, #2, #4 and #5 -->
## What happens next if the owner picks it

<!-- Source: Base (original, modified); reason: ledger-authority sentence appended from round1-advocate-2.md A-002 (Variant 2 advocate), merged per Change #5 -->
- The ledger records "Q18: not before R4 or a TUIBBS statement" with the date. The ledger is the authoritative record; the Coder#477 sentence below only repeats it.
<!-- Source: Base (original, modified); reason: wording replaced per round1-advocate-1.md Concessions 4 and round1-advocate-3.md C-002 (Variant 1 and Variant 3 advocates), merged per Change #2; base citation kept -->
- The Coder#477 reply (CO-01) states that no channel exists and one is deferred until observer release 4 or an owner decision on a TUIBBS screen (merged-requirements.md line 353, "the channel per Q18").
<!-- Source: Base (original, modified); reason: Variant 2 "What it costs or risks" bullet 1 (data exposure) merged per Change #1 -->
- CO-04 stays deferred with its two triggers written in (line 356). When a trigger fires, CO-04's design must name five things before any code: a transport, an identity envelope, an age rule (Q22) and a re-sanitising step (ADJ line 306), and who may read a copy, because the snapshot is written with mode 0600 on purpose (ADJ line 244), including whether the whole snapshot or only part of it leaves the host.
<!-- Source: Base (original, modified); reason: Variant 2 "What happens next" bullet 5 (guard sentence) merged per Change #4 -->
- The contract note keeps "single owner, single OS user, single host" (line 453) and adds one guard sentence: any future copy off this host is read-only and may start only after CO-04's design names all its pieces.

<!-- Source: Base (original, modified); reason: third bullet reworded per Change #3 -->
## What it unlocks

<!-- Source: Base (original) -->
- CO-01 can be posted with a settled channel sentence.
- Keeps every current item on one host, matching the spec's out-of-scope list (line 145) and the owner's own "background, not deciding" record (ADJ line 306).
<!-- Source: Base (original, modified); reason: overclaim removed per round1-advocate-1.md Concessions 3 (Variant 1 advocate), merged per Change #3 -->
- Leaves the snapshot's TUIBBS-ready shape in place, so a later channel starts from the existing file; whether the identity and age pieces need new fields in it is not yet decided.

<!-- Source: Base (original, modified); reason: orchestrator edit after merge to resolve contradictions C1 and C2 in merge-log.md (five pieces after Change #1) -->
## What it costs or risks

- If the owner does want a TUIBBS screen soon, the five missing pieces (transport, identity, age, re-sanitising, who may read a copy) are designed later rather than now.
- "Or an owner statement" relies on the owner remembering to say it; nothing prompts it except Q4 (line 1177).
- Coder#477's text may need a second edit when the channel opens.

<!-- Source: Base (original) -->
## What stays unresolved

- Whether a TUIBBS screen will ever exist.
- The transport and identity design.
