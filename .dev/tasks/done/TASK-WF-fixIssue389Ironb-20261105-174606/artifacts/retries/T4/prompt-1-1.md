9de0e72980892dc6e354c97a656313acf0eea4ef
Review one task for spec compliance.

Task brief: ## Task 4: Update the ccsession tests in tests/unit/test_ccsession_tag.py that read status lines from stdout

Depends on: Task 3

In `tests/unit/test_ccsession_tag.py`:
- `test_shim_is_detected_without_lsof` (stand-in claude `echo launched` at lines 399-401): change line 431 to `assert "Starting model-alias shim" in first.stderr` and line 441 to `assert "already running" in second.stderr`, and add `assert first.stdout == "launched\n"` and `assert second.stdout == "launched\n"` next to them.
- `_label_launch` (lines 1158-1193) returns only `result.stdout`. Split it: add `_label_run(tmp_path, transcript, args=("demo",))` with the same body returning `(result, label_kept)` where `result` is the `subprocess.CompletedProcess`, and make `_label_launch` call it and return `(result.stdout, label_kept)` so its other callers (lines 1226, 1252, 1277, 1294 and any others) need no change.
- `test_label_with_missing_transcript_starts_new_session` (lines 1218-1222): use `_label_run`; assert `"has no saved conversation; starting a new one" in result.stderr`, `"[ccsession]" not in result.stdout`, that `"--resume"` is not in `json.loads(result.stdout.strip().splitlines()[-1])`, and that the label is not kept.
- `test_label_with_saved_transcript_resumes` (lines 1225-1229): keep it on `_label_launch`; it reads the last stdout line, which is still Claude's JSON.
- Leave `test_models_refresh_*`-style tests that call `models.py refresh` directly (line 1054 asserts `model list updated to ...` in stdout and `second.stdout == ""`) unchanged: `models.py` is not edited.

Acceptance criteria:
- `test_shim_is_detected_without_lsof` (or its skip, on a machine without a usable shim) and `test_label_with_missing_transcript_starts_new_session` pass, and no test in `tests/unit/test_ccsession_tag.py` that passed before Task 2 fails now.
- `uv run pytest tests/unit/test_ccsession_tag.py -q -p no:cacheprovider` passes; its output is saved to `./artifacts/t4-tag-tests.log`.

AC ids:
T4.AC1: `test_shim_is_detected_without_lsof` (or its skip, on a machine without a usable shim) and `test_label_with_missing_transcript_starts_new_session` pass, and no test in `tests/unit/test_ccsession_tag.py` that passed before Task 2 fails now.
T4.AC2: `uv run pytest tests/unit/test_ccsession_tag.py -q -p no:cacheprovider` passes; its output is saved to `./artifacts/t4-tag-tests.log`.

(Repository root: /home/coder/workspaces/worktrees/IronClaude/ic-issue-389. The task's own evidence files `./artifacts/...` live in /home/coder/workspaces/worktrees/IronClaude/ic-issue-389/.dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/ .)
Global constraints: - Scope is the launcher scripts `src/superclaude/skills/ccsession-tag/ccsession` and `src/superclaude/skills/ccsession-tag/ccsession-orca`, the tests that read their output, `CHANGELOG.md` and the skill `README.md`. `src/superclaude/skills/ccsession-tag/models.py` is not edited: its two `[ccsession]` notes (line 313 `model list updated`, line 837 `model data check`) are routed to standard error at their one call site in `ccsession` (line 1733), so the documented `ccsession --refresh-models` report keeps printing on standard output.
- `src/superclaude/cli/eval/commands.py` (the version probe and `_parse_version`) is not edited. Hardening it (treat a non-zero exit code as "not callable", prefer the `X.Y.Z (Claude Code)` form) is a separate pending decision and must not be added here. Its failure-path behavior (stdout empty because the launcher exited early) is deliberately not pinned by any test in this plan.
- These stay on standard output because the shell captures them: every `models.py` print captured with `$(...)` in `ccsession` (the `PROFILE_*=` lines, digests, shim port, tier lists, compact settings, the `models` and `status` reports), and the values printed by `ccsession --ask`, `--auto-name`, `--list`, `--rm`, `--refresh-models` and `--models-status`.
- Existing `>&2` warnings and errors (`ccsession` lines 823, 944, 973, 980, 1002, 1013, 1080, 1856; `ccsession-orca` lines 136, 211) are correct and stay as they are.
- Edit only under `src/superclaude/skills/ccsession-tag/`, `tests/` and `CHANGELOG.md`. Do not edit `.claude/` mirrors by hand; `make sync-dev` is the only way they change and they are never staged.
- Hardening closure for this fix: the replay run recorded in Task 2 is the positive witness (the negative witness was run before this plan on the unfixed tree), Task 8 supplies the parser fixtures, and the executor's final independent review is the off-path review.
- Evidence the tasks name (logs, outputs) is written under `./artifacts/` in this package.
Start sha: 9de0e72980892dc6e354c97a656313acf0eea4ef
Diff against the start snapshot: 
diff --git a/tests/unit/test_ccsession_tag.py b/tests/unit/test_ccsession_tag.py
index 8fae8263..f31924b2 100644
--- a/tests/unit/test_ccsession_tag.py
+++ b/tests/unit/test_ccsession_tag.py
@@ -430,7 +430,8 @@ def test_shim_is_detected_without_lsof(tmp_path: Path) -> None:
             stdin=subprocess.DEVNULL,
         )
         assert first.returncode == 0, first.stderr
