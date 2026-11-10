# Ledger plan for review 2

review: 2 of 3
document: ../orca-worker-contract-spec.md; snapshot snapshots/r2.md sha256 347e32c26f7dc0249df835d8c2557045b60ed7a19c1f3e2a290fd0321234d9bd

## Rows to answer

### R1: MAJOR, rule WC-4, status fixed

- finding: workflow is marked ready but cannot meet WC-4: --output retired (sc-workflow-protocol/SKILL.md:24), generated package id (SKILL.md:44), no yaml on pre-creation STOP (SKILL.md:26).
- wrong outcome: Coordinator passes --output to /sc:workflow and the run STOPs E-LEGACY; without it the contract path is unknown before dispatch and a pre-creation STOP writes no contract at all.
- old anchor: Write the contract for pre-creation STOPs too
- span in r2: lines 95-95
- hunk c1#8 (claimed by answer), r1 lines 92-92 -> r2 lines 95-95

old text:
```text
| workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
```
new text:
```text
| workflow | `--handoff none`; under `--unattended` also `--report-dir <dir>`; never `--output` (retired, it stops with `E-LEGACY`) | `.dev/tasks/to-do/<id>/return-contract.yaml`, whose `<id>` is generated at run time, so that path is not known before dispatch | Fresh package each run | Add `--report-dir <dir>` (P1). Under `--unattended` the WC-4 report is `<report-dir>/worker-contract.yaml` (WC-4a), known before dispatch and written on every outcome, including a pre-creation STOP, which today writes no package and no yaml; on such a STOP it carries `status: failed` and the STOP code, and after a package exists its `report_path` is the package's `<id>.md` and its `artifacts` list the package's own contract. The package and its contract stay as today (R1) | `sk/sc-workflow-protocol/SKILL.md:24,26,44,58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
```

### R2: MAJOR, rule FR-8, status fixed

- finding: WC-4 fixed status set conflicts with keep-their-fields; refs/return-contract.md:7 and sc-brainstorm-protocol/SKILL.md:341 use success.
- wrong outcome: 7.2 step 4 assertion rejects existing workflow/brainstorm contracts with status: success, or renaming the value breaks their current readers.
- old anchor: Commands that already write a contract keep their fields and add the missing ones.
- span in r2: lines 63-63
- hunk c1#2 (claimed by answer), r1 empty at line 63 -> r2 lines 63-63

old text:
```text

```
new text:
```text
| WC-4a | **Report path and existing contracts (R2, R4).** The WC-4 path is fixed from the brief before dispatch. A directory output flag (`--output <dir>`, `--output-dir <dir>`) gives `<dir>/return-contract.yaml`. A file output flag (`--output <file>`, as `/sc:tdd` and `/sc:init-lite` take) gives `<file>.return-contract.yaml` beside that file, so two runs writing different files in one directory never share a report. A command with no output flag uses the report flag its section 3 row names (workflow: `--report-dir <dir>`, R1). A command that already writes a file named `return-contract.yaml` in any mode (today adversarial, brainstorm, reflect, workflow, and troubleshoot when `--caller task-unified`) keeps that file exactly as today, because other commands read its own `status` values; its WC-4 report is a separate file, `worker-contract.yaml`, in the directory the rules above give. The WC-4 `status` values therefore never replace an existing `success`, and two schemas never share one path. This replaces WC-4's sentence "Commands that already write a contract keep their fields and add the missing ones." Wherever this spec says "the contract", "the WC-4 contract path" or "the WC-4 file", it means the path these rules give. | Command writes; coordinator records the path before dispatch | File output flags: `cmd/tdd.md:49`, `cmd/init-lite.md:32`. Existing vocabularies: `sk/sc-workflow-protocol/refs/return-contract.md:7`, `sk/sc-brainstorm-protocol/SKILL.md:341`, `sk/sc-adversarial-protocol/SKILL.md:436`, `sk/sc-reflect-protocol/SKILL.md:665`, `sk/sc-troubleshoot-protocol/SKILL.md:560`. Readers of `status: success`: `sk/sc-implement-protocol/refs/managed-workspace.md:10`, `sk/sc-reflect-protocol/refs/remediation-handoff.md:75`, `sk/sc-auggie-review-protocol/refs/remediation-handoff.md:77`; TFEP reader: `sk/sc-task-protocol/SKILL.md:220` |
```

### R3: MAJOR, rule FR-8, status fixed

- finding: troubleshoot already writes <output-dir>/return-contract.yaml with the TFEP schema (sc-troubleshoot-protocol/SKILL.md:560); WC-4 reuses the path.
- wrong outcome: Under /sc:task --unattended, troubleshoot writes two schemas to one path, so either the TFEP consumer or the coordinator reads the wrong contract.
- old anchor: `REPORT.md` (`report_path`)
- span in r2: lines 94-94
- hunk c1#7 (claimed by answer), r1 empty at line 91 -> r2 lines 93-93

old text:
```text

