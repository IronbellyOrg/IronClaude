# AC-0.7: where Orca enforces nested-worker depth (read-only trace)

Read-only trace of Orca's installed code on 2026-11-03. No live probe was run and no Orca command that starts, sends or creates anything was used.

- Orca version: `orca --version` prints `1.4.237-aidev02.0e4491a95e92`.
- Code root: `/opt/Orca/resources/app.asar.unpacked/out/`, written below as `out/`.
- The main bundle is minified, so each `path:line` is followed by the column where the cited code starts. Bundle checksum: `md5 9084dbc3ccb03eda2a36db54eeb8d5b2  out/main/chunks/orcad-migration-source-retention-BKoqlqOo.js` (written below as `BUNDLE`).

## Starting points (`./source.md` section 7.3, AC-0.7 block)

```sh
grep -rlE 'nested_worker_depth_exceeded|NESTED_WORKER_DEPTH_EXCEEDED_CODE' /opt/Orca/resources/app.asar.unpacked/out/
```

Output (exit 0):

```text
/opt/Orca/resources/app.asar.unpacked/out/shared/nested-worker-depth.js
/opt/Orca/resources/app.asar.unpacked/out/cli/bundled-skill-guides.js
/opt/Orca/resources/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-BKoqlqOo.js
```

## The check itself

- `out/shared/nested-worker-depth.js:11`: `NESTED_WORKER_MAX_DEPTH_DEFAULT = 1`. Line 13: `ROOT_DISPATCH_DEPTH = 0`, with the comment at line 12, "Root coordinators are depth 0; the first generation of workers is depth 1". Line 14: the error code `nested_worker_depth_exceeded`. Lines 30-35: a missing or invalid setting falls back to 1.
- `BUNDLE:650` col 243, `function wZe` (registered as `resolveChildDispatchDepth` at `BUNDLE:650` col 476, in `TZe`): the child depth is `resolveCreatorDepth(creator) + 1`, and when it exceeds the maximum it throws `nested_worker_depth_exceeded` ("Sub-worker dispatch is not permitted at depth ...") with `effectsApplied:!1`, so nothing is created.
- `BUNDLE:645` col 1775, `function SZe` (`resolveCreatorDepth`): a `system` creator is depth 0; a terminal creator takes the depth of its active dispatch and of any live remote attachment, and is 0 when it has none.
- `BUNDLE:1828`: the dispatch table comment "Nesting depth: a root coordinator's worker is 1, its worker's worker is 2."

Every call of `resolveChildDispatchDepth`, `createDispatchContext` and `createStartingWorkerDispatch` in `out/` is in `BUNDLE` (a recursive `grep -rln` for the three names lists only that file). A scan of `BUNDLE` for calls of the three methods (`.resolveChildDispatchDepth(`, `.createDispatchContext(`, `.createStartingWorkerDispatch(`) finds seven call sites:

| Call site | What it is | Reached from |
|---|---|---|
| `BUNDLE:650` col 3344 | `resolveChildDispatchDepth`, first statement of `createDispatchContext` (`PZe`) | the two `createDispatchContext` calls below |
| `BUNDLE:2443` col 321 | `resolveChildDispatchDepth`, inside `createStartingWorkerDispatch` (`L4e`) | the two `createStartingWorkerDispatch` calls below |
| `BUNDLE:2548` col 7735 | `resolveChildDispatchDepth`, `--dry-run` branch | `orchestration.dispatch` handler |
| `BUNDLE:2548` col 9095 | `createDispatchContext` | `orchestration.dispatch` handler (plain and `--inject`) |
| `BUNDLE:2548` col 19170 | `createDispatchContext` with `creator:{kind:`system`}` and `maxDepth: nestedWorkerMaxDepth`, in `p6e` | Orca's own coordinator loop: the `orchestration.run` handler (`BUNDLE:2548` col 24898) starts loop class `g6e` (`BUNDLE:2548` col 20394), which calls `p6e` (`BUNDLE:2548` col 23922). A `system` creator is depth 0, so its workers are depth 1. |
| `BUNDLE:578` col 24175 | `createStartingWorkerDispatch` in `mKe` | `orchestration.workerStart` handler (remote environment) |
| `BUNDLE:590` col 23752 | `createStartingWorkerDispatch` in `EYe` | `orchestration.workerStart` handler (local) |

