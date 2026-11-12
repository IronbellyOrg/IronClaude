# Research 05: Orca development-source provenance (worker-start authority, dispatch-report mailbox, worker-run binding)

- Topic: Orca development-checkout source for helper routing (worker-start authority), the dispatch-report mailbox, and the worker/run binding
- Investigation type: Architecture analysis (source read, no live Orca, no Orca CLI call)
- Scope: three files under `/home/coder/workspaces/IronOrca/src/main/runtime/` (checkout source). Fix cycle 1 added read-only reads of the installed build files under `/opt/Orca/resources/app.asar.unpacked/out/` and read-only `git` comparisons of the checkout with the installed build's recorded commit (sections 1 and 5.2). The running Orca process, its stored settings and other hosts remain out of observed evidence and tagged UNVERIFIED.
- Date: 2026-11-11 (session date)
- Status: Complete

## Evidence classes used in this file

- CHECKOUT-SOURCE: text read directly from the development checkout at the commit recorded below.
- INSTALLED-FILES (added in fix cycle 1): file contents read under `/opt/Orca/resources/app.asar.unpacked/out/` (compiled output; `main/` is a minified bundle). Evidence about the installed build's code, not about the running process or its stored settings.
- INSTALLED-COMMIT-SOURCE (added in fix cycle 1): the source tree at the commit that the installed `out/package.json` records (`9cfecdd30b2a90c06e5178b1245cb31a97d11bac`), read with `git show` / `git diff` in the IronOrca repository. It stands in for the unminified source of the installed files; it is not the installed bundle itself.
- HISTORICAL-TRACE: reports or notes written earlier (here: `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/RESEARCH-REPORT-sub-orchestrator-mode.md`, read in fix cycle 1 at `:225-250` and `:393-450`).
- UNVERIFIED-DEPLOYED: running Orca process, its effective stored settings, other hosts, live behavior. Not observed.

## 1. Checkout git provenance (read-only git, CHECKOUT-SOURCE)

- Path: `/home/coder/workspaces/IronOrca`
- Branch: `main`
- HEAD commit: `dc57b3d6e81c9825446a520bf0aee8600a2f5586` (2026-10-27 07:30:16 -0700) `test: remove 61 low-value runtime tests and five suites (#34431)`
- Remote `origin`: `https://github.com/IronbellyOrg/IronOrca.git` (fetch and push)
- Working-tree status: clean (no `git status --short` output)
- Path check: all three assigned files exist at the exact assigned paths (glob under `src/main/runtime/` returned each once).
- Note: HEAD date (2026-10-27) predates this task package (2026-11-10). Package version at this commit: `1.4.214` (`/home/coder/workspaces/IronOrca/package.json:3`).
- Installed build provenance (fix cycle 1, read-only): `/opt/Orca/resources/app.asar.unpacked/out/package.json` records `name: orca-compiled-output`, `version: 1.4.245-aidev02.9cfecdd30b2a`, `commit: 9cfecdd30b2a90c06e5178b1245cb31a97d11bac`; the installed files carry mtime 2026-11-08 (`stat` of `cli/specs/core.js`). In the IronOrca repository that commit exists and is on `remotes/origin/aidev02` (`git branch -a --contains`), the checkout HEAD `dc57b3d6e` is an ancestor of it (`git merge-base --is-ancestor`), and `git rev-list --count dc57b3d6e..9cfecdd30b2a...` printed 1048. So the checkout is an OLDER snapshot of the same repository, not the installed build. The earlier report records the same metadata (`RESEARCH-REPORT-sub-orchestrator-mode.md:242`, "Version `1.4.245-aidev02.9cfecdd30b2a`; commit `9cfecdd30b2a...`").
- Source-level comparison of the files this research cites, checkout HEAD vs the installed build's commit (`git diff --quiet dc57b3d6e 9cfecdd30b2a... -- <file>`): IDENTICAL for `worker-start-authority.ts`, `worker-run-binding.ts`, `dispatch-report-mailbox.ts`, `worker-dispatch-start.ts`, `dispatch-depth.ts`, `local-worker-start.ts`, `dispatch-creator.ts`, `run-binding.ts`, `run-scope.ts`, `run-create.ts`; DIFFERENT for `shared/nested-worker-depth.ts` (24 added, 2 removed lines: default 2 instead of 1), `shared/default-global-settings.ts` (43/12), `rpc/.../runs/runs.ts` (6/2, in the `runUse` takeover check only, not `runCreate`) and `rpc/.../worker/workers.ts` (1 added line, `requires: ['accounts']`). Whether the installed minified bundle equals that commit's compiled output was not shown in general; for the depth default specifically, the installed `out/shared/nested-worker-depth.js:10` and `out/shared/default-global-settings.js:161-162` agree with that commit's `src/shared/nested-worker-depth.ts` (default 2, same fork comment) (section 5.2); the installed bundle's `runCreate` handler (`main/chunks/orcad-migration-source-retention-B-HAVPZ-.js:388`) shows no worker refusal, like the source.
- Scope note (research-notes.md:35 assignment): the three files were located at their assigned paths; no basename search fallback was needed. No Orca process or CLI was started or called.

## 2. `worker-start-authority.ts` (CHECKOUT-SOURCE, 74 lines)

Path: `/home/coder/workspaces/IronOrca/src/main/runtime/rpc/methods/orchestration/worker/worker-start-authority.ts`

### 2.1 Exports and signatures

