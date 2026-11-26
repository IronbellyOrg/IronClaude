# Redesign 3 (Axis-Flip Challenge): owner-authorised time-cap exception

Owner decision 2026-11-14: the +35% elapsed-time rule may be exceeded so the collaboration arm runs on panels where the measured n (challenges a receiving reviewer may start) is 0. It is switched on by the environment variable `TIME_CAP_EXCEPTION=<forced n>` (default off; allowed 1, 2 or 3; 1 is the decision). Nothing was staged, committed or pushed. Only files under this folder changed (plus scratch under `/tmp/r3-tce/`).

This design (F1) is a between-phase design: the quantity that hits 0 is **n** (per receiving reviewer, 6.5 of the design). F1 does not act on k; k is only logged, so it is not forced (it is recorded as `k_measured`).

## 1. What changed (files and lines)

| File | Lines | Change |
|---|---|---|
| `r3lib/values.py` | 75-147 | `tce_forced()` reads and validates `TIME_CAP_EXCEPTION` (unset or 0 = off; 1, 2, 3 allowed; anything else exits with `E_TCE`). `tce_plan` / `tce_all` compute the widened numbers per package (section 2). `tce_floor_n` raises a measured n of 0 to the forced n (bounded by the receiver's cap) while the widened phase-2 deadline still has room for `start_cost + 2 x forced x turn_p90`. |
| `r3lib/values.py` | 215-224 | `load(..., prefer_frozen=False)`: new option, set only when the exception is on. A smoke run then uses the frozen values file when one exists, so the forced n is exercised on the measured Spike 4 numbers (without the exception, smoke still uses planning values, A10). |
| `r3lib/cli.py` | 204-209, 370 | `values-show --tce N` also prints the widened numbers for every package (`.tce.<pkg>`). |
| `r3lib/digest.py` | 228-241 | `build` applies `tce_floor_n` after `compute_n`; the digest log records `n_base` and `n_forced`. Absent `pkg.json` key `tce` means off, so nothing changes. |
| `bin/launch-panel.sh` | 26-28, 43, 59-61 | Preflight reads `TIME_CAP_EXCEPTION`; a bad value, `PANEL_COLLAB=0`, or `R3_SPIKE4=1` with it exits 1 (`E_TCE`, nothing launched). `run.json` gets `time_cap_exception` (bool) and `tce_forced_n`. |
| `lib/package.sh` | 20-24, 34-37, 43-47, 78-82 | Reads the exception from `run.json` (never from the environment, as for `PANEL_COLLAB`). When on: `HANG_AT` and `P2_DEADLINE` use the widened offsets; `pkg.json` gets the `tce` block and its finish offset; the scheduler's `n_now` applies the same floor in awk. |
| `r3lib/metrics.py` | 250-280 | `collab.json` gets `time_cap_exception` and a `tce` block (section 3). |
| `r3lib/metrics.py` | 641-653, 715-721 | The results row gets `time_cap_exception` (true or false) and `tce` (null when off). |
| `r3lib/metrics.py` | 824-850, 862-865, 914, 997-1013 | `summarize` splits rows stamped `time_cap_exception` off before computing anything: arms A1 and A3, `cap_check`, convergence, echo and the Fisher test use only rows that obeyed the cap. Exception rows get their own section `time_cap_exception` and their own table. |
| `tests/test_tce.py` | new | 20 tests (section 5). |
| `tests/conftest.py` | 110 | The `env` fixture clears `TIME_CAP_EXCEPTION` so a caller's value cannot leak into tests. |

Not changed: `config/` (all of it), `values/`, `values-slack30/`, the judge, the blind judge path, `lib/reviewer.sh`, `lib/common.sh`, the admission control, the model allowlist, `NOFALLBACK=1`, the audit and contamination checks.

**Off means identical.** With the variable unset, `tce_floor_n` returns its input, `package.sh` takes no new branch, and `compute_n`, `compute_k`, `finish_offset` are untouched. The 102 earlier tests pass unchanged (section 5).

## 2. The exact numbers (override on, forced n = 1)

Rules, per package, with B_A1 = the `B_f` of that package in the frozen Spike 4 values file (`values/<panel>.json`, the A1 baseline median):

| Quantity | Off | On |
|---|---|---|
| n at a launch attempt | measured `compute_n` | measured value; **1 only where the measured value is 0** and the widened deadline has room for one challenge (`P2 offset - t_rel - start_cost >= 2 x 1 x turn_p90`, start cost 6 s resume or 16 s fresh fallback). Never lowered, never above the receiver's cap |
| Hang guard (phase-1 kill) | T0 + 1.5 x B_f | T0 + max(1.5 x B_f, **3.0 x B_A1**) |
| Phase-2 deadline (kill of phase 2, resume, fallback and re-ask) | T0 + 1.30 x B_f (+ `PANEL_SLACK_S`) | T0 + max(that, hang guard + 16 s + 2 x forced n x largest turn p90 of the panel) |
| Finish offset (logged, `finish_would_fire`) | 1.35 x B - turn_p90 - T_report_p90 | max(old, hang guard - turn_p90 of the critical model - T_report_p90) = 3.0 x B_A1 - turn_p90 - T_report_p90 |
| k | logged, not used by F1 | unchanged, logged as `k_measured` |

Values for all panels and packages (forced n = 1). The last column is the planning view at T0 + B_A1 for (searcher, luna, luna), measured n -> n with the override; a receiver that seals later sees a smaller measured n and is forced to 1.

| Panel | Package | B_A1 (s) | Hang guard old -> new (s) | Phase-2 deadline old -> new (s) | Finish offset old -> new (s) | k measured | n measured -> forced |
|---|---|---|---|---|---|---|---|
| el2 | design | 137.8 | 206.7 -> 413.4 | 179.2 -> 453.8 | 160.3 -> 387.7 | 0 | [3, 1, 1] -> [3, 1, 1] |
| el2 | designSpec | 92.1 | 138.2 -> 276.4 | 119.8 -> 316.7 | 104.5 -> 256.5 | 0 | [3, 0, 0] -> [3, 1, 1] |
| el2 | makeTheAliasOnly | 100.9 | 151.4 -> 302.7 | 131.2 -> 343.1 | 114.7 -> 281.1 | 0 | [3, 0, 0] -> [3, 1, 1] |
| hl2 | design | 203.5 | 305.2 -> 610.4 | 264.5 -> 699.9 | 219.0 -> 554.8 | 0 | [0, 2, 2] -> [1, 2, 2] |
| hl2 | designSpec | 327.9 | 491.9 -> 983.8 | 426.3 -> 1073.3 | 391.6 -> 932.7 | 0 | [1, 2, 2] -> [1, 2, 2] |
| hl2 | makeTheAliasOnly | 303.3 | 455.0 -> 909.9 | 394.3 -> 999.5 | 358.8 -> 859.3 | 0 | [1, 2, 2] -> [1, 2, 2] |
| sl2 | design | 214.0 | 321.0 -> 642.1 | 278.2 -> 693.8 | 253.0 -> 606.2 | 1 | [1, 2, 2] -> [1, 2, 2] |
| sl2 | designSpec | 270.9 | 406.4 -> 812.8 | 352.2 -> 864.5 | 312.6 -> 759.6 | 1 | [2, 2, 2] -> [2, 2, 2] |
| sl2 | makeTheAliasOnly | 330.4 | 495.6 -> 991.2 | 429.5 -> 1042.9 | 404.9 -> 950.1 | 2 | [2, 2, 2] -> [2, 2, 2] |

Generated by `/tmp/r3-tce/numbers.py` from the three frozen values files (same code as the harness). Ember's turn p90 is 2.9 s, luna's 12.2 s, haiku's 36.8 s, sonnet's 17.8 s.

**What the widening costs.** A normal run ends near B_A1 to 1.2 x B_A1; the new kill times (up to 3 x B_A1 + 16 s + 2 x forced n x turn) are only reached by a hung session. A late receiver is no longer left without its message by the 1.30 B clock, but a session that really hangs now holds its package open for up to 3 x B_A1 instead of 1.5 x. Two acceptance criteria use the old clocks: **AC-7** (no phase-2 process alive after T0 + 1.30 B_f + 3 s, no phase-1 process after T0 + 1.5 B_f + 5 s) is read, for exception rows, as the widened offsets above (`pkg.json` `P2_DEADLINE`, `HANG_AT`); and the summary's `cap_check` (1.35 x B_c) does not apply to exception rows.

## 3. Stamps and columns on every override row

Every row with the override on carries `time_cap_exception: true` in `run.json`, `collab.json`, `result.json` and the line appended to the results file (`results/results.jsonl`, or `results/smoke.jsonl` for a smoke run). A row without it carries `time_cap_exception: false`. The row's `tce.by_pkg.<package>` (also in each package's `collab.json` under `tce`) has:

