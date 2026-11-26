---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-devGuideRefactor-20261104-135403
version: "1"
priority: Medium
created_date: "2026-11-04"
---

# Make the developer guide teach Orca-ready commands, skills and agents (round 3 plan)

Source: ./source.md
Goal: `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` has one new subsection, 7.6, that explains how a command, skill or agent must be written so an Orca coordinator can run it as a worker, and every touchpoint the source lists points to 7.6 under the source's pointer rule. Every worker claim matches `src/superclaude/core/WORKER-CONTRACT.md`, every rollout or rationale claim matches the planning spec and says so, and each list, number and exact string the source names is written out once, in 7.6.

## Constraints

- Only one delivery file changes: `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`. Do not edit `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, or any command, skill, agent or test file, and add no new test file. Scripts and evidence go under this package's `./artifacts/`.
- Allowed sources. Worker behaviour: `src/superclaude/core/WORKER-CONTRACT.md` (the authority), the "Orca coordination" section at the end of `src/superclaude/core/HOW-WE-WORK.md`, and `~/.claude/skills/orchestration/SKILL.md` (a discovery stub). Rollout phases (section 6), coordinator-only reasons (section 4) and SA-1 to SA-6 (section 5): `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, and every sentence taken from it carries a label such as "per the rollout plan". Test behaviour: `tests/skills/test_worker_contract.py`. Per-command facts in 3.2: `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md` or the contract's ready table.
- The guide summarizes contract rules in its own words and points to `~/.claude/WORKER-CONTRACT.md`. It never reproduces the contract's guard line, brief template, coordinator section or the WC-4 error string.
- One home: the never-as-worker list, the person-mode flags, the WC-10 wait limit in minutes, the `worker_status` values with the full WC-4 status mapping, and the description of the WC-4 report-directory error are written out only in 7.6; elsewhere a touchpoint refers to them by rule ID or "section 7.6".
- Pointer rule (source "Pointer rule for touchpoints"): in prose, tables and list items outside code fences, a touchpoint that refers to a 7.6 topic names its rule ID or "section 7.6" and links to `#76-orca-orchestration-commands-as-workers`; this covers the Context Loading sentence, 3.1, 3.2, 3.6, 4.2, 5.9, 5.10, 8.4, 9.1, 9.3, 9.7 and the Appendix E rows. Inside a code fence (the Installation Locations block, the 8.3 bash block, the Appendix A and B templates) it names the rule ID and "section 7.6" as plain text. The table-of-contents entry carries the link only. Appendix A's `## Return Contract` note points only to section 5.9 and names no rule. Appendix D rows carry paths only.
- WC-4 two-case rule. In prose that explains the worker contract file (7.6 and 5.9) both cases are stated in full: a command that already writes `return-contract.yaml` in the report directory itself keeps every existing field, including its own `status`, and adds the worker fields beside them; a command whose own contract lives elsewhere leaves that file unchanged, and the worker contract at `<report-dir>/return-contract.yaml` lists it in `artifacts`. Elsewhere (5.10, 9.3, 9.7, the glossary) a line naming "the WC-4 two-case rule" with a link to 7.6 or 5.9 is enough. No line states the first case without its condition.
- Report directory flag. Wherever the guide lists or defines `--report-dir` (7.6, 3.1, Appendix B, the glossary) it says: a command uses its own directory-valued `--output` or `--output-dir` as the report directory; `--report-dir` is for a command without such a flag, or for a brief that does not pass that flag; passing both, or neither, is refused before any work (WC-4).
- Rule anchors. WC-8 is cited only for a command calling `worker-start`, `dispatch` or `task-create`. "Commands contain no Orca calls" is cited to the contract's opening. "No `orca` or `orca-ide` command anywhere, and no need for Orca to be installed" is cited as "per the rollout plan, SA-2". Agent rules cite WC-7 and WC-8, never WC-13. WC-7 is a worker-session duty.
- Nobody is asked. No new sentence says or implies that a worker session, a command or an agent asks the person or the user under `--unattended`. Under `--unattended` nothing asks the person (WC-2); only the worker session may put a blocked question to the coordinator, and only when its brief allows it (WC-3). Every added line containing "the person", "the user" or "a person" states that nothing asks them; other new text uses other words (for example "someone" or "a human").
- Skills and agents under a command: the guide presents as its own authoring convention, not as a contract rule, that they follow the command's `## Unattended mode` section (WC-2) and, for a skill's own contract file, the WC-4 two-case rule.
- Every mention of the brief guard says it applies from P1.
- Rollout state as on disk: at P0 no command accepts `--unattended` or `--report-dir`; `tests/skills/test_worker_contract.py` holds `UNATTENDED_COMMANDS: frozenset = frozenset()`. Without `--unattended` every command behaves as it does today.
- New and edited text is plain English and contains no em dash and no en dash, including new checklist items (no dash after the bold label). Existing ones in untouched lines stay.
- When the guide tells an agent or primitive to read a file, it uses the installed path (`~/.claude/WORKER-CONTRACT.md`, `~/.claude/HOW-WE-WORK.md`, `~/.claude/skills/orchestration/SKILL.md`). A `src/superclaude/...` path appears only where the guide describes this repository's own source layout or a maintainer step (the Installation Locations block, 7.6's maintainer edit, 8.4's audit scope, the Appendix D path table), as the guide's "Path rules for primitives" subsection allows.
- Unrelated stale content stays untouched (the stray `p` before the H1 on line 1, the `/sc:task-unified` examples, the 3.4 performance profiles, the nested fences outside Appendix B). Record such findings in the task's evidence notes.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included. Staging is not committing; commit only when the user asks.

