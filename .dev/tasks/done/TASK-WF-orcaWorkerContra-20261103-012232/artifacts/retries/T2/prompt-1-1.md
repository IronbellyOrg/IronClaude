9abb9c846983facb19a5f9d616b7dfb96c42deb3
Review one task for spec compliance.

Task brief: ## Task 2: Add the coordinator rules and the brief template to `WORKER-CONTRACT.md`

Depends on: Task 1

Add the coordinator's rules to `src/superclaude/core/WORKER-CONTRACT.md` from `./source.md`:
- WC-6: every retry is a new Task, never `--retry-of`; the three-failed-starts comparison; settling a crashed or stalled attempt.
- Section 2.3 in full: what the brief states, including the P0-only item "the command's report file and the outcome rule AC-0.4 gives for it (WC-5)"; the brief layout with the exact guard line; feature and child worktrees (Orca default paths, the WC-11 triggers, the placement map, merge-back and removal rules); git and GitHub ownership (fork only, PRs only through `/sc:pr-submit --monitor 3`, review before pushing unseen worker commits, the coordinator stages `.dev/tasks` at every commit and at the end of the run); reading a result before anything depends on it (including the guard-refusal bullet and the rule that dependents are created only after their inputs settle); the `/sc:implement` stop rules (freeze, lifting the freeze, the seven-condition check before a resume Task, placement); and the fan-in rule, in the spec's words: the merge command's "maximum of 10 inputs", and a merge Task only when "at least 2 inputs are admitted".

Then add a coordinator brief template. It carries the guard line copied word for word from section 2.3 "Brief layout" before the first `Command:` line. It lists, per command, the "Brief must pass" flags of `./source.md` section 3.1 for the 12 ready commands: adversarial, brainstorm, cleanup-audit, graph, impact, index-repo, init-lite, reflect, release-split, tdd, troubleshoot and workflow. It marks `--report-dir` as "from P1", because no command accepts it at P0 (section 6, P1 row). It has a P0-only line for the report file and outcome rule of AC-0.4.

Append one phrase per rule added in this task to `./artifacts/t1-rule-phrases.md`, following the same rules as Task 1.

Acceptance criteria:
- `./artifacts/t1-rule-phrases.md` names at least one phrase for WC-6 and for each section 2.3 rule above, and each phrase is present in `WORKER-CONTRACT.md`.
- `WORKER-CONTRACT.md` states WC-6 and every section 2.3 rule named above, including the exact guard line text from section 2.3 "Brief layout" and the P0-only brief item.
- The brief template places the guard line before the first `Command:` line, names the section 3.1 flags for each of the 12 ready commands, marks `--report-dir` as "from P1", and has the P0-only report-file and outcome-rule line.
- The file mentions Orca commands only as the coordinator's and the worker session's channel, which `./source.md` SA-2 permits for this file.

AC ids, in the order of the Acceptance criteria bullets: T2.AC1, T2.AC2, T2.AC3, T2.AC4.
Package root (resolves ./artifacts/ and ./source.md): /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232
Global constraints: ## Constraints

