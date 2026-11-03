---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-orcaWorkerContra-20261103-012232
version: "2"
priority: Medium
created_date: "2026-11-03"
---

# Orca worker contract: Phase P0 static plan (contract, routing guide, static tests, read-only Orca checks)

Source: ./source.md
Goal: The static part of Phase P0 of the Orca worker-contract spec is delivered and checked. `src/superclaude/core/WORKER-CONTRACT.md` exists, is listed in `KNOWN_CORE_FILES` and installs into a fresh directory. The routing guide has an Orca section in every copy the repo keeps. `tests/skills/test_worker_contract.py` pins the contract's rules and the git and GitHub write-verb audit. The read-only Orca checks (nesting-depth trace and depth setting) are recorded. A static report states each static check's result and the exact file list for the owner-approved commit, which happens outside this plan.

## Constraints

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

## Phase 1: Shared worker contract

## Task 1: Write the command-side and worker-session rules of `WORKER-CONTRACT.md` and register it as a core file

Before any edit in this plan, record two baselines:
- the AC-C3 baseline: run `uv run pytest tests/skills/ -q -rf` and save its full output to `./artifacts/ac-c3-baseline.txt` (`./source.md` section 7.1, AC-C3);
- the wider baseline that Task 4 compares against: run `uv run pytest tests/core tests/commands tests/recommend tests/cli -q -rf --ignore=tests/cli/eval/test_perf_home_setup.py` and save its full output to `./artifacts/t1-baseline-wider.txt`. The `--ignore` keeps that test from rewriting the tracked file `.dev/releases/current/cliEval/evidence/T02.15/perf.json`. After each baseline run, `git status --short` must show no tracked file changed by the run.

Both baselines are inputs, not evidence: they may contain failures that exist before this plan. Eight such failures are known on 2026-11-03 and are accepted as the baseline:
- `tests/cli/eval/test_ban_import_rule.py::test_clean_tree_passes_ruff_check`
- `tests/cli/eval/test_ban_import_rule.py::test_synthetic_import_anthropic_is_flagged_by_ruff`
- `tests/cli/eval/test_ban_import_rule.py::test_ban_message_references_fr_g1`
- `tests/cli/eval/test_claude_process_adapter.py::test_ruff_flags_synthetic_anthropic_import_under_cli_eval`
- `tests/cli/eval/test_claude_process_adapter.py::test_ruff_passes_on_real_adapter_module`
- `tests/cli/test_verify_sync_hooks.py::test_V1_clean_tree_exits_zero`
- `tests/cli/test_verify_sync_hooks.py::test_V2_missing_claude_hook_detected`
- `tests/cli/test_verify_sync_hooks.py::test_V7_regression_to_master`

Write `./artifacts/t1-accepted-failures.md`. It records that both baseline files exist and lists every test that fails in either baseline. Each failing test gets one of two labels: `accepted` if it is in the list above, or `pre-existing` if not. Cite that file, not the raw logs, as this task's evidence.

