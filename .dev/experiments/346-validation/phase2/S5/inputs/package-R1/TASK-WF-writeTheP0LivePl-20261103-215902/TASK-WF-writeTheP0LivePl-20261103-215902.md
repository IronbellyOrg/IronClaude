---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-writeTheP0LivePl-20261103-215902
version: "2"
priority: Medium
created_date: "2026-11-03"
---

# P0 live plan: Orca worker-contract live checks and phase report

Source: ./source.md
Goal: Run the three AC-0.4 live worker checks (troubleshoot, workflow, adversarial) with all seven section 7.2 steps each, measure AC-0.5, answer AC-0.6, and write the P0 phase report that cites the passed static report, adds the live results and states the P0 verdict.

## Constraints

- Executor: this plan is run by `/sc:implement` in a top-level session the person opens in Orca (an Orca terminal, so `ORCA_TERMINAL_HANDLE` is set), in the feature worktree on branch `ironbelly/OrcaCLICommandRefactor-Specs`. That session is the coordinator at depth 0. It is never run inside an Orca worker: AC-C6 shows `nestedWorkerMaxDepth` 1 (`.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-c6-depth-setting.txt`), and Tasks 2-4 start Orca workers, which a depth-1 worker may not do.
- Scope: the P0 live checks AC-0.4, AC-0.5 and AC-0.6 (spec `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:301-303`), the seven section 7.2 steps (spec lines 281-293), and the P0 phase report (spec line 238: the phase passes only when both plans' checks pass). The static checks are not re-run; they passed in `.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/p0-static-report.md`.
- No edit to any source, command, skill, agent or test file (nothing under `src/`, `plugins/`, `tests/` or `.claude/` is edited by hand), in the feature worktree or in any disposable worktree. In the feature worktree this plan writes only inside this package (`./artifacts/...`, plus the executor's own `progress.md`). `make sync-dev` inside a disposable worktree is allowed (spec line 282). Paths written `./artifacts/...` are inside this package.
- No git commit, push, merge, rebase, reset, stash, branch deletion, PR, `gh` write of any kind, and no `superclaude install` in any form. The executor's own git-state changes are only the disposable worktrees that `orca worktree create` makes and `orca worktree rm` removes, and the staging the next bullet states. `orca worktree rm` may delete a disposable worktree's local branch by itself when it can prove the branch is merged (`.dev/orca-command-refactor/review/p0-live-orca-flag-check.md`); the executor never deletes a branch. A worker's own git actions inside its disposable worktree are recorded in Step 6, not prevented. No interaction with the SuperClaude-Org upstream repository.
- UV for every Python command. Test runs set `PYTHONDONTWRITEBYTECODE=1` and pass `-p no:cacheprovider`.
- Staging: never stage anything under `.claude/`. Leave `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/` untouched and unstaged: every `git add .dev/tasks` in this run, including the executor's own re-add after the archive move (`~/.claude/skills/sc-implement-protocol/refs/managed-workspace.md:36`), is immediately followed by `git restore --staged -- .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950`. This one-path exception to the always-staged rule is the owner's instruction for this package only. Leave `.dev/brainstorms/`, `.dev/review-loop-convergence/` and `.dev/reflect/` untouched.
- A failed live check is a recorded result: it is not retried, rerun or repaired, and no second worker is started for it. A task is compliant when its check ran as written and every step's result is recorded faithfully with its evidence; a FAIL is then carried into the phase report, where per AC-0.4 it reopens spec section 1.
- Expected outcomes for the final review: `./artifacts/symptom-check.txt` passes when it shows exactly the three named failing tests, because those failures are the troubleshoot symptom. A FAIL inside an `lc<N>-*` step file, an `lc<N>-result.md` verdict of FAIL, or a P0 verdict of FAIL is a recorded result, not a task failure. Only `lc<N>-result.md`, `ac-0.5.md`, `ac-0.6.md` and `p0-phase-report.md` carry verdicts. Each `lc<N>-result.md` ends with the line `Recording status: complete (verdict recorded, not a task failure)`, and the executor cites that line, not raw step logs, on a task's `evidence=`.
- Retry, repair and resume never repeat a live check: a fix pass, a retry attempt (A2-A5) or a resume of Task 2, 3 or 4 only rebuilds `./artifacts/` from evidence already saved (saved receipts, files under `./artifacts/` including `./artifacts/retries/T<id>/artifacts-<k>/`, and `worker-read` output, which survives release). It never creates a worktree, Task or worker. Before its Worktree step, each of Tasks 2-4 checks `orca worktree list --json` and `orca orchestration worker-list --run <run_id> --json`: if a `p0-live-<name>` worktree or a worker for this check already exists, it continues from the first procedure step that has no saved evidence, using that worktree and worker. A step whose evidence is gone and cannot be rebuilt is recorded FAIL with that reason.
- Orca usage: every verb and flag in this plan was checked against Orca 1.4.237's `--help` before the run (`.dev/orca-command-refactor/review/p0-live-orca-flag-check.md`). An Orca usage error at run time is recorded as that step's FAIL with the error and the verb's `--help` output saved under `./artifacts/`; the command is never corrected at run time, because any plan edit after the first task starts halts the run (E-PLAN-CHANGED).
- Every `orca orchestration check --wait` call runs with a Bash tool timeout of at least 300000 ms. A Bash tool timeout is an executor mishap: the same wait is issued again, and it is not a check failure.
- The executor session makes every Orca call. Workers get the briefs below unchanged; a brief is never edited at run time. The briefs' `Worktree:` and `Report directory:` values are deliberate section 7.2 departures from the WORKER-CONTRACT template (spec line 282); the brief guard checks only `Command:` lines.
- Disposable worktree facts used by every live check: Orca repo selector `id:de550e99-fa3c-42e2-abfe-1d092771c759` (the IronClaude repo in `orca repo list`); base ref `refs/heads/ironbelly/OrcaCLICommandRefactor-Specs`, which Orca uses as given and which must resolve to commit `8db29f1165508187b7a14a48f2f66793e269d596` (`.dev/orca-command-refactor/review/p0-live-orca-flag-check.md`); agent `claude` with no `--model` and no `--effort`, so the person's normal launch setup is used (AC-0.5); run id `<run_id>` = the `result.run.id` field of `./artifacts/live-run.json`.
- Live-check procedure, followed by Tasks 2, 3 and 4 with their own check number `<N>`, name `<name>`, brief and report file. Evidence files go under `./artifacts/lc<N>-...`:
  - Worktree: `orca worktree create --repo id:de550e99-fa3c-42e2-abfe-1d092771c759 --name p0-live-<name> --base-branch refs/heads/ironbelly/OrcaCLICommandRefactor-Specs --no-parent --json`, receipt saved to `./artifacts/lc<N>-worktree.json`. Its path must not contain `/.dev/worktrees/`, and `git -C <path> rev-parse HEAD` must print `8db29f1165508187b7a14a48f2f66793e269d596`. Save `git -C <path> branch --show-current` to `./artifacts/lc<N>-branch.txt`. Then `make -C <path> sync-dev` must exit 0 (spec line 282: make sync-dev runs before dispatch, because Orca's `--setup run` is not confirmed to do it, UNVERIFIED item 27). Then `git -C <path> status --porcelain` is saved as `./artifacts/lc<N>-status-before.txt`. Any failure here fails step 1: record it, skip to Remove, and do not dispatch.
  - No-unattended check: `grep -c '^## Unattended mode' <path>/.claude/commands/sc/<command>.md ~/.claude/commands/sc/<command>.md`, saved to `./artifacts/lc<N>-unattended-check.txt`, must show 0 for both copies, which confirms the brief's `Command:` line rightly has no `--unattended` at P0.
  - Step 1: save the task's brief, exactly as written in its fenced block, to `./artifacts/lc<N>-brief.txt`. Run `orca orchestration task-create --spec "$(cat <that file>)" --task-title "P0 live check <N>: <name>" --run <run_id> --json`, then `orca orchestration worker-start --task <task_id> --worktree path:<path> --agent claude --run <run_id> --json`, timed with `date +%s.%N` before and after. Save both receipts and the elapsed seconds to `./artifacts/lc<N>-step1.txt`. Pass: worker-start exits 0 with `state: ready`. If worker-start fails, record steps 1-6 as FAIL or not run, release whatever the receipt says it still owns with `orca orchestration worker-release --dispatch <dispatch_id> --json` when it names a dispatch, then go to Step 7 and Remove.
  - Step 2: wait in turns of `orca orchestration check --run <run_id> --wait --types "worker_done,escalation,question" --timeout-ms 240000 --json`, and after every turn run `orca orchestration worker-show --dispatch <dispatch_id> --json`. Append one line per sample (UTC time and the `observation.agentWait` value) to `./artifacts/lc<N>-step2-samples.txt`, so samples are at most 5 minutes apart. Pass: `observation.agentWait` is never non-null.
  - Step 3: keep waiting until `worker_done` arrives. When a turn ends with no message, read `orca orchestration worker-read --dispatch <dispatch_id> --source transcript --json`: a growing transcript means keep waiting. A `question` message is answered only with facts about the environment; a request for a decision is not answered, and step 3 fails. Save the `worker_done` message to `./artifacts/lc<N>-step3.json`, then acknowledge its delivery with `orca orchestration check --run <run_id> --ack <delivery_id> --json`. Pass (AC-0.4 form): exactly one `worker_done`; its `--report-path` is the task's report file; its `--outcome` equals the AC-0.4 rule applied by the executor to that file (failed when the file is missing or empty, or its status is failed or blocked; otherwise succeeded).
  - Step 3 exits when no `worker_done` comes: (a) stall proof, meaning a transcript whose final agent turn sent no `worker_done`, or `exited` liveness in `orca orchestration worker-list --run <run_id> --json`: record step 3 FAIL with that proof, run `orca orchestration worker-stop --dispatch <dispatch_id> --json` and `orca orchestration task-update --id <task_id> --status failed --result cancelled --run <run_id> --json`, record steps 4-6 from what exists, then go to Step 7 and Remove; (b) a non-null `observation.agentWait` or an unanswered decision question with no stall proof: record step 2 or step 3 FAIL with that sample or message and keep waiting, because Orca forbids stopping a waiting worker without positive proof (`.dev/orca-command-refactor/inventory/orca-capabilities.md:114`); if 60 minutes pass after that sample with no `worker_done` and no stall proof, record steps 3-6 FAIL, leave the worker and its worktree running, write their dispatch id and path into `lc<N>-result.md` as left for the person, record Step 7 and Remove as not run because the worker is not settled, and move to the next task.
  - Step 4 (AC-0.4 form): `test -s <path>/<report file>` exits 0, saved to `./artifacts/lc<N>-step4.txt`.
  - Step 5: read the whole transcript with `worker-read --source transcript --json`, following `--cursor` until no next cursor remains, saving each page as `./artifacts/lc<N>-transcript-<page>.json`. Use `--source terminal` instead only if AC-0.6 (Task 2) recorded "no". Write `./artifacts/lc<N>-step5.md` with one verdict and a quoted excerpt for each condition: no `AskUserQuestion` call (WC-2); the command was invoked in the worker's top-level session, not inside an Agent-tool call (WC-7); a `check` call appears after the command finished and before `worker_done` (WC-12); heartbeat `send` calls are at most the cadence the worker's preamble states apart, except inside an Agent-tool call or a blocked `ask` or `check --wait` (WC-10), with the cadence quoted from the preamble and the run length stated; no `worker-start`, `dispatch` or `task-create` call and no `worktree create --agent` or `agent launch` call (WC-13). Pass: all five hold.
  - Step 6: `git -C <path> status --porcelain` saved to `./artifacts/lc<N>-status-after.txt`, and `git -C <path> diff --cached --name-only` saved to `./artifacts/lc<N>-index-after.txt`. Pass: every path not in `lc<N>-status-before.txt` is under the task's report directory or is a documented artifact of the command, with the file and line that documents it cited in `./artifacts/lc<N>-step6.md`. Ignored paths are not checked. Any path the worker staged is listed in `lc<N>-step6.md` as a known P0 gap (WC-9: at P0 no command has an unattended mode that stops its own staging), which the phase report carries.
  - Evidence copy: copy the report file, plus any file the task names, into `./artifacts/lc<N>-report/` before Step 7.
  - Step 7: `orca orchestration worker-release --dispatch <dispatch_id> --json`, then `orca orchestration worker-list --run <run_id> --terminal-state reclaimable --json`, both saved to `./artifacts/lc<N>-step7.txt`. Pass: the list returns no rows.
  - Remove: `orca worktree rm --worktree path:<path> --force --json` (spec line 282: the worktree is removed after step 7), saved to `./artifacts/lc<N>-remove.json`. Then save `orca worktree list --json` to `./artifacts/lc<N>-worktree-list-after.json`, the feature worktree's `git rev-parse HEAD` to `./artifacts/lc<N>-head-after.txt`, and `git branch --list "<the name in lc<N>-branch.txt>"` to `./artifacts/lc<N>-branch-after.txt`, which records whether the branch remains.
  - Result: `./artifacts/lc<N>-result.md` lists the worktree setup, steps 1-7 and Remove as PASS, FAIL or not run, one line each, with the evidence file for each, the AC-0.4 outcome the rule gives, and the check's overall verdict (PASS only when steps 1-7 all pass). Its last line is `Recording status: complete (verdict recorded, not a task failure)`.

## Phase 1: Preflight and run binding

## Task 1: Record the preflight facts and open the coordinator run

Before any other write, save `git status --porcelain` to `./artifacts/status-baseline.txt`. Then write `./artifacts/preflight.md` from these checks, run in the feature worktree, each with its command and output: `echo "$ORCA_TERMINAL_HANDLE"` is non-empty; `git rev-parse HEAD` prints `8db29f1165508187b7a14a48f2f66793e269d596` and `git branch --show-current` prints `ironbelly/OrcaCLICommandRefactor-Specs`; `git rev-parse refs/heads/ironbelly/OrcaCLICommandRefactor-Specs` prints the same commit; `cmp ~/.claude/WORKER-CONTRACT.md src/superclaude/core/WORKER-CONTRACT.md` exits 0 (the owner-approved install from that commit reached `~/.claude`); the AC-C6 command from spec line 278 prints only `"nestedWorkerMaxDepth":1`; `orca status --json` shows the runtime `ready`; `orca repo list --json` lists repo id `de550e99-fa3c-42e2-abfe-1d092771c759`. Save the `--help` output of every Orca verb this plan uses (`worktree create`, `worktree rm`, `worktree list`, and `orchestration run-create`, `task-create`, `worker-start`, `check`, `worker-show`, `worker-read`, `worker-release`, `worker-list`, `worker-stop`, `task-update`) to `./artifacts/orca-help.txt`. Then confirm the troubleshoot symptom is still current: `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/cli/eval/test_ban_import_rule.py -q -rf -p no:cacheprovider` saved to `./artifacts/symptom-check.txt`. It must report the three tests listed as accepted failures in `.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t1-accepted-failures.md:24-26` as failed. Then run `orca orchestration run-create --objective "P0 live checks AC-0.4, AC-0.5, AC-0.6 for the Orca worker contract" --json` and save the receipt to `./artifacts/live-run.json`. Last, save `git status --porcelain` to `./artifacts/status-end-t1.txt`.

Acceptance criteria:
- `./artifacts/preflight.md` shows every check above with its output, and each one passes.
- `./artifacts/orca-help.txt` holds the help text of every verb listed, and every flag and selector the live-check procedure uses appears in it.
- `./artifacts/symptom-check.txt` shows exactly `test_clean_tree_passes_ruff_check`, `test_synthetic_import_anthropic_is_flagged_by_ruff` and `test_ban_message_references_fr_g1` failing; this is the expected result.
- `./artifacts/live-run.json` holds `result.run.id` and a `result.run.coordinator_handle` equal to the `ORCA_TERMINAL_HANDLE` recorded in `preflight.md`.
- `./artifacts/status-end-t1.txt` lists no path that is not in `./artifacts/status-baseline.txt` or under this package, and shows no tracked file modified that is not already modified in `./artifacts/status-baseline.txt`, apart from this package's own files.

## Phase 2: Troubleshoot live check, launch timing and transcript shape

## Task 2: Run live check 1 on /sc:troubleshoot, with AC-0.5 and AC-0.6

Depends on: Task 1

Follow the live-check procedure in Constraints with `<N>` = 1, `<name>` = troubleshoot, command file `troubleshoot.md`. The symptom is a real current failure (Task 1's `./artifacts/symptom-check.txt`). Report directory `.dev/p0-live/troubleshoot/` inside the disposable worktree; report file `.dev/p0-live/troubleshoot/REPORT.md`, status from its `**Status**:` line (spec line 301; `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md:14`). The brief is the WORKER-CONTRACT section 5 template filled as below, passed to `task-create --spec` exactly:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p0-live/troubleshoot/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-Specs for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
P0 only: Report file: .dev/p0-live/troubleshoot/REPORT.md, with the status in its **Status**: line. Outcome rule: --outcome failed when the file is missing or empty, or its status is failed or blocked; otherwise --outcome succeeded. This rule replaces the WC-5 mapping for this Task.
Command: /sc:troubleshoot "uv run pytest tests/cli/eval/test_ban_import_rule.py fails 3 tests (test_clean_tree_passes_ruff_check, test_synthetic_import_anthropic_is_flagged_by_ruff, test_ban_message_references_fr_g1); find the root cause" --type test --output-dir .dev/p0-live/troubleshoot/
```

Before Step 5, answer AC-0.6 (spec line 303) from this worker's transcript: write `./artifacts/ac-0.6.md` stating yes or no to "tool calls appear by name" with a quoted transcript excerpt that supports the answer (for yes, at least one named call such as `Bash` or `Skill`). Write `./artifacts/ac-0.5.md` (spec line 302) from Step 1: the exit code, `state`, the elapsed seconds and the receipt's launch fields. AC-0.5 passes when worker-start exits 0 with `state: ready` in under 45 s. When worker-start never ran, `ac-0.5.md` records `not measured: <reason>`; when no transcript exists, `ac-0.6.md` records `not answerable: <reason>`, Step 5 is recorded as not run, and Step 5 in Tasks 3 and 4 uses the transcript source unless `ac-0.6.md` says no.

Acceptance criteria:
- `./artifacts/lc1-result.md` exists, records every procedure step with its evidence file and the check's overall verdict, and ends with the recording-status line.
- `./artifacts/lc1-report/REPORT.md` is a copy of the worker's report file, or `lc1-result.md` states that the file was missing.
- `./artifacts/ac-0.5.md` states the measured seconds and PASS or FAIL against the 45 s limit, or `not measured: <reason>` when worker-start never ran.
- `./artifacts/ac-0.6.md` states yes or no with a quoted transcript excerpt that supports that answer, or `not answerable: <reason>` when no transcript exists; `./artifacts/lc1-step5.md` names the source (transcript or terminal) that answer selects, or `lc1-result.md` records Step 5 as not run.
- Either `./artifacts/lc1-head-after.txt` shows `8db29f1165508187b7a14a48f2f66793e269d596` and `./artifacts/lc1-worktree-list-after.json` does not list the `p0-live-troubleshoot` worktree, or `lc1-result.md` records why the worktree remains (the Step 3 exit rule, or a recorded Remove FAIL).

## Phase 3: Workflow live check

## Task 3: Run live check 2 on /sc:workflow

Depends on: Task 2

Follow the live-check procedure in Constraints with `<N>` = 2, `<name>` = workflow, command file `workflow.md`. Before Step 1, save `ls -1 <path>/.dev/tasks/to-do/` to `./artifacts/lc2-todo-before.txt`. The report file is the `return-contract.yaml` in the one `TASK-WF-*` directory under `<path>/.dev/tasks/to-do/` that is not in `lc2-todo-before.txt`, status from its top-level `status` (spec line 301; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:3-7`). Step 3 and Step 4 fail when no new directory, or more than one, appears. The Evidence copy also copies that package's `<id>.md` plan file into `./artifacts/lc2-report/`. The run is plan-only, so README.md must stay unchanged. Workflow takes no report-directory flag at P0 (`--report-dir` arrives in P1, WORKER-CONTRACT section 5 table). In Step 6, the command's documented artifacts are the new package and the files its Wave 4 reflect run writes; cite where each is documented. The workflow protocol stages `.dev/tasks` itself (`src/superclaude/skills/sc-workflow-protocol/SKILL.md:28`), so Step 6's index file is expected to list the new package: record it as the known P0 gap. The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: the one new TASK-WF-* package directory this run creates under .dev/tasks/to-do/ (workflow takes no report-directory flag at P0)
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-Specs for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
P0 only: Report file: the return-contract.yaml in the one new TASK-WF-* package directory this run creates under .dev/tasks/to-do/, with the status in its top-level status key; a package that existed before this run never counts. Outcome rule: --outcome failed when the file is missing or empty, or its status is failed or blocked; otherwise --outcome succeeded. This rule replaces the WC-5 mapping for this Task.
Command: /sc:workflow "Add one sentence to the Installation section of README.md stating that superclaude install --force overwrites files that already exist in ~/.claude" --handoff none
```

Acceptance criteria:
- `./artifacts/lc2-result.md` exists, records every procedure step with its evidence file and the check's overall verdict, and ends with the recording-status line.
- `./artifacts/lc2-todo-before.txt` exists, and `lc2-result.md` names the one new package directory or states that none or several appeared.
- `./artifacts/lc2-report/` holds a copy of that package's `return-contract.yaml` and its `<id>.md` plan file, when they exist.
- `lc2-step6.md` states whether `README.md` was modified in the disposable worktree, with the status line as evidence, and lists what `./artifacts/lc2-index-after.txt` shows as staged.
- Either `./artifacts/lc2-head-after.txt` shows `8db29f1165508187b7a14a48f2f66793e269d596` and `./artifacts/lc2-worktree-list-after.json` does not list the `p0-live-workflow` worktree, or `lc2-result.md` records why the worktree remains (the Step 3 exit rule, or a recorded Remove FAIL).

## Phase 4: Adversarial live check

## Task 4: Run live check 3 on /sc:adversarial

Depends on: Task 2

Follow the live-check procedure in Constraints with `<N>` = 3, `<name>` = adversarial, command file `adversarial.md`. The two inputs are committed files at commit `8db29f11`: `.dev/orca-command-refactor/decisions/D1/option-a.md` and `.dev/orca-command-refactor/decisions/D1/option-b.md` (two rival options for one decision, 23 and 25 lines). `--compare` takes comma-separated paths (`src/superclaude/commands/adversarial.md:39`). Report directory `.dev/p0-live/adversarial/`; report file `.dev/p0-live/adversarial/adversarial/merge-log.md`, status from the `Status:` line of its `## Metadata` section, not the per-change `**Status**` lines (spec line 301; `src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:294-299`). The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p0-live/adversarial/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-Specs for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
P0 only: Report file: .dev/p0-live/adversarial/adversarial/merge-log.md, with the status in the Status: line of its ## Metadata section (the per-change **Status** lines do not count). Outcome rule: --outcome failed when the file is missing or empty, or its status is failed or blocked; otherwise --outcome succeeded. This rule replaces the WC-5 mapping for this Task.
Command: /sc:adversarial --compare .dev/orca-command-refactor/decisions/D1/option-a.md,.dev/orca-command-refactor/decisions/D1/option-b.md --depth quick --output .dev/p0-live/adversarial/
```

Acceptance criteria:
- `./artifacts/lc3-result.md` exists, records every procedure step with its evidence file and the check's overall verdict, and ends with the recording-status line.
- `./artifacts/lc3-report/merge-log.md` is a copy of the worker's report file, or `lc3-result.md` states that the file was missing.
- `lc3-step6.md` states whether the two input files were modified in the disposable worktree, with the status lines as evidence.
- Either `./artifacts/lc3-head-after.txt` shows `8db29f1165508187b7a14a48f2f66793e269d596` and `./artifacts/lc3-worktree-list-after.json` does not list the `p0-live-adversarial` worktree, or `lc3-result.md` records why the worktree remains (the Step 3 exit rule, or a recorded Remove FAIL).

## Phase 5: P0 phase report

## Task 5: Write the P0 phase report and stage the package

Depends on: Task 2, Task 3, Task 4

Write `./artifacts/p0-phase-report.md`. Static part: cite `.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/p0-static-report.md` by path and list each static check ID it covers (AC-0.1, AC-0.2, AC-0.3, AC-0.7, AC-0.9, AC-C1 to AC-C6) with the verdict it records, without copying its evidence. Carry forward its AC-0.7 finding that `task-create`, `worktree create --agent` and `agent launch` are covered only by WC-13 and section 7.2 step 5. Live part: one row each for AC-0.4 (each of the three checks, from `./artifacts/lc1-result.md`, `lc2-result.md` and `lc3-result.md`), AC-0.5 (`./artifacts/ac-0.5.md`) and AC-0.6 (`./artifacts/ac-0.6.md`), each with its verdict and evidence path. Name at least one checked run that lasted longer than the heartbeat cadence, or state that none did, so the heartbeat part of step 5 is not passed vacuously in every run (spec line 291). List each disposable worktree's branch from `lc<N>-branch-after.txt` that remains after removal, any worker or worktree left for the person, and any staging Step 6 found inside a disposable worktree (the known P0 gap), for the coordinator. State the P0 verdict: PASS only when every static check and every live check passes; otherwise FAIL, naming each failed check. An AC-0.4 failure is recorded as reopening spec section 1. End the report with the post-archive check the coordinator runs after the executor archives the package: `git diff --cached --name-only` must list nothing under `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950`. Then run `git add .dev/tasks` followed by `git restore --staged -- .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950`, save `git diff --cached --name-only` to `./artifacts/staged.txt` (the pre-archive snapshot), and save `git rev-parse HEAD` to `./artifacts/head-final.txt`.

Acceptance criteria:
- `./artifacts/p0-phase-report.md` has the static part citing the static report, the live part with rows for AC-0.4 (three checks), AC-0.5 and AC-0.6, the heartbeat-length statement, the remaining branches, any left workers and any worker staging, one P0 verdict line consistent with every row, and the post-archive check as its last section.
- Every live verdict in the report matches its `lc<N>-result.md`, `ac-0.5.md` or `ac-0.6.md` file.
- `./artifacts/staged.txt` lists only `.dev/tasks/` paths, none under `TASK-WF-orcaWorkerContra-20261102-231950` and none under `.claude/`.
- `./artifacts/head-final.txt` shows `8db29f1165508187b7a14a48f2f66793e269d596`.
