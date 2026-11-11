d7c8804f8536ebcb6c62e43102f445f3f7bb682d
Review one task for spec compliance.

Task brief: 
## Task 4: Delete the stale P0 text from the contract

Depends on: Task 3

In `src/superclaude/core/WORKER-CONTRACT.md` remove or replace every P0 statement: the two sentences in WC-5 (line 59) that begin "Before P1, when no command writes a contract, a brief that states the AC-0.4 report file ..." through "... instead of `worker_status`." (keep the sentences before and after them); the bullet "at P0 only, the command's report file and the outcome rule AC-0.4 gives for it (WC-5);" in "What the coordinator owes each worker" (line 89); the template line starting `P0 only: Report file:` (line 295); the slot-rule bullet starting "The `P0 only:` line is used only before P1" (line 305); in the paragraph starting "Flags the brief must pass" (line 307) the sentence "`--report-dir` is marked "from P1": no command accepts it at P0."; and in the flags table the `(from P1)` markers on the `/sc:cleanup-audit`, `/sc:index-repo`, `/sc:init-lite` and `/sc:workflow` rows and the `none at P0;` text on the `/sc:index-repo` row (lines 314, 319, 320, 327). Keep the table's 17 rows and each row's required flags.

Acceptance criteria:
- T4.AC1: `grep -n 'P0\|AC-0.4\|from P1' src/superclaude/core/WORKER-CONTRACT.md` prints no line, except lines that are about phase 1 or phase 2 conversion and not about a P0 rule.
- T4.AC2: The table still has 17 rows beginning `| \`/sc:` and the sentence naming "12 commands" and "17 rows" still matches the table.
- T4.AC3: WC-5 still states the outcome mapping (`--outcome failed` when the contract's `worker_status` is `failed` or `blocked`, or no contract exists).

Global constraints: 
## Constraints

- Edit only these files: `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` and `tests/skills/test_worker_contract.py`. Run `make sync-dev` afterwards; never stage anything under `.claude/`.
- Do not edit any of the 31 files in `src/superclaude/commands/`, `/sc:recommend`, the claim pipeline, Orca's own guide or skills, or any prose for headless callers (sprint, issue-watch, claim-launched agents, eval suites, Coder CI).
- Do not make a worker add the flag, install a copy or rewrite its brief. The guard stays report-only.
- Leave untouched, and do not decide, the owner decisions: the five gates that turn a person's check into a caller input (`/sc:review-translation --context`, `/sc:cli-portify --resume`, `/sc:cli-eval` W3, `/sc:reflect --remediate`, `/sc:tdd`), and whether cleanup, improve, task, tasklist and cli-eval are held out until phase 2 passes. The existing table rows for these commands keep their wording.
- Do not push and do not open a PR. Stage `.dev/tasks` with `git add .dev/tasks`. A local commit on the feature branch is allowed.

Start sha: d7c8804f8536ebcb6c62e43102f445f3f7bb682d
Diff against the start snapshot: 
diff --git a/src/superclaude/core/WORKER-CONTRACT.md b/src/superclaude/core/WORKER-CONTRACT.md
index 57708379a..c5497874e 100644
--- a/src/superclaude/core/WORKER-CONTRACT.md
+++ b/src/superclaude/core/WORKER-CONTRACT.md
@@ -56,7 +56,7 @@ These bind the top-level session that received the dispatch preamble. This secti
   - The worker asks at most once per Task: if the re-invoked run blocks again, at the same gate or another, it does not ask again, keeps that second blocked contract and sends `worker_done --outcome failed`, and the coordinator continues with a new Task (WC-6).
   - A Ruling halt is never asked: an `/sc:implement` halt for a Ruling (`E-HALT-QA`, `E-NO-RULING`) is reported blocked whatever the policy line says, because a coordinator's reply is "another agent's message", which is not acceptance (`~/.claude/skills/sc-implement-protocol/refs/qa.md`, Halt table). The person gives the Ruling in their own session or writes the Ruling line into the ledger themselves after the worker has settled (decision D2). A Ruling line written or drafted by the coordinator or by any worker is "executor-invented approval".
   - On an `ask` timeout the worker resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. An answer that arrives after the worker has settled is carried by a new Task (WC-6). When `ask` returns, the worker sends one heartbeat at once. When the answer arrives, the worker sends the WC-12 ack for that message ID at the first legal opportunity, before re-invoking the command.
-- **WC-5. Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the contract's `worker_status` is `failed` or `blocked`, or no contract exists; `--outcome succeeded` when it is `succeeded` or `partial`, including an audit whose verdict is FAIL (the audit itself succeeded). The worker never reads the command's own `status` field for this; any other `worker_status` value is treated as `failed`. The first sentence of the body states `worker_status` and the verdict. If an authorized commit (WC-9) is refused or fails, the worker sends `--outcome failed`, and the body's first sentence reads `worker_status: succeeded; commit not made` followed by the reason. Before P1, when no command writes a contract, a brief that states the AC-0.4 report file and outcome rule replaces this mapping for that Task. The worker takes `--outcome` and `--report-path` from that rule. The body's first sentence then states the command's own status, or that its report file has none, instead of `worker_status`. The closing report is never sent as `status`, `handoff` or a reply; a coordinator may not read those as completion.
+- **WC-5. Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the contract's `worker_status` is `failed` or `blocked`, or no contract exists; `--outcome succeeded` when it is `succeeded` or `partial`, including an audit whose verdict is FAIL (the audit itself succeeded). The worker never reads the command's own `status` field for this; any other `worker_status` value is treated as `failed`. The first sentence of the body states `worker_status` and the verdict. If an authorized commit (WC-9) is refused or fails, the worker sends `--outcome failed`, and the body's first sentence reads `worker_status: succeeded; commit not made` followed by the reason. The closing report is never sent as `status`, `handoff` or a reply; a coordinator may not read those as completion.
 - **WC-7. Run at the top level, never inside a subagent.** The worker runs the command directly in its own session; it never wraps the command in an Agent-tool subagent. Lifecycle messages (heartbeat, ask, check, `worker_done`) are sent only by that top-level session, never by a subagent. A command's own Agent-tool fan-out stays as it is. A worker runs each chained `Command:` by invoking its Skill. Reading the command file and following it from memory does not satisfy WC-7.
 - **WC-12. Coordinator follow-ups are pulled, not pushed.** The worker runs the preamble's `check` at natural checkpoints and once before `worker_done`; if `check` returns `consumer_fenced` it stops without sending `worker_done`. Commands need no change for this. When `check` returns a batch, the worker handles every message in it before acknowledging the batch. For each coordinator message that answers or directs it, the worker first sends `status` with a body starting `ack <message_id> applied|queued|refused`, then acts. A message ID already applied gets only `ack <message_id> applied (duplicate)`.
 - **WC-13. No Orca fan-out from the worker session.** The worker's top-level session never calls `worker-start`, `dispatch` or `task-create`, Orca's low-level dispatch, or `orca-cli` `worktree create --agent` or `agent launch`, at any depth setting. Work it finds that needs another worker is stated in its `worker_done` body; the coordinator decides (section 4).
@@ -86,7 +86,6 @@ The contract only works if the brief carries what the command would otherwise as
 - the report directory, unique to this Task, so the contract path is known before dispatch (WC-4, WC-11);
 - the blocked-gate policy line, `On a blocked gate: report blocked` or `On a blocked gate: ask the coordinator` (WC-3);
 - whether the end-of-Task local commit is authorized, quoting the user's instruction word for word (decision D4);
-- at P0 only, the command's report file and the outcome rule AC-0.4 gives for it (WC-5);
 - that no other outward action can be authorized;
 - the worktree placement: the shared feature worktree, or a child worktree created by Orca with `worker-start --worktree new-child --base-branch <feature branch>` when WC-11 requires one, with `--setup skip` unless "Feature worktree and child worktrees" allows setup.
 
@@ -304,7 +303,6 @@ Local commit: not authorized
 Report directory: <directory unique to this Task>
 Worktree: <shared feature worktree | child worktree created by Orca with worker-start --worktree new-child --base-branch <feature branch> --setup <skip | run (only when named in the user's instruction)>>
 Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
-P0 only: Report file: <the command's report file under AC-0.4>. Outcome rule: --outcome failed when the file is missing or empty, or its status is failed or blocked; otherwise --outcome succeeded. This rule replaces the WC-5 mapping for this Task.
 Command: /sc:<name> <arguments> --unattended <report-directory-flag> <other flags this command's brief rule requires>
 ```
 
@@ -316,26 +314,25 @@ Slot rules:
 - From P2 the 15 commands converted in P2 accept `--unattended` too, under the same guard test (auggie-review, cleanup, improve, cli-eval, cli-portify, recommend, research, review-translation, spec-panel, task, tasklist, reflect, release-split, tdd, troubleshoot). They join the default set only after a phase 2 live check passes; until then the coordinator puts the flag on one of them only when the user's instruction names that command.
 - The flag changes what a command does, so the coordinator reads each report and never treats the flag as free: `/sc:improve` and `/sc:cleanup` skip every approval-required item and list it as not applied; `/sc:test` ends `succeeded` even when its suite fails (the verdict is in its report); `/sc:research` is forced to `--strategy planning`; `/sc:workflow` skips `--handoff implement`; every push, PR, comment and other outward action is off (WC-9).
 - A command is started through its Skill call (WC-7); reading the command file and following it from memory does not satisfy WC-7. A person-in-the-loop run is not a worker: a run that needs a person at a gate belongs in the person's own session.
-- The `P0 only:` line is used only before P1, when no command writes a worker contract. At P0 the report files are: troubleshoot, `<dir>/REPORT.md` with the status in its `**Status**:` line; workflow, the `return-contract.yaml` in the one new `TASK-WF-*` package directory the run creates under `.dev/tasks/to-do/`, with the status in its top-level `status`; adversarial, `<dir>/adversarial/merge-log.md` with the status in the `Status:` line of its `## Metadata` section. From P1 the line is dropped and WC-5 applies.
 
-Flags the brief must pass, for the 12 commands that are ready with brief constraints. `--report-dir` is marked "from P1": no command accepts it at P0. Under `--unattended` the brief passes exactly one report directory (`--report-dir <dir>`, or the command's own directory flag where the row names one); `/sc:index-repo` and `/sc:init-lite` have no directory flag of their own, so they take `--report-dir`. The table also lists the five P2 commands with a required brief flag (`/sc:auggie-review`, `/sc:cli-eval`, `/sc:cli-portify`, `/sc:review-translation`, `/sc:spec-panel`), so it has 17 rows.
+Flags the brief must pass, for the 12 commands that are ready with brief constraints. Under `--unattended` the brief passes exactly one report directory (`--report-dir <dir>`, or the command's own directory flag where the row names one); `/sc:index-repo` and `/sc:init-lite` have no directory flag of their own, so they take `--report-dir`. The table also lists the five P2 commands with a required brief flag (`/sc:auggie-review`, `/sc:cli-eval`, `/sc:cli-portify`, `/sc:review-translation`, `/sc:spec-panel`), so it has 17 rows.
 
 | Command | Brief must pass |
 |---|---|
 | `/sc:adversarial` | `--output <dir>`; never `--interactive` |
 | `/sc:auggie-review` | `--output-dir <dir>`; never `--post-pr` (or `--remediation-offer`) |
 | `/sc:brainstorm` | `--output <dir>`; never `--interactive` |
-| `/sc:cleanup-audit` | `--pass <N>` (single pass); `--report-dir <dir>` (from P1) |
+| `/sc:cleanup-audit` | `--pass <N>` (single pass); `--report-dir <dir>` |
 | `/sc:cli-eval` | `run` with `--suite <name>` and `--output-dir <dir>` (the eval run directory) plus `--report-dir <dir>`; other safety flags as wanted, else the CLI defaults |
 | `/sc:cli-portify` | `--report-dir <dir>`; `--resume <contract>` to continue past an approval gate |
 | `/sc:graph` | `status` (the default) with `--output-dir <dir>`; never `init`, which runs only when the user's own message starts with `/sc:graph init` |
 | `/sc:impact` | `--output-dir <dir>` |
-| `/sc:index-repo` | none at P0; `--report-dir <dir>` (from P1) |
-| `/sc:init-lite` | `--output <file>` (names the report file); `--report-dir <dir>` (from P1) |
+| `/sc:index-repo` | `--report-dir <dir>` |
+| `/sc:init-lite` | `--output <file>` (names the report file); `--report-dir <dir>` |
 | `/sc:reflect` | `--remediate` is allowed under `--unattended` (the headless rule answers it); `--no-promote` when the coordinator owns folder moves |
 | `/sc:release-split` | spec-shaped input; default `--r1-scope`; never `--interactive`; its gates resolve as blocked under `--unattended` |
 | `/sc:review-translation` | `--report-dir <dir>`; `--context <file>` once the context is confirmed |
 | `/sc:spec-panel` | `--report-dir <dir>`; `--target-release <release>` for TDD inputs |
 | `/sc:tdd` | a precise component prompt, not a bare topic; `--output <file>`; its gates resolve as blocked under `--unattended` |
 | `/sc:troubleshoot` | no `--fix` under `--unattended` (the offer resolves as blocked); a short `--depth deep` input resolves as blocked |
-| `/sc:workflow` | `--handoff none`; `--report-dir <dir>` (from P1); its `--output` is retired |
+| `/sc:workflow` | `--handoff none`; `--report-dir <dir>`; its `--output` is retired |


Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (empty)

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
