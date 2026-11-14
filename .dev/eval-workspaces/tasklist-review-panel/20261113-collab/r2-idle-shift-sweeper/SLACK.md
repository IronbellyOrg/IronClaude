# SLACK: time cap 1.35 x B + 30 s (R2, Idle-Shift Sweeper)

Owner decision 2026-11-14: the cap becomes `1.35 x B + SLACK_S`, `SLACK_S = 30`. Read from the environment variable
`PANEL_SLACK_S` (default 0, which reproduces every existing pinned value and test). No model session was run for this change;
the new values were recomputed from the four Spike 4 runs per panel already on disk (`runs/spike4-<panel>-r1..r4`).

## 1. What changed (all under this folder)

| File | Change |
|---|---|
| `py/values.py:23-33` | New `slack_s()`: reads `PANEL_SLACK_S` at call time (unset or empty = 0); refuses non-numbers, negatives, nan, inf. |
| `py/values.py:36-37` | `finish_at` = `1.35 B + SLACK_S - turn_crit - report_crit`. `k` and `sweeper_kill` follow from it. |
| `py/values.py:46-47` | `k_r42` (literal R-42 form) = `floor((0.35 B + SLACK_S - hooks - turn - report) / (2 turn))`. |
| `py/values.py:68-69` | `compute` writes `"slack_s": 30` into a values file only when the slack is non-zero, so slack-0 files stay byte-identical. |
| `py/values.py` `pin` / `--values-dir` | `pin` takes `--values-dir` (default `values`) and names pins `<values-dir>/<panel>/<pkg>.json`. |
| `py/summarize_arm.py:72-82` | SLO check is `elapsed > 1.35 B_c + SLACK_S` (loads `values.py` by path because the script runs under `python -I`). Run it with the same `PANEL_SLACK_S` the rows used. |
| `bin/launch-panel.sh:18-26, 45-47, 64, 71, 82` | `PANEL_SLACK_S` unset/0: as before. `30`: uses `config/values-slack30/` and `config/manifest-slack30.json` (exported to every child as `R2_MANIFEST`, so build-sandbox and judge check the copy). Exit 2 if the slack manifest copy or a slack values file is missing, if its sha256 differs, if `--planning-values` is combined with 30, or if the value is anything other than 0 or 30. `slack_s` is stored in the run dir and a resume with a different value is refused. |
| `config/values-slack30/<panel>/<pkg>.json` (9 files) | New. `values.py reduce` on the Spike 4 run dirs with `PANEL_SLACK_S=30`. |
| `config/manifest-slack30.json` | New. `values.py pin --values-dir values-slack30`: same base SHAs, judge/catalogue/brief pins as `manifest.json` (checked equal), plus the 9 slack values pins. |
| `tests/conftest.py` | `PANEL_SLACK_S` removed from the test environment by default. |
| `tests/test_values.py`, `test_summarize_arm.py`, `test_preflight.py` | 54 new tests; 2 older preflight tests fixed (below). |

Not changed on purpose: the hang guard `1.5 x B` (`hang_s`, and `elapsed > 1.5 * B_f` in `py/collab_metrics.py:275`), which is not derived from the 35% cap. `config/values/`, `config/manifest.json`, `config/planning-values.json` are untouched.
Control: `values.py reduce` with `PANEL_SLACK_S=0` reproduced all 9 pinned values files byte for byte before the slack files were written.

## 2. Launch commands (PANEL_SLACK_S=30)

Run from the repository root. Rows use a new `-s30-` name so they never resume an older row. `PANEL_COLLAB=1` is the collaboration arm, `PANEL_COLLAB=0` the isolated baseline.

```bash
R2=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper
L="flock /tmp/collab-gateway.lock env NOFALLBACK=1 PANEL_SLACK_S=30"

# ember + 2x luna (EL2)
$L PANEL_COLLAB=1 bash $R2/bin/launch-panel.sh --panel EL2 --row f4-el2-s30-r1
$L PANEL_COLLAB=0 bash $R2/bin/launch-panel.sh --panel EL2 --row a1-el2-s30-r1
# sonnet + 2x luna (SL2)
$L PANEL_COLLAB=1 bash $R2/bin/launch-panel.sh --panel SL2 --row f4-sl2-s30-r1
$L PANEL_COLLAB=0 bash $R2/bin/launch-panel.sh --panel SL2 --row a1-sl2-s30-r1
# haiku + 2x luna (HL2)
$L PANEL_COLLAB=1 bash $R2/bin/launch-panel.sh --panel HL2 --row f4-hl2-s30-r1
$L PANEL_COLLAB=0 bash $R2/bin/launch-panel.sh --panel HL2 --row a1-hl2-s30-r1

# arm summary, same slack:
PANEL_SLACK_S=30 uv run --no-project python -I $R2/py/summarize_arm.py --rows $R2/results/f4-el2-s30-*.json --baseline-rows $R2/results/a1-el2-s30-*.json --out $R2/results/arm-f4-el2-s30.json
```

Each launch runs the three packages (designSpec, alias, design), merges, anonymises, judges with the unchanged `judge-one.sh` (Opus, blind judge only) and writes `$R2/results/<row>.json`. `--no-judge` stops before judging.
With `PANEL_COLLAB=0` the sweeper does not run and `k` is not used, so the baseline rows are the same as before apart from the row name and the stored `values_sha256`.

## 3. New k per panel and package (old = `config/values/`, new = `config/values-slack30/`)

