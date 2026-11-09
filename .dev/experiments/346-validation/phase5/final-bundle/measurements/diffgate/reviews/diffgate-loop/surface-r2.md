# Diffgate surface: review 2 of 3

format: diffgate/1
coverage: 8% of lines changed

Review only the changed tokens below. Anchor each new finding with `hunk=<id>` on a changed
token, or `via=<id>` for an unchanged line a hunk breaks, or `cites=<prior id>`.

## Prior blocking findings

| id | label | at | finding |
|---|---|---|---|
| R1.1 | major | [62, 62] | WC-4 report location is unknowable or undefined for workflow, tdd, init-lite and a missing flag |
| R1.2 | major | [62, 62] | the new status field collides with existing contract status fields |
| R1.3 | major | [64, 64] | WC-6 fresh directory conflicts with the brief-fixed directory of WC-4 |
| R1.4 | major | [65, 65] | WC-7 does not require the Skill invocation and no check detects its absence |
| R1.5 | major | [172, 172] | AC-C1 scans the folder that holds the contract file SA-2 lets mention Orca |
| R1.6 | major | [195, 195] | load has no report but AC-1.1 requires one |
| R1.7 | major | [228, 228] | no parse rule for the --unattended token |

## Hunks

### H2.1 (section: 2.1 Terms; owners: R1.7)

New lines 51-51:
```text
   51: - **Unattended mode**: the behaviour a command switches to when its caller passes `--unattended`. It is the only command-side change the contract asks for besides report files and resume. It names no Orca command, so the same mode serves any caller that has no person at the keyboard. The mode is on only when `--unattended` is a standalone argument token outside any quoted argument; the same text inside a quoted topic or prompt (for example `/sc:troubleshoot "the worker ignores --unattended"`) is part of that argument and leaves the mode off, so a person's run cannot switch by accident (R1.7). How the mode is selected (flag versus detecting the preamble) is open decision D1 in section 9; this spec is written for the recommended flag.
```
Changed tokens: `The`@51 `mode`@51 `is`@51 `on`@51 `only`@51 `when`@51 ``--unattended``@51 `is`@51 `a`@51 `standalone`@51 `argument`@51 `token`@51 `outside`@51 `any`@51 `quoted`@51 `argument;`@51 `the`@51 `same`@51 `text`@51 `inside`@51 `a`@51 `quoted`@51 `topic`@51 `or`@51 `prompt`@51 `(for`@51 `example`@51 ``/sc:troubleshoot`@51 `"the`@51 `worker`@51 `ignores`@51 `--unattended"`)`@51 `is`@51 `part`@51 `of`@51 `that`@51 `argument`@51 `and`@51 `leaves`@51 `the`@51 `mode`@51 `off,`@51 `so`@51 `a`@51 `person's`@51 `run`@51 `cannot`@51 `switch`@51 `by`@51 `accident`@51 `(R1.7).`@51

### H2.2 (section: 2.2 Requirements; owners: R1.2,R1.1,R1.3,R1.4)

