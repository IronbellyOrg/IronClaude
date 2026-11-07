# Reviewer 1 brief (persona: analyzer, model class: sonnet)

spec_path: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/source.md
tasklist_path: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/TASK-WF-p1LivePlanBrief-20261105-164506.md
persona_lens: analyzer
mode: pre (UC-1). Audit the TASKLIST against the SPEC. There is no diff; "deviation" means a place where the tasklist departs from, omits, contradicts or misstates the spec, or where a statement in the tasklist is false against the grounding hunks. Classify with the 4 categories; use Drift for an unjustified omission or addition, Regression for a statement that contradicts a load-bearing fact or rule in the grounding hunks (for example a wrong command flag, a step the spec forbids), Necessary deviation for a justified departure, Authorized expansion for an addition the spec permits. Read-only: change nothing, run nothing; return the findings table and the adherence summary in your reply.
Reflect output_path (orchestrator writes it): /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/reflect/pre-TASK-WF-p1LivePlanBrief-20261105-164506-20261105172548/reviewer-cards/reviewer-1-card.yaml

## T1 card excerpt

## Root-cause / deviation (analyzer slice)

- Pass 1 found 0 parsed requirement ids (the brief uses AC-x.y, lcNN and D-P1-n labels). Pass 2 enumerated 39 quote-pinned rows (`artifacts/coverage-matrix.yaml`).
- Candidate deviation (a), Drift: plan line 52 and Task 24 (line 552) replace the brief's owner grant file (`source.md:79`) with a Constraints bullet. The brief still names the file; the plan supersedes it on purpose, because the file is in no spec or decision. Candidate label: Necessary deviation, documented at plan line 19 and line 52.
- Candidate deviation (b), Authorized expansion: the plan adds a Gate line (line 36) and a Section check (line 38) the brief states only in prose (`source.md:30`).
- Candidate deviation (c), Necessary deviation: Task 24 (line 552) creates the child worktree with `orca worktree create --parent-worktree active` and syncs it before dispatch, instead of the brief's `worker-start --worktree new-child --setup run` (`source.md:79`), because spec 7.2 step 1 requires the sync before dispatch (`orca-worker-contract-spec.md:283`) and WORKER-CONTRACT.md slot rules allow `--setup run` only when the user names it (`WORKER-CONTRACT.md:174`).
- Verified-open risk: whether `orca worktree create --parent-worktree active` accepts `active` from this terminal is UNVERIFIED; Task 1 saves the help text (plan line 58) and a usage error is recorded as FAIL (plan line 29).

## Grounding hunks

codegraph run state: index_state=not-checked checked_at=n/a worktree_root=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1 projectPath=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1

## G0 Codegraph run state
index_state: not-checked (UC-1 pre-mode over a plan). Reviewers use Read and Grep only.

