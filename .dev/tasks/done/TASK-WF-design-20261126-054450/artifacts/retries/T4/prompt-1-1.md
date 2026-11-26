60574182a90a5b4cfdc55cdbd78daa35e9138182
Review one task for spec compliance.

Task brief: ## Task 4: Add the agents row to the installer-row test table

Depends on: Task 2, Task 3

In `tests/cli/test_install_keep.py` add the `agents` row to the table of Task 2: call `install_agents(target_path=t, force=f)` (add `from superclaude.cli.install_agents import install_agents`), target `tmp_path / "agents"`, victim the first `*.md` in that folder, noun `agent`. Do not change any test body except where a row-specific assertion is needed: TR-005 stays core-only, and in `test_plain_install_keeps_the_edit_and_makes_no_backup` the agents message must contain no `differ` text (agents get no kept-but-different note).

Acceptance criteria:
- `uv run pytest tests/cli/test_install_keep.py -q` passes with TR-001 to TR-004, TR-006, TR-007, TR-009 and TR-010 running for the `agents` row.
- The backup of an agent is named `<agent>.md.bak.<stamp>` and is found by `_victim_baks`.
- The `core` row results are unchanged.

AC ids:
- T4.AC1: `uv run pytest tests/cli/test_install_keep.py -q` passes with TR-001 to TR-004, TR-006, TR-007, TR-009 and TR-010 running for the `agents` row.
- T4.AC2: The backup of an agent is named `<agent>.md.bak.<stamp>` and is found by `_victim_baks`.
- T4.AC3: The `core` row results are unchanged.
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
Start sha: 60574182a90a5b4cfdc55cdbd78daa35e9138182
Diff against the start snapshot: diff --git a/tests/cli/test_install_keep.py b/tests/cli/test_install_keep.py
index 1c9d01a42..974c98312 100644
--- a/tests/cli/test_install_keep.py
+++ b/tests/cli/test_install_keep.py
@@ -21,6 +21,7 @@ import pytest
 
 from superclaude.cli import install_keep
 from superclaude.cli import install_user_setup as setup
+from superclaude.cli.install_agents import install_agents
 from superclaude.cli.install_commands import install_commands
 from superclaude.cli.install_core import install_core_files
 from superclaude.cli.install_keep import backup_if_differs, same_content
@@ -244,6 +245,15 @@ _ROWS = {
             key=lambda v, t: v.name,
             kept_note=True,
         ),
+        _Row(
+            id="agents",
+            install=lambda t, f: install_agents(target_path=t, force=f),
+            target=lambda tmp: tmp / "agents",
+            victims=lambda t: sorted(t.glob("*.md")),
+            noun="agent",
+            key=lambda v, t: v.stem,
+            kept_note=False,
+        ),
     )
 }

Task-owned evidence artifact artifacts/t4-test.log (a log the task wrote; cite it as ./artifacts/t4-test.log:<line>):
1: $ uv run pytest -p no:cacheprovider tests/cli/test_install_keep.py -q
2: tests/cli/test_install_keep.py .....................................     [100%]
3: 
4: ============================== 37 passed in 1.26s ==============================
5: 
6: $ uv run pytest -p no:cacheprovider tests/cli/test_install_keep.py -v -k agents
7: test_forced_install_saves_a_differing_file_then_replaces_it[agents] PASSED [ 10%]
8: test_forced_install_of_a_matching_or_missing_file_makes_no_backup[agents] PASSED [ 20%]
9: test_a_second_forced_run_makes_no_further_backup[agents] PASSED [ 30%]
10: test_plain_install_keeps_the_edit_and_makes_no_backup[agents] PASSED [ 40%]
11: test_failed_save_leaves_the_file_untouched[agents-permission] PASSED [ 50%]
12: test_failed_save_leaves_the_file_untouched[agents-enospc] PASSED [ 60%]
13: test_save_then_failed_replacement_keeps_the_backup[agents] PASSED [ 70%]
14: test_backup_names_do_not_collide_on_one_instant[agents] PASSED [ 80%]
15: test_same_size_same_mtime_edit_is_saved_when_forced[agents] PASSED [ 90%]
16: test_directory_at_the_victim_path_fails_closed[agents] PASSED [100%]
17: ====================== 10 passed, 27 deselected in 1.10s =======================
18: 
19: $ uv run pytest -p no:cacheprovider tests/cli/test_install_keep.py -q -k core
20: 
21: ====================== 12 passed, 25 deselected in 1.14s =======================
22: 

Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:51:49Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-676
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-676
call codegraph only when index_state: fresh, never to widen scope
Q2b: test-only change; the row table `_ROWS` (tests/cli/test_install_keep.py) and the `row` fixture read it, so the new row reaches every table test (listed in ./artifacts/t4-test.log). Production symbol used: install_agents (Task 3, complete; failure key is the agent stem, src/superclaude/cli/install_agents.py:66-67). TR-005 stays core-only (_ROWS["core"]).
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
