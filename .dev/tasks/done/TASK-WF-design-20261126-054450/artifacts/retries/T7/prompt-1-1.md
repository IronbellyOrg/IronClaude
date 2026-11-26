d4c7ff9ea65f39db5531ae3567fbd6f0162e01f5
Review one task for spec compliance.

Task brief: ## Task 7: Add the templates row and the template, listing and shipped-name tests

Depends on: Task 2, Task 4, Task 5, Task 6

In `tests/cli/test_install_keep.py` add the `templates` row to the table: call `install_templates(target_path=t, force=f)` (add the import), target `tmp_path / "templates"`, victim the first file under `workflow/`, noun `template`. In `test_plain_install_keeps_the_edit_and_makes_no_backup` the templates message must contain no `differ` text. Add these tests:

- `test_empty_and_binary_content_is_saved_exactly` (TR-008, templates row): set the victim to `b""`, force, then to bytes containing `\x00` and `\xff`, force; each backup equals those bytes.
- `test_nested_template_backup_and_excluded_folder` (TR-011, templates row): the backup sits in the victim's own subfolder; with `install_templates._get_templates_source` patched to a temporary source that holds `agent-memory/x.md` and one normal file, a differing `<target>/agent-memory/x.md` keeps its bytes and gets no `x.md.bak.*` after a forced run (a target-only file would pass even with the protected-folder guard removed, because the installer visits source files only). Moving the backup step above the protected-folder skip must make this test fail.
- `test_listings_ignore_backups` (TR-012): patch `Path.home` to `tmp_path` (as `tests/cli/test_how_we_work_install.py:33` does for the core listing); install core files, agents and templates with `force=True` into the home layout, then seed `.bak.` files (one with a `-2` suffix) in `~/.claude/templates/workflow/`, `~/.claude/agents/` and `~/.claude/`; `list_installed_templates()` omits them and equals `list_available_templates()` in length, and `list_installed_agents()` and `list_installed_core_files()` omit theirs.
- `test_no_shipped_template_name_contains_bak` (TR-013): no name in `list_available_templates()` contains `.bak.`.

Acceptance criteria:
- `uv run pytest tests/cli/test_install_keep.py tests/unit/test_cli_install.py tests/cli/test_how_we_work_install.py -q` passes, with TR-001 to TR-004, TR-006, TR-007, TR-009 and TR-010 running for the `templates` row and TR-008, TR-011, TR-012 and TR-013 present.
- TR-012 fails if the filter of Task 6 is removed.

AC ids:
- T7.AC1: `uv run pytest tests/cli/test_install_keep.py tests/unit/test_cli_install.py tests/cli/test_how_we_work_install.py -q` passes, with TR-001 to TR-004, TR-006, TR-007, TR-009 and TR-010 running for the `templates` row and TR-008, TR-011, TR-012 and TR-013 present.
- T7.AC2: TR-012 fails if the filter of Task 6 is removed.
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
Start sha: d4c7ff9ea65f39db5531ae3567fbd6f0162e01f5
Diff against the start snapshot: diff --git a/tests/cli/test_install_keep.py b/tests/cli/test_install_keep.py
index 974c98312..4be9fa4ea 100644
--- a/tests/cli/test_install_keep.py
+++ b/tests/cli/test_install_keep.py
@@ -20,10 +20,15 @@ from typing import Callable, NamedTuple
 import pytest
 
 from superclaude.cli import install_keep
+from superclaude.cli import install_templates as templates_mod
 from superclaude.cli import install_user_setup as setup
-from superclaude.cli.install_agents import install_agents
+from superclaude.cli.install_agents import install_agents, list_installed_agents
 from superclaude.cli.install_commands import install_commands
-from superclaude.cli.install_core import install_core_files
+from superclaude.cli.install_core import (
+    KNOWN_CORE_FILES,
+    install_core_files,
+    list_installed_core_files,
+)
 from superclaude.cli.install_keep import backup_if_differs, same_content
 
 STYLE = "pragmatic.md"
