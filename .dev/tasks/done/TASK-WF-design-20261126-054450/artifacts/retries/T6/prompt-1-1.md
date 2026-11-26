b6b13d7a1db459ba3d7deee303f2a793bd6cea4f
Review one task for spec compliance.

Task brief: ## Task 6: Make list_installed_templates ignore backup files

In `src/superclaude/cli/install_templates.py`, function `list_installed_templates()` (line 145), add one more condition to the comprehension filter (lines 150-156), next to `f.is_file()`, `"__pycache__" not in f.parts` and the `_PROTECTED_TARGET_SUBDIRS` check: `".bak." not in f.name`. Do not filter on the `.md` suffix, because a non-`.md` template ships (`modularization-template-review/synthetic-dnsp-finding.contract`). Leave `list_available_templates()` unchanged.

Acceptance criteria:
- With `Path.home` patched to a temporary folder holding the installed templates plus an extra `workflow/<file>.bak.20261126T000000Z` and a `workflow/<file>.bak.20261126T000000Z-2`, `list_installed_templates()` omits both and its length equals `len(list_available_templates())`.
- A non-`.md` shipped template such as `synthetic-dnsp-finding.contract` is still listed as installed after a normal install.
- `install --list` (`src/superclaude/cli/main.py` lines 143-155, the only caller of `list_installed_templates`) prints `Templates: N available, N installed` with equal N for an isolated home that holds only shipped templates and their backups.
- The consumer inventory still holds, as a reviewed list of readers (the grep hits unrelated code, so its output needs a reader's judgement, not a mechanical count): `grep -rnE 'rglob\("\*"\)|glob\("\*"\)|iterdir\(|os\.walk\(|scandir|listdir' src tests` shows no hit that reads the agents folder, the templates folder or the `~/.claude/` root without a filter, other than `list_installed_templates` with the new condition. Other readers match `*.md`, known names or exact names: `install_agents.py` line 141, `install_core.py` line 171, `doctor.py` line 315, `src/superclaude/cli/recommend/prompts.py` line 135 and `install_retired_files.py` line 201. A grep cannot see a pattern built at runtime or the host's own loader; say so in the task's notes if a new reader turns up.

AC ids:
- T6.AC1: With `Path.home` patched to a temporary folder holding the installed templates plus an extra `workflow/<file>.bak.20261126T000000Z` and a `workflow/<file>.bak.20261126T000000Z-2`, `list_installed_templates()` omits both and its length equals `len(list_available_templates())`.
- T6.AC2: A non-`.md` shipped template such as `synthetic-dnsp-finding.contract` is still listed as installed after a normal install.
- T6.AC3: `install --list` (`src/superclaude/cli/main.py` lines 143-155, the only caller of `list_installed_templates`) prints `Templates: N available, N installed` with equal N for an isolated home that holds only shipped templates and their backups.
- T6.AC4: The consumer inventory still holds, as a reviewed list of readers (the grep hits unrelated code, so its output needs a reader's judgement, not a mechanical count): `grep -rnE 'rglob\("\*"\)|glob\("\*"\)|iterdir\(|os\.walk\(|scandir|listdir' src tests` shows no hit that reads the agents folder, the templates folder or the `~/.claude/` root without a filter, other than `list_installed_templates` with the new condition. Other readers match `*.md`, known names or exact names: `install_agents.py` line 141, `install_core.py` line 171, `doctor.py` line 315, `src/superclaude/cli/recommend/prompts.py` line 135 and `install_retired_files.py` line 201. A grep cannot see a pattern built at runtime or the host's own loader; say so in the task's notes if a new reader turns up.
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
Start sha: b6b13d7a1db459ba3d7deee303f2a793bd6cea4f
Diff against the start snapshot: diff --git a/src/superclaude/cli/install_templates.py b/src/superclaude/cli/install_templates.py
index 91f2cfd95..8fd5d9d29 100644
--- a/src/superclaude/cli/install_templates.py
+++ b/src/superclaude/cli/install_templates.py
@@ -172,5 +172,6 @@ def list_installed_templates() -> List[str]:
         for f in target.rglob("*")
         if f.is_file()
         and "__pycache__" not in f.parts
+        and ".bak." not in f.name  # saved copies made by install --force and update
         and not any(p in _PROTECTED_TARGET_SUBDIRS for p in f.relative_to(target).parts)
     )

Task-owned evidence artifact artifacts/t6-test.log (a log the task wrote; cite it as ./artifacts/t6-test.log:<line>):
1: $ ad hoc behaviour check of list_installed_templates and install --list (script /tmp/impl676/t6_check.py, not committed)
2: AC1 backups on disk: 2 | omitted from the listing: True | installed length == available length: True 53 53
3: AC2 non-.md template still listed: True
4: AC3 install --list exit: 0 | ['Templates: 53 available, 53 installed']
5: AC3 equal counts: True | backups still on disk after the listing: 2
6: 
7: $ grep -rnE 'rglob\("\*"\)|glob\("\*"\)|iterdir\(|os\.walk\(|scandir|listdir' src tests --include=*.py | wc -l
8: 335
9: Reviewed list of the readers that touch the agents folder, the templates folder or the ~/.claude root (hits in src that name install/doctor/templates/agents paths):
10: install_templates.py:172 list_installed_templates = the one unfiltered reader, now with the .bak. condition (src/superclaude/cli/install_templates.py:176)
11: install_templates.py:61 and :158 walk the shipped SOURCE tree, not ~/.claude
12: install_retired_files.py:109 and :256 walk a skill folder (skills are not backed up)
13: install_skills.py:166, doctor.py:343, install_skill.py:109,137 walk ~/.claude/skills
14: install_user_setup.py:103 walks the shipped source of rules/output styles
15: sweep/probes.py:671 walks .dev/tasks; probes.py:1456 walks ~/.claude/projects/<key> (session logs)
16: Readers that match *.md, known names or exact names: install_agents.py list_installed_agents, install_core.py list_installed_core_files, doctor.py:315, recommend/prompts.py:135, install_retired_files.py:201
17: (a grep cannot see a pattern built at runtime or the host loader)
18: 

Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:51:49Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-676
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-676
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents of list_installed_templates not in the diff: src/superclaude/cli/main.py:144 (install --list; count line main.py:153-155); tests stub it in tests/cli/test_update_command.py:164 (_stub_listings). Callers confirmed by Read; the reader inventory for AC4 is in ./artifacts/t6-test.log.
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
