| Status | Result |
|---|---|
| DONE | I wrote the design for the Idle-Shift Sweeper (Redesign 2) to `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper/DESIGN.md`. It is 750 lines and covers all 7 items you asked for. |
| DONE | Three independent reviews ran. Review 1 found 8 blocking defects and review 2 found 2 more; all were fixed. Review 3 passed with 0 blocking defects. The reviews are in `design-report/review-1.md` to `review-3.md`. |
| DONE | Wrote the worker contract: `design-report/return-contract.yaml`, status `succeeded`. |
| NEXT | Confirm or change the sweeper model for the sonnet and haiku panels (below), then build it with `/sc:implement` using DESIGN.md as the spec. |

NOT BUILT: all of it. This is a design only: no scripts, tests or spike results exist yet, and no model was run.

**Three choices I made where the source didn't fit your panels:**
- **The search helper on sonnet + 2x luna and haiku + 2x luna is an ember session started at the beginning.** The source has ember search during its idle time after its own review. Sonnet and haiku take 14 to 23 s per turn and finish after the lunas, so their facts would arrive too late. `SWEEPER_MODEL` can override this with any allowed model.
- **The number of facts each luna gets is worked out from luna's own timings.** On ember + 2x luna this is exactly the source formula. On the haiku panel, the source formula taken as written gives 0 facts, which would turn the design off.
- **Only the two lunas get hooks.** So the "finish now" message never cuts short a sonnet or haiku review whose work the design does not change.

**Other points:**
- **Judge output stays out of the earlier eval folder.** The unchanged `judge-one.sh` is called with a relative folder argument, so its scores land under the r2 folder.
- **The judge can tell these rows come from the new harness**, but not which ones are collaboration and which are the baseline. Compare collaboration rows only with baseline rows from this same harness.

RECOMMENDED ACTION: Read the "Open questions" table (section 7.2, Q-1 to Q-3) in DESIGN.md and confirm the defaults. Q-1, the ember helper on the sonnet and haiku panels, decides what those two panels actually measure.

Not checked: whether hooks fire on the gateway models, the model act rates, and all timing values. These are left to the Gate 0 spikes in section 6.3. There are no gain estimates for the sonnet and haiku panels, so their results are exploratory.