@@ -254,6 +259,19 @@ _ROWS = {
             key=lambda v, t: v.stem,
             kept_note=False,
         ),
+        _Row(
+            id="templates",
+            install=lambda t, f: templates_mod.install_templates(
+                target_path=t, force=f
+            ),
+            target=lambda tmp: tmp / "templates",
+            victims=lambda t: sorted(
+                p for p in (t / "workflow").rglob("*") if p.is_file()
+            ),
+            noun="template",
+            key=lambda v, t: str(v.relative_to(t)),
+            kept_note=False,
+        ),
     )
 }
 
@@ -446,3 +464,70 @@ def test_directory_at_the_victim_path_fails_closed(row, tmp_path):
     )
     assert victim.is_dir()
     assert not _victim_baks(victim)
+
+
+# --- templates only: content, nesting, excluded folder, listings --------------------
+
+
+def test_empty_and_binary_content_is_saved_exactly(tmp_path):
+    row = _ROWS["templates"]
+    target, victim = _installed_target(row, tmp_path)
+    victim.write_bytes(b"")
+    assert row.install(target, True)[0]
+    binary = b"head\x00middle\xfftail"
+    victim.write_bytes(binary)
+    assert row.install(target, True)[0]
+    assert sorted(b.read_bytes() for b in _victim_baks(victim)) == [b"", binary]
+
+
+def test_nested_template_backup_and_excluded_folder(tmp_path, monkeypatch):
+    row = _ROWS["templates"]
+    target, victim = _installed_target(row, tmp_path)
+    _edit(victim)
+    assert row.install(target, True)[0]
+    baks = _victim_baks(victim)
+    assert len(baks) == 1 and baks[0].parent == victim.parent  # its own subfolder
+
+    # The installer visits source files only, so the protected folder is tested with a
+    # temporary source that holds one: a target-only file would pass without the guard.
+    source = tmp_path / "source"
+    (source / "agent-memory").mkdir(parents=True)
+    (source / "agent-memory" / "x.md").write_text("shipped memory\n")
+    (source / "workflow").mkdir()
+    (source / "workflow" / "y.md").write_text("shipped y\n")
+    other = tmp_path / "other"
+    (other / "agent-memory").mkdir(parents=True)
+    (other / "agent-memory" / "x.md").write_text("USER MEMORY\n")
+    (other / "workflow").mkdir()
+    (other / "workflow" / "y.md").write_text("edited y\n")
+    monkeypatch.setattr(templates_mod, "_get_templates_source", lambda: source)
+    ok, message = templates_mod.install_templates(target_path=other, force=True)
+    assert ok, message
+    assert (other / "agent-memory" / "x.md").read_text() == "USER MEMORY\n"
+    assert not list((other / "agent-memory").glob("x.md.bak.*"))
+    assert [b.read_text() for b in sorted((other / "workflow").glob("y.md.bak.*"))] == [
+        "edited y\n"
+    ]
+
+
+def test_listings_ignore_backups(tmp_path, monkeypatch):
+    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
+    claude = tmp_path / ".claude"
+    assert install_core_files(force=True)[0]
+    assert install_agents(force=True)[0]
+    assert templates_mod.install_templates(force=True)[0]
+    template = sorted((claude / "templates" / "workflow").glob("*"))[0]
+    agent = sorted((claude / "agents").glob("*.md"))[0]
+    core = next(p for p in sorted(claude.glob("*.md")) if p.name in KNOWN_CORE_FILES)
+    for f in (template, agent, core):
+        (f.parent / (f.name + ".bak.20261126T000000Z")).write_text("old")
+        (f.parent / (f.name + ".bak.20261126T000000Z-2")).write_text("older")
+    installed = templates_mod.list_installed_templates()
+    assert not any(".bak." in n for n in installed)
+    assert len(installed) == len(templates_mod.list_available_templates())
+    assert not any(".bak." in n for n in list_installed_agents())
+    assert not any(".bak." in n for n in list_installed_core_files())
+
+
+def test_no_shipped_template_name_contains_bak():
+    assert not [n for n in templates_mod.list_available_templates() if ".bak." in n]

