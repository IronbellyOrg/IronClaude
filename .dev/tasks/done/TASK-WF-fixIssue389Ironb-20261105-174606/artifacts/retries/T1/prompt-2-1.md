ce35c6d0c850b99092a711707782d011227b3fd5
Review one task for spec compliance.

Task brief: ## Task 1: Add the permanent replay test and record it failing on the unfixed tree

Add `test_version_through_orca_keeps_stdout_clean(tmp_path)` to `tests/unit/test_ccsession_tag.py`, in the ccsession-orca section after the `_orca_no_tty` helper (the helper starts at line 1470; `_orca_env` is at line 1316 and `ORCA` at line 1304). Model it on the throwaway replay at `.dev/troubleshoot/bug-ccsession-prints-status-lines-stdout-20261105170635/artifacts/test_negative_witness.py`, but use the file's own helpers instead of loading the module by path. Build the environment with `_orca_env(tmp_path)`, overwrite the stand-in `tools/claude-record` (the file `_orca_env` creates) with a shell script that only prints `2.1.318 (Claude Code)`, make it executable, then run `subprocess.run([str(ORCA), "--version"], env=env, cwd=tmp_path / "work", stdin=subprocess.DEVNULL, text=True, capture_output=True, timeout=60)`. Do not use `_orca_no_tty`: it joins stdout and stderr and could not tell the streams apart. Import `_parse_version` from `superclaude.cli.eval.commands` at the top of the test file.

Assert, in this order: the return code is 0; `result.stdout == "2.1.318 (Claude Code)\n"`; `"[ccsession] Starting untagged session" in result.stderr`; and `_parse_version(result.stdout + result.stderr) == (2, 1, 318)`.

Run only this test on the tree as it is now, before any launcher edit, and keep the output.

Acceptance criteria:
- The new test exists in `tests/unit/test_ccsession_tag.py` and uses `subprocess.run(..., capture_output=True)` directly, with stdout and stderr read separately.
- Run on the unfixed tree with `uv run pytest tests/unit/test_ccsession_tag.py::test_version_through_orca_keeps_stdout_clean -q -p no:cacheprovider`, it FAILS on the stdout assertion, and the failure output shows three `[ccsession]` lines (tier line, `Shim already running on 127.0.0.1:4555 (reusing)`, `Starting untagged session`) ahead of Claude's line. That output is saved to `./artifacts/t1-negative.log`.

AC ids:
T1.AC1: The new test exists in `tests/unit/test_ccsession_tag.py` and uses `subprocess.run(..., capture_output=True)` directly, with stdout and stderr read separately.
T1.AC2: Run on the unfixed tree with `uv run pytest tests/unit/test_ccsession_tag.py::test_version_through_orca_keeps_stdout_clean -q -p no:cacheprovider`, it FAILS on the stdout assertion, and the failure output shows three `[ccsession]` lines (tier line, `Shim already running on 127.0.0.1:4555 (reusing)`, `Starting untagged session`) ahead of Claude's line. That output is saved to `./artifacts/t1-negative.log`.

(Repository root: /home/coder/workspaces/worktrees/IronClaude/ic-issue-389. The task's own evidence files `./artifacts/...` live in /home/coder/workspaces/worktrees/IronClaude/ic-issue-389/.dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/ .)
Global constraints: - Scope is the launcher scripts `src/superclaude/skills/ccsession-tag/ccsession` and `src/superclaude/skills/ccsession-tag/ccsession-orca`, the tests that read their output, `CHANGELOG.md` and the skill `README.md`. `src/superclaude/skills/ccsession-tag/models.py` is not edited: its two `[ccsession]` notes (line 313 `model list updated`, line 837 `model data check`) are routed to standard error at their one call site in `ccsession` (line 1733), so the documented `ccsession --refresh-models` report keeps printing on standard output.
- `src/superclaude/cli/eval/commands.py` (the version probe and `_parse_version`) is not edited. Hardening it (treat a non-zero exit code as "not callable", prefer the `X.Y.Z (Claude Code)` form) is a separate pending decision and must not be added here. Its failure-path behavior (stdout empty because the launcher exited early) is deliberately not pinned by any test in this plan.
- These stay on standard output because the shell captures them: every `models.py` print captured with `$(...)` in `ccsession` (the `PROFILE_*=` lines, digests, shim port, tier lists, compact settings, the `models` and `status` reports), and the values printed by `ccsession --ask`, `--auto-name`, `--list`, `--rm`, `--refresh-models` and `--models-status`.
- Existing `>&2` warnings and errors (`ccsession` lines 823, 944, 973, 980, 1002, 1013, 1080, 1856; `ccsession-orca` lines 136, 211) are correct and stay as they are.
- Edit only under `src/superclaude/skills/ccsession-tag/`, `tests/` and `CHANGELOG.md`. Do not edit `.claude/` mirrors by hand; `make sync-dev` is the only way they change and they are never staged.
- Hardening closure for this fix: the replay run recorded in Task 2 is the positive witness (the negative witness was run before this plan on the unfixed tree), Task 8 supplies the parser fixtures, and the executor's final independent review is the off-path review.
- Evidence the tasks name (logs, outputs) is written under `./artifacts/` in this package.
Start sha: ce35c6d0c850b99092a711707782d011227b3fd5
Diff against the start snapshot: 
diff --git a/tests/unit/test_ccsession_tag.py b/tests/unit/test_ccsession_tag.py
index 62cf1979..f56e44fb 100644
--- a/tests/unit/test_ccsession_tag.py
+++ b/tests/unit/test_ccsession_tag.py
@@ -28,6 +28,7 @@ REPO_ROOT = Path(__file__).resolve().parents[2]
 SKILL_DIR = REPO_ROOT / "src" / "superclaude" / "skills" / "ccsession-tag"
 sys.path.insert(0, str(SKILL_DIR))
 import models  # noqa: E402
+from superclaude.cli.eval.commands import _parse_version  # noqa: E402
 
 # A fake shim reports the code fingerprint of the real one, so launches reuse it.
 SHIM_CODE = models.code_digest(str(SKILL_DIR / "local-gateway-alias-proxy.py"))
@@ -1483,6 +1484,43 @@ def _orca_no_tty(tmp_path: Path, *args: str, **extra: str) -> tuple[str, dict]:
     )
 
 
