---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-orcaWorkerContra-20261102-231950
version: "1"
priority: Medium
created_date: "2026-11-02"
---

# Orca worker contract: Phase P0 (contract, routing guide, static tests, live baseline)

Source: ./source.md
Goal: Phase P0 of the approved Orca worker-contract spec is delivered: `src/superclaude/core/WORKER-CONTRACT.md` exists and installs to `~/.claude/`, the routing guide has an Orca section in all its required copies, `tests/skills/test_worker_contract.py` pins the contract's rules and the git/GitHub write-verb audit, and the live Orca baseline (three smoke runs, launch timing, transcript tool names, nesting-depth trace) is recorded, with every P0 check of `./source.md` section 7 passing.

## Constraints

- Scope is Phase P0 only (`./source.md` section 6, P0 row; section 7.1 common checks; section 7.3 rows AC-0.1 to AC-0.9). The spec requires one written plan per phase (`./source.md` section 6, last paragraph) and says later phases start only after the earlier phase's checks pass (section 6, first paragraph). Phases P1 (report files and no-gate commands), P2 (gate conversion), P3 (interface drift and shared state) and P4 (implement, post-release) are deferred to their own `/sc:workflow` plans, written after this plan's checks pass; they are not dropped.
- P0 edits no command, skill or agent file (`./source.md` section 6, P0 row: "no command edits"). No command gains `--unattended` or an `## Unattended mode` section in P0 (section 6, table "Which commands accept `--unattended`", P0 row: none).
- `WORKER-CONTRACT.md` restates only what `./source.md` sections 2.1, 2.2 and 2.3 already say; it adds no rule the spec lacks, and for Orca verb syntax and heartbeat cadence it points to the dispatch preamble instead of copying them (section 2.1, "Contract file").
- `src/superclaude/` is the source of truth. After editing it, run `make sync-dev`; never stage `.claude/` paths other than `.claude/settings.json` (repo `CLAUDE.md`, "Never Stage or Commit `.claude/` Contents"). `.dev/tasks/` is always staged (`git add .dev/tasks`); staging is not committing.
- No command, skill or agent file may call `orca` or `orca-ide` (`./source.md` SA-2, AC-C1). Only `WORKER-CONTRACT.md` and `HOW-WE-WORK.md` (and their plugin copies) may describe the coordinator side.
- Every git and GitHub outward action targets `IronbellyOrg/IronClaude` only; SuperClaude upstream is never pushed to or interacted with (`./source.md` section 2.3, "Git and GitHub ownership"). This plan pushes nothing and opens no PR.
- Commits and installs need the owner's approval at the moment of action: committing P0's edits for the live checks, and running `uv run superclaude install --force` from this checkout (`./source.md` section 7.2). `--force` overwrites installed core files, rules, output styles and agents in `~/.claude/`, including `~/.claude/CLAUDE.md`; say so when asking. If P0 is abandoned, reinstall from master with `superclaude install --force`.
- Orca: outside an Orca terminal the executable is `orca-ide`, never bare `orca` (`./source.md` section 7, `ORCA` note). The coordinator for live checks is a session the person opened, never one started by `worker-start` (`./source.md` D5, non-goal 2). Worktrees are created by Orca at Orca's default paths, never under `.dev/worktrees/`, and removed with `orca-ide worktree rm` after use.
- Use `uv run` for all Python.

## Phase 1: Shared worker contract

## Task 1: Write the command-side and worker-session rules of `WORKER-CONTRACT.md`

Before any edit in this plan, record the test baseline for AC-C3: run `uv run pytest tests/skills/ -q -rf` and save its full output to `./artifacts/ac-c3-baseline.txt` (`./source.md` section 7.1, AC-C3).