New lines 60-65:
```text
   60: | WC-2 | **No person-blocking step in unattended mode.** Under `--unattended` the command never calls `AskUserQuestion`, never ends its turn on a chat question or `[yes / no]` offer, and never says STOP AND WAIT. Each gate resolves one of three ways, listed per command in section 3: (a) a documented default; (b) a value the caller supplied as a flag; (c) **blocked**: the command writes its report with `worker_status: blocked` (R1.2) and the exact question, and stops. | Command | Gates per command at `INV-A:76-83`, `INV-B:292`; a worker waiting on a prompt is "healthy", so a stall is invisible (`CAPS:52`, `CAPS:129`); a plain chat offer also stalls (`INV-A:62`) |
   61: | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
   62: | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<report-dir>/return-contract.yaml`, where `<report-dir>` is the directory the brief passes with the new flag `--report-dir <dir>` (R1.1). `--report-dir` is separate from the command's own output flags, which keep their meaning (workflow's generated package, the file-valued `--output` of tdd and init-lite, adversarial's `<output>/adversarial/`), so the path is known before dispatch for every command. The command creates the directory if it is missing. If `--unattended` is given without `--report-dir`, the command does no work, writes nothing and stops with an error naming the missing flag; the worker then has no report, so WC-5 sends `--outcome failed` (R1.1). The file follows the return-contract pattern several commands already use and carries at least: `worker_status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written, including the command's own contract when it lies elsewhere), and, when blocked, `blocked_question`. The field is `worker_status`, not `status`, because existing contracts already use `status` with other values (R1.2). A command that already writes a contract keeps it and all its fields unchanged; when that contract's path is `<report-dir>/return-contract.yaml`, it adds the fields above as new top-level keys, otherwise it writes the WC-4 file separately. The command sets `worker_status` from its own result: `success` → `succeeded`; `partial` → `partial`; a WC-2 (c) gate stop → `blocked`; `failed` or any other stop value (for example reflect's `stopped-precondition`) → `failed` (R1.2). It is written on success, failure, blocked and partial outcomes, including stops before any other output exists (for workflow, the pre-creation STOPs that write no package contract, R1.1). The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97`; R1.1 output flags: `sk/sc-workflow-protocol/SKILL.md:24,44`, `sk/sc-workflow-protocol/refs/return-contract.md:39`, `cmd/tdd.md:49`, `cmd/init-lite.md:32`; R1.2 existing `status` values: `sk/sc-workflow-protocol/refs/return-contract.md:7`, `sk/sc-adversarial-protocol/SKILL.md:432,436`, `sk/sc-reflect-protocol/SKILL.md:250` |
   63: | WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the report's `worker_status` is `failed` or `blocked` (R1.2), or no report exists; `--outcome succeeded` otherwise, including `partial` and including an audit whose verdict is FAIL (the audit itself succeeded). The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
   64: | WC-6 | **Resume or safe re-run.** A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output. A command either resumes from its on-disk state when given its resume flag, or, if it has none, re-runs clean into new directories. The coordinator, not the command, chooses those directories: each attempt's brief, a `--retry-of` retry included, names a new `--report-dir` and, for a command without resume, a new output location, so the first attempt's files stay as they were and the report path is recorded before dispatch (R1.3). A WC-3 re-invocation inside one worker is the same attempt: it reuses that attempt's directories, and its report replaces the `blocked` report of the first invocation; the question itself stays recorded in the Run (`CAPS:58`) (R1.3). Section 3 names which applies per command. | Command (resume or clean re-run); coordinator (directories per attempt, R1.3) | `CAPS:116` (retry and circuit breaker); resume mechanisms in column (e) of `INV-A:35-55`, `INV-B:31-52` |
   65: | WC-7 | **Run at the top level, never inside a subagent.** The worker runs the command directly in its own session; it never wraps the command in an Agent-tool subagent. Lifecycle messages (`heartbeat`, `ask`, `check`, `worker_done`) are sent only by that top-level session, never by a subagent. A command's own Agent-tool fan-out stays as it is. When the command's file says to invoke a skill, the worker loads that skill with the Skill tool before any other step, as a person's `/sc:` message would; reading the command file and performing the protocol from memory does not satisfy WC-7, because the repo's Skill rule fires only on a message that starts with `/sc:`, which a preamble-wrapped brief never is (R1.4). | Worker session | `src/superclaude/core/CLAUDE.md:73` (Skill rule, R1.4); `sk/sc-pr-submit-protocol/SKILL.md:37-39` (top-level rule); `CAPS:159-161`; `INV-A:95` (nesting loses tools at Claude Code's depth limit) |
```
Changed tokens: ``worker_status:`@60 `(R1.2)`@60 ``<report-dir>/return-contract.yaml`,`@62 ``<report-dir>``@62 `brief`@62 `passes`@62 `with`@62 `the`@62 `new`@62 `flag`@62 ``--report-dir`@62 `<dir>``@62 `(R1.1).`@62 ``--report-dir``@62 `is`@62 `separate`@62 `from`@62 `the`@62 `command's`@62 `own`@62 `output`@62 `flags,`@62 `which`@62 `keep`@62 `their`@62 `meaning`@62 `(workflow's`@62 `generated`@62 `package,`@62 `the`@62 `file-valued`@62 ``--output``@62 `of`@62 `tdd`@62 `and`@62 `init-lite,`@62 `adversarial's`@62 ``<output>/adversarial/`),`@62 `so`@62 `the`@62 `path`@62 `is`@62 `known`@62 `before`@62 `dispatch`@62 `for`@62 `every`@62 `command.`@62 `The`@62 `command`@62 `creates`@62 `the`@62 `directory`@62 `if`@62 `it`@62 `is`@62 `missing.`@62 `If`@62 ``--unattended``@62 `is`@62 `given`@62 `without`@62 ``--report-dir`,`@62 `the`@62 `command`@62 `does`@62 `no`@62 `work,`@62 `writes`@62 `nothing`@62 `and`@62 `stops`@62 `with`@62 `an`@62 `error`@62 `naming`@62 `the`@62 `missing`@62 `flag;`@62 `the`@62 `worker`@62 `then`@62 `has`@62 `no`@62 `report,`@62 `so`@62 `WC-5`@62 `sends`@62 ``--outcome`@62 `failed``@62 `(R1.1).`@62 `The`@62 `file`@62 ``worker_status``@62 `written,`@62 `including`@62 `the`@62 `command's`@62 `own`@62 `contract`@62 `when`@62 `it`@62 `lies`@62 `elsewhere),`@62 `The`@62 `field`@62 `is`@62 ``worker_status`,`@62 `not`@62 ``status`,`@62 `because`@62 `existing`@62 `contracts`@62 `already`@62 `use`@62 ``status``@62 `with`@62 `other`@62 `values`@62 `(R1.2).`@62 `A`@62 `command`@62 `that`@62 `already`@62 `writes`@62 `a`@62 `contract`@62 `keeps`@62 `it`@62 `and`@62 `all`@62 `its`@62 `fields`@62 `unchanged;`@62 `when`@62 `that`@62 `contract's`@62 `path`@62 `is`@62 ``<report-dir>/return-contract.yaml`,`@62 `it`@62 `adds`@62 `the`@62 `fields`@62 `above`@62 `as`@62 `new`@62 `top-level`@62 `keys,`@62 `otherwise`@62 `it`@62 `writes`@62 `the`@62 `WC-4`@62 `file`@62 `separately.`@62 `The`@62 `command`@62 `sets`@62 ``worker_status``@62 `from`@62 `its`@62 `own`@62 `result:`@62 ``success``@62 `→`@62 ``succeeded`;`@62 ``partial``@62 `→`@62 ``partial`;`@62 `a`@62 `WC-2`@62 `(c)`@62 `gate`@62 `stop`@62 `→`@62 ``blocked`;`@62 ``failed``@62 `or`@62 `any`@62 `other`@62 `stop`@62 `value`@62 `(for`@62 `example`@62 `reflect's`@62 ``stopped-precondition`)`@62 `→`@62 ``failed``@62 `(R1.2).`@62 `exists`@62 `(for`@62 `workflow,`@62 `the`@62 `pre-creation`@62 `STOPs`@62 `no`@62 `package`@62 `contract,`@62 `R1.1).`@62 ``INV-A:97`;`@62 `R1.1`@62 `output`@62 `flags:`@62 ``sk/sc-workflow-protocol/SKILL.md:24,44`,`@62 ``sk/sc-workflow-protocol/refs/return-contract.md:39`,`@62 ``cmd/tdd.md:49`,`@62 ``cmd/init-lite.md:32`;`@62 `R1.2`@62 `existing`@62 ``status``@62 `values:`@62 ``sk/sc-workflow-protocol/refs/return-contract.md:7`,`@62 ``sk/sc-adversarial-protocol/SKILL.md:432,436`,`@62 ``sk/sc-reflect-protocol/SKILL.md:250``@62 `report's`@63 ``worker_status``@63 `is`@63 ``blocked``@63 `(R1.2),`@63 `re-runs`@64 `clean`@64 `into`@64 `new`@64 `directories.`@64 `The`@64 `coordinator,`@64 `not`@64 `the`@64 `command,`@64 `chooses`@64 `those`@64 `directories:`@64 `attempt's`@64 `brief,`@64 ``--retry-of``@64 `retry`@64 `included,`@64 `names`@64 `a`@64 `new`@64 ``--report-dir``@64 `and,`@64 `for`@64 `a`@64 `command`@64 `without`@64 `resume,`@64 `a`@64 `new`@64 `location,`@64 `the`@64 `first`@64 `attempt's`@64 `files`@64 `stay`@64 `as`@64 `they`@64 `were`@64 `and`@64 `the`@64 `report`@64 `path`@64 `is`@64 `recorded`@64 `before`@64 `dispatch`@64 `(R1.3).`@64 `A`@64 `WC-3`@64 `re-invocation`@64 `inside`@64 `one`@64 `worker`@64 `is`@64 `the`@64 `same`@64 `attempt:`@64 `it`@64 `reuses`@64 `that`@64 `attempt's`@64 `directories,`@64 `and`@64 `its`@64 `report`@64 `replaces`@64 `the`@64 ``blocked``@64 `report`@64 `of`@64 `the`@64 `first`@64 `invocation;`@64 `the`@64 `question`@64 `itself`@64 `stays`@64 `recorded`@64 `in`@64 `the`@64 `Run`@64 `(`CAPS:58`)`@64 `(R1.3).`@64 `(resume`@64 `or`@64 `clean`@64 `re-run);`@64 `coordinator`@64 `(directories`@64 `per`@64 `attempt,`@64 `R1.3)`@64 `When`@65 `the`@65 `command's`@65 `file`@65 `says`@65 `to`@65 `invoke`@65 `a`@65 `skill,`@65 `the`@65 `worker`@65 `loads`@65 `that`@65 `skill`@65 `with`@65 `the`@65 `Skill`@65 `tool`@65 `before`@65 `any`@65 `other`@65 `step,`@65 `as`@65 `a`@65 `person's`@65 ``/sc:``@65 `message`@65 `would;`@65 `reading`@65 `the`@65 `command`@65 `file`@65 `and`@65 `performing`@65 `the`@65 `protocol`@65 `from`@65 `memory`@65 `does`@65 `not`@65 `satisfy`@65 `WC-7,`@65 `because`@65 `the`@65 `repo's`@65 `Skill`@65 `rule`@65 `fires`@65 `only`@65 `on`@65 `a`@65 `message`@65 `that`@65 `starts`@65 `with`@65 ``/sc:`,`@65 `which`@65 `a`@65 `preamble-wrapped`@65 `brief`@65 `never`@65 `is`@65 `(R1.4).`@65 ``src/superclaude/core/CLAUDE.md:73``@65 `(Skill`@65 `rule,`@65 `R1.4);`@65
Removed from old lines 60-65 (anchor with `side=old`):
```text
   60: | WC-2 | **No person-blocking step in unattended mode.** Under `--unattended` the command never calls `AskUserQuestion`, never ends its turn on a chat question or `[yes / no]` offer, and never says STOP AND WAIT. Each gate resolves one of three ways, listed per command in section 3: (a) a documented default; (b) a value the caller supplied as a flag; (c) **blocked**: the command writes its report with `status: blocked` and the exact question, and stops. | Command | Gates per command at `INV-A:76-83`, `INV-B:292`; a worker waiting on a prompt is "healthy", so a stall is invisible (`CAPS:52`, `CAPS:129`); a plain chat offer also stalls (`INV-A:62`) |
   61: | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
   62: | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
   63: | WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise, including `partial` and including an audit whose verdict is FAIL (the audit itself succeeded). The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
   64: | WC-6 | **Resume or safe re-run.** A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output. A command either resumes from its on-disk state when given its resume flag, or, if it has none, writes each run into a fresh output directory so a re-run starts clean. Section 3 names which applies per command. | Command | `CAPS:116` (retry and circuit breaker); resume mechanisms in column (e) of `INV-A:35-55`, `INV-B:31-52` |
   65: | WC-7 | **Run at the top level, never inside a subagent.** The worker runs the command directly in its own session; it never wraps the command in an Agent-tool subagent. Lifecycle messages (`heartbeat`, `ask`, `check`, `worker_done`) are sent only by that top-level session, never by a subagent. A command's own Agent-tool fan-out stays as it is. | Worker session | `sk/sc-pr-submit-protocol/SKILL.md:37-39` (top-level rule); `CAPS:159-161`; `INV-A:95` (nesting loses tools at Claude Code's depth limit) |
```
Removed tokens: ``status:`@60 ``<output-dir>/return-contract.yaml`,`@62 ``<output-dir>``@62 `coordinator`@62 `passed`@62 `(`--output``@62 `/`@62 ``--output-dir`).`@62 `It`@62 ``status``@62 `written),`@62 `exists.`@62 `Commands`@62 `already`@62 `a`@62 `contract`@62 `keep`@62 `their`@62 `fields`@62 `and`@62 `add`@62 `the`@62 `missing`@62 `ones.`@62 ``INV-A:97``@62 `report`@63 `says`@63 ``blocked`,`@63 `writes`@64 `run`@64 `into`@64 `fresh`@64 `directory`@64 `a`@64 `re-run`@64 `starts`@64 `clean.`@64

### H2.3 (section: 2.3 What the coordinator owes each worker; owners: R1.1,R1.3)

New lines 73-73:
```text
   73: The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; a report directory passed as `--report-dir`, new for each attempt including retries, so the report path is known before dispatch, and for a command without resume a new output location per attempt as well (WC-4, WC-6; R1.1, R1.3); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```
Changed tokens: `a`@73 `report`@73 `directory`@73 `passed`@73 `as`@73 ``--report-dir`,`@73 `new`@73 `for`@73 `each`@73 `attempt`@73 `including`@73 `retries,`@73 `dispatch,`@73 `and`@73 `for`@73 `a`@73 `command`@73 `without`@73 `resume`@73 `a`@73 `new`@73 `output`@73 `location`@73 `per`@73 `attempt`@73 `as`@73 `well`@73 `(WC-4,`@73 `WC-6;`@73 `R1.1,`@73 `R1.3);`@73
Removed from old lines 73-73 (anchor with `side=old`):
```text
   73: The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```
Removed tokens: `the`@73 `output`@73 `directory,`@73 `dispatch`@73 `(WC-4);`@73

### H2.4 (section: 3. Per-command changes; owners: R1.1,R1.3)

New lines 76-76:
```text
   76: The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<report-dir>/return-contract.yaml`, written to the `--report-dir` every brief passes (R1.1). "Fresh dir" in a Resume column means the coordinator names a new output location in each attempt's brief (WC-6, R1.3). Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
```
Changed tokens: ``<report-dir>/return-contract.yaml`,`@76 `written`@76 `to`@76 `the`@76 ``--report-dir``@76 `every`@76 `brief`@76 `passes`@76 `(R1.1).`@76 `"Fresh`@76 `dir"`@76 `in`@76 `a`@76 `Resume`@76 `column`@76 `means`@76 `the`@76 `coordinator`@76 `names`@76 `a`@76 `new`@76 `output`@76 `location`@76 `in`@76 `each`@76 `attempt's`@76 `brief`@76 `(WC-6,`@76 `R1.3).`@76
Removed from old lines 76-76 (anchor with `side=old`):
```text
   76: The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
```
Removed tokens: ``<output-dir>/return-contract.yaml`.`@76

