# Final gate decision (item 14.32)

Final gate: PASS by owner ruling, open: FIN-F7

## How this outcome was reached

- Cycle 2 (`cycle2-decision.md`): F_2 = {FIN-F7}, |F_2| = 1, below |F_1| = 2; no check of the cycle-1 PASS set regressed; all 238 checks pass in both cycle-2 verifier reports; FIN-F5 is resolved.
- `|F_2|` is not 0, so the hard cap of two fix cycles applied. The plan's rule gave a HALT with the open finding FIN-F7 (recorded in the plan's Execution Log as the item 14.32 HALT row, and in `cycle-ledger.md` row 2). The HALT rule was applied (plan status Blocked, `blocker_reason` set, item not ticked) and the open MAJOR finding was escalated to the owner.
- The owner ruled FIN-F7 a documented limitation on 2026-11-12 (`phase-outputs/plans/FINAL-GATE-FIN-F7-ruling.md`). The HALT is resolved by that ruling (HALT RESOLVED row in the Execution Log); the plan status is back to Doing.

## The open finding

- FIN-F7 (MAJOR): the chat reply of the exempt `/sc:sweep` run prints the summary counts and the report path alone, so an exit 0 run during an Orca outage reads like a normal run there. The report at the printed path states the outage, and the skill requires the session to Read that report to its last line first. Fixing it needs an edit of `src/superclaude/output-styles/pragmatic.md` (the sweep exception, 7 sites), the revision addendum, DESIGN 7.6 and the tests. It goes into the follow-up issue.

## Ledger

`cycle-ledger.md` has the cycle-0 row, the halted cycle-1 row, the re-check cycle-1 row and the cycle-2 row.
