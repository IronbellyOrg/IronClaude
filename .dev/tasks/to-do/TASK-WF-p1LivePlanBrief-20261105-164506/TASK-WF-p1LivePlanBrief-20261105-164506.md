---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-p1LivePlanBrief-20261105-164506
version: "1"
priority: Medium
created_date: "2026-11-05"
---

# P1 live plan: Orca worker-contract live checks and phase report

Source: ./source.md (a byte-exact snapshot of the brief; where the plan and the snapshot differ, the plan governs: the snapshot's owner grant file is replaced by the "AC-1.8 owner instruction" Constraints bullet, and its fixed branch tip by the tip recorded in Task 1)
Goal: Run the P1 live checks of the Orca worker-contract spec (AC-1.2 on the sixteen P1 commands, AC-1.3 file creation, AC-1.5, AC-1.6, AC-1.7 three cases, AC-1.8 commit grant) with all seven section 7.2 steps each, and write the P1 phase report that cites the passed static report, adds the live results and states the phase verdict.

## Constraints

- Spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` is called "the spec"; "spec 7.2" is its section 7.2 (live worker check, lines 281-304), "spec 7.3" its section 7.3 (per-phase checks), "WC-n" a requirement of its section 2.2. The P1 static plan passed and is archived at `.dev/tasks/done/TASK-WF-writeTheP1Static-20261105-033458/`; its report `artifacts/p1-static-report.md` is cited, not copied. Its edits are committed as `7127c2478756c9444afc600af3e3066b3f7f24db` on branch `ironbelly/OrcaCLICommandRefactor-P1`. The branch tip has moved since: a merge of `origin/master` (`185f8349a57fd6cf1ba5b2e42a90925f0b6f50ae`, pushed once to the fork for safekeeping) and a small `WORKER-CONTRACT.md` brief-flag table edit (`f0e307eb8596f1362bd7b372c55877fc98b1ea1b`, local). So this plan never pins the tip: Task 1 records `git rev-parse HEAD` in `./artifacts/branch-tip.txt`, requires `7127c2478756c9444afc600af3e3066b3f7f24db` to be an ancestor of it, and every later check compares against that file. Revision note: this plan was revised once before its first task started, from the findings of its pre-execution review (tip pin, install comparison, child worktree setup for AC-1.8, step 5 for guard refusals, Orca version and help coverage); the revision list is in `.dev/reflect/pre-TASK-WF-p1LivePlanBrief-20261105-164506-20261105165021/post-fix-rechecks.md`. The archived P0 live plan `.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/` is the model for the procedure and the evidence file names; its P0-only rule (the AC-0.4 report-file and outcome rule) does not apply here, because from P1 on the commands write the WC-4 contract.
- Executor: this plan is run by `/sc:implement` in a top-level session the person opens in Orca (an Orca terminal, so `ORCA_TERMINAL_HANDLE` is set), in the feature worktree on branch `ironbelly/OrcaCLICommandRefactor-P1`. That session is the coordinator at depth 0. It is never run inside an Orca worker: AC-C6 shows `nestedWorkerMaxDepth` 1 (`.dev/tasks/done/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-c6-depth-setting.txt`), and the live tasks start Orca workers.
- Install precondition: the plan never installs. Per spec 7.2 the owner approves, and the coordinator runs `uv run superclaude install --force` from this branch, before this plan runs. Task 1 verifies it. If any installed file differs from the branch, Task 1 records the install line FAIL, and every later live task records `not run: install precondition failed` in its `lc<NN>-result.md` and starts no worktree, Task or worker.
- Scope: the P1 live checks of spec 7.3 (AC-1.2, AC-1.3 file-creation part, AC-1.5, AC-1.6, AC-1.7, AC-1.8), the seven spec 7.2 steps for each, and the P1 phase report (spec line 238: the phase passes only when both plans' checks pass). The static checks (AC-1.1, AC-1.4, AC-C1 to AC-C6) are not re-run. The prompt-and-default-behaviour part of AC-1.3 is manual: it is listed for the owner in the phase report and is not run by this plan.
- No edit to any source, command, skill, agent or test file (nothing under `src/`, `plugins/`, `tests/` or `.claude/` is edited by hand), in the feature worktree or in any disposable worktree. In the feature worktree this plan writes only inside this package (`./artifacts/...`, plus the executor's own `progress.md`). `make sync-dev` inside a disposable worktree is allowed (spec 7.2). Paths written `./artifacts/...` are inside this package.
- No git commit, push, merge, rebase, reset, stash, branch deletion, PR, `gh` write of any kind, no `superclaude install`, no interaction with the SuperClaude-Org upstream repository, and no Orca link flag (`--issue`, `--pr`, `--linear-issue`, `--gitlab-issue`, `--gitlab-mr`), because Orca records this project as the upstream (`github:superclaude-org/superclaude_framework`). The only git writes are the disposable worktrees that `orca worktree create` makes (including the AC-1.8 child created with `--parent-worktree active`) and `orca worktree rm` removes, the staging this plan's last task states, and the one commit a worker makes under AC-1.8 inside its own child worktree. `orca worktree rm` may delete a disposable worktree's local branch by itself; the executor never deletes a branch. Reads of the fork are allowed: `git ls-remote origin` once `git remote get-url origin` prints `https://github.com/IronbellyOrg/IronClaude`, and `gh pr list --repo IronbellyOrg/IronClaude --author @me`.
- UV for every Python command, in the executor and in every subagent or helper it starts: `uv run --no-project python -I <script>` for scripts and `uv run python -c ...` where the project is needed. Never bare `python`, `python3` or `pip` (the P0 run had 24 such calls from review helpers). Every prompt the executor writes for a helper repeats this rule. Test runs set `PYTHONDONTWRITEBYTECODE=1` and pass `-p no:cacheprovider`.
- Staging: never stage anything under `.claude/`. Every `.dev/tasks/` package other than this plan's own stays untouched. This plan's own package is staged by the last task (`git add .dev/tasks`).
- A failed live check is a recorded result: it is not retried, rerun or repaired, and no second worker is started for it. A task is compliant when its check ran as written and every step's result is recorded faithfully with its evidence. A FAIL inside an `lc<NN>-*` step file, an `lc<NN>-result.md` verdict of FAIL, or a P1 verdict of FAIL is a recorded result, not a task failure. Only `lc<NN>-result.md`, `ac-1.3.md` and `p1-phase-report.md` carry verdicts. Each `lc<NN>-result.md` ends with the line `Recording status: complete (verdict recorded, not a task failure)`, and the executor cites that line, not raw step logs, on a task's `evidence=`. A FAIL of AC-1.2 on a P1 command is recorded as a gap in that command; the command is not repaired by this plan.
- Retry, repair and resume never repeat a live check: a fix pass, a retry attempt or a resume of a live task only rebuilds `./artifacts/` from evidence already saved (saved receipts, files under `./artifacts/`, and `worker-read` output, which survives release). It never creates a worktree, Task or worker. Before its Worktree step each live task checks `orca worktree list --json` and `orca orchestration worker-list --run <run_id> --json`; if a `p1-live-<name>` worktree or a worker for this check already exists, it continues from the first procedure step that has no saved evidence, using that worktree and worker. A step whose evidence is gone and cannot be rebuilt is recorded FAIL with that reason.
- Orca usage: Task 1 saves the `--help` text of every verb this plan uses. The Orca runtime is 1.4.245-aidev02 (P0 ran on 1.4.237). An Orca usage error at run time is recorded as that step's FAIL with the error and the verb's help text saved under `./artifacts/`; the command is never corrected at run time, because any plan edit after the first task starts halts the run (E-PLAN-CHANGED).
- Every `orca orchestration check --wait` call runs with a Bash tool timeout of at least 300000 ms. A Bash tool timeout is an executor mishap: the same wait is issued again, and it is not a check failure. The executor session makes every Orca call. Workers get the briefs below unchanged; a brief is never edited at run time (the one exception is the owner instruction copied into Task 24's brief, stated there). The briefs' `Worktree:` and `Report directory:` values are deliberate spec 7.2 departures from the WORKER-CONTRACT template; the brief guard checks only `Command:` lines.
- Heartbeat reading (owner decision H1, `.dev/orca-command-refactor/decisions/APPROVED.md`, 2026-11-05): a gap between heartbeats that lies inside a command's own subagent fan-out is accepted. Step 5 condition 4 is exactly limits (a) and (b) of spec 7.2 step 5; the stricter reading is rejected. At least one checked run in this phase must last longer than the heartbeat cadence the worker's preamble states, and the phase report names it.
- Step 5 source: `worker-read --source transcript` returns only the last 40 to 50 messages of a long run (P0 note 1), so step 5 is read from the worker's own Claude session file and cross-checked with `worker-read`. The P0 scripts are `.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/session-analysis.py` (arguments: the `<dir>` folder, the top-level session file; prints the tool tally, the Skill-call timing, the Orca commands, the heartbeat times and the WC-13 scan) and `session-hbcover.py` (argument: the top-level session file; prints heartbeat gaps with subagent time removed), each run as `uv run --no-project python -I <script> <arguments>`. A missing, ambiguous or unreadable session file makes conditions 1, 2, 4 and 5 `not verifiable`; the check is then not recorded as passed and the phase report lists the gap.
- Disposable worktree facts used by every live check: Orca repo selector `id:de550e99-fa3c-42e2-abfe-1d092771c759`; base ref `refs/heads/ironbelly/OrcaCLICommandRefactor-P1`, used as given, which must resolve to the sha recorded in `./artifacts/branch-tip.txt` (Task 1); agent `claude` with no `--model` and no `--effort`; run id `<run_id>` is the `result.run.id` field of `./artifacts/live-run.json`. Every report directory below is inside the worktree under `.dev/p1-live/`.
- Contract facts the extra assertions rely on (decisions of the static plan, `.dev/tasks/done/TASK-WF-writeTheP1Static-20261105-033458/artifacts/p1-static-report.md`): D-P1-1 graph and impact keep their existing `command` key (`graph`, `impact`) as the worker `command` field; D-P1-2 the report-style commands write `<report-dir>/<name>-report.md` unless `--output` names a file; D-P1-4 brainstorm passes `--unattended` and a nested report directory `<report-dir>/nested/<command>-<n>/` (n starts at 1) to its `/sc:analyze` enrichment and adversarial call, and skips research enrichment and the tasklist and task handoffs; D-P1-7 document needs `--output` for the external, api and guide types; D-P1-8 a failing test suite is a verdict, not a failed run; D-P1-9 adversarial `report_path` is its merged output or null; D-P1-11 init-lite writes the worker contract also on `--dry-run`.
- Live-check procedure, followed by every live task with its own check number `<NN>`, name `<name>`, command file `<command>.md`, brief, report directory `<R>` and extras. Evidence files go under `./artifacts/lc<NN>-...`:
  - Gate: read `./artifacts/preflight.md`. If its install line is FAIL, write `./artifacts/lc<NN>-result.md` with `not run: install precondition failed` and its recording-status line, and stop the task.
  - Worktree: `orca worktree create --repo id:de550e99-fa3c-42e2-abfe-1d092771c759 --name p1-live-<name> --base-branch refs/heads/ironbelly/OrcaCLICommandRefactor-P1 --no-parent --json`, receipt saved to `./artifacts/lc<NN>-worktree.json`. Its path must not contain `/.dev/worktrees/`, and `git -C <path> rev-parse HEAD` must print the sha recorded in `./artifacts/branch-tip.txt`. Save `git -C <path> branch --show-current` to `./artifacts/lc<NN>-branch.txt`. Then `make -C <path> sync-dev` must exit 0 (output to `./artifacts/lc<NN>-sync-dev.txt`). Then `git -C <path> status --porcelain` is saved as `./artifacts/lc<NN>-status-before.txt`. Any failure here fails step 1: record it, skip to Remove, and do not dispatch.
  - Section check: `grep -c '^## Unattended mode' <path>/.claude/commands/sc/<command>.md ~/.claude/commands/sc/<command>.md`, saved to `./artifacts/lc<NN>-unattended-check.txt`. For a command that accepts `--unattended` at P1 both copies must print 1; for troubleshoot (Task 21) both must print 0; for help (Task 22) the check is not made because that case is decided by the command name alone. A count other than the one required fails step 1: record it, skip to Remove, and do not dispatch.
  - Step 1: save the task's brief, exactly as written in its fenced block, to `./artifacts/lc<NN>-brief.txt`. Run `orca orchestration task-create --spec "$(cat ./artifacts/lc<NN>-brief.txt)" --task-title "P1 live check <NN>: <name>" --run <run_id> --json`, then `orca orchestration worker-start --task <task_id> --worktree path:<path> --agent claude --run <run_id> --json`, timed with `date +%s.%N` before and after. Save both receipts and the elapsed seconds to `./artifacts/lc<NN>-step1.txt`. Pass: worker-start exits 0 with `state: ready`. If worker-start fails, record steps 1-6 as FAIL or not run, release whatever the receipt says it still owns with `orca orchestration worker-release --dispatch <dispatch_id> --json` when it names a dispatch, then go to Step 7 and Remove.
  - Step 2: wait in turns of `orca orchestration check --run <run_id> --wait --types "worker_done,escalation,question" --timeout-ms 240000 --json`, and after every turn run `orca orchestration worker-show --dispatch <dispatch_id> --json`. Append one line per sample (UTC time and the `observation.agentWait` value) to `./artifacts/lc<NN>-step2-samples.txt`, so samples are at most 5 minutes apart. Pass: `observation.agentWait` is never non-null. When a step 2 turn returns the `worker_done` message, that message is step 3's message: save and acknowledge it, and do not wait again.
  - Step 3: keep waiting until `worker_done` arrives. When a turn ends with no message, read `orca orchestration worker-read --dispatch <dispatch_id> --source transcript --json`: a growing transcript means keep waiting. A `question` message is answered only with facts about the environment; a request for a decision is not answered, and step 3 fails. Save the `worker_done` message to `./artifacts/lc<NN>-step3.json`, then acknowledge its delivery with `orca orchestration check --run <run_id> --ack <delivery_id> --json`. Pass: exactly one `worker_done`; its `--outcome` matches the contract's `worker_status` under WC-5 (`succeeded` and `partial` give `succeeded`; `failed` and `blocked` give `failed`); its report path is the WC-4 contract path `<R>/return-contract.yaml`. The refusal checks of Tasks 18, 20, 21 and 22 replace this pass rule with their own (Task 19 keeps it).
  - Step 3 exits when no `worker_done` comes: (a) stall proof, meaning a transcript whose final agent turn sent no `worker_done`, or `exited` liveness in `orca orchestration worker-list --run <run_id> --json`: record step 3 FAIL with that proof, run `orca orchestration worker-stop --dispatch <dispatch_id> --json` and `orca orchestration task-update --id <task_id> --status failed --result cancelled --run <run_id> --json`, record steps 4-6 from what exists, then go to Step 7 and Remove; (b) a non-null `observation.agentWait` or an unanswered decision question with no stall proof: record step 2 or step 3 FAIL with that sample or message and keep waiting, because Orca forbids stopping a waiting worker without positive proof; if 60 minutes pass after that sample with no `worker_done` and no stall proof, record steps 3-6 FAIL, leave the worker and its worktree running, write their dispatch id and path into `lc<NN>-result.md` as left for the person, record Step 7 and Remove as not run because the worker is not settled, and move to the next task.
  - Step 4: `test -s <path>/<R>/return-contract.yaml`, then `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['worker_contract_version'] == '1'; assert d['worker_status'] in {'succeeded','partial','failed','blocked'}; assert d['command']; assert d['worker_status'] != 'blocked' or d.get('blocked_question')" <path>/<R>/return-contract.yaml`, both saved to `./artifacts/lc<NN>-step4.txt`, then the check's extra assertions. Pass: both commands exit 0 and every extra holds. The refusal checks replace this step with their own conditions.
  - Step 5: locate the worker's session file: `~/.claude/projects/<dir>/<session id>.jsonl`, where `<dir>` is the worktree path with each `/` replaced by `-`; `<dir>` must hold exactly one top-level `.jsonl` file and each subagent's file is under `<dir>/<session id>/subagents/`. Run the two P0 scripts on it after step 3 and before step 7, and save their output to `./artifacts/lc<NN>-session-analysis.txt`. Record the session file's path, byte length and sha256 in `./artifacts/lc<NN>-step5.md`; do not copy the file into the repo. Cross-check: read `orca orchestration worker-read --dispatch <dispatch_id> --source transcript --json` page 1, then once more with the returned `--cursor`, saved as `./artifacts/lc<NN>-transcript-1.json` and `./artifacts/lc<NN>-transcript-2.json`; record `contentComplete`, the time window page 1 covers and whether page 2 is empty; page 1 must show the same final `check` call and the same `worker_done` as the session file. Write `./artifacts/lc<NN>-step5.md` with one verdict and a quoted excerpt for each of five conditions, all read from the session file: no `AskUserQuestion` call in the top-level session or any subagent session (WC-2); the command was run in the worker's top-level session, not inside an Agent-tool call (WC-7); a `check` call appears after the command finished and before `worker_done` (WC-12); heartbeats (WC-10) satisfy limits (a) and (b) of spec 7.2 step 5 against the cadence quoted from the worker's preamble, with the run length and heartbeat count stated; no `worker-start`, `dispatch` or `task-create` call and no `worktree create --agent` or `agent launch` call in any Bash command of the top-level or any subagent session (WC-13), with read-only Orca calls listed. Pass: all five hold. A run shorter than the cadence passes condition 4 vacuously and is recorded as such. For the guard refusal checks (Tasks 20 to 22) the worker refuses before invoking anything, so condition 2 is recorded `not applicable: guard refused before any invocation` and is replaced by `the command was not invoked` (read from the session file); conditions 1, 3, 4 and 5 apply unchanged. For Tasks 18 and 19 the command itself refuses, so all five apply.
  - Step 6: `git -C <path> status --porcelain` saved to `./artifacts/lc<NN>-status-after.txt`, and `git -C <path> diff --cached --name-only` saved to `./artifacts/lc<NN>-index-after.txt`. Pass: every path not in `lc<NN>-status-before.txt` is under `<R>` or is a documented artifact of the command, with the file and line that documents it cited in `./artifacts/lc<NN>-step6.md`. Ignored paths are not checked. Any path the worker staged is listed in `lc<NN>-step6.md` as a WC-9 finding for the phase report.
  - Evidence copy: copy `<path>/<R>` into `./artifacts/lc<NN>-report/` (and any other file the task names) before Step 7.
  - Step 7: `orca orchestration worker-release --dispatch <dispatch_id> --json`, then `orca orchestration worker-list --run <run_id> --terminal-state reclaimable --json`, both saved to `./artifacts/lc<NN>-step7.txt`. Pass: the list returns no rows.
  - Remove: `orca worktree rm --worktree path:<path> --force --json`, saved to `./artifacts/lc<NN>-remove.json`. Then save `orca worktree list --json` to `./artifacts/lc<NN>-worktree-list-after.json`, the feature worktree's `git rev-parse HEAD` to `./artifacts/lc<NN>-head-after.txt`, and `git branch --list "<the name in lc<NN>-branch.txt>"` to `./artifacts/lc<NN>-branch-after.txt`.
  - Result: `./artifacts/lc<NN>-result.md` lists the worktree setup, the section check, steps 1-7 and Remove as PASS, FAIL or not run, one line each, with the evidence file for each, the extras result, and the check's overall verdict (PASS only when steps 1-7 all pass, with steps 3 and 4 as replaced for the refusal checks, and every extra holds). Its last line is `Recording status: complete (verdict recorded, not a task failure)`.
- Brief layout (spec 2.3). Each live task has one fenced brief in this layout, saved to `./artifacts/lc<NN>-brief.txt` and passed to `task-create --spec` unchanged. The first line is the guard line, so the Task text never starts with `/sc:`.
- Expected outcomes for the final review: a `lc<NN>-result.md` verdict of FAIL or `not verifiable`, or a refusal check whose refusal did not happen, is a recorded result, not a task failure. An AC-1.8 owner instruction that still reads `NOT YET GIVEN` makes Task 24 a recorded `not run`, not a task failure.
- AC-1.8 owner instruction (WC-9, decision D4): NOT YET GIVEN. `/sc:implement` may not prompt the owner during the run, so the owner's one sentence naming a local commit for the AC-1.8 check is given in the session before the run and copied here as given; the plan edit is allowed because it happens before the first task starts. No separate file is made.

## Phase 1: Preflight and run binding

## Task 1: Record the preflight facts, verify the install precondition and open the coordinator run

Before any other write, save `git status --porcelain` to `./artifacts/status-baseline.txt` and `orca worktree list --json` to `./artifacts/worktree-list-before.json`. Then write `./artifacts/preflight.md` from these checks, run in the feature worktree, each with its command and output: `echo "$ORCA_TERMINAL_HANDLE"` is non-empty; `git rev-parse HEAD` is saved to `./artifacts/branch-tip.txt` and `git branch --show-current` prints `ironbelly/OrcaCLICommandRefactor-P1`; `git rev-parse refs/heads/ironbelly/OrcaCLICommandRefactor-P1` prints the same commit; `git merge-base --is-ancestor 7127c2478756c9444afc600af3e3066b3f7f24db HEAD` exits 0; `git status --porcelain` shows no modified tracked file (a dirty tree makes the worktrees differ from the branch); `orca --version` is saved to `./artifacts/orca-version.txt`; `git remote get-url origin` prints `https://github.com/IronbellyOrg/IronClaude`; the AC-C6 command from spec line 278 (`grep -ho '"nestedWorkerMaxDepth":[0-9]*' "${ORCA_RUNTIME_SOURCE_PROFILE_PATH:-$HOME/.config/orca}"/profiles/*/orca-data.json`) prints only `"nestedWorkerMaxDepth":1`; `orca status --json` shows the runtime `ready`; `orca repo list --json` lists repo id `de550e99-fa3c-42e2-abfe-1d092771c759`. The install line: `cmp` every file under `src/superclaude/commands/` (the whole folder, changed or not) with its installed copy `~/.claude/commands/sc/<name>.md`; `cmp` every file path printed by `git diff --name-only "$(git merge-base master HEAD)" HEAD -- src/superclaude/skills` that still exists with its installed copy `~/.claude/skills/<skill>/<rest>` (a path deleted on the branch is listed as `deleted, skipped`); and `cmp ~/.claude/WORKER-CONTRACT.md src/superclaude/core/WORKER-CONTRACT.md`; the line is PASS only when every `cmp` exits 0, and the file lists each path with its exit code. Save the `--help` output of every Orca verb this plan uses (`status`, `repo list`, `worktree create`, `worktree rm`, `worktree list`, and `orchestration run-create`, `task-create`, `worker-start`, `check`, `worker-show`, `worker-read`, `worker-release`, `worker-list`, `worker-stop`, `task-update`) to `./artifacts/orca-help.txt`, and `claude --help` to `./artifacts/claude-help.txt`. Then run `orca orchestration run-create --objective "P1 live checks AC-1.2, AC-1.3, AC-1.5, AC-1.6, AC-1.7, AC-1.8 for the Orca worker contract" --json` and save the receipt to `./artifacts/live-run.json`. Last, save `git status --porcelain` to `./artifacts/status-end-t1.txt`.

Acceptance criteria:
- `./artifacts/preflight.md` shows every check above with its output, and each one passes; the install line lists every compared path with its `cmp` exit code and is PASS, or is FAIL with the differing paths named (a recorded result that stops every later live task).
- `./artifacts/branch-tip.txt` holds the 40-character branch tip, the ancestor check exits 0, and `./artifacts/orca-version.txt` holds the Orca version.
- `./artifacts/orca-help.txt` holds the help text of every verb listed (every Orca verb this plan calls), and every flag and selector the procedure uses appears in it; `./artifacts/claude-help.txt` shows `--max-budget-usd` and `--permission-mode`.
- `./artifacts/live-run.json` holds `result.run.id` and a `result.run.coordinator_handle` equal to the `ORCA_TERMINAL_HANDLE` recorded in `preflight.md`.
- `./artifacts/status-end-t1.txt` lists no path that is not in `./artifacts/status-baseline.txt` or under this package, and shows no tracked file modified that is not already modified in `./artifacts/status-baseline.txt`.

## Phase 2: Live checks on the eight report-style commands

## Task 2: Run live check lc01 on /sc:analyze

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 01, `<name>` = analyze, command file `analyze.md`, report directory `.dev/p1-live/analyze/`. Extra for step 4: the contract's `report_path` is non-null and that file exists in the worktree (default `<R>analyze-report.md`, D-P1-2). The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p1-live/analyze/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:analyze src/superclaude/cli/install_core.py --focus quality --depth quick --unattended --report-dir .dev/p1-live/analyze/
```

Acceptance criteria:
- `./artifacts/lc01-result.md` exists, records the section check, the worktree setup, steps 1 to 7 and Remove with the evidence file of each, the extra, and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc01-step5.md` holds the session file path, byte length and sha256, the heartbeat cadence quoted from the preamble, the run length and heartbeat count, and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason).
- `./artifacts/lc01-report/` holds a copy of `.dev/p1-live/analyze/` from the worktree, or `lc01-result.md` states that the directory was missing.
- Either `./artifacts/lc01-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc01-worktree-list-after.json` does not list `p1-live-analyze`, or `lc01-result.md` records why the worktree remains.

## Task 3: Run live check lc02 on /sc:build

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 02, `<name>` = build, command file `build.md`, report directory `.dev/p1-live/build/`. Extra for step 4: `report_path` is non-null and that file exists. In step 6 a build output such as `dist/` is a documented artifact when it is ignored or named in the build report, which `lc02-step6.md` cites. The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p1-live/build/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:build --type dev --unattended --report-dir .dev/p1-live/build/
```

Acceptance criteria:
- `./artifacts/lc02-result.md` exists, records the section check, the worktree setup, steps 1 to 7 and Remove with the evidence file of each, the extra, and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc02-step5.md` holds the session file path, byte length and sha256, the cadence, the run length and heartbeat count, and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason).
- `./artifacts/lc02-report/` holds a copy of `.dev/p1-live/build/` from the worktree, or `lc02-result.md` states that the directory was missing.
- Either `./artifacts/lc02-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc02-worktree-list-after.json` does not list `p1-live-build`, or `lc02-result.md` records why the worktree remains.

