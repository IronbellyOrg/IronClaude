d936a9c23f11223e186e32fd0a77ea8f6f9badce
Review one task for spec compliance.

Task brief: ## Task 10: Add the real failed-save update test and run the full install-related test set

Depends on: Task 1, Task 8

In `tests/cli/test_update_command.py` add the test for TR-017: after `native_install`, edit `<home>/.claude/RULES.md`; replace `shutil.copy2` with a wrapper around the real function that raises `OSError` only when the destination name starts with `RULES.md.bak.`; run `CliRunner().invoke(main, ["update", "--target", str(target)])`. Assert exit code 1; the output contains `RULES.md: could not save a copy first, left untouched`; the output contains exactly one `❌ Failed`; the victim's bytes are unchanged. Because only the victim's backup is failed, the hooks phase still writes its own `settings.json.bak.<stamp>`, so exit code 1 can come only from the new guard.

Run `make sync-dev` before the gate commands below, so the gitignored `.claude/` mirrors exist for `tests/cli/test_verify_sync_hooks.py`.

Acceptance criteria:
- `uv run pytest tests/cli/test_update_command.py -q` passes with the test present.
- `uv run pytest tests/cli/test_install_keep.py tests/cli/test_update_command.py tests/cli/test_install_failures.py tests/cli/test_how_we_work_install.py tests/commands/test_routing_plugin_parity.py tests/docs/test_onboarding_deck.py tests/unit/test_cli_install.py -q` passes.
- `uv run pytest tests/cli tests/unit -q` passes.

AC ids:
- T10.AC1: `uv run pytest tests/cli/test_update_command.py -q` passes with the test present.
- T10.AC2: `uv run pytest tests/cli/test_install_keep.py tests/cli/test_update_command.py tests/cli/test_install_failures.py tests/cli/test_how_we_work_install.py tests/commands/test_routing_plugin_parity.py tests/docs/test_onboarding_deck.py tests/unit/test_cli_install.py -q` passes.
- T10.AC3: `uv run pytest tests/cli tests/unit -q` passes.
Global constraints: ## Constraints

