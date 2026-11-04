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
  - (case 1) every existing copy has an `## Unattended mode` section and the line lacks a standalone `--unattended`: `guard refused: brief lacks --unattended`;
  - (case 2) no existing copy has the section and the line has the flag: `guard refused: loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale)`;
  - the copies disagree: `guard refused: command copies disagree (stale copy): <paths>`;
  - (case 3) the command is on the never-as-worker list; the body still starts `guard refused:`.

  A command invoked by another command, through the Skill tool or the Agent tool, is never checked; the nested propagation rule governs it. The guard checks once, before the first run: a WC-3 re-invocation keeps every token of the brief's `Command:` line, `--unattended` included, and only adds the answer.
- **Never-as-worker list**: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers. These are never dispatched as workers and get no `--unattended` mode. The list changes only when the coordinator-only command set or D3 changes, never per phase. If D3 adds a worker route for pr-submit, D3 also states how that route passes the brief guard.
- **Nested propagation rule**: under `--unattended`, a command that invokes another `/sc:` command or protocol skill, through the Skill tool or the Agent tool, passes `--unattended` when the invoked command accepts it at this phase, together with its own report directory `<caller report-dir>/nested/<command>-<n>/` (WC-4, WC-11). The caller lists the nested contract in its `artifacts`; only the top-level contract drives WC-5. When the invoked command does not accept the flag yet, that step must be gate-free, or the caller skips it under `--unattended` and records the skip in its contract. Each command's `## Unattended mode` section names its nested invocations.

## 2. Command-side rules

These rules bind a command run with `--unattended`. Without the flag a command behaves exactly as it does for a person today.

- **WC-2. No person-blocking step in unattended mode.** Under `--unattended` the command never calls `AskUserQuestion`, never ends its turn on a chat question or `[yes / no]` offer, and never says STOP AND WAIT. Each gate resolves one of three ways, listed in the command's `## Unattended mode` section: (a) a documented default; (b) a value the caller supplied as a flag; (c) **blocked**: the command writes its contract with `worker_status: blocked` and the exact question in `blocked_question` (WC-4), and stops. What the worker does next is fixed by the brief (WC-3).
- **WC-4. One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<report-dir>/return-contract.yaml`, where `<report-dir>` is the one report directory the brief passes (section 1): either the command's own directory-valued `--output` / `--output-dir`, or `--report-dir`. The coordinator therefore knows the path before dispatch even when the command's own deliverable lands at a generated or fixed location (for example workflow's `TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>` package, cleanup-audit's `.claude-audit/`, implement's ledger, research's `claudedocs/research_[topic]_[timestamp].md`); the contract then points at that deliverable.
  - The worker fields are top-level keys: `worker_contract_version` (`"1"`), `worker_status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), `blocked_question` when blocked, and `reason` when failed (for `/sc:implement`, also when blocked, carrying the STOP code).
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
- **WC-10. Liveness during long waits.** The worker sends heartbeats at the cadence its preamble sets. A command step that blocks a single Bash call for longer than 4 minutes (a poll wait, a long eval) must be split into waits of at most 4 minutes so the session can heartbeat between them. A command's own Agent-tool fan-out (kept unchanged by WC-7) can hold the session longer than the cadence with no way to heartbeat; that gap is accepted, not required away, because commands may not call Orca and the subagents may not send lifecycle messages (WC-7). The coordinator therefore treats a missing heartbeat as absence, never as death: it never stops, retries or releases a worker because a heartbeat is late, and it acts only on Orca's stall proofs.
- **WC-11. Parallel-safe writes.** Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug the coordinator passes, and the coordinator gives every Task its own report directory; single-owner shared files (for example memory keys overwritten whole) are not written in unattended mode. Workers share the feature worktree only when they write nothing but their own report directory, which goes under `.dev/`. A worker gets its own child worktree (section 4) when its brief grants local commits; when it runs `/sc:implement` and any other writer (another worker, the coordinator, the person, a taken-over terminal or a hook) may write outside `.dev/` in the same worktree during the run; when it is a parallel experiment to compare or discard; or when its command writes the user index.

## 3. Worker-session duties

These bind the top-level session that received the dispatch preamble. This section states only the IronClaude-specific rule for each duty; the dispatch preamble is the authority for the Orca verb syntax and for the heartbeat cadence.