## Phase 1: Add the Orca orchestration subsection

## Task 1: Write subsection 7.6 "Orca Orchestration: Commands as Workers"

Insert `### 7.6 Orca Orchestration: Commands as Workers` in `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` after section 7.5 "Dynamic Context Injection" (its last paragraph ends "...adapt to the current repository state.") and before the `---` that precedes `## 8. Development Workflow`. Before writing, read `src/superclaude/core/WORKER-CONTRACT.md` in full, the "Orca coordination" section at the end of `src/superclaude/core/HOW-WE-WORK.md`, `~/.claude/skills/orchestration/SKILL.md`, and sections 4, 5 and 6 of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. The subsection holds these parts:

- How the pieces fit: a coordinator is a session someone opened by hand, never one Orca started as a worker; it plans the work, creates one Orca Task per unit of work, starts one worker per Task and reads each worker's report (`WORKER-CONTRACT.md` opening and section 4). A worker is a top-level Claude session that runs one `/sc:` command and reports with `worker_done`. Commands contain no Orca calls (the contract's opening). The `/orchestration` skill (`~/.claude/skills/orchestration/SKILL.md`) is a discovery stub that loads Orca's version-matched guide from the Orca binary; the IronClaude coordinator rules are in section 4 of `~/.claude/WORKER-CONTRACT.md`. Point also to the "Orca coordination" section of `~/.claude/HOW-WE-WORK.md`.
- Rollout state: at P0 no command accepts `--unattended` or `--report-dir`; per the rollout plan, a command gains `--unattended` and its `## Unattended mode` section in the phase that converts its gates, from P1. Per the rollout plan (SA-1), without the flag every command behaves as it does today, and per the rollout plan (SA-2) no command, skill or agent runs an `orca` or `orca-ide` command or needs Orca installed.
- Deciding whether a new command can be a worker: the never-as-worker list as `WORKER-CONTRACT.md` section 1 states it (`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn`, `/sc:swarm-wizard`, plus `/sc:pr-submit` while decision D3 keeps it off workers); per the rollout plan, these are commands whose purpose is orchestration, a conversation with a human, or an outward action that must be authorized; they get no `--unattended` mode. Adding a command to the list is a maintainer edit of `src/superclaude/core/WORKER-CONTRACT.md` and of `NEVER_AS_WORKER` in `tests/skills/test_worker_contract.py`.
- What a command does under `--unattended`, one bullet per rule: the flag parse rule (a standalone argument token outside any quoted argument); the person-mode refusal with its flag list (`--interactive`, `--format interactive`, `--mode socratic`, `--watch`, `--monitor 1`); WC-2 (no `AskUserQuestion`, no chat question or `[yes / no]` offer, no STOP AND WAIT; each gate resolves by a documented default, a caller flag, or blocked with the question in `blocked_question`); WC-4 report directory (the condition from the Constraints "Report directory flag" bullet, with the WC-4 error described here and not quoted); WC-4 contract (`<report-dir>/return-contract.yaml` written on every outcome, including stops before any other output; fields `worker_contract_version`, `worker_status`, `command`, `report_path`, `artifacts`, plus `blocked_question` when blocked and `reason` when failed, and for `/sc:implement` also when blocked; the `worker_status` values `succeeded`, `partial`, `failed`, `blocked`; both two-case-rule cases in full; the five-case status mapping: `success` to `succeeded`, `partial` to `partial`, `failed` to `failed`, `stopped-precondition` to `failed` with the precondition in `reason`, and the flag-STOP `blocked` of impact and graph to `failed` with the STOP in `reason`); WC-8 (a command never calls `worker-start`, `dispatch` or `task-create`); WC-9 (every outward default and the command's own commit step are off under `--unattended`, and the skills that stage `.dev/tasks` themselves defer that); WC-10 (a single blocking Bash call lasts at most 4 minutes; a longer wait is split so the session can heartbeat between the parts); WC-11 (default output paths carry a timestamp or the caller's slug; single-owner shared files are not written under `--unattended`); the nested propagation rule (pass `--unattended` and `<caller report-dir>/nested/<command>-<n>/` to a nested command that accepts the flag and list its contract in `artifacts`; otherwise keep that step gate-free or skip it and record the skip).
- The worker session, not the command (WC-7): the worker runs the command at its own top level, never inside a subagent; only that session sends lifecycle messages (heartbeat, ask, check, `worker_done`); a command's own Agent-tool fan-out stays as it is (WC-7).
- The `## Unattended mode` section a converted command carries: only that command's gate resolutions, its report file, its report directory flag, its nested invocations and its resume input if any, plus a pointer to `~/.claude/WORKER-CONTRACT.md`; shared rules are not restated. From P1 the worker's brief guard checks every copy of the command file it sees (the project `.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md`) for this section, so copies that disagree make the worker refuse.
- How skills and agents under a command fit, as separate sentences: as this guide's authoring convention, skills and agents that run under a command follow its `## Unattended mode` section (WC-2), and a skill follows the WC-4 two-case rule for its own contract file; only the top-level worker session sends lifecycle messages, never a subagent (WC-7); no agent calls `worker-start`, `dispatch` or `task-create`, because the command it runs under never does (WC-8); under `--unattended` nothing asks the person, and only the worker session may put a blocked question to the coordinator, when its brief allows it (WC-2, WC-3).

