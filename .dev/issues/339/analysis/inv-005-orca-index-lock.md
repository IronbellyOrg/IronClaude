# INV-005: do Orca read verbs take `index.lock` in a live worker's worktree?

## Question

`/sc:sweep` will call Orca read verbs (`orchestration worker-list`, `orchestration worker-show`, `orchestration run-current`, `worktree list`, `worktree current`) and its own `git --no-optional-locks status --porcelain --branch`. A plain `git status` refreshes the index and briefly holds `index.lock`. For a linked worktree that file is `<common gitdir>/worktrees/<name>/index.lock`. WC-9 tells a worker that finds `index.lock` to report `blocked` with the path (`src/superclaude/core/WORKER-CONTRACT.md:44`). INV-005 (`BS/invariant-probe.md:11`) and GQ-103 (`.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/gaps-and-questions.md:126`) ask whether the Orca read verbs could take that lock inside a live worker's worktree, how likely that is, and what to do about it. The debate left it as an UNVERIFIED residual risk that needs owner sign-off (`BS/debate/round3-final-v3.md:34`).

`BS` = `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/adversarial/adversarial`.

Scope: the Orca build installed here. `/opt/Orca/resources/app.asar.unpacked/out/package.json` gives version `1.4.245-aidev02.780594c521aa`, commit `780594c521aaa2399b242b0022045017f4a77436`. No Orca command other than `--help` was run, and no git was run in any existing worktree. All Orca evidence is a static read of the shipped JavaScript.

## Verdict

**Unlikely.**

Deciding fact: each of these read verbs is a remote procedure call to the long-running Orca runtime. The runtime answers from its own database, its terminal (PTY) state and a cached `git worktree list --porcelain` run in the repository root. None of them runs `git status`, or any other index-writing git command, inside a worker worktree. Separately, the runtime's own background status polling opts out of optional locks (`GIT_OPTIONAL_LOCKS=0` or `--no-optional-locks`).

Why not "Ruled out": the trace stops at the second level of helper functions for the worker projections, not every leaf. It is a static read, not a live observation (a live check is forbidden here). Remote hosts were not traced. It holds for this Orca version only.

## Evidence

Path shorthand: `RES` = `/opt/Orca/resources`; `CLI` = `RES/app.asar.unpacked/out/cli`; `ORCAD` = `RES/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js`; `RUNNER` = `RES/app.asar.unpacked/out/main/chunks/runner-DFFK-DPE.js`; `MAIN` = `out/main/index.js` inside `RES/app.asar` (read from an extracted copy). The bundles are minified onto very few lines, so `@N` is a byte offset from `grep -bo`, not a line number.

**How the CLI reaches git**

- E1. VERIFIED. `orca-ide` runs the CLI under Electron's Node mode: `RES/bin/orca-ide:30` sets `CLI="$RESOURCES_DIR/app.asar.unpacked/out/cli/index.js"` and line 37 runs `ELECTRON_RUN_AS_NODE=1 exec "$ELECTRON" "$CLI" "$@"`.
- E2. VERIFIED. The CLI is a thin client. `CLI/runtime/client.js:116-121` reads runtime metadata and calls `sendRequest(metadata, method, params, ...)`. `client.js:90-101` is the remote websocket path. Only `openOrca` launches the app (`client.js:208-217`).
- E3. VERIFIED. A search of the CLI's `child_process` uses found none that runs git.
- E4. VERIFIED. The verb handlers send a method name and parameters, no environment. `worker-list` calls `orchestration.workerList` with `paginate`, `run`, `terminalState`, optional `includeRemote`, `cursor` and `limit` (`CLI/handlers/orchestration/worker-terminal-handlers.js:57-64`). `worker-show` calls `orchestration.workerShow` (`worker-observation-handlers.js:10-12`). `run-current` calls `orchestration.runCurrent` (`run-handlers.js:28-30`). `worktree ps`, `list`, `show` and `current` call `worktree.ps`, `worktree.list` and `worktree.show` (`CLI/handlers/worktree.js:49-50, 58-59, 66-67, 72-73`).

**Where the runtime takes its git environment**