-        assert "Starting model-alias shim" in first.stdout
+        assert "Starting model-alias shim" in first.stderr
+        assert first.stdout == "launched\n"
         second = subprocess.run(
             command,
             env=env,
@@ -440,7 +441,8 @@ def test_shim_is_detected_without_lsof(tmp_path: Path) -> None:
             stdin=subprocess.DEVNULL,
         )
         assert second.returncode == 0, second.stderr
-        assert "already running" in second.stdout
+        assert "already running" in second.stderr
+        assert second.stdout == "launched\n"
     finally:
         subprocess.run(["pkill", "-f", str(shim_copy)], check=False)
 
@@ -1157,9 +1159,10 @@ def test_help_and_unknown_profile_list_data_profiles(tmp_path: Path) -> None:
     assert "Valid profiles: " + ", ".join(_bundled()["profiles"]) in result.stderr
 
 
-def _label_launch(
+def _label_run(
     tmp_path: Path, transcript: bool, args: tuple[str, ...] = ("demo",)
-) -> tuple[str, bool]:
+) -> tuple[subprocess.CompletedProcess[str], bool]:
+    """Run ccsession on a saved label; return the finished process and whether the label stayed."""
     home = tmp_path / "home"
     work = tmp_path / "work"
     work.mkdir(parents=True)
@@ -1192,7 +1195,15 @@ def _label_launch(
         capture_output=True,
         check=True,
     )
-    return result.stdout, (topics / "demo.txt").exists()
+    return result, (topics / "demo.txt").exists()
+
+
+def _label_launch(
+    tmp_path: Path, transcript: bool, args: tuple[str, ...] = ("demo",)
+) -> tuple[str, bool]:
+    """Like _label_run, but only the standard output (Claude's last line is its JSON)."""
+    result, label_kept = _label_run(tmp_path, transcript, args)
+    return result.stdout, label_kept
 
 
 def test_rm_removes_an_existing_label_that_starts_with_a_dash(tmp_path: Path) -> None:
@@ -1218,9 +1229,10 @@ def test_rm_removes_an_existing_label_that_starts_with_a_dash(tmp_path: Path) ->
 
 
 def test_label_with_missing_transcript_starts_new_session(tmp_path: Path) -> None:
-    stdout, label_kept = _label_launch(tmp_path, transcript=False)
-    assert "has no saved conversation; starting a new one" in stdout
-    assert "--resume" not in json.loads(stdout.strip().splitlines()[-1])
+    result, label_kept = _label_run(tmp_path, transcript=False)
+    assert "has no saved conversation; starting a new one" in result.stderr
+    assert "[ccsession]" not in result.stdout
+    assert "--resume" not in json.loads(result.stdout.strip().splitlines()[-1])
     assert not label_kept
 
 

--- new untracked file .dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/t4-tag-tests.log ---
============================= test session starts ==============================
collected 259 items

tests/unit/test_ccsession_tag.py ....................................... [ 15%]
........................................................................ [ 42%]
........................................................................ [ 70%]
........................................................................ [ 98%]
....                                                                     [100%]

======================= 259 passed in 115.49s (0:01:55) ========================

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
