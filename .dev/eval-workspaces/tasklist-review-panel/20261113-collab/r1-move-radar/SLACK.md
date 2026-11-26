# Redesign 1, Move Radar: the +30 s slack on the time cap

Owner decision 2026-11-14: the time cap is `1.35 x B + SLACK_S`, `SLACK_S = 30` (env `PANEL_SLACK_S`, default 0 = the old behaviour).
Done 2026-11-14 with no model session. Abbreviations: `REPO` = `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel`,
`R1` = `REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar`.

## 1. What changed

| File | Lines | Change |
|---|---|---|
| `tools/values.py` | 13-15, 33-43 | `slack_s()` reads `PANEL_SLACK_S` at call time (unset or empty = 0, negative refused); `values_dir()` = `values` at 0, else `values-slack<S>` |
| `tools/values.py` | 51-52, 56-57, 66 | `k_for`: `0.35 B + SLACK_S`; `finish_offset`: `1.35 B + SLACK_S - turn - T_report`; `guard_offset`: `min(1.35 B + SLACK_S - G, finish_off)`. The A-2 reader k follows from the finish offset. Hang guard `1.5 B` unchanged |
| `tools/values.py` | 106, 129-141 (spike4), 226-227 (load), 239-240, 248 (deadlines) | values files carry `slack_s`; `spike4` writes to `values_dir()` (still refuses to overwrite, per directory); `load` refuses a file whose `slack_s` differs from the environment; with a non-zero slack `deadlines` has no planning fallback (exit 2 when the slack values are missing, collab 0 as well as collab 1); output has `slack_s` |
| `tools/alarms.py` | 8, 62, 66 | the SLO limit is `1.35 x B_c + SLACK_S` |
| `tools/launch.sh` | 47-50, 62-64, 111 | reads `PANEL_SLACK_S` (whole number, 0 or more, else exit 2), exports it, uses `values-slack<S>/` when non-zero, exits 2 naming the missing `values-slack30/<panel>/<pkg>.json` (or its `.sha256`) for collab 1 and for collab 0, writes `slack_s` into `runs/<row>/<pkg>/run.json` |
| `tests/test_slack.py` | new, 10 tests | see section 4 |
| `values-slack30/<panel>/<pkg>.json` + `.sha256` | 9 + 9 files | recomputed from the Spike 4 rows already on disk (`el2-c0-r1..3`, `sl2-c0-r1..3`, `hl2-c0-r1..3`) |

Not changed: `values/` (the 18 original files are byte-identical, checked with `sha256sum -c`), `config/`, `manifest.json` (its pins cover the catalogue, brief and judge script, none of which changed), the hook, `gate0-check.sh` and `spikes/gate0.json`.
Run to recompute (done): `PANEL_SLACK_S=30 uv run python R1/tools/values.py spike4 <panel> <panel>-c0-r1 <panel>-c0-r2 <panel>-c0-r3` for `el2`, `sl2`, `hl2`. Each new `.sha256` verifies; `run.json` records the hash as `values`.

## 2. How to launch one panel on all three packages with `PANEL_SLACK_S=30`

Run from `REPO`. `<rep>` is a whole number of 1 or more. Collab-1 rows can use reps 1-3 (their collab-0 partners from Spike 4 exist). A new collab-0 row under slack must use a rep that has no results file yet (reps 1-3 are finished rows, a launch exits 2), so use 4 or more, and run the collab-1 partner at the same rep.

| Panel | Collab 1 | `PANEL_COLLAB=0` |
|---|---|---|
| ember + 2x luna (`el2`) | `cd REPO && PANEL_SLACK_S=30 PANEL_COLLAB=1 bash R1/tools/launch.sh el2 <rep>` | `cd REPO && PANEL_SLACK_S=30 PANEL_COLLAB=0 bash R1/tools/launch.sh el2 <rep>` |
| sonnet + 2x luna (`sl2`) | `cd REPO && PANEL_SLACK_S=30 PANEL_COLLAB=1 bash R1/tools/launch.sh sl2 <rep>` | `cd REPO && PANEL_SLACK_S=30 PANEL_COLLAB=0 bash R1/tools/launch.sh sl2 <rep>` |
| haiku + 2x luna (`hl2`) | `cd REPO && PANEL_SLACK_S=30 PANEL_COLLAB=1 bash R1/tools/launch.sh hl2 <rep>` | `cd REPO && PANEL_SLACK_S=30 PANEL_COLLAB=0 bash R1/tools/launch.sh hl2 <rep>` |

(Write `R1` out in full: `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar`.) `NOFALLBACK` unset or 1. Without `PANEL_SLACK_S` the launcher behaves exactly as before and reads `values/`.
Exit codes as in IMPLEMENTATION.md section 3 (0 ok, 1 row written with a bad package, 2 refused).

## 3. New k next to the old one (from `values-slack30/` and `values/`)

k = messages a reviewer may act on, as `{searcher, reader}`; el2 uses one number for both (R-42), sl2 and hl2 have the A-2 reader k. Seconds from T0; guard 0 or less means the hook skips every injection.

