# Redesign 5: +30 s slack on the time cap (owner decision 2026-11-14)

The cap was `1.35 x B`. It is now `1.35 x B + SLACK_S`, with `SLACK_S = 30`, read from the environment variable `PANEL_SLACK_S` (whole seconds, default 0). With `PANEL_SLACK_S` unset or 0 every number and every old test is unchanged. The hang guard (`1.5 x B`) is not derived from the 35% cap and did not move. No model session ran for this change; the slack values were recomputed from the Spike 4 rows already on disk.

**Result in one line:** with +30 s, `k` is still 0 on every panel and package that has values (el2 and hl2), so `PANEL_COLLAB=1` is still refused on both; only the finish offset and the slowdown limit moved. Details in sections 3 and 5.

## 1. What changed

All paths are under this folder. Nothing under `src/`, `.claude/`, `.dev/tasks/`, `20261111-a1` or another design's folder was touched; nothing was staged or committed.

| File | Lines | Change |
|---|---|---|
| `lib/r5/timing.py` | 18-32 | New `slack_s()` (reads `PANEL_SLACK_S`; rejects anything but `0` or a whole number without leading zero; empty = 0) and `values_dirname()` (`values`, or `values-slack<S>`) |
| `lib/r5/timing.py` | 36, 40, 48 | `k`: `0.35 B + SLACK_S - hooks - turn - report`; `finish_offset`: `1.35 B + SLACK_S - turn - report`; `slowdown_limit`: `(0.35 B + SLACK_S - (hooks + 2k turn)) / B`. `hang_offset` unchanged. The file uses float seconds, not integer ms, so the arithmetic stayed float |
| `lib/r5/timing.py` | 105, 149 | `spike4` writes to `config/<values_dirname()>/<panel>/` and records `slack_s` in each values file |
| `lib/r5/collab.py` | 87 | `over_cap` (the SLO budget): `elapsed > 1.35 B + slack_s`, with `slack_s` read from `run.json` (written at run time), not from the environment, so a later re-run of `r5.collab` gives the same answer |
| `bin/launch.sh` | 37-46, 51, 53, 58, 61, 63 | Validates `PANEL_SLACK_S`; reads `values-slack<S>/` when it is not 0; exit 2 with a clear message if `PANEL_SLACK_S` is not 0 and the slack values (file or `SHA256SUMS`) for any requested package are missing |
| `bin/run-panel.sh` | 16-18, 26-32, 43-44 | Same folder rule; refuses (exit 3) a values file whose recorded `slack_s` differs from `PANEL_SLACK_S`; writes `slack_s` into `run.json` |
| `bin/pins-check.sh` | 32-35 | Checks `values*/*/SHA256SUMS`, so `values-slack30/<panel>/` is verified like `values/<panel>/` |
| `tests/test_timing.py`, `tests/test_launch_preflight.py`, `tests/test_faults.py`, `tests/conftest.py` | n/a | 17 new tests (section 4); `write_values` takes a `dirname`; the `env` fixture ignores `values-slack*` when copying the config and clears `PANEL_SLACK_S` |
| `tests/fake/claude` | 33 | Fallback session id when `/proc/sys/kernel/random/uuid` is unreadable (see section 4); test helper only |
| `config/values-slack30/{el2,hl2}/` | new | 6 values files + 2 `SHA256SUMS`. The old `config/values/` was not touched (its sums were checked before and after) |

Not changed: `DESIGN.md`, `IMPLEMENTATION.md` (their 0.35 and 1.35 text still describes the no-slack rule), `config/pins.json` (it pins config files, templates, `judge-one.sh` and the parser, not `timing.py` or the values).

**About `config/SHA256SUMS`:** this design has no such file. Its value pins are the per-panel `config/values/<panel>/SHA256SUMS`. The new files have their own `config/values-slack30/<panel>/SHA256SUMS` (written by `r5.timing spike4`, checked by `run-panel.sh` and `launch.sh`, and now by `pins-check.sh`: `OK   values-slack30/el2`, `OK   values-slack30/hl2`).

How the values were made (rows `s4-a1-<p>-r1..4`, `s4-a2-<p>-r1..2` on disk, no model calls):

```bash
cd /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
R5=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r5-coverage-deflection
for p in el2 hl2; do
  PANEL_SLACK_S=30 PYTHONPATH=$R5/lib uv run --no-sync python -m r5.timing spike4 --panel $p \
    --rows s4-a1-$p-r1,s4-a1-$p-r2,s4-a1-$p-r3,s4-a1-$p-r4 --kit-rows s4-a2-$p-r1,s4-a2-$p-r2
done
```

