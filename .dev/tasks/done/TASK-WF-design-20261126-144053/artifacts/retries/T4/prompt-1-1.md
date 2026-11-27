58ffc5bfb760d648654e61f8ba890f19b306f78f
Review one task for spec compliance.

Task brief: ## Task 4: Replace the worktree card on slide 12

Depends on: Task 3

In `docs/onboarding/ironclaude-onboarding.html`, replace lines 520-524, the `<div class="card">` whose heading is "Worktree and branch protocol" and whose paragraph says the topic "is being worked out in issue #289", with the HTML block of section 4 (K5) of `./source.md`. The new card keeps the heading, keeps the glossary line (`<div class="term">`) and has no `<code>` element that holds a command or flag (its two `<code>` elements hold the name pattern and the example name). Lines 515-519 (the slide opening, eyebrow, "Being worked out" heading, introduction and the grid opening) and lines 525-530 (the issue 290 card and the closing tags) stay byte-identical.

Dependents: `tests/docs/test_onboarding_deck.py`, whose test `test_every_deck_command_and_flag_is_in_the_guide` reads every `<code>` element of the page and requires each command and flag in it to be in the guide.

Acceptance criteria:
T4.AC1: The page holds the example `clayphi/issue-289-wtrule` and the card heading "Worktree and branch protocol"; the sentence "how they are named is being worked out" is gone; the phrase "is being worked out in" occurs exactly once on the page, in the issue 290 card (`issues/290` is still in that sentence and `issues/289` is gone) (D-1).
T4.AC2: `git diff -U0 HEAD -- docs/onboarding/ironclaude-onboarding.html`, run after this task and before Task 5 (after Task 5 the file has a second hunk, the footer) (D-1), shows one changed hunk, inside the former lines 520-524; the issue 290 card (heading "Contributing rules") and lines 516-518 are untouched.
T4.AC3: `uv run pytest tests/docs/test_onboarding_deck.py -q` passes.
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
Start sha: 58ffc5bfb760d648654e61f8ba890f19b306f78f
Diff against the start snapshot: --- a/docs/onboarding/ironclaude-onboarding.html
+++ b/docs/onboarding/ironclaude-onboarding.html
@@ -520,7 +520,7 @@
     <div class="card">
       <h3>Worktree and branch protocol</h3>
       <div class="term"><b>Worktree:</b> a second checkout of the same repository in its own folder, on its own branch, so parallel sessions do not touch each other's files.</div>
-      <p>When a session should get its own worktree and branch, where they live and how they are named is being worked out in <a href="https://github.com/IronbellyOrg/IronClaude/issues/289">issue #289</a>.</p>
+      <p>New work gets a new worktree and branch, made by Orca with an agent. A fix to delivered work reuses the original worktree while it exists, after the checks in the guide. Name: <code>&lt;login&gt;/issue-&lt;N&gt;-&lt;words&gt;</code>, at most 24 characters, no spaces, for example <code>clayphi/issue-289-wtrule</code>. Before removal the owner writes the lessons on the issue, and a person pins the worktree until then. Details: HOW-WE-WORK, "Worktrees and branches".</p>
     </div>
     <div class="card">
       <h3>Contributing rules</h3>


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