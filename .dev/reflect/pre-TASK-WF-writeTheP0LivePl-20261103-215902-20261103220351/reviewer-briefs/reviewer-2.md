# Reviewer 2 brief (persona: qa)

## T1 card excerpt

## QA: coverage and acceptance

### F-009: Task 1's git-status AC fails on a correct run: five untracked paths exist, not four
- Severity: should-fix
- Claim: The AC allows "the four untracked folders that existed before the plan". The worktree already has five untracked paths outside this package. The fifth is `.dev/reflect/pre-TASK-WF-writeTheP0LivePl-...`, written by the plan's own Wave-4 reflect. A reviewer reading the AC literally finds an unlisted change.
- Evidence:
  - `plan:52` "`git status --porcelain` shows no change outside this package and the four untracked folders that existed before the plan."
  - `git status --porcelain` (run now): two `.dev/brainstorms/...` folders, `.dev/reflect/pre-TASK-WF-writeTheP0LivePl-20261103-215902-20261103220351/`, `.dev/review-loop-convergence/`, `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/`, plus this package.
- Tag: Grounded
- Fix: List the allowed paths by name, including `.dev/reflect/pre-TASK-WF-writeTheP0LivePl-20261103-215902-*`. Better: save `git status --porcelain` at the start of Task 1 to `./artifacts/status-baseline.txt`, and make the AC "no path beyond status-baseline.txt and this package".

### F-010: Several ACs have no saved evidence file
- Severity: should-fix
- Claim: The managed reviewer works from the diff and the package's `./artifacts/` files. These ACs name live state that no file records: "`orca worktree list --json` no longer lists ... and the feature worktree's HEAD is unchanged" (Tasks 2-4), Task 1's `git status` check and Task 5's `git rev-parse HEAD`. A claim the reviewer cannot verify with no evidence row counts as `ac-outcome-missing=yes`, which is blocking and costs a fix pass.
- Evidence:
  - `plan:80` "`orca worktree list --json` no longer lists the `p0-live-troubleshoot` worktree, and the feature worktree's HEAD is unchanged." (same at `plan:106`, `plan:131`)
  - `plan:145` "`git rev-parse HEAD` still prints `8db29f1165508187b7a14a48f2f66793e269d596`."
  - `~/.claude/skills/sc-implement-protocol/refs/qa.md:87` "a claim the reviewer could not verify has no evidence row (`ac-outcome-missing=yes`, anchored on the AC words)."
- Tag: Grounded
- Fix: Add saved outputs: `orca worktree list --json` to `lc<N>-worktree-list-after.json`, `git rev-parse HEAD` to `lc<N>-head-after.txt`, Task 1's status into `preflight.md`, and Task 5's HEAD to `./artifacts/head-final.txt`. Have each AC cite its file.

### F-011: An absent `agentWait` counts as a pass
- Severity: minor
- Claim: "Never non-null" is also true when the field is missing, and Orca says a missing field means it never looked. Step 2 can pass without Orca ever checking.
- Evidence: `plan:32` "Pass: `observation.agentWait` is never non-null."; `.dev/orca-command-refactor/inventory/orca-capabilities.md:129` "An absent field means it never looked"
- Tag: Grounded
- Fix: Record `absent` separately in each sample line. Write step 2 as "PASS (observed)" only when at least one sample is a non-absent null; otherwise "PASS (not observed)", and carry that wording into the phase report.

### F-012: The unattended-section grep exits 1 on its passing result
- Severity: minor
- Claim: With two files and no match, `grep -c` prints `file:0` for each file and exits 1. An executor that treats a non-zero exit as failure records a false FAIL.
- Evidence: `plan:30` "`grep -c '^## Unattended mode' <path>/.claude/commands/sc/<command>.md ~/.claude/commands/sc/<command>.md` ... must show 0 for both copies"
- Tag: [INFERRED] (standard grep exit behaviour)
- Fix: State "exit 1 with both counts 0 is the pass; exit 2 (a file is missing) is a FAIL."

### F-013: The wait command runs longer than the default Bash tool timeout
- Severity: minor
- Claim: `check --wait --timeout-ms 240000` blocks for up to 240 s. The executor's Bash tool defaults to 120 s, so the call is killed first unless the plan sets a longer timeout.
- Evidence: `plan:32` "`orca orchestration check --wait --types \"worker_done,escalation,question\" --timeout-ms 240000 --json`"
- Tag: [INFERRED] (Claude Code Bash default timeout of 120000 ms)
- Fix: Add "run each wait with a Bash tool timeout of at least 300000 ms".

### F-014: AC-0.6 needs a transcript read that the plan does not place
- Severity: minor
- Claim: AC-0.6 must be answered "before Step 5". Before step 5, though, the transcript is read only when a wait ends with no message, which may never happen. The executor has to add a read the plan does not name.
- Evidence: `plan:73` "Before Step 5, answer AC-0.6 (spec line 303) from this worker's transcript"; `plan:33` "When a turn ends with no message, read `orca orchestration worker-read ... --source transcript --json`"
- Tag: Grounded
- Fix: "After Step 4, read the first page with `worker-read --dispatch <id> --source transcript --json`, save it as `lc1-ac06-page.json`, and answer AC-0.6 from it."

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-03T22:04:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs projectPath=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs

# Grounding hunks

Verbatim excerpts the T1 card and the coverage matrix rely on. Paths are relative to the repo root unless they start with `~`. Long single lines are excerpted to the relevant clause, unchanged.