- E5. VERIFIED. In `RUNNER` near @17551: `fn(e=process.env)` returns `{...e,GIT_OPTIONAL_LOCKS:"0"}` and is exported as `q` (call sites write `F.q()`). `z(e=process.env)` returns `{...e,...ye}`, where `ye` (@2834) adds only locale variables. The git spawner uses `env:z(...)` (@53902 area). So `GIT_OPTIONAL_LOCKS=0` is opt-in per call site, and the base environment is the runtime process's own `process.env`, never the CLI's.
- E6. VERIFIED. `RUNNER` @7106 lists the read git commands (`status`, `diff`, `rev-parse` and others). `RUNNER` @53902 sends non-read commands through Orca's own repository lock (`needsLock`). That lock is internal to Orca. It does not coordinate with git run by worker processes.

**Runtime handlers for the read verbs**

- E7. VERIFIED. `orchestration.runCurrent` (`ORCAD` @1365678) reads the orchestration database only.
- E8. VERIFIED. `orchestration.workerShow` (`ORCAD` @1447744) reads the database, may write the database (`markWorkerStartUnknown` / `markWorkerStopUnknown`), checks terminal liveness (`pG` @1419878, terminal state only) and builds a projection through `vG` and `_G` (@1423399).
- E9. VERIFIED. `orchestration.workerList` (`ORCAD` @1484595) reads the database and projects through `wK` and `l5e` (@1486569). A scan of the projection functions `l5e`, `_G`, `wK`, `vG`, `oW`, `iW`, `KG`, `fK`, `p3e`, `w6e`, `eW` and `r5e` found no git call.
- E10. VERIFIED. `worktree.list` (`ORCAD` @1122262) calls `listManagedWorktrees`, which reads a cached scan (`MAIN` @5189860 `listResolvedWorktrees`; @5191497 `listRepoWorktreesForResolution`, with `worktreeScanCache` and expiry times). `refreshRepoWorktreeScan` (`MAIN` @5195289) reuses results for 300000 ms after a cheap fingerprint probe. On a miss, `MAIN` @5194760 calls `ORCAD` export `Kg`, which is `Yb` (@668196). `Yb` runs `ab` (@651393): `git worktree list --porcelain -z` in the repository root. It then calls `DOe` (@667271) and `Lb` (@665537) per worktree. `Lb` finds the gitdir by reading the `.git` file with `fs` and reads `info/sparse-checkout` and `config` files. That sparse result is cached for 300000 ms (`wOe=3e5`, `ORCAD` @666899).
- E11. VERIFIED. `worktree.show`, used by `worktree show` and `worktree current`, calls `showManagedWorktree` (`MAIN` @4988108), then `resolveWorkspaceSelector` (@5175247) and `resolveGitWorktreeSelector` (@5181979). These use the cached rows from E10 and match the selector in memory.
- E12. VERIFIED. `worktree.ps` (`ORCAD` @1121974) calls `getWorktreePs` (`MAIN` @4945394), which combines the worktree snapshot (E10), PTY records and stored summaries. No git call was seen.

**Runtime `git status` and `git diff` call sites**

- E13. VERIFIED. All `status` argv sites in the runtime bundles were listed. Status polling `OTe`, fed by `xTe` (`ORCAD` @602820) and file watchers, uses `env:F.q()`. `ITe` (@606248), `status --porcelain=v2 --branch --untracked-files=all`, uses `env:F.q()`. `oOe` (@662984) uses `--no-optional-locks status`. `Gyt` (@2123487) uses `env:F.q()`. The only plain status is `lS` (@691352), `status --porcelain ... --untracked-files=all --ignore-submodules=none`, in the worktree-removal dirty check. That is a mutation path reached by `worktree rm`, not by a read verb.
- E14. VERIFIED. `git diff` sites: `dv` (`ORCAD` @598028) passes `-c diff.autoRefreshIndex=false` with `env:F.q()`, and `ECe` (@575279) passes `diff.autoRefreshIndex=false`. `lEe` (@620678, staging), `uy` (@622837, staged diff for a commit message), `Px` (@679854, branch merge check) and `MAIN` @2190148 (pull request text) are user-triggered actions, not read verbs.

