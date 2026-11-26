d10b3a60b5e12a1dc9d0cfbdf84f74370f4b5c48
Review one task for spec compliance.

Task brief: ## Task 3: Describe the blocker stop in the /sc:issue command file

Depends on: Task 1

Edit `src/superclaude/commands/issue.md`, the `--claim` bullet under "Two modes on the repository that `origin` points at" (the long bullet that begins "`--claim` takes an existing issue"). After the sentence that ends "Orca must be running (STOP `E-ORCA-REQUIRED` otherwise, before anything is assigned or posted)." add one sentence: the claim first reads the issue's GitHub "blocked by" links and stops with `E-BLOCKED`, naming each open blocker, while any is open (before anything is assigned or posted); a list that cannot be read does not stop the claim, and its final output says the check could not run. Add no new flag and change nothing else in the file, including the "Coordinator handoff" paragraph and the `## Boundaries` lists.

Acceptance criteria (ids added by the orchestrator):
- T3.AC1: `src/superclaude/commands/issue.md` contains `E-BLOCKED` in the `--claim` bullet and still contains no text `src/superclaude/`.
- T3.AC2: The Options table and the STOP rules list of the file are unchanged, and `tests/commands/test_issue_command.py` and `tests/skills/test_issue_protocol.py::test_st11_no_source_tree_path_in_the_command_file` pass.
Global constraints: ## Constraints

- Change only what the source asks: the blocker read and `E-BLOCKED` stop in the claim, their description in four places, and the tests. Not the issue watcher, not dependency links, and not any other claim behaviour.
- Edit only the canonical files under `src/superclaude/`, the plugin guide copy and the tests. Do not edit or stage anything under `.claude/`; the generated copies come from `make sync-dev`.
- Inside the skill files and the command file under `src/superclaude/skills/sc-issue-protocol/` and `src/superclaude/commands/issue.md`, never write the text `src/superclaude/` (two existing tests forbid it), never write `{owner}/{repo}`, and keep every `gh api` path spelled `repos/<R>/...`.
- Do not touch the paragraph that begins "Coordinator handoff for `--pipeline none`:"; it must stay identical in `refs/claim.md`, `SKILL.md` and `commands/issue.md`.
- Do not add fields to the claim return contract in `SKILL.md`; a test pins its exact keys. A failed read is reported as one line of the final output.
- `SKILL.md` must stay under 500 lines.
Start sha: d10b3a60b5e12a1dc9d0cfbdf84f74370f4b5c48
Diff against the start snapshot: 
diff --git a/src/superclaude/commands/issue.md b/src/superclaude/commands/issue.md
index 911c3db1c..9bd7fc88e 100644
--- a/src/superclaude/commands/issue.md
+++ b/src/superclaude/commands/issue.md
@@ -13,7 +13,7 @@ argument-hint: "--claim <number|url> [--pipeline worktree|full|none] [--submit]
 
 Two modes on the repository that `origin` points at:
 
-- `--claim` takes an existing issue: assigns it to you on GitHub and, when one exists, on its ClickUp task; checks whether the issue text is still accurate against today's code and the pull requests merged since it was opened; writes a summary and a next-step prompt under `.dev/issues/<N>/`; posts two marked comments; then, unless `--pipeline none`, creates (or reuses) the Orca worktree `issue-<N>` and launches one Claude Code agent in it at the `--pipeline` level. Orca must be running (STOP `E-ORCA-REQUIRED` otherwise, before anything is assigned or posted). The levels: `worktree` stops at a plan a human approves, `full` also implements without a commit or a push, `full` with `--submit` also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`, and `none` stops after the comments: it creates no worktree and launches no agent. With no `--pipeline` the claim picks `worktree` or `full` from the issue (the rule is in the skill, `refs/claim.md`). Nothing ever merges. When the launch-level guard is missing or not effective the claim refuses the launch with `W-ENFORCEMENT-ABSENT` (no agent starts and no launch record is written); the claim installs the L2 pre-push hook in the clone's shared hooks directory, and when that hook is not in effect it warns with `W-L2-ABSENT` and the launch continues (the IR-7 refusal arrives switched off in the separate last #441 commit, `IR7_REFUSE = False`). No governed claim (`worktree` or `full`) is used on a real issue until OB-H1 item 1 (parent `session_id` in subagent payloads), OB-H2 and OB-H3 have passed. In `sc-issue-launch-level-hook.md`, section 7 (U1) requires item 1 before a `full` or `--submit` claim and OB-H1 item 5 (self-started turns wrapped) before a claim at any level; OB-H2 and OB-H3 come from its sections 11 and 14.
+- `--claim` takes an existing issue: assigns it to you on GitHub and, when one exists, on its ClickUp task; checks whether the issue text is still accurate against today's code and the pull requests merged since it was opened; writes a summary and a next-step prompt under `.dev/issues/<N>/`; posts two marked comments; then, unless `--pipeline none`, creates (or reuses) the Orca worktree `issue-<N>` and launches one Claude Code agent in it at the `--pipeline` level. Orca must be running (STOP `E-ORCA-REQUIRED` otherwise, before anything is assigned or posted). The claim first reads the issue's GitHub "blocked by" links and stops with `E-BLOCKED`, naming each open blocker, while any is open (before anything is assigned or posted); a list that cannot be read does not stop the claim, and its final output says the check could not run. The levels: `worktree` stops at a plan a human approves, `full` also implements without a commit or a push, `full` with `--submit` also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`, and `none` stops after the comments: it creates no worktree and launches no agent. With no `--pipeline` the claim picks `worktree` or `full` from the issue (the rule is in the skill, `refs/claim.md`). Nothing ever merges. When the launch-level guard is missing or not effective the claim refuses the launch with `W-ENFORCEMENT-ABSENT` (no agent starts and no launch record is written); the claim installs the L2 pre-push hook in the clone's shared hooks directory, and when that hook is not in effect it warns with `W-L2-ABSENT` and the launch continues (the IR-7 refusal arrives switched off in the separate last #441 commit, `IR7_REFUSE = False`). No governed claim (`worktree` or `full`) is used on a real issue until OB-H1 item 1 (parent `session_id` in subagent payloads), OB-H2 and OB-H3 have passed. In `sc-issue-launch-level-hook.md`, section 7 (U1) requires item 1 before a `full` or `--submit` claim and OB-H1 item 5 (self-started turns wrapped) before a claim at any level; OB-H2 and OB-H3 come from its sections 11 and 14.
 - `--create` turns a description into a GitHub issue built from one of four templates, with a GitHub issue type, the Complexity issue field and a mode label. GitHub only: no ClickUp task.
 
 Both modes post directly to GitHub; nothing is shown for approval first.

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