+def test_version_through_orca_keeps_stdout_clean(tmp_path: Path) -> None:
+    """Issue 389: a scripted `claude --version` gets only Claude's own output.
+
+    The status lines of ccsession go to standard error. Reading the streams
+    apart (not through _orca_no_tty, which joins them) is the point of this test.
+    """
+    # A Coder workspace runs in tier mode, so its first status line names the
+    # tier; give the scratch launch the same mode (a workspace env block with
+    # one stand-in model per slot the bundled model data asks for).
+    defaults = tmp_path / "defaults.sh"
+    lines = ["export CCSESSION_DEFAULT_TIER=tier2"]
+    for name, tier in models.load()[0]["tiers"].items():
+        lines.append(f"export T{models.tier_number(name)}_WINDOW=500000")
+        for slot in tier["models_env"]:
+            lines.append(f"export {slot}=stand-in-{slot.lower()}")
+            lines.append(f"export {slot}_WINDOW=500000")
+    defaults.write_text("\n".join(lines) + "\n")
+    env = _orca_env(tmp_path, AIDEV_AI_DEFAULTS_PATH=str(defaults))
+    stand_in = tmp_path / "tools" / "claude-record"
+    stand_in.write_text("#!/bin/sh\necho '2.1.318 (Claude Code)'\n")
+    stand_in.chmod(0o700)
+    result = subprocess.run(
+        [str(ORCA), "--version"],
+        env=env,
+        cwd=tmp_path / "work",
+        stdin=subprocess.DEVNULL,
+        text=True,
+        capture_output=True,
+        timeout=60,
+    )
+    assert result.returncode == 0, result.stderr
+    assert result.stdout == "2.1.318 (Claude Code)\n"
+    assert "[ccsession] Starting untagged session" in result.stderr
+    # superclaude eval reads the Claude version from this text.
+    assert _parse_version(result.stdout + result.stderr) == (2, 1, 318)
+
+
 def _assert_through_shim(record: dict) -> None:
     assert record["base_url"] == "http://127.0.0.1:4555"
     # One credential reaches Claude Code, never both.

--- new untracked file .dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/t1-negative.log ---
============================= test session starts ==============================
collecting ... collected 1 item

tests/unit/test_ccsession_tag.py::test_version_through_orca_keeps_stdout_clean FAILED [100%]

=================================== FAILURES ===================================
_________________ test_version_through_orca_keeps_stdout_clean _________________
tests/unit/test_ccsession_tag.py:1518: in test_version_through_orca_keeps_stdout_clean
    assert result.stdout == "2.1.318 (Claude Code)\n"
