# R4 (Flag-and-Adjudicate): time cap with slack, 1.35 B + SLACK_S

Owner decision 2026-11-14: the time cap is `1.35 x B + SLACK_S` with `SLACK_S = 30` seconds. `SLACK_S` is read from the environment variable `PANEL_SLACK_S` (default 0, which is the old cap; every old pinned test and file is unchanged). No model session was run for this change.

## 1. What changed (all paths relative to this folder; line numbers as of this write)

| File | Lines | Change |
|---|---|---|
| `lib/values.py` | 4-5, 34-39 | `slack_s()` reads `PANEL_SLACK_S` (non-negative number, else exit with a message) |
| `lib/values.py` | 42-48 | `k_of`: numerator `0.35 B + SLACK_S - hooks - turn - rep` (integer ms, optional `slack=` argument, default from the environment) |
| `lib/values.py` | 51-54 | `finish_offset`: `1.35 B + SLACK_S - turn - rep` |
| `lib/values.py` | 80-87 | `slowdown_limit`: `(0.35 B + SLACK_S - W) / B` |
| `lib/values.py` | 196-208 | `out_dir()` writes to `values-slack<S>/` when slack > 0 (the old `values/` is never written); `write_pinned` stamps `"slack_s": 30` in every file it writes when slack > 0 (nothing is stamped at 0, so old output is byte-identical) |
| `lib/values.py` | unchanged | `hang_s` (1.5 B) and `tce_entry` (keeps its distance to the hang guard) are not derived from the 35% cap |
| `lib/arm_summary.py` | 16, 140, 168 | The two `1.35 * B_c` limits (SLO budget share, per-package time verdict) become `1.35 * B_c + SLACK_S`; the 1.5 B hang guard check is unchanged |
| `bin/run-panel.sh` | 36, 52, 58-61, 66, 105-107 | Reads `PANEL_SLACK_S`; refuses a non-number; with slack > 0 and no `--values` it uses `values-slack<S>/<panel>.json`, and exits 2 if that file (or its `.sha256`) is missing; refuses (exit 2) any values file whose `slack_s` differs from `PANEL_SLACK_S` (so old files cannot be used under slack and slack files cannot be used without it); stamps `slack_s` in `run.json` |
| `frozen/pins.sha256` | lines 8, 10 | New sha256 of `lib/values.py` and `lib/arm_summary.py` (the only pinned files edited). `sha256sum -c pins.sha256` run from `frozen/`: all OK. Previous pins file kept at `/tmp/pins.sha256.before-slack` |
| `tests/test_slack.py` | new, 9 tests | See section 4 |
| `values-slack30/` | new, 18 files | `<P>.json`, `<P>-srun.json`, `<P>-slowdown.json` and each `.sha256`, for EL2, SL2, HL2. Built with `PANEL_SLACK_S=30` from the same rows the old files used: `runs/s4-a1-<panel>-1..4`; SL2 slowdown also uses `runs/s4-sr-sl2-1,2`. EL2 and HL2 have no srun rows, so their slowdown file has `s: null` (as the old files did). `values/` is untouched. `sha256sum -c` on all nine: OK |

Note: `runs/s4-a1-sl2-1` is marked QUARANTINED in `runs/` (audit found `.claude/projects` path use). The existing `values/SL2.json` already includes it and so does the slack file, so the two files stay comparable. Whether to drop that row is a separate decision I did not take.

## 2. Launch commands (one panel, all three packages, slack 30)

```bash
R4=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r4-flag-and-adjudicate
export PANEL_SLACK_S=30 NOFALLBACK=1
# no --values: the launcher takes $R4/values-slack30/<P>.json (checked: sha256, panel, slack_s = 30)
# no --packages: all three packages, one after another. Row ids are single-use; change r01 for a repeat.

# ember + 2x luna (EL2)
PANEL_COLLAB=1 flock /tmp/collab-gateway.lock $R4/bin/run-panel.sh --panel EL2 --row f7s30-el2-r01 --block b01   # REFUSED, see section 5
PANEL_COLLAB=0 flock /tmp/collab-gateway.lock $R4/bin/run-panel.sh --panel EL2 --row a1s30-el2-r01 --block b01

# sonnet + 2x luna (SL2)
PANEL_COLLAB=1 flock /tmp/collab-gateway.lock $R4/bin/run-panel.sh --panel SL2 --row f7s30-sl2-r01 --block b01
PANEL_COLLAB=0 flock /tmp/collab-gateway.lock $R4/bin/run-panel.sh --panel SL2 --row a1s30-sl2-r01 --block b01

# haiku + 2x luna (HL2)
PANEL_COLLAB=1 flock /tmp/collab-gateway.lock $R4/bin/run-panel.sh --panel HL2 --row f7s30-hl2-r01 --block b01   # REFUSED, see section 5
PANEL_COLLAB=0 flock /tmp/collab-gateway.lock $R4/bin/run-panel.sh --panel HL2 --row a1s30-hl2-r01 --block b01
```

Arm summary under the same cap: `PANEL_SLACK_S=30 uv run --frozen --project <REPO> python $R4/lib/arm_summary.py --panel <P> --a1 <a1 results> --arm <f7 results> --out ...`. Without `PANEL_SLACK_S=30` the summary applies the old 1.35 B cap.

