99d4b284f1ea757b3cf4cde3b007e52edb7bb8f2
Review one task for spec compliance.

Task brief: ## Task 8: Add eval version-check tests for wrapped launcher output

Depends on: Task 2

In `tests/cli/eval/test_doctor_version.py` (the file imports `_check_claude_version` and `doctor_module`; its existing cases pass lambda probes), add:
- A pure parser test: `_parse_version` (import it from `superclaude.cli.eval.commands`) applied to the text Claude's real output then the launcher's standard error, `"2.1.318 (Claude Code)\n[ccsession] Shim already running on 127.0.0.1:4078 (reusing)"`, returns `(2, 1, 318)`. Write the expected text as a single Python string literal so no line of the test file starts with a digit.
- A parser fixture that keeps the old formats working: `claude 0.5.0` and `claude 0.7.3 (build 12)` still parse to `(0, 5, 0)` and `(0, 7, 3)`.
- A real-probe test: create a stand-in `claude` shell script in `tmp_path` that prints `2.1.318 (Claude Code)` on standard output and `[ccsession] Shim already running on 127.0.0.1:4078 (reusing)` on standard error, make it executable, put `tmp_path` first on `PATH` with `monkeypatch.setenv`, call `_check_claude_version()` with no probe (so the real `_default_claude_version_probe` runs) and assert `status.passed is True` and `status.detail == "claude 2.1.318"`.

Do not add a test for the case where standard output is empty; that behavior belongs to the separate eval hardening decision.

Acceptance criteria:
- The three tests pass on the fixed launcher scripts (they do not start `ccsession`, so they also pass on the unfixed tree: they are contract guards for the stdout-first ordering that makes the fix work, not failing-first tests).
- `uv run pytest tests/cli/eval -q -p no:cacheprovider` passes; its output is saved to `./artifacts/t8-eval-tests.log`.

AC ids:
T8.AC1: The three tests pass on the fixed launcher scripts (they do not start `ccsession`, so they also pass on the unfixed tree: they are contract guards for the stdout-first ordering that makes the fix work, not failing-first tests).
T8.AC2: `uv run pytest tests/cli/eval -q -p no:cacheprovider` passes; its output is saved to `./artifacts/t8-eval-tests.log`.