## 2. How to launch one panel on all three packages with `PANEL_SLACK_S=30`

Same as `IMPLEMENTATION.md` section 2, plus `PANEL_SLACK_S=30`. Row names must be new. Run from the repository root:

```bash
cd /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
export NOFALLBACK=1 PANEL_SLACK_S=30
R5=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r5-coverage-deflection

# collaboration on (F6)
flock /tmp/collab-gateway.lock env PANEL_COLLAB=1 bash $R5/bin/launch.sh el2 f6s-el2-r01   # ember + 2x luna
flock /tmp/collab-gateway.lock env PANEL_COLLAB=1 bash $R5/bin/launch.sh sl2 f6s-sl2-r01   # sonnet + 2x luna
flock /tmp/collab-gateway.lock env PANEL_COLLAB=1 bash $R5/bin/launch.sh hl2 f6s-hl2-r01   # haiku + 2x luna

# PANEL_COLLAB=0 baseline (A1)
flock /tmp/collab-gateway.lock env PANEL_COLLAB=0 PANEL_KIT=0 bash $R5/bin/launch.sh el2 a1s-el2-r01
flock /tmp/collab-gateway.lock env PANEL_COLLAB=0 PANEL_KIT=0 bash $R5/bin/launch.sh sl2 a1s-sl2-r01
flock /tmp/collab-gateway.lock env PANEL_COLLAB=0 PANEL_KIT=0 bash $R5/bin/launch.sh hl2 a1s-hl2-r01
```

`PANEL_SLACK_S` must be exported or placed after `env` as shown; the `flock ... env` form passes it through. Exit codes as before: 0 complete, 1 partial, 2 preflight refused, 3 F6 not runnable.

What these commands do today (the refusals were run for real with the no-model preflight, output sent to a temp folder):

| Command | Result |
|---|---|
| `PANEL_COLLAB=1 ... el2` | exit 3: `k = 0 on every package` |
| `PANEL_COLLAB=1 ... hl2` | exit 3: `budget_ok false for TASK-WF-designSpec-...` (slowdown 0.580 > limit 0.477) |
| `PANEL_COLLAB=1 ... sl2`, `PANEL_COLLAB=0 ... sl2` | exit 2: `PANEL_SLACK_S=30 but the slack values for panel sl2 ... are missing` |
| `PANEL_COLLAB=0 PANEL_KIT=0 ... el2` / `hl2` | pass the preflight and would start model sessions; **not run here** (no model sessions allowed). The same code path with the fake `claude` is covered by `test_f17_slack_extends_over_cap` |
| `PANEL_SLACK_S=30s` (or `30.5`, `-1`) | exit 2: `must be a whole number of seconds` |

## 3. `k` per panel and package, old (no slack) and new (+30 s)

Inputs are the Spike 4 values on disk (turn and report are 90th percentile, seconds). `k` is the number of messages a receiver may act on (0 to 2). Design 5 never runs on `sl2` by owner order, so `sl2` has no slack values; its pilot numbers are not part of this table.

| Panel | Package | B_f | turn p90 | report p90 | k old | **k new** | finish offset old -> new | cap new (1.35 B + 30) | hang guard (1.5 B) | slowdown vs limit old -> new | budget_ok old -> new |
|---|---|---|---|---|---|---|---|---|---|---|---|
| el2 | design | 116.8 | 40.4 | 57.4 | 0 | **0** | 59.9 -> 89.9 | 187.7 | 175.2 | 0.442 vs 0.333 -> 0.590 | false -> **true** |
| el2 | designSpec | 120.2 | 43.8 | 88.4 | 0 | **0** | 30.0 -> 60.0 | 192.2 | 180.2 | -0.047 vs 0.333 -> 0.583 | true -> true |
| el2 | alias | 144.5 | 31.5 | 73.5 | 0 | **0** | 90.0 -> 120.0 | 225.0 | 216.7 | 0.123 vs 0.336 -> 0.544 | true -> true |
| hl2 | design | 209.5 | 59.5 | 91.3 | 0 | **0** | 132.0 -> 162.0 | 312.8 | 314.2 | 0.249 vs 0.340 -> 0.484 | true -> true |
| hl2 | designSpec | 220.9 | 94.6 | 247.7 | 0 | **0** | -44.0 -> -14.0 | 328.3 | 331.4 | 0.580 vs 0.341 -> 0.477 | false -> false |
| hl2 | alias | 264.1 | 76.7 | 84.7 | 0 | **0** | 195.1 -> 225.1 | 386.5 | 396.1 | 0.243 vs 0.342 -> 0.456 | true -> true |

