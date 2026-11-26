b7e4c0bdc73ce8d743c0603bc5964ed0548ddef0
Review one task for spec compliance.

Task brief: ## Task 18: Correct the "Saved copies of changed files" section of docs/getting-started/upgrading.md (lines 335-364)

Depends on: Task 17

Edit the section that starts "### Saved copies of changed files":

- The lead names the six categories: command, rule, output-style, core file, agent and template.
- "Why so many": every forced upgrade saves each file whose shipped bytes changed, edited or not, and the newest copy may be an older shipped version rather than your edit, so read the copies before restoring.
- "Not loaded": the copy ends in a time stamp, not in `.md`, so Claude Code does not load it as a command, agent or core file.
- "Not covered": skill folders and hook scripts are overwritten without a copy (the sentence that wraps over two lines near line 349 is rewritten).
- "If a copy cannot be saved": `superclaude install --force` or `superclaude update` prints that file as a failure and exits 1 (it currently says only `superclaude install`); add the cause and fix from W-4.
- "Nothing deletes them": the two `find` commands become `find ~/.claude/commands/sc ~/.claude/rules ~/.claude/output-styles ~/.claude/agents ~/.claude/templates -name '*.bak.*'` and `find ~/.claude -maxdepth 1 -name '*.md.bak.*'`, each with its `-delete` form. The root search uses `*.md.bak.*`, never `*.bak.*`, because `settings.json.bak.<timestamp>` lives there and is a separate file the installer writes on every run.

Acceptance criteria:
- The section names the six categories, says skill folders and hook scripts are not covered, and has no `ls -t ... | head -1` restore advice.
- The `find` commands match the two shown above, with the `-maxdepth 1 -name '*.md.bak.*'` form for the `~/.claude` root and no `*.bak.*` search of the root.
- The heading "Saved copies of changed files" is unchanged, so the anchor `#saved-copies-of-changed-files` still works.

AC ids:
- T18.AC1: The section names the six categories, says skill folders and hook scripts are not covered, and has no `ls -t ... | head -1` restore advice.
- T18.AC2: The `find` commands match the two shown above, with the `-maxdepth 1 -name '*.md.bak.*'` form for the `~/.claude` root and no `*.bak.*` search of the root.
- T18.AC3: The heading "Saved copies of changed files" is unchanged, so the anchor `#saved-copies-of-changed-files` still works.
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
Start sha: b7e4c0bdc73ce8d743c0603bc5964ed0548ddef0
Diff against the start snapshot: diff --git a/docs/getting-started/upgrading.md b/docs/getting-started/upgrading.md
index fa28a415c..2322b5567 100644
--- a/docs/getting-started/upgrading.md
+++ b/docs/getting-started/upgrading.md
@@ -337,33 +337,48 @@ disappear from them.
 ### Saved copies of changed files
 
 `superclaude install --force` and `superclaude update` save a copy of every
-command, rule and output-style file that differs from the shipped one before
-they overwrite it. The install output lists the copies, for example
-`Saved 27 changed command(s) before overwriting:` (and the same for `rule
-file(s)` and `output style(s)`).
+command, rule, output-style, core, agent and template file that differs from the
+shipped one before they overwrite it. The install output lists the copies, for
+example `Saved 27 changed command(s) before overwriting:` (and the same for
+`rule file(s)`, `output style(s)`, `core file(s)`, `agent(s)` and
+`template(s)`).
 
 - **Why so many.** A file from an older release and a file you edited look the
-  same to the installer, so both are saved. An upgrade from 5.0.0 leaves a copy
-  of every command that changed since then, whether you edited it or not.
+  same to the installer, so both are saved. Every forced upgrade saves each file
+  whose shipped bytes changed, edited or not, so an upgrade from 5.0.0 leaves a
+  copy of every file that changed since then. The newest copy may be an older
+  shipped version rather than your edit, so read the copies before you restore
+  one.
 - **Not loaded.** The copy is named `<name>.bak.<UTC time>` (for example
   `analyze.md.bak.20261118T170151Z`). It ends in a time stamp, not in `.md`, so
-  Claude Code does not load it as a command.
-- **Not covered.** Core files, agents and skill folders are overwritten without a
-  copy (see Step 1). A plain `superclaude install` overwrites nothing; it names
-  each kept file that differs from this version (`N kept command(s) differ from
-  this version and were NOT updated`).
+  Claude Code does not load it as a command, agent or core file.
+- **Not covered.** Skill folders and hook scripts get no copy (see Step 1).
+  A plain `superclaude install` overwrites nothing; it names each kept file that
+  differs from this version (`N kept command(s) differ from this version and
+  were NOT updated`).
 - **If a copy cannot be saved,** that one file is left as it is, and
-  `superclaude install` prints it as a failure and exits 1.
+  `superclaude install --force` or `superclaude update` prints it as a failure
+  (`could not save a copy first, left untouched`) and exits 1. The installer
+  could not write the `.bak.` copy next to the file, because the folder is not
+  writable, the disk is full, the file cannot be read, or a folder sits at the
+  file's path. Make the folder writable or free space and run the command
+  again, or move the file aside yourself. A `.bak.` file left behind by a failed
+  save may be incomplete.
 - **Nothing deletes them.** List the copies, then delete them when you no longer
