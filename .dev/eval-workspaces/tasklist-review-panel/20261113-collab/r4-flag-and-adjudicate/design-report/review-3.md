# Review 3: Redesign 4 Flag-and-Adjudicate DESIGN.md

## Scope checked

- `DESIGN.md` read in full (lines 1-574) in three pieces of at most 200 lines.
- `review-2.md` read in full (N-1, N-2, m-1..m-13).
- Code: `EVAL/tools/run-reviewer.sh` (`RR`) lines 1-87; `EVAL/tools/tmp-scripts/judge-one.sh` (all). sha256 of `judge-one.sh`, `findings.py` and `ledger.py` recomputed: all three equal the AC-03 pins.
- Source of truth `REQ`: grep of R-01, R-05, R-09 and section 5.5 (lines 255-258, 1005-1018, 1041-1044).
- Host checks (read only):
  - `/usr/local/bin/claude` (10-line `sh` wrapper).
  - `~/.local/bin/ccsession-orca` (the `-p` handling, lines 20-40, 90-110 and 160-190).
  - `ps -eo pid,args`, and `pgrep -fa '(^|/)claude -p( |$)'`.
  - `CCSESSION_LAUNCH_ID` in the current environment.
- Past reviewer outputs: the tool calls in 19 `EVAL/TASK-WF-*/reviews/*.attempt1.json` files.
- The five 2.10 content markers grepped in the three candidates, the three `source.md` files, `~/.claude/rules` and the `sc-spec-panel*` skills: 0 hits.
- Ground-truth files: only line counts and the number of lines without a marker were taken (`wc -l`, `grep -cv`). No content was read.
- Recomputed:
  - k at every `test_values.py` vector in integer ms.
  - Section 3 thresholds (19.4 s, 51.795 s, 81.3 s).
  - PANEL_FINISH_AT offsets (143.8, 341.5, 275.3 s) and hang guards (174, 410.6, 357 s).
  - Fisher one-sided p for 0 vs 4, 1 vs 6 and 2 vs 7 of 12: 0.0466, 0.0343 and 0.0447, which round to the stated 0.047 / 0.034 / 0.045.
  - The SLO vector (3/36 = 1/12 is not above the limit; 4/36 is).
- All of these are correct.
- Interfaces cross-checked:
  - The `r4-hook` and `bin/card` arguments in 1.2 against the settings and wrapper text in 5.1 step 2.1.
  - The `panel.json` fields.
  - The step cross-references in 2.2, 2.3, 2.6 and 5.1.

## Review-2 blocking findings status

| Id | Status | DESIGN.md text and evidence |
|---|---|---|
| N-1 concurrency pattern never matches | **FIXED** (minor residual m3-1) | 5.1 step 0: "count model sessions host-wide with `pgrep -fc '(^|/)claude -p( |$)'` and ember sessions with `pgrep -fc '(^|/)claude -p --model muse-ember-1.0( |$)'`". The live `-p` process on this host is `278422 /opt/nvm/versions/node/v24.22.2/bin/claude -p --model claude-opus-5-5 ...`, and `pgrep -fa` with the new pattern returns exactly that PID (count=1). Its parent `278419 timeout 3600 claude -p ...` is not matched. The S0 failure action no longer stops F7: "A wrong concurrency count or an extra `--settings` is a harness fix (adjust the pattern, or call the real binary), not a model failure" (6.3). |
| N-2 ground truth reachable by concurrent reviewers | **PARTLY** | **Fixed:** `STAGE` is now deleted on every exit path: "`STAGE` is deleted by a `trap` set right after `mktemp` ... removed on success, on failure and on a signal" (5.1 step 5.6). A content layer was added: "tool results ... must not contain ... `"blocking_in_implement"`, `"plan_quote"`, `"gt_covered_any"`, `"wrong_blockers"`, nor ... `"panel-msg/1"`" (2.10). **Still open (graded blocking, see N3-3):** 2.10 claims the content layer "catches any route, relative paths and recursive searches included". That is false for the ground-truth files. The `EVAL` ground truth is pretty-printed, so most lines carry no marker: 188 of 207, 97 of 104 and 44 of 48 lines contain neither `plan_quote` nor `blocking_in_implement`. A `cd / && grep -rn <word> home` call (no `/home/`, no `~/`) returns description lines that the content layer does not flag. |

## Review-1 fixes spot check

