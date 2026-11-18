8a6a6ca4ec6909298c4d02cdf76f7f133588444a
Review one task for spec compliance.

Task brief: ## Task 7: Add dated amendment notes to the two design records
Depends on: Task 1

In `docs/designs/sc-issue-claim-pipeline-flag.md` add a note "Amended 2026-11-18 (second)" saying the default is now picked from the issue (bug: `full`; simple or medium feature of 16 hours or less: `full`; complex feature, feature over 16 hours or unreadable: `worktree`; an explicit `--pipeline` wins; the issue watcher always passes `--pipeline none`), inside the last cell of the table rows at lines 21, 43, 45 (decision P4, "The default stop is an approved plan", which already carries an "Amended 2026-11-08" note), 66, 78 and 274 (each of the others already carries an "Amended 2026-11-18" note: append the new note after it, never edit the existing text), and at the prose sentence at line 87; leave line 85 as it is. In `docs/designs/sc-issue-command.md` add the same note inside the last cell of the B17 row (line 44) after its existing note, and as a new blockquote paragraph after the existing "Amended 2026-11-18" block at line 66. Keep every original word.
Acceptance criteria (ids):
T7.AC1: Both files carry the new note at the places above (including the decision P4 row at line 45 of the flag record); `git diff docs/designs` shows only added text (no removed word of an existing decision or note except appending inside the same cell).
T7.AC2: No line without a leading `|` sits between two rows of any table in either file, and line 85 of `docs/designs/sc-issue-claim-pipeline-flag.md` is byte for byte unchanged.
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
Start sha: 8a6a6ca4ec6909298c4d02cdf76f7f133588444a
Diff against the start snapshot: diff --git a/docs/designs/sc-issue-claim-pipeline-flag.md b/docs/designs/sc-issue-claim-pipeline-flag.md
index ced345ece..8968148fe 100644
--- a/docs/designs/sc-issue-claim-pipeline-flag.md
+++ b/docs/designs/sc-issue-claim-pipeline-flag.md
@@ -18,7 +18,7 @@ Today `/sc:issue --claim` assigns the issue, checks its accuracy, writes `next-s
 
 | Level | Flag | What happens after the claim's Waves 0-6 | Agent stops at |
 |---|---|---|---|
-| `worktree` (default) | `--pipeline worktree` or nothing | An Orca worktree `issue-<N>` is created (or reused) and a Claude Code agent is launched in it. It runs `next-steps.md` up to the plan boundary. | An approved plan: it prints the plan path and "Waiting for approval" until a human approves. Amended 2026-11-18: `worktree` is no longer the default; a person who types the command with no `--pipeline` gets `full`, and the issue watcher always passes `--pipeline none` |
+| `worktree` (default) | `--pipeline worktree` or nothing | An Orca worktree `issue-<N>` is created (or reused) and a Claude Code agent is launched in it. It runs `next-steps.md` up to the plan boundary. | An approved plan: it prints the plan path and "Waiting for approval" until a human approves. Amended 2026-11-18: `worktree` is no longer the default; a person who types the command with no `--pipeline` gets `full`, and the issue watcher always passes `--pipeline none`. Amended 2026-11-18 (second): the default is now picked from the issue (a bug or a simple or medium feature of 16 hours or less gets `full`; a complex feature, a feature over 16 hours or an issue that cannot be classified gets `worktree`; an explicit `--pipeline` always wins; the issue watcher always passes `--pipeline none`) |
 | `full` | `--pipeline full` | Same, but the agent runs every step including `/sc:implement` or `/task`. | Finished implementation, unstaged, uncommitted, unpushed |
 | `full` + `--submit` | `--pipeline full --submit` | Same, then the agent commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`. | A pushed branch with an open PR on the fork |
 | `none` | `--pipeline none` | The claim ends after the comments (amended 2026-11-08): no worktree is created, no agent is launched. | The claim itself runs nothing. Without a coordinator, the user runs `next-steps.md` from the main checkout's `.dev/issues/<N>/`. With a coordinator that owns the issue (amended 2026-11-17), the coordinator creates the worktree with `orca_worktree.py worktree` and starts a worker in it with `worker-start`; see the "Coordinator handoff for `--pipeline none`" paragraph of `src/superclaude/commands/issue.md` |