### .dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/source.md:1-1
```text
Scope is exactly the P0 live checks and the phase report: AC-0.4 (section 7.3 row: three section 7.2 live checks, one each for /sc:troubleshoot "<real symptom>" --output-dir <dir> with no --fix and no --depth deep, /sc:workflow "<small change>" --handoff none, and /sc:adversarial --compare <two files> --depth quick --output <dir>, each run directly by the worker with the AC-0.4 report-file and outcome rule in its brief), AC-0.5 (timed worker-start under 45 s with the normal launch setup), AC-0.6 (whether worker-read --source transcript names tool calls, with a quoted excerpt), all seven section 7.2 steps per live check
...
Constraints: no edit to any source, command, skill, agent or test file; no git commit, push, PR, gh write or superclaude install; no interaction with the SuperClaude-Org upstream; UV only; never stage .claude/; leave the superseded package .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/ unstaged and untouched; stage .dev/tasks at the end.
...
A failed live check is recorded in the phase report, not retried silently; per spec AC-0.4 a failure reopens section 1.
```

### .dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/TASK-WF-writeTheP0LivePl-20261103-215902.md:22-25
```text
- No git commit, push, merge, rebase, reset, stash, branch deletion, PR, `gh` write of any kind, and no `superclaude install` in any form. The only git-state changes are the disposable worktrees that `orca worktree create` makes and `orca worktree rm` removes, as the live-check procedure below states. No interaction with the SuperClaude-Org upstream repository.
- UV for every Python command. Test runs set `PYTHONDONTWRITEBYTECODE=1` and pass `-p no:cacheprovider`.
- Never stage anything under `.claude/`. Leave `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/` untouched and unstaged. Leave `.dev/brainstorms/` and `.dev/review-loop-convergence/` untouched.
- A failed live check is a recorded result: it is not retried, rerun or repaired, and no second worker is started for it. A task is compliant when its check ran as written and every step's result is recorded faithfully with its evidence; a FAIL is then carried into the phase report, where per AC-0.4 it reopens spec section 1.
```

### .dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/TASK-WF-writeTheP0LivePl-20261103-215902.md:28-30
```text
- Live-check procedure, followed by Tasks 2, 3 and 4 with their own check number `<N>`, name `<name>`, brief and report file. Evidence files go under `./artifacts/lc<N>-...`:
  - Worktree: `orca worktree create --repo id:de550e99-fa3c-42e2-abfe-1d092771c759 --name p0-live-<name> --base-branch ironbelly/OrcaCLICommandRefactor-Specs --no-parent --json`, receipt saved to `./artifacts/lc<N>-worktree.json`. Its path must not contain `/.dev/worktrees/`, and `git -C <path> rev-parse HEAD` must print `8db29f1165508187b7a14a48f2f66793e269d596`. Then `make -C <path> sync-dev` must exit 0 (spec line 282: make sync-dev runs before dispatch, because Orca's `--setup run` is not confirmed to do it, UNVERIFIED item 27). Then `git -C <path> status --porcelain` is saved as `./artifacts/lc<N>-status-before.txt`. Any failure here fails step 1: record it, skip to Remove, and do not dispatch.
  - No-unattended check: `grep -c '^## Unattended mode' <path>/.claude/commands/sc/<command>.md ~/.claude/commands/sc/<command>.md`, saved to `./artifacts/lc<N>-unattended-check.txt`, must show 0 for both copies, which confirms the brief's `Command:` line rightly has no `--unattended` at P0.
```

### .dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/TASK-WF-writeTheP0LivePl-20261103-215902.md:32-33
```text
  - Step 2: wait in turns of `orca orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 240000 --json`, and after every turn run `orca orchestration worker-show --dispatch <dispatch_id> --json`. Append one line per sample (UTC time and the `observation.agentWait` value) to `./artifacts/lc<N>-step2-samples.txt`, so samples are at most 5 minutes apart. Pass: `observation.agentWait` is never non-null.
  - Step 3: keep waiting until `worker_done` arrives. When a turn ends with no message, read `orca orchestration worker-read --dispatch <dispatch_id> --source transcript --json`: a final agent turn that sent no `worker_done` is a stall and step 3 fails; a growing transcript means keep waiting. A `question` message is answered only with facts about the environment; a request for a decision is not answered, and step 3 fails. Save the `worker_done` message to `./artifacts/lc<N>-step3.json`, then acknowledge its delivery with `check --ack <delivery_id>`. Pass (AC-0.4 form): exactly one `worker_done`; its `--report-path` is the task's report file; its `--outcome` equals the AC-0.4 rule applied by the executor to that file (failed when the file is missing or empty, or its status is failed or blocked; otherwise succeeded).
```

### .dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/TASK-WF-writeTheP0LivePl-20261103-215902.md:38-39
```text
  - Step 7: `orca orchestration worker-release --dispatch <dispatch_id> --json`, then `orca orchestration worker-list --terminal-state reclaimable --json`, both saved to `./artifacts/lc<N>-step7.txt`. Pass: the list returns no rows.
  - Remove: `orca worktree rm --worktree path:<path> --force --json` (spec line 282: the worktree is removed after step 7), saved to `./artifacts/lc<N>-remove.json`, plus `git branch --list p0-live-<name>*` to record whether its branch remains. The branch is not deleted.
```