(Repository root: /home/coder/workspaces/worktrees/IronClaude/ic-issue-389. The task's own evidence files `./artifacts/...` live in /home/coder/workspaces/worktrees/IronClaude/ic-issue-389/.dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/ .)
Global constraints: - Scope is the launcher scripts `src/superclaude/skills/ccsession-tag/ccsession` and `src/superclaude/skills/ccsession-tag/ccsession-orca`, the tests that read their output, `CHANGELOG.md` and the skill `README.md`. `src/superclaude/skills/ccsession-tag/models.py` is not edited: its two `[ccsession]` notes (line 313 `model list updated`, line 837 `model data check`) are routed to standard error at their one call site in `ccsession` (line 1733), so the documented `ccsession --refresh-models` report keeps printing on standard output.
- `src/superclaude/cli/eval/commands.py` (the version probe and `_parse_version`) is not edited. Hardening it (treat a non-zero exit code as "not callable", prefer the `X.Y.Z (Claude Code)` form) is a separate pending decision and must not be added here. Its failure-path behavior (stdout empty because the launcher exited early) is deliberately not pinned by any test in this plan.
- These stay on standard output because the shell captures them: every `models.py` print captured with `$(...)` in `ccsession` (the `PROFILE_*=` lines, digests, shim port, tier lists, compact settings, the `models` and `status` reports), and the values printed by `ccsession --ask`, `--auto-name`, `--list`, `--rm`, `--refresh-models` and `--models-status`.
- Existing `>&2` warnings and errors (`ccsession` lines 823, 944, 973, 980, 1002, 1013, 1080, 1856; `ccsession-orca` lines 136, 211) are correct and stay as they are.
- Edit only under `src/superclaude/skills/ccsession-tag/`, `tests/` and `CHANGELOG.md`. Do not edit `.claude/` mirrors by hand; `make sync-dev` is the only way they change and they are never staged.
- Hardening closure for this fix: the replay run recorded in Task 2 is the positive witness (the negative witness was run before this plan on the unfixed tree), Task 8 supplies the parser fixtures, and the executor's final independent review is the off-path review.
- Evidence the tasks name (logs, outputs) is written under `./artifacts/` in this package.
Start sha: 99d4b284f1ea757b3cf4cde3b007e52edb7bb8f2
Diff against the start snapshot: 
diff --git a/tests/cli/eval/test_doctor_version.py b/tests/cli/eval/test_doctor_version.py
index 48176104..f24a7509 100644
--- a/tests/cli/eval/test_doctor_version.py
+++ b/tests/cli/eval/test_doctor_version.py
@@ -19,6 +19,7 @@ These tests cover the four acceptance criteria from the phase tasklist:
 
 from __future__ import annotations
 
+import os
 import shutil
 from pathlib import Path
 
@@ -29,6 +30,7 @@ from superclaude.cli.eval import commands as doctor_module
 from superclaude.cli.eval.commands import (
     HARD_FAIL_EXIT_CODE,
     _check_claude_version,
+    _parse_version,
     build_doctor_report,
     eval_group,
 )
@@ -183,3 +185,41 @@ def test_cli_doctor_exits_two_when_stub_reports_0_4_0(
     assert result.exit_code == HARD_FAIL_EXIT_CODE
     assert "claude.min_version" in result.stderr
     assert "< required 0.5.0" in result.stderr
+
+
+# ---------------------------------------------------------------------------
+# Wrapped launcher: ccsession prints its notices on stderr (issue 389), so the
+# probe text is Claude's own version first, then any launcher notice. The
+# parser reads the first X.Y.Z, which must be Claude's.
+# ---------------------------------------------------------------------------
+
+
+def test_parse_version_takes_claude_before_launcher_stderr() -> None:
+    text = "2.1.318 (Claude Code)\n[ccsession] Shim already running on 127.0.0.1:4078 (reusing)"
+    assert _parse_version(text) == (2, 1, 318)
+
+
+@pytest.mark.parametrize(
+    ("text", "expected"),
+    [("claude 0.5.0", (0, 5, 0)), ("claude 0.7.3 (build 12)", (0, 7, 3))],
+)
+def test_parse_version_keeps_older_formats(
+    text: str, expected: tuple[int, ...]
+) -> None:
+    assert _parse_version(text) == expected
+
+
+def test_real_probe_reads_claude_version_not_the_launcher_notice(
+    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
+) -> None:
+    stand_in = tmp_path / "claude"
+    stand_in.write_text(
+        "#!/bin/sh\n"
+        "echo '2.1.318 (Claude Code)'\n"
+        "echo '[ccsession] Shim already running on 127.0.0.1:4078 (reusing)' >&2\n"
+    )
+    stand_in.chmod(0o755)
+    monkeypatch.setenv("PATH", f"{tmp_path}{os.pathsep}{os.environ['PATH']}")
+    status = _check_claude_version()
+    assert status.passed is True
+    assert status.detail == "claude 2.1.318"

--- new untracked file .dev/tasks/to-do/TASK-WF-fixIssue389Ironb-20261105-174606/artifacts/t8-eval-tests.log ---
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 5.0.0
rootdir: /home/coder/workspaces/worktrees/IronClaude/ic-issue-389
configfile: pyproject.toml
plugins: superclaude-5.0.0, anyio-4.16.0
collected 1502 items

tests/cli/eval/test_artifact_layout.py ...................               [  1%]
tests/cli/eval/test_artifact_reproducibility.py ........                 [  1%]
tests/cli/eval/test_atomic_setup.py ...................                  [  3%]
tests/cli/eval/test_ban_import_rule.py ...                               [  3%]
tests/cli/eval/test_capability_classifications.py ....................   [  4%]
tests/cli/eval/test_capability_dataclass.py ................             [  5%]
tests/cli/eval/test_capability_gates.py ..................               [  6%]
tests/cli/eval/test_capability_report.py ..........                      [  7%]
tests/cli/eval/test_claude_process_adapter.py .............              [  8%]
tests/cli/eval/test_config.py ......                                     [  8%]
tests/cli/eval/test_containment.py ...............................       [ 10%]
tests/cli/eval/test_coverage_gate.py ...........................         [ 12%]
tests/cli/eval/test_coverage_gate_integration.py ......                  [ 13%]
tests/cli/eval/test_defense_in_depth.py ...................              [ 14%]
tests/cli/eval/test_describe.py .........................                [ 15%]
tests/cli/eval/test_disk_budget.py .................................     [ 18%]
tests/cli/eval/test_doctor.py .......................................... [ 20%]
......                                                                   [ 21%]
tests/cli/eval/test_doctor_version.py .................                  [ 22%]
tests/cli/eval/test_eval_context.py .............................        [ 24%]
tests/cli/eval/test_eval_group.py .....                                  [ 24%]
tests/cli/eval/test_eval_id_regex.py ................................... [ 27%]
................................                                         [ 29%]
tests/cli/eval/test_eval_lifecycle.py ......................             [ 30%]
tests/cli/eval/test_eval_outcome.py ........................             [ 32%]
tests/cli/eval/test_eval_result.py ................                      [ 33%]
tests/cli/eval/test_eval_run.py .................                        [ 34%]
tests/cli/eval/test_exit_codes.py .s.s.                                  [ 34%]
tests/cli/eval/test_expect_duration.py ...................               [ 36%]
tests/cli/eval/test_expect_exit_code.py ....................             [ 37%]
tests/cli/eval/test_expect_failure.py .............                      [ 38%]
tests/cli/eval/test_expect_file.py ..................                    [ 39%]
tests/cli/eval/test_expect_jsonl.py ...................                  [ 40%]
tests/cli/eval/test_expect_primitives.py ...........................     [ 42%]
tests/cli/eval/test_expect_result.py ............                        [ 43%]
tests/cli/eval/test_expect_settings_json.py .....................        [ 44%]
tests/cli/eval/test_expect_stdio.py .......................              [ 46%]
tests/cli/eval/test_hard_guard_real_home.py ......                       [ 46%]
tests/cli/eval/test_home_isolation.py ...........................        [ 48%]
tests/cli/eval/test_home_isolation_extend.py ........................... [ 50%]
............                                                             [ 51%]
tests/cli/eval/test_hook_adapter.py ............                         [ 51%]
tests/cli/eval/test_isolation_dataclass.py ............................. [ 53%]
...                                                                      [ 53%]
tests/cli/eval/test_isolation_layers_probe.py .............              [ 54%]
tests/cli/eval/test_list.py ...................                          [ 56%]
tests/cli/eval/test_mcp_retry_once.py ..........................         [ 57%]
tests/cli/eval/test_no_mcp_skip.py ...........s                          [ 58%]
tests/cli/eval/test_no_pty_exclusion.py ..............                   [ 59%]
tests/cli/eval/test_no_shared_state.py ..........                        [ 60%]
tests/cli/eval/test_orchestrator.py ......................               [ 61%]
tests/cli/eval/test_parallel_15.py .......                               [ 62%]
tests/cli/eval/test_path_containment.py ................................ [ 64%]
...............                                                          [ 65%]
tests/cli/eval/test_path_traversal.py ...............                    [ 66%]
tests/cli/eval/test_perf_home_setup.py .                                 [ 66%]
tests/cli/eval/test_perf_resource_bounds.py ..                           [ 66%]
tests/cli/eval/test_phase_report_probe.py .........................      [ 68%]
tests/cli/eval/test_pty_driver.py .....................                  [ 69%]
tests/cli/eval/test_pty_lifecycle.py .....                               [ 69%]
tests/cli/eval/test_pty_stream.py ..............................         [ 71%]
tests/cli/eval/test_reporter.py .........................                [ 73%]
tests/cli/eval/test_reporter_contract.py ....                            [ 73%]
tests/cli/eval/test_retention_policy.py ....s.                           [ 74%]
tests/cli/eval/test_retry_policy.py ...........                          [ 74%]
tests/cli/eval/test_run_report.py ...................                    [ 76%]
tests/cli/eval/test_run_summary.py .........................             [ 77%]
tests/cli/eval/test_runner_class.py ...........                          [ 78%]
tests/cli/eval/test_schema_id_rejection.py ....................          [ 79%]
tests/cli/eval/test_schema_load.py .............                         [ 80%]
tests/cli/eval/test_schema_validate.py ..............                    [ 81%]
tests/cli/eval/test_scratch_root_allowlist.py ....................       [ 83%]
tests/cli/eval/test_scratch_root_policy.py ..................            [ 84%]
tests/cli/eval/test_signal_handling.py .........................         [ 85%]
tests/cli/eval/test_single_command.py ..                                 [ 86%]
tests/cli/eval/test_suite_loader.py .........................            [ 87%]
tests/cli/eval/test_suite_runtime.py .......                             [ 88%]
tests/cli/eval/test_summary_schema.py .................                  [ 89%]
tests/cli/eval/test_symlink_attacks.py ..............                    [ 90%]
tests/cli/eval/test_tavily_eval_capability.py ...                        [ 90%]
tests/cli/eval/test_validation_commands.py ..................            [ 91%]
tests/cli/eval/test_workflow_vs_task_builder_companion.py .............. [ 92%]
........................................................................ [ 97%]
.......................................                                  [100%]

======================= 1498 passed, 4 skipped in 36.64s =======================

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
