# Diffgate surface: review 3 of 3

format: diffgate/1
coverage: 2% of lines changed

Review only the changed tokens below. Anchor each new finding with `hunk=<id>` on a changed
token, or `via=<id>` for an unchanged line a hunk breaks, or `cites=<prior id>`.

## Prior blocking findings

| id | label | at | finding |
|---|---|---|---|
| R2.1 | major | [196, 196] | AC-1.2 passes --output to workflow and runs the contract check on load |
| R2.2 | major | [182, 182] | step 3 needs worker_status that no P0 command writes |
| R1.3 | major | [64, 64] | WC-6 fresh directory conflicts with the brief-fixed directory of WC-4 |

## Hunks

### H3.1 (section: 2.2 Requirements; owners: R1.3)

New lines 64-64:
```text
   64: | WC-6 | **Resume or safe re-run.** A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output. A command either resumes from its on-disk state when given its resume flag, or, if it has none, re-runs clean. A `--retry-of` retry reuses the failed Task and its spec, so it receives the first attempt's brief, `--report-dir` included: no Orca verb changes a Task's spec, and a new Task would route around the circuit breaker (R1.3). The coordinator, not the command, therefore keeps attempts apart: before it runs `worker-start --retry-of <dispatch_id>`, it renames the failed attempt's `<report-dir>/return-contract.yaml` to `return-contract.<dispatch_id>.yaml` and, for a command without resume, renames that attempt's output location to `<location>.<dispatch_id>`, using the failed Dispatch's ID. The retry then writes the paths the brief recorded before dispatch into a location that holds no earlier output, and the first attempt's files stay intact under the new names (R1.3). Orca's guide allows a retry only of a positively proven failed or stopped attempt, so the first attempt no longer writes when its files are renamed (R1.3). A WC-3 re-invocation inside one worker is the same attempt: it reuses that attempt's directories, and its report replaces the `blocked` report of the first invocation; the question itself stays recorded in the Run (`CAPS:59-60`) (R1.3). Section 3 names which applies per command. | Command (resume or clean re-run); coordinator (renames a failed attempt's files before a retry, R1.3) | `CAPS:116` (retry and circuit breaker); R1.3, Orca 1.4.245 read 2026-11-09: `orca orchestration worker-start --help` Notes ("--retry-of needs --task naming the failed Task (--spec creates a new one)"), `orca orchestration task-update --help` Usage (only `--status` and `--result`), `orca orchestration` guide reference `recovery-and-cleanup` line 112 ("Retry only a positively proven failed or stopped attempt"); resume mechanisms in column (e) of `INV-A:35-55`, `INV-B:31-52` |
```
Changed tokens: `clean.`@64 `A`@64 ``--retry-of``@64 `retry`@64 `reuses`@64 `the`@64 `failed`@64 `Task`@64 `and`@64 `its`@64 `spec,`@64 `so`@64 `it`@64 `receives`@64 `the`@64 `first`@64 `attempt's`@64 `brief,`@64 ``--report-dir``@64 `included:`@64 `no`@64 `Orca`@64 `verb`@64 `changes`@64 `a`@64 `Task's`@64 `spec,`@64 `and`@64 `a`@64 `Task`@64 `would`@64 `route`@64 `around`@64 `the`@64 `circuit`@64 `breaker`@64 `(R1.3).`@64 `therefore`@64 `keeps`@64 `attempts`@64 `apart:`@64 `before`@64 `it`@64 `runs`@64 ``worker-start`@64 `--retry-of`@64 `<dispatch_id>`,`@64 `it`@64 `renames`@64 `the`@64 `failed`@64 ``<report-dir>/return-contract.yaml``@64 `to`@64 ``return-contract.<dispatch_id>.yaml``@64 `renames`@64 `that`@64 `attempt's`@64 `output`@64 `location`@64 `to`@64 ``<location>.<dispatch_id>`,`@64 `using`@64 `the`@64 `failed`@64 `Dispatch's`@64 `ID.`@64 `The`@64 `retry`@64 `then`@64 `writes`@64 `the`@64 `paths`@64 `the`@64 `brief`@64 `recorded`@64 `before`@64 `dispatch`@64 `into`@64 `location`@64 `that`@64 `holds`@64 `no`@64 `earlier`@64 `output,`@64 `and`@64 `intact`@64 `under`@64 `new`@64 `names`@64 `(R1.3).`@64 `Orca's`@64 `guide`@64 `allows`@64 `a`@64 `retry`@64 `only`@64 `of`@64 `a`@64 `positively`@64 `proven`@64 `failed`@64 `or`@64 `stopped`@64 `attempt,`@64 `so`@64 `the`@64 `first`@64 `attempt`@64 `no`@64 `longer`@64 `writes`@64 `when`@64 `its`@64 `files`@64 `are`@64 `renamed`@64 `(`CAPS:59-60`)`@64 `(renames`@64 `a`@64 `failed`@64 `attempt's`@64 `files`@64 `before`@64 `a`@64 `retry,`@64 `R1.3,`@64 `Orca`@64 `1.4.245`@64 `read`@64 `2026-11-09:`@64 ``orca`@64 `orchestration`@64 `worker-start`@64 `--help``@64 `Notes`@64 `("--retry-of`@64 `needs`@64 `--task`@64 `naming`@64 `the`@64 `failed`@64 `Task`@64 `(--spec`@64 `creates`@64 `a`@64 `new`@64 `one)"),`@64 ``orca`@64 `orchestration`@64 `task-update`@64 `--help``@64 `Usage`@64 `(only`@64 ``--status``@64 `and`@64 ``--result`),`@64 ``orca`@64 `orchestration``@64 `guide`@64 `reference`@64 ``recovery-and-cleanup``@64 `line`@64 `112`@64 `("Retry`@64 `only`@64 `a`@64 `positively`@64 `proven`@64 `failed`@64 `or`@64 `stopped`@64 `attempt");`@64
Removed from old lines 64-64 (anchor with `side=old`):
```text
   64: | WC-6 | **Resume or safe re-run.** A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output. A command either resumes from its on-disk state when given its resume flag, or, if it has none, re-runs clean into new directories. The coordinator, not the command, chooses those directories: each attempt's brief, a `--retry-of` retry included, names a new `--report-dir` and, for a command without resume, a new output location, so the first attempt's files stay as they were and the report path is recorded before dispatch (R1.3). A WC-3 re-invocation inside one worker is the same attempt: it reuses that attempt's directories, and its report replaces the `blocked` report of the first invocation; the question itself stays recorded in the Run (`CAPS:58`) (R1.3). Section 3 names which applies per command. | Command (resume or clean re-run); coordinator (directories per attempt, R1.3) | `CAPS:116` (retry and circuit breaker); resume mechanisms in column (e) of `INV-A:35-55`, `INV-B:31-52` |
```
Removed tokens: `clean`@64 `into`@64 `directories.`@64 `chooses`@64 `those`@64 `directories:`@64 `each`@64 `brief,`@64 `a`@64 ``--retry-of``@64 `retry`@64 `included,`@64 `names`@64 `a`@64 `new`@64 ``--report-dir``@64 `new`@64 `output`@64 `location,`@64 `so`@64 `as`@64 `they`@64 `were`@64 `and`@64 `report`@64 `path`@64 `is`@64 `recorded`@64 `before`@64 `dispatch`@64 `(`CAPS:58`)`@64 `(directories`@64 `per`@64 `attempt,`@64

