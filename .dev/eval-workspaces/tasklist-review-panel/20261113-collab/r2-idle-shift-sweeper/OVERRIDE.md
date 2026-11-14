# OVERRIDE: owner-authorised time-cap exception (R2, Idle-Shift Sweeper)

Owner decision 2026-11-14: the +35% elapsed-time rule may be exceeded so the collaboration arm runs. The switch is
`TIME_CAP_EXCEPTION=1` (default unset or 0 = off). Everything below is inside this folder; `src/`, `tests/`, `.claude/`,
`.dev/tasks/`, `20261111-a1/` and the other designs were not touched, and nothing was staged or committed.

## 0. Read this first

- **The premise does not match the Spike 4 values on disk.** `config/values/` (pinned, Spike 4, n = 4 runs per panel) has measured **k = 0 only for EL2** (all three packages). SL2 and HL2 are already **k = 2** on all three packages, so for them the override changes no value (see section 2). It still stamps their rows, so they are kept apart from cap-obeying rows. If you expected k = 0 on SL2 and HL2, the Spike 4 files say otherwise.
- **The smoke row ran the collaboration path on real models but delivered nothing.** The sweeper started (k = 1), posted 2 facts, and both facts reached the board after each luna's last tool call (late). AC-4 therefore FAILED (section 4). Widening the timers does not fix this: the lunas end by themselves at about 80 s, the EL2 sweeper only starts when ember's review ends (about 59 s) and needs about 25 s to post. Decision for the owner in section 6.

## 1. What changed