## Task 4: Run live check lc03 on /sc:business-panel

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 03, `<name>` = business-panel, command file `business-panel.md`, report directory `.dev/p1-live/business-panel/`. Extra for step 4: `report_path` is non-null and that file exists. The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p1-live/business-panel/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:business-panel .dev/orca-command-refactor/decisions/D1/option-a.md --mode discussion --experts "porter,drucker" --unattended --report-dir .dev/p1-live/business-panel/
```

Acceptance criteria:
- `./artifacts/lc03-result.md` exists, records the section check, the worktree setup, steps 1 to 7 and Remove with the evidence file of each, the extra, and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc03-step5.md` holds the session file path, byte length and sha256, the cadence, the run length and heartbeat count, and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason).
- `./artifacts/lc03-report/` holds a copy of `.dev/p1-live/business-panel/` from the worktree, or `lc03-result.md` states that the directory was missing.
- Either `./artifacts/lc03-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc03-worktree-list-after.json` does not list `p1-live-business-panel`, or `lc03-result.md` records why the worktree remains.

## Task 5: Run live check lc04 on /sc:design

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 04, `<name>` = design, command file `design.md`, report directory `.dev/p1-live/design/`. Extras for step 4: `report_path` is non-null and that file exists; step 6 shows no source file changed (D-P1-12: design changes no architecture under `--unattended`). The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p1-live/design/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:design "a read-only status endpoint that reports whether the installed commands match the repository" --type api --format spec --unattended --report-dir .dev/p1-live/design/
```

Acceptance criteria:
- `./artifacts/lc04-result.md` exists, records the section check, the worktree setup, steps 1 to 7 and Remove with the evidence file of each, the extras, and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc04-step5.md` holds the session file path, byte length and sha256, the cadence, the run length and heartbeat count, and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason).
- `./artifacts/lc04-report/` holds a copy of `.dev/p1-live/design/` from the worktree, or `lc04-result.md` states that the directory was missing.
- Either `./artifacts/lc04-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc04-worktree-list-after.json` does not list `p1-live-design`, or `lc04-result.md` records why the worktree remains.

