# Proposal C: never; the observer reads Orca only, by design

## Answer

No, as a standing boundary: the observer shows the Orca ledger and coordinator questions only, and never reads the sweep's report or JSON. Sweep facts are shown by the sweep's own report and, later, by Orchestrator v2; the contract note records this as a rule, not a postponement.

## What happens next if the owner picks it

- The ledger records "Q17: never (boundary)" with the date.
- OB-09 condition (3) is fixed as "snapshot v1 only"; the SW-11 to OB-09 edge is removed rather than left soft (merged-requirements.md lines 257, 708).
- The contract note (XC-05) states: the observer reads no sweep output; the sweep reads no observer output. The verbatim-words rule for a sweep panel (ADJ line 253) is kept only as history.
- SW-11 (sweep JSON storage) is decided on v2's and Coder#477's needs alone (ADJ line 361 names those as the only candidate carriers).

## What it unlocks

- The cleanest separation of the two programs: two collectors with two contracts and no reader crossing between them, which removes the risk of mixing "stale", "historical" and `null` versus `"UNKNOWN"` on one screen (ADJ lines 131, 250 to 256).
- The observer's release planning never waits on the sweep, its merge or its persistence.
- No future reviewer reopens the question by default.

## What it costs or risks

- Closes a door that reviews 01 and 04 wanted kept open "eventually, for facts only the sweep has" (round2-rebuttal-V5.md line 69).
- A person deciding what to do about a worker must always read two outputs.
- If Decision Desk later proves it needs safe-to-close or frozen-plan facts, the owner must reverse a written boundary, not just answer a deferred question.
- Goes further than the debate: its 78 percent judgement was about "now", not "ever" (ADJ line 361).

## What stays unresolved

- Where a person sees Orca state and sweep classes together, if anywhere (likely v2, which is unbuilt).
