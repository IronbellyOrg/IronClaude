| Status | Result |
|---|---|
| DONE | `TIME_CAP_EXCEPTION=1` override added (default off) and the pins re-checked. The pin check passes. |
| DONE | Full test suite: 124 passed, 0 failed (106 existing, 9 new override tests, 9 from another session's slack change). |
| DONE | One real smoke row on EL2, control package, override on: all 38 checks pass. |
| DONE | `OVERRIDE.md` written, with the numbers, the smoke result and launch commands for EL2, HL2 and SL2 plus the baseline commands. |
| NEXT | Run the three collaboration rows and the three baseline rows from `OVERRIDE.md` section 7. |

**What the override does.** With `TIME_CAP_EXCEPTION=1`, any package whose measured `k` is 0 runs with `k = 1`. `k` is the number of messages each adjudicator can receive. The hang guard becomes `max(old, 3.0 × B_A1)`, and the finish time keeps its old distance to the guard. For EL2's control package that is hang 342.363 s and finish 229.22 s. All nine panel and package numbers are in `OVERRIDE.md` section 2. With the override off, no computed value changes; a test checks this against the values file.

**Stamping and summary.** Rows are stamped `time_cap_exception: true` in the run, panel, collab and results files. The columns are B_A1, elapsed, the ratio, the forced `k`, and delivered messages per reviewer. The summariser reports exception rows in their own block and never mixes them into the cap-obeying figures.

**Refusals.** The launcher refuses the override with `PANEL_COLLAB=0`, with planning or `-srun` values, or when `deliver` is false.

**Re-pin.** I re-pinned `values.py`, `results.py` and `arm_summary.py` only. Every other check is untouched: `NOFALLBACK=1`, the observed-model check, the audit checks, and the blind judge.

**Smoke result.** The row `tce-smoke-f7-el2-1` ran in 111.4 s against a 114.1 s baseline, a ratio of 0.976. Two cards were sent and two delivered, one to each luna, and the finish signal never fired. Only one of the two lunas visibly settled its card: `t3-1` wrote "card c1: passed", while `t4-1` neither converted its card nor wrote a passed line. This row does not show the cost of the exception, since it was no slower than the baseline.

**Concurrent session.** Another session edited `values.py`, `arm_summary.py`, `run-panel.sh` and the pins in this same folder at 12:33 for a "30 s slack" decision (`SLACK.md`). The two changes coexist. My first full test run had 5 failures because that session re-pinned mid-run; the rerun on stable files passed.

Not checked: the SL2 and HL2 smoke rows, which share the code path but ran only offline, and the override combined with `PANEL_SLACK_S=30`. `lib/` is git-ignored here, so committing the edited files needs `git add -f` on the design's `lib/` folder. I staged and committed nothing.

**RECOMMENDED ACTION:** Run the EL2 row first, `tce-f7-el2-r01` (first command in `OVERRIDE.md` section 7), and check `results/tce-f7-el2-r01.json` for `valid: true` and `audit_ok: true` before launching HL2 and SL2.

The launch commands, test results and smoke check are all in `OVERRIDE.md`; the smoke checker output is `spikes/out/smoke-check-tce-smoke-f7-el2-1.json`.