## Task 6: Run live check lc05 on /sc:document

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 05, `<name>` = document, command file `document.md`, report directory `.dev/p1-live/document/`. Extra for step 4: `report_path` equals `.dev/p1-live/document/install_core_api.md` and that file exists (D-P1-7). The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p1-live/document/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:document src/superclaude/cli/install_core.py --type api --style brief --output .dev/p1-live/document/install_core_api.md --unattended --report-dir .dev/p1-live/document/
```

Acceptance criteria:
- `./artifacts/lc05-result.md` exists, records the section check, the worktree setup, steps 1 to 7 and Remove with the evidence file of each, the extra, and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc05-step5.md` holds the session file path, byte length and sha256, the cadence, the run length and heartbeat count, and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason).
- `./artifacts/lc05-report/` holds a copy of `.dev/p1-live/document/` from the worktree, or `lc05-result.md` states that the directory was missing.
- Either `./artifacts/lc05-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc05-worktree-list-after.json` does not list `p1-live-document`, or `lc05-result.md` records why the worktree remains.

## Task 7: Run live check lc06 on /sc:explain

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 06, `<name>` = explain, command file `explain.md`, report directory `.dev/p1-live/explain/`. Extra for step 4: `report_path` is non-null and that file exists. The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p1-live/explain/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:explain src/superclaude/cli/install_core.py --level basic --format text --unattended --report-dir .dev/p1-live/explain/
```

Acceptance criteria:
- `./artifacts/lc06-result.md` exists, records the section check, the worktree setup, steps 1 to 7 and Remove with the evidence file of each, the extra, and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc06-step5.md` holds the session file path, byte length and sha256, the cadence, the run length and heartbeat count, and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason).
- `./artifacts/lc06-report/` holds a copy of `.dev/p1-live/explain/` from the worktree, or `lc06-result.md` states that the directory was missing.
- Either `./artifacts/lc06-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc06-worktree-list-after.json` does not list `p1-live-explain`, or `lc06-result.md` records why the worktree remains.