@@ -40,9 +40,9 @@ No level merges anything. Humans only review and merge; nobody opens a PR by han
 | # | Decision | Source |
 |---|---|---|
 | P1 | Orca is a dependency. No code, warning, option or document text exists only for a project without Orca. | Owner, AD 1.2 |
-| P2 | One flag, `--pipeline worktree\|full\|none`, default `worktree`. The `--worktree` flag of MR does not exist. Amended 2026-11-18: the default is `full` when a person types the command, and the issue watcher always passes `--pipeline none`. | Owner, AD 1.6; owner, 2026-11-18 |
+| P2 | One flag, `--pipeline worktree\|full\|none`, default `worktree`. The `--worktree` flag of MR does not exist. Amended 2026-11-18: the default is `full` when a person types the command, and the issue watcher always passes `--pipeline none`. Amended 2026-11-18 (second): the default is now picked from the issue (a bug or a simple or medium feature of 16 hours or less gets `full`; a complex feature, a feature over 16 hours or an issue that cannot be classified gets `worktree`; an explicit `--pipeline` always wins; the issue watcher always passes `--pipeline none`). | Owner, AD 1.6; owner, 2026-11-18 |
 | P3 | `--submit` is a second flag, valid with `--pipeline full` only. It turns on commit, push of a feature branch and `/sc:pr-submit --monitor 3`. It never merges. | Owner, AD 1.4 |
-| P4 | The default stop is an approved plan. `full` adds implementation. `none` launches no agent. Amended 2026-11-08: `none` also creates no worktree, because every worktree gets an agent. | Owner, AD 1.3; owner, 2026-11-08 |
+| P4 | The default stop is an approved plan. `full` adds implementation. `none` launches no agent. Amended 2026-11-08: `none` also creates no worktree, because every worktree gets an agent. Amended 2026-11-18 (second): the default stop is no longer always an approved plan; with no `--pipeline` the level is picked from the issue (a bug or a simple or medium feature of 16 hours or less gets `full`; a complex feature, a feature over 16 hours or an issue that cannot be classified gets `worktree`, which stops at an approved plan; an explicit `--pipeline` always wins; the issue watcher always passes `--pipeline none`). | Owner, AD 1.3; owner, 2026-11-08 |
 | P5 | The launched agent is Claude Code behind the ccsession shim, always. | Owner, AD 1.5 |
 | P6 | **B2 is rewritten (new text below).** B16 (worktree after `next-steps.md`), B17 (launch levels) and B18 (`--submit`) are new design decisions in `docs/designs/sc-issue-command.md`. | Owner, AD 1.1 and 3 |
 | P7 | The agent is started with `orca agent launch --agent claude --surface terminal`, a Claude CLI session. Never a plain terminal, and never `--surface chat` (a chat is not behind the shim). | #412 (merged), AD FR-22 |
@@ -63,7 +63,7 @@ No level merges anything. Humans only review and merge; nobody opens a PR by han
 | Create JSON shape | MR R2 UNVERIFIED | AD observed `result.worktree.{id, path, branch, ...}`. FR-20 (path from a row-id difference) stays; the field is not relied on. | The set difference works with an opaque create result. |
 | `worktree_warning` holds one code | MR open item | The code that set the status wins; any other goes in `detail`. Launch codes use their own field `launch_warning`. | Two independent steps can each warn. |
 | Statuses | MR: `created \| reused \| skipped \| failed` | `created \| reused \| failed` | AD 4.2 and 4.4: `skipped` existed only for a missing `orca`. |
-| Unflagged claim | MR FR-3: byte-identical to today | Dropped. An unflagged claim is `--pipeline worktree`. Amended 2026-11-18: an unflagged claim typed by a person is now `--pipeline full`; the issue watcher always passes `--pipeline none`. | AD 4.3. |
+| Unflagged claim | MR FR-3: byte-identical to today | Dropped. An unflagged claim is `--pipeline worktree`. Amended 2026-11-18: an unflagged claim typed by a person is now `--pipeline full`; the issue watcher always passes `--pipeline none`. Amended 2026-11-18 (second): the default is now picked from the issue (a bug or a simple or medium feature of 16 hours or less gets `full`; a complex feature, a feature over 16 hours or an issue that cannot be classified gets `worktree`; an explicit `--pipeline` always wins; the issue watcher always passes `--pipeline none`). | AD 4.3. |
 | `--worktree` with `--create` | MR FR-2 | `--pipeline` or `--submit` with `--create`: STOP `E-CLAIM-ONLY-FLAG`. | AD section 2. |
 
 ## 4. Command interface