| Field | Meaning |
|---|---|
| `B_A1` and `B_A1_source` | baseline of the package from the Spike 4 values file (`frozen`) |
| `elapsed_s` | measured elapsed of the package (last process end minus T0) |
| `ratio` | `elapsed_s / B_A1` |
| `forced_n` | the forced n (the value of `TIME_CAP_EXCEPTION`) |
| `delivered` | challenges actually delivered per reviewer id (`n_launched`: slots in the digest that was sent; 0 when nothing was sent) |
| `n_planned` | n at each reviewer's first launch attempt (after the floor) |
| `forced_applied` | per reviewer: true when the floor changed that reviewer's n (measured 0 -> forced) |
| `hang_offset_s`, `p2_deadline_offset_s`, `finish_offset_s`, `finish_offset_cap_s`, `k_measured` | the widened kill times, the widened and the old finish offset, the measured k |

`summarize` (`bash -c 'source lib/common.sh; r3_py summarize --panel <panel>'`) reports these under `time_cap_exception` in the JSON and in a separate table (B_A1, elapsed, ratio, forced n, delivered per reviewer, plus the quality means of the exception rows). Exception rows never enter arms A1 or A3, `cap_check`, `convergence`, `echo` or the Fisher test (unit test `test_summary_keeps_exception_rows_apart`: the arms and the cap check are identical with and without an exception row).