### .dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/TASK-WF-writeTheP0LivePl-20261103-215902.md:46-52
```text
Write `./artifacts/preflight.md` from these checks, run in the feature worktree, each with its command and output: `echo "$ORCA_TERMINAL_HANDLE"` is non-empty; `git rev-parse HEAD` prints `8db29f1165508187b7a14a48f2f66793e269d596` and `git branch --show-current` prints `ironbelly/OrcaCLICommandRefactor-Specs`; `cmp ~/.claude/WORKER-CONTRACT.md src/superclaude/core/WORKER-CONTRACT.md` exits 0 (the owner-approved install from that commit reached `~/.claude`); the AC-C6 command from spec line 278 prints only `"nestedWorkerMaxDepth":1`; `orca status --json` shows the runtime `ready`; `orca repo list --json` lists repo id `de550e99-fa3c-42e2-abfe-1d092771c759`. Then confirm the troubleshoot symptom is still current: `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/cli/eval/test_ban_import_rule.py -q -rf -p no:cacheprovider` saved to `./artifacts/symptom-check.txt`. It must report the three tests listed as accepted failures in `.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t1-accepted-failures.md:24-26` as failed. Finally run `orca orchestration run-create --objective "P0 live checks AC-0.4, AC-0.5, AC-0.6 for the Orca worker contract" --json` and save the receipt to `./artifacts/live-run.json`.

Acceptance criteria:
- `./artifacts/preflight.md` shows every check above with its output, and each one passes.
- `./artifacts/symptom-check.txt` shows `test_clean_tree_passes_ruff_check`, `test_synthetic_import_anthropic_is_flagged_by_ruff` and `test_ban_message_references_fr_g1` failing.
- `./artifacts/live-run.json` holds a run id whose `coordinator_handle` equals the session's `ORCA_TERMINAL_HANDLE`.
- `git status --porcelain` shows no change outside this package and the four untracked folders that existed before the plan.
```

### .dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/TASK-WF-writeTheP0LivePl-20261103-215902.md:63-70
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

### .dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/TASK-WF-writeTheP0LivePl-20261103-215902.md:73-80
```text
Before Step 5, answer AC-0.6 (spec line 303) from this worker's transcript: write `./artifacts/ac-0.6.md` stating yes or no to "tool calls appear by name" with a quoted excerpt showing at least one named call such as `Bash` or `Skill`. Write `./artifacts/ac-0.5.md` (spec line 302) from Step 1: the exit code, `state`, the elapsed seconds and the receipt's launch fields. AC-0.5 passes when worker-start exits 0 with `state: ready` in under 45 s.

Acceptance criteria:
- `./artifacts/lc1-result.md` exists and records every procedure step with its evidence file and the check's overall verdict.
- `./artifacts/lc1-report/REPORT.md` is a copy of the worker's report file, or `lc1-result.md` states that the file was missing.
- `./artifacts/ac-0.5.md` states the measured seconds and PASS or FAIL against the 45 s limit.
- `./artifacts/ac-0.6.md` states yes or no with a quoted transcript excerpt, and `./artifacts/lc1-step5.md` names the source (transcript or terminal) that answer selects.
- `orca worktree list --json` no longer lists the `p0-live-troubleshoot` worktree, and the feature worktree's HEAD is unchanged.
```

### .dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/TASK-WF-writeTheP0LivePl-20261103-215902.md:98-98
```text
Command: /sc:workflow "Add one sentence to the Installation section of README.md stating that superclaude install --force overwrites files that already exist in ~/.claude" --handoff none
```

### .dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/TASK-WF-writeTheP0LivePl-20261103-215902.md:112-114
```text
Depends on: Task 2

Follow the live-check procedure in Constraints with `<N>` = 3, `<name>` = adversarial, command file `adversarial.md`. The two inputs are committed files at commit `8db29f11`: `.dev/orca-command-refactor/decisions/D1/option-a.md` and `.dev/orca-command-refactor/decisions/D1/option-b.md` (two rival options for one decision, 23 and 25 lines). `--compare` takes comma-separated paths (`src/superclaude/commands/adversarial.md:39`). Report directory `.dev/p0-live/adversarial/`; report file `.dev/p0-live/adversarial/adversarial/merge-log.md`, status from the `Status:` line of its `## Metadata` section, not the per-change `**Status**` lines (spec line 301; `src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:294-299`). The brief:
```

### .dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/TASK-WF-writeTheP0LivePl-20261103-215902.md:139-145
```text
Write `./artifacts/p0-phase-report.md`. Static part: cite `.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/p0-static-report.md` by path and list each static check ID it covers (AC-0.1, AC-0.2, AC-0.3, AC-0.7, AC-0.9, AC-C1 to AC-C6) with the verdict it records, without copying its evidence. Carry forward its AC-0.7 finding that `task-create`, `worktree create --agent` and `agent launch` are covered only by WC-13 and section 7.2 step 5. Live part: one row each for AC-0.4 (each of the three checks, from `./artifacts/lc1-result.md`, `lc2-result.md` and `lc3-result.md`), AC-0.5 (`./artifacts/ac-0.5.md`) and AC-0.6 (`./artifacts/ac-0.6.md`), each with its verdict and evidence path. Name at least one checked run that lasted longer than the heartbeat cadence, or state that none did, so the heartbeat part of step 5 is not passed vacuously in every run (spec line 291). List each disposable worktree's branch that remains after removal, for the coordinator. State the P0 verdict: PASS only when every static check and every live check passes; otherwise FAIL, naming each failed check. An AC-0.4 failure is recorded as reopening spec section 1. Then run `git add .dev/tasks` followed by `git restore --staged .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950`, and save `git diff --cached --name-only` to `./artifacts/staged.txt`.

