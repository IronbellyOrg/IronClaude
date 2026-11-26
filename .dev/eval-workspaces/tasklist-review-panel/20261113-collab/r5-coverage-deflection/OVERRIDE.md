# Redesign 5: owner-authorised time-cap exception (2026-11-14)

**Owner decision 2026-11-14:** the +35% elapsed-time rule may be exceeded. Spike 4 measured turn times far above the planning values, so the number of messages `k` that fit in the +35% window is 0 on every el2 and hl2 package, and the launcher refused the collaboration arm (exit 3). This file records the minimal, explicit exception that lets the arm run. Nothing here is on by default.

**Switch:** `TIME_CAP_EXCEPTION=1` (environment variable). Unset, empty or `0` = off. Any other value is refused with exit 2. It applies to the collaboration arm only (`PANEL_COLLAB=1`); a baseline row with the variable set is refused (exit 2), so a baseline can never be stamped or run with widened guards. It cannot be combined with `PANEL_SLACK_S` (exit 2) or `SPIKE4=1`.

**Result in one line:** with the switch on, every el2 and hl2 package runs with `k = 1` (measured 0), hang guard 3.0 x B_A1, finish signal at 2.7 x B_A1 minus the receiver's turn and report times. One real smoke row (el2, package `TASK-WF-design-20261108-041415`) passed all 8 checks; it finished in 0.91 x baseline, so it proves the chain but did not need the widened guards. All 160 tests pass.

## 1. What changed

All paths are under this folder. Nothing under `src/`, `tests/`, `.claude/`, `.dev/tasks/`, `20261111-a1` or another design's folder was edited; nothing was staged or committed. (`git status` shows untracked files under `20261111-a1/.../reviews-failed-launch-1/`; they are older than this work and this harness only reads that folder.)

| File | Lines | Change |
|---|---|---|
| `lib/r5/timing.py` | 51-86 | New `EXC_HANG_FACTOR = 3.0`, `EXC_CAP_FACTOR = 2.7`, `EXC_FORCED_K = 1`; `time_cap_exception()` (reads the variable, 0 or 1 only); `exception_plan(vals, on)`: one pure function that returns everything a package runs with. **Off: returns the values file's own numbers unchanged; no existing function (`k`, `finish_offset`, `hang_offset`, `slowdown_limit`) was edited.** |
| `lib/r5/timing.py` | 206-208 | CLI `python -m r5.timing exception <values.json>` prints the plan as JSON (used by the two shell scripts) |
| `bin/run-panel.sh` | 19-26 | Validates the variable; refuses `COLLAB=0`, `PANEL_SLACK_S`, `SPIKE4=1` with the exception (exit 2) |
| `bin/run-panel.sh` | 44-52 | After the values file sum is checked, asks `r5.timing exception` for the plan, sets `K`, finish and hang offsets, and writes an **effective copy** `runs/<row>/<pkg>/values-effective.json` that `run-reviewer-r5.sh` reads (it takes its hang guard from that file, so the reviewer script itself is unchanged). The frozen values file in `config/values/` is never edited |
| `bin/run-panel.sh` | 61-63 | `run.json` gains `time_cap_exception`, `k_measured`, `k_forced`, `time_cap_s` (always written; `false`/`null` when off) |
| `bin/launch.sh` | 41-47 | Same validation and refusals at preflight (exit 2) |
| `bin/launch.sh` | 62-70 | F6 values check: with the exception, `budget_ok` and `k` come from the plan; the plan per package is stored in `launch.json` (`time_cap_plan`) |
| `bin/launch.sh` | 84-88 | `launch.json` records `time_cap_exception` and `env.TIME_CAP_EXCEPTION` |
| `lib/r5/collab.py` | 87-92, 133 | `over_cap` uses `time_cap_s` (2.7 x B) when the exception is on, else the old `1.35 B + slack`. New `collab.json` keys: `time_cap_exception`, `B_A1_s`, `time_cap_s`, `k_measured`, `k_forced`, `elapsed_over_baseline`, `messages_delivered` (per reviewer; `null` when there is no board) |
| `lib/r5/results.py` | 79, 96-99 | Results row gets `time_cap_exception` (true/false) and, when true, a `time_cap` block per package: `B_A1_s`, `elapsed_s`, `elapsed_over_baseline`, `time_cap_s`, `k_measured`, `k_forced`, `k_run`, `messages_delivered` |
| `lib/r5/alarms.py` | 55-90 | `arm` summary: reports the same columns per run (`time_cap_runs`), **refuses (`SystemExit`) to summarise rows with `time_cap_exception` true and false together**, and writes exception arms to `arm-summary-<arm>-tcx.json` so they never overwrite or feed the cap-obeying summary |
| `tests/test_time_cap_exception.py` | new, 35 tests | Section 5 |
| `tests/conftest.py` | 131 | The `env` fixture also clears `TIME_CAP_EXCEPTION` |
| `spikes/smoke-check-tcx.sh` | new | The 6.4 checks that apply to one collaboration row (items 1-4, 6, 7; item 5 is A1-only) plus the stamp checks; appends to `spikes/NOTES.md` |

