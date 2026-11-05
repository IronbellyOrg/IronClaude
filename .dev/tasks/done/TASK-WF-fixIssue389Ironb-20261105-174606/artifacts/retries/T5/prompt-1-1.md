441ab803236e03d522f0ac1c2e7ae56fe3167bf6
Review one task for spec compliance.

Task brief: ## Task 5: Update the ccsession tier tests in tests/unit/test_ccsession_tiers.py that read status lines from stdout

Depends on: Task 3

In `tests/unit/test_ccsession_tiers.py`:
- `test_default_tier_sets_model_and_tier_window` (line 400): `_launch` returns `(returncode, out, err, seen)` and the stand-in claude prints nothing. Change line 412 to assert `"tier2" in err and "muse-spark-1.3" in err` and add `assert out == ""`. If `out` is not empty, find which write reaches standard output and report it instead of weakening the assertion.
- `_real_launch` (lines 1465-1497) ends with `return proc.stdout, (tmp_path / "seen").read_text().strip()`: add `assert proc.stdout == ""` after the existing return-code assertion, return `proc.stderr` instead of `proc.stdout`, and update its docstring to say the first value is the launcher's standard error (its status lines). The callers `test_a_busy_shim_is_never_stopped_by_a_new_launch` (assertion at line 1523, `"leaving it running" in out`) and `test_upgraded_code_starts_a_new_shim_and_keeps_the_old` (assertions at lines 1918 `"older code" in out` and 1922 `"reusing" in out`) then need no change to their assertion text.
- `test_model_outside_tier_mode_stays_where_it_was_typed` (line 2051): change line 2060 so `"labeled 'work'"` is asserted in `err` (the second `_launch` already unpacks `err`).
- Leave every other test in the file unchanged: tests that read a pty or `stdout + stderr` (for example lines 449-479 and 509), the `--models-status` and `--help` tests, and the `workspace owner unknown` count at line 2526.

Acceptance criteria:
- The four tests named above pass (the two shim tests may skip on a machine without a usable shim), and no other test in `tests/unit/test_ccsession_tiers.py` that passed before Task 2 fails now.
- `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider` passes; its output is saved to `./artifacts/t5-tiers-tests.log`.

AC ids:
T5.AC1: The four tests named above pass (the two shim tests may skip on a machine without a usable shim), and no other test in `tests/unit/test_ccsession_tiers.py` that passed before Task 2 fails now.
T5.AC2: `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider` passes; its output is saved to `./artifacts/t5-tiers-tests.log`.

