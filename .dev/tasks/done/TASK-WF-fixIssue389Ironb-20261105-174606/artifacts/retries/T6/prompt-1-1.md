5efc9ab849dd911f2092df60dd0dbfab363e36a4
Review one task for spec compliance.

Task brief: ## Task 6: Add stream-pinning tests for launch variants, the model refresh note and the refresh report

Depends on: Task 4

In `tests/unit/test_ccsession_tag.py`, using the `_label_run` helper from Task 4:
- Add `test_launch_status_lines_are_on_stderr_only`, parametrized with the same six `(args, transcript)` cases as `test_every_launch_restores_grep_and_glob` (lines 1232-1242). For each case assert that `result.stdout.strip().splitlines()` has exactly one line (the stand-in's JSON argument list), that `"[ccsession]" not in result.stdout`, and that `"[ccsession]" in result.stderr`. Set `CC_CLAUDE_FLAGS` the way the neighbouring test does (`monkeypatch.delenv("CC_CLAUDE_FLAGS", raising=False)`).
- Add a test that the model list update note reaches standard error at launch: follow `test_private_addon_profiles_never_download_model_data` (around line 1259) and its `_DataServer` helper to serve a newer model data version, leave `CCSESSION_MODELS_REFRESH` unset, point `CCSESSION_MODELS_URL` at the server, launch `ccsession --profile claude` with the stand-in claude, and assert `"model list updated"` is in `result.stderr` and not in `result.stdout`. Read the neighbouring tests first and reuse their environment helpers instead of building a new one.
- Add a guard that `ccsession --refresh-models` (handled at `ccsession` lines 1676-1678, with `CCSESSION_MODELS_VERBOSE` set by the script) keeps its `model data check: ...` report on standard output, using the same `_DataServer` pattern, so nobody later moves `models.py` line 837 to standard error.

Acceptance criteria:
- The three new tests pass on the fixed tree and each uses separate captures of stdout and stderr (no `stdout + stderr` join).
- The parametrized test is a real stream pin: its `"[ccsession]" not in result.stdout` assertion is the one that the pre-fix output recorded in `./artifacts/t1-negative.log` (three `[ccsession]` lines on standard output) would violate, and each of the six cases prints at least one `[ccsession]` line on the fixed tree.
- `uv run pytest tests/unit/test_ccsession_tag.py -q -p no:cacheprovider` passes; its output is saved to `./artifacts/t6-tag-tests.log`.

AC ids:
T6.AC1: The three new tests pass on the fixed tree and each uses separate captures of stdout and stderr (no `stdout + stderr` join).
T6.AC2: The parametrized test is a real stream pin: its `"[ccsession]" not in result.stdout` assertion is the one that the pre-fix output recorded in `./artifacts/t1-negative.log` (three `[ccsession]` lines on standard output) would violate, and each of the six cases prints at least one `[ccsession]` line on the fixed tree.
T6.AC3: `uv run pytest tests/unit/test_ccsession_tag.py -q -p no:cacheprovider` passes; its output is saved to `./artifacts/t6-tag-tests.log`.

(Repository root: /home/coder/workspaces/worktrees/IronClaude/ic-issue-389. The task's own evidence files `./artifacts/...` live in /home/coder/workspaces/worktrees/IronClaude/ic-issue-389/.dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/ .)
Global constraints: - Scope is the launcher scripts `src/superclaude/skills/ccsession-tag/ccsession` and `src/superclaude/skills/ccsession-tag/ccsession-orca`, the tests that read their output, `CHANGELOG.md` and the skill `README.md`. `src/superclaude/skills/ccsession-tag/models.py` is not edited: its two `[ccsession]` notes (line 313 `model list updated`, line 837 `model data check`) are routed to standard error at their one call site in `ccsession` (line 1733), so the documented `ccsession --refresh-models` report keeps printing on standard output.
- `src/superclaude/cli/eval/commands.py` (the version probe and `_parse_version`) is not edited. Hardening it (treat a non-zero exit code as "not callable", prefer the `X.Y.Z (Claude Code)` form) is a separate pending decision and must not be added here. Its failure-path behavior (stdout empty because the launcher exited early) is deliberately not pinned by any test in this plan.
- These stay on standard output because the shell captures them: every `models.py` print captured with `$(...)` in `ccsession` (the `PROFILE_*=` lines, digests, shim port, tier lists, compact settings, the `models` and `status` reports), and the values printed by `ccsession --ask`, `--auto-name`, `--list`, `--rm`, `--refresh-models` and `--models-status`.
- Existing `>&2` warnings and errors (`ccsession` lines 823, 944, 973, 980, 1002, 1013, 1080, 1856; `ccsession-orca` lines 136, 211) are correct and stay as they are.
- Edit only under `src/superclaude/skills/ccsession-tag/`, `tests/` and `CHANGELOG.md`. Do not edit `.claude/` mirrors by hand; `make sync-dev` is the only way they change and they are never staged.
- Hardening closure for this fix: the replay run recorded in Task 2 is the positive witness (the negative witness was run before this plan on the unfixed tree), Task 8 supplies the parser fixtures, and the executor's final independent review is the off-path review.
- Evidence the tasks name (logs, outputs) is written under `./artifacts/` in this package.
Start sha: 5efc9ab849dd911f2092df60dd0dbfab363e36a4
Diff against the start snapshot: 
diff --git a/tests/unit/test_ccsession_tag.py b/tests/unit/test_ccsession_tag.py
index f31924b2..ba191184 100644
--- a/tests/unit/test_ccsession_tag.py
+++ b/tests/unit/test_ccsession_tag.py
@@ -1243,17 +1243,17 @@ def test_label_with_saved_transcript_resumes(tmp_path: Path) -> None:
     assert label_kept
 
 
-@pytest.mark.parametrize(
-    ("args", "transcript"),
-    [
-        (("-p", "x"), False),
-        (("--profile", "claude", "-p", "x"), False),
-        (("demo",), False),
-        (("demo",), True),
-        (("--profile", "claude", "demo"), False),
-        (("--profile", "claude", "demo"), True),
-    ],
-)
+_LAUNCH_CASES = [
+    (("-p", "x"), False),
+    (("--profile", "claude", "-p", "x"), False),
+    (("demo",), False),
+    (("demo",), True),
+    (("--profile", "claude", "demo"), False),
+    (("--profile", "claude", "demo"), True),
+]
+
+
+@pytest.mark.parametrize(("args", "transcript"), _LAUNCH_CASES)
 def test_every_launch_restores_grep_and_glob(
     tmp_path: Path, args: tuple[str, ...], transcript: bool, monkeypatch
 ) -> None:
@@ -1270,6 +1270,20 @@ def test_every_launch_restores_grep_and_glob(
     assert ("--resume" in launched) == transcript
 
 
+@pytest.mark.parametrize(("args", "transcript"), _LAUNCH_CASES)
+def test_launch_status_lines_are_on_stderr_only(
+    tmp_path: Path, args: tuple[str, ...], transcript: bool, monkeypatch
+) -> None:
+    # Issue 389: a scripted `claude` call must see only Claude's own output on
+    # standard output. Here that is the stand-in's one JSON line; every
+    # [ccsession] notice belongs on standard error.
+    monkeypatch.delenv("CC_CLAUDE_FLAGS", raising=False)
+    result, _ = _label_run(tmp_path, transcript=transcript, args=args)
+    assert len(result.stdout.strip().splitlines()) == 1, result.stdout
+    assert "[ccsession]" not in result.stdout
+    assert "[ccsession]" in result.stderr
+
+
 def test_private_addon_profiles_never_download_model_data(
     tmp_path: Path, monkeypatch
 ) -> None:
@@ -1285,6 +1299,50 @@ def test_private_addon_profiles_never_download_model_data(
         server.close()
 
 
+def test_model_list_update_note_goes_to_stderr_at_launch(
+    tmp_path: Path, monkeypatch
+) -> None:
+    newer = _bundled()
+    newer["version"] = "9999-01-01.1"
+    server = _DataServer(newer)
+    monkeypatch.setenv("CCSESSION_MODELS_REFRESH", "1")
+    monkeypatch.setenv("CCSESSION_MODELS_URL", server.url)
+    try:
+        result = _addon_launch(tmp_path, "--profile", "claude")
+    finally:
+        server.close()
+    assert result.returncode == 0, result.stderr
+    assert "model list updated to 9999-01-01.1" in result.stderr
+    assert "model list updated" not in result.stdout
+
+
+def test_refresh_models_report_stays_on_stdout(tmp_path: Path) -> None:
+    # `ccsession --refresh-models` is a report the user asked for, so unlike a
+    # launch notice it stays on standard output.
+    server = _DataServer(_bundled())
+    env = {
+        **os.environ,
+        "HOME": str(tmp_path),
+        "XDG_CACHE_HOME": str(tmp_path),
+        "CCSESSION_MODELS_URL": server.url,
+    }
+    try:
+        result = subprocess.run(
+            [str(SKILL_DIR / "ccsession"), "--refresh-models"],
+            env=env,
+            cwd=tmp_path,
+            text=True,
+            capture_output=True,
+            check=False,
+            timeout=60,
+        )
+    finally:
+        server.close()
+    assert result.returncode == 0, result.stderr
+    assert "[ccsession] model data check:" in result.stdout
+    assert "model data check" not in result.stderr
+
+
 def test_claude_args_passes_the_rest_to_claude_unchanged(tmp_path: Path) -> None:
     # After --claude-args nothing is a label or a ccsession option, and the
     # marker itself is not passed on.

--- new untracked file .dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/t6-tag-tests.log ---
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 5.0.0
rootdir: /home/coder/workspaces/worktrees/IronClaude/ic-issue-389
configfile: pyproject.toml
plugins: superclaude-5.0.0, anyio-4.16.0
collected 267 items

tests/unit/test_ccsession_tag.py ....................................... [ 14%]
........................................................................ [ 41%]
........................................................................ [ 68%]
........................................................................ [ 95%]
............                                                             [100%]

======================= 267 passed in 117.98s (0:01:57) ========================

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