```
new text:
```text
| troubleshoot as run by `/sc:task` (TFEP) (R3) | set by `/sc:task`: `--caller task-unified --output-dir <dir>`, no `--fix` | `<output-dir>/return-contract.yaml` with the 7-field TFEP schema, which `/sc:task` reads | as troubleshoot below | None to the TFEP file: it stays exactly as today for `/sc:task`. Troubleshoot's own WC-4 report is `<output-dir>/worker-contract.yaml` (WC-4a), so the two schemas never share a path, and `/sc:task` gives TFEP an `<output-dir>` other than the task worker's own WC-4 directory. Under `/sc:task --unattended` only the task worker reports to Orca, with the task's own WC-4 report (WC-5, WC-7) (P1) | `sk/sc-troubleshoot-protocol/SKILL.md:560`; `sk/sc-task-protocol/SKILL.md:216,220` |
```

### R4: MAJOR, rule WC-4, status fixed

- finding: WC-4 output-dir undefined for file-valued --output (tdd.md:49; spec 3.1 tdd and init-lite rows; AC-2.2 example).
- wrong outcome: For /sc:tdd --output <file> the contract path is undefined, so 7.2 step 3 and AC-2.2 cannot locate it.
- old anchor: where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)
- span in r2: lines 62-62
- hunk c1#2 (claimed by answer), r1 empty at line 63 -> r2 lines 63-63

old text:
```text