- `resolveWorkerStartRun(runtime: OrcaRuntimeService, args: { coordinator: OrchestrationCallerIdentity | null; from: string; callerSession: OrchestrationSessionCaller | undefined; runId: string | undefined }): { run: RunRow; helperCreator?: DispatchContextRow }` at `worker-start-authority.ts:12-20`.
- `assertHelperStartScope(db: OrchestrationDb, creator: DispatchContextRow, args: { task: TaskRow | undefined; params: { on?: string; terminal?: string } }): void` at `worker-start-authority.ts:51-55`.
- Private `fenced(message)` returns `OrchestrationError('consumer_fenced', message)` at `worker-start-authority.ts:72-74`.

### 2.2 `resolveWorkerStartRun` decision order [CODE-VERIFIED]

1. Coordinator path (`:21-30`): `db.getCurrentRunForCoordinator(args.coordinator)` (only when `args.coordinator` is non-null). If a Run is bound and `args.runId` is given but differs, throw `consumer_fenced` "This caller coordinates Run X, not Y." (`:26-28`); otherwise return `{ run: coordinated }` with NO `helperCreator`.
2. Worker-as-helper-starter path (`:31-47`), reached only when the caller coordinates no Run:
   - `resolveDispatchCreator(runtime, args.from, args.callerSession)` (`:33`, defined at `rpc/methods/orchestration/runs/dispatch-creator.ts:7-39`) builds a `DispatchCreator`.
   - `db.resolveCreatorDispatchId(creator)` (`:32`, defined at `orchestration/db/dispatch-depth.ts:96-112`) proves the caller's own active Dispatch.
   - Then `getDispatchContextById(creatorId)` and `getRun(creator.run_id)` (`:35-36`).
   - If no creator Dispatch, no Run, or `run.legacy === 1`: `consumer_fenced` "worker-start needs the coordinator bound to the Run, or a worker on an active Dispatch in it." (`:37-41`).
   - If `args.runId` names a different Run than the creator Dispatch's Run: `consumer_fenced` "...it starts helpers only there." (`:42-46`).
   - Return `{ run, helperCreator: creator }` (`:47`).
3. Fail-closed property: a caller that is neither the bound coordinator nor a worker with exactly one provable active non-self Dispatch gets `consumer_fenced`. `resolveCreatorDispatchId` returns null unless exactly one local-or-remote match exists (`dispatch-depth.ts:108-110`), and `AmbiguousDispatchParentError` is thrown for multiple live remote attachments (`dispatch-depth.ts:156-160`). [CODE-VERIFIED]

### 2.3 `assertHelperStartScope` rules [CODE-VERIFIED]

- Rejects `--on` or `--terminal` (`:56-62`) with `invalid_argument` "A worker starts helpers in a new agent on this host; omit --on and --terminal. No effects were applied." Rationale comment (`:57`): remote reports reach the Run home mailbox, so a remote helper could not report to its creator.
- Rejects reusing a Task not last run by a helper of this creator Dispatch (`:64-69`): `db.getDispatchContext(task.id)?.creator_dispatch_id !== creator.id` gives `task_not_found` "...start new helper work with --spec."
- Doc comment (`:50`): workers may launch fresh local helpers or retry their own helper's latest Attempt, never coordinator Tasks or another party's pane.

### 2.4 Sole caller and what happens after (CODE-VERIFIED)

- Only caller of both functions: `orchestration.workerStart` handler, `worker/workers.ts:42` (`resolveWorkerStartRun`) and `:56` (`assertHelperStartScope`, only `if (helperCreator)`). Import at `workers.ts:10`.
- Handler order: caller identity via `resolveOrchestrationCaller` (`workers.ts:37-41`), authority resolution (`:42-47`), Task existence in the Run (`:48-54`), helper scope (`:55-57`), prompt budget (`:58`), start mode (`:59-62`), remote branch for `params.on` (`:71-83`), else `startLocalWorker` with `helperCreator` (`:84-95`).
- `startLocalWorker` forwards the creator to the database: `local-worker-start.ts:153-156` calls `db.createStartingWorkerDispatch({ creator: resolveDispatchCreator(...), maxDepth: runtime.getNestedWorkerMaxDepth(), requiredCreatorDispatchId: args.helperCreator?.id, ...})` and sets `taskParentId: params.parent ?? args.helperCreator?.task_id` (`:162`) so the Task tree records the helper under its creator's Task.
- Race guard: `worker-dispatch-start.ts:137-147` re-resolves the creator inside the creating transaction and throws `consumer_fenced` "Dispatch X is no longer this caller's active work, so it cannot start a helper." if it differs from `requiredCreatorDispatchId`.
- Depth cap: the new row's depth is `this.resolveChildDispatchDepth(params.creator, params.maxDepth)` (`worker-dispatch-start.ts:167`); see section 5.2 for the depth defaults (checkout 1, installed files 2).
- Transaction note: the creator re-check and row insert sit inside `createStartingWorkerDispatch` (`worker-dispatch-start.ts:12`), which opens `BEGIN IMMEDIATE` at `:48` and commits at `:202` [CODE-VERIFIED].

## 3. `dispatch-report-mailbox.ts` (CHECKOUT-SOURCE, 37 lines)

Path: `/home/coder/workspaces/IronOrca/src/main/runtime/orchestration/dispatch-report-mailbox.ts`

### 3.1 Exports and signatures