Not changed: `DESIGN.md`, `IMPLEMENTATION.md` and `SLACK.md` (their 0.35 / 1.35 text still describes the cap rule; the exception is documented only here), `config/` (templates, catalogue, values), `bin/run-reviewer-r5.sh`, `bin/hook-posttool.sh`, `lib/r5/watcher.py`. The earlier `PANEL_SLACK_S` mechanism is untouched and still works; it is mutually exclusive with this one.

## 2. The numbers

Per package, with the switch on (B_A1 = `B_f_s` of the frozen Spike 4 values file; turn and report are the receiver's p90 from that file; the receivers are the two lunas on el2 and haiku on hl2):

| Quantity | Off (unchanged) | On |
|---|---|---|
| `k` | the file's `k` (0 on all six) | `1` where the file's `k` is 0; a measured 1 or 2 is kept |
| Hang guard (kills any reviewer, scouts included) | `1.5 x B_A1` (the file's `hang_offset_s`) | `max(file value, 3.0 x B_A1)` |
| Cap (for `over_cap` and the finish signal) | `1.35 x B_A1` | `2.7 x B_A1` (0.9 x the new hang guard, the same ratio as 1.35 / 1.5) |
| Finish-signal offset | `1.35 B - turn - report` | `2.7 B - turn - report` |
| Kit-slowdown limit for `budget_ok` | `(0.35 B - (2 + 2 k turn)) / B` | `(1.7 B - (2 + 2 k turn)) / B` with the forced `k` |

`budget_ok` is the one launch check whose answer changes with the switch on. It compares the catalogue kit's measured slowdown with the room inside the cap, so it is a cap check; it is still enforced, now against the widened cap. Result: `true` on all six packages (it was `false` on el2 `design` and hl2 `designSpec`).

All values in seconds (computed by `r5.timing exception` from the six files in `config/values/`):

| Panel | Package | B_A1 | turn p90 | report p90 | k measured -> run | Hang guard old -> new | Finish offset old -> new | Cap new | Kit slowdown vs limit old -> new | budget_ok old -> new |
|---|---|---|---|---|---|---|---|---|---|---|
| el2 | design | 116.8 | 40.4 | 57.4 | 0 -> 1 | 175.2 -> 350.3 | 59.9 -> 217.5 | 315.3 | 0.442 vs 0.333 -> 0.991 | false -> true |
| el2 | designSpec | 120.2 | 43.8 | 88.4 | 0 -> 1 | 180.2 -> 360.5 | 30.0 -> 192.2 | 324.4 | -0.047 vs 0.333 -> 0.954 | true -> true |
| el2 | alias | 144.5 | 31.5 | 73.5 | 0 -> 1 | 216.7 -> 433.4 | 90.0 -> 285.0 | 390.0 | 0.123 vs 0.336 -> 1.250 | true -> true |
| hl2 | design | 209.5 | 59.5 | 91.3 | 0 -> 1 | 314.2 -> 628.5 | 132.0 -> 414.9 | 565.6 | 0.249 vs 0.340 -> 1.122 | true -> true |
| hl2 | designSpec | 220.9 | 94.6 | 247.7 | 0 -> 1 | 331.4 -> 662.8 | -44.0 -> 254.2 | 596.5 | 0.580 vs 0.341 -> 0.835 | false -> true |
| hl2 | alias | 264.1 | 76.7 | 84.7 | 0 -> 1 | 396.1 -> 792.2 | 195.1 -> 551.6 | 713.0 | 0.243 vs 0.342 -> 1.112 | true -> true |

A test (`test_on_real_spike4_numbers`) checks for each of these six: finish offset is positive, finish offset + turn + report fits inside the hang guard, and the one forced exchange (`B + 2 + 2 turn`) fits inside the cap.

**sl2 (sonnet + 2x luna) is not covered:** it has no frozen values (only the one-package Spike 4 pilot, kept outside `config/values/`), so `launch.sh sl2` is refused (exit 3, "no values file") with or without the switch. It needs the full Spike 4 first.

Where the switch is on, all three packages of a row get the widened guards and the stamp, including a package whose measured `k` is already 1 or 2 (none today). The row is the unit that is stamped, so a row never mixes capped and uncapped packages.

## 3. Stamps and columns

A row run with the switch on carries `time_cap_exception: true` in `runs/<row>/<pkg>/run.json`, in `runs/<row>/<pkg>/collab.json`, in `runs/<row>/launch.json` and in `results/<row>.json` (and the `results.jsonl` line). Rows made with the switch off carry `false`; rows written before this change have no field and count as `false`.

Columns recorded per package (results row `time_cap.<pkg>`, `collab.json`, and the arm summary `time_cap_runs`):

| Column | Meaning |
|---|---|
| `B_A1_s` | baseline from the Spike 4 values file |
| `elapsed_s` | measured panel elapsed (every attempt and re-ask) |
| `elapsed_over_baseline` | `elapsed_s / B_A1_s` |
| `k_measured`, `k_forced`, `k_run` | file `k`; whether it was forced to 1; the `k` the run used |
| `messages_delivered` | cards actually delivered per reviewer, e.g. `{"t4-1":1,"t3-1":0,"t2b-1":0}` (scouts always 0) |
| `time_cap_s` | the cap the row was judged against (2.7 x B) |

`python -m r5.alarms arm <arm> <rows...>` prints and writes these columns and exits with an error if the rows it is given mix `true` and `false`.

## 4. Pins

`config/pins.json` pins `judge-one.sh`, the config files and templates, and the worktree and installed `findings.py` / `ledger.py`; the values files are pinned by `config/values/<panel>/SHA256SUMS`. This change edits none of them (it reads the frozen values files and writes its widened numbers into a per-run copy). Procedure run: `R5_PINS=/tmp/r5-pins-regen.json bash bin/pins-check.sh --write` (the design's own regenerate command, pointed at a scratch file) gives a `pins.json` identical to the committed one, so nothing was re-pinned; `bash bin/pins-check.sh` prints `OK` on all 18 lines (judge-one.sh, 8 config files, 4 parser files, 4 values folders, audit static) and exits 0. The launcher preflight passed in the smoke run. No identity check, allow-list, `NOFALLBACK=1`, contamination safeguard or blind-judge step was changed.

## 5. Tests

Command (the one in `IMPLEMENTATION.md` section 3, from the repository root):

```bash
R5=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r5-coverage-deflection
mkdir -p /tmp/evalsb-collab-r5 && PYTHONPATH=$R5/lib uv run pytest -p no:cacheprovider --basetemp=/tmp/evalsb-collab-r5/pytest $R5/tests -v -rs
```

**160 passed, 0 failed, 0 skipped** (125 existing + 35 new) in 143 s; `uv run --no-sync ruff check $R5/lib $R5/tests` reports no errors. (After that full run I renamed two new test functions to satisfy a lint rule and re-ran `tests/test_time_cap_exception.py` alone: 35 passed.)

The 35 new tests (`tests/test_time_cap_exception.py`):

| Group | What it checks |
|---|---|
| Switch | default off (unset, empty, `0`); `1` is on; `2`, `-1`, `true`, `1.0`, ` 1`, `01` are refused |
| Off | `exception_plan(..., False)` returns the file's numbers unchanged for three value sets (including a slack file); `k`, `finish_offset`, `hang_offset`, `slowdown_limit` still give the pinned numbers of `test_timing.py` with the variable set to 1; `run-panel.sh` without the switch: `k = 2` row has the old finish and hang offsets, no `values-effective.json`, `time_cap_exception: false`; `k = 0` row still runs as A2 (no board, `k0_isolated`) |
| On | forced `k = 1` only where measured `k` is 0 (1 and 2 kept); hang = `max(file, 3.0 B)` both ways; cap, finish offset and slowdown limit values; `budget_ok` against the widened cap (and false with no kit measurement); the six real Spike 4 packages; the CLI |
| Launcher | refused (exit 2, no model call): `PANEL_COLLAB=0`, value `2`, with `PANEL_SLACK_S`; `k = 0` everywhere is refused (exit 3) off and runs on; `budget_ok` still refuses when the kit slowdown exceeds even the widened limit |
| End to end (fake `claude`) | `run.json`, `values-effective.json`, `collab.json`, `launch.json` and the results row carry the stamps and columns; one card delivered to the receiver with `messages_delivered == {"t1b-1":1,"t4-1":0,"t3-1":0}`; every card has the design's keys and at most `k` items; a 3.5 s receiver is `ok` with the switch on and hang-killed (`SLO_BREACH`) by the old 3 s guard without it |
| Summariser | columns reported; mixed rows refused; exception and cap-obeying summaries go to different files |

## 6. Smoke row (one real row, override on)

Command (as the design's section 6.4 F6 row, with the switch, panel el2, package design):

```bash
cd /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
export NOFALLBACK=1
flock /tmp/collab-gateway.lock env PANEL_COLLAB=1 TIME_CAP_EXCEPTION=1 bash $R5/bin/launch.sh el2 smoke-tcx-el2-1 --pkgs TASK-WF-design-20261108-041415
bash $R5/spikes/smoke-check-tcx.sh smoke-tcx-el2-1 0
```

Models used: `muse-ember-1.0` (scout), `gpt-6-luna` x2 (receivers), `claude-opus-5-5` only inside `judge-one.sh`; `NOFALLBACK=1`; 3 reviewer sessions at once. Row `smoke-tcx-el2-1`: exit 0, status `complete`, audit `pass`. Files: `runs/smoke-tcx-el2-1/`, `results/smoke-tcx-el2-1.json`, section appended to `spikes/NOTES.md`.

| # | Check | Result |
|---|---|---|
| 1 | exit 0, status `complete` | PASS |
| 2 | every final attempt `model_ok`, observed model equals requested (ember, luna, luna) | PASS |
| 3 | `dropped_lines` 0; 3 reviewer ids in the merge | PASS |
| 4 | card posted and delivered (`cards_delivered` 1), `snapshot_missing` 0, `hook_error` 0, card text in the receiver's transcript 45 ms after the seal, card passes the validator, snapshot sha matches | PASS |
| AC-9 | cards have only the design's keys and at most `k` = 1 item; none posted or delivered at or after the finish time | PASS |
| 6 | anonymise post-check 0, `score.json` parses, audit pass | PASS |
| 7 | no hang kill; `elapsed_s` 105.8 s inside the hang guard of 350.3 s | PASS |
| 8 | `time_cap_exception: true` in run, collab and results; `k_measured` 0, `k_forced` true, `k` 1; `B_A1_s` 116.782 equals the values file | PASS |

Columns of the row: B_A1 116.782 s; elapsed 105.825 s; elapsed/baseline 0.906; forced `k` 1; messages delivered `t4-1` 1, `t3-1` 0, `t2b-1` (scout) 0; `requests_acted` 1.

What the smoke row does and does not show:

- It exercised the collaboration path on real models: ember finished at 57 s, the watcher posted one card to each luna (`T3`, `T7`), the hook sealed `t4-1`'s transcript and delivered its card at 78.7 s, and that luna's report carries a finding on the requested Task.
- The other luna (`t3-1`) got no card. Its last tool call was at 54 s, before the card was posted at 58 s, so the card was marked `late` (the design's own rule, DESIGN 2.8). Forcing `k = 1` does not guarantee delivery when a receiver finishes its tool calls before the scout exits; on el2 ember is fast, so expect some `late` cards. `messages_delivered` records exactly that.
- The row finished inside the baseline (0.91 x B_A1), so the finish signal and the hang guard never fired. The widened guards were exercised by the fake-`claude` tests, not by this real row.
- Design item 5 (the A1 row) was not run; the task asked for one real row only. The package is the control package, so its scores are not meaningful as results.

## 7. Launch commands

Run from the repository root. One launch = one panel, all three packages (designSpec, alias, control, one after another), then merge, anonymise, judge (Opus, blind) and write the results row; at most 3 reviewer sessions at a time. Row names must be new (existing: `s4-*`, `s4pilot-*`, `smoke-*`). Exit codes: 0 complete, 1 partial or quarantined, 2 preflight refused, 3 collaboration not runnable. Do not set `PANEL_SLACK_S`.

```bash
cd /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
export NOFALLBACK=1
R5=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r5-coverage-deflection
```

**Collaboration row with the exception (the rows to stamp `time_cap_exception: true`):**

```bash
# el2: muse-ember-1.0 scout + 2x gpt-6-luna receivers
flock /tmp/collab-gateway.lock env PANEL_COLLAB=1 TIME_CAP_EXCEPTION=1 bash $R5/bin/launch.sh el2 f6x-el2-r01
# hl2: claude-haiku-5-5 receiver + 2x gpt-6-luna scouts
flock /tmp/collab-gateway.lock env PANEL_COLLAB=1 TIME_CAP_EXCEPTION=1 bash $R5/bin/launch.sh hl2 f6x-hl2-r01
```

**Matching isolated baseline row (A1: no hooks, no watcher, no board, no kit; same harness, same values; it obeys the cap, so the variable must NOT be set):**

```bash
flock /tmp/collab-gateway.lock env PANEL_COLLAB=0 PANEL_KIT=0 bash $R5/bin/launch.sh el2 a1x-el2-r01
flock /tmp/collab-gateway.lock env PANEL_COLLAB=0 PANEL_KIT=0 bash $R5/bin/launch.sh hl2 a1x-hl2-r01
```

(Static-kit comparator A2, if wanted: the same with `PANEL_KIT=1`.) Drop `flock /tmp/collab-gateway.lock` when the gateway is not shared. Add `--pkgs <full package id>[,<id>...]` to run fewer than three packages. A row name is used once; use `-r02`, `-r03` for repeats.

**Summarise after the rows (never mix the two kinds in one call):**

```bash
PYTHONPATH=$R5/lib uv run python -m r5.alarms arm A1-el2 a1x-el2-r01                 # baseline reference first (writes arm-summary-A1-el2.json)
PYTHONPATH=$R5/lib uv run python -m r5.alarms arm F6-el2 f6x-el2-r01                  # writes arm-summary-F6-el2-tcx.json with the time_cap_runs columns
```

(The same for `hl2`.) The per-package alarms inside each launch read `results/arm-summary-A1-<panel>.json` as their reference; until the A1 summary exists they record `reference: "missing"`.

## 8. Risks and things not done

- **hl2 designSpec** has a haiku report turn of 247.7 s (Spike 4 maximum of 4 runs). The finish signal is at 254 s and the hang guard at 662.8 s; the row will be slow (up to 3.0 x B_A1), and any reviewer still running at the hang guard is killed and counted `SLO_BREACH`.
- Rows with the exception can take up to 3.0 x B_A1 per package (about 6 to 13 minutes on hl2); a three-package hl2 row can run past 25 minutes plus three judge calls.
- `late` cards are expected on el2 (ember exits in about 57 s; a luna that has already made its last tool call receives nothing). The comparison against baseline should read `messages_delivered`, not `k`.
- The exception rows are not comparable to cap-obeying rows on elapsed time by design; the stamp and the separate summary file are what keep them apart. Any shared analysis outside this folder must filter on `time_cap_exception` itself.
- Not done: the full three-package rows (the orchestrator runs them), the A1 smoke row, an `sl2` Spike 4, edits to `DESIGN.md` or `IMPLEMENTATION.md`.