- This is the static plan of Phase P0 (`./source.md` section 6, last paragraph: each phase's plan has a static part and a live part). It covers AC-0.1, AC-0.2, AC-0.3, AC-0.7 and AC-0.9 (section 7.3), and the common checks AC-C1, AC-C2, AC-C3, AC-C5 and AC-C6 (section 7.1). AC-C4 is checked on the index at the end of this plan and again by the coordinator at commit time. The live checks (AC-0.4, AC-0.5, AC-0.6) and the P0 phase report belong to the P0 live plan, which is written after this plan's checks pass. AC-0.8 is a P1 check (section 7.3). Phases P1-P4 get their own plans later; they are not dropped.
- No task in this plan commits, installs into `~/.claude`, starts an Orca worker or asks the owner a question. Between this plan and the live plan, the coordinator session asks the owner, commits and runs `uv run superclaude install --force`, as `./source.md` section 7.2 states, outside any plan run. `/sc:implement` may not prompt the user outside its halt paths (`./source.md` section 6, last paragraph).
- P0 edits no command file, no `SKILL.md` and no agent file (`./source.md` section 6, P0 row: "no command edits"). The only file this plan writes inside a skill package (`src/superclaude/skills/` or `plugins/superclaude/skills/`) is the byte-for-byte copy of `HOW-WE-WORK.md` at `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` that Task 4 makes. `tests/skills/test_worker_contract.py` is a test file, not a skill package. The `.claude/` copies that `make sync-dev` writes are sync output. No command gains `--unattended` or an `## Unattended mode` section in P0 (section 6, table "Which commands accept `--unattended`", P0 row: none).
- `WORKER-CONTRACT.md` restates only what `./source.md` sections 2.1, 2.2 and 2.3 say and adds no rule the spec lacks. The one exception is the brief template, which also carries the section 3.1 "Brief must pass" flags and the section 6 phase markers (`--report-dir` marked "from P1"). For the worker-session duties (WC-3, WC-5, WC-7, WC-12, WC-13 and heartbeats), the contract states only the IronClaude-specific rule and points to the dispatch preamble for Orca verb syntax and heartbeat cadence, never copying them (section 2.1, "Contract file"). These duties are not copied in full. Task 5 pins them by the short phrases that Tasks 1 and 2 record. This no-copy rule does not cover the coordinator's brief template, whose guard line and `worker_done` text are copied word for word from section 2.3 "Brief layout".
- `WORKER-CONTRACT.md` and the new `HOW-WE-WORK.md` section are installed files, so they use installed paths only (`~/.claude/...`). They copy none of the spec's evidence ids (`CAPS:`, `INV-`, `EVIDENCE.md:`) and no `src/superclaude/...` or other repo-path citations (repo `CLAUDE.md`, "Never Hardcode `src/superclaude/` Paths in Installed Primitives"). Where a rule needs to cite a skill file (for example `ledger.md:71` or `refs/retry.md:498` in the section 2.3 resume check), the citation is rewritten as an installed path, such as `~/.claude/skills/sc-implement-protocol/refs/ledger.md`.
- `src/superclaude/` is the source of truth. After editing it, run `make sync-dev`; never stage `.claude/` paths other than `.claude/settings.json` (repo `CLAUDE.md`, "Never Stage or Commit `.claude/` Contents"). `.dev/tasks/` is always staged (`git add .dev/tasks`); staging is not committing.
- No command, skill or agent file may name `orca` or `orca-ide` verbs (`./source.md` SA-2, AC-C1). Only `WORKER-CONTRACT.md` and `HOW-WE-WORK.md`, and their plugin copies, may describe the coordinator side.
- Every git and GitHub outward action targets `IronbellyOrg/IronClaude` only; SuperClaude upstream is never pushed to or interacted with (`./source.md` section 2.3, "Git and GitHub ownership"). This plan pushes nothing and opens no PR.
- Orca checks in this plan are read-only: no Orca command that starts, sends or creates anything is run.
- Use `uv run` for all Python.
Start sha: 9abb9c846983facb19a5f9d616b7dfb96c42deb3
Diff against the start snapshot: Files present in the start tree (diff against the start tree):
```diff
diff --git a/src/superclaude/core/WORKER-CONTRACT.md b/src/superclaude/core/WORKER-CONTRACT.md
index 1c5f7cfa..9350c622 100644
--- a/src/superclaude/core/WORKER-CONTRACT.md
+++ b/src/superclaude/core/WORKER-CONTRACT.md
@@ -59,3 +59,144 @@ These bind the top-level session that received the dispatch preamble. This secti
 - **WC-12. Coordinator follow-ups are pulled, not pushed.** The worker runs the preamble's `check` at natural checkpoints and once before `worker_done`; if `check` returns `consumer_fenced` it stops without sending `worker_done`. Commands need no change for this.
 - **WC-13. No Orca fan-out from the worker session.** The worker's top-level session never calls `worker-start`, `dispatch` or `task-create`, Orca's low-level dispatch, or `orca-cli` `worktree create --agent` or `agent launch`, at any depth setting. Work it finds that needs another worker is stated in its `worker_done` body; the coordinator decides (section 4).
 - **Heartbeats.** The worker session sends heartbeats at the cadence its preamble sets, using the preamble's own command; it sends none while blocked in `ask` or `check --wait`, and a subagent never sends one (WC-7). Command steps keep each blocking wait short enough for this (WC-10).
+
+## 4. Coordinator rules
+
+These bind the coordinator: an Orca coordinator session the person opened. It plans, creates Tasks, starts workers, reads their reports and performs every outward action.
+
+### WC-6. Every retry is a new Task
+
+A Task's brief cannot change after creation (Orca's `task-update` changes only `--status` and `--result`), and a re-run into the first attempt's directories could mix its files with the retry's. So the coordinator never uses `worker-start --retry-of`: every retry, whether or not its command line changes (an answer after a blocked gate, a resume input from the command's Resume rule), is a new Task created with `task-create --spec`, with its own report directory, recording the old Task ID.
+
+- This is new work, not a way around the circuit breaker, so a command line that is unchanged apart from its report-directory value is never re-created after three failed starts; Orca counts failures only per Task, so the coordinator makes this comparison itself.
+- No retry while the earlier attempt is not settled or reads `unverifiable`: absence never authorizes a retry.
+- A crashed or stalled attempt is settled by the coordinator: after Orca's positive stall proof it stops the worker and sets the old Task `failed --result cancelled` before creating the new Task.
+- A follow-up `send --to dispatch:<id>` is not used to carry a retry's new brief: the Dispatch ID is known only after `worker-start` returns ready, by which time a Claude worker has already received its task on the command line, so the message could arrive after the command started.
+
+### What the coordinator owes each worker
+
+The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states:
+
+- the exact command line, including `--unattended` where the command accepts it at this phase, and every flag the command's brief rule lists as required, written as a `Command:` line in the layout below;
+- the report directory, unique to this Task, so the contract path is known before dispatch (WC-4, WC-11);
+- the blocked-gate policy line, `On a blocked gate: report blocked` or `On a blocked gate: ask the coordinator` (WC-3);
+- whether the end-of-Task local commit is authorized, quoting the user's instruction word for word (decision D4);
+- at P0 only, the command's report file and the outcome rule AC-0.4 gives for it (WC-5);
+- that no other outward action can be authorized;
+- the worktree placement: the shared feature worktree, or a child worktree created by Orca with `worker-start --worktree new-child --base-branch <feature branch>` when WC-11 requires one.
+
+After `worker_done`, the coordinator opens the contract, then releases or reuses the worker.
+
+### Brief layout
+
+The brief puts the preamble-facing instructions and the guard line before the commands, and gives each command its own labelled `Command:` line in run order (for example `Command: /sc:load ...`, then the converted command), so the Task text never starts with `/sc:`. Guard line:
+
+```text
+Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
+```
+
+The coordinator decides whether a `Command:` line carries `--unattended` by the guard's own test, run on the copies the worker will see (the target worktree's project `.claude/commands/sc/` copy and `~/.claude/commands/sc/`), not on its own copy. A WC-3 re-invocation keeps every token of the `Command:` line and only adds the answer.
+
+### Feature worktree and child worktrees
+
+- Every worktree is created by Orca at Orca's default location, never with raw `git worktree add` and never under `.dev/worktrees/`. Each feature has one feature worktree on its feature branch, where the coordinator runs.
+- A child is dispatched only after its setup has succeeded (`--setup run`); if that setup does not run `make sync-dev`, the coordinator runs it before dispatch.
+- The coordinator keeps a placement map (which Task writes in which worktree, and whether it is the sole writer) in its run notes and in each `worker-start --comment`.
+- A Task placed in a child gets an absolute report directory inside that child, which the coordinator reads by absolute path before merge-back; concurrent `/sc:implement` runs in different worktrees use distinct plan slugs. A resume runs in its existing child, selected with `--worktree id:<worktree id>`.
+- After a child's result is admitted, the coordinator merges the child branch into the feature branch, then removes the child with `orca worktree rm` and deletes its branch; a discarded experiment is removed without merging; a merge conflict is stopped and reported, never resolved automatically.
+- It never removes a worktree or branch that holds unmerged commits, an open PR, uncommitted changes, an unfinished `/sc:implement` ledger, or a report it has not read, without the user's instruction. It never runs one managed package in two worktrees at once.
+
+### Git and GitHub ownership
+
+- The coordinator performs every git and GitHub outward action, and every install, VM or paid run, in its own conversation, only when the user's instruction names that action, and confirms with the person at the moment of action unless that instruction is in its live conversation.
+- Every such action targets `IronbellyOrg/IronClaude`: never the SuperClaude upstream, and never through Orca's issue or PR linking while Orca records the project as the upstream.
+- Progress posts (issue comments, project fields) are such actions, made from contracts the coordinator has read; workers report progress only through heartbeats and `worker_done` (WC-5, WC-10).
+- PRs go only through `/sc:pr-submit --monitor 3`, run in an ordinary top-level session as decision D3 states, never as a worker.
+- Before any push that would publish worker commits the person has not seen, the coordinator shows them to the person and pushes only on the person's go; no earlier pre-authorization waives this. A commit grant covers one Task and ends at that Task's `worker_done`.
+- The coordinator commits or merges in a worktree only when no worker runs there and no `/sc:implement` Task there is frozen (below). It compares `git status --porcelain` with the settled contracts and reports unlisted paths, stages explicit paths plus `.dev/tasks` at every commit and again at the end of the run, which satisfies the repo's always-staged rule for worker sessions, commits with `git commit --only -- <paths>`, treats "nothing to commit" as success, and stops and reports on any hook rewrite, hook failure or conflict, never `--no-verify`.
+- The plan or brief records who owns each PR.
+
+### Reading a result before anything depends on it
+
+Orca settles a Task on any valid `worker_done` and does not start ready Tasks itself, so the coordinator decides what runs next:
+
+- `succeeded`: dependents may start.
+- `partial`: dependents do not start until the coordinator has read the contract's `report_path` and recorded, in its own run notes, whether the partial deliverable is usable; an unusable one is handled like `failed`.
+- `failed` or `blocked`: dependents do not start; the coordinator retries per WC-6, answers per the worked example below, or reports the failure to the person. Exception: an `/sc:implement` Task follows "After an `/sc:implement` stop" below, because a WC-6 retry of a Ruling-halted plan would start an operator review by automation, which `/sc:implement` forbids (`~/.claude/skills/sc-implement-protocol/refs/qa.md`, "Closed list of interrupts").
+- No contract, and a `worker_done --outcome failed` body that starts `guard refused:`: a brief-guard refusal; nothing ran. The coordinator fixes the brief in a new Task (WC-6), never re-creates it unchanged, and allows at most 2 brief fixes for the same work (3 attempts); a third refusal escalates to the person.
+- Every dependent Task is created only after all its inputs have settled and been admitted under the bullets above, with `--deps` naming the Tasks that actually succeeded (an original Task or its replacement). No dependent is created up front on an unsettled input, because every retry is a new Task (WC-6), a dependent created on the old Task stays blocked, and Orca offers no way to re-point it.
+- The coordinator starts only Tasks it created itself. A ready Task it did not create is not started; it is reported to the person with its spec text. In its run notes the coordinator also records each follow-up Task it created because a worker's result showed work that could not be planned before dispatch, with the extra time that cost. This is the evidence decision D5's revisit trigger reads.
+
+### After an `/sc:implement` stop (decision D2)
+
+1. *Freeze.* A plan is frozen when its latest implement contract is `blocked`, or `failed` with any STOP code other than `E-RESUME-NEEDED`. It is also frozen when the ledger's first non-complete task has `halt` or `blocked` as its last record with no eligible Ruling after it. While a plan is frozen:
+   - The coordinator shows the person the contract and the full halt text, and dispatches no Task for that plan.
+   - No Task that writes outside its own report directory is dispatched into the halted worktree.
+   - No one runs a git command there that changes HEAD, the index or the working tree. The halted worktree is not merged or removed.
+
+   `E-RESUME-NEEDED` alone may be re-run by the coordinator without the person, as the same command in the same worktree, and only when the ledger shows no freeze.
+2. *Lifting the freeze.* The freeze lifts only when the person's explicit hand-back is recorded in the coordinator's run notes **and** the ledger shows the matching state:
+   - "Ruling written" requires the check in item 3 to pass.
+   - "session ended" (after the person ran `/sc:implement` in their own session) requires the halted task to be `complete` and the ledger's last line to parse. The drift baseline is then re-recorded.
+
+   After a stop with no halted task (for example `E-ARCHIVE-BLOCKED`), only the person's recorded instruction lifts it. After the hand-back the person makes no further edit in that worktree until the resume Task settles.
+3. *Check before a resume Task after "Ruling written".* The coordinator reads the ledger and the worktree, never edits either, and dispatches only if all of the following hold. On any failure it tells the person which condition failed and sends them to run `/sc:implement` in their own session.
+   - (1) The worker has settled (WC-6).
+   - (2) After the later of the halted task's latest `halt` and latest `blocked` record, the only new lines are one Ruling line per halted task named in the contract. Each line has that task's id, ends in `\n` with no `\r`, and matches the Ruling line regex in `~/.claude/skills/sc-implement-protocol/refs/ledger.md`.
+   - (3) No field is blank, whitespace-only, punctuation-only or an angle-bracket placeholder, and the line has exactly two ` — ` separators.
+   - (4) The line is eligible under either clause of the Ruling eligibility rule in `~/.claude/skills/sc-implement-protocol/refs/retry.md`.
+   - (5) No `halt` after the task's latest `start` has `reason=dispute`; and the latest `halt` reason is not `no-evidence`, `no-snapshot` or `head-moved`.
+   - (6) `HEAD` equals `<retries>/T<id>/q0-head`, and the paths in the `files=` field of the latest `blocked` line are unchanged against the tree its review graded. A missing `q0-head` or graded tree fails this condition.
+   - (7) The resume brief has no `--force`.
+4. *Placement.* The resume Task starts in the halted worktree by selector (`worker-start --worktree path:<absolute worktree path>`), never in a new or child worktree. When the person runs `/sc:implement` themselves, they run it from that same worktree with the same absolute plan path.
+
+### Fan-in rule (several workers, then one merge)
+
+For N input Tasks feeding one merge Task (for example N `/sc:troubleshoot` workers, then `/sc:adversarial --compare`): wait until all N have settled. Admit an input only if its `worker_status` is `succeeded`, or `partial` judged usable as above. Each `blocked` input is answered and re-run as a new Task (WC-6) before the merge, or dropped with the reason recorded; each `failed` input is retried or dropped the same way. The coordinator plans N no larger than the merge command's maximum of 10 inputs; a re-run replaces its input rather than adding one, so the admitted count never exceeds 10. Create the merge Task only when at least 2 inputs are admitted, and list every dropped input and its reason in its brief. With fewer than 2 there is no merge: the coordinator reports the single admitted result, or the failure, to the person.
+
+### Worked example: gate hit, answer, new Task
+
+1. Task T1 brief, in the brief layout above: the guard line, `On a blocked gate: report blocked`, then `Command: /sc:tdd "auth" --unattended --output .dev/tdd/auth-1/tdd.md --report-dir .dev/tdd/auth-1/`.
+2. The bare topic hits tdd's topic-only clarification gate. The command writes `.dev/tdd/auth-1/return-contract.yaml` with `worker_status: blocked` and `blocked_question` set to the gate's own question; the worker sends `worker_done --outcome failed --report-path .dev/tdd/auth-1/return-contract.yaml`.
+3. The coordinator reads `blocked_question` and gets the answer (from its own plan, or from the person when the question is theirs to answer).
+4. The coordinator creates Task T2 with `task-create --spec` and a brief in the same layout: the guard line, `replaces T1`, then `Command: /sc:tdd "token-based login service: session issue, refresh and revoke" --unattended --output .dev/tdd/auth-2/tdd.md --report-dir .dev/tdd/auth-2/`. T1's contract stays untouched in `auth-1/`.
+5. T2 ends `succeeded`; anything that needed the TDD is created now, depending on T2.
+
+## 5. Coordinator brief template
+
+Copy this template into each Task's spec, one brief per Task, and fill every angle-bracket slot. The guard line is copied word for word and comes before the first `Command:` line.
+
+```text
+Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
+On a blocked gate: report blocked
+Local commit: not authorized
+Report directory: <directory unique to this Task>
+Worktree: <shared feature worktree | child worktree created by Orca with worker-start --worktree new-child --base-branch <feature branch>>
+Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
+P0 only: Report file: <the command's report file under AC-0.4>. Outcome rule: --outcome failed when the file is missing or empty, or its status is failed or blocked; otherwise --outcome succeeded. This rule replaces the WC-5 mapping for this Task.
+Command: /sc:<name> <arguments> <flags this command's brief rule requires>
+```
+
+Slot rules:
+
+- `On a blocked gate:` is `report blocked` (the default) or `ask the coordinator` (WC-3).
+- `Local commit:` is `not authorized`, or `authorized` followed by the user's instruction naming a local commit for this Task, quoted word for word (WC-9, decision D4).
+- `--unattended` goes on a `Command:` line only when the guard's test shows that every copy of that command file the worker will see has an `## Unattended mode` section. At P0 no command accepts it.
+- The `P0 only:` line is used only before P1, when no command writes a worker contract. At P0 the report files are: troubleshoot, `<dir>/REPORT.md` with the status in its `**Status**:` line; workflow, the `return-contract.yaml` in the one new `TASK-WF-*` package directory the run creates under `.dev/tasks/to-do/`, with the status in its top-level `status`; adversarial, `<dir>/adversarial/merge-log.md` with the status in the `Status:` line of its `## Metadata` section. From P1 the line is dropped and WC-5 applies.
+
+Flags the brief must pass, for the 12 commands that are ready with brief constraints. `--report-dir` is marked "from P1": no command accepts it at P0.
+
+| Command | Brief must pass |
+|---|---|
+| `/sc:adversarial` | `--output <dir>`; never `--interactive` |
+| `/sc:brainstorm` | `--output <dir>`; never `--interactive` |
+| `/sc:cleanup-audit` | `--pass <N>` (single pass); `--report-dir <dir>` (from P1) |
+| `/sc:graph` | `status` (the default) with `--output-dir <dir>`; never `init`, which runs only when the user's own message starts with `/sc:graph init` |
+| `/sc:impact` | `--output-dir <dir>` |
+| `/sc:index-repo` | none |
+| `/sc:init-lite` | `--output <file>` |
+| `/sc:reflect` | no `--remediate`; `--no-promote` when the coordinator owns folder moves |
+| `/sc:release-split` | spec-shaped input; default `--r1-scope`; never `--interactive` |
+| `/sc:tdd` | a precise component prompt, not a bare topic; `--output <file>` |
+| `/sc:troubleshoot` | no `--fix` (and no `--depth deep` until P2) |
+| `/sc:workflow` | `--handoff none`; `--report-dir <dir>` (from P1); its `--output` is retired |
diff --git a/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t1-rule-phrases.md b/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t1-rule-phrases.md
index 98c25d25..d1eb0a41 100644
--- a/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t1-rule-phrases.md
+++ b/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t1-rule-phrases.md
@@ -55,3 +55,37 @@ WC-13 :: No Orca fan-out from the worker session
 heartbeats :: The worker session sends heartbeats at the cadence its preamble sets
 heartbeats :: the dispatch preamble is the authority for the Orca verb syntax and for the heartbeat cadence
 ```
+
+## Task 2: coordinator rules (spec WC-6 and section 2.3)
+
+```text
+WC-6 :: WC-6. Every retry is a new Task
+WC-6 :: the coordinator never uses `worker-start --retry-of`
+WC-6-three-failed-starts :: is never re-created after three failed starts
+WC-6-settle :: A crashed or stalled attempt is settled by the coordinator
+brief-contents :: The contract only works if the brief carries what the command would otherwise ask a person
+brief-P0-item :: at P0 only, the command's report file and the outcome rule AC-0.4 gives for it (WC-5)
+brief-layout :: so the Task text never starts with `/sc:`
+guard-line :: Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
+worktrees-default-paths :: Every worktree is created by Orca at Orca's default location
+worktrees-WC-11-trigger :: a child worktree created by Orca with `worker-start --worktree new-child --base-branch <feature branch>` when WC-11 requires one
+worktrees-placement-map :: The coordinator keeps a placement map
+worktrees-merge-back :: the coordinator merges the child branch into the feature branch, then removes the child
+worktrees-removal :: It never removes a worktree or branch that holds unmerged commits
+git-fork-only :: Every such action targets `IronbellyOrg/IronClaude`
+git-prs :: PRs go only through `/sc:pr-submit --monitor 3`
+git-unseen-commits :: Before any push that would publish worker commits the person has not seen
+git-stage-dev-tasks :: stages explicit paths plus `.dev/tasks` at every commit and again at the end of the run
+read-before-depend :: Reading a result before anything depends on it
+read-guard-refusal :: a brief-guard refusal; nothing ran
+dependents-after-settle :: Every dependent Task is created only after all its inputs have settled
+implement-freeze :: *Freeze.* A plan is frozen when
+implement-lift :: *Lifting the freeze.* The freeze lifts only when
+implement-check :: dispatches only if all of the following hold
+implement-placement :: *Placement.* The resume Task starts in the halted worktree by selector
+fan-in-max :: maximum of 10 inputs
+fan-in-min :: at least 2 inputs are admitted
+brief-template :: ## 5. Coordinator brief template
+brief-template-report-dir :: `--report-dir` is marked "from P1": no command accepts it at P0
+brief-template-P0-line :: P0 only: Report file: <the command's report file under AC-0.4>.
+```
```

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
