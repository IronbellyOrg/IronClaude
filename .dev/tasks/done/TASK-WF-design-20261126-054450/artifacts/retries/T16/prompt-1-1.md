697bd33820f7f783244a28acae6585f4b44264ef
Review one task for spec compliance.

Task brief: ## Task 16: Correct docs/getting-started/installation.md lines 644 and 646

Depends on: Task 12

- Line 644: the sentence that says a plain `superclaude install` "names each kept command, rule and output-style file that differs from this version" also names core files (the core installer already does, `src/superclaude/cli/install_core.py:95-106`). Agents and templates are not added.
- Line 646, the "Warning" paragraph: keep its first sentence and do not repeat the overwrite sentence of W-1 (use only sentences 2 and 3 of W-1); remove the three-kind sentence that starts "For a command, rule or output-style file that differs from the shipped one" but keep its link to `upgrading.md#saved-copies-of-changed-files` and put that link after sentence 3 of W-1; then replace the text "Core files such as `~/.claude/CLAUDE.md` and `~/.claude/RULES.md`, agents and skills are overwritten with no copy, and each shipped skill folder ... is deleted and re-copied, so any file you added inside one is lost. If you edited or added any of those files, copy them first (for example `cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.mine`), then re-apply your changes after the upgrade." with W-1 and W-2, and change the `cp` example so it copies a file added inside a skill folder to a path outside `~/.claude/skills/`. Keep the rest of the paragraph (the codegraph phase, exit code 1 note and the link to the saved-copies section) unchanged.

Acceptance criteria:
- Line 646 names skill folders and hook scripts as the files overwritten with no copy and contains no `cp` example that targets `CLAUDE.md`.
- The link `upgrading.md#saved-copies-of-changed-files` is unchanged and still resolves to the section edited in Task 18.
- No other line of `installation.md` changes.

AC ids:
- T16.AC1: Line 646 names skill folders and hook scripts as the files overwritten with no copy and contains no `cp` example that targets `CLAUDE.md`.
- T16.AC2: The link `upgrading.md#saved-copies-of-changed-files` is unchanged and still resolves to the section edited in Task 18.
- T16.AC3: No other line of `installation.md` changes.
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
Start sha: 697bd33820f7f783244a28acae6585f4b44264ef
Diff against the start snapshot: diff --git a/docs/getting-started/installation.md b/docs/getting-started/installation.md
index 8e6363448..0f3f70922 100644
--- a/docs/getting-started/installation.md
+++ b/docs/getting-started/installation.md
@@ -641,9 +641,9 @@ claude mcp remove codegraph --scope user
 
 then delete the owned paths `superclaude install --list` printed; see [Removing codegraph](../user-guide/mcp-installation.md#removing-codegraph).
 
-A plain `superclaude install` keeps framework files you already have and names each kept command, rule and output-style file that differs from this version (it still runs the codegraph phase and the cleanup steps); run `superclaude install --force` to refresh them, for example to get the new `~/.claude/CLAUDE.md` and the latest `~/.claude/HOW-WE-WORK.md`. Unlike `superclaude update`, it also installs codegraph and retires old MCP registrations.
+A plain `superclaude install` keeps framework files you already have and names each kept command, rule, output-style and core file that differs from this version (it still runs the codegraph phase and the cleanup steps); run `superclaude install --force` to refresh them, for example to get the new `~/.claude/CLAUDE.md` and the latest `~/.claude/HOW-WE-WORK.md`. Unlike `superclaude update`, it also installs codegraph and retires old MCP registrations.
 
-> **Warning:** `superclaude install --force` overwrites every file it ships, the same files `superclaude update` overwrites. For a command, rule or output-style file that differs from the shipped one it first saves a copy next to it as `<name>.bak.<UTC time>` (see [Saved copies](upgrading.md#saved-copies-of-changed-files)). Core files such as `~/.claude/CLAUDE.md` and `~/.claude/RULES.md`, agents and skills are overwritten with no copy, and each shipped skill folder in `~/.claude/skills/` is deleted and re-copied, so any file you added inside one is lost. If you edited or added any of those files, copy them first (for example `cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.mine`), then re-apply your changes after the upgrade. After refreshing the files it also runs the codegraph phase and the cleanup steps; if the codegraph phase fails, the command exits 1 even though the files were already refreshed. Fix the cause and run it again.
+> **Warning:** `superclaude install --force` overwrites every file it ships, the same files `superclaude update` overwrites. When a command, rule, output-style, core, agent or template file differs from the shipped one, the installer first saves a copy next to it as `<name>.bak.<UTC time>`. Skill folders (deleted and re-copied) and hook scripts get no copy (see [Saved copies](upgrading.md#saved-copies-of-changed-files)). Copy any file you changed or added inside a skill folder, and any hook script you changed, to a place outside `~/.claude/skills/` before you run either command (for example `cp ~/.claude/skills/<skill-name>/<file> ~/<file>.mine`), then re-apply your changes after the upgrade. After refreshing the files it also runs the codegraph phase and the cleanup steps; if the codegraph phase fails, the command exits 1 even though the files were already refreshed. Fix the cause and run it again.
 
 ---

Task-owned evidence artifact artifacts/t16-test.log (a log the task wrote; cite it as ./artifacts/t16-test.log:<line>):
1: == AC1 646 has skill folders and hook scripts; no cp CLAUDE.md ==
2: Skill folders (deleted and re-copied) and hook scripts get no copy
3: 0
4: == AC2 link and heading ==
5: (upgrading.md#saved-copies-of-changed-files)
6: 335:### Saved copies of changed files
7: == AC3 changed lines (expect 644 and 646 only) ==
8: @@ -644 +644 @@ then delete the owned paths `superclaude install --list` printed; see [Removing
9: @@ -646 +646 @@ A plain `superclaude install` keeps framework files you already have and names e
10: 

Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:51:49Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-676
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-676
call codegraph only when index_state: fresh, never to widen scope
Q2b: documentation only (docs/getting-started/installation.md lines 644 and 646). No test in tests/ names installation.md (grep -rln found none). Line 644 now also names core files (the core installer already does: src/superclaude/cli/install_core.py:95-106; agents and templates are not added, per the plan). The link to upgrading.md#saved-copies-of-changed-files points at the heading "### Saved copies of changed files" (upgrading.md:335), which Task 18 rewrites without changing the heading. Wording kit W-1..W-4 is in the plan Constraints (plan line 28). The plan says to use only sentences 2 and 3 of W-1 on line 646 (the paragraph's first sentence already says the command overwrites what it ships) and to put the saved-copies link after sentence 3.
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