### H3.2 (section: 2.3 What the coordinator owes each worker; owners: R1.3)

New lines 73-73:
```text
   73: The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; a report directory passed as `--report-dir`, so the report path is known before dispatch and stays the same for a `--retry-of` retry, which reuses this brief (WC-4, WC-6; R1.1, R1.3); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`); before a `--retry-of` retry it renames the failed attempt's report and, for a command without resume, its output location (WC-6, R1.3).
```
Changed tokens: `dispatch`@73 `stays`@73 `the`@73 `same`@73 ``--retry-of``@73 `retry,`@73 `which`@73 `reuses`@73 `this`@73 `brief`@73 `(`CAPS:107-113`);`@73 `before`@73 `a`@73 ``--retry-of``@73 `retry`@73 `it`@73 `renames`@73 `the`@73 `failed`@73 `attempt's`@73 `report`@73 `and,`@73 `for`@73 `a`@73 `command`@73 `without`@73 `resume,`@73 `its`@73 `output`@73 `location`@73 `(WC-6,`@73 `R1.3).`@73
Removed from old lines 73-73 (anchor with `side=old`):
```text
   73: The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; a report directory passed as `--report-dir`, new for each attempt including retries, so the report path is known before dispatch, and for a command without resume a new output location per attempt as well (WC-4, WC-6; R1.1, R1.3); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```
