5deb85f67a6b9775ccbf9e06026aa1fa207c3bbc
Review one task for spec compliance.

Task brief: ## Task 20: Add the CHANGELOG entry and confirm the whole change is limited to its scope

Depends on: Task 9, Task 10, Task 19

In `CHANGELOG.md`, under `## [Unreleased]` (line 5), add one entry above the existing first entry, in the file's style (a `###` heading naming the change and issue, then a bullet): heading "Installers: core files, agents and templates are saved before `--force` and `update` overwrite them (issue 676)"; bullet "`superclaude install --force` and `superclaude update` now save a core file, agent or template that differs from the shipped one as `<name>.bak.<UTC time>` next to it, as they already did for commands, rules and output styles. A save that fails leaves that file as it was, lists it as failed and makes the command exit 1. `install --list` no longer counts these copies as installed templates. Skill folders and hook scripts are still overwritten with no copy. Releases 6.1.0 and earlier overwrite core files, agents and templates with no copy."

Run `make sync-dev` before the gate commands below, so the gitignored `.claude/` mirrors exist for `make verify-sync`.

Acceptance criteria:
- The `[Unreleased]` section has exactly this one new entry and no released entry changed.
- `grep -n "backup_if_differs(" src/superclaude/cli/*.py` shows exactly five call sites besides the definition: `install_commands.py`, `install_user_setup.py`, `install_core.py`, `install_agents.py` and `install_templates.py`.
- `git diff --stat` shows no change to `src/superclaude/cli/main.py`, and `git diff -- src/superclaude/cli/install_keep.py` shows only the docstring hunk.
- `git status --porcelain` lists, outside `.dev/`, only the three installers, `install_keep.py`, `tests/cli/test_install_keep.py`, `tests/cli/test_update_command.py`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `CHANGELOG.md` and the documentation files named in Tasks 13 to 19. Paths under `.dev/` (the task package, `progress.md`, reflect and brainstorm artifacts) are outside this check, and `.dev/tasks/` stays staged.
- `uv run pytest tests/cli/test_install_keep.py tests/cli/test_update_command.py tests/cli/test_install_failures.py tests/cli/test_how_we_work_install.py tests/commands/test_routing_plugin_parity.py tests/docs/test_onboarding_deck.py tests/unit/test_cli_install.py -q` and `uv run pytest tests/cli tests/unit -q` pass.
- `uv run pytest tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_merge_guard_protocol.py tests/commands/test_worktrees_command.py tests/core/test_how_we_work_routing_table.py tests/skills/test_review_prompt_overrides.py -q` passes (these read `CHANGELOG.md`, `flags.md` or the guide copies and pin text other than this entry).
- After `make sync-dev`, `make verify-sync` exits 0 and `git diff --cached --name-only -- .claude` prints nothing.

AC ids:
- T20.AC1: The `[Unreleased]` section has exactly this one new entry and no released entry changed.
- T20.AC2: `grep -n "backup_if_differs(" src/superclaude/cli/*.py` shows exactly five call sites besides the definition: `install_commands.py`, `install_user_setup.py`, `install_core.py`, `install_agents.py` and `install_templates.py`.
- T20.AC3: `git diff --stat` shows no change to `src/superclaude/cli/main.py`, and `git diff -- src/superclaude/cli/install_keep.py` shows only the docstring hunk.
- T20.AC4: `git status --porcelain` lists, outside `.dev/`, only the three installers, `install_keep.py`, `tests/cli/test_install_keep.py`, `tests/cli/test_update_command.py`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `CHANGELOG.md` and the documentation files named in Tasks 13 to 19. Paths under `.dev/` (the task package, `progress.md`, reflect and brainstorm artifacts) are outside this check, and `.dev/tasks/` stays staged.
- T20.AC5: `uv run pytest tests/cli/test_install_keep.py tests/cli/test_update_command.py tests/cli/test_install_failures.py tests/cli/test_how_we_work_install.py tests/commands/test_routing_plugin_parity.py tests/docs/test_onboarding_deck.py tests/unit/test_cli_install.py -q` and `uv run pytest tests/cli tests/unit -q` pass.
- T20.AC6: `uv run pytest tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_merge_guard_protocol.py tests/commands/test_worktrees_command.py tests/core/test_how_we_work_routing_table.py tests/skills/test_review_prompt_overrides.py -q` passes (these read `CHANGELOG.md`, `flags.md` or the guide copies and pin text other than this entry).
- T20.AC7: After `make sync-dev`, `make verify-sync` exits 0 and `git diff --cached --name-only -- .claude` prints nothing.
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
Start sha: 5deb85f67a6b9775ccbf9e06026aa1fa207c3bbc
Diff against the start snapshot: diff --git a/CHANGELOG.md b/CHANGELOG.md
index eb86c8e51..5665aa66e 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -4,6 +4,10 @@ All notable changes to IronClaude are documented in this file.
 
 ## [Unreleased]
 
