---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-refactorDocsDeve-20261104-062532
version: "1"
priority: Medium
created_date: "2026-11-04"
---

# Make the developer guide teach Orca-ready commands, skills and agents

Source: ./source.md
Goal: `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` has one new section that explains how a command, skill or agent must be written so an Orca coordinator can run it as a worker, and every authoring touchpoint the source names (table of contents, introduction, command anatomy and archetypes, registration, agent patterns, contracts, skill checklist, workflow, testing, best practices, anti-patterns, templates, path reference, glossary) points to that section and to `~/.claude/WORKER-CONTRACT.md`, with no rule copied out of the contract and no claim the contract does not make.

## Constraints

- Only one delivery file changes: `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`. Do not edit `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, any command, skill, agent or test file.
- `src/superclaude/core/WORKER-CONTRACT.md` is the single authority. The guide summarizes each rule in one or two plain sentences, names its rule ID (for example WC-4) and points to `~/.claude/WORKER-CONTRACT.md`; it never reproduces the contract's full rule text, its brief template or its coordinator section. Every factual claim about worker behaviour must be traceable to a line of that file, or to the "Orca coordination" section at the end of `src/superclaude/core/HOW-WE-WORK.md`, or to `~/.claude/skills/orchestration/SKILL.md`.
- Rollout state must be stated as it is on disk: at P0 no command accepts `--unattended` or `--report-dir` (WORKER-CONTRACT.md section 5 slot rules and the "from P1" note above its flags table; `tests/skills/test_worker_contract.py` holds `UNATTENDED_COMMANDS = frozenset()`). The `## Unattended mode` section appears in a command only in the phase that converts its gates, from P1 on. Without `--unattended` every command behaves exactly as it does for a person today.
- New and edited text is plain English and contains no em dash and no en dash. Existing em dashes in untouched lines stay as they are.
- When the guide tells an agent or a primitive to read a file, it uses the installed path (`~/.claude/WORKER-CONTRACT.md`, `~/.claude/HOW-WE-WORK.md`, `~/.claude/skills/orchestration/SKILL.md`). A `src/superclaude/...` path appears only in maintainer instructions (edit this file, then run `make sync-dev`), as the guide's existing "Path rules for primitives" subsection allows.
- Unrelated stale content stays untouched (for example the stray `p` before the H1 on line 1, the `/sc:task-unified` examples, the 3.4 performance profiles). Report any such finding in the task's notes instead of fixing it.
- The guide's skill checklist in 5.10 uses checkbox lines; new checklist items there follow that existing format. This plan itself describes those items in prose.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included. Staging is not committing; commit only when the user asks.

## Phase 1: Add the Orca orchestration section

## Task 1: Write section 7.6 "Orca Orchestration: Commands as Workers"