Acceptance criteria:
- `grep -n '^### 7.6 Orca Orchestration: Commands as Workers' docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` prints one line, after `### 7.5 Dynamic Context Injection` and before `## 8. Development Workflow`.
- The subsection names WC-2, WC-3, WC-4, WC-7, WC-8, WC-9, WC-10 and WC-11, the flag parse rule, the person-mode refusal and the nested propagation rule, lists the seven worker field names with `blocked_question` and `reason` described as conditional, gives all five status-mapping cases, and states both two-case-rule cases; each name and value matches its spelling in `src/superclaude/core/WORKER-CONTRACT.md`.
- The `--report-dir` text carries the own-flag case, the brief-does-not-pass-it case and the both-or-neither refusal.
- No line of the subsection cites WC-13, and WC-8 appears only beside `worker-start`, `dispatch` and `task-create`.
- Every line of the subsection containing "the person", "the user" or "a person" states that nothing asks them; the matching lines, found with `grep -nE 'the person|the user|a person'` over the subsection's line range, are saved to `./artifacts/t1-ask-check.txt` with a one-line verdict per line.
- The brief guard mention includes "from P1"; every spec-derived sentence carries a "per the rollout plan" label; the subsection points to `~/.claude/WORKER-CONTRACT.md`, `~/.claude/HOW-WE-WORK.md` and `~/.claude/skills/orchestration/SKILL.md` by those paths.
- `grep -c 'Guard: before running anything' docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` prints 0, and the subsection does not contain the text `unattended mode needs exactly one report directory`.

## Phase 2: Point the reference chapters at 7.6

