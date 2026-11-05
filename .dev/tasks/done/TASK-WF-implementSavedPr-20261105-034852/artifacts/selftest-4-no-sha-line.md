this is not a start sha
Review one task for spec compliance.

Task brief: T1 (AC ids in order of the "Acceptance criteria:" bullets: T1.AC1,T1.AC2,T1.AC3,T1.AC4,T1.AC5,T1.AC6,T1.AC7). Plan file: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/TASK-WF-devGuideRefactor-20261104-135403.md, lines 38-57:
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

Global constraints: (plan ## Constraints, .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/TASK-WF-devGuideRefactor-20261104-135403.md lines 17-34)
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

Start sha: 6043f58f8df35b5b271c051146e687665fce7fc6
Diff against the start snapshot: (git diff 6043f58f8df35b5b271c051146e687665fce7fc6 -- docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md, plus the task's new artifact files under .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/ listed after the diff)
diff --git a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
index 4c3073a0..407db6f7 100644
--- a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
+++ b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
@@ -957,6 +957,62 @@ Skills can use shell preprocessing to inject runtime context:
 
 The `!command` syntax executes shell commands and injects their output into the skill context. This enables skills to adapt to the current repository state.
 
+### 7.6 Orca Orchestration: Commands as Workers
+
+Orca can run IronClaude commands as workers under an Orca coordinator (the `/orchestration` skill). The rules live in one installed core file, `~/.claude/WORKER-CONTRACT.md`. This subsection says what they mean for someone writing a command, skill or agent; it summarizes the contract and does not replace it, so read the contract before you rely on a worker rule.
+
+#### How the pieces fit
+
+- A coordinator is a session someone opened by hand, never one that Orca started as a worker. It plans the work, creates one Orca Task per unit of work, starts one worker per Task and reads each worker's report (`~/.claude/WORKER-CONTRACT.md`, opening and section 4).
+- A worker is a top-level Claude session that runs one `/sc:` command and reports it with `worker_done`: one command per worker.
+- Commands contain no Orca calls (the contract's opening). Per the rollout plan (SA-2), no command, skill or agent runs an `orca` or `orca-ide` command, and none needs Orca to be installed or running.
+- The `/orchestration` skill (`~/.claude/skills/orchestration/SKILL.md`) is a discovery stub that loads Orca's version-matched guide from the Orca binary. The IronClaude coordinator rules are in section 4 of `~/.claude/WORKER-CONTRACT.md`. The "Orca coordination" section of `~/.claude/HOW-WE-WORK.md` gives the short routing view.
+
+#### Rollout state
+
+- At P0 no command accepts `--unattended` or `--report-dir`, and `UNATTENDED_COMMANDS` in `tests/skills/test_worker_contract.py` is empty.
+- Per the rollout plan, a command gains `--unattended` and its `## Unattended mode` section in the phase that converts its gates, from P1 on, so no command accepts the flag while it can still stop for a human.
+- Per the rollout plan (SA-1), without `--unattended` every command behaves exactly as it does today: the same prompts, approval gates, default values, output paths and outward defaults.
+
+#### Deciding whether a new command can be a worker
+
+- The never-as-worker list (`~/.claude/WORKER-CONTRACT.md`, section 1): `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while decision D3 keeps it off workers. These commands are never dispatched as workers and get no `--unattended` mode.
+- Per the rollout plan, these are commands whose purpose is orchestration, a conversation with a human, or an outward action that must be authorized, so making them workers would remove their purpose.
+- Adding a command to the list is a maintainer edit of `src/superclaude/core/WORKER-CONTRACT.md` and of `NEVER_AS_WORKER` in `tests/skills/test_worker_contract.py`.
+- Any other command gets `--unattended` only after each of its gates has an unattended resolution (WC-2).
+
+#### What a command does under `--unattended`
+
+- **Flag parse rule.** `--unattended` counts only as a standalone argument token outside any quoted argument. The same text inside a quoted prompt or topic never switches the mode.
+- **Person-mode refusal.** Under `--unattended` every command refuses the flags that exist to involve a human: `--interactive`, `--format interactive` (explain), `--mode socratic` (business-panel), `--watch` (test) and `--monitor 1` (pr-submit). The refusal is a stop before any work: the command writes its worker contract with `worker_status: failed` and the refused flag in `reason`, or, when no report directory is known, prints the refusal in chat only (WC-4).
+- **WC-2, no waiting for a human.** Under `--unattended` nothing asks the person: the command never calls `AskUserQuestion`, never ends its turn on a chat question or a `[yes / no]` offer, and never says STOP AND WAIT. Each gate resolves one of three ways, listed in the command's `## Unattended mode` section: a documented default, a value the caller passed as a flag, or blocked, where the command writes its contract with `worker_status: blocked` and the exact question in `blocked_question`, then stops.
+- **WC-4, the report directory.** The brief passes exactly one report directory. A command uses its own directory-valued `--output` or `--output-dir` as the report directory; `--report-dir <dir>` is for a command without such a flag, or for a brief that does not pass that flag. Passing both, or neither, is refused before any work (WC-4): the command does no work, writes nothing, and prints one fixed error message in chat that names both ways to pass a report directory. With no contract written, the worker reports the run as failed (WC-5).
+- **WC-4, the worker contract.** The command writes `<report-dir>/return-contract.yaml` on every outcome (succeeded, failed, blocked and partial), including stops before any other output exists. Its top-level fields are `worker_contract_version` (`"1"`), `worker_status`, `command` (the exact command line), `report_path` (the main human-readable deliverable, if any) and `artifacts` (every other file written), plus `blocked_question` when blocked and `reason` when failed (for `/sc:implement`, also when blocked, carrying the STOP code). `worker_status` is one of `succeeded`, `partial`, `failed` or `blocked`. It is not named `status`, because existing contracts already use `status` with other values.
+- **WC-4, the two-case rule.** A command that already writes `return-contract.yaml` in the report directory itself keeps every existing field, including its own `status`, and adds the worker fields beside them. A command whose own contract lives elsewhere leaves that file unchanged, and the worker contract at `<report-dir>/return-contract.yaml` lists it in `artifacts`.
+- **WC-4, the status mapping.** A command's own status maps to `worker_status` in five cases: `success` to `succeeded`, `partial` to `partial`, `failed` to `failed`, `stopped-precondition` to `failed` with the precondition in `reason`, and the flag-STOP `blocked` of impact and graph to `failed` with the STOP in `reason`.
+- **WC-8, no dispatch from a command.** A command never calls `worker-start`, `dispatch` or `task-create`. Fan-out that needs Orca records is split into separate Tasks by the coordinator.
+- **WC-9, no outward action.** Under `--unattended` every outward default (push, merge into a shared branch, PR, GitHub post, install on a shared or real target, VM, paid external run) is off, and no brief can turn it on. The command's own commit step is off too, and the skills that stage `.dev/tasks` themselves defer that staging.
+- **WC-10, long waits.** A single blocking Bash call lasts at most 4 minutes. A longer wait (a poll, a long eval) is split into waits of at most 4 minutes so the worker session can heartbeat between the parts.
+- **WC-11, parallel-safe writes.** Default output paths carry a timestamp or the slug the coordinator passes, so two workers never write the same file. Single-owner shared files (for example memory keys overwritten whole) are not written under `--unattended`.
+- **Nested propagation rule.** When the command invokes another `/sc:` command or protocol skill, through the Skill tool or the Agent tool, it passes `--unattended` and the report directory `<caller report-dir>/nested/<command>-<n>/` if the invoked command accepts the flag at this phase, and lists the nested contract in its `artifacts`. Otherwise that step must be gate-free, or the caller skips it under `--unattended` and records the skip in its contract.
+
+#### The worker session, not the command (WC-7)
+
+WC-7 is a duty of the worker session. The worker runs the command at its own top level, never inside an Agent-tool subagent. Only that session sends lifecycle messages (heartbeat, ask, check, `worker_done`). A command's own Agent-tool fan-out stays as it is (WC-7).
+
+#### The `## Unattended mode` section of a converted command
+
+A converted command carries a short `## Unattended mode` section. Per the contract it lists that command's own gate resolutions and report file and names its nested invocations; as this guide's template convention (Appendix B), it also names its report directory flag and its resume input, if any. It points to `~/.claude/WORKER-CONTRACT.md` and does not restate the shared rules.
+
+From P1, the worker's brief guard checks every copy of the command file it can see (the project `.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md`) for this section, and copies that disagree make the worker refuse.
+
+#### Skills and agents under a command
+
+- As this guide's authoring convention, skills and agents that run under a command follow that command's `## Unattended mode` section (WC-2), and a skill follows the WC-4 two-case rule for its own contract file.
+- Only the top-level worker session sends lifecycle messages, never a subagent (WC-7).
+- No agent calls `worker-start`, `dispatch` or `task-create`, because the command it runs under never does (WC-8).
+- Under `--unattended` nothing asks the person. Only the worker session may put a blocked question to the coordinator, and only when its brief allows it (WC-2, WC-3).
+
 ---
 
 ## 8. Development Workflow

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t1-ask-check.txt ===
# T1 ask check: lines in 7.6 (guide lines 960-1018) matching 'the person|the user|a person'
guide line 988: - **WC-2, no waiting for a human.** Under `--unattended` nothing asks the person: the command never calls `AskUserQuestion`, never ends its turn on a chat question or a `[yes / no]` offer, and never says STOP AND WAIT. Each gate resolves one of three ways, listed in the command's `## Unattended mode` section: a documented default, a value the caller passed as a flag, or blocked, where the command writes its contract with `worker_status: blocked` and the exact question in `blocked_question`, then stops.
verdict: states that nothing asks the person (contains 'nothing asks the person')
guide line 1014: - Under `--unattended` nothing asks the person. Only the worker session may put a blocked question to the coordinator, and only when its brief allows it (WC-2, WC-3).
verdict: states that nothing asks the person (contains 'nothing asks the person')

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 
Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