### H2.5 (section: 3.1 Ready today (10); owners: R1.1)

New lines 83-83:
```text
   83: | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix its own contract filename to `<output>/adversarial/return-contract.yaml`; the WC-4 report still goes to `--report-dir` (R1.1) (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
```
Changed tokens: `its`@83 `own`@83 ``<output>/adversarial/return-contract.yaml`;`@83 `the`@83 `WC-4`@83 `report`@83 `still`@83 `goes`@83 `to`@83 ``--report-dir``@83 `(R1.1)`@83
Removed from old lines 83-83 (anchor with `side=old`):
```text
   83: | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
```
Removed tokens: `the`@83 ``<output>/adversarial/return-contract.yaml``@83

### H2.6 (section: 3.1 Ready today (10); owners: R1.1)

New lines 92-92:
```text
   92: | workflow | `--handoff none`; never `--output` (retired, `E-LEGACY`, R1.1) | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Under `--unattended`, write the WC-4 report to `--report-dir` on every outcome, including the pre-creation STOPs that write no package contract (R1.1) (P1) | `sk/sc-workflow-protocol/SKILL.md:24,58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
```
Changed tokens: `none`;`@92 `never`@92 ``--output``@92 `(retired,`@92 ``E-LEGACY`,`@92 `R1.1)`@92 `Under`@92 ``--unattended`,`@92 `write`@92 `WC-4`@92 `report`@92 `to`@92 ``--report-dir``@92 `on`@92 `every`@92 `outcome,`@92 `including`@92 `the`@92 `that`@92 `write`@92 `no`@92 `package`@92 `contract`@92 `(R1.1)`@92 ``sk/sc-workflow-protocol/SKILL.md:24,58,66,72`;`@92
Removed from old lines 92-92 (anchor with `side=old`):
```text
   92: | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
```
Removed tokens: `none``@92 `Write`@92 `contract`@92 `for`@92 `too`@92 `(WC-4`@92 `"every`@92 `outcome")`@92 ``sk/sc-workflow-protocol/SKILL.md:58,66,72`;`@92

### H2.7 (section: 3.2 Needs a change (27); owners: R1.2)

New lines 95-95:
```text
   95: "Blocked" means the WC-2 (c) resolution: write the contract with `worker_status: blocked` (R1.2) and the question, then stop.
