e0e0b260f165153b193e63510f7a55cdbc5a7396
Review one task for spec compliance.

Task brief: ## Task 3: Make full the default level in the command file
In `src/superclaude/commands/issue.md` make these narrow edits. In the paragraph that lists the levels (line 16), move "(the default)" from `worktree` to `full`. In the Options table, set the `--pipeline` row default to `` `full` `` and add "Omitted means `full`." to its meaning; leave its values cell as `worktree`, `full`, `none`. Under the table add one sentence: a person who types `--claim` with no `--pipeline` gets `full`, and the issue watcher never relies on the default because it always passes `--pipeline none`; `--submit` still needs an explicit `--pipeline full`, even though `full` is the default. In the STOP rules keep the `E-SUBMIT-NEEDS-FULL` rule and its quoted message `"--submit needs --pipeline full"` and change its condition to "`--submit` with a value, without `--pipeline full`, or with no `--pipeline`" (the wording of `docs/designs/sc-issue-claim-pipeline-flag.md` line 85), so that the stated default cannot satisfy it. In the `--submit` row keep the words `--pipeline full` and add "an explicit `--pipeline full` is still required". Add the example line `/sc:issue --claim 302 --pipeline worktree` to the Examples block.
Acceptance criteria (ids):
T3.AC1: The Options table `--pipeline` row default cell is exactly `` `full` `` and its values cell still lists `worktree`, `full`, `none` in that order.
T3.AC2: `/sc:issue --claim 302 --pipeline worktree` is a line of the Examples block, and the existing examples for `none`, `full` and `full --submit` are still present.
T3.AC3: The STOP rule order is unchanged (create-only, claim-only, bad value, submit) and the text `src/superclaude/` does not appear in the file.
T3.AC4: The `E-SUBMIT-NEEDS-FULL` rule still carries the quoted message and now also names the case of no `--pipeline`; the `--submit` row still contains `--pipeline full`.
Global constraints: ## Constraints
- Edit only source files: `src/superclaude/...`, `tests/...`, `docs/...` and the one mirror file `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. Never edit or stage anything under `.claude/`; Task 10 regenerates those copies with `make sync-dev`.
- The default level applies to a bare `--claim`. The issue watcher always passes `--pipeline none` (`build_claim_prompt` in `src/superclaude/cli/issue_watch/launch.py`, pinned by `tests/issue_watch/test_launch.py`). Do not edit either file and do not add any human-versus-agent detection.
- The default level does not authorize a commit, a push or a pull request: `E-SUBMIT-NEEDS-FULL` keeps its meaning, so a `--submit` with no `--pipeline` still stops and `--submit` needs an explicit `--pipeline full` (the design record `docs/designs/sc-issue-claim-pipeline-flag.md` line 85 already says so).
- No file under `src/superclaude/skills/sc-issue-protocol/` and not `src/superclaude/commands/issue.md` may contain the text `src/superclaude/` (`tests/skills/test_issue_protocol.py::test_no_source_tree_path_in_skill_files` and `tests/commands/test_issue_command.py::test_no_source_tree_path` forbid it): in those files cite code by file name, never by its `src/superclaude/` path.
- New lines in command and skill files must not contain `git add`, `git commit`, `git push`, `git merge`, `gh pr` or `gh api`: `tests/skills/test_worker_contract.py` audits those verbs line by line.
- Leave the ship-gate sentences (OB-H1, OB-H2, OB-H3) and the `--pipeline none` coordinator-handoff paragraph exactly as written. The worktree `claim-handoff-planb` edits the same files (`issue.md`, `SKILL.md`, `refs/claim.md`, `HOW-WE-WORK.md`), so keep every edit narrow and rebase onto `origin/master` before any pull request.
- Out of scope: `/tech-research`, `/task-builder` and `/task` handling, the complex bug row, model tiers, `orca_worktree.py`, every other chain row, and the command version (it stays 1.1.0, which `tests/commands/test_issue_command.py` pins).
- Also out of scope, recorded on purpose: `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt` lines 17-19 (the coordinator path keeps its brainstorm step for simple work); the owner-run bare launch prompts in `docs/designs/issue-watcher-setup.md` lines 616-619 (a launch with them now starts at `full`; update them before reuse if a claim-only capture is wanted); and the dated records `docs/designs/issue-watcher.md` lines 41 and 48 and `docs/designs/issue-watcher-setup.md` line 575.
- Known risk, not fixed here: a person's bare `/sc:issue --claim <N>` on an issue that a coordinator already owns reuses its worktree and starts a second agent, now at `full`, because only the claim's own launch step writes the launch record (`cmd_pending` in `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` writes only a pending record). Do not claim such an issue without `--pipeline none`.
Start sha: e0e0b260f165153b193e63510f7a55cdbc5a7396
Diff against the start snapshot: diff --git a/src/superclaude/commands/issue.md b/src/superclaude/commands/issue.md
index b2be54a23..d1c4efd5e 100644
--- a/src/superclaude/commands/issue.md
+++ b/src/superclaude/commands/issue.md
@@ -13,7 +13,7 @@ argument-hint: "--claim <number|url> [--pipeline worktree|full|none] [--submit]
 
 Two modes on the repository that `origin` points at:
 
-- `--claim` takes an existing issue: assigns it to you on GitHub and, when one exists, on its ClickUp task; checks whether the issue text is still accurate against today's code and the pull requests merged since it was opened; writes a summary and a next-step prompt under `.dev/issues/<N>/`; posts two marked comments; then, unless `--pipeline none`, creates (or reuses) the Orca worktree `issue-<N>` and launches one Claude Code agent in it at the `--pipeline` level. Orca must be running (STOP `E-ORCA-REQUIRED` otherwise, before anything is assigned or posted). The levels: `worktree` (the default) stops at a plan a human approves, `full` also implements without a commit or a push, `full` with `--submit` also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`, and `none` stops after the comments: it creates no worktree and launches no agent. Nothing ever merges. When the launch-level guard is missing or not effective the claim refuses the launch with `W-ENFORCEMENT-ABSENT` (no agent starts and no launch record is written); the claim installs the L2 pre-push hook in the clone's shared hooks directory, and when that hook is not in effect it warns with `W-L2-ABSENT` and the launch continues (the IR-7 refusal arrives switched off in the separate last #441 commit, `IR7_REFUSE = False`). No governed claim (`worktree` or `full`) is used on a real issue until OB-H1 item 1 (parent `session_id` in subagent payloads), OB-H2 and OB-H3 have passed. In `sc-issue-launch-level-hook.md`, section 7 (U1) requires item 1 before a `full` or `--submit` claim and OB-H1 item 5 (self-started turns wrapped) before a claim at any level; OB-H2 and OB-H3 come from its sections 11 and 14.
+- `--claim` takes an existing issue: assigns it to you on GitHub and, when one exists, on its ClickUp task; checks whether the issue text is still accurate against today's code and the pull requests merged since it was opened; writes a summary and a next-step prompt under `.dev/issues/<N>/`; posts two marked comments; then, unless `--pipeline none`, creates (or reuses) the Orca worktree `issue-<N>` and launches one Claude Code agent in it at the `--pipeline` level. Orca must be running (STOP `E-ORCA-REQUIRED` otherwise, before anything is assigned or posted). The levels: `worktree` stops at a plan a human approves, `full` (the default) also implements without a commit or a push, `full` with `--submit` also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`, and `none` stops after the comments: it creates no worktree and launches no agent. Nothing ever merges. When the launch-level guard is missing or not effective the claim refuses the launch with `W-ENFORCEMENT-ABSENT` (no agent starts and no launch record is written); the claim installs the L2 pre-push hook in the clone's shared hooks directory, and when that hook is not in effect it warns with `W-L2-ABSENT` and the launch continues (the IR-7 refusal arrives switched off in the separate last #441 commit, `IR7_REFUSE = False`). No governed claim (`worktree` or `full`) is used on a real issue until OB-H1 item 1 (parent `session_id` in subagent payloads), OB-H2 and OB-H3 have passed. In `sc-issue-launch-level-hook.md`, section 7 (U1) requires item 1 before a `full` or `--submit` claim and OB-H1 item 5 (self-started turns wrapped) before a claim at any level; OB-H2 and OB-H3 come from its sections 11 and 14.
 - `--create` turns a description into a GitHub issue built from one of four templates, with a GitHub issue type, the Complexity issue field and a mode label. GitHub only: no ClickUp task.
 
 Both modes post directly to GitHub; nothing is shown for approval first.
@@ -40,11 +40,13 @@ Explicit only: the user types `/sc:issue --claim ...` or `/sc:issue --create ...
 | `--depth` | create | `quick` | `quick`, `standard`, `deep` | How hard the command checks the flags and fills the body |
 | `--mode` | create | chosen by a worker when omitted | `feature`, `bug` | Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label |
 | `--type` | create | chosen by a worker when omitted | `cicd`, `command`, `skill`, `agent`, `hook`, `cli`, `core`, `docs`, `tests`, `install`, `other` | Area of the change; a feature in `tests` gets the issue type Test, otherwise the area is recorded in `flags.md`; no label is applied for it |
-| `--pipeline` | claim | `worktree` | `worktree`, `full`, `none` | How far the launched agent goes. `worktree` and `full` create the worktree and launch an agent; `none` creates no worktree and launches no agent |
-| `--submit` | claim | off | no value | Only with `--pipeline full`: the agent also commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`. Never merges |
+| `--pipeline` | claim | `full` | `worktree`, `full`, `none` | How far the launched agent goes. Omitted means `full`. `worktree` and `full` create the worktree and launch an agent; `none` creates no worktree and launches no agent |
+| `--submit` | claim | off | no value | Only with `--pipeline full` (an explicit `--pipeline full` is still required, even though `full` is the default): the agent also commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`. Never merges |
 
 There is no repository option (the repo is always `origin`), no dry-run option and no preview option.
 
+A person who types `--claim` with no `--pipeline` gets `full`. The issue watcher never relies on the default: it always passes `--pipeline none`. `--submit` still needs an explicit `--pipeline full`, even though `full` is the default.
+
 ## STOP rules (checked before Activation)
 
 - Exactly one of `--claim` / `--create` is required. Both or neither: STOP and print the Usage block.
@@ -54,13 +56,14 @@ There is no repository option (the repo is always `origin`), no dry-run option a
 - An empty `--claim` argument: STOP and print the Usage block.
 - `--pipeline` or `--submit` together with `--create`: STOP `E-CLAIM-ONLY-FLAG` ("--pipeline and --submit apply to --claim only").
 - A `--pipeline` value that is not `worktree`, `full` or `none`, or `--pipeline` with no value: STOP and list those three values.
-- `--submit` with a value, or without `--pipeline full`: STOP `E-SUBMIT-NEEDS-FULL` ("--submit needs --pipeline full").
+- `--submit` with a value, without `--pipeline full`, or with no `--pipeline`: STOP `E-SUBMIT-NEEDS-FULL` ("--submit needs --pipeline full").
 
 ## Examples
 
 ```text
 /sc:issue --claim 302
 /sc:issue --claim https://github.com/<owner>/<repo>/issues/302
+/sc:issue --claim 302 --pipeline worktree
 /sc:issue --claim 302 --pipeline none
 /sc:issue --claim 302 --pipeline full
 /sc:issue --claim 302 --pipeline full --submit


Codegraph context
index_state: fresh
checked_at: 2026-11-18T05:09:43Z
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
