<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (proposal-B) -->
<!-- Merge date: 2026-11-14 -->

<!-- Source: Base (original) -->
# Proposal B: not now; ask again later, and only then make storage a requirement

<!-- Source: Base (original) -->
## Answer

No sweep-facts panel now. The observer stays on the Orca ledger alone for the coming releases; if the owner later wants sweep facts on that screen, that "yes" turns Q9 (where the sweep's JSON lives) into a real requirement at that time.

<!-- Source: Base (original, modified): two bullets appended, per Change #2 and Change #1 -->
## What happens next if the owner picks it

- The ledger records "Q17: no, not now" with the date.
- OB-09 condition (3) is settled for now as "snapshot v1 only"; the soft edge from SW-11 to OB-09 stays inactive (merged-requirements.md lines 257, 708).
- SW-11 keeps Q9's own default: not now, Phase 2 caller-side capture first (ADJ line 779). Nothing about the sweep's files changes.
- The contract note (XC-05) keeps the rule that if a panel ever shows sweep rows, it prints the sweep's words verbatim and labels the report age (ADJ line 253), so a later "yes" has a rule waiting.
<!-- Source: Variant 1 (proposal-A), "What it costs or risks" bullet 4 (diff points U-001, C-005), merged per Change #2 -->
- The contract note also records that sweep facts are always older than live Orca rows (the coordinator sweep is capped at once per 5 minutes, a cap and not a schedule, ADJ line 81), so any later panel must show the report age prominently.
<!-- Source: round1-advocate-1, round1-advocate-2 and round1-advocate-3 (shared suggestion for base weakness U-002), merged per Change #1 -->
- The ledger also records a re-ask trigger: ask Q17 again when Q19 (which reviewer ask comes first) picks Decision Desk or OB-09 is scheduled, and only after PR #539 has merged.

<!-- Source: Base (original) -->
## What it unlocks

- Observer release 3 can be planned against one contract (observe snapshot v1) with no dependency on the open sweep PR (#539) or on any persistence decision.
- NFR-001 ("a sweep adds exactly one report file") and its two pinned tests stay as they are.
- Matches the debate's 78 percent judgement that the sweep JSON is a carrier for v2 and Coder#477, not the observer (ADJ line 361).

<!-- Source: Base (original, modified): mitigation sentence appended to the layout-rework bullet, per Change #3 -->
## What it costs or risks

- A person still needs two places to look: the observer for Orca state and the sweep report for proof-backed classes.
<!-- Source: Variant 1 advocate (round1-advocate-1, "Steelman of Variant 2" critique and "Suggested merge"), final sentence merged per Change #3 -->
- The question comes back later; if Decision Desk is designed first without sweep facts, adding them later may mean reworking its layout. Mitigation: one sentence in OB-09 asks the Decision Desk layout to leave room for a possible sweep-facts area.
<!-- Source: Base (original, modified): reworded by the orchestrator after merge to resolve contradiction C-1 in merge-log.md (Change #1 adds the trigger) -->
- "Not now" could drift into "never" without a decision; the re-ask trigger recorded in the ledger (above) is what prevents that, so the trigger must actually be written down when Q17 is answered.

<!-- Source: Base (original, modified): one bullet appended, per Change #4 -->
## What stays unresolved

- Whether the observer should ever show sweep facts.
- The persistence decision (Q9), left at its default.
<!-- Source: Variant 3 (proposal-C), "What happens next" bullet 4 and "What stays unresolved" (diff point C-004), merged per Change #4 -->
- Where a person sees Orca state and sweep classes together, if anywhere. A possible home is Orchestrator v2, which is linked to sweep facts through SW-11 (merged-requirements.md line 200) but is unbuilt.