Acceptance criteria:
- `./artifacts/p0-phase-report.md` has the static part citing the static report, the live part with rows for AC-0.4 (three checks), AC-0.5 and AC-0.6, the heartbeat-length statement, the remaining branches, and one P0 verdict line consistent with every row.
- Every live verdict in the report matches its `lc<N>-result.md`, `ac-0.5.md` or `ac-0.6.md` file.
- `./artifacts/staged.txt` lists only `.dev/tasks/` paths, none under `TASK-WF-orcaWorkerContra-20261102-231950` and none under `.claude/`.
- `git rev-parse HEAD` still prints `8db29f1165508187b7a14a48f2f66793e269d596`.
```

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:238-238
```text
Each phase is one written plan executed under the repo's level-3 route (`/sc:workflow`, then `/sc:implement` when execution is requested), because each touches more than one source file (hard limit at `src/superclaude/core/CLAUDE.md:66` and `src/superclaude/core/HOW-WE-WORK.md:22`). Because the 7.2 live checks need the owner's commit and install approvals, and `/sc:implement` may not prompt the user outside its halt paths (`sk/sc-implement-protocol/refs/qa.md:288`), each phase's plan comes in two parts. The static plan holds the edits and the checks that need no live Orca run. The live plan holds the 7.2 live checks and the phase report. Between them, the coordinator session asks the owner, commits and installs as 7.2 states, outside any plan run. The live plan is written after the static plan's checks pass, and the phase passes only when both plans' checks pass.
```

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:278-278
```text
grep -ho '"nestedWorkerMaxDepth":[0-9]*' "${ORCA_RUNTIME_SOURCE_PROFILE_PATH:-$HOME/.config/orca}"/profiles/*/orca-data.json
```

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:283-285
```text
1. `ORCA orchestration task-create --spec "<brief per section 2.3>" --json`. Then either `ORCA orchestration worker-start --task <task_id> --worktree new-top-level --base-branch <branch> --setup run --agent claude --json`, when the setup is confirmed to run `make sync-dev`; or create the worktree first with `ORCA worktree create` from `<branch>`, run `make sync-dev` inside it, and start the worker with `--worktree path:<worktree>`. For a command that accepts `--unattended` at this phase, confirm before dispatch that every existing copy of its file (`<worktree>/.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md`) has its `## Unattended mode` section. **Pass:** exit 0 and `state: ready` (`CAPS:46`).
2. While it runs, `ORCA orchestration worker-show --dispatch <dispatch_id> --json` at least once per 5 minutes. **Pass:** `observation.agentWait` is never non-null (a non-null value means the worker is parked on a prompt only a person can answer, `CAPS:129`). Sampling can only find a wait, not prove there was none; step 3 adds the positive proof.
3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. If the wait ends without one, read `ORCA orchestration worker-read --dispatch <dispatch_id> --source transcript --json`: a final agent turn that sent no `worker_done` is Orca's positive proof of a stall (`CAPS:126`), and the check fails; a transcript still growing means keep waiting. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `worker_status` under WC-5; its report path is the WC-4 contract path. At P0, before the contract exists, AC-0.4 replaces the last two conditions.
```

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:291-293
```text
5. `ORCA orchestration worker-read --dispatch <dispatch_id> --source transcript --json`. **Pass:** no `AskUserQuestion` call (WC-2); the command was run in the top-level session, not inside an Agent-tool call (WC-7); a `check` call appears after the command finished and before `worker_done` (WC-12); heartbeat `send` calls are at most the preamble's cadence apart, except while the session is inside an Agent-tool call or blocked in `ask` or `check --wait` (WC-10); the worker session made no `worker-start`, `dispatch` or `task-create` call and no `orca-cli` `worktree create --agent` or `agent launch` call (WC-13). A run shorter than the cadence passes the heartbeat part vacuously, so each phase report names at least one checked run that lasted longer than the cadence. This step relies on the transcript naming tool calls, which AC-0.6 confirms in P0; if AC-0.6 finds it does not, this step uses `--source terminal` output instead and the phase report records the gap.
6. `git status --porcelain` in the disposable worktree. **Pass:** every path it prints that the phase did not edit is under the brief's output or report directory or is a documented artifact of the command. Ignored paths (tool caches, `.venv/`) are not checked.
7. `ORCA orchestration worker-release` for the settled worker, then `ORCA orchestration worker-list --run <run_id> --terminal-state reclaimable --json` returns no rows (`CAPS:107-113`).
```

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:301-303
```text
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>" --output-dir <dir>` (no `--fix`, no `--depth deep`), `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-7 pass. Steps 3 and 4 are adapted because the contract arrives in P1 (`decisions/APPROVED.md` S1).
| P0 | AC-0.5 | WC-1: `worker-start` with the user's normal launch setup (the same shell wrapper, hooks and startup command a person's sessions use), timed | exit 0, `state: ready`, and the start returns in under 45 s.
| P0 | AC-0.6 | Read one AC-0.4 transcript with `worker-read --source transcript --json` and record whether tool calls appear by name (for example `Bash`, `Agent`, `AskUserQuestion`) | the phase report states yes or no with a quoted excerpt; 7.2 step 5 follows that answer |
```

### src/superclaude/core/WORKER-CONTRACT.md:42-42
```text
  - Outside that grant a worker never runs `git add` (including `git add .dev/tasks`), never commits, never moves HEAD and never touches a remote: the coordinator stages `.dev/tasks` (section 4). The skills that stage it themselves (`~/.claude/skills/sc-implement-protocol/refs/managed-workspace.md`, `~/.claude/skills/sc-implement-protocol/refs/ledger.md`, `~/.claude/skills/sc-workflow-protocol/SKILL.md`, `~/.claude/skills/task/SKILL.md`) defer that staging under `--unattended`, and the MDTM CLI-mode `git add -A` (`~/.claude/skills/task-builder/SKILL.md`) is refused.
```

### src/superclaude/core/WORKER-CONTRACT.md:73-73
```text
- A crashed or stalled attempt is settled by the coordinator: after Orca's positive stall proof it stops the worker and sets the old Task `failed --result cancelled` before creating the new Task.
```

### src/superclaude/core/WORKER-CONTRACT.md:169-176
~~~~text
```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: <directory unique to this Task>
Worktree: <shared feature worktree | child worktree created by Orca with worker-start --worktree new-child --base-branch <feature branch>>
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
P0 only: Report file: <the command's report file under AC-0.4>. Outcome rule: --outcome failed when the file is missing or empty, or its status is failed or blocked; otherwise --outcome succeeded. This rule replaces the WC-5 mapping for this Task.
~~~~

### src/superclaude/core/WORKER-CONTRACT.md:185-185
```text
- The `P0 only:` line is used only before P1, when no command writes a worker contract. At P0 the report files are: troubleshoot, `<dir>/REPORT.md` with the status in its `**Status**:` line; workflow, the `return-contract.yaml` in the one new `TASK-WF-*` package directory the run creates under `.dev/tasks/to-do/`, with the status in its top-level `status`; adversarial, `<dir>/adversarial/merge-log.md` with the status in the `Status:` line of its `## Metadata` section. From P1 the line is dropped and WC-5 applies.
```

### src/superclaude/core/WORKER-CONTRACT.md:191-202
```text
| `/sc:adversarial` | `--output <dir>`; never `--interactive` |
| `/sc:brainstorm` | `--output <dir>`; never `--interactive` |
| `/sc:cleanup-audit` | `--pass <N>` (single pass); `--report-dir <dir>` (from P1) |
| `/sc:graph` | `status` (the default) with `--output-dir <dir>`; never `init`, which runs only when the user's own message starts with `/sc:graph init` |
| `/sc:impact` | `--output-dir <dir>` |
| `/sc:index-repo` | none |
| `/sc:init-lite` | `--output <file>` |
| `/sc:reflect` | no `--remediate`; `--no-promote` when the coordinator owns folder moves |
| `/sc:release-split` | spec-shaped input; default `--r1-scope`; never `--interactive` |
| `/sc:tdd` | a precise component prompt, not a bare topic; `--output <file>` |
| `/sc:troubleshoot` | no `--fix` (and no `--depth deep` until P2) |
| `/sc:workflow` | `--handoff none`; `--report-dir <dir>` (from P1); its `--output` is retired |
```

### ~/.claude/skills/sc-implement-protocol/SKILL.md:34-34
```text
| `E-RESUME-NEEDED` | Something outside the step failed (reviewer, ref write, incomplete revert, adviser agent missing; reasons in `refs/retry.md`); re-run the same command | No T{i+1} | Nothing written |
```

### ~/.claude/skills/sc-implement-protocol/SKILL.md:79-79
```text
Ignore MDTM fields (`depends-on`, `agent:`, `wave:`, `compliance:`) except `independent`. Phase-N tasklists are accepted as markdown. MDTM-shaped files still use **this** protocol. Do not auto-handoff.
```

### ~/.claude/skills/sc-implement-protocol/refs/qa.md:52-52
```text
| `quoted-constraint-breach` | B4 constraint breach | The diff violates a parent `## Constraints` / `## Out of scope` / `## Non-goals` / `## Non-negotiable` item or an explicit task instruction ("## Compare the diff to" above), including editing text the plan reserves for another task, and the reviewer can quote that text. |
```

### ~/.claude/skills/sc-implement-protocol/refs/qa.md:87-87
```text
- a claim the reviewer could not verify has no evidence row (`ac-outcome-missing=yes`, anchored on the AC words).
```

### ~/.claude/skills/sc-implement-protocol/refs/qa.md:310-310
```text
Same isolation as above: `Do not trust the implementer's report.` One fresh subagent per archive attempt (never inline, even N=1; never reused from an earlier attempt). Input: the current full plan, the full ledger, and the current contents of every delivery file the helper's `--print-state` lists, plus the plan's `## Constraints`. Output: `pass` or `issues` with `path:line` evidence per task AC, taken from the current files and the package's `./artifacts/` logs, not copied from the ledger; reading those logs is the one exception to the Isolation rule above. A per-task `evidence=` line number is a pointer recorded when that task was reviewed, and a later task can move it, so a moved line number alone is never `issues`. `issues` when an AC is unmet at the end state, no evidence for it can be found in the current files or logs, a later change contradicts it, a plan `## Constraints` item is violated, or a log cited on a task's latest `complete` line shows a failure at its outcome line.
```

### ~/.claude/skills/sc-implement-protocol/refs/managed-workspace.md:36-36
```text
- `.dev/tasks/` is always staged (`git add .dev/tasks`): the package, its `progress.md` ledger and `artifacts/` included. Never gitignore it, never leave it untracked, and never write "do not stage" about it in a ledger note or report. Staging is not committing. After the helper moves a package to `done/`, the new path needs `git add .dev/tasks` again.
```

### ~/.claude/skills/sc-implement-protocol/refs/ledger.md:3-3
```text
One markdown file per run. Append-only. UTF-8, `\n` endings, no wrapping of record lines. Do not `git add` a legacy ledger under `.dev/implement/`. A managed package's ledger (`<pkg>/progress.md`) sits under `.dev/tasks/`, which is always staged (`git add .dev/tasks`).
```

### src/superclaude/skills/sc-workflow-protocol/SKILL.md:28-28
```text
`.dev/tasks/` is always staged (`git add .dev/tasks`): the package and its `artifacts/` included. Never gitignore it, never leave it untracked, and never write "never stage" about it in a generated plan (Constraints included). Staging is not committing.
```

### .dev/orca-command-refactor/inventory/orca-capabilities.md:113-115
```text
- **Coordinator turn cannot end with unreleased workers.** `[G]` lines 177-179: "Enumerate the terminals still owing a decision with `worker-list --run <run_id> --terminal-state reclaimable --json`, and do not end the coordinator turn until it returns none." Terminal states: `[H:worker-list]` line 3: "--terminal-state <active|reclaimable|retained|release_pending|release_unknown|released>". `[H:worker-list]` line 19: "Terminal state is process accounting and is reported separately from Task status; a completed Task can still own a live terminal."
...
- **Worktrees are never deleted by these verbs.** `[G:recovery]` lines 134-135: "`worker-stop` closes only the exact proven supervised agent terminal. It never deletes the worktree, setup terminal, configured tabs, or unrelated processes." No orchestration verb in `[H:orch]` lines 6-35 removes a worktree. Removal is an `orca-cli` operation: `[CLI]` line 100: "ORCA worktree rm --worktree id:<repoId>::<worktreePath> --force --json".
```

### .dev/orca-command-refactor/inventory/orca-capabilities.md:129-129
```text
- **Waiting on a human is healthy.** `[H:worker-show]` line 16: "observation.agentWait names a worker parked on a prompt only a human can answer ... Null means Orca looked and found no wait. An absent field means it never looked ... A waiting worker is healthy, not failed."
```

### .dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:41-41
```text
1. **Location: RESOLVED by the user (2026-11-02): defer to Orca's default paths.** Every worktree, parent or child, is created by Orca (`worker-start --worktree new-child`/`new-top-level` or `orca worktree create`) at Orca's default location, observed as `/home/coder/workspaces/worktrees/<repo>/<name>` for this spec's own Orca-created worktree (`orca-ide worktree show`: `creatorProvenance.kind = paired-device`, `createdWithAgent = claude`).
```

### .dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:50-50
```text
- `orca-ide skills get orca-cli`: `worktree create --parent-worktree <selector>`, `worktree set --parent-worktree` / `--no-parent`, lineage rules, and `--no-parent` does not choose the git base.
```

### .dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t1-accepted-failures.md:24-26
```text
| `tests/cli/eval/test_ban_import_rule.py::test_clean_tree_passes_ruff_check` | wider | accepted |
| `tests/cli/eval/test_ban_import_rule.py::test_synthetic_import_anthropic_is_flagged_by_ruff` | wider | accepted |
| `tests/cli/eval/test_ban_import_rule.py::test_ban_message_references_fr_g1` | wider | accepted |
```

### .dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-c6-depth-setting.txt:4-5
```text
$ grep -ho '"nestedWorkerMaxDepth":[0-9]*' "${ORCA_RUNTIME_SOURCE_PROFILE_PATH:-$HOME/.config/orca}"/profiles/*/orca-data.json
"nestedWorkerMaxDepth":1
```

### src/superclaude/commands/troubleshoot.md:56-56
```text
| `--output-dir` | `.dev/troubleshoot/<slug>-<timestamp>/` | Where REPORT.md, hypothesis cards, fix proposals, adversarial artifacts, and audit log are written. |
```

### src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md:14-14
```text
**Status**: <success|partial|blocked|failed> <!-- Same final merged status as audit footer and TFEP: failed > blocked > partial > success. -->
```

### src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:5-7
~~~~text
```yaml
contract_version: "1.1"
status: success | partial | failed
~~~~