- `isDispatchReportType(type: MessageType | undefined): boolean` at `:5-13`. True for `undefined`, `'worker_done'`, `'heartbeat'`, `'escalation'`, `'status'`. Doc comment (`:4`): "Reports about the worker's own task; gates and handoffs stay with the Run's coordinator." So every other message type (for example gate or handoff types) is NOT a dispatch report and is not rerouted to a creator.
- `activeCreatorDispatch(db: OrchestrationDb, dispatch: Pick<DispatchContextRow, 'creator_dispatch_id' | 'run_id'>): DispatchContextRow | undefined` at `:16-28`. Returns the creator Dispatch only if (a) `creator_dispatch_id` is set, (b) the row exists, (c) `creator.run_id === dispatch.run_id` (same Run), and (d) `creator.status` is `'pending'` or `'dispatched'` (live).
- `dispatchReportMailbox(db, dispatch): string` at `:31-37`. Returns `` `dispatch:${creator.id}` `` when a live same-Run creator exists, else `` `run:${dispatch.run_id}` ``. Doc comment (`:30`): resolves the live creator or Run on each send, so helpers follow creator settlement without rewriting routes.

### 3.2 Behavior consequences [CODE-VERIFIED]

- Coordinator-started workers have no creator Dispatch (`resolveWorkerStartRun` returns no `helperCreator` for a coordinator, `worker-start-authority.ts:29`; that the database then records a null `creator_dispatch_id` follows from `resolveCreatorDispatchId` returning null when the caller has no active non-self Dispatch, `dispatch-depth.ts:100-111`, an INFERENCE not tested by running it), so their reports go to `run:<id>` (the coordinator's mailbox). The route is a pure function of current database state, not a stored address.
- When a helper's creator Dispatch settles (status leaves `pending`/`dispatched`), later reports from that helper fall back to `run:<id>` without any row rewrite (`:30`, `:35-36`).
- No self-loop or cross-Run hop: a creator in another Run is ignored (`:25`).

### 3.3 Callers (all in checkout; grep of `src/` for each symbol) [CODE-VERIFIED]

- `isDispatchReportType` and `dispatchReportMailbox`: `rpc/methods/orchestration/messaging/send-methods.ts:5-6` import; use at `:143-154`. When `to` is empty, or the message type is `worker_done` or `heartbeat` and a Dispatch is resolved, a `isDispatchReportType` message from that Dispatch goes to `dispatchReportMailbox(db, reporting)`, else `run:<id>` (`:149-153`). Note the explicit `to` is kept for other types and for explicit recipients where the condition at `:144-148` is false.
- `dispatchReportMailbox`: `messaging/ask-methods.ts:113` (`const reportTo = dispatchReportMailbox(db, activeDispatch)`). An ask whose explicit target is neither `run:<id>`, `reportTo`, nor the Run coordinator's address is refused with `dispatch_run_mismatch` (`:114-125`); an explicit Run or coordinator target still reaches the Run, otherwise the ask goes to the creator mailbox (`:126-127`).
- `dispatchReportMailbox`: `worker/worker-topology.ts:176` for the worker-setup `status` message (`to: dispatch ? dispatchReportMailbox(args.db, dispatch) : \`run:${args.runId}\``).
- `dispatchReportMailbox`: `terminal/layout/terminal-resize-listeners.ts:147` as the `mailbox` thunk passed to `escalateWorkerFailure` for worker-failure escalation (`:142-147`), so a helper's crash escalates to its creator while the creator is live.
- `activeCreatorDispatch`: used only inside this file (`:35`); it is exported but has no other importer in `src/` [CODE-VERIFIED by grep].
- Test coverage that exercises the mailbox end to end: `src/main/runtime/structured-chat-worker-helpers.test.ts` (describe blocks at `:104` "a worker starting helpers on the Run it works for" and `:222` "a helper whose creator settles between it and the Run"; its cases assert creator-first delivery, hand-back to the Run on creator settlement, and exactly-once delivery on replay). No unit test imports the three named symbols directly [CODE-VERIFIED by grep; absence of a direct test is negative evidence, not a finding].

## 4. `worker-run-binding.ts` (CHECKOUT-SOURCE, 78 lines)

Path: `/home/coder/workspaces/IronOrca/src/main/runtime/orchestration/db/runs/worker-run-binding.ts`

### 4.1 Exports and signatures

- `findCallerWorkerDispatches(db: OrchestrationDb, caller: OrchestrationCoordinatorKey): DispatchContextRow[]` at `:11-22`. Computes `mailboxAddressOf(caller)` (`orchestration-caller-identity.ts:32`); returns `[]` when null (`:15-18`); else `db.getActiveDispatchMailboxOwners(address, caller.paneKey ?? undefined)` (`:19-20`, defined `db/dispatch-context/dispatch-lookup.ts:54`) filtered by `!isSelfCreatedDispatch(dispatch)` (`:21`, defined `db/dispatch-depth.ts:57-62`). Doc comment (`:10`): matched by address then pane "as check and send do".
- `workerRunBindingRefusal(db, caller, runId, attempted: { takeover: boolean; bind: boolean }): OrchestrationError | null` at `:45-73`.
- `unboundWorkerMessage(dispatch: DispatchContextRow): string` at `:76-78`.
- Private `callerDispatchWorkingForRun(dispatches, db, runId)` at `:25-42` (not exported).

### 4.2 Rules [CODE-VERIFIED]

- "Works for a Run" is transitive: for each of the caller's own active non-self Dispatches, walk `creator_dispatch_id` ancestors (`:33-39`) until a row with `run_id === runId` is found, with a `visited` set to stop cycles (`:32`, `:34-37`). The walk ends at the first match and returns the caller's own Dispatch (`:35`).
- `workerRunBindingRefusal` (`:45-73`):
  - If `callerDispatchWorkingForRun` matches: error `worker_cannot_coordinate_own_run` (`:58-62`) with two message forms: own Run (`:55`) "You work Dispatch X in Run R, so you cannot coordinate that Run." or ancestor Run (`:56-57`) "...which was started from work in Run R, so you cannot coordinate Run R." Both append "Your mail arrives through plain `orchestration check` (no --run); report with `orchestration send`. No effects were applied." Data: `{ effectsApplied: false, dispatchId: own.id }`.
  - Else if the caller works any active delegated Dispatch (`dispatches[0]`) AND both `attempted.bind` and `attempted.takeover` are true: `worker_cannot_take_over_run` "A caller working an active Dispatch cannot use a takeover flag." (`:64-71`).
  - Else `null` (no refusal; the caller is not a worker for this Run).
- `unboundWorkerMessage` (`:76-77`): what a worker with no Run binding is told: it works Dispatch D in Run R, is not bound, reads mail with plain `orchestration check`, reports with `orchestration send`.
- Design consequence stated by the code (corrected in fix cycle 1): `workerRunBindingRefusal` is NARROW. It refuses (a) a worker binding its own Run or an ancestor Run (`:52-63`) and (b) a takeover flag from a caller working an active Dispatch (`:64-71`). It is called only from `run-binding.ts:49` (the bind path used by `run-use`) and `run-scope.ts:187` (`resolveRunScope`, `bind: false`). It is NOT called on `orchestration.runCreate` (`rpc/methods/orchestration/runs/runs.ts:31-55`), which resolves the caller and calls `db.createRun(...)` (`db/runs/run-create.ts:7-50`); neither contains a worker check, and `createRun` only unbinds the caller's other Runs (`run-lookup.ts:163-`). A worker with an active Dispatch can therefore create a NEW Run and become its bound coordinator, after which `resolveWorkerStartRun` takes the coordinator path (`worker-start-authority.ts:22-30`, no `helperCreator`). In the checkout this is not refused by the three files studied; the nested-worker depth cap is the barrier that limits what such a coordinator can then start (section 5.2; the earlier report records that a new Run does not reset the caller's delegation depth, `RESEARCH-REPORT-sub-orchestrator-mode.md:408`, HISTORICAL-TRACE, not re-derived here). The same holds in the installed build's recorded commit (`git diff --quiet` of `run-create.ts` between `dc57b3d6e` and `9cfecdd30b2a...` printed no difference; the commit's `runs.ts` differs only in `runUse`), and the installed bundle's `runCreate` handler (`main/chunks/orcad-migration-source-retention-B-HAVPZ-.js:388`) shows no worker refusal. [CODE-VERIFIED] (checkout and installed-commit source; bundle read at the handler head only). The effect of the depth cap on that case was not run. This is a development-source rule "a worker cannot bind or take over its own or an ancestor Run"; it does NOT make a helper-starting worker unable to coordinate, and it does not implement any subordinate coordinator mode.