- Scope: change only `src/superclaude/cli/install_core.py`, `install_agents.py`, `install_templates.py` (and the docstring of `install_keep.py`), tests under `tests/cli/`, the documentation files named in the tasks, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (the routing-guide copy) and `CHANGELOG.md`. Do not change `src/superclaude/cli/main.py`. Do not change the logic of `backup_if_differs`, `same_content` or `_backup_target`. Add no shared helper function and no code that deletes backups.
- Non-goals: no stale-file notes for agents and templates on a plain `install` (recorded as a follow-up), no change to skill-folder or hook-script copying, no rollback of a failed replacement, no change to `README.md:68` (a 6.0.0 section pinned to `@v6.0.0`), no change to released CHANGELOG entries, `docs/testing/`, `docs/designs/` or `docs/docs-product/`.
- Never hand-edit or stage a path under `.claude/`; regenerate the gitignored mirrors with `make sync-dev`, whose output is never staged. Edit the file under `src/superclaude/` or `plugins/` instead.
- Line numbers in the tasks are as at HEAD 3cf7e2259; locate by the quoted text if an earlier task shifted them.
- When commits are requested, make one per work package as in `./source.md` section 6: each installer's code together with its test row, and the docstring, guide copy and CHANGELOG with the documentation. `/sc:implement` itself never commits.
- The helper contract (unchanged): `backup_if_differs(shipped: Path, target: Path) -> Path | None` in `src/superclaude/cli/install_keep.py` returns `None` when the bytes match, otherwise copies `target` to `<name>.bak.<YYYYmmddTHHMMSSZ>` beside it (a `-2`, `-3` suffix while that name exists) and returns that path; it raises `OSError` when the copy fails, and the caller must then leave `target` untouched.
- Exact strings every installer uses. Saved block, printed only when `backed_up` is non-empty, after the skipped and kept notes and before the failed block: the text `\n💾 Saved {n} changed {noun}(s) before overwriting:` and then one line `   - {backup path}` per saved copy; nouns are `core file`, `agent`, `template`. Failure line, added to `failed`: `<key>: could not save a copy first, left untouched (<error>)`.
- Pattern to copy for the code tasks: `src/superclaude/cli/install_commands.py` lines 54-82 (the backup step with its own `try`/`except OSError`, then the copy `try`) and 108-113 (the saved block).
- Terms: the six backed-up categories are commands, rules, output styles, core files, agents and templates. Skill folders (deleted and re-copied) and hook scripts (`src/superclaude/cli/install_hooks.py:286-287`, a plain `shutil.copy2`) are overwritten with no copy. The word "excluded" names the `agent-memory` folder the template installer never writes.
- Documentation wording kit (use the pieces the task names; keep the wording the same in every file). W-1: "`superclaude install --force` and `superclaude update` overwrite every file they ship. When a command, rule, output-style, core, agent or template file differs from the shipped one, the installer first saves a copy next to it as `<name>.bak.<UTC time>`. Skill folders (deleted and re-copied) and hook scripts get no copy." W-2: "Copy any file you changed or added inside a skill folder, and any hook script you changed, to a place outside `~/.claude/skills/` before you run either command." W-3: "Releases 6.1.0 and earlier overwrite core files, agents and templates with no copy." W-4: "`could not save a copy first, left untouched`: the installer could not write the `.bak.` copy next to a file, because the folder is not writable, the disk is full, the file cannot be read, or a folder sits at the file's path. That file is left as it is, the run lists it under the failed files, and `superclaude install --force` or `superclaude update` exits 1. Make the folder writable or free space and run the command again, or move the file aside yourself. A `.bak.` file left behind by a failed save may be incomplete."
- Test conventions: run tests with `uv run pytest`; never `python -m` or bare `pip`. Unit tests live in `tests/cli/test_install_keep.py` (existing helpers `_baks` at line 32 and `_rewrite_keeping_stat` at line 39; existing failed-save tests at lines 144-157 and 202-214 patch `install_keep.shutil.copy2`, which is the same `shutil` module the installers call).
Start sha: d936a9c23f11223e186e32fd0a77ea8f6f9badce
Diff against the start snapshot: diff --git a/tests/cli/test_update_command.py b/tests/cli/test_update_command.py
index ba9e3b56d..0d2bfd44c 100644
--- a/tests/cli/test_update_command.py
+++ b/tests/cli/test_update_command.py
@@ -4,6 +4,7 @@ from __future__ import annotations
 
 import json
 import os
+import shutil
 import subprocess
 from pathlib import Path
 from types import SimpleNamespace
@@ -385,6 +386,31 @@ def test_install_keeps_edits_and_update_saves_them_first(native_install):
         assert [b.read_bytes() for b in _victim_baks(victim)] == [b"my own edit\n"]
 
 
+def test_update_exits_one_when_the_core_file_copy_cannot_be_saved(
+    native_install, monkeypatch
+):
+    home, target = native_install
+    victim = home / ".claude/RULES.md"
+    victim.write_bytes(b"my own edit\n")
+    real_copy2 = shutil.copy2
+
+    def copy2(src, dst, *args, **kwargs):
+        if Path(dst).name.startswith("RULES.md.bak."):
+            raise OSError("No space left on device")
+        return real_copy2(src, dst, *args, **kwargs)
+
+    monkeypatch.setattr(shutil, "copy2", copy2)
+
+    result = CliRunner().invoke(main, ["update", "--target", str(target)])
+
+    # Only the victim's saved copy fails: the hooks phase still writes its own
+    # settings.json.bak.<stamp>, so exit code 1 can come only from the new guard.
+    assert result.exit_code == 1, result.output
+    assert "RULES.md: could not save a copy first, left untouched" in result.output
+    assert result.output.count("❌ Failed") == 1
+    assert victim.read_bytes() == b"my own edit\n"
+
+
 def test_install_runs_codegraph_phase_after_user_setup_before_retire(monkeypatch):
     calls = _stub_installers(monkeypatch)
     result = CliRunner().invoke(main, ["install"])