## 4. Pins and identity

`config/pins.json` pins the judge script, `findings.py`, `ledger.py`, `merge_cmd.py` and every file under `config/`. None of them was touched, so no re-pin was needed; `pin --check` printed `pins ok` before the work (12:56 UTC), after the smoke run, and on every launcher preflight. If a pinned file is ever edited, the design's documented procedure is `bash -c 'source lib/common.sh; r3_py pin'` (rewrites `config/pins.json`), then `r3_py pin --check`.

Nothing else was loosened: observed model equals requested model in every used session (`model_ok`), `NOFALLBACK=1` is required by the launcher, models stay on the allowlist, the audit, the contamination checks (`gt_text_leak`, `QUARANTINE`) and the blind judge path are unchanged. The override is refused with `PANEL_COLLAB=0` (the isolated baseline has no messages) and with `R3_SPIKE4=1`.

## 5. Tests

`tests/test_tce.py` (20 tests):

- Off: unset means 0; the floor returns its input; `compute_n`, `compute_k`, the values path and smoke planning values are unchanged; a launch on the fake `claude` without the variable has `time_cap_exception: false`, no `tce` block, hang guard 1.5 x B_f, deadline 1.30 x B_f and delivers nothing when the measured n is 0.
- On: the parser accepts 0 to 3 and refuses `abc`, `-1`, `4`, `1.5`, `yes`; the el2 design numbers (hang 3.0 x B_A1, deadline +16 s +2 x turn, finish offset); the floor applies only where the measured n is 0, never lowers, respects the receiver's cap, and stays 0 when the widened deadline has no room (also for the 16 s fresh start); a launch on the fake `claude` with B_f 40 s and turn 30 s (measured n 0 everywhere) delivers 1 challenge per reviewer, stamps `run.json`, `pkg.json`, `collab.json` and `result.json`, has hang guard 120 s and deadline 196 s after T0, and no audit violation; the launcher refuses a bad value and `PANEL_COLLAB=0` with exit 1 and no run directory.
- Summary: exception rows are kept apart, with the new columns.

Full suite, command from IMPLEMENTATION.md section 3 (`override-report/tests-full.log`): **122 passed, 0 failed, 0 skipped in 231.65 s** (the 102 earlier tests plus 20). `ruff check` and `ruff format --check` clean on `r3lib/` and `tests/`; `bash -n` clean on `bin/launch-panel.sh` and `lib/package.sh`.

## 6. Smoke result (real models, override on)

Command (as 15.5, plus the override):

```bash
flock /tmp/collab-gateway.lock env R3_SMOKE=1 TIME_CAP_EXCEPTION=1 NOFALLBACK=1 PANEL_COLLAB=1 bash bin/launch-panel.sh el2 --pkgs TASK-WF-design-20261108-041415
```

Run `runs/el2-c1-20261114T125635Z-eb5d`, started 12:56:35 UTC, exit 0, one line printed: `found14=0 real_blocking8=0 control_found2=0 tokens=44079 elapsed=149.7`. Reviewer sessions: 3 at once, then at most 2 phase-2 sessions. Judges: Opus, 2 (full and sealed).

| 15.5 condition | Observed |
|---|---|
| exit 0 | yes |
| `collab.json` validates | written for the package; `time_cap_exception: true`, `tce` block complete |
| at least one phase-2 session with `model_ok` true | yes: ember `t2b-1` (3 challenges delivered, 12.7 s) and luna `t4-1` (1 challenge, 59.1 s); both resumed, no fallback, no timeout, observed model equals requested. Luna `t3-1`: no slots (`no_launch` reason `no_slots`, logged) |
| `merged-anon.md` passes the residue check | yes; `P2-` count 0 in both |
| `score.json` for `full` and `sealed` | both exist (`judge_ok` true) |
| row in `results/smoke.jsonl` | yes (5th line, `time_cap_exception: true`, `smoke: true`); `results/results.jsonl` was not touched |
| `audit.json` no violations | `violations: []`, `source_read` true for all three; `contaminated: false`, `gt_text_leak` 0 |
| sandbox check (9.4, AC-15) | `git status --porcelain` empty; with `--ignored` also empty after cleanup; candidate sha256 equals the `pkg.json` value |
| AC-14 manifests of `REPO/src` and `EVAL` | sha256 of the sorted `find -type f` manifest identical before and after (`b90f963e...`, `/tmp/r3-tce/manifest-before.txt`, `-after.txt`) |
| identity | observed model equals requested in all 3 phase-1 and both phase-2 sessions; every reviewer sealed on attempt 1; no hang kill; no SLO breach |