**Git behavior (throwaway repository, git 2.47.3)**

- E15. VERIFIED. Command: a new `mktemp -d` repository under `/tmp` with a linked worktree `wt`, an inotify watch on `<repo>/.git/worktrees/wt`, and the tracked file touched before each case so the index is stale. Output:
  - plain `git status` in the worktree: `rc=0`, events `['create:index.lock', 'moved_from:index.lock', 'moved_to:index']`
  - `git --no-optional-locks status`: `rc=0`, events `[]`
  - `GIT_OPTIONAL_LOCKS=0 git status`: `rc=0`, events `[]`
  - `git worktree list --porcelain` in the repository root: `rc=0`, events `[]`
  - `git diff --name-only`, `git diff --cached`, `git rev-parse --git-dir`: `rc=0`, events `[]`

  Both temporary directories were deleted afterwards, and `ls` confirmed they were gone.
- E16. VERIFIED. Same setup with `index.lock` created first: `git add a.txt` printed `fatal: Unable to create '.../.git/worktrees/wt/index.lock': File exists. Another git process seems to be running...` with `rc=128` after 4 ms. `git commit --allow-empty` failed the same way with `rc=128` after 3 ms. Both plain and `--no-optional-locks` `git status` still exited 0 while the lock existed.
- E17. VERIFIED. `git help git` line 134: `--no-optional-locks` is the same as setting `GIT_OPTIONAL_LOCKS` to 0. Lines 1256-1260: `GIT_OPTIONAL_LOCKS` false "will prevent git status from refreshing the index", default 1. `git help status`, BACKGROUND REFRESH (lines 366-372): the lock taken for the refresh can make other simultaneous git processes fail.
- E18. VERIFIED. `git help config`: lock retry settings exist only for refs, `core.filesRefLockTimeout` (line 1889, default 100 ms) and `core.packedRefsTimeout` (line 1893, default 1000 ms), and for `reftable.lockTimeout`. None covers `index.lock`, which matches the immediate failure in E16.

**Help text**

- E19. VERIFIED. `orca orchestration worker-list --help`, `worker-show --help`, `run-current --help`, `orca worktree list --help` and `orca worktree current --help` all exited 0. None mentions git, locks or index refresh. `worktree current` "Resolves the current shell directory to a path: selector".

**Follow-up verbs (added 2026-11-08, same method and limits)**