- **WC-3. Questions go to the coordinator, not to a local prompt.** The brief fixes the policy for a blocked gate; under `ask the coordinator` the worker applies the eligibility test below and makes no other choice.
  - With the brief line `On a blocked gate: report blocked` (the default when the brief says nothing), the worker lets the command write its blocked contract and sends `worker_done --outcome failed`.
  - With `On a blocked gate: ask the coordinator`, at a gate that fires before the command has written any output except its blocked contract and whose answer fits an existing argument or flag (any other gate is reported blocked as under the default), the worker session asks with the preamble's `ask` command, waits, then re-invokes the command in the same session with the answer as the command's argument or flag and the same report directory; the second run's contract replaces the blocked one whole.
  - The worker asks at most once per Task: if the re-invoked run blocks again, at the same gate or another, it does not ask again, keeps that second blocked contract and sends `worker_done --outcome failed`, and the coordinator continues with a new Task (WC-6).
  - A Ruling halt is never asked: an `/sc:implement` halt for a Ruling (`E-HALT-QA`, `E-NO-RULING`) is reported blocked whatever the policy line says, because a coordinator's reply is "another agent's message", which is not acceptance (`~/.claude/skills/sc-implement-protocol/refs/qa.md`, Halt table). The person gives the Ruling in their own session or writes the Ruling line into the ledger themselves after the worker has settled (decision D2). A Ruling line written or drafted by the coordinator or by any worker is "executor-invented approval".
  - On an `ask` timeout the worker resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. An answer that arrives after the worker has settled is carried by a new Task (WC-6).
- **WC-5. Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the contract's `worker_status` is `failed` or `blocked`, or no contract exists; `--outcome succeeded` when it is `succeeded` or `partial`, including an audit whose verdict is FAIL (the audit itself succeeded). The worker never reads the command's own `status` field for this; any other `worker_status` value is treated as `failed`. The first sentence of the body states `worker_status` and the verdict. If an authorized commit (WC-9) is refused or fails, the worker sends `--outcome failed`, and the body's first sentence reads `worker_status: succeeded; commit not made` followed by the reason. Before P1, when no command writes a contract, a brief that states the AC-0.4 report file and outcome rule replaces this mapping for that Task. The worker takes `--outcome` and `--report-path` from that rule. The body's first sentence then states the command's own status, or that its report file has none, instead of `worker_status`.
- **WC-7. Run at the top level, never inside a subagent.** The worker runs the command directly in its own session; it never wraps the command in an Agent-tool subagent. Lifecycle messages (heartbeat, ask, check, `worker_done`) are sent only by that top-level session, never by a subagent. A command's own Agent-tool fan-out stays as it is.
- **WC-12. Coordinator follow-ups are pulled, not pushed.** The worker runs the preamble's `check` at natural checkpoints and once before `worker_done`; if `check` returns `consumer_fenced` it stops without sending `worker_done`. Commands need no change for this.
- **WC-13. No Orca fan-out from the worker session.** The worker's top-level session never calls `worker-start`, `dispatch` or `task-create`, Orca's low-level dispatch, or `orca-cli` `worktree create --agent` or `agent launch`, at any depth setting. Work it finds that needs another worker is stated in its `worker_done` body; the coordinator decides (section 4).
- **Heartbeats.** The worker session sends heartbeats at the cadence its preamble sets, using the preamble's own command; it sends none while blocked in `ask` or `check --wait`, and a subagent never sends one (WC-7). Command steps keep each blocking wait short enough for this (WC-10).

## 4. Coordinator rules

These bind the coordinator: an Orca coordinator session the person opened. It plans, creates Tasks, starts workers, reads their reports and performs every outward action.

### WC-6. Every retry is a new Task

