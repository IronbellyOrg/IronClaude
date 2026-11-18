a4a4adeda76c70ba08c4c0e16abaeb59bd924a29
Review one task for spec compliance.

Task brief: ## Task 6: Update the user guide and the architecture reference
Depends on: Task 1

In `docs/user-guide/commands.md`: line 368 (the `--pipeline` row) set the default cell to "`full` or `worktree`, picked from the issue" and replace "omitted means `full`" with the one-sentence outcome (a bug or a simple or medium feature of 16 hours or less gets `full`; a complex feature, a feature over 16 hours or an unclassifiable issue gets `worktree`); line 371 keep the `E-SUBMIT-NEEDS-FULL` sentence and the watcher sentence but change "(write `--pipeline full --submit`, even though `full` is the default)" to "(write `--pipeline full --submit`)", and say an explicit `--pipeline` always wins; in the levels table move "(default)" off the `full` row (line 378) and say in the table's lead-in line that the default is picked from the issue; leave the example at line 388 and the guard and ship-gate paragraph (line 382) unchanged. In `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md`: line 1557 change the `--pipeline` default from `full` to "`full` or `worktree`, picked from the issue by `refs/claim.md` Wave 5 (an explicit value wins)" and keep the Impact cell, which already names the no `--pipeline` case; line 1635 is unchanged.
Acceptance criteria (ids):
T6.AC1: `grep -n "(default)" docs/user-guide/commands.md` prints no line from the `/sc:issue` levels table, and the options row and the lead-in say the default is picked from the issue; `grep -n "even though .full. is the default" docs/user-guide/commands.md` prints nothing.
T6.AC2: The syntax block, the ClickUp table and the guard paragraph of `docs/user-guide/commands.md` are unchanged; line 1557 of the architecture reference shows the picked default and line 1635 is unchanged.
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
Start sha: a4a4adeda76c70ba08c4c0e16abaeb59bd924a29
Diff against the start snapshot: diff --git a/docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md b/docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md
index 63b1aab1e..81a943d7b 100644
--- a/docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md
+++ b/docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md
@@ -1554,7 +1554,7 @@ Settings and flags that change behavior, with the default of each build kept sep
 | `orchestrationHeartbeatIntervalMinutes` | Minutes between heartbeats | 5; range 1-60; anything else (0, 61, 2.5, strings) becomes 5 (`orchestration-heartbeat.ts:6,10-12,15-31`, re-read) | The "two missed intervals" threshold (`:9`) is a warning only in the retired scheduler (`coordinator-task-dispatch.ts:16-34`); on the live surface Orca derives no verdict from heartbeat age. Heartbeat age as a stall indicator is IronClaude policy (S-table, deadline W) |
 | `IR7_REFUSE` (L2 pre-push refusal) | Whether a missing L2 hook refuses the launch | CHECKOUT: no such switch; the claim warns `W-L2-ABSENT` only (`orca_worktree.py:800-801`). ORIGIN/MASTER and the installed copy: `IR7_REFUSE = False` (research 04 F5, installed line 819, not traced further) | Warning only in both; ORIGIN/MASTER also installs an owned L2 pre-push hook |
 | `--unattended` and `--report-dir <dir>` (command flags, `WORKER-CONTRACT.md:12-15`) | Switch a command to worker mode; the one report directory | off; `--unattended` counts only as a standalone token outside quotes | Person-mode flags (`--interactive`, `--format interactive`, `--mode socratic`, `--watch`, `--monitor 1`) are refused with `worker_status: failed`; neither or both report directories is refused with the exact chat error at `:38`. The `--monitor 1` clause has no implementing `## Unattended mode` section in pr-submit (owner question C2) |