```
new text:
```text
| WC-4a | **Report path and existing contracts (R2, R4).** The WC-4 path is fixed from the brief before dispatch. A directory output flag (`--output <dir>`, `--output-dir <dir>`) gives `<dir>/return-contract.yaml`. A file output flag (`--output <file>`, as `/sc:tdd` and `/sc:init-lite` take) gives `<file>.return-contract.yaml` beside that file, so two runs writing different files in one directory never share a report. A command with no output flag uses the report flag its section 3 row names (workflow: `--report-dir <dir>`, R1). A command that already writes a file named `return-contract.yaml` in any mode (today adversarial, brainstorm, reflect, workflow, and troubleshoot when `--caller task-unified`) keeps that file exactly as today, because other commands read its own `status` values; its WC-4 report is a separate file, `worker-contract.yaml`, in the directory the rules above give. The WC-4 `status` values therefore never replace an existing `success`, and two schemas never share one path. This replaces WC-4's sentence "Commands that already write a contract keep their fields and add the missing ones." Wherever this spec says "the contract", "the WC-4 contract path" or "the WC-4 file", it means the path these rules give. | Command writes; coordinator records the path before dispatch | File output flags: `cmd/tdd.md:49`, `cmd/init-lite.md:32`. Existing vocabularies: `sk/sc-workflow-protocol/refs/return-contract.md:7`, `sk/sc-brainstorm-protocol/SKILL.md:341`, `sk/sc-adversarial-protocol/SKILL.md:436`, `sk/sc-reflect-protocol/SKILL.md:665`, `sk/sc-troubleshoot-protocol/SKILL.md:560`. Readers of `status: success`: `sk/sc-implement-protocol/refs/managed-workspace.md:10`, `sk/sc-reflect-protocol/refs/remediation-handoff.md:75`, `sk/sc-auggie-review-protocol/refs/remediation-handoff.md:77`; TFEP reader: `sk/sc-task-protocol/SKILL.md:220` |
```

### R5: MAJOR, rule WC-4, status fixed

- finding: adversarial fix path contradicts WC-4 <output-dir>/return-contract.yaml checked by 7.2 step 3.
- wrong outcome: AC-1.2 step 3 fails for adversarial whichever of the two contract paths is implemented.
- old anchor: Fix the contract filename to `<output>/adversarial/return-contract.yaml`
- span in r2: lines 85-85
- hunk c1#6 (claimed by answer), r1 lines 83-83 -> r2 lines 85-85

old text:
```text
| adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
```
new text:
```text
| adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the existing contract's filename to `<output>/adversarial/return-contract.yaml`, which stays the file other commands read; under `--unattended` the WC-4 report is the separate `<output>/worker-contract.yaml` (WC-4a), and that is the path 7.2 step 3 checks (P1) (R5) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
```

### R6: MAJOR, rule AC-0.4, status fixed

- finding: AC-0.4 exempts only step 4 but step 3 requires the WC-4 contract path and status.
- wrong outcome: P0 cannot pass because step 3 needs a WC-4 contract that arrives only in P1, and later phases wait on P0, so the rollout never starts.
- old anchor: step 4 uses the command's existing report file, since the contract arrives in P1
- span in r2: lines 197-197
- hunk c1#12 (claimed by answer), r1 lines 194-194 -> r2 lines 197-197

old text:
```text
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
```
new text:
```text
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | The WC-4 report arrives in P1, so wherever 7.2 names it, P0 uses the command's existing report file instead (section 3.1 "Report today": troubleshoot's `REPORT.md`, workflow's package `return-contract.yaml`, the contract file adversarial wrote) (R6). Steps 1, 2, 5, 6 and 7 pass as written; step 3 passes with exactly one `worker_done` whose report path is that existing file and whose `--outcome` is `failed` only when that file is missing or reports a failure; step 4 is not run in P0. The step-5 transcript also shows the Skill tool call for the command's skill before any protocol output (WC-7a, R10), and the phase report records the longest gap between heartbeats and whether it fell inside an Agent-tool call (WC-10, R11); if no subagent call lasted over 5 minutes, that question stays UNVERIFIED. Record the results in the phase report; a failure here reopens section 1 |
```

### R7: MAJOR, rule WC-6, status fixed

- finding: WC-6 fresh-dir rule conflicts with retry reusing the Task brief (orca-capabilities.md:116) and WC-4 known-before-dispatch.
- wrong outcome: A --retry-of worker gets the same brief and --output, so it overwrites attempt 1 or writes to a directory the coordinator never recorded.
- old anchor: writes each run into a fresh output directory so a re-run starts clean
- span in r2: lines 65-65
- hunk c1#3 (claimed by answer), r1 lines 64-64 -> r2 lines 65-65

old text:
```text
| WC-6 | **Resume or safe re-run.** A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output. A command either resumes from its on-disk state when given its resume flag, or, if it has none, writes each run into a fresh output directory so a re-run starts clean. Section 3 names which applies per command. | Command | `CAPS:116` (retry and circuit breaker); resume mechanisms in column (e) of `INV-A:35-55`, `INV-B:31-52` |
```
new text:
```text
| WC-6 | **Resume or safe re-run at the same path.** A retry worker (`worker-start --retry-of`) runs the same Task, so it gets the same brief and the same output flag; the report path the coordinator recorded before dispatch (WC-4a) never changes, and a command never picks a new directory on its own. A command either resumes from its on-disk state when given its resume flag, or, if it has none, runs again in the same place: at start it overwrites any earlier WC-4 report at that path with `status: failed` and the reason "attempt started, not finished", so a crash never leaves the earlier attempt's report looking current; it writes the final report last, and that report's `report_path` and `artifacts` name only files this attempt wrote, so a file left by an earlier attempt is never read as a result. Where section 3 says "fresh dir" or "fresh file", it means this same-path re-run. A coordinator that wants the earlier attempt's files kept moves them aside before it starts the retry. Section 3 names which applies per command. (R7) | Command; coordinator (keeping an earlier attempt) | `CAPS:116` (retry is `worker-start --task <task_id> --retry-of <dispatch_id>` on the same Task; circuit breaker); resume mechanisms in column (e) of `INV-A:35-55`, `INV-B:31-52` |
```

### R8: MAJOR, rule WC-3, status fixed

- finding: WC-3 answer-as-flag route undefined for flagless gates.
- wrong outcome: For gates with no answer flag (recommend, tdd topic, task confidence) the coordinator's answer cannot reach the command, and a fresh-dir re-run changes the report path.
- old anchor: then re-invoke or resume the command with the answer as a flag
- span in r2: lines 61-61
- hunk c1#1 (claimed by answer), r1 lines 61-61 -> r2 lines 61-61

old text:
```text
| WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
```
new text:
```text
| WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-run the command with the answer. The answer goes in through the gate's own flag when one exists (for example `/sc:task`'s confidence-below-0.70 gate, which names `--compliance [tier]`); when the gate has no flag, the answer is folded into the command's main input (its request, topic or component text) and the command runs again, which is the route for `/sc:recommend`'s one clarifying question and `/sc:tdd`'s topic clarification. A gate that only a person may answer (an approval, or an `/sc:implement` Ruling under D2 (a)) is not asked; the command ends blocked (WC-2 (c)). The re-run keeps every other flag of the brief, including the output flag, so the report path the coordinator recorded before dispatch does not change (WC-4a, WC-6). On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. (R8) | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11); gate routes: `cmd/task.md:93` ("If confidence <0.70, prompt user: Override with `--compliance [tier]`"), `cmd/recommend.md:44` ("it asks one question and stops"), `sk/tdd/SKILL.md:52-61` ("Proceed once you have at least #1 answered clearly") |
```

### R9: MAJOR, rule WC-9, status fixed

- finding: P1 accepts --unattended on every command but gated commands convert only in P2-P4; auggie-review.md:51 posts with no prompt.
- wrong outcome: Between P1 and P2, /sc:auggie-review --unattended still posts to the PR by default, an outward action the contract says is off.
- old anchor: (a no-op where a command has no gate)
- span in r2: lines 162-162
- hunk c1#9 (claimed by answer), r1 lines 159-159 -> r2 lines 162-162

old text:
```text
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
```
new text:
```text
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2. A command whose gates or outward defaults are converted in P2-P4 does nothing under `--unattended` until its own phase except write its WC-4 report with `status: blocked` and a `blocked_question` naming the phase that converts it, so no prompt and no outward default can run early; for example `/sc:auggie-review` posts to the PR by default with no prompt (`cmd/auggie-review.md:51`) and would otherwise post between P1 and P2 (WC-9, R9). Every other command runs normally under the flag. Output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
```

### R10: MAJOR, rule WC-7, status fixed

- finding: WC-7 does not require the Skill tool invocation mandated by CLAUDE.md:11; no check tests it.
- wrong outcome: A worker that reads the command file and improvises the protocol without the Skill call passes 7.2 step 5 and AC-0.4.
- old anchor: it never wraps the command in an Agent-tool subagent
- span in r2: lines 66-66
- hunk c1#4 (claimed by answer), r1 empty at line 66 -> r2 lines 67-67

old text:
```text