- E20. VERIFIED. CLI handler `orchestration task-list` (`CLI/handlers/orchestration/task-handlers.js:32-44`) sends `orchestration.taskList` with `status`, `ready` (true when `--ready` is given), `brief`, `run` and `callerTerminalHandle`, and no environment. When `--run` is given, the caller handle comes from `runScopedSessionCaller` (`CLI/handlers/orchestration/terminal-identity.js:143-147`), which reads a flag and an injected session id only, with no extra call to the runtime. `--json` only changes printing (`task-handlers.js:53`).
- E21. VERIFIED. The runtime router (`ORCAD` @2462576) passes `orchestration.taskList` with a run straight to its registered handler (``if(e.method===`orchestration.taskList`&&a)return{handled:!1}``). The handler (`ORCAD` @1910713) calls `getOrchestrationDb()`, `getRun(e.run)`, then `CU` (@1355649), which with a run id and `requireCurrentConsumer` false returns that database row at once. It then calls `listTasksWithDispatch({status, ready, runId})` and, for `--brief` only, `Hut` (@1905584), which shortens the `spec` text.
- E22. VERIFIED. `listTasksWithDispatch` is `qct` (`ORCAD` @1824828, bound at @1825864). It builds one SQL `SELECT t.*, d.assignee_handle, d.id FROM tasks t LEFT JOIN dispatch_contexts d ...` with `t.run_id = ?` and, for `--ready`, `t.status = 'ready'`, and returns `this.db.prepare(r).all(...)`. No git, file system or process call.
- E23. VERIFIED. `--ready` and plain `task-list` differ only in that one `WHERE` clause (E22). Neither writes the database on this path (no `$(this.db, ...)` transition call in `qct`, unlike `promoteReadyTasks` next to it).
- E24. VERIFIED. `getWorktreePs` (`MAIN` @4945400) calls, in order: `listResolvedWorktreeSnapshot` (@5189950, the cached snapshot from E10 through `computeResolvedWorktrees` @5190128), `visibleResolvedWorktreeSnapshot` (@4946940, settings filter), `refreshPtyWorktreeRecordsFromController` (@5202469) and `refreshPtyWorktreeRecordsWithControllerInventory` (@5205305, terminal daemon process inventory through `listPtyControllerInventory` @5202790), then `Ahr` (@4904256, store reads; its only `git` text is the label ``workspaceKind:`git` ``), `Mhr`, `Nhr`, `Ihr`, `zhr`, `Rhr`, `K6n`, `Ghr`, `C9n` and, when terminal waits are requested, `Khr`. The structured summary reader `readStatusSummary` reads a published status feed (`CH/structured-agent-session-host-assembly-Bf2xth4M.js` @296699 `readStatusSummary=e=>this.statusFeed.readPublished(e)`).
- E25. VERIFIED. A brace-matched body scan of those functions and their second-level callees (`Fhr`, `j5`, `M5`, `y9n`, `Phr`, `Lhr`, `Uhr`, `Whr`, `S9n`, `w9n`, `G6n`, `jhr`, `PSr`, `repoWorktreeRowDeps`, `refreshPtyForegroundAgent`, `refreshFloatingWorkspacePtyLiveness`, `makeRuntimePaneKey`, `paneOfPty`, `getPtyTitleDisplayClear`, `getPtyLivenessVerdict`, `getExistingTerminalHandlesForPtyId`, `listKnownExecutionHostIds`, `buildRuntimeVisibilitySourceMatchersByRepoId`, `isRuntimeWorktreeVisible`) found none of: `execFile`, `spawn(`, `child_process`, a `` [`status` `` argv, `--porcelain`, `` `worktree`,`list` ``, `GIT_OPTIONAL_LOCKS`, `no-optional-locks`, `update-index`, `.Kg(`. The CLI sends only `limit`, plus `includeAgentWait` when both `--json` and `--agent-wait` are given (`CLI/handlers/worktree.js:49-53`); that flag turns on `Khr`, which reads terminal wait state. `--json` alone changes printing only. The functions `Ahr` calls through the `s.` module (`s.Yu`, `s.Ku`, `s.Xu`, `s.QC`, `s.zC`) were not opened; UNVERIFIED, though their call sites only pass store rows.

## Per-verb table

| Verb | Served from | Git command run | Takes `index.lock`? | Evidence |
|---|---|---|---|---|
| `orchestration run-current` | Runtime database | None | no | E4, E7 |
| `orchestration worker-show` | Runtime database plus terminal liveness; may write the database, not git | None found to the second helper level | no | E4, E8 |
| `orchestration worker-list` | Runtime database and projections | None found to the second helper level | no (local); unknown with `--include-remote` | E4, E9 |
| `worktree list` | Runtime cache; on a miss, git in the repository root plus `fs` reads | `git worktree list --porcelain -z` in the repository root | no | E10, E15 |
| `worktree current` / `worktree show` | The same cached rows, matched in memory | As `worktree list`, on a cache miss only | no | E11, E15 |
| `worktree ps` / `worktree ps --json` (named in INV-005) | Cached rows plus PTY records and stored summaries | As `worktree list`, on a cache miss only | no | E12, E24, E25 |
| `orchestration task-list --run <run> --json` | Runtime database (one SQL `SELECT`) | None | no | E20, E21, E22, E23 |
| `orchestration task-list --ready --run <run> --json` | Runtime database (the same `SELECT` with `status = 'ready'`) | None | no | E20, E21, E22, E23 |
| Sweep's own `git --no-optional-locks status --porcelain --branch` | Live git in each worktree | That command | no | E15, E17 |

## Background Orca git activity

This runs whether or not the sweep calls Orca, so it is not a sweep effect, but it shares the worker's repository.

- Status polling, driven by file watchers, always uses `GIT_OPTIONAL_LOCKS=0` or `--no-optional-locks` (E13). Diff counts use `diff.autoRefreshIndex=false` (E14). VERIFIED that these do not take `index.lock`.
- Ref maintenance runs `git pack-refs --all --prune` (`qEe`, `ORCAD` @632885). It is turned off by `ORCA_DISABLE_REPO_REF_MAINTENANCE=1` (`TDe`, @652324), and it pauses while Orca runs its own pull, fetch or fast-forward. It takes `packed-refs.lock` and ref locks in the common gitdir, not `index.lock` (VERIFIED from the argv). Nearby constants are 1 h, 30 min, 12 h and 6 h (`HEe=36e5`, `UEe=18e5`, `WEe=432e5`, `jy=216e5`); which one is the interval is UNVERIFIED. A collision with a worker's commit is covered by git's ref retries (100 ms per ref, 1000 ms for `packed-refs`, E18), unless pack-refs holds the lock longer, which is UNVERIFIED. This is outside WC-9's `index.lock` rule.
- No automatic fetch was found. `fetch --prune` (`ORCAD` @659458) is on the user pull and fetch path only.
- Index-writing git (`add`, `commit`, the removal check `lS`) runs only when a person acts in Orca's source-control or worktree interface, or on `worktree rm` (E13, E14). If a person stages files in Orca on a worker's worktree, the worker can see `index.lock`. That is a human action, not the sweep.

## How bad a hit is

- Duration: a plain `git status` creates `index.lock`, writes the refreshed index into it and renames it over `index`, all in one run (E15). The lock lasts for the refresh and write. In a one-file repository that was a few milliseconds. For a worker-sized repository the duration is UNVERIFIED; it grows with the number of tracked files.
- What the worker sees: a git command that writes the index (`add`, `commit`, `checkout`, `merge`, `reset`, `stash`) fails at once with exit 128 and `Unable to create '<gitdir>/worktrees/<name>/index.lock': File exists.` (E16). Git does not retry `index.lock` (E18). Read-only git in the worker is not affected (E16).
- Contract effect: under WC-9 (`WORKER-CONTRACT.md:44`) the worker reports `blocked` with the path. A collision lasting milliseconds would become a false `blocked` that stops the Task until the coordinator looks at it.
- Stale lock: the lock outlives the command only if the git process dies mid-write. The sweep's own git cannot cause this, because `--no-optional-locks` never creates the file (E15).

## Mitigations ranked

1. **Limit the sweep to verbs proven store-served.** Allow only `run-current`, `worker-list` without `--include-remote`, `worker-show`, `worktree list` and `worktree current`, and pin that allowlist in a test. Evidence: E7 to E12 and the per-verb table. Cost: low, one allowlist and one test. Record the checked Orca version so the claim stays scoped to it. Change type: sweep-only.
2. **Skip Orca for any per-worktree git state and use our own `--no-optional-locks` git.** No allowed verb runs git in a worker worktree today, so this is a rule for later design changes: dirty state and branch come from `_git`, never from an Orca summary or source-control call. Evidence: E15 and E17 show the flag stops the lock. Cost: none, it is already GQ-103's first safety item. Change type: sweep-only.
3. **WC-9: retry a short-lived lock before reporting `blocked`.** On meeting `index.lock`, wait a bounded time (for example up to a few seconds), check again, and report `blocked` only if the lock is still there. Evidence: a reader's lock is created and removed within one command (E15), and git never retries it (E18). Without this, any brief collision from any source (a person in Orca's interface, an editor, another tool) becomes a false `blocked`. Cost: a contract edit and a test; a stale lock is still reported, a little later. Change type: neither Orca nor sweep; a worker-contract change (`WORKER-CONTRACT.md:44`) that needs owner approval.
4. **Ask the Orca project to pass `--no-optional-locks` everywhere and document it.** Orca already does this on its read and background status paths (E13); only the removal check `lS` uses plain status. The useful request is a documented promise that read verbs never take optional git locks, so it survives later versions. ("Upstream" here means the Orca project, never the SuperClaude upstream.) Cost: outside our control and timeline. Change type: Orca change.
5. **Run the sweep only when no worker is in a git write phase.** No signal for "in a git write phase" was found in the worker projections (UNVERIFIED that one exists), and any check races: a worker can start `git commit` right after it. With mitigations 1 and 2 the sweep takes no lock, so this adds cost without lowering risk. Change type: sweep-only. Not recommended.
6. **Export `GIT_OPTIONAL_LOCKS=0` to the `orca` call.** Does not work. The CLI runs no git (E3), sends only method and parameters (E2, E4), and the runtime builds git's environment from its own `process.env` (E5). The variable never reaches the git Orca runs. It would only matter if set where the Orca runtime starts, which is a settings change outside this work, and the runtime already opts out where it matters (E13). Change type: sweep-only, but it gives false assurance. Do not adopt; this matches the debate's decision not to require it (`round3-final-v3.md:34`).