## Task 2: Update the header, table of contents and introduction

Depends on: Task 1

In `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`: change the header's `**Last Updated**` date to 2026-11-04; under item 7 of `## Table of Contents` add an indented entry `[7.6 Orca Orchestration: Commands as Workers](#76-orca-orchestration-commands-as-workers)` (link only); in the `### Installation Locations` code block add a `core/` line to the `src/superclaude/` block (core framework files, including `CLAUDE.md`, `HOW-WE-WORK.md` and `WORKER-CONTRACT.md`) and a matching core-files line to the `~/.claude/` block that names `WORKER-CONTRACT.md` and "section 7.6" as plain text; in `### Context Loading Sequence` item 1 add one sentence that `~/.claude/WORKER-CONTRACT.md` is installed beside `CLAUDE.md`, is read on demand by a coordinator and, from P1, by a worker applying the brief guard, and is never `@`-imported, with a link to `#76-orca-orchestration-commands-as-workers`. Confirm the facts first by reading `KNOWN_CORE_FILES` and `_get_core_source` in `src/superclaude/cli/install_core.py` and the imports in `src/superclaude/core/CLAUDE.md`.

Acceptance criteria:
- The table-of-contents link target is `#76-orca-orchestration-commands-as-workers`.
- `### Installation Locations` shows a `core/` entry under `src/superclaude/` and a core-files entry under `~/.claude/` naming `WORKER-CONTRACT.md` and "section 7.6".
- The Context Loading sentence says "from P1" for the brief guard, states the file is never `@`-imported, and links to `#76-orca-orchestration-commands-as-workers`.
- The outputs of `grep -nE '"(HOW-WE-WORK|WORKER-CONTRACT)\.md"' src/superclaude/cli/install_core.py`, `grep -n 'package_root / "core"' src/superclaude/cli/install_core.py` and `grep -n '^@' src/superclaude/core/CLAUDE.md` are saved to `./artifacts/t2-core-evidence.txt`; the first shows both names and the last prints only the `@BASH_INSPECTION_POLICY.md` line.
- The header reads `**Last Updated**: 2026-11-04`.

## Task 3: Add worker pointers to the commands chapter

Depends on: Task 1

In section 3 of `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, after reading `.dev/orca-command-refactor/inventory/commands-a.md`, `.dev/orca-command-refactor/inventory/commands-b.md`, section 5 of `src/superclaude/core/WORKER-CONTRACT.md` (the ready-with-brief-constraints table) and `tests/skills/test_worker_contract.py` (`UNATTENDED_COMMANDS` and `_check_no_unattended_sections`):

- `### 3.1 Anatomy of a Command File`: add a body-table row for `## Unattended mode` (purpose: this command's gate resolutions, report file, report directory flag and nested invocations under `--unattended`; required: only when the command accepts `--unattended`, which no command does at P0), and one sentence after the table: a command that accepts `--unattended` lists it in `## Options`; it takes `--report-dir` when it has no directory-valued `--output` or `--output-dir` of its own, or when the brief does not pass that flag; passing both or neither is refused before any work (WC-4); link to `#76-orca-orchestration-commands-as-workers`.
- `### 3.2 Command Archetypes`: add one bullet starting `**Worker fit**` to each archetype, stating only sourced facts, naming rule IDs and linking to 7.6, never repeating a list from 7.6. Analysis Pipeline: `/sc:cleanup-audit` is in the contract's ready-with-brief-constraints table; `/sc:explain` has a person-mode flag that is refused under `--unattended` (section 7.6); a command gets `--unattended` only after each of its gates has an unattended resolution (WC-2). Meta-Orchestrator: `/sc:spawn` is a never-as-worker command (section 7.6); `/sc:adversarial` is in the ready table; such a command may fan out with the Agent tool (WC-7) but never calls `worker-start`, `dispatch` or `task-create` (WC-8). Unified Executor: outward actions and the command's own commit step are off under `--unattended` (WC-9); per the rollout plan, `/sc:implement` is converted in P4. No bullet calls any archetype a natural or default worker.
- `### 3.6 Registering a New Command`: add one paragraph, in the guide's own words: a command that accepts `--unattended` needs no entry in any worker list, because the coordinator decides from whether the command file has an `## Unattended mode` section (the "Orca coordination" section of `~/.claude/HOW-WE-WORK.md`); the one registration step it does need is the maintainer adding its name to `UNATTENDED_COMMANDS` in `tests/skills/test_worker_contract.py`, as 8.4 describes; the never-as-worker list changes only through the maintainer edit section 7.6 describes; link to `#76-orca-orchestration-commands-as-workers`.

