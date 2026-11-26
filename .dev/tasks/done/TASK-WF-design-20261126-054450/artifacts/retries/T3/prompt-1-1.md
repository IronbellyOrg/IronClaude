506b3ffb2b9c8acd97f60893c8a7d64ca1421047
Review one task for spec compliance.

Task brief: ## Task 3: Save a differing agent file before a forced overwrite in install_agents

In `src/superclaude/cli/install_agents.py`, function `install_agents(target_path, force)` (line 15):

- Add `from .install_keep import backup_if_differs` after the imports at lines 7-9.
- Add `backed_up = []` beside `installed`, `skipped` and `failed` (lines 43-45).
- In the loop over `agent_files`, between the skip path (ending at line 53) and the `try:` at line 55, add the backup step as in Task 1: when `target_file.exists()`, in its own `try`, call `backup_if_differs(agent_file, target_file)`; append a returned path to `backed_up` as `str(path)`; on `OSError as e` append `f"{agent_name}: could not save a copy first, left untouched ({e})"` to `failed` and `continue` (`agent_name` is the stem set at line 49). The existing `try`/`except Exception` around `shutil.copy2` stays unchanged and does not contain the backup call.
- Print the saved block (noun `agent`) after the skipped block (lines 68-73) and before the failed block (line 75).
- Add no kept-but-different note; leave `list_available_agents`, `list_installed_agents` and `_EXCLUDE_FILES` unchanged.

Acceptance criteria:
- `install_agents(target_path=t, force=True)` over an edited `t/<agent>.md` leaves the shipped bytes in `t/<agent>.md`, exactly one `t/<agent>.md.bak.<stamp>` with the old bytes, and a message containing `Saved 1 changed agent(s) before overwriting:` and the path.
- A byte-identical file, an empty target, and `force=False` make no backup; a failed backup leaves the agent's bytes unchanged, lists `<agent>: could not save a copy first, left untouched (<error>)` under `❌ Failed to install`, returns `False`, and still installs the other agents.
- `list_installed_agents()` does not list `<agent>.md.bak.<stamp>` (it globs `*.md`), and `README.md` stays excluded.
- `uv run pytest tests/cli/test_install_failures.py tests/troubleshoot/test_diagnostic_worker_contract.py tests/unit/test_cli_install.py tests/cli/test_update_command.py tests/cli/test_install_retired_files.py -q` passes: these are the existing callers of `install_agents`. Most force-install into an empty target or run without force; `test_install_retired_files.py` (its upgrade test lays 5.0.0 agent files into the agents folder and force-installs over them; it needs the v5.0.0 tag) and the real `update` in `test_update_command.py` do reach the new backup call.

AC ids:
- T3.AC1: `install_agents(target_path=t, force=True)` over an edited `t/<agent>.md` leaves the shipped bytes in `t/<agent>.md`, exactly one `t/<agent>.md.bak.<stamp>` with the old bytes, and a message containing `Saved 1 changed agent(s) before overwriting:` and the path.
- T3.AC2: A byte-identical file, an empty target, and `force=False` make no backup; a failed backup leaves the agent's bytes unchanged, lists `<agent>: could not save a copy first, left untouched (<error>)` under `❌ Failed to install`, returns `False`, and still installs the other agents.
- T3.AC3: `list_installed_agents()` does not list `<agent>.md.bak.<stamp>` (it globs `*.md`), and `README.md` stays excluded.
- T3.AC4: `uv run pytest tests/cli/test_install_failures.py tests/troubleshoot/test_diagnostic_worker_contract.py tests/unit/test_cli_install.py tests/cli/test_update_command.py tests/cli/test_install_retired_files.py -q` passes: these are the existing callers of `install_agents`. Most force-install into an empty target or run without force; `test_install_retired_files.py` (its upgrade test lays 5.0.0 agent files into the agents folder and force-installs over them; it needs the v5.0.0 tag) and the real `update` in `test_update_command.py` do reach the new backup call.
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
Start sha: 506b3ffb2b9c8acd97f60893c8a7d64ca1421047
Diff against the start snapshot: diff --git a/src/superclaude/cli/install_agents.py b/src/superclaude/cli/install_agents.py
index 9899d2a9e..07ea3b706 100644
--- a/src/superclaude/cli/install_agents.py
+++ b/src/superclaude/cli/install_agents.py
@@ -8,6 +8,8 @@ import shutil
 from pathlib import Path
 from typing import List, Tuple
 
+from .install_keep import backup_if_differs
+
 # Files to exclude from installation
 _EXCLUDE_FILES = {"README.md", "__init__.py"}
 
@@ -43,6 +45,7 @@ def install_agents(target_path: Path = None, force: bool = False) -> Tuple[bool,
     installed = []
     skipped = []
     failed = []
+    backed_up = []
 
     for agent_file in agent_files:
         target_file = target_path / agent_file.name
@@ -52,6 +55,18 @@ def install_agents(target_path: Path = None, force: bool = False) -> Tuple[bool,
             skipped.append(agent_name)
             continue
 
+        # A forced overwrite first saves a differing file next to itself
+        try:
+            if target_file.exists():
+                backup = backup_if_differs(agent_file, target_file)
+                if backup is not None:
+                    backed_up.append(str(backup))
+        except OSError as e:
+            failed.append(
+                f"{agent_name}: could not save a copy first, left untouched ({e})"
+            )
+            continue
+
         try:
             shutil.copy2(agent_file, target_file)
             installed.append(agent_name)
@@ -72,6 +87,13 @@ def install_agents(target_path: Path = None, force: bool = False) -> Tuple[bool,
         for name in skipped:
             messages.append(f"   - {name}")
 
+    if backed_up:
+        messages.append(
+            f"\n💾 Saved {len(backed_up)} changed agent(s) before overwriting:"
+        )
+        for path in backed_up:
+            messages.append(f"   - {path}")
+
     if failed:
         messages.append(f"\n❌ Failed to install {len(failed)} agents:")
         for fail in failed:

Task-owned evidence artifact artifacts/t3-test.log (a log the task wrote; cite it as ./artifacts/t3-test.log:<line>):
1: $ uv run pytest -p no:cacheprovider tests/cli/test_install_failures.py tests/troubleshoot/test_diagnostic_worker_contract.py tests/unit/test_cli_install.py tests/cli/test_update_command.py tests/cli/test_install_retired_files.py -q
2: tests/cli/test_update_command.py ....................                    [ 83%]
3: tests/cli/test_install_retired_files.py ................................ [100%]
4: 
5: ============================= 199 passed in 5.52s ==============================
6: 
7: $ ad hoc behaviour check of install_agents (not committed)
8: AC1 replaced: True | one backup with old bytes: True | message has Saved line: True
9: AC2 matching file, no further backup: True
10: AC2 force=False no Saved line: True
11: AC2 failed backup: ok= False | untouched: True | line: True
12: AC3 backup excluded by the *.md glob: True
13: 
14: $ ad hoc AC3 check: list_installed_agents with a saved copy present (not committed)
15: backups on disk: 1 | listed installed: 49 | available: 49 | no .bak. listed: True | README.md listed: False
16: 

Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:51:49Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-676
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-676
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents of install_agents not in the diff (signature unchanged): src/superclaude/cli/main.py:198 (install), src/superclaude/cli/main.py:396 (update); tests: tests/cli/test_install_failures.py, tests/troubleshoot/test_diagnostic_worker_contract.py:411-415, tests/unit/test_cli_install.py:933, tests/cli/test_update_command.py, tests/cli/test_install_retired_files.py (all in the evidence log). install_retired_files.py:164 reads only list_available_agents (unchanged).
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
