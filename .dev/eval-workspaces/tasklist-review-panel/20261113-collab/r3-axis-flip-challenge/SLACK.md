# Redesign 3 (Axis-Flip Challenge): time cap 1.35 x B + SLACK_S (SLACK_S = 30)

Owner decision 2026-11-14: the cap is `1.35 x B + SLACK_S`. Set by the environment variable `PANEL_SLACK_S` (default 0, which keeps every old number). Nothing was staged, committed or pushed. No model session was started. Only files under this folder changed.

## 1. What changed

| File | Lines | Change |
|---|---|---|
| `r3lib/values.py` | 21-38 | New `slack_s()` (reads `PANEL_SLACK_S`; empty = 0; refuses text, negative, nan, inf with `E_SLACK`) and `slack_tag()` (30 -> `slack30`) |
| `r3lib/values.py` | 41-68 | `compute_n`: box = `1.30 x B_f + S - (t_launch - T0)`, and the fixed box cap (`box_cap_s`, 35 on EL2) becomes `box_cap + S`. `compute_k`: `0.35 x B + S - ...`. `finish_offset` (and so `finish_at`): `1.35 x B + S - ...` |
| `r3lib/values.py` | 133, 243 | `planning()` and `freeze()` record `"slack_s"` in the values file |
| `r3lib/values.py` | 156-160, 170-173 | `load()` refuses a frozen file whose `slack_s` differs from `PANEL_SLACK_S` (old files have none = 0); the "missing" message names the slack fix |
| `r3lib/paths.py` | 41-50 | `values_file(panel)` reads `values-slack<S>/<panel>.json` when `PANEL_SLACK_S` is above 0, else `values/<panel>.json` (the `R3_VALUES_FILE` test override still wins) |
| `r3lib/metrics.py` | 836-846 | Arm summary cap check: `median_ok` and `over_135` use `1.35 x B_c + S`. `over_150` (1.5 x B_c) unchanged |
| `lib/package.sh` | 29-30, 70 | `P2_DEADLINE = T0 + 1.30 x B_f + S` (the phase-2 kill time, the 30% share of the 35% cap) and the same `+ S` in the scheduler's `n_now` box and box cap. `HANG_AT = T0 + 1.5 x B_f` unchanged. `S` comes from the values JSON (`slack_s`), which `values-show` has already checked against the environment |
| `bin/launch-panel.sh` | 26-31, 56 | Preflight: `PANEL_SLACK_S` above 0 and the slack values file missing -> prints the path and the freeze command, **exit 2**, nothing launched (skipped for `R3_SMOKE=1` / `R3_SPIKE4=1`, which use planning values, and when the test override `R3_VALUES_FILE` is set). `run.json` now records `slack_s` |
| `tests/test_slack.py` | new | 13 tests (section 4) |
| `values-slack30/{el2,sl2,hl2}.json` + `.json.sha256` | new | Frozen values recomputed from the Spike 4 rows on disk (section 3) |

Not changed: `config/` (so `pins.json` stays valid; `pin --check` prints `pins ok`), `values/` (the three old files and their `.sha256` are byte-identical: el2 `25f76cf3...`), the 1.5 x B hang guard, the `over_150` check, `turn_p90`, `B_f` and `T_report_p90` (the same Spike 4 data gives the same numbers; only `k` and `panel_finish_offset_s` differ).

## 2. Launch commands (PANEL_SLACK_S=30)

Run from this folder. Each launch runs all three packages in parallel and holds the gateway lock. Values files already exist for all three panels, so no Spike 4 is needed.

```bash
cd /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge
# <panel> = el2 (ember + 2x luna) | sl2 (sonnet + 2x luna) | hl2 (haiku + 2x luna)
flock /tmp/collab-gateway.lock env NOFALLBACK=1 PANEL_SLACK_S=30 PANEL_COLLAB=1 bash bin/launch-panel.sh <panel>   # collaboration on
flock /tmp/collab-gateway.lock env NOFALLBACK=1 PANEL_SLACK_S=30 PANEL_COLLAB=0 bash bin/launch-panel.sh <panel>   # baseline
```