## Task 8: Run live check lc07 on /sc:index

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 07, `<name>` = index, command file `index.md`, report directory `.dev/p1-live/index/`. Extras for step 4: `report_path` equals `.dev/p1-live/index/structure.md` and that file exists; step 6 shows no existing documentation file changed (D-P1-12: no existing manual documentation is overwritten under `--unattended`). The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p1-live/index/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:index src/superclaude/pm_agent --type structure --format md --output .dev/p1-live/index/structure.md --unattended --report-dir .dev/p1-live/index/
```

Acceptance criteria:
- `./artifacts/lc07-result.md` exists, records the section check, the worktree setup, steps 1 to 7 and Remove with the evidence file of each, the extras, and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc07-step5.md` holds the session file path, byte length and sha256, the cadence, the run length and heartbeat count, and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason).
- `./artifacts/lc07-report/` holds a copy of `.dev/p1-live/index/` from the worktree, or `lc07-result.md` states that the directory was missing.
- Either `./artifacts/lc07-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc07-worktree-list-after.json` does not list `p1-live-index`, or `lc07-result.md` records why the worktree remains.

## Task 9: Run live check lc08 on /sc:test

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 08, `<name>` = test, command file `test.md`, report directory `.dev/p1-live/test/`. Extras for step 4: `report_path` is non-null, that file exists and holds a verdict (D-P1-8); `pgrep -af -- '--watch'` shows no watcher process started by the worker. The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p1-live/test/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:test tests/skills/test_worker_contract.py --type unit --unattended --report-dir .dev/p1-live/test/
```

Acceptance criteria:
- `./artifacts/lc08-result.md` exists, records the section check, the worktree setup, steps 1 to 7 and Remove with the evidence file of each, the extras, and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc08-step5.md` holds the session file path, byte length and sha256, the cadence, the run length and heartbeat count, and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason).
- `./artifacts/lc08-report/` holds a copy of `.dev/p1-live/test/` from the worktree, or `lc08-result.md` states that the directory was missing.
- Either `./artifacts/lc08-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc08-worktree-list-after.json` does not list `p1-live-test`, or `lc08-result.md` records why the worktree remains.

