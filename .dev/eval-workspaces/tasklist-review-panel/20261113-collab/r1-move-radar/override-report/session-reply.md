| Status | Result |
|---|---|
| DONE | `TIME_CAP_EXCEPTION=1` override added to Move Radar (r1) and written up in `OVERRIDE.md`. |
| DONE | All 167 tests pass (138 old, 10 from the separate slack session, 19 new). Lint and `bash -n` clean. |
| DONE | One real smoke row, `el2-c1x-r0` (el2, design package), ran with exit 0. All 7 smoke conditions and my 6 override checks hold. |
| NEXT | Run the full override rows for el2, hl2 and sl2 with the commands in `OVERRIDE.md` section 8. |

**How it works.** Where a role's measured k is 0, it gets k = 1; roles with k of 1 or 2 keep theirs. Hang guard = max(old, 3.0 × B_A1). Finish offset moves by the same amount. The no-injection guard is set equal to the finish offset. The old guard is negative on all hl2 packages and on sl2 designSpec, so without that change nothing would ever have been injected there. With the override off, every value is unchanged.

**Rows and stamps.** Override rows get the id `<panel>-c1x-r<rep>`, so they never mix with `-c1-` rows. They carry `time_cap_exception: true`, B_A1, elapsed, the elapsed/baseline ratio, forced k, and messages delivered per reviewer. `alarms.py` lists them in a separate section and leaves them out of every arm-level check. The per-package numbers for all nine panel/package cells are in `OVERRIDE.md` section 2.

**Smoke result.**
- Elapsed 106.0 s, which is 1.09 × B_A1.
- Ember got M2 at call 6, and one luna got M8 at call 8.
- The other luna ended after 5 calls and never reached its checkpoint, so it received nothing. Forcing k = 1 cannot help a reader that finishes before call 8. Lowering the reader checkpoint is a separate decision I did not make.

**Pins.** Nothing the design pins was edited, so there was nothing to re-pin. I ran `gate0-check.sh` and every gate now reads pass. Nothing was staged or committed.

**Overlap with another session.** The `launch-slack.sh` session was editing `values.py`, `launch.sh` and `alarms.py` in this same folder (a `PANEL_SLACK_S` change, documented in its own `SLACK.md`). It finished at 12:25 UTC. My edits sit on top of its version and the suite passes with both. I did not test combining the two switches; run override rows with `PANEL_SLACK_S` unset.

**RECOMMENDED ACTION:** Run the el2 override row first. This gives it a rep-1 row to compare against the existing `el2-c0-r1`:

`cd /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel && TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 bash .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh el2 1`

The hl2 and sl2 commands, and the baseline commands, are in `OVERRIDE.md` section 8.
