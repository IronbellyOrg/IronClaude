961a4081861a60f337a6cc508f6c80130d6a46df
Review one task for spec compliance.

Task brief: ## Task 12: Correct the routing guide sentence and copy it to the plugin twin

In `src/superclaude/core/HOW-WE-WORK.md` line 3, replace the sentence that starts "`superclaude install --force` and `superclaude update` both overwrite every file they ship, including an edited `~/.claude/CLAUDE.md`, and keep no backup." through "...Copy any file you changed or added before you run either one." (this includes the sentence about deleting and re-copying each shipped skill folder) with W-1 followed by W-2 from the Constraints. Keep the rest of line 3 (the text before it about `superclaude install --force` refreshing the guide, and the text after it starting "Plugin installs ship only some of these commands and skills") exactly as it is. Then make `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` a byte-for-byte copy of the edited source file (for example with `cp`). Change nothing in the level-table block, the routing-table block or any other line.

Acceptance criteria:
- `diff src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing.
- `git diff -- src/superclaude/core/HOW-WE-WORK.md` shows only line 3 changed; the text "keep no backup" no longer appears in either file.
- `uv run pytest tests/commands/test_routing_plugin_parity.py tests/docs/test_onboarding_deck.py tests/cli/test_how_we_work_install.py tests/commands/test_worktrees_command.py tests/core/test_how_we_work_routing_table.py tests/skills/test_review_prompt_overrides.py -q` passes (`test_worktrees_command.py` reads both copies of the guide and asserts that other sentences are absent; `test_how_we_work_routing_table.py` fails on any non-ASCII character in the guide except the ruling example, so write W-1 and W-2 in plain ASCII; `test_review_prompt_overrides.py` checks that the guide and its plugin twin are byte-equal).

AC ids:
- T12.AC1: `diff src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing.
- T12.AC2: `git diff -- src/superclaude/core/HOW-WE-WORK.md` shows only line 3 changed; the text "keep no backup" no longer appears in either file.
- T12.AC3: `uv run pytest tests/commands/test_routing_plugin_parity.py tests/docs/test_onboarding_deck.py tests/cli/test_how_we_work_install.py tests/commands/test_worktrees_command.py tests/core/test_how_we_work_routing_table.py tests/skills/test_review_prompt_overrides.py -q` passes (`test_worktrees_command.py` reads both copies of the guide and asserts that other sentences are absent; `test_how_we_work_routing_table.py` fails on any non-ASCII character in the guide except the ruling example, so write W-1 and W-2 in plain ASCII; `test_review_prompt_overrides.py` checks that the guide and its plugin twin are byte-equal).
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
Start sha: 961a4081861a60f337a6cc508f6c80130d6a46df
Diff against the start snapshot: diff --git a/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md b/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
index 7f3147b4c..2bf32ecb8 100644
--- a/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
+++ b/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
@@ -1,6 +1,6 @@
 # IronClaude: How We Work
 
-This guide tells you which IronClaude skills and commands to use for each kind of work, and in what order. Keep it open while you work. `superclaude install` copies this guide to `~/.claude/HOW-WE-WORK.md`; after upgrading IronClaude run `superclaude install --force` to refresh that copy (it also installs codegraph and retires old MCP registrations; `superclaude update` refreshes files only). `superclaude install --force` and `superclaude update` both overwrite every file they ship, including an edited `~/.claude/CLAUDE.md`, and keep no backup. They also delete and re-copy each shipped skill folder in `~/.claude/skills/`, so any file you added inside one is lost. Copy any file you changed or added before you run either one. Plugin installs ship only some of these commands and skills; for the full set run `pipx install git+https://github.com/IronbellyOrg/IronClaude && superclaude install` (the `superclaude` package on PyPI is the upstream project, not IronClaude).
+This guide tells you which IronClaude skills and commands to use for each kind of work, and in what order. Keep it open while you work. `superclaude install` copies this guide to `~/.claude/HOW-WE-WORK.md`; after upgrading IronClaude run `superclaude install --force` to refresh that copy (it also installs codegraph and retires old MCP registrations; `superclaude update` refreshes files only). `superclaude install --force` and `superclaude update` overwrite every file they ship. When a command, rule, output-style, core, agent or template file differs from the shipped one, the installer first saves a copy next to it as `<name>.bak.<UTC time>`. Skill folders (deleted and re-copied) and hook scripts get no copy. Copy any file you changed or added inside a skill folder, and any hook script you changed, to a place outside `~/.claude/skills/` before you run either command. Plugin installs ship only some of these commands and skills; for the full set run `pipx install git+https://github.com/IronbellyOrg/IronClaude && superclaude install` (the `superclaude` package on PyPI is the upstream project, not IronClaude).
 
 ---
 