| Id | Still intact | Quoted line |
|---|---|---|
| B-1 | yes | Decision 6: "The staging directory is **not** under `SBR` and is deleted as soon as its results are copied back". |
| B-2 | yes | 2.6 step 5: "`<rid>.final.md` is always written. If the last attempt has no findings block, it is a copy of `<rid>.md`". |
| B-3 | yes | 5.1 step 0: "append `{"row":...,"time":...,"reason":...}` to `runs/refusals.jsonl`, never creating or touching `runs/<row>/`". |
| B-4 | yes | 2.7: "computed in integer milliseconds ... SL2 gives k = 1 at T_report_p90 = 51.795 s and k = 0 at 51.8 s". Rechecked: 95795 - 2000 - 14000 - 51795 = 28000, and 28000 / 28000 = 1; 27995 gives 0. |
| B-5 | yes | 2.7: "A turn's duration is the **last** entry's `timestamp` in the group minus the `timestamp` of the last entry before the group". |
| B-6 | yes | 5.1 step 4: "`[panel card cN]`, `panel card cN`, `card cN: passed` and every other `card cN` (all case-insensitive, `\bcards? c[0-9]+\b`) are deleted". The 2.10 grep list keeps `panel card` and `\bcards? c[0-9]+\b`. |

## New blocking findings

### N3-1. The new path rule flags the brief's own required read, so almost every row (A1 included) is quarantined

- **DESIGN.md location:**
  - 2.10, row "Reviewers never see ground truth": "a tool call naming `ground-truth`, `judge.json`, `score.json`, `/tmp/jdg.`, `/home/`, `~/`, `$HOME`, `.claude/projects` ... is a violation".
  - 1.1 `frozen/brief-a1.txt`: "The 'First-review rules' paragraph (the grading text) stays byte-identical to `RR:17`".
- **Evidence:**
  - `RR:17`: "First-review rules (from ~/.claude/rules/prompts/document_review_loop_prompts.md, read it first)". The file exists at `/home/coder/.claude/rules/prompts/document_review_loop_prompts.md`.
  - 16 of 19 past `EVAL/TASK-WF-*/reviews/*.attempt1.json` files contain `/home/coder/.claude/` in their tool calls. Example: `TASK-WF-design-20261108-041415/reviews/t1b-1.attempt1.json` has `Read {"file_path":"/home/coder/.claude/rules/prompts/document_review_loop_prompts.md"}`. The Read tool takes absolute paths, so following the brief always names `/home/`.
  - The brief also opens with `/sc:spec-panel`, whose command and skill files live under `~/.claude/`. The candidates edit installed primitives, so reviewers also have a normal reason to read `~/.claude/skills/...`.
- **Why it matters:**
  - In both arms, nearly every reviewer that obeys the brief is a "violation". 5.1 step 3 then sets `audit_ok: false` and writes `QUARANTINED`.
  - 2.9 `independence` ("zero audit violations: every row `audit_ok: true`") fails for every arm.
  - AC-12 ("`audit_ok: true`"), AC-13, AC-11 and the 6.4 smoke test ("`audit_ok: true`") cannot pass.
  - The audit becomes noise, so a real ground-truth read cannot be told apart from it.
- **Suggested fix:**
  - Drop the blanket `/home/`, `~/` and `$HOME` patterns.
  - Keep `.claude/projects`, and add an allow-list for read-only access under `~/.claude/rules/`, `~/.claude/skills/`, `~/.claude/commands/`, `~/.claude/agents/` and the core `~/.claude/*.md` files.
  - Flag the real targets by name instead: the absolute `REPO` and `EVAL` prefixes (also after `~` expansion), `workspaces/`, `ground-truth`, `judge.json`, `score.json`, `jdg.`.
  - Add one test-plan case: a fixture transcript that reads `/home/coder/.claude/rules/prompts/document_review_loop_prompts.md` gives no violation.

### N3-2. The fallback for a killed reviewer's transcript picks another reviewer's file

- **DESIGN.md location:** 2.6 step 4: "when the result JSON has no `session_id` because the process was killed, take the newest `*.jsonl` under the sandbox's project directory created after `t_start_ms`".
- **Evidence:**
  - The cwd is `SBR/sb/<pkg>/repo` for every reviewer of a package (2.6 step 2; layout 1.5 `sb/<pkg>/repo/`). The three reviewers of a package start together (5.1 step 2.3, "within 2 s of each other", `test_launcher.py`).
  - Concurrent rows reuse the same per-package sandbox (2.10: "rows of other launchers that overlapped in time on the same sandbox are listed"; 5.1 step 0: "Three panels launched together").
  - Claude Code keys the project directory by cwd, so 3 to 9 live sessions write into one directory, and all of them were created after `t_start_ms`.
- **Why it matters:**
  - A hang-killed reviewer (an expected event, R-43) gets a peer's transcript. Its timing is then wrong, and that includes the Spike 4 turn and T_report statistics if a Spike 4 row has a kill.
  - Its audit is wrong too. A luna given the flagger's transcript "names the board directory" (the flagger's `bin/card` lives under `SBR/board/...`), so the row is falsely quarantined. A real violation in the killed session goes unseen.
  - m-6's fix introduced this.
- **Suggested fix (smallest):**
  - Give each launch a known id: `reviewer.sh` generates a UUID and passes `--session-id <uuid>`. List this as an allowed argv difference in section 4 and `test_reviewer.py`.
  - Alternatively, take `session_id` from the first hook input (collaboration runs only) and record `transcript_missing` for A1 kills.
  - Either way, never pick by recency.