## 3. k per panel and package (messages a reviewer may act on)

B = median elapsed of the four A1 rows; turn and report are the 90th-percentile (p90) values the old files already held (unchanged by slack). k = max(0, min(2, floor((0.35 B + SLACK_S - 2 - turn - report) / (2 turn)))).

| Panel | Package | B (s) | turn p90 (s) | report p90 (s) | k old | **k new (slack 30)** | finish offset old -> new (s) | slowdown limit new |
|---|---|---|---|---|---|---|---|---|
| EL2 | design | 114.1 | 43.8 | 52.2 | 0 | **0** | 58.0 -> 88.0 | none (k = 0) |
| EL2 | designSpec | 102.5 | 48.8 | 71.3 | 0 | **0** | 18.3 -> 48.3 | none |
| EL2 | makeTheAlias | 131.8 | 35.4 | 49.2 | 0 | **0** | 93.3 -> 123.3 | none |
| SL2 | design | 259.0 | 15.4 | 22.1 | 1 | **2** | 312.1 -> 342.1 | 0.161 (old 0.164); measured s = -0.295, pass |
| SL2 | designSpec | 207.7 | 28.5 | 75.3 | 0 | **0** | 176.5 -> 206.5 | none |
| SL2 | makeTheAlias | 211.9 | 23.6 | 17.9 | 0 | **1** | 244.6 -> 274.6 | 0.149; measured s = +0.057, pass |
| HL2 | design | 218.9 | 47.6 | 82.3 | 0 | **0** | 165.6 -> 195.6 | none |
| HL2 | designSpec | 248.1 | 85.9 | 12.4 | 0 | **0** | 236.6 -> 266.6 | none |
| HL2 | makeTheAlias | 280.1 | 32.5 | 100.7 | 0 | **0** | 245.0 -> 275.0 | none |

Hang guard (1.5 B) is unchanged on every row. The slowdown for SL2 was measured with the two old srun rows, which ran with the old k (1 on design, 0 on the others); the slack limit is applied to that same measurement, so the SL2 slowdown at k = 2 on design and k = 1 on makeTheAlias is not measured at those k values.

## 4. Tests

Command, from the repository root: `uv run pytest .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r4-flag-and-adjudicate/tests`.

- **Full suite: 124 passed, 0 failed, 0 errors in 171 s** (log `/tmp/r4-slack-pytest.log`). The count is the 106 of `IMPLEMENTATION.md`, 9 time-cap-exception tests added by an earlier session, and 9 new slack tests. `ruff check lib tests`: all checks passed. `bash -n bin/run-panel.sh`: clean. `sha256sum -c frozen/pins.sha256` (from `frozen/`): all OK after the run.
- `tests/test_slack.py` (9 tests): default 0 leaves `k_of`, `finish_offset`, `slowdown_limit` unchanged (env unset and `PANEL_SLACK_S=0`); k goes 0 -> 1 for (B 116, turn 14, report 14) and 1 -> 2 for the measured SL2 design package; integer-ms thresholds (k 0 at turn 20 and 23, 2 at turn 10); finish offset 143.8 -> 173.8 and the hang guard stays 174.0; slowdown limit gains 30 / B; a bad `PANEL_SLACK_S` exits; the `planning` CLI writes `values-slack30/planning-EL2.json` with `slack_s: 30` and does not create `values/`; `arm_summary` reads the slack; launcher refusals (slack values missing, old file under slack, slack file without slack, default slack path picked up then refused on k = 0, bad number).
- Real-file check of the launcher (no model started): EL2 and HL2 with `PANEL_COLLAB=1` and slack 30 were refused with `F7 not runnable ... k = 0 on every package`; `values/EL2.json` under `PANEL_SLACK_S=30` was refused for slack mismatch. These three refusals are lines in `runs/refusals.jsonl` (rows `slackcheck-*`); no run directory was created.

## 5. What still refuses to run, and why

- **EL2 `PANEL_COLLAB=1` and HL2 `PANEL_COLLAB=1` with slack 30: refused (exit 2).** k is still 0 on all three packages of both panels. The measured turn times (EL2 35-49 s, HL2 32-86 s) are larger than what 30 s of slack buys: for example EL2 design gives `0.35 x 114.1 + 30 - 2 - 43.8 - 52.2 = -28 s`, which is below the 0 needed for even one message. Only the `PANEL_COLLAB=0` rows run for those two panels.
- **Existing route, owner-authorised separately, not used here:** `TIME_CAP_EXCEPTION=1` forces k = 1 on a k = 0 package and widens the hang guard to at least 3 x B. It accepts the slack files (kind `measured`); `values.py tce` on EL2 design with slack 30 prints `k 1, finish offset 259.22 s, hang 342.4 s`. Rows run that way are stamped as exceptions and are not comparable with cap-obeying rows. I did not run it.
- **SL2 `PANEL_COLLAB=1` runs**, but only design (k = 2) and makeTheAlias (k = 1) use cards; designSpec has k = 0 and runs isolated (`k0_isolated`) inside the same row, as the design specifies.
- The earlier gate (luna act rate 0 of 5 on the unannounced probe, `IMPLEMENTATION.md` section 5) is unchanged by this decision.
- Slack values must be given as a plain number (`30`, not `30.0`) if the default path is used, because the directory name is `values-slack30`.
