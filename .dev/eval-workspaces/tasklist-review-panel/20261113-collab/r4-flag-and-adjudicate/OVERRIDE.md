# R4 (Flag-and-Adjudicate): owner-authorised time-cap exception (`TIME_CAP_EXCEPTION=1`)

Owner decision 2026-11-14: the +35% elapsed-time rule may be exceeded. Spike 4's measured turn times make `k = 0` on 8 of the 9 panel-package pairs (only SL2 on the control package has `k = 1`), so without this the collaboration arm is refused or runs with nothing happening. This file records the one explicit, default-off exception, the numbers it uses, the one real smoke row, and the launch commands. Nothing outside this folder was edited, nothing was staged or committed.

## 1. What changed (paths relative to this folder; line numbers as of this write)

| File | Lines | Change |
|---|---|---|
| `lib/values.py` | 62-77 | `TCE_HANG_X = 3` and `tce_entry(v)`: from one package's values entry returns `k = max(1, measured k)`, `k_measured`, `k_forced`, the widened `hang_s` and `finish_offset_s` (formulas in section 2). Pure function; never called when the override is off |
| `lib/values.py` | 12, 310-316 | CLI `values.py tce --values <file> --pkg <id>`: prints that entry as JSON, writes no file |
| `bin/run-panel.sh` | 33-35 | `TCE=${TIME_CAP_EXCEPTION:-0}` (default off) |
| `bin/run-panel.sh` | 51-53, 67-69, 87-90 | Preflight refusals (exit 2, logged to `runs/refusals.jsonl`): value not `0`/`1`; `PANEL_COLLAB` not `1`; values file `kind` is `planning` or `srun`; a package with `deliver` not true. It also computes `tce_entry` for every selected package before any work |
| `bin/run-panel.sh` | 92 | The "F7 not runnable: k = 0 on every package" refusal applies only when the override is off |
| `bin/run-panel.sh` | 98, 105-107, 115, 154-156, 221 | Stderr banner; `run.json` gets `time_cap_exception`; each package's effective `k`, `finish_offset_s`, `hang_s` replace the values-file ones (`V + tce_entry`), which feeds the existing `K`, `F`, `H`, board, helper `--cap 2k` and hook arguments unchanged; `panel.json` gets `time_cap_exception`, `k_measured`, `k_forced`, `finish_offset_s`, `hang_s`; the `schedule.jsonl` line gets `time_cap_exception: true` |
| `lib/collab.py` | 254-259 | `collab.json` gets `time_cap_exception`, `k_measured`, `k_forced`, `hang_s`, `finish_offset_s`, `elapsed_over_baseline`, `delivered_per_reviewer` |
| `lib/results.py` | 123-128, 161 | Results row gets top-level `time_cap_exception` (true or false) and, in each `collab.<pkg>`, the same columns plus `elapsed_s` (`baseline_elapsed_s` was already there and is B_A1) |
| `lib/arm_summary.py` | 49-76 | `summarize` moves every row stamped `time_cap_exception` out of the cap-obeying statistics (A1 side too) into its own block `time_cap_exception` = `rows` (columns below) + `stats` (the same analysis over those rows only, without the `time_verdict`, `slo` and `interim_futility` keys, which test the cap this exception waives) + a note; `n_arm_time_cap_exception` counts them |
| `frozen/pins.sha256` | lines 8-10 | Re-pinned (section 4) |
| `tests/test_time_cap_exception.py` | new, 9 tests | Section 5 |

`bin/reviewer.sh`, `bin/r4-hook`, `bin/panel-post` and every frozen text are unchanged. The reviewer's hang kill reads `hang_ms` from `panel.json`, the hook and the card writer receive the finish time as a baked argument, so the widened numbers reach them without touching those scripts.

Another session changed the same folder at the same time for the "30 s slack" decision (`SLACK.md`: `PANEL_SLACK_S`, `values-slack30/`, `tests/test_slack.py`; it also edited `lib/values.py`, `lib/arm_summary.py`, `bin/run-panel.sh` and re-pinned). The two changes coexist: with both off nothing changes; the exception does not read `PANEL_SLACK_S`.

## 2. The numbers

