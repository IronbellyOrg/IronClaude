31479e9baae6ae144456c44073a32251dd59d153
Review one task for spec compliance.

Task brief: ## Task 1: Save a differing core file before a forced overwrite in install_core_files

In `src/superclaude/cli/install_core.py`, function `install_core_files(target_path, force)` (line 33):

- Extend the import at line 12 to `from .install_keep import backup_if_differs, same_content`.
- Add `backed_up = []` beside `installed`, `skipped` and `failed` (lines 64-66).
- In the loop over `core_files`, between the skip path (`if dest_file.exists() and not force:` ... `continue`, ending at line 73) and the `try:` at line 75, add the backup step: when `dest_file.exists()`, inside its own `try`, call `backup_if_differs(src_file, dest_file)`; append a returned path to `backed_up` as `str(path)`; on `OSError as e` append `f"{src_file.name}: could not save a copy first, left untouched ({e})"` to `failed` and `continue`. The backup call must not sit inside the existing `try`/`except Exception` that wraps `shutil.copy2`, which stays unchanged.
- Print the saved block (see Constraints, noun `core file`) after the whole `if skipped:` block (it ends at line 106) and before `if failed:` (line 108). It must sit outside `if skipped:`: a forced run has no skipped files, so a block inside it would never print.
- In the kept-file note at lines 101-104, change `(run with --force or `superclaude update` to refresh):` to `(run with --force or `superclaude update` to refresh; a differing file is saved as <name>.bak.<time> first):`, the words used at `install_commands.py:101-103`.
- Leave `KNOWN_CORE_FILES`, `_get_core_source`, `list_core_files` and `list_installed_core_files` unchanged. The return stays `success = len(failed) == 0`.

Acceptance criteria:
- `install_core_files(target_path=t, force=True)` over an existing `t/RULES.md` whose bytes differ from the shipped file leaves `t/RULES.md` equal to the shipped bytes, leaves exactly one `t/RULES.md.bak.<stamp>` holding the old bytes, the returned message contains `Saved 1 changed core file(s) before overwriting:` and that backup path before any `Failed to install` block, and the `✅ Installed` list still names `RULES.md` (a backed-up file still counts as installed).
- The same call with a byte-identical `RULES.md`, or into an empty target, makes no backup and the message has no `Saved`.
- `force=False` writes nothing and makes no backup; for a differing kept file the message contains `a differing file is saved as <name>.bak.<time> first`.
- When the backup copy raises `OSError`, that file's bytes are unchanged, `failed` holds `RULES.md: could not save a copy first, left untouched (<error>)`, the function returns `False`, and the other core files in the same run are still installed.
- `uv run pytest tests/cli/test_how_we_work_install.py tests/cli/test_issue_body_templates.py tests/cli/test_bash_inspection_policy.py tests/cli/test_install_failures.py tests/unit/test_cli_install.py tests/cli/test_update_command.py tests/cli/test_install_retired_files.py -q` passes: these are the existing callers of `install_core_files`. Most run without force or force-install into an empty target; `test_install_retired_files.py` (its upgrade tests need the v5.0.0 tag and skip without it) and the real `update` in `test_update_command.py` run the real installers with force over existing files, so they do reach the new backup call.

AC ids:
- T1.AC1: `install_core_files(target_path=t, force=True)` over an existing `t/RULES.md` whose bytes differ from the shipped file leaves `t/RULES.md` equal to the shipped bytes, leaves exactly one `t/RULES.md.bak.<stamp>` holding the old bytes, the returned message contains `Saved 1 changed core file(s) before overwriting:` and that backup path before any `Failed to install` block, and the `✅ Installed` list still names `RULES.md` (a backed-up file still counts as installed).
- T1.AC2: The same call with a byte-identical `RULES.md`, or into an empty target, makes no backup and the message has no `Saved`.
- T1.AC3: `force=False` writes nothing and makes no backup; for a differing kept file the message contains `a differing file is saved as <name>.bak.<time> first`.
- T1.AC4: When the backup copy raises `OSError`, that file's bytes are unchanged, `failed` holds `RULES.md: could not save a copy first, left untouched (<error>)`, the function returns `False`, and the other core files in the same run are still installed.
- T1.AC5: `uv run pytest tests/cli/test_how_we_work_install.py tests/cli/test_issue_body_templates.py tests/cli/test_bash_inspection_policy.py tests/cli/test_install_failures.py tests/unit/test_cli_install.py tests/cli/test_update_command.py tests/cli/test_install_retired_files.py -q` passes: these are the existing callers of `install_core_files`. Most run without force or force-install into an empty target; `test_install_retired_files.py` (its upgrade tests need the v5.0.0 tag and skip without it) and the real `update` in `test_update_command.py` run the real installers with force over existing files, so they do reach the new backup call.
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
Start sha: 31479e9baae6ae144456c44073a32251dd59d153
Diff against the start snapshot: diff --git a/src/superclaude/cli/install_core.py b/src/superclaude/cli/install_core.py
index 0c2a2fa45..e81088342 100644
--- a/src/superclaude/cli/install_core.py
+++ b/src/superclaude/cli/install_core.py
@@ -9,7 +9,7 @@ import shutil
 from pathlib import Path
 from typing import List, Tuple
 
