cac0f6915072cd2936a43e34329b3995b96f7f15
Review one task for spec compliance.

Task brief: T10 (source: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/DESIGN.md; the orchestrator's finish instruction quoted in .dev/implement/collab-r1-move-radar/tasks.md). The orchestrator deliverable: rewrite .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/IMPLEMENTATION.md so it is true.
T10.AC1: IMPLEMENTATION.md states what was built (file list); how to run one panel on all three packages (an exact command for each of ember + 2x luna, sonnet + 2x luna and haiku + 2x luna, plus PANEL_COLLAB=0); test results with counts; spike and smoke results; and every requirement or acceptance criterion that is not met, with the reason. Every statement in it must be true on disk (files exist, commands are exact and would be accepted by the scripts, counts match a run, results match the records).
Global constraints: Orchestrator constraints (global): create and edit files only under .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/ (plus .dev/implement/collab-r1-move-radar/ and scratch under /tmp/evalsb-collab-r1/ and /tmp/collab-r1/); do not edit src/, tests/, .claude/, .dev/tasks/, the 20261111-a1 eval folder or any other redesign's folder; do not stage, commit or push; python only through uv; models allowed muse-ember-1.0, gpt-6-luna, claude-haiku-5-5, claude-sonnet-5-5, grok-4.7, Opus only as the blind judge, never Qwen or glm; NOFALLBACK=1; no full panel runs; at most 3 reviewer or judge sessions at once.
Start sha: cac0f6915072cd2936a43e34329b3995b96f7f15
Diff against the start snapshot: diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/IMPLEMENTATION.md b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/IMPLEMENTATION.md
new file mode 100644
index 000000000..dbca8cbd7
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/IMPLEMENTATION.md
@@ -0,0 +1,157 @@
+# Redesign 1, Move Radar (F3): implementation report
+
+Source design: `DESIGN.md` in this folder. Status as of 2026-11-13 23:30 UTC, written after verifying the files, the test run and the
+spike records on disk (not copied from the first session's claims). Ledger: `.dev/implement/collab-r1-move-radar/progress.md`
+(T1-T10, evidence and reviewer notes in `.dev/implement/collab-r1-move-radar/retries/T<n>/`).
+
+Abbreviations: `REPO` = `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel`, `R1` = `REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar`,
+`DS` = `TASK-WF-designSpec-20261107-075614`, `AL` = `TASK-WF-makeTheAliasOnly-20261105-051649`, `DE` = `TASK-WF-design-20261108-041415`.
+
+## 1. Bottom line
+
+| What | State |
+|---|---|
+| Harness (hook, classifier, validator, runner, summary, anonymiser, results, alarms, launcher) | Built, 138 tests pass, lint clean |
+| Gate 0 | G-BASE pass, G-PINS pass, S0 pass, S2 pass, REQ-S3 recorded. **S3 missing, Spike 4 missing** (see section 7) |
+| Smoke | Collab-0 smoke row ran for real in R1: all 7 conditions hold. The real collab-1 smoke row could **not** run (the gate refuses it). A provisional collab-1 smoke ran in a scratch root and holds all 7 conditions; it is not a Gate 0 result |
+| Full rows (3 panels x collab 1 and 0) | Not run, as instructed (the orchestrator runs them). Collab-1 rows cannot start until Spike 4 and S3 are done |
+
+## 2. What was built (all under `R1/`)
+
+- `config/`: `panels.json` (three panels), `catalogue.json` + `catalogue.sha256` (frozen move texts), `brief.txt` (H1 brief). `manifest.json` (base commits and pins).
+- `tools/` (15 files): `launch.sh`, `sandbox.sh`, `radar-index.sh`, `radar-classify.jq`, `radar-hook.sh`, `settings-gen.sh`, `msg-validate.sh`,
+  `run-reviewer.sh`, `h2_normalize.py`, `values.py`, `collab_summary.py`, `anon.sh`, `results.py`, `alarms.py`, `cleanup-sessions.sh`.
+- `spikes/`: `g-base.sh`, `g-pins.sh`, `gate0-check.sh`, `spike4.sh`, `probe-hook.sh`, `s0-hooks.sh`, `s2-resume.sh`, `reqs3-actrate.sh`, records `s0/`, `s2/`, `reqs3/`,
+  `reqs3.json`, `g-cat.json`, `gate0.json`; `spikes/smoke/`: `smokecheck.sh` (decides the 7 conditions of 6.4), `s3-record.sh` (writes `spikes/s3.json` from the two real smoke rows),
+  `mkscratch.sh` (builds the provisional scratch root), the two check outputs and the saved evidence of the provisional collab-1 row (`provisional-c1/`).
+- `tests/`: `conftest.py`, fixtures, and 21 test modules (section 4).
+- Run data kept on disk: `index/` (3 per-package indexes), `runs/el2-c0-r0/` and `results/` (the collab-0 smoke row), `scoring/b808fb857780/` (its anonymised report and judge output),
+  `implement-report/` (the first session's logs), `design-report/`.
+- Not part of the harness but required by the work: the ledger folder `.dev/implement/collab-r1-move-radar/`.
+
+Files outside `R1/` that were written: only the ledger folder, scratch under `/tmp/collab-r1/` and `/tmp/evalsb-collab-r1/` (sandboxes, per-session working files, the scratch root), and the
+spike/smoke session transcripts that Claude itself keeps under `~/.claude/projects/` (their `.jsonl` files were deleted by id; see section 8, item 7).
+
+## 3. How to run one panel on all three packages
+
+Run from `REPO`. A launch runs DS, AL, DE one after another, three reviewer sessions at a time, then the judge (Opus). `<rep>` is a whole number; **0 is reserved for smoke rows** and is ignored by `alarms.py`.
+Use `nohup ... &` or the Bash tool's background mode. Exit code 0 = row written and every package ok, 1 = row written but a package is invalid, quarantined or judge_failed, 2 = refused before running.
+
+| Panel (reviewers) | Collab 1 (radar hook on) | `PANEL_COLLAB=0` (baseline, no hook, no `--settings`) |
+|---|---|---|
+| `el2`: ember (`muse-ember-1.0`) + 2x luna (`gpt-6-luna`) | `cd REPO && PANEL_COLLAB=1 bash .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh el2 <rep>` | `cd REPO && PANEL_COLLAB=0 bash .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh el2 <rep>` |
+| `sl2`: sonnet (`claude-sonnet-5-5`) + 2x luna | `cd REPO && PANEL_COLLAB=1 bash .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh sl2 <rep>` | `cd REPO && PANEL_COLLAB=0 bash .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh sl2 <rep>` |
+| `hl2`: haiku (`claude-haiku-5-5`) + 2x luna | `cd REPO && PANEL_COLLAB=1 bash .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh hl2 <rep>` | `cd REPO && PANEL_COLLAB=0 bash .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh hl2 <rep>` |
+
+One package only (smoke): append the package, for example `PANEL_COLLAB=1 bash .../tools/launch.sh el2 0 TASK-WF-designSpec-20261107-075614`.
+`NOFALLBACK` is unset or `1` (the launcher exports 1 and refuses any other value, including an empty one); `PANEL_COLLAB` must be `0` or `1` (default 1; empty or anything else is refused, exit 2).
+
+What a launch needs (it refuses, exit 2, naming the missing item):
+
+1. Pins in `manifest.json` match `config/catalogue.json`, `config/brief.txt` and `A1DIR/tools/tmp-scripts/judge-one.sh`; a base sha per package.
+2. `spikes/gate0.json` (run `bash R1/spikes/gate0-check.sh` first; the launcher reads the file, it does not refresh it): collab 0 needs G-BASE and G-PINS = pass; collab 1 also S0 and S2 = pass, and for `<rep>` of 1 or more S3 = pass.
+3. Collab 1 also needs `values/<panel>/<pkg>.json` + `.sha256` for every requested package (Spike 4). Collab 0 without values uses the planning values and a 2.0 x planning-B hang guard.
+4. `results/<row>.json` must not exist (a finished row is never re-run). A partly finished row resumes per package: a package with status `ok` is skipped, any other earlier attempt is moved aside to `runs/<row>/<pkg>.prev-<epoch>`.
+
+Order of work to unlock collab-1 rows (not done here):
+
+```bash
+cd /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
+R1=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar
+bash $R1/spikes/spike4.sh el2        # 3 collab-0 rows (reps 1 2 3, 9 reviewer sessions each), then writes values/el2/*.json; repeat for sl2, hl2
+bash $R1/spikes/gate0-check.sh
+PANEL_COLLAB=1 bash $R1/tools/launch.sh el2 0 TASK-WF-designSpec-20261107-075614   # the real collab-1 smoke (rep 0)
+bash $R1/spikes/smoke/s3-record.sh   # writes spikes/s3.json only when both smoke rows (el2-c1-r0, el2-c0-r0) exist; pass only if all 7 conditions hold in both
+bash $R1/spikes/gate0-check.sh
+```
+
+Arm-level alarms over many rows: `uv run python $R1/tools/alarms.py <panel>` (reads `results/results.jsonl`, prints convergence, SLO, drift and snapshot alarms per arm).
+
+## 4. Test results
+
+`uv run pytest .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests -q -rs -p no:cacheprovider` from `REPO`, final run 2026-11-13 23:22 UTC:
+**138 passed, 0 skipped, 0 failed, exit 0, 41.7 s**. `uv run ruff check` on the folder: all checks passed. `bash -n` on every shell script: clean.
+
+| Module | Tests | Covers (DESIGN.md 6.1 / 6.2) |
+|---|---|---|
+| `test_catalogue.py` | 5 | T-1 |
+| `test_index.py` | 1 | T-2 |
+| `test_classify.py` | 23 | T-3 |
+| `test_order.py` | 2 | T-4 |
+| `test_hook_schedule.py` | 8 | T-5 |
+| `test_hook_finish.py` | 1 | T-6 |
+| `test_hook_seal.py` | 2 | T-7 |
+| `test_hook_errors.py` | 6 | T-8 |
+| `test_validate.py` | 16 | T-9 |
+| `test_settings_and_cmd.py` + `test_launch.py` (gate order) | 4 + 12 | T-10, kill switch, F-4, F-5, F-10, F-11, F-12 launch parts |
+| `test_h2.py` | 13 | T-11 |
+| `test_values.py` | 13 | T-12 |
+| `test_runner_retry.py` | 3 | T-13 |
+| `test_anon.py` | 1 | T-14 |
+| `test_judge_path.py` | 1 | T-15 |
+| `test_results.py` | 2 | T-16 |
+| `test_collab_summary.py` | 9 | T-17 |
+| `test_alarms.py` | 4 | T-18, F-2 |
+| `test_cleanup.py` | 1 | T-19 |
+| `test_faults.py` | 11 | F-1, F-3, F-4, F-6, F-7, F-8, F-9, F-10, F-13, F-14 (F-5, F-11, F-12 are in `test_launch.py`) |
+
+Every one of T-1..T-19 and F-1..F-14 has at least one collected test with real asserts (checked by a fresh reviewer under T7). No test calls the gateway; tests use stub `claude` and `superclaude`
+executables. `spikes/smoke/s3-record.sh` has no pytest; it was exercised by hand (section 6).
+
+## 5. Spike results (Gate 0), 2026-11-13
+
+Current `spikes/gate0.json`, decided by `spikes/gate0-check.sh`: G-BASE **pass**, G-PINS **pass**, S0 **pass**, S2 **pass**, REQ-S3 **recorded**, S3 **missing**, Spike 4 **missing**.
+
+- **G-BASE / G-PINS** (reused from the first session, re-decided by `gate0-check.sh` against freshly built sandboxes for all three packages): base commits are the first parents of the squash commits (`method: squash-first-parent` in `manifest.json`), the three pins match the live files, the catalogue has 0 ground-truth hits (`spikes/g-cat.json`).
+- **S0** (4 models, one probe session each; `spikes/s0/<model>.json`): pass for muse-ember-1.0, gpt-6-luna, claude-sonnet-5-5, claude-haiku-5-5. Hook stdin carries `tool_name`, `tool_input`, `transcript_path` on every call (5 calls each);
+  the subagent's Bash call reaches the hook **with** `agent_id` on all four; the snapshot is written and hashed; a handler sleeping past its 1 s timeout shows as `hook_cancelled` and the session still ends `success`; the injected `PROBE-CONTEXT-n` text is in the transcript for all four and all four models repeated it;
+  no other PostToolUse additionalContext entry appeared (0). `hook_ms_p95` 20-22 ms. The user settings hold PostToolUse hooks (they fire in both arms); the sandbox settings hold only PreToolUse.
+- **S2** (4 models; `spikes/s2/<model>.json`): pass. `--resume <session_id>` answered the random code word in the same session, the stream's `result` event parsed with `jq -s`; resume first event 1.0-1.1 s, resume wall 3.6-4.9 s (planning value 6 s).
+- **REQ-S3** (recorded, not gated; 3 sessions per model with the real A1 brief on DS; `spikes/reqs3.json`, `spikes/reqs3/<model>.json`):
+
+| Model | Item act rate (call right after the injection) | Item act within the session | Finish act rate |
+|---|---|---|---|
+| muse-ember-1.0 | 1.00 | 1.00 | 0.33 |
+| gpt-6-luna | 0.33 | 1.00 | 1.00 |
+| claude-sonnet-5-5 | 1.00 | 1.00 | 1.00 |
+| claude-haiku-5-5 | 0.00 | 0.33 | 1.00 |
+
+  Limits of these numbers: "next call" is the next call that reached the hook; when a model issues parallel tool calls the injection can only be seen at the next assistant turn, so the next-call rate under-counts luna and haiku (a reviewer's next-turn reading gave luna 1.0, haiku 0.33). A session that simply ends at call 8 counts as having obeyed "finish now" (`session_ended_at_finish_call` is recorded; all six sonnet and haiku sessions did end at call 8). Three sessions per model is a screen, not a measurement. Cap respected: at most 3 concurrent model sessions.
+
+## 6. Smoke results
+
+- **Collab 0, real, row `el2-c0-r0`, package DS** (`runs/el2-c0-r0/`, `results/el2-c0-r0.json`, `spikes/smoke/check-el2-c0-r0.tsv`): all 7 conditions of 6.4 hold. Models ember + 2x luna all `model_ok`; `dropped_lines` 0 (one ember re-ask, 5.5 s); no `settings/`, no `msgs/`, no `--settings` in any argv; merge rc 0 and the three reviewer ids are in the merged report; `anon_leak` 0, judge `score.json` parsed (covered 0 of the GT items, 0 wrong blockers: a plain baseline value for one sample);
+  `results` row has the 5.4 shape (`incomplete`, as expected for one package); sandbox `git status` empty, candidate sha unchanged, the 3 recorded session files deleted. Elapsed 107.1 s, 21,127 output tokens, 0 injections.
+- **Collab 1, real**: `PANEL_COLLAB=1 bash tools/launch.sh el2 0 DS` was run and **refused (exit 2)**: `PANEL_COLLAB=1 needs values/el2/<DS>.json with a matching .sha256 (Spike 4)`. This is the gate working; nothing ran.
+- **Collab 1, provisional, scratch root** (`/tmp/collab-r1/r1scratch`, built by `spikes/smoke/mkscratch.sh` with the planning values and a hand-written gate file; evidence copied to `spikes/smoke/provisional-c1/`, checks in `spikes/smoke/check-provisional-el2-c1-r0.tsv`): all 7 conditions hold.
+  The hook fired for all three reviewers (10, 9 and 8 calls), 4 injections: ember M2 at call 6 and M7 at call 10 (both observable moves, neither executed afterwards), the two lunas M3 and M8 at call 8; all before the guard (last at 56.2 s, guard 109.6 s); each reviewer's seal event precedes its first inject event (equal millisecond, order shown by the event order in `board/metrics`);
+  0 leak violations, 0 `task_hint` keys in `msgs/radar.jsonl`, hook p95 105-139 ms per call, elapsed 92.0 s, judge covered GT3 and GT7. One sample with planning values: not usable as a result, and **not a Gate 0 pass**.
+- `spikes/smoke/s3-record.sh` refuses (exit 1, writes no file) while the real `el2-c1-r0` row is missing; run against a test root that links the real collab-0 row and the provisional collab-1 row it returns pass (output to `/tmp` only), so the mechanism works.
+- Isolation: the hash of the `A1DIR` file listing (path + mtime) is identical before and after the smoke rows; nothing under `A1DIR` is newer than `R1/manifest.json`; no `fallback.log` anywhere under `R1/runs`.
+
+## 7. Requirements and acceptance criteria that are NOT met, and why
+
+| Item | Not met | Reason |
+|---|---|---|
+| AC-2 Gate 0 | Spike 4 and S3 are not `pass` | Spike 4 = 3 full collab-0 rows per panel (27 reviewer sessions per panel plus judges); the orchestrator forbids full panel runs here. S3 needs the real collab-1 smoke row, which needs the Spike 4 values file |
+| AC-3 Smoke | No real collab-1 smoke row exists in R1 | Blocked by the previous line. The collab-0 row passes all 7; collab 1 passes all 7 only in the provisional scratch-root row, which is a stand-in |
+| AC-5 Isolation (literal text) | "`git status --porcelain` in REPO shows changes only under R1/" is false in this shared worktree | Thousands of untracked entries from other sessions (other redesigns, brainstorms, earlier batches) exist outside R1/. Nothing attributable to this work was found outside `R1/`, the ledger folder, `/tmp/collab-r1` and `/tmp/evalsb-collab-r1`; the `A1DIR` half holds |
+| AC-6 Each panel runs | No full row (3 packages) for el2, sl2, hl2 with collab 1 or collab 0 | Full panel runs are the orchestrator's job; collab 1 additionally needs Spike 4 |
+| AC-7, AC-8 on full rows | Not checked on AC-6 rows (none exist) | They hold on the two smoke rows: audits clean, `model_ok` true on all six reviewer runs, no `fallback.log` |
+| REQ-S3 | Rates are screens only | 3 sessions per model; next-call versus next-turn limit (section 5) |
+| T8 task text "spikes run under the gateway lock" | No gateway lock exists in the design or the repo | Read as the orchestrator's cap of 3 concurrent model sessions, NOFALLBACK=1 and allowed models only |
+
+AC-1 (tests) and AC-4 (kill switch) are met.
+
+## 8. Deviations from DESIGN.md, and known limits (all recorded in the reviewers' notes files)
+
+1. `launch.sh` checks the Spike 4 gate through the per-panel values files, and does not read the `Spike 4` entry of `gate0.json`; the S0/S2/S3 entries it does read. It has four test-only options (`--root`, `--sb`, `--a1`, `--prebuilt`); defaults are the production paths.
+2. Resume keeps non-ok attempts as `runs/<row>/<pkg>.prev-<epoch>` and re-runs them (the design says only "a package with score.json reached is skipped"). `cleanup-sessions.sh` does not look into `.prev-*` folders, so session files of a kept-aside attempt are left under `~/.claude/projects` (orphans only).
+3. S0 passes only when the injected context also reached the session transcript and the observed model equals the expected one (stricter than the design's list). The check that no other PostToolUse hook adds context is recorded (`other_hook_additional_context_entries`) but is not part of `pass`.
+4. `alarms.py` takes B_c as the median over all collab-0 rows of the panel (the design allows either reading); `baseline_drift` uses the same-rep collab-0 row. A collab-1 or collab-0 row that is not complete contributes no `ledger_rows` to the convergence rule.
+5. The `results` object `hook_ms_p95` is the worst package p95, not a sum; packages that were not run carry status `not_run` (outside the four-value list of 5.4; the row is `incomplete`).
+6. `collab_summary.py` skips the 12-character ground-truth audit silently if `ground-truth.json` is missing (default paths exist).
+7. Session cleanup deletes only the recorded `.jsonl` session files, never directories (R-46); empty-ish per-session subfolders (`subagents/`, `tool-results/`, about 3.6 MB for the DS sandbox project folder in total) from the spike sessions remain under `~/.claude/projects/-tmp-evalsb-collab-r1-*`.
+8. Test code written for T7/T8/T9 has these recorded minors: F-3 recounts slots instead of reading the results counter; F-13 breaks `ctx/index.json` instead of making the hook exit 1; the F-5 test asserts only the ALARM line; `spikes/s0-hooks.sh` does not put `other_hook_additional_context_entries` into `pass`.
+9. The retry ladder was used once (T4): its advisers ran on `claude-opus-5-5` because no verified GPT T1 spawn path exists on this install (`family-fallback` header in `.dev/implement/collab-r1-move-radar/retries/T4/advice-3-b.md`).
+10. Reviewer count of minors/notes recorded per task (informational, nothing asked of the owner): T1 2, T4 6 (5 superseded), T5 6, T6 3, T7 4, T8 3, T9 6; T2, T3, T10 none. They are in `.dev/implement/collab-r1-move-radar/retries/T<n>/notes.md`.

Codegraph context: index_state: fresh; checked_at: 2026-11-13T22:17:42Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel; projectPath: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel. call codegraph only when index_state: fresh, never to widen scope. Q2b dependents: none outside the diff (shell, markdown and untracked test files are not indexed; Grep floor used).
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): Facts the reviewer should check against disk, not trust: the file list in section 2; the test counts in section 4 (run uv run pytest <R1>/tests -q --collect-only -q, do not start model sessions); the spike numbers in section 5 against .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/{s0,s2,reqs3}/*.json and .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/reqs3.json; the smoke numbers in section 6 against .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/runs/el2-c0-r0, .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/results/el2-c0-r0.json, .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/smoke/ ; the commands in section 3 against .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh (argument order, options, refusal conditions) and .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/spike4.sh and .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/smoke/s3-record.sh; the deviations in section 8 against the code. Check that every requirement the design lists in sections 6.3-6.5 that is not met is named in section 7.


Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.