### 4.3 Callers [CODE-VERIFIED by grep of `src/`]

- `db/runs/run-binding.ts:7` imports `findCallerWorkerDispatches` and `workerRunBindingRefusal`. The binding method refuses first (`run-binding.ts:44-55`: `sameBinding ? null : workerRunBindingRefusal(this, coordinator, params.runId, { takeover: explicitTakeover, bind: true })`, thrown at `:53-55`). The comment at `:46` says this is before the legacy gate so a worker never sees its `--takeover-legacy` recovery command. A second use at `run-binding.ts:125-132`: for a Run with live legacy work where the caller is not the proven coordinator, a worker gets `consumer_fenced` "Run X still has active legacy work and this caller cannot bind it. Nothing changed." instead of the takeover recovery command.
- `rpc/methods/orchestration/runs/run-scope.ts:18-20` imports `findCallerWorkerDispatches`, `unboundWorkerMessage`, `workerRunBindingRefusal`. In `unboundCallerError` (`run-scope.ts:139-143`) a worker gets `run_required` with `unboundWorkerMessage(worked)` instead of the coordinator-binding command; in `resolveRunScope` (`:183-194`) a worker naming its own or ancestor Run gets `workerRunBindingRefusal(db, caller, explicit.id, { takeover: false, bind: false })` before the unbound error. Also `run-scope.ts:158-163`: a caller with no terminal handle gets `run_required` containing "A worker never binds a Run: its mail arrives through plain `orchestration check`, and it reports with `orchestration send`."
- The `bind: false` refusal in `resolveRunScope` applies only when `explicit && current?.id !== explicit.id` (`run-scope.ts:185-188`).

## 5. How the three files connect (data flow, config, edge cases)

### 5.1 End-to-end flow for a worker-started helper [CODE-VERIFIED, traced by reading, not by running]

1. A worker (active non-self Dispatch D in Run R) calls `orchestration worker-start --from <its handle> ...` which lands in the `orchestration.workerStart` handler (`worker/workers.ts:21-28`, permission `'workspace'`).
2. `resolveOrchestrationCaller` yields a coordinator identity only if the caller coordinates a Run (`workers.ts:37-41`); a plain worker is not bound, so `resolveWorkerStartRun` takes the helper path (`worker-start-authority.ts:31-47`) and returns `{ run: R, helperCreator: D }`.
3. `assertHelperStartScope` forbids `--on` and `--terminal` and foreign Tasks (`:51-70`).
4. `startLocalWorker` calls `createStartingWorkerDispatch` with `requiredCreatorDispatchId: D.id` and `maxDepth = runtime.getNestedWorkerMaxDepth()` (`local-worker-start.ts:153-156`). Inside `BEGIN IMMEDIATE` the creator is re-proven (`worker-dispatch-start.ts:137-147`), the depth cap applied (`:167`), and the helper's row stores `creatorDispatchId` and the recorded creator identity (`:170-171`, via `recordedCreatorIdentity`, `dispatch-depth.ts:34-54`).
5. When the helper later sends `worker_done`/`heartbeat`/`escalation`/`status` or asks, `dispatchReportMailbox` picks `dispatch:<D>` while D is `pending` or `dispatched` in the same Run, else `run:<R>` (`dispatch-report-mailbox.ts:31-37`; `send-methods.ts:143-154`; `ask-methods.ts:113,126-127`; `terminal-resize-listeners.ts:147`; `worker-topology.ts:176`).
6. D (the creator worker) reads these in its own plain `orchestration check`; D never binds R (`worker-run-binding.ts:45-62`; `run-scope.ts:139-143,183-194`). Gates and handoffs, which are not dispatch-report types (`dispatch-report-mailbox.ts:4-13`), remain with the Run's coordinator.