A Task's brief cannot change after creation (Orca's `task-update` changes only `--status` and `--result`), and a re-run into the first attempt's directories could mix its files with the retry's. So the coordinator never uses `worker-start --retry-of`: every retry, whether or not its command line changes (an answer after a blocked gate, a resume input from the command's Resume rule), is a new Task created with `task-create --spec`, with its own report directory, recording the old Task ID.

- This is new work, not a way around the circuit breaker, so a command line that is unchanged apart from its report-directory value is never re-created after three failed starts; Orca counts failures only per Task, so the coordinator makes this comparison itself.
- No retry while the earlier attempt is not settled or reads `unverifiable`: absence never authorizes a retry.
- A crashed or stalled attempt is settled by the coordinator: after Orca's positive stall proof it stops the worker and sets the old Task `failed --result cancelled` before creating the new Task.
- A follow-up `send --to dispatch:<id>` is not used to carry a retry's new brief: the Dispatch ID is known only after `worker-start` returns ready, by which time a Claude worker has already received its task on the command line, so the message could arrive after the command started.

### What the coordinator owes each worker

The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states:

- the exact command line, including `--unattended` where the command accepts it at this phase, and every flag the command's brief rule lists as required, written as a `Command:` line in the layout below;
- the report directory, unique to this Task, so the contract path is known before dispatch (WC-4, WC-11);
- the blocked-gate policy line, `On a blocked gate: report blocked` or `On a blocked gate: ask the coordinator` (WC-3);
- whether the end-of-Task local commit is authorized, quoting the user's instruction word for word (decision D4);
- at P0 only, the command's report file and the outcome rule AC-0.4 gives for it (WC-5);
- that no other outward action can be authorized;
- the worktree placement: the shared feature worktree, or a child worktree created by Orca with `worker-start --worktree new-child --base-branch <feature branch>` when WC-11 requires one, with `--setup skip` unless "Feature worktree and child worktrees" allows setup.

After `worker_done`, the coordinator opens the contract, then releases or reuses the worker.

### Brief layout

The brief puts the preamble-facing instructions and the guard line before the commands, and gives each command its own labelled `Command:` line in run order (for example `Command: /sc:load ...`, then the converted command), so the Task text never starts with `/sc:`. Guard line:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
```

The coordinator decides whether a `Command:` line carries `--unattended` by the guard's own test, run on the copies the worker will see (the target worktree's project `.claude/commands/sc/` copy and `~/.claude/commands/sc/`), not on its own copy. A WC-3 re-invocation keeps every token of the `Command:` line and only adds the answer.

### Feature worktree and child worktrees

- Every worktree is created by Orca at Orca's default location, never with raw `git worktree add` and never under `.dev/worktrees/`. Each feature has one feature worktree on its feature branch, where the coordinator runs.
- A child's setup depends on the repository. In an IronClaude checkout, where `git remote get-url origin` run in the coordinator's feature worktree prints exactly `https://github.com/IronbellyOrg/IronClaude` or `git@github.com:IronbellyOrg/IronClaude`, with or without a trailing `.git`, the coordinator creates the child with `--setup run` or `--setup skip`, and if the child's setup did not run `make sync-dev`, the coordinator runs it in the child; this trusts the Makefile and the Orca setup hooks on the feature branch. In any other repository, including a fork of IronClaude, a mirror or a checkout without `origin`, the coordinator creates the child with `--setup skip`, because Orca's `worker-start` otherwise defaults a new worktree to `--setup run`, which runs the repository's own setup hooks, or with `--setup run` only when the user's instruction, in the coordinator's own conversation, names that step; after creation it runs `make sync-dev` or any other Makefile target, script or hook that the repository defines only when that instruction names that step, and in both cases it confirms with the person at the moment of action unless that instruction is in its live conversation. A child is dispatched only after its setup has succeeded.
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
On a blocked gate: report blocked
Local commit: not authorized
Report directory: <directory unique to this Task>
Worktree: <shared feature worktree | child worktree created by Orca with worker-start --worktree new-child --base-branch <feature branch> --setup <skip | run (IronClaude checkout, or named in the user's instruction)>>
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
P0 only: Report file: <the command's report file under AC-0.4>. Outcome rule: --outcome failed when the file is missing or empty, or its status is failed or blocked; otherwise --outcome succeeded. This rule replaces the WC-5 mapping for this Task.
Command: /sc:<name> <arguments> <flags this command's brief rule requires>
```

Slot rules:

- `On a blocked gate:` is `report blocked` (the default) or `ask the coordinator` (WC-3).
- `Local commit:` is `not authorized`, or `authorized` followed by the user's instruction naming a local commit for this Task, quoted word for word (WC-9, decision D4).
- `--unattended` goes on a `Command:` line only when the guard's test shows that every copy of that command file the worker will see has an `## Unattended mode` section. At P0 no command accepts it.
- The `P0 only:` line is used only before P1, when no command writes a worker contract. At P0 the report files are: troubleshoot, `<dir>/REPORT.md` with the status in its `**Status**:` line; workflow, the `return-contract.yaml` in the one new `TASK-WF-*` package directory the run creates under `.dev/tasks/to-do/`, with the status in its top-level `status`; adversarial, `<dir>/adversarial/merge-log.md` with the status in the `Status:` line of its `## Metadata` section. From P1 the line is dropped and WC-5 applies.

Flags the brief must pass, for the 12 commands that are ready with brief constraints. `--report-dir` is marked "from P1": no command accepts it at P0.

| Command | Brief must pass |
|---|---|
| `/sc:adversarial` | `--output <dir>`; never `--interactive` |
| `/sc:brainstorm` | `--output <dir>`; never `--interactive` |
| `/sc:cleanup-audit` | `--pass <N>` (single pass); `--report-dir <dir>` (from P1) |
| `/sc:graph` | `status` (the default) with `--output-dir <dir>`; never `init`, which runs only when the user's own message starts with `/sc:graph init` |
| `/sc:impact` | `--output-dir <dir>` |
| `/sc:index-repo` | none |
| `/sc:init-lite` | `--output <file>` |
| `/sc:reflect` | no `--remediate`; `--no-promote` when the coordinator owns folder moves |
| `/sc:release-split` | spec-shaped input; default `--r1-scope`; never `--interactive` |
| `/sc:tdd` | a precise component prompt, not a bare topic; `--output <file>` |
| `/sc:troubleshoot` | no `--fix` (and no `--depth deep` until P2) |
| `/sc:workflow` | `--handoff none`; `--report-dir <dir>` (from P1); its `--output` is retired |