```
Changed tokens: ``worker_status:`@95 `(R1.2)`@95
Removed from old lines 95-95 (anchor with `side=old`):
```text
   95: "Blocked" means the WC-2 (c) resolution: write the contract with `status: blocked` and the question, then stop.
```
Removed tokens: ``status:`@95

### H2.8 (section: 5. Standalone use without Orca keeps working unchanged; owners: R1.5)

New lines 147-147:
```text
  147: | SA-2 | No command, skill or agent file runs an `orca` or `orca-ide` command, and none requires Orca to be installed or running. The only allowed mention of Orca is inside the contract file, as an example of a caller's channels for questions, reports and checks (WC-3, WC-5, WC-12); AC-C1 excludes that one file (R1.5). | Commands run in other projects (`CLAUDE.md:74`); without Orca the calls fail with `runtime_unavailable` (`CAPS:147`). | `CAPS:145-149`; today's baseline: only `sk/ccsession-tag/` mentions Orca (section 1.2, E5) |
```
Changed tokens: `inside`@147 `the`@147 `contract`@147 `file,`@147 `channels`@147 `for`@147 `questions,`@147 `reports`@147 `and`@147 `checks`@147 `(WC-3,`@147 `WC-5,`@147 `WC-12);`@147 `AC-C1`@147 `excludes`@147 `that`@147 `one`@147 `file`@147 `(R1.5).`@147
Removed from old lines 147-147 (anchor with `side=old`):
```text
  147: | SA-2 | No command, skill or agent file runs an `orca` or `orca-ide` command, and none requires Orca to be installed or running. The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file. | Commands run in other projects (`CLAUDE.md:74`); without Orca the calls fail with `runtime_unavailable` (`CAPS:147`). | `CAPS:145-149`; today's baseline: only `sk/ccsession-tag/` mentions Orca (section 1.2, E5) |