### src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:294-299
```text
## Metadata
- Base: Variant <X> (<agent-spec>)
- Executor: merge-executor agent
- Changes applied: <N> of <total planned>
- Status: success/partial/failed
- Timestamp: <ISO-8601>
```

### src/superclaude/skills/sc-adversarial-protocol/SKILL.md:2072-2072
```text
    output_path: "<output-dir>/adversarial/merge-log.md"
```

### src/superclaude/commands/adversarial.md:39-39
```text
- `--compare`: Comma-separated file paths (2-10 existing files)
```

### README.md:53-53
```text
## Installation
```

### git status --porcelain (feature worktree, run 2026-11-03 during this review)
```text
?? .dev/brainstorms/20261102-1446-review-loop-remediation/
?? .dev/brainstorms/20261102-1621-jev-decision-layer/
?? .dev/reflect/pre-TASK-WF-writeTheP0LivePl-20261103-215902-20261103220351/
?? .dev/review-loop-convergence/
?? .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/
?? .dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/
```

### .dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/source.md:1-1
```markdown
Write the P0 LIVE plan of the Orca worker-contract spec .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (two-part rule at spec line 238; the P0 static plan already passed and is archived at .dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/, committed locally as 8db29f11 on branch ironbelly/OrcaCLICommandRefactor-Specs, and the owner-approved uv run superclaude install --force already ran from that commit). Scope is exactly the P0 live checks and the phase report: AC-0.4 (section 7.3 row: three section 7.2 live checks, one each for /sc:troubleshoot "<real symptom>" --output-dir <dir> with no --fix and no --depth deep, /sc:workflow "<small change>" --handoff none, and /sc:adversarial --compare <two files> --depth quick --output <dir>, each run directly by the worker with the AC-0.4 report-file and outcome rule in its brief), AC-0.5 (timed worker-start under 45 s with the normal launch setup), AC-0.6 (whether worker-read --source transcript names tool calls, with a quoted excerpt), all seven section 7.2 steps per live check (fresh disposable worktree created by Orca at its default path from branch ironbelly/OrcaCLICommandRefactor-Specs at 8db29f11, never under .dev/worktrees/; make sync-dev inside it before dispatch unless --setup run is confirmed to do it; orca worktree rm after step 7), and a P0 phase report in the package artifacts that combines the static report (.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/p0-static-report.md, cited not copied) with the live results and states the phase verdict. The plan must fix concrete inputs in advance, not leave them to the executor: for troubleshoot use a real current symptom from the static run's accepted pre-existing failures (.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t1-accepted-failures.md), for workflow a small harmless change prompt, and for adversarial two existing committed files under .dev/orca-command-refactor/. Constraints: no edit to any source, command, skill, agent or test file; no git commit, push, PR, gh write or superclaude install; no interaction with the SuperClaude-Org upstream; UV only; never stage .claude/; leave the superseded package .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/ unstaged and untouched; stage .dev/tasks at the end. Execution constraint the plan must state: because AC-C6 shows nestedWorkerMaxDepth 1, the live plan is executed by /sc:implement in a top-level session the person opens (depth 0, the coordinator), never inside an Orca worker, since its own live checks start Orca workers. A failed live check is recorded in the phase report, not retried silently; per spec AC-0.4 a failure reopens section 1.
```

