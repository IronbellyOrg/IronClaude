ee6a08d2cb1c7c2279a282740af1c0dca64bdfb5
Review one task for spec compliance.

Task brief: T9 (AC ids in order of the "Acceptance criteria:" bullets: T9.AC1,T9.AC2,T9.AC3,T9.AC4,T9.AC5,T9.AC6,T9.AC7). Plan file: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/TASK-WF-devGuideRefactor-20261104-135403.md, lines 168-185:
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

Start sha: ee6a08d2cb1c7c2279a282740af1c0dca64bdfb5
Diff against the start snapshot: (git diff ee6a08d2cb1c7c2279a282740af1c0dca64bdfb5 -- docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md, plus the task's new artifact files under .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/ listed after the diff)
diff --git a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
index f92ae120..ea89d489 100644
--- a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
+++ b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
@@ -2199,7 +2199,9 @@ All paths are relative to the SuperClaude Framework repository root:
 | Commands | `src/superclaude/commands/*.md` | `~/.claude/commands/sc/*.md` |
 | Agents | `src/superclaude/agents/*.md` | `~/.claude/agents/*.md` |
 | Skills | `src/superclaude/skills/*/SKILL.md` | `~/.claude/skills/*/SKILL.md` |
-| Core files | `src/superclaude/*.md` | `~/.claude/*.md` |
+| Core files | `src/superclaude/core/*.md` | `~/.claude/*.md` |
+| Worker contract | `src/superclaude/core/WORKER-CONTRACT.md` | `~/.claude/WORKER-CONTRACT.md` |
+| Worker contract tests | `tests/skills/test_worker_contract.py` | N/A (not installed) |
 | Dev copies | `.claude/commands/sc/`, `.claude/agents/`, `.claude/skills/` | N/A (dev only) |
 
 ## Appendix E: Glossary
@@ -2207,23 +2209,33 @@ All paths are relative to the SuperClaude Framework repository root:
 | Term | Definition |
 |------|-----------|
 | **Agent spec** | Mini-language format `model[:persona[:"instruction"]]` for dynamic agent creation |
+| **Brief guard** | The worker session's check, from P1, that each `Command:` line of its brief matches the `## Unattended mode` state of the command file copies it can see ([section 7.6](#76-orca-orchestration-commands-as-workers)) |
 | **CEV protocol** | Claim-Evidence-Verdict format for qualitative scoring |
 | **Circuit breaker** | Pattern that disables failing MCP servers and uses fallbacks |
 | **Compliance tier** | STRICT/STANDARD/LIGHT/EXEMPT classification for task execution depth |
 | **Context-Oriented Configuration** | SuperClaude's architecture: .md files that shape Claude Code behavior |
+| **Coordinator** | The session, opened by hand, that plans Orca work, creates one Task per unit of work and starts one worker per Task ([section 7.6](#76-orca-orchestration-commands-as-workers)) |
 | **Frontmatter** | YAML metadata block at the top of .md files, delimited by `---` |
 | **Lazy loading** | Skills load name/description (~50 tokens) at start; full content on invocation |
+| **Lifecycle messages** | The Orca messages that only the top-level worker session sends, never a subagent (WC-7, [section 7.6](#76-orca-orchestration-commands-as-workers)) |
 | **MCP** | Model Context Protocol -- servers that extend Claude Code capabilities |
+| **Nested propagation rule** | How a command run with `--unattended` passes the flag and a nested report directory to a nested `/sc:` command ([section 7.6](#76-orca-orchestration-commands-as-workers)) |
+| **Never-as-worker list** | The commands that are never dispatched as Orca workers and get no `--unattended` mode ([section 7.6](#76-orca-orchestration-commands-as-workers)) |
 | **Persona** | Specialized behavior profile (architect, security, qa, etc.) |
 | **Position-bias mitigation** | Dual-pass scoring (forward + reverse) to eliminate order effects |
 | **Progressive disclosure** | Information loaded incrementally as needed, not all at once |
 | **refs/** | Reference files in a skill directory, loaded on-demand per wave |
+| **Report directory** | The one directory the brief passes for the worker contract: either the command's own directory-valued `--output` or `--output-dir`, or `--report-dir` for a command without one or a brief that does not pass it; both or neither is refused before any work (WC-4, [section 7.6](#76-orca-orchestration-commands-as-workers)) |
 | **Return contract** | Structured data a skill returns for inter-command composition |
 | **REVISE loop** | Max 2 iteration retry for scores in 70-84% range |
 | **sc- prefix** | Skill prefix indicating it backs a `/sc:` command |
 | **Steelman** | Debate strategy: present the strongest version of each argument |
 | **STOP pattern** | Explicit halt condition when required inputs are missing |
+| **Unattended mode** | The behaviour a command switches to when its caller passes `--unattended`, with no step that waits for a human (WC-2, [section 7.6](#76-orca-orchestration-commands-as-workers)) |
 | **Wave** | One stage in multi-phase command execution |
+| **Worker (Orca)** | A top-level Claude session that an Orca coordinator starts to run one `/sc:` command; not an Agent-tool subagent ([section 7.6](#76-orca-orchestration-commands-as-workers)) |
+| **Worker contract** | The `return-contract.yaml` a command writes in its report directory on every outcome under `--unattended`, following the WC-4 two-case rule ([section 7.6](#76-orca-orchestration-commands-as-workers)) |
+| **`worker_status`** | The worker contract's outcome field, kept separate from a command's own `status` (WC-4, [section 7.6](#76-orca-orchestration-commands-as-workers)) |
 
 ---
 

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t9-one-home.txt ===
# One-home check: 7.6 range is guide lines 998-1056 (heading to '## 8. Development Workflow')
/sc:swarm-wizard: inside=1 outside=0
/sc:pm: inside=1 outside=0
--mode socratic: inside=1 outside=0
--monitor 1: inside=1 outside=0
4 minutes: inside=1 outside=0

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t9-dash-check.txt ===
$ git diff HEAD -U0 -- docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md | grep '^+' | grep -v '^+++' | LC_ALL=C grep -P '\xE2\x80[\x93\x94]'
rc=1 (1 = no match: no em dash or en dash in any added line)

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t9-ask-check.txt ===
# Ask check: added lines in git diff HEAD -U0 -- docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md matching 'the person|the user|a person'
guide line 481: - Under `--unattended` nothing asks the person, so an agent resolves a gate the way its command's `## Unattended mode` section says (this guide's convention); only the worker session may put a blocked question to the coordinator, and only when its brief allows it (WC-2, WC-3).
verdict: states that nothing asks the person (contains 'nothing asks the person')
guide line 1026: - **WC-2, no waiting for a human.** Under `--unattended` nothing asks the person: the command never calls `AskUserQuestion`, never ends its turn on a chat question or a `[yes / no]` offer, and never says STOP AND WAIT. Each gate resolves one of three ways, listed in the command's `## Unattended mode` section: a documented default, a value the caller passed as a flag, or blocked, where the command writes its contract with `worker_status: blocked` and the exact question in `blocked_question`, then stops.
verdict: states that nothing asks the person (contains 'nothing asks the person')
guide line 1052: - Under `--unattended` nothing asks the person. Only the worker session may put a blocked question to the coordinator, and only when its brief allows it (WC-2, WC-3).
verdict: states that nothing asks the person (contains 'nothing asks the person')

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t9-pytest.txt ===
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 4.3.5
rootdir: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs
configfile: pyproject.toml
plugins: superclaude-4.3.5, anyio-4.16.0
collected 204 items

tests/docs/test_chrome_devtools_mcp_removed.py .                         [  0%]
tests/docs/test_retired_docs_absent.py ..                                [  1%]
tests/docs/test_tavily_doc_alignment.py .....                            [  3%]
tests/skills/test_worker_contract.py ................................... [ 21%]
........................................................................ [ 56%]
........................................................................ [ 91%]
.................                                                        [100%]

============================= 204 passed in 0.82s ==============================
rc=0

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t9-pytest-core.txt ===
# Note: tests/core pins HOW-WE-WORK.md and CLAUDE.md, which the guide cross-references; a failure here blocks only if this change caused it.
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 4.3.5
rootdir: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs
configfile: pyproject.toml
plugins: superclaude-4.3.5, anyio-4.16.0
collected 104 items

tests/core/test_claude_md_routing_block.py ......                        [  5%]
tests/core/test_codegraph_guide.py ...............                       [ 20%]
tests/core/test_how_we_work_routing_table.py ........................... [ 46%]
....................................................                     [ 96%]
tests/core/test_research_config.py ....                                  [100%]

============================= 104 passed in 0.59s ==============================
rc=0

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t9-changed-files.txt ===
$ git diff HEAD --name-only -- docs src plugins tests
docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md
$ git status --porcelain -- docs src plugins tests
 M docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
 M docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md

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
