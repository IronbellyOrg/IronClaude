d35875e71c4b7be86a428ee3673a3c63a115b305
Review one task for spec compliance.

Task brief: ## Task 3: Redirect the Reopening notices in ccsession-orca and record which tests now fail

Depends on: Task 2

Edit `src/superclaude/skills/ccsession-tag/ccsession-orca`: add `>&2` to the two `echo` lines at 185 (`Reopening this tab's session '$name'`) and 188 (`Reopening this tab's session ${session:0:8}`). These are reachable only when stdin and stdout are terminals and `ORCA_PANE_KEY` is set; the change keeps every `[ccsession]` status line on one stream. Lines 136 and 211 already use `>&2`.

Then run `uv run pytest tests/unit/test_ccsession_tag.py tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider` with only the source edits of Tasks 2 and 3 applied.

Acceptance criteria:
- `bash -n src/superclaude/skills/ccsession-tag/ccsession-orca` exits 0, and `grep -n 'echo "\[ccsession\]' src/superclaude/skills/ccsession-tag/ccsession-orca | grep -v '>&2'` prints nothing.
- The set of failing tests in that run is recorded in `./artifacts/t3-expected-failures.log` and is exactly these six: `test_shim_is_detected_without_lsof`, `test_label_with_missing_transcript_starts_new_session`, `test_default_tier_sets_model_and_tier_window`, `test_a_busy_shim_is_never_stopped_by_a_new_launch`, `test_upgraded_code_starts_a_new_shim_and_keeps_the_old` and `test_model_outside_tier_mode_stays_where_it_was_typed` (the two shim tests may be skipped instead of failing on a machine without a usable shim, and the new replay test must pass). A different failing set means a stdout reader was missed; read that test and handle it in Task 4 or Task 5 before going on.

AC ids:
T3.AC1: `bash -n src/superclaude/skills/ccsession-tag/ccsession-orca` exits 0, and `grep -n 'echo "\[ccsession\]' src/superclaude/skills/ccsession-tag/ccsession-orca | grep -v '>&2'` prints nothing.
T3.AC2: The set of failing tests in that run is recorded in `./artifacts/t3-expected-failures.log` and is exactly these six: `test_shim_is_detected_without_lsof`, `test_label_with_missing_transcript_starts_new_session`, `test_default_tier_sets_model_and_tier_window`, `test_a_busy_shim_is_never_stopped_by_a_new_launch`, `test_upgraded_code_starts_a_new_shim_and_keeps_the_old` and `test_model_outside_tier_mode_stays_where_it_was_typed` (the two shim tests may be skipped instead of failing on a machine without a usable shim, and the new replay test must pass). A different failing set means a stdout reader was missed; read that test and handle it in Task 4 or Task 5 before going on.

