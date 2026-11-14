# Proposal B: not now; ask again later, and only then make storage a requirement

## Answer

No sweep-facts panel now. The observer stays on the Orca ledger alone for the coming releases; if the owner later wants sweep facts on that screen, that "yes" turns Q9 (where the sweep's JSON lives) into a real requirement at that time.

## What happens next if the owner picks it

- The ledger records "Q17: no, not now" with the date.
- OB-09 condition (3) is settled for now as "snapshot v1 only"; the soft edge from SW-11 to OB-09 stays inactive (merged-requirements.md lines 257, 708).
- SW-11 keeps Q9's own default: not now, Phase 2 caller-side capture first (ADJ line 779). Nothing about the sweep's files changes.
- The contract note (XC-05) keeps the rule that if a panel ever shows sweep rows, it prints the sweep's words verbatim and labels the report age (ADJ line 253), so a later "yes" has a rule waiting.

## What it unlocks

- Observer release 3 can be planned against one contract (observe snapshot v1) with no dependency on the open sweep PR (#539) or on any persistence decision.
- NFR-001 ("a sweep adds exactly one report file") and its two pinned tests stay as they are.
- Matches the debate's 78 percent judgement that the sweep JSON is a carrier for v2 and Coder#477, not the observer (ADJ line 361).

## What it costs or risks

- A person still needs two places to look: the observer for Orca state and the sweep report for proof-backed classes.
- The question comes back later; if Decision Desk is designed first without sweep facts, adding them later may mean reworking its layout.
- "Not now" has no trigger written down; it may drift into "never" without a decision.

## What stays unresolved

- Whether the observer should ever show sweep facts.
- The persistence decision (Q9), left at its default.
