701fa81abcf419441a31f2e710c534e9c6fc8e93
Review one task for spec compliance.

Task brief: T4 (AC ids in order of the "Acceptance criteria:" bullets: T4.AC1,T4.AC2,T4.AC3,T4.AC4). Plan file: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/TASK-WF-devGuideRefactor-20261104-135403.md, lines 90-100:
## Task 4: Add the worker-session rules to the agents chapter

Depends on: Task 1

In `### 4.2 Agent Patterns` of `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`: add a short opening paragraph that separates the two meanings of "worker" (a pattern such as Constrained Worker is an Agent-tool subagent inside one session; an Orca worker is a whole top-level session the coordinator starts; link to `#76-orca-orchestration-commands-as-workers`). Add one sentence to Pattern 3 "Process Orchestrator": an orchestrating agent coordinates subagents inside its own session only; it never calls `worker-start`, `dispatch` or `task-create`, because the command it runs under never does (WC-8). After the four patterns add a bullet list with three separate items: only the top-level worker session sends lifecycle messages (heartbeat, ask, check, `worker_done`), never a subagent (WC-7); no agent calls `worker-start`, `dispatch` or `task-create`, because the command never does (WC-8); under `--unattended` nothing asks the person, so an agent resolves a gate the way its command's `## Unattended mode` section says (this guide's convention), and only the worker session may put a blocked question to the coordinator when its brief allows it (WC-2, WC-3).

Acceptance criteria:
- 4.2 contains the two-meanings paragraph with a link to `#76-orca-orchestration-commands-as-workers`.
- The Pattern 3 sentence cites WC-8 beside the three dispatch verbs; `grep -n 'WC-13' docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` prints nothing.
- The closing list has three separate items citing WC-7, WC-8, and WC-2 with WC-3; the WC-7 item lists heartbeat, ask, check and `worker_done`.
- Every added 4.2 line containing "the person", "the user" or "a person" states that nothing asks them; the matching lines with a one-line verdict each are saved to `./artifacts/t4-ask-check.txt`.

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

Start sha: 701fa81abcf419441a31f2e710c534e9c6fc8e93
Diff against the start snapshot: (git diff 701fa81abcf419441a31f2e710c534e9c6fc8e93 -- docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md, plus the task's new artifact files under .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/ listed after the diff)
diff --git a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
index 41433d4e..3d8848fc 100644
--- a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
+++ b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
@@ -436,6 +436,8 @@ permissionMode: restricted     # Permission level
 
 ### 4.2 Agent Patterns
 
+"Worker" has two meanings in this guide. A pattern such as Constrained Worker below is an Agent-tool subagent inside one session. An Orca worker is a whole top-level session that a coordinator starts to run one command ([section 7.6](#76-orca-orchestration-commands-as-workers)).
+
 Agents follow four recurring patterns:
 
 #### Pattern 1: Constrained Worker
@@ -461,6 +463,7 @@ An agent that coordinates other agents without doing the work itself. Manages se
 - **Example**: `debate-orchestrator` -- coordinates adversarial debate without participating
 - **Characteristics**: Task tool for delegation, strict neutrality, process integrity focus, return contracts
 - **Key constraint**: "Does NOT participate in debates or advocate for any variant"
+- **Orca boundary**: an orchestrating agent coordinates subagents inside its own session only; it never calls `worker-start`, `dispatch` or `task-create`, because the command it runs under never does (WC-8)
 - **Typical size**: 60-100 lines
 
 #### Pattern 4: Meta-Layer Agent
@@ -471,6 +474,12 @@ An agent that operates across sessions and manages knowledge, learning, and docu
 - **Characteristics**: `.superclaude/memory/` files for session persistence, PDCA self-evaluation, mandatory session start activation
 - **Typical size**: 100-150 lines
 
+When an Orca coordinator runs the command as a worker, these rules hold for every agent under it ([section 7.6](#76-orca-orchestration-commands-as-workers)):
+
+- Only the top-level worker session sends lifecycle messages (heartbeat, ask, check, `worker_done`), never a subagent (WC-7).
+- No agent calls `worker-start`, `dispatch` or `task-create`, because the command it runs under never does (WC-8).
+- Under `--unattended` nothing asks the person, so an agent resolves a gate the way its command's `## Unattended mode` section says (this guide's convention); only the worker session may put a blocked question to the coordinator, and only when its brief allows it (WC-2, WC-3).
+
 ### 4.3 Agent Spec Format (Dynamic Instantiation)
 
 Skills can dynamically create agents using the agent spec mini-language:

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t4-ask-check.txt ===
# T4 ask check: lines added to docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md by T4 (git diff 701fa81abcf419441a31f2e710c534e9c6fc8e93 -U0) matching 'the person|the user|a person'
guide line 481: - Under `--unattended` nothing asks the person, so an agent resolves a gate the way its command's `## Unattended mode` section says (this guide's convention); only the worker session may put a blocked question to the coordinator, and only when its brief allows it (WC-2, WC-3).
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