Task-owned evidence artifact artifacts/t7-test.log (a log the task wrote; cite it as ./artifacts/t7-test.log:<line>):
1: $ MUTATION CHECK: the Task 6 filter line removed from list_installed_templates (temporary, restored afterwards)
2: $ uv run pytest -p no:cacheprovider tests/cli/test_install_keep.py -q -k listings_ignore_backups
3:     assert not any(".bak." in n for n in installed)
4: E   assert not True
5: FAILED tests/cli/test_install_keep.py::test_listings_ignore_backups - assert ...
6: ======================= 1 failed, 50 deselected in 0.92s =======================
7: 
8: $ MUTATION CHECK 2: a backup attempt for files of the protected folder placed above the protected-folder skip in install_templates (temporary, restored afterwards)
9: $ uv run pytest -p no:cacheprovider tests/cli/test_install_keep.py -q -k nested_template_backup_and_excluded_folder
10: (the test then fails on: assert not [... agent-memory/x.md.bak.<stamp>], i.e. the protected-folder assertion)
11: product file restored byte-identical (cmp against the saved copy)
12: 
13: $ uv run pytest -p no:cacheprovider tests/cli/test_install_keep.py tests/unit/test_cli_install.py tests/cli/test_how_we_work_install.py -q
14: tests/cli/test_how_we_work_install.py .........                          [100%]
15: 
16: ============================= 154 passed in 1.98s ==============================
17: 
18: $ uv run pytest -p no:cacheprovider tests/cli/test_install_keep.py -v -k "templates or listings or bak or binary or nested"
19: test_forced_install_saves_a_differing_file_then_replaces_it[templates] PASSED [  6%]
20: test_forced_install_of_a_matching_or_missing_file_makes_no_backup[templates] PASSED [ 13%]
21: test_a_second_forced_run_makes_no_further_backup[templates] PASSED [ 20%]
22: test_plain_install_keeps_the_edit_and_makes_no_backup[templates] PASSED [ 26%]
23: test_core_kept_note_names_the_bak_naming PASSED [ 33%]
24: test_failed_save_leaves_the_file_untouched[templates-permission] PASSED [ 40%]
25: test_failed_save_leaves_the_file_untouched[templates-enospc] PASSED [ 46%]
26: test_save_then_failed_replacement_keeps_the_backup[templates] PASSED [ 53%]
27: test_backup_names_do_not_collide_on_one_instant[templates] PASSED [ 60%]
28: test_same_size_same_mtime_edit_is_saved_when_forced[templates] PASSED [ 66%]
29: test_directory_at_the_victim_path_fails_closed[templates] PASSED [ 73%]
30: test_empty_and_binary_content_is_saved_exactly PASSED [ 80%]
31: test_nested_template_backup_and_excluded_folder PASSED [ 86%]
32: test_listings_ignore_backups PASSED      [ 93%]
33: test_no_shipped_template_name_contains_bak PASSED [100%]
34: ====================== 15 passed, 36 deselected in 1.17s =======================
35: 

Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:51:49Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-676
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-676
call codegraph only when index_state: fresh, never to widen scope
Q2b: test-only change in tests/cli/test_install_keep.py (no production symbol changed; src/superclaude/cli/install_templates.py was edited and restored byte-identical during the mutation checks in ./artifacts/t7-test.log, so it is not in the diff). Production symbols the tests exercise: install_templates and list_installed_templates (Tasks 5, 6), install_agents / list_installed_agents (Task 3), install_core_files / list_installed_core_files / KNOWN_CORE_FILES (Task 1). Failure key for templates is str(rel) (install_templates.py:84-86).
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
