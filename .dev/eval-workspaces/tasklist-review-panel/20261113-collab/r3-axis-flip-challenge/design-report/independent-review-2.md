# Independent review 2: Redesign 3 (Axis-Flip Challenge, F1) DESIGN.md

verdict: FAIL

Reviewed file: `R3/DESIGN.md` (950 lines, read in full). R3 = `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge`, REQ = `.dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md`, EVAL = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1`, RR = `EVAL/tools/run-reviewer.sh`.

Summary: 9 of the 10 blocking findings from review 1 are fixed. #3 is still open: the test row was not updated. The revision also added one new blocking defect (N1): the stricter sandbox audit flags files that a user-level SessionStart hook writes into every new sandbox, so every run would be marked contaminated.

## Blocking findings of review 1

| # | Status | Current DESIGN.md evidence | Re-check |
|---|---|---|---|
| 1 | FIXED | :723 counts `timeout` parents: `pgrep -fc '^timeout .* claude -p --model '`, plus an ember variant | `/usr/local/bin/claude:3-10` execs `/opt/nvm/.../bin/claude` or `ccsession-orca`, as stated. RR:48 runs `timeout 3000 claude -p --model ...` and judge-one.sh:25 runs `timeout 900 claude -p --model ...`, so both are counted. The 5.2, 5.4 and 7.2 commands all start with `timeout ... claude -p --model "<model>"`. Test arithmetic (:817): 7+3=10 proceeds, 8+3=11 waits; ember 3+1=4 proceeds, 4+1=5 waits. Correct. |
| 2 | FIXED | A9 (:59), 8.2 step 4 (:497) and `test_combine` (:809, the 250-character anchor case) all compare with `normalise(sealed line)`. The seal at :341 stays raw | One rule, used everywhere. |
| 3 | NOT FIXED | 5.2 (:311) now lists `--kill-after=5` as part of the hang guard, and REQ:1009 (R-05) allows "the common hang guard". But the `test_command_diff` row (:800) is unchanged: "differ only in: cwd, brief, timeout value, missing `--no-session-persistence`; nothing added". `--kill-after=5` is an added token, so the specified test still fails on the specified command. Also, :339 says `test_command_diff` "asserts this for all four command forms", but the :800 row covers only the phase-1 command against RR:48, and `reviewer.sh print-cmd` (:86, :311) prints only the phase-1 line. | Fix: in :800 list "timeout arguments (`--kill-after=5 <T>` instead of `3000`)" and add cases for the 5.4 re-ask, the 7.2 resume, the 7.3 fallback and the 7.4 re-ask commands (asserting `--model`, `--permission-mode bypassPermissions`, `--disallowedTools Edit Write NotebookEdit`), with a `print-cmd` mode for each form. |
| 4 | FIXED | 5.4 re-ask (:333-337) has the full flag set. 7.4 (:469) uses the 7.2 command (:452-454, full flags). 7.3 (:465) reuses the same command. The rule is stated at :339 | The test assertion part is still missing; see #3. |
| 5 | FIXED | A10 (:60), step 2 (:266) and preflight (:712) require a frozen values file unless `R3_SMOKE=1` or `R3_SPIKE4=1`. Spike-4 rows go to `spikes/spike4/rows.jsonl` (:597). `summarize` refuses non-frozen rows and keeps `judge_ok: false` rows out of the quality means (:627). Covered by `test_guards` (:817) | |
| 6 | FIXED | 8.3 (:508-512) passes absolute paths. 10.1 step 3 (:573) redacts every `report <path>`. The residue list (:575) adds `p1norm`, `/runs/`, `/reviews/` and `-c[01]-`. `test_anon` (:812) has a relative-path case | `ledger.py:421-423` prints `- {rid}: report {path}, block ok ...` and `merge_cmd.py:86-95` takes the path verbatim, as stated. None of the 3 candidates contains any residue string (grep run). |
| 7 | FIXED | :549 adds `/.claude/projects/` to the forbidden reads and covers every attempt, re-ask, phase-2, fallback and subagent session. 9.5 (:559) captures all sessions, including killed attempts, before cleanup. F14b (:838) | Residual precision issues are listed as notes m4 and m5. |
| 8 | FIXED | AC-14 (:885) uses a sha256 manifest of `REPO/src` and `EVAL`, with ignored files included, plus `test_guards`. The git-status approach is explicitly rejected | |
| 9 | FIXED | `test_guards.py` (:817) covers the write guard (including symlink and non-`/tmp` override cases), admission with a stub `pgrep`, lock release, and the switch refusals | |
| 10 | FIXED | Section 4 (:276) gives one rule: `hang_kill` packages are invalid but stay in the time verdict as `SLO_BREACH`. `summarize` (:627) prints the slo_breach, invalid, judge-failure and contaminated counts, counts contaminated rows as rule-5 violations, and limits only the quality means. F8 (:831) and F10 (:833) agree | |

## New findings

| # | Grade | DESIGN.md line | Defect | Evidence | Fix |
|---|---|---|---|---|---|
| N1 | blocking | 9.4 "Sandbox untouched" (:547), 13.5 step 3 (:738) | The revised sandbox check uses `git status --porcelain --ignored --untracked-files=all` with an allowlist of only `__pycache__/`, `*.pyc`, `.pytest_cache/` and `.ruff_cache/`. The user-level SessionStart hook `~/.claude/hooks/codegraph-session-start.sh` (registered in `~/.claude/settings.json`, matcher `startup`) starts a detached `codegraph init --yes <git toplevel>` for any new session whose toplevel has no `.codegraph/codegraph.db`. `SB/<pkg>/repo` is a git repo (5.1 step 4), so the first reviewer session writes `.codegraph/` into the sandbox. `.codegraph/` is gitignored at all three base commits (`.gitignore:266`), and 13.5 cleanup removes only allowlisted caches, so the files persist. As a result every run's audit lists `sandbox_dirty`: `QUARANTINE`, `contaminated: true`, launcher exit 3, and every row is dropped from the quality means and counted as a rule-5 violation. The 13.5 step 3 "status is empty" check also never passes. This is not a reviewer write. The REQ check (R-09, REQ:1018, :1044) is plain `git status`. A reviewer `uv run` (`.venv/`) would trip the same check. | The legacy reviewer sandbox `/tmp/evalsb/repo` holds `!! .codegraph/.gitignore`, `!! .codegraph/codegraph.db` (136 MB), `!! .codegraph/daemon.log` and 2,579 `.venv/` entries under exactly this status command. `~/.local/state/superclaude/codegraph-init.log:2666-2681` shows `Initialized in /tmp/evalsb/repo` and repeated racing inits. DESIGN.md has no mention of codegraph or `SUPERCLAUDE_CODEGRAPH_AUTOINIT`. | Export `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` for every reviewer and judge session. This is an environment setting, identical in A1 and A3, so the command line does not change; state it in 5.2 and 12. Base the violation on R-09's `git status --porcelain --untracked-files=all` (tracked and non-ignored files), and log ignored-file writes as descriptive `ignored_writes`. Make 5.1 reuse, 13.5 step 3 and AC-15 use the same rule. Add a G0 check that runs one real session in a fresh sandbox and lists every file that appears. |

Notes (minor, not blocking):

| # | DESIGN.md line | Note |
|---|---|---|
| m1 | :125, AC-11 (:882) | These say "one row per non-smoke launch" goes to `results.jsonl`, but Spike-4 rows go to `spikes/spike4/rows.jsonl` (:60, :597). Say "non-smoke, non-Spike-4". |
| m2 | 13.1 exit codes (:708) | A `--no-judge` (Spike-4) run is "not judged", so it always exits 2. Give `--no-judge` runs exit 0 when every package is valid. |
| m3 | 13.5 (:736-737) | Step 1 queues subagent files, but step 2 deletes only paths ending in `/<uuid>.jsonl`, so subagent `agent-*.jsonl` files are never deleted. This is safe but contradicts step 1. |
| m4 | 9.5 (:559) | Killed-attempt recovery matches on "first user message equals the rendered brief" within `[t_start, t_end]`. All three reviewers of a package get the identical brief at T0, and a second run on the same sandbox has the same brief, so this over-captures peers' and other runs' sessions and can cause false cross-run contamination. Also match on the model and run window. Whether a `/sc:spec-panel ...` prompt is stored verbatim as the first user message is unverified (the fake in F14b stores it verbatim). |
| m5 | :549 vs :155 | The forbidden pattern `/.claude/projects/` is literal, but tests point `R3_CLAUDE_PROJECTS` at a pytest temp dir. F14b(a) passes only if the audit pattern uses the configured root or the temp root ends in `.claude/projects`. |
| m6 | 15.3 F8 (:831) | The fake sleeps 60 s and the hang guard fires at 1.5 x 40 = 60 s, so the kill wins only by the fake's start-up margin. Use `sleep_s` 120. |
| m7 | `test_msg` (:808) vs 6.7 (:415) | "1,800 characters" vs "1,800 bytes". |
| m8 | 2.2 tree | `reviews/sessions/<id>/` (9.5) and `runs/<run_id>/cleanup.json` (13.5) are missing from the tree. |
| m9 | AC-14 (:885) | 627 EVAL files changed on 2026-11-13 (latest 15:55 UTC) through other work. A concurrent EVAL write during the smoke run fails AC-14 for reasons unrelated to R3. Record the window or exclude paths written by others. |

## What I checked

- Read review 1 in full and DESIGN.md in full (lines 1-950). Read REQ:255-282 (kill switch, timing table) and the R-05, R-09, R-28, R-43 and R-46 rows.
- Re-read the cited code: `/usr/local/bin/claude:1-11`; RR:1-87 (line 48 runs under `timeout 3000` with `--no-session-persistence`); `judge-one.sh:1-31` (:7 skip, :21 schema, :25 `timeout 900 claude -p --model claude-opus-5-5`); `ledger.py:408-494`; `merge_cmd.py:60-99`.
- Recomputed the numbers: EL2 126.6, 147.6 (+27.2%), 141.2, 150.8, 174; SL2 B 273.7 (821/3) → 355.8, 410.6, box 82.1, 305.3, 335.7, edges 19.0 and 38.0; HL2 309.4, 357, 269.6, 290, edge 32.7; `test_n` (132.0 → 1, 132.01 → 0, 7.3 → 1, fallback 118 → 1, ember 3, sonnet 2 and 1, haiku 1 and 0); admission 7/8 and 3/4 edges.
- Checked the residue strings against the three candidates (no hits).
- Checked the sandbox side effects of the host's hooks: the `~/.claude/settings.json` SessionStart list, `codegraph-session-start.sh`, `.codegraph/` ignored at all three bases, and the legacy `/tmp/evalsb/repo` strict status and init log (evidence for N1).
- Checked EVAL modification times (for m9).
- Not done: I ran no test and no model, did not open ground-truth descriptions or plan quotes, and edited no file except this report.