| Panel | Package | B (s) | k old | k new | Finish offset old to new (s) | Guard offset old to new (s) |
|---|---|---|---|---|---|---|
| el2 | designSpec | 83.8 | 0 / 0 | 0 / 0 | 53.8 to 83.8 | 53.8 to 83.8 |
| el2 | makeTheAliasOnly | 145.1 | 0 / 0 | 0 / 0 | 103.2 to 133.2 | 103.2 to 133.2 |
| el2 | design | 97.0 | 0 / 0 | 0 / 0 | 40.2 to 70.2 | 40.2 to 70.2 |
| sl2 | designSpec | 165.8 | 0 / 0 | **0 / 1** | 138.3 to 168.3 | -22.0 to 8.0 |
| sl2 | makeTheAliasOnly | 302.3 | 0 / 2 | 0 / 2 | 319.0 to 349.0 | 183.6 to 213.6 |
| sl2 | design | 197.6 | 0 / 1 | 0 / 1 | 169.6 to 199.6 | 101.2 to 131.2 |
| hl2 | designSpec | 231.1 | 0 / 0 | 0 / 0 | 110.6 to 140.6 | -402.8 to -372.8 |
| hl2 | makeTheAliasOnly | 342.1 | 0 / 2 | 0 / 2 | 255.1 to 285.1 | -201.9 to -171.9 |
| hl2 | design | 203.7 | 0 / 0 | 0 / 0 | 49.1 to 79.1 | -67.9 to -37.9 |

Hang guard (`1.5 x B`) unchanged, in seconds (designSpec / makeTheAliasOnly / design): el2 126 / 218 / 145, sl2 249 / 453 / 296, hl2 347 / 513 / 306.

## 4. Tests

`cd REPO && uv run pytest R1/tests -q -p no:cacheprovider` (no model calls; stub `claude` and `superclaude`): **148 passed, 0 failed, 0 skipped, 46.9 s** (the 138 earlier tests unchanged plus 10 new in `tests/test_slack.py`). `uv run ruff check R1`: all checks passed. `bash -n` on every script in `tools/` and `spikes/`: clean.
`test_slack.py`: default 0 leaves `k_for`, `finish_offset`, `guard_offset` unchanged; empty is 0, negative is refused; slack 30 changes `k_for` for two cases that were 0 (B 100 / 238), finish offset +30, guard offset +30; the measured sl2 designSpec case gives reader k 0 to 1, finish and guard +30, hang guard equal, on every planning panel finish +30 and hang equal; `spike4` under slack writes `values-slack30/` with a matching `.sha256`, leaves `values/` byte-identical and refuses a second write; `deadlines` follows the slack directory, refuses (exit 2) without slack values for collab 0 and 1, and `FINISH_MS` is exactly 30 000 ms later; a values file with another `slack_s` is refused; `alarms.py` SLO limit moves from 156.6 s to 186.6 s; `launch.sh` exits 2 without the slack values (collab 1 and 0) and for `abc`, `-5`, `3.5`, `030`, empty; with slack values it runs, writes `slack_s` 30 and the new finish offset into `run.json`.

## 5. What does not give the owner's intended result, and what still refuses

1. **The extra 30 s hardly moves k.** k divides the headroom by two receiver turns (`2 x turn_p90`; at the measured 12-44 s turns that is 24 to 88 s), so 30 s adds 0.3 to 1.25 messages before rounding down. Only one of nine cells changed (sl2 designSpec, reader 0 to 1). The searcher k stays 0 on sl2 and hl2, and el2 stays 0 on all three packages. If every reviewer should be able to act on at least one message, the time formula itself has to change (owner decision; not done here).
2. **The guard offset is at or below 0 for hl2 (all packages) and 8 s for sl2 designSpec.** The guard is `1.35 B + 30 - G` with `G = 47 x turn_p90[crit] / 6.4` (A-3), 166 to 715 s on sl2 and hl2; slack does not rescue it, so the hook skips every injection there (`skip guard`). Not changed, because the instruction covered only adding the slack.
3. Finished rows are never re-run: collab-0 reps 1-3 on all three panels and `el2-c1-r0` have `results/*.json`, so launching them exits 2 (rep 0 is smoke and is ignored by `alarms.py`). Collab 0 under slack needs a new rep (4 or more).
4. `PANEL_SLACK_S=30` with collab 0 also needs the slack values (no planning fallback), as the instruction asked; the collab-0 hang guard is the same `1.5 x B`.
5. `gate0-check.sh` / `gate0.json` are not slack-aware; the launcher does not read the `Spike 4` entry (it checks the values files itself), so nothing is blocked by it. Its stored `Spike 4: missing` (sl2) is stale from 07:29 UTC.
6. Row names do not carry the slack. A slack-30 row `el2-c1-r1` and a slack-0 row of the same name cannot both exist; tell them apart by `slack_s` in `runs/<row>/<pkg>/run.json` and the `values` hash in the results row.
7. Collab-0 baselines at reps 1-3 were run with planning values and the 2.0 x planning-B hang guard, before slack existed; slack does not affect a collab-0 run except through the unchanged hang guard.