```
Removed tokens: `in`@147 `a`@147 `changed`@147 `command`@147 `question`@147 `channel`@147 `inside`@147 `the`@147 `contract`@147 `file.`@147

### H2.9 (section: 7. Acceptance checks per phase; owners: R1.1)

New lines 167-167:
```text
  167: Run from the repo root. `ORCA` means `orca-ide` outside an Orca terminal and `orca` inside one (`CAPS:145`). A phase passes only when every check in its block and every common check passes. Every `--unattended` run in these checks also passes `--report-dir <dir>` (WC-4, R1.1).
```
Changed tokens: `Every`@167 ``--unattended``@167 `run`@167 `in`@167 `these`@167 `checks`@167 `also`@167 `passes`@167 ``--report-dir`@167 `<dir>``@167 `(WC-4,`@167 `R1.1).`@167

### H2.10 (section: 7.1 Common checks (every phase); owners: R1.5)

New lines 172-172:
```text
  172: | AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \| grep -v '^src/superclaude/skills/ccsession-tag/' \| grep -v '^src/superclaude/core/WORKER-CONTRACT\.md:'` | prints nothing (SA-2, WC-8); the contract file is excluded because SA-2 lets it name the caller's Orca channels (R1.5) |
```
Changed tokens: `'^src/superclaude/skills/ccsession-tag/'`@172 `\|`@172 `grep`@172 `-v`@172 `'^src/superclaude/core/WORKER-CONTRACT\.md:'``@172 `WC-8);`@172 `the`@172 `contract`@172 `file`@172 `is`@172 `excluded`@172 `because`@172 `SA-2`@172 `lets`@172 `it`@172 `name`@172 `the`@172 `caller's`@172 `Orca`@172 `channels`@172 `(R1.5)`@172
Removed from old lines 172-172 (anchor with `side=old`):
```text
  172: | AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \| grep -v '^src/superclaude/skills/ccsession-tag/'` | prints nothing (SA-2, WC-8) |
