6dc7d77c5f6ee66e6b7b3d6e5eeebf1c5d0b1010
Review one task for spec compliance.

Task brief: ## Task 8: Amend the two design records for the new default
In `docs/designs/sc-issue-claim-pipeline-flag.md` add a dated amendment note, "Amended 2026-11-18", under decision P2 and next to the levels table row at line 21: the default is `full` when a person types the command, and the issue watcher always passes `--pipeline none`. In `docs/designs/sc-issue-command.md` add the same dated note under the existing "Amended 2026-11-07" note (line 64) and in the sentence at line 494 change "with the default `--pipeline worktree`" to "with `--pipeline worktree`". In `docs/designs/sc-issue-claim-pipeline-flag.md` (not the command design record) also add amendment notes beside lines 66 ("An unflagged claim is `--pipeline worktree`."), 78 (the options row) and 87 ("worktree level") saying the default is now `full` for a person, and beside line 274 (the `--submit` condition) saying a `--submit` with no `--pipeline` also stops; leave line 85 (the `--submit` stop rule) as it is, because it still holds. Lines 21, 43, 66, 78 and 274 are table rows: append each note inside the row's last cell (as decision P4 at line 45 does with its "Amended" text) and never as a new line under the row, which would split the table; line 87 is prose. In `docs/designs/sc-issue-command.md` also amend the sentence at line 44 (B17, "`worktree` (default, ...)") the same way and add a "Superseded 2026-11-18" bullet to the Notes list (lines 245-249), after the existing "Superseded by #384" bullet at line 248, naming the Feature, simple row at line 238 (do not put a plain line directly under the table row, which would split the table). Keep the original decision text; only add amendments.
Acceptance criteria (ids):
T8.AC1: `grep -n "default .--pipeline worktree" docs/designs/sc-issue-command.md` prints nothing.
T8.AC2: Both design files contain "Amended 2026-11-18" with the new default and the watcher's explicit `none`.
T8.AC3: `docs/designs/sc-issue-claim-pipeline-flag.md` carries the note beside the lines that were 21, 43, 66, 78, 87 and 274 before the edit, the line that was 85 is unchanged, each note on a table row sits inside that row, and the tables still render as tables (no line without a leading `|` between two rows of one table).
T8.AC4: `docs/designs/sc-issue-command.md` carries the note at the lines that were 44 and 64 and a "Superseded 2026-11-18" bullet in its Notes list.
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
Start sha: 6dc7d77c5f6ee66e6b7b3d6e5eeebf1c5d0b1010
Diff against the start snapshot: diff --git a/docs/designs/sc-issue-claim-pipeline-flag.md b/docs/designs/sc-issue-claim-pipeline-flag.md
index 194fb3579..ced345ece 100644
--- a/docs/designs/sc-issue-claim-pipeline-flag.md
+++ b/docs/designs/sc-issue-claim-pipeline-flag.md
@@ -18,7 +18,7 @@ Today `/sc:issue --claim` assigns the issue, checks its accuracy, writes `next-s
 
 | Level | Flag | What happens after the claim's Waves 0-6 | Agent stops at |
 |---|---|---|---|
-| `worktree` (default) | `--pipeline worktree` or nothing | An Orca worktree `issue-<N>` is created (or reused) and a Claude Code agent is launched in it. It runs `next-steps.md` up to the plan boundary. | An approved plan: it prints the plan path and "Waiting for approval" until a human approves |
+| `worktree` (default) | `--pipeline worktree` or nothing | An Orca worktree `issue-<N>` is created (or reused) and a Claude Code agent is launched in it. It runs `next-steps.md` up to the plan boundary. | An approved plan: it prints the plan path and "Waiting for approval" until a human approves. Amended 2026-11-18: `worktree` is no longer the default; a person who types the command with no `--pipeline` gets `full`, and the issue watcher always passes `--pipeline none` |
 | `full` | `--pipeline full` | Same, but the agent runs every step including `/sc:implement` or `/task`. | Finished implementation, unstaged, uncommitted, unpushed |
 | `full` + `--submit` | `--pipeline full --submit` | Same, then the agent commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`. | A pushed branch with an open PR on the fork |
 | `none` | `--pipeline none` | The claim ends after the comments (amended 2026-11-08): no worktree is created, no agent is launched. | The claim itself runs nothing. Without a coordinator, the user runs `next-steps.md` from the main checkout's `.dev/issues/<N>/`. With a coordinator that owns the issue (amended 2026-11-17), the coordinator creates the worktree with `orca_worktree.py worktree` and starts a worker in it with `worker-start`; see the "Coordinator handoff for `--pipeline none`" paragraph of `src/superclaude/commands/issue.md` |