Summary of slack runs: `PANEL_SLACK_S=30 bash -c 'source lib/common.sh; r3_py summarize --panel <panel>'` (the cap check needs the same variable). Every launch appends one row to `results/results.jsonl`; the row's `values_sha256` is the slack file's hash, and `run.json` carries `slack_s: 30`. Do not mix slack and no-slack rows in one summary.

## 3. New k per panel and package (old = `values/`, new = `values-slack30/`)

Frozen from the same 3 Spike 4 runs per panel as the old files: el2 `el2-c0-20261114T052713Z-43b2`, `...T052937Z-e3dc`, `...T053114Z-0af7`; sl2 `sl2-c0-20261114T090920Z-0a45`, `...T091511Z-d76f`, `...T092046Z-600c`; hl2 `hl2-c0-20261114T070925Z-55fd`, `...T071737Z-d6a2`, `...T072325Z-9571`. Command (example): `PANEL_SLACK_S=30 bash -c 'source lib/common.sh; r3_py values-freeze --panel el2 --runs <3 run ids>'`.

k = messages a reviewer may act on (0 to 2). Finish offset = the time after T0 by which the critical reviewers must have sealed. It is logged only; this design (F1) acts on neither for the control package.

| Panel | Package | B_f (s) | k old -> new | Finish offset old -> new (s) |
|---|---|---|---|---|
| el2 | design | 137.8 | 0 -> **2** | 160.3 -> 190.3 |
| el2 | designSpec | 92.1 | 0 -> **1** | 104.5 -> 134.5 |
| el2 | makeTheAliasOnly | 100.9 | 0 -> **1** | 114.7 -> 144.7 |
| sl2 | design | 214.0 | 1 -> 1 | 253.0 -> 283.0 |
| sl2 | designSpec | 270.9 | 1 -> 1 | 312.6 -> 342.6 |
| sl2 | makeTheAliasOnly | 330.4 | 2 -> 2 | 404.9 -> 434.9 |
| hl2 | design | 203.5 | 0 -> 0 | 219.0 -> 249.0 |
| hl2 | designSpec | 327.9 | 0 -> **1** | 391.6 -> 421.6 |
| hl2 | makeTheAliasOnly | 303.3 | 0 -> **1** | 358.8 -> 388.8 |

n (challenges a receiving reviewer may start; this is what F1 actually uses), computed with `compute_n` for a receiver that starts phase 2 at T0 + B_f, start cost 6 s, the Spike 4 turn p90, old -> new. A receiver that starts later gets less; this is a planning view, not a measurement:

| Panel | Package | Reviewers (cap): n old -> new |
|---|---|---|
| el2 | design | ember t2b-1 (3): 3 -> 3; luna t4-1 (2): 1 -> 2; luna t3-1 (2): 1 -> 2 |
| el2 | designSpec | ember 3 -> 3; luna t4-1: 0 -> 2; luna t3-1: 0 -> 2 |
| el2 | makeTheAliasOnly | ember 3 -> 3; luna t4-1: 0 -> 2; luna t3-1: 0 -> 2 |
| sl2 | design | sonnet t1b-1 (3): 1 -> 2; luna 2 -> 2; luna 2 -> 2 |
| sl2 | designSpec | sonnet 2 -> 2; luna 2 -> 2; luna 2 -> 2 |
| sl2 | makeTheAliasOnly | sonnet 2 -> 3; luna 2 -> 2; luna 2 -> 2 |
| hl2 | design | haiku t2-1 (3): 0 -> 1; luna 2 -> 2; luna 2 -> 2 |
| hl2 | designSpec | haiku 1 -> 1; luna 2 -> 2; luna 2 -> 2 |
| hl2 | makeTheAliasOnly | haiku 1 -> 1; luna 2 -> 2; luna 2 -> 2 |