Task-owned evidence artifact artifacts/t10-test.log (a log the task wrote; cite it as ./artifacts/t10-test.log:<line>):
1: $ make sync-dev   (gitignored .claude/ mirrors; never staged)
2:    Commands:  36 files
3:    Hooks:     17 files
4:    Templates: 52 files
5: git status --porcelain -- .claude: []
6: 
7: $ uv run pytest -p no:cacheprovider tests/cli/test_update_command.py -q
8: tests/cli/test_update_command.py ................................        [100%]
9: 
10: ============================== 32 passed in 2.54s ==============================
11: 
12: $ uv run pytest -p no:cacheprovider tests/cli/test_install_keep.py tests/cli/test_update_command.py tests/cli/test_install_failures.py tests/cli/test_how_we_work_install.py tests/commands/test_routing_plugin_parity.py tests/docs/test_onboarding_deck.py tests/unit/test_cli_install.py -q
13: .....................................................                    [100%]
14: 
15: ============================= 198 passed in 4.19s ==============================
16: 
17: $ uv run pytest -p no:cacheprovider tests/cli tests/unit -q
18:   /home/coder/workspaces/worktrees/IronClaude/issue-676/tests/cli/reflect/test_contract_status_cli.py:157: DeprecationWarning: 'isolated_filesystem' is deprecated and will be removed in Click 9.0. Use 'tempfile.TemporaryDirectory' or pytest's 'tmp_path' fixture with absolute paths instead.
19:     with cli_runner.isolated_filesystem():
20: 
21: tests/cli/reflect/test_contract_status_cli.py::test_contract_status_validate_output_redacts_raw_payload_body
22:   /home/coder/workspaces/worktrees/IronClaude/issue-676/tests/cli/reflect/test_contract_status_cli.py:259: DeprecationWarning: 'isolated_filesystem' is deprecated and will be removed in Click 9.0. Use 'tempfile.TemporaryDirectory' or pytest's 'tmp_path' fixture with absolute paths instead.
23:     with cli_runner.isolated_filesystem() as fs:
24: 
25: -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
26: =========================== short test summary info ============================
27: FAILED tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval
28: FAILED tests/cli/eval/test_claude_process_adapter.py::test_ruff_passes_on_real_adapter_module
29: ====== 2 failed, 3295 passed, 7 skipped, 5 warnings in 501.43s (0:08:21) =======
30: 
31: NOTE: the two failures above are environmental (.venv/bin/python: No module named ruff, raised by tests/cli/eval/test_claude_process_adapter.py::test_ruff_*; neither file is touched by this change). Fix: uv pip install ruff (dev dependency of the project; no repo file changes).
32: $ uv run pytest -p no:cacheprovider tests/cli/eval/test_claude_process_adapter.py -q
33: 
34: ============================== 13 passed in 1.11s ==============================
35: 

Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:51:49Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-676
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-676
call codegraph only when index_state: fresh, never to widen scope
Q2b: test-only change in tests/cli/test_update_command.py (one new test and `import shutil`); no production symbol changed. The test exercises update (src/superclaude/cli/main.py:356) and the core installer's failure path (Task 1). The task text says to run `make sync-dev` before the gate commands: the log records it (gitignored output, nothing under .claude/ is staged or shows in git status). The two failures in the full tests/cli + tests/unit run were environmental (ruff not installed in the venv, tests/cli/eval/test_claude_process_adapter.py); the log records the dev-dependency install and the rerun of that file (13 passed). The full 8-minute suite was not rerun after that install.
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
