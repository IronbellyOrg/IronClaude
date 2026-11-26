| Status | Result |
|---|---|
| DONE | Override added: `TIME_CAP_EXCEPTION=1` (default off) forces `k = 1` where the measured `k` is 0, hang guard `max(existing, 3.0 x B_A1)`, finish signal at `2.7 x B_A1 - turn - report`. Off-mode numbers are unchanged. |
| DONE | Every exception row is stamped `time_cap_exception: true` and records B_A1, elapsed, elapsed/baseline, k measured/forced/run and messages delivered per reviewer. The summariser refuses to mix stamped and unstamped rows. |
| DONE | Pins: nothing pinned changed, so nothing was re-pinned. A `pins-check.sh --write` into a scratch file is identical to `pins.json`, and `pins-check.sh` is 18 of 18 OK. |
| DONE | Tests: 160 passed (125 existing plus 35 new) and ruff is clean. After that full run I renamed two new tests for lint and re-ran only the new file, which passed. |
| DONE | One real smoke row passed all 8 checks: `smoke-tcx-el2-1` (el2, `TASK-WF-design-20261108-041415`, override on, `NOFALLBACK=1`). |
| NEXT | Orchestrator runs the full rows with the commands in OVERRIDE.md section 7. |

**Smoke details:**
- **Cards:** ember finished at 57 s and the watcher posted a card to each luna. One luna received and acted on its card.
- **Late card:** the other luna had made its last tool call at 54 s, before the card was posted, so its card is marked `late`. Expect this on el2 because ember finishes first.
- **Elapsed time:** the row took 105.8 s, which is 0.91 x baseline, so the widened guards never fired on a real model. Only the fake-`claude` tests exercise them.

**Numbers:** on all six el2 and hl2 packages `k` goes 0 to 1 and the hang guard becomes 3.0 x B_A1 (for example, el2 design 175.2 s to 350.3 s). OVERRIDE.md section 2 has the full per-package table.

**Preflight change:** the kit-slowdown check (`budget_ok`) is the one launch check that changes with the override on. It is re-evaluated against the widened cap and passes on all six packages; it was false on el2 design and hl2 designSpec. I did not waive it.

**Limits:**
- **Panels:** sl2 is not covered. It has no frozen Spike 4 values, so `launch.sh sl2` still exits 3. I covered el2 and hl2 only.
- **Baseline:** the isolated baseline row must run without the variable. A baseline with the variable set is refused (exit 2).
- **Slack:** the override cannot be combined with `PANEL_SLACK_S`.
- **Not run:** the A1 smoke row (design item 5) and the full three-package rows.

RUNS: `launch.sh` with the override on, for el2 and hl2 (el2 package run for real; the rest covered by fake-`claude` tests). NOT BUILT: sl2 values, edits to `DESIGN.md` and `IMPLEMENTATION.md`.

**RECOMMENDED ACTION:** run the el2 collaboration row first (OVERRIDE.md section 7, `f6x-el2-r01`). Then the matching baseline `a1x-el2-r01`, and compare using `messages_delivered`, not `k`, because `late` cards will occur. Start hl2 only after el2 looks sane, since hl2 designSpec can run up to 662.8 s per package.

Everything is in `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r5-coverage-deflection/`; the report is `OVERRIDE.md`.
