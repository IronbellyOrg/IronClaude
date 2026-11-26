ef8a2b333495e0bb50a452d53d88f52527c31830
Review one task for spec compliance.

Task brief: ## Task 5: Save a differing template file before a forced overwrite in install_templates

In `src/superclaude/cli/install_templates.py`, function `install_templates(target_path, force)` (line 30):

- Add `from .install_keep import backup_if_differs` after line 22 (`from typing import List, Tuple`).
- Add `backed_up: List[str] = []` beside `installed`, `skipped` and `failed` (lines 54-56).
- In the loop over the sorted source files, after the excluded-folder skip (`if any(p in _PROTECTED_TARGET_SUBDIRS for p in rel.parts): continue`, lines 67-68), after `dest = target_path / rel` (line 70) and the skip path (`if dest.exists() and not force:` ... `continue`, lines 71-73), and before the `try:` at line 74, add the backup step: when `dest.exists()`, in its own `try`, call `backup_if_differs(src_file, dest)`; append a returned path to `backed_up` as `str(path)`; on `OSError as e` append `f"{rel}: could not save a copy first, left untouched ({e})"` to `failed` and `continue`. The existing `try` (which holds `dest.parent.mkdir` and `shutil.copy2`) and its `except Exception` stay unchanged; no new `mkdir` is needed because a backup exists only when `dest` exists.
- Print the saved block (noun `template`) after the skipped block (lines 86-91) and before the failed block (line 92).
- Add no kept-but-different note.

Acceptance criteria:
- `install_templates(target_path=t, force=True)` over an edited nested template such as `t/workflow/<file>` leaves the shipped bytes in it, exactly one `t/workflow/<file>.bak.<stamp>` in the same subfolder with the old bytes, and a message containing `Saved 1 changed template(s) before overwriting:` and the path.
- With `install_templates._get_templates_source` patched to a temporary source that holds `agent-memory/x.md` and one normal file, a differing `t/agent-memory/x.md` keeps its bytes and gets no backup (the shipped source has no `agent-memory` folder, so the real source cannot show this); a byte-identical template, an empty target and `force=False` make no backup.
- A failed backup leaves the template unchanged, lists `<rel>: could not save a copy first, left untouched (<error>)` under `❌ Failed to install`, returns `False`, and the other templates are still installed.
- `uv run pytest tests/cli/test_install_failures.py tests/unit/test_cli_install.py tests/cli/test_update_command.py tests/cli/test_install_retired_files.py -q` passes: the existing callers of `install_templates` run without force or force-install into an empty target, except the real `update` in `test_update_command.py` and `test_install_retired_files.py`, which force over existing files and reach the new backup call.

AC ids:
- T5.AC1: `install_templates(target_path=t, force=True)` over an edited nested template such as `t/workflow/<file>` leaves the shipped bytes in it, exactly one `t/workflow/<file>.bak.<stamp>` in the same subfolder with the old bytes, and a message containing `Saved 1 changed template(s) before overwriting:` and the path.
- T5.AC2: With `install_templates._get_templates_source` patched to a temporary source that holds `agent-memory/x.md` and one normal file, a differing `t/agent-memory/x.md` keeps its bytes and gets no backup (the shipped source has no `agent-memory` folder, so the real source cannot show this); a byte-identical template, an empty target and `force=False` make no backup.
- T5.AC3: A failed backup leaves the template unchanged, lists `<rel>: could not save a copy first, left untouched (<error>)` under `❌ Failed to install`, returns `False`, and the other templates are still installed.
- T5.AC4: `uv run pytest tests/cli/test_install_failures.py tests/unit/test_cli_install.py tests/cli/test_update_command.py tests/cli/test_install_retired_files.py -q` passes: the existing callers of `install_templates` run without force or force-install into an empty target, except the real `update` in `test_update_command.py` and `test_install_retired_files.py`, which force over existing files and reach the new backup call.
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
Start sha: ef8a2b333495e0bb50a452d53d88f52527c31830
Diff against the start snapshot: diff --git a/src/superclaude/cli/install_templates.py b/src/superclaude/cli/install_templates.py
index d88a8eacf..91f2cfd95 100644
--- a/src/superclaude/cli/install_templates.py
+++ b/src/superclaude/cli/install_templates.py
@@ -21,6 +21,8 @@ import shutil
 from pathlib import Path
 from typing import List, Tuple
 
+from .install_keep import backup_if_differs
+
 # Files we refuse to ever write into the target directory (defensive —
 # the source tree shouldn't contain these names, but if it did, we
 # would still skip them).
@@ -54,6 +56,7 @@ def install_templates(
     installed: List[str] = []
     skipped: List[str] = []
     failed: List[str] = []
+    backed_up: List[str] = []
 
     for src_file in sorted(source.rglob("*")):
         if not src_file.is_file():
@@ -71,6 +74,17 @@ def install_templates(
         if dest.exists() and not force:
             skipped.append(str(rel))
             continue
+
+        # A forced overwrite first saves a differing file next to itself
+        try:
+            if dest.exists():
+                backup = backup_if_differs(src_file, dest)
+                if backup is not None:
+                    backed_up.append(str(backup))
+        except OSError as exc:
+            failed.append(f"{rel}: could not save a copy first, left untouched ({exc})")
+            continue
+
         try:
             dest.parent.mkdir(parents=True, exist_ok=True)
             shutil.copy2(src_file, dest)
@@ -89,6 +103,12 @@ def install_templates(
         )
         for rel in skipped:
             messages.append(f"   - {rel}")
+    if backed_up:
+        messages.append(
+            f"\n💾 Saved {len(backed_up)} changed template(s) before overwriting:"
+        )
+        for path in backed_up:
+            messages.append(f"   - {path}")
     if failed:
         messages.append(f"\n❌ Failed to install {len(failed)} templates:")
         for fail in failed:

Task-owned evidence artifact artifacts/t5-test.log (a log the task wrote; cite it as ./artifacts/t5-test.log:<line>):
1: $ uv run pytest -p no:cacheprovider tests/cli/test_install_failures.py tests/unit/test_cli_install.py tests/cli/test_update_command.py tests/cli/test_install_retired_files.py -q
2: tests/cli/test_install_retired_files.py ................................ [100%]
3: 
4: ============================= 150 passed in 5.34s ==============================
5: 
6: $ ad hoc behaviour check of install_templates (script /tmp/impl676/t5_check.py, not committed)
7: AC1 ok: True | replaced: True | one backup in the same subfolder with old bytes: True | Saved line: True | path in message: True
8: AC2 matching files, no new backup: True
9: AC2 empty target, no Saved: True
10: AC2 force=False keeps the edit, no backup added: True
11: AC2 agent-memory kept: True | no x.md backup: True | y.md replaced and saved: True
12: AC3 ok: False | untouched: True | failure line: True | under Failed block: True
13: AC3 other templates still installed: True | returns False: True
14: 

Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:51:49Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-676
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-676
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents of install_templates not in the diff (signature unchanged): src/superclaude/cli/main.py:229 (install), src/superclaude/cli/main.py:417 (update); tests: tests/cli/test_install_failures.py, tests/unit/test_cli_install.py:959, tests/cli/test_update_command.py, tests/cli/test_install_retired_files.py (all in the evidence log). list_installed_templates (not changed by this task; Task 6) is read by main.py:144.
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