### 5.2 Configuration ceiling: nested-worker depth default is 1 in the checkout and 2 in the installed build files [CODE-VERIFIED in both sources; effective stored setting and running build UNVERIFIED]

Corrected in fix cycle 1. The first pass read the checkout only and concluded "helper start is disabled by default". That holds for the checkout default (1) and not for the installed build files (2). Three sources, one row each:

| Source | Default | Evidence | Provenance |
|---|---|---|---|
| Orca development checkout (`main`, `dc57b3d6e`, version 1.4.214) | 1 | `IronOrca/src/shared/nested-worker-depth.ts:3-7` (`NESTED_WORKER_MAX_DEPTH_DEFAULT = 1`; "at one, root coordinators dispatch workers but workers cannot dispatch further"); `IronOrca/src/shared/default-global-settings.ts:153` (`nestedWorkerMaxDepth: 1`) | CHECKOUT-SOURCE |
| Installed build files on this host (`/opt/Orca/resources/app.asar.unpacked/out/`, version `1.4.245-aidev02.9cfecdd30b2a`) | 2 (legacy value 1 migrated once to 2) | `shared/nested-worker-depth.js:10` (`NESTED_WORKER_MAX_DEPTH_DEFAULT = 2`), `:9` ("at two, a coordinator's worker can dispatch one more level and no deeper"), `:12` (legacy 1), `:26-31` (resolver: unsafe or below-one input falls back to the default 2), `:34-42` (migration to 2 only if `nestedWorkerMaxDepthDefaultedToTwo !== true` and the value equals 1); `shared/default-global-settings.js:161-162` (`nestedWorkerMaxDepth` = the default constant, `nestedWorkerMaxDepthDefaultedToTwo: true`); comment `nested-worker-depth.js:7-8`: "aidev02 fork difference: upstream v1.4.251+ defaults this to 4 ... keep 2 and this guard name, or drop the fork change if 4 is accepted" | INSTALLED-FILES; same text in INSTALLED-COMMIT-SOURCE (`git show 9cfecdd30b2a...:src/shared/nested-worker-depth.ts` lines 1-14) |
| Earlier report (HISTORICAL-TRACE) | originally researched build `1.4.245-aidev02.780594c521aa` (commit `780594c521aaa2399b242b0022045017f4a77436`): source default/fallback 1 and a filtered stored value of 1; a dated 2026-11-09 observation of the replacement installed source (version `1.4.245-aidev02.9cfecdd30b2a`): default/fallback 2 with a guarded legacy-1-to-2 migration; public upstream baseline 4 (external) | `RESEARCH-REPORT-sub-orchestrator-mode.md:233-236` (evidence-class table), `:242-247` (metadata, constants, resolver, migration, default construction), `:410` ("Neither observation proves the effective loaded maximum"), `:720`, `:997`, `:1009` | HISTORICAL-TRACE; its dated observation and the installed files read here agree |

