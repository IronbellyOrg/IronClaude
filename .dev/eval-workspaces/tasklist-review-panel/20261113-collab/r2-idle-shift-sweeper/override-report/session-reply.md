| Status | Result |
|---|---|
| DONE | Added the override `TIME_CAP_EXCEPTION=1` (default off), re-pinned the new values and manifest, and wrote `OVERRIDE.md`. |
| DONE | Full suite: 448 passed, 0 failed (412 before, plus 36 new tests for the override on and off). |
| DONE | Ran one real smoke row on EL2 with the override on. |
| NEXT | Your decision on the EL2 sweeper start time (below). |

RUNS: the override, the stamps, the summariser separation and the launcher preflight. Nothing is stubbed.

**1. The override works, but only EL2 needs it.** The Spike 4 files on disk show k = 0 only for EL2. SL2 and HL2 are already k = 2 on all three packages, so for them the override changes no value, though their rows are still stamped. On EL2, k becomes 1. The hang guard becomes 3.0 times the baseline B_A1, for example 308.456 s on the control package. The exact numbers for all nine packages are in `OVERRIDE.md`.

**2. The smoke row delivered nothing.** The launch exited 0, the sweeper ran and posted 2 facts, and the identity, audit, anonymiser and judge checks passed. Elapsed time was 86 s against a 102.8 s baseline, so no extra time was even needed. But both facts arrived after each luna's last tool call, so AC-4 (at least one delivery) failed. I did not re-run it.

**3. Why, and what widening can't fix.** On EL2 the sweeper only starts when ember's review ends (about 59 s) and needs about 25 s to post. The lunas finish by themselves at about 80 s. Wider timers don't change that.

**4. Launch commands.** `OVERRIDE.md` section 5 has the collaboration and isolated-baseline commands for EL2, SL2 and HL2. The baseline rows carry the same stamp on purpose, because the summariser refuses to mix stamped and unstamped rows.

**RECOMMENDED ACTION:** Decide whether to start the EL2 sweeper at the beginning of the run (T0) instead of after ember, as SL2 and HL2 already do. That is a one-line change in `config/panels.json` and gives the sweeper about 59 s more lead time. The cost is 4 sessions at once on EL2, above your limit of 3 if the sweeper counts as a reviewer session. I did not make this change because it alters the session plan, not just the timers. Reply "start EL2 sweeper at T0" and I will make it and re-smoke, or run the `OVERRIDE.md` commands as they are.

Files are in `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper/`:
- `OVERRIDE.md`
- `tests/test_time_cap_exception.py`
- `spikes/s3-exception-smoke.sh`
- `config/manifest-exception.json`

Nothing was staged or committed. I did not run a shell linter beyond `bash -n`.