diff --git a/src/superclaude/core/HOW-WE-WORK.md b/src/superclaude/core/HOW-WE-WORK.md
index 7f3147b4c..2bf32ecb8 100644
--- a/src/superclaude/core/HOW-WE-WORK.md
+++ b/src/superclaude/core/HOW-WE-WORK.md
@@ -1,6 +1,6 @@
 # IronClaude: How We Work
 
-This guide tells you which IronClaude skills and commands to use for each kind of work, and in what order. Keep it open while you work. `superclaude install` copies this guide to `~/.claude/HOW-WE-WORK.md`; after upgrading IronClaude run `superclaude install --force` to refresh that copy (it also installs codegraph and retires old MCP registrations; `superclaude update` refreshes files only). `superclaude install --force` and `superclaude update` both overwrite every file they ship, including an edited `~/.claude/CLAUDE.md`, and keep no backup. They also delete and re-copy each shipped skill folder in `~/.claude/skills/`, so any file you added inside one is lost. Copy any file you changed or added before you run either one. Plugin installs ship only some of these commands and skills; for the full set run `pipx install git+https://github.com/IronbellyOrg/IronClaude && superclaude install` (the `superclaude` package on PyPI is the upstream project, not IronClaude).
+This guide tells you which IronClaude skills and commands to use for each kind of work, and in what order. Keep it open while you work. `superclaude install` copies this guide to `~/.claude/HOW-WE-WORK.md`; after upgrading IronClaude run `superclaude install --force` to refresh that copy (it also installs codegraph and retires old MCP registrations; `superclaude update` refreshes files only). `superclaude install --force` and `superclaude update` overwrite every file they ship. When a command, rule, output-style, core, agent or template file differs from the shipped one, the installer first saves a copy next to it as `<name>.bak.<UTC time>`. Skill folders (deleted and re-copied) and hook scripts get no copy. Copy any file you changed or added inside a skill folder, and any hook script you changed, to a place outside `~/.claude/skills/` before you run either command. Plugin installs ship only some of these commands and skills; for the full set run `pipx install git+https://github.com/IronbellyOrg/IronClaude && superclaude install` (the `superclaude` package on PyPI is the upstream project, not IronClaude).
 
 ---

Task-owned evidence artifact artifacts/t12-test.log (a log the task wrote; cite it as ./artifacts/t12-test.log:<line>):
1: $ diff src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
2: (prints nothing: identical)
3: 
4: $ git diff --stat -- src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
5:  plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md | 2 +-
6:  src/superclaude/core/HOW-WE-WORK.md                         | 2 +-
7:  2 files changed, 2 insertions(+), 2 deletions(-)
8: changed line numbers in the source guide: @@ -3 +3 @@ 
9: non-ASCII characters on the changed line: 0
10: 
11: $ grep -c "keep no backup" (both files)
12: src/superclaude/core/HOW-WE-WORK.md:0
13: plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:0
14: 
15: $ uv run pytest -p no:cacheprovider tests/commands/test_routing_plugin_parity.py tests/docs/test_onboarding_deck.py tests/cli/test_how_we_work_install.py tests/commands/test_worktrees_command.py tests/core/test_how_we_work_routing_table.py tests/skills/test_review_prompt_overrides.py -q
16: ...                                                                      [100%]
17: 
18: ============================= 121 passed in 1.65s ==============================
19: 
20: $ uv run pytest -p no:cacheprovider tests/core tests/recommend tests/skills/test_sc_recommend_routing_contract.py -q   (other readers of the guide, extra)
21: ......                                                                   [100%]
22: 
23: ============================= 333 passed in 4.34s ==============================
24: 

Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:51:49Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-676
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-676
call codegraph only when index_state: fresh, never to widen scope
Q2b: documentation only (no code symbol). Readers of the guide that were run (see ./artifacts/t12-test.log): tests/commands/test_routing_plugin_parity.py, tests/docs/test_onboarding_deck.py, tests/cli/test_how_we_work_install.py, tests/commands/test_worktrees_command.py, tests/core/test_how_we_work_routing_table.py, tests/skills/test_review_prompt_overrides.py and, as an extra, tests/core, tests/recommend and tests/skills/test_sc_recommend_routing_contract.py. The level-table block of src/superclaude/core/CLAUDE.md is not affected (line 3 is outside it). `make sync-dev` does not mirror the guide (it copies skills, agents, commands, hooks and templates).
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