## Phase 3: Live checks on the eight ready commands

## Task 10: Run live check lc09 on /sc:adversarial

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 09, `<name>` = adversarial, command file `adversarial.md`, report directory `.dev/p1-live/adversarial/` (the command's own `--output` flag). Extras for step 4: the contract's `artifacts` lists a path ending `adversarial/return-contract.yaml`, which exists in the worktree and holds the command's own nested `return_contract:` block unchanged in shape; `report_path` is the merged output file or null (D-P1-9). The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p1-live/adversarial/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:adversarial --compare .dev/orca-command-refactor/decisions/D1/option-a.md,.dev/orca-command-refactor/decisions/D1/option-b.md --depth quick --unattended --output .dev/p1-live/adversarial/
```

Acceptance criteria:
- `./artifacts/lc09-result.md` exists, records the section check, the worktree setup, steps 1 to 7 and Remove with the evidence file of each, the extras, and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc09-step5.md` holds the session file path, byte length and sha256, the cadence, the run length and heartbeat count, and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason).
- `./artifacts/lc09-report/` holds a copy of `.dev/p1-live/adversarial/` from the worktree, or `lc09-result.md` states that the directory was missing.
- Either `./artifacts/lc09-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc09-worktree-list-after.json` does not list `p1-live-adversarial`, or `lc09-result.md` records why the worktree remains.

## Task 11: Run live check lc10 on /sc:brainstorm

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 10, `<name>` = brainstorm, command file `brainstorm.md`, report directory `.dev/p1-live/brainstorm/` (the command's own `--output` flag). Extras for step 4: the contract keeps the command's own fields, `status` included, beside the worker fields; research enrichment is recorded as skipped; for each of the codebase-enrichment and adversarial waves that ran, the directory `nested/analyze-1/` or `nested/adversarial-1/` exists under the report directory, holds its own `return-contract.yaml` and is listed in `artifacts` (D-P1-4); a wave that did not run is recorded as not run with the reason from the contract. The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p1-live/brainstorm/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:brainstorm "how a coordinator should name report directories for parallel workers" --depth quick --proposals 2 --codebase --handoff none --unattended --output .dev/p1-live/brainstorm/
```

Acceptance criteria:
- `./artifacts/lc10-result.md` exists, records the section check, the worktree setup, steps 1 to 7 and Remove with the evidence file of each, the extras, and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc10-step5.md` holds the session file path, byte length and sha256, the cadence, the run length and heartbeat count, and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason); condition 2 also covers the nested `/sc:analyze` and adversarial calls, which are made by the command and are not checked by the brief guard.
- `./artifacts/lc10-report/` holds a copy of `.dev/p1-live/brainstorm/` from the worktree, including any `nested/` directories, or `lc10-result.md` states that the directory was missing.
- Either `./artifacts/lc10-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc10-worktree-list-after.json` does not list `p1-live-brainstorm`, or `lc10-result.md` records why the worktree remains.

## Task 12: Run live check lc11 on /sc:cleanup-audit

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 11, `<name>` = cleanup-audit, command file `cleanup-audit.md`, report directory `.dev/p1-live/cleanup-audit/`. Extra for step 4: the contract lists the audit output under `.claude-audit/` in `artifacts` or `report_path`. In step 6 the `.claude-audit/` directory of the worktree is a documented artifact of the command, which `lc11-step6.md` cites from `src/superclaude/commands/cleanup-audit.md`. The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p1-live/cleanup-audit/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:cleanup-audit tests/pr_submit --pass surface --unattended --report-dir .dev/p1-live/cleanup-audit/
```

Acceptance criteria:
- `./artifacts/lc11-result.md` exists, records the section check, the worktree setup, steps 1 to 7 and Remove with the evidence file of each, the extra, and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc11-step5.md` holds the session file path, byte length and sha256, the cadence, the run length and heartbeat count, and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason).
- `./artifacts/lc11-report/` holds a copy of `.dev/p1-live/cleanup-audit/` and of `.claude-audit/` from the worktree, or `lc11-result.md` states what was missing.
- Either `./artifacts/lc11-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc11-worktree-list-after.json` does not list `p1-live-cleanup-audit`, or `lc11-result.md` records why the worktree remains.

## Task 13: Run live check lc12 on /sc:graph

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 12, `<name>` = graph, command file `graph.md`, report directory `.dev/p1-live/graph/` (the command's own `--output-dir` flag). Extras for step 4: `command` equals `graph` (D-P1-1) and `report_path` is null; step 5 shows no codegraph build command (`codegraph init` or `index`) in any Bash command of the session (a `codegraph sync` is listed as a note, not a failure). The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p1-live/graph/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:graph status --unattended --output-dir .dev/p1-live/graph/
```

Acceptance criteria:
- `./artifacts/lc12-result.md` exists, records the section check, the worktree setup, steps 1 to 7 and Remove with the evidence file of each, the extras, and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc12-step5.md` holds the session file path, byte length and sha256, the cadence, the run length and heartbeat count, and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason).
- `./artifacts/lc12-report/` holds a copy of `.dev/p1-live/graph/` from the worktree, or `lc12-result.md` states that the directory was missing.
- Either `./artifacts/lc12-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc12-worktree-list-after.json` does not list `p1-live-graph`, or `lc12-result.md` records why the worktree remains.