## Recommendation for the design stage

- Adopt mitigations 1 and 2 as requirements: a fixed `_orca` read-verb allowlist pinned by a test, and all per-worktree git state from `_git` with `--no-optional-locks`.
- Replace `Orca read verbs' git effects on worker worktrees: UNVERIFIED` with a scoped claim, for example `unlikely (static check of Orca <version>, see inv-005-orca-index-lock.md)`, and fall back to UNVERIFIED when the installed Orca version differs.
- Do not add `GIT_OPTIONAL_LOCKS=0` to `_orca` or a test for it (mitigation 6).
- Offer mitigation 3, a bounded WC-9 retry, to the owner as a separate contract change. It covers lock sources the sweep cannot control.
- The owner sign-off required by `round3-final-v3.md:34` still applies. This report is evidence for that decision, not a replacement for it.

## Negative evidence

Searched and not found:

- Any git spawn in the CLI (E3).
- Any runtime `git status` without the optional-lock opt-out, other than the removal check `lS` (E13).
- Any git call in the worker projection helpers checked (E9) or on the `worktree ps` path (E12).
- Any automatic background fetch.
- Any mention of `index.lock`, optional locks or `worktree ps` in the installed `orca-cli` and `orchestration` SKILL.md files.
- Any git or lock note in the `--help` text of the five verbs (E19).
- Any `index.lock` event from `git worktree list`, `git diff`, `git diff --cached` or `git rev-parse` (E15).