E   AssertionError: assert '[ccsession] tier2 (Tier 2: stand-in-t2model01, stand-in-t2model02, stand-in-t2model03, stand-in-t2model04, stand-in-t2model05, stand-in-t2model06): model claude-gw-tier2[1m], context 500000, auto-compact window 500000\n[ccsession] Shim already running on 127.0.0.1:4555 (reusing)\n[ccsession] Starting untagged session\n2.1.318 (Claude Code)\n' == '2.1.318 (Claude Code)\n'
E     
E     + [ccsession] tier2 (Tier 2: stand-in-t2model01, stand-in-t2model02, stand-in-t2model03, stand-in-t2model04, stand-in-t2model05, stand-in-t2model06): model claude-gw-tier2[1m], context 500000, auto-compact window 500000
E     + [ccsession] Shim already running on 127.0.0.1:4555 (reusing)
E     + [ccsession] Starting untagged session
E       2.1.318 (Claude Code)
=========================== short test summary info ============================
FAILED tests/unit/test_ccsession_tag.py::test_version_through_orca_keeps_stdout_clean - AssertionError: assert '[ccsession] tier2 (Tier 2: stand-in-t2model01, stand-in-t2model02, stand-in-t2model03, stand-in-t2model04, stand-in-t2model05, stand-in-t2model06): model claude-gw-tier2[1m], context 500000, auto-compact window 500000\n[ccsession] Shim already running on 127.0.0.1:4555 (reusing)\n[ccsession] Starting untagged session\n2.1.318 (Claude Code)\n' == '2.1.318 (Claude Code)\n'
  
  + [ccsession] tier2 (Tier 2: stand-in-t2model01, stand-in-t2model02, stand-in-t2model03, stand-in-t2model04, stand-in-t2model05, stand-in-t2model06): model claude-gw-tier2[1m], context 500000, auto-compact window 500000
  + [ccsession] Shim already running on 127.0.0.1:4555 (reusing)
  + [ccsession] Starting untagged session
    2.1.318 (Claude Code)
============================== 1 failed in 1.11s ===============================

Delta diff from the previous reviewed tree (empty on the first review): 
diff --git a/.dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/t1-negative.log b/.dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/t1-negative.log
deleted file mode 100644
index bb025c55..00000000
--- a/.dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/t1-negative.log
+++ /dev/null
@@ -1,17 +0,0 @@
-============================= test session starts ==============================
-collected 1 item
-
-tests/unit/test_ccsession_tag.py F                                       [100%]
-
-=================================== FAILURES ===================================
-_________________ test_version_through_orca_keeps_stdout_clean _________________
-tests/unit/test_ccsession_tag.py:1507: in test_version_through_orca_keeps_stdout_clean
-    assert result.stdout == "2.1.318 (Claude Code)\n"
-E   AssertionError: assert '[ccsession] ...laude Code)\n' == '2.1.318 (Claude Code)\n'
-E     
-E     + [ccsession] Shim already running on 127.0.0.1:4555 (reusing)
-E     + [ccsession] Starting untagged session
-E       2.1.318 (Claude Code)
-=========================== short test summary info ============================
-FAILED tests/unit/test_ccsession_tag.py::test_version_through_orca_keeps_stdout_clean
-============================== 1 failed in 1.18s ===============================
diff --git a/tests/unit/test_ccsession_tag.py b/tests/unit/test_ccsession_tag.py
index 98813ebc..f56e44fb 100644
--- a/tests/unit/test_ccsession_tag.py
+++ b/tests/unit/test_ccsession_tag.py
@@ -1490,7 +1490,18 @@ def test_version_through_orca_keeps_stdout_clean(tmp_path: Path) -> None:
     The status lines of ccsession go to standard error. Reading the streams
     apart (not through _orca_no_tty, which joins them) is the point of this test.
     """
-    env = _orca_env(tmp_path)
+    # A Coder workspace runs in tier mode, so its first status line names the
+    # tier; give the scratch launch the same mode (a workspace env block with
+    # one stand-in model per slot the bundled model data asks for).
+    defaults = tmp_path / "defaults.sh"
+    lines = ["export CCSESSION_DEFAULT_TIER=tier2"]
+    for name, tier in models.load()[0]["tiers"].items():
+        lines.append(f"export T{models.tier_number(name)}_WINDOW=500000")
+        for slot in tier["models_env"]:
+            lines.append(f"export {slot}=stand-in-{slot.lower()}")
+            lines.append(f"export {slot}_WINDOW=500000")
+    defaults.write_text("\n".join(lines) + "\n")
+    env = _orca_env(tmp_path, AIDEV_AI_DEFAULTS_PATH=str(defaults))
     stand_in = tmp_path / "tools" / "claude-record"
     stand_in.write_text("#!/bin/sh\necho '2.1.318 (Claude Code)'\n")
     stand_in.chmod(0o700)

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B1 ac=T1.AC2 at=.dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/t1-negative.log:11-13 anchor="the failure output shows three `[ccsession]` lines (tier line, `Shim already running on 127.0.0.1:4555 (reusing)`, `Starting untagged session`) ahead of Claude's line" chk=y,n,n,n family=t1-negative-witness-tier-line fix=make the fixture enter tier mode (explicit AIDEV_AI_DEFAULTS_PATH with a tier block) so the unfixed tree prints the tier line, re-record the log first=A1 origin=new: The saved log shows only two [ccsession] lines (log lines 12-13), so the tier line is missing.
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
