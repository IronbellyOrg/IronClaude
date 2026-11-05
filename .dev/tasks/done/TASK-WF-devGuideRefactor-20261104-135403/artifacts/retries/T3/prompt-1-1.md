9ad65574bcae5fb46f853c7a0b9f0c4d7e50979d
Review one task for spec compliance.

Task brief: T3 (AC ids in order of the "Acceptance criteria:" bullets: T3.AC1,T3.AC2,T3.AC3,T3.AC4). Plan file: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/TASK-WF-devGuideRefactor-20261104-135403.md, lines 74-88:
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

Start sha: 9ad65574bcae5fb46f853c7a0b9f0c4d7e50979d
Diff against the start snapshot: (git diff 9ad65574bcae5fb46f853c7a0b9f0c4d7e50979d -- docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md, plus the task's new artifact files under .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/ listed after the diff)
diff --git a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
index 8124b52b..41433d4e 100644
--- a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
+++ b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
@@ -303,6 +303,9 @@ version: "2.0.0"              # Explicit spec version (used in task-unified)
 | `## Examples` | Copy-paste invocation samples | Yes |
 | `## Boundaries` | Will / Will Not lists | Yes |
 | `## Related Commands` | Links to related `/sc:*` commands | Recommended |
+| `## Unattended mode` | This command's gate resolutions, report file, report directory flag and nested invocations under `--unattended` ([section 7.6](#76-orca-orchestration-commands-as-workers)) | Only when the command accepts `--unattended`, which no command does at P0 |
+
+A command that accepts `--unattended` lists it in `## Options` (this guide's convention). It takes `--report-dir` when it has no directory-valued `--output` or `--output-dir` of its own, or when the brief does not pass that flag; passing both, or neither, is refused before any work (WC-4, [section 7.6](#76-orca-orchestration-commands-as-workers)).
 
 ### 3.2 Command Archetypes
 
@@ -314,6 +317,7 @@ Commands that read, analyze, and report without modifying files.
 
 - **Examples**: `/sc:analyze`, `/sc:cleanup-audit`, `/sc:explain`
 - **Characteristics**: Read-heavy tools, native reasoning for deep analysis, produces reports
+- **Worker fit**: `/sc:cleanup-audit` is in the contract's ready-with-brief-constraints table; one of `/sc:explain`'s flags is refused under `--unattended` (section 7.6); a command gets `--unattended` only after each of its gates has an unattended resolution (WC-2). See [section 7.6](#76-orca-orchestration-commands-as-workers).
 - **Typical frontmatter**:
 
 ```yaml
@@ -329,6 +333,7 @@ Commands that decompose work and delegate to sub-agents without directly executi
 - **Examples**: `/sc:spawn`, `/sc:adversarial`
 - **Characteristics**: Task tool for delegation, defines stop conditions, produces task hierarchies or coordination artifacts
 - **Key pattern**: Explicit "STOP AFTER" boundary preventing the command from executing what it plans
+- **Worker fit**: `/sc:spawn` is a never-as-worker command (section 7.6); `/sc:adversarial` is in the contract's ready-with-brief-constraints table. Such a command may fan out with the Agent tool (WC-7) but never calls `worker-start`, `dispatch` or `task-create` (WC-8). See [section 7.6](#76-orca-orchestration-commands-as-workers).
 
 Example from `/sc:spawn`:
 ```
@@ -344,6 +349,7 @@ Commands that handle the full lifecycle from classification through execution to
 
 - **Examples**: `/sc:task-unified`, `/sc:implement`, `/sc:build`
 - **Characteristics**: Multiple MCP servers, many personas, tiered compliance, sub-agent delegation
+- **Worker fit**: outward actions and the command's own commit step are off under `--unattended` (WC-9); per the rollout plan, `/sc:implement` is converted in P4. See [section 7.6](#76-orca-orchestration-commands-as-workers).
 - **Typical frontmatter**:
 
 ```yaml
@@ -384,6 +390,8 @@ Some commands declare `wave-enabled: true` in their frontmatter, and many protoc
 
 After creating a command file, register it in `src/superclaude/core/HOW-WE-WORK.md`. Routing-table rows are per job, not per command: if a workflow should use the new command, add it to that job's row in the routing table (its steps and mandatory flags), or add a new job row; if no workflow uses it, add one row to the "Other commands" table instead. Then copy the guide byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (and, if you edited the level table, re-copy it into `src/superclaude/core/CLAUDE.md`), run `make sync-dev` and `make verify-sync`, and run `uv run pytest tests/core tests/commands` (these tests check the routing table and the plugin copy). No other framework file needs registering: `/sc:help` lists installed commands live.
 
+A command that accepts `--unattended` needs no entry in any worker list, because the coordinator decides from whether the command file has an `## Unattended mode` section (the "Orca coordination" section of `~/.claude/HOW-WE-WORK.md`). The one registration step it does need is in a test file: the maintainer adds its name to `UNATTENDED_COMMANDS` in `tests/skills/test_worker_contract.py`, as section 8.4 describes. The never-as-worker list changes only through the maintainer edit that [section 7.6](#76-orca-orchestration-commands-as-workers) describes.
+
 ---
 
 ## 4. Agents Deep Dive

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t3-ready-table.txt ===
# Ready-with-brief-constraints table membership, in section 5 of src/superclaude/core/WORKER-CONTRACT.md
$ grep -n '^## ' src/superclaude/core/WORKER-CONTRACT.md
9:## 1. Terms
26:## 2. Command-side rules
47:## 3. Worker-session duties
63:## 4. Coordinator rules
165:## 5. Coordinator brief template
$ grep -n 'ready with brief constraints' src/superclaude/core/WORKER-CONTRACT.md
187:Flags the brief must pass, for the 12 commands that are ready with brief constraints. `--report-dir` is marked "from P1": no command accepts it at P0.
$ grep -nE '^\| `/sc:(adversarial|cleanup-audit)`' src/superclaude/core/WORKER-CONTRACT.md
191:| `/sc:adversarial` | `--output <dir>`; never `--interactive` |
193:| `/sc:cleanup-audit` | `--pass <N>` (single pass); `--report-dir <dir>` (from P1) |
Result: both rows sit at lines 191 and 193, after '## 5. Coordinator brief template' (line 165), inside the table introduced at line 187.

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