## Coverage slice

```yaml
# sc:reflect --mode pre, Wave 1B coverage matrix (UC-1)
# spec:     .dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/source.md (one physical line)
# tasklist: .dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/TASK-WF-writeTheP0LivePl-20261103-215902.md
#
# Pass 1: ID_REGEX \b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b over source.md (no fenced code) -> 0 hits.
#   source.md labels its requirements AC-0.4 / AC-0.5 / AC-0.6 / AC-C6, which the regex does not capture;
#   no range tokens, so no expansion.
# Pass 2: requirement-shaped content (scope items, input rules, constraint bullets, execution constraint),
#   each row a verbatim quote of source.md:1 (checked to be byte-present before matching).
# Matching: containment rule only (no parsed rows). Case-fold, fixed stopword set (articles, conjunctions,
#   prepositions, auxiliaries, pronouns), match when >= 0.6 of the quote's content words appear in ONE
#   tasklist item; best ratio wins, first item in tasklist order breaks ties.
#   Tasklist items in order: C1..C10 = the ten top-level bullets of "## Constraints" (plan lines 19, 20, 21,
#   22, 23, 24, 25, 26, 27, 28-40; C10 = the live-check procedure with its sub-bullets), then T1..T5 =
#   "## Task 1".."## Task 5" bodies (plan lines 44-52, 56-80, 84-106, 110-131, 135-145).
#   Ratios were computed by a throwaway script applying the rule as written; the ratio is in match_basis.

parsed_count: 0
inferred_count: 24

rows:
  - id: INF-001
    source: inferred
    quote: '/sc:troubleshoot "<real symptom>" --output-dir <dir> with no --fix and no --depth deep'
    citation: source.md:1
    matched_task: null
    match_basis: 'containment 0.50 < 0.6 -> none. Covered in substance by the T2 brief (plan line 70: --output-dir, no --fix, no --depth).'
  - id: INF-002
    source: inferred
    quote: '/sc:workflow "<small change>" --handoff none'
    citation: source.md:1
    matched_task: T3
    match_basis: 'containment 0.60 -> T3'
  - id: INF-003
    source: inferred
    quote: '/sc:adversarial --compare <two files> --depth quick --output <dir>'
    citation: source.md:1
    matched_task: T4
    match_basis: 'containment 0.875 -> T4'
  - id: INF-004
    source: inferred
    quote: 'each run directly by the worker with the AC-0.4 report-file and outcome rule in its brief'
    citation: source.md:1
    matched_task: C10
    match_basis: 'containment 0.75 -> Constraints bullet 10 (live-check procedure)'
  - id: INF-005
    source: inferred
    quote: 'AC-0.5 (timed worker-start under 45 s with the normal launch setup)'
    citation: source.md:1
    matched_task: C9
    match_basis: 'containment 0.625 -> Constraints bullet 9 (first in order); also realized in T2 (plan line 73)'
  - id: INF-006
    source: inferred
    quote: 'AC-0.6 (whether worker-read --source transcript names tool calls, with a quoted excerpt)'
    citation: source.md:1
    matched_task: C10
    match_basis: 'containment 0.90 -> Constraints bullet 10; also realized in T2 (plan line 73)'
  - id: INF-007
    source: inferred
    quote: 'all seven section 7.2 steps per live check'
    citation: source.md:1
    matched_task: C2
    match_basis: 'containment 0.714 -> Constraints bullet 2 (scope)'
  - id: INF-008
    source: inferred
    quote: 'fresh disposable worktree created by Orca at its default path from branch ironbelly/OrcaCLICommandRefactor-Specs at 8db29f11, never under .dev/worktrees/'
    citation: source.md:1
    matched_task: null
    match_basis: 'containment 0.583 < 0.6 -> none. Covered in substance by C9 + C10 (plan lines 27, 29).'
  - id: INF-009
    source: inferred
    quote: 'make sync-dev inside it before dispatch unless --setup run is confirmed to do it'
    citation: source.md:1
    matched_task: C10
    match_basis: 'containment 0.889 -> Constraints bullet 10'
  - id: INF-010
    source: inferred
    quote: 'orca worktree rm after step 7'
    citation: source.md:1
    matched_task: C10
    match_basis: 'containment 1.00 -> Constraints bullet 10 (Remove sub-bullet, plan line 39)'
  - id: INF-011
    source: inferred
    quote: 'a P0 phase report in the package artifacts that combines the static report (.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/p0-static-report.md, cited not copied) with the live results and states the phase verdict'
    citation: source.md:1
    matched_task: null
    match_basis: 'containment 0.571 < 0.6 -> none. Covered in substance by T5 (plan line 139).'
  - id: INF-012
    source: inferred
    quote: 'for troubleshoot use a real current symptom from the static run''s accepted pre-existing failures (.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t1-accepted-failures.md)'
    citation: source.md:1
    matched_task: null
    match_basis: 'containment 0.583 < 0.6 -> none. Covered in substance by the T1 symptom check (plan line 46) and the T2 brief (plan line 70).'
  - id: INF-013
    source: inferred
    quote: 'for workflow a small harmless change prompt'
    citation: source.md:1
    matched_task: null
    match_basis: 'containment 0.20 < 0.6 -> none. Covered in substance by the T3 Command: line (plan line 98).'
  - id: INF-014
    source: inferred
    quote: 'for adversarial two existing committed files under .dev/orca-command-refactor/'
    citation: source.md:1
    matched_task: T4
    match_basis: 'containment 0.667 -> T4'
  - id: INF-015
    source: inferred
    quote: 'no edit to any source, command, skill, agent or test file'
    citation: source.md:1
    matched_task: C3
    match_basis: 'containment 1.00 -> Constraints bullet 3'
  - id: INF-016
    source: inferred
    quote: 'no git commit, push, PR, gh write or superclaude install'
    citation: source.md:1
    matched_task: C4
    match_basis: 'containment 1.00 -> Constraints bullet 4'
  - id: INF-017
    source: inferred
    quote: 'no interaction with the SuperClaude-Org upstream'
    citation: source.md:1
    matched_task: C4
    match_basis: 'containment 1.00 -> Constraints bullet 4'
  - id: INF-018
    source: inferred
    quote: 'UV only'
    citation: source.md:1
    matched_task: T1
    match_basis: 'containment 1.00 -> T1 (mechanical: "uv" and "only" both occur in T1; C5 states the rule but scores 0.5)'
  - id: INF-019
    source: inferred
    quote: 'never stage .claude/'
    citation: source.md:1
    matched_task: C6
    match_basis: 'containment 1.00 -> Constraints bullet 6'
  - id: INF-020
    source: inferred
    quote: 'leave the superseded package .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/ unstaged and untouched'
    citation: source.md:1
    matched_task: C6
    match_basis: 'containment 0.667 -> Constraints bullet 6. Matched but at risk: t1-card F-001 (the executor re-stages .dev/tasks after the archive move).'
  - id: INF-021
    source: inferred
    quote: 'stage .dev/tasks at the end'
    citation: source.md:1
    matched_task: T5
    match_basis: 'containment 0.667 -> T5'
  - id: INF-022
    source: inferred
    quote: 'the live plan is executed by /sc:implement in a top-level session the person opens (depth 0, the coordinator), never inside an Orca worker, since its own live checks start Orca workers'
    citation: source.md:1
    matched_task: C1
    match_basis: 'containment 0.75 -> Constraints bullet 1'
  - id: INF-023
    source: inferred
    quote: 'A failed live check is recorded in the phase report, not retried silently; per spec AC-0.4 a failure reopens section 1.'
    citation: source.md:1
    matched_task: C7
    match_basis: 'containment 0.867 -> Constraints bullet 7. Matched but at risk: t1-card F-002 (the managed FINAL treats a cited log that shows a failure as issues).'
  - id: INF-024
    source: inferred
    quote: 'The plan must fix concrete inputs in advance, not leave them to the executor'
    citation: source.md:1
    matched_task: null
    match_basis: 'containment 0.286 < 0.6 -> none. Covered in substance: T2-T4 fix every Command: line word for word (plan lines 70, 98, 124).'

coverage_pct: null              # parsed-only; parsed_count is 0
coverage_pct_union: 0.7500      # 18 of 24 rows matched by the containment rule
unmapped_requirements: []       # parsed-only
unmapped_requirements_union: [INF-001, INF-008, INF-011, INF-012, INF-013, INF-024]
coverage_undefined: false       # Pass 2 emitted valid quote-pinned rows
coverage_degraded: parsed-sparse   # inferred_count (24) > parsed_count (0)
S_scope: 5                      # Tasks 1-5
S_domains: 1                    # every path the plan writes is under .dev/ (docs); tests are only run, and Orca state is not a file path
S_dev_density: 0.2500           # 6 unmapped / 24 union; missing_implementations_count 0 (no abstract symbols in scope)
note: >-
  All six mechanically unmapped rows are covered in substance (match_basis names the plan line); they miss the
  0.6 threshold because the source uses placeholder and path wording that the plan restates differently.
  S_dev_density > 0.20 and coverage_degraded parsed-sparse both route to Tier 2 under the rubric.
```