-  need what is in them (look at the ones for files you edited first):
+  need what is in them (look at the ones for files you edited first). The first
+  pair covers the folders and the second pair the core files in `~/.claude`
+  itself:
 
   ```bash
-  find ~/.claude/commands/sc ~/.claude/rules ~/.claude/output-styles -name '*.bak.*'
-  find ~/.claude/commands/sc ~/.claude/rules ~/.claude/output-styles -name '*.bak.*' -delete
+  find ~/.claude/commands/sc ~/.claude/rules ~/.claude/output-styles ~/.claude/agents ~/.claude/templates -name '*.bak.*'
+  find ~/.claude/commands/sc ~/.claude/rules ~/.claude/output-styles ~/.claude/agents ~/.claude/templates -name '*.bak.*' -delete
+  find ~/.claude -maxdepth 1 -name '*.md.bak.*'
+  find ~/.claude -maxdepth 1 -name '*.md.bak.*' -delete
   ```
 
   The `settings.json.bak.<timestamp>` files in `~/.claude/` are separate: the
-  installer writes one on every run.
+  installer writes one on every run, and the root search above leaves them
+  alone.
 
 ## Step 5: Move your session memories

Task-owned evidence artifact artifacts/t18-test.log (a log the task wrote; cite it as ./artifacts/t18-test.log:<line>):
1: == AC1: six categories line ==
2: 340:command, rule, output-style, core, agent and template file that differs from the
3: == AC1: no copy lines in 337-380 (each must name skill folders/hook scripts) ==
4: 19:- **Not covered.** Skill folders and hook scripts get no copy (see Step 1).
5: == AC1: ls -t head -1 (expect none) ==
6: == AC2: find commands ==
7: 373:  find ~/.claude/commands/sc ~/.claude/rules ~/.claude/output-styles ~/.claude/agents ~/.claude/templates -name '*.bak.*'
8: 374:  find ~/.claude/commands/sc ~/.claude/rules ~/.claude/output-styles ~/.claude/agents ~/.claude/templates -name '*.bak.*' -delete
9: 375:  find ~/.claude -maxdepth 1 -name '*.md.bak.*'
10: 376:  find ~/.claude -maxdepth 1 -name '*.md.bak.*' -delete
11: == AC2: any *.bak.* search of the root (expect none) ==
12: == AC3: heading ==
13: 337:### Saved copies of changed files
14: == changed hunks ==
15: @@ -45,2 +45,2 @@ your edited copy is saved first depends on the kind of file:
16: @@ -49 +49,3 @@ your edited copy is saved first depends on the kind of file:
17: @@ -52,2 +54 @@ Copy anything you changed in the second row first, for example:
18: @@ -101,3 +102,4 @@ without `pipx` it stops at that first command (exit 127). Install pipx with
19: @@ -338,4 +340,5 @@ disappear from them.
20: @@ -344,2 +347,5 @@ file(s)` and `output style(s)`).
21: @@ -348,5 +354,5 @@ file(s)` and `output style(s)`).
22: @@ -354 +360,7 @@ file(s)` and `output style(s)`).
23: @@ -356 +368,3 @@ file(s)` and `output style(s)`).
24: @@ -359,2 +373,4 @@ file(s)` and `output style(s)`).
25: @@ -364 +380,2 @@ file(s)` and `output style(s)`).
26: == installer nouns (source) ==
27: 92:            f"\n💾 Saved {len(backed_up)} changed agent(s) before overwriting:"
28: 110:            f"\n💾 Saved {len(backed_up)} changed command(s) before overwriting:"
29: 124:            f"\n💾 Saved {len(backed_up)} changed core file(s) before overwriting:"
30: 108:            f"\n💾 Saved {len(backed_up)} changed template(s) before overwriting:"
31: 

Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:51:49Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-676
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-676
call codegraph only when index_state: fresh, never to widen scope
Q2b: documentation only (docs/getting-started/upgrading.md, section "### Saved copies of changed files", lines 337-384). The heading is unchanged, so the link upgrading.md#saved-copies-of-changed-files in installation.md:646 (Task 16) and #saved-copies-of-changed-files in Step 1 (Task 17) still resolve. The saved-block nouns in the lead were checked against the installers (./artifacts/t18-test.log last lines): "command(s)", "core file(s)", "agent(s)", "template(s)"; "rule file(s)" and "output style(s)" were already in the page. The two find commands for the folders and the two for the root are the exact forms the plan gives; the root search uses '*.md.bak.*' with -maxdepth 1 because settings.json.bak.<timestamp> lives in ~/.claude and is a separate file the installer writes on every run. Wording kit W-1..W-4 is in the plan Constraints (plan line 28). Earlier hunks in the diff against HEAD (lines 43-56, 99-106) belong to Task 17 and are already reviewed.
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
