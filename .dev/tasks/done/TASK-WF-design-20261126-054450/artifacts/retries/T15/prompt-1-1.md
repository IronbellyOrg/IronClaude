189c6c324c883c181f1c1fc12dea8ca8057c0bc3
Review one task for spec compliance.

Task brief: ## Task 15: Correct docs/reference/troubleshooting.md and add the failed-save entry

Depends on: Task 12

At lines 159-161 (under "Reset Installation") replace "It saves a differing command, rule or output-style file as `<name>.bak.<UTC time>` first; edited core files, agents and skills get no copy, so copy those first." with W-1 and W-2 (the paragraph's first sentence already says the command overwrites the files it ships, so use sentences 2 and 3 of W-1, then W-2, and say that "no copy" for skill folders and hook scripts on one line). Directly after that paragraph add a short entry that uses W-4 verbatim (the message, the cause, the fix, the exit code 1 and the note that a `.bak.` copy left by a failed save may be incomplete). Leave the sentence "There is no uninstall command." and the rest of the file unchanged.

Acceptance criteria:
- The paragraph no longer says edited core files or agents get no copy; it names skill folders and hook scripts.
- The new entry contains the exact message `could not save a copy first, left untouched` and states that `superclaude install --force` and `superclaude update` exit 1.
- No restore command in the file uses `ls -t ... | head -1` for these backup files.

AC ids:
- T15.AC1: The paragraph no longer says edited core files or agents get no copy; it names skill folders and hook scripts.
- T15.AC2: The new entry contains the exact message `could not save a copy first, left untouched` and states that `superclaude install --force` and `superclaude update` exit 1.
- T15.AC3: No restore command in the file uses `ls -t ... | head -1` for these backup files.
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
Start sha: 189c6c324c883c181f1c1fc12dea8ca8057c0bc3
Diff against the start snapshot: diff --git a/docs/reference/troubleshooting.md b/docs/reference/troubleshooting.md
index 3f5ed35f9..ac853185a 100644
--- a/docs/reference/troubleshooting.md
+++ b/docs/reference/troubleshooting.md
@@ -156,11 +156,26 @@ grep -r "@" ~/.claude/CLAUDE.md      # Verify imports
 superclaude install --force          # Overwrite the installed framework files
 ```
 
-`superclaude install --force` overwrites the files it ships in `~/.claude/`. It
-saves a differing command, rule or output-style file as `<name>.bak.<UTC time>`
-first; edited core files, agents and skills get no copy, so copy those first.
+`superclaude install --force` overwrites the files it ships in `~/.claude/`.
+When a command, rule, output-style, core, agent or template file differs from
+the shipped one, the installer first saves a copy next to it as
+`<name>.bak.<UTC time>`.
+Skill folders (deleted and re-copied) and hook scripts get no copy.
+Copy any file you changed or added inside a skill folder, and any hook script
+you changed, to a place outside `~/.claude/skills/` before you run either
+command.
 There is no uninstall command.
 
+**Failed to save a copy:**
+
+`could not save a copy first, left untouched`: the installer could not write
+the `.bak.` copy next to a file, because the folder is not writable, the disk
+is full, the file cannot be read, or a folder sits at the file's path. That file
+is left as it is, the run lists it under the failed files, and
+`superclaude install --force` or `superclaude update` exits 1. Make the folder
+writable or free space and run the command again, or move the file aside
+yourself. A `.bak.` file left behind by a failed save may be incomplete.
+
 ## Get Help
 
 **Documentation:**

Task-owned evidence artifact artifacts/t15-test.log (a log the task wrote; cite it as ./artifacts/t15-test.log:<line>):
1: == AC1: lines with 'no copy' ==
2: 163:Skill folders (deleted and re-copied) and hook scripts get no copy.
3: == AC1: core/agents + no copy (expect none) ==
4: == AC2: exact message and exit 1 ==
5: 171:`could not save a copy first, left untouched`: the installer could not write
6: 175:`superclaude install --force` or `superclaude update` exits 1. Make the folder
7: == AC3: ls -t | head -1 (expect none) ==
8: 132:ls -t ~/.claude/settings.json.bak.* | head -1 | xargs -I{} cp {} ~/.claude/settings.json
9: == diff stat ==
10:  docs/reference/troubleshooting.md | 21 ++++++++++++++++++---
11:  1 file changed, 18 insertions(+), 3 deletions(-)
12: == longest line ==
13: 172
14: == AC3 note ==
15: The one hit (line 132) is the pre-existing "Restore settings.json after a bad merge" command. It restores ~/.claude/settings.json.bak.* (written by the hook installer), not a .bak. copy of a command, rule, output-style, core, agent or template file. It is outside the paragraph this task changes and is left as it was (the task says the rest of the file stays unchanged).
16: == pytest (no test reads this file by name; docs tests run) ==
17: No test in tests/ names troubleshooting.md (grep -rln found none); no test run for this task.
18: 

Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:51:49Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-676
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-676
call codegraph only when index_state: fresh, never to widen scope
Q2b: documentation only (docs/reference/troubleshooting.md, lines 159-177). No test in tests/ names this file (see ./artifacts/t15-test.log). The pre-existing command at line 132 (ls -t ~/.claude/settings.json.bak.* | head -1 ...) restores settings.json backups made by the hook installer, not the .bak. copies this change describes; the plan says the rest of the file stays unchanged, so it was left alone. Wording kit W-1..W-4 is in the plan Constraints (line 28 of the plan).
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
