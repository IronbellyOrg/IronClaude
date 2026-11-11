# Spec panel round 2: independent re-review of orca-worker-contract-spec.md

- Task: task_07a4ccee1042 (dispatch ctx_e20d46b8ab3c), Task 7 of the Orca command-refactor run
- Reviewer: independent worker; did not write or revise the spec
- Spec reviewed: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (revised, v2)
- Inputs: `review/spec-panel.md` (round 1), `review/disposition.md`, `inventory/*.md`
- Date: 2026-11-09

## Method
- Ledger: `ledger.json` via `status` (2026-11-09): `phase: verify`, `review_header: "review: 2 of 3"`, 13 rows `fixed`, 4 `deferred`, `snapshots_intact: true`, no unclaimed hunks. `cmp snapshots/r2.md` against the live spec: identical (sha256 `347e32c2...d9bd`). This session ran only `status` and `verify --dry-run`; every ledger write belongs to the coordinator's ledger step (`~/.claude/commands/sc/spec-panel-ledger.md:258`, Setup bullet).
- Repo root: `/home/coder/workspaces/worktrees/IronClaude/exp346-v-ledger` (the brief's root). Spec lines are cited `spec:N` (live file = `snapshots/r2.md`); `plan:N` = `specs/orca-worker-contract-spec.review-ledger/plan-r2.md`.
- Every source citation in section 2 was re-read on 2026-11-09 with `sed -n`/`grep -n`; Orca facts with `orca orchestration worker-list --help` and `worker-show --help` (this is an Orca terminal, so bare `orca` is correct here).
- Stance: adversarial. For each fix: does the new text remove the round-1 wrong outcome, and does it create a new one?

## 1. Round-1 finding resolution table
"Resolved" is judged from the spec text, not from `disposition.md`. `touched_ok: no` means the fix text itself carries a new defect, filed in section 3 with that row as parent.

| Row | Round-1 wrong outcome (`review/spec-panel.md`) | Spec text now (`spec:N`) | Resolved? | touched_ok | Notes |
|---|---|---|---|---|---|
| R1 | workflow refuses `--output`, path unknown before dispatch, no yaml on pre-creation STOP (`spec-panel.md:76`) | workflow row adds `--report-dir <dir>`; WC-4 report `<report-dir>/worker-contract.yaml` "written on every outcome, including a pre-creation STOP" (`spec:95`) | Yes | yes | Source confirms the premise: `--output` retired (`sk/sc-workflow-protocol/SKILL.md:24`), no yaml on pre-creation STOP (`SKILL.md:26`, `refs/return-contract.md:39`). AC-1.4 wording now lags (new finding 13, minor). |
| R2 | 7.2 step 4 rejects `status: success`, or renaming breaks readers (`spec-panel.md:77`) | WC-4a: existing `return-contract.yaml` kept as is; WC-4 report is separate `worker-contract.yaml` (`spec:63`) | Yes | yes | Readers confirmed (`managed-workspace.md:10`, `reflect/refs/remediation-handoff.md:75`, `auggie/refs/remediation-handoff.md:77`). AC-1.1 no longer checks the new filename for these five (new finding 14, minor). |
| R3 | TFEP and WC-4 schemas share one path under `/sc:task` (`spec-panel.md:78`) | New TFEP row: troubleshoot's WC-4 report is `<output-dir>/worker-contract.yaml`; `/sc:task` must give TFEP a different `<output-dir>` (`spec:93`) | Yes for troubleshoot's own files | no | The `/sc:task` half of the fix is tagged P1, but `/sc:task` is a P2 command and its own row has no matching text, so the collision can return through task's own WC-4 report (new finding 2). |
| R4 | `<output-dir>` undefined for `--output <file>` (`spec-panel.md:79`) | WC-4a: file flag gives `<file>.return-contract.yaml` (`spec:63`) | Yes for tdd and init-lite | no | The sibling rule "A command with no output flag uses the report flag its section 3 row names" points at rows that name no flag (new finding 1). |
| R5 | adversarial path contradicts WC-4 path checked by 7.2 step 3 (`spec-panel.md:80`) | adversarial row: existing contract at `<output>/adversarial/return-contract.yaml`; WC-4 report `<output>/worker-contract.yaml`, "the path 7.2 step 3 checks" (`spec:85`) | Yes | yes | One WC-4 path per command now. |
| R6 | AC-0.4 step 3 needs a contract that arrives in P1 (`spec-panel.md:81`) | AC-0.4: P0 uses the existing report wherever 7.2 names the WC-4 report; step 3 restated; step 4 not run (`spec:197`) | Yes for step 3 | yes | P0 still cannot pass, now through step 6 after the R12 rewrite (new finding 8, parent R12). |
| R7 | retry overwrites attempt 1 or writes to an unrecorded directory (`spec-panel.md:82`) | WC-6: same-path re-run, "attempt started, not finished" report at start, final report names only this attempt's files (`spec:65`) | Yes | yes | Retry is the same Task (`CAPS:116`). Brief reuse is still UNVERIFIED (disposition UNVERIFIED 1). |
| R8 | answer has no route for flagless gates; re-run changes report path (`spec-panel.md:83`) | WC-3: gate flag when one exists, else folded into main input; person-only gates end blocked; output flag kept (`spec:61`) | Yes | no | Quoted sources hold (`cmd/task.md:93`, `cmd/recommend.md:44`, `sk/tdd/SKILL.md:52-61`). But naming tdd's topic gate as an `ask` route makes AC-2.2's required `--outcome failed` depend on the worker's choice (new finding 4). |
| R9 | `/sc:auggie-review --unattended` posts between P1 and P2 (`spec-panel.md:84`) | P1 row: P2-P4 commands "do nothing under `--unattended` until its own phase except write its WC-4 report with `status: blocked`" (`spec:162`) | Yes for auggie-review | no | auggie-review already takes `--output-dir`, so it can write the report. Several P2-P4 commands get their output flag only in their own phase, so their P1 blocked report has no known path (new finding 5). |
| R10 | improvising worker passes 7.2 step 5 and AC-0.4 (`spec-panel.md:85`) | WC-7a requires the Skill call (`spec:67`); AC-0.4 checks the transcript for it (`spec:197`) | Yes (requirement exists; P0 checks it) | yes | 7.2 step 5 still checks only `AskUserQuestion` (`spec:187`), so P1-P4 live checks pass an improvising worker (new finding 10, outside the hunks). |
| R11 | subagent call or 300 s call blocks heartbeat, unchecked (`spec-panel.md:86`) | WC-10: no call of 4 minutes or more; subagent heartbeat UNVERIFIED and recorded in AC-0.4; coordinator liveness rule (`spec:70`) | Yes for the 300 s case and the recording | no | New boundary contradiction at exactly 240 s (new finding 6); the substitute liveness rule cannot detect a hung subagent (new finding 7). |
| R12 | step 6 fails on any other untracked file; staging collision (`spec-panel.md:87`) | 7.2 step 6: before/after comparison; staging workers never share a worktree (`spec:188`) | Yes for P1-P4 | no | The rewrite dropped the old "command's documented artifacts" allowance, and P0 has no WC-4 report with `report_path`/`artifacts`, so AC-0.4's troubleshoot and workflow runs fail step 6 (new finding 8). |
| R13 | `^-[^-]` misses deleted bullets (`spec-panel.md:88`) | AC-C5: `git diff --numstat` deleted count is `0` (`spec:179`) | Yes | no | Re-tested 2026-11-09 in a scratch repo: deleting `- item two` gave grep rc=1 and `--numstat` `0 1 f.md`, so the new check works. The spec's own record "printed `1 1`" is wrong for a deletion (`1 1` is what a one-line edit prints) (new finding 9, minor). AC-0.3 still shows the old grep (new finding 12, minor). |
| R14-R17 | minor, stored `deferred` | unchanged (`spec:4`, `spec:59`, `spec:64`, `spec:175`) | Not answerable this cycle (deferred) | n/a | Still true: for example `spec:4` still names `.../OrcaCLICommandRefactor-Specs`. Deferred rows never block under the ledger profile. |

## 2. Citation check (citations added or changed by the revision)
Scope: every citation in the 12 revised hunks (`plan:16-227`). "OK" means the live line says what the spec says.

| # | Spec location | Citation | Read on 2026-11-09 | Result |
|---|---|---|---|---|
| 1 | workflow row `spec:95` | `sk/sc-workflow-protocol/SKILL.md:24,26,44` | 24: "`--output` is retired → `E-LEGACY`"; 26: "No package, no plan file, no yaml on a pre-creation STOP"; 44: `<pkg>/<id>.md`, e.g. `TASK-WF-authLogin-20261001-063000.md` | OK |
| 2 | workflow row `spec:95` | `refs/return-contract.md:3-19,39,41` | 3: writes `.dev/tasks/to-do/<id>/return-contract.yaml`; 39: "chat only — **no package directory, no yaml**"; 41: "After the package exists: any STOP → write the `failed` contract" | OK |
| 3 | WC-4a `spec:63` | `cmd/tdd.md:49`, `cmd/init-lite.md:32` | 49: "`--output` ... Output path for the final TDD document"; 32: "`--output` ... Report output path" | OK |
| 4 | WC-4a `spec:63` | `refs/return-contract.md:7`; `sk/sc-brainstorm-protocol/SKILL.md:341`; `sk/sc-reflect-protocol/SKILL.md:665` | `status: success \| partial \| failed`; `... \| dry-run`; `... \| dry-run` | OK |
| 5 | WC-4a `spec:63` | `sk/sc-adversarial-protocol/SKILL.md:436` | `status: "success"  # success \| partial \| failed`, inside a `return_contract:` block that sc:adversarial "returns" "When invoked by another command" (`SKILL.md:429-436`) | OK for the status vocabulary. OVERSTATED where WC-4a lists adversarial among commands that "already write a file named `return-contract.yaml`": lines 425-436 name no filename, and the spec's own adversarial row says "contract, but filename not fixed" (`spec:85`). Minor, new finding 15. |
| 6 | WC-4a and TFEP row `spec:63,93` | `sk/sc-troubleshoot-protocol/SKILL.md:560` | "Emit TFEP return-contract (conditional, when `caller=task-unified`) — write `<output-dir>/return-contract.yaml`" with 7 fields; status values `success\|partial\|blocked\|failed` | OK |
| 7 | WC-4a `spec:63` | `sk/sc-implement-protocol/refs/managed-workspace.md:10` | "Sibling `return-contract.yaml` has ... `status: success` or `partial`" | OK |
| 8 | WC-4a `spec:63` | `sk/sc-reflect-protocol/refs/remediation-handoff.md:75`; `sk/sc-auggie-review-protocol/refs/remediation-handoff.md:77` | 75: "Read `<pkg>/return-contract.yaml` ... `status: success` →"; 77: "Read `.dev/tasks/to-do/<id>/return-contract.yaml`: `status: success` →" | OK |
| 9 | WC-4a, TFEP row `spec:63,93` | `sk/sc-task-protocol/SKILL.md:216,220` | 216: "`/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir}` ... Pass NO `--fix`"; 220: "Read ... from `{output_dir}/return-contract.yaml`" | OK. Line 206 also writes `{output_dir}/context.yaml` into the same directory; where `{output_dir}` is defined was not found (UNVERIFIED, as disposition UNVERIFIED 3). |
| 10 | WC-4a `spec:63` | completeness of the writer list "adversarial, brainstorm, reflect, workflow, and troubleshoot" | `grep -rln return-contract.yaml src/superclaude/skills src/superclaude/commands`: the other hits (roadmap, tasklist, task, task-builder, implement) read another command's contract (`sk/sc-roadmap-protocol/SKILL.md:187,201`; `sk/sc-tasklist-protocol/SKILL.md:1171`; `sk/task/SKILL.md:576`; `managed-workspace.md:10`) | OK (no missed writer among the 43 command files in `cmd/`) |
| 11 | WC-3 `spec:61` | `cmd/task.md:93` quote | "If confidence <0.70, prompt user: \"Override with `--compliance [tier]`\"" | OK |
| 12 | WC-3 `spec:61` | `cmd/recommend.md:44` quote "it asks one question and stops" | line 44 ends "If the objective stays ambiguous, it asks one question and stops." | OK |
| 13 | WC-3 `spec:61` | `sk/tdd/SKILL.md:52-61` quote | 52: "If the user provides only a topic name ... **do NOT proceed immediately**"; 61: "Proceed once you have at least #1 answered clearly." | OK |
| 14 | WC-6 `spec:65` | `CAPS:116` | "`worker-start --task <task_id> --retry-of <dispatch_id> ...`" and the three-failure circuit breaker | OK |
| 15 | WC-7a `spec:67` | `CLAUDE.md:11` quote | "you MUST invoke the corresponding skill via the Skill tool BEFORE generating any other output" | OK |
| 16 | WC-10 `spec:70` | `~/.claude/commands/sc/spec-panel-ledger.md:261` | line 261 is the Sweep bullet: "only when a recorded smoke check showed that a dispatched worker can spawn an Agent-tool subagent and keep sending its 5-minute heartbeat through a subagent run longer than 5 minutes" | OK |
| 17 | WC-10 `spec:70` | `CAPS:123` (`worker-list` `projection.liveness`, `worker-show`) | "`worker-list`'s `projection.liveness` is the fleet verdict for the agent; `worker-show`'s `observation.status` is PTY liveness only. A live terminal can still hold a dead or stuck agent." `orca orchestration worker-list --help` does not mention `projection.liveness` (guide-only fact) | OK as a citation. The rule built on it is weaker than stated (new finding 7). |
| 18 | P1 row `spec:162` | `cmd/auggie-review.md:51` | "`--post-pr` \| `true` when target is a PR \| Auto-post ... **No confirmation prompt**" | OK |
| 19 | 7.2 step 6 `spec:188` | `sk/sc-workflow-protocol/SKILL.md:28` | "`.dev/tasks/` is always staged (`git add .dev/tasks`)" | OK |
| 20 | 7.2 step 6 `spec:188` | `CAPS:115` ("placement guide allows when sharing is unsafe") | "Create a worktree only when the user requested one or a concrete checkout or filesystem conflict makes sharing unsafe." | OK |
| 21 | AC-C5 `spec:179` | test record "the grep printed nothing while `--numstat` printed `1 1`" | Re-run 2026-11-09 in a scratch repo under `/tmp`: deleting one bullet gives grep rc=1 and `--numstat` `0 1 f.md`; `1 1` appears only when the line is edited | WRONG detail (the check itself is correct). Minor, new finding 9. |
| 22 | AC-0.4 `spec:197` | section 3.1 "Report today" names (`REPORT.md`, package `return-contract.yaml`, adversarial's contract file) | match `spec:85,94,95` | OK internally; adversarial's file has no fixed name in P0 (`spec:85`), so "the contract file adversarial wrote" is identified only after the run. |

Result: 20 citations OK, 1 overstated (#5), 1 wrong detail (#21). Neither changes a requirement's meaning; both are minor.

## 3. New findings (spec-panel-ledger, critique, focus requirements + architecture)
Command run: `/sc:spec-panel-ledger --ledger .dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger --revert-unclaimed @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`. Ledger phase `verify`, so this is the Verify step: every `plan-r2.md` row is answered once and one new-defect check covers this round's 12 hunks on both diff sides. Defects found elsewhere are still filed; the script stores them `scope=outside`.

### Panel notes (revised hunks)
**Wiegers (requirements).** WC-4a's path rule has three branches (directory flag, file flag, "no output flag uses the report flag its section 3 row names", `spec:63`). The third branch is empty for rows that name no flag: research ("contract naming the generated `claudedocs/research_*.md` path", `spec:119`; `cmd/research.md` has no `--output`, only `claudedocs/research_[topic]_[timestamp].md` at `cmd/research.md:103`), task ("contract on every tier", `spec:124`), recommend ("write the handoff envelope to a file", `spec:118`). For build, cleanup, improve and test the rows say only "add a report path" (`spec:104,106,113,126`), so whether WC-4a's file branch or directory branch applies is not decided. Finding 1.

**Adzic (examples).** AC-2.2 uses `/sc:tdd "auth" --unattended --output <file>` with a bare topic and requires `worker_done --outcome failed` and `status: blocked` (`spec:203`). Revised WC-3 now names exactly that gate as an `ask` route: the worker "may instead ask the coordinator ... which is the route for ... `/sc:tdd`'s topic clarification" (`spec:61`). A worker that follows WC-3 gets an answer, re-runs and reports `succeeded`, so AC-2.2 fails although both rules were followed. Finding 4.

**Cockburn (actors).** The TFEP row gives `/sc:task` a duty ("`/sc:task` gives TFEP an `<output-dir>` other than the task worker's own WC-4 directory", `spec:93`) and tags it P1, but `/sc:task` is a P2 command (`spec:124`, `spec:163`), the P1 command list does not name it (`spec:162`), and the task row does not repeat the duty. Finding 2.

**Fowler (interfaces).** The 240 s boundary now disagrees across three places: WC-10 forbids a call of "4 minutes or more" (`spec:70`), the cli-eval row asks for "waits of at most 4 minutes" (`spec:107`), and AC-4.3 passes when "no single tool call exceeds 240 s" (`spec:213`). Finding 6.

**Nygard (failure modes).** WC-10's substitute liveness rule tells the coordinator not to treat a heartbeat gap during subagent fan-out as a hang and to judge by `projection.liveness` and `worker-show` (`spec:70`). Those verdicts are process liveness: "Render only `live`, `unverifiable`, or `exited`" and "A live terminal can still hold a dead or stuck agent" (`CAPS:122-123`). A hung subagent leaves the agent process `live`, and 7.2 step 3 waits "until `worker_done` arrives" with no total bound (`spec:185`). Finding 7. Whether `projection.liveness` would ever flag a stuck agent is UNVERIFIED; the guide text read describes process verdicts only.

**Whittaker (adversarial).**
- I can break this specification by a **Zero/Empty Attack**. The invariant at WC-4a (`spec:63`), "The WC-4 path is fixed from the brief before dispatch", fails when the command has no output flag and its row names none. Concrete attack: the coordinator dispatches `/sc:research "x" --unattended`. Before: brief has no path flag. After: the report lands at a generated `claudedocs/research_x_<ts>.md` beside an undefined WC-4 file, so 7.2 step 3's "its report path is the WC-4 contract path" (`spec:185`) has nothing to compare with. (Finding 1)
- I can break this specification by a **Sentinel Collision Attack**. The invariant "two schemas never share one path" (`spec:63`) fails when `/sc:task`'s own WC-4 directory equals the `{output_dir}` it passes to TFEP. Concrete attack: in P2, `/sc:task --unattended --output .dev/t/` with no P1 change to `/sc:task` passes `--output-dir .dev/t/` to troubleshoot (`sk/sc-task-protocol/SKILL.md:216`). Before: `.dev/t/return-contract.yaml` absent. After: troubleshoot writes the 7-field TFEP file there (`sk/sc-troubleshoot-protocol/SKILL.md:560`) and task writes its WC-4 `return-contract.yaml` (task has no existing contract, so WC-4a's directory branch applies) to the same path. (Finding 2)
- I can break this specification by a **Sequence Attack**. The invariant "Later phases do not start until the earlier phase's checks in section 7 pass" (`spec:157`) blocks forever when AC-0.4's step 6 cannot pass in P0. Concrete attack: P0 runs `/sc:troubleshoot "<real symptom>"` with no `--output-dir` (`spec:197`). Before: baseline `git status`. After: new untracked files under `.dev/troubleshoot/<slug>-<timestamp>/` (default, `cmd/troubleshoot.md:56`); the brief named no output directory and P0's substitute report `REPORT.md` has no `report_path`/`artifacts` fields, so every new line fails step 6 (`spec:188`). The same holds for workflow's `.dev/tasks/to-do/<id>/` files, whose package contract lists `plan_path` and `source_path`, not `report_path`/`artifacts` (`refs/return-contract.md:6-19`). Round 1's step 6 allowed "the command's documented artifacts" (`plan:205`); the rewrite removed it. (Finding 8)
- I can break this specification by a **Divergence Attack**. The branch at WC-10 (`spec:70`) sits at exactly 240 s: forbidden by WC-10, allowed by the cli-eval row and AC-4.3. An implementer who follows the cli-eval row ships 240 s waits that AC-4.3-style checks pass and WC-10 forbids. (Finding 6)

**Newman (evolution).** The P1 rule makes every P2-P4 command "write its WC-4 report with `status: blocked`" under `--unattended` (`spec:162`). Several of those commands get their output or report flag only in their own phase: spec-panel "add `--output`" (P2, `spec:123`), cleanup and improve "add a report path" (P2, `spec:106,113`), recommend, research and task (P2, no flag at all). In P1 they cannot write a report at a path the coordinator recorded before dispatch. Finding 5.

**Hohpe (message flow).** 7.2 step 2 passes when "`observation.agentWait` is never non-null" (`spec:184`). Orca's help says an absent field "never means the worker is not waiting" (`orca orchestration worker-show --help`, Notes, read 2026-11-09). An absent field passes step 2 for a worker parked on a prompt. Finding 11 (outside the hunks; not found in round 1).

### Guard Condition Boundary Table (revised guards)
| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-4 path selection | WC-4a `spec:63` | Zero/Empty | no output flag, row names no report flag (research, task, recommend) | none of the three branches | unspecified | GAP (Finding 1) |
| WC-4 path selection | WC-4a `spec:63` | One/Minimal | `--output docs/TDD.md` (file) | file branch | `docs/TDD.md.return-contract.yaml` | OK |
| WC-4 path selection | WC-4a `spec:63` | Typical | `--output-dir .dev/r/` | directory branch | `.dev/r/return-contract.yaml` | OK |
| WC-4 path selection | WC-4a `spec:63` | Maximum/Overflow | command already writes `return-contract.yaml` in that directory | existing-contract branch | `worker-contract.yaml` in the same directory | OK |
| WC-4 path selection | WC-4a, TFEP row `spec:63,93` | Sentinel Value Match | task's WC-4 directory equals the TFEP `{output_dir}` | directory branch for task | collides with TFEP `return-contract.yaml`; the separating duty is tagged P1 but sits in no P1 scope | GAP (Finding 2) |
| WC-4 path selection | WC-4a `spec:63` | Legitimate Edge Case | "add a report path" rows (build, cleanup, improve, test): value could be a file or a directory | undecided | unspecified | GAP (Finding 1) |
| single-call wait limit | WC-10 `spec:70` | Zero/Empty | 0 s | allowed | nothing required | OK |
| single-call wait limit | WC-10 `spec:70` | One/Minimal | 1 s poll | allowed | nothing required | OK |
| single-call wait limit | WC-10 `spec:70` | Typical | 200 s poll | allowed | allowed | OK |
| single-call wait limit | WC-10 `spec:70` | Maximum/Overflow | 3600 s eval | forbidden | split into waits under 4 minutes | OK |
| single-call wait limit | WC-10 `spec:70` | Sentinel Value Match | exactly 240 s | forbidden by WC-10 | allowed by cli-eval row (`spec:107`) and AC-4.3 (`spec:213`) | GAP (Finding 6) |
| single-call wait limit | WC-10 `spec:70` | Legitimate Edge Case | one Agent-tool call of 10 minutes, then hangs | not limited | coordinator ignores the heartbeat gap and judges by process liveness, which stays `live` | GAP (Finding 7) |

### Numbered new findings
Severity uses the panel scale; blocking follows the ledger's `spec-panel` profile (CRITICAL, FR-8/FR-9, or MAJOR with a concrete wrong outcome). "Scope" is where the anchor sits: `in` = inside a revised hunk, `outside` = elsewhere (the script decides the stored scope).

| # | Finding | Severity | Parent row | Spec section | Evidence (path:line) | Scope |
|---|---|---|---|---|---|---|
| 1 | WC-4a's "no output flag uses the report flag its section 3 row names" is empty for research, task and recommend (no flag named), and the "add a report path" rows (build, cleanup, improve, test) do not say file or directory, so the WC-4 path cannot be fixed before dispatch and 7.2 step 3 has no path to check. | MAJOR | R4 | 2.2 WC-4a; 3.2 rows | `spec:63`, `spec:104,106,113,118,119,124,126`, `spec:185`; `cmd/research.md:103` | in |
| 2 | The TFEP row puts a P1 duty on `/sc:task` (separate TFEP `<output-dir>`), but task is P2, the P1 list omits it and task's row lacks it; if it is never built, task's WC-4 `return-contract.yaml` and troubleshoot's TFEP file share one path again. | MAJOR | R3 | 3.1 TFEP row; 3.2 task row; 6 P1 | `spec:93`, `spec:124`, `spec:162-163`; `sk/sc-task-protocol/SKILL.md:206,216,220`; `sk/sc-troubleshoot-protocol/SKILL.md:560` | in |
| 3 | Section 3.1 is still headed "Ready today (10)" and section 3 still counts "10 ready today", but the table now has 11 rows because the TFEP row (a mode of troubleshoot, not a command) was added. | MINOR | none | 3, 3.1 | `spec:78`, `spec:80`, `spec:85-95` | outside |
| 4 | Revised WC-3 names tdd's topic clarification as an `ask` route, while AC-2.2 uses that same gate and requires `--outcome failed` and `status: blocked`; a worker following WC-3 reports `succeeded` and AC-2.2 fails. | MAJOR | R8 | 2.2 WC-3; 7.3 AC-2.2 | `spec:61`, `spec:203` | in |
| 5 | The P1 blocked-report rule needs a WC-4 path for every P2-P4 command, but spec-panel, cleanup, improve, recommend, research and task get their output or report flag only in their own phase (or never), so their P1 blocked report has no known path. | MAJOR | R9 | 6 P1; 3.2 rows | `spec:162`, `spec:106,113,118,119,123,124` | in |
| 6 | The 240 s boundary contradicts itself: WC-10 forbids a call of "4 minutes or more", the cli-eval row asks for "waits of at most 4 minutes", and AC-4.3 passes "no single tool call exceeds 240 s"; the Decisions row still says 4 minutes. | MAJOR (FR-8) | R11 | 2.2 WC-10; 3.2 cli-eval; 7.3 AC-4.3; Decisions | `spec:70`, `spec:107`, `spec:213`, `spec:269` | in |
| 7 | WC-10 tells the coordinator to ignore heartbeat gaps during subagent fan-out and judge by `projection.liveness`/`worker-show`, which report process liveness only; a hung subagent stays `live`, and 7.2 step 3 waits for `worker_done` with no total bound, so a hang is never detected. | MAJOR | R11 | 2.2 WC-10; 7.2 step 3 | `spec:70`, `spec:185`; `CAPS:122-123` | in |
| 8 | AC-0.4 says step 6 passes "as written" in P0, but the R12 rewrite dropped the "documented artifacts" allowance; P0's troubleshoot run (no `--output-dir`) and workflow run write files outside any brief output directory, and their existing reports have no `report_path`/`artifacts` fields, so P0 cannot pass and no later phase starts. | MAJOR | R12 | 7.2 step 6; 7.3 AC-0.4; 6 | `spec:188`, `spec:197`, `spec:157`; `cmd/troubleshoot.md:56`; `sk/sc-workflow-protocol/refs/return-contract.md:6-19`; `plan:205` | in |
| 9 | AC-C5's test record says `--numstat` "printed `1 1`" for a deleted bullet; a pure deletion prints `0 1` (re-run 2026-11-09). The check is right, the record is wrong. | MINOR | R13 | 7.1 AC-C5 | `spec:179` | in |
| 10 | 7.2 step 5 still searches only for `AskUserQuestion`; the WC-7a Skill-call check exists only in AC-0.4, so the P1-P4 live checks (AC-1.2, AC-2.3) pass a worker that improvises the protocol without the Skill call. | MAJOR | none | 7.2 step 5; 7.3 AC-1.2, AC-2.3 | `spec:187`, `spec:67`, `spec:199`, `spec:204` | outside |
| 11 | 7.2 step 2 passes when `observation.agentWait` is "never non-null", but Orca says an absent field "never means the worker is not waiting", so a worker parked on a prompt on a host that did not look passes. | MAJOR | none | 7.2 step 2 | `spec:184`; `orca orchestration worker-show --help` Notes | outside |
| 12 | AC-0.3 still prints the `grep -E '^-[^-]'` test that AC-C5 now says is wrong; the override lives only in AC-C5's text. | MINOR | none | 7.3 AC-0.3 | `spec:196`, `spec:179` | outside |
| 13 | AC-1.4 still says "workflow states the contract is written for pre-creation STOPs", while the workflow row keeps the package contract unwritten on such STOPs; only WC-4a's global "the contract means" sentence reconciles them. | MINOR | none | 7.3 AC-1.4 | `spec:201`, `spec:95`, `spec:63` | outside |
| 14 | AC-1.1 asserts each `## Unattended mode` section names `return-contract.yaml`; for the five commands whose WC-4 report is `worker-contract.yaml`, the test passes on the old filename and never checks the new one. | MINOR | none | 7.3 AC-1.1 | `spec:198`, `spec:63` | outside |
| 15 | WC-4a lists adversarial among commands that "already write a file named `return-contract.yaml`", but its skill names no filename and the spec's own row says "filename not fixed". | MINOR | none | 2.2 WC-4a | `spec:63`, `spec:85`; `sk/sc-adversarial-protocol/SKILL.md:425-436` | in |
| 16 | The section 3 lead-in still glosses "Contract" as `<output-dir>/return-contract.yaml` and the Decisions row "Report shape" still says reuse `return-contract.yaml`; both are overridden only by WC-4a. | MINOR | none | 3 lead-in; Decisions | `spec:78`, `spec:264`, `spec:63` | outside |

Blocking candidates under the profile: findings 1, 2, 4, 5, 6, 7, 8, 10, 11 (MAJOR with a concrete wrong outcome, or FR-8). Minor notes: 3, 9, 12, 13, 14, 15, 16.

### Ledger input
Verify answers for every `plan-r2.md` row plus the new rows (labels N1-N16, matching the numbered list). Checked with `verify --input <this report> --dry-run`; the result is recorded under Decisions.

```ledger-input
{
  "answers": [
    {"row": "R1", "result": "resolved", "evidence": "Under `--unattended` the WC-4 report is `<report-dir>/worker-contract.yaml` (WC-4a)", "touched_ok": "yes"},
    {"row": "R2", "result": "resolved", "evidence": "its WC-4 report is a separate file, `worker-contract.yaml`, in the directory the rules above give", "touched_ok": "yes"},
    {"row": "R3", "result": "resolved", "evidence": "Troubleshoot's own WC-4 report is `<output-dir>/worker-contract.yaml` (WC-4a), so the two schemas never share a path", "touched_ok": "no", "reason": "the /sc:task half of the fix is tagged P1 but task is P2 and absent from the P1 scope (N2)"},
    {"row": "R4", "result": "resolved", "evidence": "gives `<file>.return-contract.yaml` beside that file", "touched_ok": "no", "reason": "the no-output-flag branch is empty for rows that name no flag (N1)"},
    {"row": "R5", "result": "resolved", "evidence": "and that is the path 7.2 step 3 checks", "touched_ok": "yes"},
    {"row": "R6", "result": "resolved", "evidence": "step 4 is not run in P0", "touched_ok": "yes"},
    {"row": "R7", "result": "resolved", "evidence": "the report path the coordinator recorded before dispatch (WC-4a) never changes", "touched_ok": "yes"},
    {"row": "R8", "result": "resolved", "evidence": "when the gate has no flag, the answer is folded into the command's main input", "touched_ok": "no", "reason": "naming tdd's topic gate as an ask route contradicts AC-2.2's required failed outcome (N4)"},
    {"row": "R9", "result": "resolved", "evidence": "does nothing under `--unattended` until its own phase except write its WC-4 report with `status: blocked`", "touched_ok": "no", "reason": "P2-P4 commands without an output flag in P1 cannot write the blocked report at a known path (N5)"},
    {"row": "R10", "result": "resolved", "evidence": "the first step of the command is the Skill tool call for that skill", "touched_ok": "yes"},
    {"row": "R11", "result": "resolved", "evidence": "No single tool call a command makes may block the session for 4 minutes or more", "touched_ok": "no", "reason": "240 s boundary contradicts the cli-eval row and AC-4.3 (N6); liveness substitute cannot detect a hung subagent (N7)"},
    {"row": "R12", "result": "resolved", "evidence": "lines already present before step 1 are ignored", "touched_ok": "no", "reason": "dropping the documented-artifacts allowance makes P0 step 6 fail for troubleshoot and workflow (N8)"},
    {"row": "R13", "result": "resolved", "evidence": "the second number (deleted lines) is `0`: edits are additive", "touched_ok": "no", "reason": "the recorded test output 1 1 is wrong for a pure deletion, which prints 0 1 (N9)"}
  ],
  "new_rows": [
    {"label": "N1", "grade": "MAJOR", "rule": "WC-4", "wrong_outcome": "For /sc:research, /sc:task or /sc:recommend under --unattended (no output flag, none named in their rows), or a build/cleanup/improve/test report path of unknown kind, the coordinator cannot fix the WC-4 path before dispatch and 7.2 step 3 has no path to compare.", "anchor": "A command with no output flag uses the report flag its section 3 row names", "finding": "WC-4a no-output-flag branch is empty for rows that name no flag (spec:118,119,124; cmd/research.md:103) and file-vs-dir is undecided for 'add a report path' rows (spec:104,106,113,126).", "side": "new", "parent": "R4"},
    {"label": "N2", "grade": "MAJOR", "rule": "FR-8", "wrong_outcome": "The /sc:task duty is tagged P1 but sits in no P1 scope or task row, so it is never built; task's WC-4 return-contract.yaml and troubleshoot's TFEP file then share one path again.", "anchor": "`/sc:task` gives TFEP an `<output-dir>` other than the task worker's own WC-4 directory", "finding": "TFEP row assigns a P1 change to /sc:task, a P2 command absent from the P1 list (spec:162-163) and whose row (spec:124) lacks the duty; sk/sc-task-protocol/SKILL.md:216,220.", "side": "new", "parent": "R3"},
    {"label": "N3", "grade": "MINOR", "rule": null, "wrong_outcome": null, "anchor": "### 3.1 Ready today (10)", "finding": "3.1 table now has 11 rows (TFEP row added) while the header and section 3 lead-in still count 10.", "side": "new"},
    {"label": "N4", "grade": "MAJOR", "rule": "WC-3", "wrong_outcome": "A worker following revised WC-3 asks the coordinator about the bare tdd topic, re-runs and reports succeeded, so AC-2.2 (requires --outcome failed and status: blocked) fails although both rules were followed.", "anchor": "which is the route for `/sc:recommend`'s one clarifying question and `/sc:tdd`'s topic clarification", "finding": "WC-3 names tdd's topic gate as an ask route; AC-2.2 (spec:203) uses that gate and requires a blocked outcome.", "side": "new", "parent": "R8"},
    {"label": "N5", "grade": "MAJOR", "rule": "WC-9", "wrong_outcome": "In P1, /sc:spec-panel, /sc:cleanup, /sc:improve, /sc:recommend, /sc:research or /sc:task under --unattended must write a blocked WC-4 report but has no output or report flag until its own phase, so the report lands at an unknown path or not at all.", "anchor": "so no prompt and no outward default can run early", "finding": "P1 blocked-report rule needs a WC-4 path for P2-P4 commands whose output flags arrive only in their own phase (spec:106,113,118,119,123,124).", "side": "new", "parent": "R9"},
    {"label": "N6", "grade": "MAJOR", "rule": "FR-8", "wrong_outcome": "An implementer following the cli-eval row ships 240 s waits that WC-10 forbids, and AC-4.3 passes a 240 s call, so the rule and its checks disagree at the boundary.", "anchor": "(one 300 s call is therefore not allowed)", "finding": "WC-10 forbids 4 minutes or more; cli-eval row 'at most 4 minutes' (spec:107), AC-4.3 'no single tool call exceeds 240 s' (spec:213), Decisions 'Wait size' (spec:269).", "side": "new", "parent": "R11"},
    {"label": "N7", "grade": "MAJOR", "rule": "WC-10", "wrong_outcome": "A worker whose Agent-tool subagent hangs keeps a live process, so projection.liveness stays live, the coordinator ignores the heartbeat gap by rule, and 7.2 step 3 waits for worker_done with no total bound.", "anchor": "the coordinator does not treat a heartbeat gap during a worker's subagent fan-out as a hang by itself", "finding": "Substitute liveness signals are process liveness only (CAPS:122-123); no bound replaces the heartbeat signal (spec:185).", "side": "new", "parent": "R11"},
    {"label": "N8", "grade": "MAJOR", "rule": "AC-0.4", "wrong_outcome": "P0's /sc:troubleshoot run (no --output-dir, default .dev/troubleshoot/<slug>-<timestamp>/) and /sc:workflow run (.dev/tasks/to-do/<id>/) add files outside any brief output directory, and REPORT.md and the package contract have no report_path/artifacts fields, so step 6 fails, AC-0.4 fails and no later phase starts.", "anchor": "a path in this worker's WC-4 report (`report_path`, `artifacts`)", "finding": "R12 rewrite dropped the 'command's documented artifacts' allowance (plan-r2.md:205); AC-0.4 (spec:197) says step 6 passes as written in P0; cmd/troubleshoot.md:56; refs/return-contract.md:6-19.", "side": "new", "parent": "R12"},
    {"label": "N9", "grade": "MINOR", "rule": null, "wrong_outcome": null, "anchor": "while `--numstat` printed `1 1`", "finding": "A pure deletion prints 0 1 (re-run 2026-11-09); 1 1 is an edit. The check is correct, the record is wrong.", "side": "new", "parent": "R13"},
    {"label": "N10", "grade": "MAJOR", "rule": "WC-7a", "wrong_outcome": "In P1-P4, a worker that reads the command file and improvises the protocol without the Skill call passes AC-1.2 and AC-2.3, because 7.2 step 5 checks only for AskUserQuestion.", "anchor": "search the transcript for `AskUserQuestion`", "finding": "The WC-7a Skill-call check exists only in AC-0.4 (spec:197); 7.2 step 5 (spec:187) used by AC-1.2 and AC-2.3 does not check it.", "side": "new"},
    {"label": "N11", "grade": "MAJOR", "rule": "7.2", "wrong_outcome": "A worker parked on a person-only prompt on a host whose worker-show omits agentWait passes step 2, since an absent field is not non-null.", "anchor": "`observation.agentWait` is never non-null", "finding": "orca orchestration worker-show --help: an absent agentWait 'never means the worker is not waiting'.", "side": "new"},
    {"label": "N12", "grade": "MINOR", "rule": null, "wrong_outcome": null, "anchor": "`git diff -U0 master...HEAD -- src/superclaude/core/HOW-WE-WORK.md", "finding": "AC-0.3 still shows the grep test AC-C5 calls wrong; the override sits only in AC-C5.", "side": "new"},
    {"label": "N13", "grade": "MINOR", "rule": null, "wrong_outcome": null, "anchor": "workflow states the contract is written for pre-creation STOPs", "finding": "AC-1.4 wording lags the R1 fix; only WC-4a's global 'the contract means' sentence reconciles it.", "side": "new"},
    {"label": "N14", "grade": "MINOR", "rule": null, "wrong_outcome": null, "anchor": "naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`", "finding": "AC-1.1 never checks worker-contract.yaml for the five commands that use it.", "side": "new"},
    {"label": "N15", "grade": "MINOR", "rule": null, "wrong_outcome": null, "anchor": "(today adversarial, brainstorm, reflect, workflow, and troubleshoot when `--caller task-unified`)", "finding": "adversarial is listed as already writing a file named return-contract.yaml, but its skill names no filename (sk/sc-adversarial-protocol/SKILL.md:425-436) and spec:85 says filename not fixed.", "side": "new"},
    {"label": "N16", "grade": "MINOR", "rule": null, "wrong_outcome": null, "anchor": "\"Contract\" means the WC-4 file `<output-dir>/return-contract.yaml`.", "finding": "Section 3 lead-in and the Decisions 'Report shape' row (spec:264) still describe the pre-WC-4a path; overridden only by WC-4a.", "side": "new"}
  ]
}
```

## 4. Verdict
**FAIL.**
- Part 1: all 13 blocking round-1 rows are resolved by the spec text (each evidence quote occurs once in `snapshots/r2.md`), but 7 of the 13 fixes carry a new defect (`touched_ok: no` for R3, R4, R8, R9, R11, R12, R13).
- Part 2: 22 revised citations re-read; 20 OK, 1 overstated (#5), 1 wrong detail (#21).
- Part 3: 16 new findings: 9 MAJOR (1, 2, 4, 5, 6, 7, 8, 10, 11), 7 MINOR (3, 9, 12, 13, 14, 15, 16). The brief's rule is that any finding of any severity is FAIL.
- Ledger preview: `verify --input <this report> --dry-run` returned `ok: true`, `rows: 33`, `blocking: 20`, `U: 7`, `verified: 13`, `deferred: 13`, `loop_decision: CONTINUE`, new rows R18-R33 (N1-N16 in order). Findings 10 and 11 sit outside this round's hunks, so the script stores them `scope=outside`, deferred; they still count in the `O` metric. The binding loop decision is the script's `close` tail, which the coordinator's ledger step appends; the next round would be review 3 of 3, the last before escalation.

No Self-Audit is given because the verdict is FAIL.

## Decisions
| Decision | Options considered | Rationale |
|---|---|---|
| Ledger writes | Run `verify` myself; leave every write to the coordinator | The brief allows writing only this report, and the command's Setup bullet limits this session to `status`, `verdict` and `--dry-run` (`~/.claude/commands/sc/spec-panel-ledger.md:258`). Only `status` and `verify --dry-run` were run. |
| Repo root | The spec's `OrcaCLICommandRefactor-Specs` (`spec:4`, `README.md:8`); the brief's `exp346-v-ledger` | The brief's root: the ledger snapshot matches the live spec here byte for byte. The README's root mismatch is round-1 minor R16, still deferred. |
| R10 answer | `open` (P1-P4 checks still miss the Skill call); `resolved` plus a new row | `resolved`: the row's stated wrong outcome named AC-0.4, which now checks the call, and WC-7a states the requirement. The remaining gap sits in 7.2 step 5, outside the hunks, filed as finding 10. |
| R13 answer | `open`; `resolved` with a minor child row | `resolved`: the reproduced test shows the new check catches a deleted bullet; only the recorded output is wrong (finding 9). |
| Findings 1 and 5 | One finding; two | Two: finding 1 is rows that never name a path flag; finding 5 is commands whose flag arrives after P1 but must already write a P1 blocked report. Separate fixes. |
| Grade of finding 7 | MINOR (the spec marks the subagent question UNVERIFIED); MAJOR | MAJOR: the rule actively tells the coordinator to ignore the only hang signal and gives no bound in its place, which is a concrete wrong outcome whatever the UNVERIFIED answer is. |
| Grade of finding 11 | Skip (pre-existing, outside the hunks); file it | Filed: the Verify step says anything found elsewhere is still filed (`spec-panel-ledger.md:260`), and round 1 did not report it. |

## UNVERIFIED items
1. Whether `worker-list`'s `projection.liveness` ever reports a stuck but running agent as anything other than `live` (finding 7). The guide text read (`CAPS:122-123`) describes process verdicts only; `worker-list --help` does not mention the field.
2. Where `/sc:task` defines `{output_dir}` for TFEP (`sk/sc-task-protocol/SKILL.md:206,216,220`); finding 2 depends on it being equal to, or chosen independently of, task's own WC-4 directory.
3. Whether a `--retry-of` worker receives the identical brief (carried from round 1 and the disposition; R7 rests on it).
4. Whether troubleshoot's `REPORT.md` lists every file it writes in some section (finding 8 rests on the absence of WC-4's `report_path`/`artifacts` field names, which was read from WC-4 `spec:62`, not on a full read of `refs/report-template.md`).

<!-- review-ledger tail: written by review_ledger.py close; do not edit -->
## Review ledger

review: 2 of 3

| id | grade | rule | blocking | status | scope | anchor |
|---|---|---|---|---|---|---|
| R1 | MAJOR | WC-4 | yes | verified | in | Write the contract for pre-creation STOPs too |
| R2 | MAJOR | FR-8 | yes | verified | in | Commands that already write a contract keep their fields and add the missing ones. |
| R3 | MAJOR | FR-8 | yes | verified | in | `REPORT.md` (`report_path`) |
| R4 | MAJOR | WC-4 | yes | verified | in | where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`) |
| R5 | MAJOR | WC-4 | yes | verified | in | Fix the contract filename to `<output>/adversarial/return-contract.yaml` |
| R6 | MAJOR | AC-0.4 | yes | verified | in | step 4 uses the command's existing report file, since the contract arrives in P1 |
| R7 | MAJOR | WC-6 | yes | verified | in | writes each run into a fresh output directory so a re-run starts clean |
| R8 | MAJOR | WC-3 | yes | verified | in | then re-invoke or resume the command with the answer as a flag |
| R9 | MAJOR | WC-9 | yes | verified | in | (a no-op where a command has no gate) |
| R10 | MAJOR | WC-7 | yes | verified | in | it never wraps the command in an Agent-tool subagent |
| R11 | MAJOR | FR-8 | yes | verified | in | A command step that blocks a single tool call for longer than 5 minutes (a poll wait, a long eval) |
| R12 | MAJOR | WC-11 | yes | verified | in | only files under the brief's output directory (and the command's documented artifacts) appear |
| R13 | MAJOR | SA-4 | yes | verified | in | src/superclaude/commands/<name>.md |
| R14 | MINOR |  | no | deferred | in | The first sentence of the body states the report's status and verdict. |
| R15 | MINOR |  | no | deferred | in | Launch setup, not commands |
| R16 | MINOR |  | no | deferred | in | Repo root: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs. |
| R17 | MINOR |  | no | deferred | in | prints nothing (SA-2, WC-8) |
| R18 | MAJOR | WC-4 | yes | open | in | A command with no output flag uses the report flag its section 3 row names |
| R19 | MAJOR | FR-8 | yes | open | in | `/sc:task` gives TFEP an `<output-dir>` other than the task worker's own WC-4 directory |
| R20 | MINOR |  | no | deferred | outside | ### 3.1 Ready today (10) |
| R21 | MAJOR | WC-3 | yes | open | in | which is the route for `/sc:recommend`'s one clarifying question and `/sc:tdd`'s topic clarification |
| R22 | MAJOR | WC-9 | yes | open | in | so no prompt and no outward default can run early |
| R23 | MAJOR | FR-8 | yes | open | in | (one 300 s call is therefore not allowed) |
| R24 | MAJOR | WC-10 | yes | open | in | the coordinator does not treat a heartbeat gap during a worker's subagent fan-out as a hang by itself |
| R25 | MAJOR | AC-0.4 | yes | open | in | a path in this worker's WC-4 report (`report_path`, `artifacts`) |
| R26 | MINOR |  | no | deferred | in | while `--numstat` printed `1 1` |
| R27 | MAJOR | WC-7a | no | deferred | outside | search the transcript for `AskUserQuestion` |
| R28 | MAJOR | 7.2 | no | deferred | outside | `observation.agentWait` is never non-null |
| R29 | MINOR |  | no | deferred | outside | `git diff -U0 master...HEAD -- src/superclaude/core/HOW-WE-WORK.md |
| R30 | MINOR |  | no | deferred | outside | workflow states the contract is written for pre-creation STOPs |
| R31 | MINOR |  | no | deferred | outside | naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` |
| R32 | MINOR |  | no | deferred | in | (today adversarial, brainstorm, reflect, workflow, and troubleshoot when `--caller task-unified`) |
| R33 | MINOR |  | no | deferred | outside | "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. |

### Reviser brief

Blocking rows to fix: R18, R19, R21, R22, R23, R24, R25
Revise only text a listed blocking row names; minor (deferred) rows are not answerable; add no rule, mechanism or section no blocking row calls for; each added paragraph or table cites its row id; report the byte size before and after.

loop_decision: CONTINUE (U=7, X=0, I=true)
verdict: FAIL
