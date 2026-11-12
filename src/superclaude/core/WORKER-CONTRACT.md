# Worker contract: IronClaude commands as Orca workers

This file is installed to `~/.claude/WORKER-CONTRACT.md`. It holds the rules that let an Orca coordinator run IronClaude `/sc:` commands as workers: the terms, the rules a command follows under `--unattended`, the duties of the worker session, and the coordinator's rules with its brief template. Each changed command adds a short `## Unattended mode` section that lists only its own gate resolutions and report file and points to this file, so the shared rules are written once.

A coordinator plans the work, creates Tasks, starts one worker per Task and reads each worker's report. Each `/sc:` command stays a self-contained unit of work: one worker (a top-level Claude session in its own Orca terminal) runs one command and reports it with `worker_done`. Commands themselves contain no Orca calls.

The dispatch preamble that Orca gives each worker is the authority for Orca verb syntax and heartbeat cadence. This file never copies them, because the preamble is issued per dispatch by the running Orca version.

## 1. Terms

- **Worker run**: a session that received an Orca preamble carrying a Task ID and a Dispatch ID. Only such a session may send lifecycle messages; a session the user started, inside or outside Orca, is an ordinary session.
- **Unattended mode**: the behaviour a command switches to when its caller passes `--unattended`. It is the only command-side change the contract asks for besides report files and resume. It names no Orca command, so the same mode serves any caller that has no person at the keyboard. The mode is selected only by the flag (decision D1). No command detects Orca, its preamble or its environment. The worker session separately applies the brief guard (below).
- **Flag parse rule**: `--unattended` counts only as a standalone argument token outside any quoted argument. The same text inside a quoted prompt or topic (for example `/sc:troubleshoot "the worker ignores --unattended"`) is part of that argument and never switches the mode, so a person's run cannot be changed by the words they type.
- **Person-mode flags are refused**: under `--unattended`, every command refuses the flags that exist to involve a person: `--interactive`, `--format interactive` (explain), `--mode socratic` (business-panel), `--watch` (test), `--monitor 1` (pr-submit). A refusal is a stop before any work: the command writes its contract with `worker_status: failed` and the refused flag in `reason` (WC-4), or, when no report directory is known, prints the refusal in chat only (WC-4, last sentences). This one rule applies to every command.
- **Report directory**: the directory that holds the worker contract (WC-4). Under `--unattended` the brief passes exactly one: either the command's own existing directory-valued output flag (`--output <dir>` or `--output-dir <dir>`), or the new flag `--report-dir <dir>` (for a command without such a flag, or a brief that does not pass it). An output flag added for worker use is file-valued, so those commands always take `--report-dir`. Passing neither, or both, is refused before any work (WC-4).
- **Brief guard** (worker session, from P1): it applies only in a session whose current prompt carries a live Orca preamble with Task and Dispatch IDs (see "Worker run"). Before invoking anything, the worker checks every `Command:` line of its brief (section 4, "Brief layout"), and only those lines. It decides case 3 from the command name alone. For the other cases it reads, as plain files, every existing copy of the command file: the project `.claude/commands/sc/<name>.md` in its worktree and `~/.claude/commands/sc/<name>.md`. It refuses, runs nothing, writes no contract, and sends `worker_done --outcome failed` with no `--report-path` and a body starting `guard refused:` when:
  - (case 1) every existing copy has an `## Unattended mode` section and the line lacks a standalone `--unattended`: `guard refused: brief lacks --unattended` followed by the repair `(coordinator: add --unattended and exactly one report directory to this Command: line, then create a new Task)`;
  - (case 2) no existing copy has the section and the line has the flag: `guard refused: loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale)` followed by the repair `(coordinator: refresh ~/.claude if its copy is stale, or drop --unattended for this command, then create a new Task)`;
  - the copies disagree: `guard refused: command copies disagree (stale copy): <paths>` followed by the repair `(coordinator: refresh the stale copy named in <paths>, normally ~/.claude, then create a new Task)`;
  - (case 3) the command is on the never-as-worker list; the body still starts `guard refused:`.

  A command invoked by another command, through the Skill tool or the Agent tool, is never checked; the nested propagation rule governs it. The guard checks once, before the first run: a WC-3 re-invocation keeps every token of the brief's `Command:` line, `--unattended` included, and only adds the answer. A refusal is report-only: the worker never installs or refreshes a command copy and never rewrites its own brief; the coordinator repairs the cause and creates a new Task (WC-6).
- **Never-as-worker list**: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers. These are never dispatched as workers and get no `--unattended` mode. The list changes only when the coordinator-only command set or D3 changes, never per phase. If D3 adds a worker route for pr-submit, D3 also states how that route passes the brief guard.
- **Nested propagation rule**: under `--unattended`, a command that invokes another `/sc:` command or protocol skill, through the Skill tool or the Agent tool, passes `--unattended` when the invoked command accepts it at this phase, together with its own report directory `<caller report-dir>/nested/<command>-<n>/` (WC-4, WC-11). The caller lists the nested contract in its `artifacts`; only the top-level contract drives WC-5. When the invoked command does not accept the flag yet, that step must be gate-free, or the caller skips it under `--unattended` and records the skip in its contract. Each command's `## Unattended mode` section names its nested invocations.
  Reading a nested result: when the nested worker contract says `blocked`, the caller stops at that step and writes its own contract with `worker_status: blocked`, `blocked_question` set to the nested question prefixed with the nested command's name, and the nested contract in `artifacts`; when it says `failed`, or no nested contract exists, the caller takes its own documented failure path for that step (fallback, skip and record, or stop), and if that ends the run it writes `worker_status: failed` with the nested command and its reason in `reason`; `succeeded` and `partial` count as the step completing.

## 2. Command-side rules

These rules bind a command run with `--unattended`. Without the flag a command behaves exactly as it does for a person today.