Not checked, so not claimed:

- Helper functions deeper than the second level below the worker projections.
- Remote, SSH and WSL host paths, including what a remote runtime does for `--include-remote`.
- Any live run of an Orca read verb (forbidden for this investigation).
- Lock hold time in a large repository.

## Open questions

1. Do any helpers below the second level call git? Cheap to close with the same static scan.
2. What is the ref-maintenance interval, does it run on repositories with live workers, and can `pack-refs` hold `packed-refs.lock` longer than git's 1000 ms retry during a worker commit? This is a ref lock, outside WC-9's `index.lock` rule.
3. How long does a plain `git status` hold `index.lock` in a worker-sized repository? This matters only for lock sources other than the sweep.
4. Does a remote host's runtime keep the same behavior for `worker-list --include-remote`? Until that is known, the sweep should not pass that flag.
5. Will later Orca versions keep these properties? Re-run this static check, or get mitigation 4, when the installed version changes.

## Addendum 2026-11-08: task-list and worktree ps

Checked with the same method and limits: static reads of the shipped code only, no Orca command run, no git in any worktree. `out/main/index.js` was extracted again into a private temporary directory and deleted afterwards.

- `orchestration task-list --run <run> --json`: served from the store. One SQL `SELECT` on the orchestration database (E20 to E22). Runs no git. Cannot take `index.lock`.
- `orchestration task-list --ready --run <run> --json`: the same path with one extra `WHERE t.status = 'ready'` (E23). Runs no git. Cannot take `index.lock`.
- `worktree ps --json`: re-confirmed to the second helper level (E24, E25). Cached worktree rows, terminal daemon inventory, store records and a status feed. Its only git is the cached `git worktree list --porcelain -z` in the repository root on a cache miss (E10), which takes no `index.lock` (E15).

Both `task-list` forms can join the mitigation 1 allowlist. Keep passing `--run`: without it the CLI first resolves the coordinator terminal through another runtime call, which was not traced here. The new evidence does not contradict the verdict; it stays **Unlikely**.