Acceptance criteria:
- The 3.1 body table has a `## Unattended mode` row; the sentence after the table carries the own-flag case, the brief-does-not-pass-it case and the both-or-neither refusal, cites WC-4 and links to `#76-orca-orchestration-commands-as-workers`.
- Each of the three archetype blocks in 3.2 has one bullet starting `**Worker fit**` with a rule ID and the 7.6 link; the Meta-Orchestrator bullet names both `/sc:spawn` and `/sc:adversarial`; `grep -n 'natural worker' docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` prints nothing.
- The ready-table membership of `/sc:cleanup-audit` and `/sc:adversarial` is confirmed by grep in section 5 of `src/superclaude/core/WORKER-CONTRACT.md`, saved to `./artifacts/t3-ready-table.txt`.
- The 3.6 paragraph names `UNATTENDED_COMMANDS`, does not contain "no extra registration", contains no sentence copied word for word from the "Orca coordination" section of `src/superclaude/core/HOW-WE-WORK.md`, and does not contradict the 8.4 text Task 6 writes.

## Task 4: Add the worker-session rules to the agents chapter

Depends on: Task 1

In `### 4.2 Agent Patterns` of `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`: add a short opening paragraph that separates the two meanings of "worker" (a pattern such as Constrained Worker is an Agent-tool subagent inside one session; an Orca worker is a whole top-level session the coordinator starts; link to `#76-orca-orchestration-commands-as-workers`). Add one sentence to Pattern 3 "Process Orchestrator": an orchestrating agent coordinates subagents inside its own session only; it never calls `worker-start`, `dispatch` or `task-create`, because the command it runs under never does (WC-8). After the four patterns add a bullet list with three separate items: only the top-level worker session sends lifecycle messages (heartbeat, ask, check, `worker_done`), never a subagent (WC-7); no agent calls `worker-start`, `dispatch` or `task-create`, because the command never does (WC-8); under `--unattended` nothing asks the person, so an agent resolves a gate the way its command's `## Unattended mode` section says (this guide's convention), and only the worker session may put a blocked question to the coordinator when its brief allows it (WC-2, WC-3).

Acceptance criteria:
- 4.2 contains the two-meanings paragraph with a link to `#76-orca-orchestration-commands-as-workers`.
- The Pattern 3 sentence cites WC-8 beside the three dispatch verbs; `grep -n 'WC-13' docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` prints nothing.
- The closing list has three separate items citing WC-7, WC-8, and WC-2 with WC-3; the WC-7 item lists heartbeat, ask, check and `worker_done`.
- Every added 4.2 line containing "the person", "the user" or "a person" states that nothing asks them; the matching lines with a one-line verdict each are saved to `./artifacts/t4-ask-check.txt`.

## Task 5: Add the worker contract to the skills chapter

Depends on: Task 1

In section 5 of `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`:

- `### 5.9 Input and Output Contracts`: after the "Output / Return Contracts" example, add a "Worker contract (under `--unattended`)" part: the worker contract file is `<report-dir>/return-contract.yaml`; its status field is `worker_status`, not `status`, because existing skills already use `status` with other values (WC-4); then both two-case-rule cases in full; then one example marked as an example ("for example, a skill's own `success` becomes `succeeded`") with a pointer to WC-4 in `~/.claude/WORKER-CONTRACT.md` and a link to `#76-orca-orchestration-commands-as-workers` for the full mapping.
- `### 5.10 Skill-Authoring Checklist`: add checklist items in the file's existing checkbox format (`- [ ] **Label**` followed by plain text, no dash after the label), each naming its rule ID and linking to `#76-orca-orchestration-commands-as-workers`, never repeating a list or number from 7.6: decide whether the command can be a worker or is a never-as-worker command (section 7.6); every person-blocking step has an unattended resolution listed in the command's `## Unattended mode` section (WC-2); the worker contract is written on every outcome and follows the WC-4 two-case rule; no call to `worker-start`, `dispatch` or `task-create` in the skill, its refs or scripts (WC-8), and, per the rollout plan (SA-2), no `orca` or `orca-ide` command at all; outward defaults and the skill's own commit or `.dev/tasks` staging step are off under `--unattended` (WC-9); no single blocking Bash wait exceeds the WC-10 limit; default write paths are parallel-safe (WC-11); nested `/sc:` invocations follow the nested propagation rule (section 7.6).