Insert a new subsection `### 7.6 Orca Orchestration: Commands as Workers` in `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` after section 7.5 "Dynamic Context Injection" (its last paragraph ends "...adapt to the current repository state.") and before the `---` separator that precedes `## 8. Development Workflow`. Read `src/superclaude/core/WORKER-CONTRACT.md` sections 1 to 3, the "Orca coordination" section at the end of `src/superclaude/core/HOW-WE-WORK.md`, `~/.claude/skills/orchestration/SKILL.md`, and sections 3, 4, 5 and 6 of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` before writing. The subsection holds these parts, each as a short paragraph, bullet list or table:

- How the pieces fit: a coordinator is a session the person opened; it uses the `/orchestration` skill (`~/.claude/skills/orchestration/SKILL.md`, a discovery stub whose version-matched guide is served by the Orca binary) to plan, create one Orca Task per unit of work, start one worker per Task and read each worker's report. Each worker is a top-level Claude session that runs one `/sc:` command and reports with `worker_done`. Commands, skills and agents contain no Orca calls. Point to `~/.claude/WORKER-CONTRACT.md` as the authority and to the "Orca coordination" section of `~/.claude/HOW-WE-WORK.md`.
- Rollout state: the wording the Constraints require (P0: no command accepts `--unattended` or `--report-dir`; the section appears from P1 in the phase that converts a command's gates; standalone behaviour unchanged without the flag; no command, skill or agent may run an `orca` or `orca-ide` command or require Orca to be installed).
- Deciding whether a new command can be a worker: the never-as-worker list exactly as WORKER-CONTRACT.md section 1 states it (`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn`, `/sc:swarm-wizard`, plus `/sc:pr-submit` while decision D3 keeps it off workers), the reason class from the spec's section 4 (its purpose is orchestration, a conversation with a person, or an outward action the user must authorize), and that such commands get no `--unattended` mode. Say that adding a command to that list is a maintainer edit of `src/superclaude/core/WORKER-CONTRACT.md` and of `NEVER_AS_WORKER` in `tests/skills/test_worker_contract.py`, done in its own reviewed change, never as part of writing the command.
- What a worker-capable command must do under `--unattended`, one bullet per rule with its ID: the flag parse rule (a standalone token outside quoted arguments only); the person-mode flag refusal (`--interactive`, `--format interactive`, `--mode socratic`, `--watch`, `--monitor 1`); WC-2 (no `AskUserQuestion`, no chat question or `[yes / no]` offer, no STOP AND WAIT; each gate resolves by a documented default, a caller flag, or blocked with `blocked_question`); WC-4 (exactly one report directory, from the command's own directory-valued `--output`/`--output-dir` or `--report-dir`; `<report-dir>/return-contract.yaml` written on every outcome including early stops; the seven worker fields; the exact error when there is no report directory or both); WC-8 (no `worker-start`, `dispatch` or `task-create`; Agent-tool fan-out inside the command is allowed and stays as it is); WC-9 (every outward default off and the command's own commit step off; skills that stage `.dev/tasks` themselves defer that under `--unattended`); WC-10 (split any single blocking Bash call longer than 4 minutes); WC-11 (default output paths carry a timestamp or caller slug; no single-owner shared file written under `--unattended`); WC-7 (the command runs at the top level of the worker session; subagents never send lifecycle messages); the nested propagation rule (pass `--unattended` and `<caller report-dir>/nested/<command>-<n>/` to a nested command that accepts it, list the nested contract in `artifacts`, otherwise keep the step gate-free or skip it and record the skip).
- The `## Unattended mode` section a converted command carries: it lists only that command's own gate resolutions, its report file and report directory flag, its nested invocations and its resume input if any, and points to `~/.claude/WORKER-CONTRACT.md` instead of restating shared rules. State that the brief guard decides from the presence of this section in every copy of the command file the worker sees (the project `.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md`), so a stale copy makes the worker refuse.
- How skills and agents under the command inherit the rules: the skill protocol carries the branch for each gate (the command's section names the resolution, the skill applies it); a skill keeps its own `status` field and writes `worker_status` beside it per WC-4; agents launched with the Agent tool never call Orca, never send heartbeat, ask, check or `worker_done`, and never ask the person.

Acceptance criteria:
- `grep -n '^### 7.6 Orca Orchestration: Commands as Workers' docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` prints one line, and that line comes after the `### 7.5 Dynamic Context Injection` heading and before `## 8. Development Workflow`.
- The new subsection names WC-2, WC-4, WC-7, WC-8, WC-9, WC-10 and WC-11, the flag parse rule, the person-mode refusal, the nested propagation rule, all seven worker field names (`worker_contract_version`, `worker_status`, `command`, `report_path`, `artifacts`, `blocked_question`, `reason`) and every command on the never-as-worker list; each name matches its spelling in `src/superclaude/core/WORKER-CONTRACT.md`.
- The subsection states that at P0 no command accepts `--unattended` or `--report-dir`, and points to `~/.claude/WORKER-CONTRACT.md`, `~/.claude/HOW-WE-WORK.md` and `~/.claude/skills/orchestration/SKILL.md` by those installed paths.
- The subsection does not contain the contract's guard line text, brief template or section 4 coordinator rules verbatim: `grep -c 'Guard: before running anything' docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` prints 0.
- `grep -nP '[\x{2013}\x{2014}]'` over the new subsection's line range prints nothing; the range and the grep output are saved to `./artifacts/t1-dash-check.txt`.

## Phase 2: Wire the section into the reference chapters

## Task 2: Update the header, table of contents and introduction

Depends on: Task 1

In `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`: change the header's `**Last Updated**` date to 2026-11-04; under item 7 of `## Table of Contents` add an indented entry linking `[7.6 Orca Orchestration: Commands as Workers](#76-orca-orchestration-commands-as-workers)`; in `### Installation Locations` add a core-files line under the `~/.claude/` block naming `WORKER-CONTRACT.md` (and `HOW-WE-WORK.md`) as installed core docs; in `### Context Loading Sequence` item 1 add one sentence that `~/.claude/WORKER-CONTRACT.md` is also installed beside `CLAUDE.md`, is read on demand by a coordinator or by a worker applying the brief guard, and is never `@`-imported. Confirm the never-imported claim by reading `src/superclaude/core/CLAUDE.md` (its only import is `@BASH_INSPECTION_POLICY.md`) and confirm installation by reading `KNOWN_CORE_FILES` in `src/superclaude/cli/install_core.py`.

Acceptance criteria:
- The table-of-contents link target matches the GitHub anchor of the Task 1 heading (`#76-orca-orchestration-commands-as-workers`).
- `grep -n 'WORKER-CONTRACT.md' docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` shows hits inside both `### Installation Locations` and `### Context Loading Sequence`.
- `grep -n '"WORKER-CONTRACT.md"' src/superclaude/cli/install_core.py` prints a hit and `grep -n '^@' src/superclaude/core/CLAUDE.md` prints only the `@BASH_INSPECTION_POLICY.md` line; both outputs are saved to `./artifacts/t2-core-file-evidence.txt`.
- The header reads `**Last Updated**: 2026-11-04`.

## Task 3: Add worker guidance to the commands chapter

Depends on: Task 1

In section 3 of `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`:

- `### 3.1 Anatomy of a Command File`: add a row to the Markdown body table for `## Unattended mode` (purpose: this command's gate resolutions, report file and nested invocations under `--unattended`, pointing to `~/.claude/WORKER-CONTRACT.md`; required: only when the command accepts `--unattended`, which no command does at P0), and one sentence after the table that `--unattended` and `--report-dir` are listed in `## Options` only by a command that accepts them, with a link to section 7.6.
- `### 3.2 Command Archetypes`: add one "Worker fit" bullet to each archetype. Analysis Pipeline: a natural worker, because it reads and writes a report the contract can point at. Meta-Orchestrator: `/sc:spawn` is on the never-as-worker list because its decomposition is the coordinator's job; a new meta-orchestrator may fan out with the Agent tool but never with Orca (WC-8). Unified Executor: outward actions and its own commit step are off under `--unattended` (WC-9); `/sc:implement` is converted only in P4.
- `### 3.6 Registering a New Command`: add one paragraph saying that a worker-capable command needs no extra registration, because the coordinator checks the command file for `## Unattended mode` instead of a list (quote the rule from the "Orca coordination" section of `src/superclaude/core/HOW-WE-WORK.md`), and that a coordinator-only command is added to the never-as-worker list only by the maintainer edit section 7.6 describes.

Acceptance criteria:
- The 3.1 body table has a `## Unattended mode` row and the text after it links to `#76-orca-orchestration-commands-as-workers`.
- Each of the three archetype headings in 3.2 is followed, within its own block, by a bullet starting `**Worker fit**`.
- The 3.6 paragraph says the coordinator checks the command file rather than a list, matching the "`--unattended` only where the command supports it" bullet of the "Orca coordination" section of `src/superclaude/core/HOW-WE-WORK.md`.

## Task 4: Add worker guidance to the agents chapter

Depends on: Task 1

In `### 4.2 Agent Patterns` of `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, add a short paragraph at the start of the subsection that separates the two meanings of "worker": an agent pattern such as Constrained Worker is an Agent-tool subagent inside one session, while an Orca worker is a whole top-level session the coordinator starts (section 7.6). Then add one sentence to Pattern 3 "Process Orchestrator" that an orchestrating agent coordinates subagents inside its session only and never creates Orca Tasks or workers (WC-8, WC-13), and one bullet after the four patterns stating that under `--unattended` no agent sends lifecycle messages (heartbeat, ask, check, `worker_done`), calls Orca, or asks the person; only the top-level worker session does (WC-7).

Acceptance criteria:
- 4.2 contains the distinction between an Agent-tool subagent and an Orca worker session, with a link to `#76-orca-orchestration-commands-as-workers`.
- The Pattern 3 block names WC-8, and the closing bullet names WC-7 and lists heartbeat, ask, check and `worker_done`.
- Every rule cited matches WORKER-CONTRACT.md section 2 and section 3 wording (WC-7 "Lifecycle messages (heartbeat, ask, check, `worker_done`) are sent only by that top-level session, never by a subagent").

## Task 5: Add the worker contract to the skills chapter

Depends on: Task 1

In section 5 of `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`:

- `### 5.9 Input and Output Contracts`: after the "Output / Return Contracts" example, add a "Worker contract (under `--unattended`)" part that explains, without copying WC-4 whole: the worker contract is `<report-dir>/return-contract.yaml`; its status field is `worker_status` (`succeeded`, `partial`, `failed`, `blocked`), not `status`, because existing skills already use `status` with other values; a skill that writes its own `return-contract.yaml` in the report directory keeps every field and adds the worker fields beside them; a skill whose own contract lives elsewhere leaves it unchanged and the worker contract lists it in `artifacts`; the status mapping (`success` to `succeeded`, `partial` to `partial`, `failed` and `stopped-precondition` to `failed`). Point to WC-4 in `~/.claude/WORKER-CONTRACT.md`.
- `### 5.10 Skill-Authoring Checklist`: add checklist items, in the file's existing checkbox format, for: deciding whether the command is worker-capable or belongs on the never-as-worker list; for a worker-capable command, every person-blocking step (each `AskUserQuestion`, chat question, `[yes / no]` offer, STOP AND WAIT) has an unattended resolution listed in the command's `## Unattended mode` section; the worker contract is written on every outcome; no Orca command anywhere in the skill, its refs or scripts; outward defaults and the skill's own commit or `.dev/tasks` staging step are off under `--unattended`; no single Bash wait longer than 4 minutes; default write paths are parallel-safe; nested `/sc:` invocations follow the nested propagation rule. Each item links to section 7.6.

Acceptance criteria:
- 5.9 contains the words `worker_status` and `stopped-precondition` and names the four `worker_status` values exactly as WORKER-CONTRACT.md WC-4 lists them.
- 5.10 has at least eight new checklist items covering each topic listed above, each in the same checkbox format as the existing items, and none of them says any command accepts `--unattended` today.
- Every status mapping stated in 5.9 matches the "Mapping from a command's own status" bullet of WC-4.

## Phase 3: Wire the section into the workflow and practice chapters

## Task 6: Add Orca readiness to the development workflow and testing

Depends on: Task 1

In section 8 of `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`:

- `### 8.3 Creating a New Component: Full Workflow`: inside the bash block, add a comment step between "2. Write the component" and "3. Sync to .claude/" that says: decide worker eligibility (section 7.6); if the command will accept `--unattended`, write its `## Unattended mode` section. Keep the block's existing comment style.
- `### 8.4 Testing Components`: add an "Orca readiness checks" list: run `uv run pytest tests/skills/test_worker_contract.py`; its write-verb audit (`test_every_write_verb_hit_is_classified`) fails on any new git or gh write verb in a skill, command or agent until the line gets an entry in `WRITE_VERB_CLASSIFICATION` with a category and reason; a command given an `## Unattended mode` section must also be added to `UNATTENDED_COMMANDS`, or `test_no_command_has_unattended_mode_section_after_p0` fails; run the command once without `--unattended` and confirm its prompts, outputs and outward defaults are unchanged. Read `tests/skills/test_worker_contract.py` to confirm these names before writing them.

Acceptance criteria:
- The 8.3 bash block contains a comment naming `## Unattended mode` and section 7.6, placed before the `make sync-dev` step.
- 8.4 names `tests/skills/test_worker_contract.py`, `WRITE_VERB_CLASSIFICATION`, `UNATTENDED_COMMANDS`, `test_every_write_verb_hit_is_classified` and `test_no_command_has_unattended_mode_section_after_p0`, and `grep -n` for each of those four identifiers in `tests/skills/test_worker_contract.py` prints a hit; that output is saved to `./artifacts/t6-test-identifiers.txt`.
- 8.4 includes the standalone check that behaviour without `--unattended` is unchanged.

## Task 7: Add Orca rules to best practices and anti-patterns

Depends on: Task 1

In section 9 of `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`:

- `### 9.1 Command Design`: add Do bullets (decide worker eligibility up front; when the command accepts `--unattended`, list every gate's resolution and the report file in `## Unattended mode` and point to `~/.claude/WORKER-CONTRACT.md`) and Do not bullets (call Orca from a command; copy shared contract rules into the command; leave an outward default on under `--unattended`).
- `### 9.3 Skill Design`: add Do bullets (write the worker contract on every outcome; keep the skill's own `status` and add `worker_status` beside it; split long Bash waits) and Do not bullets (call `AskUserQuestion` or end on a question under `--unattended`; write a fixed shared output path or a single-owner shared file under `--unattended`).
- `### 9.7 Anti-Patterns`: add rows, each with Problem and Solution columns, for: a person-blocking step under `--unattended` (worker stalls; resolve as default, flag or blocked, WC-2); an Orca call inside a command or skill (fails without Orca and competes with the coordinator; let the coordinator split the work, WC-8); a contract written only on success (coordinator cannot tell a crash from a stop; write it on every outcome, WC-4); reusing `status` for the worker outcome (clashes with existing values; use `worker_status`, WC-4); a single Bash wait longer than 4 minutes (no heartbeats; split the wait, WC-10); a fixed shared output path (two workers overwrite each other; timestamp or caller slug plus own report directory, WC-11); copying the contract into a command (rules drift; point to `~/.claude/WORKER-CONTRACT.md`).

Acceptance criteria:
- 9.1 and 9.3 each gain at least two Do and two Do not bullets on the topics above, each naming its rule ID where one exists.
- 9.7 gains seven rows, one per anti-pattern listed above, each citing its rule ID or the installed contract path.
- `grep -nP '[\x{2013}\x{2014}]'` over the lines this task added prints nothing; the line range and output are saved to `./artifacts/t7-dash-check.txt`.

## Phase 4: Update the templates and reference appendices

## Task 8: Add unattended slots to the skill and command templates

Depends on: Task 1

In `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`:

- `## Appendix A: SKILL.md Skeleton Template`: inside the template, add a protocol note under `## Protocol` that each person-blocking step applies the resolution its command's `## Unattended mode` section names when the run has `--unattended`, and add a comment line under `## Return Contract` that under `--unattended` the worker fields of WC-4 are added beside `status` in `<report-dir>/return-contract.yaml`.
- `## Appendix B: Command Template`: inside the template, add optional `--unattended` and `--report-dir` rows to the Options table, each marked "only if this command accepts unattended mode", and an optional `## Unattended mode` section before `## Boundaries` with slots for each gate and its resolution (default, flag, or blocked), the report file, the report directory flag, nested invocations, resume input, and the pointer line to `~/.claude/WORKER-CONTRACT.md`. Mark the section as optional, and delete-if-unused, with the same angle-bracket placeholder style the template already uses.

Acceptance criteria:
- Appendix B's template contains `## Unattended mode` with slots for gates, report file, report directory flag, nested invocations and resume input, and a line naming `~/.claude/WORKER-CONTRACT.md`.
- Appendix A's template mentions `--unattended` under `## Protocol` and `worker_status` under `## Return Contract`.
- The fenced blocks of both appendices still open and close in pairs: the count of lines starting with three backticks between the `## Appendix A` and `## Appendix C` headings is even, and that count is saved to `./artifacts/t8-fence-count.txt`.

## Task 9: Update the path reference and glossary

Depends on: Task 1

In `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`:

- `## Appendix D: File Path Reference`: add a row for the worker contract (`src/superclaude/core/WORKER-CONTRACT.md` installed to `~/.claude/WORKER-CONTRACT.md`) and a row for the Orca-readiness test (`tests/skills/test_worker_contract.py`, not installed). The existing "Core files" row reads `src/superclaude/*.md`, which contradicts the new row; correct it to `src/superclaude/core/*.md` after confirming the installer's source directory in `src/superclaude/cli/install_core.py`, because the two rows would otherwise disagree.
- `## Appendix E: Glossary`: add rows, in alphabetical order with the existing rows, for Brief guard, Coordinator, Lifecycle messages, Nested propagation rule, Never-as-worker list, Report directory, Unattended mode, Worker (Orca), Worker contract and `worker_status`, each defined in one sentence that matches WORKER-CONTRACT.md section 1 or the rule it names.

Acceptance criteria:
- Appendix D has a `WORKER-CONTRACT.md` row with both the source and installed paths, a `test_worker_contract.py` row, and a "Core files" row reading `src/superclaude/core/*.md`; the installer evidence for that directory is saved to `./artifacts/t9-core-dir-evidence.txt`.
- Appendix E's table has the ten new terms, and its rows remain in alphabetical order.
- `uv run pytest tests/docs tests/skills/test_worker_contract.py tests/core -q` passes, with its output saved to `./artifacts/t9-pytest.txt`, and `git diff --name-only -- . ':!.dev'` lists only `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` plus the pre-existing `docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md` change, saved to `./artifacts/t9-changed-files.txt`.
