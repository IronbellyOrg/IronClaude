feef7cef998a2b6175e6e9063e9cc2bc9a3dd0eb
Review one task for spec compliance.

Task brief: ## Task 7: Trace Orca's nesting-depth enforcement and read the depth setting (AC-0.7, AC-C6)

Read-only, no live probe. Start from the AC-0.7 starting points in `./source.md` section 7.3 (the block below the table): `grep -rlE 'nested_worker_depth_exceeded|NESTED_WORKER_DEPTH_EXCEEDED_CODE' /opt/Orca/resources/app.asar.unpacked/out/`. From there, trace which calls check nesting depth (`worker-start`, `dispatch`, `task-create`, low-level dispatch, `worktree create --agent`, `agent launch`) and what depth Orca gives a session the person opens (expected 0). Then run the AC-C6 check from `./source.md` section 7.1: `grep -ho '"nestedWorkerMaxDepth":[0-9]*' "${ORCA_RUNTIME_SOURCE_PROFILE_PATH:-$HOME/.config/orca}"/profiles/*/orca-data.json`.

Acceptance criteria:
- `./artifacts/ac-0.7-depth-trace.md` lists each call as checked, not checked or not found, and the depth of a person-opened session, each with a `path:line` in Orca's installed code. Any call not checked is recorded as covered only by WC-13 and 7.2 step 5.
- `./artifacts/ac-c6-depth-setting.txt` holds the AC-C6 output, and every printed line is `"nestedWorkerMaxDepth":1`. Any profile that prints nothing is recorded as using Orca's presumed default of 1.

AC ids, in the order of the Acceptance criteria bullets: T7.AC1, T7.AC2.
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
Start sha: feef7cef998a2b6175e6e9063e9cc2bc9a3dd0eb
Diff against the start snapshot: Files present in the start tree (diff against the start tree):
```diff
```
New untracked files written by this task (absent from the start tree; the whole file is the diff, Read each in full from disk):
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-0.7-depth-trace.md
- /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-c6-depth-setting.txt

Delta diff from the previous reviewed tree (empty on the first review): ```diff
diff --git a/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-0.7-depth-trace.md b/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-0.7-depth-trace.md
index b9210861..abcb99a8 100644
--- a/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-0.7-depth-trace.md
+++ b/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-0.7-depth-trace.md
@@ -27,7 +27,19 @@ Output (exit 0):
 - `BUNDLE:645` col 1775, `function SZe` (`resolveCreatorDepth`): a `system` creator is depth 0; a terminal creator takes the depth of its active dispatch and of any live remote attachment, and is 0 when it has none.
 - `BUNDLE:1828`: the dispatch table comment "Nesting depth: a root coordinator's worker is 1, its worker's worker is 2."
 
-Every call of `resolveChildDispatchDepth`, `createDispatchContext` and `createStartingWorkerDispatch` in `out/` is in `BUNDLE` (a recursive `grep -rln` for the three names lists only that file). The call sites are `BUNDLE:650` col 3344 (`createDispatchContext`), `BUNDLE:2443` col 321 (`createStartingWorkerDispatch`), `BUNDLE:2548` col 7735 (dispatch dry run), `BUNDLE:578` col 24175 and `BUNDLE:590` col 23752 (worker start). No other code path calls the check.
+Every call of `resolveChildDispatchDepth`, `createDispatchContext` and `createStartingWorkerDispatch` in `out/` is in `BUNDLE` (a recursive `grep -rln` for the three names lists only that file). A scan of `BUNDLE` for calls of the three methods (`.resolveChildDispatchDepth(`, `.createDispatchContext(`, `.createStartingWorkerDispatch(`) finds seven call sites:
+
+| Call site | What it is | Reached from |
+|---|---|---|
+| `BUNDLE:650` col 3344 | `resolveChildDispatchDepth`, first statement of `createDispatchContext` (`PZe`) | the two `createDispatchContext` calls below |
+| `BUNDLE:2443` col 321 | `resolveChildDispatchDepth`, inside `createStartingWorkerDispatch` (`L4e`) | the two `createStartingWorkerDispatch` calls below |
+| `BUNDLE:2548` col 7735 | `resolveChildDispatchDepth`, `--dry-run` branch | `orchestration.dispatch` handler |
+| `BUNDLE:2548` col 9095 | `createDispatchContext` | `orchestration.dispatch` handler (plain and `--inject`) |
+| `BUNDLE:2548` col 19170 | `createDispatchContext` with `creator:{kind:`system`}` and `maxDepth: nestedWorkerMaxDepth`, in `p6e` | Orca's own coordinator loop: the `orchestration.run` handler (`BUNDLE:2548` col 24898) starts loop class `g6e` (`BUNDLE:2548` col 20394), which calls `p6e` (`BUNDLE:2548` col 23922). A `system` creator is depth 0, so its workers are depth 1. |
+| `BUNDLE:578` col 24175 | `createStartingWorkerDispatch` in `mKe` | `orchestration.workerStart` handler (remote environment) |
+| `BUNDLE:590` col 23752 | `createStartingWorkerDispatch` in `EYe` | `orchestration.workerStart` handler (local) |
+
+These seven are every call of the three methods in `out/`. The `orchestration.run` loop is checked too, though it is not one of the six calls AC-0.7 names. This trace does not claim that no other code creates dispatch records: for example, a remote federation attach (`orchestration.federationAttachStart`) receives a depth from the home peer instead of calling these methods, and it was not traced further.
 
 ## Per call
 
```
Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B2 ac=T7.AC1 at=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-0.7-depth-trace.md:30 anchor=/opt/Orca/resources/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-BKoqlqOo.js:2548 chk=n,y,n,n family=incomplete-call-site-enumeration fix=Add BUNDLE:2548 col 19170 (createDispatchContext in function p6e, the orchestration.run coordinator loop, creator {kind:`system`}) to the call-site list, or drop the sentence "No other code path calls the check." covers="lists each call as checked, not checked or not found" first=A1 origin=new: The trace lists five call sites and then says "No other code path calls the check." That is false. The bundle has a sixth: `createDispatchContext` at line 2548, column 19170, inside `p6e`. That is the automatic coordinator loop behind `orchestration.run`, and it dispatches with a `system` creator (depth 0, so the child is depth 1). This path is not one of the six calls the AC names, so the per-call results and the depth value are still correct. Only the claim that the list is complete is wrong.
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