`B` is the Spike 4 median elapsed time. Finish offset = `panel_finish_at_s`; kill = sweeper kill time (seconds from T0). `hang_s` is unchanged.

| Panel | Package | B (s) | k old | k new | Finish old -> new (s) | Sweeper kill old -> new (s) | Hang (s) |
|---|---|---|---|---|---|---|---|
| EL2 | design | 102.8 | 0 | **1** | 110.7 -> 140.7 | 85.7 -> 115.7 | 154.2 |
| EL2 | designSpec | 131.7 | 0 | **1** | 153.7 -> 183.7 | 123.8 -> 153.8 | 197.6 |
| EL2 | alias | 99.4 | 0 | **1** | 101.5 -> 131.5 | 73.8 -> 103.8 | 149.2 |
| SL2 | design | 294.6 | 2 | 2 | 346.1 -> 376.1 | 320.9 -> 350.9 | 441.9 |
| SL2 | designSpec | 224.0 | 2 | 2 | 256.8 -> 286.8 | 225.7 -> 255.7 | 336.0 |
| SL2 | alias | 254.5 | 2 | 2 | 293.9 -> 323.9 | 264.2 -> 294.2 | 381.8 |
| HL2 | design | 181.8 | 2 | 2 | 166.1 -> 196.1 | 136.5 -> 166.5 | 272.7 |
| HL2 | designSpec | 230.7 | 2 | 2 | 221.0 -> 251.0 | 193.4 -> 223.4 | 346.0 |
| HL2 | alias | 280.4 | 2 | 2 | 321.4 -> 351.4 | 291.0 -> 321.0 | 420.6 |

Correction to the premise: in the Spike 4 values on disk only EL2 had k = 0 (all three packages); SL2 and HL2 were already at the maximum 2. Slack lifts EL2 to 1, not 2: `floor((140.7 - 102.8 - 2) / (2 x 12.5)) = 1` for the design package, because the receiver turn p90 is 12.5 to 15.0 s. k = 2 on the EL2 design package would need a finish offset of 154.9 s, i.e. a slack of about 44 s instead of 30. `E_recv` equals `B_f` on EL2 because the critical role is also a receiver there.

## 4. Test results

`uv run pytest $R2/tests -q -p no:cacheprovider -rs` (no model call; `tests/fakes/claude` stands in): **412 passed, 0 failed, 0 skipped in 141 s** (the previous report: 358 passed). The 54 new tests:

| File | New | Covers |
|---|---|---|
| `test_values.py` | 47 | default 0 unchanged (no `slack_s` key, EL2 k 0, finish 110.723); k 0 -> 1 for the measured EL2 case; finish +30, kill +30, hang unchanged; D-2 equals R-42 under slack (30 cases); bad values refused (4); all 9 frozen slack files = pinned file + 30 and sha256 equal to `manifest-slack30.json` (9) |
| `test_summarize_arm.py` | 2 | SLO cap 135 s -> 165 s with slack 30 (150 s passes, 170 s breaches); bad `PANEL_SLACK_S` exits 2 |
| `test_preflight.py` | 5 | value other than 0/30 refused; 30 without manifest copy; 30 with slack values missing (exit 2, message names `values-slack30` and `PANEL_SLACK_S=30`); sha mismatch; 30 with `--planning-values` |

Two existing tests in `test_preflight.py` were already failing before this change, because they assumed `config/values/` does not exist and Spike 4 created it on 2026-11-14 (`test_refuses_values_sha_mismatch`: `mkdir` on an existing dir; `test_refuses_missing_values_without_planning`: found the real values and failed on the sha instead). I changed the tests only (`exist_ok=True`; a harness copy without `config/values`).
`ruff check` with the project rule set (E, F, I, W): passes. With all rules: 19 pep8-naming findings (was 18; the new one is the single-letter `B` test parameter, same kind as the others, and `pyproject.toml` excludes `.dev/`). `bash -n bin/launch-panel.sh` passes.
No end-to-end launch was run, so the launcher change is tested up to preflight (and by the unit tests of the shared code), not through a package run.

## 5. What still refuses to run, and why

- **`PANEL_SLACK_S` other than unset, 0 or 30**: launcher exits 2. Only 0 and 30 have frozen, pinned values.
- **`PANEL_SLACK_S=30 --planning-values`**: exit 2. The planning values are a fixed file computed without slack; there is no slack variant.
- **`summarize_arm.py`**: refuses planning rows (unchanged), and exits 2 on a bad `PANEL_SLACK_S`. It does not know which slack the rows were launched with (the results row does not store it), so a slack-30 arm must be summarised with `PANEL_SLACK_S=30` set; with 0 its SLO check would count slow rows as breaches.
- **Open items from `IMPLEMENTATION.md` section 5.1 that this change does not touch**: U-2 (SL2 and HL2 collaboration rows start 4 sessions at once, above a cap of 3 if the ember helper counts), U-7 (AC-6 passes only under the narrowed audit), U-8 (`/tmp/panel-probe`, `/tmp/collab-gateway.lock`). The `flock /tmp/collab-gateway.lock` in the commands above is part of the existing launch recipe.
- **Ember as a receiver does not act on injected text** (REQ-S3: 0 of 4, 0 of 5). It is the sweeper or critical role on EL2, so a delivered k of 1 matters only for the two luna receivers.
- `config/manifest.json` and `spikes/RESULTS.md` show as modified in git from the Spike 4 runs before this change; this change did not edit them.
