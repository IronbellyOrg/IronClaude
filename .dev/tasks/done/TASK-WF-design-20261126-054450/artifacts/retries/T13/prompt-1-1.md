6e1359c3e8100702766409c8427541ca37ad0b35
Review one task for spec compliance.

Task brief: ## Task 13: Correct the user guide pages docs/user-guide/how-we-work.md and docs/user-guide/flags.md

Depends on: Task 12

- In `docs/user-guide/how-we-work.md` line 3, the sentence "...a command, rule or output-style file that differs from the shipped one is first saved as `<name>.bak.<UTC time>`; an edited core file such as `~/.claude/CLAUDE.md`, an agent or a skill is overwritten with no copy. They also delete and re-copy each shipped skill folder in `~/.claude/skills/`, so any file you add..." becomes the same rule as W-1 and W-2 in its own prose: the six backed-up categories are saved first, skill folders and hook scripts get no copy, and the advice names skill files and hook scripts.
- In `docs/user-guide/flags.md` line 233 (the `--force` row), replace "it saves a differing command, rule or output-style file as `<name>.bak.<UTC time>` first, overwrites edited core files and agents without a copy, and re-copies skill folders" with W-1 in the row's compact style: the six categories are saved first, skill folders are re-copied, and hook scripts are overwritten with no copy.

Acceptance criteria:
- Neither file says that core files, agents or templates are overwritten with no copy; both name skill folders and hook scripts as the files that get no copy.
- The `--force` table row in `flags.md` still has its other cells and column count unchanged.
- `grep -nE "no copy|without a copy|no backup" docs/user-guide/how-we-work.md docs/user-guide/flags.md` prints only lines about skill folders or hook scripts.
- `uv run pytest tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_merge_guard_protocol.py tests/commands/test_worktrees_command.py -q` passes: the first pins another sentence in `docs/user-guide/flags.md` (the pr-submit late re-sync sentence) and the second reads `flags.md` too, so only the `--force` row may change there.

AC ids:
- T13.AC1: Neither file says that core files, agents or templates are overwritten with no copy; both name skill folders and hook scripts as the files that get no copy.
- T13.AC2: The `--force` table row in `flags.md` still has its other cells and column count unchanged.
- T13.AC3: `grep -nE "no copy|without a copy|no backup" docs/user-guide/how-we-work.md docs/user-guide/flags.md` prints only lines about skill folders or hook scripts.
- T13.AC4: `uv run pytest tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_merge_guard_protocol.py tests/commands/test_worktrees_command.py -q` passes: the first pins another sentence in `docs/user-guide/flags.md` (the pr-submit late re-sync sentence) and the second reads `flags.md` too, so only the `--force` row may change there.
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
Start sha: 6e1359c3e8100702766409c8427541ca37ad0b35
Diff against the start snapshot: diff --git a/docs/user-guide/flags.md b/docs/user-guide/flags.md
index 762f96221..348a3e534 100644
--- a/docs/user-guide/flags.md
+++ b/docs/user-guide/flags.md
@@ -230,7 +230,7 @@ Like the flags at the top of this page, the flags under Scope and Focus and Exec
 | `--help` | `superclaude --help`, or `superclaude <subcommand> --help` | Show the options of the command or subcommand |
 | `--verbose` | `superclaude doctor --verbose` | Show detailed diagnostic information |
 | `--dry-run` | `superclaude mcp --dry-run` | Show what would happen without doing it |
-| `--force` | `superclaude install --force`, `superclaude install-skill <name> --force` | Reinstall even if the files already exist. `install --force` is required to refresh existing files (for example in the upgrades to 5.0.0 and 6.0.0), because a plain `install` skips existing files; it saves a differing command, rule or output-style file as `<name>.bak.<UTC time>` first, overwrites edited core files and agents without a copy, and re-copies skill folders |
+| `--force` | `superclaude install --force`, `superclaude install-skill <name> --force` | Reinstall even if the files already exist. `install --force` is required to refresh existing files (for example in the upgrades to 5.0.0 and 6.0.0), because a plain `install` skips existing files; it saves a differing command, rule, output-style, core, agent or template file as `<name>.bak.<UTC time>` first, re-copies skill folders, and overwrites hook scripts, with no copy of either |
 | `--list` | `superclaude install --list` | List the framework components without installing |
 
 ## Flag Interactions