Why `k` stays 0: one exchange needs the receiver to spend about `2 + turn + report` seconds before it can act on a card, with `turn` 31-95 s and `report` 57-248 s that is 91-345 s, and the room is `0.35 B + 30` = 71-122 s. The measured receiver turns are 2 to 7 times the 6.4 s planning value, so 30 s does not close the gap. The slack only starts to give `k` = 1 when `0.35 B + 30 - 2 - turn - report >= 2 turn`; the unit test cases show where that happens (for example B 100 s, turn 14 s, report 14 s: k 0 -> 1; B 273.7 s, turn 14 s, report 51.8 s: k 0 -> 2).

## 4. Test results

Command (`IMPLEMENTATION.md` AC-1, no model calls, fake `claude`):

```bash
mkdir -p /tmp/evalsb-collab-r5 && PYTHONPATH=$R5/lib uv run pytest -p no:cacheprovider --basetemp=/tmp/evalsb-collab-r5/pytest $R5/tests -v -rs
```

**125 passed, 0 failed, 0 skipped in 101.19 s** (108 existing + 17 new). `uv run --no-sync ruff check lib tests`: all checks passed.

New tests (17):

| File | Count | What |
|---|---|---|
| `test_timing.py` | 12 | default 0 (unset and empty) leaves `k` and the finish offset unchanged; 5 invalid values rejected (`30.5`, `-1`, `abc`, `030`, ` 30`); `k` with 30 for 4 cases (3 change from 0 to 1 or 2, 1 stays 0 on the real el2 numbers); finish offset +30, hang offset unchanged, slowdown limit +30/B; `spike4` with 30 writes only `values-slack30/`, records `slack_s`, `k` 0 -> 2 on the fixture rows, sums match, `values/` not created |
| `test_launch_preflight.py` | 4 | slack values missing -> exit 2 with message (F6 and A1, normal values present and not used); non-integer value -> exit 2; `values-slack30` is the folder read (k = 2 in `values/`, k = 0 in `values-slack30/`, exit 3 "k = 0 on every package"); a values file computed with another slack is refused by `run-panel.sh` (exit 3) |
| `test_faults.py` | 1 | a 2 s receiver against B = 1 s is `over_cap` without slack (existing test) and `ok` with `PANEL_SLACK_S=30`; `run.json` carries `slack_s: 30` |

One thing I fixed that is not part of the slack rule: the first full run gave 123 passed, 2 failed (`test_f09a_reask_used`, `test_f09c_reask_other_model`). The cause is this sandbox: `/proc/sys/kernel/random/uuid` cannot be read ("Transport endpoint is not connected"), so the fake `claude` produced an empty session id and the runner skipped the re-ask. The fake now falls back to a `$$`/`$RANDOM`/time id (`tests/fake/claude:33`). Not caused by the slack change; the real runner code was not touched.

## 5. What still refuses to run, and why

- **F6 (`PANEL_COLLAB=1`) on el2: refused, exit 3.** `k` = 0 on all three packages (turn p90 31-44 s, report p90 57-88 s against `0.35 B + 30` = 71-80 s). No card can be delivered in time, so there is nothing to run. This is the rule working as designed, not a bug.
- **F6 on hl2: refused, exit 3.** designSpec has `budget_ok` false (kit slowdown 0.580 against limit 0.477) and `k` = 0 on all three packages. Its finish offset is also negative (-14 s): haiku's report alone (247.7 s) is longer than `1.35 B + 30 - turn`.
- **Everything on sl2 with `PANEL_SLACK_S=30`: refused, exit 2.** No slack values exist and design 5 does not run on sl2 by owner order. The sl2 pilot values (scratch config) are one package only and were not turned into slack values.
- **A1 (`PANEL_COLLAB=0`) on el2 and hl2: runs.** The A1 arm does not use `k` or the finish offset; B_f and the hang guard are identical to the old values, so an A1 row with slack equals an A1 row without it, apart from `slack_s` in `run.json` and the `over_cap` threshold in `collab.json`.

Two risks the owner should know (not changed, because the instruction said the hang guard stays at 1.5 B):

1. **On el2 the hang guard kills before the new cap.** Cap 187.7 / 192.2 / 225.0 s against hang 175.2 / 180.2 / 216.7 s. A reviewer that finishes between the hang time and the cap is killed and counted `SLO_BREACH`, so it is not "allowed to finish". On hl2 the hang guard is 1.4 to 9.6 s above the cap. If every reviewer must really be allowed to finish up to the cap, the hang guard needs to become `max(1.5 B, 1.35 B + SLACK_S)`: a one-line change in `hang_offset`, which would need new values files (the hang offset is stored in them).
2. `over_cap` can never be set on el2 for the same reason (the hang kill comes first).
