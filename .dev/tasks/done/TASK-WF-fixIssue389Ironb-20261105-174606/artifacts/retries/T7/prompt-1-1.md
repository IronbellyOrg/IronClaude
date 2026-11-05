cd31e898b60bbeb7b17de4315093f8ad47c66023
Review one task for spec compliance.

Task brief: ## Task 7: Add a source guard test for the status echoes that tests cannot reach

Depends on: Task 3

Add `test_status_lines_in_launcher_scripts_go_to_stderr` to `tests/unit/test_ccsession_tag.py`. It reads the text of `ccsession` and `ccsession-orca` (use the `SKILL_DIR` constant the file already defines) and asserts: every line that contains `echo "[ccsession]` also contains `>&2`; the cache warm-up heredoc line is `python3 - >&2 <<'PY'` (so the Python print for `Cached N curated gateway models` cannot return to standard output); and the `refresh --wait` line in `ccsession` has `>&2` before `|| true`. This covers the sites a launch test cannot reach in a scratch environment: the Reopening notices (terminal and `ORCA_PANE_KEY` only) and the model cache print (no gateway in the test environment).

Acceptance criteria:
- The test passes on the fixed tree and fails if any one of the lines edited in Tasks 2 and 3 loses its `>&2` (check by confirming the assertion message names the offending file and line).
- `uv run pytest tests/unit/test_ccsession_tag.py::test_status_lines_in_launcher_scripts_go_to_stderr -q -p no:cacheprovider` passes; its output is saved to `./artifacts/t7-source-guard.log`.

AC ids:
T7.AC1: The test passes on the fixed tree and fails if any one of the lines edited in Tasks 2 and 3 loses its `>&2` (check by confirming the assertion message names the offending file and line).
T7.AC2: `uv run pytest tests/unit/test_ccsession_tag.py::test_status_lines_in_launcher_scripts_go_to_stderr -q -p no:cacheprovider` passes; its output is saved to `./artifacts/t7-source-guard.log`.

(Repository root: /home/coder/workspaces/worktrees/IronClaude/ic-issue-389. The task's own evidence files `./artifacts/...` live in /home/coder/workspaces/worktrees/IronClaude/ic-issue-389/.dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/ .)
Global constraints: - Scope is the launcher scripts `src/superclaude/skills/ccsession-tag/ccsession` and `src/superclaude/skills/ccsession-tag/ccsession-orca`, the tests that read their output, `CHANGELOG.md` and the skill `README.md`. `src/superclaude/skills/ccsession-tag/models.py` is not edited: its two `[ccsession]` notes (line 313 `model list updated`, line 837 `model data check`) are routed to standard error at their one call site in `ccsession` (line 1733), so the documented `ccsession --refresh-models` report keeps printing on standard output.
- `src/superclaude/cli/eval/commands.py` (the version probe and `_parse_version`) is not edited. Hardening it (treat a non-zero exit code as "not callable", prefer the `X.Y.Z (Claude Code)` form) is a separate pending decision and must not be added here. Its failure-path behavior (stdout empty because the launcher exited early) is deliberately not pinned by any test in this plan.
- These stay on standard output because the shell captures them: every `models.py` print captured with `$(...)` in `ccsession` (the `PROFILE_*=` lines, digests, shim port, tier lists, compact settings, the `models` and `status` reports), and the values printed by `ccsession --ask`, `--auto-name`, `--list`, `--rm`, `--refresh-models` and `--models-status`.
- Existing `>&2` warnings and errors (`ccsession` lines 823, 944, 973, 980, 1002, 1013, 1080, 1856; `ccsession-orca` lines 136, 211) are correct and stay as they are.
- Edit only under `src/superclaude/skills/ccsession-tag/`, `tests/` and `CHANGELOG.md`. Do not edit `.claude/` mirrors by hand; `make sync-dev` is the only way they change and they are never staged.
- Hardening closure for this fix: the replay run recorded in Task 2 is the positive witness (the negative witness was run before this plan on the unfixed tree), Task 8 supplies the parser fixtures, and the executor's final independent review is the off-path review.
- Evidence the tasks name (logs, outputs) is written under `./artifacts/` in this package.
Start sha: cd31e898b60bbeb7b17de4315093f8ad47c66023
Diff against the start snapshot: 
diff --git a/tests/unit/test_ccsession_tag.py b/tests/unit/test_ccsession_tag.py
index ba191184..eeb54315 100644
--- a/tests/unit/test_ccsession_tag.py
+++ b/tests/unit/test_ccsession_tag.py
@@ -1370,6 +1370,30 @@ def test_plain_double_dash_still_reaches_claude(tmp_path: Path) -> None:
     assert launched[-2:] == ["--", "-weird prompt"]
 
 
+def test_status_lines_in_launcher_scripts_go_to_stderr() -> None:
+    # Issue 389. A launch test cannot reach the Reopening notices (terminal and
+    # ORCA_PANE_KEY only) or the model cache print (needs a gateway), so read
+    # the scripts themselves.
+    for name in ("ccsession", "ccsession-orca"):
+        for number, line in enumerate((SKILL_DIR / name).read_text().splitlines(), 1):
+            if 'echo "[ccsession]' in line:
+                assert ">&2" in line, (
+                    f"{name}:{number} prints to stdout: {line.strip()}"
+                )
+    lines = (SKILL_DIR / "ccsession").read_text().splitlines()
+    assert any(line.strip() == "python3 - >&2 <<'PY'" for line in lines), (
+        "ccsession: the cache warm-up heredoc must start with python3 - >&2 <<'PY'"
+    )
+    refresh = [
+        (number, line)
+        for number, line in enumerate(lines, 1)
+        if 'refresh --wait "${CCSESSION_MODELS_WAIT' in line
+    ]
+    assert len(refresh) == 1, refresh
+    number, line = refresh[0]
+    assert ">&2 || true" in line, f"ccsession:{number} refresh note goes to stdout"
+
+
 # ccsession-orca: Orca's Claude command. Each launch runs the real wrapper and
 # the real ccsession against a fake claude that records its argv and env, and a
 # fake shim that ccsession reuses.

--- new untracked file .dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/t7-source-guard.log ---
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 5.0.0
rootdir: /home/coder/workspaces/worktrees/IronClaude/ic-issue-389
configfile: pyproject.toml
plugins: superclaude-5.0.0, anyio-4.16.0
collected 1 item

tests/unit/test_ccsession_tag.py .                                       [100%]

============================== 1 passed in 0.59s ===============================

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