Numbers recorded in the row: B_A1 137.81 s (frozen), elapsed 149.73 s, ratio 1.086, forced n 1, delivered `{t2b-1: 3, t4-1: 1, t3-1: 0}`, `n_planned` `{3, 1, 1}`, `HANG_AT` T0 + 413.43 s, `P2_DEADLINE` T0 + 453.78 s, finish offset 387.65 s (old 160.26 s).

**The forced floor did not fire in this smoke run, and this is not a pass of that part.** Both lunas sealed early (76.5 s and 89.1 s after T0), so the measured n was already 1 for them (`n_base` 1, `forced_applied` false everywhere). What ran on real models: the override path through the launcher, the widened kill times, the stamps and columns, phase 2 on ember and luna, the sealed merge, both judges. What is shown only on the fake `claude` and in unit tests: a measured n of 0 becoming 1. It will show in real rows as `forced_applied: true` and a `delivered` count of 1 where the old rule would have delivered 0; check that column in the first full rows. Also note a delivered count of 0 with n >= 1 is possible (`t3-1` above: the deal gave it no real anchor and no gap slot filled), so the override guarantees n, not a message.

Deviation from 15.5, only when the override is on: the smoke used the frozen values (so B_A1 and the turn p90 are the measured ones) instead of planning values. Without the override smoke still uses planning values.

## 7. Launch commands

Run from this folder. One launch runs all three packages in parallel (9 reviewer sessions at once; admission control limits the host total), judges with Opus (at most 4 at once) and appends one row to `results/results.jsonl`. Frozen values exist for all three panels, so no Spike 4 is needed.

```bash
cd /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge

# Collaboration row WITH the exception (arm A3, time_cap_exception: true), one per panel:
flock /tmp/collab-gateway.lock env NOFALLBACK=1 TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 bash bin/launch-panel.sh el2   # ember + 2x luna
flock /tmp/collab-gateway.lock env NOFALLBACK=1 TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 bash bin/launch-panel.sh hl2   # haiku + 2x luna
flock /tmp/collab-gateway.lock env NOFALLBACK=1 TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 bash bin/launch-panel.sh sl2   # sonnet + 2x luna

# Isolated baseline row with the same harness (arm A1, no messages, rules that obey the cap; do not set TIME_CAP_EXCEPTION):
flock /tmp/collab-gateway.lock env NOFALLBACK=1 PANEL_COLLAB=0 bash bin/launch-panel.sh el2
flock /tmp/collab-gateway.lock env NOFALLBACK=1 PANEL_COLLAB=0 bash bin/launch-panel.sh hl2
flock /tmp/collab-gateway.lock env NOFALLBACK=1 PANEL_COLLAB=0 bash bin/launch-panel.sh sl2

# Summary per panel (exception rows are reported in their own section and never mixed with cap-obeying rows):
bash -c 'source lib/common.sh; r3_py summarize --panel el2'
```

Exit codes as before: 0 all valid and judged, 1 preflight refused, 2 a package invalid or not judged, 3 audit violation. A row with the override on sits in `results/results.jsonl` next to cap-obeying rows; tell them apart by `time_cap_exception`. Do not combine `TIME_CAP_EXCEPTION` with `PANEL_SLACK_S` unless intended: they compose (the phase-2 deadline is the larger of the two rules; the slack values file is then also required), but the exception already widens every timer.

## 8. Open points

1. The forced n is proven on real models only as far as section 6 says: the widened timers and stamps ran for real, the 0-to-1 step ran on the fake `claude`. A real row will show it as `forced_applied: true`.
2. AC-3 (luna sends no text before a mid-answer kill) is still open and now matters more: a luna phase 2 killed at the widened deadline still salvages nothing.
3. The hang guard is 3.0 x B_A1 even where only the phase-2 clock was too short. That is the owner's number; a package whose phase 1 hangs now takes up to 3 x B_A1 to be declared `hang_kill`.
4. Spike 4's exit 3 on hl2 runs 1 and 3 and el2 run 3 (noted in `SLACK.md`) was not investigated here.
