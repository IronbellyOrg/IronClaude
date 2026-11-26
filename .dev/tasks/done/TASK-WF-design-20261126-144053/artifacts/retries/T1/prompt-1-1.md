4fa93ed8e4f9ed9d3768df1288c452f47a13bab0
Review one task for spec compliance.

Task brief: ## Task 1: Add the "Worktrees and branches" section to the guide

In `src/superclaude/core/HOW-WE-WORK.md`, insert a new unnumbered heading `## Worktrees and branches` and its bullets between the closing routing-table marker comment (line 350) and the `## Orca coordination` heading (line 352), with one blank line before the heading and one blank line after the section. The content is the fenced text block of section 3 of `./source.md` (between the `guide-section:begin` and `guide-section:end` comments). Use it with exactly these four edits (D-3): (1) in the first paragraph change "a second checkout in its own folder, on its own branch" to "a second checkout on its own branch"; (2) in the fix bullet change "Then `git fetch origin`," to "`git fetch origin`,"; (3) in the lessons bullet change "pins the worktree in the Orca app when the PR opens" to "pins the worktree when the PR opens"; (4) in the claim bullet change "is exempt." to "is exempt, and so is a handoff of unfinished work after the first session has stopped."; the result is 394 words by `len(text.split())`; recount after editing, and if the count is above 400 tighten other wording without dropping a rule and without removing the example `clayphi/issue-289-wtrule` (the only backticked branch example; Task 7's test needs one). The section is bullets and short paragraphs only (no table), holds no HTML comment or marker, and does not contain the three phrases that `tests/commands/test_worktrees_command.py:124-137` bans: "Every verb is a dry run", "every verb is a dry run" and "Verbs (a dry run unless --apply is given)".

Dependents that read this file and must keep passing: `tests/core/test_how_we_work_routing_table.py` (each marker once and in order, numbered-heading reference check at `_HEADING_RE`, ASCII guard at lines 329-334), `tests/core/test_claude_md_routing_block.py` (the level table copy in `src/superclaude/core/CLAUDE.md` equals the guide's), `tests/commands/test_worktrees_command.py` (banned phrases), `tests/cli/test_how_we_work_install.py` (the installed copy equals the guide bytes), and `tests/commands/test_help_command.py`.

Acceptance criteria:
T1.AC1: `src/superclaude/core/HOW-WE-WORK.md` has exactly one line `## Worktrees and branches`, located after the closing routing-table marker comment line and before the `## Orca coordination` line, with no marker or HTML comment inside the section.
T1.AC2: The section, from its heading to the line before `## Orca coordination`, is at most 400 words by `len(text.split())` and is ASCII only (`text.isascii()` is true).
T1.AC3: The section contains each of these exact substrings: `new worktree and branch`, `One writer per worktree`, `original worktree while it still exists`, `--ff-only`, `stop and ask`, `/sc:issue --claim`, `at most 24 characters`, `no spaces`, `no run of 2 to 4 digits`, `create nothing and ask the owner`, `Lessons comment`, `pins the worktree`, `checks that comment first`, `is exempt`, `handoff of unfinished work` (D-3); each of the fifteen substrings occurs once in the section.
T1.AC4: `uv run pytest tests/core/test_how_we_work_routing_table.py tests/core/test_claude_md_routing_block.py tests/commands/test_worktrees_command.py tests/cli/test_how_we_work_install.py tests/commands/test_help_command.py -q` passes.
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
Start sha: 4fa93ed8e4f9ed9d3768df1288c452f47a13bab0
Diff against the start snapshot: --- a/src/superclaude/core/HOW-WE-WORK.md
+++ b/src/superclaude/core/HOW-WE-WORK.md
@@ -349,6 +349,16 @@
 
 <!-- /routing-table -->
 
+## Worktrees and branches
+
+A worktree is a second checkout on its own branch. Orca creates every worktree, with an agent, at its default location (never raw `git worktree add`). The creator owns the agent; no session creates a worktree for itself.
+
+- **New work gets a new worktree and branch.** One writer per worktree; a second writer gets its own. Supervised workers follow `~/.claude/WORKER-CONTRACT.md`.
+- **A fix to delivered work reuses the original worktree while it still exists, after these checks:** same repository, issue and branch; the issue is open (a closed one needs a bug issue `#<M>` named in the fix PR); no other live agent (`orca terminal list`); no uncommitted changes; the PR that counts (`gh pr list --repo <owner>/<repo> --head <branch> --state all`: newest merged, else newest) is merged and none is open. `git fetch origin`, `git merge --ff-only origin/<base>`, check that HEAD moved, and run `orca agent launch`. Any other state (PR closed unmerged, no PR, several worktrees, a worktree missing from `orca worktree list`, anything unknown): stop and ask. A removed worktree means a new one.
+- **Check before `/sc:issue --claim` or a Project Status change.** A claim reuses the worktree it finds and starts its agent at once; the watcher claims by itself. A re-run of the claim's own earlier run (no `launch` entry in its `worktree.json`) is exempt, and so is a handoff of unfinished work after the first session has stopped.
+- **Names:** `<login>/issue-<N>[-<words>]`, at most 24 characters, no spaces; `<login>` is `gh api user --jq .login`. Create with `--name issue-<N>-<words>`; Orca adds the login (use `--branch` if it does not). Words are lowercase letters and digits with no run of 2 to 4 digits (cleanup reads it as an issue). Example: `clayphi/issue-289-wtrule` (24). Drop the words when they do not fit; if even `<login>/issue-<N>` is over 24, create nothing and ask the owner. After creation the agent checks `git branch --show-current` and may run `git branch -m` before any push; never switch branches in a worktree.
+- **Lessons before removal.** The owner pins the worktree when the PR opens. After the merge the owner posts a Lessons comment on the issue (what happened, evidence by PR or commit, action) or "no reusable lesson", runs `/sc:closeout`, then unpins. A person runs `/sc:worktrees archive`, `retire` and `--apply`, and checks that comment first, because cleanup reads none.
+
 ## Orca coordination
 
 Orca can run IronClaude commands as workers. The rules live in `~/.claude/WORKER-CONTRACT.md`; this section only says how the pieces fit.


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