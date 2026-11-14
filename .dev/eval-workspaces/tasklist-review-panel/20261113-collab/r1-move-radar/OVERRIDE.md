# Redesign 1, Move Radar: owner-authorised time-cap exception (OVERRIDE.md)

Owner decision 2026-11-14: the +35% elapsed-time rule may be exceeded so that the collaboration arm runs on el2, hl2 and sl2.
Written 2026-11-14 12:35 UTC from the files, the test run and the smoke row on disk. `REPO` = `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel`,
`R1` = `REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar`, `DS` / `AL` / `DE` = the designSpec / makeTheAliasOnly / design packages.

## 1. The switch

`TIME_CAP_EXCEPTION` (environment variable, read once by `tools/launch.sh`). Unset or `0` = off: every value, file and row id is exactly as before. `1` = on.
Anything else (including empty) is refused, exit 2. `1` with `PANEL_COLLAB=0` is refused, exit 2 (the baseline keeps its own timers).
An override row has the id `<panel>-c1x-r<rep>` (for example `el2-c1x-r1`), so it can never share a results file, a run folder or a results line with a row that obeyed the cap
(`el2-c1-r<rep>`). It passes the same gates as any collab-1 row (G-BASE, G-PINS, S0, S2; S3 for `rep` of 1 or more) and needs the same `values/<panel>/<pkg>.json` + `.sha256`.

## 2. The rule and the exact numbers (`tools/values.py: cap_exception`)

Per package, applied to the Spike 4 values file as it stands (the values file is never rewritten; its sha256 is checked before and after the smoke row):

- every role whose measured k is 0 gets k = 1; a role with a measured k of 1 or 2 keeps it (sl2 and hl2 designSpec/alias/design readers with k 2 stay at 2);
- hang guard = max(existing hang guard, 3.0 x B_A1), where B_A1 = `B_f` in the values file; the existing hang guard is 1.5 x B_A1, so in every cell the new one is 3.0 x B_A1;
- finish offset (PANEL_FINISH_AT) = old finish offset + (new hang guard - old hang guard), which keeps the gap between the finish signal and the hang guard that the design had;
- injection guard = the new finish offset. Reason: the original guard was `min(1.35 B - G, finish)` with G = 47 s (el2) or 47 x turn_p90 / 6.4 (sl2, hl2), a headroom derived from the waived cap; with the measured turn times it is **negative on hl2 (all three packages) and on sl2 designSpec** (table below), so without this line the hook would skip every injection there even with k forced to 1. After the change the finish signal is the last point for an injection, as the design's step 5 already says;
- if no role has a measured k of 0, nothing changes for that package (it obeyed the cap).

The kill timer of `run-reviewer.sh` (`timeout --kill-after=5 <HANG_MS - now>`) and the hang test read `HANG_MS` from `run.json`, so they follow the widened guard with no edit. The hook, the classifier, the catalogue and the brief are not touched.

All nine cells (seconds from T0; "old" = the Spike 4 values file, "new" = with `TIME_CAP_EXCEPTION=1`; k shown as searcher/reader; computed by `cap_exception` over the nine files):

| Panel | Pkg | B_A1 | k measured | k used | hang old | hang new | finish old | finish new | guard old | guard new |
|---|---|---|---|---|---|---|---|---|---|---|
| el2 | DS | 83.8 | 0/0 | 1/1 | 125.7 | 251.4 | 53.8 | 179.5 | 53.8 | 179.5 |
| el2 | AL | 145.1 | 0/0 | 1/1 | 217.6 | 435.2 | 103.2 | 320.8 | 103.2 | 320.8 |
| el2 | DE | 97.0 | 0/0 | 1/1 | 145.5 | 290.9 | 40.2 | 185.6 | 40.2 | 185.6 |
| sl2 | DS | 165.8 | 0/0 | 1/1 | 248.7 | 497.5 | 138.3 | 387.0 | -22.0 | 387.0 |
| sl2 | AL | 302.3 | 0/2 | 1/2 | 453.4 | 906.9 | 319.0 | 772.4 | 183.6 | 772.4 |
| sl2 | DE | 197.6 | 0/1 | 1/1 | 296.5 | 592.9 | 169.6 | 466.1 | 101.2 | 466.1 |
| hl2 | DS | 231.1 | 0/0 | 1/1 | 346.7 | 693.3 | 110.6 | 457.3 | -402.8 | 457.3 |
| hl2 | AL | 342.1 | 0/2 | 1/2 | 513.2 | 1026.4 | 255.1 | 768.3 | -201.9 | 768.3 |
| hl2 | DE | 203.7 | 0/0 | 1/1 | 305.6 | 611.2 | 49.1 | 354.7 | -67.9 | 354.7 |