diff --git a/docs/user-guide/how-we-work.md b/docs/user-guide/how-we-work.md
index fedba1195..d20b55dcc 100644
--- a/docs/user-guide/how-we-work.md
+++ b/docs/user-guide/how-we-work.md
@@ -1,3 +1,3 @@
 # How We Work
 
-Which IronClaude command or skill to use for each kind of work, in what order, and with which required flags, is written down in one place: the IronClaude guide [`HOW-WE-WORK.md`](../../src/superclaude/core/HOW-WE-WORK.md). It sorts every job into six levels, from "ask a question" to "write a full specification", sets the hard limit on how much change may skip a written plan, gives step-by-step workflows for building, fixing, investigating, reviewing, and resuming work, and ends with the routing table that `/sc:recommend` reads. `/sc:help` prints its level table and hard limit. `superclaude install` copies the guide to `~/.claude/HOW-WE-WORK.md`, so you can open it from any project; after upgrading run `superclaude install --force` to refresh that copy (it also installs codegraph and retires old MCP registrations; `superclaude update` refreshes files only). `superclaude install --force` and `superclaude update` both overwrite every file they ship. A command, rule or output-style file that differs from the shipped one is first saved as `<name>.bak.<UTC time>`; an edited core file such as `~/.claude/CLAUDE.md`, an agent or a skill is overwritten with no copy. They also delete and re-copy each shipped skill folder in `~/.claude/skills/`, so any file you added inside one is lost. Copy any core file, agent or skill you changed or added before you run either one. If you are still unsure which tool fits your job, run `/sc:recommend "<what you want to do, and why>"`.
+Which IronClaude command or skill to use for each kind of work, in what order, and with which required flags, is written down in one place: the IronClaude guide [`HOW-WE-WORK.md`](../../src/superclaude/core/HOW-WE-WORK.md). It sorts every job into six levels, from "ask a question" to "write a full specification", sets the hard limit on how much change may skip a written plan, gives step-by-step workflows for building, fixing, investigating, reviewing, and resuming work, and ends with the routing table that `/sc:recommend` reads. `/sc:help` prints its level table and hard limit. `superclaude install` copies the guide to `~/.claude/HOW-WE-WORK.md`, so you can open it from any project; after upgrading run `superclaude install --force` to refresh that copy (it also installs codegraph and retires old MCP registrations; `superclaude update` refreshes files only). `superclaude install --force` and `superclaude update` both overwrite every file they ship. When a command, rule, output-style, core (such as `~/.claude/CLAUDE.md`), agent or template file differs from the shipped one, the installer first saves a copy next to it as `<name>.bak.<UTC time>`. Skill folders in `~/.claude/skills/` (deleted and re-copied, so any file you added inside one is lost) and hook scripts get no copy. Copy any file you changed or added inside a skill folder, and any hook script you changed, to a place outside `~/.claude/skills/` before you run either one. If you are still unsure which tool fits your job, run `/sc:recommend "<what you want to do, and why>"`.

Task-owned evidence artifact artifacts/t13-test.log (a log the task wrote; cite it as ./artifacts/t13-test.log:<line>):
1: == AC3 grep ==
2: docs/user-guide/how-we-work.md:3:Which IronClaude command or
3: docs/user-guide/flags.md:233:| `--force` | `superclaude inst
4: == flags.md row 233 column count ==
5: 3 cells
6: 3 cells (neighbour row)
7: == pytest ==
8: tests/pr_submit/test_merge_guard_protocol.py ........................... [ 72%]
9: .............................                                            [ 92%]
10: tests/commands/test_worktrees_command.py ............                    [100%]
11: 
12: ============================= 151 passed in 0.52s ==============================
13: 

Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:51:49Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-676
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-676
call codegraph only when index_state: fresh, never to widen scope
Q2b: documentation only (no code symbol). Readers of flags.md that were run (see ./artifacts/t13-test.log): tests/pr_submit/test_conflict_sync_protocol.py (pins the pr-submit late re-sync sentence), tests/pr_submit/test_merge_guard_protocol.py, tests/commands/test_worktrees_command.py; all 151 pass. Only the --force row of flags.md and line 3 of how-we-work.md changed. The same rule wording (W-1, W-2 of the plan Constraints) is in src/superclaude/core/HOW-WE-WORK.md line 3 (Task 12, already reviewed compliant); how-we-work.md is written in its own prose, so it need not be word-for-word.
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