```
Removed tokens: `'^src/superclaude/skills/ccsession-tag/'``@172 `WC-8)`@172

### H2.11 (section: 7.2 Live worker check (used by P0-P4); owners: R1.2,R1.4)

New lines 182-184:
```text
  182: 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `worker_status` under WC-5 (R1.2); its report path is the WC-4 contract path.
  183: 4. `test -s <contract>` and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['worker_status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`; field name per WC-4, R1.2). **Pass:** both exit 0.
  184: 5. `ORCA orchestration worker-read --dispatch <dispatch_id> --source transcript --json` and search the transcript for `AskUserQuestion` and, when the command's file names a skill, for the Skill tool call that loads it. **Pass:** no `AskUserQuestion` call, and that Skill call appears before the command's first output (WC-7, R1.4).
```
Changed tokens: ``worker_status``@182 `WC-5`@182 `(R1.2);`@182 `d['worker_status']`@183 ``pyproject.toml:38`;`@183 `field`@183 `name`@183 `per`@183 `WC-4,`@183 `R1.2).`@183 ``AskUserQuestion``@184 `and,`@184 `when`@184 `the`@184 `command's`@184 `file`@184 `names`@184 `a`@184 `skill,`@184 `for`@184 `the`@184 `Skill`@184 `tool`@184 `call`@184 `that`@184 `loads`@184 `it.`@184 `call,`@184 `and`@184 `that`@184 `Skill`@184 `call`@184 `appears`@184 `before`@184 `the`@184 `command's`@184 `first`@184 `output`@184 `(WC-7,`@184 `R1.4).`@184
Removed from old lines 182-184 (anchor with `side=old`):
```text
  182: 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
  183: 4. `test -s <contract>` and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both exit 0.
  184: 5. `ORCA orchestration worker-read --dispatch <dispatch_id> --source transcript --json` and search the transcript for `AskUserQuestion`. **Pass:** no `AskUserQuestion` call.
