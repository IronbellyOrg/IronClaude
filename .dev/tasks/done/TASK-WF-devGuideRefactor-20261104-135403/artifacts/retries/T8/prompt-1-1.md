0df448b6cea179f453ce6fddb23fabea285b5b62
Review one task for spec compliance.

Task brief: T8 (AC ids in order of the "Acceptance criteria:" bullets: T8.AC1,T8.AC2,T8.AC3,T8.AC4). Plan file: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/TASK-WF-devGuideRefactor-20261104-135403.md, lines 149-166:
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

Start sha: 0df448b6cea179f453ce6fddb23fabea285b5b62
Diff against the start snapshot: (git diff 0df448b6cea179f453ce6fddb23fabea285b5b62 -- docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md, plus the task's new artifact files under .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/ listed after the diff)
diff --git a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
index 5c1e3ce8..f92ae120 100644
--- a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
+++ b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
@@ -2038,6 +2038,8 @@ personas: [<personas>]
 
 ## Protocol
 
+<When the run has --unattended, each step that waits for a human applies the resolution its command's ## Unattended mode section names (WC-2, section 7.6; this guide's convention).>
+
 ### Step 1: <Name>
 <What happens, what refs to load, what output produced.>
 Output: `artifacts/<filename>`
@@ -2053,6 +2055,8 @@ Output: `artifacts/<filename>`
 
 ## Return Contract
 
+<Under --unattended a worker contract is written too; see section 5.9.>
+
 | Field | Type | Description |
 |-------|------|-------------|
 | `status` | string | `success`, `partial`, `failed` |
@@ -2075,7 +2079,7 @@ Output: `artifacts/<filename>`
 
 ## Appendix B: Command Template
 
-```markdown
+````markdown
 ---
 name: <command-name>
 description: "<one-line description>"
@@ -2102,6 +2106,8 @@ personas: [<personas>]
 | Flag | Short | Default | Description |
 |------|-------|---------|-------------|
 | `--flag` | `-f` | `value` | <description> |
+| `--unattended` | | off | <Optional row: only if this command accepts unattended mode (WC-2, section 7.6)> |
+| `--report-dir` | | none | <Optional row: only if this command has no directory-valued `--output` or `--output-dir`, or the brief does not pass it; both or neither is refused before any work (WC-4, section 7.6)> |
 
 ## Behavioral Flow
 1. <Step 1>
@@ -2118,6 +2124,18 @@ personas: [<personas>]
 /sc:<name> --flag value       # With options
 ```
 
+## Unattended mode
+<Optional section: delete it if this command does not accept --unattended.>
+
+Under `--unattended`:
+- <Gate name>: <resolution: default <value> | flag <--flag> | blocked with the question>
+- Report file: <path of the main deliverable>
+- Report directory flag: <--output <dir> | --output-dir <dir> | --report-dir <dir>>
+- Nested invocations: <each nested /sc: command and its nested report directory, or none>
+- Resume input: <the input a resumed run takes, or none>
+
+Shared rules (WC-4, section 7.6): see `~/.claude/WORKER-CONTRACT.md`.
+
 ## Boundaries
 
 **Will:**
@@ -2125,7 +2143,7 @@ personas: [<personas>]
 
 **Will Not:**
 - <constraint>