| File | Lines | Change |
|---|---|---|
| `py/values.py` | 58-88 | `EXC_HANG_X = 3.0`; `time_cap_exception()` (reads `TIME_CAP_EXCEPTION`, only unset, 0 or 1 accepted); `exception_values(v)` computes the exception variant of one measured values file. `compute()`, `finish_at`, `k`, `hang` are unchanged (a test pins that the switch does not alter `compute()`). |
| `py/values.py` | 220-222, 246-252 | New `values.py exception --src config/values --dst config/values-exception` command. |
| `bin/launch-panel.sh` | 28-38, 57, 76, 83-85 | `TIME_CAP_EXCEPTION=1`: uses `config/values-exception/` and `config/manifest-exception.json` (exported as `R2_MANIFEST` to every child, as the slack variant does). Exit 2 if the value is not 0/1, if combined with `PANEL_SLACK_S=30` or `--planning-values`, if the manifest copy or a values file is missing, or if a sha256 differs. Writes `runs/<row>/time_cap_exception`; a resume with a different value is refused. |
| `py/collab_metrics.py` | 265-284 | `collab.json` gains `time_cap_exception`, `time_cap_exception_applied`, `B_A1`, `k_measured`, `elapsed_over_baseline`, `messages_delivered` (per reviewer). `slo_breach` uses the widened `hang_s` only for a package where the exception was applied; every other package keeps `elapsed > 1.5 x B`. |
| `py/results_row.py` | 52, 96-104, 164 | Row-level `time_cap_exception` (true when the run dir carries the stamp) and per package `time_cap_exception`, `time_cap_exception_applied`, `B_A1`, `elapsed_s` (existing), `elapsed_over_baseline`, `k` (existing, the forced k), `k_measured`, `messages_delivered`. A stamped row whose package values carry no stamp is listed in `invalid`. |
| `py/summarize_arm.py` | 42-48, 88-93, 111-115 | Refuses (exit 2) to mix rows with `time_cap_exception` true and rows without, among `--rows` and `--baseline-rows` together. For exception rows the `1.35 B_c + slack` elapsed test is waived (only a row's own `slo_breach` counts) and the summary carries `time_cap_exception_columns` (row, package, applied, B_A1, elapsed_s, elapsed_over_baseline, k_measured, k, messages_delivered). |
| `config/values-exception/<panel>/<pkg>.json` | 9 files | New. `values.py exception` applied to the 9 pinned Spike 4 files. |
| `config/manifest-exception.json` | new | `values.py pin --values-dir values-exception`: same base SHAs and the same judge, catalogue and brief pins as `manifest.json` (a test checks equality), plus 9 pins for the exception values. |
| `spikes/s3-exception-smoke.sh`, `spikes/s3_exception_check.py` | new | The one-package smoke row with the override on, and its checks (AC-2, 2b, 4, 5, 6, 9, 10 of DESIGN 6.5, plus OV-1 to OV-3 for the override). |
| `tests/test_time_cap_exception.py` | new | 36 tests (section 3). |

Not changed: `config/values/`, `config/manifest.json`, `config/values-slack30/`, `config/planning-values.json`, every identity check (observed model must equal requested, `NOFALLBACK=1`, allowed models), the audits, the anonymiser, the blind judge call.

## 2. The numbers (exact, from `config/values-exception/`)

Rule, per package, when the measured k is 0 (the override applies): `k = 1`; `hang_s = max(existing, round(3.0 x B_A1, 3))`; `panel_finish_at_s = max(existing, round(hang_s - turn_p90_crit - T_report_p90_crit, 3))` (the design's own "cap minus turn minus report" relation, with the cap now equal to the widened hang guard); `sweeper_kill_s = max(existing, round(panel_finish_at_s - 2 x turn_p90_recv, 3))`. The script refuses to write a file if the widened finish still does not fit one message by the design's D-2 rule. When the measured k is above 0 nothing changes. `B_A1` is `B_f` of the Spike 4 values file (median elapsed of 4 isolated runs). All times in seconds from T0.

| Panel | Package | B_A1 | Measured k | Forced k | Applied | Hang old -> new | Finish old -> new | Sweeper kill old -> new |
|---|---|---|---|---|---|---|---|---|
| EL2 | design | 102.8185 | 0 | **1** | yes | 154.228 -> **308.456** | 110.723 -> **280.374** | 85.685 -> **255.336** |
| EL2 | designSpec | 131.7125 | 0 | **1** | yes | 197.569 -> **395.138** | 153.703 -> **371.029** | 123.791 -> **341.117** |
| EL2 | alias | 99.447 | 0 | **1** | yes | 149.171 -> **298.341** | 101.491 -> **265.579** | 73.841 -> **237.929** |
| HL2 | design | 181.7905 | 2 | 2 | no | 272.686 (same) | 166.112 (same) | 136.468 (same) |
| HL2 | designSpec | 230.6925 | 2 | 2 | no | 346.039 (same) | 220.971 (same) | 193.391 (same) |
| HL2 | alias | 280.3925 | 2 | 2 | no | 420.589 (same) | 321.432 (same) | 290.954 (same) |
| SL2 | design | 294.588 | 2 | 2 | no | 441.882 (same) | 346.119 (same) | 320.933 (same) |
| SL2 | designSpec | 224.009 | 2 | 2 | no | 336.014 (same) | 256.761 (same) | 225.667 (same) |
| SL2 | alias | 254.5455 | 2 | 2 | no | 381.818 (same) | 293.934 (same) | 264.192 (same) |

Consequence on EL2: the finish signal fires 28 to 34 s before the widened hang guard, i.e. at 265 to 371 s, which no reviewer will reach (the lunas end by themselves at roughly 80 to 130 s). In practice only the sweeper's kill time and the hang guard still bound the run. With the switch off the values are the old ones (a test and the 9 frozen files check this).

### Stamps and recorded columns

Every row run with `TIME_CAP_EXCEPTION=1` has `time_cap_exception: true` at the top of `results/<row>.json` and on every package; per package: `B_A1`, `elapsed_s`, `elapsed_over_baseline` (elapsed / B_A1), `k` (the forced k), `k_measured`, `time_cap_exception_applied`, `messages_delivered` (`{reviewer id: messages delivered}`; the facts delivered per luna also stay in `facts_delivered`). `collab.json` carries the same. `summarize_arm.py` prints these as `time_cap_exception_columns` and exits 2 on mixed rows.

### Re-pinning (the design's procedure, as used for the slack variant)

```bash
R2=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper
uv run --no-project python -I $R2/py/values.py exception --src $R2/config/values --dst $R2/config/values-exception
uv run --no-project python -I $R2/py/values.py pin --r2 $R2 --repo . --eval .dev/eval-workspaces/tasklist-review-panel/20261111-a1 \
  --out $R2/config/manifest-exception.json --values-dir values-exception
```

Both were run; the launcher preflight (sha256 of `judge-one.sh`, catalogue, both briefs, the three values files) passed in the smoke row. The non-value pins of `manifest-exception.json` equal those of `manifest.json`. If any `config/values/` file is re-measured, rerun both commands.

## 3. Tests

`uv run pytest $R2/tests -q -p no:cacheprovider -rs` from the repository root (command of `IMPLEMENTATION.md` section 3): **448 passed, 0 failed, 0 skipped in 148 s** (before: 412). The 36 new tests in `tests/test_time_cap_exception.py`:

| Group | Tests | Covers |
|---|---|---|
| switch | 6 | unset, empty, 0 = off; 1 = on (one test); `2`, `-1`, `abc`, `true`, `1.0` refused (five) |
| values, off and on | 5 | `compute()` unchanged when the switch is set; k forced to 1 with hang = 3.0 B, finish = hang - turn - report, kill = finish - 2 turn (EL2 control package: 308.456, 280.374, 255.336); measured k above 0 left alone; an existing guard is never narrowed; refusal when one message cannot fit |
| frozen files | 10 | 9 files equal `exception_values` of the pinned ones, sha256 equals `manifest-exception.json`; non-value pins equal `manifest.json` |
| `collab.json` | 4 | off: not stamped, old 1.5 B rule; on: all columns, widened hang guard (160 s inside 300 s) and a breach above it (310 s) still flagged; stamped but not applied keeps the cap rule |
| summariser | 4 | mixed rows refused in all three directions and exit 2 from the command line; columns reported and elapsed cap waived; off unchanged |
| launcher and end to end | 7 | bad value, missing manifest copy, combined with slack or planning, missing values, sha mismatch, other checks still in force (`NOFALLBACK`, allowed models, judge sha); a full launch with the fake `claude` with the switch on (k 1, baked hook `--k 1`, finish offset, sweeper ran, row and package columns, resume with the switch changed refused) and off (not stamped, k 0, sweeper skipped) |

`ruff check --select E,F,I,W --ignore E501` on `py/`, `tests/` and the two new spike files: clean. `bash -n` passes on `bin/launch-panel.sh` and `spikes/s3-exception-smoke.sh`.

## 4. Smoke result (ONE real row, override on)

Command (run once; not re-run): `flock /tmp/collab-gateway.lock bash $R2/spikes/s3-exception-smoke.sh EL2 smoke-el2-exc-collab`, which runs `NOFALLBACK=1 PANEL_COLLAB=1 TIME_CAP_EXCEPTION=1 bash bin/launch-panel.sh --panel EL2 --row smoke-el2-exc-collab --packages TASK-WF-design-20261108-041415` (frozen exception values, no planning values, judged). Evidence: `runs/smoke-el2-exc-collab/`, `results/smoke-el2-exc-collab.json`, `spikes/out/s3-exception/check-smoke-el2-exc-collab.json`; one `S3-EXC FAIL` line was appended to `spikes/RESULTS.md`.

| Check | Result |
|---|---|
| Launch exit | 0 (all 7 steps OK, `invalid: []`) |
| AC-2 nothing under `src/` or `20261111-a1/` changed | PASS |
| AC-2b `dropped_lines` 0, no re-ask problems | PASS |
| **AC-4 at least one receiver has a delivery** | **FAIL**: delivered t4-1 0, t3-1 0 (every other AC-4 part held: schema valid, 2 facts posted, delivered <= k, `stop_blocks` 0) |
| AC-5 3 reviewers in merge, anonymised, `score.json` under `scoring/`, nothing new under `EVAL/arms`, all row fields | PASS |
| AC-6 `audit.json` ok (ground-truth audit included) | PASS |
| AC-9 observed model equals requested for all 4 sessions (ember, luna, luna, ember sweeper), no fallback file | PASS |
| AC-10 elapsed within hang guard | PASS (86.4 s against 308.456 s) |
| OV-1 stamps and forced k | PASS (row and package `time_cap_exception: true`, `time_cap_exception_applied: true`, k 1, k_measured 0) |
| OV-2 columns present | PASS: B_A1 102.8185, elapsed_s 86.407, elapsed/B_A1 0.8404, k 1, k_measured 0, messages_delivered `{t2b-1: 0, t4-1: 0, t3-1: 0}` |
| OV-3 sweeper ran instead of being skipped at k = 0 | PASS (started about 59 s after T0, ended about 86 s, `model_ok`) |

What happened: ember's review ended at 58.8 s; the sweeper started then and posted `f-0` at 83.0 s and `f-1` at 84.6 s (two earlier attempts of `f-0` were rejected by the validator; reasons in `board/msgs/rejected.jsonl`). t3-1 had finished at 79.6 s and t4-1 at 83.9 s. Both facts were counted `late` (after the receiver's last tool call), both lunas are in `isolated_for`. Other numbers: `cmd_unrun` 2 of 2 (the known issue of `IMPLEMENTATION.md` 5.2), control package found 0 / wrong blockers 1, 28,801 output tokens, 3 reviewer sessions at most at any time (ember plus 2 lunas, then sweeper plus 2 lunas). The elapsed time was below B_A1, so this row did not use any extra time; the cap exception was available but not needed for time, the failure is delivery timing.

## 5. Launch commands

Run from the repository root. Each command runs the three packages (designSpec, alias, design), merges, anonymises, judges with the unchanged `judge-one.sh` (Opus, `claude-opus-5-5`, blind judge only) and writes `$R2/results/<row>.json`. A re-run with the same `--row` resumes. Row names carry `exc` so they never resume or mix with older rows.

```bash
R2=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r2-idle-shift-sweeper
L="flock /tmp/collab-gateway.lock env NOFALLBACK=1 TIME_CAP_EXCEPTION=1"

# ember + 2x luna (EL2): collaboration arm, then the isolated baseline with the same harness
$L PANEL_COLLAB=1 bash $R2/bin/launch-panel.sh --panel EL2 --row f4-el2-exc-r1
$L PANEL_COLLAB=0 bash $R2/bin/launch-panel.sh --panel EL2 --row a1-el2-exc-r1

# sonnet + 2x luna (SL2)
$L PANEL_COLLAB=1 bash $R2/bin/launch-panel.sh --panel SL2 --row f4-sl2-exc-r1
$L PANEL_COLLAB=0 bash $R2/bin/launch-panel.sh --panel SL2 --row a1-sl2-exc-r1

# haiku + 2x luna (HL2)
$L PANEL_COLLAB=1 bash $R2/bin/launch-panel.sh --panel HL2 --row f4-hl2-exc-r1
$L PANEL_COLLAB=0 bash $R2/bin/launch-panel.sh --panel HL2 --row a1-hl2-exc-r1

# arm summary (rows and baseline rows must all be exception rows, else exit 2)
uv run --no-project python -I $R2/py/summarize_arm.py --rows $R2/results/f4-el2-exc-*.json \
  --baseline-rows $R2/results/a1-el2-exc-*.json --out $R2/results/arm-f4-el2-exc.json
```

Notes:
- The isolated baseline rows carry the same stamp on purpose, so the summariser accepts them next to the collaboration rows; with `PANEL_COLLAB=0` the sweeper does not run and k is unused, so only the hang guard (EL2) differs from a plain baseline row.
- `--no-judge` stops before judging. `SWEEPER_MODEL` is still limited to the allowed models. `TIME_CAP_EXCEPTION=1` with `PANEL_SLACK_S=30` or `--planning-values` exits 2.
- SL2 and HL2 collaboration rows start 4 sessions at once (3 reviewers plus the ember sweeper at T0, DESIGN decision D-1); this is open item U-2 of `IMPLEMENTATION.md` section 5.1 and is unchanged. EL2 never exceeds 3.
- Because EL2 has k = 1 and the sweeper waits for ember, expect many EL2 facts to arrive late (see section 6). Delivered counts per luna are in `messages_delivered` and `facts_delivered`.

## 6. Decision for the owner

The override makes the EL2 collaboration arm run, but the smoke row shows the arm can still deliver zero messages. Recommended: start the EL2 sweeper at T0 instead of after ember (set `"sweeper": {"start": "t0"}` for EL2 in `config/panels.json`, which is not sha-pinned), as SL2 and HL2 already do. That gives the sweeper about 59 s more lead, at the price of 4 sessions at once on EL2 (the cap of 3 holds only if the sweeper does not count as a reviewer session, the same question as U-2). I did not make this change: it alters the design's session plan, not just its timers. Reply "start EL2 sweeper at T0" to have it done and re-smoked, or run the commands above as they are.