@@ -75,7 +75,7 @@ No level merges anything. Humans only review and merge; nobody opens a PR by han
 
 | Flag | Mode | Default | Values | Meaning |
 |---|---|---|---|---|
-| `--pipeline` | claim | `worktree` | `worktree`, `full`, `none` | How far the launched agent goes (section 1). `worktree` and `full` create the worktree and launch an agent; `none` creates no worktree and launches no agent. Amended 2026-11-18: the default is now `full` for a person; the issue watcher always passes `--pipeline none` |
+| `--pipeline` | claim | `worktree` | `worktree`, `full`, `none` | How far the launched agent goes (section 1). `worktree` and `full` create the worktree and launch an agent; `none` creates no worktree and launches no agent. Amended 2026-11-18: the default is now `full` for a person; the issue watcher always passes `--pipeline none`. Amended 2026-11-18 (second): the default is now picked from the issue (a bug or a simple or medium feature of 16 hours or less gets `full`; a complex feature, a feature over 16 hours or an issue that cannot be classified gets `worktree`; an explicit `--pipeline` always wins; the issue watcher always passes `--pipeline none`) |
 | `--submit` | claim | off | no value | With `--pipeline full` only: after implementation the agent commits, pushes the feature branch to `origin` and runs `/sc:pr-submit --monitor 3`. Never merges |
 
 STOP rules added to the command file, checked in this order after the existing ones (before Activation, no external call):
@@ -84,7 +84,7 @@ STOP rules added to the command file, checked in this order after the existing o
 2. A `--pipeline` value that is not one of the three: STOP, list `worktree`, `full`, `none`. `--pipeline` with no value: the same STOP.
 3. `--submit` with a value, or with `--pipeline worktree` or `--pipeline none` or no `--pipeline`: STOP `E-SUBMIT-NEEDS-FULL` ("--submit needs --pipeline full").
 
-Examples: `/sc:issue --claim 302` (worktree level; amended 2026-11-18: now the `full` level when a person types it, and the issue watcher always passes `--pipeline none`), `/sc:issue --claim 302 --pipeline none`, `/sc:issue --claim 302 --pipeline full`, `/sc:issue --claim 302 --pipeline full --submit`.
+Examples: `/sc:issue --claim 302` (worktree level; amended 2026-11-18: now the `full` level when a person types it, and the issue watcher always passes `--pipeline none`; amended 2026-11-18 (second): the level is now picked from the issue, `full` for a bug or a simple or medium feature of 16 hours or less and `worktree` otherwise), `/sc:issue --claim 302 --pipeline none`, `/sc:issue --claim 302 --pipeline full`, `/sc:issue --claim 302 --pipeline full --submit`.
 
 `commands/issue.md` gets `version: "1.1.0"` (8 of 47 commands carry one; the claim behaviour changes for every user). `argument-hint`, Usage, Options table, Examples, Outputs, Boundaries and the claim paragraph are updated. Boundaries, Will Not: replace "Run any next-step command" with "Run `/sc:implement`, `/task`, a commit, a push or `/sc:pr-submit` itself (the launched agent may, at the level the user chose)", and add "Pass an Orca link flag" and "Merge anything". `SKILL.md` Will / Will Not mirror this.
 
@@ -271,7 +271,7 @@ New STOPs:
 |---|---|
 | `E-ORCA-REQUIRED` | Wave 0: `orca_worktree.py preflight` returns `ok: false` |
 | `E-CLAIM-ONLY-FLAG` | `--pipeline` or `--submit` with `--create` |
-| `E-SUBMIT-NEEDS-FULL` | `--submit` without `--pipeline full`. Amended 2026-11-18: a `--submit` with no `--pipeline` also stops, because the default is now `full` but `--submit` still needs `--pipeline full` written out |
+| `E-SUBMIT-NEEDS-FULL` | `--submit` without `--pipeline full`. Amended 2026-11-18: a `--submit` with no `--pipeline` also stops, because the default is now `full` but `--submit` still needs `--pipeline full` written out. Amended 2026-11-18 (second): the default is now picked from the issue; that changes nothing here, because a `--submit` with no `--pipeline` still stops |
 
 Warnings (the claim `status` stays `success` for all of them). `W-ORCA-MISSING` and the `skipped` status of MR no longer exist.
 
