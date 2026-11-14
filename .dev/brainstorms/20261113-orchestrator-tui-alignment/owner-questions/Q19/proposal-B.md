# Proposal B: pick no first ask yet; decide when release 3's gates are met

## Answer

Do not pick a first ask now. Leave OB-09 unstarted (the spec's default) and choose the first ask only after QUESTION-LINK is established, the questions read is switched on (OB-06) and your direction-selection record (AC-S, OB-02) exists.

## What happens next if the owner picks it

- The ledger records "Q19: deferred until release 3's gates are met" with the date.
- OB-09 does not start (merged-requirements.md line 546). Nothing is added to `release-gates.md` for the four asks yet.
- The #409 correction pass keeps the planned sentence that the place where the four asks are built is still to be decided (ADJ line 557, BC-15).
- Q19 is asked again when QUESTION-LINK, OB-06 and OB-02 are all recorded.

## What it unlocks

- No commitment while every release 3 prerequisite is open: QUESTION-LINK is "Not established" (variant-5-original.md line 65), the questions read is off on master (ADJ line 187), and AC-S does not exist (ADJ line 187).
- The choice is made with the real state of the data sources in view, including the shared capture (XC-03) and the contract note (XC-05, XC-07).
- No work is spent on an ask whose data source is unknown (Fleet Quilt) or missing (links).

## What it costs or risks

- The reviewer's comment of 2026-11-11 stays without an answer on priority; none of the four asks moves.
- Release 3 planning has no stated first target, so its design may drift toward whatever is easiest rather than what the reviewer valued.
- When the gates open, the question returns as one more owner decision on the critical path.

## What stays unresolved

- Which ask comes first and in which program.
- Whether the deterministic summary option (review 01 F-08) is ever used.