-from .install_keep import same_content
+from .install_keep import backup_if_differs, same_content
 
 # Core files this version ships; list_installed_core_files reports only these.
 KNOWN_CORE_FILES = frozenset(
@@ -64,6 +64,7 @@ def install_core_files(
     installed = []
     skipped = []
     failed = []
+    backed_up = []
 
     for src_file in core_files:
         dest_file = target_path / src_file.name
@@ -72,6 +73,18 @@ def install_core_files(
             skipped.append(src_file.name)
             continue
 
+        # A forced overwrite first saves a differing file next to itself
+        try:
+            if dest_file.exists():
+                backup = backup_if_differs(src_file, dest_file)
+                if backup is not None:
+                    backed_up.append(str(backup))
+        except OSError as e:
+            failed.append(
+                f"{src_file.name}: could not save a copy first, left untouched ({e})"
+            )
+            continue
+
         try:
             shutil.copy2(src_file, dest_file)
             installed.append(src_file.name)
@@ -100,11 +113,19 @@ def install_core_files(
         if stale:
             messages.append(
                 f"\n⚠️  {len(stale)} kept file(s) differ from this version and were "
-                "NOT updated (run with --force or `superclaude update` to refresh):"
+                "NOT updated (run with --force or `superclaude update` to refresh; "
+                "a differing file is saved as <name>.bak.<time> first):"
             )
             for name in stale:
                 messages.append(f"   - {name}")
 
+    if backed_up:
+        messages.append(
+            f"\n💾 Saved {len(backed_up)} changed core file(s) before overwriting:"
+        )
+        for path in backed_up:
+            messages.append(f"   - {path}")
+
     if failed:
         messages.append(f"\n❌ Failed to install {len(failed)} files:")
         for fail in failed:

Task-owned evidence artifact artifacts/t1-test.log (a log the task wrote; cite it as ./artifacts/t1-test.log:<line>):
1: $ uv run pytest -p no:cacheprovider tests/cli/test_how_we_work_install.py tests/cli/test_issue_body_templates.py tests/cli/test_bash_inspection_policy.py tests/cli/test_install_failures.py tests/unit/test_cli_install.py tests/cli/test_update_command.py tests/cli/test_install_retired_files.py -q
2: tests/cli/test_update_command.py ....................                    [ 81%]
3: tests/cli/test_install_retired_files.py ................................ [100%]
4: 
5: ============================= 169 passed in 5.39s ==============================
6: rc=0 if the line above says passed
7: 

Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:51:49Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-676
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-676
call codegraph only when index_state: fresh, never to widen scope
Dependents of install_core_files not in the diff (callers; signature unchanged): src/superclaude/cli/main.py:180 (install), src/superclaude/cli/main.py:383 (update); tests: tests/cli/test_how_we_work_install.py, tests/cli/test_issue_body_templates.py, tests/cli/test_bash_inspection_policy.py, tests/cli/test_install_failures.py, tests/unit/test_cli_install.py, tests/cli/test_install_keep.py:72-77 (all run green: 169 passed).
Delta diff from the previous reviewed tree (empty on the first review): (no change to tracked files since the reviewed tree r1-1; the evidence log artifacts/t1-test.log was rewritten with the command and its full pytest summary)
Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B1 ac=T1.AC5 at=tests/cli/test_update_command.py:228 anchor="`uv run pytest tests/cli/test_how_we_work_install.py tests/cli/test_issue_body_templates.py tests/cli/test_bash_inspection_policy.py tests/cli/test_install_failures.py tests/unit/test_cli_install.py tests/cli/test_update_command.py tests/cli/test_install_retired_files.py -q` passes" chk=y,n,n,n family=unrun-ac-command fix=Run the exact AC5 command and record its pass/skip counts first=A1 origin=new: The review package held no record of the AC5 command passing (the run was done but its log was not in the package).
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