Acceptance criteria:
- 5.9's new part states both two-case-rule cases in full, marks its mapping line as an example, links to `#76-orca-orchestration-commands-as-workers`, and does not list the four `worker_status` values.
- 5.10 gains at least eight new checklist items in the `- [ ] **Label**` format, each with a rule ID or "section 7.6" and the 7.6 link; none contains a digit followed by "minute"; none contains an em dash or en dash.
- The 5.10 WC-8 item names the three dispatch verbs, and its wider no-Orca clause carries "per the rollout plan (SA-2)".
- No sentence in 5.9 or 5.10 says "beside `status`" without the condition "already writes `return-contract.yaml` in the report directory".

## Phase 3: Point the workflow and practice chapters at 7.6

## Task 6: Add Orca readiness to the development workflow and testing

Depends on: Task 1

In section 8 of `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, after reading `tests/skills/test_worker_contract.py` (the `AUDIT_ROOTS`, `WRITE_VERB_RE`, `WRITE_VERB_CLASSIFICATION`, `UNATTENDED_COMMANDS` definitions and the tests that use them):

- `### 8.3 Creating a New Component: Full Workflow`: inside the bash block, add a comment step between "2. Write the component" and "3. Sync to .claude/": decide worker eligibility (WC-2, section 7.6); if the command will accept `--unattended`, write its `## Unattended mode` section and add it to `UNATTENDED_COMMANDS`. Keep the block's comment style.
- `### 8.4 Testing Components`: add an "Orca readiness checks" list that opens with one sentence naming WC-2, WC-4 and WC-9 and linking to `#76-orca-orchestration-commands-as-workers`, then: run `uv run pytest tests/skills/test_worker_contract.py`; its write-verb audit scans the skills, commands and agents under `src/superclaude/` for `git add`, `commit`, `push`, `merge`, `stash`, `update-ref`, `worktree add` and `worktree remove` (also written with `-C <path>`), and for every `gh pr` and `gh api` line, reads included; each matching line needs an entry in `WRITE_VERB_CLASSIFICATION` with a category and a reason, and an entry whose line was edited or removed fails `test_classification_table_has_no_stale_entries`; a command given an `## Unattended mode` section must be added to `UNATTENDED_COMMANDS`, or `test_no_command_has_unattended_mode_section_after_p0` fails; and someone runs the command once without `--unattended` to confirm its prompts, outputs and outward defaults are unchanged.

Acceptance criteria:
- The 8.3 bash block has a comment naming `## Unattended mode`, `UNATTENDED_COMMANDS`, a WC rule ID and "section 7.6", placed before the `make sync-dev` line.
- 8.4's list opens with a sentence naming at least one WC rule ID and linking to `#76-orca-orchestration-commands-as-workers`.
- 8.4 names `tests/skills/test_worker_contract.py`, `WRITE_VERB_CLASSIFICATION`, `UNATTENDED_COMMANDS`, `test_classification_table_has_no_stale_entries` and `test_no_command_has_unattended_mode_section_after_p0`, and its verb list matches `WRITE_VERB_RE`; `grep -n` for each identifier and for `WRITE_VERB_RE` in `tests/skills/test_worker_contract.py` is saved to `./artifacts/t6-test-identifiers.txt`.
- 8.4 does not say the audit catches "any" git or gh write verb, and includes the check that behaviour without `--unattended` is unchanged.

## Task 7: Add Orca rules to best practices and anti-patterns

Depends on: Task 1

In section 9 of `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, each new line naming its rule ID and linking to `#76-orca-orchestration-commands-as-workers`, never repeating a list or number from 7.6:

- `### 9.1 Command Design`: Do bullets (decide worker eligibility up front, section 7.6; when the command accepts `--unattended`, list each gate's resolution, the report file and the report directory flag in `## Unattended mode` and point to `~/.claude/WORKER-CONTRACT.md`, WC-2); Do not bullets (call Orca from a command: the contract's opening says commands contain no Orca calls, and WC-8 bars `worker-start`, `dispatch` and `task-create`; copy shared contract rules into the command; leave an outward default on under `--unattended`, WC-9).
- `### 9.3 Skill Design`: Do bullets (write the worker contract on every outcome, WC-4; follow the WC-4 two-case rule for a skill's own contract file; split long blocking Bash waits, WC-10); Do not bullets (call `AskUserQuestion` or end on a question under `--unattended`, WC-2; write a fixed shared output path or a single-owner shared file under `--unattended`, WC-11).
- `### 9.7 Anti-Patterns`: add rows with Problem and Solution columns for: a person-blocking step under `--unattended` (the worker stalls; resolve by default, flag or blocked, WC-2); an Orca call inside a command or skill (per the rollout plan, SA-2, commands run where Orca is absent, and it competes with the coordinator; WC-8 for the dispatch verbs; the coordinator splits the work); a contract written only on success (the coordinator cannot tell a crash from a stop; write it on every outcome, WC-4); reusing `status` for the worker outcome (clashes with existing values; use `worker_status` under the WC-4 two-case rule); one long blocking Bash wait (no heartbeats; split it within the WC-10 limit); a fixed shared output path (two workers overwrite each other; timestamp or caller slug plus its own report directory, WC-11); copying the contract into a command (the copies drift; point to `~/.claude/WORKER-CONTRACT.md`).

Acceptance criteria:
- 9.1 and 9.3 each gain at least two Do and two Do not bullets as listed, each with its rule ID and the 7.6 link.
- 9.7 gains seven rows, one per anti-pattern listed, each citing its rule ID or the installed contract path, and the Orca-call row labels its SA-2 rationale "per the rollout plan".
- No new line in section 9 contains a digit followed by "minute", cites WC-8 for anything but the three dispatch verbs, or states "beside `status`" without the two-case condition.

## Phase 4: Fix the templates and reference appendices, then check the whole change

## Task 8: Fix Appendix B's fences and add unattended slots to the templates

Depends on: Task 1, Task 5

In `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`:

- First write a fence-state script at `./artifacts/t8-fence-check.py` (never under docs/, src/, plugins/ or tests/) that tracks each fence's opening backtick run and closes it only on a bare fence of at least that length, and prints, for a given file, each heading line's fence state and every spot where an inner fence closes an outer one; run it with `uv run python -I ./artifacts/t8-fence-check.py docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` before and after the edits below.
- `## Appendix B: Command Template`: change the template's outer fence from three to four backticks (the opening `markdown` fence after the heading becomes four backticks plus `markdown`; the closing fence before `## Appendix C` becomes four backticks). Then, inside the template, add optional `--unattended` and `--report-dir` rows to the Options table: the `--unattended` row marked "only if this command accepts unattended mode (WC-2, section 7.6)"; the `--report-dir` row marked "only if this command has no directory-valued `--output` or `--output-dir`, or the brief does not pass it; both or neither is refused (WC-4, section 7.6)". Add an optional `## Unattended mode` section before `## Boundaries` with slots for each gate and its resolution (default, flag, or blocked), the report file, the report directory flag, nested invocations, resume input, and a pointer line naming WC-4, "section 7.6" and `~/.claude/WORKER-CONTRACT.md`, marked optional and delete-if-unused, in the template's angle-bracket placeholder style.
- `## Appendix A: SKILL.md Skeleton Template`: inside the template, add a note under `## Protocol` that names WC-2 and "section 7.6" as plain text and says each person-blocking step applies the resolution its command's `## Unattended mode` section names when the run has `--unattended`; and a note under `## Return Contract` that only points to section 5.9 for the worker contract under `--unattended` and names no rule.
- Record in `./artifacts/t8-stale-fences.txt` every nested-fence spot outside Appendix B that the script reports (including the 2.1 Quick Start spot around guide lines 132 to 212 and the section 10 spots), with line numbers and a one-line description each; these are reported, not fixed.

Acceptance criteria:
- The script's "after" output, saved to `./artifacts/t8-fence-check.txt`, shows `## Appendix B` content (including its `## Unattended mode` slot and `## Boundaries`) inside one four-backtick fence and the `## Appendix C: Agent Template` heading outside any fence.
- Appendix B's template contains `## Unattended mode` with slots for gates, report file, report directory flag, nested invocations and resume input, and a pointer line naming WC-4, "section 7.6" and `~/.claude/WORKER-CONTRACT.md`; the `--report-dir` row carries the own-flag case, the brief case and the both-or-neither refusal.
- Appendix A's `## Protocol` note contains `WC-2` and `section 7.6`; its `## Return Contract` note mentions section 5.9, contains no WC rule ID and does not contain the word "beside".
- `./artifacts/t8-stale-fences.txt` lists the 2.1 spot and every spot the script flags outside Appendix B; `git diff HEAD --name-only` shows no new file under docs/, src/, plugins/ or tests/.

## Task 9: Update the path reference and glossary, then run the whole-change checks

Depends on: Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8

In `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`:

- `## Appendix D: File Path Reference`: add a row for the worker contract (`src/superclaude/core/WORKER-CONTRACT.md`, installed to `~/.claude/WORKER-CONTRACT.md`) and a row for `tests/skills/test_worker_contract.py` (not installed), paths only; correct the "Core files" row from `src/superclaude/*.md` to `src/superclaude/core/*.md`, which the installer reads (`package_root / "core"` in `src/superclaude/cli/install_core.py`).
- `## Appendix E: Glossary`: add rows, in alphabetical order with the existing rows, for Brief guard (applies from P1), Coordinator, Lifecycle messages, Nested propagation rule, Never-as-worker list, Report directory, Unattended mode, Worker (Orca), Worker contract and `worker_status`; each is one sentence that names its rule ID or "section 7.6", links to `#76-orca-orchestration-commands-as-workers`, and repeats no list, flag set, value set or number from 7.6. The Report directory row says: the one directory the brief passes for the worker contract, either the command's own directory-valued `--output` or `--output-dir`, or `--report-dir` for a command without one or a brief that does not pass it; both or neither is refused (WC-4). The Worker contract row names the WC-4 two-case rule with a link and states no case alone.
- Run the whole-change checks below and save their outputs.

Acceptance criteria:
- Appendix D has a `WORKER-CONTRACT.md` row with source and installed paths, a `test_worker_contract.py` row, and a "Core files" row reading `src/superclaude/core/*.md`.
- Appendix E has the ten new terms in alphabetical order, each with the 7.6 link; the Brief guard row says "from P1"; the Report directory row carries the own-flag case, the brief case and the both-or-neither refusal.
- One-home check: for each of `/sc:swarm-wizard`, `/sc:pm`, `--mode socratic`, `--monitor 1` and `4 minutes`, the count of occurrences outside 7.6's line range (from its heading to the `## 8. Development Workflow` heading) is 0 and inside it is at least 1; counts saved to `./artifacts/t9-one-home.txt`. A failing count is recorded with its line and fixed in the section that owns that line.
- Dash check: `git diff HEAD -U0 -- docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md | grep '^+' | grep -v '^+++' | LC_ALL=C grep -P '\xE2\x80[\x93\x94]'` prints nothing; output saved to `./artifacts/t9-dash-check.txt`.
- Ask check: every added line in the guide's `git diff HEAD -U0` containing "the person", "the user" or "a person" states that nothing asks them; lines and verdicts saved to `./artifacts/t9-ask-check.txt`.
- `uv run pytest tests/docs tests/skills/test_worker_contract.py -q` passes, output saved to `./artifacts/t9-pytest.txt`; `uv run pytest tests/core -q` is also run and saved to `./artifacts/t9-pytest-core.txt` with the note that it pins `HOW-WE-WORK.md` and `CLAUDE.md`, which the guide cross-references (a failure there is recorded with its test name and blocks only if this change caused it).
- `git diff HEAD --name-only -- docs src plugins tests` lists only `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` and the already-modified `docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md`; output saved to `./artifacts/t9-changed-files.txt`.
