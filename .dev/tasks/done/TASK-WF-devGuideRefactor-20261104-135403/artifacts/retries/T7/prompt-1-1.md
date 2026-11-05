70eb51e80e5c58390556d29ebc0df5512560144e
Review one task for spec compliance.

Task brief: T7 (AC ids in order of the "Acceptance criteria:" bullets: T7.AC1,T7.AC2,T7.AC3). Plan file: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/TASK-WF-devGuideRefactor-20261104-135403.md, lines 134-147:
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

Start sha: 70eb51e80e5c58390556d29ebc0df5512560144e
Diff against the start snapshot: (git diff 70eb51e80e5c58390556d29ebc0df5512560144e -- docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md, plus the task's new artifact files under .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/ listed after the diff)
diff --git a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
index 5f74bf05..5c1e3ce8 100644
--- a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
+++ b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
@@ -1190,12 +1190,17 @@ The plugin repo is a **build output**, not a primary editing location. Always ed
 - Include 3-5 copy-paste examples covering common use cases
 - Declare MCP servers and personas in frontmatter even if empty (`[]`)
 - Use the existing command archetypes as starting points
+- Decide worker eligibility up front ([section 7.6](#76-orca-orchestration-commands-as-workers))
+- When the command accepts `--unattended`, list each gate's resolution, the report file and the report directory flag in `## Unattended mode`, and point to `~/.claude/WORKER-CONTRACT.md` (WC-2, [section 7.6](#76-orca-orchestration-commands-as-workers))
 
 **Do not**:
 - Create commands that do everything (single responsibility principle)
 - Skip the Boundaries section (leads to scope creep)
 - Hardcode file paths (use arguments and `@<path>` references)
 - Forget to register the command in the guide (a job row or the Other commands table, see 3.6)
+- Call Orca from a command: commands contain no Orca calls (the contract's opening), and WC-8 bars `worker-start`, `dispatch` and `task-create` ([section 7.6](#76-orca-orchestration-commands-as-workers))
+- Copy shared contract rules into the command; point to `~/.claude/WORKER-CONTRACT.md` instead ([section 7.6](#76-orca-orchestration-commands-as-workers))
+- Leave an outward default on under `--unattended` (WC-9, [section 7.6](#76-orca-orchestration-commands-as-workers))
 
 ### 9.2 Agent Design
 
@@ -1221,6 +1226,9 @@ The plugin repo is a **build output**, not a primary editing location. Always ed
 - Define input contracts with STOP/WARN conditions
 - Define return contracts for composability
 - Declare per-wave ref loading instructions
+- Write the worker contract on every outcome (WC-4, [section 7.6](#76-orca-orchestration-commands-as-workers))
+- Follow the WC-4 two-case rule for the skill's own contract file, as this guide's convention ([section 7.6](#76-orca-orchestration-commands-as-workers))
+- Split long blocking Bash waits (WC-10, [section 7.6](#76-orca-orchestration-commands-as-workers))
 
 **Do not**:
 - Ship a skill without a command in front of it (the command is the user-facing interface; the skill is the behavioral engine)
@@ -1230,6 +1238,8 @@ The plugin repo is a **build output**, not a primary editing location. Always ed
 - Use unrestricted `Bash` when specific commands suffice
 - Create skills without tool allowlisting
 - Skip the Will Do / Will Not Do boundaries
+- Call `AskUserQuestion` or end on a question under `--unattended` (WC-2, [section 7.6](#76-orca-orchestration-commands-as-workers))
+- Write a fixed shared output path or a single-owner shared file under `--unattended` (WC-11, [section 7.6](#76-orca-orchestration-commands-as-workers))
 
 ### 9.4 Token Management
 
@@ -1291,6 +1301,13 @@ These patterns emerged from real-world Claude Code usage:
 | Hardcoded file paths in skills | Breaks portability | Use arguments and relative paths |
 | Skipping the routing-table row | /sc:recommend never gets a matched-row answer for the command; it can only find it through live enumeration (slower, with no mandatory flags) | Add the command to a job row in the routing table, or to the "Other commands" table, in src/superclaude/core/HOW-WE-WORK.md |
 | No error handling matrix | Silent failures, confusing behavior | Define scenario/behavior/fallback table |
+| A step that waits for a human under `--unattended` | WC-2 forbids the question, so the step has no allowed outcome and the worker cannot finish it | Resolve each gate by a documented default, a caller flag or blocked (WC-2, [section 7.6](#76-orca-orchestration-commands-as-workers)) |
+| An Orca call inside a command or skill | Per the rollout plan (SA-2), commands run where Orca is absent; per the rollout plan, two controllers compete, which is why orchestrating commands stay with the coordinator | Leave fan-out to the coordinator, which splits the work into separate Tasks; WC-8 bars `worker-start`, `dispatch` and `task-create` ([section 7.6](#76-orca-orchestration-commands-as-workers)) |
+| A worker contract written only on success | A stop with no contract reads as a failure with no report (WC-5) | Write it on every outcome (WC-4, [section 7.6](#76-orca-orchestration-commands-as-workers)) |
+| Reusing `status` for the worker outcome | It clashes with the values existing contracts already give `status` | Use `worker_status` under the WC-4 two-case rule ([section 7.6](#76-orca-orchestration-commands-as-workers)) |
+| One long blocking Bash wait | The worker session cannot heartbeat during it | Split it into waits within the WC-10 limit ([section 7.6](#76-orca-orchestration-commands-as-workers)) |
+| A fixed shared output path | Two workers in one worktree overwrite each other's files | Use a timestamp or the slug the coordinator passes, plus the Task's own report directory (WC-11, [section 7.6](#76-orca-orchestration-commands-as-workers)) |
+| Copying the contract into a command | The copies drift from the contract | Point to `~/.claude/WORKER-CONTRACT.md` ([section 7.6](#76-orca-orchestration-commands-as-workers)) |
 
 ---
 

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