@@ -40,7 +40,7 @@ No level merges anything. Humans only review and merge; nobody opens a PR by han
 | # | Decision | Source |
 |---|---|---|
 | P1 | Orca is a dependency. No code, warning, option or document text exists only for a project without Orca. | Owner, AD 1.2 |
-| P2 | One flag, `--pipeline worktree\|full\|none`, default `worktree`. The `--worktree` flag of MR does not exist. | Owner, AD 1.6 |
+| P2 | One flag, `--pipeline worktree\|full\|none`, default `worktree`. The `--worktree` flag of MR does not exist. Amended 2026-11-18: the default is `full` when a person types the command, and the issue watcher always passes `--pipeline none`. | Owner, AD 1.6; owner, 2026-11-18 |
 | P3 | `--submit` is a second flag, valid with `--pipeline full` only. It turns on commit, push of a feature branch and `/sc:pr-submit --monitor 3`. It never merges. | Owner, AD 1.4 |
 | P4 | The default stop is an approved plan. `full` adds implementation. `none` launches no agent. Amended 2026-11-08: `none` also creates no worktree, because every worktree gets an agent. | Owner, AD 1.3; owner, 2026-11-08 |
 | P5 | The launched agent is Claude Code behind the ccsession shim, always. | Owner, AD 1.5 |
@@ -63,7 +63,7 @@ No level merges anything. Humans only review and merge; nobody opens a PR by han
 | Create JSON shape | MR R2 UNVERIFIED | AD observed `result.worktree.{id, path, branch, ...}`. FR-20 (path from a row-id difference) stays; the field is not relied on. | The set difference works with an opaque create result. |
 | `worktree_warning` holds one code | MR open item | The code that set the status wins; any other goes in `detail`. Launch codes use their own field `launch_warning`. | Two independent steps can each warn. |
 | Statuses | MR: `created \| reused \| skipped \| failed` | `created \| reused \| failed` | AD 4.2 and 4.4: `skipped` existed only for a missing `orca`. |
-| Unflagged claim | MR FR-3: byte-identical to today | Dropped. An unflagged claim is `--pipeline worktree`. | AD 4.3. |
+| Unflagged claim | MR FR-3: byte-identical to today | Dropped. An unflagged claim is `--pipeline worktree`. Amended 2026-11-18: an unflagged claim typed by a person is now `--pipeline full`; the issue watcher always passes `--pipeline none`. | AD 4.3. |
 | `--worktree` with `--create` | MR FR-2 | `--pipeline` or `--submit` with `--create`: STOP `E-CLAIM-ONLY-FLAG`. | AD section 2. |
 
 ## 4. Command interface
@@ -75,7 +75,7 @@ No level merges anything. Humans only review and merge; nobody opens a PR by han
 
 | Flag | Mode | Default | Values | Meaning |
 |---|---|---|---|---|
-| `--pipeline` | claim | `worktree` | `worktree`, `full`, `none` | How far the launched agent goes (section 1). `worktree` and `full` create the worktree and launch an agent; `none` creates no worktree and launches no agent |
+| `--pipeline` | claim | `worktree` | `worktree`, `full`, `none` | How far the launched agent goes (section 1). `worktree` and `full` create the worktree and launch an agent; `none` creates no worktree and launches no agent. Amended 2026-11-18: the default is now `full` for a person; the issue watcher always passes `--pipeline none` |
 | `--submit` | claim | off | no value | With `--pipeline full` only: after implementation the agent commits, pushes the feature branch to `origin` and runs `/sc:pr-submit --monitor 3`. Never merges |
 
 STOP rules added to the command file, checked in this order after the existing ones (before Activation, no external call):
@@ -84,7 +84,7 @@ STOP rules added to the command file, checked in this order after the existing o
 2. A `--pipeline` value that is not one of the three: STOP, list `worktree`, `full`, `none`. `--pipeline` with no value: the same STOP.
 3. `--submit` with a value, or with `--pipeline worktree` or `--pipeline none` or no `--pipeline`: STOP `E-SUBMIT-NEEDS-FULL` ("--submit needs --pipeline full").
 