(Repository root: /home/coder/workspaces/worktrees/IronClaude/ic-issue-389. The task's own evidence files `./artifacts/...` live in /home/coder/workspaces/worktrees/IronClaude/ic-issue-389/.dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/ .)
Global constraints: - Scope is the launcher scripts `src/superclaude/skills/ccsession-tag/ccsession` and `src/superclaude/skills/ccsession-tag/ccsession-orca`, the tests that read their output, `CHANGELOG.md` and the skill `README.md`. `src/superclaude/skills/ccsession-tag/models.py` is not edited: its two `[ccsession]` notes (line 313 `model list updated`, line 837 `model data check`) are routed to standard error at their one call site in `ccsession` (line 1733), so the documented `ccsession --refresh-models` report keeps printing on standard output.
- `src/superclaude/cli/eval/commands.py` (the version probe and `_parse_version`) is not edited. Hardening it (treat a non-zero exit code as "not callable", prefer the `X.Y.Z (Claude Code)` form) is a separate pending decision and must not be added here. Its failure-path behavior (stdout empty because the launcher exited early) is deliberately not pinned by any test in this plan.
- These stay on standard output because the shell captures them: every `models.py` print captured with `$(...)` in `ccsession` (the `PROFILE_*=` lines, digests, shim port, tier lists, compact settings, the `models` and `status` reports), and the values printed by `ccsession --ask`, `--auto-name`, `--list`, `--rm`, `--refresh-models` and `--models-status`.
- Existing `>&2` warnings and errors (`ccsession` lines 823, 944, 973, 980, 1002, 1013, 1080, 1856; `ccsession-orca` lines 136, 211) are correct and stay as they are.
- Edit only under `src/superclaude/skills/ccsession-tag/`, `tests/` and `CHANGELOG.md`. Do not edit `.claude/` mirrors by hand; `make sync-dev` is the only way they change and they are never staged.
- Hardening closure for this fix: the replay run recorded in Task 2 is the positive witness (the negative witness was run before this plan on the unfixed tree), Task 8 supplies the parser fixtures, and the executor's final independent review is the off-path review.
- Evidence the tasks name (logs, outputs) is written under `./artifacts/` in this package.
Start sha: d35875e71c4b7be86a428ee3673a3c63a115b305
Diff against the start snapshot: 
diff --git a/src/superclaude/skills/ccsession-tag/ccsession-orca b/src/superclaude/skills/ccsession-tag/ccsession-orca
index 9cb4b724..9f98b8a7 100755
--- a/src/superclaude/skills/ccsession-tag/ccsession-orca
+++ b/src/superclaude/skills/ccsession-tag/ccsession-orca
@@ -182,10 +182,10 @@ if [ "$ask_ok" = 1 ] && [ -n "${ORCA_PANE_KEY:-}" ] && [ "$name_from_env" = 0 ];
     # dropped above and does not stop a reopen).
     unset CCSESSION_NAME CCSESSION_ASK_TIMEOUT
     if [ -n "$name" ]; then
-      echo "[ccsession] Reopening this tab's session '$name'"
+      echo "[ccsession] Reopening this tab's session '$name'" >&2
       exec "$CCSESSION" --name "$name" --shim --claude-args "$@"
     fi
-    echo "[ccsession] Reopening this tab's session ${session:0:8}"
+    echo "[ccsession] Reopening this tab's session ${session:0:8}" >&2
     exec "$CCSESSION" --shim --claude-args "$@" --resume "$session"
   fi
 fi

--- new untracked file .dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/t3-expected-failures.log ---
============================= test session starts ==============================
collected 395 items

tests/unit/test_ccsession_tag.py ........F...................F.......... [  9%]
........................................................................ [ 28%]
........................................................................ [ 46%]
........................................................................ [ 64%]
....                                                                     [ 65%]
tests/unit/test_ccsession_tiers.py ...........F......................... [ 74%]
................................F.........F.........F................... [ 93%]
...........................                                              [100%]

=================================== FAILURES ===================================
______________________ test_shim_is_detected_without_lsof ______________________
tests/unit/test_ccsession_tag.py:433: in test_shim_is_detected_without_lsof
    assert "Starting model-alias shim" in first.stdout
E   AssertionError: assert 'Starting model-alias shim' in 'launched\n'
E    +  where 'launched\n' = CompletedProcess(args=['/home/coder/workspaces/worktrees/IronClaude/ic-issue-389/src/superclaude/skills/ccsession-tag/...d not pre-load gateway models; Claude Code will retry discovery after launch\n[ccsession] Starting untagged session\n').stdout
____________ test_label_with_missing_transcript_starts_new_session _____________
tests/unit/test_ccsession_tag.py:1222: in test_label_with_missing_transcript_starts_new_session
    assert "has no saved conversation; starting a new one" in stdout
E   assert 'has no saved conversation; starting a new one' in '["--dangerously-skip-permissions", "--allowedTools=Grep", "--name", "demo"]\n'
_________________ test_default_tier_sets_model_and_tier_window _________________
tests/unit/test_ccsession_tiers.py:412: in test_default_tier_sets_model_and_tier_window
    assert "tier2" in out and "muse-spark-1.3" in out
E   AssertionError: assert ('tier2' in '')
______________ test_a_busy_shim_is_never_stopped_by_a_new_launch _______________
tests/unit/test_ccsession_tiers.py:1523: in test_a_busy_shim_is_never_stopped_by_a_new_launch
    assert "leaving it running" in out
E   AssertionError: assert 'leaving it running' in ''
____________ test_upgraded_code_starts_a_new_shim_and_keeps_the_old ____________
tests/unit/test_ccsession_tiers.py:1918: in test_upgraded_code_starts_a_new_shim_and_keeps_the_old
    assert url2 == f"http://127.0.0.1:{port + 101}" and "older code" in out
E   AssertionError: assert ('http://127.0.0.1:53884' == 'http://127.0.0.1:53884'
E     
E       http://127.0.0.1:53884 and 'older code' in '')
____________ test_model_outside_tier_mode_stays_where_it_was_typed _____________
tests/unit/test_ccsession_tiers.py:2060: in test_model_outside_tier_mode_stays_where_it_was_typed
    assert "--model=sonnet" in seen["argv"] and "labeled 'work'" in out
E   assert ('--model=sonnet' in ['--dangerously-skip-permissions', '--allowedTools=Grep', '--name', 'work', '--model=sonnet'] and "labeled 'work'" in '')
=========================== short test summary info ============================
FAILED tests/unit/test_ccsession_tag.py::test_shim_is_detected_without_lsof
FAILED tests/unit/test_ccsession_tag.py::test_label_with_missing_transcript_starts_new_session
FAILED tests/unit/test_ccsession_tiers.py::test_default_tier_sets_model_and_tier_window
FAILED tests/unit/test_ccsession_tiers.py::test_a_busy_shim_is_never_stopped_by_a_new_launch
FAILED tests/unit/test_ccsession_tiers.py::test_upgraded_code_starts_a_new_shim_and_keeps_the_old
FAILED tests/unit/test_ccsession_tiers.py::test_model_outside_tier_mode_stays_where_it_was_typed
================== 6 failed, 389 passed in 250.78s (0:04:10) ===================

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

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