-```
+````
 
 ## Appendix C: Agent Template
 

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-fence-check.py ===
"""Fence-state checker for one Markdown file (Task 8 evidence; not a delivery file).

A fence opens on a line of 3 or more backticks or tildes (optionally followed by an
info string) and closes only on a bare fence line of the same character that is at
least as long as the opening run. While a fence is open, a line that looks like a new
opening fence with an info string (for example ```bash inside a ```markdown block) is
recorded as a nested opening; when a bare fence then closes the outer fence, that spot
is reported as an inner fence closing the outer one.

Usage: uv run python -I t8-fence-check.py <file.md>
Prints every heading line with its fence state, then every inner-closes-outer spot.
"""
import re
import sys

OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def scan(lines):
    headings = []
    spots = []
    fence = None  # (char, length, open_line, info)
    nested = None  # line number of the latest nested opening-shaped line
    for n, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        m = OPEN_RE.match(line)
        if fence is None:
            if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
                fence = (m.group(1)[0], len(m.group(1)), n, m.group(2).strip())
                nested = None
            elif re.match(r"^#{1,6} ", line):
                headings.append((n, line, "outside"))
            continue
        char, length, open_line, info = fence
        if m and m.group(1)[0] == char:
            run = len(m.group(1))
            rest = m.group(2).strip()
            if rest == "" and run >= length:
                if nested is not None:
                    spots.append((open_line, info, nested, n))
                fence = None
                nested = None
                continue
            if rest != "" and run >= length:
                # A shorter run is a valid nested fence; only a run at least as long
                # as the outer one marks a nested block whose bare close ends the outer.
                nested = n
                continue
        if re.match(r"^#{1,6} ", line):
            headings.append((n, line, f"inside fence opened at line {open_line} ({'`' * length if char == '`' else '~' * length}{info})"))
    if fence is not None:
        spots.append((fence[2], fence[3], None, None))
    return headings, spots


def main():
    path = sys.argv[1]
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    headings, spots = scan(lines)
    print(f"# Fence state of {path}")
    print("## Headings")
    for n, text, state in headings:
        print(f"L{n}: {text}  [{state}]")
    print("## Inner fence closes outer fence")
    if not spots:
        print("none")
    for open_line, info, nested, close in spots:
        if close is None:
            print(f"outer fence opened at L{open_line} ({info}) is never closed")
        else:
            print(f"outer fence opened at L{open_line} ({info}); nested opening at L{nested}; bare fence at L{close} closes the OUTER fence")


if __name__ == "__main__":
    main()

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-fence-check-before.txt ===
# Fence state of docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
## Headings
L9: ## Table of Contents  [outside]
L25: ## 1. Introduction  [outside]
L27: ### What SuperClaude Is  [outside]
L39: ### The Three-Tier Architecture  [outside]
L61: ### The Activation Pattern  [outside]
L66: ## Activation  [inside fence opened at line 65 (```markdown)]
L77: ### Installation Locations  [outside]
L98: ### Path rules for primitives  [outside]
L117: ### Context Loading Sequence  [outside]
L130: ## 2. Quick Start  [outside]
L132: ### 2.1 Create a Minimal Command  [outside]
L146: # /sc:hello - Hello World Command  [inside fence opened at line 136 (```markdown)]
L148: ## Triggers  [inside fence opened at line 136 (```markdown)]
L152: ## Usage  [inside fence opened at line 136 (```markdown)]
L158: ## Behavioral Flow  [outside]
L162: ## Examples  [outside]
L169: ## Boundaries  [outside]
L179: ### 2.2 Create a Minimal Agent  [inside fence opened at line 177 (```)]
L190: # Greeter Agent  [inside fence opened at line 177 (```)]
L192: ## Triggers  [inside fence opened at line 177 (```)]
L196: ## Behavioral Mindset  [inside fence opened at line 177 (```)]
L200: ## Tools  [inside fence opened at line 177 (```)]
L204: ## Outputs  [inside fence opened at line 177 (```)]
L208: ## Boundaries  [inside fence opened at line 177 (```)]
L218: ### 2.3 Create a Minimal Skill  [outside]
L229: # Hello Skill  [inside fence opened at line 222 (```markdown)]
L231: ## Purpose  [inside fence opened at line 222 (```markdown)]
L234: ## Protocol  [inside fence opened at line 222 (```markdown)]
L240: ## Will Do  [inside fence opened at line 222 (```markdown)]
L244: ## Will Not Do  [inside fence opened at line 222 (```markdown)]
L249: ### 2.4 Sync and Test  [outside]
L252: # Copy new components from src/ to .claude/  [inside fence opened at line 251 (```bash)]
L255: # Verify sync succeeded  [inside fence opened at line 251 (```bash)]
L258: # Test the command in Claude Code  [inside fence opened at line 251 (```bash)]
L259: # Type: /sc:hello  [inside fence opened at line 251 (```bash)]
L264: ## 3. Commands Deep Dive  [outside]
L266: ### 3.1 Anatomy of a Command File  [outside]
L310: ### 3.2 Command Archetypes  [outside]
L314: #### Archetype 1: Analysis Pipeline  [outside]
L329: #### Archetype 2: Meta-Orchestrator  [outside]
L340: ## CRITICAL BOUNDARIES  [inside fence opened at line 339 (```)]
L346: #### Archetype 3: Unified Executor  [outside]
L363: ### 3.3 Command Processing Pipeline  [outside]
L375: ### 3.4 Performance Profiles  [outside]
L385: ### 3.5 Wave-Enabled Commands  [outside]
L389: ### 3.6 Registering a New Command  [outside]
L397: ## 4. Agents Deep Dive  [outside]
L399: ### 4.1 Anatomy of an Agent File  [outside]
L437: ### 4.2 Agent Patterns  [outside]
L443: #### Pattern 1: Constrained Worker  [outside]
L451: #### Pattern 2: Specialist Investigator  [outside]
L459: #### Pattern 3: Process Orchestrator  [outside]
L469: #### Pattern 4: Meta-Layer Agent  [outside]
L483: ### 4.3 Agent Spec Format (Dynamic Instantiation)  [outside]
L502: ### 4.4 Agent Activation Methods  [outside]
L514: ## 5. Skills Deep Dive  [outside]
L516: ### 5.1 Anatomy of a Skill  [outside]
L531: ### 5.2 SKILL.md Frontmatter  [outside]
L571: ### 5.3 Extended Metadata Comment  [outside]
L586: ### 5.4 Tool Allowlisting  [outside]
L602: ### 5.5 Skill Complexity Tiers  [outside]
L606: #### Tier 1: Simple (SKILL.md only)  [outside]
L626: #### Tier 2: Medium (SKILL.md + allowed-tools + compliance logic)  [outside]
L648: #### Tier 3: Complex (SKILL.md + refs/ + agents + multi-phase)  [outside]
L673: ### 5.6 The refs/ Pattern (Lazy Loading)  [outside]
L685: ## Wave 2: Analysis  [inside fence opened at line 684 (```markdown)]
L698: ### 5.7 The sc- Prefix Convention  [outside]
L710: ### 5.8 Machine-Readable Headers  [outside]
L726: ### 5.9 Input and Output Contracts  [outside]
L728: #### Input Contracts  [outside]
L733: ## Required Input (STOP if missing)  [inside fence opened at line 732 (```markdown)]
L735: ### Mode A: Compare existing artifacts  [inside fence opened at line 732 (```markdown)]
L738: ### Mode B: Generate variants from source  [inside fence opened at line 732 (```markdown)]
L747: #### Output / Return Contracts  [outside]
L752: ## Return Contract  [inside fence opened at line 751 (```markdown)]
L765: #### Worker contract (under `--unattended`)  [outside]
L774: ### 5.10 Skill-Authoring Checklist  [outside]
L802: ## 6. Multi-Phase Architecture  [outside]
L804: ### 6.1 Wave System  [outside]
L836: ### 6.2 Compliance Tiers  [outside]
L866: ### 6.3 Delegation Intelligence  [outside]
L888: ### 6.4 Resource Management Zones  [outside]
L902: ## 7. Integration Patterns  [outside]
L904: ### 7.1 Command + Skill + Agent Composition  [outside]
L930: ### 7.2 MCP Server Integration  [outside]
L950: ### 7.3 Persona Integration  [outside]
L975: ### 7.4 Thinking Depth Flags  [outside]
L985: ### 7.5 Dynamic Context Injection  [outside]
L990: ## Repository Context  [inside fence opened at line 989 (```markdown)]
L998: ### 7.6 Orca Orchestration: Commands as Workers  [outside]
L1002: #### How the pieces fit  [outside]
L1009: #### Rollout state  [outside]
L1015: #### Deciding whether a new command can be a worker  [outside]
L1022: #### What a command does under `--unattended`  [outside]
L1037: #### The worker session, not the command (WC-7)  [outside]
L1041: #### The `## Unattended mode` section of a converted command  [outside]
L1047: #### Skills and agents under a command  [outside]
L1056: ## 8. Development Workflow  [outside]
L1058: ### 8.1 Source of Truth  [outside]
L1071: ### 8.2 Sync Workflow  [outside]
L1076: # 1. Make your changes in src/superclaude/  [inside fence opened at line 1075 (```bash)]
L1077: # 2. Sync to .claude/  [inside fence opened at line 1075 (```bash)]
L1080: # 3. Verify sync succeeded  [inside fence opened at line 1075 (```bash)]
L1087: # 1. Copy changes back to src/superclaude/ manually  [inside fence opened at line 1086 (```bash)]
L1088: # 2. Verify both sides match  [inside fence opened at line 1086 (```bash)]
L1094: ### 8.3 Creating a New Component: Full Workflow  [outside]
L1097: # 1. Scaffold the component  [inside fence opened at line 1096 (```bash)]
L1098: #    Command:  [inside fence opened at line 1096 (```bash)]
L1101: #    Agent:  [inside fence opened at line 1096 (```bash)]
L1104: #    Skill (simple):  [inside fence opened at line 1096 (```bash)]
L1108: #    Skill (complex with refs):  [inside fence opened at line 1096 (```bash)]
L1113: # 2. Write the component (see templates in Section 10)  [inside fence opened at line 1096 (```bash)]
L1115: # 2a. Decide worker eligibility (WC-2, section 7.6)  [inside fence opened at line 1096 (```bash)]
L1116: #    If the command will accept --unattended, write its ## Unattended mode section  [inside fence opened at line 1096 (```bash)]
L1117: #    and add its name to UNATTENDED_COMMANDS in tests/skills/test_worker_contract.py  [inside fence opened at line 1096 (```bash)]
L1119: # 3. Sync to .claude/ for testing  [inside fence opened at line 1096 (```bash)]
L1122: # 4. Verify sync  [inside fence opened at line 1096 (```bash)]
L1125: # 5. Test in Claude Code  [inside fence opened at line 1096 (```bash)]
L1126: #    - Invoke the command/agent/skill  [inside fence opened at line 1096 (```bash)]
L1127: #    - Verify triggers activate correctly  [inside fence opened at line 1096 (```bash)]
L1128: #    - Validate output matches expected behavior  [inside fence opened at line 1096 (```bash)]
L1129: #    - Test edge cases and error conditions  [inside fence opened at line 1096 (```bash)]
L1131: # 6. Register the component (commands only)  [inside fence opened at line 1096 (```bash)]
L1132: #    Register it in src/superclaude/core/HOW-WE-WORK.md (a job row, or the Other commands table; see 3.6)  [inside fence opened at line 1096 (```bash)]
L1134: # 7. Commit  [inside fence opened at line 1096 (```bash)]
L1141: ### 8.4 Testing Components  [outside]
L1167: ### 8.5 Plugin Build Workflow (Future)  [outside]
L1172: # Build plugin artifacts  [inside fence opened at line 1171 (```bash)]
L1175: # Sync to plugin repository  [inside fence opened at line 1171 (```bash)]
L1183: ## 9. Best Practices  [outside]
L1185: ### 9.1 Command Design  [outside]
L1205: ### 9.2 Agent Design  [outside]
L1219: ### 9.3 Skill Design  [outside]
L1244: ### 9.4 Token Management  [outside]
L1257: ### 9.5 Error Handling  [outside]
L1262: ## Error Handling  [inside fence opened at line 1261 (```markdown)]
L1273: ### 9.6 Community Tips (from Research)  [outside]
L1291: ### 9.7 Anti-Patterns  [outside]
L1314: ## 10. Complete Examples  [outside]
L1316: ### Example 1: Simple Command + Agent (Beginner)  [outside]
L1332: # /sc:summary - Project Summary Generator  [inside fence opened at line 1322 (```markdown)]
L1334: ## Triggers  [inside fence opened at line 1322 (```markdown)]
L1338: ## Usage  [inside fence opened at line 1322 (```markdown)]
L1346: ## Options  [outside]
L1353: ## Behavioral Flow  [outside]
L1361: ## Examples  [outside]
L1369: ## Boundaries  [outside]
L1390: # Summary Reporter  [inside fence opened at line 1379 (```)]
L1392: ## Triggers  [inside fence opened at line 1379 (```)]
L1396: ## Behavioral Mindset  [inside fence opened at line 1379 (```)]
L1400: ## Tools  [inside fence opened at line 1379 (```)]
L1405: ## Outputs  [inside fence opened at line 1379 (```)]
L1412: ## Does NOT  [inside fence opened at line 1379 (```)]
L1417: ## Boundaries  [inside fence opened at line 1379 (```)]
L1429: ### Example 2: Medium Command + Skill with Compliance (Intermediate)  [outside]
L1445: # /sc:pr-review - Pull Request Review  [inside fence opened at line 1435 (```markdown)]
L1447: ## Triggers  [inside fence opened at line 1435 (```markdown)]
L1451: ## Usage  [inside fence opened at line 1435 (```markdown)]
L1459: ## Options  [outside]
L1467: ## Behavioral Flow  [outside]
L1478: ## MCP Integration  [outside]
L1482: ## Examples  [outside]
L1490: ## Boundaries  [outside]
L1519: # PR Review Skill  [inside fence opened at line 1501 (```)]
L1521: ## Purpose  [inside fence opened at line 1501 (```)]
L1525: ## Compliance Tier Classification  [inside fence opened at line 1501 (```)]
L1527: ### Auto-Detection  [inside fence opened at line 1501 (```)]
L1544: ### Tier Workflows  [inside fence opened at line 1501 (```)]
L1571: ## Output Format  [inside fence opened at line 1501 (```)]
L1574: # PR Review: <branch-name>  [inside fence opened at line 1501 (```)]
L1576: ## Classification  [inside fence opened at line 1501 (```)]
L1581: ## Findings  [inside fence opened at line 1501 (```)]
L1583: ### Critical (must fix)  [inside fence opened at line 1501 (```)]
L1586: ### Warning (should fix)  [inside fence opened at line 1501 (```)]
L1589: ### Info (consider)  [inside fence opened at line 1501 (```)]
L1592: ## Summary  [inside fence opened at line 1501 (```)]
L1596: ## Will Do  [outside]
L1601: ## Will Not Do  [outside]
L1609: ### Example 3: Complex Command + Skill + Agents with Refs (Advanced)  [inside fence opened at line 1605 (```)]
L1625: # /sc:adversarial - Adversarial Debate & Merge Pipeline  [inside fence opened at line 1605 (```)]
L1627: ## Required Input  [inside fence opened at line 1605 (```)]
L1631: ## Usage  [inside fence opened at line 1605 (```)]
L1634: # Mode A: Compare existing files  [inside fence opened at line 1605 (```)]
L1637: # Mode B: Generate variants from source + compare  [inside fence opened at line 1605 (```)]
L1641: ## Options  [outside]
L1654: ## Behavioral Summary  [outside]
L1663: ## Boundaries  [outside]
L1692: # Adversarial Debate & Merge Pipeline  [inside fence opened at line 1674 (```)]
L1694: ## Purpose  [inside fence opened at line 1674 (```)]
L1702: ## Input Contract  [inside fence opened at line 1674 (```)]
L1704: ### Mode A: Compare existing artifacts (STOP if invalid)  [inside fence opened at line 1674 (```)]
L1708: ### Mode B: Generate + compare (STOP if invalid)  [inside fence opened at line 1674 (```)]
L1714: ## 5-Step Protocol  [inside fence opened at line 1674 (```)]
L1716: ### Step 1: Diff Analysis  [inside fence opened at line 1674 (```)]
L1720: ### Step 2: Adversarial Debate  [inside fence opened at line 1674 (```)]
L1726: ### Step 3: Base Selection  [inside fence opened at line 1674 (```)]
L1733: ### Step 4: Refactoring Plan  [inside fence opened at line 1674 (```)]
L1737: ### Step 5: Merge Execution  [inside fence opened at line 1674 (```)]
L1742: ## Delegation Pattern  [inside fence opened at line 1674 (```)]
L1750: ## Return Contract  [inside fence opened at line 1674 (```)]
L1760: ## Error Handling  [inside fence opened at line 1674 (```)]
L1770: ## Output Collision Protocol  [inside fence opened at line 1674 (```)]
L1773: ## Will Do  [inside fence opened at line 1674 (```)]
L1778: ## Will Not Do  [inside fence opened at line 1674 (```)]
L1788: # Scoring Protocol Reference  [inside fence opened at line 1787 (```markdown)]
L1790: ## Hybrid Scoring Algorithm  [inside fence opened at line 1787 (```markdown)]
L1794: ### Quantitative Metrics (Deterministic)  [inside fence opened at line 1787 (```markdown)]
L1800: ### Qualitative Rubric (LLM with CEV Protocol)  [inside fence opened at line 1787 (```markdown)]
L1812: ### Position-Bias Mitigation  [inside fence opened at line 1787 (```markdown)]
L1819: ### Tiebreaker Protocol  [inside fence opened at line 1787 (```markdown)]
L1829: # Agent Specification Reference  [inside fence opened at line 1828 (```markdown)]
L1831: ## Agent Spec Format  [inside fence opened at line 1828 (```markdown)]
L1837: ### Examples  [inside fence opened at line 1835 (```)]
L1842: ## Advocate Prompt Template  [inside fence opened at line 1835 (```)]
L1858: ## Strengths (with evidence)  [outside]
L1859: ## Weaknesses (with mitigation)  [outside]
L1860: ## Unique Contributions  [outside]
L1861: ## Response to Opposing Arguments  [outside]
L1864: ## Advocate Output Format  [inside fence opened at line 1862 (```)]
L1869: ## Advocate Report: Variant {N}  [inside fence opened at line 1862 (```)]
L1871: ### Strengths  [inside fence opened at line 1862 (```)]
L1875: ### Weaknesses (with mitigation)  [inside fence opened at line 1862 (```)]
L1878: ### Unique Contributions  [inside fence opened at line 1862 (```)]
L1881: ### Response to Opposing Arguments  [inside fence opened at line 1862 (```)]
L1895: # Debate Orchestrator  [inside fence opened at line 1884 (```)]
L1897: ## Triggers  [inside fence opened at line 1884 (```)]
L1901: ## Behavioral Mindset  [inside fence opened at line 1884 (```)]
L1906: ## Model Preference  [inside fence opened at line 1884 (```)]
L1909: ## Tools  [inside fence opened at line 1884 (```)]
L1917: ## Responsibilities  [inside fence opened at line 1884 (```)]
L1927: ## Outputs  [inside fence opened at line 1884 (```)]
L1934: ## Does NOT  [inside fence opened at line 1884 (```)]
L1939: ## Boundaries  [inside fence opened at line 1884 (```)]
L1960: # Merge Executor  [inside fence opened at line 1953 (```markdown)]
L1962: ## Triggers  [inside fence opened at line 1953 (```markdown)]
L1966: ## Behavioral Mindset  [inside fence opened at line 1953 (```markdown)]
L1971: ## Tools  [inside fence opened at line 1953 (```markdown)]
L1976: ## Responsibilities  [inside fence opened at line 1953 (```markdown)]
L1985: ## Outputs  [inside fence opened at line 1953 (```markdown)]
L1989: ## Does NOT  [inside fence opened at line 1953 (```markdown)]
L1994: ## Boundaries  [inside fence opened at line 1953 (```markdown)]
L2008: ## Appendix A: SKILL.md Skeleton Template  [outside]
L2026: # <Skill Title>  [inside fence opened at line 2012 (```markdown)]
L2028: ## Purpose  [inside fence opened at line 2012 (```markdown)]
L2031: ## Input Contract  [inside fence opened at line 2012 (```markdown)]
L2033: ### Required Input (STOP if missing)  [inside fence opened at line 2012 (```markdown)]
L2036: ### Optional Input  [inside fence opened at line 2012 (```markdown)]
L2039: ## Protocol  [inside fence opened at line 2012 (```markdown)]
L2041: ### Step 1: <Name>  [inside fence opened at line 2012 (```markdown)]
L2045: ### Step 2: <Name>  [inside fence opened at line 2012 (```markdown)]
L2048: ## Delegation Pattern  [inside fence opened at line 2012 (```markdown)]
L2054: ## Return Contract  [inside fence opened at line 2012 (```markdown)]
L2061: ## Error Handling  [inside fence opened at line 2012 (```markdown)]
L2067: ## Will Do  [inside fence opened at line 2012 (```markdown)]
L2071: ## Will Not Do  [inside fence opened at line 2012 (```markdown)]
L2076: ## Appendix B: Command Template  [outside]
L2088: # /sc:<name> - <Title>  [inside fence opened at line 2078 (```markdown)]
L2090: ## Triggers  [inside fence opened at line 2078 (```markdown)]
L2094: ## Usage  [inside fence opened at line 2078 (```markdown)]
L2100: ## Options  [outside]
L2106: ## Behavioral Flow  [outside]
L2111: ## MCP Integration  [outside]
L2114: ## Examples  [outside]
L2121: ## Boundaries  [outside]
L2130: ## Appendix C: Agent Template  [inside fence opened at line 2128 (```)]
L2139: # <Agent Title>  [inside fence opened at line 2128 (```)]
L2141: ## Triggers  [inside fence opened at line 2128 (```)]
L2145: ## Behavioral Mindset  [inside fence opened at line 2128 (```)]
L2148: ## Model Preference  [inside fence opened at line 2128 (```)]
L2151: ## Tools  [inside fence opened at line 2128 (```)]
L2154: ## Responsibilities  [inside fence opened at line 2128 (```)]
L2158: ## Outputs  [inside fence opened at line 2128 (```)]
L2162: ## Does NOT  [inside fence opened at line 2128 (```)]
L2166: ## Boundaries  [inside fence opened at line 2128 (```)]
L2175: ## Appendix D: File Path Reference  [outside]
L2187: ## Appendix E: Glossary  [outside]
## Inner fence closes outer fence
outer fence opened at L136 (markdown); nested opening at L154; bare fence at L156 closes the OUTER fence
outer fence opened at L177 (); nested opening at L183; bare fence at L216 closes the OUTER fence
outer fence opened at L1322 (markdown); nested opening at L1340; bare fence at L1344 closes the OUTER fence
outer fence opened at L1379 (); nested opening at L1383; bare fence at L1425 closes the OUTER fence
outer fence opened at L1435 (markdown); nested opening at L1453; bare fence at L1457 closes the OUTER fence
outer fence opened at L1501 (); nested opening at L1573; bare fence at L1594 closes the OUTER fence
outer fence opened at L1605 (); nested opening at L1633; bare fence at L1639 closes the OUTER fence
outer fence opened at L1674 (); nested opening at L1678; bare fence at L1783 closes the OUTER fence
outer fence opened at L1862 (); nested opening at L1868; bare fence at L1883 closes the OUTER fence
outer fence opened at L1884 (); nested opening at L1888; bare fence at L1949 closes the OUTER fence
outer fence opened at L2078 (markdown); nested opening at L2096; bare fence at L2098 closes the OUTER fence
outer fence opened at L2128 (); nested opening at L2132; bare fence at L2173 closes the OUTER fence

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-fence-check.txt ===
# Fence state of docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
## Headings
L9: ## Table of Contents  [outside]
L25: ## 1. Introduction  [outside]
L27: ### What SuperClaude Is  [outside]
L39: ### The Three-Tier Architecture  [outside]
L61: ### The Activation Pattern  [outside]
L66: ## Activation  [inside fence opened at line 65 (```markdown)]
L77: ### Installation Locations  [outside]
L98: ### Path rules for primitives  [outside]
L117: ### Context Loading Sequence  [outside]
L130: ## 2. Quick Start  [outside]
L132: ### 2.1 Create a Minimal Command  [outside]
L146: # /sc:hello - Hello World Command  [inside fence opened at line 136 (```markdown)]
L148: ## Triggers  [inside fence opened at line 136 (```markdown)]
L152: ## Usage  [inside fence opened at line 136 (```markdown)]
L158: ## Behavioral Flow  [outside]
L162: ## Examples  [outside]
L169: ## Boundaries  [outside]
L179: ### 2.2 Create a Minimal Agent  [inside fence opened at line 177 (```)]
L190: # Greeter Agent  [inside fence opened at line 177 (```)]
L192: ## Triggers  [inside fence opened at line 177 (```)]
L196: ## Behavioral Mindset  [inside fence opened at line 177 (```)]
L200: ## Tools  [inside fence opened at line 177 (```)]
L204: ## Outputs  [inside fence opened at line 177 (```)]
L208: ## Boundaries  [inside fence opened at line 177 (```)]
L218: ### 2.3 Create a Minimal Skill  [outside]
L229: # Hello Skill  [inside fence opened at line 222 (```markdown)]
L231: ## Purpose  [inside fence opened at line 222 (```markdown)]
L234: ## Protocol  [inside fence opened at line 222 (```markdown)]
L240: ## Will Do  [inside fence opened at line 222 (```markdown)]
L244: ## Will Not Do  [inside fence opened at line 222 (```markdown)]
L249: ### 2.4 Sync and Test  [outside]
L252: # Copy new components from src/ to .claude/  [inside fence opened at line 251 (```bash)]
L255: # Verify sync succeeded  [inside fence opened at line 251 (```bash)]
L258: # Test the command in Claude Code  [inside fence opened at line 251 (```bash)]
L259: # Type: /sc:hello  [inside fence opened at line 251 (```bash)]
L264: ## 3. Commands Deep Dive  [outside]
L266: ### 3.1 Anatomy of a Command File  [outside]
L310: ### 3.2 Command Archetypes  [outside]
L314: #### Archetype 1: Analysis Pipeline  [outside]
L329: #### Archetype 2: Meta-Orchestrator  [outside]
L340: ## CRITICAL BOUNDARIES  [inside fence opened at line 339 (```)]
L346: #### Archetype 3: Unified Executor  [outside]
L363: ### 3.3 Command Processing Pipeline  [outside]
L375: ### 3.4 Performance Profiles  [outside]
L385: ### 3.5 Wave-Enabled Commands  [outside]
L389: ### 3.6 Registering a New Command  [outside]
L397: ## 4. Agents Deep Dive  [outside]
L399: ### 4.1 Anatomy of an Agent File  [outside]
L437: ### 4.2 Agent Patterns  [outside]
L443: #### Pattern 1: Constrained Worker  [outside]
L451: #### Pattern 2: Specialist Investigator  [outside]
L459: #### Pattern 3: Process Orchestrator  [outside]
L469: #### Pattern 4: Meta-Layer Agent  [outside]
L483: ### 4.3 Agent Spec Format (Dynamic Instantiation)  [outside]
L502: ### 4.4 Agent Activation Methods  [outside]
L514: ## 5. Skills Deep Dive  [outside]
L516: ### 5.1 Anatomy of a Skill  [outside]
L531: ### 5.2 SKILL.md Frontmatter  [outside]
L571: ### 5.3 Extended Metadata Comment  [outside]
L586: ### 5.4 Tool Allowlisting  [outside]
L602: ### 5.5 Skill Complexity Tiers  [outside]
L606: #### Tier 1: Simple (SKILL.md only)  [outside]
L626: #### Tier 2: Medium (SKILL.md + allowed-tools + compliance logic)  [outside]
L648: #### Tier 3: Complex (SKILL.md + refs/ + agents + multi-phase)  [outside]
L673: ### 5.6 The refs/ Pattern (Lazy Loading)  [outside]
L685: ## Wave 2: Analysis  [inside fence opened at line 684 (```markdown)]
L698: ### 5.7 The sc- Prefix Convention  [outside]
L710: ### 5.8 Machine-Readable Headers  [outside]
L726: ### 5.9 Input and Output Contracts  [outside]
L728: #### Input Contracts  [outside]
L733: ## Required Input (STOP if missing)  [inside fence opened at line 732 (```markdown)]
L735: ### Mode A: Compare existing artifacts  [inside fence opened at line 732 (```markdown)]
L738: ### Mode B: Generate variants from source  [inside fence opened at line 732 (```markdown)]
L747: #### Output / Return Contracts  [outside]
L752: ## Return Contract  [inside fence opened at line 751 (```markdown)]
L765: #### Worker contract (under `--unattended`)  [outside]
L774: ### 5.10 Skill-Authoring Checklist  [outside]
L802: ## 6. Multi-Phase Architecture  [outside]
L804: ### 6.1 Wave System  [outside]
L836: ### 6.2 Compliance Tiers  [outside]
L866: ### 6.3 Delegation Intelligence  [outside]
L888: ### 6.4 Resource Management Zones  [outside]
L902: ## 7. Integration Patterns  [outside]
L904: ### 7.1 Command + Skill + Agent Composition  [outside]
L930: ### 7.2 MCP Server Integration  [outside]
L950: ### 7.3 Persona Integration  [outside]
L975: ### 7.4 Thinking Depth Flags  [outside]
L985: ### 7.5 Dynamic Context Injection  [outside]
L990: ## Repository Context  [inside fence opened at line 989 (```markdown)]
L998: ### 7.6 Orca Orchestration: Commands as Workers  [outside]
L1002: #### How the pieces fit  [outside]
L1009: #### Rollout state  [outside]
L1015: #### Deciding whether a new command can be a worker  [outside]
L1022: #### What a command does under `--unattended`  [outside]
L1037: #### The worker session, not the command (WC-7)  [outside]
L1041: #### The `## Unattended mode` section of a converted command  [outside]
L1047: #### Skills and agents under a command  [outside]
L1056: ## 8. Development Workflow  [outside]
L1058: ### 8.1 Source of Truth  [outside]
L1071: ### 8.2 Sync Workflow  [outside]
L1076: # 1. Make your changes in src/superclaude/  [inside fence opened at line 1075 (```bash)]
L1077: # 2. Sync to .claude/  [inside fence opened at line 1075 (```bash)]
L1080: # 3. Verify sync succeeded  [inside fence opened at line 1075 (```bash)]
L1087: # 1. Copy changes back to src/superclaude/ manually  [inside fence opened at line 1086 (```bash)]
L1088: # 2. Verify both sides match  [inside fence opened at line 1086 (```bash)]
L1094: ### 8.3 Creating a New Component: Full Workflow  [outside]
L1097: # 1. Scaffold the component  [inside fence opened at line 1096 (```bash)]
L1098: #    Command:  [inside fence opened at line 1096 (```bash)]
L1101: #    Agent:  [inside fence opened at line 1096 (```bash)]
L1104: #    Skill (simple):  [inside fence opened at line 1096 (```bash)]
L1108: #    Skill (complex with refs):  [inside fence opened at line 1096 (```bash)]
L1113: # 2. Write the component (see templates in Section 10)  [inside fence opened at line 1096 (```bash)]
L1115: # 2a. Decide worker eligibility (WC-2, section 7.6)  [inside fence opened at line 1096 (```bash)]
L1116: #    If the command will accept --unattended, write its ## Unattended mode section  [inside fence opened at line 1096 (```bash)]
L1117: #    and add its name to UNATTENDED_COMMANDS in tests/skills/test_worker_contract.py  [inside fence opened at line 1096 (```bash)]
L1119: # 3. Sync to .claude/ for testing  [inside fence opened at line 1096 (```bash)]
L1122: # 4. Verify sync  [inside fence opened at line 1096 (```bash)]
L1125: # 5. Test in Claude Code  [inside fence opened at line 1096 (```bash)]
L1126: #    - Invoke the command/agent/skill  [inside fence opened at line 1096 (```bash)]
L1127: #    - Verify triggers activate correctly  [inside fence opened at line 1096 (```bash)]
L1128: #    - Validate output matches expected behavior  [inside fence opened at line 1096 (```bash)]
L1129: #    - Test edge cases and error conditions  [inside fence opened at line 1096 (```bash)]
L1131: # 6. Register the component (commands only)  [inside fence opened at line 1096 (```bash)]
L1132: #    Register it in src/superclaude/core/HOW-WE-WORK.md (a job row, or the Other commands table; see 3.6)  [inside fence opened at line 1096 (```bash)]
L1134: # 7. Commit  [inside fence opened at line 1096 (```bash)]
L1141: ### 8.4 Testing Components  [outside]
L1167: ### 8.5 Plugin Build Workflow (Future)  [outside]
L1172: # Build plugin artifacts  [inside fence opened at line 1171 (```bash)]
L1175: # Sync to plugin repository  [inside fence opened at line 1171 (```bash)]
L1183: ## 9. Best Practices  [outside]
L1185: ### 9.1 Command Design  [outside]
L1205: ### 9.2 Agent Design  [outside]
L1219: ### 9.3 Skill Design  [outside]
L1244: ### 9.4 Token Management  [outside]
L1257: ### 9.5 Error Handling  [outside]
L1262: ## Error Handling  [inside fence opened at line 1261 (```markdown)]
L1273: ### 9.6 Community Tips (from Research)  [outside]
L1291: ### 9.7 Anti-Patterns  [outside]
L1314: ## 10. Complete Examples  [outside]
L1316: ### Example 1: Simple Command + Agent (Beginner)  [outside]
L1332: # /sc:summary - Project Summary Generator  [inside fence opened at line 1322 (```markdown)]
L1334: ## Triggers  [inside fence opened at line 1322 (```markdown)]
L1338: ## Usage  [inside fence opened at line 1322 (```markdown)]
L1346: ## Options  [outside]
L1353: ## Behavioral Flow  [outside]
L1361: ## Examples  [outside]
L1369: ## Boundaries  [outside]
L1390: # Summary Reporter  [inside fence opened at line 1379 (```)]
L1392: ## Triggers  [inside fence opened at line 1379 (```)]
L1396: ## Behavioral Mindset  [inside fence opened at line 1379 (```)]
L1400: ## Tools  [inside fence opened at line 1379 (```)]
L1405: ## Outputs  [inside fence opened at line 1379 (```)]
L1412: ## Does NOT  [inside fence opened at line 1379 (```)]
L1417: ## Boundaries  [inside fence opened at line 1379 (```)]
L1429: ### Example 2: Medium Command + Skill with Compliance (Intermediate)  [outside]
L1445: # /sc:pr-review - Pull Request Review  [inside fence opened at line 1435 (```markdown)]
L1447: ## Triggers  [inside fence opened at line 1435 (```markdown)]
L1451: ## Usage  [inside fence opened at line 1435 (```markdown)]
L1459: ## Options  [outside]
L1467: ## Behavioral Flow  [outside]
L1478: ## MCP Integration  [outside]
L1482: ## Examples  [outside]
L1490: ## Boundaries  [outside]
L1519: # PR Review Skill  [inside fence opened at line 1501 (```)]
L1521: ## Purpose  [inside fence opened at line 1501 (```)]
L1525: ## Compliance Tier Classification  [inside fence opened at line 1501 (```)]
L1527: ### Auto-Detection  [inside fence opened at line 1501 (```)]
L1544: ### Tier Workflows  [inside fence opened at line 1501 (```)]
L1571: ## Output Format  [inside fence opened at line 1501 (```)]
L1574: # PR Review: <branch-name>  [inside fence opened at line 1501 (```)]
L1576: ## Classification  [inside fence opened at line 1501 (```)]
L1581: ## Findings  [inside fence opened at line 1501 (```)]
L1583: ### Critical (must fix)  [inside fence opened at line 1501 (```)]
L1586: ### Warning (should fix)  [inside fence opened at line 1501 (```)]
L1589: ### Info (consider)  [inside fence opened at line 1501 (```)]
L1592: ## Summary  [inside fence opened at line 1501 (```)]
L1596: ## Will Do  [outside]
L1601: ## Will Not Do  [outside]
L1609: ### Example 3: Complex Command + Skill + Agents with Refs (Advanced)  [inside fence opened at line 1605 (```)]
L1625: # /sc:adversarial - Adversarial Debate & Merge Pipeline  [inside fence opened at line 1605 (```)]
L1627: ## Required Input  [inside fence opened at line 1605 (```)]
L1631: ## Usage  [inside fence opened at line 1605 (```)]
L1634: # Mode A: Compare existing files  [inside fence opened at line 1605 (```)]
L1637: # Mode B: Generate variants from source + compare  [inside fence opened at line 1605 (```)]
L1641: ## Options  [outside]
L1654: ## Behavioral Summary  [outside]
L1663: ## Boundaries  [outside]
L1692: # Adversarial Debate & Merge Pipeline  [inside fence opened at line 1674 (```)]
L1694: ## Purpose  [inside fence opened at line 1674 (```)]
L1702: ## Input Contract  [inside fence opened at line 1674 (```)]
L1704: ### Mode A: Compare existing artifacts (STOP if invalid)  [inside fence opened at line 1674 (```)]
L1708: ### Mode B: Generate + compare (STOP if invalid)  [inside fence opened at line 1674 (```)]
L1714: ## 5-Step Protocol  [inside fence opened at line 1674 (```)]
L1716: ### Step 1: Diff Analysis  [inside fence opened at line 1674 (```)]
L1720: ### Step 2: Adversarial Debate  [inside fence opened at line 1674 (```)]
L1726: ### Step 3: Base Selection  [inside fence opened at line 1674 (```)]
L1733: ### Step 4: Refactoring Plan  [inside fence opened at line 1674 (```)]
L1737: ### Step 5: Merge Execution  [inside fence opened at line 1674 (```)]
L1742: ## Delegation Pattern  [inside fence opened at line 1674 (```)]
L1750: ## Return Contract  [inside fence opened at line 1674 (```)]
L1760: ## Error Handling  [inside fence opened at line 1674 (```)]
L1770: ## Output Collision Protocol  [inside fence opened at line 1674 (```)]
L1773: ## Will Do  [inside fence opened at line 1674 (```)]
L1778: ## Will Not Do  [inside fence opened at line 1674 (```)]
L1788: # Scoring Protocol Reference  [inside fence opened at line 1787 (```markdown)]
L1790: ## Hybrid Scoring Algorithm  [inside fence opened at line 1787 (```markdown)]
L1794: ### Quantitative Metrics (Deterministic)  [inside fence opened at line 1787 (```markdown)]
L1800: ### Qualitative Rubric (LLM with CEV Protocol)  [inside fence opened at line 1787 (```markdown)]
L1812: ### Position-Bias Mitigation  [inside fence opened at line 1787 (```markdown)]
L1819: ### Tiebreaker Protocol  [inside fence opened at line 1787 (```markdown)]
L1829: # Agent Specification Reference  [inside fence opened at line 1828 (```markdown)]
L1831: ## Agent Spec Format  [inside fence opened at line 1828 (```markdown)]
L1837: ### Examples  [inside fence opened at line 1835 (```)]
L1842: ## Advocate Prompt Template  [inside fence opened at line 1835 (```)]
L1858: ## Strengths (with evidence)  [outside]
L1859: ## Weaknesses (with mitigation)  [outside]
L1860: ## Unique Contributions  [outside]
L1861: ## Response to Opposing Arguments  [outside]
L1864: ## Advocate Output Format  [inside fence opened at line 1862 (```)]
L1869: ## Advocate Report: Variant {N}  [inside fence opened at line 1862 (```)]
L1871: ### Strengths  [inside fence opened at line 1862 (```)]
L1875: ### Weaknesses (with mitigation)  [inside fence opened at line 1862 (```)]
L1878: ### Unique Contributions  [inside fence opened at line 1862 (```)]
L1881: ### Response to Opposing Arguments  [inside fence opened at line 1862 (```)]
L1895: # Debate Orchestrator  [inside fence opened at line 1884 (```)]
L1897: ## Triggers  [inside fence opened at line 1884 (```)]
L1901: ## Behavioral Mindset  [inside fence opened at line 1884 (```)]
L1906: ## Model Preference  [inside fence opened at line 1884 (```)]
L1909: ## Tools  [inside fence opened at line 1884 (```)]
L1917: ## Responsibilities  [inside fence opened at line 1884 (```)]
L1927: ## Outputs  [inside fence opened at line 1884 (```)]
L1934: ## Does NOT  [inside fence opened at line 1884 (```)]
L1939: ## Boundaries  [inside fence opened at line 1884 (```)]
L1960: # Merge Executor  [inside fence opened at line 1953 (```markdown)]
L1962: ## Triggers  [inside fence opened at line 1953 (```markdown)]
L1966: ## Behavioral Mindset  [inside fence opened at line 1953 (```markdown)]
L1971: ## Tools  [inside fence opened at line 1953 (```markdown)]
L1976: ## Responsibilities  [inside fence opened at line 1953 (```markdown)]
L1985: ## Outputs  [inside fence opened at line 1953 (```markdown)]
L1989: ## Does NOT  [inside fence opened at line 1953 (```markdown)]
L1994: ## Boundaries  [inside fence opened at line 1953 (```markdown)]
L2008: ## Appendix A: SKILL.md Skeleton Template  [outside]
L2026: # <Skill Title>  [inside fence opened at line 2012 (```markdown)]
L2028: ## Purpose  [inside fence opened at line 2012 (```markdown)]
L2031: ## Input Contract  [inside fence opened at line 2012 (```markdown)]
L2033: ### Required Input (STOP if missing)  [inside fence opened at line 2012 (```markdown)]
L2036: ### Optional Input  [inside fence opened at line 2012 (```markdown)]
L2039: ## Protocol  [inside fence opened at line 2012 (```markdown)]
L2043: ### Step 1: <Name>  [inside fence opened at line 2012 (```markdown)]
L2047: ### Step 2: <Name>  [inside fence opened at line 2012 (```markdown)]
L2050: ## Delegation Pattern  [inside fence opened at line 2012 (```markdown)]
L2056: ## Return Contract  [inside fence opened at line 2012 (```markdown)]
L2065: ## Error Handling  [inside fence opened at line 2012 (```markdown)]
L2071: ## Will Do  [inside fence opened at line 2012 (```markdown)]
L2075: ## Will Not Do  [inside fence opened at line 2012 (```markdown)]
L2080: ## Appendix B: Command Template  [outside]
L2092: # /sc:<name> - <Title>  [inside fence opened at line 2082 (````markdown)]
L2094: ## Triggers  [inside fence opened at line 2082 (````markdown)]
L2098: ## Usage  [inside fence opened at line 2082 (````markdown)]
L2104: ## Options  [inside fence opened at line 2082 (````markdown)]
L2112: ## Behavioral Flow  [inside fence opened at line 2082 (````markdown)]
L2117: ## MCP Integration  [inside fence opened at line 2082 (````markdown)]
L2120: ## Examples  [inside fence opened at line 2082 (````markdown)]
L2127: ## Unattended mode  [inside fence opened at line 2082 (````markdown)]
L2139: ## Boundaries  [inside fence opened at line 2082 (````markdown)]
L2148: ## Appendix C: Agent Template  [outside]
L2157: # <Agent Title>  [inside fence opened at line 2150 (```markdown)]
L2159: ## Triggers  [inside fence opened at line 2150 (```markdown)]
L2163: ## Behavioral Mindset  [inside fence opened at line 2150 (```markdown)]
L2166: ## Model Preference  [inside fence opened at line 2150 (```markdown)]
L2169: ## Tools  [inside fence opened at line 2150 (```markdown)]
L2172: ## Responsibilities  [inside fence opened at line 2150 (```markdown)]
L2176: ## Outputs  [inside fence opened at line 2150 (```markdown)]
L2180: ## Does NOT  [inside fence opened at line 2150 (```markdown)]
L2184: ## Boundaries  [inside fence opened at line 2150 (```markdown)]
L2193: ## Appendix D: File Path Reference  [outside]
L2205: ## Appendix E: Glossary  [outside]
## Inner fence closes outer fence
outer fence opened at L136 (markdown); nested opening at L154; bare fence at L156 closes the OUTER fence
outer fence opened at L177 (); nested opening at L183; bare fence at L216 closes the OUTER fence
outer fence opened at L1322 (markdown); nested opening at L1340; bare fence at L1344 closes the OUTER fence
outer fence opened at L1379 (); nested opening at L1383; bare fence at L1425 closes the OUTER fence
outer fence opened at L1435 (markdown); nested opening at L1453; bare fence at L1457 closes the OUTER fence
outer fence opened at L1501 (); nested opening at L1573; bare fence at L1594 closes the OUTER fence
outer fence opened at L1605 (); nested opening at L1633; bare fence at L1639 closes the OUTER fence
outer fence opened at L1674 (); nested opening at L1678; bare fence at L1783 closes the OUTER fence
outer fence opened at L1862 (); nested opening at L1868; bare fence at L1883 closes the OUTER fence
outer fence opened at L1884 (); nested opening at L1888; bare fence at L1949 closes the OUTER fence

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-stale-fences.txt ===
# Nested-fence spots outside Appendix B (reported, not fixed; out of scope per the plan)
# Source: ./artifacts/t8-fence-check.txt ("Inner fence closes outer fence" section), guide line numbers as of the end of Task 8.
# In each spot a three-backtick outer template fence holds a three-backtick inner block; the inner block's bare closing fence closes the outer fence instead, and the template's own closing fence then opens a new, unlabelled fence that swallows the text after it.