[CONTRADICTION: `/home/coder/workspaces/IronOrca/src/shared/nested-worker-depth.ts:4` (default 1, this file's first pass) vs `/opt/Orca/resources/app.asar.unpacked/out/shared/nested-worker-depth.js:10` (default 2) and `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/RESEARCH-REPORT-sub-orchestrator-mode.md:235,243-247` (default/fallback 2, plus the historical build's 1 at `:234`). Resolution from provenance: they are different builds of one repository (the checkout is 1048 commits behind the installed build's commit, section 1), so neither value is wrong; each holds for its own build. What none of them shows is the effective stored `nestedWorkerMaxDepth` of the running Orca: UNVERIFIED-DEPLOYED. The earlier report also records `D5` as policy "depth one" (`:233`); native capability does not amend policy.]

Facts common to the sources:
- `resolveNestedWorkerMaxDepth` maps anything that is not a safe integer >= 1 to the default, so malformed settings cannot disable the fence (checkout `nested-worker-depth.ts:25-33`, comment `:24`; installed `nested-worker-depth.js:25-31`). `runtime.getNestedWorkerMaxDepth()` reads the store setting (checkout `workspaces/workspace-selectors.ts:150-154`).
- `resolveNestedWorkerMaxDepth` (`nested-worker-depth.ts:25-33`) maps anything that is not a safe integer >= 1 to the default, so malformed settings cannot disable the fence (comment `:24`). `runtime.getNestedWorkerMaxDepth()` reads the store setting (`workspaces/workspace-selectors.ts:150-154`).
- `resolveChildDispatchDepth` throws `nested_worker_depth_exceeded` when `childDepth > maxDepth` (`db/dispatch-depth.ts:165-179`), with message "Sub-worker dispatch is not permitted at depth N (max M). Complete this task yourself." (`nested-worker-depth.ts:11-17`) and next steps including raising "Nested worker depth" in Settings, Orchestration (`:19-22`; UI control at `renderer/src/components/settings/OrchestrationPane.tsx:156-160`).
- Consequence, by source (the check is `childDepth > maxDepth` refuses, `dispatch-depth.ts:165-179`; a coordinator-started worker has depth 1 = `ROOT_DISPATCH_DEPTH + 1`; a helper start from it has child depth 2):
  - Checkout default 1: 2 > 1, the helper start is refused. In the checkout, the code path in sections 2-3 is reachable only when `nestedWorkerMaxDepth` is raised to 2 or more.
  - Installed-file default 2: 2 > 2 is false, so the helper start is NOT refused by the depth cap; a helper's own helper (child depth 3) is. At the installed default, the barrier that keeps a worker from starting a helper is not Orca code: it is contract rule WC-13 (`WORKER-CONTRACT.md:62`, "at any depth setting"), which is text read by the worker LLM and is not enforced in code (`require-orca-worktree-agent.sh` does not inspect `worker-start`, research/03 section F). This is a consequence derived from reading the two sources, not a run.
  - Effective stored setting on the running Orca: UNVERIFIED-DEPLOYED (it lives in the Orca desktop app's settings store; not read). The earlier report likewise records that source contents do not establish effective settings (`RESEARCH-REPORT-sub-orchestrator-mode.md:235,410`).
- The worker preamble mirrors the cap: `canDispatchSubWorkers = depth < maxDepth` in `coordinator-task-dispatch.ts:123`, `runs/dispatch-methods.ts:78,166,245`, `worker/deliver-worker-dispatch-preamble.ts:51` and `federation/federation.ts:212`; `preamble.ts:142-146` appends a `=== SUB-DISPATCH ===` section only when true. At cap 1 workers are not told they may start helpers; at cap 2 a depth-1 worker is (1 < 2), so the preamble invites helper start while WC-13 forbids it. Not run; inferred from the comparison.

### 5.3 Two different sub-dispatch preamble texts (edge case to flag) [CODE-VERIFIED text; runtime behavior of the second UNVERIFIED]

- Local variant `buildSubDispatchSection` (`preamble.ts:220-238`): "You may start helpers for this task. They work in this Dispatch's Run and report to you ... `orchestration worker-start --from <handle> --spec ... --worktree current --agent <agent> --json`". This matches the helper path traced above.
- Federated variant `buildOwnRunSubDispatchSection` (`preamble.ts:240-256`, selected when `subWorkersInOwnRun` is true at `:143-145`; set only at `federation/federation.ts:214`, the remote-host preamble): tells a REMOTE worker to `run-create` its own Run, `task-create`, and `worker-start --task`, then "Wait for every sub-worker's worker_done". This is a different mechanism (the remote worker becomes the coordinator of its own host-local Run), reachable only through federation. I did not trace that path end to end, so whether it works at runtime is UNVERIFIED. It must not be conflated with the deferred IronClaude subordinate/sub-orchestrator mode: it is Orca's own federated nesting text, not an IronClaude contract surface, and its mere existence in preamble text is not evidence that IronClaude ships sub-orchestration.

### 5.4 Edge cases and guards in the code [CODE-VERIFIED]

- Ambiguity: more than one live remote attachment for the creator identity throws `AmbiguousDispatchParentError` rather than picking one (`dispatch-depth.ts:155-160`); `resolveCreatorDispatchId` returns null (so helper start is `consumer_fenced`) when local+remote matches are not exactly one (`:108-110`).
- Self-dispatch is bookkeeping: `isSelfCreatedDispatch` treats a Dispatch whose creator pane equals its assignee pane (or creator handle equals assignee handle when pane keys are absent) as not a parent (`dispatch-depth.ts:57-62`). Pre-v37 rows without creator identity count conservatively as parents (comment `:56`). `findCallerWorkerDispatches` applies the same filter (`worker-run-binding.ts:21`).
- Identity trust: `resolveDispatchCreator` uses runtime-attested pane/incarnation (`dispatch-creator.ts:6`, `:27-37`); params are untrusted for remote attachment matching. A handle-less structured session is identified by its Orca session id (`:21-26`); no declared caller resolves to `{ kind: 'system' }` (depth zero, `:12-15`).
- Cycle safety: `callerDispatchWorkingForRun` uses a `visited` set (`worker-run-binding.ts:32-37`). `creator_dispatch_id` chains are walked without a depth bound other than the cycle guard.
- Settlement hand-back: no rewrite of helper routes occurs; the mailbox is recomputed on each send (`dispatch-report-mailbox.ts:30`). Tested in `structured-chat-worker-helpers.test.ts:222-293` (hand-back, replay, rollback cases).

## 6. Evidence classification (what each claim rests on)

| Claim | Class | Basis |
|---|---|---|
| The three files exist and export the signatures in sections 2-4 | CHECKOUT-SOURCE | Read at commit `dc57b3d6e81c9825446a520bf0aee8600a2f5586` on branch `main`, clean tree |
| All three are wired: every exported function except `activeCreatorDispatch` has a non-test caller in `src/` | CHECKOUT-SOURCE | Grep of `src/` (sections 2.4, 3.3, 4.3); `activeCreatorDispatch` is used only inside its own file at `:35` |
| A worker can start local helpers in its own Run and receive their reports | CHECKOUT-SOURCE (read-traced; also exercised by `structured-chat-worker-helpers.test.ts` per its test titles, whose pass/fail was NOT run) | Sections 5.1, 3.3 |
| With the CHECKOUT default (1) a worker's helper start is refused by the depth cap | CHECKOUT-SOURCE (defaults) | `nested-worker-depth.ts:4`, `default-global-settings.ts:153`, `dispatch-depth.ts:165-179` |
| With the INSTALLED-FILE default (2) a worker's helper start is NOT refused by the depth cap (a helper's helper is) | INSTALLED-FILES and INSTALLED-COMMIT-SOURCE (defaults) | `/opt/Orca/resources/app.asar.unpacked/out/shared/nested-worker-depth.js:10`, `shared/default-global-settings.js:161-162`; `dispatch-depth.ts:165-179` is identical at the installed commit |
| Earlier report's historical build default | HISTORICAL-TRACE | originally researched build `780594c521aa`: default/fallback 1; its dated 2026-11-09 replacement-source observation: 2 (`RESEARCH-REPORT-sub-orchestrator-mode.md:233-236,243-247`) |
| Conflict between the three default values | recorded, resolved by provenance | marker in section 5.2 citing `IronOrca/src/shared/nested-worker-depth.ts:4`, installed `shared/nested-worker-depth.js:10` and the report `:235,243-247` |
| The installed Orca binary matches the checkout commit | CONTRADICTED by provenance: installed build commit `9cfecdd30b2a...` is 1048 commits ahead of `dc57b3d6e` on `origin/aidev02`; the cited files are identical except the depth defaults and `runUse` (section 1) | `git` read-only |
| The running host's effective `nestedWorkerMaxDepth` value | UNVERIFIED-DEPLOYED | Setting lives in the Orca settings store; not read |
| Federated `run-create` sub-dispatch path works at runtime | UNVERIFIED | Only the preamble text and its selector were read (section 5.3) |
| IronOrca-side human-facing docs describe helper start | NOT FOUND | `grep -i helper` over `skills/`, `docs/`, `resources/` markdown found only five unrelated files (`skills/orca-emulator/SKILL.md`, two `docs/styleguide/*`, two `docs/agents-md-refs/*`); `grep worker-start\|workerStart` under `skills/` found no files |

## 7. Gaps, contradictions, stale documentation, DEFECT review

### 7.1 DEFECT review (documented-as-shipped but unwired)

- In scope: helper routing (`worker-start-authority.ts`), report mailbox, run binding refusal. None is dead code: each is imported and called on the live `orchestration.workerStart`, send, ask, escalation and run-binding paths (sections 2.4, 3.3, 4.3). No DEFECT recorded.
- The checkout default depth of 1 disables helper start unless the setting is raised; the installed files default to 2, which does not disable it (section 5.2). Either way this is configuration gating, not an unwired capability, and nothing read here documents helper start as enabled by default, so no DEFECT is claimed. If an IronClaude document states that workers can start helpers (or cannot) without naming the depth setting and the Orca build, that is a documentation gap for the synthesis to check; no such statement was read in this assignment. This conclusion does not close A01 of the earlier report, which stays an open DEFECT there (`RESEARCH-REPORT-sub-orchestrator-mode.md:853`); the local wording edit does not close it.

### 7.2 Doc-sourced claims tagged

- [CODE-VERIFIED] research-notes.md:35: Orca dev source contains helper routing (`resolveWorkerStartRun`/`assertHelperStartScope`), the dispatch-report mailbox, and worker/run binding in the three named files.
- [CODE-VERIFIED] Code comments quoted in sections 2-4 (for example "Coordinators start workers in their Run; active workers start helpers as themselves so reports return to their Dispatch without moving its mailbox", `worker-start-authority.ts:11`) agree with the executable logic traced.
- [CODE-CONTRADICTED]: none found in this assignment.
- [UNVERIFIED] The first sentence of research-notes.md:35 says the checkout is "identified by scope agent"; the identification of `/home/coder/workspaces/IronOrca` as the dev checkout was given in the assignment message, not independently confirmed here beyond git remote `IronbellyOrg/IronOrca` and the files existing.

### 7.3 Gaps (not investigated or not provable here)

1. Installed Orca parity with this commit: CLOSED in fix cycle 1 at source level. The installed build is a different, newer build (version `1.4.245-aidev02.9cfecdd30b2a`, 1048 commits ahead, section 1); the cited files are identical at its commit except the depth defaults and the `runUse` takeover check. Why it matters: a reference must not describe the older checkout as the installed build. Remaining: whether the minified bundle equals that commit's compiled output is not shown beyond the depth files and the `runCreate` and `worker-dispatch-start` heads (needs a rebuild or a live run: out of scope). Reference wording: "Source cited from the Orca development checkout `dc57b3d6e`; the installed build is `1.4.245-aidev02.9cfecdd30b2a`, whose source at the cited files is identical except the depth default (2) and the `runUse` takeover check."
2. Effective `nestedWorkerMaxDepth` in the running Orca settings: UNVERIFIED-DEPLOYED. Why it matters: it decides whether a worker's helper start is refused (section 5.2); at installed default 2 it is not, so WC-13 text is the only IronClaude-side barrier. Closure: needs the live Orca settings store, out of scope (reading a user profile is not authorized). Reference wording: "The effective nested-worker depth of the running Orca was not read; the installed files default to 2 and the development checkout to 1."
3. Test results: tests were not run (no Orca/test execution authorized); only describe/it titles at `structured-chat-worker-helpers.test.ts:104,105,222,245,260,293` were read. Why it matters: the end-to-end helper claim in section 6 rests on source reading. Closure: run that test file in the IronOrca checkout (writes caches; needs authorization, out of scope here). Reference wording: "Helper routing was read from source; the Orca test suite that exercises it was not run."
4. The federated `subWorkersInOwnRun` path (`federation.ts:196-217`) and `federated-worker-start` were not traced end to end. Why it matters: it must not be mistaken for sub-orchestration (section 5.3). Closure: a read-only trace of `federation.ts` and the remote start path in the IronOrca checkout, or live federation (out of scope). Reference wording: "Orca's federated own-Run helper text exists in preamble code; its runtime behavior was not traced."
5. `orchestration-caller-identity.ts`, `dispatch-lookup.ts:getActiveDispatchMailboxOwners`, `run-lookup.ts:getCurrentRunForCoordinator` internals: CLOSED in fix cycle 1 (read-only). `getActiveDispatchMailboxOwners` (`db/dispatch-context/dispatch-lookup.ts:54-`) selects `pending`/`dispatched` Dispatches by `assignee_handle`, then by exact `assignee_pane_key`, then by an equivalent pane key; `getCurrentRunForCoordinator` (`db/runs/run-lookup.ts:141-147`) returns the first of `runsBoundToCoordinator` (`:150-161`, by pane or Orca session id); `mailboxAddressOf` (`orchestration-caller-identity.ts:32-40`) prefers the terminal handle, else the session address. This supports the call-site claim "matched by address then pane" ([CODE-VERIFIED], dev checkout; the pane-equivalence fallback beyond `:84` was not read).
6. No IronClaude-side contract text was cross-checked in this file (assignment is Orca provenance only); cross-checks belong to files 01-04 and 06. Why it matters: none for correctness of Orca facts; the cross-checks are made in 01 section C (new "Orca source enforcement" note) and 03 section F. Closure: done there. Reference wording: n/a.

### 7.4 Stale-documentation list

- None identified for the three assigned files within the evidence read. Possible stale or missing: IronOrca checkout skills/docs do not mention `worker-start` helper start (section 6 last row); if the installed `orchestration` skill describes helper start, its parity with this source is UNVERIFIED.
- Stale in the FIRST PASS of this file (corrected in fix cycle 1): "helper start is refused under default settings", "nested-worker depth defaults to 1" and "the local code refuses exactly that for local Dispatches" were true only of the older checkout (depth) or false (run-create, section 4.2); the installed files default to 2. A reader of the earlier report's `:234` alone (default 1) is likewise reading the originally researched build, not the installed one.

### 7.5 Subordinate/sub-orchestrator mode

- Not implemented and not presented as shipped here. What the checkout implements is a bounded worker-started HELPER: a worker with an active Dispatch can start local helpers in the same Run (`worker-start-authority.ts:31-47,56-62`) when the depth setting allows it (checkout default 1 refuses; installed-file default 2 allows one helper level, section 5.2), and `workerRunBindingRefusal` stops a worker from binding its own or an ancestor Run and from using a takeover flag (`worker-run-binding.ts:52-71`). It does NOT stop a worker from creating a new Run (`runs.ts:31-55`, `run-create.ts:7-50`), so Orca source alone does not refuse a worker-turned-coordinator of its own new Run; the depth cap is the only barrier in source (corrected in fix cycle 1; the first pass said the local code "refuses exactly that"). Subordinate/sub-orchestrator mode therefore stays deferred because it is not built in IronClaude (no command, skill, flag or contract role) and is forbidden by contract rule WC-13 (`WORKER-CONTRACT.md:62`, text, not code-enforced), not because Orca refuses it. The federated preamble text (section 5.3) is unverified and must not be read as shipping IronClaude sub-orchestration.

## Key takeaways

1. Checkout provenance: `/home/coder/workspaces/IronOrca`, branch `main`, commit `dc57b3d6e81c9825446a520bf0aee8600a2f5586`, clean tree, origin `IronbellyOrg/IronOrca`.
2. `worker-start-authority.ts` lets only the Run's bound coordinator, or a worker on exactly one provable active Dispatch in that Run, call `worker-start`; workers get a local-only, same-Run helper with no `--on`/`--terminal` and no foreign Tasks.
3. `dispatch-report-mailbox.ts` routes `worker_done`/`heartbeat`/`escalation`/`status`/untyped reports to the live creator Dispatch, else the Run, recomputed on every send; gates and handoffs stay with the coordinator.
4. `worker-run-binding.ts` refuses a worker (and anyone descended from work in a Run) binding that Run and using takeover flags on the bind path, and gives workers plain `check`/`send` guidance. It is narrow: `orchestration.runCreate` has no worker check, so a worker can create and coordinate a NEW Run; the depth cap is the only source barrier.
5. Helper start is gated by `nestedWorkerMaxDepth`: default 1 in the checkout (refuses a worker's helper start) and default 2 in the installed build files (allows one helper level). The effective setting of the running Orca is UNVERIFIED-DEPLOYED. At the installed default, only contract rule WC-13 (text) bars a worker's helper start.

## Summary

Three development-source files in the IronOrca checkout (`main` at `dc57b3d6e81c9825446a520bf0aee8600a2f5586`, clean, version 1.4.214) define how a worker starts helpers, where helper reports land, and how a worker is kept from binding its own Run; all three are wired into live RPC, messaging, ask, escalation and run-binding paths, so no unwired-capability DEFECT was found. The installed Orca build files (`1.4.245-aidev02.9cfecdd30b2a`, 1048 commits newer) are identical at those files except the nested-worker depth default, which is 1 in the checkout (helper start refused) and 2 in the installed files (helper start allowed one level); the effective setting of the running Orca is UNVERIFIED. The run-binding refusal is narrow: a worker can create a new Run through `runCreate`, so the depth cap and contract rule WC-13 (text) are what limit nested coordination, not an Orca refusal. Test outcomes, the live setting and the federated own-Run preamble path are not observed. Sub-orchestrator mode remains unimplemented and contract-forbidden, not Orca-refused.

Status: Complete

