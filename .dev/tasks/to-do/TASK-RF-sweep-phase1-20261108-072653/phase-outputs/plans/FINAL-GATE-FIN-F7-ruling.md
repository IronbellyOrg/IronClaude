# Final gate, item 14.32 halt: owner ruling on FIN-F7 (2026-11-12)

Status: RULED by the owner. Chosen: documented limitation (the recommended action).

## Context

The final QA gate reached its two-fix-cycle cap with one open MAJOR finding: FIN-F7. The chat reply of the exempt `/sc:sweep` run prints the summary counts and the report path alone, so an exit 0 run during an Orca outage reads like a normal run in that reply. The report at the printed path states the outage, the skill requires the session to Read that report to its last line first, and the lower-bound note still prints with the counts. Fixing it needs edits of `src/superclaude/output-styles/pragmatic.md` (the sweep exception, 7 sites), the revision addendum, DESIGN 7.6 and the tests.

## Owner's words

The owner pasted back the recommended action as their answer ("I record the ruling in the gate decision and write Final gate: PASS by owner ruling, open: FIN-F7. I set the plan back to Doing and tick 14.32. FIN-F7 goes into the follow-up issue, with the fix list above as its starting point. The run continues to the fidelity gate (14.33 to 14.45)").

## Ruling

- FIN-F7 is a documented limitation of Phase 1. It is not fixed in this run.
- Gate decision: `Final gate: PASS by owner ruling, open: FIN-F7`.
- The plan returns to "Doing", item 14.32 is ticked, the run continues to the fidelity gate (items 14.33 to 14.45).
- FIN-F7 goes into the end-of-run follow-up issue with its fix list: edit the sweep exception in `pragmatic.md` (7 sites) to allow one outage line in the exempt reply, the revision addendum (`design-addendum.md` lines 29 and 37), DESIGN 7.6 `:663` (step 3 takes `orca_available`; the line was `:662` before the owner edit of line 614), the skill steps 3 and 4 and their pins, then re-verify.