## Task 14: Run live check lc13 on /sc:impact

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 13, `<name>` = impact, command file `impact.md`, report directory `.dev/p1-live/impact/` (the new `--report-dir` flag on a command that also has `--output-dir`). Extras for step 4: `command` equals `impact` (D-P1-1); `report_path` ends with `impact.md` and that file exists. The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p1-live/impact/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:impact install_core_files --depth 1 --limit 10 --unattended --report-dir .dev/p1-live/impact/
```

Acceptance criteria:
- `./artifacts/lc13-result.md` exists, records the section check, the worktree setup, steps 1 to 7 and Remove with the evidence file of each, the extras, and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc13-step5.md` holds the session file path, byte length and sha256, the cadence, the run length and heartbeat count, and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason).
- `./artifacts/lc13-report/` holds a copy of `.dev/p1-live/impact/` from the worktree and of the default `.dev/impact/` directory if the command wrote one there, or `lc13-result.md` states what was missing.
- Either `./artifacts/lc13-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc13-worktree-list-after.json` does not list `p1-live-impact`, or `lc13-result.md` records why the worktree remains.

## Task 15: Run live check lc14 on /sc:index-repo

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 14, `<name>` = index-repo, command file `index-repo.md`, report directory `.dev/p1-live/index-repo/`. Extra for step 4: the contract lists `PROJECT_INDEX.md` and `PROJECT_INDEX.json`. In step 6 those two files at the worktree root are documented artifacts of the command (they are tracked files, so they may show as modified), which `lc14-step6.md` cites from `src/superclaude/commands/index-repo.md`. The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p1-live/index-repo/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:index-repo mode=quick --unattended --report-dir .dev/p1-live/index-repo/
```

Acceptance criteria:
- `./artifacts/lc14-result.md` exists, records the section check, the worktree setup, steps 1 to 7 and Remove with the evidence file of each, the extra, and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc14-step5.md` holds the session file path, byte length and sha256, the cadence, the run length and heartbeat count, and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason).
- `./artifacts/lc14-report/` holds a copy of `.dev/p1-live/index-repo/`, `PROJECT_INDEX.md` and `PROJECT_INDEX.json` from the worktree, or `lc14-result.md` states what was missing.
- Either `./artifacts/lc14-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc14-worktree-list-after.json` does not list `p1-live-index-repo`, or `lc14-result.md` records why the worktree remains.

## Task 16: Run live check lc15 on /sc:init-lite

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 15, `<name>` = init-lite, command file `init-lite.md`, report directory `.dev/p1-live/init-lite/`. Extras for step 4: the contract is written although the run is a `--dry-run` (D-P1-11); step 6 shows no `.dev/superclaude/` directory created. The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p1-live/init-lite/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:init-lite --context-optimized --dry-run --unattended --report-dir .dev/p1-live/init-lite/
```

Acceptance criteria:
- `./artifacts/lc15-result.md` exists, records the section check, the worktree setup, steps 1 to 7 and Remove with the evidence file of each, the extras, and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc15-step5.md` holds the session file path, byte length and sha256, the cadence, the run length and heartbeat count, and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason).
- `./artifacts/lc15-report/` holds a copy of `.dev/p1-live/init-lite/` from the worktree, or `lc15-result.md` states that the directory was missing.
- Either `./artifacts/lc15-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc15-worktree-list-after.json` does not list `p1-live-init-lite`, or `lc15-result.md` records why the worktree remains.

## Task 17: Run live check lc16 on /sc:workflow

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 16, `<name>` = workflow, command file `workflow.md`, report directory `.dev/p1-live/workflow/`. Extras for step 4: exactly one new `TASK-WF-*` package directory exists under `.dev/tasks/to-do/` in the worktree and shows as new in step 6 (a documented artifact of the command, `src/superclaude/commands/workflow.md`); `report_path` is that package's `<id>.md`; `artifacts` lists the package's `return-contract.yaml` and `source.md`; the index of the worktree is empty (the worker did not stage `.dev/tasks`, D-P1-5 and the section's outward-action rule). This is expected to be the longest run of the phase. The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p1-live/workflow/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:workflow "Add one sentence to the Installation section of README.md stating that superclaude install --force overwrites files that already exist in ~/.claude" --depth quick --handoff none --unattended --report-dir .dev/p1-live/workflow/
```

Acceptance criteria:
- `./artifacts/lc16-result.md` exists, records the section check, the worktree setup, steps 1 to 7 and Remove with the evidence file of each, the extras, and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc16-step5.md` holds the session file path, byte length and sha256, the cadence, the run length and heartbeat count, and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason).
- `./artifacts/lc16-report/` holds a copy of `.dev/p1-live/workflow/` and of the new `TASK-WF-*` package from the worktree, or `lc16-result.md` states what was missing.
- Either `./artifacts/lc16-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc16-worktree-list-after.json` does not list `p1-live-workflow`, or `lc16-result.md` records why the worktree remains.

## Phase 4: Refusal live checks

## Task 18: Run live check lc17 on /sc:analyze without a report directory (AC-1.5)

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 17, `<name>` = missing-report-dir, command file `analyze.md`, with steps 3 and 4 replaced by this task's conditions (spec 7.3 AC-1.5). There is no report directory, so the evidence copy step is skipped and `lc17-result.md` says so. Pass conditions: step 6 shows nothing written (every path in the status-after file is also in the status-before file); the worker's reply in the transcript or the session file shows the exact text `unattended mode needs exactly one report directory: --report-dir <dir>, or this command's own directory output flag`; `worker_done` has `--outcome failed` and no `--report-path`; step 2 never shows `agentWait`. The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: none
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:analyze src/ --unattended
```

Acceptance criteria:
- `./artifacts/lc17-result.md` exists, records the section check, the worktree setup, steps 1, 2, 5, 6, 7 and Remove, the replaced step 3 and 4 conditions (each PASS or FAIL with its evidence file), and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc17-step3.json` holds the `worker_done` message, and `lc17-result.md` quotes the exact error text from the transcript or session file, or records that it was not found.
- `./artifacts/lc17-step5.md` holds the session file path, byte length and sha256 and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason).
- Either `./artifacts/lc17-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc17-worktree-list-after.json` does not list `p1-live-missing-report-dir`, or `lc17-result.md` records why the worktree remains.

## Task 19: Run live check lc18 on /sc:test --watch under --unattended (AC-1.6)

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 18, `<name>` = person-mode-watch, command file `test.md`, report directory `.dev/p1-live/watch/`. Step 3 keeps its pass rule, and step 4 adds these conditions (spec 7.3 AC-1.6): the contract has `worker_status: failed` with `--watch` in `reason`; `worker_done` has `--outcome failed`; `pgrep -af -- '--watch'` is saved before dispatch and after the worker settles, and the second output has no new process. The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p1-live/watch/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:test --watch --unattended --report-dir .dev/p1-live/watch/
```

Acceptance criteria:
- `./artifacts/lc18-result.md` exists, records the section check, the worktree setup, steps 1 to 7 and Remove with the evidence file of each, the contract conditions and the process check, and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc18-step4.txt` shows the contract's `worker_status` and `reason`, and `./artifacts/lc18-pgrep-before.txt` and `./artifacts/lc18-pgrep-after.txt` hold the two process listings.
- `./artifacts/lc18-step5.md` holds the session file path, byte length and sha256, the cadence, the run length and heartbeat count, and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason).
- Either `./artifacts/lc18-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc18-worktree-list-after.json` does not list `p1-live-person-mode-watch`, or `lc18-result.md` records why the worktree remains.