Create `src/superclaude/core/WORKER-CONTRACT.md` with the rules `./source.md` section 2.1 ("Contract file") assigns to it, written from these source sections:
- Terms from section 2.1: worker run, unattended mode (selected only by the flag, decision D1), the flag parse rule, the person-mode flag refusals, the report directory rule (exactly one of the command's own directory output flag or `--report-dir`), the brief guard (its scope, its three refusal cases plus the copies-disagree refusal, and their exact `guard refused:` reason texts), the never-as-worker list, and the nested propagation rule.
- Command-side requirements from section 2.2: WC-2, WC-4 (the contract fields `worker_contract_version`, `worker_status`, `command`, `report_path`, `artifacts`, `blocked_question`, `reason`; the status mapping; the exact missing-directory error text), WC-8, WC-9, WC-10 and WC-11.
- Worker-session duties from section 2.2: WC-3, WC-5, WC-7, WC-12, WC-13 and heartbeats, stating only the IronClaude-specific rule and pointing to the dispatch preamble for verb syntax and cadence.

Acceptance criteria:
- `src/superclaude/core/WORKER-CONTRACT.md` exists and contains each item listed above, using the spec's own identifiers (WC-2 to WC-13 as listed, the four `guard refused:` reason texts, and the never-as-worker list naming `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn`, `/sc:swarm-wizard` and `/sc:pr-submit`).
- The file contains no `orca orchestration` verb syntax copied from Orca's guides and no fixed heartbeat cadence; it points to the dispatch preamble for both.
- `./artifacts/ac-c3-baseline.txt` exists and was written before any file in this plan changed.

## Task 2: Add the coordinator rules and brief template to `WORKER-CONTRACT.md`

Depends on: Task 1

Add the coordinator's rules to `src/superclaude/core/WORKER-CONTRACT.md` from `./source.md`: WC-6 (every retry is a new Task, never `--retry-of`; the three-failed-starts comparison; settling a crashed attempt), and section 2.3 in full: what the brief states, the brief layout with the exact guard line, feature and child worktrees (Orca default paths, the WC-11 triggers, placement map, merge-back and removal rules), git and GitHub ownership (fork only, PRs only through `/sc:pr-submit --monitor 3`, review before pushing unseen worker commits, the coordinator stages `.dev/tasks` at every commit and at the end of the run), reading a result before anything depends on it (including the guard-refusal bullet and the rule that dependents are created only after their inputs settle), the `/sc:implement` stop rules (freeze, lifting the freeze, the seven-condition check before a resume Task, placement), and the fan-in rule (at most 10 inputs, merge only with at least 2 admitted). Then add a coordinator brief template that carries the guard line before the `Command:` lines and lists, per command, the "Brief must pass" flags of `./source.md` section 3.1 (adversarial, brainstorm, cleanup-audit, graph, impact, index-repo, init-lite, reflect, release-split, tdd, troubleshoot, workflow).

Acceptance criteria:
- `WORKER-CONTRACT.md` states WC-6 and every section 2.3 rule named above, including the exact guard line text from section 2.3 "Brief layout".
- The brief template places the guard line before the first `Command:` line and names the section 3.1 flags for each of the 12 ready commands.
- The file mentions Orca commands only as the coordinator's and worker session's channel, which `./source.md` SA-2 permits for this file.

## Task 3: Register `WORKER-CONTRACT.md` as an installed core file

Depends on: Task 1

Add `"WORKER-CONTRACT.md"` to `KNOWN_CORE_FILES` in `src/superclaude/cli/install_core.py` (lines 13-25 today). `tests/cli/test_how_we_work_install.py:44` asserts that `KNOWN_CORE_FILES` equals the set the installer ships, so both must agree. Decide whether a copy belongs in `plugins/superclaude/core/` by reading `scripts/build_superclaude_plugin.py` and the files already in `plugins/superclaude/core/`: add the copy only if that existing convention requires it, and record the decision with its evidence in `./artifacts/t3-plugin-mirror.md`.

Acceptance criteria:
- `uv run python -c "from superclaude.cli.install_core import KNOWN_CORE_FILES; assert 'WORKER-CONTRACT.md' in KNOWN_CORE_FILES"` exits 0 (AC-0.1, first part).
- The AC-0.1 install check exits 0: `uv run python -c "import pathlib, tempfile; from superclaude.cli.install_core import install_core_files; d = pathlib.Path(tempfile.mkdtemp()); ok, msg = install_core_files(target_path=d); assert ok, msg; assert (d / 'WORKER-CONTRACT.md').is_file()"`.
- `uv run pytest tests/cli/test_how_we_work_install.py tests/cli/test_issue_body_templates.py -q` passes.
- `./artifacts/t3-plugin-mirror.md` states whether a plugin copy was added and cites the file lines that decided it.

## Phase 2: Routing guide

## Task 4: Add an Orca section to the routing guide and its copies

Depends on: Task 2

Add one new section to `src/superclaude/core/HOW-WE-WORK.md` describing Orca coordination as `./source.md` defines it: the coordinator is a session the person opened (D5); it dispatches IronClaude commands as workers using the brief template in `~/.claude/WORKER-CONTRACT.md`; a command is dispatched with `--unattended` only after the phase that converts it has passed (after P0, none); `/sc:pr-submit` and the six section 4 commands are never workers; worktrees are created by Orca at its default paths; outward actions stay with the coordinator on `IronbellyOrg/IronClaude`. Point to `~/.claude/WORKER-CONTRACT.md` for the rules instead of restating them. Change no existing line and no routing-table row (`./source.md` SA-5). Then copy the file byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; if the level table is untouched, `src/superclaude/core/CLAUDE.md` needs no change (repo `CLAUDE.md`, "Key Documentation Files"). Run `make sync-dev`.

Acceptance criteria:
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` exits 0, and `uv run pytest tests/core/test_how_we_work_routing_table.py tests/core/test_claude_md_routing_block.py tests/cli/test_how_we_work_install.py -q` passes (AC-0.2).
- `git diff --numstat "$(git merge-base master HEAD)" -- src/superclaude/core/HOW-WE-WORK.md | awk '$2 != 0'` prints nothing (AC-0.3: no existing line deleted).
- The AC-C1 scan in `./source.md` section 7.1 prints nothing, and `make verify-sync` exits 0 (AC-C2).

## Phase 3: Static tests

## Task 5: Add `tests/skills/test_worker_contract.py` for the contract's rules

Depends on: Task 2

Create `tests/skills/test_worker_contract.py`. It reads `src/superclaude/core/WORKER-CONTRACT.md` and asserts that the file states each rule `./source.md` section 2.1 assigns to it (the items listed in Tasks 1 and 2, including the four `guard refused:` reason texts, the never-as-worker list and the nested propagation rule), the section 2.3 dependent-creation rule and the fan-in cap (AC-0.1, last part), and that the brief template carries the guard line before its `Command:` lines. It also asserts that no file in `src/superclaude/commands/` has an `## Unattended mode` section, because no command accepts `--unattended` after P0 (`./source.md` section 6 table, P0 row); later phases extend this list.

Acceptance criteria:
- `uv run pytest tests/skills/test_worker_contract.py -q` passes.
- Deleting any one asserted rule from a scratch copy of `WORKER-CONTRACT.md` makes the matching assertion fail; record the scratch-copy run in `./artifacts/t5-negative-check.txt`.

## Task 6: Add the git and GitHub write-verb audit (AC-0.9)

Depends on: Task 5

Extend `tests/skills/test_worker_contract.py` with the AC-0.9 audit (`./source.md` section 7.3): scan `src/superclaude/skills/`, `src/superclaude/commands/` and `src/superclaude/agents/` for git and gh write verbs (`git add`, `git commit`, `git push`, `git merge`, `git worktree add`, `git worktree remove`, `git stash`, `git update-ref`, `gh pr`, and `gh api` posts). Each hit must be allowed by WC-9 (for example `/sc:implement`'s snapshot, refs and revert), marked as refused under `--unattended` by the phase that converts its command, or listed on an explicit allowlist in the test with a one-line reason. List every hit in the test's allowlist or classification table; do not leave discovery to a later run. Save the raw hit list to `./artifacts/ac-0.9-hits.txt`. Then compare the full skills suite with the Task 1 baseline (AC-C3).

Acceptance criteria:
- `uv run pytest tests/skills/test_worker_contract.py -q` passes with the audit included, and the audit fails when a new unclassified write verb is added to a scratch skill file (recorded in `./artifacts/t6-negative-check.txt`).
- `./artifacts/ac-0.9-hits.txt` lists every hit with its classification.
- `uv run pytest tests/skills/ -q -rf` shows no test that passed in `./artifacts/ac-c3-baseline.txt` now failing (AC-C3); the comparison is saved to `./artifacts/ac-c3-after.txt`.

## Phase 4: Live Orca baseline

## Task 7: Commit P0's edits and install P0 into `~/.claude`, each with the owner's approval

Depends on: Task 4, Task 6

`./source.md` section 7.2 requires the phase's edits on a branch before Orca can build a test worktree, and P0 installed into `~/.claude` before the live checks. Ask the owner, in plain words, to approve committing P0's edits to the current feature branch `ironbelly/OrcaCLICommandRefactor-Specs`; on approval, stage the explicit P0 paths plus `.dev/tasks` (never `.claude/` mirrors) and commit with `git commit --only -- <paths>`, never `--no-verify`, and do not push. Then ask the owner to approve `uv run superclaude install --force` run from this checkout, stating that `--force` overwrites installed core files, rules, output styles and agents in `~/.claude/` including `~/.claude/CLAUDE.md`; on approval, run it. If either approval is refused, stop this task and report that the live checks cannot run. Make the commit the last action of the task.

Acceptance criteria:
- `./artifacts/t7-approvals.md` records both questions, the owner's answers verbatim, the commit ID and the install output.
- `git diff --cached --name-only | grep '^\.claude/' | grep -v '^\.claude/settings\.json$'` printed nothing before the commit (AC-C4).
- `test -s ~/.claude/WORKER-CONTRACT.md` succeeds and `cmp ~/.claude/WORKER-CONTRACT.md src/superclaude/core/WORKER-CONTRACT.md` exits 0.
- `git ls-remote origin` shows no new push from this task.

## Task 8: Run the P0 smoke runs as live Orca workers (AC-0.4, AC-0.5, AC-0.6)

Depends on: Task 7

From the person-opened session acting as coordinator, create one Orca Run and run the `./source.md` section 7.2 live check, steps 1-3 and 5-7 (step 4 uses each command's existing report file, since the contract arrives in P1), on each of: `/sc:troubleshoot "<real symptom>"` with no `--fix` and no `--depth deep`; `/sc:workflow "<small change>" --handoff none`; `/sc:adversarial --compare <two files> --depth quick --output <dir>`. Each brief uses the section 2.3 brief layout with the command on a `Command:` line, and each worker runs its command directly, not inside an Agent-tool call. For AC-0.5, time one `worker-start` that uses the person's normal launch setup. For AC-0.6, read one transcript with `orca-ide orchestration worker-read --dispatch <id> --source transcript --json` and record whether tool calls appear by name. Use disposable worktrees created by Orca at its default paths from the Task 7 commit, run `make sync-dev` inside each unless `--setup run` is confirmed to do it (UNVERIFIED item 27), and remove each with `orca-ide worktree rm` after step 7.

Acceptance criteria:
- `./artifacts/ac-0.4-smoke.md` records, per command, each 7.2 step's result, the dispatch ID, the report file path and whether the transcript shows the command run at the top level; all listed steps pass, or the failure is recorded and flagged as reopening `./source.md` section 1.
- `./artifacts/ac-0.5-timing.md` records the measured start time; it passes when the start returns `state: ready` in under 45 s.
- `./artifacts/ac-0.6-transcript.md` states yes or no with a quoted transcript excerpt.
- `orca-ide orchestration worker-list --run <run_id> --terminal-state reclaimable --json` returns no rows, and every disposable worktree is gone from `orca-ide worktree list --json`.

## Task 9: Trace Orca's nesting-depth enforcement and check the depth setting (AC-0.7, AC-C6)

Read-only. Using the AC-0.7 starting point in `./source.md` section 7.3 (`grep -rlE 'nested_worker_depth_exceeded|NESTED_WORKER_DEPTH_EXCEEDED_CODE' /opt/Orca/resources/app.asar.unpacked/out/`), trace which calls check nesting depth (`worker-start`, `dispatch`, `task-create`, low-level dispatch, `worktree create --agent`, `agent launch`) and what depth Orca gives a session the person opens. No live probe. Then run the AC-C6 check: `grep -ho '"nestedWorkerMaxDepth":[0-9]*' "${ORCA_RUNTIME_SOURCE_PROFILE_PATH:-$HOME/.config/orca}"/profiles/*/orca-data.json`.

Acceptance criteria:
- `./artifacts/ac-0.7-depth-trace.md` lists each call as checked, not checked or not found, and the depth of a person-opened session, each with a `path:line` in Orca's installed code; any call not checked is recorded as covered only by WC-13 and 7.2 step 5.
- `./artifacts/ac-c6-depth-setting.txt` holds the AC-C6 output; every printed line is `"nestedWorkerMaxDepth":1`, and any profile that prints nothing is recorded as using Orca's presumed default of 1.