- **WC-2. No person-blocking step in unattended mode.** Under `--unattended` the command never calls `AskUserQuestion`, never ends its turn on a chat question or `[yes / no]` offer, and never says STOP AND WAIT. Each gate resolves one of three ways, listed in the command's `## Unattended mode` section: (a) a documented default; (b) a value the caller supplied as a flag; (c) **blocked**: the command writes its contract with `worker_status: blocked` and the exact question in `blocked_question` (WC-4), and stops. What the worker does next is fixed by the brief (WC-3).
- **WC-4. One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<report-dir>/return-contract.yaml`, where `<report-dir>` is the one report directory the brief passes (section 1): either the command's own directory-valued `--output` / `--output-dir`, or `--report-dir`. The coordinator therefore knows the path before dispatch even when the command's own deliverable lands at a generated or fixed location (for example workflow's `TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>` package, cleanup-audit's `.claude-audit/`, implement's ledger, research's `claudedocs/research_[topic]_[timestamp].md`); the contract then points at that deliverable.
  - The worker fields are top-level keys: `worker_contract_version` (`"1"`), `worker_status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), `blocked_question` when blocked, and `reason` when failed (for `/sc:implement`, also when blocked, carrying the STOP code).
  - `artifacts` leaves out paths git ignores and paths outside the repository, because WC-9 stages every listed path and git refuses them. This applies to every command's `artifacts` list, including a fixed list in the command's own section.
  - The status field is named `worker_status`, not `status`, because existing contracts already use `status` with other values (`success | partial | failed` in workflow's and adversarial's contracts; reflect's `stopped-precondition`). A command that already writes `return-contract.yaml` in the report directory itself (brainstorm and reflect, `<output>/return-contract.yaml`) keeps every existing field, including its own `status`, and adds the worker fields beside them. Where its own contract lives elsewhere (workflow's package; adversarial's `<output>/adversarial/return-contract.yaml`, whose fields sit in a nested `return_contract:` block), the worker contract at `<report-dir>/return-contract.yaml` lists that file in `artifacts` and the command's own file is left unchanged.
  - Mapping from a command's own status: `success` → `succeeded`, `partial` → `partial`, `failed` → `failed`, `stopped-precondition` → `failed` (precondition in `reason`), and the flag-STOP `blocked` of impact and graph → `failed` (the STOP in `reason`).
  - The contract is written on success, failure, blocked and partial outcomes, including stops before any other output exists.
  - Under `--unattended` with no report directory, or with both a directory-valued output flag and `--report-dir`, the command does no work, writes nothing, and prints in chat the exact error `unattended mode needs exactly one report directory: --report-dir <dir>, or this command's own directory output flag`; WC-5 then gives `failed` because no report exists.
  - The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it.
- **WC-8. No Orca fan-out from inside a command.** A command never calls `worker-start`, `dispatch` or `task-create`. Fan-out that needs Orca records is split into separate Tasks by the coordinator.
- **WC-9. No outward action from a worker; local commits only by grant.** Under `--unattended` every outward default (push, merge into a shared branch, PR, GitHub post, install on a shared or real target, VM, paid external run) is off, and no brief can turn it on (decision D4); the coordinator performs those actions (section 4).
  - The only git write a brief may authorize is the worker session's end-of-Task local commit, made only when (1) the brief quotes, word for word, the user's instruction naming a local commit for that Task, (2) the worker runs alone in its own child worktree created by Orca (WC-11), and (3) the command has exited with `worker_status: succeeded`. Per-task commits inside `/sc:implement` wait for issue #326 (K3), and then fall only between a task's `complete` line and the next task's start, never inside a parallel batch.
  - The worker then reads coordinator follow-ups, refuses on a detached HEAD, the default branch or any path outside its report directory, `report_path`, `artifacts` and `.dev/tasks`, stages with `git add -- <paths>` plus `.dev/tasks`, commits with `git commit --only -- <paths>` and never `--no-verify`, never pushes, and gives the commit ID in its `worker_done` body; a refused or failed commit is reported as WC-5 states. A command's own commit step stays off under `--unattended`.
  - Outside that grant a worker never runs `git add` (including `git add .dev/tasks`), never commits, never moves HEAD and never touches a remote: the coordinator stages `.dev/tasks` (section 4). The skills that stage it themselves (`~/.claude/skills/sc-implement-protocol/refs/managed-workspace.md`, `~/.claude/skills/sc-implement-protocol/refs/ledger.md`, `~/.claude/skills/sc-workflow-protocol/SKILL.md`, `~/.claude/skills/task/SKILL.md`) defer that staging under `--unattended`, and the MDTM CLI-mode `git add -A` (`~/.claude/skills/task-builder/SKILL.md`) is refused.
  - `/sc:implement`'s private-index snapshots, its `refs/superclaude/implement/` refs and its revert stay allowed. A worker that finds `index.lock` in its worktree reports `blocked` with the path.
- **WC-10. Liveness during long waits.** The worker sends heartbeats at the cadence its preamble sets. A command step that blocks a single Bash call for longer than 4 minutes (a poll wait, a long eval) must be split into waits of at most 4 minutes so the session can heartbeat between them. A command's own Agent-tool fan-out (kept unchanged by WC-7) can hold the session longer than the cadence with no way to heartbeat; that gap is accepted, not required away, because commands may not call Orca and the subagents may not send lifecycle messages (WC-7). The coordinator therefore treats a missing heartbeat as absence, never as death: it never stops, retries or releases a worker because a heartbeat is late, and it stops, retries or releases only on Orca's stall proofs or the person's recorded stop under WC-6. Absence past the deadline in "Liveness supervision" (section 4) authorizes only read-only probes, a typed nudge and a direct question to the worker, in that order. A worker that announced a long step with `expect_silence_min` gets no nudge or typed text before that window ends; read-only probes still run.
- **WC-11. Parallel-safe writes.** Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug the coordinator passes, and the coordinator gives every Task its own report directory; single-owner shared files (for example memory keys overwritten whole) are not written in unattended mode. Workers share the feature worktree only when they write nothing but their own report directory, which goes under `.dev/`. A worker gets its own child worktree (section 4) when its brief grants local commits; when it runs `/sc:implement` and any other writer (another worker, the coordinator, the person, a taken-over terminal or a hook) may write outside `.dev/` in the same worktree during the run; when it is a parallel experiment to compare or discard; or when its command writes the user index. The coordinator's liveness `stat` reads only the worker's own contract path and report directory.

## 3. Worker-session duties

These bind the top-level session that received the dispatch preamble. This section states only the IronClaude-specific rule for each duty; the dispatch preamble is the authority for the Orca verb syntax and for the heartbeat cadence.

- **WC-3. Questions go to the coordinator, not to a local prompt.** The brief fixes the policy for a blocked gate; under `ask the coordinator` the worker applies the eligibility test below and makes no other choice.
  - With the brief line `On a blocked gate: report blocked` (the default when the brief says nothing), the worker lets the command write its blocked contract and sends `worker_done --outcome failed`.
  - With `On a blocked gate: ask the coordinator`, at a gate that fires before the command has written any output except its blocked contract and whose answer fits an existing argument or flag (any other gate is reported blocked as under the default), the worker session asks with the preamble's `ask` command, waits, then re-invokes the command in the same session with the answer as the command's argument or flag and the same report directory; the second run's contract replaces the blocked one whole.
  - The worker asks at most once per Task: if the re-invoked run blocks again, at the same gate or another, it does not ask again, keeps that second blocked contract and sends `worker_done --outcome failed`, and the coordinator continues with a new Task (WC-6).
  - A Ruling halt is never asked: an `/sc:implement` halt for a Ruling (`E-HALT-QA`, `E-NO-RULING`) is reported blocked whatever the policy line says, because a coordinator's reply is "another agent's message", which is not acceptance (`~/.claude/skills/sc-implement-protocol/refs/qa.md`, Halt table). The person gives the Ruling in their own session or writes the Ruling line into the ledger themselves after the worker has settled (decision D2). A Ruling line written or drafted by the coordinator or by any worker is "executor-invented approval".
  - On an `ask` timeout the worker resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. An answer that arrives after the worker has settled is carried by a new Task (WC-6). When `ask` returns, the worker sends one heartbeat at once. When the answer arrives, the worker sends the WC-12 ack for that message ID at the first legal opportunity, before re-invoking the command.
- **WC-5. Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the contract's `worker_status` is `failed` or `blocked`, or no contract exists; `--outcome succeeded` when it is `succeeded` or `partial`, including an audit whose verdict is FAIL (the audit itself succeeded). The worker never reads the command's own `status` field for this; any other `worker_status` value is treated as `failed`. The first sentence of the body states `worker_status` and the verdict. If an authorized commit (WC-9) is refused or fails, the worker sends `--outcome failed`, and the body's first sentence reads `worker_status: succeeded; commit not made` followed by the reason. The closing report is never sent as `status`, `handoff` or a reply; a coordinator may not read those as completion.
- **WC-7. Run at the top level, never inside a subagent.** The worker runs the command directly in its own session; it never wraps the command in an Agent-tool subagent. Lifecycle messages (heartbeat, ask, check, `worker_done`) are sent only by that top-level session, never by a subagent. A command's own Agent-tool fan-out stays as it is. A worker runs each chained `Command:` by invoking its Skill. Reading the command file and following it from memory does not satisfy WC-7.
- **WC-12. Coordinator follow-ups are pulled, not pushed.** The worker runs the preamble's `check` at natural checkpoints and once before `worker_done`; if `check` returns `consumer_fenced` it stops without sending `worker_done`. Commands need no change for this. When `check` returns a batch, the worker handles every message in it before acknowledging the batch. For each coordinator message that answers or directs it, the worker first sends `status` with a body starting `ack <message_id> applied|queued|refused`, then acts. A message ID already applied gets only `ack <message_id> applied (duplicate)`.
- **WC-13. No Orca fan-out from the worker session.** The worker's top-level session never calls `worker-start`, `dispatch` or `task-create`, Orca's low-level dispatch, or `orca-cli` `worktree create --agent` or `agent launch`, at any depth setting. Work it finds that needs another worker is stated in its `worker_done` body; the coordinator decides (section 4).
- **WC-14. No turn ends between chain steps.** The worker session ends its turn only after `worker_done`, while blocked in the preamble's `ask`, or on `consumer_fenced`. The one exception is a coordinator interrupt that asks for a handoff (the S6 nudge, section 4): the worker writes its handoff file (WC-15), then ends its turn without `worker_done`. When a `Command:` line finishes, the next action in the same turn is the next `Command:` line, or the WC-5 steps after the last one.
- **WC-15. Context-safe reading and handoff files.** The worker reads files of unknown size and prior reports, logs and transcripts in pieces of at most 80 lines and never rereads a whole prior report. After each `Command:` line, whatever its outcome, the worker session writes `<report-dir>/handoff/<n>-<command>.md` (at most 40 lines: the command line, the Task ID and Dispatch ID, `worker_status`, deliverable paths, decisions, applied message IDs, the next `Command:` line) and lists it in `artifacts`.
- **Heartbeats.** The worker session sends heartbeats at the cadence its preamble sets, using the preamble's own command; it sends none while blocked in `ask` or `check --wait`, and a subagent never sends one (WC-7). Each heartbeat carries a progress token, in the heartbeat's subject or phase text, or a `status` body line: the current `Command:` line index and a count that rises only when on-disk progress rises (WC-15), plus `expect_silence_min` before a step expected to outlast the cadence. A heartbeat whose token has not changed is evidence that the process exists, not that the work is progressing. Command steps keep each blocking wait short enough for this (WC-10).

## 4. Coordinator rules

These bind the coordinator: an Orca coordinator session the person opened. It plans, creates Tasks, starts workers, reads their reports and performs every outward action.

### WC-6. Every retry is a new Task

A Task's brief cannot change after creation (Orca's `task-update` changes only `--status` and `--result`), and a re-run into the first attempt's directories could mix its files with the retry's. So the coordinator never uses `worker-start --retry-of`: every retry, whether or not its command line changes (an answer after a blocked gate, a resume input from the command's Resume rule), is a new Task created with `task-create --spec`, with its own report directory, recording the old Task ID.

- This is new work, not a way around the circuit breaker, so a command line that is unchanged apart from its report-directory value is never re-created after three failed starts; Orca counts failures only per Task, so the coordinator makes this comparison itself.
- No retry while the earlier attempt is not settled or reads `unverifiable`: absence never authorizes a retry.
- A crashed or stalled attempt is settled by the coordinator: after Orca's positive stall proof it stops the worker and sets the old Task `failed --result cancelled` before creating the new Task.
- A follow-up `send --to dispatch:<id>` is not used to carry a retry's new brief: the Dispatch ID is known only after `worker-start` returns ready, by which time a Claude worker has already received its task on the command line, so the message could arrive after the command started.
- A live attempt (its terminal still open) settles only when the person directs its cancellation and the coordinator has confirmed quiescence: no tool running, no input accepted, and two reads 5 minutes apart that agree. Context exhaustion, heartbeats and the coordinator's own nudges are not stall proofs. A message from a settled or replaced attempt is logged and shown to the person, never applied.

### What the coordinator owes each worker

The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states:

- the exact command line, including `--unattended` where the command accepts it at this phase, and every flag the command's brief rule lists as required, written as a `Command:` line in the layout below;
- the report directory, unique to this Task, so the contract path is known before dispatch (WC-4, WC-11);
- the blocked-gate policy line, `On a blocked gate: report blocked` or `On a blocked gate: ask the coordinator` (WC-3);
- whether the end-of-Task local commit is authorized, quoting the user's instruction word for word (decision D4);
- that no other outward action can be authorized;
- the worktree placement: the shared feature worktree, or a child worktree created by Orca with `worker-start --worktree new-child --base-branch <feature branch>` when WC-11 requires one, with `--setup skip` unless "Feature worktree and child worktrees" allows setup.

After `worker_done`, the coordinator opens the contract, then releases or reuses the worker.

### Liveness supervision

These are the v1 liveness rules. Every time and cap below is a starting value, not a measured one: the coordinator keeps the values it uses in its run notes, a brief may override them, and a worker may not.

**The wait.** The coordinator waits with every type listed:

`orca orchestration check --wait --types status,dispatch,worker_done,merge_ready,escalation,handoff,decision_gate,question,heartbeat --timeout-ms 300000`

- `--types` only decides when a waiter wakes. A returned Delivery is the whole FIFO batch, replayed until `--ack`, and shared by every wait on one Run inbox.
- The coordinator handles every message in the batch and writes one run-notes line per message ID before it sends `--ack`. If the notes write fails, the batch is not acked.
- An unknown type puts its sender in S11 and is shown to the person, never silently acked.
- `worker_done`, `question`, `escalation`, `handoff` and `merge_ready` are checked against the sender's current Task ID and Dispatch ID; a mismatch is quarantined: logged and shown to the person, never applied.
- After three empty waits in a row, the coordinator enumerates its workers with `worker-list`.
- Per type: `heartbeat` updates the worker's heartbeat record and is never a stall proof; a `status` carrying an ack line goes to the ack rules below, one naming a report path or saying the work is complete sets S9 when the brief has no later `Command:` line and is otherwise logged, any other is logged; `worker_done` opens the contract, and a second one for the same dispatch is logged and ignored; a `question` is answered with `reply --id` or forwarded to the person, and starts the ack clock; an `escalation` gets L1, then L5; a `decision_gate` goes to the person; a `handoff` leaves any new work to the coordinator's decision (WC-13); a `merge_ready` merges only on the person's instruction; a `dispatch` is logged as unexpected. The coordinator never sends or synthesizes `worker_done` for a worker.

**The sweep.** After every wake or timeout, at most once every 5 minutes, the coordinator runs one sweep: one `worker-list`, one prompt-wait listing (`worktree ps --agent-wait`) and one `stat` per worker contract path (WC-11), updating each worker's heartbeat record (arrival time, progress token, declared window). Costly probes (transcript tail, screen read) run only for workers a trigger fired for in this sweep.

- Deadline W is `max(10 min, 2 x the observed median heartbeat interval)`, or the worker's declared `expect_silence_min`, capped at 45 minutes.
- A semantic change is a substantive change of the progress token, the contract file or the transcript content. A message arrival or a repeated identical read is not one.
- Starting values: startup grace 10 minutes; a read-only probe after 10 minutes with no semantic change; a named state or an L5 report by 15 minutes after the last semantic change; an unreachable report after 10 minutes of continuous `unverifiable`.

| State | Trigger | Response |
|---|---|---|
| S0 starting | No progress token or transcript 10 minutes after start | L1, then L2 "begin your brief", then L5 by 15 minutes |
| S1 progressing | Token changed within W and a semantic change within 10 minutes | L0 |
| S2 long step | A declared window, or transcript activity under 5 minutes old | L1 at 10 minutes even inside the window (the window defers only nudges and typed text); past the window, L1, L3, then L5 by 15 minutes |
| S3 idle at prompt | No token change for W, and all of: the last transcript entry is 5 minutes old or older with no `worker_done` in the final turn; the screen shows an empty prompt with no tool running; no pending ask | L1, L2, L3; L4 only with a stall proof; a third idle episode goes to L5 |
| S4 blocked on a person prompt | `agentWait` is non-null | Capture the screen; L5 at 5 minutes plus Orca's own delay, re-reported every 15 minutes; never answer the prompt |
| S5 blocked in ask | An open `question` | Answer it, then the ack timeline |
| S6 context exhausted | Token unchanged for W while heartbeats arrive, or the S3 trigger fires; in both cases screen text such as `Autocompact is thrashing` confirmed by a second read 5 minutes later | Interrupt with "write your handoff file now, then end your turn" (the WC-14 exception); if the turn ends without `worker_done`, L4 within the budget, otherwise L5 and ask the person for a recorded stop |
| S7 unreachable | Liveness `unverifiable` | L5 after 10 minutes; never L4 |
| S8 exited | Liveness `exited` | Settle under WC-6, then L4 or L5 |
| S9 finished but unreported | Contract present, the brief has no `Command:` line after the step that wrote it, and no `worker_done` within one sweep | L1 (read the contract), then L2 "send `worker_done` per WC-5 with `--report-path <path>`", then L5 by 10 minutes after the nudge |
| S10 settled | `worker_done` received | None |
| S11 unknown | The deciding evidence is stale or unknown | L1, then as the resulting state; no typed input while S11 |

**Answers and acks.** The coordinator never resends a mailbox copy of an answer; the worker confirms each answer with an ack line (WC-12). The ack timeline, from the moment the answer is sent:

- A1, at 0: record the answer as pending_ack.
- A2, at 5 minutes with no ack and no heartbeat showing the ask returned: L1 probe of `agentWait`, the transcript tail and the screen.
- A3, at 5 minutes, only when the probe positively shows an idle, empty prompt: type ONE copy into the terminal with `orca terminal send --text "<copy>" --enter --wait-submit <s>`, at most one per message ID.
- A4, at 15 minutes: L5 report to the person with the message ID, the answer, the receipt fields and the probe results.
- Input veto: never interrupt; never type into a busy, S11 or S4 session; never answer a person prompt. Without a positive idle identification, skip to A4. A worker with no terminal skips A3.
- A duplicate ack is a no-op. An ack does not prove the answer was right: the outcome is still read from the contract after `worker_done`. At settlement, a pending ack closes as `unacked-at-settlement`.

The typed copy is one line:

```text
[coordinator] Answer to your message <message_id> (reply <R-task-n>): <answer>. If you already applied <message_id>, only send: ack <message_id> applied (duplicate). Otherwise send the ack first, then continue.
```

**The ladder.** A lineage is the original Task plus every replacement; caps count per lineage.

| Rung | Action | When | Cap |
|---|---|---|---|
| L0 observe | Watch only | Always | None |
| L1 probe | Read-only: `worker-show`, `worker-read --source transcript`, a screen read, the contract `stat` | A trigger fired | Every sweep; at most 2 costly probes per triggered worker per sweep |
| L2 nudge | Typed with `--wait-submit`; the S6 variant is an interrupt plus a handoff request | L1 confirms S3, S9 or S6 at an identified prompt | 1 per incident, 2 per lineage; a nudge with no turn start still counts |
| L3 ask | Typed: "Reply with `status`: current step, what you are waiting for" | L2 failed once and the state is still ambiguous | 1 per incident |
| L4 restart with resume note | Reconcile, stop the worker, settle it, set the old Task `failed --result cancelled`, create a new Task | Only with an Orca stall proof, or a person-directed cancellation with confirmed quiescence (WC-6), and only within the restart budget | 1 per rolling 60 minutes, 2 per lineage; WC-6's three-failed-starts rule also applies, whichever is stricter |
| L5 report to the person | Report the state, its evidence and what was tried | Any person-only state, or any cap reached | S4 is re-reported every 15 minutes |

When the ladder is exhausted, the coordinator reports to the person (L5). It restarts a worker (L4) only on one of Orca's positive stall proofs (`exited`, the process exit, or a transcript whose final agent turn sent no `worker_done`), or on the person's recorded stop, and then settles it under WC-6. Nudges, asks, heartbeats, repeated identical reads and context exhaustion are never stall proofs.

- Restart budget: per lineage, 1 restart per rolling 60 minutes and 2 in total. The cause classes are `idle`, `context-exhausted`, `exited` and `unreachable-then-exited`; the same class twice means no plain restart. For `context-exhausted`, the next Task reduces the load (splits the `Command:` lines or narrows the inputs), or the coordinator goes to L5.

The nudge, typed with `--wait-submit` and its receipt logged:

```text
[coordinator liveness check <UTC time>] If a step is running, ignore this and continue. If your turn ended before worker_done, continue with your next Command: line now. If all Command: lines are done, send worker_done per WC-5. Do not restart finished steps.
```

**The resume note.** An L4 restart puts this note in the new Task's brief, after the guard line and before the `Command:` lines. The new Task gets its own report directory; the old one is read-only input. For `/sc:implement`, its own `E-RESUME-NEEDED` re-run takes priority.

```text
Resume: replaces Task <old task id> (cause: <class>, evidence: <source>@<time>).
Lineage: <lineage id>, attempt <n>.
Task ID / Dispatch ID of the replaced attempt: <ids>.
Completed Command: lines: <n of m>, contracts: <paths>.
Last progress token: <step>/<counter>.
Handoff file: <old report-dir>/handoff/<latest>.md (read this first, at most 80 lines at a time).
Answered message IDs already applied: <ids>.
Uncertain effects: <actions started but not confirmed, e.g. a push or a message send>; verify before redoing.
Load rule: read reports and logs in pieces of at most 80 lines; do not reread whole prior reports.
Start at: Command: line <k>.
```

**Never on silence.** On silence, a passed deadline, `unverifiable` liveness or screen text alone, the coordinator never:

- stops a worker;
- creates a retry Task;
- releases a worker or a worktree;
- marks a Task failed;
- answers a permission or person-only prompt;
- writes or drafts a Ruling;
- sends a lifecycle message for the worker.

Silence authorizes only L1, L2 and L3.

**Not yet verified.** These points are open; the rules above do not depend on them being true:

- UNVERIFIED: what `check --wait` wakes on when `--types` is not given. The coordinator always lists every type.
- UNVERIFIED: the cause of case 5, answers a worker did not see. Lead: `orca orchestration reply` stores type `status` with subject "Re: Question", so a waiter with a narrow `--types` list may miss it.
- UNVERIFIED: whether Orca has an attention category for a permission prompt or for compact thrashing; until it is confirmed, S4 rests on `agentWait` and S6 on screen text read twice. The delay Orca adds before `agentWait` shows a prompt is also unmeasured.
- UNVERIFIED: what Claude Code does with text typed while a tool call runs; this is why typed text goes only to a positively idle prompt.
- UNVERIFIED: whether two consumers on one mailbox both get a batch; the coordinator runs one wait per Run inbox.

### Brief layout

The brief puts the preamble-facing instructions and the guard line before the commands, and gives each command its own labelled `Command:` line in run order (for example `Command: /sc:load ...`, then the converted command), so the Task text never starts with `/sc:`. Guard line:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
```

Chain line, right after the guard line and before the first `Command:` line (C-8):

```text
Chain: run every Command: line in one turn without stopping between them (WC-14); write a handoff file after each (WC-15); send ack lines for coordinator answers (WC-12).
```

Whether a `Command:` line carries `--unattended` is decided by the preflight below.

### Before the first task-create for a command

Before it creates the first Task for a command, the coordinator decides by the two-copy test whether that command's `Command:` line carries `--unattended` and a report directory. The test is the brief guard's own test, run by the coordinator on the copies the worker will see, never on the coordinator's own copy. It runs once per command per run, before the first `task-create` that names the command (a Task spec cannot be edited afterwards, so a wrong line costs a refused Task and a new one under WC-6), and again after any change to that command's file or to an installed copy (a sync of the development copies, or a new `superclaude install`).

1. Read, as plain files, the target worktree's `.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md`. A copy that does not exist is skipped.
2. In each existing copy, look for a line that is exactly `## Unattended mode`.
3. Every existing copy has the section: the `Command:` line carries `--unattended` and exactly one report directory (section 5).
4. The existing copies disagree: create no Task for that command until the stale copy is refreshed, normally `~/.claude`, which the person refreshes with `superclaude install`. The worker's guard would refuse the Task as "copies disagree".
5. No existing copy has the section: the `Command:` line carries no flag, and the brief says so. A run of that command that needs a person at a gate is a person-in-the-loop run, not a worker.

A WC-3 re-invocation keeps every token of the `Command:` line and only adds the answer, so it never re-decides the flag.

### Feature worktree and child worktrees

- Every worktree is created by Orca at Orca's default location, never with raw `git worktree add` and never under `.dev/worktrees/`. Each feature has one feature worktree on its feature branch, where the coordinator runs.
- The coordinator creates a child with `--setup skip`, because Orca's `worker-start` otherwise defaults a new worktree to `--setup run`, which runs the repository's own setup hooks, or with `--setup run` only when the user's instruction, in the coordinator's own conversation, names that step; after creation it runs `make sync-dev` or any other Makefile target, script or hook that the repository defines only when that instruction names that step, and in both cases it confirms with the person at the moment of action unless that instruction is in its live conversation. This holds in every repository, IronClaude included: an `origin` check proves which repository a checkout is, not that its checked-out branch is trusted. A child is dispatched only after its setup has succeeded.
- The coordinator keeps a placement map (which Task writes in which worktree, and whether it is the sole writer) in its run notes and in each `worker-start --comment`.
- A Task placed in a child gets an absolute report directory inside that child, which the coordinator reads by absolute path before merge-back; concurrent `/sc:implement` runs in different worktrees use distinct plan slugs. A resume runs in its existing child, selected with `--worktree id:<worktree id>`.
- After a child's result is admitted, the coordinator merges the child branch into the feature branch, then removes the child with `orca worktree rm` and deletes its branch; a discarded experiment is removed without merging; a merge conflict is stopped and reported, never resolved automatically.
- It never removes a worktree or branch that holds unmerged commits, an open PR, uncommitted changes, an unfinished `/sc:implement` ledger, or a report it has not read, without the user's instruction. It never runs one managed package in two worktrees at once.

### Git and GitHub ownership

- The coordinator performs every git and GitHub outward action, and every install, VM or paid run, in its own conversation, only when the user's instruction names that action, and confirms with the person at the moment of action unless that instruction is in its live conversation.
- Every such action targets `IronbellyOrg/IronClaude`: never the SuperClaude upstream, and never through Orca's issue or PR linking while Orca records the project as the upstream.
- Progress posts (issue comments, project fields) are such actions, made from contracts the coordinator has read; workers report progress only through heartbeats and `worker_done` (WC-5, WC-10).
- PRs go only through `/sc:pr-submit --monitor 3`, run in an ordinary top-level session as decision D3 states, never as a worker.
- Before any push that would publish worker commits the person has not seen, the coordinator shows them to the person and pushes only on the person's go; no earlier pre-authorization waives this. A commit grant covers one Task and ends at that Task's `worker_done`.
- The coordinator commits or merges in a worktree only when no worker runs there and no `/sc:implement` Task there is frozen (below). It compares `git status --porcelain` with the settled contracts and reports unlisted paths, stages explicit paths plus `.dev/tasks` at every commit and again at the end of the run, which satisfies the repo's always-staged rule for worker sessions, commits with `git commit --only -- <paths>`, treats "nothing to commit" as success, and stops and reports on any hook rewrite, hook failure or conflict, never `--no-verify`.
- The plan or brief records who owns each PR.

### Reading a result before anything depends on it

Orca settles a Task on any valid `worker_done` and does not start ready Tasks itself, so the coordinator decides what runs next:

- `succeeded`: dependents may start.
- `partial`: dependents do not start until the coordinator has read the contract's `report_path` and recorded, in its own run notes, whether the partial deliverable is usable; an unusable one is handled like `failed`.
- `failed` or `blocked`: dependents do not start; the coordinator retries per WC-6, answers per the worked example below, or reports the failure to the person. Exception: an `/sc:implement` Task follows "After an `/sc:implement` stop" below, because a WC-6 retry of a Ruling-halted plan would start an operator review by automation, which `/sc:implement` forbids (`~/.claude/skills/sc-implement-protocol/refs/qa.md`, "Closed list of interrupts").
- No contract, and a `worker_done --outcome failed` body that starts `guard refused:`: a brief-guard refusal; nothing ran. The coordinator fixes the brief in a new Task (WC-6), never re-creates it unchanged, and allows at most 2 brief fixes for the same work (3 attempts); a third refusal escalates to the person.
- Every dependent Task is created only after all its inputs have settled and been admitted under the bullets above, with `--deps` naming the Tasks that actually succeeded (an original Task or its replacement). No dependent is created up front on an unsettled input, because every retry is a new Task (WC-6), a dependent created on the old Task stays blocked, and Orca offers no way to re-point it.
- The coordinator starts only Tasks it created itself. A ready Task it did not create is not started; it is reported to the person with its spec text. In its run notes the coordinator also records each follow-up Task it created because a worker's result showed work that could not be planned before dispatch, with the extra time that cost. This is the evidence decision D5's revisit trigger reads.

### After an `/sc:implement` stop (decision D2)

1. *Freeze.* A plan is frozen when its latest implement contract is `blocked`, or `failed` with any STOP code other than `E-RESUME-NEEDED`. It is also frozen when the ledger's first non-complete task has `halt` or `blocked` as its last record with no eligible Ruling after it. While a plan is frozen:
   - The coordinator shows the person the contract and the full halt text, and dispatches no Task for that plan.
   - No Task that writes outside its own report directory is dispatched into the halted worktree.
   - No one runs a git command there that changes HEAD, the index or the working tree. The halted worktree is not merged or removed.

   `E-RESUME-NEEDED` alone may be re-run by the coordinator without the person, as the same command in the same worktree, and only when the ledger shows no freeze.
2. *Lifting the freeze.* The freeze lifts only when the person's explicit hand-back is recorded in the coordinator's run notes **and** the ledger shows the matching state:
   - "Ruling written" requires the check in item 3 to pass.
   - "session ended" (after the person ran `/sc:implement` in their own session) requires the halted task to be `complete` and the ledger's last line to parse. The drift baseline is then re-recorded.

   After a stop with no halted task (for example `E-ARCHIVE-BLOCKED`), only the person's recorded instruction lifts it. After the hand-back the person makes no further edit in that worktree until the resume Task settles.
3. *Check before a resume Task after "Ruling written".* The coordinator reads the ledger and the worktree, never edits either, and dispatches only if all of the following hold. On any failure it tells the person which condition failed and sends them to run `/sc:implement` in their own session.
   - (1) The worker has settled (WC-6).
   - (2) After the later of the halted task's latest `halt` and latest `blocked` record, the only new lines are one Ruling line per halted task named in the contract. Each line has that task's id, ends in `\n` with no `\r`, and matches the Ruling line regex in `~/.claude/skills/sc-implement-protocol/refs/ledger.md`.
   - (3) No field is blank, whitespace-only, punctuation-only or an angle-bracket placeholder, and the line has exactly two ` — ` separators.
   - (4) The line is eligible under either clause of the Ruling eligibility rule in `~/.claude/skills/sc-implement-protocol/refs/retry.md`.
   - (5) No `halt` after the task's latest `start` has `reason=dispute`; and the latest `halt` reason is not `no-evidence`, `no-snapshot` or `head-moved`.
   - (6) `HEAD` equals `<retries>/T<id>/q0-head`, and the paths in the `files=` field of the latest `blocked` line are unchanged against the tree its review graded. A missing `q0-head` or graded tree fails this condition.
   - (7) The resume brief has no `--force`.
4. *Placement.* The resume Task starts in the halted worktree by selector (`worker-start --worktree path:<absolute worktree path>`), never in a new or child worktree. When the person runs `/sc:implement` themselves, they run it from that same worktree with the same absolute plan path.

### Fan-in rule (several workers, then one merge)

For N input Tasks feeding one merge Task (for example N `/sc:troubleshoot` workers, then `/sc:adversarial --compare`): wait until all N have settled. Admit an input only if its `worker_status` is `succeeded`, or `partial` judged usable as above. Each `blocked` input is answered and re-run as a new Task (WC-6) before the merge, or dropped with the reason recorded; each `failed` input is retried or dropped the same way. The coordinator plans N no larger than the merge command's maximum of 10 inputs; a re-run replaces its input rather than adding one, so the admitted count never exceeds 10. Create the merge Task only when at least 2 inputs are admitted, and list every dropped input and its reason in its brief. With fewer than 2 there is no merge: the coordinator reports the single admitted result, or the failure, to the person.

### WC-16. Coordinator loop

The coordinator keeps watching its Run until every Task it created is settled and every result has been inspected and its admission or rejection recorded. It never stops watching on its own. When a wait on Orca expires, the coordinator re-arms it. On every coordinator wake or wait timeout, at most once every 5 minutes, the coordinator runs "The sweep." under `### Liveness supervision` unchanged and, in the same pass, runs `/sc:sweep` and reads its report before it acts. `/sc:sweep` is an added read: it does not replace that sweep, it is not a second pass, and it does not update heartbeat records or run the `worktree ps --agent-wait` listing. Its own reads are not L1 probes and do not count against the L1 cap; the coordinator's own L1 probes stay limited to workers a trigger fired for. The coordinator keeps that pass scheduled while work remains. Phase 1 adds this duty, not a scheduler. The `/sc:sweep` classes follow WC-10: only Orca's stall proofs make a worker stalled; anything else it cannot prove is could not determine. A missing heartbeat is absence, never death. The coordinator escalates to the person, and does not act alone, on: a failed or blocked result it cannot retry under WC-6, a partial result it judges unusable, a third brief-guard refusal, a ready Task it did not create, needing ownership review, a frozen plan, and a fan-in with fewer than 2 admitted inputs. Person-started sessions appear in the report, observed from transcripts and ccsession files; they are never messaged. The `/sc:sweep` report is a dated local file; it is never posted. `/sc:sweep` recommends nothing: no stop, retry, release, merge or removal. The coordinator decides and performs any action under those rules. The coordinator records each admission or rejection in its run notes; `/sc:sweep` does not observe them.

### Worked example: gate hit, answer, new Task

1. Task T1 brief, in the brief layout above: the guard line, `On a blocked gate: report blocked`, then `Command: /sc:tdd "auth" --unattended --output .dev/tdd/auth-1/tdd.md --report-dir .dev/tdd/auth-1/`.
2. The bare topic hits tdd's topic-only clarification gate. The command writes `.dev/tdd/auth-1/return-contract.yaml` with `worker_status: blocked` and `blocked_question` set to the gate's own question; the worker sends `worker_done --outcome failed --report-path .dev/tdd/auth-1/return-contract.yaml`.
3. The coordinator reads `blocked_question` and gets the answer (from its own plan, or from the person when the question is theirs to answer).
4. The coordinator creates Task T2 with `task-create --spec` and a brief in the same layout: the guard line, `replaces T1`, then `Command: /sc:tdd "token-based login service: session issue, refresh and revoke" --unattended --output .dev/tdd/auth-2/tdd.md --report-dir .dev/tdd/auth-2/`. T1's contract stays untouched in `auth-1/`.
5. T2 ends `succeeded`; anything that needed the TDD is created now, depending on T2.

## 5. Coordinator brief template

Copy this template into each Task's spec, one brief per Task, and fill every angle-bracket slot. The guard line is copied word for word and comes before the first `Command:` line.

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
Chain: run every Command: line in one turn without stopping between them (WC-14); write a handoff file after each (WC-15); send ack lines for coordinator answers (WC-12).
On a blocked gate: report blocked
Local commit: not authorized
Report directory: <directory unique to this Task>
Worktree: <shared feature worktree | child worktree created by Orca with worker-start --worktree new-child --base-branch <feature branch> --setup <skip | run (only when named in the user's instruction)>>
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:<name> <arguments> --unattended <report-directory-flag> <other flags this command's brief rule requires>
```

Slot rules:

- `On a blocked gate:` is `report blocked` (the default) or `ask the coordinator` (WC-3).
- `Local commit:` is `not authorized`, or `authorized` followed by the user's instruction naming a local commit for this Task, quoted word for word (WC-9, decision D4).
- Put `--unattended` and exactly one report directory on every `Command:` line, for each step and never as a session-wide setting, unless the two-copy test in "Before the first task-create for a command" (section 4) fails for that command. `<report-directory-flag>` in the template is the command's own directory flag where its row in the table below names one (for example `--output <dir>`), else `--report-dir <dir>`; the directory is unique to the Task. The default set is the 16 commands converted in P1 (adversarial, brainstorm, cleanup-audit, graph, impact, index-repo, init-lite, workflow, analyze, build, business-panel, design, document, explain, index, test) until a phase 2 live check passes.
- From P2 the 15 commands converted in P2 accept `--unattended` too, under the same guard test (auggie-review, cleanup, improve, cli-eval, cli-portify, recommend, research, review-translation, spec-panel, task, tasklist, reflect, release-split, tdd, troubleshoot). They join the default set only after a phase 2 live check passes; until then the coordinator puts the flag on one of them only when the user's instruction names that command.
- The flag changes what a command does, so the coordinator reads each report and never treats the flag as free: `/sc:improve` and `/sc:cleanup` skip every approval-required item and list it as not applied; `/sc:test` ends `succeeded` even when its suite fails (the verdict is in its report); `/sc:research` is forced to `--strategy planning`; `/sc:workflow` skips `--handoff implement`; every push, PR, comment and other outward action is off (WC-9).
- A command is started through its Skill call (WC-7); reading the command file and following it from memory does not satisfy WC-7. A person-in-the-loop run is not a worker: a run that needs a person at a gate belongs in the person's own session.

Flags the brief must pass, for the 12 commands that are ready with brief constraints. Under `--unattended` the brief passes exactly one report directory (`--report-dir <dir>`, or the command's own directory flag where the row names one); `/sc:index-repo` and `/sc:init-lite` have no directory flag of their own, so they take `--report-dir`. The table also lists the five P2 commands with a required brief flag (`/sc:auggie-review`, `/sc:cli-eval`, `/sc:cli-portify`, `/sc:review-translation`, `/sc:spec-panel`), so it has 17 rows.

| Command | Brief must pass |
|---|---|
| `/sc:adversarial` | `--output <dir>`; never `--interactive` |
| `/sc:auggie-review` | `--output-dir <dir>`; never `--post-pr` (or `--remediation-offer`) |
| `/sc:brainstorm` | `--output <dir>`; never `--interactive` |
| `/sc:cleanup-audit` | `--pass <N>` (single pass); `--report-dir <dir>` |
| `/sc:cli-eval` | `run` with `--suite <name>` and `--output-dir <dir>` (the eval run directory) plus `--report-dir <dir>`; other safety flags as wanted, else the CLI defaults |
| `/sc:cli-portify` | `--report-dir <dir>`; `--resume <contract>` to continue past an approval gate |
| `/sc:graph` | `status` (the default) with `--output-dir <dir>`; never `init`, which runs only when the user's own message starts with `/sc:graph init` |
| `/sc:impact` | `--output-dir <dir>` |
| `/sc:index-repo` | `--report-dir <dir>` |
| `/sc:init-lite` | `--output <file>` (names the report file); `--report-dir <dir>` |
| `/sc:reflect` | `--remediate` is allowed under `--unattended` (the headless rule answers it); `--no-promote` when the coordinator owns folder moves |
| `/sc:release-split` | spec-shaped input; default `--r1-scope`; never `--interactive`; its gates resolve as blocked under `--unattended` |
| `/sc:review-translation` | `--report-dir <dir>`; `--context <file>` once the context is confirmed |
| `/sc:spec-panel` | `--report-dir <dir>`; `--target-release <release>` for TDD inputs |
| `/sc:tdd` | a precise component prompt, not a bare topic; `--output <file>`; its gates resolve as blocked under `--unattended` |
| `/sc:troubleshoot` | no `--fix` under `--unattended` (the offer resolves as blocked); a short `--depth deep` input resolves as blocked |
| `/sc:workflow` | `--handoff none`; `--report-dir <dir>`; its `--output` is retired |