-Examples: `/sc:issue --claim 302` (worktree level), `/sc:issue --claim 302 --pipeline none`, `/sc:issue --claim 302 --pipeline full`, `/sc:issue --claim 302 --pipeline full --submit`.
+Examples: `/sc:issue --claim 302` (worktree level; amended 2026-11-18: now the `full` level when a person types it, and the issue watcher always passes `--pipeline none`), `/sc:issue --claim 302 --pipeline none`, `/sc:issue --claim 302 --pipeline full`, `/sc:issue --claim 302 --pipeline full --submit`.
 
 `commands/issue.md` gets `version: "1.1.0"` (8 of 47 commands carry one; the claim behaviour changes for every user). `argument-hint`, Usage, Options table, Examples, Outputs, Boundaries and the claim paragraph are updated. Boundaries, Will Not: replace "Run any next-step command" with "Run `/sc:implement`, `/task`, a commit, a push or `/sc:pr-submit` itself (the launched agent may, at the level the user chose)", and add "Pass an Orca link flag" and "Merge anything". `SKILL.md` Will / Will Not mirror this.
 
@@ -271,7 +271,7 @@ New STOPs:
 |---|---|
 | `E-ORCA-REQUIRED` | Wave 0: `orca_worktree.py preflight` returns `ok: false` |
 | `E-CLAIM-ONLY-FLAG` | `--pipeline` or `--submit` with `--create` |
-| `E-SUBMIT-NEEDS-FULL` | `--submit` without `--pipeline full` |
+| `E-SUBMIT-NEEDS-FULL` | `--submit` without `--pipeline full`. Amended 2026-11-18: a `--submit` with no `--pipeline` also stops, because the default is now `full` but `--submit` still needs `--pipeline full` written out |
 
 Warnings (the claim `status` stays `success` for all of them). `W-ORCA-MISSING` and the `skipped` status of MR no longer exist.
 
