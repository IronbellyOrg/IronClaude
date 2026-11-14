# Proposal A: yes, plan a sweep-facts panel for the observer's release 3

## Answer

Yes. The observer's release 3 (Decision Desk) should show the sweep's facts that only the sweep has (frozen plans, safe-to-close, waiting-on-a-person, git state) next to the Orca ledger, read from a captured copy of the sweep's JSON and labelled with the report's age.

## What happens next if the owner picks it

- The ledger records "Q17: yes" with the date.
- Q9 (where the sweep's JSON lives) becomes a real requirement now, not a someday item: SW-11 must choose caller-side capture of the sweep's stdout first (Q9's own recommended first step, ADJ line 779) or a stored file (which means relaxing NFR-001, "a sweep adds exactly one report file", and changing its two pinned tests).
- OB-09 condition (3) is settled as "reads snapshot v1 and sweep facts", so release 3 depends on SW-11 (merged-requirements.md line 257; graph row 61).
- The contract note (XC-05) gains a section on how the observer reads sweep rows: the sweep's words printed verbatim and the report age shown (ADJ line 253).

## What it unlocks

- One screen for a person deciding what to do next: the Orca state of a worker and the sweep's proof-backed class (for example "safe to close: could not determine") side by side. Reviews 01 and 04 asked for this "eventually, for facts only the sweep has" (round2-rebuttal-V5.md line 69).
- Gives Decision Desk content the observer cannot get any other way (ADJ line 240: the observer owns none of these facts).

## What it costs or risks

- Persistence work moves forward: either a capture step in every coordinator sweep pass or a change to a pinned design rule (NFR-001).
- The debate judged at 78 percent that the sweep JSON is not a carrier for the observer (ADJ line 361); this answer goes against that.
- A second data source with different words ("stale", "historical", `null` versus `"UNKNOWN"`) on one screen invites misreading (ADJ lines 131, 250 to 256).
- The sweep is not merged (PR #539 open), and its report changes only when a coordinator runs it (capped at once per 5 minutes), so sweep facts on a live screen are always older than the Orca rows beside them.

## What stays unresolved

- Capture versus stored file (Q9).
- Which sweep facts, exactly, and how old a report may be before it is hidden (Q22, the staleness age question).