## Task 20: Run live check lc19 on the brief guard, case 1 (AC-1.7)

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 19, `<name>` = guard-case1, command file `analyze.md`, with steps 3 and 4 replaced by this task's conditions (spec 7.3 AC-1.7, case 1: a converted command with its report directory and no `--unattended`). Pass conditions: step 6 shows nothing written; `worker_done` has `--outcome failed`, no `--report-path`, and a body starting `guard refused:`; step 2 never shows `agentWait`; step 5 shows the command was not run. The evidence copy step is skipped and `lc19-result.md` says so. The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p1-live/guard1/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:analyze src/superclaude/cli/install_core.py --report-dir .dev/p1-live/guard1/
```

Acceptance criteria:
- `./artifacts/lc19-result.md` exists, records the section check, the worktree setup, steps 1, 2, 5, 6, 7 and Remove, the replaced step 3 and 4 conditions (each PASS or FAIL with its evidence file), and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc19-step3.json` holds the `worker_done` message, and `lc19-result.md` quotes the first words of its body (expected `guard refused: brief lacks --unattended`).
- `./artifacts/lc19-step5.md` holds the session file path, byte length and sha256 and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason), and states whether `/sc:analyze` was invoked.
- Either `./artifacts/lc19-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc19-worktree-list-after.json` does not list `p1-live-guard-case1`, or `lc19-result.md` records why the worktree remains.

## Task 21: Run live check lc20 on the brief guard, case 2 (AC-1.7)

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 20, `<name>` = guard-case2, command file `troubleshoot.md` (not converted at P1, so both copies print 0 in the section check), with steps 3 and 4 replaced by this task's conditions (spec 7.3 AC-1.7, case 2: a command with no section and the flag). Pass conditions: step 6 shows nothing written; `worker_done` has `--outcome failed`, no `--report-path`, and a body starting `guard refused:`; step 2 never shows `agentWait`; step 5 shows the command was not run. The evidence copy step is skipped and `lc20-result.md` says so. The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: .dev/p1-live/guard2/
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:troubleshoot "the install check prints nothing" --unattended --report-dir .dev/p1-live/guard2/
```

Acceptance criteria:
- `./artifacts/lc20-result.md` exists, records the section check, the worktree setup, steps 1, 2, 5, 6, 7 and Remove, the replaced step 3 and 4 conditions (each PASS or FAIL with its evidence file), and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc20-unattended-check.txt` shows 0 for both copies of `troubleshoot.md`, and `./artifacts/lc20-step3.json` holds the `worker_done` message, whose body starts `guard refused:` (expected `guard refused: loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale)`).
- `./artifacts/lc20-step5.md` holds the session file path, byte length and sha256 and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason), and states whether `/sc:troubleshoot` was invoked.
- Either `./artifacts/lc20-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc20-worktree-list-after.json` does not list `p1-live-guard-case2`, or `lc20-result.md` records why the worktree remains.

## Task 22: Run live check lc21 on the brief guard, case 3 (AC-1.7)

Depends on: Task 1

Follow the live-check procedure in Constraints with `<NN>` = 21, `<name>` = guard-case3, command file `help.md` (the section check is not made: case 3 is decided by the command name alone), with steps 3 and 4 replaced by this task's conditions (spec 7.3 AC-1.7, case 3: a command on the never-as-worker list; `/sc:help` is used, never `/sc:pm`, `/sc:agent`, `/sc:git` or `/sc:pr-submit`). Pass conditions: step 6 shows nothing written; `worker_done` has `--outcome failed`, no `--report-path`, and a body starting `guard refused:`; step 2 never shows `agentWait`; the step 5 analysis of the session file shows `/sc:help` was never invoked (no Skill or command call naming it). The evidence copy step is skipped and `lc21-result.md` says so. The brief:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: none
Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:help
```

Acceptance criteria:
- `./artifacts/lc21-result.md` exists, records the worktree setup, steps 1, 2, 5, 6, 7 and Remove, the replaced step 3 and 4 conditions (each PASS or FAIL with its evidence file), and the overall verdict, and ends with the recording-status line (or records `not run: install precondition failed`).
- `./artifacts/lc21-step3.json` holds the `worker_done` message, and `lc21-result.md` quotes the first words of its body (expected to start `guard refused:`).
- `./artifacts/lc21-step5.md` holds the session file path, byte length and sha256 and a verdict with a quoted excerpt for each of the five conditions (or states `not verifiable` with the reason), and states that `/sc:help` was never invoked or quotes the call that invoked it.
- Either `./artifacts/lc21-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt` and `./artifacts/lc21-worktree-list-after.json` does not list `p1-live-guard-case3`, or `lc21-result.md` records why the worktree remains.

## Phase 5: Flagless behaviour and the commit grant

## Task 23: Run the AC-1.3 flagless file-creation check

Depends on: Task 1

Gate: read `./artifacts/preflight.md`; if its install line is FAIL, write `./artifacts/ac-1.3.md` with `not run: install precondition failed` and stop. Otherwise create one scratch worktree like the procedure's Worktree step with `<name>` = flagless and files `./artifacts/ac13-...` (receipt `ac13-worktree.json`, `make -C <path> sync-dev` output, `git -C <path> status --short` saved as `ac13-status-before.txt`). In it run these two print-mode sessions, each under `timeout 1200`, with the output saved to `./artifacts/ac13-run-1.txt` and `./artifacts/ac13-run-2.txt`, and `git -C <path> status --short` saved after each as `ac13-status-after-1.txt` and `ac13-status-after-2.txt`: `claude -p "/sc:analyze src/superclaude/cli/install_core.py --depth quick" --max-budget-usd 2 --permission-mode acceptEdits` and `claude -p "/sc:explain src/superclaude/cli/install_core.py --level basic" --max-budget-usd 2 --permission-mode acceptEdits`, each started with the worktree as its current directory (`cd <path>` inside the same Bash command). Then `find <path> -name return-contract.yaml -not -path '*/.git/*'` is saved to `./artifacts/ac13-find.txt`; tracked files that existed before the runs do not count. Remove the worktree as in the procedure's Remove step (`ac13-remove.json`, `ac13-worktree-list-after.json`). If a `claude -p` run fails to start or is refused by the budget, record that faithfully and do not retry. Write `./artifacts/ac-1.3.md`: the file-creation result (PASS only when both runs completed and the find output is empty; FAIL when a contract file appears; `not verifiable` with the reason when a run did not complete), the two runs' tail output, and the open owner item for the manual part: "run `/sc:analyze <path>` and `/sc:explain <path>` in a plain interactive Claude Code session and in the coordinator session with `WORKER-CONTRACT.md` loaded, and confirm that today's prompts and defaults appear and that no brief-guard refusal occurs". The file ends with the line `Recording status: complete (verdict recorded, not a task failure)`.

Acceptance criteria:
- `./artifacts/ac-1.3.md` exists with the file-creation verdict, the evidence files `ac13-run-1.txt`, `ac13-run-2.txt`, `ac13-find.txt`, the status-before and status-after files, the manual owner item quoted above, and the recording-status line.
- Either `./artifacts/ac13-worktree-list-after.json` does not list `p1-live-flagless`, or `ac-1.3.md` records why the worktree remains.
- The feature worktree's HEAD is unchanged: `git rev-parse HEAD` printed into `./artifacts/ac13-head-after.txt` shows the sha recorded in `./artifacts/branch-tip.txt`.

## Task 24: Run live check lc22, the WC-9 commit grant (AC-1.8)

Depends on: Task 1

Gate: read `./artifacts/preflight.md`; if its install line is FAIL, write `./artifacts/lc22-result.md` with `not run: install precondition failed` and its recording-status line, and stop. Then read the bullet "AC-1.8 owner instruction" in Constraints. It holds the owner's own instruction, given in the session and copied into this plan as given, that names a local commit for this one Task (WC-9, decision D4); no separate file is used. If it still reads `NOT YET GIVEN`, write `./artifacts/lc22-result.md` with `not run: no owner instruction`, the verdict `NOT RUN`, and the recording-status line, start nothing, and stop; the phase report carries this as an open owner item.

Otherwise, before dispatch save the four records to `./artifacts/lc22-before-head.txt` (`git log -1 --format=%H` in the feature worktree), `lc22-before-refs.txt` (`git for-each-ref refs/heads` in the feature worktree), `lc22-before-lsremote.txt` (`git ls-remote origin`, after `git remote get-url origin` prints `https://github.com/IronbellyOrg/IronClaude`) and `lc22-before-prs.txt` (`gh pr list --repo IronbellyOrg/IronClaude --author @me`). Save the brief to `./artifacts/lc22-brief.txt`, with the one allowed substitution below, and create the child worktree first, as spec 7.2 step 1 allows (a child created by Orca keeps its parent lineage, WC-11; the repo's rule is never raw `git worktree add`): `orca worktree create --repo id:de550e99-fa3c-42e2-abfe-1d092771c759 --name p1-live-commit-grant --base-branch refs/heads/ironbelly/OrcaCLICommandRefactor-P1 --parent-worktree active --json`, receipt `./artifacts/lc22-worktree.json`. Its path must not contain `/.dev/worktrees/` and `git -C <path> rev-parse HEAD` must print the sha recorded in `./artifacts/branch-tip.txt`; `make -C <path> sync-dev` must exit 0; save `git -C <path> branch --show-current` as `lc22-branch.txt` and `git -C <path> status --porcelain` as `lc22-status-before.txt`. Any failure here fails the check: record it, remove the worktree, and do not dispatch. Then run `task-create` as in the procedure's Step 1 and start the worker with `orca orchestration worker-start --task <task_id> --worktree path:<path> --agent claude --run <run_id> --json` (no `--setup` flag: the sync was run by the coordinator, so no setup slot needs the user's instruction). Then follow the procedure's steps 2 to 7 with `<NN>` = 22, `<name>` = commit-grant, command file `explain.md` and report directory `.dev/p1-live/commit-grant/`. Before dispatch, `grep -c '^## Unattended mode'` on `<path>/.claude/commands/sc/explain.md` and `~/.claude/commands/sc/explain.md` must print 1 for both (`lc22-unattended-check.txt`). After the run save the four records again as `lc22-after-head.txt` and `lc22-after-refs.txt` (both taken in the child worktree), `lc22-after-lsremote.txt` and `lc22-after-prs.txt`, and `git -C <path> log --format='%H %P %s' <the sha in ./artifacts/branch-tip.txt>..HEAD` and `git -C <path> show --stat --format=%H HEAD` as `lc22-commits.txt`. Pass conditions beyond the procedure: the worker made a commit only after the contract showed `worker_status: succeeded`; the only change is new commits on the child's own branch; every path in them is under `.dev/p1-live/commit-grant/`, the contract's `report_path` and `artifacts`, or `.dev/tasks`; no `--no-verify` appears in any Bash command of the session; the before and after `git ls-remote origin` outputs are identical and the before and after PR lists are identical. Remove the child worktree with `orca worktree rm --worktree path:<path> --force --json` after recording its commit id in `lc22-result.md`.

