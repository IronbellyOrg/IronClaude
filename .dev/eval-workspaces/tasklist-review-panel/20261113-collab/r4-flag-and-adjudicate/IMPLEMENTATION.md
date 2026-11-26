# Redesign 4, Flag-and-Adjudicate (F7): implementation report

Source: `DESIGN.md` in this folder. Ledger: `.dev/implement/collab-r4-flag-and-adjudicate/progress.md`.

## 1. Status

This file was rewritten by the resumed implementation session (the first session was killed when its host session ended) after re-running everything. Facts on disk, 2026-11-13 23:25-23:55 UTC:

| Part | State |
|---|---|
| Files of design section 1 | RUNS: all built except the Spike 4 values files (`values/<P>.json`, `-srun.json`, `-slowdown.json`, see below); `bash -n` clean on every shell script, `ruff check lib tests` clean |
| Offline tests (design 6.1, 6.2) | RUNS: 106 passed, 0 failed (section 4) |
| Gate 0 spikes S0, REQ-S3, S2 | RAN on 2026-11-13 21:01-21:41 UTC (reused, not repeated); results in section 5; luna act rate is 0/5 |
| One-package smoke (design 6.4), EL2 on the control package, F7 row and A1 row | RUNS: both pass every 6.4 condition (section 6). The first two F7 smoke rows are kept as invalid rows: the first died with the host session, the second exposed a real hook race that is now fixed (section 6) |
| Spike 4 (values files, slowdown) and full EL2/SL2/HL2 rows | NOT RUN (orchestrator constraint: full panel runs are the orchestrator's). Section 7 lists every acceptance criterion that is therefore not met |
| SL2 and HL2 smoke | NOT RUN. Design AC-11 asks for them only for panels that Spike 4 makes runnable, and Spike 4 was not run |
| Design review 3 fixes | NOT RE-REVIEWED (the design's own status: the review loop allows no fourth review) |

## 2. What was built

All paths are relative to this folder (`R4`). Every file named in design section 1 exists except the Spike 4 values files `values/<P>.json`, `values/<P>-srun.json` and `values/<P>-slowdown.json` (and their `.sha256`), which need full panel runs and were not built (section 7). Line counts are from `wc -l` after the last code edit.

| File | Lines | What it does |
|---|---|---|
| `frozen/packages.json` | 1 | The three packages, their H3 base trees and run order |
| `frozen/panels.json` | 10 | EL2, SL2, HL2: flagger and two luna adjudicators, critical-path role, planning numbers, allowed models, TIER and ALIAS maps (from `merge-b11.sh:11-12`) |
| `frozen/brief-a1.txt` | 5 | `RR:13-17` with `{CAND}`, `{SHA}`, `{SRC}` and the one H1 sentence; checked line by line against `run-reviewer.sh` |
| `frozen/brief-flagger.txt`, `frozen/brief-adjudicator.txt` | 6, 1 | The role paragraphs of design 2.4 |
| `frozen/moves.json`, `frozen/templates.json` | 12, 6 | M1-M10 verbatim from `REQ` 2.0; the `challenge`, `finding`, `finish`, `reask` texts of design 2.5 |
| `frozen/pins.sha256` | 14 | sha256 of every frozen file, `lib/values.py`, `lib/results.py`, `lib/arm_summary.py`, `REQ`, `judge-one.sh`, `findings.py`, `ledger.py` |
| `lib/card.jq` | 17 | The only card schema check (writer, reader, audit, metrics) |
| `bin/panel-post` | 78 | Card writer: refusal order of design 2.2, flock append, deal, `post_accepted` with line sha256 |
| `bin/r4-hook` | 138 | PostToolUse reader: call counter, finish signal, delivery gates, seal before first delivery, forms, never fails a review; steps 6-10 run under a per-reviewer lock so parallel tool calls cannot deliver a card twice (section 6) |
| `bin/reviewer.sh` | 147 | One reviewer: RR launch line with the section 4 changes, hang guard, 2-attempt retry (attempt 2 isolated), transcript copy by session id, H2 normalise and one `--resume` re-ask, meta and cost |
| `bin/build-sandbox.sh` | 45 | H3/H4 sandboxes from the T1 start trees, candidate/source copies, `candidate.flat`, `manifest.json` |
| `bin/run-panel.sh` | 200 | The launcher: preflight refusals, concurrency gate, boards/settings/helper, three reviewers at once, merge, collab, audit, quarantine, anonymise, judge, results, schedule |
| `bin/anon.sh` | 46 | Anonymiser and its forbidden-string check |
| `bin/judge.sh` | 43 | Runs the unchanged `judge-one.sh` through a `/tmp/jdg.*` staging directory, retry once, EVAL-write check, cleanup trap |
| `lib/normalize.py` | 67 | H2 truncation plus the real `findings.parse_block` |
| `lib/values.py` | 291 | k, finish offset, hang guard, slowdown limit, turn parsing, p90; CLIs `planning`, `build`, `srun`, `slowdown` |
| `lib/collab.py` | 283 | `overlap12`, `task_of`, slots, conversion, peer-tag sidecar, Jaccard, `collab.json` |
| `lib/audit.py` | 283 | Sandbox, candidate, board-line and transcript audit; ground-truth contamination checks |
| `lib/results.py` | 192 | The results row of design 5.2, including judge-credited conversion |
| `lib/arm_summary.py` | 210 | Arm-level stop rules, alarms, SLO budget, drift band, no-loss, Fisher reach, form contrast, interim futility |
| `spikes/probe-hook`, `spikes/s0-req-s3.sh`, `spikes/s2-resume.sh` | 29, 85, 32 | Gate 0 spikes S0, REQ-S3 and S2 |
| `tests/fake-claude` | 203 | **Test scaffolding only**: the stand-in `claude` the tests put first on `PATH` |
| `tests/r4help.py`, `tests/conftest.py`, `tests/test_*.py` (15 files) | 1,580 | The offline test plan of design 6.1 and 6.2, plus the parallel-hook test added by this session |
| `ruff.toml` | 7 | Not in the design. Lint config for this folder only: extends the repository `pyproject.toml` and ignores N803/N806 in `lib/` and `tests/`, because `B`, `K`, `N` are the design's own symbols and `lib/values.py` is pinned by sha256, so it is not renamed |
| `manifest.json` | | Written by `build-sandbox.sh` (rebuilt this session; `/tmp/evalsb-collab-r4` had been cleared) |
| `implement-report/`, `design-report/` | | Session logs of the implementation and design sessions (not code) |
| `values/planning-{EL2,SL2,HL2}.json` (+ `.sha256`) | | Planning values, written by `values.py planning` for the smoke test |
| `spikes/out/` | | Spike results (section 5) |
| `runs/`, `results/` | | Smoke rows (section 6) |

Scratch outside this folder: sandboxes, boards and candidate copies under `/tmp/evalsb-collab-r4`; spike work directories and logs under `/tmp/collab-r4`; Claude Code's own session transcripts under `~/.claude/projects`.

## 3. How to run one panel on all three packages

Run from any directory; every path below is absolute. Each launch holds the shared gateway lock. A row id can be used once (a re-run with the same id is refused and leaves the row untouched).

```bash
R4=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r4-flag-and-adjudicate
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel

# once: sandboxes (idempotent) and planning values
$R4/bin/build-sandbox.sh
for P in EL2 SL2 HL2; do uv run --frozen --project $REPO python $R4/lib/values.py planning --panel $P; done
```

**Values file.** The design's arm runs use the Spike 4 file `values/<P>.json`, which does not exist yet (Spike 4 needs four full `PANEL_COLLAB=0` rows per panel, which this build was told not to run; section 7). Until it exists, use `values/planning-<P>.json`. After Spike 4, replace `planning-<P>.json` by `<P>.json` in every command below.

```bash
# ember + 2x luna (EL2), collaboration on, then off
PANEL_COLLAB=1 NOFALLBACK=1 flock /tmp/collab-gateway.lock $R4/bin/run-panel.sh --panel EL2 --row f7-el2-r01 --values $R4/values/planning-EL2.json --block b01
PANEL_COLLAB=0 NOFALLBACK=1 flock /tmp/collab-gateway.lock $R4/bin/run-panel.sh --panel EL2 --row a1-el2-r01 --values $R4/values/planning-EL2.json --block b01

# sonnet + 2x luna (SL2)
PANEL_COLLAB=1 NOFALLBACK=1 flock /tmp/collab-gateway.lock $R4/bin/run-panel.sh --panel SL2 --row f7-sl2-r01 --values $R4/values/planning-SL2.json --block b01
PANEL_COLLAB=0 NOFALLBACK=1 flock /tmp/collab-gateway.lock $R4/bin/run-panel.sh --panel SL2 --row a1-sl2-r01 --values $R4/values/planning-SL2.json --block b01

# haiku + 2x luna (HL2)
PANEL_COLLAB=1 NOFALLBACK=1 flock /tmp/collab-gateway.lock $R4/bin/run-panel.sh --panel HL2 --row f7-hl2-r01 --values $R4/values/planning-HL2.json --block b01
PANEL_COLLAB=0 NOFALLBACK=1 flock /tmp/collab-gateway.lock $R4/bin/run-panel.sh --panel HL2 --row a1-hl2-r01 --values $R4/values/planning-HL2.json --block b01
```

- The HL2 `PANEL_COLLAB=1` command is **refused at planning values** (exit 2, `F7 not runnable on HL2: k = 0 on every package`), as design section 3 specifies: haiku's planning turn time (23 s) gives k = 0. It runs only with a Spike 4 values file in which k >= 1 on at least one package. The HL2 `PANEL_COLLAB=0` command runs.
- Output: `runs/<row>/` (per package: `panel.json`, `reviews/`, `board/`, `tags/`, `slots.json`, `collab.json`, `merged-1.md`, `scoring/`), `runs/<row>/audit.json`, `results/<row>.json`, one line in `runs/schedule.jsonl`; a refused launch appends to `runs/refusals.jsonl`. Exit 0 when every package was scored, 1 otherwise, 2 on a refusal.
- `--seed <int>` fixes the deal coins; `--packages "<ids>"` limits the row (a partial row is `valid: false`); `--no-judge` stops after the audit (Spike 4 rows).
- Arm summary after rows exist: `uv run --frozen --project $REPO python $R4/lib/arm_summary.py --panel EL2 --a1 $R4/results/a1-el2-*.json --arm $R4/results/f7-el2-*.json --out $R4/results/EL2-F7-summary.json`.
- Spike 4 order per panel (design 6.3): 4 rows of `PANEL_COLLAB=0 ... --values values/planning-<P>.json --no-judge`; `values.py build --panel <P> --runs <those 4 row dirs>`; `values.py srun --panel <P>`; 2 rows of `PANEL_COLLAB=1 ... --values values/<P>-srun.json --no-judge`; `values.py slowdown --panel <P> --a1 <4 dirs> --srun <2 dirs>`.

## 4. Test results

Command, from `REPO`: `uv run pytest .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r4-flag-and-adjudicate/tests`. Last run (after every code change of this session): **106 passed, 0 failed, 0 errors in 145 s** (log `/tmp/collab-r4/pytest-final.log`; the run before the hook fix gave 105 passed in 144 s). No test calls a real model: `tests/fake-claude` stands in for `claude`, and `HOME`, `R4_SBR` and `R4_OUT` point at pytest temporary directories.

| File | Tests | Covers (design 6.1 / 6.2) |
|---|---|---|
| `test_card_validator.py` | 4 | 4 good cards pass unchanged; `claim`, `verdict`, category on a `move` line, M1, 11-character anchor, luna `from`, extra `note` rejected; the 601-byte line dropped by the caller; 3rd post with cap 2 refused `over_cap` |
| `test_panel_post.py` | 7 | `too_early` then accepted; `after_finish`; whitespace variant stored flattened; `anchor_not_in_candidate`; `bad_args`/enum refusals; deal for r = 0 and r = 1; 8 concurrent posts give c0..c7 once each |
| `test_hook.py` | 13 | 16 parallel hook calls per luna deliver each of its 2 cards exactly once with one seal and no `nosnap` (added; it failed before the fix with 8 deliveries); no delivery before call 6; t4-1 gets c0 (challenge) then c2 (finding), t3-1 c1 (finding) then c3 (challenge); c = 1 forms F, C, C, F; at most one per call and k per luna; flagger receives nothing; `--deliver 0`; finish text once and nothing after; delivery under `env -i`; output shape and 1,500-character cap; seal before first delivery; subagent calls counted apart; forged line never delivered; `calls` = `abc` gives `hook_error`; garbage line skipped; missing transcript and read-only `snap/` give `nosnap` |
| `test_normalize.py` | 6 | 250-character anchor cut to 200 and still located; claim cut to 300 with other lines byte-identical; line breaks; bad severity; no block; idempotent |
| `test_values.py` | 13 | all eight `k_of` vectors including the SL2 51.795/51.8 threshold and HL2 rows; 143.8 and 174.0; turn parsing with a two-entry final message and a sidechain entry; nearest-rank p90; the four CLIs and their `.sha256`; section 3 slowdown limits |
| `test_collab.py` | 6 | `overlap12` at 12 and 11; `task_of` T3 and None; forms and deal; R-25 Jaccard fixture; peer tags, conversion, `late`, `flag_finding_overlap` 0.5; every R-23 key present, design-only keys null |
| `test_anon.py` | 3 | all forbidden strings stripped and one label per id; "a peer reviewer" rewritten; `T4-1` makes the check fail |
| `test_judge.py` | 3 | one run copied back, staging under `/tmp/jdg.` resolved through `C`, removed, nothing new under `EVAL`, `judge-one.sh` sha256 unchanged; API error retried exactly once; double failure `judge_failed` |
| `test_results.py` | 2 | hand-computed totals and credited conversion; a failed package nulls every total |
| `test_arm_summary.py` | 14 | `STOP:no_cards` at 7/12; `STOP:flag_finding_overlap`; CONVERGENCE by Jaccard and by ledger rows; SNAPSHOT; AGREEMENT both ways; SLO 4/36 vs 3/36; independence fails on an audit row; Fisher p 0.047, 0.034, 0.045; form-contrast z and run-paired difference; no-loss fails at wrong blockers A1 + 1.5; drift band |
| `test_reviewer.py` | 4 | `PANEL_COLLAB=0` argv equals `RR:48` except section 4's differences; collaboration adds only `--settings`; flagger and k = 0 briefs |
| `test_launcher.py` | 9 | refusals (no `NOFALLBACK`, bad `PANEL_COLLAB`, unknown panel, values sha mismatch, all k = 0, glm, Qwen, Opus, luna flagger, pins mismatch) exit 2 before any reviewer and log to `refusals.jsonl`; full offline F7 row and A1 row with every 1.5 file and 5.2 key; reviewers start within 2 s; existing row refused and byte-identical; A1 has no board or `--settings`; concurrency count ignores `timeout` and `bash` parents |
| `test_faults.py` | 19 | flagger never posts; cards on Task 1 give `early_tasks_only`; findings reuse 3 of 4 anchors gives 0.75; snapshot missing (review still `final_ok`); luna past finish; hang in A1 and F7 rows killed within 6 s of T0 + 1.5 B; hook error with review complete; attempt 1 fails gives isolated attempt 2; parser drop gives exactly one re-ask and `dropped_lines = 1`; wrong model gives `invalid_model`; one reviewer without a block is still merged and judged; no valid block gives `merge_refused`; two forged lines give `board_lines_invalid = 2`; three ground-truth access routes quarantine the row; sandbox write; harness text leak |
| `test_build_sandbox.py` | 1 | real trees: no leak directories, clean `git status --ignored`, manifest trees, candidate sha, a Task-edited file differs from HEAD, second build skips |
| `test_pins.py` | 2 | harness text has no 12-character `plan_quote` overlap (the A1 brief's one hit, `", or when the "` on designSpec GT3, is printed, not asserted); `sha256sum -c pins.sha256` run from `frozen/` passes (the pins file lists paths relative to `frozen/` and absolute paths, so the check must run from there; run from `R4` it reports files it cannot read) |

Extras: `ruff check lib tests` prints `All checks passed!` (the first session left 13 style findings; this session renamed the `A` alias, removed an unused test variable and a `;`, sorted imports, and added `ruff.toml` for the design's `B`/`K`/`N` symbols); `bash -n` passes on every shell script and on `r4-hook`, `panel-post` and `probe-hook`; `tests/fake-claude` is a Python script (`uv run ... python -I` shebang), so `bash -n` does not apply to it; `ruff check tests/fake-claude`, named explicitly, passes.

## 5. Gate 0 spike results

All real-model spikes ran on 2026-11-13 between 21:01 and 21:41 UTC, each under `flock /tmp/collab-gateway.lock` with `NOFALLBACK=1`, in the designSpec sandbox. The raw work directories under `/tmp/collab-r4/s0-*` and `s2-*` no longer exist (`/tmp` was cleared before the resume), so the per-session hook logs cannot be re-read; the recorded results in `spikes/out/` are what remains and were reused, not repeated. Results are in `spikes/out/`; `spikes/out/s0-summary.json` is the authoritative S0/REQ-S3 file (recomputed from the hook logs, see the correction below).

**S2, resume part (`spikes/out/s2-<model>.json`).**

| Model | `--session-id` names the transcript file (D-5) | `--resume` reply | Model on resume | Result |
|---|---|---|---|---|
| gpt-6-luna | yes | `BETA` + `ALPHA` | right | pass |
| muse-ember-1.0 | yes | `BETA` + `ALPHA` | right | pass |
| claude-sonnet-5-5 | yes | `BETA` + `ALPHA` | right | pass |
| claude-haiku-5-5 | yes | `ALPHA` only | right | **strict fail** |

Haiku's resumed session kept the earlier context (it repeated `ALPHA`) and the model was right, so the H2 re-ask mechanism works on haiku; it did not follow the second half of the instruction (`BETA`). Deviation D-5 is confirmed on all four models.

**S0 (`spikes/out/s0-summary.json`, 5 sessions per model; ember 4, see below).**

| Check | Result |
|---|---|
| PostToolUse hook with no matcher fires on every successful main-thread tool call | yes, all four models (6-8 hook calls per session) |
| `transcript_path` present and readable; copy + sha256 at call 2 | yes, every session |
| Hook time per call | probe hook at most 27 ms (`hook_ms_max` per model in `s0-summary.json`). For `r4-hook` itself, the board metrics of `smoke-f7-el2-3` give 9 to 143 ms over 35 calls; the earlier "9-81 ms offline" figure of the first session has no file behind it and is dropped |
| Transcript entries carry `timestamp` | yes |
| One assistant message written as several entries | yes, in every model (thinking, text and tool_use blocks share one `message.id`); no tool result ever appears between entries of one message, so the turn rule of design 2.7 holds |
| A tool call that exits non-zero fires PostToolUse | **no**, in all 19 usable sessions (step 5, `ls /nonexistent-...`) |
| A subagent's tool calls fire the session's hook and carry `agent_id` | yes (ember and haiku session 1 each started a subagent: one hook input with `agent_id`); luna and sonnet never started one |
| The `claude` wrapper adds a `--settings` of its own | no: the real binary's argv holds exactly our one `--settings` |
| Concurrency pattern counts a live session once | Only partly shown by S0. The recorded process list (`real_process_argv` in `s0-<model>.json`) holds the real binary `/opt/nvm/.../bin/claude -p ...` and its `timeout 600 claude -p ...` parent, and the pattern separates those two by their command lines; the recorded count during a run (`"6 0"`) includes other sessions on the host, so S0 holds no one-session baseline. The counting itself is unit-tested (`tests/test_launcher.py`, `test_concurrency_count_pattern`) |
| Sandbox project hooks | the sandbox `.claude/settings.json` registers two PreToolUse commands whose scripts are gitignored and absent; S0 recorded `sandbox_project_hook_events: ["PreToolUse"]` for luna, sonnet and haiku (null for ember), and our PostToolUse hook fired in every session, so the sandbox's project settings and our `--settings` file both apply. The raw logs are gone, so whether those two hooks printed errors cannot be re-read |

Consequence of the non-zero-exit finding (design 2.2 and 2.3 asked for a re-check): the call counters count *successful* tool calls only. A refused `panel-post` (exit 1) does not advance the flagger's counter, and a luna's failing Bash calls do not count toward its 6th-call delivery gate, so a luna with many failing commands receives its cards later. No code change was made; the gates stay as designed.

**REQ-S3 act rates (`spikes/out/act-rates.json`).**

| Model | Sessions | Acted on the injected `run ls /tmp/panel-probe` | Stopped after the finish text (no further tool call) |
|---|---|---|---|
| gpt-6-luna | 5 | **0/5** | 2/5 |
| muse-ember-1.0 | 4 | 0/4 | 0/4 |
| claude-sonnet-5-5 | 5 | 3/5 | 5/5 |
| claude-haiku-5-5 | 5 | 0/5 | 0/5 |

- Correction: the first summaries written by `s0-req-s3.sh` counted a session as "finished within one turn" when it made at most 7 hooked calls. Because a failing call fires no hook, a session that ran every remaining step also ends at 7, so that rule reported luna 5/5 and haiku 4/5. The rule is now "no hooked main-thread call after call 6"; the numbers above are recomputed from the hook logs and the script is fixed (and re-checked against the fake).
- Ember session 5 never started: Claude Code updated itself at 21:24 and `/usr/local/bin/claude` failed with `exec: /opt/nvm/versions/node/v24.22.2/bin/claude: not found`. A reviewer launched at that moment would fail its attempt the same way (attempt 2 would then run isolated).
- The design's gate reads "The F7 arm runs only with a non-zero act rate for luna (the receiver)". Measured luna act rate is **0/5**, so by the design's own rule the F7 arm is not run. The probe is an unannounced instruction; real cards are announced in the adjudicator brief ("Settle every card you receive"), so the smoke row's conversions and `card <id>: passed` lines (section 6) are the direct evidence for luna acting on cards. Whether that evidence may replace the probe rate is the owner's decision (section 7).
- The finish signal is ignored by luna in 3 of 5 sessions and by ember and haiku every time, so on those models the bound is the hang guard, not the finish signal.

**G0-F7 cards (`cards_sent > 0` per flagger model).** See section 6: the EL2 smoke row covers ember (4 cards sent). Sonnet is not covered, because no SL2 smoke row was run; haiku cannot be checked, because HL2 F7 is refused at planning values (k = 0).

**Not run:** Spike 4 (needs 4 full `PANEL_COLLAB=0` rows and 2 srun rows per panel, which are full panel runs the orchestrator reserved for itself); Spike 5 and S1 (deviation D-4 and design 6.3: not owned by this build).

## 6. One-package smoke test

Design 6.4 (EL2 = muse-ember-1.0 flagger `t2b-1` + gpt-6-luna `t4-1` and `t3-1`, planning values, control package `TASK-WF-design-20261108-041415` only). Commands, run from any directory after `build-sandbox.sh` and `values.py planning --panel EL2` (the A1 command is the same with `PANEL_COLLAB=0`):

```bash
PANEL_COLLAB=1 NOFALLBACK=1 flock /tmp/collab-gateway.lock $R4/bin/run-panel.sh --panel EL2 --row smoke-f7-el2-3 --values $R4/values/planning-EL2.json --packages TASK-WF-design-20261108-041415
```

Checked by a scratch script (`/tmp/collab-r4/check_smoke.py`, not part of the build) that tests each pass condition of 6.4; its output is kept in `spikes/out/smoke-check-<row>.json`.

| Row | Result |
|---|---|
| `smoke-f7-el2-3` (F7, valid smoke) | **Every 6.4 condition passes**, `all_ok: true`. Three `model_ok: true`, `dropped_lines` 0, no re-ask, no retry; `merged-1.md`, `merged-anon.md`, `score.json` exist; `collab.json` has the 23 top-level keys the checker tests (`test_collab_schema` covers the full R-23 list offline); `cards_sent` 4 (cap 2k = 4, none rejected), `cards_delivered` 4 (2 challenge, 2 finding), `late` 0, `no_snapshot` 0; both lunas `seal_sha_ok: true`; `audit_ok: true`, `harness_text_gt_overlap` 0, `board_lines_invalid` 0; anonymiser grep clean; nothing under `EVAL` newer than the run start; no `/tmp/jdg.*` left; results row has every 5.2 key and `valid: false` (one package, by definition). Elapsed 117.7 s against B 116 s (+1.5%); reviewer wall 28 s (flagger), 99 s and 118 s (lunas). Mechanism: 2 of 4 delivered cards converted into a luna finding (1 challenge, 1 finding form), 2 cards got a `card <id>: passed` line, `flag_finding_overlap` 0.25, `adjudication_agreement` 0.5, card Tasks T10, T1, none, T8. Judge (descriptive only): found 0 of 2 control items, 1 wrong blocker, 1 merged row. `anchor_gt_overlap` 2 (two card anchors overlap a ground-truth quote by 12+ characters: counted, not failed, design open question 3). `hook_ms_p95`: 16 ms flagger, 143 ms and 90 ms lunas (above the 0.1 s planning budget at its p95; UNVERIFIED cause: the calls that deliver a card, plus waiting for the new delivery lock when calls run in parallel) |
| `smoke-a1-el2-1` (A1, `PANEL_COLLAB=0`) | **Every 6.4 condition passes**, `all_ok: true`. No board directory in the run or under `/tmp/evalsb-collab-r4/board`, no `--settings` (attempt meta `settings: false` for all three), `cards_sent` 0, `arm: "A1"`. Elapsed 110.0 s (-5.1% against B), 2 ledger rows, found 0 of 2, 1 wrong blocker, `audit_ok: true` |
| `smoke-f7-el2-2` (F7, kept as an invalid row) | Completed and scored, but showed a real defect: both lunas ran parallel tool calls, two hook processes raced, each luna's first card was delivered twice (`c0` to `t4-1`, `c1` to `t3-1`, both in the `state/<rid>.delivered` files) and a false `nosnap` blocked `c2` and `c3` (`cards_delivered` 2 of 4, `snapshot_missing: true` although the seal was written). Fixed in `bin/r4-hook` (per-reviewer lock around steps 6-10) and covered by the new `test_parallel_tool_calls_deliver_each_card_once`; this row is not evidence of the fixed hook |
| `smoke-f7-el2-1` (F7, kept as an invalid row) | Died, most likely with the host session of the first implementation run (it started 21:55:56 UTC, the reviewers' stderr stops at 21:57): three empty `attempt1.json` files and no `meta.json`, `run.json` still `"status":"running"`. Not repeated as such, because `run-panel.sh` refuses an existing row id; `smoke-f7-el2-2` and `-3` replaced it |

Nothing outside this folder changed during the smoke: `git status --porcelain --untracked-files=all` before and after differs only in files under the four `20261113-collab/r*` folders and the sibling brainstorm folder written by the other session. Model sessions run by this session: three rows (`smoke-f7-el2-2`, `smoke-f7-el2-3`, `smoke-a1-el2-1`), each 3 reviewer sessions plus 1 Opus judge session, so 9 reviewer and 3 judge sessions, never more than 3 reviewers at once. No Qwen, glm or grok session ran.

## 7. Requirements and acceptance criteria not met

### 7.1 Acceptance criteria of design 6.5

| Id | Status | Evidence or reason |
|---|---|---|
| AC-01 | MET | 106 passed, 0 failed, 0 errors (section 4) |
| AC-02 | MET for the smoke rows | `git status --porcelain --untracked-files=all` taken before `smoke-f7-el2-2` and after `smoke-a1-el2-1`, the three smoke rows of this session: every new path is under `R4/`, the other `20261113-collab/r*` folders, `.dev/implement/collab-r*` or the sibling brainstorm folder (other sessions); nothing under `src/` or `EVAL`. Not checked for a full row (none was run) |
| AC-03 | MET | `sha256sum -c pins.sha256` run from `frozen/` is clean (also run by `test_pins` and by the launcher before every row); `judge-one.sh` `a01bd70d...cfcc`, `findings.py` `f0e53967...ad5a`, `ledger.py` `29085498...8b8179` re-measured during this session and equal the design's values |
| AC-04 | MET | `test_reviewer.py` (argv of `PANEL_COLLAB=0` equals `RR:48` except section 4's differences) |
| AC-05 | MET | `test_launcher.py` refusals; `reviewer.sh` has no model ladder; the judge is `claude-opus-5-5` only |
| AC-06 | MET | tests, and both valid smoke rows (`board_lines_invalid` 0, lunas `msgs_sent` 0) |
| AC-07 | MET after the fix | tests and `smoke-f7-el2-3` (each luna got exactly its 2 cards once, on its 6th and 7th hook calls, with a `seal` metric line before the first delivery line, and no finish signal was sent). `smoke-f7-el2-2` broke it (duplicate delivery) before the fix |
| AC-08 | MET | `test_hook.py` vectors |
| AC-09 | MET | `test_faults.py` and `test_hook.py` fault cases (`hook_error` logged, review `final_ok: true`) |
| AC-10 | MET in the fault tests only | killed within 6 s of T0 + 1.5 B in an A1 and an F7 row with the fake `claude`. No real reviewer hit the guard |
| AC-11 | **PARTLY MET** | EL2 smoke passes with the planning values (section 6). Not done: the repeat with `values/EL2.json` (needs Spike 4), and the smoke for SL2 and HL2 (HL2 is refused at planning values by design; SL2 was not run) |
| AC-12 | **NOT MET** | No full EL2 row under either switch was run: the orchestrator reserved full panel runs for itself, so `valid: true` and `audit_ok: true` on a full row are untested. Both smoke rows are `valid: false` by definition |
| AC-13 | MET for the rows run | `smoke-f7-el2-2`, `-3` and `smoke-a1-el2-1` have `audit_ok: true` and `harness_text_gt_overlap` 0; no `/tmp/jdg.*` directory existed when checked once after all three rows had finished (`test_judge.py` checks the cleanup on every exit path offline). Not shown for a full row |
| AC-14 | MET for the two valid smoke rows | `find EVAL -newer <stamp>` empty (checker); not checked for `smoke-f7-el2-2` |

### 7.2 Gate 0 and other requirements not met

| Item | Status and reason |
|---|---|
| REQ-S3 gate: "the F7 arm runs only with a non-zero act rate for luna" | **NOT MET.** Measured luna act rate on the unannounced probe is 0 of 5 (section 5), so by the design's own rule the F7 arm is not to be run. This session ran F7 only as the smoke the design lists, where the cards are announced in the brief: there luna settled cards (2 passed lines, 2 conversions). Whether that evidence replaces the probe rate is the owner's decision |
| S2 on haiku | Strict fail: the resumed session repeated `ALPHA` but not `BETA` (section 5). The re-ask mechanism worked (context kept, model right) |
| G0-F7 (`cards_sent > 0` for each flagger model) | Met for ember (4 cards). Not run for sonnet (SL2 smoke) and not runnable for haiku (HL2 F7 refused at planning values) |
| Spike 4 (values files `values/<P>.json`, `<P>-srun.json`, `<P>-slowdown.json`) | **NOT RUN** (4 isolated full rows plus 2 slowdown rows per panel are full panel runs). Consequence: only `values/planning-<P>.json` exist, R-30's pinned measured values do not, and the slowdown limit s is unmeasured |
| Spike 5 and S1 | Not built, by design (D-4 and design 6.3) |
| Timing budget of the hook | `hook_ms_p95` was 143 ms and 90 ms on the lunas in `smoke-f7-el2-3`, above the roughly 0.1 s per call the design budgets (all 35 hook calls of that row: 9 to 143 ms). The review was not slowed visibly (+1.5% elapsed) but the budget is not met at p95 |
| Finish signal | Not acted on by luna in 3 of 5 spike sessions and by ember and haiku every time (section 5): the bound on those models is the hang guard, not the finish signal. This is a measurement, not a defect of the build |
| Design review 3 fixes (2.10 audit layers, D-5, coverage statement) | Not re-reviewed (design's own status). Minor findings m3-1 and m3-6 of the design review stay open. S0 did not close m3-1: it recorded the real process list and the pattern is unit-tested, but S0 holds no one-session count baseline (section 5) |
| Calls that exit non-zero | Do not fire PostToolUse (S0, all sessions), so the call counters count successful calls only. A refused `panel-post` does not advance the flagger's counter. The design asked for a re-check and no code was changed |
| Judge-credited conversion | Approximation by design (risk 6): `credited_method` says so in every row |
| Content-marker false positive | `score.json` appears in two sandbox files; a reviewer that reads either would be quarantined wrongly (note 7 of section 8). Not changed: the marker list is the design's |
| A full-row pass of the anonymiser and judge on the two bigger packages | Not run: only the control package went through merge, anonymiser and judge |

## 8. Implementation notes and departures from the design text

Each is a detail the design left open or could not hold on this host; none changes what a reviewer or the judge receives.

1. **`card.jq` call form.** Callers run `jq -R -r --arg flagger <rid> -f lib/card.jq` (raw line in, the same raw line out) instead of the design's `jq -c ...`, so the reader and audit hash and compare the exact board bytes and a non-JSON line yields nothing instead of a jq error.
2. **Merge command.** The `superclaude` on `PATH` (`~/.local/bin/superclaude`) is a separate `uv tool` install, not this repository's pinned `findings.py`/`ledger.py`. The launcher therefore runs `uv run --frozen --project REPO superclaude review merge ...` with exactly the design's arguments.
3. **Session ids.** `uuidgen` is not installed; the `--session-id` value (deviation D-5) comes from `/proc/sys/kernel/random/uuid`. A test caught this (the first argv test failed with an empty id).
4. **Test-only overrides.** Besides `R4_SBR` and `R4_OUT`, the scripts read `R4_REPO` (repository root, so tests can run a copy of `bin/lib/frozen` with changed `panels.json` or pins), and `audit.py`/`results.py` read `R4_EVAL` and `R4_FROZEN` (fixture ground truth, a leaking test copy of `templates.json`). `run-panel.sh --print-session-count` prints the concurrency counts so the pattern can be tested. Production runs set none of these.
5. **`task_of`.** Returns `None` when a non-Task `#` or `##` heading lies between the anchor and the last `## Task n:` heading above it, so an anchor in a `## Constraints` section after the Tasks is not attributed to the last Task.
6. **Results row additions.** `collab.<pkg>` also carries `receiving_lunas` (lunas dealt at least one card) and `baseline_elapsed_s` (B_A1), which `arm_summary.py` needs for the SNAPSHOT alarm and the drift band.
7. **File-name content markers can match the sandbox.** `score.json` occurs in two files of every sandbox tree (`.dev/releases/backlog/v5xx-Spec-generator-framework/SC_SPEC_COMMAND.md` and `UNIFIED_SPEC_GENERATOR_SPECIFICATION.md`). The design's claim covers only the five key markers, which occur in no sandbox. A reviewer that reads either backlog file would be flagged `content_marker` (a false-positive quarantine). Not changed, because the marker list is the design's.
8. **Judge status.** `judge.sh` writes `scoring/judge-status` (`ok`, `judge_failed`, `judge_wrote_into_eval`, `judge_setup_failed`), which the launcher copies into the package status.
9. **`dropped_lines`** is 0 for a reviewer with no findings block (its whole report is invalid; `final_ok` is false and the merge records `block ok false`).
10. **Audit heuristics.** `home_other` and `tmp_other` come from path-like tokens in tool-call inputs; `first_hand_suspect` counts adjudicator claims with a number followed by a count noun (files, lines, matches, ...) only when the transcript holds no Bash call. Both are descriptive, as designed.
11. **Exit code.** The launcher exits 0 when every package it ran was scored; a single-package smoke row therefore exits 0 although its results row is `valid: false` by definition.
12. **Delivery lock (departure from design 2.3).** The design takes a lock only for the call counter. Steps 6-10 of the reader now run under `flock` on `state/<rid>.deliver.lock`, held until the hook exits, and re-check the finish time after the wait. Reason: a reviewer that issues parallel tool calls fires several hooks at once (luna does), which delivered one card twice and made the seal race set `nosnap` (`smoke-f7-el2-2`). The frozen texts, the card schema and the deal are unchanged.
13. **Environment drift.** `/tmp/evalsb-collab-r4` and `/tmp/collab-r4` had been cleared when this session resumed, so the sandboxes were rebuilt with `build-sandbox.sh` (13 s; the manifest records the same trees). The installed `claude` is 2.1.325 (the design measured 2.1.323); it self-updated at 21:24 UTC during the first session, which briefly broke launches.
14. **Reused, not repeated.** The S0, REQ-S3 and S2 results (19 S0 and REQ-S3 sessions and 4 S2 sessions) were kept as recorded; no spike session was run again. Only the three smoke rows of section 6 used model sessions in this session.
15. **`lib/` is git-ignored by the repository.** `.gitignore:13` holds `lib/`, so `git check-ignore` matches every file under `R4/lib/` (six Python modules and `card.jq`), and a plain `git add` of this folder skips them. They are on disk and the tests and runs use them, but committing the build needs `git add -f` for `R4/lib` (this is not the `.claude/` case that the repository rules forbid). Not changed here: the folder name `lib/` is the design's.
16. **Known cosmetic inaccuracy.** In `r4-hook` the delivery time logged for a card is taken when the hook starts, so `first_delivery_t` can be a few tens of milliseconds earlier than `seal_t` (seen in `smoke-f7-el2-3`, `t4-1`) although the seal is written first. The order of the metric lines is the true order; no gate reads these two times against each other.