```
Removed tokens: ``status``@182 `WC-5;`@182 `d['status']`@183 ``pyproject.toml:38`).`@183 ``AskUserQuestion`.`@184 `call.`@184

### H2.12 (section: 7.3 Per-phase checks; owners: R1.4,R1.6)

New lines 194-195:
```text
  194: | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, and the command's skill loaded with the Skill tool, both verified in the step-5 transcript; R1.4) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
  195: | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `/sc:load` (no report, per its 3.2 row and the Decisions table, R1.6) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```
Changed tokens: `and`@194 `the`@194 `command's`@194 `skill`@194 `loaded`@194 `with`@194 `the`@194 `Skill`@194 `tool,`@194 `both`@194 `transcript;`@194 `R1.4)`@194 `except`@195 ``/sc:load``@195 `(no`@195 `report,`@195 `per`@195 `its`@195 `3.2`@195 `row`@195 `and`@195 `the`@195 `Decisions`@195 `table,`@195 `R1.6)`@195
Removed from old lines 194-195 (anchor with `side=old`):
```text
  194: | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
  195: | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```
Removed tokens: `transcript)`@194

### H2.13 (section: 7.3 Per-phase checks; owners: R1.1,R1.2)

New lines 198-200:
```text
  198: | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the `--report-dir` report is written for pre-creation STOPs (R1.1) |
  199: | P2 | AC-2.1 | `test_worker_contract.py` gains one assertion per gate listed in the section 3 row, for example the auggie-review section names both `--no-post-pr` and `--no-remediation-offer` | passes |
  200: | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `worker_status: blocked` (R1.2) with a non-empty `blocked_question`; step 2 never shows `agentWait` |
```
Changed tokens: ``--report-dir``@198 `report`@198 `(R1.1)`@198 ``worker_status:`@200 `(R1.2)`@200
Removed from old lines 198-200 (anchor with `side=old`):
```text
  198: | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
  199: | P2 | AC-2.1 | `test_worker_contract.py` gains one assertion per gate listed in the section 3 row, for example the auggie-review section names both `--no-post-pr` and `--no-remediation-offer` | passes |
  200: | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
