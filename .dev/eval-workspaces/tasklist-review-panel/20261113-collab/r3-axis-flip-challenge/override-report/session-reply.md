| Status | Result |
|---|---|
| DONE | The override `TIME_CAP_EXCEPTION=1` is built. Default is off, and with it off nothing changes. |
| DONE | Full test suite: 122 passed, 0 failed, 0 skipped (102 existing plus 20 new). Ruff is clean. |
| DONE | One real smoke row on el2, design package, override on: exit 0, all 15.5 checks pass. |
| DONE | `OVERRIDE.md` is written with files and lines, numbers, smoke result and launch commands. |
| NEXT | Run the real el2, hl2 and sl2 rows (commands below). |

**What the smoke did not prove:** the forced 0-to-1 step did not fire on real models. Both lunas finished early (76.5 s and 89.1 s), so their measured n was already 1. On real models the smoke exercised the widened timers, the stamps and columns, phase 2 on ember and luna, and both judges. The 0-to-1 step itself is shown only on the fake `claude` and in unit tests. In real rows, look for `forced_applied: true`.

**How the override works (this design uses n, not k):**
- A measured n of 0 becomes 1 (never lowered, never above the receiver's cap), while the widened deadline still has room for it.
- Hang guard is `max(1.5 x B_f, 3.0 x B_A1)`.
- Phase-2 deadline is `max(old, hang guard + 16 s + 2 x n x largest turn)`. For el2 design that is 413.4 s and 453.8 s.
- Finish offset is `3.0 x B_A1 - turn - T_report` (el2 design: 160.3 s to 387.7 s).
- Per-package numbers for all three panels are in `OVERRIDE.md`.

**Stamps and summary:**
- Rows carry `time_cap_exception: true`, plus B_A1, elapsed, ratio, forced n and delivered per reviewer.
- The summariser reports those rows in a separate section and never mixes them into the cap-obeying arms or the cap check.
- The override is refused with `PANEL_COLLAB=0` and with `R3_SPIKE4=1`.

**Pins:** no re-pin was needed. I did not touch anything pinned (judge script, parser, ledger, merge command, `config/`), and `pin --check` prints `pins ok`.

**Deviation from 15.5:** with the override on, the smoke loads the frozen values file instead of planning values. Without the override, smoke is unchanged.

**RECOMMENDED ACTION:** run the three collaboration rows from this folder (`.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge`), then check `forced_applied` and `delivered` per reviewer in each row. Run the matching isolated baselines without the override.
```bash
flock /tmp/collab-gateway.lock env NOFALLBACK=1 TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 bash bin/launch-panel.sh el2   # then hl2, sl2
flock /tmp/collab-gateway.lock env NOFALLBACK=1 PANEL_COLLAB=0 bash bin/launch-panel.sh el2                       # baseline; then hl2, sl2
```

**Skipped or not checked:**
- A delivered count of 0 is still possible with n of 1. In the smoke, luna `t3-1` got no slots, which the override does not change.
- The luna kill-salvage problem (AC-3) is still open.
- Nothing was staged, committed or pushed.