guide lines 136-156, then 177-216 (2.1 Quick Start, "Create a Minimal Command"): the command template's ```markdown fence (line 136) is closed at line 156 by the inner Usage block (opened line 154); the template's closing fence at line 177 then opens a fence that swallows the "### 2.2 Create a Minimal Agent" heading (line 179) and the agent template's headings until line 216.
guide lines 1322-1344, then 1379-1425 (section 10, Example 1 command file): ```markdown fence (line 1322) closed at line 1344 by the inner block opened at line 1340; the fence from line 1379 swallows the agent file's headings (lines 1392-1417) until line 1425.
guide lines 1435-1457, then 1501-1594 (section 10, Example 2 command file): ```markdown fence (line 1435) closed at line 1457 by the inner block opened at line 1453; the fence from line 1501 swallows the skill file's headings (lines 1521-1583) until line 1594.
guide lines 1605-1639 (section 10, Example 2 after "## Will Not Do"): fence from line 1605 closed at line 1639 by the inner block opened at line 1633.
guide lines 1674-1783 (section 10, Example 3 after "## Boundaries"): fence from line 1674 closed at line 1783 by the inner block opened at line 1678.
guide lines 1862-1883 and 1884-1949 (section 10, Example 3 advocate prompt, "Response to Opposing Arguments"): fence from line 1862 closed at line 1883 by the inner block opened at line 1868; a new fence from line 1884 is closed at line 1949 by the inner block opened at line 1888.

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-changed-files.txt ===
$ git diff HEAD --name-only
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/TASK-WF-writeTheP0LivePl-20261103-215902.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/ac-0.5.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/ac-0.6.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/head-final.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-branch-after.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-branch.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-brief.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-checks.log
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-head-after.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-index-after.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-remove.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-report/REPORT.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-result.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-session-analysis-hb.py
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-session-analysis.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-status-after.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-status-before.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-step1.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-step2-samples.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-step3-ack.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-step3.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-step4.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-step5.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-step6.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-step7.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-sync-dev.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-task-create.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-transcript-1.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-transcript-2.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-transcript-after-release.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-transcript-limit1000.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-unattended-check.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-worker-start.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-worktree-list-after.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc1-worktree.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-branch-after.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-branch.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-brief.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-checks.log
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-head-after.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-index-after.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-remove.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-report/TASK-WF-addOneSentenceTo-20261104-070008.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-report/return-contract.yaml
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-result.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-session-analysis.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-status-after.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-status-before.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-step1.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-step2-samples.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-step3-ack.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-step3.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-step4.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-step5.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-step6.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-step7.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-sync-dev.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-task-create.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-todo-after.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-todo-before.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-transcript-1.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-transcript-2.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-unattended-check.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-worker-start.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-worktree-list-after.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc2-worktree.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-branch-after.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-branch.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-brief.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-checks.log
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-head-after.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-index-after.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-inputs-sha-after.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-inputs-sha-before.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-remove.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-report-dir-files.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-report/merge-log.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-result.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-session-analysis.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-status-after.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-status-before.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-step1.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-step2-samples.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-step3-ack.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-step3.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-step4.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-step5.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-step6.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-step7.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-sync-dev.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-task-create.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-transcript-1.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-transcript-2.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-unattended-check.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-worker-start.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-worktree-list-after.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/lc3-worktree.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/live-run.json
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/orca-help.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/p0-phase-report.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/preflight.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/retries/T1/prompt-1-1.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/retries/T1/q0-head
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/retries/T2/notes.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/retries/T2/prompt-2-1.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/retries/T2/q0-head
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/retries/T3/prompt-3-1.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/retries/T3/q0-head
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/retries/T4/prompt-4-1.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/retries/T4/q0-head
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/retries/T5/prompt-5-1.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/retries/T5/q0-head
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/session-analysis.py
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/session-hbcover.py
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/staged.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/status-baseline.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/status-end-t1.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/symptom-check.txt
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/progress.md
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/return-contract.yaml
.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/source.md
.dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-124528/TASK-WF-devGuideRefactor-20261104-124528.md
.dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-124528/return-contract.yaml
.dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-124528/source.md
.dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/TASK-WF-devGuideRefactor-20261104-135403.md
.dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/return-contract.yaml
.dev/tasks/to-do/TASK-WF-devGuideRefactor-20261104-135403/source.md
.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md
.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/return-contract.yaml
.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md
.dev/tasks/to-do/TASK-WF-refactorDocsDeve-20261104-062532/TASK-WF-refactorDocsDeve-20261104-062532.md
.dev/tasks/to-do/TASK-WF-refactorDocsDeve-20261104-062532/return-contract.yaml
.dev/tasks/to-do/TASK-WF-refactorDocsDeve-20261104-062532/source.md
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