### N3-3. N-2 residual: the content layer is claimed to catch recursive searches but does not

- **DESIGN.md location:** 2.10: "**Content (catches any route, relative paths and recursive searches included):**" followed by the five key markers.
- **Evidence:**
  - The ground-truth files are pretty-printed. 188/207, 97/104 and 44/48 lines contain neither marker (line counts only, no content read).
  - A recursive grep such as `cd / && grep -rn <word> home` names none of the 2.10 path patterns. With N3-1 fixed as suggested, even a `~/` form names none.
  - Its result lines carry the file name `.../ground-truth.json:` and the description text, but no marker key.
  - The test plan expects a violation for "one running `grep -r x /tmp`" (6.2 "Ground-truth access"). Under 2.10, any other `/tmp` path "is listed as `tmp_other` (descriptive)", so the spec and the test disagree.
- **Why it matters:**
  - This is a harness-created route to ground truth (check g). AC-13 would report it clean, and the design states a guarantee it does not have.
- **Suggested fix:**
  - Add file-name markers to the content layer: `ground-truth.json`, `judge.json`, `score.json`, `jdg.`. `grep -r` prints file names, and `cat` must name the path in the call.
  - Add the ground-truth `description` strings (the audit already reads ground truth after the row).
  - Classify a recursive search (`grep -r`, `rg`, `find`, `ls -R`) rooted at `/`, `/tmp`, `/home`, `~` or an ancestor of `SBR` as a violation. That makes the 6.2 test consistent.
  - Or delete the "catches any route" claim and list the gap as a risk.

## Minor findings

### m3-1. The N-1 pattern depends on the launch environment

- **Location:** 5.1 step 0: "On this host `/usr/local/bin/claude` is a wrapper that `exec`s the real binary by its full path".
- **Evidence:**
  - The wrapper `exec`s the real binary only when `CCSESSION_LAUNCH_ID` is set (`/usr/local/bin/claude:6`). It is set when the launcher runs from a Claude session's shell; here it is `85890.1401232509`.
  - Otherwise the wrapper goes through `ccsession-orca` (line 8). Sessions started that way show as `/opt/nvm/.../bin/claude --dangerously-skip-permissions --allowedTools=Grep --settings {...} ...` (for example PID 37433). There, `-p` would not follow `/claude`, and the argv would differ from `RR:48`.
  - S0 catches this, so it is not blocking.
- **Fix:** Have `reviewer.sh` call the real binary path, or refuse when `CCSESSION_LAUNCH_ID` is unset. Record which in `run.json`.

### m3-2. Model list still disagrees

- **Location:** Decision 5: "(ember, luna, haiku, sonnet; Opus only as the judge)". 1.1 `allowed_models` and AC-05 include `grok-4.7` (review-2 m-10).
- **Fix:** Remove grok, or amend decision 5.

### m3-3. A bare "panel card" still fails the package

- **Location:** 5.1 step 4. A bare "panel card" (no id) in a luna finding still hits the forbidden grep (`panel card`) and makes the package `anon_failed`.
- **Why:** This drops F7 packages only, the same bias m-13 fixed for "peer reviewer".
- **Fix:** Rewrite or delete the bare phrase too, and count the rewrites.

### m3-4. `uv run` without `--frozen` in decision 4

- **Location:** Decision 4 still says "`uv run --project REPO python <file>`" without `--frozen`. Section 1 and 5.1 now use `--frozen` (review-2 m-2 residual).

### m3-5. SLO budget baseline differs

- **Location:** Open question 5: "may exceed 1.35 B_A1". 2.9 uses "1.35 B_c(pkg)".
- **Fix:** Use one baseline.

### m3-6. Judge sessions are not gated by the concurrency lock

- **Location:** 5.1 step 0, "plus any judge sessions". The lock admits reviewers up to 10 sessions, and judges of other rows then start ungated, so the `REQ` 4 limit of 10 can be exceeded.
- **Fix:** Take `launch.lock` and apply the same count in `judge.sh`.

### m3-7. Risk numbering out of order

- **Location:** 7.1 lists risk 16 before risk 15.

### m3-8. Results row omits two audit fields

- **Location:** 5.2 `audit` omits `tmp_other` and `ignored_only`, which 2.10 and 5.1 step 3 produce.

## Verdict

- N-1: fixed. N-2: partly fixed (residual N3-3).
- All six review-1 fixes are intact.
- Three blocking findings:
  - N3-1: the new `/home/` and `~/` audit patterns flag the brief's own required read in 16 of 19 historical reviewer runs, so every arm fails `independence`, AC-12 and the smoke test.
  - N3-2: the killed-reviewer transcript fallback picks another session's file in a shared cwd.
  - N3-3: the content audit's "catches any route" claim is false for the pretty-printed ground truth, and the 6.2 `/tmp` test contradicts 2.10.
- Eight minor findings (m3-1 to m3-8).
- Arithmetic, test vectors, pins, interfaces and cross-references check out.

verdict: FAIL
