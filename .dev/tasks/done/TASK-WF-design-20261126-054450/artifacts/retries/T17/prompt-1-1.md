b440b39779bcd7338115a00c56799ec7c02a2c18
Review one task for spec compliance.

Task brief: ## Task 17: Correct the backup table and the upgrade steps in docs/getting-started/upgrading.md (lines 43-56 and 99-103)

Depends on: Task 12

- Lines 43-56 (Step 1 "Back up files you edited"): the two-row table becomes: row one lists commands (`commands/sc/`), rules (`rules/`), output styles (`output-styles/`), core files, agents (`agents/`) and templates (`templates/`) as saved next to the file as `<name>.bak.<UTC time>` before the overwrite, with W-3 stating that 6.1.0 and earlier overwrite core files, agents and templates with no copy; row two lists skill folders (`skills/`, deleted and copied again, so a file added inside one is lost) and hook scripts as overwritten with no copy. The `settings.json` row is unchanged. The `cp` example that copies `CLAUDE.md` and `RULES.md` and the sentence "Copy anything you changed in the second row first" change to W-2 with an example that copies a file from a skill folder to a path outside `~/.claude/skills/`.
- Lines 99-103 ("What the upgrade does", step 1): "A command, rule or output-style file that differs from the shipped one is saved as `<name>.bak.<UTC time>` first." lists the six categories and carries W-3.

Acceptance criteria:
- `upgrading.md` lines 43-56 and 99-103 no longer say that core files or agents are overwritten with no copy for this version, and keep the 6.1.0 qualifier.
- The page title (line 1, 6.0.0) and the `@v6.0.0` pin (lines 65-66) are unchanged.
- The table keeps its two columns and the `settings.json` row.

AC ids:
- T17.AC1: `upgrading.md` lines 43-56 and 99-103 no longer say that core files or agents are overwritten with no copy for this version, and keep the 6.1.0 qualifier.
- T17.AC2: The page title (line 1, 6.0.0) and the `@v6.0.0` pin (lines 65-66) are unchanged.
- T17.AC3: The table keeps its two columns and the `settings.json` row.
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
Start sha: b440b39779bcd7338115a00c56799ec7c02a2c18
Diff against the start snapshot: diff --git a/docs/getting-started/upgrading.md b/docs/getting-started/upgrading.md
index 370ce570e..fa28a415c 100644
--- a/docs/getting-started/upgrading.md
+++ b/docs/getting-started/upgrading.md
@@ -42,15 +42,16 @@ your edited copy is saved first depends on the kind of file:
 
 | In `~/.claude/` | If your copy differs from the shipped one |
 |-----------------|-------------------------------------------|