Create `src/superclaude/core/WORKER-CONTRACT.md` with the rules `./source.md` section 2.1 ("Contract file") assigns to it, written from these source sections:
- Terms from section 2.1: worker run; unattended mode (selected only by the flag, decision D1); the flag parse rule; the person-mode flag refusals; the report directory rule (exactly one of the command's own directory output flag or `--report-dir`); the brief guard, with its scope and its four refusal conditions (case 1, case 2, copies disagree, case 3), its three exact reason texts (`guard refused: brief lacks --unattended`, `guard refused: loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale)`, `guard refused: command copies disagree (stale copy): <paths>`) and the `guard refused:` body prefix for case 3; the never-as-worker list; and the nested propagation rule.
- Command-side requirements from section 2.2: WC-2; WC-4 (the contract fields `worker_contract_version`, `worker_status`, `command`, `report_path`, `artifacts`, `blocked_question`, `reason`, the status mapping, and the exact missing-directory error text); WC-8, WC-9, WC-10 and WC-11.
- Worker-session duties from section 2.2: WC-3, WC-5 (including its last sentences: before P1, a brief that states the AC-0.4 report file and outcome rule replaces the mapping for that Task), WC-7, WC-12, WC-13 and heartbeats, stating only the IronClaude-specific rule and pointing to the dispatch preamble for verb syntax and cadence.

For each rule above, record in `./artifacts/t1-rule-phrases.md` at least one short phrase that the contract file carries for it. Take the phrase from `./source.md` where the spec's own wording can be used (for example the reason texts and the WC-4 error text, copied exactly). For WC-12, WC-13 and heartbeats, use the phrases "Coordinator follow-ups are pulled, not pushed" and "at natural checkpoints" (`./source.md` WC-12), "No Orca fan-out from the worker session" (WC-13), and "at the cadence its preamble sets" (WC-10). Do not copy any Orca verb syntax. Task 5 pins these phrases.

In the same task, add `"WORKER-CONTRACT.md"` to the `KNOWN_CORE_FILES` frozenset in `src/superclaude/cli/install_core.py`. `tests/cli/test_how_we_work_install.py` asserts that `KNOWN_CORE_FILES` equals the set of core files the installer ships, so the file and the entry must land together.

Acceptance criteria:
- `src/superclaude/core/WORKER-CONTRACT.md` exists and contains each item listed above under the spec's own identifiers: WC-2 to WC-13 as listed, the four refusal conditions with the three exact reason texts and the case-3 prefix, the WC-5 P0 override, and the never-as-worker list naming `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn`, `/sc:swarm-wizard` and `/sc:pr-submit`.
- The worker-session part contains no `orca orchestration` verb syntax copied from Orca's guides and no fixed heartbeat cadence; it points to the dispatch preamble for both.
- `uv run python -c "from superclaude.cli.install_core import KNOWN_CORE_FILES; assert 'WORKER-CONTRACT.md' in KNOWN_CORE_FILES"` exits 0 (AC-0.1, first part), and `uv run pytest tests/cli/test_how_we_work_install.py -q` passes.
- `./artifacts/t1-accepted-failures.md` records that `./artifacts/ac-c3-baseline.txt` and `./artifacts/t1-baseline-wider.txt` were written before any file in this plan changed. It lists every failing test in them, labelled `accepted` or `pre-existing`, and states that the runs changed no tracked file.
- `./artifacts/t1-rule-phrases.md` names at least one phrase per rule listed above. Each phrase is present in `src/superclaude/core/WORKER-CONTRACT.md`, and none of them is Orca verb syntax.
- The file contains no `src/superclaude/` path and no `CAPS:`, `INV-` or `EVIDENCE.md:` citation.

## Task 2: Add the coordinator rules and the brief template to `WORKER-CONTRACT.md`

Depends on: Task 1

Add the coordinator's rules to `src/superclaude/core/WORKER-CONTRACT.md` from `./source.md`:
- WC-6: every retry is a new Task, never `--retry-of`; the three-failed-starts comparison; settling a crashed or stalled attempt.
- Section 2.3 in full: what the brief states, including the P0-only item "the command's report file and the outcome rule AC-0.4 gives for it (WC-5)"; the brief layout with the exact guard line; feature and child worktrees (Orca default paths, the WC-11 triggers, the placement map, merge-back and removal rules); git and GitHub ownership (fork only, PRs only through `/sc:pr-submit --monitor 3`, review before pushing unseen worker commits, the coordinator stages `.dev/tasks` at every commit and at the end of the run); reading a result before anything depends on it (including the guard-refusal bullet and the rule that dependents are created only after their inputs settle); the `/sc:implement` stop rules (freeze, lifting the freeze, the seven-condition check before a resume Task, placement); and the fan-in rule, in the spec's words: the merge command's "maximum of 10 inputs", and a merge Task only when "at least 2 inputs are admitted".

Then add a coordinator brief template. It carries the guard line copied word for word from section 2.3 "Brief layout" before the first `Command:` line. It lists, per command, the "Brief must pass" flags of `./source.md` section 3.1 for the 12 ready commands: adversarial, brainstorm, cleanup-audit, graph, impact, index-repo, init-lite, reflect, release-split, tdd, troubleshoot and workflow. It marks `--report-dir` as "from P1", because no command accepts it at P0 (section 6, P1 row). It has a P0-only line for the report file and outcome rule of AC-0.4.

Append one phrase per rule added in this task to `./artifacts/t1-rule-phrases.md`, following the same rules as Task 1.

Acceptance criteria:
- `./artifacts/t1-rule-phrases.md` names at least one phrase for WC-6 and for each section 2.3 rule above, and each phrase is present in `WORKER-CONTRACT.md`.
- `WORKER-CONTRACT.md` states WC-6 and every section 2.3 rule named above, including the exact guard line text from section 2.3 "Brief layout" and the P0-only brief item.
- The brief template places the guard line before the first `Command:` line, names the section 3.1 flags for each of the 12 ready commands, marks `--report-dir` as "from P1", and has the P0-only report-file and outcome-rule line.
- The file mentions Orca commands only as the coordinator's and the worker session's channel, which `./source.md` SA-2 permits for this file.

## Task 3: Decide the plugin copy of `WORKER-CONTRACT.md` and run the AC-0.1 install check

Depends on: Task 2

Decide whether a copy of `WORKER-CONTRACT.md` belongs in `plugins/superclaude/core/`. Read `scripts/build_superclaude_plugin.py` and list the files already in `plugins/superclaude/core/` (today it holds some core files but not `CLAUDE.md` or `HOW-WE-WORK.md`). Add the copy only if that existing convention requires it, and record the decision and the file lines that decided it in `./artifacts/t3-plugin-mirror.md`. If a copy is added, run `make sync-dev` afterwards.

Acceptance criteria:
- The AC-0.1 install check in `./source.md` section 7.3 (the block below the table) exits 0: `uv run python -c "import pathlib, tempfile; from superclaude.cli.install_core import install_core_files; d = pathlib.Path(tempfile.mkdtemp()); ok, msg = install_core_files(target_path=d); assert ok, msg; assert (d / 'WORKER-CONTRACT.md').is_file()"`.
- `uv run pytest tests/cli/test_how_we_work_install.py tests/cli/test_issue_body_templates.py -q` passes.
- `./artifacts/t3-plugin-mirror.md` states whether a plugin copy was added and cites the file lines that decided it; if a copy was added, `cmp src/superclaude/core/WORKER-CONTRACT.md plugins/superclaude/core/WORKER-CONTRACT.md` exits 0.

## Phase 2: Routing guide

## Task 4: Add an Orca section to the routing guide and its copies

Depends on: Task 2

Add one new section to `src/superclaude/core/HOW-WE-WORK.md` that describes Orca coordination as `./source.md` defines it:
- the coordinator is a session the person opened (D5);
- it dispatches IronClaude commands as workers using the brief template in `~/.claude/WORKER-CONTRACT.md`;
- a command is dispatched with `--unattended` only when its command file has an `## Unattended mode` section (section 6, "Which commands accept `--unattended`");
- `/sc:pr-submit` and the other commands on the never-as-worker list in `~/.claude/WORKER-CONTRACT.md` are never workers;
- worktrees are created by Orca at its default paths;
- outward actions stay with the coordinator, on `IronbellyOrg/IronClaude`.

Append the section as a new top-level `##` section after the `<!-- /routing-table -->` marker at the end of the file, outside the level-table, other-commands and routing-table markers. Write it in ASCII only: no em dashes, arrows or other non-ASCII characters (`tests/core/test_how_we_work_routing_table.py` checks this). Point to `~/.claude/WORKER-CONTRACT.md` for the rules instead of restating them, and do not hard-code which commands accept the flag. Change no existing line and no routing-table row (`./source.md` SA-5). Then copy the file byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. The section 6 P0 row's other mirrored copy is the level table in `src/superclaude/core/CLAUDE.md`: if the level table is untouched, that copy needs no change (repo `CLAUDE.md`, "Key Documentation Files"). Run `make sync-dev`.

Acceptance criteria:
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` exits 0, and `uv run pytest tests/core/test_how_we_work_routing_table.py tests/core/test_claude_md_routing_block.py tests/cli/test_how_we_work_install.py -q` passes (AC-0.2).
- `git diff --numstat "$(git merge-base master HEAD)" -- src/superclaude/core/HOW-WE-WORK.md | awk '$2 != 0'` prints nothing (AC-0.3: no existing line deleted).
- `uv run pytest tests/core tests/commands tests/recommend tests/cli -q -rf --ignore=tests/cli/eval/test_perf_home_setup.py` shows no test that passed in `./artifacts/t1-baseline-wider.txt` now failing. The per-test comparison, which names each remaining failure as accepted in `./artifacts/t1-accepted-failures.md`, is saved to `./artifacts/t4-wider-compare.md`. That comparison file is this check's evidence, not the raw log, and `git status --short` shows no tracked file changed by the run.
- The AC-C1 scan in `./source.md` section 7.1 prints nothing, and `make verify-sync` exits 0 (AC-C2).

## Phase 3: Static tests

## Task 5: Add `tests/skills/test_worker_contract.py` for the contract's rules

Depends on: Task 3

Create `tests/skills/test_worker_contract.py`. It reads the contract from a module-level path constant (default `src/superclaude/core/WORKER-CONTRACT.md`) that tests can monkeypatch. For each rule `./source.md` section 2.1 assigns to the file, it asserts the phrase recorded for that rule in `./artifacts/t1-rule-phrases.md`. Copy the phrases into the test as data; the test must not read the artifact. Each phrase carries the rule's meaning, not only its label:
- each WC identifier from Tasks 1 and 2 with its rule's recorded phrase;
- the four refusal conditions, the three exact reason texts and the case-3 `guard refused:` prefix;
- the never-as-worker list (all seven commands);
- the nested propagation rule;
- the WC-4 missing-directory error text;
- the WC-5 outcome mapping and its P0 override;
- the section 2.3 rule that dependents are created only after their inputs settle;
- the fan-in caps "maximum of 10 inputs" and "at least 2 inputs are admitted";
- the guard line, and that it comes before the first `Command:` line of the brief template.

If Task 3 added `plugins/superclaude/core/WORKER-CONTRACT.md`, the test also asserts that this copy is byte-identical to `src/superclaude/core/WORKER-CONTRACT.md`. Follow the pattern of `test_plugin_mirror_matches_src` in `tests/commands/test_workflow_command.py`.

It also asserts that no file in `src/superclaude/commands/` has an `## Unattended mode` section, because no command accepts `--unattended` after P0 (`./source.md` section 6 table, P0 row); later phases extend this list.

Acceptance criteria:
- `uv run pytest tests/skills/test_worker_contract.py -q` passes.
- A negative check makes the matching assertion fail for each rule removed from a `tmp_path` copy of `WORKER-CONTRACT.md` that the path constant is monkeypatched to. The negative check is run by a test in the same file or recorded in `./artifacts/t5-negative-check.txt`, and no scratch file is written under `src/superclaude/`.

## Task 6: Add the git and GitHub write-verb audit (AC-0.9)

Depends on: Task 5

Extend `tests/skills/test_worker_contract.py` with the AC-0.9 audit (`./source.md` section 7.3). It scans `src/superclaude/skills/`, `src/superclaude/commands/` and `src/superclaude/agents/` (scan roots held in a module-level constant that tests can monkeypatch) for these git and gh write verbs: `git add`, `git commit`, `git push`, `git merge`, `git worktree add`, `git worktree remove`, `git stash`, `git update-ref`, `gh pr`, and `gh api` posts. Match each verb as whole words, not followed by a word character or `-` (for example the lookahead `(?![\w-])`), so `git merge-base` is not counted as `git merge`. The test defines the regex as one module-level constant, and the hit unit is one matching line. A `gh api` post is a `gh api` call whose method is not GET. A call with `--method GET` or `-X GET` is a read even when it passes `-f` or `-F`.

Classify every hit into exactly one of five categories, each with a one-line reason:
- `wc9-allowed`: allowed by WC-9, for example `/sc:implement`'s private-index snapshot, its refs and its revert.
- `deferred:<phase>`: the command that owns the hit is converted, or its write turned off under `--unattended`, in the named phase of `./source.md` section 6.
- `never-worker`: the hit is in a command or skill on the never-as-worker list (`./source.md` section 4 and D3).
- `no-command`: no command converts this file; the reason says why.
- `read-only`: a read-only use or a false match, such as `gh pr view`, `gh pr list` or `gh pr checks`.

Name a phase only for `deferred:<phase>`. Key each entry by repo-relative path, verb and the stripped line text, never by line number. List every hit in the test's classification table; do not leave discovery to a later run. WC-9's "a worker writes no git state" covers only the hits classified here. Save the raw hit list with each hit's classification to `./artifacts/ac-0.9-hits.txt`. Then compare the full skills suite with the Task 1 baseline (AC-C3).

Acceptance criteria:
- `uv run pytest tests/skills/test_worker_contract.py -q` passes with the audit included.
- The audit fails when an unclassified write verb is added to a scratch skill file under a `tmp_path` scan root that the scan-root constant is monkeypatched to. This is run by a test in the same file or recorded in `./artifacts/t6-negative-check.txt`, and no scratch file is written under `src/superclaude/`.
- `./artifacts/ac-0.9-hits.txt` lists every hit with its classification.
- `uv run pytest tests/skills/ -q -rf` shows no test that passed in `./artifacts/ac-c3-baseline.txt` now failing, and the new tests pass (AC-C3); the per-test comparison is saved to `./artifacts/ac-c3-compare.md`.

## Phase 4: Read-only Orca checks and static close-out

## Task 7: Trace Orca's nesting-depth enforcement and read the depth setting (AC-0.7, AC-C6)

Read-only, no live probe. Start from the AC-0.7 starting points in `./source.md` section 7.3 (the block below the table): `grep -rlE 'nested_worker_depth_exceeded|NESTED_WORKER_DEPTH_EXCEEDED_CODE' /opt/Orca/resources/app.asar.unpacked/out/`. From there, trace which calls check nesting depth (`worker-start`, `dispatch`, `task-create`, low-level dispatch, `worktree create --agent`, `agent launch`) and what depth Orca gives a session the person opens (expected 0). Then run the AC-C6 check from `./source.md` section 7.1: `grep -ho '"nestedWorkerMaxDepth":[0-9]*' "${ORCA_RUNTIME_SOURCE_PROFILE_PATH:-$HOME/.config/orca}"/profiles/*/orca-data.json`.

Acceptance criteria:
- `./artifacts/ac-0.7-depth-trace.md` lists each call as checked, not checked or not found, and the depth of a person-opened session, each with a `path:line` in Orca's installed code. Any call not checked is recorded as covered only by WC-13 and 7.2 step 5.
- `./artifacts/ac-c6-depth-setting.txt` holds the AC-C6 output, and every printed line is `"nestedWorkerMaxDepth":1`. Any profile that prints nothing is recorded as using Orca's presumed default of 1.

## Task 8: Write the P0 static report and the commit list for the owner's approval

Depends on: Task 4, Task 6, Task 7

Re-run these checks at the end of the static plan and save each output as its evidence file:
- AC-0.1: the three commands of `./source.md` section 7.3 (the `KNOWN_CORE_FILES` assertion, the install check and `uv run pytest tests/skills/test_worker_contract.py -q`), saved to `./artifacts/ac-0.1.txt`;
- AC-0.2: the `cmp` and the routing-guide test run from Task 4, saved to `./artifacts/ac-0.2.txt`;
- AC-0.3: the deletions check, saved to `./artifacts/ac-0.3.txt`;
- AC-C1: the scan prints nothing, saved to `./artifacts/ac-c1.txt`;
- AC-C2: `make verify-sync` exits 0, saved to `./artifacts/ac-c2.txt`;
- AC-C3 (cite `./artifacts/ac-c3-compare.md` from Task 6, re-running it if any file changed since);
- AC-C5, recorded in `./artifacts/ac-c5.txt` as run with an empty edit set, because P0 edits no command file;
- AC-C6 (cite `./artifacts/ac-c6-depth-setting.txt`).

Run the AC-C4 check on the index and save its output. Write `./artifacts/p0-static-report.md`, then finish the task with `git add .dev/tasks`, so the report and every artifact are staged. The report has one PASS or FAIL line, with its evidence file, for each of AC-0.1, AC-0.2, AC-0.3, AC-0.7, AC-0.9, AC-C1, AC-C2, AC-C3, AC-C4, AC-C5 and AC-C6. It also lists every repo path this plan created or changed, outside `.claude/`, that the coordinator's owner-approved commit must include. That list covers at least `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/cli/install_core.py`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `tests/skills/test_worker_contract.py`, any plugin copy from Task 3, and `.dev/tasks`. It ends with the next steps of `./source.md` section 6 and section 7.2: the coordinator asks the owner to approve the commit, then `uv run superclaude install --force` from this checkout, and then the P0 live plan is written.

Acceptance criteria:
- `./artifacts/p0-static-report.md` has a PASS or FAIL line for each of the eleven checks listed above. Each line names its evidence file, and that file exists: `ac-0.1.txt`, `ac-0.2.txt`, `ac-0.3.txt`, `ac-0.7-depth-trace.md`, `ac-0.9-hits.txt`, `ac-c1.txt`, `ac-c2.txt`, `ac-c3-compare.md`, `ac-c4-index.txt`, `ac-c5.txt` and `ac-c6-depth-setting.txt`, all under `./artifacts/`. The report also has the commit path list.
- `./artifacts/ac-c4-index.txt` holds the output of `git diff --cached --name-only | grep '^\.claude/' | grep -v '^\.claude/settings\.json$'`, and the file is empty (AC-C4 on the index).
- `git diff --cached --name-only -- .dev/tasks` lists this package's files.
