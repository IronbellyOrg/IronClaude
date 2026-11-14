# Proposal C: Fleet Quilt or Decision Desk first, in the observer, after the contract note and the shared capture

## Answer

The first ask is Fleet Quilt or Decision Desk (you name which), built in the observer as a new release row, and started only after the contract note between the observer and the sweep is final and the shared read-only Orca capture is recorded.

## What happens next if the owner picks it

- The ledger records "Q19: <Fleet Quilt or Decision Desk> first, in the observer, after XC-07 and XC-03" with the date. XC-07 is the step that links and finalises the contract note; XC-03 is the one read-only recorded session against live Orca.
- One row is added to the observer's `release-gates.md` for the chosen ask, with its data gate, as review 05 recommended (variant-5-original.md lines 252 to 254).
- If Decision Desk: it remains release 3 and still needs QUESTION-LINK, the questions-read switch-on (OB-06) and the AC-S record (OB-02) (merged-requirements.md line 257; graph row 59). If Fleet Quilt: its data gate must be written into its new row first, since no source records what it reads.
- OB-09's condition (2) ("Q19 names the first ask and its program") is met.

## What it unlocks

- Follows the order the reviewer values, as review 05 read it ("Fleet Quilt and Decision Desk first", line 252), and the spec's recommendation (line 546).
- Keeps the asks in the program the reviewer was looking at (the observer dashboard), so no other program changes its scope.
- Starting after the note and the capture means the release is designed against confirmed field meanings, not guesses.

## What it costs or risks

- Leaves the final choice between two asks to you, so one more small decision remains.
- Decision Desk is blocked on QUESTION-LINK, which is not established; if you pick it, nothing moves until that gate opens.
- Fleet Quilt has no recorded data source in the sources read; its first step is discovering what it needs.
- The summary, named steps and links, the asks with a known deterministic source (review 01 F-08, F-10), wait.

## What stays unresolved

- Which of the two comes first.
- Where the summary and links will be built.
