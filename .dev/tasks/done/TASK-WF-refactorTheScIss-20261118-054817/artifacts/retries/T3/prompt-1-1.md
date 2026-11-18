904bc3cb55c3b4a7aadb46e9ae0aa665971827a8
Review one task for spec compliance.

Task brief: ## Task 3: Describe the picked default in the command file
Depends on: Task 1

In `src/superclaude/commands/issue.md`: at line 16 replace "`full` (the default)" so the levels list says `worktree` stops at a plan a human approves, `full` also implements without a commit or a push, and that without `--pipeline` the claim picks one of them from the issue; in the Options table row of `--pipeline` (line 43) replace the default cell `full` with "`full` or `worktree`, picked from the issue" and replace "Omitted means `full`." in the meaning cell with a pointer sentence: omitted means the level is picked from the issue (a bug or a simple or medium feature of 16 hours or less gets `full`; a complex feature, a feature over 16 hours or an issue that cannot be classified gets `worktree`; the rule is in the skill, `refs/claim.md`). Rewrite the paragraph under the table (line 48) to say that a person who types `--claim` with no `--pipeline` gets the picked level, that an explicit `--pipeline` always wins, that the issue watcher never relies on the default and always passes `--pipeline none`, and that `--submit` still needs an explicit `--pipeline full`. In line 44 (`--submit` row) drop the clause ", even though `full` is the default" and keep "an explicit `--pipeline full` is still required" (the paragraph rewritten at line 48 must not use that clause either). Keep the STOP rules at lines 52-59 with the quoted message "--submit needs --pipeline full" and the words "no `--pipeline`", and the examples at lines 64-69 as they are.
Acceptance criteria (ids):
T3.AC1: `src/superclaude/commands/issue.md` states the picked default in the intro, the `--pipeline` row and the paragraph under the table, names the 16-hour line only once (in the row), and points to the skill for the rule.
T3.AC2: The paragraph still contains "always passes `--pipeline none`", the examples still contain the exact line `/sc:issue --claim 302 --pipeline worktree`, and the STOP rule line for `E-SUBMIT-NEEDS-FULL` is unchanged.
T3.AC3: `uv run pytest tests/commands/test_issue_command.py -v` fails only in `test_option_defaults` (its pinned default cell is updated in Task 4), and `grep -n "src/superclaude/" src/superclaude/commands/issue.md` prints nothing, and `grep -n "even though .full. is the default" src/superclaude/commands/issue.md` prints nothing.
Global constraints: ## Constraints
- The rule is authored once, in `src/superclaude/skills/sc-issue-protocol/refs/claim.md` (Wave 5). `issue.md`, `SKILL.md`, the next-steps template, the docs and the routing guide state the outcome in one sentence, which may name the 16-hour line once per file, and do not restate the order of the rule's checks or its unreadable fallback as a second rule; the full rule lives only in `refs/claim.md`.
- The rule reads three lines of `<D>/issue-summary.md`, which Wave 4 already writes from `templates/issue-summary.md`: `Type`, `Complexity` and `Effort estimate`. A value that is missing or not one of the allowed words counts as unreadable and gives `worktree`.
- No new return-contract field. The claim return contract keeps its ten fields (a test pins them); `pipeline_level` carries the level actually used.
- An `already_launched` re-claim still reports the stored level from the `launch` entry of `worktree.json` or its mirror file; that path is not changed.
- `--submit` still stops with `E-SUBMIT-NEEDS-FULL` when `--pipeline full` is not written out, including when `--pipeline` is omitted. The rule text of that STOP and its quoted message "--submit needs --pipeline full" stay as they are.
- Do not edit `tests/issue_watch/`, `src/superclaude/cli/issue_watch/launch.py`, `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, the launch-level guard text, or the ship-gate and OB-H paragraphs. The issue watcher keeps passing an explicit `--pipeline none` and never reaches the rule.
- Text added to installed skill, command and core files names no `src/superclaude/` path and no git or gh verb that `tests/skills/test_worker_contract.py` audits in new lines.
- Design and user-guide records keep their original text: this change only adds dated "Amended 2026-11-18" notes, and a note on a table row goes inside that row's last cell so the table stays a table.
- The new text is prose that a model follows, so the tests pin its wording and order, not an executable rule. Each task says which words are pinned.
- Never `git add` or `git add -f` any path under `.claude/`; `make sync-dev` writes those copies and they stay unstaged. `claim-handoff-planb` edits some of the same files, so rebase onto `origin/master` before any PR.
Start sha: 904bc3cb55c3b4a7aadb46e9ae0aa665971827a8
Diff against the start snapshot: diff --git a/src/superclaude/commands/issue.md b/src/superclaude/commands/issue.md
index d1c4efd5e..7b07723cf 100644
--- a/src/superclaude/commands/issue.md
+++ b/src/superclaude/commands/issue.md
@@ -13,7 +13,7 @@ argument-hint: "--claim <number|url> [--pipeline worktree|full|none] [--submit]
 
 Two modes on the repository that `origin` points at:
 
-- `--claim` takes an existing issue: assigns it to you on GitHub and, when one exists, on its ClickUp task; checks whether the issue text is still accurate against today's code and the pull requests merged since it was opened; writes a summary and a next-step prompt under `.dev/issues/<N>/`; posts two marked comments; then, unless `--pipeline none`, creates (or reuses) the Orca worktree `issue-<N>` and launches one Claude Code agent in it at the `--pipeline` level. Orca must be running (STOP `E-ORCA-REQUIRED` otherwise, before anything is assigned or posted). The levels: `worktree` stops at a plan a human approves, `full` (the default) also implements without a commit or a push, `full` with `--submit` also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`, and `none` stops after the comments: it creates no worktree and launches no agent. Nothing ever merges. When the launch-level guard is missing or not effective the claim refuses the launch with `W-ENFORCEMENT-ABSENT` (no agent starts and no launch record is written); the claim installs the L2 pre-push hook in the clone's shared hooks directory, and when that hook is not in effect it warns with `W-L2-ABSENT` and the launch continues (the IR-7 refusal arrives switched off in the separate last #441 commit, `IR7_REFUSE = False`). No governed claim (`worktree` or `full`) is used on a real issue until OB-H1 item 1 (parent `session_id` in subagent payloads), OB-H2 and OB-H3 have passed. In `sc-issue-launch-level-hook.md`, section 7 (U1) requires item 1 before a `full` or `--submit` claim and OB-H1 item 5 (self-started turns wrapped) before a claim at any level; OB-H2 and OB-H3 come from its sections 11 and 14.
+- `--claim` takes an existing issue: assigns it to you on GitHub and, when one exists, on its ClickUp task; checks whether the issue text is still accurate against today's code and the pull requests merged since it was opened; writes a summary and a next-step prompt under `.dev/issues/<N>/`; posts two marked comments; then, unless `--pipeline none`, creates (or reuses) the Orca worktree `issue-<N>` and launches one Claude Code agent in it at the `--pipeline` level. Orca must be running (STOP `E-ORCA-REQUIRED` otherwise, before anything is assigned or posted). The levels: `worktree` stops at a plan a human approves, `full` also implements without a commit or a push, `full` with `--submit` also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`, and `none` stops after the comments: it creates no worktree and launches no agent. With no `--pipeline` the claim picks `worktree` or `full` from the issue (the rule is in the skill, `refs/claim.md`). Nothing ever merges. When the launch-level guard is missing or not effective the claim refuses the launch with `W-ENFORCEMENT-ABSENT` (no agent starts and no launch record is written); the claim installs the L2 pre-push hook in the clone's shared hooks directory, and when that hook is not in effect it warns with `W-L2-ABSENT` and the launch continues (the IR-7 refusal arrives switched off in the separate last #441 commit, `IR7_REFUSE = False`). No governed claim (`worktree` or `full`) is used on a real issue until OB-H1 item 1 (parent `session_id` in subagent payloads), OB-H2 and OB-H3 have passed. In `sc-issue-launch-level-hook.md`, section 7 (U1) requires item 1 before a `full` or `--submit` claim and OB-H1 item 5 (self-started turns wrapped) before a claim at any level; OB-H2 and OB-H3 come from its sections 11 and 14.
 - `--create` turns a description into a GitHub issue built from one of four templates, with a GitHub issue type, the Complexity issue field and a mode label. GitHub only: no ClickUp task.
 
 Both modes post directly to GitHub; nothing is shown for approval first.
@@ -40,12 +40,12 @@ Explicit only: the user types `/sc:issue --claim ...` or `/sc:issue --create ...
 | `--depth` | create | `quick` | `quick`, `standard`, `deep` | How hard the command checks the flags and fills the body |
 | `--mode` | create | chosen by a worker when omitted | `feature`, `bug` | Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label |
 | `--type` | create | chosen by a worker when omitted | `cicd`, `command`, `skill`, `agent`, `hook`, `cli`, `core`, `docs`, `tests`, `install`, `other` | Area of the change; a feature in `tests` gets the issue type Test, otherwise the area is recorded in `flags.md`; no label is applied for it |
-| `--pipeline` | claim | `full` | `worktree`, `full`, `none` | How far the launched agent goes. Omitted means `full`. `worktree` and `full` create the worktree and launch an agent; `none` creates no worktree and launches no agent |
-| `--submit` | claim | off | no value | Only with `--pipeline full` (an explicit `--pipeline full` is still required, even though `full` is the default): the agent also commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`. Never merges |
+| `--pipeline` | claim | `full` or `worktree`, picked from the issue | `worktree`, `full`, `none` | How far the launched agent goes. Omitted means the level is picked from the issue: a bug or a simple or medium feature of 16 hours or less gets `full`; a complex feature, a feature over 16 hours or an issue that cannot be classified gets `worktree` (the rule is in the skill, `refs/claim.md`). `worktree` and `full` create the worktree and launch an agent; `none` creates no worktree and launches no agent |
+| `--submit` | claim | off | no value | Only with `--pipeline full` (an explicit `--pipeline full` is still required): the agent also commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`. Never merges |
 
 There is no repository option (the repo is always `origin`), no dry-run option and no preview option.
 
-A person who types `--claim` with no `--pipeline` gets `full`. The issue watcher never relies on the default: it always passes `--pipeline none`. `--submit` still needs an explicit `--pipeline full`, even though `full` is the default.
+A person who types `--claim` with no `--pipeline` gets the picked level, and an explicit `--pipeline` always wins. The issue watcher never relies on the default: it always passes `--pipeline none`. `--submit` still needs an explicit `--pipeline full`.
 
 ## STOP rules (checked before Activation)
 


Codegraph context
index_state: fresh
checked_at: 2026-11-18T06:18:32Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline
projectPath: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor: the task changes Markdown or test text, not code symbols; no dependents outside the touched set were listed.

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