-| Commands (`commands/sc/`), rules (`rules/`) and output styles (`output-styles/`) | A copy is saved next to it as `<name>.bak.<UTC time>` (for example `analyze.md.bak.20261118T170151Z`) before the file is overwritten. See [Saved copies](#saved-copies-of-changed-files). |
-| Core files (`CLAUDE.md`, `RULES.md` and the other core `.md` files), agents (`agents/`) and skill folders (`skills/`) | Overwritten with no copy. Each shipped skill folder is deleted and copied again, so any file you added inside one is lost. |
+| Commands (`commands/sc/`), rules (`rules/`), output styles (`output-styles/`), core files (`CLAUDE.md`, `RULES.md` and the other core `.md` files), agents (`agents/`) and templates (`templates/`) | A copy is saved next to it as `<name>.bak.<UTC time>` (for example `analyze.md.bak.20261118T170151Z`) before the file is overwritten. See [Saved copies](#saved-copies-of-changed-files). Releases 6.1.0 and earlier overwrite core files, agents and templates with no copy. |
+| Skill folders (`skills/`) and hook scripts (`hooks/`) | Overwritten with no copy. Each shipped skill folder is deleted and copied again, so any file you added inside one is lost. |
 | `settings.json` | Backed up as `settings.json.bak.<timestamp>` before the installer merges its entries, on every run. |
 
-Copy anything you changed in the second row first, for example:
+Copy any file you changed or added inside a skill folder, and any hook script
+you changed, to a place outside `~/.claude/skills/` before you run either
+command (`superclaude install --force` or `superclaude update`), for example:
 
 ```bash
-cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.mine
-cp ~/.claude/RULES.md ~/.claude/RULES.md.mine
+cp ~/.claude/skills/<skill-name>/<file> ~/<file>.mine
 ```
 
 Re-apply your changes after the upgrade.
@@ -98,9 +99,10 @@ without `pipx` it stops at that first command (exit 127). Install pipx with
 
 1. Refreshes the framework files in `~/.claude/`: 12 core files, 35 commands,
    48 agents, 35 skills, hooks, templates, rules and output styles, and merges
-   its hook entries into `~/.claude/settings.json`. A command, rule or
-   output-style file that differs from the shipped one is saved as
-   `<name>.bak.<UTC time>` first.
+   its hook entries into `~/.claude/settings.json`. A command, rule,
+   output-style, core, agent or template file that differs from the shipped one
+   is saved as `<name>.bak.<UTC time>` first. Releases 6.1.0 and earlier
+   overwrite core files, agents and templates with no copy.
 2. Installs codegraph 1.6.2: downloads the release for your platform, checks its
    SHA-256, extracts it under `~/.codegraph/`, links `~/.local/bin/codegraph`
    and registers it as a user-scope MCP server.

Task-owned evidence artifact artifacts/t17-test.log (a log the task wrote; cite it as ./artifacts/t17-test.log:<line>):
1: == AC1: remaining no copy/without a copy lines in 38-110 ==
2: 8:| Commands (`commands/sc/`), rules (`rules/`), output styles (`output-styles/`), core files (`CLAUDE.md`, `RULES.md` and the other core `.md` files), agents (`agents/`) and templates (`templates/`) | A copy is saved next to it as `<name>.bak.<UTC time>` (for example `analyze.md.bak.20261118T170151Z`) before the file is overwritten. See [Saved copies](#saved-copies-of-changed-files). Releases 6.1.0 and earlier overwrite core files, agents and templates with no copy. |
3: 9:| Skill folders (`skills/`) and hook scripts (`hooks/`) | Overwritten with no copy. Each shipped skill folder is deleted and copied again, so any file you added inside one is lost. |
4: 68:   overwrite core files, agents and templates with no copy.
5: == AC1: 6.1.0 qualifier ==
6: 45:| Commands (`commands/sc/`), rules (`rules/`), output styles (`output-styles/`), core files (`CLAUDE.md`, `RULES.md` and the other core `.md` files), agents (`agents/`) and templates (`templates/`) | A copy is saved next to it as `<name>.bak.<UTC time>` (for example `analyze.md.bak.20261118T170151Z`) before the file is overwritten. See [Saved copies](#saved-copies-of-changed-files). Releases 6.1.0 and earlier overwrite core files, agents and templates with no copy. |
7: 104:   is saved as `<name>.bak.<UTC time>` first. Releases 6.1.0 and earlier
8: == AC2: title and pin ==
9: # Upgrading to IronClaude 6.0.0
10: 67:`git+https://github.com/IronbellyOrg/IronClaude@v6.0.0` in the first command.
11: (no title/pin diff lines above = unchanged)
12: == AC3: table cells per row ==
13: 2 cells
14: 2 cells
15: 2 cells
16: 2 cells
17: 2 cells
18: | `settings.json` | Backed up as `settings.json.bak.<timesta
19: == changed hunks ==
20: @@ -45,2 +45,2 @@ your edited copy is saved first depends on the kind of file:
21: @@ -49 +49,3 @@ your edited copy is saved first depends on the kind of file:
22: @@ -52,2 +54 @@ Copy anything you changed in the second row first, for example:
23: @@ -101,3 +102,4 @@ without `pipx` it stops at that first command (exit 127). Install pipx with
24: 

Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:51:49Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-676
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-676
call codegraph only when index_state: fresh, never to widen scope
Q2b: documentation only (docs/getting-started/upgrading.md, Step 1 table and cp example at lines 43-58 and "What the upgrade does" step 1 at lines ~101-106). The "Saved copies of changed files" section (heading at about line 337) and the other "no copy" sentences in this file are Task 18, not this task, and were not touched here. The page title (line 1, 6.0.0) and the @v6.0.0 pin (now line 67, was 66 because the intro grew by two lines) are unchanged in content. W-2 was used with one addition ("(`superclaude install --force` or `superclaude update`)" after "either command") because this page names only install --force in the paragraph above. Wording kit W-1..W-4 is in the plan Constraints (plan line 28). Evidence log: ./artifacts/t17-test.log.
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