```
new text:
```text
| WC-7a | **Invoke the command's skill (R10).** The worker starts the command with its `/sc:<name>` line, and when the command file names a skill, the first step of the command is the Skill tool call for that skill, before any protocol output, as the repo requires for every `/sc:` command (lifecycle calls such as `heartbeat` and `check` may come before it). A worker that reads the command or skill file and carries out the protocol itself, without that Skill call, does not meet WC-7. Check: the 7.2 step-5 transcript shows that Skill call (AC-0.4). | Worker session | `CLAUDE.md:11` ("you MUST invoke the corresponding skill via the Skill tool BEFORE generating any other output") |
```

### R11: MAJOR, rule FR-8, status fixed

- finding: WC-10 ignores subagent waits kept by WC-7; spec-panel-ledger.md:261 treats heartbeat through a long subagent run as unproven.
- wrong outcome: An Agent-tool subagent call or a single 300 s call blocks the session past the 5-minute heartbeat and no check outside AC-4.3 detects it.
- old anchor: A command step that blocks a single tool call for longer than 5 minutes (a poll wait, a long eval)
- span in r2: lines 70-70
- hunk c1#5 (claimed by answer), r1 lines 68-68 -> r2 lines 70-70

old text:
```text
| WC-10 | **Liveness during long waits.** The worker sends a heartbeat every 5 minutes while working. A command step that blocks a single tool call for longer than 5 minutes (a poll wait, a long eval) must be split into waits of at most 4 minutes so the session can heartbeat between them. | Command (wait size); worker (heartbeat) | Cadence is from the dispatch preamble, not a guide (`CAPS:130`); pr-submit's 600 s is a cumulative per-wait budget made of repeated iterations (one foreground poll, then a sleep of at least `--poll-interval`), not one blocking call (`cmd/pr-submit.md:49`; `sk/sc-pr-submit-protocol/SKILL.md:46-64`); `sk/sc-cli-eval-protocol/SKILL.md:151-152` (eval timeouts up to 3600 s) via `INV-A:65` |
```
new text:
```text
| WC-10 | **Liveness during long waits.** The worker sends a heartbeat every 5 minutes while working. No single tool call a command makes may block the session for 4 minutes or more: a poll wait or a long eval is split into waits under 4 minutes so the session can heartbeat between them (one 300 s call is therefore not allowed). An Agent-tool subagent call, which WC-7 keeps, can also block the session, and whether a dispatched worker keeps heartbeating through a subagent call longer than 5 minutes is UNVERIFIED: the repo itself treats it as unproven until a recorded smoke check shows it (`~/.claude/commands/sc/spec-panel-ledger.md:261`). AC-0.4 records it. Until a recorded run shows heartbeats continue through such a call, the coordinator does not treat a heartbeat gap during a worker's subagent fan-out as a hang by itself; it judges liveness by `worker-list`'s `projection.liveness` and by `worker-show` (`CAPS:123`, 7.2 step 2). (R11) | Command (wait size); worker (heartbeat); coordinator (liveness) | Cadence is from the dispatch preamble, not a guide (`CAPS:130`); pr-submit's 600 s is a cumulative per-wait budget made of repeated iterations (one foreground poll, then a sleep of at least `--poll-interval`), not one blocking call (`cmd/pr-submit.md:49`; `sk/sc-pr-submit-protocol/SKILL.md:46-64`); `sk/sc-cli-eval-protocol/SKILL.md:151-152` (eval timeouts up to 3600 s) via `INV-A:65` |
```

### R12: MAJOR, rule WC-11, status fixed

- finding: step 6 and WC-11 ignore shared worktree and git index state (orca-capabilities.md:115; sc-workflow-protocol/SKILL.md:28).
- wrong outcome: 7.2 step 6 fails whenever the shared worktree has any other untracked file (this checkout already shows ?? .dev/orca-command-refactor/), and two workers can collide on git add .dev/tasks.
- old anchor: only files under the brief's output directory (and the command's documented artifacts) appear
- span in r2: lines 188-188
- hunk c1#11 (claimed by answer), r1 lines 185-185 -> r2 lines 188-188

old text:
```text
6. `git status --short`. **Pass:** only files under the brief's output directory (and the command's documented artifacts) appear.
```
new text:
```text
6. `git status --short --untracked-files=all`, saved before step 1 and run again after step 3. **Pass:** every line that is new between the two runs names a path under the brief's output directory, a path in this worker's WC-4 report (`report_path`, `artifacts`), or a path in the WC-4 report of another worker that ran in the same worktree at the same time; lines already present before step 1 are ignored, so other people's and other workers' earlier files do not fail the check (a tracked file that was already modified before step 1 is not re-checked by this step). Two workers whose commands stage files (workflow runs `git add .dev/tasks`, `sk/sc-workflow-protocol/SKILL.md:28`) never run in the same worktree at the same time; the coordinator gives one of them its own worktree, which Orca's placement guide allows when sharing is unsafe (`CAPS:115`). (R12)
```

### R13: MAJOR, rule SA-4, status fixed

- finding: additive-edit regex misses deleted lines starting with '-'; tested NO_MATCH.
- wrong outcome: A deleted Markdown bullet shows as '-- item', which grep -E '^-[^-]' does not match, so AC-C5 and AC-0.3 pass a non-additive edit.
- old anchor: src/superclaude/commands/<name>.md
- span in r2: lines 179-179
- hunk c1#10 (claimed by answer), r1 lines 176-176 -> r2 lines 179-179

old text:
```text
| AC-C5 | For every command file the phase edits without a named defect fix (SA-4): `git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md \| grep -E '^-[^-]'` | prints nothing: edits are additive |
```
new text:
```text
| AC-C5 | For every command file the phase edits without a named defect fix (SA-4): `git diff --numstat master...HEAD -- src/superclaude/commands/<name>.md` | the second number (deleted lines) is `0`: edits are additive. Counting deletions replaces the earlier `grep -E '^-[^-]'` test, which misses a deleted Markdown bullet (it shows as `-- item`; tested 2026-11-09: the grep printed nothing while `--numstat` printed `1 1`). AC-0.3 applies this same `--numstat` test to `src/superclaude/core/HOW-WE-WORK.md` in place of its grep (R13) |
```

## Unclaimed hunks

(none)

## Reviser gap entries

- R2/R4: section 3 lead-in (spec:78) still glosses Contract as <output-dir>/return-contract.yaml; WC-4a overrides it.
- R2: Decisions row 'Report shape' (spec:264) still says reuse return-contract.yaml; WC-4a adds worker-contract.yaml for commands with an existing contract.
- R13: AC-0.3 (spec:196) still shows grep -E '^-[^-]'; AC-C5 says AC-0.3 uses the --numstat test instead.
- R10: 7.2 step 5 (spec:187) checks only AskUserQuestion; the Skill-call check is in WC-7a and AC-0.4.
- R11: no heartbeat-gap check outside AC-0.4 and AC-4.3; WC-10 gives a coordinator liveness rule meanwhile.
- R12: WC-11 (spec:71) still covers output files only; the git-staging rule is in 7.2 step 6.
- R1: AC-1.4 (spec:201) wording about the workflow contract on pre-creation STOPs now means the WC-4 worker-contract.yaml in --report-dir.