+### Installers: core files, agents and templates are saved before `--force` and `update` overwrite them (issue 676)
+
+- `superclaude install --force` and `superclaude update` now save a core file, agent or template that differs from the shipped one as `<name>.bak.<UTC time>` next to it, as they already did for commands, rules and output styles. A save that fails leaves that file as it was, lists it as failed and makes the command exit 1. `install --list` no longer counts these copies as installed templates. Skill folders and hook scripts are still overwritten with no copy. Releases 6.1.0 and earlier overwrite core files, agents and templates with no copy.
+
 ### New command: /sc:worktrees and scripts/worktree_cleanup.py (issue 687)
 
 - `/sc:worktrees <list|archive|retire|prune>` removes git worktrees of our repos once their work is finished. A worktree goes only when its own pull request is merged, nothing was added after it, its issues are closed, nothing unsaved is in it, nothing but its own Orca terminals is using it, it has been idle for 7 days and it is not pinned. `list`, `retire` and `prune` are dry runs unless `--apply` is typed; `archive` is the one verb that writes without it (to the evidence repo only, and it removes nothing). Before a removal, the untracked and ignored `.dev/` files are saved to the evidence repo `IronbellyOrg/run-evidence` and checked against GitHub; if anything cannot be read or saved, the worktree is kept and the reason is shown. The script is `scripts/worktree_cleanup.py` (Python standard library only), and the command is on the never-as-worker list. The removal rules are adapted from files of Jay Wedgeworth's AI-Fleet-Coordinator under Apache-2.0; see `scripts/worktree_cleanup_PROVENANCE.md` and `NOTICE`. A definition for a daily Orca automation is in `scripts/worktree_cleanup_orca_automation.md`; it is written and not switched on.

Task-owned evidence artifact artifacts/t20-test.log (a log the task wrote; cite it as ./artifacts/t20-test.log:<line>):
1: == make sync-dev ==
2:    Agents:    49 files
3:    Commands:  36 files
4:    Hooks:     17 files
5:    Templates: 52 files
6: == AC3 backup_if_differs( call sites ==
7: src/superclaude/cli/install_agents.py:61:                backup = backup_if_differs(agent_file, target_file)
8: src/superclaude/cli/install_commands.py:68:                backup = backup_if_differs(command_file, target_file)
9: src/superclaude/cli/install_core.py:79:                backup = backup_if_differs(src_file, dest_file)
10: src/superclaude/cli/install_keep.py:42:def backup_if_differs(shipped: Path, target: Path) -> Path | None:
11: src/superclaude/cli/install_templates.py:81:                backup = backup_if_differs(src_file, dest)
12: src/superclaude/cli/install_user_setup.py:114:                backup = backup_if_differs(src, target)
13: == AC3 main.py diff and install_keep diff hunks ==
14: 0
15: 1
16: -``install --force`` and ``update`` overwrite, so a differing file is saved
17: -next to itself first (``<name>.bak.<UTC stamp>``, which Claude Code does not
18: -load) and the overwrite is skipped when that save fails.
19: +``install --force`` and ``update`` overwrite, so the commands, rules,
20: +output-styles, core, agent and template installers first save a differing file
21: +next to itself (``<name>.bak.<UTC stamp>``, which Claude Code does not load) and
22: +skip the overwrite when that save fails. Skill folders and hook scripts do not
23: +use this helper: they are overwritten with no copy.
24: == AC4 git status outside .dev ==
25:  M CHANGELOG.md
26:  M docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md
27:  M docs/getting-started/installation.md
28:  M docs/getting-started/upgrading.md
29:  M docs/onboarding/ironclaude-onboarding.html
30:  M docs/reference/troubleshooting.md
31:  M docs/user-guide/flags.md
32:  M docs/user-guide/how-we-work.md
33:  M plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
34:  M src/superclaude/cli/install_agents.py
35:  M src/superclaude/cli/install_core.py
36:  M src/superclaude/cli/install_keep.py
37:  M src/superclaude/cli/install_templates.py
38:  M src/superclaude/core/HOW-WE-WORK.md
39:  M tests/cli/test_install_keep.py
40:  M tests/cli/test_update_command.py
41: == AC5a focused set ==
42: .....................................................                    [100%]
43: 
44: ============================= 198 passed in 4.06s ==============================
45: == AC6 doc readers ==
46: ...                                                                      [100%]
47: 
48: ============================= 243 passed in 1.16s ==============================
49: == AC7 verify-sync ==
50: verify-sync exit=0
51:   ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes
52: 
53: ✅ All components in sync.
54: == staged .claude paths (expect none) ==
55: 0
56: == AC1 CHANGELOG diff ==
57: @@ -6,0 +7,4 @@ All notable changes to IronClaude are documented in this file.
58: +### Installers: core files, agents and templates are saved before `--force` and `update` overwrite them (issue 676)
59: +
60: +- `superclaude install --force` and `superclaude update` now save a core file, agent or template that differs from the 
61: +
62: == AC5b full tests/cli + tests/unit ==
63: 
64: -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
65: =========== 3297 passed, 7 skipped, 5 warnings in 499.76s (0:08:19) ============
66: exit=0
67: 

Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:51:49Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-676
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-676
call codegraph only when index_state: fresh, never to widen scope
Q2b: documentation only for the edit (CHANGELOG.md, one new entry under [Unreleased]); the rest of Task 20 is a set of gate commands whose output is in ./artifacts/t20-test.log: make sync-dev, the backup_if_differs( call-site grep, the main.py and install_keep.py diffs, git status outside .dev/, the focused pytest set (198 passed), the doc-reader pytest set (243 passed), the full tests/cli + tests/unit run (3297 passed, 7 skipped, exit 0), make verify-sync (exit 0) and the staged-.claude check (0 paths). The git status list in the log is taken with `git status --porcelain | grep -v ' .dev/'`; every listed path is one the plan allows (installers, install_keep.py, the two test files, the two guide copies, CHANGELOG.md and the documentation files of Tasks 13 to 19). Wording of the entry is the text given in the plan (Task 20) word for word.
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