Still k = 0 (or n = 0): hl2 design has k = 0 (haiku turn p90 is 36.8 s; (0.35 x 203.5 + 30 - 2 - 36.8 - 18.9) / 73.5 = 0.59). Nobody has n = 0 any more at T0 + B_f.

## 4. Tests

| Run | Result |
|---|---|
| Full suite, no model calls (`tests/`, command in IMPLEMENTATION.md section 3), default `PANEL_SLACK_S` unset | **102 passed, 0 failed, 0 skipped** in 231 s (`slack-report/tests-full.log`). The 89 pinned tests of the earlier report pass unchanged, plus 13 new |
| `tests/test_slack.py` alone | 13 passed |
| `ruff check r3lib tests` / `ruff format --check` | All checks passed / 32 files already formatted |
| `bash -n` on `bin/launch-panel.sh`, `lib/package.sh` | ok |

The 13 new tests: default 0 leaves `compute_k`, `finish_offset`, `compute_n` and the values path unchanged; `k` goes 0 -> 2 for the el2 design Spike 4 numbers; `finish_offset` and `finish_at` gain exactly 30; `compute_n` gains the slack in the box and in the box cap (1 -> 2, late launch 0 -> 1, no-cap panel 0 -> 1); four bad values (`abc`, `-1`, `nan`, `inf`) are refused; the summary cap check passes 140 s against B_c 100 s with slack 30 (`median_ok` true, `over_135` 0, `over_150` still 1); the slack values path, the missing-file message, the slack-mismatch refusal and the planning value; the launcher exits 2 with a clear message when the slack values are missing; and two launches on the fake `claude` (slack 0 and 30) check `P2_DEADLINE - T0 = 1.30 x B_f + S`, `HANG_AT - T0 = 1.5 x B_f` and `run.json.slack_s`. The suite ran before one formatting-only pass (`ruff format` on three files); the touched test files and the full run were repeated afterwards (13 and 102 passed).

## 5. What still refuses to run, and what to watch

Nothing refuses to run for these 6 launches: `values-slack30/` exists for all three panels, `pin --check` passes, `values-show` loads each file with its sha256. Refusals that remain by design: `PANEL_SLACK_S` other than 30 (for example 7) exits 2 until its own `values-slack<S>/` is frozen; a malformed `PANEL_SLACK_S` exits 1; a values file frozen with another slack is refused. Still open from `IMPLEMENTATION.md` section 7 and not touched: AC-3 (luna sends no text before a mid-answer kill, so a killed luna phase 2 salvages nothing), so a late luna can still burn its time for nothing. The Spike 4 logs show exit 3 for hl2 runs 1 and 3 and el2 run 3; the freeze accepted those runs (the cause of exit 3 was not looked into).

Calls that were mine and the owner may overrule:
1. **The fixed box cap** `box_cap_s` (35 s on EL2) also got `+ S` (65 s). It is the 30% share of 116 s written as a constant, so I treated it as derived from the cap. Without it, EL2's lunas stay at n = 1 whatever the slack.
2. **The 1.5 x B hang guard is now earlier than the cap on small B.** Phase 1 is killed at 1.5 x B_f; the phase-2 deadline is 1.30 x B_f + 30, which is later than 1.5 x B_f when B_f is below 150 s (all three el2 packages: 92-138 s). The guard only covers phase 1, so nothing breaks, but an el2 phase 2 can now end past 1.5 x B_c and show up in `over_150` of the summary (the "none over 1.5 x B_c" rule, left unchanged as instructed). For sl2 and hl2 (B 200-330 s) the cap and the guard stay apart.
3. Mixed rows: slack and no-slack rows both go to `results/results.jsonl`; summarise each with its own `PANEL_SLACK_S`.