-| `/sc:issue --claim` launch level: command flags `--pipeline` and `--submit`; claim-helper argument `--level` | The command takes `--pipeline worktree\|full\|none` and `--submit` (only with `--pipeline full`) (`src/superclaude/commands/issue.md:43-44`). `--level worktree\|full` is not a command flag: it is the required argument of the helper subcommands `prompt` and `launch` (`orca_worktree.py:1448,1458`), together with `--submit`; the skill passes the level `<L>` to `launch` (`refs/claim.md:118`). The level word written to `pending/<nonce>` is `worktree`, `full`, or `full-submit` when `--submit` is given (`orca_worktree.py:1334`); `main` rejects `--submit` without `--level full` (`:1467-1468`) | `--pipeline`: `full`; `--submit`: off (`issue.md:43-44`); the helper's `--level` has no default (required) | `--pipeline none` ends the claim before Wave 7 and 8: no worktree, no agent (`refs/claim.md:93`). `--submit` with a pipeline other than `full`, with no `--pipeline`, or with a value, is refused before Activation with `E-SUBMIT-NEEDS-FULL` (`sc-issue-protocol/SKILL.md:144`) |
+| `/sc:issue --claim` launch level: command flags `--pipeline` and `--submit`; claim-helper argument `--level` | The command takes `--pipeline worktree\|full\|none` and `--submit` (only with `--pipeline full`) (`src/superclaude/commands/issue.md:43-44`). `--level worktree\|full` is not a command flag: it is the required argument of the helper subcommands `prompt` and `launch` (`orca_worktree.py:1448,1458`), together with `--submit`; the skill passes the level `<L>` to `launch` (`refs/claim.md:118`). The level word written to `pending/<nonce>` is `worktree`, `full`, or `full-submit` when `--submit` is given (`orca_worktree.py:1334`); `main` rejects `--submit` without `--level full` (`:1467-1468`) | `--pipeline`: `full` or `worktree`, picked from the issue by `refs/claim.md` Wave 5 (an explicit value wins); `--submit`: off (`issue.md:43-44`); the helper's `--level` has no default (required) | `--pipeline none` ends the claim before Wave 7 and 8: no worktree, no agent (`refs/claim.md:93`). `--submit` with a pipeline other than `full`, with no `--pipeline`, or with a value, is refused before Activation with `E-SUBMIT-NEEDS-FULL` (`sc-issue-protocol/SKILL.md:144`) |
 | `onFailure` (Claude Code hook field) | Makes a failing or timed-out hook block | Not set on any registration here | DOCUMENTED: with `"block"` a timeout blocks (Claude Code v2.1.295 or later); the design rejects it because a broken hook would then block ungoverned sessions (`merged-requirements.md:98,694,701`, per `gap-P3-G06.md` 2) |
 | `disableAllHooks`, `allowManagedHooksOnly`, `--bare`, `CLAUDE_CODE_SIMPLE`, `--safe-mode` (Claude Code) | Switch the settings-registered guards off | not set on the research host (`disableAllHooks` only) | DOCUMENTED routes, not observed bypasses; `disableAllHooks` alone is detected by the claim preflight |
 | Worker start readiness `timeoutMs` (Orca) | Deadline for the agent to become ready | 60 s (`local-worker-start.ts:145,228`, ORCA-CHECKOUT) | Expiry throws "Agent did not become ready" for a terminal worker (`:245-257`); the 30 s ask limit of ccsession is chosen to stay under it. The resulting Dispatch state was not traced |
diff --git a/docs/user-guide/commands.md b/docs/user-guide/commands.md
index 331c82d9a..097ff8823 100644
--- a/docs/user-guide/commands.md
+++ b/docs/user-guide/commands.md
@@ -365,17 +365,19 @@ When codegraph, the index or its lookup tools are not usable, it falls back to G
 | `--depth quick\|standard\|deep` | create | `quick` | How hard the command checks your flags and fills the body; `deep` uses the complex template |
 | `--mode feature\|bug` | create | chosen by a worker | Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` or `bug` label |
 | `--type <type>` | create | chosen by a worker | Area of the change: `cicd`, `command`, `skill`, `agent`, `hook`, `cli`, `core`, `docs`, `tests`, `install` or `other`; a feature in `tests` gets the issue type Test, otherwise the area is recorded in `flags.md` and no label is applied for it |
-| `--pipeline worktree\|full\|none` | claim | `full` | How far the launched agent goes (see the levels below); omitted means `full`; `worktree` and `full` create the worktree and launch an agent, `none` creates no worktree and launches no agent |
+| `--pipeline worktree\|full\|none` | claim | `full` or `worktree`, picked from the issue | How far the launched agent goes (see the levels below); omitted means the level is picked from the issue: a bug or a simple or medium feature of 16 hours or less gets `full`, a complex feature, a feature over 16 hours or an issue that cannot be classified gets `worktree`; `worktree` and `full` create the worktree and launch an agent, `none` creates no worktree and launches no agent |
 | `--submit` | claim | off | Only with `--pipeline full`: the agent also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`. Takes no value |
 
-`--depth`, `--mode` and `--type` work with `--create` only; `--pipeline` and `--submit` work with `--claim` only (`E-CLAIM-ONLY-FLAG`), and `--submit` with `--pipeline worktree`, with `--pipeline none` or with no `--pipeline` stops with `E-SUBMIT-NEEDS-FULL` (write `--pipeline full --submit`, even though `full` is the default). The issue watcher never relies on the default: it always passes `--pipeline none`. There is no repository option: the repository is always `origin`.
+`--depth`, `--mode` and `--type` work with `--create` only; `--pipeline` and `--submit` work with `--claim` only (`E-CLAIM-ONLY-FLAG`), and `--submit` with `--pipeline worktree`, with `--pipeline none` or with no `--pipeline` stops with `E-SUBMIT-NEEDS-FULL` (write `--pipeline full --submit`). An explicit `--pipeline` always wins over the picked level. The issue watcher never relies on the default: it always passes `--pipeline none`. There is no repository option: the repository is always `origin`.
 
 **Claim levels (`--pipeline`):**
 
+With no `--pipeline` the claim picks `full` or `worktree` from the issue (see the options table above); an explicit `--pipeline` always wins.
+
 | Level | What the launched agent does | Commit, push, PR |
 |-------|------------------------------|------------------|
 | `worktree` | Runs the steps of `next-steps.md` up to the plan boundary, prints the plan path and `Waiting for approval`, then waits until you run the printed implement command (a plain `approved` reply no longer releases it) | No |
-| `full` (default) | Runs every step, implementation included, and leaves the changes in the working tree, nothing staged | No |
+| `full` | Runs every step, implementation included, and leaves the changes in the working tree, nothing staged | No |
 | `full` with `--submit` | Does the same, then commits, pushes a feature branch to `origin` and opens a PR through `/sc:pr-submit --monitor 3` | Yes; never merges |
 | `none` | Stops after the comments: no worktree, no agent. You run `.dev/issues/<N>/next-steps.md` yourself from this checkout | No |
 


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