Removed tokens: `new`@73 `for`@73 `each`@73 `attempt`@73 `including`@73 `retries,`@73 `dispatch,`@73 `command`@73 `without`@73 `resume`@73 `a`@73 `new`@73 `output`@73 `location`@73 `per`@73 `attempt`@73 `as`@73 `well`@73 `(`CAPS:107-113`).`@73

### H3.3 (section: 3. Per-command changes; owners: R1.3)

New lines 76-76:
```text
   76: The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<report-dir>/return-contract.yaml`, written to the `--report-dir` every brief passes (R1.1). "Fresh dir" in a Resume column means the command has no resume: before a retry the coordinator renames the failed attempt's output location, so the retry writes into an empty one (WC-6, R1.3). Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
```
Changed tokens: `command`@76 `has`@76 `no`@76 `resume:`@76 `before`@76 `a`@76 `retry`@76 `the`@76 `renames`@76 `the`@76 `failed`@76 `attempt's`@76 `location,`@76 `so`@76 `the`@76 `retry`@76 `writes`@76 `into`@76 `an`@76 `empty`@76 `one`@76
Removed from old lines 76-76 (anchor with `side=old`):
```text
   76: The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<report-dir>/return-contract.yaml`, written to the `--report-dir` every brief passes (R1.1). "Fresh dir" in a Resume column means the coordinator names a new output location in each attempt's brief (WC-6, R1.3). Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
```
Removed tokens: `names`@76 `a`@76 `new`@76 `location`@76 `in`@76 `each`@76 `attempt's`@76 `brief`@76

### H3.4 (section: 7.3 Per-phase checks; owners: R2.2,R2.1)

New lines 194-196:
```text
  194: | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, and the command's skill loaded with the Skill tool, both verified in the step-5 transcript; R1.4) | steps 1-3 and 5-7 pass, with the P0 differences that the contract, `--unattended` and `--report-dir` arrive only in P1: the step-1 brief carries the command line shown here, with neither flag; step 3 checks only that exactly one `worker_done` arrives and that its report path names the command's existing report file, not `worker_status` or the WC-4 path; step 4 uses that existing report file (R2.2). Record the results in the phase report; a failure here reopens section 1 |
  195: | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `/sc:load` (no report, per its 3.2 row and the Decisions table, R1.6) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
  196: | P1 | AC-1.2 | 7.2 live check on each P1 command except `/sc:load` (no report, as in AC-1.1), with the brief per section 2.3: `--unattended --report-dir <dir>` plus the flags that command's section 3 row requires, which for workflow are `--handoff none` and never `--output` (R2.1) | all steps pass |
```
Changed tokens: `pass,`@194 `with`@194 `the`@194 `P0`@194 `differences`@194 `that`@194 `the`@194 `contract,`@194 ``--unattended``@194 `and`@194 ``--report-dir``@194 `arrive`@194 `only`@194 `in`@194 `P1:`@194 `the`@194 `step-1`@194 `brief`@194 `carries`@194 `the`@194 `command`@194 `line`@194 `shown`@194 `here,`@194 `with`@194 `neither`@194 `flag;`@194 `3`@194 `checks`@194 `only`@194 `that`@194 `exactly`@194 `one`@194 ``worker_done``@194 `arrives`@194 `and`@194 `that`@194 `its`@194 `report`@194 `path`@194 `names`@194 `not`@194 ``worker_status``@194 `or`@194 `WC-4`@194 `path;`@194 `step`@194 `4`@194 `uses`@194 `that`@194 `existing`@194 `report`@194 `file`@194 `(R2.2).`@194 `except`@196 ``/sc:load``@196 `(no`@196 `report,`@196 `as`@196 `in`@196 `AC-1.1),`@196 `the`@196 `brief`@196 `per`@196 `section`@196 `2.3:`@196 `--report-dir`@196 `plus`@196 `the`@196 `flags`@196 `that`@196 `command's`@196 `section`@196 `3`@196 `row`@196 `requires,`@196 `which`@196 `for`@196 `workflow`@196 `are`@196 ``--handoff`@196 `none``@196 `and`@196 `never`@196 ``--output``@196 `(R2.1)`@196
Removed from old lines 194-196 (anchor with `side=old`):
```text
  194: | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, and the command's skill loaded with the Skill tool, both verified in the step-5 transcript; R1.4) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
  195: | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `/sc:load` (no report, per its 3.2 row and the Decisions table, R1.6) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
  196: | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
```
Removed tokens: `pass;`@194 `4`@194 `uses`@194 `since`@194 `contract`@194 `arrives`@194 `in`@194 `P1.`@194 `--output`@196