(Exact values to the millisecond are in each row's `runs/<row>/<pkg>/run.json` under `cap_exception`: `hang_offset_s_orig`, `finish_offset_s_orig`, `guard_offset_s_orig`.)
Unchanged when the override is off: `k_for`, `finish_offset`, `guard_offset`, `compute`, the values files, every `run.json` key, every `collab.json` key, every results key. Asked for on or off, `values.py deadlines` returns the same numbers it did before when the flag is absent (test `test_deadlines_off_is_exactly_the_old_output_and_on_is_the_rule`).

## 3. Stamps and columns (only on override rows)

| Where | What is added |
|---|---|
| `runs/<row>/run.json` | `time_cap_exception: true` |
| `runs/<row>/<pkg>/run.json` | `time_cap_exception: true`, `cap_exception` {`forced_k`, `k_measured`, `forced_roles`, `hang_offset_s_orig`, `finish_offset_s_orig`, `guard_offset_s_orig`} (and the widened `k`, `HANG_MS`, `FINISH_MS`, `GUARD_MS`) |
| `runs/<row>/<pkg>/collab.json` | `time_cap_exception: true`, `B_A1` (baseline from the values file), `elapsed_s` (existing), `elapsed_over_baseline`, `forced_k`, `k_measured`, `forced_roles`, `cap_exception`, `delivered` = messages delivered per reviewer id (every inject event, including the source.md check) |
| `results/<row>.json` and the `results.jsonl` line | row: `time_cap_exception: true`, `forced_k: 1`; per package: `B_A1`, `elapsed_s`, `elapsed_over_baseline`, `forced_k`, `k_measured`, `forced_roles`, `delivered`, `hang_offset_s` (the widened guard that package ran with) |
| `launch.log` | a `CAP_EXCEPTION` line per row and per package |

`tools/alarms.py <panel>` (the summariser over `results.jsonl`) leaves every override row out of convergence, snapshot, SLO budget, baseline drift and same-gaps, and reports them in their own section `time_cap_exception.rows` with those columns per package (smoke rows of rep 0 included there, although the arm-level checks ignore rep 0). Rows that obeyed the cap are summarised exactly as before (test `test_alarms_keep_exception_rows_apart` asserts the other keys are identical with and without exception rows).
Not built: a comparison of override rows against the collab-0 rows. Read it off the columns (`elapsed_over_baseline`) and the collab-0 rows `el2-c0-r1..3`, `sl2-c0-r1..3`, `hl2-c0-r1..3`.

## 4. What changed (files and lines, all under `R1/`)

| File | Lines | Change |
|---|---|---|
| `tools/values.py` | 7-11 (usage), 74-93 (`CAP_EXC_HANG_X`, `cap_exception`), 232-253 (`deadlines`: `cap_exc` parameter, collab-1-only refusal, extra output keys only when on), 266-267 (`--cap-exception 1` in `main`) | the rule of section 2 |
| `tools/launch.sh` | 38-43 (read and validate `TIME_CAP_EXCEPTION`, `CAPARG`), 72 (row id `c1x`), 77-79 (row-level stamp and log line), 102-104 (pass `--cap-exception 1`, per-package log line), 115 (`run.json` stamp and `cap_exception`) | switch, row id, stamps |
| `tools/collab_summary.py` | 330-336 | the `collab.json` columns, only when `run.json` carries the stamp |
| `tools/results.py` | 55-57 (per-package columns), 66-69 (row id regex accepts `c1x`; `c0x` is rejected), 124 (row stamp) | results columns and stamp |
| `tools/alarms.py` | 13-15 (doc), 45-56 (`CX_PKG_COLS`, `cap_exception_rows`, exception rows filtered out), 102-103 (new report section) | summariser |
| `spikes/smoke/smokecheck.sh` | 5 | package taken from `SMOKE_PKG` (default unchanged, designSpec) |
| `spikes/smoke/override-check.sh` | new, 53 lines | the seven 6.4 conditions for a package other than designSpec plus override conditions O1-O6 (stamps; forced k exactly where measured k is 0 and the values file untouched; hang = max(old, 3.0 B_A1) and finish/guard moved with it; columns and ratio; delivered = inject events and at most k; model identity and no `fallback.log`) |
| `tests/test_cap_exception.py` | new, 250 lines, 15 test functions (19 cases) | section 6 |

Not changed: `radar-hook.sh`, `radar-classify.jq`, `msg-validate.sh`, `run-reviewer.sh`, `sandbox.sh`, `anon.sh`, `config/*`, `manifest.json`, `values/*`, the judge, `NOFALLBACK` handling (still exported as 1 and refused otherwise), the identity check (`model_ok` = observed equals requested), the leak check and the anonymiser. Files outside `R1/`: none written except scratch under `/tmp` (`/tmp/r1-pre-override`, `/tmp/r1-override-smoke.out`) and the sandboxes under `/tmp/evalsb-collab-r1`.

## 5. Pins

Nothing the design pins by sha256 was edited, so there was nothing to re-pin: `config/catalogue.json` (`catalogue.sha256` and `manifest.json`), `config/brief.txt` and `judge-one.sh` (`manifest.json`) all still match, and the nine `values/*.json` still match their `.sha256`.
Procedure used (the design's own `spikes/gate0-check.sh`, which re-decides G-BASE and G-PINS against `manifest.json`): `sha256sum -c --quiet config/catalogue.sha256`, then `bash spikes/gate0-check.sh`. Result 12:29 UTC: `G-BASE pass, G-PINS pass, S0 pass, S2 pass, REQ-S3 recorded, S3 pass, Spike 4 pass` (the earlier file said Spike 4 `missing` because the sl2 values did not exist when it was last written). `g-pins.sh` was not re-run: it would rewrite `manifest.json` with identical hashes. The launcher preflight passed for the smoke row.

## 6. Tests

`uv run pytest .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests -q -rs -p no:cacheprovider` from `REPO`: **167 passed, 0 skipped, 0 failed, 52.9 s**; `uv run ruff check` on the folder clean; `bash -n` clean on every script.
That is the 138 earlier tests, 10 in `tests/test_slack.py` (added meanwhile by the separate `PANEL_SLACK_S` change, see section 9) and 19 new cases in `tests/test_cap_exception.py`:

- the rule on and off (input not mutated; off and "no measured 0" return the same object; only the zero role forced; hang guard is a max, never a cut; all nine real values files);
- `values.py deadlines`: off output has exactly the old keys and numbers, on gives forced k, 3.0 x B hang guard, finish +(hang delta), guard = finish; refused for collab 0 and when the values file is missing;
- `launch.sh`: on (row id `el2-c1x-r0`, stamps in all four files, hook argument K = 1 in every settings file, hang 300 s / finish 200 s for B = 100 s, results columns), off both unset and `0` (k 0, hang 150 s, no stamp, no new key anywhere), refused values `2`, empty, `yes`, and `1` with `PANEL_COLLAB=0` (exit 2, nothing ran), and the normal gates and values checks still apply;
- `collab_summary.py` columns only with the stamp; `results.py` row id and stamp (`c0x` rejected); `alarms.py` keeps the exception rows apart.
A mutation check (hang multiplier 3.0 changed to 2.0) made 4 of the 19 fail; the file was restored.

## 7. Smoke result (one real row, model sessions: 3 reviewers + the Opus judge)

Command (run from `REPO`): `TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 bash R1/tools/launch.sh el2 0 TASK-WF-design-20261108-041415`. Row `el2-c1x-r0`, exit 0, 12:29:09 to 12:32:08 UTC. At most 3 reviewer sessions at once; models ember `muse-ember-1.0` and 2x `gpt-6-luna` as reviewers, `claude-opus-5-5` only as the judge; `NOFALLBACK=1`; no `fallback.log`.
Checked with `bash R1/spikes/smoke/override-check.sh R1 el2-c1x-r0 TASK-WF-design-20261108-041415` (output kept in `spikes/smoke/check-override-el2-c1x-r0.tsv`): **all seven 6.4 conditions true, and O1-O6 true**.

| Item | Value |
|---|---|
| B_A1 (values file) | 96.976 s |
| Measured k / used k | searcher 0 / 1, reader 0 / 1 |
| Timers used | hang 290.9 s (old 145.5), finish 185.6 s (old 40.2), guard 185.6 s |
| Elapsed (panel, T0 to last reviewer end) | 106.0 s, ratio 1.093 x B_A1 (`slo_breach` false, no hang kill, no finish signal) |
| Delivered | t2b-1 (ember) 1: M2 at tool call 6 (t = 19.5 s), search slot, not executed afterwards; t3-1 (luna) 1: M8 at call 8 (t = 38.1 s), reading slot; **t4-1 (luna) 0: it ended after 5 tool calls (64.8 s) and never reached its checkpoint at call 8** |
| Hook | `hook_calls` 10 / 5 / 14, `hook_ms_p95` 128 / 29 / 144, 0 hook errors, snapshot taken before each delivery, 0 leak violations, 0 `task_hint` keys |
| Judge | parsed `score.json`, `gt_covered_any` empty, `wrong_blockers` 3 (one sample, not a result) |
| Conditions 6.4 | models ok; dropped lines 0; hooks and injections <= k, none after the guard; merge rc 0; anonymiser leak 0; `status` `incomplete` (one package) as the design expects; sandbox clean, candidate sha unchanged, 3 session files deleted |

What the smoke shows about the arm itself: forcing k = 1 does deliver a message when the reviewer reaches its checkpoint call, but a reader that finishes in fewer than 8 calls gets nothing whatever k is (the earlier real smoke on designSpec had one luna at 5 calls too). The checkpoint call numbers (searcher 6 and 10, readers 8 and 12) are unchanged because the owner asked only for the time exception; whether to lower the reader checkpoint is a separate owner decision.

## 8. Launch commands

All from `REPO`; each launch runs DS, AL, DE one after another, 3 reviewer sessions at a time, then the Opus judge, and exits 0 (row written, all packages ok), 1 (row written, a package invalid, quarantined or judge_failed) or 2 (refused). Use `nohup ... &` or the Bash tool's background mode. `<rep>` is a whole number of 1 or more (0 is reserved for smoke; `el2-c1x-r0` exists). Set `R1=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar` first.

Collaboration row with the override (one panel, three packages, judged):

```bash
cd /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
R1=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar
TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 bash $R1/tools/launch.sh el2 1   # el2: ember + 2x luna  -> row el2-c1x-r1
TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 bash $R1/tools/launch.sh hl2 1   # hl2: haiku + 2x luna  -> row hl2-c1x-r1
TIME_CAP_EXCEPTION=1 PANEL_COLLAB=1 bash $R1/tools/launch.sh sl2 1   # sl2: sonnet + 2x luna -> row sl2-c1x-r1
```

Longest hang guard per package on each panel (the cap that kills a stuck reviewer): el2 435 s, sl2 907 s, hl2 1026 s; the three guards of a panel add up to about 16 (el2), 33 (sl2) and 39 (hl2) minutes, the most a launch can take before the judge runs.

Isolated baseline with the same harness (no hook, no `--settings`, no override; `TIME_CAP_EXCEPTION=1` is refused here). The collab-0 rows `<panel>-c0-r1..r3` already exist for all three panels (they are the Spike 4 rows and a finished row is never re-run, so launching rep 1-3 again exits 2); the matching new baseline needs `rep` 4 or more:

```bash
PANEL_COLLAB=0 bash $R1/tools/launch.sh el2 4   # -> row el2-c0-r4
PANEL_COLLAB=0 bash $R1/tools/launch.sh hl2 4   # -> row hl2-c0-r4
PANEL_COLLAB=0 bash $R1/tools/launch.sh sl2 4   # -> row sl2-c0-r4
```

One package only (a smoke row, as run here): append the package name, with `rep` 0 for the collab-1 override smoke on a panel.
Summaries: `uv run python $R1/tools/alarms.py <panel>` (override rows in the `time_cap_exception` section only); per-row columns in `results/<row>.json`.

## 9. Things the owner should know

1. **Two changes in the same folder at once.** A separate session (`launch-slack.sh`, output in `SLACK.md`, tests in `tests/test_slack.py`) changed `tools/values.py`, `tools/launch.sh` and `tools/alarms.py` for `PANEL_SLACK_S` (30 s on top of the cap) while this work ran. My edits are additive and were made after reading its version; the full suite passes with both. The two switches are independent and combining them (`PANEL_SLACK_S=30` with `TIME_CAP_EXCEPTION=1`, which would apply the exception to the `values-slack30` files) is **not tested here**; run override rows with `PANEL_SLACK_S` unset.
2. **The finish signal can still fire.** On an override row it fires at the widened finish offset (for example el2 DE at 185.6 s, 1.9 x B_A1); a reviewer still running then gets "finish now" and may then run to the hang guard. It did not fire in the smoke (every reviewer ended before 107 s).
3. **Time verdict.** Override rows are by definition outside the +35% window; the columns give the measured ratio per package but no row is judged against the old SLO.
4. **Model rule.** No Qwen, glm or grok was started by this work; Opus ran only as the blind judge. (The earlier implementation session's Opus use for T4 advice is a separate matter recorded in `IMPLEMENTATION.md` section 8, item 10.)
5. Nothing was staged, committed or pushed. Not run: full three-package rows (the orchestrator runs them).