The brief, with one allowed substitution: `<OWNER INSTRUCTION>` is replaced by the text of the Constraints bullet "AC-1.8 owner instruction", copied as it stands, and nothing else in the brief changes:

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: authorized for this one Task. Owner instruction, quoted as given: <OWNER INSTRUCTION>
Report directory: .dev/p1-live/commit-grant/
Worktree: child worktree created by Orca (orca worktree create --parent-worktree active) from ironbelly/OrcaCLICommandRefactor-P1 for this check only; you are its only writer.
Outward actions: none other than the local commit above; the coordinator performs every push, PR, comment, install and paid run.
Command: /sc:explain src/superclaude/cli/install_core.py --level basic --format text --unattended --report-dir .dev/p1-live/commit-grant/
```

Acceptance criteria:
- `./artifacts/lc22-result.md` exists and either records `not run: no owner instruction` (the Constraints bullet still reads `NOT YET GIVEN`) or `not run: install precondition failed`, or records the section check, steps 1 to 7, Remove and the commit-grant conditions with the evidence file of each, and the overall verdict; it ends with the recording-status line.
- When the check ran, `./artifacts/lc22-commits.txt` and the four before and four after record files exist, and `lc22-result.md` states whether `git ls-remote origin` and the PR list are identical before and after.
- When the check ran, `./artifacts/lc22-step5.md` holds the session file path, byte length and sha256 and a verdict with a quoted excerpt for each of the five conditions, and states whether any Bash command used `--no-verify` or `git push`.
- When the check ran, either `./artifacts/lc22-worktree-list-after.json` does not list `p1-live-commit-grant`, or `lc22-result.md` records why the child worktree remains.

## Phase 6: P1 phase report

## Task 25: Write the P1 phase report and stage the package

Depends on: Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10, Task 11, Task 12, Task 13, Task 14, Task 15, Task 16, Task 17, Task 18, Task 19, Task 20, Task 21, Task 22, Task 23, Task 24

Create `./artifacts/p1-phase-report.md` stub-first from the section layout of `.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/p0-phase-report.md`, then fill each section from the saved evidence. Sections: the header (plan, spec, checkout branch and HEAD from `git rev-parse HEAD`, run date, Orca runtime version from `./artifacts/orca-version.txt`, run id from `./artifacts/live-run.json`); the P1 verdict; the static part, cited from `.dev/tasks/done/TASK-WF-writeTheP1Static-20261105-033458/artifacts/p1-static-report.md` (its PASS lines for AC-1.1, AC-1.4, AC-C1 to AC-C6 named, evidence not copied); the live part, a table with one row per check (lc01 to lc22 and ac-1.3) giving its verdict taken from the `lc<NN>-result.md` or `ac-1.3.md` file and that evidence file; a heartbeat section giving, per check, the run length and heartbeat count from its `lc<NN>-step5.md`, and naming at least one checked run that lasted longer than the heartbeat cadence; the brief-guard refusal bodies quoted from `lc19`, `lc20` and `lc21`; the exact WC-4 error text from `lc17`; branches that remain after removal (from the `lc<NN>-branch-after.txt` files); workers or worktrees left for the person; staging found inside a disposable worktree (from the `lc<NN>-index-after.txt` files); the open owner items (the manual part of AC-1.3 quoted from `ac-1.3.md`, and AC-1.8 when `lc22-result.md` says it was not run); and notes for the coordinator and owner (deviations, `not verifiable` items, anything that bears on P2). The verdict line reads `P1 verdict: PASS` only when every check the plan ran has the verdict PASS and nothing is `not verifiable` or `not run`; otherwise it reads `P1 verdict: FAIL` or `P1 verdict: PASS pending`, followed by the cause and the check ids, and a FAIL of AC-1.2 on a command is recorded as a gap in that command. The report states that the phase passes only when this report and the static report both pass. Then save `git rev-parse HEAD` to `./artifacts/head-final.txt`, `git status --porcelain` to `./artifacts/status-final.txt`, run `git add .dev/tasks`, and save `git diff --cached --name-only` to `./artifacts/staged.txt`.

Acceptance criteria:
- `./artifacts/p1-phase-report.md` exists with every section above filled (no placeholder text left), one table row for each of lc01 to lc22 and ac-1.3, each naming an evidence file that exists under `./artifacts/`, and a line starting `P1 verdict:`.
- The report's verdict agrees with the check rows: a row that reads FAIL, `not verifiable` or `not run` appears in the cause of a verdict that is not `P1 verdict: PASS`, and `./artifacts/lc22-result.md` or the report states plainly when AC-1.8 was not run for lack of the owner grant file.
- `./artifacts/head-final.txt` shows the sha recorded in `./artifacts/branch-tip.txt`, and `./artifacts/staged.txt` lists this package's files and no path under `.claude/`.
- `./artifacts/status-final.txt` lists no tracked file modified that is not already modified in `./artifacts/status-baseline.txt`, apart from this package's own files.
