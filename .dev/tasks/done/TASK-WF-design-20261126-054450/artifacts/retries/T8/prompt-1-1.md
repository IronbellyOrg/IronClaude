e86b35357cf6cc9bf96c2a8fb721b30df0a766d8
Review one task for spec compliance.

Task brief: ## Task 8: Add the install --list count and the install-then-update happy-path tests to tests/cli/test_update_command.py

Depends on: Task 1, Task 3, Task 5, Task 6

In `tests/cli/test_update_command.py` (existing fixtures: the autouse `isolated_home_guard` at line 34, which pins HOME and `CLAUDE_CONFIG_DIR` under `tmp_path`; `native_install` at line 188, which runs a real `install --target <home>/.claude/commands/sc` and returns `(home, target)`; the existing real update call at line 240 is `CliRunner().invoke(main, ["update", "--target", str(target)])`) add:

- A test for TR-014: after `native_install`, edit one template under `<home>/.claude/templates/workflow/`, call `install_templates(force=True)` directly (with `Path.home` patched as `native_install` does), assert that exactly one `<victim>.bak.*` holding the edit now exists beside the victim, then `CliRunner().invoke(main, ["install", "--list"])` with the listings not stubbed; the output contains `Templates: N available, N installed` with equal N and the listing writes no file. The count check holds only in this isolated home.
- A test for TR-015: after `native_install`, edit `<home>/.claude/RULES.md`, one `<home>/.claude/agents/*.md` and one template. Run `install` with no force: exit code 0, the three edits kept, and no `<victim>.bak.*` file. Then run `update --target <target>`: exit code 0 and exactly one `<victim>.bak.*` beside each victim holding the edited bytes. Count with `sorted(victim.parent.glob(victim.name + ".bak.*"))` per victim, never with the folder-wide `_baks(~/.claude)`, because the hook installer writes `settings.json.bak.<stamp>` in `~/.claude/` on every run (`src/superclaude/cli/install_hooks.py:336-346`).

Acceptance criteria:
- `uv run pytest tests/cli/test_update_command.py -q` passes with both tests present.
- Both tests isolate core files, agents and templates through the pinned HOME, not through `--target` (which redirects only the commands installer, as `test_install_force_target_do_not_redirect` at line 255 pins).
- The existing tests in the file are unchanged.

AC ids:
- T8.AC1: `uv run pytest tests/cli/test_update_command.py -q` passes with both tests present.
- T8.AC2: Both tests isolate core files, agents and templates through the pinned HOME, not through `--target` (which redirects only the commands installer, as `test_install_force_target_do_not_redirect` at line 255 pins).
- T8.AC3: The existing tests in the file are unchanged.
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
Start sha: e86b35357cf6cc9bf96c2a8fb721b30df0a766d8
Diff against the start snapshot: diff --git a/tests/cli/test_update_command.py b/tests/cli/test_update_command.py
index a341865fa..59b983232 100644
--- a/tests/cli/test_update_command.py
+++ b/tests/cli/test_update_command.py
@@ -11,6 +11,7 @@ from types import SimpleNamespace
 import pytest
 from click.testing import CliRunner
 
+from superclaude.cli.install_templates import install_templates
 from superclaude.cli.main import main
 
 _INSTALLERS = (
@@ -277,6 +278,60 @@ def test_install_force_target_do_not_redirect(monkeypatch, isolated_home_guard):
     }
 
 
+def _victim_baks(victim: Path) -> list[Path]:
+    """Saved copies of this one file. Never count ``~/.claude`` as a whole: the hook
+    installer writes ``settings.json.bak.<stamp>`` there on every run."""
+    return sorted(victim.parent.glob(victim.name + ".bak.*"))
+
+
+def test_install_list_does_not_count_saved_template_copies(native_install):
+    home, _ = native_install
+    victim = sorted((home / ".claude/templates/workflow").glob("*"))[0]
+    victim.write_bytes(b"my own edit\n")
+    ok, message = install_templates(force=True)
+    assert ok, message
+    assert [b.read_bytes() for b in _victim_baks(victim)] == [b"my own edit\n"]
+    before = sorted(str(p) for p in home.rglob("*"))
+
+    result = CliRunner().invoke(main, ["install", "--list"])
+
+    assert result.exit_code == 0, result.output
+    line = next(
+        text for text in result.output.splitlines() if text.startswith("Templates:")
+    )
+    available, installed = (
+        int(w) for w in line.replace(",", "").split() if w.isdigit()
+    )
+    assert available == installed
+    assert (
+        sorted(str(p) for p in home.rglob("*")) == before
+    )  # the listing writes no file
+
+
+def test_install_keeps_edits_and_update_saves_them_first(native_install):
+    home, target = native_install
+    claude = home / ".claude"
+    victims = [
+        claude / "RULES.md",
+        sorted((claude / "agents").glob("*.md"))[0],
+        sorted((claude / "templates/workflow").glob("*"))[0],
+    ]
+    for victim in victims:
+        victim.write_bytes(b"my own edit\n")
+
+    result = CliRunner().invoke(main, ["install"])
+    assert result.exit_code == 0, result.output
+    for victim in victims:
+        assert victim.read_bytes() == b"my own edit\n"
+        assert not _victim_baks(victim)
+
+    result = CliRunner().invoke(main, ["update", "--target", str(target)])
+    assert result.exit_code == 0, result.output
+    for victim in victims:
+        assert victim.read_bytes() != b"my own edit\n"
+        assert [b.read_bytes() for b in _victim_baks(victim)] == [b"my own edit\n"]
+
+
 def test_install_runs_codegraph_phase_after_user_setup_before_retire(monkeypatch):
     calls = _stub_installers(monkeypatch)
     result = CliRunner().invoke(main, ["install"])

Task-owned evidence artifact artifacts/t8-test.log (a log the task wrote; cite it as ./artifacts/t8-test.log:<line>):
1: $ uv run pytest -p no:cacheprovider tests/cli/test_update_command.py -q
2: 
3: tests/cli/test_update_command.py ......................                  [100%]
4: 
5: ============================== 22 passed in 2.60s ==============================
6: 
7: $ uv run pytest -p no:cacheprovider tests/cli/test_update_command.py -v -k "saved_template_copies or update_saves_them"
8: test_install_list_does_not_count_saved_template_copies PASSED [ 50%]
9: test_install_keeps_edits_and_update_saves_them_first PASSED [100%]
10: ======================= 2 passed, 20 deselected in 1.44s =======================
11: 
12: $ git diff --stat -- tests/cli/test_update_command.py (only additions, existing tests unchanged)
13:  tests/cli/test_update_command.py | 55 ++++++++++++++++++++++++++++++++++++++++
14:  1 file changed, 55 insertions(+)
15: removed lines in the diff: 0
16: 

Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:51:49Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-676
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-676
call codegraph only when index_state: fresh, never to widen scope
Q2b: test-only change in tests/cli/test_update_command.py; no production symbol changed. It exercises install (src/superclaude/cli/main.py:46, calls at 180,198,229), update (main.py:356, calls at 383,396,417) and list_installed_templates (main.py:144). The fixtures it uses (isolated_home_guard line 34, native_install line ~190) are unchanged.
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