(Repository root: /home/coder/workspaces/worktrees/IronClaude/ic-issue-389. The task's own evidence files `./artifacts/...` live in /home/coder/workspaces/worktrees/IronClaude/ic-issue-389/.dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/ .)
Global constraints: - Scope is the launcher scripts `src/superclaude/skills/ccsession-tag/ccsession` and `src/superclaude/skills/ccsession-tag/ccsession-orca`, the tests that read their output, `CHANGELOG.md` and the skill `README.md`. `src/superclaude/skills/ccsession-tag/models.py` is not edited: its two `[ccsession]` notes (line 313 `model list updated`, line 837 `model data check`) are routed to standard error at their one call site in `ccsession` (line 1733), so the documented `ccsession --refresh-models` report keeps printing on standard output.
- `src/superclaude/cli/eval/commands.py` (the version probe and `_parse_version`) is not edited. Hardening it (treat a non-zero exit code as "not callable", prefer the `X.Y.Z (Claude Code)` form) is a separate pending decision and must not be added here. Its failure-path behavior (stdout empty because the launcher exited early) is deliberately not pinned by any test in this plan.
- These stay on standard output because the shell captures them: every `models.py` print captured with `$(...)` in `ccsession` (the `PROFILE_*=` lines, digests, shim port, tier lists, compact settings, the `models` and `status` reports), and the values printed by `ccsession --ask`, `--auto-name`, `--list`, `--rm`, `--refresh-models` and `--models-status`.
- Existing `>&2` warnings and errors (`ccsession` lines 823, 944, 973, 980, 1002, 1013, 1080, 1856; `ccsession-orca` lines 136, 211) are correct and stay as they are.
- Edit only under `src/superclaude/skills/ccsession-tag/`, `tests/` and `CHANGELOG.md`. Do not edit `.claude/` mirrors by hand; `make sync-dev` is the only way they change and they are never staged.
- Hardening closure for this fix: the replay run recorded in Task 2 is the positive witness (the negative witness was run before this plan on the unfixed tree), Task 8 supplies the parser fixtures, and the executor's final independent review is the off-path review.
- Evidence the tasks name (logs, outputs) is written under `./artifacts/` in this package.
Start sha: 441ab803236e03d522f0ac1c2e7ae56fe3167bf6
Diff against the start snapshot: 
diff --git a/tests/unit/test_ccsession_tiers.py b/tests/unit/test_ccsession_tiers.py
index df655a5d..edccd198 100644
--- a/tests/unit/test_ccsession_tiers.py
+++ b/tests/unit/test_ccsession_tiers.py
@@ -409,7 +409,8 @@ def test_default_tier_sets_model_and_tier_window(tmp_path: Path) -> None:
     assert _compact(seen, "claude-gw-tier1a") == 850000
     assert seen["custom"] == ""  # tiers are already in the picker
     assert seen["base_url"] == "http://127.0.0.1:4555"  # shim is always on
-    assert "tier2" in out and "muse-spark-1.3" in out
+    assert "tier2" in err and "muse-spark-1.3" in err
+    assert out == ""
 
 
 def test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier(
@@ -1466,6 +1467,8 @@ def _real_launch(tmp_path: Path, port: int | None, *args: str, **extra: str):
     """Launch the real script (fake claude) so it starts or reuses real shims.
 
     port None leaves CC_SHIM_PORT unset, so the script picks the port itself.
+    Returns the launcher's standard error (its status lines) and the base URL
+    the fake claude saw.
     """
     fake = tmp_path / "bin" / "claude"
     fake.parent.mkdir(exist_ok=True)
@@ -1494,7 +1497,8 @@ def _real_launch(tmp_path: Path, port: int | None, *args: str, **extra: str):
         timeout=60,
     )
     assert proc.returncode == 0, proc.stderr
-    return proc.stdout, (tmp_path / "seen").read_text().strip()
+    assert proc.stdout == ""  # the fake claude prints nothing; status is on stderr
+    return proc.stderr, (tmp_path / "seen").read_text().strip()
 
 
 def test_a_busy_shim_is_never_stopped_by_a_new_launch(tmp_path: Path) -> None:
@@ -2057,7 +2061,7 @@ def test_model_outside_tier_mode_stays_where_it_was_typed(tmp_path: Path) -> Non
     assert seen["argv"][-3:] == ["--model", "sonnet", "review this code"]
     rc, out, err, seen = _launch(tmp_path, "work", "--model=sonnet", defaults=None)
     assert rc == 0, err
-    assert "--model=sonnet" in seen["argv"] and "labeled 'work'" in out
+    assert "--model=sonnet" in seen["argv"] and "labeled 'work'" in err
 
 
 def test_launch_never_attaches_to_a_shim_that_won_the_port_race(

--- new untracked file .dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/t5-tiers-tests.log ---
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 5.0.0
rootdir: /home/coder/workspaces/worktrees/IronClaude/ic-issue-389
configfile: pyproject.toml
plugins: superclaude-5.0.0, anyio-4.16.0
collected 136 items

tests/unit/test_ccsession_tiers.py ..................................... [ 27%]
........................................................................ [ 80%]
...........................                                              [100%]

======================= 136 passed in 140.22s (0:02:20) ========================

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