```
Removed tokens: `contract`@198 ``status:`@200

### H2.14 (section: 7.3 Per-phase checks; owners: R1.2)

New lines 208-208:
```text
  208: | P4 | AC-4.1 | `/sc:implement <plan> --unattended` on a plan with one acceptance criterion that cannot be met | ledger shows the halt; contract `worker_status: blocked` (R1.2); outcome `failed`; the ledger records no Ruling unless D2 allows a relayed one, in which case the Ruling quotes the person's words verbatim |
```
Changed tokens: ``worker_status:`@208 `blocked``@208 `(R1.2);`@208
Removed from old lines 208-208 (anchor with `side=old`):
```text
  208: | P4 | AC-4.1 | `/sc:implement <plan> --unattended` on a plan with one acceptance criterion that cannot be met | ledger shows the halt; contract `status: blocked`; outcome `failed`; the ledger records no Ruling unless D2 allows a relayed one, in which case the Ruling quotes the person's words verbatim |
```
Removed tokens: ``status:`@208 `blocked`;`@208

### H2.15 (section: 9. Open decisions for the user; owners: R1.7,R1.1)

New lines 228-228:
```text
  228: - (a) **Explicit `--unattended` flag in the brief (recommended).** The coordinator writes it into every worker's command line as a standalone token; text inside a person's quoted argument never counts (parse rule in section 2.1, R1.7). Example: `/sc:troubleshoot "login fails" --unattended --report-dir .dev/troubleshoot/login/`. It is testable by grep and cannot misfire on a person.
```
Changed tokens: `line`@228 `as`@228 `standalone`@228 `token;`@228 `text`@228 `inside`@228 `a`@228 `person's`@228 `quoted`@228 `argument`@228 `counts`@228 `(parse`@228 `rule`@228 `in`@228 `section`@228 `2.1,`@228 `R1.7).`@228 `--report-dir`@228
Removed from old lines 228-228 (anchor with `side=old`):
```text
  228: - (a) **Explicit `--unattended` flag in the brief (recommended).** The coordinator writes it into every worker's command line; a person never types it. Example: `/sc:troubleshoot "login fails" --unattended --output .dev/troubleshoot/login/`. It is testable by grep and cannot misfire on a person.
```
Removed tokens: `line;`@228 `person`@228 `types`@228 `it.`@228 `--output`@228

### H2.16 (section: Decisions; owners: R1.2)

New lines 262-262:
```text
  262: | Status vocabulary | Copy each command's own statuses; a fixed four-value set | Fixed set `succeeded / partial / failed / blocked` in its own field `worker_status`, because existing contracts already use `status` (WC-4, R1.2), mapped to Orca's two outcomes in WC-5, because Orca accepts only `succeeded` or `failed` (`CAPS:73`). |
```
Changed tokens: `blocked``@262 `in`@262 `its`@262 `own`@262 `field`@262 ``worker_status`,`@262 `because`@262 `existing`@262 `contracts`@262 `already`@262 `use`@262 ``status``@262 `(WC-4,`@262 `R1.2),`@262
Removed from old lines 262-262 (anchor with `side=old`):
```text
  262: | Status vocabulary | Copy each command's own statuses; a fixed four-value set | Fixed set `succeeded / partial / failed / blocked`, mapped to Orca's two outcomes in WC-5, because Orca accepts only `succeeded` or `failed` (`CAPS:73`). |
```
Removed tokens: `blocked`,`@262

