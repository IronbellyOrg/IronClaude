f44b056a9e7996eeff8c498c492644c004e30332
Review one task for spec compliance.

Task brief: ## Task 5: Update the build footer of the onboarding page

Depends on: Task 4

In `docs/onboarding/ironclaude-onboarding.html` line 579, replace `f3c1ef06` in the footer `Built from HOW-WE-WORK.md at commit f3c1ef06.` with the 8-character hash printed by `git rev-parse --short=8 HEAD` at the time of this edit. The commit that will hold the guide change does not exist yet, so a person corrects the footer when the artifact is re-published after the merge; that is a known limit and it is written in the pull request body, not in the page. The page's own maintenance rule (lines 3-5 of the file) requires the footer to be updated in the same pull request as a guide change.

Acceptance criteria:
T5.AC1: Line 579 of `docs/onboarding/ironclaude-onboarding.html` reads `Built from HOW-WE-WORK.md at commit <hash>.`, where `<hash>` is 8 hexadecimal characters equal to the output of `git rev-parse --short=8 HEAD` run at the time of the edit, and it differs from `f3c1ef06`.
T5.AC2: No other line of the page changes in this task.
T5.AC3: `uv run pytest tests/docs/test_onboarding_deck.py -q` passes, including `test_deck_keeps_its_build_commit_footer`.
Global constraints: ## Constraints

- Scope is five deliverables: the new guide section and the removal-timing pointer in `src/superclaude/core/HOW-WE-WORK.md`, the byte-identical mirror `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, the worktree card and build footer of `docs/onboarding/ironclaude-onboarding.html`, and the new `tests/core/test_how_we_work_worktree_policy.py`. No production code changes.
- Out of scope: the claim launcher and its `issue-<N>` naming, the cleanup script and its rules, the issue watcher, the `CLAUDE.md` examples at lines 318-341, the issue 290 card, the slide introduction at lines 516-518, and any tool that extracts lessons. Section 1 of `./source.md` lists them.
- The open owner questions of section 7 of `./source.md` (dropping the words from a name, lessons of issue-less worktrees, whether the watcher or the claim should refuse an issue that already has a worktree, the slide introduction, the `CLAUDE.md` examples, the footer rule) are not decided by this plan and are not written into the guide. They belong in the pull request body.
- The guide is a shared file: the level-table, routing-table and other-commands marker comments and every other section stay as they are, and every line the change adds is ASCII (plain hyphens, no en dashes).
- The mirror is never edited by hand: it is a copy of the guide after the guide's last edit.
- Python and tests run through uv (`uv run pytest`, `uv run ruff`); never `python -m` or bare `pip`.
- The tasks run in a straight line and the new test file comes last (the design's section 6 puts it first) so that the acceptance criteria of every task can pass the moment that task is done.
- Stage the changed files and `.dev/tasks`; never stage anything under `.claude/` or `.dev/issues/`. Staging is not committing.
- Where this plan and `./source.md` disagree this plan wins: it overrides source.md line 106 (page-wide absence of "is being worked out in") and lines 53 and 108 (the list of 13 key phrases, now 15), as stated in Tasks 1, 4 and 7 (D-1, D-3).
Start sha: f44b056a9e7996eeff8c498c492644c004e30332
Diff against the start snapshot: --- a/docs/onboarding/ironclaude-onboarding.html
+++ b/docs/onboarding/ironclaude-onboarding.html
@@ -576,7 +576,7 @@
 </main>
 
 <footer>
-  <p>Built from HOW-WE-WORK.md at commit f3c1ef06.</p>
+  <p>Built from HOW-WE-WORK.md at commit 86238485.</p>
   <p>Source of truth for every command and flag: <a href="https://github.com/IronbellyOrg/IronClaude/blob/master/src/superclaude/core/HOW-WE-WORK.md">HOW-WE-WORK.md</a>, except <code>--plugin</code>, which comes from the <a href="https://github.com/IronbellyOrg/IronClaude/blob/master/src/superclaude/commands/recommend.md"><code>/sc:recommend</code> command file</a>.</p>
 </footer>
 


Codegraph context
index_state: fresh
checked_at: 2026-11-26T14:52:15Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-289
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-289
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents (floor: Grep for the file names; Markdown and HTML are not in the index) of the changed guide: tests/core/test_how_we_work_routing_table.py, tests/core/test_claude_md_routing_block.py, tests/commands/test_worktrees_command.py, tests/cli/test_how_we_work_install.py, tests/commands/test_help_command.py (all five run and pass: 95 passed), and later tasks of this plan (mirror, onboarding page, policy tests). Context only.

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