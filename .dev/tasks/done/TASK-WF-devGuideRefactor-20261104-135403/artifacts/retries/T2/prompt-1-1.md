6f177c1ee9f1519536f1a6eabf7f64638f63a69c
Review one task for spec compliance.

Task brief: T2 (AC ids in order of the "Acceptance criteria:" bullets: T2.AC1,T2.AC2,T2.AC3,T2.AC4,T2.AC5). Plan file: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/TASK-WF-devGuideRefactor-20261104-135403.md, lines 61-72:
## Task 2: Update the header, table of contents and introduction

Depends on: Task 1

In `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`: change the header's `**Last Updated**` date to 2026-11-04; under item 7 of `## Table of Contents` add an indented entry `[7.6 Orca Orchestration: Commands as Workers](#76-orca-orchestration-commands-as-workers)` (link only); in the `### Installation Locations` code block add a `core/` line to the `src/superclaude/` block (core framework files, including `CLAUDE.md`, `HOW-WE-WORK.md` and `WORKER-CONTRACT.md`) and a matching core-files line to the `~/.claude/` block that names `WORKER-CONTRACT.md` and "section 7.6" as plain text; in `### Context Loading Sequence` item 1 add one sentence that `~/.claude/WORKER-CONTRACT.md` is installed beside `CLAUDE.md`, is read on demand by a coordinator and, from P1, by a worker applying the brief guard, and is never `@`-imported, with a link to `#76-orca-orchestration-commands-as-workers`. Confirm the facts first by reading `KNOWN_CORE_FILES` and `_get_core_source` in `src/superclaude/cli/install_core.py` and the imports in `src/superclaude/core/CLAUDE.md`.

Acceptance criteria:
- The table-of-contents link target is `#76-orca-orchestration-commands-as-workers`.
- `### Installation Locations` shows a `core/` entry under `src/superclaude/` and a core-files entry under `~/.claude/` naming `WORKER-CONTRACT.md` and "section 7.6".
- The Context Loading sentence says "from P1" for the brief guard, states the file is never `@`-imported, and links to `#76-orca-orchestration-commands-as-workers`.
- The outputs of `grep -nE '"(HOW-WE-WORK|WORKER-CONTRACT)\.md"' src/superclaude/cli/install_core.py`, `grep -n 'package_root / "core"' src/superclaude/cli/install_core.py` and `grep -n '^@' src/superclaude/core/CLAUDE.md` are saved to `./artifacts/t2-core-evidence.txt`; the first shows both names and the last prints only the `@BASH_INSPECTION_POLICY.md` line.
- The header reads `**Last Updated**: 2026-11-04`.

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

Start sha: 6f177c1ee9f1519536f1a6eabf7f64638f63a69c
Diff against the start snapshot: (git diff 6f177c1ee9f1519536f1a6eabf7f64638f63a69c -- docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md, plus the task's new artifact files under .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/ listed after the diff)
diff --git a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
index 407db6f7..8124b52b 100644
--- a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
+++ b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
@@ -1,6 +1,6 @@
 p# SuperClaude Developer Guide: Commands, Skills, and Agents
 
-> **Version**: 1.0.0 | **Last Updated**: 2026-02-21
+> **Version**: 1.0.0 | **Last Updated**: 2026-11-04
 > **Audience**: Developers creating, extending, or maintaining SuperClaude framework components
 > **Source of Truth**: `src/superclaude/` -- all component source files live here
 
@@ -15,6 +15,7 @@ p# SuperClaude Developer Guide: Commands, Skills, and Agents
 5. [Skills Deep Dive](#5-skills-deep-dive)
 6. [Multi-Phase Architecture](#6-multi-phase-architecture)
 7. [Integration Patterns](#7-integration-patterns)
+   - [7.6 Orca Orchestration: Commands as Workers](#76-orca-orchestration-commands-as-workers)
 8. [Development Workflow](#8-development-workflow)
 9. [Best Practices](#9-best-practices)
 10. [Complete Examples](#10-complete-examples)
@@ -80,8 +81,10 @@ Source of truth (development):     src/superclaude/
   commands/                        Command .md files
   skills/                          Skill directories (SKILL.md + refs/)
   agents/                          Agent .md files
+  core/                            Core framework files (CLAUDE.md, HOW-WE-WORK.md, WORKER-CONTRACT.md, ...)
 
 Installation target (user):        ~/.claude/
+  *.md                             Installed core files, including WORKER-CONTRACT.md (worker rules, section 7.6)
   commands/sc/                     Installed commands
   skills/                          Installed skills
   agents/                          Installed agents
@@ -116,6 +119,7 @@ Rules:
 When Claude Code starts a session, it loads context in this priority order:
 
 1. **Core file** (always loaded): `~/.claude/CLAUDE.md`, which imports only `BASH_INSPECTION_POLICY.md`. The routing guide `~/.claude/HOW-WE-WORK.md` is installed beside it but is read on demand (by `/sc:help`, `/sc:recommend`, or a person); it is never `@`-imported.
+   The worker contract `~/.claude/WORKER-CONTRACT.md` is installed beside `CLAUDE.md` too. It is read on demand by an Orca coordinator and, from P1, by a worker applying the brief guard, and it is never `@`-imported ([section 7.6](#76-orca-orchestration-commands-as-workers)).
 2. **Explicit commands**: User types `/sc:<command>` -- loads the command file
 3. **Manual agents**: User references `@agent-<name>` -- loads the agent file
 4. **Flag-triggered**: per-command flags (each command file lists its own); `--c7`, `--play` and similar are behavioural hints, see `docs/user-guide/flags.md`

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t2-core-evidence.txt ===
$ grep -nE '"(HOW-WE-WORK|WORKER-CONTRACT)\.md"' src/superclaude/cli/install_core.py
20:        "HOW-WE-WORK.md",
26:        "WORKER-CONTRACT.md",
$ grep -n 'package_root / "core"' src/superclaude/cli/install_core.py
121:    package_core_dir = package_root / "core"
$ grep -n '^@' src/superclaude/core/CLAUDE.md
3:@BASH_INSPECTION_POLICY.md

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