These seven are every call of the three methods in `out/`. The `orchestration.run` loop is checked too, though it is not one of the six calls AC-0.7 names. This trace does not claim that no other code creates dispatch records: for example, a remote federation attach (`orchestration.federationAttachStart`) receives a depth from the home peer instead of calling these methods, and it was not traced further.

## Per call

| Call | Result | Evidence |
|---|---|---|
| `worker-start` | checked | Handler `orchestration.workerStart` at `BUNDLE:590` col 28676 calls `EYe` (`BUNDLE:590` col 29974, local) or `mKe` (`BUNDLE:590` col 29833, remote environment). Both call `createStartingWorkerDispatch({creator:..., maxDepth: getNestedWorkerMaxDepth()})` (`BUNDLE:590` col 23752; `BUNDLE:578` col 24175). That method is `L4e` (`BUNDLE:2439` col 2952, registered at `BUNDLE:2447` col 542), which sets `depth: this.resolveChildDispatchDepth(e.creator, e.maxDepth)` at `BUNDLE:2443` col 321, so an over-depth start throws before the dispatch row is inserted. |
| `dispatch` | checked | Handler `orchestration.dispatch` at `BUNDLE:2548` col 7030. A `--dry-run` resolves the depth with `resolveChildDispatchDepth` (`BUNDLE:2548` col 7735). A real dispatch calls `createDispatchContext({... creator, maxDepth: getNestedWorkerMaxDepth()})` at `BUNDLE:2548` col 9095. That method is `PZe` (`BUNDLE:650` col 3232), whose first statement calls `resolveChildDispatchDepth` (`BUNDLE:650` col 3344). |
| low-level dispatch (`dispatch --to <handle> --inject`) | checked | Orca's own guide calls `dispatch --inject` the low-level route and says never to "use it to route around the nested-depth limit" (`out/cli/bundled-skill-guides.js:46`). It is the same `orchestration.dispatch` handler: the `--inject` precondition (`stable_pane_required`) is checked first, then the same `createDispatchContext` call at `BUNDLE:2548` col 9095 runs, so the depth check applies. |
| `task-create` | not checked | Handler `orchestration.taskCreate` at `BUNDLE:2548` col 4872 resolves the Run and calls `createTask(...)` only. It calls none of the three depth functions, so a worker session at depth 1 is not refused by depth when it creates a Task. |
| `worktree create --agent` | not checked | Handler `worktree.create` at `BUNDLE:244` col 27387. Its code names no dispatch or depth function (it records an `agentTerminalHandle` only), and none of the depth call sites listed above is reached from it. |
| `agent launch` | not checked | Handler `agent.launch` at `BUNDLE:2568` col 82175 calls `R_t` (`BUNDLE:2568` col 82446) or `m5` (`BUNDLE:2568` col 82335). Neither calls a depth function, and no depth call site lies in that region. |

The three calls that are not checked (`task-create`, `worktree create --agent`, `agent launch`) are covered only by WC-13 (the worker session never makes these calls, at any depth setting) and by `./source.md` section 7.2 step 5 (the transcript check that the worker session made no `worker-start`, `dispatch` or `task-create` call and no `orca-cli` `worktree create --agent` or `agent launch` call).

## Depth of a session the person opens

0. A person-opened coordinator session is a terminal with no active dispatch and no remote attachment, so `resolveCreatorDepth` returns 0 for it (`BUNDLE:645` col 1775; the same value as `ROOT_DISPATCH_DEPTH = 0` at `out/shared/nested-worker-depth.js:13`). A Task it dispatches gets depth 0 + 1 = 1, which the default maximum of 1 allows (`BUNDLE:650` col 243). A worker at depth 1 that dispatches would need depth 2 and is refused. This matches the spec's expected value (`./source.md` section 7.3, AC-0.7: "expected 0").
