ce3bd8e3688ff6406695701e98497f46b099798c
Review one task for spec compliance.

Task brief: ## Task 14: Rewrite the onboarding deck card at docs/onboarding/ironclaude-onboarding.html:510

Depends on: Task 12

At line 510 the card `<div class="card"><h3><code>superclaude update</code> overwrites</h3><p>It overwrites every file it ships, including an edited <code>~/.claude/CLAUDE.md</code>, keeps no backup, and deletes and re-copies each shipped skill folder...` becomes plain sentences with the W-1 rule: every file it ships is overwritten; a command, rule, output-style, core, agent or template file that differs is first saved as `<name>.bak.<UTC time>`; skill folders are deleted and re-copied and hook scripts are overwritten with no copy, so copy any skill file or hook script you changed or added to a place outside `~/.claude/skills/` before you run it. Keep `superclaude update` in the heading `<code>`; do not put a `/command` or `--flag` token inside a `<code>` element unless `src/superclaude/core/HOW-WE-WORK.md` states that same token, because `tests/docs/test_onboarding_deck.py` (lines 83-87) fails on any token the guide lacks.

Acceptance criteria:
- `uv run pytest tests/docs/test_onboarding_deck.py -q` passes.
- The card's rendered text names the saved copy as `<name>.bak.<UTC time>` (written with `&lt;` and `&gt;` in the HTML source, so a literal search of the source for the angle brackets finds nothing) and names skill folders and hook scripts as the files with no copy; the card advises copying to a place outside `~/.claude/skills/`; the words "keeps no backup" no longer appear in the file.
- The rest of the HTML file is unchanged, except the footer line that starts "Built from HOW-WE-WORK.md at commit": the deck's own maintenance rule (the comment at the top of the file) requires it to name the commit that carries the guide change, so update it when that commit exists, otherwise leave it and record in the pull request that the footer and the re-publish of the deck are a follow-up. `uv run pytest tests/docs/test_onboarding_deck.py -q` still passes either way.

AC ids:
- T14.AC1: `uv run pytest tests/docs/test_onboarding_deck.py -q` passes.
- T14.AC2: The card's rendered text names the saved copy as `<name>.bak.<UTC time>` (written with `&lt;` and `&gt;` in the HTML source, so a literal search of the source for the angle brackets finds nothing) and names skill folders and hook scripts as the files with no copy; the card advises copying to a place outside `~/.claude/skills/`; the words "keeps no backup" no longer appear in the file.
- T14.AC3: The rest of the HTML file is unchanged, except the footer line that starts "Built from HOW-WE-WORK.md at commit": the deck's own maintenance rule (the comment at the top of the file) requires it to name the commit that carries the guide change, so update it when that commit exists, otherwise leave it and record in the pull request that the footer and the re-publish of the deck are a follow-up. `uv run pytest tests/docs/test_onboarding_deck.py -q` still passes either way.
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
Start sha: ce3bd8e3688ff6406695701e98497f46b099798c
Diff against the start snapshot: diff --git a/docs/onboarding/ironclaude-onboarding.html b/docs/onboarding/ironclaude-onboarding.html
index df0797f7b..81b0cde96 100644
--- a/docs/onboarding/ironclaude-onboarding.html
+++ b/docs/onboarding/ironclaude-onboarding.html
@@ -507,7 +507,7 @@
   <h2 id="s11-h">Where things live</h2>
   <div class="grid2">
     <div class="card"><h3>Work is written to files</h3><p>Plans, research and findings are saved to files, most under <code>.dev/</code>, not only into the chat. If a session dies, the files are what survives.</p></div>
-    <div class="card"><h3><code>superclaude update</code> overwrites</h3><p>It overwrites every file it ships, including an edited <code>~/.claude/CLAUDE.md</code>, keeps no backup, and deletes and re-copies each shipped skill folder, so any file you added inside one is lost. Copy any file you changed or added before you run it.</p></div>
+    <div class="card"><h3><code>superclaude update</code> overwrites</h3><p>It overwrites every file it ships. When a command, rule, output-style, core (such as <code>~/.claude/CLAUDE.md</code>), agent or template file differs from the shipped one, it first saves a copy next to it as <code>&lt;name&gt;.bak.&lt;UTC time&gt;</code>. Skill folders are deleted and re-copied, so any file you added inside one is lost, and hook scripts are overwritten; neither gets a copy. Copy any skill file or hook script you changed or added to a place outside <code>~/.claude/skills/</code> before you run it.</p></div>
     <div class="card"><h3>Resume after a crash</h3><p>Before you need it, name the conversation with <code>/rename &lt;name&gt;</code> and send one more message (or quit) so ccsession records it; later, from a terminal in the same folder, run <code>ccsession &lt;name&gt;</code>.</p><p>This always works: run the same command again on the work's own files, <code>/sc:implement</code> on the plan.</p></div>
   </div>
 </section>

Task-owned evidence artifact artifacts/t14-test.log (a log the task wrote; cite it as ./artifacts/t14-test.log:<line>):
1: == keeps no backup ==
2: 0
3: == literal angle brackets in card ==
4: 0
5: == outside skills ==
6: outside <code>~/.claude/skills/</code>
7: == diff stat ==
8:  docs/onboarding/ironclaude-onboarding.html | 2 +-
9:  1 file changed, 1 insertion(+), 1 deletion(-)
10: == pytest ==
11: tests/docs/test_onboarding_deck.py ...                                   [100%]
12: 
13: ============================== 3 passed in 0.06s ===============================
14: 

Codegraph context
index_state: fresh
checked_at: 2026-11-26T05:51:49Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-676
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-676
call codegraph only when index_state: fresh, never to widen scope
Q2b: documentation only (one HTML card at docs/onboarding/ironclaude-onboarding.html:510). The reader that was run is tests/docs/test_onboarding_deck.py (3 passed, see ./artifacts/t14-test.log); it fails on any /command or --flag token inside a <code> element that src/superclaude/core/HOW-WE-WORK.md lacks. The footer line 579 ("Built from HOW-WE-WORK.md at commit f3c1ef06") was deliberately left unchanged: the plan says to update it only when the commit that carries the guide change exists, otherwise leave it and record in the pull request that the footer and the re-publish of the deck are a follow-up. That commit does not exist yet, so leaving it is correct for this task.
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