diff --git a/docs/designs/sc-issue-command.md b/docs/designs/sc-issue-command.md
index 6a45d5395..492c10dc3 100644
--- a/docs/designs/sc-issue-command.md
+++ b/docs/designs/sc-issue-command.md
@@ -41,7 +41,7 @@ Every row is binding. "Owner" is the issue author's comments of 2026-10-30; "Com
 | B14 | Brainstorm and implement work after a claim runs on T1 or T2 by complexity. | Owner, 2026-10-30 14:15 |
 | B15 | Order of work for this feature: `/sc:design`, then `/sc:workflow`, then `/sc:implement` (the issue body's "before invoking Brainstorm" is superseded). | Coordinator brief carrying the owner instruction |
 | B16 | After `next-steps.md` is written and both comments are posted, the claim creates (or reuses) an Orca worktree `issue-<N>` and copies `.dev/issues/<N>/` into it. Orca is required (`E-ORCA-REQUIRED`); every later failure is a warning and the claim stays a success. | Owner, 2026-11-05; `docs/designs/sc-issue-claim-pipeline-flag.md` |
-| B17 | Launch levels through `--pipeline`: `worktree` (default, plans and waits for approval), `full` (also implements, no commit or push), `none` (no worktree and no agent; amended 2026-11-08, it was "worktree only, no agent" before every worktree needed an agent; amended 2026-11-17, the claim still makes no worktree and no agent, and a coordinator that owns the issue may then create the worktree and start a worker, see "Coordinator handoff for `--pipeline none`" in `src/superclaude/commands/issue.md`). For `worktree` and `full` the agent starts behind the ccsession shim through `orca agent launch --surface terminal`. | Owner, 2026-11-05; `docs/designs/sc-issue-claim-pipeline-flag.md` |
+| B17 | Launch levels through `--pipeline`: `worktree` (default, plans and waits for approval), `full` (also implements, no commit or push), `none` (no worktree and no agent; amended 2026-11-08, it was "worktree only, no agent" before every worktree needed an agent; amended 2026-11-17, the claim still makes no worktree and no agent, and a coordinator that owns the issue may then create the worktree and start a worker, see "Coordinator handoff for `--pipeline none`" in `src/superclaude/commands/issue.md`). For `worktree` and `full` the agent starts behind the ccsession shim through `orca agent launch --surface terminal`. Amended 2026-11-18: the default is now `full` for a person who types the command, and the issue watcher always passes `--pipeline none`. | Owner, 2026-11-05; `docs/designs/sc-issue-claim-pipeline-flag.md` |
 | B18 | `--submit` (with `--pipeline full` only) turns on the commit, the push of a feature branch and `/sc:pr-submit --monitor 3`. Nothing merges at any level; humans only review and merge. | Owner, 2026-11-05; `docs/designs/sc-issue-claim-pipeline-flag.md` |
 
 ## 3. Corrections to the issue text
@@ -63,6 +63,8 @@ Every row is binding. "Owner" is the issue author's comments of 2026-10-30; "Com
 
 > **Amended 2026-11-07:** `--claim` also takes `--pipeline worktree|full|none` (default `worktree`) and `--submit`; their STOP rules (`E-CLAIM-ONLY-FLAG`, `E-SUBMIT-NEEDS-FULL`) follow the existing ones. See `docs/designs/sc-issue-claim-pipeline-flag.md` section 4.
 
+> **Amended 2026-11-18:** the `--pipeline` default is `full` when a person types the command (not `worktree`); the issue watcher always passes `--pipeline none`. A `--submit` with no `--pipeline` still stops with `E-SUBMIT-NEEDS-FULL`.
+
 ```text
 /sc:issue --claim <number|url>
 /sc:issue --create "<description>" [--depth quick|standard|deep] [--mode feature|bug] [--type <type>]
@@ -246,6 +248,7 @@ Notes:
 - `--depth quick` with `--fix` is a STOP in `/sc:troubleshoot`, so the simple bug row has no `--fix` and hands the report to `/sc:implement` (issue body: "Hand the output directly off ... /sc:implement").
 - `/sc:troubleshoot --depth deep` STOPs on a description under 10 words without `--scope`; the rows always pass `--scope`.
 - `/sc:brainstorm --models` defaults to `opus,sonnet,haiku`, rotated across proposals, and takes aliases only. Every brainstorm row passes `--models opus,sonnet` so no proposal runs on the `haiku` alias, which on this workspace resolves to `glm-5.3` (section 6), below T2 (B14). Aliases cannot name a picker ID, so this is the closest the chain can get to B14 inside a brainstorm; the session tier itself is pinned by the `/model` line (default D25). Superseded by #384: the chains use the default models; see `docs/reference/model-aliases.md`.
+- Superseded 2026-11-18: the Feature, simple row no longer starts with `/sc:brainstorm`; it is `/sc:workflow <S> --depth quick --handoff none`, then `/sc:implement <plan path printed by step 1>`, because the issue summary already states the requirements.
 - `/sc:design --type` is chosen per issue by `/sc:recommend` from the four values the command accepts.
 
 ## 10. Output files and templates
@@ -491,7 +494,7 @@ Checked on 2026-11-04 against the installed files `~/.claude/commands/sc/<name>.
 
 > **Amended 2026-11-07:** criterion 1 below now ends with the worktree and the launched agent instead of "stops"; the new criteria are in `docs/designs/sc-issue-claim-pipeline-flag.md` section 17.
 
-1. `/sc:issue --claim <N>` on an open, unassigned issue of the origin repo: the T3 worker runs first; the issue is assigned to the current user; `.dev/issues/<N>/` holds `scout.md`, `clickup.json`, `accuracy-check.md`, `issue-summary.md` (with an hours estimate), `recommend.md`, `next-steps.md`, `claim-comment.md`; two marked comments are posted; the skill itself runs no next-step command (with the default `--pipeline worktree` the launched agent plans and waits for approval).
+1. `/sc:issue --claim <N>` on an open, unassigned issue of the origin repo: the T3 worker runs first; the issue is assigned to the current user; `.dev/issues/<N>/` holds `scout.md`, `clickup.json`, `accuracy-check.md`, `issue-summary.md` (with an hours estimate), `recommend.md`, `next-steps.md`, `claim-comment.md`; two marked comments are posted; the skill itself runs no next-step command (with `--pipeline worktree` the launched agent plans and waits for approval).
 2. Running the same claim again edits both comments; the comment count on the issue does not grow.
 3. A closed issue, or one assigned to someone else, stops with the stated message and makes no GitHub or ClickUp write.
 4. A claim URL for any repo other than origin stops with `E-FOREIGN-REPO`; no `gh` call is made without `--repo <origin repo>`.


Codegraph context
index_state: fresh
checked_at: 2026-11-18T05:09:43Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline
projectPath: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor: the task changes Markdown or test text, not code symbols; no dependents outside the touched set were listed.

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): F1.1 ac=T8.AC4 at=docs/designs/sc-issue-command.md:44 anchor="Keep the original decision text; only add amendments." chk=amiss:n,false:n,harm:n,constraint:y family=amend-vs-rewrite fix=restore "worktree (default, plans and waits for approval)" and append "Amended 2026-11-18: ..." in the same cell [covers="Keep the original decision text; only add amendments"]: the B17 cell's original "(default, ...)" wording was edited rather than preserved with an appended note. The new default is stated correctly, so this is low impact.
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