## G1 Spec 7.2 live worker check (spec lines 281-304)
```
### 7.2 Live worker check (used by P0-P4)
For each command under test, the coordinator runs the steps below with one worker in a fresh disposable worktree that holds the phase's edits, so step 6 can attribute every change to the worker under test (WC-11 allows sharing a worktree in normal use; the check does not). Orca creates worktrees from a git base, and the phase's edits are uncommitted until the user asks (`CLAUDE.md:37`), so before the check the phase's edits are committed to the feature branch or a scratch branch with the user's authorization (a decision point each phase). The disposable worktree is created by Orca at Orca's default path from that branch, never under `.dev/worktrees/`. `make sync-dev` is run inside it before dispatch unless Orca's `--setup run` is confirmed to do it (UNVERIFIED item 27). Before the phase's live checks, the coordinator asks the owner for approval, then installs that phase into `~/.claude` by running `superclaude install --force` from the phase branch, as `uv run superclaude install --force` inside a checkout of that branch, because the installer copies from the running package's own location (`src/superclaude/cli/install_core.py:117-122`), so a separately installed `superclaude` would install its own files, not the branch's. One approval per phase, asked before every phase's install. If a phase is abandoned, the coordinator reinstalls from master (`superclaude install --force` from master). Both installs pass `--force` because without it the installer skips every file that already exists (`src/superclaude/cli/install_commands.py:55-57`), so the phase would never reach `~/.claude`; `update.sh:8` runs the same `superclaude install --force`. After step 7 the worktree is removed with `orca worktree rm`, because orchestration verbs never delete worktrees (`CAPS:115`).
1. `ORCA orchestration task-create --spec "<brief per section 2.3>" --json`. Then either `ORCA orchestration worker-start --task <task_id> --worktree new-top-level --base-branch <branch> --setup run --agent claude --json`, when the setup is confirmed to run `make sync-dev`; or create the worktree first with `ORCA worktree create` from `<branch>`, run `make sync-dev` inside it, and start the worker with `--worktree path:<worktree>`. For a command that accepts `--unattended` at this phase, confirm before dispatch that every existing copy of its file (`<worktree>/.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md`) has its `## Unattended mode` section. **Pass:** exit 0 and `state: ready` (`CAPS:46`).
2. While it runs, `ORCA orchestration worker-show --dispatch <dispatch_id> --json` at least once per 5 minutes. **Pass:** `observation.agentWait` is never non-null (a non-null value means the worker is parked on a prompt only a person can answer, `CAPS:129`). Sampling can only find a wait, not prove there was none; step 3 adds the positive proof.
3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. If the wait ends without one, read `ORCA orchestration worker-read --dispatch <dispatch_id> --source transcript --json`: a final agent turn that sent no `worker_done` is Orca's positive proof of a stall (`CAPS:126`), and the check fails; a transcript still growing means keep waiting. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `worker_status` under WC-5; its report path is the WC-4 contract path. At P0, before the contract exists, AC-0.4 replaces the last two conditions.
4. Check the contract (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both commands exit 0. At P0, AC-0.4 replaces this step.
   ```sh
   test -s <contract>
   uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['worker_contract_version'] == '1'; assert d['worker_status'] in {'succeeded','partial','failed','blocked'}; assert d['command']; assert d['worker_status'] != 'blocked' or d.get('blocked_question')" <contract>
   ```
5. Check the worker's behaviour over the whole run. The primary source is the worker's own session file; `worker-read` is the cross-check for the end of the run (P0 found that `worker-read` returns only the last 40 to 50 messages of a long run and its cursor never ends, so it cannot show the start of a run; UNVERIFIED items 28-33).
   - **Source file.** For a Claude worker started on this machine the file is `~/.claude/projects/<dir>/<session id>.jsonl`, where `<dir>` is the worker's worktree path with each `/` replaced by `-`; each subagent's own file is under `~/.claude/projects/<dir>/<session id>/subagents/`. The disposable worktree is fresh, so `<dir>` must hold exactly one top-level `.jsonl` file; none or several make the source ambiguous. Run the analysis after step 3 and before step 7, with Python under `uv run`. Record the file's path, byte length and sha256 in the phase evidence; the file keeps growing after `worker_done`, so a later re-check uses the first recorded byte length. Do not copy the file into the repo (it holds full prompts and tool output); keep the analysis only. The P0 analysis scripts are `.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/session-analysis.py` (arguments: the `<dir>` folder, the top-level session file; prints the tool tally, the Skill-call timing, the Orca commands, the heartbeat times and the WC-13 scan) and `session-hbcover.py` (argument: the top-level session file; prints the heartbeat gaps with subagent time removed), each run as `uv run --no-project python -I <script> <arguments>`.
   - **Cross-check.** `ORCA orchestration worker-read --dispatch <dispatch_id> --source transcript --json`, page 1, then once more with the returned `cursor`. Record `contentComplete`, the time window page 1 covers, and whether the second page is empty. It must show the same final `check` call and the same `worker_done` as the session file, and tool calls by name (AC-0.6). If the two sources disagree, step 5 fails.
   - **Pass conditions, all read from the session file:**
     1. No `AskUserQuestion` call, in the top-level session or in any subagent session (WC-2).
     2. The command was run in the worker's top-level session, not inside an Agent-tool call (WC-7): the Skill or command call is a top-level message, not a subagent message.
     3. A `check` call appears after the command finished and before `worker_done` (WC-12).
     4. Heartbeats (WC-10), against the cadence in the worker's own dispatch preamble (5 minutes in Orca 1.4.237). Measure the time between consecutive heartbeats, from the brief to the first heartbeat, and from the last heartbeat to `worker_done`. Both limits must hold: (a) after removing the time during which any subagent of the worker was running or the worker was blocked in `ask` or `check --wait`, at most the cadence; (b) with nothing removed, at most 20 minutes. A subagent's running time is the interval from the first to the last timestamp in that subagent's own session file. Limit (a) removes legitimate waiting on a command's fan-out, during which the worker cannot heartbeat (WC-10); limit (b) bounds a hung subagent.
     5. No `worker-start`, `dispatch` or `task-create` call and no `worktree create --agent` or `agent launch` call (WC-13), searching every Bash command of the top-level and all subagent sessions under any Orca binary name. Read-only calls through the Orca binary (for example `orca-ide skills get ...`, `orca-ide --version`, `orca-ide orchestration worker-list --json`) are not these calls and are listed in the evidence.
   - **Not verifiable.** If the session file is missing, ambiguous, unreadable or contains no tool calls (it is Claude Code's format, not Orca's), conditions 1, 2, 4 and 5 are recorded `not verifiable`. Step 5 is then not passed, the live check is not recorded as passed, and the phase report lists the gap; the phase is not reported PASS until the owner accepts the gap in writing in the phase report. Condition 3 may be judged from the `worker-read` page when that page covers the end of the run. A condition that was not checked is never recorded as PASS. For an agent other than Claude no source file is defined here, so step 5 is `not verifiable` until one is specified.
   - A run shorter than the cadence passes condition 4 vacuously, so each phase report names at least one checked run that lasted longer than the cadence.
   - AC-0.6 (P0) confirmed that tool calls appear by name in `worker-read`; the session file records them as `tool_use` blocks with a `name`.
6. `git status --porcelain` in the disposable worktree. **Pass:** every path it prints that the phase did not edit is under the brief's output or report directory or is a documented artifact of the command. Ignored paths (tool caches, `.venv/`) are not checked.
7. `ORCA orchestration worker-release` for the settled worker, then `ORCA orchestration worker-list --run <run_id> --terminal-state reclaimable --json` returns no rows (`CAPS:107-113`).
```

## G2 Spec 7.3 P1 rows (spec lines 317-324)
```
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command listed for P1 in the section 6 table of commands accepting `--unattended` has a `## Unattended mode` section naming `return-contract.yaml`, `~/.claude/WORKER-CONTRACT.md` and its report directory flag, and that no other command has one yet (load, pr-submit under D3 (a), the section 4 commands, and the P2-P4 commands until their phase). Each later phase extends the list to its own commands. The test also asserts that `WORKER-CONTRACT.md` states the brief guard (its four refusal conditions, the three exact reason texts, and the `guard refused:` prefix for case 3), the never-as-worker list and the nested propagation rule; that the brief template carries the guard line before the `Command:` lines; and that brainstorm's `## Unattended mode` section turns automatic research enrichment off under `--unattended`. | passes |
| P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended` and its report directory (`--output <dir>` or `--report-dir <dir>`) | all steps pass |
| P1 | AC-1.3 | For two P1 commands, run once with no `--unattended` and no new output flag, then `git status --short`. This covers file creation only (SA-3): `claude -p "/sc:analyze src/superclaude/cli/install_core.py"` in a scratch worktree is acceptable for that, although print mode is not a person's plain session (reflect treats it as headless, section 5 SA-6). Prompt and default behaviour (SA-1) is checked separately in a plain interactive session, in the manual style of AC-2.5. Check: also one flagless run of a converted P1 command in the coordinator session with `WORKER-CONTRACT.md` loaded (manual). | no `return-contract.yaml` appears (SA-3); the manual run shows today's prompts and defaults (SA-1). Pass: that run shows today's behaviour, with no brief-guard refusal. |
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names `<output>/adversarial/return-contract.yaml` as its own contract, and its `## Unattended mode` section names `<output>/return-contract.yaml` as the worker contract that lists that file in `artifacts` (WC-4); workflow states that under `--unattended` the worker contract is written in `--report-dir` for pre-creation STOPs |
| P1 | AC-1.5 | WC-4 missing report directory: `/sc:analyze src/ --unattended` with neither `--output` nor `--report-dir`, as a 7.2 live check whose steps 3-4 are replaced by this row's conditions | no file written (step 6 empty); the chat shows the exact WC-4 error; `worker_done --outcome failed` with no `--report-path` |
| P1 | AC-1.6 | Person-mode refusal (section 2.1): `/sc:test --watch --unattended --report-dir <dir>` as a 7.2 live check | contract `worker_status: failed` with `--watch` in `reason`; outcome `failed`; no test watcher left running |
| P1 | AC-1.7 | Brief-guard refusals (section 2.1), one 7.2 live check per case, with steps 3-4 replaced by this row's conditions. Case 1: a P1 command with its report directory and no `--unattended` (for example `/sc:analyze <path> --report-dir <dir>`). Case 2: `<command with no section at this phase> --unattended --report-dir <dir>`. Case 3: `/sc:help` in the disposable worktree, never `/sc:pm`, `/sc:agent`, `/sc:git` or `/sc:pr-submit`. | For each: no file written (step 6 empty); `worker_done --outcome failed` with no `--report-path` and a body starting `guard refused:`. For case 3, the step-5 analysis of the worker's session file also shows the command was never invoked. |
| P1 | AC-1.8 | WC-9 commit grant: a commit-authorized worker started with `--worktree new-child --base-branch <feature branch>`, with the four records of AC-4.2 taken before dispatch and after the run | the only change is new commits on the worker's child branch; `git ls-remote origin` and the PR list are unchanged |
```

## G3 Spec brief guard, report directory, WC-4, WC-5 (spec lines 58-60 and 72-73)
```
- **Report directory**: the directory that holds the worker contract (WC-4). Under `--unattended` the brief passes exactly one: either the command's own existing directory-valued output flag (`--output <dir>` or `--output-dir <dir>`), or the new flag `--report-dir <dir>` (for a command without such a flag, or a brief that does not pass it). An output flag a section 3 row adds is file-valued, so those commands always take `--report-dir`. Passing neither, or both, is refused before any work (WC-4, last sentences).
- **Contract file**: one shared document, proposed as `src/superclaude/core/WORKER-CONTRACT.md`, installed to `~/.claude/WORKER-CONTRACT.md`. Core `.md` files install to `~/.claude/`: the installer copies every `*.md` in `core/` (`src/superclaude/cli/install_core.py:36,56,65-70`; `CLAUDE.md:83,408`). The new name is also added to `KNOWN_CORE_FILES` (`src/superclaude/cli/install_core.py:13-27`), which only controls which installed files `list_installed_core_files` reports (`install_core.py:12,155`); installation itself is checked by AC-0.1. The file holds the command-side rules (WC-2, WC-4, WC-8 to WC-11, the flag parse rule, the person-mode refusal above and the nested propagation rule below), the worker session's brief guard and the never-as-worker list below, and the coordinator's rules (WC-6 and section 2.3, including its brief template and the template's guard line). For the worker-session duties (WC-3, WC-5, WC-7, WC-12, WC-13 and heartbeats) it states only the IronClaude-specific rule (outcome mapping from `worker_status`, including WC-5's P0 brief override, top-level only, ask only when the brief allows it) and points to the dispatch preamble as the authority for Orca verb syntax and heartbeat cadence; it never copies them, because the preamble is issued per dispatch by the running Orca version (`CAPS:130`). Each changed command adds a short `## Unattended mode` section that lists only its own gate resolutions and report file and points to the installed contract path, so the shared rules are written once.
- **Brief guard** (worker session, from P1): it applies only in a session whose current prompt carries a live Orca preamble with Task and Dispatch IDs (see "Worker run"). Before invoking anything, the worker checks every `Command:` line of its brief (section 2.3, "Brief layout"), and only those lines. It decides case 3 from the command name alone. For the other cases it reads, as plain files, every existing copy of the command file: the project `.claude/commands/sc/<name>.md` in its worktree and `~/.claude/commands/sc/<name>.md`. It refuses, runs nothing, writes no contract, and sends `worker_done --outcome failed` with no `--report-path` and a body starting `guard refused:` when: (case 1) every existing copy has an `## Unattended mode` section and the line lacks a standalone `--unattended` (`guard refused: brief lacks --unattended`); (case 2) no existing copy has the section and the line has the flag (`guard refused: loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale)`); the copies disagree (`guard refused: command copies disagree (stale copy): <paths>`); (case 3) the command is on the never-as-worker list. A command invoked by another command, through the Skill tool or the Agent tool, is never checked; the nested propagation rule governs it. The guard checks once, before the first run: a WC-3 re-invocation keeps every token of the brief's `Command:` line, `--unattended` included, and only adds the answer.
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<report-dir>/return-contract.yaml`, where `<report-dir>` is the one report directory the brief passes (section 2.1): either the command's own directory-valued `--output` / `--output-dir`, or `--report-dir`. The coordinator therefore knows the path before dispatch even when the command's own deliverable lands at a generated or fixed location (workflow's `TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>` package, `cmd/workflow.md:12,42`; cleanup-audit's `.claude-audit/`, `cmd/cleanup-audit.md:112`; implement's ledger, `cmd/implement.md:58`; research's `claudedocs/research_[topic]_[timestamp].md`, `cmd/research.md:103`); the contract then points at that deliverable. The worker fields are top-level keys: `worker_contract_version` (`"1"` for this spec), `worker_status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), `blocked_question` when blocked, and `reason` when failed (for `/sc:implement`, also when blocked, carrying the STOP code; section 3.2 implement row). The new status field is named `worker_status`, not `status`, because existing contracts already use `status` with other values (`success | partial | failed` at `sk/sc-workflow-protocol/refs/return-contract.md:7` and `sk/sc-adversarial-protocol/SKILL.md:436`; reflect's `stopped-precondition` at `sk/sc-reflect-protocol/SKILL.md:250`). A command that already writes `return-contract.yaml` in the report directory itself (brainstorm and reflect, `<output>/return-contract.yaml`, section 3.1) keeps every existing field, including its own `status`, and adds the worker fields beside them. Where its own contract lives elsewhere (workflow's package; adversarial's `<output>/adversarial/return-contract.yaml`, whose fields sit in a nested `return_contract:` block, `sk/sc-adversarial-protocol/SKILL.md:432`, `INV-A:35`), the worker contract at `<report-dir>/return-contract.yaml` lists that file in `artifacts` and the command's own file is left unchanged. Mapping from a command's own status: `success` → `succeeded`, `partial` → `partial`, `failed` → `failed`, `stopped-precondition` → `failed` (precondition in `reason`), and the flag-STOP `blocked` of impact and graph → `failed` (the STOP in `reason`). The contract is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Under `--unattended` with no report directory, or with both a directory-valued output flag and `--report-dir`, the command does no work, writes nothing, and prints in chat the exact error `unattended mode needs exactly one report directory: --report-dir <dir>, or this command's own directory output flag`; WC-5 then gives `failed` because no report exists. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
| WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the contract's `worker_status` is `failed` or `blocked`, or no contract exists; `--outcome succeeded` when it is `succeeded` or `partial`, including an audit whose verdict is FAIL (the audit itself succeeded). The worker never reads the command's own `status` field for this; any other `worker_status` value is treated as `failed`. The first sentence of the body states `worker_status` and the verdict. If an authorized commit (WC-9) is refused or fails, the worker sends `--outcome failed`, and the body's first sentence reads `worker_status: succeeded; commit not made` followed by the reason. Before P1, when no command writes a contract, a brief that states the AC-0.4 report file and outcome rule replaces this mapping for that Task. The worker takes `--outcome` and `--report-path` from that rule. The body's first sentence then states the command's own status, or that its report file has none, instead of `worker_status`. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
```

## G4 Spec 2.3 brief layout and WC-9 commit grant (spec lines 77, 85-86)
```
| WC-9 | **No outward action from a worker; local commits only by grant.** Under `--unattended` every outward default (push, merge into a shared branch, PR, GitHub post, install on a shared or real target, VM, paid external run) is off, and no brief can turn it on (D4); the coordinator performs those actions (section 2.3). The only git write a brief may authorize is the worker session's end-of-Task local commit, made only when (1) the brief quotes, word for word, the user's instruction naming a local commit for that Task, (2) the worker runs alone in its own child worktree created by Orca (WC-11), and (3) the command has exited with `worker_status: succeeded` (per-task commits inside `/sc:implement` wait for #326 K3, and then fall only between a task's `complete` line and the next task's start, never inside a parallel batch). The worker then reads coordinator follow-ups, refuses on a detached HEAD, the default branch or any path outside its report directory, `report_path`, `artifacts` and `.dev/tasks`, stages with `git add -- <paths>` plus `.dev/tasks`, commits with `git commit --only -- <paths>` and never `--no-verify`, never pushes, and gives the commit ID in its `worker_done` body; a refused or failed commit is reported as WC-5 states. A command's own commit step stays off under `--unattended`. Outside that grant a worker never runs `git add` (including `git add .dev/tasks`), never commits, never moves HEAD and never touches a remote: the coordinator stages `.dev/tasks` (section 2.3), so the skills that stage it themselves (`sk/sc-implement-protocol/refs/managed-workspace.md:36`, `refs/ledger.md:3`, `sk/sc-workflow-protocol/SKILL.md:28`, `sk/task/SKILL.md:35`) defer that staging under `--unattended`, and MDTM's CLI-mode `git add -A` (`sk/task-builder/SKILL.md:2237`) is refused. `/sc:implement`'s private-index snapshots, its `refs/superclaude/implement/` refs and its revert stay allowed. A worker that finds `index.lock` in its worktree reports `blocked` with the path. | Command (defaults and refusals); worker session (commit grant) | `cmd/auggie-review.md:51-54` (posts by default, no prompt); `CLAUDE.md:37`; `src/superclaude/core/HOW-WE-WORK.md:282,324`; `sk/sc-post-release-protocol/SKILL.md:351`; `sk/sc-implement-protocol/SKILL.md:111,113`; `sk/sc-implement-protocol/refs/retry.md:41,220`; `.dev/orca-command-refactor/review/issue-326-evaluation.md:51,74`; per-command outward actions in column (f) of the inventories |

**Brief layout.** The brief puts the preamble-facing instructions and the guard line before the commands, and gives each command its own labelled `Command:` line in run order (for example `Command: /sc:load ...`, then the converted command), so the Task text never starts with `/sc:`. Guard line: `Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".` The coordinator decides whether a `Command:` line carries `--unattended` by the guard's own test, run on the copies the worker will see (the target worktree's project `.claude/commands/sc/` copy and `~/.claude/commands/sc/`), not on its own copy. A WC-3 re-invocation keeps every token of the `Command:` line and only adds the answer.
```

## G5 Usage line of each of the 16 P1 commands (src/superclaude/commands at the current tip)
```
### adversarial
```bash
# Mode A: Compare existing files
/sc:adversarial --compare file1.md,file2.md[,...,fileN.md] [options]
# Mode B: Generate variants from source + compare
/sc:adversarial --source source.md --generate <type> --agents <agent-spec>[,...] [options]
# Pipeline Mode: Multi-phase DAG execution (inline shorthand)
/sc:adversarial --pipeline "generate:opus:architect,haiku:architect -> compare" [options]
# Pipeline Mode: Multi-phase DAG execution (YAML file)
/sc:adversarial --pipeline @pipeline.yaml [options]
```
### Arguments
**Mode A (Compare)**:
### brainstorm
```bash
/sc:brainstorm "<topic>" [--proposals N] [--depth quick|standard|deep] \
  [--strategy systematic|agile|enterprise|auto] \
  [--codebase|--no-codebase] [--research light|deep|none|--no-research] \
  [--personas p1,p2,...] [--models opus,sonnet,haiku] \
  [--blind] [--convergence FLOAT] [--interactive] \
  [--handoff none|design|tasklist|task] [--output DIR] \
  [--dry-run] [--resume-from PATH] [--force-stale]
/sc:brainstorm "<topic>" --unattended --report-dir DIR   # worker mode, see Unattended mode
```
### cleanup-audit
```
/sc:cleanup-audit [target-path] [--pass surface|structural|cross-cutting|all] [--batch-size N] [--focus infrastructure|frontend|backend|all]
/sc:cleanup-audit --pass surface --unattended --report-dir DIR   # worker mode, see Unattended mode
```
### Arguments
- **target-path**: Directory to audit (default: `.` for entire repo)
- **--pass**: Audit pass to run (`surface` = Pass 1, `structural` = Pass 2, `cross-cutting` = Pass 3, `all` = sequential 3-pass)
- **--batch-size**: Files per agent batch (default: 50 for surface, 25 for structural, 30 for cross-cutting)
- **--focus**: Domain filter for targeted auditing (`infrastructure`, `frontend`, `backend`, `all`)
- **--unattended**: Worker mode: no step waits for a person; see Unattended mode
- **--report-dir**: With `--unattended`, the directory that holds the worker contract (required; the command has no other directory flag)
### graph
```bash
/sc:graph                                 # status (default): readiness report, 8 lines
/sc:graph status --output-dir .dev/graph  # also write return-contract.yaml
/sc:graph init                            # index this worktree (user-typed only)
/sc:graph init --worktree-local           # nested worktree: build its own index instead of the parent's
/sc:graph status --unattended --output-dir .dev/graph/run1   # worker mode: contract written there
/sc:graph status --unattended --report-dir .dev/graph/run1   # worker mode: contract in the report directory
```
### impact
```bash
/sc:impact parse_config                         # dependents of one symbol
/sc:impact load_spec write_report --depth 3     # several symbols, three hops
/sc:impact --diff                               # symbols changed in the working tree vs HEAD
/sc:impact --diff origin/master --tests         # symbols a branch changed, plus advisory tests
/sc:impact parse_config --caller sc-implement-protocol --output-dir .dev/impact/t3
/sc:impact parse_config --unattended --report-dir .dev/impact/run1   # worker mode: contract written there
```
### index-repo
**Create index**:
```
/index-repo
```
**Update existing index**:
```
/index-repo mode=update
```
**Quick index (skip tests)**:
```
/index-repo mode=quick
```
### init-lite
```text
/sc:init-lite --context-optimized [--project-root <dir>] [--output <path>] [--dry-run] [--scaffold] [--force]
/sc:init-lite --context-optimized --unattended --report-dir <dir>   # worker mode, see Unattended mode
```
### workflow
```bash
/sc:workflow <path-or-prompt>
             [--strategy systematic|agile|enterprise]
             [--depth quick|standard|deep]
             [--handoff none|design|implement|tasklist]
/sc:workflow <path-or-prompt> --unattended --report-dir <dir>   # worker mode, see Unattended mode
```
### analyze
```
/sc:analyze [target] [--focus quality|security|performance|architecture] [--depth quick|deep] [--format text|json|report]
/sc:analyze [target] [--output <file>] [--unattended] [--report-dir <dir>]
```
`--output <file>` writes the report to that file. A standalone run writes a file only when you pass it.
### build
```
/sc:build [target] [--type dev|prod|test] [--clean] [--optimize] [--verbose]
/sc:build [target] [--output <file>] [--unattended] [--report-dir <dir>]
```
`--output <file>` writes the build report to that file. A standalone run writes a file only when you pass it.
### business-panel
### Basic Usage
```bash
/sc:business-panel [document_path_or_content]
```
### Advanced Options
```bash
/sc:business-panel [content] --experts "porter,christensen,meadows"
/sc:business-panel [content] --mode debate
/sc:business-panel [content] --focus "competitive-analysis"
/sc:business-panel [content] --synthesis-only
```
### Mode Commands
### design
```
/sc:design [target] [--type architecture|api|component|database] [--format diagram|spec|code]
/sc:design [target] [--output <file>] [--unattended] [--report-dir <dir>]
```
`--output <file>` writes the design document to that file. A standalone run writes a file only when you pass it.
### document
```
/sc:document [target] [--type inline|external|api|guide] [--style brief|detailed]
/sc:document [target] [--output <path>] [--unattended] [--report-dir <dir>]
```
`--output <path>` writes the generated documentation to that path. `--type inline` edits files in place and needs no `--output`.
### explain
```
/sc:explain [target] [--level basic|intermediate|advanced] [--format text|examples|interactive] [--context domain]
/sc:explain [target] [--output <file>] [--unattended] [--report-dir <dir>]
```
`--output <file>` writes the explanation to that file. A standalone run writes a file only when you pass it.
### index
```
/sc:index [target] [--type docs|api|structure|readme] [--format md|json|yaml]
/sc:index [target] [--output <path>] [--unattended] [--report-dir <dir>]
```
`--output <path>` writes the generated documentation to that path. Without it a standalone run behaves as before.
### test
```
/sc:test [target] [--type unit|integration|e2e|all] [--coverage] [--watch] [--fix]
/sc:test [target] [--output <file>] [--unattended] [--report-dir <dir>]
```
`--output <file>` writes the test and coverage summary to that file. A standalone run writes a file only when you pass it.
```

## G6 orca worker-start usage (Orca 1.4.245-aidev02.dfe1eb410300)
```
orca orchestration worker-start

Usage: orca orchestration worker-start (--task <task_id> | --spec <text>) [--on <saved-environment>] [--worktree <current|selector|new-child|new-top-level>] (--agent <agent> | --terminal <handle>) [--task-title <text>] [--deps <json_array>] [--parent <task_id>] [--model <id>] [--effort <level>] [--name <name>] [--repo <selector>] [--base-branch <ref>] [--display-name <text>] [--comment <text>] [--

Start one supervised worker on the Run home or a connected Orca server

Options:
  --help                 Show this help message
  --timeout-ms <ms>     Maximum wait time before timing out
  --run
  --from
  --retry-request

Notes:
  Current and existing worktrees never rerun setup; a fresh agent terminal is created unless --terminal is explicit.
  When reusing --terminal, pass --worktree for that terminal; current means the coordinator worktree.
  --agent takes an Orca agent id enabled on the worker server, such as claude, codex, cursor, antigravity, muse, zcode, opencode, or opencode2.
  --model supports Claude, Codex, Cursor, Antigravity, and Muse opaque provider model ids; --effort requires --model. OMP accepts --model only; --effort is unsupported. Neither can combine with --terminal. OpenCode model selection requires an existing worktree, a verified execution-host CLI, and an available model; effort is unsupported. Other agents, including zcode, launch with the model from th
  New worktrees use agent-first creation and default --setup to run. Repository start-immediately runs setup beside the agent; wait-for-setup gates agent readiness and task input.
  New worktrees without --name get the name Orca gives an unnamed workspace; the receipt names it. Servers older than this change still require --name.
  Creation flags (--name, --repo, --base-branch, --display-name, --comment, --setup) are rejected for current/existing worktrees. Use exact --repo on the selected server; project/host convenience routing remains on worktree create.
  How the worker runs follows the user's own setting for new agent tabs; there is no flag for it and no caller needs to ask. A dispatch the setting cannot apply to still starts, so the placement, agent, and launch options passed here are always the ones honoured.
  Drive every worker the same way whichever way it was started: the same orchestration verbs, the same handle. Mail, dispatch, worker-show, worker-read and the whole lifecycle behave identically. The start receipt records which one ran, for operators and telemetry.
  Not every worker has a terminal. Read output with worker-read --source auto or --source transcript, which always work; --source terminal is refused when there is none, and orca terminal verbs do not accept every worker handle. Nothing above needs you to know which kind you have — the orchestration verbs cover all of them.
```

## G7 orca worktree create usage
```
orca worktree create

Usage: orca worktree create --name <name> [--repo <selector>|--project <id-or-name> [--host <host>]|--project-host-setup <id>] [--agent <id>] [--prompt <text>] [--model <id>] [--effort <level>] [--surface chat|terminal] [--setup run|skip|inherit] [--base-branch <ref>] [--branch <name>] [--reference <url-or-jira-key>...] [--reference-site <id>] [--issue <number>] [--pr <number>] [--linear-issue <identifier-or-url>] [--gitlab-issue <number-or-url>] [--gitlab-mr <number-or-url>] [--comment <text>] [--parent-worktree <selector>] [--no-parent] [--run-hooks] [--activate] [--retry-launch <operationId>] [--json]

```

## G8 Install state of ~/.claude now (after the owner-approved install)
adversarial: installed copy equals branch
analyze: installed copy equals branch
build: installed copy equals branch
load: installed copy equals branch
troubleshoot: installed copy equals branch
help: installed copy equals branch
analyze installed Unattended-mode sections: 1; troubleshoot: 0
WORKER-CONTRACT installed equals branch

## G9 Branch facts
f0e307eb docs(orca): update the WORKER-CONTRACT brief-flag table for P1
185f8349 Merge remote-tracking branch 'origin/master' into ironbelly/OrcaCLICommandRefactor-P1
7127c247 feat(orca): P1 static plan, add the unattended worker contract to 16 commands
8b4858f7 docs(onboarding): add the onboarding deck, built from the routing guide at adaa28d9 (#303)
tip: f0e307eb8596f1362bd7b372c55877fc98b1ea1b
7127c247 is an ancestor of the tip

## G10 P1 static report PASS lines
```
- PASS AC-1.1: `tests/skills/test_worker_contract.py` passes (394 tests). Evidence: `./artifacts/ac-1.1.txt`.
- PASS AC-1.4: adversarial SKILL names `<output>/adversarial/return-contract.yaml`; the workflow ref has the worker-contract section. Evidence: `./artifacts/ac-1.4.txt`.
- PASS AC-C1: Check SCAN prints nothing. Evidence: `./artifacts/ac-c1.txt`.
- PASS AC-C2: `make sync-dev` and `make verify-sync` both exit 0. Evidence: `./artifacts/ac-c2.txt`.
- PASS AC-C3: No baseline-passing test fails (tests/skills 1109 -> 1255 passed; wider run 6616 -> 6621 passed); the sixteen named test files each pass. Evidence: `./artifacts/ac-c3-compare.md, wider-compare.md`.
- PASS AC-C4: No `.claude/` path is staged. Evidence: `./artifacts/ac-c4-index.txt`.
- PASS AC-C5: Sixteen converted command files additive except business-panel (14 added, 4 deleted, limit 4) and load (1 added, 1 deleted). Evidence: `./artifacts/ac-c5.txt`.
- PASS AC-C6: 1 Orca profile line(s), each `"nestedWorkerMaxDepth":1`. Evidence: `./artifacts/ac-c6-depth-setting.txt`.
- PASS lint: `make lint` exit 0, no new ERROR, ruff finding or WARN; one existing size WARN grew and is recorded below. Evidence: `./artifacts/lint-format-compare.md`.
- PASS format: The five test files are formatted. Evidence: `./artifacts/lint-format-compare.md`.
- PASS mirror check: The four workflow mirror pairs are byte-identical. Evidence: `./artifacts/mirror-check.txt`.

Overall: PASS (11 of 11).
```

## G11 claude CLI flags used by Task 23
```
  --max-budget-usd <amount>             Maximum dollar amount to spend on API
  --permission-mode <mode>              Permission mode to use for the session
```

## G12 WORKER-CONTRACT.md sections 1 and 5 (brief guard, slot rules, template)
```
## 5. Coordinator brief template

Copy this template into each Task's spec, one brief per Task, and fill every angle-bracket slot. The guard line is copied word for word and comes before the first `Command:` line.

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
On a blocked gate: report blocked
Local commit: not authorized
Report directory: <directory unique to this Task>
Worktree: <shared feature worktree | child worktree created by Orca with worker-start --worktree new-child --base-branch <feature branch> --setup <skip | run (only when named in the user's instruction)>>
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
P0 only: Report file: <the command's report file under AC-0.4>. Outcome rule: --outcome failed when the file is missing or empty, or its status is failed or blocked; otherwise --outcome succeeded. This rule replaces the WC-5 mapping for this Task.
Command: /sc:<name> <arguments> <flags this command's brief rule requires>
```

Slot rules:

- `On a blocked gate:` is `report blocked` (the default) or `ask the coordinator` (WC-3).
- `Local commit:` is `not authorized`, or `authorized` followed by the user's instruction naming a local commit for this Task, quoted word for word (WC-9, decision D4).
- `--unattended` goes on a `Command:` line only when the guard's test shows that every copy of that command file the worker will see has an `## Unattended mode` section. At P0 no command accepts it. From P1 the 16 commands converted in P1 do (adversarial, brainstorm, cleanup-audit, graph, impact, index-repo, init-lite, workflow, analyze, build, business-panel, design, document, explain, index, test).
- The `P0 only:` line is used only before P1, when no command writes a worker contract. At P0 the report files are: troubleshoot, `<dir>/REPORT.md` with the status in its `**Status**:` line; workflow, the `return-contract.yaml` in the one new `TASK-WF-*` package directory the run creates under `.dev/tasks/to-do/`, with the status in its top-level `status`; adversarial, `<dir>/adversarial/merge-log.md` with the status in the `Status:` line of its `## Metadata` section. From P1 the line is dropped and WC-5 applies.

Flags the brief must pass, for the 12 commands that are ready with brief constraints. `--report-dir` is marked "from P1": no command accepts it at P0. Under `--unattended` the brief passes exactly one report directory (`--report-dir <dir>`, or the command's own directory flag where the row names one); `/sc:index-repo` and `/sc:init-lite` have no directory flag of their own, so they take `--report-dir`.

| Command | Brief must pass |
|---|---|
| `/sc:adversarial` | `--output <dir>`; never `--interactive` |
| `/sc:brainstorm` | `--output <dir>`; never `--interactive` |
| `/sc:cleanup-audit` | `--pass <N>` (single pass); `--report-dir <dir>` (from P1) |
| `/sc:graph` | `status` (the default) with `--output-dir <dir>`; never `init`, which runs only when the user's own message starts with `/sc:graph init` |
| `/sc:impact` | `--output-dir <dir>` |
| `/sc:index-repo` | none at P0; `--report-dir <dir>` (from P1) |
| `/sc:init-lite` | `--output <file>` (names the report file); `--report-dir <dir>` (from P1) |
| `/sc:reflect` | no `--remediate`; `--no-promote` when the coordinator owns folder moves |
| `/sc:release-split` | spec-shaped input; default `--r1-scope`; never `--interactive` |
| `/sc:tdd` | a precise component prompt, not a bare topic; `--output <file>` |
| `/sc:troubleshoot` | no `--fix` (and no `--depth deep` until P2) |
| `/sc:workflow` | `--handoff none`; `--report-dir <dir>` (from P1); its `--output` is retired |
```

## G11 claude CLI flags used by Task 23
```
  --max-budget-usd <amount>             Maximum dollar amount to spend on API
  --permission-mode <mode>              Permission mode to use for the session
```

## Coverage slice

| Requirement (inferred) | Citation | Match | Best task | Ratio |
|---|---|---|---|---|
| INF-001: 'AC-1.2: the section 7.2 live check (all seven steps) on each of the sixteen P1 commands, run with `--unattend | source.md:8 | containment | T24 | 0.88 |
| INF-002: 'AC-1.3: the file-creation part (two flagless runs, then `git status --short`).' | source.md:9 | containment | T23 | 1.00 |
| INF-003: 'AC-1.5: missing report directory. AC-1.6: person-mode refusal. AC-1.7: the three brief-guard refusal cases. A | source.md:10 | containment | T25 | 0.74 |
| INF-004: 'The P1 phase report that cites the passed static report, adds the live results and states the phase verdict.' | source.md:11 | containment | T25 | 0.64 |
| INF-005: 'If the installed files differ from the branch, Task 1 records FAIL and every later live task records `not run | source.md:17 | containment | T24 | 0.75 |
| INF-006: 'No edit to any source, command, skill, agent or test file' | source.md:18 | none | T22 | 0.57 |
| INF-007: 'No git commit, push, merge, rebase, reset, stash, branch deletion, PR, `gh` write of any kind, no `superclaud | source.md:19 | containment | T24 | 0.60 |
| INF-008: 'UV for every Python command, in the executor and in every subagent it starts' | source.md:20 | none | T21 | 0.33 |
| INF-009: 'Staging: never stage anything under `.claude/`. At the end `git add .dev/tasks`.' | source.md:21 | containment | T25 | 0.82 |
| INF-010: 'A failed live check is a recorded result: it is not retried, rerun or repaired, and no second worker is start | source.md:22 | containment | T9 | 0.64 |
| INF-011: 'Every `orca orchestration check --wait` call runs with a Bash tool timeout of at least 300000 ms' | source.md:24 | none | T24 | 0.33 |
| INF-012: 'At least one checked run in the phase must last longer than the heartbeat cadence the preamble states; the re | source.md:25 | containment | T25 | 0.69 |
| INF-013: "step 5 is read from the worker's own Claude session file with the P0 scripts" | source.md:26 | containment | T24 | 0.73 |
| INF-014: 'one fenced block per check, saved to `./artifacts/lc<NN>-brief.txt` and passed to `task-create --spec` unchan | source.md:34 | containment | T25 | 0.71 |
| INF-015: "Step 3 pass: exactly one `worker_done`; `--outcome` matches the contract's `worker_status` under WC-5" | source.md:32 | containment | T18 | 0.86 |