Override off: nothing is computed differently (the code path is not entered; a test checks `k`, `hang_ms` and `finish_ms` of an off row against the values file).

Override on, per package (`B` = the values file's `B_A1`):

- `k` = 1 where the measured `k` is 0; a measured `k` of 1 or 2 stays. Card cap `2k`, at most `k` cards delivered per luna (so 2 cards, 1 per luna, when forced).
- Hang guard `hang_s` = `max(existing 1.5 B, 3.0 B)`. In integer milliseconds. It is always `3.0 B` for these values.
- Finish offset = `new hang_s - (old hang_s - old finish_offset_s)`. The old distance (`0.15 B + turn_p90 + T_report_p90`) is kept, so the finish signal still arrives that long before the kill, and nothing is delivered or posted after it. This is a choice, not a derivation; the finish signal fires only when a reviewer is still making tool calls that late (it did not fire in the smoke).
- Applied to every package of an exception row (also those whose measured `k` is already 1), so one row never mixes two timer regimes. The kill timer stays on (`timeout --kill-after=5`), the 2-attempt retry and the re-ask keep drawing on the same (now wider) guard.

Values (from `values/<P>.json`, Spike 4, no slack):

| Panel | Package | B_A1 (s) | k measured | k used | hang old (s) | hang new (s) | finish old (s) | finish new (s) |
|---|---|---|---|---|---|---|---|---|
| EL2 | design (control) | 114.121 | 0 | 1 | 171.181 | 342.363 | 58.038 | 229.22 |
| EL2 | designSpec | 102.512 | 0 | 1 | 153.768 | 307.536 | 18.289 | 172.057 |
| EL2 | makeTheAliasOnly | 131.79 | 0 | 1 | 197.685 | 395.37 | 93.342 | 291.027 |
| HL2 | design (control) | 218.856 | 0 | 1 | 328.284 | 656.568 | 165.594 | 493.878 |
| HL2 | designSpec | 248.079 | 0 | 1 | 372.118 | 744.237 | 236.603 | 608.722 |
| HL2 | makeTheAliasOnly | 280.09 | 0 | 1 | 420.135 | 840.27 | 244.985 | 665.12 |
| SL2 | design (control) | 258.964 | 1 | 1 | 388.446 | 776.892 | 312.131 | 700.577 |
| SL2 | designSpec | 207.69 | 0 | 1 | 311.535 | 623.07 | 176.532 | 488.067 |
| SL2 | makeTheAliasOnly | 211.948 | 0 | 1 | 317.922 | 635.844 | 244.625 | 562.547 |

## 3. Stamping and columns

A row run with `TIME_CAP_EXCEPTION=1` has `time_cap_exception: true` in `run.json`, every `panel.json`, every `collab.json`, `results/<row>.json` (top level and `collab.<pkg>`) and its `schedule.jsonl` line. Rows without the override have it `false` (or absent in older files, which every reader treats as false).

Per package, `results/<row>.json` `collab.<pkg>` holds: `baseline_elapsed_s` (B_A1), `elapsed_s` (measured, `(last reviewer end - T0)`), `elapsed_over_baseline` (the ratio), `k_measured`, `k_forced`, `k`, `hang_s`, `finish_offset_s`, and `delivered_per_reviewer` (`{rid: cards delivered to it}`; the flagger is always 0, each luna 0 or 1 at `k = 1`). `cards_sent`, `cards_delivered`, `conversions`, `passed_lines` are the existing columns.

`lib/arm_summary.py` reports the same columns per row and package under `time_cap_exception.rows[].packages.{DS,AL,DE}` and never mixes those rows into the cap-obeying figures (tested: the cap-obeying output is identical with and without exception rows added). A1 isolated baseline rows can not be run with the override (section 6), so the baseline side of a comparison is always cap-obeying.

## 4. Re-pin

Procedure of design section 1.1 (`sha256sum`, by hand, only the changed files, before any arm): recomputed the lines of `lib/values.py`, `lib/results.py` and `lib/arm_summary.py` in `frozen/pins.sha256`; no other line changed. After this session's edits and the slack session's, the pinned values are `values.py 67e7b83b...9738`, `results.py 6771b5a4...51c1`, `arm_summary.py 62b299ba...54a4`; `sha256sum -c pins.sha256` run from `frozen/` prints no failure, and the launcher's own preflight passed for the smoke row. Every other check is untouched: `NOFALLBACK=1`, observed model equals requested model (`model_ok`), the allowed-model and glm/qwen/opus refusals, the audit and contamination checks, the anonymiser, and the unchanged blind judge (`claude-opus-5-5`).

## 5. Tests

Command, from the repository root: `uv run pytest .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r4-flag-and-adjudicate/tests`.

Result after the last code change: **124 passed, 0 failed, 258 s** (106 existing + 9 new + 9 of the slack session). `ruff check lib tests` clean. An earlier run showed 5 failures (`pins check failed`) because the slack session re-pinned `values.py` while the suite was running; the rerun on stable files passed.

`tests/test_time_cap_exception.py`: `tce_entry` vectors (EL2 control package, SL2 control package with measured `k = 1`, `k = 2`, a hang guard already above 3 B), no mutation, the CLI writes nothing; launcher refusals (value `2`, `PANEL_COLLAB=0`, planning values, `deliver` false; off and `=0` still refuse an all-`k = 0` row); an override-on offline row on a `k = 0` package (k forced to 1, collaboration on, hang exactly 3.0 B, finish exactly as in section 2, card cap 2, hook arguments `--k 1`, at most one card per luna, stamps and columns in `run.json`, `panel.json`, `collab.json`, the results row and `schedule.jsonl`); override on with a measured `k = 2` (k kept, hang widened); override off (`k`, `hang_ms`, `finish_ms` equal the values file, stamps false, no schedule stamp); `arm_summary` with exception rows apart and with only exception rows.

## 6. One real smoke row (override on)

`PANEL_COLLAB=1 TIME_CAP_EXCEPTION=1 NOFALLBACK=1`, panel EL2 (muse-ember-1.0 flagger `t2b-1`, gpt-6-luna `t4-1` and `t3-1`), control package `TASK-WF-design-20261108-041415`, measured `values/EL2.json`, row `tce-smoke-f7-el2-1` (`runs/tce-smoke-f7-el2-1/`, `results/tce-smoke-f7-el2-1.json`), 3 reviewer sessions at once plus 1 Opus judge session. Checked by `/tmp/tce/check_smoke.py` (not part of the build); its output is `spikes/out/smoke-check-tce-smoke-f7-el2-1.json`.

**Result: every check passes (`all_ok: true`, 38 checks).** The design 6.4 conditions: three `model_ok` with the expected models, `dropped_lines` 0, no re-ask, one attempt each, `merged-1.md`, `merged-anon.md` and `score.json` exist, anonymiser clean, `collab.json` keys, `cards_sent` 2 (at least 1), both cards `delivered`, both lunas `seal_sha_ok`, `audit_ok`, `harness_text_gt_overlap` 0, `board_lines_invalid` 0, no `QUARANTINED`, nothing under `EVAL` newer than the run start, no `/tmp/jdg.*` left, every 5.2 key present, `valid: false` (one package, by definition). Exception checks: stamped in all four places; `k = 1`, `k_measured = 0`, `k_forced = true`; hang guard 342.363 s (3.0 B); card cap 2; each luna received at most 1.

| Column | Value |
|---|---|
| B_A1 | 114.121 s |
| Measured elapsed | 111.427 s |
| Elapsed / baseline | 0.9764 |
| Forced k | 1 (measured 0) |
| Cards sent / delivered | 2 / 2 (c0 challenge to `t4-1`, c1 finding to `t3-1`) |
| Delivered per reviewer | `t2b-1` 0, `t4-1` 1, `t3-1` 1 |
| Finish signal | not fired; no hang kill |
| Reviewer wall | 68.7 s flagger, 111.3 s `t4-1`, 82.2 s `t3-1` |
| Card tasks | T1 (c0), T3 (c1) |
| Conversions | 0 of 2: `t3-1` wrote `card c1: passed`; `t4-1` neither converted c0 nor wrote a passed line |
| `flag_finding_overlap`, `adjudication_agreement` | 0.0, 0.0 |
| Judge (descriptive) | found 0 of 2 control items, 1 wrong blocker, 4 ledger rows |

So the collaboration path ran on real models with the forced `k = 1`: the flagger posted 2 cards, the hook delivered each once on the luna's 6th tool call after a sealed snapshot. The elapsed time was not longer than the baseline here, so this row does not show the cost of the exception; whether a luna acts on a delivered card is open (1 of 2 settled it visibly). One row says nothing about the arm's value.

## 7. Launch commands

Run each from any directory. Each holds the shared gateway lock, so run them one after another; a row id can be used once. The launcher waits up to 30 minutes for at most 7 model sessions host-wide (other experiments count), then refuses the remaining packages. Rows run all three packages, are judged, and write `results/<row>.json`. Use the measured files `values/<P>.json` (not `-srun`, not `planning-`); with the slack decision (`SLACK.md`) use `PANEL_SLACK_S=30` and the files that session built instead (the override takes any non-planning, non-srun values file with `deliver` true, so it should accept those too; that combination was not run). Change `r01` for a repeat.

```bash
R4=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r4-flag-and-adjudicate

# EL2 (muse-ember-1.0 + 2x gpt-6-luna): collaboration row with the exception
TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 NOFALLBACK=1 flock /tmp/collab-gateway.lock $R4/bin/run-panel.sh --panel EL2 --row tce-f7-el2-r01 --values $R4/values/EL2.json --block tce-b01
# HL2 (claude-haiku-5-5 + 2x gpt-6-luna)
TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 NOFALLBACK=1 flock /tmp/collab-gateway.lock $R4/bin/run-panel.sh --panel HL2 --row tce-f7-hl2-r01 --values $R4/values/HL2.json --block tce-b01
# SL2 (claude-sonnet-5-5 + 2x gpt-6-luna)
TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 NOFALLBACK=1 flock /tmp/collab-gateway.lock $R4/bin/run-panel.sh --panel SL2 --row tce-f7-sl2-r01 --values $R4/values/SL2.json --block tce-b01
```

Isolated baseline row with the same harness (arm A1, cap-obeying, no override; `TIME_CAP_EXCEPTION=1` with `PANEL_COLLAB=0` is refused):

```bash
PANEL_COLLAB=0 NOFALLBACK=1 flock /tmp/collab-gateway.lock $R4/bin/run-panel.sh --panel EL2 --row a1-el2-r01 --values $R4/values/EL2.json --block tce-b01
PANEL_COLLAB=0 NOFALLBACK=1 flock /tmp/collab-gateway.lock $R4/bin/run-panel.sh --panel HL2 --row a1-hl2-r01 --values $R4/values/HL2.json --block tce-b01
PANEL_COLLAB=0 NOFALLBACK=1 flock /tmp/collab-gateway.lock $R4/bin/run-panel.sh --panel SL2 --row a1-sl2-r01 --values $R4/values/SL2.json --block tce-b01
```

Arm summary after rows exist (exception rows are reported apart automatically):

```bash
uv run --frozen --project /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel python $R4/lib/arm_summary.py --panel EL2 --a1 $R4/results/a1-el2-*.json --arm $R4/results/tce-f7-el2-*.json --out $R4/results/EL2-F7-tce-summary.json
```

## 8. Limits and open points

- Not run: any full three-package row (the orchestrator's), the SL2 and HL2 smoke. HL2 and SL2 behave like EL2 by construction (same code path) but were exercised only in offline tests.
- The 3.0 B hang guard means a stuck reviewer can run up to 3 x the baseline before it is killed; the row's elapsed ratio then shows it. Elapsed above 3.0 B is impossible by design, so a ratio near 3 means a kill (`hang_kill`, `slo_breach`).
- The finish signal almost never fires in an exception row (finish is at 1.5 to 2.9 B); on ember and haiku it was ignored anyway in Gate 0, so the bound is the hang guard.
- `lib/` is git-ignored by the repository (IMPLEMENTATION.md note 15): the edited `lib/*.py` files are on disk and run, but committing them needs `git add -f` on `R4/lib`; this session did not stage anything.
- `DESIGN.md` and `IMPLEMENTATION.md` were not edited; this file is the record of the exception.