diff --git a/docs/designs/sc-issue-command.md b/docs/designs/sc-issue-command.md
index 492c10dc3..bb9eee061 100644
--- a/docs/designs/sc-issue-command.md
+++ b/docs/designs/sc-issue-command.md
@@ -41,7 +41,7 @@ Every row is binding. "Owner" is the issue author's comments of 2026-10-30; "Com
 | B14 | Brainstorm and implement work after a claim runs on T1 or T2 by complexity. | Owner, 2026-10-30 14:15 |
 | B15 | Order of work for this feature: `/sc:design`, then `/sc:workflow`, then `/sc:implement` (the issue body's "before invoking Brainstorm" is superseded). | Coordinator brief carrying the owner instruction |
 | B16 | After `next-steps.md` is written and both comments are posted, the claim creates (or reuses) an Orca worktree `issue-<N>` and copies `.dev/issues/<N>/` into it. Orca is required (`E-ORCA-REQUIRED`); every later failure is a warning and the claim stays a success. | Owner, 2026-11-05; `docs/designs/sc-issue-claim-pipeline-flag.md` |
-| B17 | Launch levels through `--pipeline`: `worktree` (default, plans and waits for approval), `full` (also implements, no commit or push), `none` (no worktree and no agent; amended 2026-11-08, it was "worktree only, no agent" before every worktree needed an agent; amended 2026-11-17, the claim still makes no worktree and no agent, and a coordinator that owns the issue may then create the worktree and start a worker, see "Coordinator handoff for `--pipeline none`" in `src/superclaude/commands/issue.md`). For `worktree` and `full` the agent starts behind the ccsession shim through `orca agent launch --surface terminal`. Amended 2026-11-18: the default is now `full` for a person who types the command, and the issue watcher always passes `--pipeline none`. | Owner, 2026-11-05; `docs/designs/sc-issue-claim-pipeline-flag.md` |
+| B17 | Launch levels through `--pipeline`: `worktree` (default, plans and waits for approval), `full` (also implements, no commit or push), `none` (no worktree and no agent; amended 2026-11-08, it was "worktree only, no agent" before every worktree needed an agent; amended 2026-11-17, the claim still makes no worktree and no agent, and a coordinator that owns the issue may then create the worktree and start a worker, see "Coordinator handoff for `--pipeline none`" in `src/superclaude/commands/issue.md`). For `worktree` and `full` the agent starts behind the ccsession shim through `orca agent launch --surface terminal`. Amended 2026-11-18: the default is now `full` for a person who types the command, and the issue watcher always passes `--pipeline none`. Amended 2026-11-18 (second): the default is now picked from the issue (a bug or a simple or medium feature of 16 hours or less gets `full`; a complex feature, a feature over 16 hours or an issue that cannot be classified gets `worktree`; an explicit `--pipeline` always wins; the issue watcher always passes `--pipeline none`). | Owner, 2026-11-05; `docs/designs/sc-issue-claim-pipeline-flag.md` |
 | B18 | `--submit` (with `--pipeline full` only) turns on the commit, the push of a feature branch and `/sc:pr-submit --monitor 3`. Nothing merges at any level; humans only review and merge. | Owner, 2026-11-05; `docs/designs/sc-issue-claim-pipeline-flag.md` |
 
 ## 3. Corrections to the issue text
@@ -65,6 +65,8 @@ Every row is binding. "Owner" is the issue author's comments of 2026-10-30; "Com
 
 > **Amended 2026-11-18:** the `--pipeline` default is `full` when a person types the command (not `worktree`); the issue watcher always passes `--pipeline none`. A `--submit` with no `--pipeline` still stops with `E-SUBMIT-NEEDS-FULL`.
 
+> **Amended 2026-11-18 (second):** with no `--pipeline` the level is picked from the issue: a bug or a simple or medium feature of 16 hours or less gets `full`; a complex feature, a feature over 16 hours or an issue that cannot be classified gets `worktree`. An explicit `--pipeline` always wins, and the issue watcher always passes `--pipeline none`. The rule lives in `refs/claim.md` Wave 5 of the skill.
+
 ```text
 /sc:issue --claim <number|url>
 /sc:issue --create "<description>" [--depth quick|standard|deep] [--mode feature|bug] [--type <type>]


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
